#!/usr/bin/env python3
"""Compare a round's records with the legacy records, field by field.

Comparisons on the aggregated fields (facets + results axis + role/size):
  - reader agreement inside the round (e.g. ciop vs cip), the inter-reader figure
    the article reports in Sec. 4.7 — measured on the ORIGINAL readings. The
    supervisor's reworks push readers towards one reading (first pilot: 45/48
    agreement before supervision, 48/48 after), so agreement after supervision
    says more about the supervisor than about the readers; it is shown separately;
  - round final (reviewer.json) vs the legacy final record in output/papers/
    (the Jul-Aug 2026 Gemini extraction): a cross-model agreement, the external
    reliability estimate the article says it lacks.

Reads files only; no model calls.

    python scripts/compare_round.py pilot-2026-11
    python scripts/compare_round.py pilot-2026-11 --papers SimpleQA 2509.18839 --diff
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import PAPERS_DIR
from src.fields import FACET_FIELDS, RESULT_FIELDS
from src.rounds import round_dir

FIELDS = ("humanities_role", "dataset_size", "evaluation_set_size", "primary_evaluation_setting",
          *FACET_FIELDS, "gold_upstream_source", *RESULT_FIELDS,
          "reported_format_gap_kind", "reported_gap_kinds")


def norm(v):
    if isinstance(v, str):
        return v.strip().lower()
    if isinstance(v, float) and v.is_integer():
        return int(v)
    return v


def legacy(paper_id: str) -> dict | None:
    for f in PAPERS_DIR.glob("*.json"):
        d = json.loads(f.read_text(encoding="utf-8"))
        if d.get("paper_id") == paper_id:
            return d
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("round")
    ap.add_argument("--papers", nargs="+")
    ap.add_argument("--diff", action="store_true", help="print every disagreeing value")
    args = ap.parse_args()

    base = round_dir(args.round) / "papers"
    papers = sorted(p for p in base.iterdir() if p.is_dir())
    agree_o = {f: [0, 0] for f in FIELDS}
    agree_r = {f: [0, 0] for f in FIELDS}
    agree_l = {f: [0, 0] for f in FIELDS}
    diffs = []
    for pdir in papers:
        art = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in pdir.glob("*.json")}
        pid = next((a.get("paper_id") for a in art.values() if a.get("paper_id")), pdir.name)
        if args.papers and pid not in args.papers:
            continue
        sup = art.get("supervisor", {}).get("readers", {})
        readers = {r: art.get(e["final_version"].removesuffix(".json"), art.get(r))
                   for r, e in sup.items()} or {k: v for k, v in art.items() if k in ("ciop", "cip")}
        final, old = art.get("reviewer"), legacy(pid)
        names = sorted(readers)
        originals = {n: art.get(n) for n in names}
        for f in FIELDS:
            if len(names) >= 2 and all(originals.values()):
                a, b = (norm(originals[n].get(f)) for n in names[:2])
                agree_o[f][0] += a == b
                agree_o[f][1] += 1
            if len(names) >= 2:
                a, b = (norm(readers[n].get(f)) for n in names[:2])
                agree_r[f][0] += a == b
                agree_r[f][1] += 1
                if a != b:
                    diffs.append((pid, f, f"{names[0]}={a!r}", f"{names[1]}={b!r}"))
            if final and old and f in old:  # fields added after the legacy run are not disagreements
                a, b = norm(final.get(f)), norm(old.get(f))
                agree_l[f][0] += a == b
                agree_l[f][1] += 1
                if a != b:
                    diffs.append((pid, f, f"round={a!r}", f"legacy={b!r}"))

    cell = lambda v: f"{v[0]}/{v[1]}" if v[1] else "-"
    print(f"{'field':28} {'readers (original)':>19} {'readers (final)':>16} {'round = legacy':>15}")
    for f in FIELDS:
        print(f"{f:28} {cell(agree_o[f]):>19} {cell(agree_r[f]):>16} {cell(agree_l[f]):>15}")
    tot = lambda d: [sum(v[i] for v in d.values()) for i in (0, 1)]
    print(f"{'TOTAL':28} {cell(tot(agree_o)):>19} {cell(tot(agree_r)):>16} {cell(tot(agree_l)):>15}")
    if args.diff:
        print()
        for d in diffs:
            print("  " + " | ".join(str(x)[:60] for x in d))


if __name__ == "__main__":
    main()
