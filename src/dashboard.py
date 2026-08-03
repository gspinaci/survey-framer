"""
Provenance dashboard — a self-contained, offline HTML page of charts describing
the provenance of the benchmark corpus (where each benchmark was found), plus what
the benchmarks cover and how they evaluate models.

Each variable is drawn with the chart that fits its semantics rather than a uniform
row of bars: a partition -> donut, a growth-over-time -> stacked columns, magnitude
across many categories -> treemap, set relationships (content/domain/both) -> Venn,
unit composition -> waffle, a ranking -> lollipop, a single proportion -> stat+meter.

It joins three sources into one record per benchmark:
  - input/papers.csv                             -> provenance (source, URLs, year, metrics)
  - input/Survey Benchmarks LLM+DH - Sources.csv -> Source -> Family taxonomy lookup
  - output/papers/*.json                         -> extracted fields (ASJC areas,
                                                    modalities, humanities role, criteria)

Charts are inline SVG + a little vanilla JS — no external libraries or network
requests, so the file works offline (double-click) and is CSP-safe / Artifact-ready.

Run:  python main.py --input input/papers.csv --step dashboard
  or: python -m src.dashboard
"""

import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from config import PAPERS_CSV, SOURCES_CSV, PAPERS_DIR, DASHBOARD_HTML
from src.csv_reader import read_papers_csv


# ---------------------------------------------------------------------------
# Provenance taxonomy
# ---------------------------------------------------------------------------

# Consolidated provenance families (entity -> fixed colour slot; order = legend order).
FAMILY_ORDER = [
    "Company system cards",
    "Academic venue",
    "Systematic review (ASReview)",
    "Benchmark hub",
    "Unspecified / direct",
]
FAMILY_COLOR = {
    "Company system cards": "s1",
    "Academic venue": "s2",
    "Systematic review (ASReview)": "s3",
    "Benchmark hub": "s4",
    "Unspecified / direct": "muted",
}

# Sources.csv `Family` values -> consolidated family.
_FAMILY_MAP = {
    "Company System Cards": "Company system cards",
    "Benchmark website": "Benchmark hub",
    "Shared-task": "Academic venue",
    "Workshop": "Academic venue",
    "SemEval": "Academic venue",
    "COLING 2024": "Academic venue",
    "LREC 2026": "Academic venue",
    "ECCV workshops": "Academic venue",
    "CVPR workshop": "Academic venue",
    "ICCV workshop": "Academic venue",
    "ACL 2025": "Academic venue",
}


def _load_source_families(path: Path) -> dict[str, str]:
    """Map each source Name -> raw Family string from the Sources lookup CSV."""
    fam: dict[str, str] = {}
    if not path.exists():
        return fam
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = (row.get("Name") or "").strip()
            if name:
                fam[name] = (row.get("Family") or "").strip()
    return fam


def _clean_source_label(source: str) -> str:
    """Human-friendly label for a specific source value."""
    s = source.strip()
    if not s:
        return "(unspecified)"
    if s.upper() == "ASREVIEW":
        return "ASReview (systematic)"
    return s.replace("Neur IPS", "NeurIPS")


def consolidate_family(source: str, fam_lookup: dict[str, str]) -> str:
    """Collapse a specific source into one of the FAMILY_ORDER buckets."""
    s = source.strip()
    if not s:
        return "Unspecified / direct"
    if s.upper() == "ASREVIEW":
        return "Systematic review (ASReview)"
    raw = fam_lookup.get(s, "")
    if raw in _FAMILY_MAP:
        return _FAMILY_MAP[raw]
    # Named source with a blank/unknown Family (conferences, DH workshops such as
    # LM4DH, NeurIPS 2024, …) -> treated as an academic venue.
    return "Academic venue"


# ---------------------------------------------------------------------------
# Field normalisation
# ---------------------------------------------------------------------------

_HOST_RESOURCE = {
    "github.com": "GitHub",
    "huggingface.co": "Hugging Face",
    "codabench.org": "Codabench",
    "gitlab.com": "GitLab",
    "zenodo.org": "Zenodo",
}


def _host(url: str) -> str:
    try:
        return urlparse(url.strip()).netloc.lower().replace("www.", "")
    except Exception:
        return ""


def resource_channel(url: str) -> str:
    if not url.strip():
        return "No public resource"
    return _HOST_RESOURCE.get(_host(url), "Other host")


_MOD_SINGULAR = {
    "images": "image",
    "texts": "text",
    "documents": "document",
    "tables": "table",
    "spreadsheets": "spreadsheet",
    "slides": "slide",
    "videos": "video",
}


def norm_modalities(mods) -> list[str]:
    out = set()
    for m in mods or []:
        m = str(m).strip().lower()
        m = _MOD_SINGULAR.get(m, m)
        if m:
            out.add(m)
    return sorted(out)


# Evaluation-metric detection. Word-boundary regex -> canonical label, so prose in
# the extracted note (e.g. "answer accuracy") can be scanned without false hits such
# as "answer" -> WER. Only known metrics are charted; unknowns are ignored.
_METRIC_PATTERNS = [
    (r"bertscore", "BERTScore"),
    (r"\bbleu\b", "BLEU"),
    (r"\brouge\b", "ROUGE"),
    (r"\bchr-?f\b", "chrF"),
    (r"\bmeteor\b", "METEOR"),
    (r"cosine", "Cosine similarity"),
    (r"hallucinat", "Hallucination rate"),
    (r"perplexit", "Perplexity"),
    (r"exact match", "Exact match"),
    (r"edit distance|levenshtein", "Edit distance"),
    (r"\bprecision\b", "Precision"),
    (r"\brecall\b", "Recall"),
    (r"\bf-?1\b|f1[- ]?score|f-measure", "F1"),
    (r"\bwer\b|word error rate", "WER"),
    (r"\bcer\b|character error rate", "CER"),
    (r"\bn?dcg\b", "DCG / nDCG"),
    (r"\bmae\b|mean absolute error", "MAE"),
    (r"\brmse\b|root mean square", "RMSE"),
    (r"pearson|spearman|correlation", "Correlation"),
    (r"cohen'?s|\bkappa\b|inter-?annotator", "Agreement (κ / ICC)"),
    (r"\bicc\b", "Agreement (κ / ICC)"),
    (r"\baccurac|top[- ]?1|\bacc\b|% correct|percentage correct", "Accuracy"),
]


