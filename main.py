#!/usr/bin/env python3
"""
Survey Framer — Agentic pipeline for analyzing scientific papers
on LLM benchmarks in the Arts & Humanities.

Usage:
    python main.py --input input/papers.csv
    python main.py --input input/papers.csv --step fetch
    python main.py --input input/papers.csv --step analyze
    python main.py --input input/papers.csv --step narrative
"""

import argparse
import json
import sys
from pathlib import Path

from tqdm import tqdm

from config import PAPERS_DIR, PDFS_DIR, OUTPUT_DIR, BEDROCK_API_KEY
from src.csv_reader import read_papers_csv
from src.pdf_fetcher import fetch_pdf
from src.pdf_extractor import extract_text
from src.analyzer import analyze_paper
from src.report_writer import write_paper_report, append_exclusion_note
from src.narrative import generate_narrative


def step_fetch(papers: list[dict]) -> dict[str, Path]:
    print(f"\n--- Fetching {len(papers)} PDFs ---")
    results = {}
    for paper in tqdm(papers, desc="Fetching PDFs"):
        pdf_path = fetch_pdf(paper, PDFS_DIR)
        if pdf_path:
            results[paper["id"]] = pdf_path
            tqdm.write(f"  OK: {paper['id']}")
        else:
            tqdm.write(f"  MISSING: {paper['id']} — no PDF found")
    print(f"Fetched {len(results)}/{len(papers)} PDFs")
    return results


def step_analyze(papers: list[dict], pdf_paths: dict[str, Path]) -> list[dict]:
    print(f"\n--- Analyzing {len(pdf_paths)} papers ---")
    analyses = []
    for paper in tqdm(papers, desc="Analyzing"):
        pid = paper["id"]
        pdf_path = pdf_paths.get(pid)
        if not pdf_path:
            tqdm.write(f"  SKIP: {pid} — no PDF")
            continue

        report_path = PAPERS_DIR / (pid.replace("/", "_") + ".md")
        if report_path.exists():
            tqdm.write(f"  CACHED: {pid}")
            continue

        try:
            text = extract_text(pdf_path)
            if len(text.strip()) < 200:
                tqdm.write(f"  SKIP: {pid} — PDF text too short, possibly scanned")
                continue

            metadata = {
                "modalities": paper.get("modalities", ""),
                "domain": paper.get("domain", ""),
                "evaluation_metrics": paper.get("evaluation_metrics", ""),
                "asjc_code": paper.get("asjc_code", ""),
                "humanities": paper.get("humanities", ""),
            }
            analysis = analyze_paper(text, title=paper.get("name", ""), metadata=metadata)
            analysis["paper_id"] = pid
            analysis["paper_name"] = paper.get("name", "")
            analysis["csv_row"] = paper.get("csv_row", "")
            analyses.append(analysis)

            write_paper_report(paper, analysis, PAPERS_DIR)
            tqdm.write(f"  OK: {pid}")

            analysis_json = PAPERS_DIR / (pid.replace("/", "_") + ".json")
            analysis_json.write_text(json.dumps(analysis, indent=2), encoding="utf-8")

        except Exception as e:
            tqdm.write(f"  ERROR: {pid} — {e}")

    return analyses


REQUIRED_CRITERIA = [
    "evaluates_generative_llm",
    "published_after_march_2023",
]


def step_validate() -> set[str]:
    """Check inclusion criteria for all analyzed papers.

    Appends an exclusion note to the markdown report of any failing paper.
    Returns the set of paper IDs that pass all criteria.
    """
    print("\n--- Validating inclusion criteria ---")
    json_files = sorted(PAPERS_DIR.glob("*.json"))
    passing, failing = [], []

    for jf in json_files:
        analysis = json.loads(jf.read_text(encoding="utf-8"))
        paper_id = analysis.get("paper_id", jf.stem)
        criteria = analysis.get("inclusion_criteria", {})

        failed = [
            (key, criteria[key].get("note", "no note"))
            for key in REQUIRED_CRITERIA
            if not criteria.get(key, {}).get("met", False)
        ]

        if failed:
            append_exclusion_note(paper_id, failed, PAPERS_DIR)
            print(f"  EXCLUDED: {paper_id} — failed {len(failed)} criterion/criteria")
            failing.append(paper_id)
        else:
            print(f"  INCLUDED: {paper_id}")
            passing.append(paper_id)

    print(f"Validation complete: {len(passing)} included, {len(failing)} excluded")
    return set(passing)


def step_narrative(passing_ids: set[str] | None = None) -> None:
    print("\n--- Generating narrative synthesis ---")
    json_files = sorted(PAPERS_DIR.glob("*.json"))
    if not json_files:
        print("No analysis JSON files found. Run the analyze step first.")
        return

    analyses = []
    for jf in json_files:
        a = json.loads(jf.read_text(encoding="utf-8"))
        if passing_ids is None or a.get("paper_id", jf.stem) in passing_ids:
            analyses.append(a)

    if not analyses:
        print("No papers passed inclusion criteria — narrative not generated.")
        return

    print(f"Synthesizing narrative from {len(analyses)} papers...")
    output_path = OUTPUT_DIR / "narrative_synthesis.md"
    generate_narrative(analyses, output_path)
    print(f"Written to {output_path}")


def find_pdfs(papers: list[dict]) -> dict[str, Path]:
    results = {}
    for paper in papers:
        pid = paper["id"]
        for pdf in PDFS_DIR.glob("*.pdf"):
            if pid.replace("/", "_") in pdf.stem:
                results[pid] = pdf
                break
    return results


def main():
    parser = argparse.ArgumentParser(description="Survey Framer pipeline")
    parser.add_argument("--input", required=True, help="Path to CSV with paper DOIs/arXiv IDs")
    parser.add_argument(
        "--step",
        choices=["fetch", "analyze", "narrative", "all"],
        default="all",
        help="Which pipeline step to run (default: all)",
    )
    args = parser.parse_args()

    csv_path = Path(args.input)
    if not csv_path.exists():
        print(f"Error: {csv_path} not found")
        sys.exit(1)

    if args.step in ("analyze", "all") and not BEDROCK_API_KEY:
        print("Error: HARVARD_BEDROCK_API_KEY not set. Copy .env.example to .env and fill in your key.")
        sys.exit(1)

    papers = read_papers_csv(csv_path)
    print(f"Loaded {len(papers)} papers from {csv_path}")

    if args.step in ("fetch", "all"):
        pdf_paths = step_fetch(papers)
    else:
        pdf_paths = find_pdfs(papers)

    if args.step in ("analyze", "all"):
        step_analyze(papers, pdf_paths)

    passing_ids = None
    if args.step in ("narrative", "all"):
        passing_ids = step_validate()
        step_narrative(passing_ids)

    print("\nDone.")


if __name__ == "__main__":
    main()
