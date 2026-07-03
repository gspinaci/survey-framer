# SimpleQA

**Paper name:** SimpleQA
**DOI:** None
**arXiv ID:** None
**Year:** 2024
**Article URL:** https://openai.com/index/introducing-simpleqa/
**Publication year (from analysis):** 2024

## Humanities Role

**Classification:** content
**Explanation:** Humanities topics (such as history, TV shows, and video games) are treated strictly as sources of raw factual data, where questions act as short-form factual QA items without interpretive or aesthetic analysis.
**Relevant ASJC areas:** History, Literature and Literary Theory, Visual Arts and Performing Arts
**CSV Humanities?:** Yes
**CSV ASJC code:** Multidisciplinary

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | YES | Designed as a general-purpose factuality benchmark spanning various subjects including science, technology, and culture/entertainment. |
| Evaluates generative LLM | YES | Evaluates frontier generative models including GPT-4o, GPT-4o-mini, o1-preview, and o1-mini. |
| LLM is primary evaluated system | YES | The language models are the primary systems under evaluation for factuality and self-calibration. |
| Arts & Humanities data/tasks | YES | Includes questions about history, TV shows, video games, and culture, mapping to ASJC areas such as History, Literature and Literary Theory, and Visual Arts and Performing Arts. |
| Quantitative performance metrics | YES | Evaluates models using accuracy metrics (correct, incorrect, not attempted rates) and calibration curves. |
| Published after Mar 2023 | YES | Published on October 30, 2024. |
| English language | YES | The paper and the SimpleQA dataset are written in English. |

## Benchmark Modalities

**Modality Types:** text

**Description:** A text-only dataset of short, fact-seeking queries and answers, evaluated using a generative text-based classifier.

## Analytical Tasks

**Task Types:** factual QA, calibration assessment

**Detailed Description:** Evaluates closed-book factual retrieval and recognition, as well as model calibration (measuring the alignment between the model's stated confidence or output frequency and its actual correctness).

## Summary

SimpleQA is a text-based, general-purpose benchmark containing 4,326 high-quality, short-form, fact-seeking questions designed to measure the factuality and calibration of frontier LLMs. The dataset focuses on indisputable facts that frequently induce hallucinations, allowing researchers to evaluate correctness, incorrect/hallucination rates, and whether models 'know what they know.'

## Key Findings

Frontier models struggle on SimpleQA, with GPT-4o scoring under 40% accuracy. Reasoning models (o1-preview and o1-mini) exhibit better calibration and choose to 'not attempt' questions more frequently than non-reasoning models (GPT-4o), though all models still consistently overstate their confidence.

## Reviewer Notes

- Minor differences in the 'analytical_tasks' field (Ciop highlighted short-form QA while Cip highlighted calibration); resolved by including both 'factual QA' and 'calibration assessment', as both are central to the paper. Otherwise, both analysts agreed on all key fields and their explanations were merged for clarity.

## Additional Fields

**Dataset Size:** 4326

**Primary Evaluation Setting:** zero-shot
