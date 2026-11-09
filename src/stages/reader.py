"""Reader stage: one reader agent, one paper, one artifact.

Runnable on its own by any operator on their own account — the unit of
distributed work. Readers never see each other's output; the supervisor stage
checks each reading, and the reviewer compares them, after the artifacts have
been merged.
"""

import hashlib
import time

from config import PDFS_DIR
from src import llm
from src.analyzer import _fill
from src.evidence import check_report
from src.fields import (ENUM_FIELDS, EVIDENCE_FIELDS, LIST_ENUM_FIELDS, check_vocab,
                        declared_fields, needs_quote, render_evidence_rules, render_schema)
from src.pdf_extractor import extract_text
from src.pdf_fetcher import pdf_filename
from src.protocol import Agent, Protocol, backend_can_serve, sha256_file
from src.rounds import now, operator, read_artifact

MIN_TEXT_CHARS = 200
PLACEHOLDER_PAPER = {"id": "<<ID>>", "name": "<<TITLE>>"}


# --- shared helpers (also used by supervisor and reviewer) ------------------------

def metadata(paper: dict) -> dict:
    return {k: paper.get(k, "") for k in
            ("modalities", "domain", "evaluation_metrics", "asjc_code", "humanities")}


def research_questions(protocol: Protocol) -> str:
    rq = protocol.research_questions
    return rq.read_text(encoding="utf-8") if rq.exists() else ""


def paper_text(paper: dict) -> tuple[str, str]:
    """(text with page markers, sha256 of the PDF) — the same input for every agent."""
    pdf = PDFS_DIR / pdf_filename(paper["id"])
    if not pdf.exists():
        raise FileNotFoundError(f"no PDF for {paper['id']} — run `python census.py fetch` first")
    text = extract_text(pdf, page_markers=True)
    if len(text.strip()) < MIN_TEXT_CHARS:
        raise ValueError(f"{paper['id']}: PDF text too short, possibly scanned")
    return text, sha256_file(pdf)


def backend_kind(protocol: Protocol, agent: Agent, backend_name: str | None) -> tuple[str, str]:
    name = backend_name or agent.backend
    kind = protocol.backends[name]["kind"]
    if kind != "mock" and not backend_can_serve(kind, agent.model):
        raise ValueError(f"backend {name} ({kind}) cannot serve model {agent.model}")
    return name, kind


def stamp(protocol: Protocol, agent: Agent, backend: str, kind: str, prompt: str,
          scaffold_text: str, extra: dict) -> dict:
    return {
        "round": protocol.round,
        "agent": agent.id,
        "role": agent.role,
        "scope": agent.scope,
        "operator": operator(),
        "backend": backend,
        "backend_kind": kind,          # "mock": no model was called
        "model": agent.model,
        "prompt_sha256": agent.prompt_sha256(),
        "scaffold_sha256": hashlib.sha256(scaffold_text.encode()).hexdigest(),
        "rendered_prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        **extra,
    }


# --- reader -----------------------------------------------------------------

def render_prompt(protocol: Protocol, agent: Agent, paper: dict, text: str) -> str:
    fields = agent.select_fields(declared_fields())
    return _fill(agent.prompt_path.read_text(encoding="utf-8"), render_schema(fields), text,
                 paper.get("name", ""), metadata(paper),
                 research_questions=research_questions(protocol),
                 evidence_rules=render_evidence_rules(fields))


def scaffold(protocol: Protocol, agent: Agent) -> str:
    """The prompt minus the paper: prompt file + schema + vocabularies + research
    questions + evidence rules. Frozen by the round, so an operator whose schema,
    extra fields or rules differ cannot contribute to it unnoticed."""
    return render_prompt(protocol, agent, PLACEHOLDER_PAPER, "<<PAPER_TEXT>>")


