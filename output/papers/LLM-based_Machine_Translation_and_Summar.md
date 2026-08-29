# LLM-based Machine Translation and Summarization for Latin

**Paper name:** LLM-based Machine Translation and Summarization for Latin
**DOI:** None
**arXiv ID:** None
**Year:** 2024
**Article URL:** https://aclanthology.org/2024.lt4hala-1.15.pdf
**Publication year (from analysis):** 2024

## Humanities Role

**Classification:** domain
**Explanation:** Tests philological competence by evaluating machine translation and summarization of 16th-century historical languages (Latin and Early New High German), requiring domain-specific vocabulary and historical place-name resolution.
**Relevant ASJC areas:** Classics, History, Language and Linguistics
**CSV Humanities?:** Yes
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | Scoped specifically to historical translation and summarization of a corpus of 16th-century letters. |
| Evaluates generative LLM | YES | Evaluates GPT-4 against neural machine translation baselines. |
| Quantitative performance metrics | YES | Uses BLEU and ChrF for translation and summarization, alongside structured human evaluation for historical correctness. |
| Published after Mar 2023 | YES | Published in May 2024 at the LT4HALA workshop. |

## Benchmark Modalities

**Modality Types:** text

**Description:** Text-only evaluation based on transcriptions of historical letters.

## Analytical Tasks

**Task Types:** translation, generation

**Detailed Description:** Machine translation of historical Latin and Early New High German into modern languages, as well as paragraph-level summarization (generation) compared against expert historical commentaries.

## Summary

This paper evaluates the performance of LLMs (specifically GPT-4) on machine translation and summarization of 16th-century letters written in Latin and Early New High German. It demonstrates that generative models significantly outperform traditional neural machine translation baselines on these historical languages and produce summaries comparable to expert-written historical commentaries.

## Key Findings

GPT-4 outperforms Google Translate by roughly 10 BLEU points for Latin-to-German (27.07 vs 17.53) and Latin-to-English (34.50 vs 25.22) translation. In manual evaluation of generated summaries, GPT-4 captured historical names, dates, and events with high accuracy and without hallucinations, despite relatively low automatic BLEU scores due to stylistic variances.

## Reviewer Notes

- Disagreement on humanities_role (Ciop: domain, Cip: content). Resolved in favor of 'domain', weighting Ciop's disciplinary judgment, because translating 16th-century historical texts and resolving historical place names (e.g., Argentina to Strasbourg) targets specific philological competence rather than merely generic MT capabilities.
- Ciop and Cip disagreed on reported_cultural_asymmetry. Ciop marked 'yes' citing the performance gap between English and German target translations, while Cip marked 'no'. I resolved to 'yes', as the paper explicitly attributes the BLEU score discrepancy to differing levels of language resources, fitting the definition of a systemic linguistic asymmetry.

## Additional Fields

**Dataset Size:** None

**Primary Evaluation Setting:** zero-shot

**Gold Source:** domain_expert

**Gold Beyond Stimulus:** no

**Gold Community Dependent:** no

**Gold Concerns Genesis:** no

**Answer Multiplicity:** single_answer

**Plurality Treatment:** not_stated

**Facets Explanation:** The reference translations for the primary 8-letter machine translation test set were manually produced by a domain expert. The reference summaries for the paragraph-level evaluation were taken from a professional, expert-edited historical edition of Heinrich Bullinger's correspondence (acting as a secondary, pre-existing source of expert reference). Answering correctly does not require knowledge outside the text, as the tasks are translation and summarization of the provided letters. Evaluation relies on automated metrics (BLEU and ChrF) comparing the generated texts to these single reference targets. The paper does not address annotator disagreement or alternative readings during the creation of the reference texts.

**Reported Format Gap:** no

**Reported Format Gap Points:** None

**Human Baseline Reported:** no

**Human Gap Points:** None

**Reported Best Score:** 34.5

**Reported Best Metric:** bleu

**Reported Cultural Asymmetry:** yes

**Results Explanation:** The paper reports that GPT-4 achieved the highest score with a BLEU score of 34.50 for translating Latin to English (Table 1). No format gaps or difficulty regimes were compared on the same data. Human translations and summaries were used as reference gold standards and humans judged the model outputs, but no quantified human baseline was evaluated on the same metrics. The paper notes a systemic linguistic asymmetry, explaining that the higher translation performance into English compared to German (27.07 BLEU) occurs because 'English is by far the highest resource language on the internet'.
