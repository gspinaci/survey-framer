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

# 8 workers x 3 agents saturated the account's spend-rate limit partway through a
# 42-paper run. Lowered to stay under it; llm.py backs off on 429 as well, but
# throttling here is cheaper than waiting there.
MAX_ANALYZE_WORKERS = 4

_NOOP_NOTE_PREFIXES = ("no significant disagreement", "no disagreement")


def _is_noop_note(note: str) -> bool:
    return note.strip().lower().startswith(_NOOP_NOTE_PREFIXES)

import shutil
from collections import Counter
from datetime import date

from config import (PAPERS_DIR, PDFS_DIR, OUTPUT_DIR, AGENTS_DIR, GEMINI_API_KEY,
                    LLM_BACKEND, PERSONA_MODEL, REVIEWER_MODEL)
from src.csv_reader import read_papers_csv
from src.pdf_fetcher import fetch_pdf, pdf_filename
from src.pdf_extractor import extract_text
from src.analyzer import analyze_paper
from src.fields import check_vocab, declared_fields, missing_fields
from src.report_writer import write_paper_report
from src.narrative import generate_narrative
from src.dashboard import generate_dashboard


def _provenance(fields: list[str]) -> dict:
    """Which backend and models produced a record (or a field increment).

    Records made before this stamp existed (the Jul-Aug 2026 Gemini run) carry no
    "extraction" key; treat its absence as gemini-3.5-flash + gemini-3.1-pro-preview.
    """
    return {
        "backend": LLM_BACKEND,
        "persona_model": PERSONA_MODEL,
        "reviewer_model": REVIEWER_MODEL,
        "date": date.today().isoformat(),
        "fields": fields,
    }


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
            stamp = _provenance(["*"])
            for report in (ciop, cip, analysis):
                report["extraction"] = stamp
            ciop_json.write_text(json.dumps(ciop, indent=2), encoding="utf-8")
            cip_json.write_text(json.dumps(cip, indent=2), encoding="utf-8")
            final_json.write_text(json.dumps(analysis, indent=2), encoding="utf-8")
            tqdm.write(f"  OK: {pid}")
        else:
            # INCREMENTAL run: extract only the newly declared fields and merge
            ciop_new, cip_new, final_new = analyze_paper(text, missing, title=title, metadata=metadata)
            stamp = _provenance(sorted(missing))
            for path, new in ((ciop_json, ciop_new), (cip_json, cip_new), (final_json, final_new)):
                data = json.loads(path.read_text(encoding="utf-8"))
                data.update({k: new[k] for k in missing if k in new})
                data.setdefault("extraction_incremental", []).append(stamp)
                note = new.get("review_notes") if path is final_json else None
                if note and not _is_noop_note(note):
                    data.setdefault("review_notes_incremental", []).append(note)
                path.write_text(json.dumps(data, indent=2), encoding="utf-8")
            analysis = json.loads(final_json.read_text(encoding="utf-8"))
            tqdm.write(f"  INCREMENTAL: {pid} — added: {', '.join(missing)}")

        for warning in check_vocab(analysis):
            tqdm.write(f"  VOCAB: {pid} — {warning}")

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

    # PAPERS_DIR accumulates results from every CSV ever run, so restrict the
    # corpus to the input actually requested — otherwise a leftover analysis from
    # an earlier run (e.g. test_papers.csv) silently joins the narrative.
    csv_ids = None
    if papers:
        csv_ids = {p["id"] for p in papers} | {p["id"].replace("/", "_") for p in papers}

    for jf in json_files:
        analysis = json.loads(jf.read_text(encoding="utf-8"))
        paper_id = analysis.get("paper_id", jf.stem)
        if csv_ids is not None and paper_id not in csv_ids and jf.stem not in csv_ids:
            print(f"  STALE: {paper_id} — not in input CSV, excluded")
            continue
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
    """Locate already-fetched PDFs for an analyze-only run.

    Resolves the exact name the fetcher wrote rather than substring-matching a
    partially sanitized id: ids derived from titles contain characters like ':'
    that become '_' on disk, so the looser match silently dropped 8 of 42
    fetched papers from the analyze step.
    """
    results = {}
    for paper in papers:
        candidate = PDFS_DIR / pdf_filename(paper["id"])
        if candidate.exists():
            results[paper["id"]] = candidate
    return results


def _validate_config(step: str) -> None:
    if step not in ("analyze", "narrative", "all"):
        return
    if LLM_BACKEND == "gemini" and not GEMINI_API_KEY:
        print("Error: LLM_BACKEND=gemini but GEMINI_API_KEY is not set. "
              "Add it to .env, or set LLM_BACKEND=claude.")
        sys.exit(1)
    if LLM_BACKEND == "claude" and not shutil.which("claude"):
        print("Error: LLM_BACKEND=claude but the `claude` CLI is not on PATH. "
              "Install Claude Code and log in, or set LLM_BACKEND=gemini.")
        sys.exit(1)
    print(f"LLM backend: {LLM_BACKEND} (personas: {PERSONA_MODEL}, reviewer: {REVIEWER_MODEL})")


def main():
    parser = argparse.ArgumentParser(description="Survey Framer pipeline")
    parser.add_argument("--input", required=True, help="Path to CSV with paper DOIs/arXiv IDs")
    parser.add_argument(
        "--step",
        choices=["fetch", "analyze", "narrative", "dashboard", "all"],
        default="all",
        help="Which pipeline step to run (default: all)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Recompute all fields for all papers, ignoring the cache",
    )
    parser.add_argument(
        "--ignore-screening",
        action="store_true",
        help="Fetch/analyze every row, not only those accepted by both reviewers "
             "(for test CSVs without Accept columns)",
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

    # Screening gate. The table now also holds discovery candidates awaiting the
    # double verification; nothing is downloaded or sent to a model before both
    # reviewers have accepted it (docs/PIPELINE.md §4).
    by_status = Counter(p["screening_status"] for p in papers)
    print("Screening: " + ", ".join(f"{n} {s}" for s, n in sorted(by_status.items())))
    if args.ignore_screening:
        workset = papers
        print("  --ignore-screening: processing every row")
    else:
        workset = [p for p in papers if p["screening_status"] == "included"]
        held = [p for p in papers if p["screening_status"] != "included"]
        if held:
            print(f"  {len(held)} not included are not fetched or analysed "
                  f"(use --ignore-screening to override)")

    if args.step in ("fetch", "all"):
        pdf_paths = step_fetch(workset)
    else:
        pdf_paths = find_pdfs(workset)

    if args.step in ("analyze", "all"):
        step_analyze(workset, pdf_paths, force=args.force)

    passing_ids = None
    if args.step in ("narrative", "all"):
        passing_ids = step_validate(papers)
        step_narrative(passing_ids)

    if args.step in ("dashboard", "all"):
        print("\n--- Building provenance dashboard ---")
        generate_dashboard(papers)

    print("\nDone.")


if __name__ == "__main__":
    main()
