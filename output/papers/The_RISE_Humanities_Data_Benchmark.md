# The RISE Humanities Data Benchmark

**Paper name:** The RISE Humanities Data Benchmark
**DOI:** None
**arXiv ID:** None
**Year:** 2026
**Article URL:** https://openhumanitiesdata.metajnl.com/articles/10.5334/johd.481
**Publication year (from analysis):** 2026

## Humanities Role

**Classification:** content
**Explanation:** The benchmark uses historical documents and archival materials (e.g., medieval manuscripts, 20th-century index cards) to test generic data processing capabilities such as OCR/HTR, layout segmentation, and structured metadata extraction, rather than disciplinary interpretative competence.
**Relevant ASJC areas:** History, Language and Linguistics
**CSV Humanities?:** 
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | Focuses specifically on digital humanities and historical document-centric workflows, not broad general-purpose capabilities. |
| Evaluates generative LLM | YES | Evaluates several generative models including GPT-4, GPT-4o, GPT-5, Claude Sonnet 4.5, and Gemini 2.0 Pro. |
| Quantitative performance metrics | YES | Uses Character Error Rate (CER), F1-score, and fuzzy string matching. |
| Published after Mar 2023 | YES | Published on February 4, 2026. |

## Benchmark Modalities

**Modality Types:** text, image

**Description:** Evaluates text-only tasks like XML structure correction, as well as vision-language tasks combining historical document images with natural language instructions and structural schemas.

## Analytical Tasks

**Task Types:** transcription and correction, information extraction, visual recognition

**Detailed Description:** Tasks include handwritten and print text transcription (HTR/OCR), layout and page segmentation, signature recognition, structured metadata and entity extraction, and structural XML error correction.

## Summary

The RISE Humanities Data Benchmark introduces a framework and eight expert-curated datasets for evaluating large language and vision-language models on digital humanities workflows. The tasks focus on document-centric processing of historical sources, such as handwritten text transcription, layout segmentation, and structured metadata extraction, prioritizing realism and interpretability over scale.

## Key Findings

Top generative models perform exceptionally well on historical data extraction, with OpenAI's GPT-5 leading in metadata extraction (e.g., 89.51% on library cards), Claude 4.5 Sonnet achieving 97.47% on XML correction, and Gemini 2.0 Pro scoring 95.70% on Fraktur layout segmentation and transcription.

## Reviewer Notes

- Ciop and Cip disagreed on humanities_role; resolved to 'content' (following Ciop) because the benchmark tests general NLP/CV capabilities (transcription, segmentation, metadata extraction) using humanities materials, rather than disciplinary reasoning. Cip's dataset_size of 440 was verified by summing the item counts in Table 1 (5+33+50+57+15+5+263+12). ASJC areas were narrowed to those directly supported by the source corpora, dropping broader or unrelated areas like Classics and Literature.

## Additional Fields

**Dataset Size:** 440

**Primary Evaluation Setting:** zero-shot

**Gold Source:** domain_expert

**Gold Beyond Stimulus:** no

**Gold Community Dependent:** no

**Gold Concerns Genesis:** no

**Answer Multiplicity:** single_answer

**Plurality Treatment:** not_addressed

**Facets Explanation:** The reference answers (ground truths) were manually created or verified by domain experts affiliated with digital humanities projects at the University of Basel. The benchmark tasks focus on document understanding, layout segmentation, transcription, and structured metadata extraction directly from the provided image or text stimuli, meaning that the answers do not require external knowledge beyond the stimulus. Evaluation is executed automatically by matching the LLM output against a single expected Pydantic schema using distance metrics such as F1, Character Error Rate, or fuzzy matching. While the paper acknowledges that ground truths represent operationalised scholarly interpretation rather than absolute correctness, it does not explicitly address how annotator disagreement or alternative readings were handled during dataset construction.
