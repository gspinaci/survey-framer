# CaLMQA

**Paper name:** CaLMQA: Exploring culturally specific long-form question answering across 23 languages
**DOI:** None
**arXiv ID:** None
**Year:** 2024
**Article URL:** https://aclanthology.org/2025.acl-long.578.pdf
**Publication year (from analysis):** 2025

## Humanities Role

**Classification:** both
**Explanation:** Evaluates LLMs on domain-specific cultural knowledge (history, religion, literature, and customs) using culturally specific, long-form questions, serving both as a content repository and an evaluation domain of global cultural alignment.
**Relevant ASJC areas:** History, Language and Linguistics, Literature and Literary Theory, Religious Studies, Visual Arts and Performing Arts
**CSV Humanities?:** 
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | It is a specialized benchmark focusing specifically on culturally specific, multilingual, long-form question answering. |
| Evaluates generative LLM | YES | Evaluates Claude-3-Opus, Gemini-1.5-Pro, GPT-4-Turbo, GPT-4o, Aya-Expanse-32B, Llama-3-70B, and Mixtral-8x22B. |
| LLM is primary evaluated system | YES | Generative LLMs are the primary systems being benchmarked on long-form generation quality and cultural knowledge. |
| Arts & Humanities data/tasks | YES | Covers several ASJC humanities areas including History, Language and Linguistics, Literature and Literary Theory, Religious Studies, and Visual Arts and Performing Arts. |
| Quantitative performance metrics | YES | Uses language identification accuracy, token repetition rate, factual precision (via VeriScore/FactScore claim counts), relevance (LLM-as-a-judge), and human evaluation ratings. |
| Published after Mar 2023 | YES | Published at ACL 2025 (July 2025). |
| English language | YES | The paper is written in English and describes a multilingual benchmark. |

## Benchmark Modalities

**Modality Types:** text

**Description:** A text-only long-form question answering dataset consisting of 51.7K questions across 23 languages, where questions are written in the native language of the target culture and require multi-sentence textual answers.

## Analytical Tasks

**Task Types:** long-form question answering, factual reasoning, cultural reasoning, factuality verification

**Detailed Description:** The benchmark evaluates models on long-form question answering requiring complex narrative synthesis, contextual interpretation, and cultural reasoning (e.g., explaining localized social practices, historical naming traditions, and regional governance policies), alongside assessing factual precision, output relevance, and language adherence.

## Summary

This paper presents CaLMQA, a multilingual long-form question answering dataset designed to benchmark LLM knowledge of culturally specific and regionally localized concepts across 23 languages. It establishes a rigorous evaluation framework measuring surface-level output quality, factual precision, and semantic relevance, paired with human ratings from native speakers. The findings show a pronounced gap in LLM capability when dealing with localized cultural knowledge compared to culturally agnostic topics, particularly in low-resource languages.

## Key Findings

Models show a major drop in factual precision (typically 45%-52%) when answering culturally specific questions compared to culturally agnostic ones (64%-71%). Open-weight models fail significantly on low-resource languages—frequently outputting English or apologies rather than the prompt language—while proprietary models like GPT-4o show higher language stability but still struggle with localized factual accuracy.

## Reviewer Notes

- No significant disagreements. Minor differences in how the analytical tasks and key findings were described were resolved by combining the insights from both reports. The inclusion of 'Visual Arts and Performing Arts' as an ASJC area was kept as the dataset includes questions on 'Language, Art and Literature'.

## Additional Fields

**Dataset Size:** 51698

**Primary Evaluation Setting:** zero-shot
