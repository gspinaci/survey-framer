#!/usr/bin/env python3
"""Import the candidates of one discovery run into the census table.

Any route that produces the agentic output format — raw/candidates.csv with the
columns of docs/deep_research_prompt.md (Name, Article URL, PDF URL, evidence
C1-C4, Borderline?, Confidence, …) — is imported the same way, whether the run
was ChatGPT Deep Research or the census-discover skill.

What it guarantees:
  - no candidate already in the table is added again (matched on arXiv id, URL,
    ID or normalised name; matches are reported, never silently dropped);
  - every added row carries its provenance (route, run, pointer to the raw row
    with the original name, date added) and empty Accept GS / Accept RG, so it
    enters the table as `pending` and is not fetched or analysed until both
    reviewers accept it;
  - the run's manifest records what was imported and when; a run is imported once.

    python scripts/import_discovery.py discovery/<run_id>            # dry run
    python scripts/import_discovery.py discovery/<run_id> --apply
"""

import csv
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import BASE_DIR, PAPERS_CSV
from src import census_table

ARXIV = re.compile(r"(?<![\d.])(\d{4}\.\d{4,5})(?:v\d+)?(?![\d])")


def _norm_url(url: str) -> str:
    return re.sub(r"^https?://(www\.)?|/+$|\.pdf$", "", url.strip().lower())


def _keys(*cells: str) -> set[str]:
    keys = set()
    for cell in cells:
        keys |= {f"arxiv:{a}" for a in ARXIV.findall(cell or "")}
        for url in re.findall(r"https?://\S+", cell or ""):
            keys.add(f"url:{_norm_url(url)}")
    return keys


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    run_dir = Path(sys.argv[1]).resolve()
    apply = "--apply" in sys.argv
    manifest_path = run_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("import"):
        sys.exit(f"{run_dir.name} was already imported on {manifest['import']['on']}")
    route = manifest["route"]
    if route not in census_table.ROUTES:
        sys.exit(f"unknown route {route!r}")
    hunter = manifest.get("hunter") or manifest["tool"].split(" (")[0]

    fieldnames, table = census_table.load(PAPERS_CSV)
    known: dict[str, str] = {}
    for row in table:
        label = row.get("ID") or row.get("Name", "")
        for key in _keys(row.get("Article URL", ""), row.get("PDF URL", ""),
                         row.get("Resource URL (Benchmark + Dataset)", "")):
            known[key] = label
        known[f"name:{census_table.norm_name(row.get('Name', ''))}"] = label
        if row.get("ID"):
            known[f"id:{row['ID']}"] = label
    taken = {row.get("ID", "") for row in table}

    raw_csv = run_dir / "raw" / "candidates.csv"
    with open(raw_csv, newline="", encoding="utf-8") as f:
        candidates = list(csv.DictReader(f))

    added, duplicates, today = [], [], date.today().isoformat()
    for line, cand in enumerate(candidates, start=2):  # line 1 is the header
        keys = _keys(cand["Article URL"], cand.get("PDF URL", ""), cand.get("Venue or status", ""))
        keys.add(f"name:{census_table.norm_name(cand['Name'])}")
        hit = next((known[k] for k in keys if k in known), None)
        if hit:
            duplicates.append({"line": line, "name": cand["Name"], "matches": hit})
            continue
        rid = census_table.derive_id(cand["Article URL"], cand["Name"], taken)
        taken.add(rid)
        for k in keys:
            known[k] = rid
        borderline = cand.get("Borderline?", "").strip()
        ref = (f"raw/candidates.csv line {line}: '{cand['Name']}' · first public "
               f"{cand.get('First public date (YYYY-MM-DD)', '?')} · confidence "
               f"{cand.get('Confidence', '?')} · borderline: {borderline or '?'}")
        added.append({
            "Name": cand["Name"],
            "Article URL": cand["Article URL"],
            "Hunter": hunter,
            "Year": cand.get("Year", ""),
            "Modalities": cand.get("Modalities", ""),
            "Domain": cand.get("Domain", ""),
            "Evaluation metrics": cand.get("Evaluation metrics", ""),
            "Humanities?": "Borderline" if "C3" in borderline else "Yes",
            "ASJC code": cand.get("Humanities areas", ""),
            "Resource URL (Benchmark + Dataset)": cand.get("Resource URL (Benchmark + Dataset)", ""),
            "Source": cand.get("Found via", ""),
            "Specific source": cand.get("Venue or status", ""),
            "ID": rid,
            "PDF URL": cand.get("PDF URL", ""),
            "Discovery route": route,
            "Discovery run": manifest["run_id"],
            "Discovery ref": ref,
            "Added on": today,
        })

    for row in added:
        print(f"  + {row['ID'][:28]:28} {row['Name'][:60]}")
    for d in duplicates:
        print(f"  = line {d['line']}: {d['name'][:50]} — already in table as {d['matches']}")
    print(f"{len(added)} to add, {len(duplicates)} already present, from {len(candidates)} candidates")

    if not apply:
        print("dry run — re-run with --apply to write")
        return
    census_table.save(PAPERS_CSV, fieldnames, table + added)
    manifest["import"] = {
        "on": today,
        "table": PAPERS_CSV.relative_to(BASE_DIR).as_posix(),
        "rows_added": len(added),
        "ids_added": [r["ID"] for r in added],
        "duplicates": duplicates,
        "not_imported": "near_misses.csv and unverified.csv stay in raw/ as leads; they lack the C1-C4 evidence a table row needs",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"appended {len(added)} rows to {PAPERS_CSV}; import recorded in {manifest_path}")


if __name__ == "__main__":
    main()
