from pathlib import Path

import fitz  # PyMuPDF


def extract_text(pdf_path: Path, max_pages: int = 80) -> str:
    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        if i >= max_pages:
            break
        pages.append(page.get_text("text"))
    doc.close()
    text = "\n\n".join(pages)
    if len(text) > 200_000:
        text = text[:200_000] + "\n\n[TRUNCATED]"
    return text
