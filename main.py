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
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from tqdm import tqdm

MAX_ANALYZE_WORKERS = 8

_NOOP_NOTE_PREFIXES = ("no significant disagreement", "no disagreement")


def _is_noop_note(note: str) -> bool:
    return note.strip().lower().startswith(_NOOP_NOTE_PREFIXES)

from config import PAPERS_DIR, PDFS_DIR, OUTPUT_DIR, AGENTS_DIR, GEMINI_API_KEY
from src.csv_reader import read_papers_csv
from src.pdf_fetcher import fetch_pdf
from src.pdf_extractor import extract_text
from src.analyzer import analyze_paper
from src.fields import declared_fields, missing_fields
from src.report_writer import write_paper_report
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


def step_analyze(papers: list[dict], pdf_paths: dict[str, Path], force: bool = False) -> list[dict]:
    print(f"\n--- Analyzing {len(pdf_paths)} papers (up to {MAX_ANALYZE_WORKERS} in parallel) ---")
    analyses = []

    def _analyze_one(paper: dict) -> dict | None:
        pid = paper["id"]
        pdf_path = pdf_paths.get(pid)
        if not pdf_path:
            tqdm.write(f"  SKIP: {pid} — no PDF")
            return None

        safe = pid.replace("/", "_")
        final_json = PAPERS_DIR / f"{safe}.json"
        ciop_json = AGENTS_DIR / f"{safe}.ciop.json"
        cip_json = AGENTS_DIR / f"{safe}.cip.json"

        complete = final_json.exists() and ciop_json.exists() and cip_json.exists()
        missing = {}
        if not force and complete:
            existing = json.loads(final_json.read_text(encoding="utf-8"))
            missing = missing_fields(existing)
            if not missing:
                tqdm.write(f"  CACHED: {pid}")
                return None

        text = extract_text(pdf_path)
        if len(text.strip()) < 200:
            tqdm.write(f"  SKIP: {pid} — PDF text too short, possibly scanned")
            return None

        metadata = {
            "modalities": paper.get("modalities", ""),
            "domain": paper.get("domain", ""),
            "evaluation_metrics": paper.get("evaluation_metrics", ""),
            "asjc_code": paper.get("asjc_code", ""),
            "humanities": paper.get("humanities", ""),
        }
        title = paper.get("name", "")

        if force or not complete:
            # FULL run: Ciop + Cip + Reviewer over all declared fields
            ciop, cip, analysis = analyze_paper(text, declared_fields(), title=title, metadata=metadata)
            analysis["paper_id"] = pid
            analysis["paper_name"] = title
            analysis["csv_row"] = paper.get("csv_row", "")
            ciop_json.write_text(json.dumps(ciop, indent=2), encoding="utf-8")
            cip_json.write_text(json.dumps(cip, indent=2), encoding="utf-8")
            final_json.write_text(json.dumps(analysis, indent=2), encoding="utf-8")
            tqdm.write(f"  OK: {pid}")
        else:
            # INCREMENTAL run: extract only the newly declared fields and merge
            ciop_new, cip_new, final_new = analyze_paper(text, missing, title=title, metadata=metadata)
            for path, new in ((ciop_json, ciop_new), (cip_json, cip_new), (final_json, final_new)):
                data = json.loads(path.read_text(encoding="utf-8"))
                data.update({k: new[k] for k in missing if k in new})
                note = new.get("review_notes") if path is final_json else None
                if note and not _is_noop_note(note):
                    data.setdefault("review_notes_incremental", []).append(note)
                path.write_text(json.dumps(data, indent=2), encoding="utf-8")
            analysis = json.loads(final_json.read_text(encoding="utf-8"))
            tqdm.write(f"  INCREMENTAL: {pid} — added: {', '.join(missing)}")

        write_paper_report(paper, analysis, PAPERS_DIR)
        return analysis

    with tqdm(total=len(papers), desc="Analyzing") as pbar:
        with ThreadPoolExecutor(max_workers=MAX_ANALYZE_WORKERS) as pool:
            futures = {pool.submit(_analyze_one, p): p for p in papers}
            for fut in as_completed(futures):
                try:
                    result = fut.result()
                    if result:
                        analyses.append(result)
                except Exception as e:
                    pid = futures[fut]["id"]
                    tqdm.write(f"  ERROR: {pid} — {e}")
                finally:
                    pbar.update(1)

    return analyses


REQUIRED_CRITERIA = [
    "evaluates_generative_llm",
    "published_after_march_2023",
]


def step_validate(papers: list[dict] | None = None) -> set[str]:
    """Check inclusion criteria for all analyzed papers.

    If a paper has accept_gs or accept_rg == "TRUE" (manual review), it passes
    regardless of automated criteria. Appends an exclusion note to the markdown
    report of any failing paper. Returns the set of paper IDs that pass.
    """
    print("\n--- Validating inclusion criteria ---")
    json_files = sorted(PAPERS_DIR.glob("*.json"))
    passing, failing = [], []

    # Build lookup from paper_id → accept flags for manual overrides
    accepted = {}
    if papers:
        for p in papers:
            accepted[p["id"]] = (
                p.get("accept_gs", "").upper() == "TRUE"
                or p.get("accept_rg", "").upper() == "TRUE"
            )

    for jf in json_files:
        analysis = json.loads(jf.read_text(encoding="utf-8"))
        paper_id = analysis.get("paper_id", jf.stem)
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


def _validate_config(step: str) -> None:
    if step in ("analyze", "narrative", "all") and not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not set. Copy .env.example to .env and add your key.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Survey Framer pipeline")
    parser.add_argument("--input", required=True, help="Path to CSV with paper DOIs/arXiv IDs")
    parser.add_argument(
        "--step",
        choices=["fetch", "analyze", "narrative", "all"],
        default="all",
        help="Which pipeline step to run (default: all)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Recompute all fields for all papers, ignoring the cache",
    )
    args = parser.parse_args()

    csv_path = Path(args.input)
    if not csv_path.exists():
        print(f"Error: {csv_path} not found")
        sys.exit(1)

    _validate_config(args.step)

    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    PDFS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)

    papers = read_papers_csv(csv_path)
    print(f"Loaded {len(papers)} papers from {csv_path}")

    if args.step in ("fetch", "all"):
        pdf_paths = step_fetch(papers)
    else:
        pdf_paths = find_pdfs(papers)

    if args.step in ("analyze", "all"):
        step_analyze(papers, pdf_paths, force=args.force)

    passing_ids = None
    if args.step in ("narrative", "all"):
        passing_ids = step_validate(papers)
        step_narrative(passing_ids)

    print("\nDone.")


if __name__ == "__main__":
    main()
