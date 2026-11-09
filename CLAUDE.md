# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Important
- Never read/open/process .env file. Any strutural modification should be done on the .env.example file.
- Test and Run the process with the correct venv

---

## Quick Start

**Survey Framer** is an agentic pipeline that analyzes academic papers on LLM benchmarks in the Arts & Humanities. It fetches PDFs, extracts text, analyzes each paper with a multi-agent flow (two persona agents + a reviewer), and synthesizes findings into a narrative survey.

**LLM backend** — `LLM_BACKEND=claude` (default since Nov 2026: Claude Code CLI `claude -p`, uses the logged-in Claude subscription, no API key) or `LLM_BACKEND=gemini` (needs `GEMINI_API_KEY`). The original 42 extractions (Jul–Aug 2026) were made with Gemini; new records carry an `extraction` provenance stamp (backend, models, date) — records without it are Gemini. The Google credits are exhausted.

---

## Common Commands

```bash

# Run the venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template and add your API key
cp .env.example .env
# Optional: LLM_BACKEND=gemini + GEMINI_API_KEY=<key> (default backend is claude, no key needed)

# Run full pipeline (fetch → analyze → narrative)
python main.py --input input/papers.csv

# Run specific stages
python main.py --input input/papers.csv --step fetch      # Download PDFs only
python main.py --input input/papers.csv --step analyze    # Multi-agent analysis of downloaded PDFs
python main.py --input input/papers.csv --step narrative  # Synthesize narrative

# Recompute everything, ignoring cache
python main.py --input input/papers.csv --step analyze --force
```

**Test with provided examples** (the test CSV has no Accept columns, hence the flag):
```bash
python main.py --input input/test_papers.csv --ignore-screening
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
   ├── Ciop (humanist persona, claude-sonnet-5-5 | gemini-3.5-flash)  → output/papers/agents/{id}.ciop.json
   ├── Cip  (technical persona, claude-sonnet-5-5 | gemini-3.5-flash) → output/papers/agents/{id}.cip.json
   └── Reviewer (claude-opus-5-5 | gemini-3.1-pro-preview) adjudicates both reports against the
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

## Census table, screening and provenance

`input/papers.csv` is the census table. Besides the original cataloguing columns it carries provenance columns (appended, never reordered): `ID` (stable, assigned once — `read_papers_csv()` uses it instead of deriving an id), `PDF URL`, `Discovery route` (curated | asreview | agentic), `Discovery run` (→ `discovery/<run_id>/manifest.json`), `Discovery ref`, `Added on`. Read/write it through `src/census_table.py`, which preserves column order and CRLF endings.

- **Screening gate:** `screening_status()` in `src/csv_reader.py` — `included` only when Accept GS and Accept RG are both TRUE. `main.py` fetches and analyses **only included records** (`--ignore-screening` overrides, for tests). New discovery candidates enter as `pending`.
- **Discovery runs:** every run (manual, ASReview, ChatGPT Deep Research, future census-discover skill) lives in `discovery/<run_id>/` with `manifest.json` (route, tool, operator, prompt + sha256, window, raw file hashes, import record) and `raw/`. Import with `python scripts/import_discovery.py discovery/<run_id>` (dry run) then `--apply`; it dedups against the table and records the import in the manifest.
- **Seeds are not discoveries:** curated rows with `Source 2 = ASREVIEW` were ASReview seed records; their route stays `curated`.
- **Findings page:** `report/findings.template.html` (authored) + `paper/article.md` → `python scripts/build_findings.py` → `output/findings.html` (generated, gitignored). Never paste the article into the template.
- Full pipeline definition and open decisions: `docs/PIPELINE.md`.

## Round-based engine (`census.py`) — modular, multi-operator

New work goes through `census.py`, not `main.py` (which remains the legacy three-agent flow). The protocol is `census.toml`: agents with role (reader | supervisor | reviewer | narrator | critic | scout | intake), scope, `count`, model and backend (`claude-cli`, `gemini`, `mock`).

```bash
python census.py status [--all]          # per paper × agent: done / missing / blocked / stale, and by whom
python census.py round init              # freeze protocol (models + prompt hashes) once, then commit round.json
python census.py fetch                   # PDFs of included records
python census.py run ciop [--papers ID…] [--limit N] [--workers N] [--force]
# requires Python 3.11+ (tomllib); CENSUS_OPERATOR=<initials> in .env
python census.py --round test-x run cip --backend mock   # plumbing tests, no model; mock only in test-* rounds
```

- One artifact per (paper, agent): `output/rounds/<round>/papers/<paper>/<agent>.json` → operators running different agents merge in git without conflicts. `--force` archives the old file in `archive/`, never overwrites.
- Each artifact stamps operator (`CENSUS_OPERATOR` in `.env`), backend, model, prompt/RQ hashes, PDF sha256, checks. Artifacts not matching the frozen round are refused/stale; readers that read different PDFs are flagged by `status`.
- Readers (`src/stages/reader.py`) get `prompts/research_questions.md` and must back the fields in `EVIDENCE_FIELDS` (`src/fields.py`) with verbatim quotes; `src/evidence.py` verifies them mechanically (normalised word sequence, so line-break hyphens match and paraphrases do not).
- Stages (`src/stages/`, registry in `__init__.py`; each exposes `scaffold`, `run`, `summary`): **reader**; **supervisor** (`prompts/supervisor.txt`: checks each reading alone, sends it back once — the redo is written as `<reader>.rework1.json`, never over the original — and passes what is still wrong to the reviewer as flags); **reviewer** (`prompts/reviewer_round.txt`: adjudicates the supervised readings → `reviewer.json` with evidence, `confidence`, `needs_human`, `review_notes`). Not yet: narrator, critics, scouts, promotion of round records into `output/papers/`.
- A round freezes model, prompt-file hash and **scaffold hash** (the rendered prompt minus the paper: schema, extra_fields.json, vocabularies, RQs, evidence rules) per agent. `test-*`/`pilot-*` rounds can be re-snapshotted with `census.py round refresh` (artifacts of changed agents become stale); real rounds cannot. Round `2026-11_claude` was frozen on 2026-11-09 after two pilots (`pilot-2026-11`, `pilot-2026-11b`, kept in `output/rounds/` as method record); changing any of its prompts or the schema now means opening a new round.
- Evidence rule: values in `ABSENCE_VALUES` (`src/fields.py`, e.g. `human_baseline_reported = "no"`) record an absence and need no quote; checking that the paper is really silent is the supervisor's job. Table rows are matched by the `table` status in `src/evidence.py`.
- `python scripts/compare_round.py <round> [--diff]` — reader agreement inside the round and agreement with the legacy (Gemini) records.

---

## Module Responsibilities

| File | Purpose | Key Functions |
|------|---------|---|
| `main.py` | CLI entry point, orchestrates pipeline, caching + incremental merge | `step_fetch()`, `step_analyze()`, `step_narrative()` |
| `config.py` | Backend choice, model names, paths | `LLM_BACKEND`, `PERSONA_MODEL`, `REVIEWER_MODEL`, `NARRATIVE_MODEL`, paths |
| `src/csv_reader.py` | Parse input CSV, extract paper IDs | `read_papers_csv()`, `_extract_arxiv_id()`, `_extract_doi()` |
| `src/pdf_fetcher.py` | Download PDFs from multiple sources | `fetch_pdf()` (tries arXiv → Unpaywall → direct URL) |
| `src/pdf_extractor.py` | Extract text from PDFs | `extract_text()` (PyMuPDF, ~200k token limit) |
| `src/analyzer.py` | Multi-agent orchestration per paper | `run_persona()`, `run_reviewer()`, `analyze_paper()` |
| `src/fields.py` | Field registry (core + extras), missing-field detection | `CORE_FIELDS`, `declared_fields()`, `missing_fields()`, `render_schema()` |
| `src/llm.py` | LLM call helpers (claude -p / Gemini backends) + prompt loading | `load_prompt()`, `generate_json()`, `generate_text()` |
| `src/report_writer.py` | Generate per-paper markdown report | `write_paper_report()` |
| `src/narrative.py` | Synthesize all analyses into narrative | `generate_narrative()` |

---

## Prompts

All agent prompts live in `prompts/` and use literal placeholder tokens (`<<SCHEMA>>`, `<<METADATA>>`, `<<PAPER_TEXT>>`, and in the reviewer `<<CIOP_REPORT>>`/`<<CIP_REPORT>>`) substituted via `str.replace` — never `str.format` (the schema's JSON braces would break it).

| File | Agent | Model |
|------|-------|-------|
| `prompts/ciop.txt` | Ciop — humanist persona | `PERSONA_MODEL` |
| `prompts/cip.txt` | Cip — technical persona | `PERSONA_MODEL` |
| `prompts/reviewer.txt` | Final reviewer (adjudicates, adds `review_notes`) | `REVIEWER_MODEL` |
| `prompts/narrative.txt` | Corpus-level synthesis | `NARRATIVE_MODEL` |
| `prompts/extra_fields.json` | Declared optional extraction fields | — |

The extraction schema itself is data: `CORE_FIELDS` in `src/fields.py` (fixed core fields, incl. the 4 inclusion criteria) plus whatever `prompts/extra_fields.json` declares. `src/fields.py` also holds the closed vocabularies — `ANALYTICAL_TASK_VOCAB` (22 task types, rendered into every prompt as `<<TASK_VOCAB>>`) and the enums checked by `check_vocab()` after extraction. See [paper/CHANGES_extraction_schema.md](paper/CHANGES_extraction_schema.md).

---

## Configuration

**Environment variables** (in `.env`):
```bash
LLM_BACKEND=claude            # or gemini
# Google Gemini API key — only for LLM_BACKEND=gemini
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

