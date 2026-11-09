"""Shared LLM call helpers and prompt loading.

Two interchangeable backends behind generate_json / generate_text, selected by
config.LLM_BACKEND: "gemini" (Google GenAI API) and "claude" (Claude Code CLI in
headless mode, using the logged-in subscription). Prompts, parsing and the
malformed-reply dump are shared, so the two differ only in the model.
"""

import json
import re
import subprocess
import tempfile
import time

from config import GEMINI_API_KEY, LLM_BACKEND, OUTPUT_DIR, PROMPTS_DIR

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


# --- Claude backend ----------------------------------------------------------
#
# `claude -p` is Claude Code's headless mode. Flags, and why each is there:
#   --tools ""              pure text-in/JSON-out: no file, shell or web access,
#                           so the model answers from the prompt alone, exactly
#                           like the Gemini call it replaces
#   --system-prompt         replaces Claude Code's coding-agent system prompt
#   --setting-sources ""    ignore user/project settings, hooks and permissions
#   --strict-mcp-config     no MCP servers
#   --no-session-persistence  don't litter the session history with 100+ calls
# Not --bare: bare mode never reads the OAuth login, i.e. it would require an
# API key and bypass the subscription this backend exists to use.
# cwd is a neutral temp dir so no project CLAUDE.md is auto-discovered.
CLAUDE_SYSTEM_PROMPT = (
    "You are a careful research assistant extracting structured information "
    "from academic papers for a systematic survey. Follow the instructions in "
    "the user message exactly. When asked for JSON, reply with the JSON object "
    "only: no markdown fences, no commentary."
)
# A reviewer call carries the full paper plus two reports (~30-60k tokens) and
# may think at length before answering; ten minutes is generous but bounded.
CLAUDE_TIMEOUT_S = 600

# Errors that clear by waiting a little. The subscription's own usage cap is NOT
# in this list: it resets on a scale of hours, so retrying would only burn time —
# it is surfaced as a hard error instead (see _claude_complete).
_CLAUDE_TRANSIENT = ("overloaded", "529", "500", "502", "503", "timed out", "ECONNRESET")


def _claude_complete(prompt: str, model: str, label: str) -> str:
    cmd = [
        "claude", "-p",
        "--model", model,
        "--output-format", "json",
        "--tools", "",
        "--system-prompt", CLAUDE_SYSTEM_PROMPT,
        "--setting-sources", "",
        "--strict-mcp-config",
        "--no-session-persistence",
    ]
    last_error: Exception | None = None
    for attempt in range(1, RATE_LIMIT_ATTEMPTS + 1):
        try:
            proc = subprocess.run(
                cmd, input=prompt, capture_output=True, text=True,
                timeout=CLAUDE_TIMEOUT_S, cwd=tempfile.gettempdir(),
            )
            try:
                envelope = json.loads(proc.stdout)
            except json.JSONDecodeError:
                raise RuntimeError(
                    f"claude -p exited {proc.returncode}: {(proc.stderr or proc.stdout)[:500]}")
            if envelope.get("is_error") or envelope.get("subtype") != "success":
                raise RuntimeError(f"claude -p error: {str(envelope.get('result'))[:500]}")
            return envelope.get("result") or ""
        except (RuntimeError, subprocess.TimeoutExpired) as e:
            message = str(e)
            if "limit" in message.lower() and "reset" in message.lower():
                raise RuntimeError(f"Claude usage limit reached — {message}") from e
            transient = isinstance(e, subprocess.TimeoutExpired) or any(
                m in message for m in _CLAUDE_TRANSIENT)
            if not transient or attempt == RATE_LIMIT_ATTEMPTS:
                raise
            last_error = e
            delay = RATE_LIMIT_BACKOFF_S * (2 ** (attempt - 1))
            print(f"  RETRY: {label} — {message[:80]}, waiting {delay}s "
                  f"(attempt {attempt}/{RATE_LIMIT_ATTEMPTS})", flush=True)
            time.sleep(delay)
    raise last_error


# --- Gemini backend ----------------------------------------------------------

def _gemini_complete(prompt: str, model: str, label: str, max_tokens: int,
                     json_mode: bool) -> str:
    import google.genai as genai  # imported lazily: only this backend needs it

    client = genai.Client(api_key=GEMINI_API_KEY)
    config = {"max_output_tokens": max_tokens}
    if json_mode:
        config["response_mime_type"] = "application/json"
    response = _generate(client, model, prompt, config, label)
    return response.text or ""


def _complete(prompt: str, model: str, label: str, max_tokens: int, json_mode: bool,
              backend: str | None = None) -> str:
    """backend: a backend *kind* ("claude-cli" | "gemini"); None = config.LLM_BACKEND
    (the legacy main.py flow). The round-based engine always passes it explicitly,
    from the agent's entry in census.toml."""
    kind = backend or ("claude-cli" if LLM_BACKEND == "claude" else "gemini")
    if kind == "claude-cli":
        return _claude_complete(prompt, model, label)
    if kind == "gemini":
        return _gemini_complete(prompt, model, label, max_tokens, json_mode)
    raise ValueError(f"backend {kind!r} cannot be called for text (mock is handled by the stage)")


def generate_json(prompt: str, model: str, label: str = "reply", backend: str | None = None) -> dict:
    last_error: Exception | None = None
    for attempt in range(1, JSON_ATTEMPTS + 1):
        reply = _complete(prompt, model, label, MAX_OUTPUT_TOKENS, json_mode=True, backend=backend)
        try:
            return _parse_json_reply(reply)
        except (json.JSONDecodeError, ValueError) as e:
            last_error = e
            _dump_malformed(reply, model, f"{label}.attempt{attempt}", e)
    raise last_error


def generate_text(prompt: str, model: str) -> str:
    """Free-form generation (the corpus narrative).

    The explicit ceiling is precautionary, not a fix for an observed clip: unlike
    generate_json, a truncated narrative would still be valid text and would pass
    silently into the output file rather than raising, so the limit is stated
    rather than inherited from the API default. (The Claude backend has no
    per-call ceiling flag; its model default is far above the narrative's size.)
    """
    return _complete(prompt, model, "narrative", MAX_NARRATIVE_TOKENS, json_mode=False)
