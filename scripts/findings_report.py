#!/usr/bin/env python3
"""Findings report: every number that appears in output/findings.html.

Companion to facet_report.py, which reports the distributions. This script asks
the next question — which of the differences in those distributions are large
enough, and stable enough, to say anything about. It reads only what the
pipeline already wrote (output/papers/ and output/papers/agents/), makes no API
calls, and can be re-run freely.

Three things it does that facet_report.py does not:

  1. Screens each claim with a two-sided Fisher exact test. scipy is not in the
     venv, so the test is implemented here from log-gammas.
  2. Reports every association twice — with and without `not_stated`. Three
     papers are silent on nearly every facet, and with them included they
     manufacture correlations between facets that are otherwise independent.
  3. Compares the two VULCA-BENCH papers field by field. They describe one
     benchmark, so the pipeline read the same object twice: the only external
     reliability estimate this corpus contains.

    python scripts/findings_report.py
"""

import collections
import itertools
import json
import math
import re
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import AGENTS_DIR, PAPERS_DIR
from src.fields import FACET_FIELDS, RESULT_FIELDS

# The two arXiv ids that describe the same benchmark. See §"reliability" below.
VULCA_IDS = ("2601.07984", "2601.07986")


# --------------------------------------------------------------------------
# loading
# --------------------------------------------------------------------------

def load_corpus() -> list[dict]:
    corpus = []
    for jf in sorted(PAPERS_DIR.glob("*.json")):
        final = json.loads(jf.read_text(encoding="utf-8"))
        if not any(f in final for f in FACET_FIELDS):
            continue
        stem = jf.stem
        ciop_p = AGENTS_DIR / f"{stem}.ciop.json"
        cip_p = AGENTS_DIR / f"{stem}.cip.json"
        final["_name"] = final.get("benchmark_name") or final.get("paper_name") or stem
        final["_ciop"] = json.loads(ciop_p.read_text(encoding="utf-8")) if ciop_p.exists() else {}
        final["_cip"] = json.loads(cip_p.read_text(encoding="utf-8")) if cip_p.exists() else {}
        corpus.append(final)
    return corpus


def is_gp(r: dict) -> bool:
    """general_purpose_benchmark, tolerating a criterion the model wrote flat."""
    v = (r.get("inclusion_criteria") or {}).get("general_purpose_benchmark")
    return bool(v.get("met")) if isinstance(v, dict) else bool(v)


def section(title: str) -> None:
    print(f"\n{'=' * 78}\n{title}\n{'=' * 78}")


# --------------------------------------------------------------------------
# statistics
# --------------------------------------------------------------------------

def fisher_exact(a: int, b: int, c: int, d: int) -> float:
    """Two-sided Fisher exact p for [[a, b], [c, d]], by summing tables no more
    likely than the observed one. Written out because scipy is not a dependency
    of this project and adding one for a single test is not worth it."""
    lf = lambda n: math.lgamma(n + 1)
    n = a + b + c + d
    if n == 0:
        return float("nan")

    def prob(x: int) -> float:
        y, z, w = a + b - x, a + c - x, d - (x - a)
        if min(y, z, w) < 0:
            return 0.0
        return math.exp(lf(a + b) + lf(c + d) + lf(a + c) + lf(b + d)
                        - lf(n) - lf(x) - lf(y) - lf(z) - lf(w))

    observed = prob(a)
    total = sum(p for x in range(min(a + b, a + c) + 1)
                if (p := prob(x)) <= observed * (1 + 1e-9))
    return min(1.0, total)


def claim(label: str, rows: list[dict], predicate, outcome) -> dict:
    """One 2x2 screen: how often `outcome` holds inside vs outside `predicate`."""
    a = sum(1 for r in rows if predicate(r) and outcome(r))
    b = sum(1 for r in rows if predicate(r) and not outcome(r))
    c = sum(1 for r in rows if not predicate(r) and outcome(r))
    d = sum(1 for r in rows if not predicate(r) and not outcome(r))
    p_in = a / (a + b) if a + b else float("nan")
    p_out = c / (c + d) if c + d else float("nan")
    p = fisher_exact(a, b, c, d)
    mark = "  <-- p<.05" if p < 0.05 else ""
    print(f"  {label:52} {a:2}/{a + b:<2} ({p_in:4.0%})  vs {c:2}/{c + d:<2} ({p_out:4.0%})"
          f"   d={p_in - p_out:+4.0%}  p={p:.3f}{mark}")
    return {"label": label, "a": a, "b": b, "c": c, "d": d, "p": p}


