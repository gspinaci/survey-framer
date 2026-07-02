# Travelogues ABSA Dataset

**Paper name:** Exploring Aspect-Based Sentiment Analysis Methodologies for Literary-Historical Research Purposes
**DOI:** None
**arXiv ID:** None
**Year:** 2024
**Article URL:** https://aclanthology.org/2024.lt4hala-1.16.pdf
**Publication year (from analysis):** 2024

## Humanities Role

**Classification:** both
**Explanation:** Uses 19th and 20th-century historical travelogues as evaluation data to test how well computational models can extract environment-related aspects and associated sentiments for literary-historical analysis.
**Relevant ASJC areas:** History, Literature and Literary Theory
**CSV Humanities?:** Yes
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | Specifically designed for literary-historical research on environmental aspects in historical travelogues. |
| Evaluates generative LLM | YES | Evaluates the open-source generative large language model Mixtral-8x7B-Instruct-v0.1. |
| LLM is primary evaluated system | NO | The LLM is evaluated alongside rule-based and supervised machine learning architectures (BERT, MacBERTh). |
| Arts & Humanities data/tasks | YES | History, Literature and Literary Theory |
| Quantitative performance metrics | YES | Strict macro F1-score and Fleiss' Kappa. |
| Published after Mar 2023 | YES | Published in May 2024 at LT4HALA 2024 @ LREC-COLING 2024. |
| English language | YES | The paper is written in English, and the pilot experiments are conducted on the English subset of the travelogues dataset. |

## Benchmark Modalities

**Modality Types:** text

**Description:** Text-only evaluation utilizing historical travelogues written in English, French, German, and Dutch.

## Analytical Tasks

**Task Types:** aspect extraction, sentiment classification

**Detailed Description:** Aspect extraction tasks evaluate the identification of specific domain-relevant entities (e.g., flora, fauna, biomes, weather) in historical texts. Sentiment classification tasks evaluate the categorization of evaluative sentiment directed toward these aspects on both 3-point and 5-point scales.

## Summary

This paper presents a pilot study exploring aspect-based sentiment analysis (ABSA) methodologies on 19th and 20th-century historical travelogues. It develops and evaluates three distinct toolchains—a rule-based system, a supervised machine learning classifier utilizing BERT and MacBERTh embeddings, and a prompt-based generative workflow using Mixtral 8x7B—to capture fine-grained environmental aspects and sentiments.

## Key Findings

For aspect extraction, the supervised Flair sequence tagger with BERT embeddings achieved the highest strict F1 (0.62), followed by MacBERTh (0.59), Mixtral 8x7B (0.34), and the rule-based system (0.20). For sentiment classification on a 3-point scale, the supervised MLP classifier with MacBERTh embeddings achieved the highest F1 (0.62), followed closely by BERT (0.61), while Mixtral 8x7B achieved 0.42 and the rule-based system achieved 0.37.
