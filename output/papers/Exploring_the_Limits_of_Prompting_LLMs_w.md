# PSH v1.0

**Paper name:** Exploring the Limits of Prompting LLMs with Speaker-Specific Rhetorical Fingerprints
**DOI:** None
**arXiv ID:** None
**Year:** 2025
**Article URL:** https://acl-bg.org/proceedings/2025/LM4DH%202025/pdf/2025.lm4dh-1.14.pdf
**Publication year (from analysis):** 2025

## Humanities Role

**Classification:** both
**Explanation:** Evaluates the linguistic, rhetorical, and stylistic mimicry capabilities of LLMs (humanities domain of Language and Linguistics) using a specially curated corpus of parole hearing transcripts compiled for digital humanities and linguistics analysis.
**Relevant ASJC areas:** Language and Linguistics
**CSV Humanities?:** Yes
**CSV ASJC code:** Language and Linguistics

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | It is a domain-specific evaluation dataset and study focusing on rhetorical and stylistic impersonation in legal hearings, rather than a general-purpose benchmark. |
| Evaluates generative LLM | YES | Evaluates GPT-4o, GPT-4.1, and DeepSeek R1. |
| LLM is primary evaluated system | YES | LLMs are the primary systems being tested on their stylistic generation limits. |
| Arts & Humanities data/tasks | YES | Mapped to Language and Linguistics (focusing on forensic linguistics, rhetoric, stylistics, and spoken discourse analysis). |
| Quantitative performance metrics | YES | Evaluates using standardized z-scores of linguistic features, Measure of Textual Lexical Diversity (MTLD), and syntactic/dependency-based complexity measurements. |
| Published after Mar 2023 | YES | Published in September 2025 (RANLP 2025 workshop). |
| English language | YES | The paper and the evaluated PSH v1.0 corpus are in English. |

## Benchmark Modalities

**Modality Types:** text

**Description:** Text-only evaluation using verbatim transcripts of parole suitability hearings.

## Analytical Tasks

**Task Types:** stylistic mimicry, rhetorical style replication, controlled text generation, linguistic profiling

**Detailed Description:** Evaluates the capacity of LLMs to replicate speaker-specific rhetorical fingerprints across multiple dimensions including sentence complexity, lexical diversity, discourse markers, nominalizations, modal verbs, and pronoun usage profiles.

## Summary

This paper evaluates the capacity of state-of-the-art LLMs to impersonate specific human speakers' rhetorical styles in a high-stakes legal context using PSH v1.0, a corpus of 100 anonymized parole hearing transcripts. By extracting multi-dimensional linguistic fingerprints of presiding commissioners, the authors test whether explicit rhetorical guidance in prompts improves stylistic alignment compared to corpus-based priming.

## Key Findings

All tested LLMs show clear limitations in replicating human rhetorical fingerprints, failing to align with individual human stylistic profiles. Regardless of prompting conditions, models revert to their own inherent, writing-biased stylistic footprints, demonstrating massive overuses of nominalizations, excessively complex sentences, and significantly higher lexical diversity than natural human speech.

## Reviewer Notes

- Resolved minor disagreement on humanities_role by assigning 'both', as the text constitutes a specially curated corpus for linguistic study (presented at a Digital Humanities workshop) and tests a core linguistics domain (rhetorical and stylistic replication). Merged analytical tasks from both reviewers for completeness.

## Additional Fields

**Dataset Size:** 100

**Primary Evaluation Setting:** zero-shot
