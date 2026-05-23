import re
import time
from pathlib import Path

import requests

from config import UNPAYWALL_EMAIL


def _safe_filename(paper_id: str) -> str:
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
    filename = _safe_filename(paper["id"])
    dest = output_dir / filename
    if dest.exists() and dest.stat().st_size > 1000:
        return dest

    pdf_bytes = None

    if paper.get("arxiv_id"):
        pdf_bytes = _fetch_arxiv_pdf(paper["arxiv_id"])

    if not pdf_bytes and paper.get("doi"):
        pdf_url = _resolve_doi_to_pdf(paper["doi"])
        if pdf_url:
            pdf_bytes = _fetch_from_url(pdf_url)

    if not pdf_bytes and paper.get("article_url"):
        pdf_bytes = _fetch_from_url(paper["article_url"])

    if not pdf_bytes and paper.get("resource_url"):
        pdf_bytes = _fetch_from_url(paper["resource_url"])

    if pdf_bytes:
        dest.write_bytes(pdf_bytes)
        time.sleep(1)
        return dest

    return None
