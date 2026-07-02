"""Field registry: core extraction schema + optional extra fields.

Extra fields are declared in prompts/extra_fields.json as
    {"field_name": {"description": "...", "type": "..."}}
and can be added between runs; the analyze step extracts only the ones
missing from each paper's final JSON (incremental merge).
"""

import json

from config import EXTRA_FIELDS_PATH

# Each core field maps to the literal JSON value text shown to the model in
# the schema block (descriptions carried over verbatim from the original
# single-agent ANALYSIS_PROMPT).
CORE_FIELDS: dict[str, str] = {
    "benchmark_name": '"Name of the benchmark (or null if paper does not introduce one)"',
    "publication_year": "2024",
    "humanities_role": '"content | domain | both | none"',
    "humanities_role_explanation": '"Brief explanation: e.g., \'Uses art history images as factual QA items\' vs \'Designed for art-historical visual understanding\'"',
    "benchmark_modalities": '["list of modalities used in the benchmark — use ONLY these lowercase values: text, image, audio, video; combine as needed, e.g. [\\"text\\", \\"image\\"]"]',
    "benchmark_modalities_explanation": '"Description of how modalities are combined and used (e.g., \'Multi-modal VQA combining artwork images with natural language questions\')"',
    "analytical_tasks": '["list of task types evaluated"]',
    "analytical_tasks_explanation": '"Detailed explanation of the analytical nature of tasks (e.g., \'factual recognition of art movements\', \'economic-grade numerical reasoning\', \'causal inference on historical events\')"',
    "inclusion_criteria": """{
    "general_purpose_benchmark": {
      "met": true/false,
      "note": "Explanation"
    },
    "evaluates_generative_llm": {
      "met": true/false,
      "note": "Which models were evaluated (e.g., GPT-4, Llama, Gemini, Claude, Mistral)"
    },
    "llm_is_primary_system": {
      "met": true/false,
      "note": "Is the LLM the primary system being benchmarked, or is it auxiliary?"
    },
    "arts_humanities_data": {
      "met": true/false,
      "note": "Which ASJC areas: History, Language and Linguistics, Archaeology, Classics, Conservation, History and Philosophy of Science, Literature and Literary Theory, Museology, Music, Philosophy, Religious Studies, Visual Arts and Performing Arts"
    },
    "quantitative_metrics": {
      "met": true/false,
      "note": "Which metrics: accuracy, F1, BLEU, exact match, ranking, human preference scores, etc."
    },
    "published_after_march_2023": {
      "met": true/false,
      "note": "Publication or preprint date"
    },
    "english_language": {
      "met": true/false,
      "note": "Language of the paper and/or benchmark"
    }
  }""",
    "summary": '"2-3 sentence summary of the paper\'s contribution"',
    "key_findings": '"Main quantitative results or takeaways"',
    "relevant_asjc_areas": '["list of matched ASJC humanities areas"]',
}


def load_extra_fields() -> dict[str, dict]:
    if not EXTRA_FIELDS_PATH.exists():
        return {}
    data = json.loads(EXTRA_FIELDS_PATH.read_text(encoding="utf-8"))
    return data or {}


def _extra_spec(definition: dict) -> str:
    desc = definition.get("description", "")
    ftype = definition.get("type", "")
    return json.dumps(f"{desc} ({ftype})" if ftype else desc)


def declared_fields() -> dict[str, str]:
    """All fields for a full run: core schema plus declared extras."""
    fields = dict(CORE_FIELDS)
    for name, definition in load_extra_fields().items():
        fields[name] = _extra_spec(definition)
    return fields


def missing_fields(analysis: dict) -> dict[str, str]:
    """Declared extra fields whose key is absent from the final JSON.

    Key presence is the test: an extracted null counts as done, so fields
    the paper doesn't state aren't retried on every run.
    """
    return {
        name: _extra_spec(definition)
        for name, definition in load_extra_fields().items()
        if name not in analysis
    }


def render_schema(fields: dict[str, str]) -> str:
    """Render the JSON schema block injected into agent prompts."""
    entries = [f'  "{name}": {spec}' for name, spec in fields.items()]
    return "{\n" + ",\n".join(entries) + "\n}"
