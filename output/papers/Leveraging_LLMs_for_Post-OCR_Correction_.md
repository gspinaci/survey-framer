# Leveraging LLMs for Post-OCR Correction of Historical Newspapers

**Paper name:** Leveraging LLMs for Post-OCR Correction of Historical Newspapers
**DOI:** None
**arXiv ID:** None
**Year:** 2024
**Article URL:** https://aclanthology.org/2024.lt4hala-1.14.pdf
**Publication year (from analysis):** 2024

## Humanities Role

**Classification:** both
**Explanation:** Evaluates LLMs on repairing OCR errors in 19th-century British newspaper articles, requiring the preservation of historical vocabulary, archaic currency formats, and old spelling conventions.
**Relevant ASJC areas:** History, Language and Linguistics
**CSV Humanities?:** Yes
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | The evaluation is restricted to the specific task of post-OCR correction on historical newspaper texts rather than general-purpose multi-task LLM evaluation. |
| Evaluates generative LLM | YES | Evaluates generative models Llama 2 (7B and 13B). |
| LLM is primary evaluated system | YES | The primary objective is evaluating instruction-tuned Llama 2 against a traditionally fine-tuned BART model. |
| Arts & Humanities data/tasks | YES | Uses BLN600, a dataset of 19th-century British newspaper articles (History, Language and Linguistics). |
| Quantitative performance metrics | YES | Character Error Rate (CER) reduction percentage based on Levenshtein distance. |
| Published after Mar 2023 | YES | Published May 2024. |
| English language | YES | The paper and dataset are in English. |

## Benchmark Modalities

**Modality Types:** text

**Description:** Text-only post-OCR correction task mapping corrupted historical text to human-transcribed ground truth segments.

## Analytical Tasks

**Task Types:** post-OCR correction, text denoising, spelling normalization, named entity correction

**Detailed Description:** Denoising textual sequences to correct OCR-induced character errors (substitutions, insertions, deletions) while maintaining historical linguistic context and preserving named entities.

## Summary

This paper investigates the adaptation of generative large language models for post-OCR correction of historical documents, using the BLN600 corpus of 19th-century British newspapers. By instruction-tuning Llama 2 and comparing it to fine-tuned BART, the authors demonstrate that a prompt-based generative approach significantly improves OCR quality and adapts well to low-data environments.

## Key Findings

Instruction-tuned Llama 2 13B achieved a 54.51% average reduction in Character Error Rate (CER) on the test set, substantially outperforming the fine-tuned BART Large model (23.30% reduction). Furthermore, Llama 2 demonstrated strong and robust performance even when trained on extremely small subsets of data (down to 80 samples).

## Reviewer Notes

- No significant disagreements. Minor differences in the phrasing of analytical tasks ('spelling normalization' vs 'spelling correction' and the inclusion of 'text denoising') were merged for completeness.

## Additional Fields

**Dataset Size:** 13192

**Primary Evaluation Setting:** fine-tuned
