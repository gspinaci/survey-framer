# Skill: Add New Extraction Field

This guided workflow walks you through adding a new field to the paper analysis pipeline. Follow the steps to extract a new piece of data from papers.

---

## Overview

When you want Survey Framer to extract additional information from papers (e.g., "benchmark_year", "dataset_size", "model_family"), you need to:
1. Update the JSON schema in the Claude prompt
2. Update the markdown report template
3. Test with a sample paper

**Time:** ~5 minutes | **Difficulty:** Easy | **Files modified:** 2

---

## Step 1: Decide Your Field

**What do you want to extract?**

Examples:
- `benchmark_year` — The year the benchmark was introduced
- `dataset_size` — Number of examples in the benchmark
- `primary_language` — Main language of the benchmark
- `model_family` — Which model families were evaluated

Choose a field name using snake_case (e.g., `my_field_name`).

**Field name:** `________________`

---

## Step 2: Update the Analysis Prompt

Open `src/analyzer.py` and find the `ANALYSIS_PROMPT` (lines 7–59).

**Location to edit:**
```python
# src/analyzer.py, lines 7-59
ANALYSIS_PROMPT = """\
...
{
  "benchmark_name": "Name of the benchmark",
  ...
  "key_findings": "Main quantitative results or takeaways",
  "relevant_asjc_areas": ["list of matched ASJC humanities areas"]
}
...
"""
```

**What to do:**
1. Find the JSON schema in the prompt (between `{` and `}`)
2. Add your new field as a JSON key-value pair
3. Include a brief instruction for Claude about what to extract

**Example: Adding "benchmark_year"**

Before:
```json
"key_findings": "Main quantitative results or takeaways",
"relevant_asjc_areas": ["list of matched ASJC humanities areas"]
```

After:
```json
"benchmark_year": 2024,
"key_findings": "Main quantitative results or takeaways",
"relevant_asjc_areas": ["list of matched ASJC humanities areas"]
```

**Do this now:**
- [ ] Open `src/analyzer.py`
- [ ] Find `ANALYSIS_PROMPT` (line 7)
- [ ] Add your field to the JSON schema with a sample value or type hint
- [ ] Save the file

---

## Step 3: Update the Report Template

Open `src/report_writer.py` and add your field to the markdown report.

**Location to edit:**
```python
# src/report_writer.py
def write_paper_report(paper, analysis, output_dir):
    # Find where markdown is generated
    # Look for lines that write analysis fields to the report
```

**What to do:**
1. Find where other analysis fields are written to the markdown (look for `analysis["benchmark_name"]`, etc.)
2. Add a section for your new field
3. Format it as markdown (heading + value)

**Example: Adding "benchmark_year"**

If other fields look like:
```python
report += f"**Publication year (from analysis):** {analysis.get('publication_year', 'N/A')}\n"
```

Add something like:
```python
if analysis.get("benchmark_year"):
    report += f"**Benchmark year:** {analysis['benchmark_year']}\n"
```

**Do this now:**
- [ ] Open `src/report_writer.py`
- [ ] Find where other analysis fields are written (search for `analysis.get` or `analysis[`)
- [ ] Add your field to the report markdown
- [ ] Save the file

---

## Step 4: Test with a Sample Paper

Clear the cache and re-analyze one paper to verify your field was extracted.

```bash
# Remove cached reports (keep one paper's JSON for testing)
rm output/papers/*.md

# Run analysis again
python main.py --input input/test_papers.csv --step analyze
```

**Verify:**
1. Check the markdown report: `cat output/papers/2601_07984.md`
   - Look for your new field in the report
2. Check the JSON: `cat output/papers/2601_07984.json | python -m json.tool`
   - Look for your new field in the JSON output
3. If the field is missing, Claude didn't extract it — check your prompt wording

**Do this now:**
- [ ] Run: `rm output/papers/*.md`
- [ ] Run: `python main.py --input input/test_papers.csv --step analyze`
- [ ] Verify field appears in markdown and JSON output

---

## Step 5: Refine the Prompt (If Needed)

If your field wasn't extracted or the value seems wrong:

1. **Too vague?** Make the prompt instruction more specific
   - ❌ Bad: `"year": 2024`
   - ✅ Good: `"year": "Publication or preprint year (e.g., 2024)"`

2. **Extraction failed?** Add an example or type hint
   - ❌ Bad: `"language": "..."`
   - ✅ Good: `"primary_language": "English, Chinese, Multilingual, etc."`

3. **Wrong format?** Specify the expected format
   - ❌ Bad: `"size": "number of examples"`
   - ✅ Good: `"num_examples": 10000` or `"size": "large (>10k), medium (1k-10k), small (<1k)"`

**To iterate:**
1. Edit `ANALYSIS_PROMPT` in `src/analyzer.py`
2. Delete cached markdown: `rm output/papers/*.md`
3. Re-run: `python main.py --input input/test_papers.csv --step analyze`
4. Check output again

**Do this now (if needed):**
- [ ] Review Claude's extraction in the JSON
- [ ] If incorrect, refine the prompt and re-test
- [ ] Repeat until satisfied

---

## Step 6: Re-analyze All Papers

Once your field works, re-analyze the full paper set:

```bash
# Remove all cached markdown (keeps JSON)
rm output/papers/*.md

# Re-analyze everything
python main.py --input input/papers.csv --step analyze

# Re-generate narrative (uses updated analyses)
python main.py --input input/papers.csv --step narrative
```

**Do this now:**
- [ ] Run: `rm output/papers/*.md`
- [ ] Run: `python main.py --input input/papers.csv --step analyze`
- [ ] Run: `python main.py --input input/papers.csv --step narrative`

---

## Troubleshooting

**Field not in output JSON?**
- Check the prompt syntax — JSON must be valid
- Verify field name doesn't have spaces or special characters
- Claude may not extract if the instruction is too vague

**Field in JSON but not in markdown report?**
- Check `src/report_writer.py` — you may have forgotten to add it there
- Verify the key name matches exactly (case-sensitive)

**Wrong values extracted?**
- Make the prompt instruction more specific with examples
- Try a different field name or wording

**Questions?**
- See `docs/CLAUDE.md` for architecture overview
- Check `docs/ARCHITECTURE.md` for detailed explanation of analyzer.py

---

## Done!

Your new extraction field is now part of the pipeline. Every paper will now include this data in the analysis output.

**Next steps:**
- Use the field in your narrative synthesis
- Add it to your survey visualization or analysis
- Share the updated code with your team

---

**Quick Reference:**
- Add field to prompt: `src/analyzer.py` lines 7–59
- Add field to report: `src/report_writer.py` (search for "analysis.get")
- Test: `python main.py --input input/test_papers.csv --step analyze`
- Full re-run: `rm output/papers/*.md && python main.py --input input/papers.csv`
