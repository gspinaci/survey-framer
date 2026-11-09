#!/usr/bin/env python3
"""One-off (2026-11-09): add provenance columns to the records catalogued before
the columns existed, reconstructing them from what the table and git already hold.

  ID               the id the pipeline has always derived for the row (arXiv id,
                   DOI or name slug), frozen so existing analyses keep joining
  PDF URL          the direct links found on 2026-11-09 for the five papers that
                   had been analysed from landing pages and the three excluded for
                   want of full text (previously input/pdf_overrides.json)
  Discovery route  'asreview' if Source or Hunter says ASREVIEW (the 12 records
                   the ASReview screening surfaced, added 2026-06-16); 'curated'
                   otherwise. A curated row with Source 2 = ASREVIEW stays
                   'curated': those rows were in the table from 2026-05-23, before
                   the screening, and were loaded into ASReview as seed records
                   (prior relevant), so finding them again there is not an
                   independent discovery. The mark is kept in Discovery ref.
  Discovery run    the reconstructed run for that route (discovery/<run_id>/)
  Discovery ref    the cells the route was read from
  Added on         date of the first commit of input/papers.csv containing the
                   row (matched by Article URL or by normalised Name) — an upper
                   bound on when the record was catalogued

    python scripts/backfill_provenance.py            # dry run: print what would change
    python scripts/backfill_provenance.py --apply    # write input/papers.csv
"""

import csv
import io
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import BASE_DIR, PAPERS_CSV
from src import census_table
from src.csv_reader import read_papers_csv

RUNS = {"curated": "2026-05_curated-sources", "asreview": "2026-05-22_asreview"}

PDF_URLS = {
    "CHVM-1K": "https://arxiv.org/pdf/2501.02039",
    "HiST-LLM": "https://ora.ox.ac.uk/objects/uuid:0efbba43-bd9b-47d0-90f1-56fe136e61a6/files/s5712m879q",
    "SimpleQA": "https://arxiv.org/pdf/2411.04368",
    "DRISHTIKON:_A_Multimodal_Multilingual_Be": "https://aclanthology.org/2025.emnlp-main.68.pdf",
    "The_RISE_Humanities_Data_Benchmark": "https://storage.googleapis.com/jnl-up-j-johd-files/journals/1/articles/481/69832b58619a1.pdf",
    "EXAMS-V:_A_Multi-Discipline_Multilingual": "https://arxiv.org/pdf/2403.10378",
    "IRLBench:_A_Multi-modal,_Culturally_Grou": "https://arxiv.org/pdf/2505.13498",
    "MultiBLiMP_1.0:_A_Massively_Multilingual": "https://arxiv.org/pdf/2504.02768",
}


def git_history() -> list[tuple[str, str, set[str], set[str]]]:
    """(commit, date, article urls, normalised names) per version of the table, oldest first."""
    rel = PAPERS_CSV.relative_to(BASE_DIR).as_posix()
    log = subprocess.run(
        ["git", "log", "--reverse", "--format=%h %ad", "--date=short", "--", rel],
        capture_output=True, text=True, check=True, cwd=BASE_DIR,
    ).stdout.split("\n")
    versions = []
    for line in filter(None, log):
        commit, day = line.split()
        text = subprocess.run(["git", "show", f"{commit}:{rel}"], capture_output=True,
                              text=True, check=True, cwd=BASE_DIR).stdout
        lines = text.splitlines()
        start = next(i for i, l in enumerate(lines) if "Name" in l)
        rows = list(csv.DictReader(io.StringIO("\n".join(lines[start:]))))
        urls = {r.get("Article URL", "").strip() for r in rows} - {""}
        names = {census_table.norm_name(r.get("Name", "")) for r in rows} - {""}
        versions.append((commit, day, urls, names))
    return versions


def main() -> None:
    apply = "--apply" in sys.argv
    fieldnames, rows = census_table.load(PAPERS_CSV)
    if "ID" in fieldnames and any(r.get("ID") for r in rows):
        sys.exit("ID column already populated — backfill has run; nothing to do")
    papers = read_papers_csv(PAPERS_CSV)  # same order as rows; ids derived the old way
    history = git_history()

    for row, paper in zip(rows, papers):
        found_by_asreview = "ASREVIEW" in (row.get("Source", "") + row.get("Hunter", "")).upper()
        routes = ["asreview"] if found_by_asreview else ["curated"]
        url, name = row.get("Article URL", "").strip(), census_table.norm_name(row.get("Name", ""))
        added = next((d for _, d, urls, names in history if url in urls or name in names), "")

        row["ID"] = paper["id"]
        row["PDF URL"] = PDF_URLS.get(paper["id"], "")
        row["Discovery route"] = ";".join(routes)
        row["Discovery run"] = ";".join(RUNS[r] for r in routes)
        ref = [f"Source: {row['Source'].strip()}" if row.get("Source", "").strip() else "Source: not recorded"]
        if row.get("Source 2", "").strip().upper() == "ASREVIEW" and not found_by_asreview:
            ref.append("Source 2: ASREVIEW (also in the ASReview pool as a seed record)")
        elif row.get("Source 2", "").strip():
            ref.append(f"Source 2: {row['Source 2'].strip()}")
        if row.get("Hunter", "").strip():
            ref.append(f"Hunter: {row['Hunter'].strip()}")
        row["Discovery ref"] = "; ".join(ref)
        row["Added on"] = added
        print(f"{paper['csv_row']:>3} {row['Discovery route']:17} {added:10} "
              f"{row['PDF URL'][:25]:25} {paper['id'][:40]}")

    assert len({r["ID"] for r in rows}) == len(rows), "duplicate IDs"
    if apply:
        census_table.save(PAPERS_CSV, fieldnames, rows)
        print(f"\nwrote {len(rows)} rows with provenance to {PAPERS_CSV}")
    else:
        print("\ndry run — re-run with --apply to write")


if __name__ == "__main__":
    main()