def detect_metrics(text: str) -> list[str]:
    """Return the distinct canonical metrics named anywhere in `text`."""
    t = (text or "").lower()
    out = []
    for pat, label in _METRIC_PATTERNS:
        if re.search(pat, t) and label not in out:
            out.append(label)
    return out


# ---------------------------------------------------------------------------
# Dataset assembly
# ---------------------------------------------------------------------------

def build_dataset(papers: list[dict] | None = None) -> list[dict]:
    """One record per benchmark, joining CSV provenance with extracted JSON."""
    if papers is None:
        papers = read_papers_csv(PAPERS_CSV)

    fam_lookup = _load_source_families(SOURCES_CSV)

    # Index extracted JSON by paper_id (the pipeline's stable arXiv/DOI-derived key)
    # and by normalised name (fallback). csv_row is NOT used: the CSV is edited between
    # runs, so row numbers and cell names drift and would attach the wrong analysis.
    def _norm(s: str) -> str:
        return re.sub(r"[^a-z0-9]+", "", (s or "").lower())

    json_by_pid: dict[str, dict] = {}
    json_by_name: dict[str, dict] = {}
    for jf in sorted(PAPERS_DIR.glob("*.json")):
        try:
            data = json.loads(jf.read_text(encoding="utf-8"))
        except Exception:
            continue
        pid = (data.get("paper_id") or "").strip()
        if pid:
            json_by_pid[pid] = data
        nm = _norm(data.get("paper_name"))
        if nm:
            json_by_name[nm] = data

    records = []
    for p in papers:
        j = json_by_pid.get(p.get("id")) or json_by_name.get(_norm(p.get("name"))) or {}

        year = None
        m = re.search(r"(20\d\d)", p.get("year", ""))
        if m:
            year = int(m.group(1))

        # Metrics: the terse CSV column plus the extracted note (much better coverage).
        crit = j.get("inclusion_criteria", {}) if j else {}
        qm = crit.get("quantitative_metrics", {}) if isinstance(crit, dict) else {}
        note = qm.get("note", "") if isinstance(qm, dict) else ""
        metrics = detect_metrics(f"{p.get('evaluation_metrics', '')} || {note}")

        records.append({
            "name": p.get("name", ""),
            "year": year,
            "source": p.get("source", ""),
            "source_label": _clean_source_label(p.get("source", "")),
            "family": consolidate_family(p.get("source", ""), fam_lookup),
            "resource_channel": resource_channel(p.get("resource_url", "")),
            "has_resource": bool((p.get("resource_url") or "").strip()),
            "metrics": metrics,
            "has_metrics": bool(metrics),
            # extracted (may be empty if no JSON join)
            "has_json": bool(j),
            "asjc": j.get("relevant_asjc_areas", []) if j else [],
            "modalities": norm_modalities(j.get("benchmark_modalities", [])) if j else [],
            "role": (j.get("humanities_role") or "").strip().lower() if j else "",
            "criteria": crit if isinstance(crit, dict) else {},
        })
    return records


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

# Modality profiles — each benchmark falls into exactly one (part-of-whole, for the waffle).
PROFILE_ORDER = ["text_only", "text_image", "text_av", "text_multi"]
PROFILE_LABEL = {
    "text_only": "Text only",
    "text_image": "Text + image",
    "text_av": "Text + audio / video",
    "text_multi": "Text + multiple",
}
PROFILE_COLOR = {"text_only": "muted", "text_image": "s1", "text_av": "s2", "text_multi": "s3"}

# One fixed colour per humanities domain (used to colour the treemap tiles). Mid-tone
# categorical hues chosen to stay legible on both the light and dark chart surface.
DOMAIN_COLOR = {
    "History": "#4e79a7",
    "Language and Linguistics": "#f28e2b",
    "Visual Arts and Performing Arts": "#e15759",
    "Literature and Literary Theory": "#76b7b2",
    "Religious Studies": "#59a14f",
    "Philosophy": "#edc948",
    "Music": "#b07aa1",
    "Classics": "#9c755f",
    "Archaeology": "#ff9da7",
    "Museology": "#17becf",
    "Conservation": "#9c9c9c",
    "History and Philosophy of Science": "#bcbd22",
    "Multidisciplinary": "#8c8c8c",
}
DEFAULT_DOMAIN_COLOR = "#9aa0a6"

# Per-benchmark dot categories for the sidebar.
ROLE_NAME = {"both": "Both", "content": "Content", "domain": "Domain", "none": "None"}
ROLE_DOT = {"both": "s5", "content": "s2", "domain": "s3", "none": "muted"}


def modality_profile(mods) -> str:
    extra = set(mods) - {"text"}
    if not extra:
        return "text_only"
    if extra == {"image"}:
        return "text_image"
    if extra <= {"audio", "video"}:
        return "text_av"
    return "text_multi"


def _grade(criteria: dict, key: str) -> bool:
    sub = criteria.get(key) if isinstance(criteria, dict) else None
    return bool(isinstance(sub, dict) and sub.get("met"))


