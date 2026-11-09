"""Mechanical check that a reader's quotes actually occur in the paper.

Deterministic and model-free: the supervisor (an LLM) decides what to do about
an unverified quote, but whether a quote is in the text is not a judgement call.
"""

import difflib
import re
import unicodedata

from src.fields import EVIDENCE_FIELDS, needs_quote
from src.pdf_extractor import PAGE_MARKER_RE

# A quote counts as found when this share of it matches one contiguous span of the
# text after normalisation. Tolerates the small damage PDF extraction does (a
# ligature, a hyphen split across lines, a dropped footnote marker) without
# letting a paraphrase through: paraphrases share words, not long spans.
FUZZY_MIN_SHARE = 0.85

_TRANSLATE = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", "—": "-", "−": "-"})


def normalise(text: str) -> str:
    """Comparable form of paper text and of quotes — the SAME rules on both sides.

    PDF extraction splits words at line ends ("Multi-\\nmodal"), and a reader may
    quote that as "Multi- modal", "Multi-modal" or "Multimodal". Hyphens and
    punctuation are therefore dropped after re-joining split words; what remains
    is the word sequence, which a paraphrase does not reproduce.
    """
    text = PAGE_MARKER_RE.sub(" ", text)
    text = unicodedata.normalize("NFKC", text).translate(_TRANSLATE).lower()
    text = re.sub(r"(\w)-\s+(\w)", r"\1\2", text)   # re-join words split at line ends
    text = text.replace("-", "")                     # multi-modal == multimodal
    text = re.sub(r"[^\w\s]", " ", text)             # quotes, brackets, commas, ligature debris
    return re.sub(r"\s+", " ", text).strip()


def find(quote: str, norm_text: str, matcher: difflib.SequenceMatcher | None = None) -> str:
    """'exact' | 'fuzzy' | 'missing' for one quote against normalised paper text.

    Pass a matcher whose seq2 is already norm_text when checking many quotes
    against the same paper: indexing the text is the expensive part.
    """
    q = normalise(quote)
    if len(q) < 8:
        return "missing"  # too short to be evidence of anything
    if q in norm_text:
        return "exact"
    if matcher is None:
        matcher = difflib.SequenceMatcher(None, autojunk=False)
        matcher.set_seq2(norm_text)
    matcher.set_seq1(q)
    match = matcher.find_longest_match(0, len(q), 0, len(norm_text))
    if match.size >= FUZZY_MIN_SHARE * len(q):
        return "fuzzy"
    return "table" if _in_window(q.split(), norm_text) else "missing"


# Table cells are extracted column by column, so a quoted row ("Llama 2 13B 54.51")
# is rarely contiguous in the text even when every cell is there. Short quotes
# whose every token occurs within one window of the text are accepted as "table".
TABLE_MAX_TOKENS = 12
TABLE_WINDOW = 400


def _in_window(tokens: list[str], norm_text: str) -> bool:
    if not tokens or len(tokens) > TABLE_MAX_TOKENS or not any(t.isdigit() or
                                                             re.fullmatch(r"\d+(?: \d+)*", t) for t in tokens):
        return False
    anchor = max(tokens, key=len)
    for m in re.finditer(r"(?<!\w)" + re.escape(anchor) + r"(?!\w)", norm_text):
        lo, hi = max(0, m.start() - TABLE_WINDOW), m.end() + TABLE_WINDOW
        window = f" {norm_text[lo:hi]} "
        if all(f" {t} " in window for t in tokens):
            return True
    return False


def check_report(report: dict, fields: dict[str, str], text: str) -> dict:
    """Verify every quote in report["evidence"] and list fields lacking support.

    Returns {"quotes": {field: [status, ...]}, "unsupported": [...], "unverified": [...]}:
      unsupported — a field with a non-silent value and no quote at all
      unverified  — a field whose quotes were all 'missing' from the text
    """
    norm = normalise(text)
    matcher = difflib.SequenceMatcher(None, autojunk=False)
    matcher.set_seq2(norm)
    evidence = report.get("evidence") or {}
    quotes, unsupported, unverified = {}, [], []
    for field in (f for f in EVIDENCE_FIELDS if f in fields):
        value = report.get(field)
        items = evidence.get(field) or []
        statuses = [find(i.get("quote", ""), norm, matcher) for i in items if isinstance(i, dict)]
        if statuses:
            quotes[field] = statuses
        if not needs_quote(field, value):
            continue
        if not statuses:
            unsupported.append(field)
        elif all(s == "missing" for s in statuses):
            unverified.append(field)
    return {"quotes": quotes, "unsupported": unsupported, "unverified": unverified}
