# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Important
- Never read/open/process .env file. Any strutural modification should be done on the .env.example file.
- Test and Run the process with the correct venv

---

## Quick Start

**Survey Framer** is an agentic pipeline that analyzes academic papers on LLM benchmarks in the Arts & Humanities. It fetches PDFs, extracts text, analyzes each paper with a multi-agent flow (two persona agents + a reviewer, via Google Gemini), and synthesizes findings into a narrative survey.

**No setup required** — just provide your Gemini API key in `.env` and a CSV of papers in `input/papers.csv`.

---

## Common Commands

```bash

# Run the venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template and add your API key
cp .env.example .env
# Edit .env: GEMINI_API_KEY=<your-key-from-aistudio.google.com/apikey>

# Run full pipeline (fetch → analyze → narrative)
python main.py --input input/papers.csv

# Run specific stages
python main.py --input input/papers.csv --step fetch      # Download PDFs only
python main.py --input input/papers.csv --step analyze    # Multi-agent analysis of downloaded PDFs
python main.py --input input/papers.csv --step narrative  # Synthesize narrative

# Recompute everything, ignoring cache
python main.py --input input/papers.csv --step analyze --force
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
[ANALYZE] Extract text, then per paper:
   ├── Ciop (humanist persona, gemini-3.5-flash)  → output/papers/agents/{id}.ciop.json
   ├── Cip  (technical persona, gemini-3.5-flash) → output/papers/agents/{id}.cip.json
   └── Reviewer (gemini-3.1-pro-preview) adjudicates both reports against the
       paper text → final output/papers/{id}.json + {id}.md
   ↓
[NARRATIVE] Synthesize per-paper analyses into thematic narrative survey
   ↓
Output: markdown reports + JSON + narrative_synthesis.md
```

**Key Design Patterns:**
- **Multi-agent analysis** — Ciop (humanist lens) and Cip (ML/NLP lens) extract the same fields independently; the Reviewer resolves disagreements against the paper text and records them in `review_notes`
- **Incremental extra fields** — optional fields declared in `prompts/extra_fields.json` can be added between runs; cached papers only extract the missing fields and merge them in (core fields never recomputed)
- **Modular stages** — Each stage is independent; re-run only what's needed
- **Smart caching** — A paper is skipped when its final JSON + both persona JSONs exist and no declared field is missing
- **Graceful degradation** — Missing PDFs don't break the pipeline; they're logged and skipped
- **CSV flexibility** — All CSV columns are preserved and passed to the agents as metadata

---

## Module Responsibilities

| File | Purpose | Key Functions |
|------|---------|---|
| `main.py` | CLI entry point, orchestrates pipeline, caching + incremental merge | `step_fetch()`, `step_analyze()`, `step_narrative()` |
| `config.py` | API key, model names, paths | `GEMINI_PERSONA_MODEL`, `GEMINI_REVIEWER_MODEL`, paths |
| `src/csv_reader.py` | Parse input CSV, extract paper IDs | `read_papers_csv()`, `_extract_arxiv_id()`, `_extract_doi()` |
| `src/pdf_fetcher.py` | Download PDFs from multiple sources | `fetch_pdf()` (tries arXiv → Unpaywall → direct URL) |
| `src/pdf_extractor.py` | Extract text from PDFs | `extract_text()` (PyMuPDF, ~200k token limit) |
| `src/analyzer.py` | Multi-agent orchestration per paper | `run_persona()`, `run_reviewer()`, `analyze_paper()` |
| `src/fields.py` | Field registry (core + extras), missing-field detection | `CORE_FIELDS`, `declared_fields()`, `missing_fields()`, `render_schema()` |
| `src/llm.py` | Shared Gemini call helpers + prompt loading | `load_prompt()`, `generate_json()`, `generate_text()` |
| `src/report_writer.py` | Generate per-paper markdown report | `write_paper_report()` |
| `src/narrative.py` | Synthesize all analyses into narrative | `generate_narrative()` |

---

## Prompts

