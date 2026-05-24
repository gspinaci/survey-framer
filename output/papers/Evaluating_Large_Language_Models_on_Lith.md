# Evaluating Large Language Models on Lithuanian Grammatical Cases

**Paper name:** Evaluating Large Language Models on Lithuanian Grammatical Cases
**DOI:** None
**arXiv ID:** None
**Year:** 2026
**Article URL:** https://aclanthology.org/2026.loreslm-1.32.pdf
**Publication year (from analysis):** 2026

## Humanities Role

**Classification:** both
**Explanation:** Evaluates the linguistic and syntactic capabilities (domain) of LLMs using Lithuanian grammatical error data sourced from language regulatory authorities (content).
**Relevant ASJC areas:** Language and Linguistics
**CSV Humanities?:** Borderline
**CSV ASJC code:** Language and Linguistics

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | It is a targeted evaluation benchmark focusing specifically on Lithuanian grammatical cases rather than broad general-purpose capabilities. |
| Evaluates generative LLM | YES | Evaluates multiple LLM families including Neurotechnology LLM (7B, 13B), EuroLLM (1.7B, 9B, 22B), and Qwen3 (0.6B to 30B). |
| LLM is primary evaluated system | YES | The LLMs are the primary systems under evaluation. |
| Arts & Humanities data/tasks | YES | The dataset is designed around Lithuanian morphology and syntax, which falls under Language and Linguistics. |
| Quantitative performance metrics | YES | Uses accuracy computed via normalized negative log-likelihood (NLL) comparisons. |
| Published after Mar 2023 | YES | Published in March 2026. |
| English language | YES | The paper is written in English, although the benchmark dataset itself is in Lithuanian. |

## Benchmark Modalities

**Modality Types:** text

**Description:** Evaluation is performed using text-only minimal pairs consisting of grammatical and ungrammatical Lithuanian sentences.

## Analytical Tasks

**Task Types:** syntactic acceptability judgment, morphological error detection

**Detailed Description:** Evaluates the model's capacity to recognize correct grammatical case markings and syntactic structures by comparing sentence negative log-likelihoods (acceptability judgment).

## Summary

The paper introduces a new Lithuanian grammatical case marking benchmark consisting of 305 minimal sentence pairs across six cases and various error types. It evaluates three LLM families (Neurotechnology, EuroLLM, and Qwen3) to assess their morphological and syntactic competence in a low-resource setting. The results show that Lithuanian case marking remains highly challenging, with monolingual training offering a significant advantage over model scale.

## Key Findings

Overall model accuracies ranged from 0.662 to 0.852, with the Lithuanian-specific Neurotechnology 7B model achieving the highest overall accuracy (0.852). Models generally showed higher accuracy on genitive and locative cases but struggled with complex rules and rare cases like the vocative (where non-Lithuanian models scored as low as 0.091).
