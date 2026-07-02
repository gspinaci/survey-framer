# Survey Framer

An agentic pipeline that analyzes scientific papers on LLM benchmarks in the Arts & Humanities, extracts structured evaluation data, and synthesizes findings into a narrative survey.

## Features

- **PDF Fetching**: Automatically downloads PDFs from arXiv, DOI resolvers, or direct URLs
- **Text Extraction**: Parses PDF text via PyMuPDF (handles up to 80 pages, 200k tokens)
- **Multi-Agent Analysis**: Two persona agents — **Ciop** (humanist background) and **Cip** (technical background) — each read the full paper and extract structured metrics via Gemini; a **Reviewer** agent adjudicates their reports against the paper text and writes the final report
- **Incremental Extra Fields**: New optional fields can be declared in `prompts/extra_fields.json` at any time; re-running the analyze step extracts only the missing fields for cached papers and merges them in
- **Inclusion Criteria Evaluation**: Automatically assesses papers against 7 criteria:
  - General-purpose benchmark
  - Evaluates generative LLMs (GPT, Llama, Gemini, Claude, Mistral)
  - LLM as primary evaluated system
  - Arts & Humanities data/tasks (ASJC areas)
  - Quantitative performance metrics
  - Published after Mar 2023
  - English language
- **Benchmark Modalities**: Extracts modality types (text, image, video, audio, multimodal) and how they're combined
- **Analytical Tasks**: Identifies specific task types (factual recognition, causal reasoning, numerical reasoning, aesthetic judgment, etc.)
- **Per-Paper Reports**: Generates markdown + JSON for each analyzed paper
- **Narrative Synthesis**: Creates thematic clusters, methodology patterns, and framing options for survey writing

## Setup

1. **Install dependencies:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Get your Gemini API key:**
   - Visit https://aistudio.google.com/apikey

3. **Configure:**
   ```bash
   cp .env.example .env
   # Edit .env and paste your GEMINI_API_KEY
   ```

## Input CSV Format

Place your CSV in `input/` with these columns:

| Column | Purpose | Example |
|--------|---------|---------|
| `Name` | Benchmark or paper title | `"MMLU"` |
| `Year` | Publication year | `2023` |
| `Article URL` | Link to paper (arXiv, DOI, or direct) | `https://arxiv.org/abs/2305.00000` |
| `Resource URL (Benchmark + Dataset)` | Benchmark/data resource link | `https://github.com/openai/MMLU` |
| `Modalities` | Data types (for context) | `"Text"` or `"Image + Text"` |
| `Domain` | Domain area | `"Science"` or `"Art History"` |
| `Evaluation metrics` | Metrics reported | `"Accuracy, F1"` |
| `Humanities?` | Pre-filtered flag | `"Yes"` or `"No"` |
| `ASJC code` | ASJC classification code | `3101` (Visual Arts) |
| Other columns | (optional, preserved in output) | Notes, URLs, etc. |

## Usage

### Run the full pipeline:
```bash
python main.py --input input/papers.csv
```

### Run individual steps:
```bash
# Fetch PDFs only
python main.py --input input/papers.csv --step fetch

# Analyze papers (requires PDFs to exist)
python main.py --input input/papers.csv --step analyze

# Generate narrative synthesis (requires analysis JSON files)
python main.py --input input/papers.csv --step narrative

# Recompute all fields for all papers, ignoring the cache
python main.py --input input/papers.csv --step analyze --force
```

### Add extra extraction fields between runs:
Declare optional fields in `prompts/extra_fields.json`:
```json
{
  "dataset_size": {
    "description": "Number of examples in the benchmark, as an integer; null if not stated",
    "type": "integer|null"
  }
}
```
Then re-run `--step analyze`: fully cached papers log `CACHED`, papers missing the new field log `INCREMENTAL` and only that field is extracted and merged into the existing reports.

## Output

### Per-Paper Reports
Each analyzed paper generates:
- **`output/papers/{paper_id}.md`** — Markdown report with:
  - Benchmark name
  - Publication year
  - Humanities classification (content / domain / both / none)
  - **Benchmark modalities** — Modality types and how they're combined
  - **Analytical tasks** — Task types and their detailed descriptions (e.g., "factual recognition", "economic-grade numerical reasoning")
  - Table of inclusion criteria (Yes/No + explanations)
  - Summary and key findings
  - Relevant ASJC areas

