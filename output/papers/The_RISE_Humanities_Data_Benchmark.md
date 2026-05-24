# The RISE Humanities Data Benchmark

**Paper name:** The RISE Humanities Data Benchmark
**DOI:** None
**arXiv ID:** None
**Year:** 2026
**Article URL:** https://openhumanitiesdata.metajnl.com/articles/10.5334/johd.481
**Publication year (from analysis):** 2026

## Humanities Role

**Classification:** both
**Explanation:** Combines digitized historical materials (content) with evaluations tailored specifically to common workflows in digital humanities research projects (domain) such as transcription, metadata extraction, and manuscript segmentation.
**Relevant ASJC areas:** History, Language and Linguistics, Philosophy, Classics, Literature and Literary Theory
**CSV Humanities?:** 
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | Specifically designed as a domain-focused benchmark for digital humanities workflows rather than a general-purpose AI capability suite. |
| Evaluates generative LLM | YES | Evaluated multiple frontier generative models, including OpenAI GPT-4o, GPT-4.1-mini, GPT-5, Anthropic Claude Sonnet 4.5, and Google Gemini 2.0 Pro. |
| LLM is primary evaluated system | YES | The primary objective is the comparative evaluation of LLM capabilities on complex document-centered tasks. |
| Arts & Humanities data/tasks | YES | Utilizes datasets corresponding to History (historical index cards, trade records), Language and Linguistics (historical translation, multilingual catalogs), Philosophy (historical bibliographies), Classics (medieval manuscript travelogues), and Literature and Literary Theory (historical newspaper adverts). |
| Quantitative performance metrics | YES | Uses F1 score, Character Error Rate (CER), and fuzzy string matching to quantitatively evaluate schema keys. |
| Published after Mar 2023 | YES | Published on February 4, 2026. |
| English language | YES | The paper is written in English, though the evaluated materials cover multilingual humanities sources including Early Modern German, Latin, French, and Greek. |

## Benchmark Modalities

**Modality Types:** text, images

**Description:** Evaluates both vision-language (multimodal) and text-only LLMs using images of historical documents (scans of index cards, book pages, manuscript folios) and text files (such as faulty XML configurations) to generate structured schema-conforming outputs.

## Analytical Tasks

**Task Types:** transcription, metadata extraction, named entity recognition, structural reasoning, page segmentation, handwritten text recognition

**Detailed Description:** Evaluates complex domain-specific tasks including character-level recognition of historical Fraktur and medieval handwritten text, structural segmentation of dense print layouts, relational metadata mapping (e.g., matching senders and recipients from archives), and logical syntactic error correction of OCR-derived XML structures.

## Summary

The paper presents the RISE Humanities Data Benchmark, a provider-agnostic framework and a collection of curated, task-specific datasets designed to evaluate Large Language Models on document-centered humanities workflows. It addresses the challenges of digital humanities workflows by incorporating expert-verified ground truths and enforcing structured output validation through Pydantic schemas. This diagnostic, small-scale framework prioritizes realism, transparency, and longitudinal reproducibility over statistical volume.

## Key Findings

The evaluation shows high performance on structured reasoning and cleaning tasks, with Claude Sonnet 4.5 achieving 97.47% on XML correction and GPT-4.1-mini reaching 95.65% on index cards. More complex layout and historical transcription tasks remain challenging, with GPT-5 obtaining 58.40% on layout-diverse company lists and 77.00% on business correspondence metadata extraction.
