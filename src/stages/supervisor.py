"""Supervisor stage: check every reading before readings are compared.

For each reader of a paper the supervisor (an LLM, guided by the script's
mechanical checks) accepts the reading or sends it back once with specific
instructions. A rework is a new reading by the same reader agent — same prompt,
same model — plus the feedback; it is written next to the original as
<reader>.rework1.json, never over it. Whatever is still wrong after the rework
travels to the reviewer as flags.

Separating this from the reviewer means that the disagreements the reviewer
adjudicates are disagreements of interpretation, not errors of reading.
"""

import json
import time

from src import llm
from src.analyzer import build_metadata_block
from src.fields import declared_fields, render_schema, render_task_vocab
from src.protocol import Agent, Protocol
from src.rounds import now, read_artifact
from src.stages import reader as R

REWORK_SPLIT = "<<<REWORK_TEMPLATE>>>"
HIDDEN_KEYS = ("checks", "extraction", "paper_id")
VERDICTS = ("accept", "rework")


def _templates(agent: Agent) -> tuple[str, str]:
    text = agent.prompt_path.read_text(encoding="utf-8")
    if REWORK_SPLIT not in text:
        raise ValueError(f"{agent.prompt} has no {REWORK_SPLIT} section")
    check, rework = text.split(REWORK_SPLIT, 1)
    return check, rework


def report_view(art: dict) -> dict:
    """What a reader actually said: fields + evidence, without the bookkeeping."""
    return {k: v for k, v in art.items() if k not in HIDDEN_KEYS}


def render_check(protocol: Protocol, agent: Agent, reader_agent: Agent, paper: dict,
                 report_json: str, checks_json: str, text: str) -> str:
    template, _ = _templates(agent)
    fields = reader_agent.select_fields(declared_fields())
    return (template
            .replace("<<RESEARCH_QUESTIONS>>", R.research_questions(protocol))
            .replace("<<READER_ID>>", reader_agent.id)
            .replace("<<READER_SCOPE>>", reader_agent.scope or "general")
            .replace("<<SCHEMA>>", render_schema(fields))
            .replace("<<TASK_VOCAB>>", render_task_vocab())
            .replace("<<METADATA>>", build_metadata_block(paper.get("name", ""), R.metadata(paper)))
            .replace("<<READER_REPORT>>", report_json)
            .replace("<<MECHANICAL_CHECKS>>", checks_json)
            .replace("<<PAPER_TEXT>>", text))


def scaffold(protocol: Protocol, agent: Agent) -> str:
    _, rework = _templates(agent)
    parts = [render_check(protocol, agent, r, R.PLACEHOLDER_PAPER, "<<READER_REPORT>>",
                          "<<MECHANICAL_CHECKS>>", "<<PAPER_TEXT>>")
             for r in protocol.by_role("reader")]
    return "\n".join(parts) + REWORK_SPLIT + rework + f"\nmax_rework={agent.options.get('max_rework', 1)}"


def _mock_verdict(art: dict) -> dict:
    checks, ev = art["checks"], art["checks"]["evidence"]
    issues = [{"field": f, "kind": "bad_quote", "problem": "quote not found in the text (mock)",
               "instruction": "quote the paper verbatim"} for f in ev["unverified"]]
    issues += [{"field": f, "kind": "unsupported", "problem": "value without quote (mock)",
                "instruction": "add a quote or use not_stated"} for f in ev["unsupported"]]
    issues += [{"field": f, "kind": "missing", "problem": "field missing (mock)",
                "instruction": "fill it"} for f in checks["missing_fields"]]
    return {"verdict": "rework" if issues else "accept", "issues": issues, "notes": "mock supervisor"}


