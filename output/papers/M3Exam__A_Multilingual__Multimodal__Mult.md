# M3Exam

**Paper name:** M3Exam: A Multilingual, Multimodal, Multilevel Benchmark for Examining Large Language Models
**DOI:** None
**arXiv ID:** None
**Year:** 2023
**Article URL:** https://proceedings.neurips.cc/paper_files/paper/2023/file/117c5c8622b0d539f74f6d1fb082a2e9-Paper-Datasets_and_Benchmarks.pdf
**Publication year (from analysis):** 2023

## Humanities Role

**Classification:** content
**Explanation:** Humanities subjects (such as history, geography, and regional languages/scripts) provide a subset of the exam questions, but the core objective of the benchmark is evaluating general-purpose language understanding, factual question answering, and multimodal alignment, rather than targeting specific humanistic scholarly methodologies.
**Relevant ASJC areas:** Language and Linguistics, History, Cultural Studies
**CSV Humanities?:** 
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | YES | Evaluates LLMs across multiple languages (9), levels of education (primary, middle, high school), and multiple subjects including language, social science, math, and natural science. |
| Evaluates generative LLM | YES | Evaluates models including GPT-4, ChatGPT (GPT-3.5), Claude-instant, BLOOM (176B), Vicuna (13B), BLIP-2, InstructBLIP, Fromage, and OpenFlamingo. |
| Quantitative performance metrics | YES | Uses accuracy as the primary evaluation metric. |
| Published after Mar 2023 | YES | Published at NeurIPS 2023 (December 2023). |

## Benchmark Modalities

**Modality Types:** text, image

**Description:** Combines text questions with accompanying images (e.g., historical photographs, maps, diagrams, and options containing visual layouts) for multimodal multiple-choice QA.

## Analytical Tasks

**Task Types:** multiple choice qa, factual recall, translation, logical and quantitative reasoning, causal and temporal reasoning, cultural reasoning, visual reasoning

**Detailed Description:** Operationalizes multiple-choice question answering testing factual recall in history, cultural reasoning using localized knowledge across 9 countries, transliteration of regional scripts (e.g., Javanese script to Latin), logical and quantitative reasoning in mathematics, causal and temporal reasoning over historical developments (e.g., Beijing suburb occupational shifts), and visual reasoning over complex diagrams, maps, and photographs.

## Summary

M3Exam is a multilingual, multimodal, and multilevel benchmark dataset designed to evaluate LLMs using official human graduation exams from primary, middle, and high school across nine diverse countries. Out of 12,317 multiple-choice questions collected, approximately 23% require cross-modal image processing, and all items are sourced directly from native educational contexts to retain local socio-cultural knowledge.

## Key Findings

GPT-4 achieves the highest average accuracy at 72.92%, but still struggles with low-resource languages (e.g., Javanese) and non-Latin scripts (e.g., Thai). Multimodal LLMs perform poorly on visual questions, failing to match simple text-only baselines due to struggles with complex image descriptions and cross-image reasoning. Additionally, LLM performance does not decrease monotonically with rising educational difficulty levels, highlighting a discrepancy between LLM capability scaling and human cognitive development.

## Reviewer Notes

- Both analysts agreed on the core metrics and humanities role (content). Cip's addition of 'logical_and_quantitative_reasoning' was retained as math questions are explicitly evaluated. Ciop's 'translation' was retained because transliteration (Javanese to Latin script) is explicitly tested and falls perfectly under the controlled vocabulary definition. Cip's 'interpretation' was dropped as the tasks represent standard school-level reading comprehension rather than hermeneutic interpretation.

## Additional Fields

**Dataset Size:** 12317

**Primary Evaluation Setting:** mix

**Gold Source:** authored_answer_key

**Gold Beyond Stimulus:** yes

**Gold Community Dependent:** no

**Gold Concerns Genesis:** no

**Answer Multiplicity:** single_answer

**Plurality Treatment:** not_addressed

**Facets Explanation:** The reference answers are sourced directly from the official answer keys of real, nationwide or regional graduation exams across nine countries. Answering these questions requires extensive prior domain and cultural knowledge that is not contained within the question stimulus itself. Because the benchmark consists entirely of standard multiple-choice questions, each question has a single static correct answer option, and the authors do not discuss or preserve divergent annotations or alternative valid interpretations.
