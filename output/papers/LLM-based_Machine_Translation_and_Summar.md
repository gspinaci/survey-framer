# LLM-based Machine Translation and Summarization for Latin

**Paper name:** LLM-based Machine Translation and Summarization for Latin
**DOI:** None
**arXiv ID:** None
**Year:** 2024
**Article URL:** https://aclanthology.org/2024.lt4hala-1.15.pdf
**Publication year (from analysis):** 2024

## Humanities Role

**Classification:** both
**Explanation:** The paper uses 16th-century ecclesiastical and political correspondence (primary historical sources) as its content. It tests translation and cross-language summarization, demanding domain-specific historical linguistic knowledge (Neo-Latin, Early New High German, code-switching) and contextual interpretation of historical entities and concepts.
**Relevant ASJC areas:** History, Language and Linguistics, Classics
**CSV Humanities?:** Yes
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | The paper does not propose a general-purpose benchmark; it evaluates LLMs on a specific, domain-targeted historical dataset of 16th-century letters. |
| Evaluates generative LLM | YES | Evaluates GPT-4 (and compares it to Google Translate, DeepL, and other translation engines). |
| LLM is primary evaluated system | YES | GPT-4 is the primary generative system evaluated for machine translation and summarization. |
| Arts & Humanities data/tasks | YES | The dataset contains historical correspondence from the Zurich reformer Heinrich Bullinger, mapping to History, Language and Linguistics, and Classics. |
| Quantitative performance metrics | YES | Uses BLEU and ChrF scores for automatic evaluation, alongside customized quantitative human evaluation rubrics (accuracy, completeness, correctness scores). |
| Published after Mar 2023 | YES | Published in May 2024. |
| English language | YES | The paper is written in English. |

## Benchmark Modalities

**Modality Types:** text

**Description:** The evaluation is purely text-based, involving the translation and summarization of historical letters written in Latin and Early New High German into modern German and English.

## Analytical Tasks

**Task Types:** machine translation, cross-lingual summarization

**Detailed Description:** Evaluates the translation accuracy of low-resource historical languages, as well as paragraph-by-paragraph cross-lingual summarization. The human evaluation of these tasks implicitly tests for the correct preservation of archaic names, places, and events.

## Summary

This paper evaluates the capability of GPT-4 to perform machine translation and cross-lingual summarization on 16th-century letters from the Heinrich Bullinger correspondence, written in Latin and Early New High German. By comparing GPT-4 against traditional neural machine translation engines, the authors demonstrate the model's significant superiority in processing historical languages and producing summaries that align well with expert humanist editions without hallucinations.

## Key Findings

GPT-4 achieved a BLEU score of 27.07 for Latin-to-German translation (outperforming Google Translate by nearly 10 BLEU points) and 34.50 for Latin-to-English. Human evaluation of GPT-4's automatic summaries showed high correctness and historical accuracy, effectively capturing names (47.2/58) and events/times (54.5/58) with zero instances of hallucination.

## Reviewer Notes

- Ciop included 'historical entity resolution' and 'human evaluation' as standalone analytical tasks; resolved by subsuming them under cross-lingual summarization and machine translation, as they are evaluation criteria rather than distinct LLM tasks. Ciop's addition of 'Classics' to the ASJC areas was retained due to the substantial focus on Latin text.

## Additional Fields

**Dataset Size:** 121

**Primary Evaluation Setting:** zero-shot