def cramers_v(rows: list[dict], f1: str, f2: str) -> tuple[float, int]:
    rows = [r for r in rows if r.get(f1) and r.get(f2)]
    n = len(rows)
    tab = collections.Counter((r[f1], r[f2]) for r in rows)
    rs = collections.Counter(r[f1] for r in rows)
    cs = collections.Counter(r[f2] for r in rows)
    if n == 0 or min(len(rs), len(cs)) < 2:
        return float("nan"), n
    chi = sum((tab[(x, y)] - rs[x] * cs[y] / n) ** 2 / (rs[x] * cs[y] / n)
              for x in rs for y in cs)
    return math.sqrt(chi / (n * (min(len(rs), len(cs)) - 1))), n


# --------------------------------------------------------------------------
# predicates shared across sections
# --------------------------------------------------------------------------

SINGLE = lambda r: r.get("answer_multiplicity") == "single_answer"
BEYOND = lambda r: r.get("gold_beyond_stimulus") == "yes"
EXPERT = lambda r: r.get("gold_source") in ("domain_expert", "existing_metadata")
NOISE = lambda r: r.get("plurality_treatment") == "noise"
SILENT = lambda r: r.get("plurality_treatment") == "not_stated"
IMAGE = lambda r: "image" in (r.get("benchmark_modalities") or [])


# --------------------------------------------------------------------------
# post-hoc coding of the gap kind
# --------------------------------------------------------------------------
# reported_format_gap turned out to be broader than its name: the extraction
# accepted any "same models, same material, different regime" comparison, and
# the 21 hits are four different phenomena. Only the first three change the
# MEASURING INSTRUMENT while holding the task fixed -- those are the ones that
# bear on the survey's argument. The other two vary the items or what the model
# is shown, which is a finding about models, not about benchmark construction.
#
# This mapping is a MANUAL reading of each paper's results_explanation, done
# after extraction. It is not a pipeline field and no agent produced it: it is
# reported here so the split is inspectable and arguable, exactly like the
# derived clusters in METHODOLOGY_facets.md §5. Keys are paper_id.
GAP_KIND: dict[str, str] = {
    # scoring strictness: identical model output, stricter matching rule
    "2604.07338": "scoring",   # Appear2Meaning: partial vs exact match
    "2510.00041": "scoring",   # C3B: ACC vs partial-credit CACC
    "2504.07199": "scoring",   # LLMs4Subjects: relaxed vs strict matching
    "2601.20975": "scoring",   # DeepSearchQA: F1 vs "fully correct"
    # answer format: closed vs open answer on the same items
    "2607.02007": "format",    # EduArt: multiple choice vs open completion
    "2410.02677": "format",    # CulturalBench: multiple choice vs binary T/F
    "2603.03884": "format",    # CzechTopic: matching vs tagging
    # depth tier: surface vs interpretation layer of the paper's own taxonomy
    "2601.07986": "depth",     # VULCA-BENCH: L1-L2 vs L3-L5
    "2601.07984": "depth",     # VULCA-BENCH: Coverage vs Depth
    # item difficulty: a harder SUBSET of items, not a different measurement
    "2604.19262": "difficulty",  # CulturALL: Easy vs Hard split
    "2305.14251": "difficulty",  # FActScore: common vs rare entities
    "2505.20246": "difficulty",  # HistBench: GAIA Level 1 vs Level 3
    "2502.14739": "difficulty",  # SuperGPQA: Easy vs Hard split
    "Finding_the_Plea:_Evaluating_the_Ability": "difficulty",
    # input representation: what the model is shown, or the pipeline around it
    "2503.15358": "input",     # AdMIRe: text+image vs text-only
    "Hanfu-Bench:_A_Multimodal_Benchmark_on_C": "input",  # single vs multi image
    "2409.02813": "input",     # MMMU-Pro: standard vs vision-only
    "Text_Is_Not_All_You_Need:_Multimodal_Pro": "input",  # audio ablation
    "Evaluating_LLMs_for_Historical_Document_": "input",  # full-page vs window
    "2603.08655": "input",     # OfficeQA Pro: parsed text vs raw PDF
    "2509.18839": "input",     # Christian Iconography: prompt enrichment
}

# The kinds that change the measuring instrument while the task stays fixed.
INSTRUMENT_KINDS = ("scoring", "format", "depth")