def compute_aggregations(records: list[dict]) -> dict:
    total = len(records)
    with_json = [r for r in records if r["has_json"]]
    nj = len(with_json)

    years = [r["year"] for r in records if r["year"]]
    distinct_sources = {r["source"].strip() for r in records if r["source"].strip()}
    n_resource = sum(1 for r in records if r["has_resource"])
    n_multimodal = sum(1 for r in with_json if set(r["modalities"]) - {"text"})
    n_with_metrics = sum(1 for r in records if r["has_metrics"])

    # General-purpose vs. purpose-built (the one inclusion criterion that actually varies).
    n_crit = sum(1 for r in with_json if r["criteria"])
    n_general = sum(1 for r in with_json if _grade(r["criteria"], "general_purpose_benchmark"))
    n_purpose = n_crit - n_general

    def pct(a, b):
        return f"{round(100 * a / b)}%" if b else "—"

    # --- KPIs (headline numbers; flat/redundant charts fold into these) --------
    kpis = [
        {"label": "Benchmarks in corpus", "value": total, "sub": "papers reviewed", "hero": True},
        {"label": "Span", "value": f"{min(years)}–{max(years)}" if years else "—",
         "sub": "publication years"},
        {"label": "Distinct sources", "value": len(distinct_sources), "sub": "venues, hubs & tools"},
        {"label": "Openly available", "value": pct(n_resource, total),
         "sub": f"{n_resource}/{total} share data or code"},
        {"label": "Multimodal", "value": pct(n_multimodal, nj),
         "sub": f"{n_multimodal}/{nj} go beyond text"},
    ]

    # --- Provenance donut (partition) + specific-source table ------------------
    fam_counter = Counter(r["family"] for r in records)
    fam_slices = [{"label": f, "value": fam_counter[f], "colorKey": FAMILY_COLOR[f]}
                  for f in FAMILY_ORDER if fam_counter[f]]
    src_counter = Counter(r["source_label"] for r in records)
    src_family = {r["source_label"]: r["family"] for r in records}
    src_table = sorted(
        ({"label": l, "value": v} for l, v in src_counter.items()),
        key=lambda x: (FAMILY_ORDER.index(src_family.get(x["label"], "Academic venue")), -x["value"]),
    )

    # --- Provenance over time (stacked columns) -------------------------------
    yr_fam = defaultdict(Counter)
    for r in records:
        if r["year"]:
            yr_fam[r["year"]][r["family"]] += 1
    years_sorted = sorted(yr_fam)
    time_series = [
        {"name": f, "colorKey": FAMILY_COLOR[f], "values": [yr_fam[y].get(f, 0) for y in years_sorted]}
        for f in FAMILY_ORDER if any(yr_fam[y].get(f, 0) for y in years_sorted)
    ]

    # --- Subjects (treemap: area = magnitude, colour = domain identity) --------
    subj_items = [{"label": k, "value": v, "color": DOMAIN_COLOR.get(k, DEFAULT_DOMAIN_COLOR)}
                  for k, v in Counter(a for r in records for a in r["asjc"]).most_common()]

    # --- Role of the humanities (Venn: content / domain / both) ---------------
    role = Counter(r["role"] for r in with_json if r["role"])
    venn = {"aLabel": "Content", "bLabel": "Domain",
            "aOnly": role.get("content", 0), "both": role.get("both", 0),
            "bOnly": role.get("domain", 0), "neither": role.get("none", 0),
            "aTotal": role.get("content", 0) + role.get("both", 0),
            "bTotal": role.get("domain", 0) + role.get("both", 0)}

    # --- Modalities (waffle: one square per benchmark) ------------------------
    prof = Counter(modality_profile(r["modalities"]) for r in with_json)
    cells = [PROFILE_COLOR[k] for k in PROFILE_ORDER for _ in range(prof.get(k, 0))]
    mod_legend = [{"label": PROFILE_LABEL[k], "colorKey": PROFILE_COLOR[k], "value": prof[k]}
                  for k in PROFILE_ORDER if prof.get(k)]
    mod_label_by_key = {PROFILE_COLOR[k]: PROFILE_LABEL[k] for k in PROFILE_ORDER}

    # --- Evaluation metrics (lollipop ranking) --------------------------------
    metric_rows = [{"label": k, "value": v}
                   for k, v in Counter(m for r in records for m in r["metrics"]).most_common(10)]

    # --- Per-benchmark list for the sidebar (name + hover dots) ----------------
    benchmarks = []
    for r in sorted(records, key=lambda x: (x["name"] or "").lower()):
        dots = [{"colorKey": FAMILY_COLOR.get(r["family"], "muted"),
                 "label": "Provenance — " + r["family"]}]
        if r["has_json"]:
            role = r["role"] or "none"
            p = modality_profile(r["modalities"])
            dots.append({"colorKey": ROLE_DOT.get(role, "muted"),
                         "label": "Role — " + ROLE_NAME.get(role, role.title())})
            dots.append({"colorKey": PROFILE_COLOR[p], "label": "Modality — " + PROFILE_LABEL[p]})
        else:
            dots.append({"colorKey": "muted", "label": "Role — not analysed"})
            dots.append({"colorKey": "muted", "label": "Modality — not analysed"})
        benchmarks.append({"name": r["name"] or "(untitled)", "dots": dots})

    charts = [
        {
            "id": "fam", "section": "prov", "type": "donut",
            "title": "Where each benchmark was found",
            "sub": "Provenance channel — each benchmark counted once",
            "slices": fam_slices, "center": {"label": "benchmarks", "value": total},
            "tableRows": src_table, "tableUnit": "count",
            "foot": "Source column of papers.csv, grouped via the Sources lookup. Table lists the specific sources.",
        },
        {
            "id": "time", "section": "prov", "type": "stack",
            "title": "How the corpus grew",
            "sub": "Benchmarks per year, stacked by provenance family",
            "years": years_sorted, "series": time_series,
            "foot": "Year as recorded at the source.",
        },
        {
            "id": "subj", "section": "cover", "type": "treemap", "wide": True,
            "title": "Humanities subjects covered",
            "sub": "Tile area = benchmarks touching that ASJC area (a benchmark can span several)",
            "items": subj_items, "foot": "Extracted relevant_asjc_areas.",
        },
        {
            "id": "role", "section": "cover", "type": "venn",
            "title": "Role of the humanities",
            "sub": "Humanities as subject content, as application domain — or both",
            "venn": venn,
            "foot": "Extracted humanities_role. ‘Both’ is the overlap of the two roles, not a third category.",
        },
        {
            "id": "mod", "section": "cover", "type": "waffle",
            "title": "Modalities",
            "sub": f"One square = one benchmark ({nj} with extracted analysis)",
            "cells": cells, "legend": mod_legend, "labelByKey": mod_label_by_key,
            "foot": "Extracted benchmark_modalities, lower-cased and singularised.",
        },
        {
            "id": "metric", "section": "eval", "type": "lollipop",
            "title": "Evaluation metrics",
            "sub": f"Most-used metrics (detected for {n_with_metrics} of {total})",
            "rows": metric_rows, "unit": "benchmarks",
            "foot": "CSV metrics column plus the extracted metric note, normalised. Top 10.",
        },
        {
            "id": "scope", "section": "eval", "type": "stat",
            "title": "General-purpose vs. purpose-built",
            "sub": "Are these broad LLM benchmarks, or built for the humanities?",
            "value": pct(n_general, n_crit), "pct": round(100 * n_general / n_crit) if n_crit else 0,
            "statLabel": "are general-purpose benchmarks",
            "sub2": f"the other {n_purpose} of {n_crit} are purpose-built for the humanities",
            "tableRows": [{"label": "General-purpose", "value": n_general},
                          {"label": "Purpose-built", "value": n_purpose}],
            "foot": "Extracted general_purpose_benchmark criterion — the only one that varies; all meet the other six.",
        },
    ]

    sections = [
        {"id": "prov", "n": "1", "title": "Provenance",
         "desc": "Where the benchmarks come from, and how the corpus grew."},
        {"id": "cover", "n": "2", "title": "What they cover",
         "desc": "Humanities subjects, the role of the humanities, and modalities."},
        {"id": "eval", "n": "3", "title": "Evaluation & scope",
         "desc": "How the benchmarks measure models, and how broad they are."},
    ]

    return {
        "meta": {
            "total": total, "n_with_json": nj, "n_general": n_general, "n_purpose": n_purpose,
            "n_multimodal": n_multimodal, "n_with_metrics": n_with_metrics,
            "generated": datetime.now().strftime("%B %d, %Y"),
        },
        "kpis": kpis,
        "charts": charts,
        "sections": sections,
        "benchmarks": benchmarks,
    }