- **`output/papers/{paper_id}.json`** — Final reviewed JSON with full analysis data including:
  - `benchmark_modalities` — List of modality types
  - `benchmark_modalities_explanation` — How modalities are combined
  - `analytical_tasks` — List of task types
  - `analytical_tasks_explanation` — Detailed analysis of task types
  - `review_notes` — Disagreements between Ciop and Cip and how the Reviewer resolved them

- **`output/papers/agents/{paper_id}.ciop.json` / `{paper_id}.cip.json`** — Intermediate persona reports, kept for auditing how the final values were adjudicated

### PDFs
Downloaded PDFs stored in `output/pdfs/` (gitignored)

### Narrative Synthesis
**`output/narrative_synthesis.md`** — Synthesis document with:
1. **Thematic Clusters** — Papers grouped by ASJC area, modality combinations, and analytical task types
2. **Modality & Task Landscape** — Distribution analysis of:
   - Which modality combinations are well-covered vs. underrepresented
   - Dominant analytical task types and their complexity
   - Alignment between tasks and domain requirements
3. **Methodological Patterns** — Recurring evaluation approaches, tested models, and task complexity patterns
4. **Narrative Framing Options** — 3 alternative survey framings with consideration of modalities and task types:
   - For newcomers to AI + Humanities
   - For digital humanities experts
   - For ML researchers
5. **Gaps and Opportunities** — Benchmark gaps by modality, task type, and ASJC area
6. **Suggested Survey Structure** — Proposed table of contents organized by modalities, task types, or domains

## Architecture

- **`config.py`** — Settings, models, paths
- **`src/csv_reader.py`** — Parses input CSV and extracts paper identifiers
- **`src/pdf_fetcher.py`** — Downloads PDFs from arXiv, Unpaywall, or direct URLs
- **`src/pdf_extractor.py`** — Extracts text from PDFs via PyMuPDF
- **`src/analyzer.py`** — Multi-agent analysis: Ciop + Cip personas, then Reviewer adjudication
- **`src/fields.py`** — Field registry: core schema + optional extra fields, missing-field detection
- **`src/llm.py`** — Shared Gemini call helpers and prompt loading
- **`src/report_writer.py`** — Generates per-paper markdown reports
- **`src/narrative.py`** — Synthesizes findings into narrative survey
- **`main.py`** — CLI orchestrator with progress bars, caching, and incremental merge
- **`prompts/`** — Agent prompts (`ciop.txt`, `cip.txt`, `reviewer.txt`, `narrative.txt`) and `extra_fields.json`

## API Details

### Google Gemini
- **Persona agents (Ciop, Cip):** `gemini-3.5-flash`
- **Reviewer & narrative:** `gemini-3.1-pro-preview`
- **Auth:** `GEMINI_API_KEY` in `.env` (from https://aistudio.google.com/apikey)

### Paper Fetching
- **arXiv:** Direct PDF download
- **DOI:** Resolves to PDF via Unpaywall (academic open-access)
- **Direct URLs:** Falls back to generic fetch

## Limitations

- PDFs are truncated at 200k tokens (~80 pages) to fit the model context
- Scanned PDFs (OCR) may fail text extraction — these are skipped
- Requires stable internet for PDF fetching (~1-2 sec delay between requests)
- Gemini API key required for analysis

## Troubleshooting

**"GEMINI_API_KEY not set"**
- Copy `.env.example` to `.env` and fill in your key from https://aistudio.google.com/apikey

**"PDF text too short"**
- Paper likely a scanned PDF (no OCR). Manually upload if needed or skip.

**"No PDF found"**
- arXiv ID, DOI, and URLs all failed. Verify URLs in CSV are correct.

**API 401 error**
- API key invalid or expired. Regenerate from portal.

**API 429 error**
- You've hit your Gemini rate limit or quota — wait and re-run; cached papers are skipped automatically.

## Notes

- Each full paper analysis makes 3 LLM calls (Ciop, Cip, Reviewer); incremental runs are much shorter
- Narrative synthesis uses a separate call
- Progress bars show live status; check logs for errors
- Analyses are cached — re-running analyze skips complete papers and only fills in newly declared fields
