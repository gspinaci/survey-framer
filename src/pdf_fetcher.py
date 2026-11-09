import re
import time
from pathlib import Path

import requests

from config import UNPAYWALL_EMAIL

# Five papers in the census were analysed from an HTML landing page saved under a
# .pdf name, because every source below returned *something* with status 200 and
# nothing checked what it was. The extraction then ran silently over 900-28,000
# characters of page chrome (article Sec. 3.3). Anything not starting with the PDF
# magic bytes is now rejected, so a landing page surfaces as MISSING instead.
PDF_MAGIC = b"%PDF-"


def _is_pdf(data: bytes | None) -> bool:
    return bool(data) and data[:1024].lstrip().startswith(PDF_MAGIC)


def pdf_filename(paper_id: str) -> str:
    """Canonical on-disk name for a paper's PDF.

    Public because the analyze step has to locate these files by the same rule;
    any divergence silently drops papers from the run.
    """
    return re.sub(r"[^\w\-.]", "_", paper_id) + ".pdf"


def _fetch_arxiv_pdf(arxiv_id: str) -> bytes | None:
    clean = arxiv_id.replace("arXiv:", "").strip()
    url = f"https://arxiv.org/pdf/{clean}"
    resp = requests.get(url, timeout=60, allow_redirects=True)
    if resp.status_code == 200 and resp.headers.get("content-type", "").startswith("application/pdf"):
        return resp.content
    return None


def _resolve_doi_to_pdf(doi: str) -> str | None:
    url = f"https://api.unpaywall.org/v2/{doi}?email={UNPAYWALL_EMAIL}"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code != 200:
            return None
        data = resp.json()
        best = data.get("best_oa_location") or {}
        return best.get("url_for_pdf") or best.get("url")
    except Exception:
        return None


def _fetch_from_url(url: str) -> bytes | None:
    try:
        resp = requests.get(url, timeout=60, allow_redirects=True, headers={
            "User-Agent": "survey-framer/1.0 (academic research; mailto:{})".format(UNPAYWALL_EMAIL)
        })
        if resp.status_code == 200:
            return resp.content
    except Exception:
        pass
    return None


def fetch_pdf(paper: dict, output_dir: Path) -> Path | None:
    filename = pdf_filename(paper["id"])
    dest = output_dir / filename
    if dest.exists() and dest.stat().st_size > 1000:
        if _is_pdf(dest.read_bytes()[:1024]):
            return dest
        # A previously saved landing page: discard it and fetch again.
        dest.unlink()

    candidates = []
    # The table's "PDF URL" column wins: it is filled where the catalogued Article
    # URL is a landing page, paywalled or unreachable from here.
    if paper.get("pdf_url"):
        candidates.append(lambda: _fetch_from_url(paper["pdf_url"]))
    if paper.get("arxiv_id"):
        candidates.append(lambda: _fetch_arxiv_pdf(paper["arxiv_id"]))
    if paper.get("doi"):
        def _via_unpaywall():
            pdf_url = _resolve_doi_to_pdf(paper["doi"])
            return _fetch_from_url(pdf_url) if pdf_url else None
        candidates.append(_via_unpaywall)
    if paper.get("article_url"):
        candidates.append(lambda: _fetch_from_url(paper["article_url"]))
    if paper.get("resource_url"):
        candidates.append(lambda: _fetch_from_url(paper["resource_url"]))

    for attempt in candidates:
        pdf_bytes = attempt()
        if _is_pdf(pdf_bytes):
            dest.write_bytes(pdf_bytes)
            time.sleep(1)
            return dest

    return None