All agent prompts live in `prompts/` and use literal placeholder tokens (`<<SCHEMA>>`, `<<METADATA>>`, `<<PAPER_TEXT>>`, and in the reviewer `<<CIOP_REPORT>>`/`<<CIP_REPORT>>`) substituted via `str.replace` — never `str.format` (the schema's JSON braces would break it).

| File | Agent | Model |
|------|-------|-------|
| `prompts/ciop.txt` | Ciop — humanist persona | `gemini-3.5-flash` |
| `prompts/cip.txt` | Cip — technical persona | `gemini-3.5-flash` |
| `prompts/reviewer.txt` | Final reviewer (adjudicates, adds `review_notes`) | `gemini-3.1-pro-preview` |
| `prompts/narrative.txt` | Corpus-level synthesis | `gemini-3.1-pro-preview` |
| `prompts/extra_fields.json` | Declared optional extraction fields | — |

The extraction schema itself is data: `CORE_FIELDS` in `src/fields.py` (fixed core fields, incl. the 7 inclusion criteria) plus whatever `prompts/extra_fields.json` declares.

---

## Configuration

**Environment variables** (in `.env`):
```bash
# Google Gemini API key
GEMINI_API_KEY=<from-aistudio.google.com/apikey>
```

**Settings** (in `config.py`):
```python
INPUT_DIR = "input/"                  # Where papers.csv lives
OUTPUT_DIR = "output/"                # Root output directory
PAPERS_DIR = "output/papers/"         # Final per-paper markdown + JSON
AGENTS_DIR = "output/papers/agents/"  # Intermediate Ciop/Cip reports
PDFS_DIR = "output/pdfs/"             # Downloaded PDFs
PROMPTS_DIR = "prompts/"
EXTRA_FIELDS_PATH = "prompts/extra_fields.json"

GEMINI_PERSONA_MODEL = "gemini-3.5-flash"        # Ciop + Cip
GEMINI_REVIEWER_MODEL = "gemini-3.1-pro-preview" # Reviewer
GEMINI_NARRATIVE_MODEL = "gemini-3.1-pro-preview"
```

---

## Common Development Tasks

### Add a New Extraction Field ⭐ Skill Available
See **[.claude/skills/add-extraction-field.md](.claude/skills/add-extraction-field.md)** for a guided walkthrough (~2 min).

Quick summary: declare the field in `prompts/extra_fields.json` (name + description + type), then re-run `--step analyze`. Cached papers extract only the missing field (INCREMENTAL) and it appears automatically in the JSON and in the report's "Additional Fields" section — no code changes.

### Add CSV Columns
1. Create CSV with new columns (see `docs/CSV_GUIDE.md` for format)
2. `csv_reader.py` automatically preserves all columns as a dict
3. Pass to the agents via the `metadata` parameter (see `main.py`)
4. Metadata is injected into all three agent prompts via `build_metadata_block()` in `src/analyzer.py`

### Modify Report Output Format
1. Open `src/report_writer.py`
2. Edit the markdown template — all sections are there
3. Markdown is a pure render of the final JSON: delete the `.md` files (or just re-run an incremental step) to regenerate

### Change a Core Field or Persona Behavior
- Core schema: edit `CORE_FIELDS` in `src/fields.py`, then re-run with `--force`
- Persona emphasis: edit `prompts/ciop.txt` / `prompts/cip.txt` / `prompts/reviewer.txt`

### Clear Cache and Re-analyze
```bash
python main.py --input input/papers.csv --step analyze --force
```
Or delete a single paper's artifacts (`output/papers/{id}.json`, `output/papers/agents/{id}.*.json`) to recompute just that paper.

---

## Testing & Verification

**Test with included sample:**
```bash
python main.py --input input/test_papers.csv
```

Expected output:
- `output/pdfs/` — downloaded PDFs
- `output/papers/` — final markdown reports + JSON files
- `output/papers/agents/` — Ciop/Cip intermediate JSONs per paper
- `output/narrative_synthesis.md` — Final narrative with thematic clusters

**Manual verification:**
1. Check one markdown report: `cat output/papers/<id>.md` — should include a "Reviewer Notes" section
2. Check JSON structure: `cat output/papers/<id>.json | python -m json.tool` — includes `review_notes`
3. Compare persona reports: `output/papers/agents/<id>.ciop.json` vs `<id>.cip.json`
4. Review narrative: `cat output/narrative_synthesis.md | head -100`

**Debugging a paper:**
- If a paper fails to fetch, check `main.py` output — paper is skipped with reason
- If text extraction fails, check `src/pdf_extractor.py` — will log if PDF is scanned or too short
- If an agent returns malformed JSON, `src/llm.py` strips fences and falls back to first-object `raw_decode`; a hard failure logs `ERROR: <id>` and the paper simply retries on the next run (no partial cache is written)

---

## Extension Points

**Add a new PDF source:**
- Edit `src/pdf_fetcher.py` — `fetch_pdf()` tries arXiv → Unpaywall → direct URL
- Add a new source by extending the try/except chain (e.g., ResearchGate, SemanticScholar)

**Add a new persona agent:**
- Create `prompts/<name>.txt` following the ciop/cip token skeleton
- Call `run_persona("<name>", ...)` in `src/analyzer.py` and pass its report to the reviewer

**Add post-processing step:**
- Add a new function in `src/narrative.py` or create `src/postprocess.py`
- Call it from `main.py` after `step_narrative()`

---

## Troubleshooting

**"GEMINI_API_KEY not set"**
- Ensure `.env` file exists and has `GEMINI_API_KEY=<value>`
- Run `source .venv/bin/activate` to activate virtual environment
- Get a key from [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

**"PDF download failed: All sources exhausted"**
- Paper was skipped (expected behavior)
- Verify paper ID in CSV (check arxiv_id or doi extraction in `csv_reader.py`)
- Try the PDF URL directly in a browser to confirm it's accessible

**"PDF text too short, possibly scanned"**
- PDF is an image scan without OCR
- Solution: Skip or manually provide extracted text in input
- These papers are logged and skipped to avoid API waste

**JSON parse ERROR on a paper**
- Occasional model output glitch; just re-run `--step analyze` — only failed papers recompute

**"No papers processed, all cached"**
- Every paper has all declared fields. Declare new fields in `prompts/extra_fields.json` for an incremental run, or use `--force` to recompute

---

## Reference Documentation

**User Guides:**
- **START_HERE.md** — High-level overview for first-time users
- **QUICKSTART.md** — 5-minute setup and test
- **CSV_GUIDE.md** — Input format and column reference
- **ARCHITECTURE.md** — Deep-dive technical architecture

**Developer Skills:**
- **.claude/skills/add-extraction-field.md** — Declare new analysis fields in extra_fields.json (~2 min)

**Examples:**
- `output/papers/HiST-LLM.md` — Sample paper report
- `output/narrative_synthesis.md` — Sample narrative output

---

**Last updated:** July 2, 2026
