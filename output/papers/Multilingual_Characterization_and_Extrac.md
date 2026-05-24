# SemEval-2025 Task 10: Multilingual Characterization and Extraction of Narratives from Online News

**Paper name:** Multilingual Characterization and Extraction of Narratives from Online New
**DOI:** None
**arXiv ID:** None
**Year:** 2025
**Article URL:** https://aclanthology.org/2025.semeval-1.331.pdf
**Publication year (from analysis):** 2025

## Humanities Role

**Classification:** both
**Explanation:** Utilizes online news articles as content to evaluate models using narrative theory, rhetorical analysis, and literary character archetypes (protagonists, antagonists, innocents) as the core analytical framework.
**Relevant ASJC areas:** Literature and Literary Theory, Language and Linguistics
**CSV Humanities?:** Borderline
**CSV ASJC code:** Literature and Literary Theory

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | The benchmark is domain-specific, focusing on narrative extraction, media analysis, and propaganda detection in news articles regarding Climate Change and the Ukraine-Russia War. |
| Evaluates generative LLM | YES | Evaluates multiple generative LLMs, including GPT-4o, Llama 3/3.1, Phi-3/4, Qwen 2.5, Gemma 2, DeepSeek-R1, Mistral, and Flan-T5 across participant submissions. |
| LLM is primary evaluated system | YES | Large Language Models are the primary technologies evaluated, fine-tuned, and benchmarked by the participating teams. |
| Arts & Humanities data/tasks | YES | Includes 'Literature and Literary Theory' due to its structural use of narrative theory, framing, and literary character archetypes, as well as 'Language and Linguistics' for multilingual processing. |
| Quantitative performance metrics | YES | Uses Exact Match Ratio (EMR) for Subtask 1, sample-averaged and macro-averaged F1 for Subtask 2, and BertScore F1 for Subtask 3. |
| Published after Mar 2023 | YES | Published in July-August 2025 as part of the SemEval-2025 proceedings. |
| English language | YES | The paper is written in English, and English is one of the five core languages featured in the benchmark dataset. |

## Benchmark Modalities

**Modality Types:** text

**Description:** The benchmark is entirely text-based, consisting of multilingual news articles, entity lists, taxonomic labels, and natural language explanations in Bulgarian, English, Hindi, Portuguese, and Russian.

## Analytical Tasks

**Task Types:** Entity Framing, Hierarchical Document Classification, Explanatory Text Generation

**Detailed Description:** Evaluates the attribution of highly nuanced, character-archetypal roles (e.g., martyr, tyrant, saboteur) to entities (Subtask 1), hierarchical multi-label classification into domain-specific narrative taxonomies (Subtask 2), and free-text generation of justifications explaining dominant narrative choices (Subtask 3).

## Summary

This paper presents SemEval-2025 Task 10, introducing a multilingual and multi-faceted benchmark designed to characterize and extract narratives from online news. The task evaluates systems across three layers: entity framing (assigning role archetypes to named entities), hierarchical narrative classification, and generating natural language justifications for dominant narratives in Climate Change and Ukraine-Russia War coverage.

## Key Findings

Participating systems leveraged generative LLMs (e.g., GLM-4, Qwen 2.5, Phi-4) optimized via prompting techniques (CoT, hierarchical prompting) or DPO tuning. For Subtask 1, the top system achieved an average Exact Match Ratio of 0.475; for Subtask 2, the top system scored an average Sample F1 of 0.435; and for Subtask 3, the best average BertScore F1 reached 0.727.
