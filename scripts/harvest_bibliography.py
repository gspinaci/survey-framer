#!/usr/bin/env python3
"""Harvest bibliographic records for the corpus, so the article can cite it.

Neither input/papers.csv nor the extracted reports carry authors or venue --
the CSV has Name, Article URL and Year and nothing else -- so in-text citations
have to be built from scratch. This script resolves each paper against arXiv
(for the arXiv ids), then OpenAlex, then Crossref, and writes one record per
paper to output/bibliography.json.

Design rule, and the reason this is a script rather than a model task: an
unresolved record is reported as unresolved. It is never filled in by guessing.
A fabricated citation is the worst defect this article could carry, so the run
ends with an explicit list of what it could not resolve, for manual checking
against output/pdfs/.

    python scripts/harvest_bibliography.py            # resolve what is missing
    python scripts/harvest_bibliography.py --refresh  # re-resolve everything
"""

import argparse
import csv
import json
import re
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import OUTPUT_DIR, PAPERS_CSV, PAPERS_DIR

BIB_PATH = OUTPUT_DIR / "bibliography.json"
MAILTO = "rgrillo@itatti.harvard.edu"   # OpenAlex/Crossref polite pool
UA = f"survey-framer/1.0 (mailto:{MAILTO})"
PAUSE = 0.4                             # be a good citizen with public APIs


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def arxiv_id_from_url(url: str) -> str | None:
    """The arXiv id in an abs/ or pdf/ URL, without the version suffix."""
    m = re.search(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5})", url or "")
    return m.group(1) if m else None


def surname(author: str) -> str:
    """Last token that looks like a family name.

    Latin-script author strings arrive as "Given Middle Family"; commas mean the
    record already leads with the family name.
    """
    author = author.strip()
    if "," in author:
        return author.split(",")[0].strip()
    parts = [p for p in author.split() if p]
    return parts[-1] if parts else author


def cite_key(authors: list[str], year) -> str | None:
    if not authors or not year:
        return None
    first = surname(authors[0])
    if len(authors) == 1:
        return f"{first}, {year}"
    if len(authors) == 2:
        return f"{first} & {surname(authors[1])}, {year}"
    return f"{first} et al., {year}"


def get(url: str, **kw) -> requests.Response | None:
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=30, **kw)
        return r if r.status_code == 200 else None
    except requests.RequestException:
        return None


# --------------------------------------------------------------------------
# resolvers -- each returns a partial record or None, never a guess
# --------------------------------------------------------------------------

def from_arxiv(arxiv_id: str) -> dict | None:
    r = get("http://export.arxiv.org/api/query",
            params={"id_list": arxiv_id, "max_results": 1})
    if r is None:
        return None
    ns = {"a": "http://www.w3.org/2005/Atom"}
    try:
        entry = ET.fromstring(r.text).find("a:entry", ns)
    except ET.ParseError:
        return None
    if entry is None:
        return None
    title = (entry.findtext("a:title", "", ns) or "").strip()
    if not title:
        return None
    published = entry.findtext("a:published", "", ns) or ""
    doi = entry.findtext("{http://arxiv.org/schemas/atom}doi", None, ns)
    return {
        "authors": [a.findtext("a:name", "", ns).strip()
                    for a in entry.findall("a:author", ns)],
        "title": " ".join(title.split()),
        "year": int(published[:4]) if published[:4].isdigit() else None,
        "venue": "arXiv preprint",
        "doi": doi,
        "url": f"https://arxiv.org/abs/{arxiv_id}",
        "source": "arxiv",
    }


def _openalex_record(w: dict) -> dict:
    loc = (w.get("primary_location") or {}).get("source") or {}
    return {
        "authors": [a["author"]["display_name"]
                    for a in w.get("authorships", []) if a.get("author")],
        "title": w.get("title") or "",
        "year": w.get("publication_year"),
        "venue": loc.get("display_name") or w.get("type") or "",
        "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
        "url": (w.get("primary_location") or {}).get("landing_page_url")
               or w.get("id"),
        "source": "openalex",
    }


def from_openalex_doi(doi: str) -> dict | None:
    r = get(f"https://api.openalex.org/works/doi:{urllib.parse.quote(doi)}",
            params={"mailto": MAILTO})
    return _openalex_record(r.json()) if r else None


def from_openalex_title(title: str) -> dict | None:
    r = get("https://api.openalex.org/works",
            params={"filter": f"title.search:{title}", "per-page": 5, "mailto": MAILTO})
    if r is None:
        return None
    for w in r.json().get("results", []):
        if _title_matches(title, w.get("title") or ""):
            return _openalex_record(w)
    return None


def from_crossref(title: str) -> dict | None:
    r = get("https://api.crossref.org/works",
            params={"query.bibliographic": title, "rows": 5, "mailto": MAILTO})
    if r is None:
        return None
    for it in r.json().get("message", {}).get("items", []):
        cand = " ".join(it.get("title") or [])
        if not _title_matches(title, cand):
            continue
        parts = (it.get("issued") or {}).get("date-parts") or [[None]]
        return {
            "authors": [" ".join(filter(None, (a.get("given"), a.get("family"))))
                        for a in it.get("author", [])],
            "title": cand,
            "year": parts[0][0],
            "venue": " ".join(it.get("container-title") or []),
            "doi": it.get("DOI"),
            "url": it.get("URL"),
            "source": "crossref",
        }
    return None


