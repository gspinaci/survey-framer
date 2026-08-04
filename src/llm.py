"""Shared Gemini call helpers and prompt loading."""

import json
import re
import time

import google.genai as genai

from config import GEMINI_API_KEY, OUTPUT_DIR, PROMPTS_DIR

# A malformed reply wastes the whole paper (three agent calls), so retry before
# giving up. A resample clears the truncations described below.
JSON_ATTEMPTS = 3

# 6 of 34 reviewer replies came back clipped mid-object — always right after
# review_notes, the last field written, with the closing brace missing. The
# reports run ~3.5-4.5k characters, so the ceiling is set well clear of that
# rather than left to the API default.
MAX_OUTPUT_TOKENS = 8192

# The narrative synthesizes the whole corpus into a multi-section survey, so it
# needs far more room than a single paper's report.
MAX_NARRATIVE_TOKENS = 32768

MALFORMED_DIR = OUTPUT_DIR / "malformed_replies"

# Gemini enforces a spend-rate limit per billing tier, and 8 workers hitting it at
# once exhausted it mid-run: 12 of 42 papers died on 429 with no retry, because the
# parse-retry loop below never covered transport errors. Backoff is generous
# because the limit is a *rate* — waiting is the only remedy, and a paper lost to
# a 429 costs three calls to redo.
RATE_LIMIT_ATTEMPTS = 5
RATE_LIMIT_BACKOFF_S = 20


def _is_retryable(error: Exception) -> bool:
    """True for transient transport failures worth waiting out."""
    text = str(error)
    return any(
        marker in text
        for marker in ("429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE", "500", "INTERNAL")
    )


def load_prompt(name: str) -> str:
    return (PROMPTS_DIR / f"{name}.txt").read_text(encoding="utf-8")


def _parse_json_reply(reply: str) -> dict:
    try:
        return json.loads(reply)
    except json.JSONDecodeError:
        pass
    cleaned = reply.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1]
        cleaned = cleaned.rsplit("```", 1)[0]
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Model appended extra content after the JSON — take the first object
        start = cleaned.index("{")
        obj, _ = json.JSONDecoder().raw_decode(cleaned[start:])
        return obj


def _dump_malformed(reply: str, model: str, label: str, error: Exception) -> None:
    """Persist an unparseable reply so the failure can be diagnosed offline."""
    try:
        MALFORMED_DIR.mkdir(parents=True, exist_ok=True)
        safe = re.sub(r"[^\w\-.]", "_", label)
        dest = MALFORMED_DIR / f"{safe}.{model}.{int(time.time())}.txt"
        dest.write_text(f"# {type(error).__name__}: {error}\n\n{reply}", encoding="utf-8")
    except OSError:
        pass  # diagnostics must never mask the original parse failure


def _generate(client, model: str, prompt: str, config: dict, label: str):
    """One generate_content call, waiting out rate limits and transient 5xx."""
    last_error: Exception | None = None
    for attempt in range(1, RATE_LIMIT_ATTEMPTS + 1):
        try:
            return client.models.generate_content(model=model, contents=prompt, config=config)
        except Exception as e:  # SDK wraps transport errors in several types
            if not _is_retryable(e) or attempt == RATE_LIMIT_ATTEMPTS:
                raise
            last_error = e
            delay = RATE_LIMIT_BACKOFF_S * (2 ** (attempt - 1))
            print(f"  RETRY: {label} — {type(e).__name__}, waiting {delay}s "
                  f"(attempt {attempt}/{RATE_LIMIT_ATTEMPTS})", flush=True)
            time.sleep(delay)
    raise last_error


def generate_json(prompt: str, model: str, label: str = "reply") -> dict:
    client = genai.Client(api_key=GEMINI_API_KEY)
    config = {
        "response_mime_type": "application/json",
        "max_output_tokens": MAX_OUTPUT_TOKENS,
    }
    last_error: Exception | None = None
    for attempt in range(1, JSON_ATTEMPTS + 1):
        response = _generate(client, model, prompt, config, label)
        try:
            return _parse_json_reply(response.text or "")
        except (json.JSONDecodeError, ValueError) as e:
            last_error = e
            _dump_malformed(response.text or "", model, f"{label}.attempt{attempt}", e)
    raise last_error


def generate_text(prompt: str, model: str) -> str:
    """Free-form generation (the corpus narrative).

    The explicit ceiling is precautionary, not a fix for an observed clip: unlike
    generate_json, a truncated narrative would still be valid text and would pass
    silently into the output file rather than raising, so the limit is stated
    rather than inherited from the API default.
    """
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = _generate(
        client, model, prompt, {"max_output_tokens": MAX_NARRATIVE_TOKENS}, "narrative"
    )
    return response.text
