# Tracking the evolution of LLM capabilities for Belarusian with OpenAI Evals

**Paper name:** Tracking the evolution of LLM capabilities for Belarusian with OpenAI Evals
**DOI:** None
**arXiv ID:** None
**Year:** 2026
**Article URL:** https://aclanthology.org/2026.loreslm-1.33.pdf
**Publication year (from analysis):** 2026

## Humanities Role

**Classification:** domain
**Explanation:** Designed specifically to evaluate linguistic and orthographic competencies of Belarusian, including classical orthography (Taraškievica), morphology, phonology, and grammar.
**Relevant ASJC areas:** Language and Linguistics
**CSV Humanities?:** Borderline
**CSV ASJC code:** Language and Linguistics

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | Specifically targets linguistic capabilities for a single low-resource language (Belarusian) rather than general-purpose multi-task evaluation. |
| Evaluates generative LLM | YES | Evaluated multiple generative LLMs including OpenAI's o4-mini, GPT-4.1, GPT-4o, GPT-3.5 Turbo, Claude 3.7 Sonnet, Gemini 2.5 Flash, Gemma 3, gpt-oss-120b, and Qwen3. |
| LLM is primary evaluated system | YES | The LLMs are the primary systems under evaluation to track their raw capabilities and progression over time. |
| Arts & Humanities data/tasks | YES | Focuses on Language and Linguistics, evaluating morpho-syntactic, phonological, lexical, and orthographic properties of Belarusian. |
| Quantitative performance metrics | YES | Uses accuracy as the primary evaluation metric and BLEU for translation evaluation. |
| Published after Mar 2023 | YES | Published in March 2026. |
| English language | YES | The paper is written in English. |

## Benchmark Modalities

**Modality Types:** text

**Description:** Evaluates models using text-based prompts and responses in Belarusian (and cross-lingual translation tasks with Russian and English).

## Analytical Tasks

**Task Types:** syllable counting, numeral to digit conversion, lexical acceptability judgment, orthographic conversion, rhyme translation and identification, morphological analogy completion, grammatical acceptability judgment, round-trip translation fidelity

**Detailed Description:** Evaluates phonological awareness (syllable counting, rhyming), orthographic variation (converting between modern standard and classical Taraškievica spelling), morphological generalization (solving inflectional analogies), and syntactic/lexical precision (acceptability judgements and translation stability).

## Summary

This paper evaluates the longitudinal progress of state-of-the-art LLMs on eight Belarusian language tasks originally contributed to OpenAI's Evals framework in 2023. To prevent evaluation issues stemming from data contamination, the authors introduce and validate new, non-overlapping test sets and provide a detailed linguistic error analysis.

## Key Findings

While models have progressed significantly in grammatical and numerical reasoning, improvements are uneven. LLMs still struggle with orthographic conversion (especially modern to classical Taraškievica), lexical discrimination (frequently misidentifying non-words as real vocabulary), and complex inflectional analogies, often exhibiting negative transfer from higher-resource Russian.
