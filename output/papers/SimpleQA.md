# SimpleQA

**Paper name:** SimpleQA
**DOI:** None
**arXiv ID:** None
**Year:** 2024
**Article URL:** https://openai.com/index/introducing-simpleqa/
**Publication year (from analysis):** 2024

## Humanities Role

**Classification:** content
**Explanation:** Uses factual questions about history, media, art, and culture (e.g., television shows and video games) as part of a general-purpose dataset for evaluating LLM factuality.
**Relevant ASJC areas:** History, Visual Arts and Performing Arts, Literature and Literary Theory
**CSV Humanities?:** Yes
**CSV ASJC code:** Multidisciplinary

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | YES | Designed as a general-purpose benchmark covering science, technology, television, video games, history, and more. |
| Evaluates generative LLM | YES | Evaluates several frontier LLMs, specifically GPT-4o, GPT-4o-mini, o1-preview, and o1-mini. |
| LLM is primary evaluated system | YES | The LLM is the central system being benchmarked for its baseline factuality and calibration capabilities. |
| Arts & Humanities data/tasks | YES | Includes questions related to History, Visual Arts and Performing Arts, and Literature and Literary Theory (e.g., television shows, video games, and cultural historical events). |
| Quantitative performance metrics | YES | Evaluates using accuracy (percentage correct), hallucination rate (percentage incorrect), non-attempt rate, and calibration curve metrics. |
| Published after Mar 2023 | YES | Published on October 30, 2024. |
| English language | YES | The benchmark questions, answers, and the publication are in English. |

## Benchmark Modalities

**Modality Types:** text

**Description:** Consists of short text-based queries and ground-truth text answers, which are evaluated using an LLM-as-a-judge classifier.

## Analytical Tasks

**Task Types:** factual question answering, confidence calibration

**Detailed Description:** Short-form factual retrieval requiring precise, indisputable answers (e.g., identifying specific sports players or media titles) and meta-cognitive evaluation of model confidence versus accuracy.

## Summary

SimpleQA is a highly challenging, curated dataset of 4,326 short, fact-seeking questions designed to measure the factuality and hallucination rates of frontier large language models. To ensure high quality, the dataset utilizes independent double-trainer verification and focuses on questions with single, indisputable answers that tend to cause hallucinations in contemporary models.

## Key Findings

Even frontier models struggle significantly on SimpleQA, with GPT-4o scoring under 40% accuracy. The study shows that reasoning-optimized models (like o1-preview) choose to decline to answer ('not attempted') rather than hallucinate and demonstrate superior calibration, alignment, and awareness of their own limitations compared to standard models.
