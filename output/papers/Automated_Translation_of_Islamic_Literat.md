# Automated Translation of Islamic Literature with LLMs: Al-Shamela Library

**Paper name:** Automated Translation of Islamic Literature with LLMs: Al-Shamela Library
**DOI:** None
**arXiv ID:** None
**Year:** 2025
**Article URL:** https://aclanthology.org/2025.clrel-1.5.pdf
**Publication year (from analysis):** 2025

## Humanities Role

**Classification:** domain
**Explanation:** Applies LLMs to the translation of classical Islamic religious and scholarly texts (Qur'an, Tafseer, Hadith, Jurisprudence) from Arabic to English.
**Relevant ASJC areas:** Religious Studies, Literature and Literary Theory, Language and Linguistics
**CSV Humanities?:** Yes
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | The paper presents an automated translation pipeline and a translated dataset rather than a general-purpose evaluation benchmark. |
| Evaluates generative LLM | YES | Evaluates GPT-4o, GPT-4o-mini, Llama 3.2, Qwen 2.5, Silma 9B, Jais 13B, Mistral 7B, Claude 3.5 Sonnet, Claude 3.5 Haiku, and Claude 3.0 Haiku. |
| LLM is primary evaluated system | YES | LLMs are the primary systems used for translation, OCR processing, and back-translation validation. |
| Arts & Humanities data/tasks | YES | Focuses on Religious Studies and Literature and Literary Theory (classical Islamic literature from the Al-Shamela library). |
| Quantitative performance metrics | YES | Evaluated using cosine similarity of vector embeddings. |
| Published after Mar 2023 | YES | Published in January 2025. |
| English language | YES | The paper and the target translation language are in English. |

## Benchmark Modalities

**Modality Types:** text

**Description:** Evaluates text translation quality by comparing original Arabic texts with back-translated Arabic texts using vector embeddings.

## Analytical Tasks

**Task Types:** machine translation, back-translation validation, semantic similarity analysis

**Detailed Description:** Evaluates the preservation of meaning (semantic similarity) of complex classical religious texts across forward (Arabic to English) and backward (English to Arabic) translations.

## Summary

This paper presents an automated pipeline using Large Language Models to translate over 250,000 pages of classical Islamic literature (including the Qur'an, Hadith, and Jurisprudence) from Arabic to English. To validate translation quality, the authors employ a back-translation validation methodology evaluated via vector embedding cosine similarity using OpenAI and Anthropic models.

## Key Findings

GPT-4o-mini was chosen as the primary translation model due to its cost-efficiency and translation quality. Back-translation validation revealed that 71% of OpenAI model results and 86% of Anthropic model results achieved acceptable semantic similarity (cosine similarity >= 0.7) compared to the original Arabic source texts.