KIND_LABEL = {
    "scoring": "scoring strictness (same output, stricter rule)",
    "format":  "answer format (closed vs open)",
    "depth":   "depth tier (surface vs interpretation)",
    "difficulty": "item difficulty (a harder subset)",
    "input":   "input representation (what the model is shown)",
}


# Seven families over the 22-term closed vocabulary in src/fields.py. Like
# GAP_KIND this is a post-hoc grouping, not a pipeline field: the 22 terms are
# extracted and validated, the families are one way of reading them. Families
# overlap on purpose — a benchmark that asks for both OCR and interpretation
# belongs to both — so the counts do not sum to 42.
TASK_FAMILIES: dict[str, tuple[str, ...]] = {
    "Conoscenza dichiarativa": ("factual_recall", "multiple_choice_qa",
                                "fact_verification", "open_ended_qa"),
    "Lettura culturale":       ("cultural_reasoning", "interpretation",
                                "normative_judgment", "stylistic_analysis"),
    "Lingua":                  ("translation", "generation", "sequence_prediction"),
    "Ragionamento":            ("logical_and_quantitative_reasoning",
                                "causal_and_temporal_reasoning",
                                "calibration_and_uncertainty"),
    "Lavoro sul documento":    ("transcription_and_correction", "information_extraction",
                                "classification", "retrieval_and_ranking", "attribution"),
    "Visione":                 ("visual_recognition", "visual_reasoning"),
    "Agentico":                ("agentic_tool_use",),
}


def best_accuracy(r: dict) -> float | None:
    """Headline accuracy on a common 0-100 scale, or None.

    Two papers report accuracy on a 0-1 scale (VQArt-Bench 0.71, AdMIRe 0.93);
    their own results_explanation glosses the first as "(71%)". Same metric,
    different scale, so they are multiplied up rather than dropped.
    """
    if r.get("reported_best_metric") != "accuracy":
        return None
    v = r.get("reported_best_score")
    if v is None:
        return None
    return v * 100 if v <= 1 else v


# --------------------------------------------------------------------------
# 1. the five findings
# --------------------------------------------------------------------------

