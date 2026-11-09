import csv
import re
from pathlib import Path


def read_papers_csv(csv_path: Path) -> list[dict]:
    papers = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        first_line = f.readline()
        # Skip leading metadata/empty row if it doesn't contain the expected header
        if "Name" not in first_line and "Article URL" not in first_line:
            start_idx = 3
        else:
            f.seek(0)
            start_idx = 2
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=start_idx):
            name = row.get("Name", "").strip()
            article_url = row.get("Article URL", "").strip()
            resource_url = row.get("Resource URL (Benchmark + Dataset)", "").strip()
            year = row.get("Year", "").strip()

            arxiv_id = _extract_arxiv_id(article_url) or _extract_arxiv_id(resource_url)
            doi = _extract_doi(article_url) or _extract_doi(resource_url)

            # The ID column is authoritative once a record has one. Deriving the id
            # from mutable cells (the URL, or worse the Name) let ids drift whenever
            # a row was edited; IDs are now assigned once, at registration, and the
            # derivation below survives only for rows that predate the column.
            paper_id = (row.get("ID") or "").strip() or arxiv_id or doi or name[:40].replace(" ", "_")

            accept_gs = row.get("Accept GS", "").strip()
            accept_rg = row.get("Accept RG", "").strip()

            paper = {
                "id": paper_id,
                "pdf_url": (row.get("PDF URL") or "").strip(),
                "discovery_route": (row.get("Discovery route") or "").strip(),
                "discovery_run": (row.get("Discovery run") or "").strip(),
                "discovery_ref": (row.get("Discovery ref") or "").strip(),
                "added_on": (row.get("Added on") or "").strip(),
                "screening_status": screening_status(accept_gs, accept_rg),
                "name": name,
                "year": year,
                "article_url": article_url,
                "resource_url": resource_url,
                "arxiv_id": arxiv_id,
                "doi": doi,
                "modalities": row.get("Modalities", "").strip(),
                "domain": row.get("Domain", "").strip(),
                "evaluation_metrics": row.get("Evaluation metrics", "").strip(),
                "humanities": row.get("Humanities?", "").strip(),
                "asjc_code": row.get("ASJC code", "").strip(),
                "source": row.get("Source", "").strip(),
                "source_2": row.get("Source 2", "").strip(),
                "specific_source": row.get("Specific source", "").strip(),
                "notes_gs": row.get("Notes GS", "").strip(),
                "notes_rg": row.get("Notes RG", "").strip(),
                "accept_gs": accept_gs,
                "accept_rg": accept_rg,
                "hunter": row.get("Hunter", "").strip(),
                "csv_row": idx,
            }
            papers.append(paper)
    return papers


def screening_status(accept_gs: str, accept_rg: str) -> str:
    """Where a record stands in the double verification (article Sec. 3.2).

    included  both reviewers TRUE — the only status that is fetched and analysed
    conflict  one TRUE, one FALSE — to be resolved by discussion
    excluded  a FALSE and no TRUE
    pending   at least one decision missing and no FALSE yet (new candidates)
    """
    votes = [v.strip().upper() for v in (accept_gs, accept_rg)]
    if votes == ["TRUE", "TRUE"]:
        return "included"
    if "TRUE" in votes and "FALSE" in votes:
        return "conflict"
    if "FALSE" in votes:
        return "excluded"
    return "pending"


def _extract_arxiv_id(url: str) -> str | None:
    if not url:
        return None
    match = re.search(r'arxiv\.org/(?:abs|pdf)/([\d.]+)', url)
    if match:
        return match.group(1)
    return None


def _extract_doi(url: str) -> str | None:
    if not url:
        return None
    match = re.search(r'doi\.org/([^\s"\'<>]+)', url)
    if match:
        return match.group(1)
    return None
