import re
from pathlib import Path

import pymupdf

PAGE_MARKER = "=== p. {} ==="
PAGE_MARKER_RE = re.compile(r"^=== p\. \d+ ===$", re.M)
MAX_CHARS = 200_000


def extract_text(pdf_path: Path, max_pages: int = 80, page_markers: bool = False) -> str:
    """Plain text of a PDF, capped at MAX_CHARS.

    With page_markers, each page is preceded by a line "=== p. N ===", so a
    reader can say where a quote comes from. The legacy pipeline keeps the
    unmarked text so its prompts stay byte-identical.
    """
    doc = pymupdf.open(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        if i >= max_pages:
            break
        text = page.get_text("text")
        pages.append(f"{PAGE_MARKER.format(i + 1)}\n{text}" if page_markers else text)
    doc.close()
    text = "\n\n".join(pages)
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + "\n\n[TRUNCATED]"
    return text