def corpus_map(corpus: list[dict]) -> None:
    section("(0) THE MAP -- what this corpus is, before any claim about it")
    n = len(corpus)

    print(f"  {n} benchmarks\n")
    print("  by year")
    for y, k in sorted(collections.Counter(
            r.get("publication_year") for r in corpus).items()):
        print(f"    {y}  {k:2}  {'#' * (k * 2)}")

    print("\n  what the model is shown")
    for combo, k in collections.Counter(
            tuple(sorted(r.get("benchmark_modalities") or [])) for r in corpus).most_common():
        print(f"    {'+'.join(combo):24} {k:2}")

    sizes = sorted(r["dataset_size"] for r in corpus if r.get("dataset_size"))
    print(f"\n  size (n={len(sizes)} declared, {n - len(sizes)} not stated)")
    print(f"    median {statistics.median(sizes):,.0f}   min {min(sizes):,}   max {max(sizes):,}")
    for label, lo, hi in (("under 1k", 0, 1000), ("1k-10k", 1000, 10000),
                          ("10k-100k", 10000, 100000), ("over 100k", 100000, 10**9)):
        print(f"    {label:12} {sum(1 for x in sizes if lo <= x < hi):2}")

    print("\n  what they ask the model to do (families overlap; see TASK_FAMILIES)")
    for fam, terms in sorted(TASK_FAMILIES.items(),
                             key=lambda kv: -sum(1 for r in corpus
                                                 if set(kv[1]) & set(r.get("analytical_tasks") or []))):
        rows = [r for r in corpus if set(terms) & set(r.get("analytical_tasks") or [])]
        img = sum(1 for r in rows if "image" in (r.get("benchmark_modalities") or []))
        print(f"    {fam:26} {len(rows):2}/{n}   multimodal {img:2}   {'#' * len(rows)}")
    per = sorted(len(r.get("analytical_tasks") or []) for r in corpus)
    print(f"    tasks per benchmark: median {statistics.median(per):.0f}, range {min(per)}-{max(per)}")

    print("\n  the headline metric")
    for m, k in collections.Counter(r.get("reported_best_metric") for r in corpus).most_common():
        print(f"    {str(m):16} {k:2}")

    print("\n  evaluation setting")
    for st, k in collections.Counter(r.get("primary_evaluation_setting") for r in corpus).most_common():
        print(f"    {str(st):16} {k:2}")

    print("\n  which models get evaluated (mentions in the inclusion-criteria notes)")
    # \b alone will not do: "GPT-4" is a prefix of "GPT-4o", so a plain
    # substring or \b match credits every GPT-4o paper to GPT-4 as well.
    fams = {
        "Gemini": r"Gemini", "Claude": r"Claude", "Llama": r"Llama",
        "Qwen": r"Qwen", "DeepSeek": r"DeepSeek", "Mistral": r"Mistral|Mixtral",
        "GPT-4o": r"GPT-4o", "GPT-4 (non-o)": r"GPT-4(?!o)(?![.\d])",
        "GPT-5": r"GPT-5", "o1 / o3 / o4": r"\bo[134]\b",
    }
    counts = collections.Counter()
    for r in corpus:
        note = ((r.get("inclusion_criteria") or {}).get("evaluates_generative_llm") or {}).get("note", "")
        for f, pat in fams.items():
            if re.search(pat, note):
                counts[f] += 1
    for f, k in counts.most_common():
        print(f"    {f:14} {k:2}/{n}   {'#' * k}")

    print("\n  ...rolled up to the provider, which is the number that matters")
    providers = {
        "OpenAI": r"GPT-|\bo[134]\b|ChatGPT|DALL", "Google": r"Gemini|PaLM|Gemma",
        "Anthropic": r"Claude", "Meta": r"Llama", "Alibaba": r"Qwen",
        "DeepSeek": r"DeepSeek", "Mistral": r"Mistral|Mixtral|Pixtral",
    }
    prov = collections.Counter()
    for r in corpus:
        note = ((r.get("inclusion_criteria") or {}).get("evaluates_generative_llm") or {}).get("note", "")
        for name, pat in providers.items():
            if re.search(pat, note):
                prov[name] += 1
    for name, k in prov.most_common():
        print(f"    {name:14} {k:2}/{n}  ({k / n:3.0%})  {'#' * k}")

    print("\n  how well the best model does -- accuracy only, so the numbers are comparable")
    scored = sorted(((best_accuracy(r), r["_name"]) for r in corpus
                     if best_accuracy(r) is not None), reverse=True)
    print(f"    n={len(scored)} of {n}; the rest report f1, bleu, cer, a bespoke metric, or no single figure")
    for v, name in scored:
        print(f"    {str(name)[:42]:44} {v:5.1f}  {'#' * int(v / 2)}")
    vals = [v for v, _ in scored]
    print(f"    median {statistics.median(vals):.1f}   range {min(vals):.1f}-{max(vals):.1f}")

    print("\n  role of the humanities material")
    for role, k in collections.Counter(r.get("humanities_role") for r in corpus).most_common():
        print(f"    {str(role):10} {k:2}")


