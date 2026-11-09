"""Read and write the census table (input/papers.csv) without disturbing it.

The table is edited by hand (and may round-trip through a spreadsheet), so
writes preserve the existing column order and CRLF line endings, and new
columns are only ever appended at the end.
"""

import csv
import re
from pathlib import Path

# Provenance columns, appended after the original cataloguing schema (§3.2 of the
# article). See docs/PIPELINE.md §4.
PROVENANCE_COLUMNS = [
    "ID",               # stable record id, assigned once at registration
    "PDF URL",          # direct full-text link where the Article URL is not one
    "Discovery route",  # curated | asreview | agentic  (";"-joined if found by several)
    "Discovery run",    # run_id(s) -> discovery/<run_id>/manifest.json
    "Discovery ref",    # pointer into the run's raw output, with the original name
    "Added on",         # date the record entered the table
]

ROUTES = ("curated", "asreview", "agentic")


def load(path: Path) -> tuple[list[str], list[dict]]:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def save(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    for col in PROVENANCE_COLUMNS:
        if col not in fieldnames:
            fieldnames = fieldnames + [col]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\r\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def norm_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def derive_id(article_url: str, name: str, taken: set[str]) -> str:
    """Stable id for a new record, from the most durable identifier available:
    arXiv id, ACL Anthology id, DOI, PMLR id, else a slug of the name."""
    url = article_url or ""
    for pattern, fmt in (
        (r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", "{}"),
        (r"aclanthology\.org/(\d{4}\.[a-z0-9-]+\.\d+)", "{}"),
        (r"doi\.org/(10\.[^\s?#]+)", "{}"),
        (r"proceedings\.mlr\.press/(v\d+)/([\w-]+?)(?:\.html?)?$", "pmlr-{}-{}"),
    ):
        m = re.search(pattern, url)
        if m:
            candidate = fmt.format(*m.groups()).rstrip("/")
            break
    else:
        candidate = re.sub(r"[^\w-]+", "_", name.strip())[:40].strip("_")
    base, n = candidate, 2
    while candidate in taken:
        candidate, n = f"{base}-{n}", n + 1
    return candidate
