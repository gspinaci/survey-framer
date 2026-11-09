RESEARCH QUESTIONS — why each field exists

This census asks one question of every benchmark: when humanities material enters an LLM benchmark, what happens to it? Every field you extract answers one of the questions below. Read the paper with the question in mind, and remember that "the paper does not say" is itself an answer: a benchmark that never states how its reference answers were produced is a finding, not a gap to fill with a plausible guess.

RQ1 — Authority of the answer key. Where do the reference answers come from, and what kind of authority do they carry? Does answering correctly require knowledge that is not in the stimulus shown to the model?
  Fields: gold_source, gold_beyond_stimulus, facets_explanation

RQ2 — Plurality. How many answers does the scoring accept? Is correctness treated as varying by cultural or linguistic community? How does the paper treat disagreement between annotators or between defensible readings?
  Fields: answer_multiplicity, gold_community_dependent, plurality_treatment

RQ3 — Instrument dependence. Does the reported score change when the format or scoring regime changes on the same material? Is there a measured human reference to compare against?
  Fields: reported_format_gap, reported_format_gap_points, primary_evaluation_setting, human_baseline_reported, human_gap_points

RQ4 — What the benchmark reports about models. The headline score and the metric it is on; whether a systematic asymmetry across cultures, languages or traditions is reported as a finding.
  Fields: reported_best_score, reported_best_metric, reported_cultural_asymmetry, key_findings, results_explanation

RQ5 — Disciplinary coverage. Which operations does the benchmark ask of the model, and which does it not? In particular, does it target how an artefact came to be (date, author, origin, provenance) rather than its content?
  Fields: analytical_tasks, humanities_role, gold_concerns_genesis, benchmark_modalities, relevant_asjc_areas, dataset_size

Gate — Does the paper fall within the census at all? You report what the paper shows; the human reviewers decide inclusion.
  Fields: inclusion_criteria
