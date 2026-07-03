# Evaluating LLMs for Historical Document OCR: A Methodological Framework for Digital Humanities

**Paper name:** Evaluating LLMs for Historical Document OCR: A Methodological Framework for Digital Humanities
**DOI:** None
**arXiv ID:** None
**Year:** 2025
**Article URL:** https://acl-bg.org/proceedings/2025/LM4DH%202025/pdf/2025.lm4dh-1.7.pdf
**Publication year (from analysis):** 2025

## Humanities Role

**Classification:** both
**Explanation:** Evaluates LLMs on diplomatic transcription of 18th-century Russian Civil font books for Digital Humanities workflows. Treats historical texts as philological artifacts, introducing metrics to evaluate period-specific character preservation and temporal biases.
**Relevant ASJC areas:** Language and Linguistics, History, Literature and Literary Theory, Religious Studies
**CSV Humanities?:** Yes
**CSV ASJC code:** Language and Linguistics

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | The paper presents a specialized domain-specific evaluation framework and dataset for historical Russian document OCR rather than a general-purpose benchmark. |
| Evaluates generative LLM | YES | Evaluates 12 leading multimodal LLMs, including Claude 3.5/3.7 Sonnet, GPT-4o, GPT-4.1, o4-mini, Gemini 2.0/2.5 series, Qwen2.5-VL-72B, and Llama-4 models. |
| LLM is primary evaluated system | YES | The primary focus is benchmarking LLMs as direct OCR engines and analyzing their transcription behaviors and biases. |
| Arts & Humanities data/tasks | YES | Uses 1,029 scanned pages of 18th-century Russian Civil print books spanning fiction, religion, and history, mapping to Language and Linguistics, History, Literature, and Religious Studies. |
| Quantitative performance metrics | YES | Employs standard OCR metrics (CER, WER, CaseER) alongside novel humanities-aligned metrics: Historical Character Preservation Rate (HCPR) and Archaic Insertion Rate (AIR). |
| Published after Mar 2023 | YES | Published in September 2025 (RANLP 2025). |
| English language | YES | The scientific paper and evaluation framework are written in English, though the source dataset is in historical Russian. |

## Benchmark Modalities

**Modality Types:** text, image

**Description:** Multimodal OCR evaluation combining scanned images of historical pages with textual prompts to generate natural language transcriptions.

## Analytical Tasks

**Task Types:** optical character recognition, diplomatic transcription, orthographic fidelity analysis, temporal bias analysis

**Detailed Description:** Evaluates character-level transcription fidelity of 18th-century Russian Civil font, testing the preservation of period-specific characters and identifying systematic temporal errors, such as the 'over-historicization' insertion of archaic pre-Petrine characters.

## Summary

This paper presents a methodological framework and a novel 1,029-page dataset for evaluating LLM-based OCR on historical documents, specifically focusing on 18th-century Russian Civil print. It introduces novel philological metrics, such as Historical Character Preservation Rate (HCPR) and Archaic Insertion Rate (AIR), to measure period-specific temporal biases. The study evaluates 12 multimodal models, revealing that while top-performing LLMs outpace traditional OCR, they systematically suffer from 'over-historicization' by hallucinating and inserting obsolete, pre-reform characters.

## Key Findings

Gemini 2.5 Pro and Qwen 2.5 VL achieved the highest transcription accuracy and output stability on the historical Russian OCR task. A critical finding is 'over-historicization': LLMs (especially OpenAI models) frequently inserted obsolete medieval Slavonic characters that had already been eliminated from the 18th-century Civil font. Additionally, providing historical text to LLMs for post-OCR correction was found to degrade performance compared to direct zero-shot transcription from the image.

## Reviewer Notes

- Minor differences were found in the analytical tasks and ASJC area mapping. The analytical tasks were merged to include both 'optical character recognition' (from Cip) and 'temporal bias analysis / orthographic fidelity' (from Ciop). The ASJC areas were expanded beyond History and Linguistics to include Literature and Religious Studies, as the paper text explicitly notes fiction (22.7%) and religion (15.7%) as major components of the dataset. Summaries and key findings were synthesized to capture both the raw accuracy metrics and the novel philological phenomena ('over-historicization').

## Additional Fields

**Dataset Size:** 1029

**Primary Evaluation Setting:** zero-shot
