# Parole Suitability Hearing Corpus (PSH v1.0)

**Paper name:** Exploring the Limits of Prompting LLMs with Speaker-Specific Rhetorical Fingerprints
**DOI:** None
**arXiv ID:** None
**Year:** 2025
**Article URL:** https://acl-bg.org/proceedings/2025/LM4DH%202025/pdf/2025.lm4dh-1.14.pdf
**Publication year (from analysis):** 2025

## Humanities Role

**Classification:** domain
**Explanation:** The benchmark evaluates LLMs on disciplinary-level competence in computational stylistics and forensic linguistics, analyzing whether they can replicate fine-grained rhetorical profiles and stylistic human signatures.
**Relevant ASJC areas:** Language and Linguistics
**CSV Humanities?:** Yes
**CSV ASJC code:** Language and Linguistics

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | Scoped strictly to speaker-specific rhetorical impersonation and style mimicry within legal transcripts (parole suitability hearings). |
| Evaluates generative LLM | YES | Evaluates GPT-4o, GPT-4.1, and DeepSeek R1. |
| Quantitative performance metrics | YES | Uses z-scores over normalized linguistic feature counts (sentence complexity, lexical diversity, and frequency-based features) compared against original human baselines. |
| Published after Mar 2023 | YES | Published in September 2025. |

## Benchmark Modalities

**Modality Types:** text

**Description:** Text-only corpus consisting of verbatim hearing transcript dialogues and generated spoken decision statements.

## Analytical Tasks

**Task Types:** generation, stylistic analysis

**Detailed Description:** Generation of spoken legal decision statements and systematic stylistic profiling based on eight linguistic dimensions: sentence complexity, lexical diversity, discourse markers, nominalizations, modals, pronoun usage, and legal jargon.

## Summary

The paper explores the capacity of LLMs to mimic human conversational monologue in a high-stakes legal setting by prompting them with speaker-specific rhetorical fingerprints. Using the PSH v1.0 corpus of parole hearings, the authors extract stylistic signatures of human commissioners to guide generative LLMs, finding that LLMs possess strong, immutable model-specific fingerprints that dominate over the prompted styles.

## Key Findings

All tested LLMs show a strong resistance to adapting to human spoken norms: they exhibit massive inflation in lexical diversity and syntactic complexity, alongside an immutable bias toward formal written syntax and nominalizations. GPT and DeepSeek models reveal strong, persistent model-specific linguistic fingerprints that limit their capacity for stylistic alignment and persona adoption.

## Reviewer Notes

- No significant disagreements. Cip's more complete benchmark name was chosen. Analyst summaries and key findings were merged for clarity.

## Additional Fields

**Dataset Size:** 100

**Primary Evaluation Setting:** zero-shot

**Gold Source:** existing_metadata

**Gold Beyond Stimulus:** yes

**Gold Community Dependent:** no

**Gold Concerns Genesis:** no

**Answer Multiplicity:** single_answer

**Plurality Treatment:** not_stated

**Facets Explanation:** The reference corpus (PSH v1.0) consists of 100 official parole suitability hearing transcripts obtained from the California Department of Corrections and Rehabilitation. The single ground truth for each case is the unique decision statement given by the presiding commissioner, which serves as a pre-existing administrative record. Generating the correct decision and rationale requires external knowledge of California state laws and parole guidelines not explicitly present in the provided interview transcript stimulus. As there is only one reference text per case, plurality and annotator consensus are not addressed.

**Reported Format Gap:** no

**Reported Format Gap Points:** None

**Human Baseline Reported:** yes

**Human Gap Points:** None

**Reported Best Score:** None

**Reported Best Metric:** None

**Reported Cultural Asymmetry:** not_stated

**Results Explanation:** The paper compares the linguistic features of LLM generations with actual human presiding commissioners' statements using z-scores, reporting human baselines for individual features under the 'Original' column in Table 1. For example, the 'Lexical Diversity' for original Commissioner 4 is '1.48' and 'Sentence Complexity' is '1.10', whereas the evaluated LLMs deviate significantly, with DeepSeek reaching a z-score of '34.91' on 'Sentence Complexity' when prompted with Commissioner 4's rhetorical 'fingerprint'. Because the findings are presented as standardized z-scores across multiple rhetorical dimensions rather than a single headline performance metric on a standardized scale, the best score, best metric, and human gap fields are null.
