# HiST-LLM

**Paper name:** HiST-LLM
**DOI:** None
**arXiv ID:** None
**Year:** 2024
**Article URL:** https://neurips.cc/virtual/2024/poster/97439
**Publication year (from analysis):** 2024

## Humanities Role

**Classification:** domain
**Explanation:** Designed specifically for evaluating expert-level historical knowledge and comprehension using curated historical data from the Seshat Global History Databank
**Relevant ASJC areas:** History
**CSV Humanities?:** Yes
**CSV ASJC code:** 1202

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | YES | Evaluates general historical knowledge capabilities across multiple LLM families |
| Evaluates generative LLM | YES | Evaluated models from Gemini, OpenAI (GPT-4-Turbo), and Llama (Llama-3.1-8B) families |
| LLM is primary evaluated system | YES | LLMs are the primary systems being benchmarked for historical knowledge comprehension |
| Arts & Humanities data/tasks | YES | History - uses Seshat Global History Databank with 36,000 data points across historical societies and scholarly references |
| Quantitative performance metrics | YES | Balanced accuracy scores ranging from 33.6% to 46% compared to random baseline of 25% |
| Published after Mar 2023 | YES | Published at NeurIPS 2024 |
| English language | YES | Paper and benchmark appear to be in English |

## Benchmark Modalities

**Modality Types:** text

**Description:** Text-based evaluation using structured historical data points converted into multiple-choice questions covering global historical societies and periods

## Analytical Tasks

**Task Types:** historical knowledge comprehension, multiple-choice question answering

**Detailed Description:** Expert-level historical knowledge evaluation through four-choice format questions based on curated historical data covering 600 historical societies from Neolithic to Industrial Revolution periods across major world regions

## Summary

HiST-LLM introduces a benchmark for evaluating LLMs' expert-level historical knowledge using the Seshat Global History Databank, covering 36,000 data points across 600 historical societies from the Neolithic to Industrial Revolution. The benchmark tests seven models from major LLM families using a four-choice format, finding performance ranges from 33.6% to 46% accuracy.

## Key Findings

LLMs achieved balanced accuracy between 33.6% (Llama-3.1-8B) and 46% (GPT-4-Turbo), outperforming random chance (25%) but falling short of expert-level comprehension. Models performed better on earlier historical periods, with regional performance being more balanced but lowest in Oceania and Sub-Saharan Africa.