def _mock_report(fields: dict[str, str], text: str) -> dict:
    """Schema-valid output without a model, for testing the plumbing at no cost.

    Quotes are lifted from the paper so they verify — except one, deliberately
    fabricated, so that every mock run also exercises the evidence check.
    """
    words = [w for w in text.split() if not w.startswith("===")]
    real_quote = " ".join(words[40:62]) or "x" * 20
    report, evidence = {}, {}
    for name in fields:
        if name in ENUM_FIELDS:
            allowed = sorted(ENUM_FIELDS[name])
            report[name] = "not_stated" if "not_stated" in allowed else allowed[0]
        elif name in LIST_ENUM_FIELDS:
            report[name] = [sorted(LIST_ENUM_FIELDS[name])[0]]
        elif name == "inclusion_criteria":
            report[name] = {c: {"met": True, "note": "mock"} for c in (
                "general_purpose_benchmark", "evaluates_generative_llm",
                "quantitative_metrics", "published_after_march_2023")}
        elif "integer" in fields[name] or "number" in fields[name] or name == "publication_year":
            report[name] = None
        else:
            report[name] = "mock"
    for name in (f for f in EVIDENCE_FIELDS if f in fields):
        if needs_quote(name, report.get(name)):
            evidence[name] = [{"quote": real_quote, "where": "p. 1"}]
    if "primary_evaluation_setting" in evidence:
        evidence["primary_evaluation_setting"] = [
            {"quote": "this sentence was invented by the mock backend and is in no paper", "where": "p. 9"}]
    report["evidence"] = evidence
    return report


def _same_pdf_as_other_readers(protocol: Protocol, agent: Agent, paper: dict, pdf_sha: str) -> None:
    """Refuse BEFORE calling a model if another reader of this paper read different
    PDF bytes. arXiv serves the latest version, so two operators who fetch weeks
    apart can hold different files; without this the mismatch would surface only
    at the supervisor, after both readings had been paid for."""
    for other in protocol.by_role("reader"):
        if other.id == agent.id:
            continue
        art = read_artifact(protocol.round, paper["id"], other.id)
        theirs = art and art["extraction"]["input"]["pdf_sha256"]
        if theirs and theirs != pdf_sha:
            raise RuntimeError(
                f"{other.id} (by {art['extraction'].get('operator', '?')}) read a different PDF of "
                f"{paper['id']} (sha {theirs[:10]}…, yours {pdf_sha[:10]}…). Get the same file from that "
                f"operator into output/pdfs/ before running {agent.id}.")


def read(protocol: Protocol, agent: Agent, paper: dict, backend_name: str | None = None,
         feedback: str | None = None, extra_stamp: dict | None = None) -> dict:
    """One reading. `feedback` (a supervisor's rework request) is appended after
    the paper text; the result is otherwise produced exactly like a first reading."""
    if agent.role != "reader":
        raise ValueError(f"{agent.id} is a {agent.role}, not a reader")
    backend, kind = backend_kind(protocol, agent, backend_name)
    text, pdf_sha = paper_text(paper)
    _same_pdf_as_other_readers(protocol, agent, paper, pdf_sha)
    fields = agent.select_fields(declared_fields())
    prompt = render_prompt(protocol, agent, paper, text)
    if feedback:
        prompt = f"{prompt}\n\n{feedback}"

    started, t0 = now(), time.monotonic()
    if kind == "mock":
        report = _mock_report(fields, text)
    else:
        report = llm.generate_json(prompt, agent.model, label=f"{paper['id'][:40]}.{agent.id}",
                                   backend=kind)
    report["checks"] = {
        "missing_fields": sorted(set(fields) - set(report)),
        "vocab_warnings": check_vocab(report),
        "evidence": check_report(report, fields, text),
    }
    report["extraction"] = stamp(protocol, agent, backend, kind, prompt, scaffold(protocol, agent), {
        "fields": sorted(fields),
        "input": {"pdf_sha256": pdf_sha, "text_chars": len(text)},
        "started": started,
        "seconds": round(time.monotonic() - t0, 1),
        **(extra_stamp or {}),
    })
    report["paper_id"] = paper["id"]
    return report


# --- stage interface (census.py) ------------------------------------------------

def run(protocol: Protocol, agent: Agent, paper: dict, backend_name: str | None = None) -> dict[str, dict]:
    """{artifact name: data} to write for this paper."""
    return {agent.id: read(protocol, agent, paper, backend_name)}


def summary(artifacts: dict[str, dict]) -> str:
    report = next(iter(artifacts.values()))
    checks = report["checks"]
    ev = checks["evidence"]
    flags = [f"{len(ev['unverified'])} unverified quote(s)" if ev["unverified"] else "",
             f"{len(ev['unsupported'])} value(s) without quote" if ev["unsupported"] else "",
             f"{len(checks['vocab_warnings'])} vocab" if checks["vocab_warnings"] else "",
             f"missing {checks['missing_fields']}" if checks["missing_fields"] else ""]
    return ", ".join(f for f in flags if f) or "clean"
