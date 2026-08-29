# Cultural Long-form Multilingual Question Answering (CaLMQA)

**Paper name:** CaLMQA: Exploring culturally specific long-form question answering across 23 languages
**DOI:** None
**arXiv ID:** None
**Year:** 2024
**Article URL:** https://aclanthology.org/2025.acl-long.578.pdf
**Publication year (from analysis):** 2025

## Humanities Role

**Classification:** content
**Explanation:** The benchmark uses culturally specific topics (such as regional history, religious traditions, and local customs) as test items to evaluate general generative LLM competencies, including factuality, relevance, and language consistency in long-form generation, rather than assessing academic disciplinary methods.
**Relevant ASJC areas:** Cultural Studies, History, Language and Linguistics, Literature and Literary Theory, Religious Studies
**CSV Humanities?:** 
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | Scoped specifically to evaluating culturally specific, multilingual long-form question answering. |
| Evaluates generative LLM | YES | Evaluated state-of-the-art LLMs including GPT-4o, GPT-4-Turbo, Claude 3 Opus, Gemini 1.5 Pro, Llama 3 70B, Mixtral 8x22B, and Aya Expanse 32B. |
| Quantitative performance metrics | YES | Measures performance using surface-level accuracy (wrong language rate, repetitions), factuality (VeriScore/FACTSCORE), relevance (GPT-4o LLM-as-a-judge), and human preference rankings. |
| Published after Mar 2023 | YES | Published at ACL 2025. |

## Benchmark Modalities

**Modality Types:** text

**Description:** Monolingual textual questions requiring models to generate long-form textual answers in the corresponding language.

## Analytical Tasks

**Task Types:** factual recall, open ended qa, generation, cultural reasoning

**Detailed Description:** Long-form open-ended question answering requiring factual recall of localized historical events and traditions, reasoning over culture-specific context and norms, and coherent multilingual text generation.

## Summary

This paper introduces CaLMQA, a translation-free multilingual dataset of 51.7K culturally specific, long-form questions across 23 languages. The authors evaluate seven state-of-the-art LLMs using a multi-aspect protocol tracking linguistic surface quality, relevance, and factual precision, corroborated by human native speakers.

## Key Findings

Models generate answers with significantly more factual errors for culturally specific questions (45%-52% factual precision) than for culturally agnostic questions (64%-71%). Open-weight models struggle severely on low-resource languages, often hallucinating or generating text in the wrong language, while closed-source models lead in both automatic and human evaluations.

## Reviewer Notes

- Ciop and Cip disagreed on humanities_role. Ciop suggested 'domain', but the benchmark tests general LLM competencies (long-form QA, multilinguality, factuality) using cultural knowledge merely as test material rather than assessing disciplinary academic methods, so 'content' was chosen. Cip's 'generation' was selected over Ciop's 'fact_verification' for analytical_tasks because the LLMs themselves perform long-form generation, while fact verification is used purely as an external automated metric (VeriScore/FACTSCORE) to judge the output.
- Ciop and Cip diverged on gold_source. Ciop chose existing_metadata because the reference answers were scraped from pre-existing QA forums. Cip chose crowd_annotation because Prolific workers were hired to harvest them and Upwork freelancers authored the Kirundi answers; resolved to crowd_annotation as the hired workers were the mechanism of dataset curation and creation. Ciop's inclusion of fact_verification in analytical_tasks was dropped because fact verification is the metric used to evaluate the LLMs (FactScore), not the task the models perform. primary_evaluation_setting was added as 'zero-shot' based on the paper's explicit text.
- Ciop and Cip disagreed on reported_best_score. Ciop extracted 56.9, which is the score on the culturally agnostic baseline split; Cip extracted 49.2, which is the score on the culturally specific split that constitutes the actual CaLMQA benchmark. I resolved to 49.2 as the more accurate reflection of the main dataset.

## Additional Fields

**Dataset Size:** 51698

**Primary Evaluation Setting:** zero-shot

**Gold Source:** crowd_annotation

**Gold Beyond Stimulus:** yes

**Gold Community Dependent:** yes

**Gold Concerns Genesis:** no

**Answer Multiplicity:** graded_human_judgment

**Plurality Treatment:** not_stated

**Facets Explanation:** Reference answers are only collected for a small subset of the 51.7K questions, sourced primarily by crowdworkers hired to harvest community QA forums, with additional answers authored by hired freelancers for Kirundi. Evaluation relies on model-based scoring (VeriScore, GPT-4o) and multi-aspect human ratings on a 5-point scale rather than exact string matching against a static key. The questions require external cultural knowledge, and answers explicitly depend on the specific cultural community. Inter-annotator variance is controlled statistically, but the treatment of divergent defensible readings is not addressed.

**Reported Format Gap:** no

**Reported Format Gap Points:** None

**Human Baseline Reported:** no

**Human Gap Points:** None

**Reported Best Score:** 49.2

**Reported Best Metric:** other

**Reported Cultural Asymmetry:** yes

**Results Explanation:** The benchmark evaluates long-form question answering using a custom overall score S (S = Ssurf * Sfact * Srel). In Table 2, the best overall score S on the core culturally specific split is 49.2, achieved by GPT-4O (which also scored 56.9 on the culturally agnostic baseline split). The paper does not report a human baseline or compare performance across different answer formats on the same items. A systematic cultural asymmetry is reported, as the authors find that answers to culturally specific questions contain more factual errors than culturally agnostic ones, and that factuality and relevance drop 'considerably on low-resource languages'.
