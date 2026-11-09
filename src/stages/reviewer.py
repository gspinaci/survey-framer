"""Reviewer stage: adjudicate the supervised readings into the final record.

Reads, for every reader, the version the supervisor settled on (original or
rework), with its quote verification and any flags the supervisor could not
resolve. Writes reviewer.json: the final record (all schema fields + evidence),
a confidence per evidence field, the fields left to the human reviewers, and
the review notes.
"""

import json
import time

from src import llm
from src.analyzer import build_metadata_block
from src.evidence import check_report
from src.fields import (EVIDENCE_FIELDS, check_vocab, declared_fields, needs_quote,
                        render_evidence_rules, render_schema, render_task_vocab)
from src.protocol import Agent, Protocol
from src.rounds import now, read_artifact
from src.stages import reader as R
from src.stages.supervisor import report_view

EXTRA_KEYS = ("confidence", "needs_human", "review_notes")


def render_prompt(protocol: Protocol, agent: Agent, paper: dict, readings: str, text: str) -> str:
    fields = declared_fields()
    return (agent.prompt_path.read_text(encoding="utf-8")
            .replace("<<RESEARCH_QUESTIONS>>", R.research_questions(protocol))
            .replace("<<TASK_VOCAB>>", render_task_vocab())
            .replace("<<SCHEMA>>", render_schema(fields))
            .replace("<<EVIDENCE_RULES>>", render_evidence_rules(fields))
            .replace("<<METADATA>>", build_metadata_block(paper.get("name", ""), R.metadata(paper)))
            .replace("<<READER_REPORTS>>", readings)
            .replace("<<PAPER_TEXT>>", text))


def scaffold(protocol: Protocol, agent: Agent) -> str:
    return render_prompt(protocol, agent, R.PLACEHOLDER_PAPER, "<<READER_REPORTS>>", "<<PAPER_TEXT>>")


def _readings(protocol: Protocol, paper: dict, sup: dict) -> tuple[str, dict]:
    blocks, used = [], {}
    for r in protocol.by_role("reader"):
        entry = sup["readers"][r.id]
        version = entry["final_version"].removesuffix(".json")
        art = read_artifact(protocol.round, paper["id"], version)
        if art is None:
            raise RuntimeError(f"supervisor points to {version}.json, which is missing")
        used[r.id] = entry["final_version"]
        blocks.append(
            f"=== READING by {r.id} ({r.scope or 'general'} lens) — supervisor: {entry['status']} ===\n"
            f"Unresolved supervisor flags: {json.dumps(entry['flags_for_reviewer'], ensure_ascii=False)}\n"
            f"Quote verification by script: {json.dumps(art['checks']['evidence']['quotes'])}\n"
            f"REPORT:\n{json.dumps(report_view(art), indent=2, ensure_ascii=False)}")
    return "\n\n".join(blocks), used


def _mock_final(protocol: Protocol, paper: dict, used: dict) -> dict:
    first = read_artifact(protocol.round, paper["id"], next(iter(used.values())).removesuffix(".json"))
    final = report_view(first)
    final["confidence"] = {f: "low" for f in EVIDENCE_FIELDS if f in final}
    final["needs_human"] = []
    final["review_notes"] = "mock reviewer: copied the first reading"
    return final


def run(protocol: Protocol, agent: Agent, paper: dict, backend_name: str | None = None) -> dict[str, dict]:
    backend, kind = R.backend_kind(protocol, agent, backend_name)
    sup = read_artifact(protocol.round, paper["id"], "supervisor")
    if sup is None:
        raise RuntimeError("supervisor not done yet")
    text, pdf_sha = R.paper_text(paper)
    if sup["extraction"]["input"]["pdf_sha256"] != pdf_sha:
        raise RuntimeError("the supervisor read a different PDF than the one on this machine")
    readings, used = _readings(protocol, paper, sup)
    prompt = render_prompt(protocol, agent, paper, readings, text)

    started, t0 = now(), time.monotonic()
    if kind == "mock":
        final = _mock_final(protocol, paper, used)
    else:
        final = llm.generate_json(prompt, agent.model, label=f"{paper['id'][:40]}.{agent.id}", backend=kind)

    fields = declared_fields()
    evidence_fields = [f for f in EVIDENCE_FIELDS if f in fields]
    final["checks"] = {
        "missing_fields": sorted((set(fields) | set(EXTRA_KEYS)) - set(final)),
        "vocab_warnings": check_vocab(final),
        "evidence": check_report(final, fields, text),
        "confidence_missing": [f for f in evidence_fields
                               if needs_quote(f, final.get(f)) and f not in (final.get("confidence") or {})],
    }
    final["extraction"] = R.stamp(protocol, agent, backend, kind, prompt, scaffold(protocol, agent), {
        "input": {"pdf_sha256": pdf_sha, "text_chars": len(text), "readings": used},
        "started": started,
        "seconds": round(time.monotonic() - t0, 1),
    })
    final["paper_id"] = paper["id"]
    final["paper_name"] = paper.get("name", "")
    return {agent.id: final}


def summary(artifacts: dict[str, dict]) -> str:
    final = artifacts["reviewer"] if "reviewer" in artifacts else next(iter(artifacts.values()))
    checks = final["checks"]
    ev = checks["evidence"]
    low = sum(v == "low" for v in (final.get("confidence") or {}).values())
    parts = [f"{len(final.get('needs_human') or [])} to humans", f"{low} low-confidence",
             f"{len(ev['unverified'])} unverified quote(s)" if ev["unverified"] else "",
             f"{len(ev['unsupported'])} unsupported" if ev["unsupported"] else "",
             f"{len(checks['vocab_warnings'])} vocab" if checks["vocab_warnings"] else "",
             f"missing {checks['missing_fields']}" if checks["missing_fields"] else ""]
    return ", ".join(p for p in parts if p)
