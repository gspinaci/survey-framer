# DRISHTIKON

**Paper name:** DRISHTIKON: A Multimodal Multilingual Benchmark for Testing Language Models' Understanding on Indian Culture
**DOI:** None
**arXiv ID:** None
**Year:** 2025
**Article URL:** https://aclanthology.org/2025.emnlp-main.68/
**Publication year (from analysis):** 2025

## Humanities Role

**Classification:** content
**Explanation:** The benchmark uses Indian cultural heritage materials (images of festivals, attire, cuisines, and art forms) as content to evaluate the multimodal reasoning and cultural understanding capabilities of general-purpose generative AI systems.
**Relevant ASJC areas:** Cultural Studies, Visual Arts and Performing Arts, History, Language and Linguistics
**CSV Humanities?:** 
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | The benchmark is explicitly scoped to Indian cultural understanding and regional nuance, rather than general-purpose multi-task capabilities. |
| Evaluates generative LLM | YES | Evaluates open-source small and large VLMs, proprietary systems, reasoning-specialized VLMs, and Indic-focused models. |
| Quantitative performance metrics | YES | Exposes performance gaps for low-resource languages and specific traditions, indicating quantitative evaluation of model capabilities. |
| Published after Mar 2023 | YES | Published at EMNLP in November 2025. |

## Benchmark Modalities

**Modality Types:** text, image

**Description:** The benchmark consists of over 64,000 aligned text-image pairs.

## Analytical Tasks

**Task Types:** cultural reasoning, visual reasoning, visual recognition, factual recall, open ended qa

**Detailed Description:** The benchmark evaluates models on visually recognizing cultural artifacts (festivals, attire, art forms) and performing culturally grounded multimodal reasoning, assessed through zero-shot and chain-of-thought QA.

## Summary

The paper introduces DRISHTIKON, a multimodal and multilingual benchmark featuring over 64,000 text-image pairs across 15 languages designed to evaluate generative AI models' understanding of Indian culture. Covering fine-grained regional topics like festivals, art forms, and heritage, the dataset reveals significant limitations in the cultural reasoning abilities of current vision-language models.

## Key Findings

Current state-of-the-art vision-language models struggle significantly with reasoning over culturally grounded, multimodal inputs, particularly when dealing with low-resource Indic languages and less-documented regional traditions.

## Reviewer Notes

- Ciop chose 'domain' for humanities_role, while Cip chose 'content'. Resolved to 'content' because the benchmark evaluates general-purpose vision-language models using cultural heritage items as data for multimodal reasoning, rather than testing specialized academic disciplinary competence. Both analysts' analytical_tasks were merged, dropping multiple_choice_qa due to lack of explicit mention in the abstract, while retaining open_ended_qa and cultural/visual reasoning given the use of chain-of-thought prompting on aligned text-image pairs.

## Additional Fields

**Dataset Size:** 64000

**Primary Evaluation Setting:** mix

**Gold Source:** not_stated

**Gold Beyond Stimulus:** not_stated

**Gold Community Dependent:** not_stated

**Gold Concerns Genesis:** not_stated

**Answer Multiplicity:** not_stated

**Plurality Treatment:** not_stated

**Facets Explanation:** The provided text consists solely of the ACL Anthology metadata and abstract for the DRISHTIKON benchmark, lacking the full paper text or a dataset-construction section. Consequently, specific procedural details regarding the generation of reference answers, requirement of external knowledge, answer multiplicity, and plurality treatment are not stated in the source text.

**Reported Format Gap:** not_stated

**Reported Format Gap Points:** None

**Human Baseline Reported:** no

**Human Gap Points:** None

**Reported Best Score:** None

**Reported Best Metric:** None

**Reported Cultural Asymmetry:** yes

**Results Explanation:** Because the provided text contains only the ACL Anthology metadata and abstract, no numeric results, format gaps, or human baselines are reported. However, the abstract explicitly identifies a systematic performance asymmetry, noting that evaluation results expose limitations in models' cultural reasoning, 'particularly for low-resource languages and less-documented traditions.'
