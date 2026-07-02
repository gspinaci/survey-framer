# History Seshat Test for LLMs (HiST-LLM)

**Paper name:** HiST-LLM
**DOI:** None
**arXiv ID:** None
**Year:** 2024
**Article URL:** https://neurips.cc/virtual/2024/poster/97439
**Publication year (from analysis):** 2024

## Humanities Role

**Classification:** both
**Explanation:** Designed specifically to evaluate LLMs on historical knowledge and uses expert-curated data from the Seshat Global History Databank covering global history from the Neolithic to the Industrial Revolution.
**Relevant ASJC areas:** History, Archaeology
**CSV Humanities?:** Yes
**CSV ASJC code:** 1202

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | Designed specifically for evaluating historical knowledge and comprehension, not general capabilities. |
| Evaluates generative LLM | YES | Evaluates seven models from the Gemini, OpenAI, and Llama families, including Llama-3.1-8B and GPT-4-Turbo. |
| LLM is primary evaluated system | YES | LLMs are the primary systems evaluated on the benchmark. |
| Arts & Humanities data/tasks | YES | History, Archaeology |
| Quantitative performance metrics | YES | Balanced accuracy |
| Published after Mar 2023 | YES | Published/Presented in 2024 (NeurIPS 2024). |
| English language | YES | The paper and dataset are in English. |

## Benchmark Modalities

**Modality Types:** Text

**Description:** Text-only evaluations based on structured multiple-choice questions (four options).

## Analytical Tasks

**Task Types:** factual historical retrieval, expert-level history comprehension

**Detailed Description:** Evaluates historical fact retrieval and complex historical comprehension across different geographical regions and chronological eras (Neolithic to Industrial Revolution) in a four-choice format.

## Summary

The paper introduces HiST-LLM, a benchmark designed to evaluate Large Language Models' graduate-level historical knowledge and comprehension. Based on the Seshat Global History Databank, the benchmark evaluates models across various regions and historical periods from the Neolithic period to the Industrial Revolution. The study tests seven state-of-the-art LLMs, revealing that while they outperform random guessing, they still fall significantly short of human expert-level comprehension.

## Key Findings

LLMs achieved a balanced accuracy ranging from 33.6% (Llama-3.1-8B) to 46% (GPT-4-Turbo) on a four-choice question format, outperforming random guessing (25%) but failing to reach expert-level performance. Models performed better on earlier historical periods, with regional biases showing higher performance for the Americas and lowest for Oceania and Sub-Saharan Africa in advanced models.
