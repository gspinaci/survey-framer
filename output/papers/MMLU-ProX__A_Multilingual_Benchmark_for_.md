# MMLU-ProX

**Paper name:** MMLU-ProX: A Multilingual Benchmark for Advanced Large Language Model Evaluation
**DOI:** None
**arXiv ID:** None
**Year:** 2025
**Article URL:** https://aclanthology.org/2025.emnlp-main.79.pdf
**Publication year (from analysis):** 2025

## Humanities Role

**Classification:** content
**Explanation:** Humanities subjects (such as history, philosophy, and literature) inherited from MMLU-Pro are utilized as static factual and reasoning-focused question-answering data to evaluate large language models' capabilities across 29 languages.
**Relevant ASJC areas:** History, Philosophy, Literature and Literary Theory, Language and Linguistics
**CSV Humanities?:** 
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | YES | Evaluates LLM capabilities across 57 subjects (grouped into 14 disciplines) in 29 different languages. |
| Evaluates generative LLM | YES | Evaluates 36 generative large language models, including GPT-4, Llama, Gemini, Qwen, DeepSeek, Mistral, and Aya. |
| LLM is primary evaluated system | YES | Generative LLMs are the primary systems being benchmarked. |
| Arts & Humanities data/tasks | YES | Includes questions categorized under History, Philosophy, Literature, and other humanities-related subjects inherited from MMLU-Pro. |
| Quantitative performance metrics | YES | Uses accuracy (percentage of correct multiple-choice selections) under zero-shot and 5-shot CoT settings. |
| Published after Mar 2023 | YES | Published in the EMNLP 2025 proceedings (November 2025). |
| English language | YES | The paper is written in English, and the English source questions are translated into 28 other target languages. |

## Benchmark Modalities

**Modality Types:** text

**Description:** The benchmark consists entirely of written text questions and multi-choice options, lacking multimodal content.

## Analytical Tasks

**Task Types:** multiple-choice question answering, cross-lingual reasoning, factual recognition, chain-of-thought reasoning

**Detailed Description:** Evaluates complex academic knowledge retrieval, cross-lingual reasoning, and multi-step deduction across disciplines using 10-choice questions and Chain-of-Thought prompting.

## Summary

The paper introduces MMLU-ProX, a comprehensive multilingual benchmark spanning 29 typologically diverse languages to evaluate the advanced reasoning capabilities of LLMs. Developed via a semi-automated translation pipeline combined with extensive expert native-speaker verification, it scales the reasoning-focused design of MMLU-Pro to 11,829 parallel questions per language. Extensive evaluations of 36 state-of-the-art models demonstrate significant performance disparities, serving as a high-difficulty diagnostic tool for global LLM evaluation.

## Key Findings

DeepSeek-R1 achieved the highest overall average accuracy of 75.5% across all 29 languages, followed by GPT-4.1 (72.7%). Reasoning-focused models (e.g., DeepSeek-R1, Qwen3-Think) showed significant accuracy boosts over standard base models, especially in low-resource settings. A massive performance disparity remains across linguistic groups: high-resource European and East Asian languages show strong performance (often over 75%), while low-resource African languages like Wolof drop heavily.

## Reviewer Notes

- Minor differences in task naming and ASJC areas (CIP included Literature, which is supported as part of MMLU subjects). Ciop noted 14 disciplines while Cip noted 57 subjects; both are mentioned in the paper, so the inclusion note was merged to reflect 57 subjects grouped into 14 disciplines. Otherwise, no significant disagreements.

## Additional Fields

**Dataset Size:** 343041

**Primary Evaluation Setting:** few-shot
