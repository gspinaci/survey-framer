# Leveraging LLMs for Post-OCR Correction of Historical Newspapers

**Paper name:** Leveraging LLMs for Post-OCR Correction of Historical Newspapers
**DOI:** None
**arXiv ID:** None
**Year:** 2024
**Article URL:** https://aclanthology.org/2024.lt4hala-1.14.pdf
**Publication year (from analysis):** 2024

## Humanities Role

**Classification:** both
**Explanation:** Uses historical 19th-century newspaper texts as evaluation data (content) and is designed specifically to resolve a core challenge in digital humanities: improving noisy OCR text for historical primary source analysis (domain).
**Relevant ASJC areas:** History, Language and Linguistics
**CSV Humanities?:** Yes
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | The study conducts a task-specific evaluation of post-OCR correction models rather than introducing a broad, multi-task general-purpose LLM benchmark. |
| Evaluates generative LLM | YES | Evaluates the Llama 2 architecture (7B and 13B variants) under a LoRA instruction-tuning framework. |
| LLM is primary evaluated system | YES | The main focus of the evaluation is measuring the generative LLM's capacity to perform spelling and layout correction compared to sequence-to-sequence baselines. |
| Arts & Humanities data/tasks | YES | History, Language and Linguistics (utilizes 19th-century British Library Newspaper articles documenting court proceedings and criminal trials). |
| Quantitative performance metrics | YES | Uses Character Error Rate (CER) reduction percentages calculated via Levenshtein distance. |
| Published after Mar 2023 | YES | Published in May 2024 at LT4HALA @ LREC-COLING-2024. |
| English language | YES | The paper and the evaluated BLN600 corpus are in English. |

## Benchmark Modalities

**Modality Types:** text

**Description:** Monolingual English text processing, mapping degraded OCR text sequences to clean, human-transcribed ground truth text.

## Analytical Tasks

**Task Types:** post-OCR error correction, spelling correction, text normalization

**Detailed Description:** Character-level and word-level text restoration, addressing OCR substitutions, insertions, deletions, and hallucinations while preserving historical 19th-century vocabulary, abbreviations, and named entities.

## Summary

This paper investigates the adaptation of generative large language models for the post-OCR correction of historical newspapers. By instruction-tuning Llama 2 on the BLN600 dataset of 19th-century British news, the authors compare a prompt-based generative method against a standard neural machine translation baseline (BART). The results show that generative LLMs can successfully restore highly degraded archival texts, even with limited alignment data.

## Key Findings

Llama 2 (13B) achieved a 54.51% average reduction in Character Error Rate (CER) on the test set, substantially outperforming the 7B variant (43.26% reduction) and BART-large (23.30% reduction). Llama 2 also exhibited strong sample efficiency, maintaining high performance even when the training set size was restricted to very small subsets.
