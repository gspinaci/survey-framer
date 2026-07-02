# Benchmarking Open-Source Large Language Models for Persian in Zero-Shot and Few-Shot Learning

**Paper name:** Benchmarking Open-Source Large Language Models for Persian in Zero-Shot and Few-Shot Learning
**DOI:** None
**arXiv ID:** None
**Year:** 2025
**Article URL:** https://arxiv.org/html/2510.12807v1
**Publication year (from analysis):** 2024

## Humanities Role

**Classification:** content
**Explanation:** Uses Persian MMLU subcategories covering humanities subjects (Theology, History, Philosophy, Literature) and linguistic tasks to evaluate general-purpose LLM capabilities.
**Relevant ASJC areas:** Language and Linguistics, Philosophy, Religious Studies, History, Literature and Literary Theory
**CSV Humanities?:** Yes
**CSV ASJC code:** Language and Linguistics

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | YES | Evaluates LLMs across a wide array of general NLP tasks and multiple academic subject domains. |
| Evaluates generative LLM | YES | Evaluates eleven open-source LLMs including Gemma 2, GLM4, Llama 3.1, Llama 3.2, Qwen 2, Qwen 2.5, Mistral, Marco-O1, Aya Expanse, Falcon 3, and Tulu 3. |
| LLM is primary evaluated system | YES | The LLMs are the primary systems being benchmarked and compared. |
| Arts & Humanities data/tasks | YES | Utilizes datasets containing content in Language and Linguistics, Philosophy, Religious Studies (Theology), History, and Literature. |
| Quantitative performance metrics | YES | Evaluates performance using Accuracy, F1-score (macro and token-level), Exact Match, BLEU, and ROUGE metrics. |
| Published after Mar 2023 | YES | Published/released in 2024, containing references up to late 2024. |
| English language | YES | The paper is written in English. |

## Benchmark Modalities

**Modality Types:** text

**Description:** Monolingual and cross-lingual text-based NLP tasks including reading comprehension, translation, and multiple-choice question answering.

## Analytical Tasks

**Task Types:** reading comprehension, textual entailment, sentiment classification, machine translation, emotion detection, named entity recognition, multiple-choice question answering, abstractive summarization

**Detailed Description:** Evaluates semantic reasoning (textual entailment), factual recall and academic reasoning across multiple disciplines (Persian MMLU), sequence labeling (named entity recognition), affective classification (sentiment and emotion), and generative text processing (summarization and translation).

## Summary

This paper presents a comprehensive benchmarking study of eleven open-source large language models on Persian natural language processing. Using zero-shot and 5-shot learning paradigms, the models are evaluated across multiple established Persian datasets covering sentiment analysis, named entity recognition, reading comprehension, machine translation, summarization, and academic subject knowledge. The results demonstrate that while models like Gemma 2 exhibit strong cross-lingual transfer, substantial performance gaps and difficulties with token-level understanding (such as NER) persist for Persian.

## Key Findings

Gemma 2 consistently outperformed all other models, achieving the highest overall average score of 0.61 in few-shot and 0.42 in zero-shot settings. Few-shot prompting yielded an average performance improvement of 13.8% across tasks, with the most notable gains in semantic reasoning (17.3% gain). However, models struggled with sequence labeling in Named Entity Recognition (achieving very low scores, such as single-digit F1-scores in zero-shot settings), and performed better in humanities subjects (average score: 0.395) compared to STEM fields (average score: 0.287) in the Persian MMLU benchmark.
