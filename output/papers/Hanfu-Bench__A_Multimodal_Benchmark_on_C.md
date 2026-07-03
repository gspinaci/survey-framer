# Hanfu-Bench

**Paper name:** Hanfu-Bench: A Multimodal Benchmark on Cross-Temporal Cultural Understanding and Transcreation
**DOI:** None
**arXiv ID:** None
**Year:** 2025
**Article URL:** https://aclanthology.org/2025.emnlp-main.1251.pdf
**Publication year (from analysis):** 2025

## Humanities Role

**Classification:** both
**Explanation:** Evaluates historical Chinese clothing (Hanfu) as both visual content and a structured domain of material culture, requiring models to understand cross-temporal dynastic evolution and apply traditional aesthetic elements to modern transcreation.
**Relevant ASJC areas:** History, Visual Arts and Performing Arts, Archaeology, Conservation
**CSV Humanities?:** 
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | Hanfu-Bench is a domain-specific cultural benchmark focusing on Chinese Hanfu clothing and material culture across dynasties. |
| Evaluates generative LLM | YES | Evaluated Vision-Language Models including GPT-4o, Doubao-1.5-V, InternVL2.5, Qwen2.5-VL-7B-Instruct, and MiniCPM-V 2.6, alongside diffusion models. |
| LLM is primary evaluated system | YES | The primary objective is to evaluate the zero-shot performance and reasoning capacities of large vision-language models on cultural VQA and transcreation tasks. |
| Arts & Humanities data/tasks | YES | Aligned with Visual Arts and Performing Arts (fashion/design), History (dynastic periods), Archaeology, and Conservation. |
| Quantitative performance metrics | YES | Uses Accuracy for VQA tasks, and 5-point expert human evaluation metrics for transcreation (visual-change, semantic-equivalence, naturalness, modern-adaptability, cultural-inheritance, attractiveness). |
| Published after Mar 2023 | YES | Published in the EMNLP 2025 proceedings (November 2025). |
| English language | YES | The paper is written in English, although dataset prompts and tasks leverage bilingual structures (Chinese and English). |

## Benchmark Modalities

**Modality Types:** text, image

**Description:** Combines images of traditional Hanfu attire with natural language questions for single and multi-image VQA, and text prompts for cultural image transcreation.

## Analytical Tasks

**Task Types:** visual question answering, fine-grained visual recognition, cross-temporal reasoning, cultural image transcreation

**Detailed Description:** Tasks include fine-grained visual recognition of historical clothing components (e.g., collars, sleeves), cross-temporal comparative reasoning across dynasties using multiple images, and cultural image transcreation (adapting traditional garments into modern designs while preserving cultural elements).

## Summary

Hanfu-Bench is an expert-curated multimodal benchmark designed to evaluate vision-language models on traditional Chinese Hanfu across multiple historical dynasties. It introduces two tasks: cultural visual understanding (via single- and multi-image VQA) and cultural image transcreation (assessing the ability to transform traditional designs into modern attire while preserving cultural heritage).

## Key Findings

Closed-source VLMs perform comparably to non-expert humans on cultural visual understanding but lag by roughly 10% behind experts, while open-source models fall significantly short. Notably, VLMs struggle with multi-image reasoning compared to single-image tasks, in stark contrast to humans. On the image transcreation task, the best-performing model achieved a success rate of only 42% under expert human evaluation, highlighting major gaps in AI's capacity for culturally grounded creative synthesis.

## Reviewer Notes

- Ciop reported dataset_size as 1192 (total images), while Cip reported 4186 (total VQA questions: 1721 SVQA + 2465 MVQA); resolved to 4186 as it represents the number of evaluation items in the benchmark. Disagreements on relevant ASJC areas (Archaeology vs. Conservation) were resolved by keeping both, as the paper touches on cultural restoration and historical material culture. Minor wording differences in analytical tasks were consolidated.

## Additional Fields

**Dataset Size:** 4186

**Primary Evaluation Setting:** zero-shot
