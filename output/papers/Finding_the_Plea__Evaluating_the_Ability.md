# Finding the Plea: Evaluating the Ability of LLMs to Identify Rhetorical Structure in Swedish and English Historical Petitions

**Paper name:** Finding the Plea: Evaluating the Ability of LLMs to Identify Rhetorical Structure in Swedish and English Historical Petitions
**DOI:** None
**arXiv ID:** None
**Year:** 2025
**Article URL:** https://acl-bg.org/proceedings/2025/LM4DH%202025/pdf/2025.lm4dh-1.8.pdf
**Publication year (from analysis):** 2025

## Humanities Role

**Classification:** domain
**Explanation:** The benchmark targets domain-specific competence in rhetorical analysis by evaluating whether models can accurately distinguish and segment fine-grained components of classical rhetoric (Salutatio, Petitio, and Conclusio) within 18th-century historical petitions.
**Relevant ASJC areas:** Language and Linguistics, History
**CSV Humanities?:** Yes
**CSV ASJC code:** Language and Linguistics

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | Specifically scoped to rhetorical span annotation within 18th-century Swedish and English petitions. |
| Evaluates generative LLM | YES | Evaluates GPT-4, Gemini 1.5 Pro, Mixtral 8x22B, Mistral 7B, LLaMA-3 8B, and LLaMA-3 70B. |
| Quantitative performance metrics | YES | Uses token-level Precision, Recall, F1, mean token-level edit distance, Mean Error for difficulty scores, and Spearman correlation. |
| Published after Mar 2023 | YES | Published at RANLP Workshop on NLP and Language Models for Digital Humanities in September 2025. |

## Benchmark Modalities

**Modality Types:** text

**Description:** The benchmark uses text transcriptions of 18th-century historical petitions in Swedish and English.

## Analytical Tasks

**Task Types:** information extraction, stylistic analysis, calibration and uncertainty

**Detailed Description:** Models are required to recognize and tag classical rhetorical structural elements (stylistic analysis, operationalized as span-level information extraction of Salutatio, Petitio, and Conclusio), and to self-estimate annotation difficulty which is compared against human ratings (calibration and uncertainty).

## Summary

This paper evaluates the performance of several large language models on annotating the classical rhetorical structure of 18th-century Swedish and English petitions using 1-shot and 3-shot prompting. It investigates how prompt detail, prompt language, and model scale affect span extraction performance while also comparing model self-estimated difficulty ratings against human gold labels.

## Key Findings

Models excel at identifying the formulaic Salutatio (F1 scores often in the high 90s), but isolating the Petitio and Conclusio is significantly harder, particularly for Swedish documents and smaller models. Additionally, models systematically underestimate document difficulty and show poor, often negative, correlation with human difficulty rankings.

## Reviewer Notes

- Disagreement on relevant_asjc_areas (Ciop included 'Literature and Literary Theory', Cip did not). Resolved by dropping 'Literature and Literary Theory' since the analyzed texts are legal and administrative historical petitions rather than literary works, keeping 'History' and 'Language and Linguistics'. Combined summaries and key findings for clarity.
- Ciop and Cip disagreed on human_baseline_reported and reported_best_score. For human_baseline_reported, resolved to 'yes' (favoring Cip) because the paper explicitly quantifies human inter-annotator agreement in Table 2 as a baseline for the task's complexity, even though the differing metrics make human_gap_points null. For reported_best_score, resolved to null (favoring Cip) because the paper only reports performance per section (salutatio, petitio, conclusio) and dataset, providing no single headline aggregated figure; Ciop's 100.0 was a maximum score on a specific sub-task (salutatio) rather than a benchmark headline.

## Additional Fields

**Dataset Size:** 200

**Primary Evaluation Setting:** few-shot

**Gold Source:** paper_authors

**Gold Beyond Stimulus:** no

**Gold Community Dependent:** no

**Gold Concerns Genesis:** no

**Answer Multiplicity:** single_answer

**Plurality Treatment:** noise

**Facets Explanation:** The reference annotations marking rhetorical spans in the Swedish and English historical petitions were produced manually by three annotators from the research team. Inter-annotator disagreements were systematically resolved through discussion after each batch to establish consistent guidelines and a unified consensus, thereby treating divergent readings as noise to be eliminated. The resulting task is evaluated by matching model outputs directly against this single-reference key.

**Reported Format Gap:** yes

**Reported Format Gap Points:** 22

**Human Baseline Reported:** yes

**Human Gap Points:** None

**Reported Best Score:** None

**Reported Best Metric:** None

**Reported Cultural Asymmetry:** yes

**Results Explanation:** The paper reports model performance across human-annotated difficulty regimes; for example, Mistral 7B on Swedish petitions with English instructions (long 3-shot) drops from an F1 of 72.8 on 'Difficulty 0' to 50.5 on 'Difficulty 2' (Table 6), a gap of 22.3 percentage points (recorded as 22). Human inter-annotator agreement is quantified as a baseline ceiling (e.g., 68.0% exact match and 0.88 Cohen's kappa overall for English in Table 2), but because these metrics differ from the token-level F1 used for models, the human gap is null. No single aggregated benchmark score is reported as a primary headline metric, as results are presented separately by rhetorical section and language. A systematic linguistic asymmetry is explicitly reported, noting that 'models generally found both Petitio and Conclusio more challenging to annotate in the Swedish Petitions' compared to the English ones.
