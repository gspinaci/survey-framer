"""Multi-agent paper analysis.

Two persona agents read the paper independently — Ciop (humanist background)
and Cip (technical background) — then a Reviewer agent adjudicates their
reports against the paper text and writes the final report.
"""

import json

from config import GEMINI_PERSONA_MODEL, GEMINI_REVIEWER_MODEL
from src import llm
from src.fields import render_schema


def build_metadata_block(title: str, metadata: dict | None) -> str:
    block = ""
    if title:
        block += f"Paper title: {title}\n"
    if metadata:
        meta_lines = []
        if metadata.get("modalities"):
            meta_lines.append(f"  - Modalities: {metadata['modalities']}")
        if metadata.get("domain"):
            meta_lines.append(f"  - Domain: {metadata['domain']}")
        if metadata.get("evaluation_metrics"):
            meta_lines.append(f"  - Evaluation metrics: {metadata['evaluation_metrics']}")
        if metadata.get("asjc_code"):
            meta_lines.append(f"  - ASJC code: {metadata['asjc_code']}")
        if metadata.get("humanities"):
            meta_lines.append(f"  - Humanities flag: {metadata['humanities']}")
        if meta_lines:
            block += "CSV Metadata:\n" + "\n".join(meta_lines) + "\n"
    return block.strip()


def _fill(template: str, schema: str, text: str, title: str, metadata: dict | None) -> str:
    return (
        template.replace("<<SCHEMA>>", schema)
        .replace("<<METADATA>>", build_metadata_block(title, metadata))
        .replace("<<PAPER_TEXT>>", text)
    )


def run_persona(persona: str, text: str, fields: dict[str, str],
                title: str = "", metadata: dict | None = None) -> dict:
    """Run one persona agent ("ciop" or "cip") over the given fields."""
    prompt = _fill(llm.load_prompt(persona), render_schema(fields), text, title, metadata)
    return llm.generate_json(prompt, GEMINI_PERSONA_MODEL)


def run_reviewer(text: str, fields: dict[str, str], ciop: dict, cip: dict,
                 title: str = "", metadata: dict | None = None) -> dict:
    prompt = _fill(llm.load_prompt("reviewer"), render_schema(fields), text, title, metadata)
    prompt = prompt.replace("<<CIOP_REPORT>>", json.dumps(ciop, indent=2))
    prompt = prompt.replace("<<CIP_REPORT>>", json.dumps(cip, indent=2))
    return llm.generate_json(prompt, GEMINI_REVIEWER_MODEL)


def analyze_paper(text: str, fields: dict[str, str], title: str = "",
                  metadata: dict | None = None) -> tuple[dict, dict, dict]:
    """Full multi-agent analysis over the given fields.

    Used for both full runs (all declared fields) and incremental runs
    (only the missing extra fields). Returns (ciop, cip, final).
    """
    ciop = run_persona("ciop", text, fields, title, metadata)
    cip = run_persona("cip", text, fields, title, metadata)
    final = run_reviewer(text, fields, ciop, cip, title, metadata)
    return ciop, cip, final
