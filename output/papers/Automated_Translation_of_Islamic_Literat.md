# Automated Translation of Islamic Literature with LLMs: Al-Shamela Library

**Paper name:** Automated Translation of Islamic Literature with LLMs: Al-Shamela Library
**DOI:** None
**arXiv ID:** None
**Year:** 2025
**Article URL:** https://aclanthology.org/2025.clrel-1.5.pdf
**Publication year (from analysis):** 2025

## Humanities Role

**Classification:** domain
**Explanation:** Evaluates LLM translation quality specifically on classical Islamic scholarly literature (including the Qur'an, Hadith, Tafseer, and Jurisprudence), emphasizing the preservation of sacred text accuracy.
**Relevant ASJC areas:** Religious Studies, Language and Linguistics, Literature and Literary Theory
**CSV Humanities?:** Yes
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | The paper presents an application-specific translation pipeline and evaluation framework for Islamic texts rather than a general-purpose benchmark dataset. |
| Evaluates generative LLM | YES | Evaluates proprietary LLMs (GPT-4o, GPT-4o-mini, Claude 3.5 Sonnet, Claude 3.5/3.0 Haiku) and open-source models (Llama 3.2, Qwen 2.5, Silma, Jais, Mistral). |
| LLM is primary evaluated system | YES | Generative LLMs are the primary systems evaluated for OCR, forward translation, and back-translation verification. |
| Arts & Humanities data/tasks | YES | Evaluates on historical Islamic literature spanning Religious Studies, Literature, and Philosophy. |
| Quantitative performance metrics | YES | Uses vector embedding cosine similarity scores to quantitatively validate translation fidelity. |
| Published after Mar 2023 | YES | Published in January 2025. |
| English language | YES | The paper is written in English and focuses on translating an Arabic corpus into English. |

## Benchmark Modalities

**Modality Types:** text

**Description:** Processes Arabic text (including OCR from document images) from the Al-Shamela digital library and evaluates the generated English translation and Arabic back-translations strictly as text.

## Analytical Tasks

**Task Types:** machine translation, semantic similarity, back-translation validation, optical character recognition

**Detailed Description:** The primary task is translating classical, highly figurative Arabic religious literature into English. Semantic preservation is then quantitatively evaluated through an automated back-translation task followed by embedding-based cosine similarity analysis.

## Summary

This paper presents an automated pipeline using LLMs (primarily GPT-4o-mini) to translate over 250,000 pages of classical Islamic scholarly literature from the Al-Shamela library into English. It introduces a validation framework that uses LLMs to back-translate the English text into Arabic and evaluates meaning preservation via vector embedding cosine similarity.

## Key Findings

GPT-4o-mini was identified as the most cost-effective and high-quality forward translation model. The validation method demonstrated that 71% of OpenAI-based back-translations and 86% of Anthropic-based back-translations achieved an acceptable semantic preservation score (cosine similarity >= 0.7) compared to the original Arabic source.

## Reviewer Notes

- No significant disagreements. Merged the analytical tasks to include MT, back-translation, semantic similarity, and OCR. Adopted Cip's dataset_size of 250000, which reflects the number of pages processed and evaluated in the application corpus.

## Additional Fields

**Dataset Size:** 250000

**Primary Evaluation Setting:** zero-shot
