import csv
import re
from pathlib import Path


def read_papers_csv(csv_path: Path) -> list[dict]:
    papers = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=2):
            name = row.get("Name", "").strip()
            article_url = row.get("Article URL", "").strip()
            resource_url = row.get("Resource URL (Benchmark + Dataset)", "").strip()
            year = row.get("Year", "").strip()

            arxiv_id = _extract_arxiv_id(article_url) or _extract_arxiv_id(resource_url)
            doi = _extract_doi(article_url) or _extract_doi(resource_url)

            paper_id = arxiv_id or doi or name[:40].replace(" ", "_")

            paper = {
                "id": paper_id,
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
                "specific_source": row.get("Specific source", "").strip(),
                "notes_gs": row.get("Notes GS", "").strip(),
                "notes_rg": row.get("Notes RG", "").strip(),
                "hunter": row.get("Hunter", "").strip(),
                "csv_row": idx,
            }
            papers.append(paper)
    return papers


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