def finding_1_format_gap(corpus: list[dict]) -> None:
    section("(1) THE MEASURING INSTRUMENT DECIDES THE SCORE  -- results axis")
    have = [r for r in corpus if r.get("reported_format_gap")]
    if not have:
        print("  results axis not extracted yet -- run --step analyze first")
        return
    counts = collections.Counter(r["reported_format_gap"] for r in have)
    print(f"  reported_format_gap over n={len(have)}: {dict(counts)}")
    print("  NB 'no' means the paper evaluates one regime throughout -- NOT that it")
    print("     compared two and found them equal. A null result would rarely be")
    print("     published, so every count below is a lower bound.")

    hits = [r for r in have if r.get("reported_format_gap") == "yes"
            and r.get("reported_format_gap_points")]
    uncoded = [r["paper_id"] for r in hits if r["paper_id"] not in GAP_KIND]
    if uncoded:
        print(f"\n  WARNING: {len(uncoded)} gaps have no GAP_KIND entry: {uncoded}")

    print(f"\n  the {len(hits)} reported gaps, split by what actually varied")
    print("  (manual post-hoc coding -- see GAP_KIND in this file):")
    for kind in ("scoring", "format", "depth", "difficulty", "input"):
        rows = [r for r in hits if GAP_KIND.get(r["paper_id"]) == kind]
        if not rows:
            continue
        tag = "  <- instrument" if kind in INSTRUMENT_KINDS else ""
        print(f"\n    {KIND_LABEL[kind]}  (n={len(rows)}){tag}")
        for r in sorted(rows, key=lambda x: -x["reported_format_gap_points"]):
            pts = r["reported_format_gap_points"]
            print(f"      {str(r['_name'])[:42]:44} {pts:3} pts  {'#' * min(44, int(pts / 2))}")

    inst = [r for r in hits if GAP_KIND.get(r["paper_id"]) in INSTRUMENT_KINDS]
    other = [r for r in hits if GAP_KIND.get(r["paper_id"]) not in INSTRUMENT_KINDS]
    for label, rows in (("instrument changed", inst), ("items or input changed", other)):
        if rows:
            pts = sorted(r["reported_format_gap_points"] for r in rows)
            print(f"\n  {label:24} n={len(rows):2}  median {statistics.median(pts):.0f} pts"
                  f"  range {min(pts)}-{max(pts)}")
    print(f"\n  Of the {len(inst)} benchmarks that measured the same material two ways,")
    print(f"  {len(inst)} report a gap. None reports 'no difference'.")

    print()
    claim("reports ANY gap | general-purpose", have, is_gp,
          lambda r: r["reported_format_gap"] == "yes")
    claim("reports an INSTRUMENT gap | single_answer", have, SINGLE,
          lambda r: GAP_KIND.get(r["paper_id"]) in INSTRUMENT_KINDS)

    n = len(have)
    hb_yes = sum(1 for r in have if r.get("human_baseline_reported") == "yes")
    hb = [r for r in have if r.get("human_gap_points") is not None]
    print(f"\n  human baseline reported: {hb_yes}/{n}; gap quantified for {len(hb)}")
    for r in sorted(hb, key=lambda x: -(x["human_gap_points"] or 0)):
        g = r["human_gap_points"]
        who = "human leads" if g > 0 else "MODEL leads"
        print(f"    {str(r['_name'])[:42]:44} {who} by {abs(g):3} pts")

    ca = collections.Counter(r.get("reported_cultural_asymmetry") for r in have)
    askable = ca["yes"] + ca["no"]
    print(f"\n  reported_cultural_asymmetry: {dict(ca)}")
    print(f"    among the {askable} benchmarks where the question arises: "
          f"{ca['yes']} report a systematic asymmetry ({ca['yes'] / askable:.0%})")


def resolution_floor(corpus: list[dict]) -> None:
    section("(1b) WHAT EACH BENCHMARK CAN RESOLVE AT ALL")
    print("  Telling two models apart at a difference of eps needs ~1/eps^2 items, so a")
    print("  benchmark of n items resolves ~1/sqrt(n) and no finer (Hardt 2026, ch. 3-4).")
    sizes = [(r["dataset_size"], r["_name"]) for r in corpus if r.get("dataset_size")]
    n = len(sizes)
    print(f"\n  of the {n} benchmarks declaring a size:")
    for need, label in ((10000, "1 point"), (2500, "2 points"), (400, "5 points")):
        k = sum(1 for sz, _ in sizes if sz >= need)
        print(f"    resolve {label:9} (n >= {need:>6,}):  {k:2}/{n}")
    med = statistics.median([sz for sz, _ in sizes])
    print(f"    median {med:,.0f} items -> resolves ~{100 / math.sqrt(med):.1f} points")

    small = sorted((sz, nm) for sz, nm in sizes if sz < 1000)
    print(f"\n  {len(small)} benchmarks under 1,000 items -- nothing finer than ~3.2 points:")
    for sz, nm in small:
        print(f"    {sz:>6,} items  ~{100 / math.sqrt(sz):4.1f} points   {str(nm)[:40]}")

    print("\n  are the instrument gaps of finding (1) bigger than their own noise floor?")
    ok = 0
    rows = [r for r in corpus
            if GAP_KIND.get(r["paper_id"]) in INSTRUMENT_KINDS
            and r.get("reported_format_gap_points")]
    for r in sorted(rows, key=lambda x: -x["reported_format_gap_points"]):
        gap, sz = r["reported_format_gap_points"], r.get("dataset_size")
        if not sz:
            print(f"    {str(r['_name'])[:30]:32} gap {gap:>3}   size not declared")
            continue
        floor = 100 / math.sqrt(sz)
        clear = gap > 3 * floor
        ok += clear
        print(f"    {str(r['_name'])[:30]:32} gap {gap:>3}   {sz:>7,} items   "
              f"floor {floor:4.1f}   {'clear' if clear else 'TOO CLOSE TO NOISE'}")
    print(f"\n  {ok}/{len(rows)} gaps exceed three times their benchmark's resolution floor")


