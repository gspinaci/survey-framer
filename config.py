import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
PAPERS_DIR = OUTPUT_DIR / "papers"
PDFS_DIR = OUTPUT_DIR / "pdfs"

BEDROCK_BASE_URL = "https://go.apis.huit.harvard.edu/ais-bedrock-llm/v2"
BEDROCK_MODEL = "us.anthropic.claude-sonnet-4-20250514-v1:0"
BEDROCK_API_KEY = os.getenv("HARVARD_BEDROCK_API_KEY", "")

ANTHROPIC_VERSION = "bedrock-2023-05-31"
MAX_TOKENS = 4096

# Model selection: "bedrock" (default) or "gemini"
MODEL = os.getenv("MODEL", "bedrock")

# Gemini configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-3.5-flash"

UNPAYWALL_EMAIL = "gspinaci@itatti.harvard.edu"
