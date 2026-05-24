# EvaHan2024

**Paper name:** Overview of EvaHan2024
**DOI:** None
**arXiv ID:** None
**Year:** 2024
**Article URL:** https://aclanthology.org/2024.lt4hala-1.27.pdf
**Publication year (from analysis):** 2024

## Humanities Role

**Classification:** domain
**Explanation:** Designed specifically for ancient Chinese computational humanities to automate sentence segmentation and punctuation on classical historical texts.
**Relevant ASJC areas:** Language and Linguistics, History, Literature and Literary Theory, Religious Studies
**CSV Humanities?:** Yes
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | It is a highly specialized domain-specific benchmark for ancient Chinese texts. |
| Evaluates generative LLM | YES | Evaluates generative LLMs, specifically XunziALLM (Xunzi-Qianwen-7B-CHAT) as a baseline and various participant-developed LLM systems. |
| LLM is primary evaluated system | YES | LLMs and LLM-based pipelines are the primary systems being benchmarked and evaluated. |
| Arts & Humanities data/tasks | YES | Uses historical Chinese texts (Siku Quanshu, Zuozhuan, local chronicles, Buddhist sutras, academy records) belonging to Language and Linguistics, History, Literature and Literary Theory, and Religious Studies. |
| Quantitative performance metrics | YES | Evaluates performance using Precision, Recall, and F1 score for both segmentation and punctuation. |
| Published after Mar 2023 | YES | Published in May 2024. |
| English language | YES | The paper is written in English, though the underlying benchmark dataset is in ancient Chinese. |

## Benchmark Modalities

**Modality Types:** text

**Description:** Monolingual text processing involving the parsing of raw classical Chinese characters into punctuated sentences.

## Analytical Tasks

**Task Types:** sentence segmentation, punctuation restoration

**Detailed Description:** Sentence segmentation (identifying clause and sentence boundaries in ancient texts) and sentence punctuation (predicting and placing 11 different types of punctuation marks, including paired quotes and book titles, at correct boundaries).

## Summary

This paper presents the results and analysis of EvaHan2024, the first international shared task evaluating automatic sentence segmentation and punctuation of ancient Chinese texts. The evaluation uses training data from Siku Quanshu and blind tests from unpublished historical sources to evaluate the capabilities of modern NLP models, particularly large language models.

## Key Findings

The top-performing system (MiDU) achieved F1 scores of 88.47% for sentence segmentation and 75.29% for punctuation in the closed modality. Generative LLMs outperformed traditional models but suffered from over-generation issues, altering 1-2% (up to 8%) of original characters, highlighting the critical need for post-processing text consistency.
