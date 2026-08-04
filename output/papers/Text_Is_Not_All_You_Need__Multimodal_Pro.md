# Text Is Not All You Need: Multimodal Prompting Helps LLMs Understand Humor

**Paper name:** Text Is Not All You Need: Multimodal Prompting Helps LLMs Understand Humor
**DOI:** None
**arXiv ID:** None
**Year:** 2025
**Article URL:** https://aclanthology.org/2025.chum-1.2.pdf
**Publication year (from analysis):** 2025

## Humanities Role

**Classification:** domain
**Explanation:** The evaluation targets specific linguistic and literary competencies, measuring the models' ability to analyze verbal humor, decode wordplay, and interpret semantic and phonetic ambiguities such as homographs and heterographs.
**Relevant ASJC areas:** Language and Linguistics, Literature and Literary Theory
**CSV Humanities?:** Yes
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | The study does not propose a general-purpose benchmark; it evaluates a specific multimodal prompting method on three specialized humor datasets. |
| Evaluates generative LLM | YES | Evaluates Gemini-1.5-Flash for humor explanation and uses GPT-4o as an LLM-as-a-judge. |
| Quantitative performance metrics | YES | Pairwise comparison win rates (assessed by LLM-as-a-judge against human explanations) and logit probability analysis. |
| Published after Mar 2023 | YES | Published in January 2025. |

## Benchmark Modalities

**Modality Types:** text, audio

**Description:** Combines textual jokes with synthetically generated spoken-word audio (via Text-to-Speech) to provide phonetic cues for a multimodal model.

## Analytical Tasks

**Task Types:** classification, generation, interpretation, stylistic analysis

**Detailed Description:** Tasks include pun detection (binary classification of text as pun or non-pun), humor explanation (generating free-text explanations of jokes), interpretation (hermeneutic decoding of semantic double meanings and homophones), and stylistic analysis (recognizing rhetorical structures and wordplay mechanisms).

## Summary

This paper investigates whether incorporating auditory cues via multimodal prompting helps Large Language Models overcome token-based limitations to better understand and explain verbal humor, specifically puns. By converting textual jokes into audio using a Text-to-Speech system and prompting a multimodal model with both modalities, the authors demonstrate improved performance in humor explanation across three datasets.

## Key Findings

Providing synthetic audio alongside text improves the model's humor explanation performance over a text-only baseline across all tested datasets. On the SemEval dataset, incorporating audio increased the model's explanation win rate against human baselines by approximately 4% for both homographic and heterographic puns. Analysis of the model's logits confirmed that auditory inputs successfully preserved phonetic ambiguities.

## Reviewer Notes

- Resolved disagreement on primary_evaluation_setting in favor of Cip ('few-shot'), as the text explicitly notes 'each prompt included six examples' under prompt configuration. For analytical_tasks, replaced Ciop's 'open_ended_qa' with Cip's 'generation', as the primary task evaluated by the LLM-as-a-judge is the quality of the generated free-text humor explanations.
- Disagreement on gold_source: Ciop inferred 'authored_answer_key' based on the reference datasets, but Cip correctly noted that the paper text itself does not detail the annotation protocols for the SemEval or Context-Situated Puns datasets (which constitute the majority of the benchmark). Following the rule to adjudicate strictly against the paper's own text and prefer 'not_stated' over plausible reconstructions, the value was resolved to 'not_stated'.

## Additional Fields

**Dataset Size:** 5444

**Primary Evaluation Setting:** few-shot

**Gold Source:** not_stated

**Gold Beyond Stimulus:** yes

**Gold Community Dependent:** no

**Gold Concerns Genesis:** no

**Answer Multiplicity:** graded_human_judgment

**Plurality Treatment:** not_addressed

**Facets Explanation:** The paper evaluates humor explanation on the SemEval 2017 Task 7, Context-Situated Puns, and ExplainTheJoke datasets. While the paper notes that these datasets provide pre-existing human annotations and explanations (with ExplainTheJoke explicitly scraped from a website), it does not describe the specific annotation processes or annotator backgrounds for the majority of the data, resulting in a 'not_stated' gold source. Evaluation is performed by GPT-4o acting as an LLM judge to perform pairwise comparisons between generated and reference explanations ('graded_human_judgment'). Recognizing and explaining puns requires external linguistic knowledge (e.g., of homophones) beyond the stimulus text itself.
