# CLEF 2025 JOKER Task 2

**Paper name:** JOKER 2025 Task 2: Translation of puns from English to French
**DOI:** None
**arXiv ID:** None
**Year:** 2025
**Article URL:** https://ceur-ws.org/Vol-4038/paper_219.pdf
**Publication year (from analysis):** 2025

## Humanities Role

**Classification:** domain
**Explanation:** The benchmark targets disciplinary competence in translation studies and computational linguistics, specifically evaluating the preservation of semantic and phonetic double meanings (wordplay and puns) during English-to-French translation.
**Relevant ASJC areas:** Language and Linguistics
**CSV Humanities?:** Yes
**CSV ASJC code:** Language and Linguistics

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | Specifically scoped to the task of pun/wordplay translation rather than general linguistic capabilities. |
| Evaluates generative LLM | YES | Evaluates a variety of generative systems, including Qwen2.5-14B, GPT-4o-mini, Mistral, mBART-50, and MarianMT. |
| Quantitative performance metrics | YES | Evaluated using BLEU, BERTScore, a novel pun-location-based metric, and expert manual human evaluation. |
| Published after Mar 2023 | YES | Published in September 2025 as part of the CLEF 2025 Working Notes. |

## Benchmark Modalities

**Modality Types:** text

**Description:** Text-only machine translation task where English punning jokes are translated into French.

## Analytical Tasks

**Task Types:** translation, generation

**Detailed Description:** The benchmark evaluates the translation of wordplay and puns from English into French, requiring generative text modeling that successfully preserves the dual meanings, phonetic structures, and humor of the original text.

## Summary

This paper presents the overview and results of Task 2 of the CLEF 2025 JOKER track, which evaluates the translation of English puns into French. It introduces a test dataset of 1,682 distinct English puns with manually annotated pun locations to facilitate fine-grained evaluation. The paper details the diverse participant approaches, ranging from fine-tuned machine translation systems to complex multi-agent LLM prompting pipelines.

## Key Findings

Multi-agent pipelines incorporating LLMs, contrastive learning, and phonetic-semantic embeddings achieved the highest manual success rates, correctly translating up to 74% of the evaluated puns. Traditional metrics like BLEU and BERTScore proved insufficient for measuring wordplay preservation; however, a newly introduced pun location-based automatic metric demonstrated a strong Pearson correlation (0.84) with expert human evaluation.

## Reviewer Notes

- Ciop included 'interpretation' and 'stylistic_analysis' under analytical_tasks, reasoning that understanding and preserving humor requires these competencies. While true conceptually, the benchmark formally evaluates the output via 'translation' and 'generation' tasks. I adopted Cip's more stringent reading to reflect the concrete evaluation setup. Both analysts agreed on all other substantive fields, which were blended for clarity.
- plurality_treatment: Ciop selected 'not_addressed', while Cip selected 'signal'. Resolved to 'not_addressed' because, while the dataset preserves multiple valid translations, the paper does not explicitly discuss treating this divergence as a theoretical signal about the material itself; it simply accommodates the standard need for multiple references in translation tasks. All other fields were agreed upon.

## Additional Fields

**Dataset Size:** 1682

**Primary Evaluation Setting:** mix

**Gold Source:** domain_expert

**Gold Beyond Stimulus:** yes

**Gold Community Dependent:** no

**Gold Concerns Genesis:** no

**Answer Multiplicity:** answer_set

**Plurality Treatment:** not_stated

**Facets Explanation:** Reference translations and pun location annotations were produced by professional translators, who serve as domain experts. A significant portion of the English puns is provided with multiple valid French translations, yielding an answer set that captures different creative strategies for rendering the wordplay. The paper does not explicitly analyze annotator disagreement or divergence as signal or noise, instead treating the multiple references as standard variations to allow robust machine translation evaluation. Successfully translating these puns requires deep linguistic, phonetic, and semantic knowledge of both languages that is not present in the source stimulus.

**Reported Format Gap:** no

**Reported Format Gap Points:** None

**Human Baseline Reported:** no

**Human Gap Points:** None

**Reported Best Score:** 43.33

**Reported Best Metric:** bleu

**Reported Cultural Asymmetry:** not_stated

**Results Explanation:** The highest score on the primary metric of BLEU is 43.33, achieved by the 'Skommarkhos_Lucie_SFT' run on the test data (Table 4). No standard human baseline score is reported for comparison on this task, though a manual evaluation by a native French speaker shows the best run achieved a 74% success rate (37 of 50 puns) in preserving both meaning and wordplay (Table 7). The paper does not evaluate alternative answer formats or report a format gap for the same models, and cross-cultural asymmetry is 'not_stated' as the task is restricted to English-to-French translation.