def finding_2_inference_single_key(corpus: list[dict]) -> None:
    section("(2) HALF THE CORPUS ASKS FOR INFERENCE AND ACCEPTS ONE ANSWER")
    core = [r for r in corpus if BEYOND(r) and SINGLE(r)]
    n = len(corpus)
    print(f"  gold_beyond_stimulus=yes AND single_answer: {len(core)}/{n}")
    gp = [r for r in corpus if is_gp(r)]
    pb = [r for r in corpus if not is_gp(r)]
    print(f"    among general-purpose : {sum(1 for r in gp if BEYOND(r) and SINGLE(r))}/{len(gp)}")
    print(f"    among purpose-built   : {sum(1 for r in pb if BEYOND(r) and SINGLE(r))}/{len(pb)}")
    print("\n  full crosstab answer_multiplicity x gold_beyond_stimulus:")
    tab = collections.Counter((r.get("answer_multiplicity"), r.get("gold_beyond_stimulus"))
                              for r in corpus)
    cols = ["yes", "no", "not_stated"]
    print(f"    {'':24}" + "".join(f"{c:>12}" for c in cols) + f"{'total':>8}")
    for am in ("single_answer", "answer_set", "graded_human_judgment", "not_stated"):
        row = [tab[(am, c)] for c in cols]
        print(f"    {am:24}" + "".join(f"{v:>12}" for v in row) + f"{sum(row):>8}")


def finding_3_who_pays(corpus: list[dict]) -> None:
    section("(3) WHO PAYS FOR THE TRUTH  -- humanities_role x gold_source")
    n = len(corpus)
    print("  where the reference answers come from, over the whole corpus")
    for src, k in collections.Counter(r.get("gold_source") for r in corpus).most_common():
        print(f"    {str(src):22} {k:2}/{n}   {'#' * (k * 3)}")
    print()
    binary = [r for r in corpus if r.get("humanities_role") in ("domain", "content")]
    DOMAIN = lambda r: r["humanities_role"] == "domain"
    claim("domain-role -> expert/curatorial gold", binary, DOMAIN, EXPERT)
    claim("content-role -> crowd/answer-key gold", binary, lambda r: not DOMAIN(r),
          lambda r: r.get("gold_source") in ("crowd_annotation", "authored_answer_key"))
    print("\n  stratified, to rule out the general-purpose block driving it:")
    claim("[purpose-built only] domain-role -> expert",
          [r for r in binary if not is_gp(r)], DOMAIN, EXPERT)
    print("\n  humanities_role x gold_source, full table:")
    sources = ["domain_expert", "existing_metadata", "authored_answer_key",
               "crowd_annotation", "model_generated", "paper_authors", "not_stated"]
    print(f"    {'':10}" + "".join(f"{s[:11]:>13}" for s in sources))
    for role in ("domain", "content", "both"):
        rows = [r for r in corpus if r.get("humanities_role") == role]
        cnt = collections.Counter(r.get("gold_source") for r in rows)
        print(f"    {role:10}" + "".join(f"{cnt[s]:>13}" for s in sources) + f"   n={len(rows)}")


def finding_4_general_purpose(corpus: list[dict]) -> None:
    section("(4) THE GENERAL-PURPOSE BLOCK HAS ONE SHAPE")
    claim("general-purpose -> authored_answer_key", corpus, is_gp,
          lambda r: r.get("gold_source") == "authored_answer_key")
    claim("general-purpose -> single_answer", corpus, is_gp, SINGLE)
    claim("general-purpose -> gold beyond stimulus", corpus, is_gp, BEYOND)
    gp_size = [r["dataset_size"] for r in corpus if is_gp(r) and r.get("dataset_size")]
    pb_size = [r["dataset_size"] for r in corpus if not is_gp(r) and r.get("dataset_size")]
    print(f"\n  median dataset_size: general-purpose {statistics.median(gp_size):,.0f} "
          f"(n={len(gp_size)})  vs purpose-built {statistics.median(pb_size):,.0f} (n={len(pb_size)})")
    print("\n  the eight general-purpose benchmarks:")
    for r in sorted((r for r in corpus if is_gp(r)), key=lambda x: x.get("publication_year", 0)):
        print(f"    {str(r['_name'])[:38]:40} {r.get('publication_year')}  "
              f"{r.get('gold_source'):20} {r.get('answer_multiplicity')}")
    print("\n  RETIRED: 'scale buys closure' -- the association is absent:")
    claim("dataset_size >= 20k -> single_answer",
          [r for r in corpus if r.get("dataset_size")],
          lambda r: r["dataset_size"] >= 20000, SINGLE)


