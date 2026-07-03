# Text Is Not All You Need: Multimodal Prompting Helps LLMs Understand Humor

**Paper name:** Text Is Not All You Need: Multimodal Prompting Helps LLMs Understand Humor
**DOI:** None
**arXiv ID:** None
**Year:** 2025
**Article URL:** https://aclanthology.org/2025.chum-1.2.pdf
**Publication year (from analysis):** 2025

## Humanities Role

**Classification:** both
**Explanation:** Uses puns and jokes as core material (content) and evaluates the linguistic and rhetorical mechanics of verbal humor, wordplay, and phonetic ambiguity (domain).
**Relevant ASJC areas:** Language and Linguistics, Literature and Literary Theory
**CSV Humanities?:** Yes
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | The paper does not introduce a new general-purpose benchmark; it evaluates a multimodal prompting methodology on existing humor datasets. |
| Evaluates generative LLM | YES | Evaluates Gemini-1.5-Flash (generation), GPT-4o (evaluator/judge), and Gazelle v0.2 (for transcription logit analysis). |
| LLM is primary evaluated system | YES | The primary system being evaluated is the generative LLM (Gemini-1.5-Flash) for its capacity to interpret humor. |
| Arts & Humanities data/tasks | YES | Focuses on Language and Linguistics, as well as Literature and Literary Theory (wordplay, punning, and humor theory). |
| Quantitative performance metrics | YES | Uses pairwise win rates, tie rates, and token probabilities (logits) to evaluate performance. |
| Published after Mar 2023 | YES | Published in January 2025. |
| English language | YES | The paper and evaluated datasets (SemEval 2017, Context-Situated Puns, ExplainTheJoke) are in English. |

## Benchmark Modalities

**Modality Types:** text, audio

**Description:** Multimodal prompting that pairs the text of a joke or pun with its synthesized audio counterpart generated via text-to-speech (TTS) to capture phonetic nuances.

## Analytical Tasks

**Task Types:** humor detection, humor explanation, phonetic transcription evaluation

**Detailed Description:** Factual and reasoning-based tasks identifying puns (humor detection), generating natural language explanations of linguistic and phonetic mechanics (humor explanation), and evaluating internal logit representations for homophones (phonetic transcription evaluation).

## Summary

This paper investigates whether incorporating an auditory modality helps LLMs better grasp the phonetic ambiguity inherent in verbal humor, such as puns. By presenting models with combined text and TTS-generated audio, the study demonstrates that multimodal cues significantly improve the accuracy and quality of generated humor explanations compared to text-only prompts.

## Key Findings

Adding audio cues to prompts improved Gemini-1.5-Flash's humor explanation quality across all tested datasets. For the SemEval 2017 dataset, it yielded a win-rate increase over the baseline text-only prompts of approximately 4% for both homographic and heterographic puns. Direct logit analysis of phonetic transcription tasks confirmed that models maintain high probabilities for homophones (e.g., 'weight' vs 'wait') when exposed to audio.

## Reviewer Notes

- Ciop and Cip disagreed slightly on humanities_role (Ciop said 'both', Cip said 'domain'); resolved to 'both' because the methodology evaluates specific linguistic features (domain) using datasets of jokes and puns (content). Cip included 'phonetic transcription evaluation' under analytical_tasks, which was retained as it accurately reflects the logit analysis explicitly evaluated in the paper. Cip's inclusion of 'Visual Arts and Performing Arts' as an ASJC area was excluded to maintain a strict focus on the paper's primary disciplines of 'Language and Linguistics' and 'Literature and Literary Theory'.

## Additional Fields

**Dataset Size:** None

**Primary Evaluation Setting:** few-shot