DISCOVERY_DIR = "discovery/"          # one folder per discovery run: manifest.json + raw/

CLAUDE_PERSONA_MODEL = "claude-sonnet-5-5"   # Ciop + Cip   (LLM_BACKEND=claude)
CLAUDE_REVIEWER_MODEL = "claude-opus-5-5"    # Reviewer
GEMINI_PERSONA_MODEL = "gemini-3.5-flash"    # (LLM_BACKEND=gemini)
GEMINI_REVIEWER_MODEL = "gemini-3.1-pro-preview"
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
python main.py --input input/test_papers.csv --ignore-screening
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

**"LLM_BACKEND=gemini but GEMINI_API_KEY is not set"** / **"`claude` CLI is not on PATH"**
- Default backend is `claude` (needs Claude Code installed and logged in); set `LLM_BACKEND=gemini` + key in `.env` to use Gemini
- `claude -p` must NOT be run with `--bare` (bare mode ignores the OAuth login, i.e. the subscription)

**"PDF is a landing page" / paper MISSING after fetch**
- The fetcher only accepts files starting with `%PDF-` (5 papers were once analysed from HTML landing pages)
- Put a direct PDF link in the record's `PDF URL` column of `input/papers.csv` — tried before every other source; the record's ID does not change
- Ensure `.env` file exists if you use Gemini: `GEMINI_API_KEY=<value>`
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

**Design docs:** `docs/PIPELINE.md` (general pipeline definition: discovery routes, agent roles by scope and number, provenance, trial plan, modular execution §7), `docs/deep_research_prompt.md` (prompt for discovering benchmarks after the May 2026 search cutoff)

**Last updated:** November 9, 2026
