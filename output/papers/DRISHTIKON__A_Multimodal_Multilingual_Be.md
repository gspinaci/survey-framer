# DRISHTIKON

**Paper name:** DRISHTIKON: A Multimodal Multilingual Benchmark for Testing Language Models' Understanding on Indian Culture
**DOI:** None
**arXiv ID:** None
**Year:** 2025
**Article URL:** https://aclanthology.org/2025.emnlp-main.68/
**Publication year (from analysis):** 2025

## Humanities Role

**Classification:** both
**Explanation:** The benchmark relies on Indian cultural heritage, local art forms, historical monuments, and religious festivals as both the dataset content and the domain of evaluation to test deep, culturally grounded reasoning.
**Relevant ASJC areas:** History, Language and Linguistics, Visual Arts and Performing Arts, Religious Studies
**CSV Humanities?:** 
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | It is a domain-specific benchmark centered exclusively on Indian culture, arts, and heritage. |
| Evaluates generative LLM | YES | Evaluates a wide range of vision-language models (VLMs), including open-source small and large models, proprietary systems, reasoning-specialized VLMs, and Indic-focused models. |
| LLM is primary evaluated system | YES | The primary systems being benchmarked are generative vision-language models. |
| Arts & Humanities data/tasks | YES | Covers History, Language and Linguistics, Visual Arts and Performing Arts, and Religious Studies. |
| Quantitative performance metrics | YES | Evaluates performance quantitatively across models in zero-shot and chain-of-thought reasoning settings. |
| Published after Mar 2023 | YES | Published in November 2025 at EMNLP. |
| English language | YES | The scientific paper is written in English, though the benchmark's content is multilingual. |

## Benchmark Modalities

**Modality Types:** text, image

**Description:** Comprises over 64,000 aligned text-image pairs where visual materials depicting Indian culture are combined with multilingual textual queries and descriptions.

## Analytical Tasks

**Task Types:** visual question answering, cultural reasoning, factual recognition, multilingual comprehension

**Detailed Description:** Evaluates models on factual recognition and reasoning over fine-grained cultural concepts, including historical contexts of heritage sites, ritual significance of festivals, and regional art forms, across 15 distinct languages.

## Summary

The paper introduces DRISHTIKON, a first-of-its-kind multimodal and multilingual benchmark containing over 64,000 aligned text-image pairs across 15 languages, dedicated exclusively to Indian culture. It spans diverse regional themes like historical heritage, festivals, cuisines, attire, and art forms to evaluate the cultural understanding of modern generative vision-language models.

## Key Findings

Current vision-language models show stark limitations in reasoning over culturally grounded, localized multimodal inputs, especially for low-resource Indian languages and less-documented regional traditions.

## Reviewer Notes

- Resolved disagreement on 'general_purpose_benchmark': marked false as the text explicitly states the benchmark is 'centered exclusively on Indian culture' (domain-specific). Cip missed 'chain-of-thought' in the primary evaluation setting, which was added back per the abstract. ASJC areas and analytical tasks were merged to include all accurate elements identified by both reviewers.

## Additional Fields

**Dataset Size:** 64000

**Primary Evaluation Setting:** zero-shot and chain-of-thought
