# Survey Framer

An agentic pipeline that analyzes scientific papers on LLM benchmarks in the Arts & Humanities, extracts structured evaluation data, and synthesizes findings into a narrative survey.

## Features

- **PDF Fetching**: Automatically downloads PDFs from arXiv, DOI resolvers, or direct URLs
- **Text Extraction**: Parses PDF text via PyMuPDF (handles up to 80 pages, 200k tokens)
- **LLM Analysis**: Sends full paper text to Claude via Harvard Bedrock API for structured analysis
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

2. **Get your Harvard API key:**
   - Visit https://portal.apis.huit.harvard.edu
   - Register your app (requires HUIT billing ID from your lab/department)
   - Copy your API key from the portal

3. **Configure:**
   ```bash
   cp .env.example .env
   # Edit .env and paste your HARVARD_BEDROCK_API_KEY
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
```

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

- **`output/papers/{paper_id}.json`** — Structured JSON with full analysis data including:
  - `benchmark_modalities` — List of modality types
  - `benchmark_modalities_explanation` — How modalities are combined
  - `analytical_tasks` — List of task types
  - `analytical_tasks_explanation` — Detailed analysis of task types

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

- **`config.py`** — Settings, API endpoints, paths
- **`src/csv_reader.py`** — Parses input CSV and extracts paper identifiers
- **`src/pdf_fetcher.py`** — Downloads PDFs from arXiv, Unpaywall, or direct URLs
- **`src/pdf_extractor.py`** — Extracts text from PDFs via PyMuPDF
- **`src/analyzer.py`** — Calls Claude via Harvard Bedrock for structured analysis
- **`src/report_writer.py`** — Generates per-paper markdown reports
- **`src/narrative.py`** — Synthesizes findings into narrative survey
- **`main.py`** — CLI orchestrator with progress bars and error handling

## API Details

### Harvard Bedrock (v2)
- **Endpoint:** `https://go.apis.huit.harvard.edu/ais-bedrock-llm/v2`
- **Model:** Claude Sonnet 4 (us.anthropic.claude-sonnet-4-20250514-v1:0)
- **Auth:** `x-api-key` header
- **Pricing:** AWS Bedrock rates, no markup
- **Budget:** Can set per-app limits via email to apihelp@harvard.edu

### Paper Fetching
- **arXiv:** Direct PDF download
- **DOI:** Resolves to PDF via Unpaywall (academic open-access)
- **Direct URLs:** Falls back to generic fetch

## Limitations

- PDFs are truncated at 200k tokens (~80 pages) to fit Claude's context
- Scanned PDFs (OCR) may fail text extraction — these are skipped
- Requires stable internet for PDF fetching (~1-2 sec delay between requests)
- Harvard Bedrock API key required for analysis (pay-as-you-go billing)

## Troubleshooting

**"HARVARD_BEDROCK_API_KEY not set"**
- Copy `.env.example` to `.env` and fill in your key from the Harvard API Portal

**"PDF text too short"**
- Paper likely a scanned PDF (no OCR). Manually upload if needed or skip.

**"No PDF found"**
- arXiv ID, DOI, and URLs all failed. Verify URLs in CSV are correct.

**API 401 error**
- API key invalid or expired. Regenerate from portal.

**API 429 error**
- You've hit your budget limit. Request increase via apihelp@harvard.edu.

## Notes

- Each paper analysis calls Claude once (~2-4 min per paper depending on queue)
- Narrative synthesis uses a separate call (costs ~10-20 input tokens per summary)
- Progress bars show live status; check logs for errors
- JSON analyses are cached — re-running analyze step skips already-analyzed papers