def _ask(protocol, agent, kind, reader_agent, paper, art, text) -> dict:
    if kind == "mock":
        return _mock_verdict(art)
    prompt = render_check(protocol, agent, reader_agent, paper,
                          json.dumps(report_view(art), indent=2, ensure_ascii=False),
                          json.dumps(art["checks"], indent=2), text)
    verdict = llm.generate_json(prompt, agent.model, label=f"{paper['id'][:40]}.{agent.id}.{reader_agent.id}",
                                backend=kind)
    if verdict.get("verdict") not in VERDICTS or not isinstance(verdict.get("issues", []), list):
        raise ValueError(f"supervisor returned an invalid verdict: {str(verdict)[:200]}")
    verdict.setdefault("issues", [])
    if verdict["verdict"] == "rework" and not verdict["issues"]:
        verdict["verdict"] = "accept"  # a rework request with nothing to fix is an accept
    return verdict


def run(protocol: Protocol, agent: Agent, paper: dict, backend_name: str | None = None) -> dict[str, dict]:
    backend, kind = R.backend_kind(protocol, agent, backend_name)
    text, pdf_sha = R.paper_text(paper)
    _, rework_template = _templates(agent)
    max_rework = int(agent.options.get("max_rework", 1))
    started, t0 = now(), time.monotonic()

    readers = protocol.by_role("reader")
    arts = {r.id: read_artifact(protocol.round, paper["id"], r.id) for r in readers}
    missing = [rid for rid, a in arts.items() if a is None]
    if missing:
        raise RuntimeError(f"readers not done yet: {', '.join(missing)}")
    mismatched = [rid for rid, a in arts.items() if a["extraction"]["input"]["pdf_sha256"] != pdf_sha]
    if mismatched:
        raise RuntimeError(f"{', '.join(mismatched)} read a different PDF than the one on this machine; "
                           f"re-fetch or re-run those readers before supervising")

    out: dict[str, dict] = {}
    entries = {}
    for r in readers:
        art = arts[r.id]
        first = _ask(protocol, agent, kind, r, paper, art, text)
        entry = {"check": first, "final_version": f"{r.id}.json"}
        remaining = first["issues"] if first["verdict"] == "rework" else []
        if first["verdict"] == "rework" and max_rework >= 1:
            feedback = (rework_template
                        .replace("<<ISSUES>>", json.dumps(first["issues"], indent=2, ensure_ascii=False))
                        .replace("<<PREVIOUS_REPORT>>",
                                 json.dumps(report_view(art), indent=2, ensure_ascii=False)))
            # The rework runs the reader's own prompt and model; with a backend override
            # (e.g. mock in a test round) the reader is reworked through the same override.
            redo = R.read(protocol, r, paper, backend_name if backend_name else r.backend,
                          feedback=feedback,
                          extra_stamp={"rework_of": f"{r.id}.json", "requested_by": agent.id, "rework": 1})
            name = f"{r.id}.rework1"
            out[name] = redo
            second = _ask(protocol, agent, kind, r, paper, redo, text)
            entry.update(recheck=second, final_version=f"{name}.json")
            remaining = second["issues"] if second["verdict"] == "rework" else []
            entry["status"] = "accepted_after_rework" if not remaining else "flagged"
        else:
            entry["status"] = "accepted" if not remaining else "flagged"
        entry["flags_for_reviewer"] = remaining
        entries[r.id] = entry

    out[agent.id] = {
        "readers": entries,
        "extraction": R.stamp(protocol, agent, backend, kind, "", scaffold(protocol, agent), {
            "input": {"pdf_sha256": pdf_sha, "text_chars": len(text)},
            "max_rework": max_rework,
            "started": started,
            "seconds": round(time.monotonic() - t0, 1),
        }),
        "paper_id": paper["id"],
    }
    return out


def summary(artifacts: dict[str, dict]) -> str:
    sup = next(v for k, v in artifacts.items() if "readers" in v)
    return ", ".join(f"{rid} {e['status']}" + (f" ({len(e['flags_for_reviewer'])} flags)"
                                               if e["flags_for_reviewer"] else "")
                     for rid, e in sup["readers"].items())