def _norm(s: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", (s or "").lower()))


def _title_matches(want: str, got: str) -> bool:
    """Token overlap, not equality: the CSV carries benchmark names, not titles.

    A benchmark called "HistBench" appears in a paper titled "HistBench:
    Benchmarking LLMs on Historical Research"; requiring equality would reject
    every correct hit, and requiring nothing would accept every wrong one.
    """
    a, b = _norm(want), _norm(got)
    if not a or not b:
        return False
    return len(a & b) / len(a) >= 0.6


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def load_targets() -> list[dict]:
    """One target per analyzed paper, carrying whatever the CSV already knows."""
    by_id = {}
    with PAPERS_CSV.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            url = (row.get("Article URL") or "").strip()
            name = (row.get("Name") or "").strip()
            key = arxiv_id_from_url(url) or name.replace("/", "_")
            if key:
                by_id[key] = {"csv_name": name, "csv_url": url,
                              "csv_year": (row.get("Year") or "").strip()}

    targets = []
    for jf in sorted(PAPERS_DIR.glob("*.json")):
        rec = json.loads(jf.read_text(encoding="utf-8"))
        pid = rec.get("paper_id", jf.stem)
        csv_row = by_id.get(pid, {})
        targets.append({
            "paper_id": pid,
            "benchmark_name": rec.get("benchmark_name"),
            "paper_name": rec.get("paper_name") or csv_row.get("csv_name"),
            "extracted_year": rec.get("publication_year"),
            "csv_url": csv_row.get("csv_url", ""),
        })
    return targets


def resolve(t: dict) -> dict:
    """Try arXiv, then OpenAlex (by DOI, then title), then Crossref."""
    arxiv_id = arxiv_id_from_url(t["csv_url"]) or (
        t["paper_id"] if re.fullmatch(r"[0-9]{4}\.[0-9]{4,5}", t["paper_id"]) else None)

    if arxiv_id:
        rec = from_arxiv(arxiv_id)
        if rec:
            # An arXiv preprint may have been published since; prefer the
            # version of record when arXiv itself records the DOI.
            if rec.get("doi"):
                time.sleep(PAUSE)
                published = from_openalex_doi(rec["doi"])
                if published and published.get("authors"):
                    published["arxiv_id"] = arxiv_id
                    return published
            rec["arxiv_id"] = arxiv_id
            return rec

    query = t.get("benchmark_name") or t.get("paper_name") or ""
    query = re.sub(r"[_:]+", " ", query).strip()
    if query:
        for fn in (from_openalex_title, from_crossref):
            time.sleep(PAUSE)
            rec = fn(query)
            if rec and rec.get("authors"):
                return rec
    return {}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--refresh", action="store_true",
                    help="re-resolve every paper, ignoring what is cached")
    args = ap.parse_args()

    cached = {}
    if BIB_PATH.exists() and not args.refresh:
        cached = {r["paper_id"]: r for r in json.loads(BIB_PATH.read_text("utf-8"))
                  .get("corpus", [])}

    targets = load_targets()
    print(f"resolving {len(targets)} papers "
          f"({len(cached)} already cached)\n")

    out, unresolved = [], []
    for t in targets:
        prior = cached.get(t["paper_id"])
        if prior and prior.get("authors"):
            out.append(prior)
            continue

        rec = resolve(t)
        merged = {**t, **rec}
        merged["cite_key"] = cite_key(rec.get("authors", []),
                                      rec.get("year") or t.get("extracted_year"))
        out.append(merged)

        if merged.get("cite_key"):
            print(f"  OK   {t['paper_id'][:34]:36} {merged['cite_key']}  [{rec.get('source')}]")
        else:
            unresolved.append(t["paper_id"])
            print(f"  ??   {t['paper_id'][:34]:36} UNRESOLVED")
        time.sleep(PAUSE)

    literature = []
    if BIB_PATH.exists():
        literature = json.loads(BIB_PATH.read_text("utf-8")).get("literature", [])

    BIB_PATH.write_text(json.dumps(
        {"corpus": out, "literature": literature}, indent=2, ensure_ascii=False),
        encoding="utf-8")

    print(f"\nwritten to {BIB_PATH}")
    print(f"resolved {len(out) - len(unresolved)}/{len(out)}")
    if unresolved:
        print("\nUNRESOLVED -- check these by hand against output/pdfs/ before citing:")
        for pid in unresolved:
            print(f"  {pid}")

    thin = [r["paper_id"] for r in out
            if r.get("authors") and len(r["authors"]) == 1]
    if thin:
        print("\nSINGLE-AUTHOR records -- plausible, but worth a glance:")
        for pid in thin:
            print(f"  {pid}")


if __name__ == "__main__":
    main()
