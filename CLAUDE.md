# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Important
- Never read/open/process .env file. Any strutural modification should be done on the .env.example file.
- Test and Run the process with the correct venv

---

## Quick Start

**Survey Framer** is an agentic pipeline that analyzes academic papers on LLM benchmarks in the Arts & Humanities. It fetches PDFs, extracts text, analyzes them with Claude via Harvard Bedrock, and synthesizes findings into a narrative survey.

**No setup required** — just provide your Harvard Bedrock API key in `.env` and a CSV of papers in `input/papers.csv`.

---

## Common Commands

```bash

# Run the venv 
source .venv/bin/activate 

# Install dependencies
pip install -r requirements.txt

# Copy environment template and add your API key
cp .env.example .env
# Edit .env: HARVARD_BEDROCK_API_KEY=<your-key-from-portal.apis.huit.harvard.edu>

# Run full pipeline (fetch → analyze → narrative)
python main.py --input input/papers.csv

# Run specific stages
python main.py --input input/papers.csv --step fetch      # Download PDFs only
python main.py --input input/papers.csv --step analyze    # Analyze downloaded PDFs
python main.py --input input/papers.csv --step narrative  # Synthesize narrative
```

**Test with provided examples:**
```bash
python main.py --input input/test_papers.csv
```

---

## Architecture Overview

Three-stage agentic pipeline:

```
CSV Input
   ↓
[FETCH] Download PDFs from arXiv, DOI, or direct URLs
   ↓
[ANALYZE] Extract text, send to Claude via Harvard Bedrock, generate JSON
   ↓
[NARRATIVE] Synthesize per-paper analyses into thematic narrative survey
   ↓
Output: markdown reports + JSON + narrative_synthesis.md
```

**Key Design Patterns:**
- **Modular stages** — Each stage is independent; re-run only what's needed
- **Smart caching** — If `output/papers/{paper_id}.md` exists, that paper is skipped during analysis
- **Graceful degradation** — Missing PDFs don't break the pipeline; they're logged and skipped
- **CSV flexibility** — All CSV columns are preserved and passed to the analyzer as metadata

---

## Module Responsibilities

| File | Purpose | Key Functions |
|------|---------|---|
| `main.py` | CLI entry point, orchestrates 3-stage pipeline | `step_fetch()`, `step_analyze()`, `step_narrative()` |
| `config.py` | API credentials, paths, settings | `BEDROCK_BASE_URL`, `BEDROCK_MODEL`, paths |
| `src/csv_reader.py` | Parse input CSV, extract paper IDs | `read_papers_csv()`, `_extract_arxiv_id()`, `_extract_doi()` |
| `src/pdf_fetcher.py` | Download PDFs from multiple sources | `fetch_pdf()` (tries arXiv → Unpaywall → direct URL) |
| `src/pdf_extractor.py` | Extract text from PDFs | `extract_text()` (PyMuPDF, ~200k token limit) |
| `src/analyzer.py` | Send text to Claude via Bedrock, parse JSON | `analyze_paper()`, `ANALYSIS_PROMPT` |
| `src/report_writer.py` | Generate per-paper markdown report | `write_paper_report()` |
| `src/narrative.py` | Synthesize all analyses into narrative | `generate_narrative()` |

---

## Harvard Bedrock API Integration

The pipeline uses the **Harvard Bedrock LLM gateway** (`https://go.apis.huit.harvard.edu/ais-bedrock-llm/v2`) to call Claude Sonnet.

