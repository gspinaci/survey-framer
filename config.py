import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
PAPERS_DIR = OUTPUT_DIR / "papers"
PDFS_DIR = OUTPUT_DIR / "pdfs"
# Per-paper intermediate reports from the persona agents (Ciop / Cip).
# Kept out of PAPERS_DIR so PAPERS_DIR.glob("*.json") only sees final reports.
AGENTS_DIR = PAPERS_DIR / "agents"

PROMPTS_DIR = BASE_DIR / "prompts"
EXTRA_FIELDS_PATH = PROMPTS_DIR / "extra_fields.json"

# Gemini configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_PERSONA_MODEL = "gemini-3.5-flash"        # Ciop (humanist) + Cip (technical)
GEMINI_REVIEWER_MODEL = "gemini-3.1-pro-preview" # final reviewer
GEMINI_NARRATIVE_MODEL = "gemini-3.1-pro-preview"

UNPAYWALL_EMAIL = "gspinaci@itatti.harvard.edu"
