"""Field registry: core extraction schema + optional extra fields.

Extra fields are declared in prompts/extra_fields.json as
    {"field_name": {"description": "...", "type": "..."}}
and can be added between runs; the analyze step extracts only the ones
missing from each paper's final JSON (incremental merge).
"""

import json

from config import EXTRA_FIELDS_PATH

# Closed vocabulary for analytical_tasks, injected into every agent prompt as
# <<TASK_VOCAB>>. Derived from clustering the 235 free-text labels the first
# ungoverned run produced over 43 papers: with no controlled list the two
# personae described the same paper with near-disjoint labels (mean Jaccard
# 0.16) — same tasks at different granularities (e.g. "figurative language
# classification" vs "classification"), which made the field unaggregable.
# Paper-specific phrasing now goes in analytical_tasks_explanation instead.
ANALYTICAL_TASK_VOCAB: dict[str, str] = {
    "factual_recall": "retrieving stated facts or declarative domain knowledge",
    "multiple_choice_qa": "answering by selecting from a closed set of options",
    "open_ended_qa": "free-text answers, incl. reading comprehension and long-form QA",
    "fact_verification": "judging whether a claim or generated passage is true or consistent",
    "classification": "assigning items to predefined labels, subjects or taxonomies",
    "information_extraction": "NER, entity/coreference resolution, metadata, layout or structure extraction",
    "retrieval_and_ranking": "searching a collection, ordering by relevance or similarity",
    "transcription_and_correction": "OCR/HTR, post-OCR repair, normalization, diplomatic transcription",
    "translation": "cross-lingual or cross-script transfer, incl. transliteration",
    "generation": "producing free text such as summaries, critiques or descriptions",
    "logical_and_quantitative_reasoning": "deduction, multi-hop inference, arithmetic, counting, constraints",
    "causal_and_temporal_reasoning": "cause/effect and chronology over events or processes",
    "interpretation": "hermeneutic reading: iconographic, symbolic, thematic, aesthetic, figurative",
    "attribution": "inferring date, author, origin or provenance of an artefact or text",
    "cultural_reasoning": "reasoning over culture-specific norms, practices and context",
    "normative_judgment": "moral, ethical, value-alignment or bias evaluation",
    "stylistic_analysis": "recognizing, profiling or imitating style and rhetorical structure",
    "visual_recognition": "identifying objects, attributes, characters or layout in images",
    "visual_reasoning": "inference over image content, spatial relations, charts, diagrams",
    "sequence_prediction": "cloze, text completion, next-item prediction",
    "calibration_and_uncertainty": "calibration, confidence or difficulty self-estimation",
    "agentic_tool_use": "multi-step search, tool or browser use, context and stopping decisions",
}


def render_task_vocab() -> str:
    """The <<TASK_VOCAB>> block: closed task list with one-line glosses."""
    lines = [f"  - {name}: {gloss}" for name, gloss in ANALYTICAL_TASK_VOCAB.items()]
    return (
        "CONTROLLED VOCABULARY for analytical_tasks — pick every value that "
        "applies, using these exact lowercase identifiers and nothing else:\n"
        + "\n".join(lines)
        + "\n\nNever invent a label. If the paper's own term is narrower (e.g. "
        '"iconographic interpretation", "post-OCR correction"), map it to the '
        "closest identifier above and record the paper's own wording in "
        "analytical_tasks_explanation so no detail is lost."
    )


