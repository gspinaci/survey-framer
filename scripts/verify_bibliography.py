#!/usr/bin/env python3
"""Check every harvested record against the paper's own PDF.

Resolving by title overlap finds the right paper most of the time and the wrong
one some of the time -- a benchmark name is not a title, and OpenAlex will
happily return an unrelated 2018 work whose title shares enough tokens. The
only ground truth available locally is the PDF the pipeline already downloaded,
so this compares each record against the first page of that file.

Two independent signals, both computed from the first 3000 characters:
  - does the resolved first-author surname appear?
  - how much of the resolved title's vocabulary appears?

Neither is conclusive alone (scanned PDFs, author lists on a later page), so
the script classifies rather than deletes, and prints what a human must check.

    python scripts/verify_bibliography.py
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import OUTPUT_DIR, PDFS_DIR
from src.pdf_extractor import extract_text
from src.pdf_fetcher import pdf_filename

BIB_PATH = OUTPUT_DIR / "bibliography.json"
STOP = {"the", "a", "an", "of", "for", "and", "on", "in", "to", "with", "is",
        "are", "we", "our", "as", "at", "by", "from", "not", "all", "you",
        "need", "using", "via", "towards", "toward", "can", "do", "does"}


def tokens(s: str) -> set[str]:
    return {t for t in re.findall(r"[a-z]{3,}", (s or "").lower()) if t not in STOP}


def head_of_pdf(paper_id: str) -> str | None:
    """First page of the paper's PDF, located by the fetcher's own naming rule.

    pdf_filename() is the single source of truth for the on-disk name: ids
    derived from titles contain ':' which becomes '_', and re-deriving that
    here instead of calling the function is exactly the divergence that once
    dropped 8 of 42 papers from the analyze step without an error.
    """
    cand = PDFS_DIR / pdf_filename(paper_id)
    if not cand.exists():
        return None
    try:
        return extract_text(cand)[:3000].lower()
    except Exception:
        return None


def main() -> None:
    data = json.loads(BIB_PATH.read_text(encoding="utf-8"))
    verdicts = {"confirmed": [], "suspect": [], "unresolved": [], "no_pdf": []}

    for rec in data["corpus"]:
        pid = rec["paper_id"]
        if not rec.get("authors"):
            verdicts["unresolved"].append((pid, "no record resolved"))
            rec["verification"] = "unresolved"
            continue

        head = head_of_pdf(pid)
        if head is None:
            verdicts["no_pdf"].append((pid, rec.get("cite_key")))
            rec["verification"] = "no_pdf"
            continue

        first = rec["authors"][0].split()[-1].lower() if rec["authors"] else ""
        author_hit = bool(first) and first in head
        want = tokens(rec.get("title", ""))
        overlap = len(want & tokens(head)) / len(want) if want else 0.0

        year_ok = True
        if rec.get("year") and rec.get("extracted_year"):
            year_ok = abs(int(rec["year"]) - int(rec["extracted_year"])) <= 1

        rec["verification_detail"] = {
            "author_in_pdf": author_hit,
            "title_overlap": round(overlap, 2),
            "year_consistent": year_ok,
        }

        if author_hit and overlap >= 0.6 and year_ok:
            rec["verification"] = "confirmed"
            verdicts["confirmed"].append((pid, rec["cite_key"]))
        else:
            rec["verification"] = "suspect"
            why = []
            if not author_hit:
                why.append(f"first author '{first}' not on page 1")
            if overlap < 0.6:
                why.append(f"title overlap {overlap:.0%}")
            if not year_ok:
                why.append(f"year {rec.get('year')} vs extracted {rec.get('extracted_year')}")
            verdicts["suspect"].append((pid, rec.get("cite_key"), "; ".join(why)))

    BIB_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"CONFIRMED   {len(verdicts['confirmed'])}")
    print(f"SUSPECT     {len(verdicts['suspect'])}")
    print(f"UNRESOLVED  {len(verdicts['unresolved'])}")
    print(f"NO PDF      {len(verdicts['no_pdf'])}")

    if verdicts["suspect"]:
        print("\n--- SUSPECT: do not cite before checking the PDF ---")
        for pid, key, why in verdicts["suspect"]:
            print(f"  {pid[:40]:42} {str(key):30} {why}")
    for label in ("unresolved", "no_pdf"):
        if verdicts[label]:
            print(f"\n--- {label.upper()} ---")
            for row in verdicts[label]:
                print(f"  {row[0][:40]:42} {row[1]}")


if __name__ == "__main__":
    main()
