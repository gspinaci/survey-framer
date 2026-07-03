# The RISE Humanities Data Benchmark

**Paper name:** The RISE Humanities Data Benchmark
**DOI:** None
**arXiv ID:** None
**Year:** 2026
**Article URL:** https://openhumanitiesdata.metajnl.com/articles/10.5334/johd.481
**Publication year (from analysis):** 2026

## Humanities Role

**Classification:** both
**Explanation:** Evaluates LLMs on domain-specific research tasks (such as transcription, layout segmentation, and structured metadata extraction) using real, expert-annotated historical and archival source materials from humanities consulting projects, treating these materials as structured content for complex document processing.
**Relevant ASJC areas:** History, Language and Linguistics, Philosophy, Classics
**CSV Humanities?:** 
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | Specifically designed as a small, specialized, domain-specific digital humanities evaluation framework rather than a general-purpose benchmark. |
| Evaluates generative LLM | YES | Evaluates models such as OpenAI's GPT-4, GPT-4o, GPT-4.1-mini, and GPT-5, Anthropic's Claude Sonnet 4.5, and Google's Gemini 2.0 Pro. |
| LLM is primary evaluated system | YES | The LLMs (text and vision-language models) are the primary systems being evaluated on their processing and extraction performance. |
| Arts & Humanities data/tasks | YES | Uses historical, linguistic, and archival sources mapping to ASJC areas: History, Language and Linguistics, Philosophy, and Classics. |
| Quantitative performance metrics | YES | Applies quantitative metrics including fuzzy string matching, F1 scores, and Character Error Rates (CER). |
| Published after Mar 2023 | YES | Published on February 4, 2026. |
| English language | YES | The paper is written in English, and the benchmark includes English tasks along with multilingual items in German, French, Latin, and Greek. |

## Benchmark Modalities

**Modality Types:** text, image

**Description:** Combines scanned document images (historical letters, index cards, print pages, and medieval manuscripts) for multimodal vision-language tasks with text-based instructions and plain text JSON/XML formats used for structured data correction and metadata extraction.

## Analytical Tasks

**Task Types:** transcription, layout segmentation, metadata extraction, named entity recognition, structural error correction, person matching

**Detailed Description:** Evaluates models on handwritten and printed (Fraktur) text recognition, document layout segmentation, multi-stage metadata extraction/NER from historical lists and library cards, person matching across correspondence, and logical/structural correction of LLM-generated XML files.

## Summary

The paper introduces the RISE Humanities Data Benchmark, a domain-specific evaluation framework designed to assess large language models on complex digital humanities workflows. The benchmark features eight curated, expert-verified datasets representing real-world challenges like transcription of historical scripts, structural correction, and metadata extraction. It provides a standardized execution pipeline and custom web interface to track and compare model performance over time.

## Key Findings

OpenAI's GPT-5 achieved the highest scores on complex extraction tasks such as Business Letters (77.00%), Company Lists (58.40%), and Library Cards (89.51%). Anthropic's Claude Sonnet 4.5 excelled at structured XML correction (97.47%), while Google's Gemini 2.0 Pro achieved 95.70% on Fraktur newspaper page segmentation and transcription.

## Reviewer Notes

- Minor disagreements on the exact benchmark name ('The RISE...' vs 'RISE...') resolved by using the full title. Discrepancies in the ASJC areas resolved by confirming the inclusion of Philosophy (from 'Bibliography of Works in the Philosophy of History') and Classics (Latin/Greek library cards) in the text, alongside History and Language and Linguistics. Combined analytical tasks to include both 'structural error correction' and 'person matching'.

## Additional Fields

**Dataset Size:** 440

**Primary Evaluation Setting:** zero-shot
