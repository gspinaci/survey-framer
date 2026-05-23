# HiST-LLM

**Paper name:** HiST-LLM
**DOI:** None
**arXiv ID:** None
**Year:** 2024
**Article URL:** https://neurips.cc/virtual/2024/poster/97439
**Publication year (from analysis):** 2024

## Humanities Role

**Classification:** both
**Explanation:** Uses expert-curated historical data from the Seshat Global History Databank as content and is specifically designed for evaluating graduate-level history comprehension
**Relevant ASJC areas:** History
**CSV Humanities?:** Yes
**CSV ASJC code:** 1202

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | YES | Evaluates multiple LLM families on standardized historical knowledge tasks |
| Evaluates generative LLM | YES | GPT-4-Turbo, Llama-3.1-8B, and Gemini family models |
| LLM is primary evaluated system | YES | LLMs are the primary systems being benchmarked for historical knowledge |
| Arts & Humanities data/tasks | YES | History - uses Seshat Global History Databank covering 600 historical societies |
| Quantitative performance metrics | YES | Balanced accuracy scores ranging from 33.6% to 46% |
| Published after Mar 2023 | YES | Published at NeurIPS 2024 |
| English language | YES | Paper and benchmark appear to be in English |

## Benchmark Modalities

**Modality Types:** text

**Description:** Text-based four-choice questions derived from structured historical data covering 600 historical societies

## Analytical Tasks

**Task Types:** historical knowledge assessment, factual comprehension

**Detailed Description:** Graduate-level historical knowledge evaluation across major world regions from Neolithic to Industrial Revolution, testing factual understanding of historical societies and periods

## Summary

HiST-LLM introduces a benchmark for evaluating LLMs' graduate-level historical knowledge using the expert-curated Seshat Global History Databank. The benchmark tests seven major LLM models on 36,000 data points covering 600 historical societies from the Neolithic to Industrial Revolution.

## Key Findings

LLMs achieved balanced accuracy between 33.6% (Llama-3.1-8B) and 46% (GPT-4-Turbo) on four-choice historical questions, outperforming random chance (25%) but falling short of expert-level comprehension. Performance varied by historical period and region, with better results on earlier periods and uneven regional performance.
