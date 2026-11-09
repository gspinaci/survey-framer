#!/usr/bin/env python3
"""census — run the census one agent at a time, by whoever has the account.

    python census.py status                  what is done, by whom, what can run next
    python census.py round init              freeze the protocol for the round (once, then commit)
    python census.py fetch                   download PDFs of the included records
    python census.py run ciop                run one agent over every paper still missing it
    python census.py run cip --papers 2409.02813 2510.12750 --workers 3

Distributed work, e.g. RG runs Ciop and GS runs Cip on their own accounts:

    RG:  python census.py run ciop   →  git add output/rounds/ && git commit && git push
    GS:  python census.py run cip    →  git pull && git add output/rounds/ && git commit && git push
    later, anyone:  git pull && python census.py status && python census.py run supervisor

Each agent writes one file per paper (output/rounds/<round>/papers/<paper>/<agent>.json),
so contributions merge without conflicts. Every file records who ran it, on which
backend and model, with which prompt (hash) and which PDF (hash); `status` checks that
all of them match the round's frozen protocol and that readers read the same PDF.
The protocol itself — agents, scopes, counts, models, backends — is census.toml.
"""

import argparse
import hashlib
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import PDFS_DIR
from src import protocol as proto
from src import rounds
from src.csv_reader import read_papers_csv
from src.pdf_fetcher import fetch_pdf
from src.stages import STAGES

IMPLEMENTED_ROLES = set(STAGES)


def _scaffolds(p: proto.Protocol) -> dict[str, str]:
    """sha256 of every implemented agent's prompt minus the paper (frozen by the round)."""
    out = {}
    for a in p.agents:
        if a.role in STAGES and a.prompt_path.exists():
            out[a.id] = hashlib.sha256(STAGES[a.role].scaffold(p, a).encode()).hexdigest()
    return out


def _papers(p: proto.Protocol, only: list[str] | None) -> list[dict]:
    included = [x for x in read_papers_csv(p.table) if x["screening_status"] == "included"]
    if not only:
        return included
    by_id = {x["id"]: x for x in included}
    unknown = [i for i in only if i not in by_id]
    if unknown:
        sys.exit(f"not included in the census (or unknown): {', '.join(unknown)}")
    return [by_id[i] for i in only]


def cmd_round(p, args) -> None:
    if args.action == "init":
        path = rounds.init_round(p, _scaffolds(p))
        print(f"round {p.round} frozen in {path}\n"
              f"commit and push it before anyone runs agents in this round.")
    else:
        changed = rounds.refresh_round(p, _scaffolds(p))
        print(f"round {p.round} re-snapshotted; changed: {', '.join(changed) or 'nothing'}"
              + ("\nartifacts of those agents are now stale — re-run them with --force" if changed else ""))


def cmd_status(p, args) -> None:
    table = read_papers_csv(p.table)
    screening = Counter(x["screening_status"] for x in table)
    rnd = rounds.load_round(p.round)
    print(f"Round {p.round} — frozen {rnd['created'][:10]} by {rnd['created_by']}")
    print("Table: " + ", ".join(f"{n} {s}" for s, n in sorted(screening.items())))
    papers = _papers(p, args.papers)
    agents = [a for a in p.agents if a.role in proto.PER_PAPER_ROLES]
    width = max([len(x["id"]) for x in papers] + [10])
    show_rows = args.papers or args.all
    if show_rows:
        print("\n" + " " * min(width, 42) + "  " + "  ".join(f"{a.id:>10}" for a in agents))
    counts: dict[str, Counter] = defaultdict(Counter)
    who: dict[str, Counter] = defaultdict(Counter)
    problems, mocks = [], 0
    for paper in papers:
        state = rounds.paper_state(p, rnd, paper["id"])
        for a in agents:
            counts[a.id][state[a.id]] += 1
            art = rounds.read_artifact(p.round, paper["id"], a.id) if state[a.id] in ("done", "stale") else None
            if art:
                stamp = art.get("extraction", {})
                who[a.id][stamp.get("operator", "?")] += 1
                mocks += stamp.get("backend_kind") == "mock"
        issue = rounds.input_consistency(p, paper["id"])
        if issue:
            problems.append(f"{paper['id']}: {issue}")
        if show_rows:
            print(f"{paper['id'][:42]:{min(width, 42)}}  " + "  ".join(f"{state[a.id]:>10}" for a in agents))
    print(f"\nIncluded papers: {len(papers)}")
    for a in agents:
        c = counts[a.id]
        by = ", ".join(f"{op} {n}" for op, n in who[a.id].most_common())
        print(f"  {a.id:11} {a.role:10} done {c['done']:>3}  missing {c['missing']:>3}  "
              f"blocked {c['blocked']:>3}  stale {c['stale']:>3}" + (f"   by: {by}" if by else ""))
    if mocks:
        print(f"\n  ! {mocks} artifacts were made by the mock backend (no model called)")
    for prob in problems:
        print(f"  ! {prob}")
    runnable = [a for a in agents if counts[a.id]["missing"]]
    if runnable:
        print("\nNext:")
        for a in runnable:
            note = "" if a.role in IMPLEMENTED_ROLES else "   (stage not implemented yet)"
            print(f"  python census.py run {a.id:11} # {counts[a.id]['missing']} papers ready{note}")


