# Evaluating LLMs for Historical Document OCR: A Methodological Framework for Digital Humanities

**Paper name:** Evaluating LLMs for Historical Document OCR: A Methodological Framework for Digital Humanities
**DOI:** None
**arXiv ID:** None
**Year:** 2025
**Article URL:** https://acl-bg.org/proceedings/2025/LM4DH%202025/pdf/2025.lm4dh-1.7.pdf
**Publication year (from analysis):** 2025

## Humanities Role

**Classification:** both
**Explanation:** Uses a newly digitized corpus of 18th-century Russian Civil font books as evaluation data (content) and designs domain-specific evaluation protocols and metrics tailored to historical diplomatic transcription in Digital Humanities (domain).
**Relevant ASJC areas:** Language and Linguistics, History, Literature and Literary Theory, Religious Studies
**CSV Humanities?:** Yes
**CSV ASJC code:** Language and Linguistics

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | The evaluation framework and dataset are highly specialized for historical OCR and diplomatic transcription, rather than a general-purpose benchmark. |
| Evaluates generative LLM | YES | Evaluates 12 commercial and open-source generative multimodal LLMs, including Claude (3.7 Sonnet, 3.5 Sonnet), OpenAI (GPT-4o, GPT-4.1, o4-mini), Gemini (2.0 Flash, 2.5 Pro, 2.5 Flash, 2.0 Flash-Lite), Qwen2.5-VL, and Llama-4 (Maverick, Scout). |
| LLM is primary evaluated system | YES | LLMs are the primary systems being benchmarked for direct OCR recognition and post-OCR correction. |
| Arts & Humanities data/tasks | YES | Uses 1,029 scanned pages from 428 unique 18th-century Russian books across ASJC areas such as History, Language and Linguistics, Literature and Literary Theory (fiction), and Religious Studies. |
| Quantitative performance metrics | YES | Employs Character Error Rate (WER), Word Error Rate (WER), Case-Insensitive metrics, Historical Character Preservation Rate (HCPR), Archaic Insertion Rate (AIR), Case Error Rate (CaseER), and Coefficient of Variation (CV) for stability testing. |
| Published after Mar 2023 | YES | Published in September 2025. |
| English language | YES | The paper is written in English, and includes prompts in both English and Russian. |

## Benchmark Modalities

**Modality Types:** image, text

**Description:** Multimodal OCR task where models are evaluated on transcribing historical document page images using textual prompts with different levels of contextual information.

## Analytical Tasks

**Task Types:** diplomatic transcription, optical character recognition, historical character preservation, error analysis, post-OCR correction

**Detailed Description:** Transcription of 18th-century Russian texts with character-level accuracy (preserving original orthography, hyphens, and typos), and evaluation of model performance under constraints like 'over-historicization' (incorrect insertion of obsolete pre-Petrine characters).

## Summary

This paper presents a comprehensive methodological framework and evaluation dataset for benchmarking LLMs on historical OCR, specifically focusing on 18th-century Russian Civil font documents. The author introduces novel metrics like Historical Character Preservation Rate (HCPR) and Archaic Insertion Rate (AIR) to detect subtle temporal biases and 'over-historicization' errors in LLM outputs. The study evaluates 12 leading multimodal LLMs, establishing guidelines for model selection, prompting strategies, and quality assessment in digital humanities digitization workflows.

## Key Findings

Gemini 2.5 Pro achieved the best overall performance with a 3.36% CER and 4.69% WER in full-page mode, alongside the highest output stability (CV of 0.037). Top LLMs significantly outperformed traditional OCR systems like Tesseract (21.55% CER) and specialized Transkribus PyLaia models (26.93% CER). However, LLMs (especially OpenAI models) exhibited 'over-historicization' by inserting pre-Petrine archaic characters (e.g., GPT-4o introduced archaic characters in 59% of files). Furthermore, LLM-based post-OCR correction consistently degraded transcription quality rather than improving it.