def finding_5_negative_space(corpus: list[dict]) -> None:
    section("(5) WHAT NOBODY ASKS  -- counts only, no test")
    n = len(corpus)
    for field, label in (("gold_concerns_genesis", "target is the object's genesis"),
                         ("gold_community_dependent", "correctness relative to a community")):
        yes = [r["_name"] for r in corpus if r.get(field) == "yes"]
        print(f"  {label:38} {len(yes):2}/{n}   {', '.join(str(x)[:26] for x in yes)}")
    av = [r["_name"] for r in corpus if {"audio", "video"} & set(r.get("benchmark_modalities") or [])]
    print(f"  {'benchmark uses audio or video':38} {len(av):2}/{n}   "
          f"{', '.join(str(x)[:26] for x in av)}")
    graded = [r["_name"] for r in corpus if r.get("answer_multiplicity") == "graded_human_judgment"]
    print(f"  {'scoring admits gradation':38} {len(graded):2}/{n}   "
          f"{', '.join(str(x)[:26] for x in graded)}")
    print("\n  modality combinations present in the corpus:")
    for combo, k in collections.Counter(
            tuple(sorted(r.get("benchmark_modalities") or [])) for r in corpus).most_common():
        print(f"    {'+'.join(combo):24} {k}")


# --------------------------------------------------------------------------
# 2. what the data does not license
# --------------------------------------------------------------------------

def caveat_disciplines(corpus: list[dict]) -> None:
    section("(A) DISCIPLINES ARE NOT MEASURABLE FROM relevant_asjc_areas")
    areas = collections.Counter(a for r in corpus for a in (r.get("relevant_asjc_areas") or []))
    print("  area counts (uncontrolled vocabulary -- note the Archaeology/Archeology split):")
    for area, k in areas.most_common():
        print(f"    {area:36} {k}")
    print("\n  who the small 'disciplinary' groups actually are:")
    for area in ("Music", "Philosophy", "Archaeology", "Classics"):
        rows = [r for r in corpus if area in (r.get("relevant_asjc_areas") or [])]
        if not rows:
            continue
        gpn = sum(1 for r in rows if is_gp(r))
        print(f"    {area} (n={len(rows)}, of which {gpn} general-purpose):")
        for r in rows:
            print(f"       {'[GP] ' if is_gp(r) else '     '}{str(r['_name'])[:40]:42} "
                  f"plurality={r.get('plurality_treatment')}")


def caveat_silence(corpus: list[dict]) -> None:
    section("(B) HALF THE CORPUS SAYS NOTHING ABOUT PLURALITY")
    n = len(corpus)
    stated = [r for r in corpus if r.get("plurality_treatment") != "not_stated"]
    print(f"  papers that say anything at all: {len(stated)}/{n}"
          f"  ({sum(1 for r in stated if NOISE(r))} noise, "
          f"{sum(1 for r in stated if r.get('plurality_treatment') == 'signal')} signal)")
    print("\n  by year:")
    for y in sorted({r.get("publication_year") for r in corpus if r.get("publication_year")}):
        s = [r for r in corpus if r.get("publication_year") == y]
        print(f"    {y}  n={len(s):2}  noise={sum(map(NOISE, s)):2}  silent={sum(map(SILENT, s)):2}"
              f"  signal={sum(1 for r in s if r.get('plurality_treatment') == 'signal')}")
    print()
    recent = lambda r: (r.get("publication_year") or 0) >= 2026
    claim("2026 -> treats divergence as noise", corpus, recent, NOISE)
    claim("2026 -> says ANYTHING about divergence", corpus, recent, lambda r: not SILENT(r))
    print("\n  the second is the defensible claim: silence disappears, which is weaker")
    print("  than 'minimisation rises' and survives a stricter test.")


