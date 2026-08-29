# MMLU-ProX

**Paper name:** MMLU-ProX: A Multilingual Benchmark for Advanced Large Language Model Evaluation
**DOI:** None
**arXiv ID:** None
**Year:** 2025
**Article URL:** https://aclanthology.org/2025.emnlp-main.79.pdf
**Publication year (from analysis):** 2025

## Humanities Role

**Classification:** content
**Explanation:** The benchmark uses various academic subjects as the thematic content of its questions to evaluate the general multi-task language understanding and advanced reasoning capabilities of LLMs across languages, rather than measuring specialized disciplinary research methods.
**Relevant ASJC areas:** Language and Linguistics, Law
**CSV Humanities?:** 
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | YES | It is a broad multi-task benchmark covering 57 subjects across humanities, social sciences, STEM, and professional fields. |
| Evaluates generative LLM | YES | Evaluates 36 generative LLMs, including DeepSeek-R1, GPT-4.1, GPT-4o, Qwen3, and Llama 3.3. |
| Quantitative performance metrics | YES | Uses accuracy (%) as the primary metric under zero-shot and 5-shot CoT evaluation settings. |
| Published after Mar 2023 | YES | Published in the EMNLP 2025 proceedings (November 2025). |

## Benchmark Modalities

**Modality Types:** text

**Description:** The benchmark is entirely text-based, consisting of multiple-choice questions across 29 target languages.

## Analytical Tasks

**Task Types:** multiple choice qa, factual recall, logical and quantitative reasoning

**Detailed Description:** The benchmark primarily consists of complex 10-option multiple-choice questions requiring massive multi-task language understanding, factual retrieval, and multi-step logical inference across 57 academic subjects.

## Summary

MMLU-ProX is a multilingual extension of the highly challenging English MMLU-Pro benchmark, featuring 11,829 identical questions parallelized across 29 typologically diverse languages. To ensure high translation quality and cultural relevance, the authors developed a semi-automated translation pipeline combining Claude 3.7 Sonnet with rigorous expert human verification.

## Key Findings

DeepSeek-R1 achieved the highest overall multilingual average of 75.5%, followed closely by GPT-4.1 (72.7%) and DeepSeek-V3 (70.5%). There is a massive performance gap between high-resource languages (where top models exceed 75% accuracy) and low-resource African languages such as Wolof, where performance dramatically degrades (ranging from 0.6% to 58.6%). Enabling thinking/reasoning modes consistently improves multilingual performance, particularly in low-resource contexts.

## Reviewer Notes

- Disagreements on `analytical_tasks`: Ciop included `causal_and_temporal_reasoning`, but this is only mentioned in the text with respect to a different benchmark (XCOPA), not MMLU-ProX itself, so it was dropped. `relevant_asjc_areas` were reduced to those explicitly supported by the text (Law) or broadly applicable to cross-lingual evaluation (Language and Linguistics), removing specific subjects like History and Philosophy which were hallucinated by both analysts based on external knowledge of the original MMLU benchmark.

## Additional Fields

**Dataset Size:** 343041

**Primary Evaluation Setting:** mix

**Gold Source:** authored_answer_key

**Gold Beyond Stimulus:** yes

**Gold Community Dependent:** no

**Gold Concerns Genesis:** no

**Answer Multiplicity:** single_answer

**Plurality Treatment:** not_stated

**Facets Explanation:** MMLU-ProX translates the MMLU-Pro benchmark, which draws its multiple-choice questions and ground-truth options from pre-existing standardized exams and academic curricula (authored_answer_key). Answering these questions requires extensive background domain knowledge not present in the brief query (gold_beyond_stimulus: yes). The benchmark assumes a single, universally correct choice across all 29 translated versions without adjusting keys for cultural context (gold_community_dependent: no). Disagreements among the human translators verifying the translations were treated as quality flags for the translation rather than conceptual plurality, and plurality of interpretations of the answers themselves is not addressed.

**Reported Format Gap:** no

**Reported Format Gap Points:** None

**Human Baseline Reported:** no

**Human Gap Points:** None

**Reported Best Score:** 75.5

**Reported Best Metric:** accuracy

**Reported Cultural Asymmetry:** yes

**Results Explanation:** The paper does not report any performance differences across task formats or difficulty tiers on the same items, evaluating models consistently on a 10-choice multiple-choice format. No human baseline is provided for solving the benchmark questions, only a human evaluation for translation quality. The best reported headline score is 75.5% average accuracy across 29 languages, achieved by DeepSeek-R1 ('DeepSeek-R1 demonstrates superior overall performance with an average of 75.5% across all languages'). A systematic cultural and linguistic asymmetry is reported as a primary finding: 'While they perform well in high-resource languages, their performance declines markedly in low-resource languages, particularly for African languages.'
