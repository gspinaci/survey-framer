# PSH v1.0

**Paper name:** Exploring the Limits of Prompting LLMs with Speaker-Specific Rhetorical Fingerprints
**DOI:** None
**arXiv ID:** None
**Year:** 2025
**Article URL:** https://acl-bg.org/proceedings/2025/LM4DH%202025/pdf/2025.lm4dh-1.14.pdf
**Publication year (from analysis):** 2025

## Humanities Role

**Classification:** both
**Explanation:** Uses transcript data from parole hearings (content) to evaluate stylistic and rhetorical mimicry, which is a core task in computational linguistics and digital humanities (domain).
**Relevant ASJC areas:** Language and Linguistics
**CSV Humanities?:** Yes
**CSV ASJC code:** Language and Linguistics

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | The dataset is a highly specialized domain-specific conversational corpus from Californian parole hearings. |
| Evaluates generative LLM | YES | Evaluates GPT-4o, GPT-4.1, and DeepSeek R1. |
| LLM is primary evaluated system | YES | The LLMs are the primary systems being benchmarked on their text-generation and stylistic impersonation capabilities. |
| Arts & Humanities data/tasks | YES | Language and Linguistics (linguistic and stylistic analysis of speech styles). |
| Quantitative performance metrics | YES | Evaluates using z-scores of normalized relative frequencies of stylistic features, MTLD for lexical diversity, and dependency-parsed clausal counts for sentence complexity. |
| Published after Mar 2023 | YES | Published in September 2025. |
| English language | YES | The paper and the corpus transcripts are in English. |

## Benchmark Modalities

**Modality Types:** text

**Description:** Text-only analysis using verbatim transcripts of parole suitability hearings and LLM-generated decision statements.

## Analytical Tasks

**Task Types:** stylistic replication, rhetorical analysis, linguistic feature control

**Detailed Description:** Evaluates the capacity of LLMs to match human speakers across several rhetorical dimensions, including syntactic complexity, lexical diversity, discourse markers, nominalizations, modal verbs, pronoun usage, and domain-specific jargon.

## Summary

This paper investigates whether state-of-the-art LLMs can be prompted to impersonate human speakers in a high-stakes legal setting (generating parole suitability decision statements). By distilling a 'rhetorical fingerprint' from transcripts of specific presiding commissioners and using it to enhance prompts, the authors test the limits of LLMs' stylistic adaptability.

## Key Findings

LLMs fail to fully replicate the linguistic profiles of specific human speakers because their own model-specific stylistic fingerprints remain dominant. Across all prompting conditions, LLMs demonstrated excessively high lexical diversity and sentence complexity (z-scores up to 40) compared to human speech, reflecting a strong training bias towards written, formal language that could not be mitigated by prompting.
