import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
PAPERS_DIR = OUTPUT_DIR / "papers"
PDFS_DIR = OUTPUT_DIR / "pdfs"

# Input CSVs used by the provenance dashboard (src/dashboard.py)
PAPERS_CSV = INPUT_DIR / "papers.csv"
SOURCES_CSV = INPUT_DIR / "Survey Benchmarks LLM+DH - Sources.csv"
DASHBOARD_HTML = OUTPUT_DIR / "provenance.html"
# Per-paper intermediate reports from the persona agents (Ciop / Cip).
# Kept out of PAPERS_DIR so PAPERS_DIR.glob("*.json") only sees final reports.
AGENTS_DIR = PAPERS_DIR / "agents"

# Discovery runs: one folder per run of any route (curated / asreview / agentic),
# each with its manifest.json and raw outputs. See docs/PIPELINE.md §3.
DISCOVERY_DIR = BASE_DIR / "discovery"

PROMPTS_DIR = BASE_DIR / "prompts"
EXTRA_FIELDS_PATH = PROMPTS_DIR / "extra_fields.json"

# LLM backend. "claude" runs the Claude Code CLI headless (`claude -p`), billed
# against the logged-in Claude subscription, no API key. "gemini" uses the Google
# GenAI API with GEMINI_API_KEY. The original 42 extractions (Jul-Aug 2026) were
# made with Gemini; the Google credits ran out in autumn 2026, hence the default.
# Every record stamps the backend and models that produced it (see "extraction"
# in main.py), so a corpus extracted by mixed models stays distinguishable.
LLM_BACKEND = os.getenv("LLM_BACKEND", "claude").strip().lower()

# Gemini configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_PERSONA_MODEL = "gemini-3.5-flash"        # Ciop (humanist) + Cip (technical)
GEMINI_REVIEWER_MODEL = "gemini-3.1-pro-preview" # final reviewer
GEMINI_NARRATIVE_MODEL = "gemini-3.1-pro-preview"

# Claude configuration — full model ids, not aliases, so a record's provenance
# names a fixed model rather than whatever "sonnet" points to on the day.
CLAUDE_PERSONA_MODEL = "claude-sonnet-5-5"   # Ciop + Cip
CLAUDE_REVIEWER_MODEL = "claude-opus-5-5"    # final reviewer
CLAUDE_NARRATIVE_MODEL = "claude-opus-5-5"

if LLM_BACKEND == "claude":
    PERSONA_MODEL, REVIEWER_MODEL, NARRATIVE_MODEL = (
        CLAUDE_PERSONA_MODEL, CLAUDE_REVIEWER_MODEL, CLAUDE_NARRATIVE_MODEL)
elif LLM_BACKEND == "gemini":
    PERSONA_MODEL, REVIEWER_MODEL, NARRATIVE_MODEL = (
        GEMINI_PERSONA_MODEL, GEMINI_REVIEWER_MODEL, GEMINI_NARRATIVE_MODEL)
else:
    raise ValueError(f"LLM_BACKEND must be 'claude' or 'gemini', got {LLM_BACKEND!r}")

UNPAYWALL_EMAIL = "gspinaci@itatti.harvard.edu"