# ---------------------------------------------------------------------------
# HTML rendering
# ---------------------------------------------------------------------------

def render_html(aggs: dict, out_path: Path) -> None:
    data_json = json.dumps(aggs, ensure_ascii=False).replace("</", "<\\/")
    html = (
        _HTML_TEMPLATE
        .replace("__TITLE__", "LLM × Cultural Heritage benchmark corpus")
        .replace("__SUBTITLE__", "Where the benchmarks in this survey come from — and what they measure")
        .replace("__GENERATED__", aggs["meta"]["generated"])
        .replace("__TOTAL__", str(aggs["meta"]["total"]))
        .replace("/*__DATA__*/", data_json)
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")


def generate_dashboard(papers: list[dict] | None = None) -> Path:
    records = build_dataset(papers)
    aggs = compute_aggregations(records)
    render_html(aggs, DASHBOARD_HTML)
    m = aggs["meta"]
    print(f"  {m['total']} benchmarks ({m['n_with_json']} joined to extracted analysis)")
    print(f"  general-purpose {m['n_general']} / purpose-built {m['n_purpose']} · "
          f"{m['n_multimodal']} multimodal · metrics for {m['n_with_metrics']}")
    print(f"Written to {DASHBOARD_HTML}")
    return DASHBOARD_HTML


# The page skeleton: palette as CSS custom properties (light + dark, both selected),
# an inline-SVG renderer with one drawing routine per chart semantic, and a data blob.
# No external requests.
_HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet">
<style>
  :root{
    --plane:#f9f9f7; --surface:#fcfcfb;
    --ink:#0b0b0b; --ink-2:#52514e; --muted:#898781;
    --grid:#e1e0d9; --axis:#c3c2b7; --ring:rgba(11,11,11,.10);
    --s1:#2a78d6; --s2:#1baf7a; --s3:#eda100; --s4:#008300; --s5:#4a3aa7;
    --track:rgba(11,11,11,.06);
  }
  /* Light is the default theme; dark applies only when the toggle sets .force-dark. */
  :root.force-dark{
    --plane:#0d0d0d; --surface:#1a1a19;
    --ink:#fff; --ink-2:#c3c2b7; --muted:#8f8d86;
    --grid:#2c2c2a; --axis:#383835; --ring:rgba(255,255,255,.12);
    --s1:#3987e5; --s2:#199e70; --s3:#c98500; --s4:#008300; --s5:#9085e9;
    --track:rgba(255,255,255,.08);
  }
  *{box-sizing:border-box}
  html,body{margin:0}
  body{
    background:var(--plane); color:var(--ink);
    font-family:system-ui,-apple-system,"Segoe UI",sans-serif;
    line-height:1.5; -webkit-font-smoothing:antialiased;
  }
  .wrap{max-width:1120px; margin:0 auto; padding:40px 24px 72px; transition:margin-left .22s ease}
  /* Collapsible benchmark sidebar */
  .sb-toggle{position:fixed; top:16px; left:16px; z-index:30; width:40px; height:40px; border-radius:10px;
    border:1px solid var(--ring); background:var(--surface); color:var(--ink); font-size:17px; line-height:1; cursor:pointer}
  .sb-toggle:hover{border-color:var(--muted)}
  .sidebar{position:fixed; top:0; left:0; height:100vh; width:360px; z-index:25; overflow:auto;
    background:var(--surface); border-right:1px solid var(--ring); padding:14px 16px 20px;
    transform:translateX(-100%); transition:transform .22s ease}
  body.sb-open .sidebar{transform:translateX(0)}
  .sb-bar{display:flex; justify-content:flex-end; align-items:center; height:40px; padding-left:46px; margin-bottom:8px}
  .sb-head{display:flex; align-items:baseline; gap:8px; font-weight:650; font-size:16px; padding:0 6px}
  .sb-count{color:var(--muted); font-size:13px; font-variant-numeric:tabular-nums}
  .sb-note{font-size:11px; color:var(--muted); padding:6px 6px 10px; border-bottom:1px solid var(--grid); margin-bottom:4px}
  .sb-it{display:flex; align-items:center; gap:10px; padding:6px 6px; border-radius:8px; font-size:13px}
  .sb-it:hover{background:var(--track)}
  .sb-dots{display:inline-flex; gap:4px; flex:none}
  .dot{width:9px; height:9px; border-radius:50%; display:inline-block}
  .sb-nm{white-space:nowrap; overflow:hidden; text-overflow:ellipsis; color:var(--ink-2)}
  @media (min-width:1101px){ body.sb-open .wrap{margin-left:384px} }
  @media (max-width:1100px){ .wrap{padding-top:64px} }
  header.page{display:flex; justify-content:space-between; align-items:flex-start; gap:24px; flex-wrap:wrap}
  h1{font-family:"Space Mono",ui-monospace,SFMono-Regular,monospace; font-size:46px; line-height:1.1; letter-spacing:-.03em; margin:0 0 10px; font-weight:700; max-width:840px}
  .lede{color:var(--ink-2); font-size:16px; margin:0; max-width:680px}
  .toggle{border:1px solid var(--ring); background:var(--surface); color:var(--ink-2);
    border-radius:999px; padding:7px 14px; font:inherit; font-size:13px; cursor:pointer; white-space:nowrap}
  .toggle:hover{color:var(--ink)}
  .kpis{display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:14px; margin:32px 0 8px}
  .kpi{background:var(--surface); border:1px solid var(--ring); border-radius:14px; padding:16px}
  .kpi .v{font-size:30px; font-weight:650; letter-spacing:-.02em; line-height:1}
  .kpi.hero .v{font-size:40px; color:var(--s1)}
  .kpi .l{font-size:13px; color:var(--ink); margin-top:8px; font-weight:550}
  .kpi .s{font-size:12px; color:var(--muted); margin-top:2px}
  section.grp{margin-top:44px}
  .grp-head{display:flex; align-items:baseline; gap:12px; margin-bottom:16px; border-bottom:1px solid var(--grid); padding-bottom:10px}
  .grp-head .num{font-family:"Space Mono",ui-monospace,monospace; font-size:36px; font-weight:400; color:var(--s1); font-variant-numeric:tabular-nums; line-height:1}
  .grp-head h2{font-family:"Space Mono",ui-monospace,SFMono-Regular,monospace; font-size:36px; margin:0; font-weight:400; letter-spacing:-.02em; line-height:1.1}
  .grp-head .d{font-family:"Space Mono",ui-monospace,SFMono-Regular,monospace; font-size:15px;
    color:var(--ink-2); margin-left:auto; text-align:right; max-width:56%; letter-spacing:-.02em; line-height:1.35}
  .grid{display:grid; grid-template-columns:repeat(2,1fr); gap:18px; align-items:start}
  figure.card{margin:0; background:var(--surface); border:1px solid var(--ring); border-radius:16px;
    padding:18px 18px 14px; min-width:0}
  figure.card.wide{grid-column:1 / -1}
  figcaption .t{font-size:15px; font-weight:600; letter-spacing:-.01em}
  figcaption .st{font-size:12.5px; color:var(--ink-2); margin-top:3px}
  .plot{margin-top:14px; overflow-x:auto}
  svg{display:block; width:100%; height:auto}
  .legend{display:flex; flex-wrap:wrap; gap:10px 16px; margin-top:12px}
  .legend .it{display:flex; align-items:center; gap:6px; font-size:12px; color:var(--ink-2)}
  .legend .sw{width:11px; height:11px; border-radius:3px; flex:none}
  .foot{font-size:11.5px; color:var(--muted); margin-top:12px; border-top:1px solid var(--grid); padding-top:9px}
  details.tbl{margin-top:8px; font-size:12px}
  details.tbl summary{color:var(--muted); cursor:pointer; list-style:none}
  details.tbl summary::-webkit-details-marker{display:none}
  details.tbl summary:before{content:"\25B8 "; color:var(--muted)}
  details.tbl[open] summary:before{content:"\25BE "}
  table{border-collapse:collapse; margin-top:8px; width:100%}
  th,td{text-align:left; padding:3px 10px 3px 0; border-bottom:1px solid var(--grid); font-variant-numeric:tabular-nums}
  th{color:var(--muted); font-weight:550}
  td.n,th.n{text-align:right}
  .txt{fill:var(--ink); font-size:12.5px}
  .txt-2{fill:var(--ink-2); font-size:12px}
  .txt-m{fill:var(--muted); font-size:11px}
  .statbox{padding:14px 2px 4px}
  .stat-v{font-size:54px; font-weight:650; letter-spacing:-.02em; line-height:1; color:var(--s1)}
  .stat-l{font-size:15px; color:var(--ink); margin-top:8px; font-weight:550}
  .meter{height:12px; border-radius:999px; background:var(--track); margin-top:16px; overflow:hidden}
  .meter-fill{height:100%; background:var(--s1); border-radius:999px}
  .stat-s{font-size:13px; color:var(--ink-2); margin-top:12px}
  .tip{position:fixed; pointer-events:none; z-index:20; opacity:0; transition:opacity .1s;
    background:var(--ink); color:var(--surface); font-size:12px; padding:6px 9px; border-radius:8px;
    white-space:nowrap; transform:translate(-50%,-130%)}
  .tip b{font-weight:650}
  footer.page{margin-top:48px; padding-top:16px; border-top:1px solid var(--grid); font-size:12px; color:var(--muted)}
  @media (max-width:860px){
    .grid{grid-template-columns:1fr}
    .grp-head .d{display:none}
    h1{font-size:24px}
  }
  @media print{
    :root.force-dark{--plane:#fff;--surface:#fff}
    .toggle{display:none} body{background:#fff}
    figure.card{break-inside:avoid; border-color:#ccc}
  }
</style>
</head>
<body>
<button class="sb-toggle" id="sbToggle" type="button" aria-label="Toggle benchmark list">&#9776;</button>
<aside class="sidebar" id="sidebar">
  <div class="sb-bar"><button class="toggle" id="themeBtn" type="button">Toggle theme</button></div>
  <div class="sb-head"><span>Benchmarks</span><span class="sb-count" id="sbCount"></span></div>
  <div class="sb-note">Dots: provenance &middot; role &middot; modality — hover each for detail</div>
  <div class="sb-list" id="sbList"></div>
</aside>
<div class="wrap viz-root" data-palette="#2a78d6,#1baf7a,#eda100,#008300,#4a3aa7">
  <header class="page">
    <div>
      <h1>__TITLE__</h1>
      <p class="lede">__SUBTITLE__</p>
    </div>
  </header>
  <div class="kpis" id="kpis"></div>
  <div id="sections"></div>
  <footer class="page">
    __TOTAL__ benchmarks &middot; generated __GENERATED__ &middot;
    Survey Framer &mdash; LLM benchmarks in the Arts &amp; Humanities.
  </footer>
</div>
<div class="tip" id="tip"></div>
<script id="data" type="application/json">/*__DATA__*/</script>
<script>
(function(){
  "use strict";
  const D = JSON.parse(document.getElementById("data").textContent);
  const NS = "http://www.w3.org/2000/svg";
  const tip = document.getElementById("tip");
  const cvar = k => "var(--" + k + ")";
  function ink(hex){
    const c = hex.replace("#",""); const n = p => parseInt(c.slice(p,p+2),16);
    return (0.299*n(0) + 0.587*n(2) + 0.114*n(4))/255 > 0.62 ? "#111" : "#fff";
  }

  function el(tag, attrs, txt){
    const e = document.createElementNS(NS, tag);
    for(const k in attrs) e.setAttribute(k, attrs[k]);
    if(txt != null) e.textContent = txt;
    return e;
  }
  function h(tag, cls, txt){
    const e = document.createElement(tag);
    if(cls) e.className = cls;
    if(txt != null) e.textContent = txt;
    return e;
  }
  function bindTip(node, html){
    node.addEventListener("mousemove", e => {
      tip.innerHTML = html; tip.style.left = e.clientX+"px"; tip.style.top = e.clientY+"px"; tip.style.opacity = "1";
    });
    node.addEventListener("mouseleave", () => tip.style.opacity = "0");
  }

  // ---- Donut (a partition) ----
  function donut(c){
    const slices = c.slices, W = 320, H = 250, cx = 118, cy = 120, R = 94, r = 58;
    const total = slices.reduce((s,x)=>s+x.value,0) || 1;
    const svg = el("svg", {viewBox:`0 0 ${W} ${H}`, role:"img"});
    let a0 = -Math.PI/2;
    slices.forEach(sl => {
      const a1 = a0 + (sl.value/total)*Math.PI*2;
      const p = el("path", {d:arc(cx,cy,R,r,a0,a1), fill:cvar(sl.colorKey)});
      bindTip(p, `<b>${sl.label}</b><br>${sl.value} (${Math.round(sl.value/total*100)}%)`);
      svg.appendChild(p);
      a0 = a1;
    });
    svg.appendChild(el("text",{x:cx,y:cy-2,class:"txt","text-anchor":"middle","font-size":"30","font-weight":"650"},String(total)));
    svg.appendChild(el("text",{x:cx,y:cy+18,class:"txt-m","text-anchor":"middle"},c.center.label));
    return svg;
  }
  function arc(cx,cy,R,r,a0,a1){
    const gap = 0.016; a0 += gap; a1 -= gap; if(a1<a0) a1=a0;
    const big = (a1-a0) > Math.PI ? 1 : 0;
    const p = (rad,a)=>[cx+rad*Math.cos(a), cy+rad*Math.sin(a)];
    const [x0,y0]=p(R,a0),[x1,y1]=p(R,a1),[xi1,yi1]=p(r,a1),[xi0,yi0]=p(r,a0);
    return `M${x0} ${y0} A${R} ${R} 0 ${big} 1 ${x1} ${y1} L${xi1} ${yi1} A${r} ${r} 0 ${big} 0 ${xi0} ${yi0} Z`;
  }

  // ---- Stacked columns (growth over time) ----
  function stack(c){
    const years=c.years, series=c.series, W=680, H=300, mL=32, mB=26, mT=12, mR=8;
    const pw=W-mL-mR, ph=H-mT-mB;
    const totals=years.map((_,i)=>series.reduce((s,se)=>s+se.values[i],0));
    const max=Math.max(1,...totals), step=niceStep(max), top=Math.ceil(max/step)*step;
    const band=pw/years.length, cw=Math.min(56, band*0.62);
    const svg=el("svg",{viewBox:`0 0 ${W} ${H}`, role:"img"});
    for(let v=0; v<=top; v+=step){
      const y=mT+ph-(v/top)*ph;
      svg.appendChild(el("line",{x1:mL,y1:y,x2:W-mR,y2:y,stroke:"var(--grid)","stroke-width":1}));
      svg.appendChild(el("text",{x:mL-6,y:y+3,class:"txt-m","text-anchor":"end"},String(v)));
    }
    years.forEach((yr,i)=>{
      const x=mL+i*band+(band-cw)/2; let acc=0;
      series.forEach(se=>{
        const v=se.values[i]; if(v<=0) return;
        const y=mT+ph-(acc+v)/top*ph;
        const rect=el("rect",{x,y:y+1,width:cw,height:Math.max(0,(v/top)*ph-2),rx:2,fill:cvar(se.colorKey)});
        bindTip(rect,`<b>${yr}</b> &middot; ${se.name}<br>${v} benchmark${v!==1?"s":""}`);
        svg.appendChild(rect); acc+=v;
      });
      svg.appendChild(el("text",{x:x+cw/2,y:H-8,class:"txt-2","text-anchor":"middle"},String(yr)));
      svg.appendChild(el("text",{x:x+cw/2,y:mT+ph-(totals[i]/top)*ph-6,class:"txt","text-anchor":"middle","font-weight":"600"},String(totals[i])));
    });
    return svg;
  }
  function niceStep(max){
    const raw=max/4, mag=Math.pow(10,Math.floor(Math.log10(raw))), n=raw/mag;
    return Math.max(1,(n<=1?1:n<=2?2:n<=5?5:10)*mag);
  }

  // ---- Treemap (magnitude across many categories) ----
  function squarify(items,W,H){
    const nodes=items.map(d=>({label:d.label,value:d.value,color:d.color}));
    const total=nodes.reduce((s,d)=>s+d.value,0)||1, scale=(W*H)/total;
    nodes.forEach(n=>n.area=n.value*scale);
    const out=[]; let free={x:0,y:0,w:W,h:H}, i=0;
    const worst=(row,sum,side)=>{const t=sum/side; let w=0; for(const n of row){const l=n.area/t; w=Math.max(w,Math.max(t/l,l/t));} return w;};
    while(i<nodes.length){
      const side=Math.min(free.w,free.h); let row=[nodes[i]], sum=nodes[i].area, j=i+1;
      while(j<nodes.length && worst([...row,nodes[j]],sum+nodes[j].area,side) <= worst(row,sum,side)){
        row.push(nodes[j]); sum+=nodes[j].area; j++;
      }
      const t=sum/side;
      if(free.w>=free.h){ let y=free.y; for(const n of row){const hh=n.area/t; out.push({...n,x:free.x,y,w:t,h:hh}); y+=hh;} free.x+=t; free.w-=t; }
      else { let x=free.x; for(const n of row){const ww=n.area/t; out.push({...n,x,y:free.y,w:ww,h:t}); x+=ww;} free.y+=t; free.h-=t; }
      i=j;
    }
    return out;
  }
  function treemap(c){
    const W=c.wide?1040:680, H=320, GAP=3;
    const svg=el("svg",{viewBox:`0 0 ${W} ${H}`, role:"img"});
    squarify(c.items,W,H).forEach(t=>{
      const x=t.x+GAP/2,y=t.y+GAP/2,w=Math.max(0,t.w-GAP),h=Math.max(0,t.h-GAP);
      const col=t.color||"#4e79a7", fg=ink(col);
      const rect=el("rect",{x,y,width:w,height:h,rx:5,fill:col});
      bindTip(rect,`<b>${t.label}</b><br>${t.value} benchmarks`);
      svg.appendChild(rect);
      if(w>66 && h>34){
        const cut=Math.floor(w/8);
        const nm=t.label.length>cut ? t.label.slice(0,cut-1)+"…" : t.label;
        svg.appendChild(el("text",{x:x+9,y:y+21,fill:fg,"font-size":"13","font-weight":"600"},nm));
        svg.appendChild(el("text",{x:x+9,y:y+38,fill:fg,"fill-opacity":".85","font-size":"12.5"},String(t.value)));
      }
    });
    return svg;
  }

  // ---- Venn (set relationships: content / domain / both) ----
  function venn(c){
    const v=c.venn, W=680, H=300;
    const svg=el("svg",{viewBox:`0 0 ${W} ${H}`, role:"img"});
    const cy=H/2+4, maxT=Math.max(v.aTotal,v.bTotal,1), R=98;
    const rA=R*Math.sqrt(v.aTotal/maxT), rB=R*Math.sqrt(v.bTotal/maxT);
    const cxA=W/2-rA*0.60, cxB=W/2+rB*0.60;
    svg.appendChild(el("circle",{cx:cxA,cy,r:rA,fill:cvar("s2"),"fill-opacity":.42,stroke:cvar("s2"),"stroke-width":1.5}));
    svg.appendChild(el("circle",{cx:cxB,cy,r:rB,fill:cvar("s3"),"fill-opacity":.42,stroke:cvar("s3"),"stroke-width":1.5}));
    svg.appendChild(el("text",{x:cxA-rA*0.35,y:cy-rA-8,class:"txt","text-anchor":"middle","font-weight":"600"},v.aLabel+" ("+v.aTotal+")"));
    svg.appendChild(el("text",{x:cxB+rB*0.35,y:cy-rB-8,class:"txt","text-anchor":"middle","font-weight":"600"},v.bLabel+" ("+v.bTotal+")"));
    const num=(x,val,lab)=>{
      svg.appendChild(el("text",{x,y:cy+2,class:"txt","text-anchor":"middle","font-size":"24","font-weight":"650"},String(val)));
      svg.appendChild(el("text",{x,y:cy+21,class:"txt-m","text-anchor":"middle"},lab));
    };
    num(cxA-rA*0.44, v.aOnly, v.aLabel.toLowerCase()+" only");
    num((cxA+cxB)/2, v.both, "both");
    num(cxB+rB*0.44, v.bOnly, v.bLabel.toLowerCase()+" only");
    if(v.neither) svg.appendChild(el("text",{x:W/2,y:H-4,class:"txt-m","text-anchor":"middle"},"Neither: "+v.neither));
    return svg;
  }

  // ---- Waffle (unit composition) ----
  function waffle(c){
    const cells=c.cells, n=cells.length, cols=14, gap=5, W=680;
    const size=(W-(cols-1)*gap)/cols, rows=Math.ceil(n/cols), H=rows*size+(rows-1)*gap+2;
    const svg=el("svg",{viewBox:`0 0 ${W} ${H}`, role:"img"});
    const lbl=c.labelByKey||{};
    cells.forEach((k,idx)=>{
      const x=(idx%cols)*(size+gap), y=Math.floor(idx/cols)*(size+gap);
      const rect=el("rect",{x,y,width:size,height:size,rx:4,fill:cvar(k)});
      bindTip(rect,`<b>${lbl[k]||""}</b>`);
      svg.appendChild(rect);
    });
    return svg;
  }

  // ---- Lollipop (a ranking) ----
  function lollipop(c){
    const rows=c.rows, W=680, ROW=34, x0=2, x1=W-34;
    const H=rows.length*ROW+6, max=Math.max(1,...rows.map(r=>r.value));
    const svg=el("svg",{viewBox:`0 0 ${W} ${H}`, role:"img"});
    rows.forEach((r,i)=>{
      const y=i*ROW+ROW/2;
      svg.appendChild(el("text",{x:x0,y:y-7,class:"txt"},r.label));
      const vx=x0+(r.value/max)*(x1-x0), ly=y+7;
      svg.appendChild(el("line",{x1:x0,y1:ly,x2:vx,y2:ly,stroke:cvar("s1"),"stroke-width":2,"stroke-linecap":"round"}));
      svg.appendChild(el("circle",{cx:vx,cy:ly,r:7,fill:"var(--surface)"}));
      const dot=el("circle",{cx:vx,cy:ly,r:5,fill:cvar("s1")});
      bindTip(dot,`<b>${r.label}</b><br>${r.value} ${c.unit||""}`);
      svg.appendChild(dot);
      svg.appendChild(el("text",{x:vx+12,y:ly+4,class:"txt-2"},String(r.value)));
    });
    return svg;
  }

  function legend(items){
    const box=h("div","legend");
    items.forEach(it=>{
      const w=h("div","it"), sw=h("span","sw"); sw.style.background=cvar(it.colorKey);
      w.appendChild(sw); w.appendChild(document.createTextNode(it.label)); box.appendChild(w);
    });
    return box;
  }
  function table(rows, unit){
    const d=h("details","tbl"); d.appendChild(h("summary",null,"Data table"));
    const t=document.createElement("table"), head=document.createElement("tr");
    head.appendChild(h("th",null,"Category")); head.appendChild(h("th","n",unit||"Count")); t.appendChild(head);
    (rows||[]).forEach(r=>{
      const tr=document.createElement("tr");
      tr.appendChild(h("td",null,r.label!=null?r.label:r.name));
      tr.appendChild(h("td","n",r.value!=null?String(r.value):""));
      t.appendChild(tr);
    });
    d.appendChild(t); return d;
  }

  // ---- KPI tiles ----
  const kbox=document.getElementById("kpis");
  D.kpis.forEach(k=>{
    const t=h("div","kpi"+(k.hero?" hero":""));
    t.appendChild(h("div","v",String(k.value)));
    t.appendChild(h("div","l",k.label));
    if(k.sub) t.appendChild(h("div","s",k.sub));
    kbox.appendChild(t);
  });

  // ---- Sections & charts ----
  const wrap=document.getElementById("sections");
  D.sections.forEach(sec=>{
    const s=h("section","grp"), head=h("div","grp-head");
    head.appendChild(h("span","num",sec.n)); head.appendChild(h("h2",null,sec.title));
    head.appendChild(h("span","d",sec.desc)); s.appendChild(head);
    const grid=h("div","grid");
    D.charts.filter(c=>c.section===sec.id).forEach(c=>{
      const card=h("figure","card"+(c.wide?" wide":""));
      const cap=h("figcaption"); cap.appendChild(h("div","t",c.title));
      if(c.sub) cap.appendChild(h("div","st",c.sub));
      card.appendChild(cap);
      const plot=h("div","plot"); card.appendChild(plot);
      let tblRows=c.tableRows;
      if(c.type==="donut"){ plot.appendChild(donut(c)); tblRows=tblRows||c.slices; }
      else if(c.type==="stack"){ plot.appendChild(stack(c)); tblRows=tblRows||c.series.map(se=>({label:se.name,value:se.values.reduce((a,b)=>a+b,0)})); }
      else if(c.type==="treemap"){ plot.appendChild(treemap(c)); tblRows=tblRows||c.items; }
      else if(c.type==="venn"){ plot.appendChild(venn(c)); tblRows=tblRows||[{label:c.venn.aLabel+" only",value:c.venn.aOnly},{label:"Both",value:c.venn.both},{label:c.venn.bLabel+" only",value:c.venn.bOnly},{label:"Neither",value:c.venn.neither}]; }
      else if(c.type==="waffle"){ plot.appendChild(waffle(c)); tblRows=tblRows||c.legend; }
      else if(c.type==="lollipop"){ plot.appendChild(lollipop(c)); tblRows=tblRows||c.rows; }
      else if(c.type==="stat"){
        const box=h("div","statbox");
        box.appendChild(h("div","stat-v",c.value));
        box.appendChild(h("div","stat-l",c.statLabel));
        const meter=h("div","meter"), fill=h("div","meter-fill"); fill.style.width=Math.max(2,c.pct)+"%"; meter.appendChild(fill); box.appendChild(meter);
        if(c.sub2) box.appendChild(h("div","stat-s",c.sub2));
        plot.appendChild(box);
      }
      if(c.type==="donut") card.appendChild(legend(c.slices.map(s=>({label:s.label+" · "+s.value, colorKey:s.colorKey}))));
      if(c.type==="stack") card.appendChild(legend(c.series.map(s=>({label:s.name, colorKey:s.colorKey}))));
      if(c.type==="waffle") card.appendChild(legend(c.legend.map(s=>({label:s.label+" · "+s.value, colorKey:s.colorKey}))));
      if(c.foot) card.appendChild(h("div","foot",c.foot));
      card.appendChild(table(tblRows, c.tableUnit));
      grid.appendChild(card);
    });
    s.appendChild(grid); wrap.appendChild(s);
  });

  // ---- Theme toggle (light is default; toggle flips to dark) ----
  document.getElementById("themeBtn").addEventListener("click",
    () => document.documentElement.classList.toggle("force-dark"));

  // ---- Sidebar: benchmark list + collapse toggle ----
  document.getElementById("sbCount").textContent = D.benchmarks.length;
  const sbList = document.getElementById("sbList");
  D.benchmarks.forEach(b => {
    const it = h("div","sb-it"), dots = h("span","sb-dots");
    b.dots.forEach(d => {
      const dd = h("span","dot"); dd.style.background = cvar(d.colorKey);
      bindTip(dd, `<b>${d.label}</b>`); dots.appendChild(dd);
    });
    it.appendChild(dots);
    const nm = h("span","sb-nm", b.name); nm.title = b.name; it.appendChild(nm);
    sbList.appendChild(it);
  });
  if(window.innerWidth > 1100) document.body.classList.add("sb-open");
  document.getElementById("sbToggle").addEventListener("click",
    () => document.body.classList.toggle("sb-open"));
})();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    generate_dashboard()
