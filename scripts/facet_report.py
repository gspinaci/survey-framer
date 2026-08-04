#!/usr/bin/env python3
"""Facet report: distributions, persona disagreement, and derived clusters.

Reads only what the pipeline already wrote — the final reports in output/papers/
and the two persona reports in output/papers/agents/ — so it makes no API calls
and can be re-run freely. That is the point of the facet design: the contested
task boundaries are derived here, offline, and a different reading of where they
fall costs a re-run of this script rather than a re-extraction of the corpus.

See METHODOLOGY_facets.md.

    python scripts/facet_report.py
"""

import collections
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import AGENTS_DIR, PAPERS_DIR
from src.fields import FACET_FIELDS, check_vocab


def load_corpus() -> list[dict]:
    """Each entry: {id, final, ciop, cip} for every paper with facets extracted."""
    corpus = []
    for jf in sorted(PAPERS_DIR.glob("*.json")):
        final = json.loads(jf.read_text(encoding="utf-8"))
        if not any(f in final for f in FACET_FIELDS):
            continue
        stem = jf.stem
        ciop_p = AGENTS_DIR / f"{stem}.ciop.json"
        cip_p = AGENTS_DIR / f"{stem}.cip.json"
        corpus.append({
            "id": final.get("paper_id", stem),
            "name": final.get("benchmark_name") or final.get("paper_name") or stem,
            "final": final,
            "ciop": json.loads(ciop_p.read_text(encoding="utf-8")) if ciop_p.exists() else {},
            "cip": json.loads(cip_p.read_text(encoding="utf-8")) if cip_p.exists() else {},
        })
    return corpus


def section(title: str) -> None:
    print(f"\n{'=' * 72}\n{title}\n{'=' * 72}")


def report_distributions(corpus: list[dict]) -> None:
    section("FACET DISTRIBUTIONS")
    n = len(corpus)
    for facet in FACET_FIELDS:
        counts = collections.Counter(str(p["final"].get(facet)) for p in corpus)
        print(f"\n{facet}  (n={n})")
        for value, k in counts.most_common():
            bar = "█" * round(40 * k / n)
            print(f"   {value:24} {k:3}  {100 * k / n:4.0f}%  {bar}")


def report_disagreement(corpus: list[dict]) -> None:
    """Persona divergence, kept as a measurement rather than adjudicated away.

    The two personae embody the humanist and the ML reading of the same paper, so
    which facets they read differently is itself a result — see METHODOLOGY_facets.md
    section 6. The reviewer still picks a final value; this recovers what it resolved.
    """
    section("PERSONA DISAGREEMENT (ciop vs cip)")
    print(f"{'facet':28} {'agree':>10}  {'contested papers'}")
    contested_by_paper = collections.Counter()
    for facet in FACET_FIELDS:
        agree = contested = 0
        examples = []
        for p in corpus:
            a, b = p["ciop"].get(facet), p["cip"].get(facet)
            if a is None or b is None:
                continue
            if str(a).strip().lower() == str(b).strip().lower():
                agree += 1
            else:
                contested += 1
                contested_by_paper[p["id"]] += 1
                examples.append((p["name"][:26], a, b, p["final"].get(facet)))
        total = agree + contested
        rate = f"{agree}/{total}" if total else "n/a"
        print(f"{facet:28} {rate:>10}  {contested}")
        for name, a, b, f in examples:
            print(f"     {name:28} ciop={str(a):20} cip={str(b):20} → {f}")

    if contested_by_paper:
        print("\nmost contested papers:")
        for pid, k in contested_by_paper.most_common(8):
            print(f"   {k} facet(s)  {pid}")


def report_crosstabs(corpus: list[dict]) -> None:
    """The format x operation crosstab the single-field schema could not express."""
    section("CROSSTAB: answer_multiplicity x gold_beyond_stimulus")
    rows = sorted({str(p["final"].get("answer_multiplicity")) for p in corpus})
    cols = sorted({str(p["final"].get("gold_beyond_stimulus")) for p in corpus})
    print(f"{'':26}" + "".join(f"{c:>16}" for c in cols))
    for r in rows:
        line = f"{r:26}"
        for c in cols:
            k = sum(
                1 for p in corpus
                if str(p["final"].get("answer_multiplicity")) == r
                and str(p["final"].get("gold_beyond_stimulus")) == c
            )
            line += f"{k:>16}"
        print(line)

    section("CROSSTAB: gold_source x plurality_treatment")
    rows = sorted({str(p["final"].get("gold_source")) for p in corpus})
    cols = sorted({str(p["final"].get("plurality_treatment")) for p in corpus})
    print(f"{'':26}" + "".join(f"{c:>16}" for c in cols))
    for r in rows:
        line = f"{r:26}"
        for c in cols:
            k = sum(
                1 for p in corpus
                if str(p["final"].get("gold_source")) == r
                and str(p["final"].get("plurality_treatment")) == c
            )
            line += f"{k:>16}"
        print(line)


def report_profiles(corpus: list[dict]) -> None:
    """Group papers by their full facet signature — clusters, derived not declared."""
    section("FACET SIGNATURES (emergent groups)")
    sigs = collections.defaultdict(list)
    for p in corpus:
        sig = tuple(str(p["final"].get(f)) for f in FACET_FIELDS)
        sigs[sig].append(p["name"][:34])
    print(f"{len(sigs)} distinct signatures over {len(corpus)} papers")
    for sig, names in sorted(sigs.items(), key=lambda kv: -len(kv[1])):
        if len(names) < 2:
            continue
        print(f"\n  n={len(names)}")
        for f, v in zip(FACET_FIELDS, sig):
            print(f"     {f:26} {v}")
        for nm in names:
            print(f"       · {nm}")
    singles = [names[0] for sig, names in sigs.items() if len(names) == 1]
    if singles:
        print(f"\n  unique signatures ({len(singles)}): {', '.join(singles)}")


def report_vocab(corpus: list[dict]) -> None:
    section("VOCABULARY CHECK")
    bad = 0
    for p in corpus:
        for w in check_vocab(p["final"]):
            print(f"  {p['id'][:34]}: {w}")
            bad += 1
    print(f"  {bad} violation(s) across {len(corpus)} papers")


def main() -> None:
    corpus = load_corpus()
    if not corpus:
        print("No papers with facets found. Run: python main.py --input input/papers.csv --step analyze")
        return
    print(f"Facet report over {len(corpus)} papers")
    report_distributions(corpus)
    report_disagreement(corpus)
    report_crosstabs(corpus)
    report_profiles(corpus)
    report_vocab(corpus)


if __name__ == "__main__":
    main()
