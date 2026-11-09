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


# Kinds of same-material comparison (reported_format_gap). The article's
# instrument-dependence claim (Sec. 4.3) counts the first three: the measuring
# rule changes while the task stays fixed.
GAP_KINDS: dict[str, str] = {
    "scoring": "identical output, stricter or looser scoring rule",
    "format": "same items, different answer format (closed vs open)",
    "depth": "surface vs interpretation tier of the paper's own taxonomy",
    "difficulty": "a harder subset of the same items",
    "input": "different representation of the same items shown to the model",
}
INSTRUMENT_GAP_KINDS = ("scoring", "format", "depth")

# Closed value sets checked after extraction. Keys absent from a report are
# skipped, so this works for incremental runs over a field subset too.
ENUM_FIELDS: dict[str, set[str]] = {
    "humanities_role": {"content", "domain", "both", "none"},
    "primary_evaluation_setting": {"zero-shot", "few-shot", "fine-tuned", "mix"},
    # Facets: observable properties of how the benchmark was built, standing in for
    # the task categories that could not be separated non-arbitrarily. See
    # METHODOLOGY_facets.md. "not_stated" is a measurement, not a missing value —
    # it must stay distinguishable from "no".
    # existing_dataset added 2026-11 (pilot-2026-11): a reused research corpus such as
    # BLN600 had no value of its own and fell into existing_metadata or not_stated.
    "gold_source": {
        "existing_metadata", "existing_dataset", "authored_answer_key", "crowd_annotation",
        "domain_expert", "paper_authors", "model_generated", "not_stated",
    },
    # For existing_dataset: how the upstream annotations were made, as far as the
    # paper says. Following the citation into the upstream paper is a separate step.
    "gold_upstream_source": {
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
    # Results axis: what the paper reports the models actually did. The facets above
    # describe how a benchmark was built; these describe what it measured, and the
    # two are only worth having together because the survey's claim is that the
    # first explains the second. Same design rule — each value must be something the
    # paper states, not something the coder judges. See RESULTS_axis in
    # paper/RESULTS_analysis.md.
    "reported_format_gap": {"yes", "no", "not_stated"},
    # The gap typology the article applied by hand (GAP_KIND in
    # scripts/findings_report.py), extracted as data from round 2026-11 on.
    "reported_format_gap_kind": set(GAP_KINDS),
    "human_baseline_reported": {"yes", "no"},
    "reported_cultural_asymmetry": {"yes", "no", "not_stated"},
    # reported_best_metric carries null legitimately (no headline figure), so the
    # check below has to tolerate None — it already does: absent and None are skipped.
    "reported_best_metric": {
        "accuracy", "f1", "exact_match", "bleu", "cer", "wer", "pass@1",
        "win_rate", "cosine_similarity", "human_score", "other",
    },
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

# The results-axis fields, kept separate from FACET_FIELDS so the two axes can be
# reported and disagreement-checked independently.
RESULT_FIELDS: tuple[str, ...] = (
    "reported_format_gap",
    "reported_format_gap_points",
    "human_baseline_reported",
    "human_gap_points",
    "reported_best_score",
    "reported_best_metric",
    "reported_cultural_asymmetry",
)

# Fields whose value must be backed by a verbatim quote from the paper (readers of
# the round-based engine; see docs/PIPELINE.md §3). These are the values the
# survey aggregates and argues from; prose fields carry their own wording already.
EVIDENCE_FIELDS: tuple[str, ...] = (
    "humanities_role",
    "dataset_size",
    "evaluation_set_size",
    "primary_evaluation_setting",
    *FACET_FIELDS,
    "gold_upstream_source",
    "reported_format_gap",
    "reported_format_gap_points",
    "reported_format_gap_kind",
    "human_baseline_reported",
    "human_gap_points",
    "reported_best_score",
    "reported_cultural_asymmetry",
)

# Values that state the paper's silence, and so need no quote.
SILENT_VALUES = {None, "not_stated", ""}

# Field values that record an ABSENCE — the paper does not do or report the thing —
# and so cannot be quoted. Found in the first pilot (2026-11-09): readers rightly
# gave no quote for these, and requiring one would push them to quote something
# irrelevant. Whether the paper is really silent is the supervisor's check, not
# the script's. Every other non-silent value needs a quote.
ABSENCE_VALUES: dict[str, set[str]] = {
    "human_baseline_reported": {"no"},
    "reported_format_gap": {"no"},
    "reported_cultural_asymmetry": {"no"},
    "gold_community_dependent": {"no"},
    "gold_concerns_genesis": {"no"},
}


def needs_quote(field: str, value) -> bool:
    if value is None or value == []:
        return False
    v = str(value).strip().lower()
    return v not in SILENT_VALUES and v not in ABSENCE_VALUES.get(field, set())


def render_evidence_rules(fields: dict[str, str]) -> str:
    """The <<EVIDENCE_RULES>> block: which of the requested fields need a quote."""
    needed = [f for f in EVIDENCE_FIELDS if f in fields]
    if not needed:
        return ""
    absences = [f'{f} = "no"' for f in needed if f in ABSENCE_VALUES]
    return (
        "EVIDENCE — every aggregated value must be traceable to the paper.\n"
        'Besides the fields above, return an "evidence" object keyed by field name, for each of: '
        + ", ".join(needed) + ".\n"
        'Each entry is a list of 1-2 items {"quote": "...", "where": "..."}:\n'
        "- quote: copied VERBATIM from the paper text below — one contiguous span of at most ~40 words, "
        "no ellipses, no paraphrase, no added words. For a number taken from a table, quote the row "
        "label and the cell value as they appear (e.g. \"GPT-4o 72.3\"). Quotes are checked mechanically "
        "against the text; a quote that cannot be found counts as no evidence.\n"
        '- where: the page marker ("p. 4") and, if visible, the section or table name.\n'
        "No quote is needed (give an empty list) for not_stated, for null, and for values that record "
        "an absence — " + (", ".join(absences) if absences else "none here") + " — because silence "
        "cannot be quoted; make sure the paper really is silent before using them.\n"
        "Every other value needs a quote. If you cannot find one, change the value to not_stated "
        "(or null) rather than keep an unsupported one."
    )


LIST_ENUM_FIELDS: dict[str, set[str]] = {
    "analytical_tasks": set(ANALYTICAL_TASK_VOCAB),
    "reported_gap_kinds": set(GAP_KINDS),
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
