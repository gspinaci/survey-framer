# Skill: Add New Extraction Field

This guided workflow walks you through adding a new field to the paper analysis pipeline. No code changes needed — fields are declared in a config file and picked up incrementally.

---

## Overview

Extraction fields come in two kinds:
- **Core fields** — the fixed schema in `src/fields.py` (`CORE_FIELDS`). Extracted for every paper on a full run.
- **Extra fields** — optional fields declared in `prompts/extra_fields.json`. They can be added at any time; the next analyze run extracts **only the missing fields** for already-processed papers and merges them into the existing reports (incremental merge). No cache clearing needed.

Every field goes through the full multi-agent flow: Ciop (humanist) and Cip (technical) each extract it, then the Reviewer adjudicates and writes the final value.

**Time:** ~2 minutes | **Difficulty:** Easy | **Files modified:** 1

---

## Step 1: Declare Your Field

Open `prompts/extra_fields.json` and add an entry:

```json
{
  "dataset_size": {
    "description": "Number of examples in the benchmark, as an integer; null if not stated",
    "type": "integer|null"
  },
  "models_evaluated": {
    "description": "List of LLM names evaluated in the paper",
    "type": "list[string]"
  }
}
```

- Use snake_case for the field name.
- `description` is shown verbatim to the agents — be specific, include an example or the expected format.
- `type` is a free-form hint (e.g. `string`, `integer|null`, `list[string]`).

---

## Step 2: Run the Analyze Step

```bash
source .venv/bin/activate
python main.py --input input/test_papers.csv --step analyze
```

Papers that already have all fields log `CACHED`. Papers missing your new field log:

```
INCREMENTAL: <paper_id> — added: dataset_size
```

Only the missing fields are extracted (cheap, short calls); existing values are never recomputed.

---

## Step 3: Verify

1. Check the JSON: `cat output/papers/<id>.json | python -m json.tool` — your field should be present.
2. Check the markdown: `cat output/papers/<id>.md` — the field appears in the **Additional Fields** section (rendered automatically, no template change needed).
3. Persona artifacts in `output/papers/agents/<id>.ciop.json` / `<id>.cip.json` also carry the field, for auditing disagreements.

**Field extracted as `null`?** That counts as done — the paper doesn't state it, and it won't be retried on the next run. If you think the description was just too vague, refine it in `extra_fields.json`, then delete the key from the affected `output/papers/<id>.json` files and re-run.

---

## Step 4: Roll Out to the Full Corpus

```bash
python main.py --input input/papers.csv --step analyze    # incremental over all papers
python main.py --input input/papers.csv --step narrative  # regenerate synthesis
```

---

## Troubleshooting

**Field not in output JSON?**
- Check `prompts/extra_fields.json` is valid JSON (`python -m json.tool prompts/extra_fields.json`)
- Make the description more specific with examples

**Wrong values extracted?**
- Refine the description, delete the key from the paper's JSON, re-run analyze
- Compare the Ciop and Cip artifacts in `output/papers/agents/` to see where the disagreement came from; the final report's `review_notes` explains the Reviewer's resolution

**Need to recompute everything (core fields included)?**
```bash
python main.py --input input/papers.csv --step analyze --force
```

**Changing a CORE field?**
- Edit `CORE_FIELDS` in `src/fields.py` (and `src/report_writer.py` if it needs a dedicated report section), then re-run with `--force`.

---

**Quick Reference:**
- Declare field: `prompts/extra_fields.json`
- Incremental run: `python main.py --input input/papers.csv --step analyze`
- Full recompute: add `--force`
- Core schema: `src/fields.py` | Report template: `src/report_writer.py`
