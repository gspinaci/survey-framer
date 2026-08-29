#!/usr/bin/env python3
"""Embed paper/article.md into output/findings.html as its own source.

The page carries the *markdown*, not a second rendered copy of it: the article
is parsed and laid out in the browser, and its table of contents is derived
from the same text at load time. There is therefore one authored artefact —
paper/article.md — and nothing to keep in sync by hand.

Two things are not negotiable and are enforced here rather than trusted:

  - The page must stay self-contained and openable from disk. A fetch() of a
    local .md from a file:// document is blocked by the browser, so the source
    has to travel inside the HTML. That is what this script does.
  - The in-page renderer handles a deliberately small subset of markdown.
    Rather than letting an unhandled construct render as literal text, this
    script refuses to embed an article that uses one.

    python scripts/embed_article.py
"""

import json
import math
import re
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import BASE_DIR, OUTPUT_DIR
from scripts.findings_report import (
    GAP_KIND, INSTRUMENT_KINDS, best_accuracy, load_corpus,
)

ARTICLE = BASE_DIR / "paper" / "article.md"
PAGE = OUTPUT_DIR / "findings.html"
START = "<!-- ARTICLE:START -->"
END = "<!-- ARTICLE:END -->"

# Everything the in-page renderer understands. Anything else is a hard error:
# a silently mis-rendered table is worse than a failed build.
UNSUPPORTED = [
    (re.compile(r"^\s*[-*+] ", re.M), "bulleted list"),
    (re.compile(r"^\s*\d+\. ", re.M), "numbered list"),
    (re.compile(r"^\|", re.M), "table"),
    (re.compile(r"^>", re.M), "blockquote"),
    (re.compile(r"^```", re.M), "fenced code block"),
    (re.compile(r"^#{4,} ", re.M), "heading below level 3"),
    (re.compile(r"!\[[^\]]*\]\("), "image"),
    (re.compile(r"(?<!!)\[[^\]]+\]\([^)]+\)"), "inline link"),
]


SHORT_NAMES = {
    "Massive Multitask Language Understanding (MMLU)": "MMLU",
    "Multi-task Indic Language Understanding Benchmark (MILU)": "MILU",
    "Multilingual Native Reasoning Challenge (MultiNRC)": "MultiNRC",
    "History Seshat Test for LLMs (HiST-LLM)": "HiST-LLM",
    "Comics Cross-Cultural Benchmark (C3B)": "C3B",
    "AdMIRe (Advancing Multimodal Idiomaticity Representation)": "AdMIRe",
    "Humanity's Last Exam (HLE)": "Humanity's Last Exam",
    "Parole Suitability Hearing Corpus (PSH v1.0)": "Parole hearings (PSH)",
    "Cultural Long-form Multilingual Question Answering": "Cultural long-form QA",
    "Evaluating LLMs for Historical Document OCR": "Historical OCR",
    "The RISE Humanities Data Benchmark": "RISE",
    "Text Is Not All You Need: Multimodal Prompting": "Text Is Not All You Need",
    "Finding the Plea: Evaluating the Ability": "Finding the Plea",
    "Leveraging LLMs for Post-OCR Correction of H": "Post-OCR correction",
    "LLM-based Machine Translation and Summar": "Latin MT and summarisation",
    "Automated Translation of Islamic Literat": "Al-Shamela translation",
    "Exploring the Limits of Prompting LLMs w": "Rhetorical fingerprints",
}


def short(name: str) -> str:
    name = str(name)
    for full, brief in SHORT_NAMES.items():
        if name.startswith(full[:34]):
            return brief
    return name