def cmd_fetch(p, args) -> None:
    papers = _papers(p, args.papers)
    missing = 0
    for paper in papers:
        if not fetch_pdf(paper, PDFS_DIR):
            missing += 1
            print(f"  MISSING: {paper['id']}")
    print(f"{len(papers) - missing}/{len(papers)} PDFs available in {PDFS_DIR}")


def cmd_run(p, args) -> None:
    agent = p.agent(args.agent)
    if agent.role not in IMPLEMENTED_ROLES:
        sys.exit(f"the {agent.role} stage is not implemented yet")
    backend = args.backend or agent.backend
    if p.backends[backend]["kind"] == "mock" and not p.round.startswith("test-"):
        sys.exit("the mock backend may only write to test rounds (--round test-...)")
    rnd = rounds.load_round(p.round)
    problems = rounds.check_against_round(rnd, p, agent.id, _scaffolds(p).get(agent.id))
    if problems:
        sys.exit(f"{agent.id} cannot contribute to round {p.round}:\n  - " + "\n  - ".join(problems))
    operator = rounds.operator()

    todo = []
    for paper in _papers(p, args.papers):
        state = rounds.paper_state(p, rnd, paper["id"])[agent.id]
        if state == "blocked":
            continue
        if state in ("done", "stale") and not args.force:
            continue
        todo.append(paper)
    if args.limit:
        todo = todo[: args.limit]
    if not todo:
        print(f"nothing to do for {agent.id} in round {p.round}")
        return
    print(f"{agent.id} ({agent.role}, {agent.scope}) · {agent.model} via {backend} · "
          f"operator {operator} · {len(todo)} papers · {args.workers} in parallel")

    stage = STAGES[agent.role]

    def one(paper: dict) -> str:
        artifacts = stage.run(p, agent, paper, args.backend)
        if args.force:  # archived only once the whole step has succeeded
            stale = set(artifacts)
            if agent.role == "supervisor":  # a rework from an earlier supervision must not linger
                stale |= {f"{r.id}.rework1" for r in p.by_role("reader")}
            for name in stale:
                rounds.archive_artifact(p.round, paper["id"], name)
        for name, data in artifacts.items():
            rounds.write_artifact(p.round, paper["id"], name, data)
        return stage.summary(artifacts)

    failed = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(one, paper): paper["id"] for paper in todo}
        for fut in as_completed(futures):
            pid = futures[fut]
            try:
                print(f"  OK    {pid}: {fut.result()}")
            except Exception as e:  # one paper failing must not stop the others
                failed += 1
                print(f"  ERROR {pid}: {e}")
    print(f"\n{len(todo) - failed}/{len(todo)} written to output/rounds/{p.round}/papers/*/{agent.id}.json")
    print("share them:  git add output/rounds/ && git commit -m '<round>: <agent> by <you>' && git push")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--round", help="override the round set in census.toml (e.g. test-...)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("round", help="round management")
    r.add_argument("action", choices=["init", "refresh"])
    s = sub.add_parser("status", help="progress of the current round")
    s.add_argument("--papers", nargs="+")
    s.add_argument("--all", action="store_true", help="one row per paper")
    f = sub.add_parser("fetch", help="download PDFs of included records")
    f.add_argument("--papers", nargs="+")
    run = sub.add_parser("run", help="run one agent")
    run.add_argument("agent")
    run.add_argument("--papers", nargs="+", help="only these paper IDs")
    run.add_argument("--limit", type=int, help="at most N papers (pilot runs)")
    run.add_argument("--force", action="store_true", help="redo papers already done (old file archived)")
    run.add_argument("--backend", help="backend name from census.toml, overriding the agent's")
    run.add_argument("--workers", type=int, default=2)
    args = ap.parse_args()

    p = proto.load()
    if args.round:
        p.round = args.round
    command = {"round": cmd_round, "status": cmd_status, "fetch": cmd_fetch, "run": cmd_run}[args.cmd]
    try:
        command(p, args)
    except (FileNotFoundError, FileExistsError, KeyError, RuntimeError) as e:
        sys.exit(f"census: {e.args[0] if e.args else e}")


if __name__ == "__main__":
    main()
