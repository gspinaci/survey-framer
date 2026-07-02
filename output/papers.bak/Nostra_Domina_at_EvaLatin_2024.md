# Nostra Domina at EvaLatin 2024

**Paper name:** Nostra Domina at EvaLatin 2024
**DOI:** None
**arXiv ID:** None
**Year:** 2024
**Article URL:** https://aclanthology.org/2024.lt4hala-1.25.pdf
**Publication year (from analysis):** 2024

## Humanities Role

**Classification:** both
**Explanation:** Evaluates sentiment and emotion polarity detection on classical Latin poetry and literature including Horace, Seneca, and Pontano.
**Relevant ASJC areas:** Classics, Language and Linguistics, Literature and Literary Theory
**CSV Humanities?:** Yes
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | The paper does not introduce a benchmark, but rather proposes data augmentation techniques to participate in the domain-specific EvaLatin 2024 shared task. |
| Evaluates generative LLM | YES | Evaluates several encoder-based language models for Latin, specifically Latin BERT, LaBERTa, PhilBERTa, mBERT, CANINE-C, CANINE-S, and SPhilBERTa. |
| LLM is primary evaluated system | YES | The primary systems being benchmarked and compared are Latin language models integrated with different neural encoders. |
| Arts & Humanities data/tasks | YES | Classics, Language and Linguistics, Literature and Literary Theory. The evaluation uses classical Latin poetry and plays (Horace, Pontano, Seneca). |
| Quantitative performance metrics | YES | Evaluated using Macro-F1 and Micro-F1 scores. |
| Published after Mar 2023 | YES | Published on May 25, 2024. |
| English language | YES | The paper is written in English, while the evaluation dataset is in Latin. |

## Benchmark Modalities

**Modality Types:** text

**Description:** Models are evaluated on classical and historical Latin text corpora.

## Analytical Tasks

**Task Types:** emotion polarity detection, sentiment analysis

**Detailed Description:** Identifying emotional polarity (positive, negative, neutral, or mixed) of sentences in classical Latin poetry and dramatic literature.

## Summary

This paper describes the Nostra Domina team's submissions to the EvaLatin 2024 shared task of emotion polarity detection. To address the scarcity of annotated training data in Latin, the authors propose two clustering-based automatic data augmentation methods (Polarity Coordinate clustering and Gaussian clustering) and evaluate several pretrained Latin language models. Their best-performing system utilizes PhilBERTa embeddings combined with a Transformer encoder trained on Gaussian-clustered data.

## Key Findings

The models trained on the Gaussian clustering augmented dataset significantly outperformed those trained on Polarity Coordinate (PC) clustering, with the PhilBERTa + Transformer model achieving an Odes Macro-F1 of 0.41. In the official EvaLatin 2024 shared task, this system achieved the highest Macro-F1 score on the Pontano subset (0.42) and placed second overall with a macro-averaged Macro-F1 of 0.28.