def figure_data() -> dict:
    """Chart data, computed from the corpus rather than transcribed.

    Every figure the article shows is derived here from the same records the
    prose is derived from, so a figure cannot drift from the sentence beside
    it. The coding decisions are imported from findings_report rather than
    restated, for the same reason.
    """
    corpus = load_corpus()

    scored = sorted(((best_accuracy(r), short(r["_name"])) for r in corpus
                     if best_accuracy(r) is not None), reverse=True)
    scores = {
        "items": [{"label": n, "value": round(v, 1)} for v, n in scored],
        "median": round(statistics.median([v for v, _ in scored]), 1),
    }

    sizes = [(r["dataset_size"], short(r["_name"])) for r in corpus if r.get("dataset_size")]
    resolution = {
        "bands": [
            {"label": "resolves 1 point", "note": "10,000+ items",
             "value": sum(1 for n, _ in sizes if n >= 10000), "total": len(sizes)},
            {"label": "resolves 2 points", "note": "2,500+ items",
             "value": sum(1 for n, _ in sizes if n >= 2500), "total": len(sizes)},
            {"label": "resolves 5 points", "note": "400+ items",
             "value": sum(1 for n, _ in sizes if n >= 400), "total": len(sizes)},
        ],
        "small": [{"label": n, "size": sz, "floor": round(100 / math.sqrt(sz), 1)}
                  for sz, n in sorted((s, n) for s, n in sizes if s < 1000)],
    }

    cols = ["yes", "no", "not_stated"]
    rows = ["single_answer", "answer_set", "graded_human_judgment", "not_stated"]
    labels = {"single_answer": "one answer only", "answer_set": "a set of answers",
              "graded_human_judgment": "graded judgement", "not_stated": "not stated"}
    crosstab = {
        "colLabels": ["needs outside knowledge", "does not", "not stated"],
        "rows": [{"label": labels[rk],
                  "cells": [sum(1 for r in corpus
                                if r.get("answer_multiplicity") == rk
                                and r.get("gold_beyond_stimulus") == c) for c in cols]}
                 for rk in rows],
    }

    kind_label = {"format": "answer format", "scoring": "scoring strictness",
                  "depth": "depth tier"}
    gaps = sorted(({"label": short(r["_name"]), "value": r["reported_format_gap_points"],
                    "kind": kind_label[GAP_KIND[r["paper_id"]]],
                    "size": r.get("dataset_size"),
                    "floor": round(100 / math.sqrt(r["dataset_size"]), 1)
                             if r.get("dataset_size") else None}
                   for r in corpus
                   if GAP_KIND.get(r["paper_id"]) in INSTRUMENT_KINDS
                   and r.get("reported_format_gap_points")),
                  key=lambda d: -d["value"])

    human = sorted(({"label": short(r["_name"]), "value": r["human_gap_points"]}
                    for r in corpus if r.get("human_gap_points") is not None),
                   key=lambda d: -d["value"])

    return {"scores": scores, "resolution": resolution, "crosstab": crosstab,
            "gaps": gaps, "human": human}


def check(md: str) -> None:
    found = [name for pattern, name in UNSUPPORTED if pattern.search(md)]
    if found:
        sys.exit(
            "article.md uses constructs the in-page renderer does not handle: "
            + ", ".join(sorted(set(found)))
            + "\nEither avoid them, or extend mdToHtml() in findings.html first."
        )
    # The source lives inside a <script> element; only this sequence can end it.
    if "</script" in md.lower():
        sys.exit("article.md contains '</script' and cannot be embedded verbatim.")


def main() -> None:
    if not ARTICLE.exists():
        sys.exit(f"missing {ARTICLE}")
    md = ARTICLE.read_text(encoding="utf-8")
    check(md)

    page = PAGE.read_text(encoding="utf-8")
    if START not in page or END not in page:
        sys.exit(f"markers {START} / {END} not found in {PAGE}")

    figures = figure_data()
    block = (
        '<script type="text/markdown" id="article-source">\n'
        + md.rstrip()
        + "\n</script>\n"
        + '<script type="application/json" id="article-figures">\n'
        + json.dumps(figures, ensure_ascii=False, indent=1)
        + "\n</script>"
    )
    before = page[: page.index(START) + len(START)]
    after = page[page.index(END):]
    PAGE.write_text(before + "\n" + block + "\n" + after, encoding="utf-8")

    heads = len(re.findall(r"^## ", md, re.M)) + len(re.findall(r"^### ", md, re.M))
    figs = re.findall(r"^\[\[figure:([a-z-]+)\]\]$", md, re.M)
    unknown = [f for f in figs if f not in figures]
    if unknown:
        sys.exit(f"article.md references figures with no data: {unknown}")
    print(f"embedded {len(md.split()):,} words ({heads} headings, "
          f"{len(figs)} figures) into {PAGE}")
    print("the page now carries the markdown itself; the HTML is built in the browser")


if __name__ == "__main__":
    main()