# Each core field maps to the literal JSON value text shown to the model in
# the schema block (descriptions carried over verbatim from the original
# single-agent ANALYSIS_PROMPT).
CORE_FIELDS: dict[str, str] = {
    "benchmark_name": '"Name of the benchmark (or null if paper does not introduce one)"',
    "publication_year": "2024",
    "humanities_role": '"content | domain | both | none — content: humanities material supplies the items but the competence tested is general (language modelling, generic QA); domain: the benchmark targets disciplinary competence itself; both: ONLY when the benchmark has distinct item groups or distinct metrics for each, not merely because it could be read either way; none: no humanities material"',
    "humanities_role_explanation": '"Brief explanation naming the evidence for the choice: e.g., \'Uses art history images as factual QA items\' (content) vs \'Designed for art-historical visual understanding\' (domain). If \'both\', state which items or metrics cover each role."',
    "benchmark_modalities": '["list of modalities used in the benchmark — use ONLY these lowercase values: text, image, audio, video; combine as needed, e.g. [\\"text\\", \\"image\\"]"]',
    "benchmark_modalities_explanation": '"Description of how modalities are combined and used (e.g., \'Multi-modal VQA combining artwork images with natural language questions\')"',
    "analytical_tasks": '["one or more identifiers from the CONTROLLED VOCABULARY block above — exact lowercase strings, no invented labels"]',
    "analytical_tasks_explanation": '"Detailed explanation of the analytical nature of the tasks, using the paper\'s own terminology (e.g., \'factual recognition of art movements\', \'economic-grade numerical reasoning\', \'causal inference on historical events\'). This is where paper-specific phrasing belongs, since analytical_tasks itself is restricted to the controlled vocabulary."',
    # Pruned after the first full run: llm_is_primary_system, arts_humanities_data
    # and english_language came back met=true on 43/43 papers, so they cost tokens
    # without discriminating (the corpus is already pre-filtered upstream) and their
    # notes carried nothing not already in relevant_asjc_areas. The four kept here
    # all still do work: general_purpose_benchmark actually splits the corpus
    # (14/43) and is the only criterion the personae disagree on, the two date/model
    # criteria each excluded a paper, and quantitative_metrics stays despite being
    # constant because dashboard.py mines its note for the metric breakdown.
    "inclusion_criteria": """{
    "general_purpose_benchmark": {
      "met": true/false,
      "note": "Explanation. true only for broad multi-task benchmarks; false for benchmarks scoped to one task, domain or framework"
    },
    "evaluates_generative_llm": {
      "met": true/false,
      "note": "Which models were evaluated (e.g., GPT-4, Llama, Gemini, Claude, Mistral)"
    },
    "quantitative_metrics": {
      "met": true/false,
      "note": "Which metrics: accuracy, F1, BLEU, exact match, ranking, human preference scores, etc."
    },
    "published_after_march_2023": {
      "met": true/false,
      "note": "Publication or preprint date"
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


# Closed value sets checked after extraction. Keys absent from a report are
# skipped, so this works for incremental runs over a field subset too.
ENUM_FIELDS: dict[str, set[str]] = {
    "humanities_role": {"content", "domain", "both", "none"},
    "primary_evaluation_setting": {"zero-shot", "few-shot", "fine-tuned", "mix"},
    # Facets: observable properties of how the benchmark was built, standing in for
    # the task categories that could not be separated non-arbitrarily. See
    # METHODOLOGY_facets.md. "not_stated" is a measurement, not a missing value —
    # it must stay distinguishable from "no".
    "gold_source": {
        "existing_metadata", "authored_answer_key", "crowd_annotation",
        "domain_expert", "paper_authors", "model_generated", "not_stated",
    },
    "gold_beyond_stimulus": {"yes", "no", "not_stated"},
    "gold_community_dependent": {"yes", "no", "not_stated"},
    "gold_concerns_genesis": {"yes", "no", "not_stated"},
    "answer_multiplicity": {
        "single_answer", "answer_set", "graded_human_judgment", "not_stated",
    },
    # "not_stated" rather than a bespoke "not_addressed": five of six facets already
    # used not_stated for the paper's silence, and the odd one out drew an
    # off-vocabulary value on the first run. One token per meaning across all facets.
    "plurality_treatment": {"noise", "signal", "not_stated"},
}

# The facets whose ciop/cip divergence is worth reporting (see FACET_FIELDS use in
# scripts/facet_report.py); facets_explanation is prose and excluded.
FACET_FIELDS: tuple[str, ...] = (
    "gold_source",
    "gold_beyond_stimulus",
    "gold_community_dependent",
    "gold_concerns_genesis",
    "answer_multiplicity",
    "plurality_treatment",
)

LIST_ENUM_FIELDS: dict[str, set[str]] = {
    "analytical_tasks": set(ANALYTICAL_TASK_VOCAB),
    "benchmark_modalities": {"text", "image", "audio", "video"},
}


def check_vocab(analysis: dict) -> list[str]:
    """Report values falling outside a closed vocabulary.

    Returns human-readable warnings rather than raising: an off-vocabulary
    label is a prompt-adherence problem worth surfacing, not a reason to throw
    away an otherwise good extraction. Aggregation code should treat any paper
    with warnings as suspect.
    """
    warnings = []
    for field, allowed in ENUM_FIELDS.items():
        value = analysis.get(field)
        if value is not None and str(value).strip().lower() not in allowed:
            warnings.append(f"{field}={value!r} not in {sorted(allowed)}")
    for field, allowed in LIST_ENUM_FIELDS.items():
        values = analysis.get(field)
        if not isinstance(values, list):
            continue
        stray = [v for v in values if str(v).strip().lower() not in allowed]
        if stray:
            warnings.append(f"{field} has off-vocabulary values: {stray}")
    return warnings
