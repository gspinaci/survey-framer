#!/usr/bin/env python3
"""Embed paper/article.md into output/findings.html as its own source.

The page carries the *markdown*, not a second rendered copy of it: the article
is parsed and laid out in the browser, and its table of contents is derived
from the same text at load time. There is therefore one authored artefact —
paper/article.md — and nothing to keep in sync by hand.

Two things are not negotiable and are enforced here rather than trusted:

  - The page must stay self-contained and openable from disk. A fetch() of a
    local .md from a file:// document is blocked by the browser, so the source
    has to travel inside the HTML. That is what this script does.
  - The in-page renderer handles a deliberately small subset of markdown.
    Rather than letting an unhandled construct render as literal text, this
    script refuses to embed an article that uses one.

    python scripts/embed_article.py
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import BASE_DIR, OUTPUT_DIR

ARTICLE = BASE_DIR / "paper" / "article.md"
PAGE = OUTPUT_DIR / "findings.html"
START = "<!-- ARTICLE:START -->"
END = "<!-- ARTICLE:END -->"

# Everything the in-page renderer understands. Anything else is a hard error:
# a silently mis-rendered table is worse than a failed build.
UNSUPPORTED = [
    (re.compile(r"^\s*[-*+] ", re.M), "bulleted list"),
    (re.compile(r"^\s*\d+\. ", re.M), "numbered list"),
    (re.compile(r"^\|", re.M), "table"),
    (re.compile(r"^>", re.M), "blockquote"),
    (re.compile(r"^```", re.M), "fenced code block"),
    (re.compile(r"^#{4,} ", re.M), "heading below level 3"),
    (re.compile(r"!\[[^\]]*\]\("), "image"),
    (re.compile(r"(?<!!)\[[^\]]+\]\([^)]+\)"), "inline link"),
]


def check(md: str) -> None:
    found = [name for pattern, name in UNSUPPORTED if pattern.search(md)]
    if found:
        sys.exit(
            "article.md uses constructs the in-page renderer does not handle: "
            + ", ".join(sorted(set(found)))
            + "\nEither avoid them, or extend mdToHtml() in findings.html first."
        )
    # The source lives inside a <script> element; only this sequence can end it.
    if "</script" in md.lower():
        sys.exit("article.md contains '</script' and cannot be embedded verbatim.")


def main() -> None:
    if not ARTICLE.exists():
        sys.exit(f"missing {ARTICLE}")
    md = ARTICLE.read_text(encoding="utf-8")
    check(md)

    page = PAGE.read_text(encoding="utf-8")
    if START not in page or END not in page:
        sys.exit(f"markers {START} / {END} not found in {PAGE}")

    block = (
        '<script type="text/markdown" id="article-source">\n'
        + md.rstrip()
        + "\n</script>"
    )
    before = page[: page.index(START) + len(START)]
    after = page[page.index(END):]
    PAGE.write_text(before + "\n" + block + "\n" + after, encoding="utf-8")

    heads = len(re.findall(r"^## ", md, re.M)) + len(re.findall(r"^### ", md, re.M))
    print(f"embedded {len(md.split()):,} words ({heads} headings) into {PAGE}")
    print("the page now carries the markdown itself; the HTML is built in the browser")


if __name__ == "__main__":
    main()
