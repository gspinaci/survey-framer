# M3Exam

**Paper name:** M3Exam: A Multilingual, Multimodal, Multilevel Benchmark for Examining Large Language Models
**DOI:** None
**arXiv ID:** None
**Year:** 2023
**Article URL:** https://proceedings.neurips.cc/paper_files/paper/2023/file/117c5c8622b0d539f74f6d1fb082a2e9-Paper-Datasets_and_Benchmarks.pdf
**Publication year (from analysis):** 2023

## Humanities Role

**Classification:** content
**Explanation:** Uses real-world humanities material—specifically history, geography, and language/linguistics questions from school examinations—as testing content to gauge general intelligence, multimodal reasoning, and cultural alignment, rather than engaging with humanities as an active domain-specific methodology.
**Relevant ASJC areas:** History, Language and Linguistics, Literature and Literary Theory
**CSV Humanities?:** 
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | YES | Evaluates LLMs across broad domains, including science, mathematics, language, and social sciences. |
| Evaluates generative LLM | YES | Evaluates closed-source generative LLMs (GPT-4, ChatGPT, Claude) and open-source/multimodal models (BLOOM, Vicuna, BLIP-2, InstructBLIP, Fromage, OpenFlamingo). |
| LLM is primary evaluated system | YES | The LLMs/MLLMs are the primary systems being benchmarked. |
| Arts & Humanities data/tasks | YES | Includes substantial materials relevant to History, Language and Linguistics, and Literature and Literary Theory. |
| Quantitative performance metrics | YES | Uses accuracy as the quantitative evaluation metric. |
| Published after Mar 2023 | YES | Presented at NeurIPS 2023. |
| English language | YES | The paper is written in English, and English is one of the nine languages featured in the benchmark. |

## Benchmark Modalities

**Modality Types:** text, image

**Description:** Multimodal multiple-choice questions integrating text with images (e.g., historical figures, maps, diagrams) within the question text or candidate option sets.

## Analytical Tasks

**Task Types:** reading comprehension, factual recognition, visual question answering, mathematical reasoning, causal reasoning

**Detailed Description:** Tasks require factual recall and reading comprehension for history and language subjects, multi-step mathematical reasoning, visual question answering over maps and diagrams, and parsing specific linguistic features.

## Summary

M3Exam is a multilingual, multimodal, and multilevel benchmark derived from real-world human graduation exams across nine countries. It contains 12,317 multiple-choice questions spanning three educational levels to evaluate LLM capabilities on diverse linguistic scripts, visual exam questions, and general intelligence.

## Key Findings

GPT-4 outperforms other models with 72.92% average accuracy but struggles with low-resource (Javanese) and non-Latin script (Thai) languages. Multimodal models perform poorly on complex visual questions, with BLIP-2 scoring under 50% overall. Notably, LLMs do not exhibit a monotonic decrease in performance as exam levels increase, contrasting sharply with human cognitive development.

## Reviewer Notes

- Ciop and Cip disagreed on humanities_role ('content' vs 'both'). Resolved to 'content' because the benchmark is a general-purpose exam dataset where humanities subjects (history, languages) are used primarily to evaluate general LLM capabilities (multilingualism, multimodality) rather than advancing domain-specific humanities methodologies. Analytical tasks were merged to include visual question answering, reading comprehension, factual recognition, and mathematical/causal reasoning.

## Additional Fields

**Dataset Size:** 12317

**Primary Evaluation Setting:** zero-shot
