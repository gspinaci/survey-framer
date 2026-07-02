# History Seshat Test for LLMs (HiST-LLM)

**Paper name:** HiST-LLM
**DOI:** None
**arXiv ID:** None
**Year:** 2024
**Article URL:** https://neurips.cc/virtual/2024/poster/97439
**Publication year (from analysis):** 2024

## Humanities Role

**Classification:** domain
**Explanation:** Designed specifically for evaluating graduate-level historical knowledge and global history comprehension using structured historical data.
**Relevant ASJC areas:** History
**CSV Humanities?:** Yes
**CSV ASJC code:** 1202

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | Specifically targets history knowledge and comprehension, not general capabilities. |
| Evaluates generative LLM | YES | Evaluates seven models from the Gemini, OpenAI, and Llama families, including Llama-3.1-8B and GPT-4-Turbo. |
| LLM is primary evaluated system | YES | Generative LLMs are the primary systems evaluated on their historical knowledge. |
| Arts & Humanities data/tasks | YES | History |
| Quantitative performance metrics | YES | Balanced accuracy |
| Published after Mar 2023 | YES | Published at NeurIPS in 2024. |
| English language | YES | The paper and benchmark are in English. |

## Benchmark Modalities

**Modality Types:** text

**Description:** A text-only benchmark presenting multiple-choice historical questions formulated from the structured Seshat Global History Databank.

## Analytical Tasks

**Task Types:** multiple-choice QA, historical knowledge retrieval, cross-regional factual recognition

**Detailed Description:** Evaluates factual recall and understanding of historical societies spanning different periods (Neolithic to Industrial Revolution) and geographical regions.

## Summary

This paper introduces HiST-LLM, a specialized benchmark for evaluating LLMs on expert-level global history knowledge, derived from the Seshat Global History Databank. Spanning from the Neolithic period to the Industrial Revolution, it tests LLM comprehension across 600 historical societies and evaluates seven major models, identifying substantial performance disparities depending on historical epochs and geographical regions.

## Key Findings

LLMs achieved balanced accuracy scores ranging from 33.6% (Llama-3.1-8B) to 46% (GPT-4-Turbo) in a four-choice format, outperforming the random guessing baseline of 25% but falling short of human expert comprehension. Models performed better on earlier historical periods, with regional performance being highest in the Americas and lowest in Oceania and Sub-Saharan Africa for advanced models.

## Reviewer Notes

- Ciop and Cip disagreed on the full benchmark name; used the full name from Cip. Cip successfully identified the dataset size (36,000) from the abstract, which Ciop missed. Cip assumed 'zero-shot' for the primary evaluation setting, but since it is not explicitly mentioned in the provided text, Ciop's 'not specified' (adapted) was preferred. Humanities role resolved to 'domain' as it tests subject-matter factual knowledge.

## Additional Fields

**Dataset Size:** 36000

**Primary Evaluation Setting:** not specified
