# Automated Translation of Islamic Literature with LLMs: Al-Shamela Library

**Paper name:** Automated Translation of Islamic Literature with LLMs: Al-Shamela Library
**DOI:** None
**arXiv ID:** None
**Year:** 2025
**Article URL:** https://aclanthology.org/2025.clrel-1.5.pdf
**Publication year (from analysis):** 2025

## Humanities Role

**Classification:** content
**Explanation:** The pipeline translates classical Islamic religious texts and performs OCR on historical documents. The humanities material serves as a challenging corpus to test general machine translation and OCR capabilities, evaluated using automated semantic similarity rather than domain-specific humanistic reasoning.
**Relevant ASJC areas:** Religious Studies, Language and Linguistics
**CSV Humanities?:** Yes
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | The paper does not present a general-purpose benchmark, but rather a specialized pipeline and evaluation for translating Islamic scholarly texts. |
| Evaluates generative LLM | YES | Evaluates OpenAI's GPT-4o-mini and Anthropic's Claude 3 Haiku. |
| Quantitative performance metrics | YES | Uses cosine similarity of vector embeddings to measure semantic equivalence between original and back-translated text. |
| Published after Mar 2023 | YES | Published in January 2025. |

## Benchmark Modalities

**Modality Types:** text, image

**Description:** The translation and back-translation evaluation is text-to-text, with an auxiliary multimodal OCR step using GPT-4o to process image-based PDF pages of Arabic texts.

## Analytical Tasks

**Task Types:** translation, transcription and correction

**Detailed Description:** Automated machine translation of classical Arabic Islamic literature into English, alongside OCR-based document transcription from image-formatted PDFs.

## Summary

This paper presents an automated pipeline using LLMs to translate a massive corpus of classical Islamic literature (over 250,000 pages) from the Al-Shamela library from Arabic to English. The authors use a back-translation validation framework, applying vector embedding cosine similarity to assess the semantic fidelity of translations produced by models like GPT-4o-mini and Claude 3 Haiku.

## Key Findings

Both evaluated LLMs demonstrated strong translation fidelity, with 71% of the OpenAI back-translation results and 86% of the Anthropic back-translation results achieving acceptable cosine similarity scores of 0.7 or higher.

## Reviewer Notes

- Ciop included 'image' in modalities and 'retrieval_and_ranking' in tasks. Cip omitted them. The paper explicitly discusses using multimodal LLMs for image-based PDF OCR (Section 3.7), so 'image' was kept. 'retrieval_and_ranking' was dropped as it refers to a system-level RAG string-matching component to preserve specific verses, rather than an LLM evaluation task itself. Both analysts agreed on all other substantive fields.
- Ciop and Cip disagreed on gold_beyond_stimulus. Resolved to 'no' because the translation task is entirely derived from the source text stimulus, requiring no external factual knowledge beyond language capability. Other fields were in agreement.

## Additional Fields

**Dataset Size:** 250000

**Primary Evaluation Setting:** zero-shot

**Gold Source:** existing_metadata

**Gold Beyond Stimulus:** no

**Gold Community Dependent:** no

**Gold Concerns Genesis:** no

**Answer Multiplicity:** single_answer

**Plurality Treatment:** noise

**Facets Explanation:** The reference texts are the original classical Arabic pages lifted directly from the digital Al-Shamela Library database. For automated evaluation, the back-translated Arabic text is compared to this single original Arabic source page using cosine similarity of vector embeddings. For manual human-in-the-loop validation, translation corrections are treated as noise to be resolved, requiring a consensus of at least two separate reviewers to be accepted.

**Reported Format Gap:** no

**Reported Format Gap Points:** None

**Human Baseline Reported:** no

**Human Gap Points:** None

**Reported Best Score:** 86

**Reported Best Metric:** other

**Reported Cultural Asymmetry:** no

**Results Explanation:** The paper evaluates translation quality by back-translating English text to Arabic and computing the cosine similarity of vector embeddings. The authors report that '86% of the Anthropic model results' (using claude-3-haiku-20240307) achieved 'cosine similarity scores >= 0.7' (reported_best_score is 86, reported_best_metric is 'other'). No quantitative human baseline or format gap comparisons are provided. Regarding cultural asymmetry, the authors discuss language bias but explicitly note that the tested commercial LLMs 'did not display detectable language bias between Arabic and English'.