def caveat_silent_papers(corpus: list[dict]) -> None:
    section("(C) THREE SILENT PAPERS MANUFACTURE CORRELATIONS BETWEEN FACETS")
    scored = [(sum(1 for f in FACET_FIELDS if r.get(f) == "not_stated"), r["_name"])
              for r in corpus]
    for k, name in sorted(scored, reverse=True)[:6]:
        print(f"    {str(name)[:44]:46} not_stated on {k}/{len(FACET_FIELDS)} facets")
    print(f"\n  {'facet pair':60}{'V all':>8}{'V excl not_stated':>20}")
    for f1, f2 in itertools.combinations(FACET_FIELDS, 2):
        v_all, _ = cramers_v(corpus, f1, f2)
        sub = [r for r in corpus if r.get(f1) != "not_stated" and r.get(f2) != "not_stated"]
        v_sub, n_sub = cramers_v(sub, f1, f2)
        flag = "  <-- collapses" if v_all - (0 if math.isnan(v_sub) else v_sub) > 0.30 else ""
        v_sub_s = "  n/a" if math.isnan(v_sub) else f"{v_sub:.2f}"
        print(f"  {f1 + ' x ' + f2:60}{v_all:>8.2f}{v_sub_s:>14} (n={n_sub}){flag}")


def caveat_reliability(corpus: list[dict]) -> None:
    section("(D) RELIABILITY: THE SAME BENCHMARK READ TWICE")
    pair = [r for r in corpus if r.get("paper_id") in VULCA_IDS]
    if len(pair) == 2:
        a, b = pair
        print(f"  {a.get('paper_id')} vs {b.get('paper_id')} -- both describe VULCA-BENCH\n")
        fields = list(FACET_FIELDS) + ["humanities_role", "primary_evaluation_setting",
                                       "dataset_size", "relevant_asjc_areas"]
        agree = 0
        for f in fields:
            va, vb = a.get(f), b.get(f)
            same = va == vb
            agree += same and f in FACET_FIELDS
            print(f"    {f:28} {str(va)[:24]:26} {str(vb)[:24]:26} {'' if same else '<-- DIFFER'}")
        print(f"\n  facet agreement on the same object: {agree}/{len(FACET_FIELDS)}")
    else:
        print("  the VULCA pair is not both present in the corpus")

    print("\n  for contrast, ciop/cip agreement (two prompts over ONE text -- convergence,")
    print("  not correctness):")
    for f in FACET_FIELDS:
        dis = sum(1 for r in corpus
                  if f in r["_ciop"] and f in r["_cip"] and r["_ciop"][f] != r["_cip"][f])
        print(f"    {f:28} agree {len(corpus) - dis}/{len(corpus)}")
    contested = sorted(
        ((sum(1 for f in FACET_FIELDS
              if f in r["_ciop"] and f in r["_cip"] and r["_ciop"][f] != r["_cip"][f]), r["_name"])
         for r in corpus), reverse=True)[:5]
    print(f"    most contested papers: "
          f"{', '.join(f'{str(n)[:22]} ({k})' for k, n in contested if k)}")


def caveat_integrity(corpus: list[dict]) -> None:
    section("(E) CORPUS INTEGRITY")
    n = len(corpus)
    names = collections.Counter((r.get("benchmark_name") or "").strip().lower() for r in corpus)
    dupes = [k for k, v in names.items() if v > 1 and k]
    print(f"  files: {n}   distinct named benchmarks: {len([k for k in names if k])}")
    print(f"  duplicated benchmark_name: {dupes or 'none'}")
    unnamed = [r.get("paper_id") for r in corpus if not r.get("benchmark_name")]
    print(f"  benchmark_name is null: {len(unnamed)}  {unnamed}")
    print(f"  dataset_size is null:   {sum(1 for r in corpus if not r.get('dataset_size'))}")
    print("\n  papers failing an inclusion criterion other than general_purpose_benchmark:")
    for r in corpus:
        bad = [k for k, v in (r.get("inclusion_criteria") or {}).items()
               if isinstance(v, dict) and v.get("met") is False and k != "general_purpose_benchmark"]
        if bad:
            print(f"    {str(r['_name'])[:44]:46} {bad}")


def main() -> None:
    corpus = load_corpus()
    print(f"findings_report -- {len(corpus)} papers from {PAPERS_DIR}")
    has_results = sum(1 for r in corpus if r.get("reported_format_gap"))
    print(f"results axis extracted for {has_results}/{len(corpus)} papers")

    corpus_map(corpus)
    finding_1_format_gap(corpus)
    resolution_floor(corpus)
    finding_2_inference_single_key(corpus)
    finding_3_who_pays(corpus)
    finding_4_general_purpose(corpus)
    finding_5_negative_space(corpus)

    caveat_disciplines(corpus)
    caveat_silence(corpus)
    caveat_silent_papers(corpus)
    caveat_reliability(corpus)
    caveat_integrity(corpus)


if __name__ == "__main__":
    main()