**Setup:**
1. Get API key from [portal.apis.huit.harvard.edu](https://portal.apis.huit.harvard.edu)
2. Add to `.env`: `HARVARD_BEDROCK_API_KEY=<your-key>`
3. Done — requests automatically use the API key from `config.py`

**Token Budget:**
- **Per-request limit:** 4096 tokens output (set in `config.py`, line 18)
- **Per-paper text limit:** ~80 pages or 200k input tokens (set in `src/pdf_extractor.py`)
- **Cost estimate:** ~$5–15 for 30–50 papers

**Analysis Prompt:**
The `ANALYSIS_PROMPT` in `src/analyzer.py` (lines 7–59) defines the JSON schema. It extracts:
- `benchmark_name`, `publication_year`
- `humanities_role` and explanation
- `benchmark_modalities` and explanation (what data types the benchmark uses)
- `analytical_tasks` and explanation (what kind of analytical work is being tested)
- `inclusion_criteria` — 7 binary checks + explanations
- `summary`, `key_findings`, `relevant_asjc_areas`

CSV metadata is automatically appended to the prompt (see `src/analyzer.py` lines 69–81).

---

## Configuration

**Environment variables** (in `.env`):
```bash
# Model selection: "bedrock" (default) or "gemini"
MODEL=bedrock

# Harvard Bedrock API (for Claude Sonnet analysis)
HARVARD_BEDROCK_API_KEY=<from-portal.apis.huit.harvard.edu>

# Google Gemini API (optional, only if MODEL=gemini)
GEMINI_API_KEY=<from-aistudio.google.com/apikey>
```

**Paths** (in `config.py`):
```python
INPUT_DIR = "input/"              # Where papers.csv lives
OUTPUT_DIR = "output/"            # Root output directory
PAPERS_DIR = "output/papers/"     # Per-paper markdown + JSON
PDFS_DIR = "output/pdfs/"         # Downloaded PDFs
```

**API Settings** (in `config.py`):
```python
# Model selection
MODEL = "bedrock"                 # or "gemini"

# Bedrock (Harvard) configuration
BEDROCK_BASE_URL = "https://go.apis.huit.harvard.edu/ais-bedrock-llm/v2"
BEDROCK_MODEL = "us.anthropic.claude-sonnet-4-20250514-v1:0"

# Gemini configuration
GEMINI_MODEL = "gemini-1.5-flash"

# Token budget
MAX_TOKENS = 4096                 # Output token budget
```

**Switching Models:**
- Use Claude (Bedrock) by default: `MODEL=bedrock` in `.env`
- Switch to Gemini: `MODEL=gemini` in `.env` (requires `GEMINI_API_KEY`)
- Both APIs use the same analysis prompt and return identical JSON structure

---

## Common Development Tasks

### Add a New Extraction Field ⭐ Skill Available
See **[.claude/skills/add-extraction-field.md](.claude/skills/add-extraction-field.md)** for a guided walkthrough (~5 min).

Quick summary: Edit `ANALYSIS_PROMPT` in `src/analyzer.py` (lines 7–59) to add JSON field, then update `src/report_writer.py` to display it.

### Add CSV Columns
1. Create CSV with new columns (see `docs/CSV_GUIDE.md` for format)
2. `csv_reader.py` automatically preserves all columns as a dict
3. Pass to analyzer via the `metadata` parameter (see `main.py` line 71)
4. Access in the prompt as shown in `analyzer.py` lines 69–81

### Modify Report Output Format
1. Open `src/report_writer.py`
2. Edit the markdown template — all sections are there
3. Run `python main.py --input input/papers.csv --step analyze` to regenerate (cached reports won't update)

### Add New Modalities or Task Types
1. Update `ANALYSIS_PROMPT` in `src/analyzer.py` to list new modalities/tasks in the prompt text
2. This guides Claude to recognize and extract them
3. No code changes needed — the prompt controls what's recognized

### Clear Cache and Re-analyze
If you modify the prompt and want to re-analyze all papers:
```bash
rm output/papers/*.md  # Remove cached markdown files
python main.py --input input/papers.csv --step analyze
```
(JSON files are preserved, so you can manually edit them first.)

---

## Testing & Verification

**Test with included sample:**
```bash
python main.py --input input/test_papers.csv
```

Expected output:
- `output/pdfs/` — 5 downloaded PDFs
- `output/papers/` — 5 markdown reports + 5 JSON files
- `output/narrative_synthesis.md` — Final narrative with thematic clusters

**Manual verification:**
1. Check one markdown report: `cat output/papers/2601_07984.md`
2. Check JSON structure: `cat output/papers/2601_07984.json | python -m json.tool`
3. Review narrative: `cat output/narrative_synthesis.md | head -100`

**Debugging a paper:**
- If a paper fails to fetch, check `main.py` output — paper is skipped with reason
- If text extraction fails, check `src/pdf_extractor.py` — will log if PDF is scanned or too short
- If analysis fails, check `config.py` — API key and endpoint are correct

---

## Extension Points

**Add a new PDF source:**
- Edit `src/pdf_fetcher.py` — `fetch_pdf()` tries arXiv → Unpaywall → direct URL
- Add a new source by extending the try/except chain (e.g., ResearchGate, SemanticScholar)

**Extend inclusion criteria:**
- Update `ANALYSIS_PROMPT` to add new criteria to the JSON schema
- Update `src/report_writer.py` to display them in the markdown table

**Add post-processing step:**
- Add a new function in `src/narrative.py` or create `src/postprocess.py`
- Call it from `main.py` after `step_narrative()`

---

## Troubleshooting

**"HARVARD_BEDROCK_API_KEY not set"**
- Ensure `.env` file exists and has `HARVARD_BEDROCK_API_KEY=<value>`
- Run `source .venv/bin/activate` to activate virtual environment
- Verify key format from [portal.apis.huit.harvard.edu](https://portal.apis.huit.harvard.edu)

**"PDF download failed: All sources exhausted"**
- Paper was skipped (expected behavior)
- Verify paper ID in CSV (check arxiv_id or doi extraction in `csv_reader.py`)
- Try the PDF URL directly in a browser to confirm it's accessible

**"PDF text too short, possibly scanned"**
- PDF is an image scan without OCR
- Solution: Skip or manually provide extracted text in input
- These papers are logged and skipped to avoid API waste

**"Request to Bedrock failed: 401"**
- API key is invalid or expired
- Re-generate from [portal.apis.huit.harvard.edu](https://portal.apis.huit.harvard.edu)
- Update `.env` file

**"Max token limit exceeded in request"**
- Increase `MAX_TOKENS` in `config.py` (line 18) if needed
- Or reduce input text length in `src/pdf_extractor.py` (currently ~80 pages, 200k tokens)

**"No papers processed, all cached"**
- All markdown files already exist in `output/papers/`
- Delete them to re-process: `rm output/papers/*.md`
- Or use `--step fetch` or `--step narrative` to run other stages

---

## Reference Documentation

**User Guides:**
- **START_HERE.md** — High-level overview for first-time users
- **QUICKSTART.md** — 5-minute setup and test
- **CSV_GUIDE.md** — Input format and column reference
- **ARCHITECTURE.md** — Deep-dive technical architecture

**Developer Skills:**
- **.claude/skills/add-extraction-field.md** — Guided workflow for adding new analysis fields (~5 min)

**Examples:**
- `output/papers/2601_07984.md` — Sample paper report
- `output/narrative_synthesis.md` — Sample narrative output

---

**Last updated:** May 23, 2026
