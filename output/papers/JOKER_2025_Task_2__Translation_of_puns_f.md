# CLEF 2025 JOKER Task 2

**Paper name:** JOKER 2025 Task 2: Translation of puns from English to French
**DOI:** None
**arXiv ID:** None
**Year:** 2025
**Article URL:** https://ceur-ws.org/Vol-4038/paper_219.pdf
**Publication year (from analysis):** 2025

## Humanities Role

**Classification:** domain
**Explanation:** Evaluates computational models on the translation of puns and wordplay, treating humour as a sophisticated linguistic and literary artifact requiring semantic and cultural-stylistic transfer.
**Relevant ASJC areas:** Language and Linguistics, Literature and Literary Theory
**CSV Humanities?:** Yes
**CSV ASJC code:** Language and Linguistics

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | It is a specialized domain-specific benchmark focused exclusively on bilingual pun and wordplay translation. |
| Evaluates generative LLM | YES | Evaluates several generative models, including Qwen2.5, GPT-4o-mini, Mistral, mBART, and NLLB. |
| LLM is primary evaluated system | YES | The primary systems being benchmarked are generative LLMs and fine-tuned neural translation models. |
| Arts & Humanities data/tasks | YES | Covers Language and Linguistics (translation, wordplay) as well as Literature and Literary Theory. |
| Quantitative performance metrics | YES | Uses BLEU, BERTScore, a novel pun location-based overlap metric, and manual expert evaluation scores. |
| Published after Mar 2023 | YES | Published in 2025 as part of the CLEF 2025 conference. |
| English language | YES | The paper and the source benchmark data are in English. |

## Benchmark Modalities

**Modality Types:** text

**Description:** A text-only machine translation task converting English punning jokes into French translations.

## Analytical Tasks

**Task Types:** wordplay translation, humour preservation, semantic meaning preservation

**Detailed Description:** Translating English puns into French while preserving both the literal/semantic meanings and the humorous dual-meaning wordplay of the source text.

## Summary

This paper presents the overview of Task 2 of the CLEF 2025 JOKER track, which evaluates automated translation of puns from English to French. It assesses 52 system runs submitted by nine teams, comparing standard machine translation metrics against a novel 'pun location-based' metric and native-speaker expert judgments.

## Key Findings

Standard translation metrics like BLEU and BERTScore correlated poorly with actual humor preservation, while the proposed 'pun location-based' metric showed a high Pearson correlation (0.84) with human expert judgments. The best-performing systems, which utilized multi-agent architectures and phonetic/semantic embeddings (e.g., based on GPT-4o-mini), achieved a manually validated translation success rate of up to 74%.

## Reviewer Notes

- 1) benchmark_name: Ciop omitted 'CLEF'; resolved to Cip's 'CLEF 2025 JOKER Task 2' for completeness. 2) humanities_role: Ciop chose 'both', Cip chose 'domain'; resolved to 'domain' because the benchmark is primarily a specialized linguistic evaluation design for wordplay translation. 3) analytical_tasks: Ciop included 'phonetic-semantic embedding alignment', which was a participant method rather than a benchmark task; adopted Cip's task list. 4) dataset_size: Ciop reported 1682 (the test set size), while Cip reported 3087 (train 1405 + test 1682); resolved to 3087 to represent the full corpus of distinct source puns provided for the benchmark.

## Additional Fields

**Dataset Size:** 3087

**Primary Evaluation Setting:** mix
