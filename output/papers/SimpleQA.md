# SimpleQA

**Paper name:** SimpleQA
**DOI:** None
**arXiv ID:** None
**Year:** 2024
**Article URL:** https://openai.com/index/introducing-simpleqa/
**Publication year (from analysis):** 2024

## Humanities Role

**Classification:** content
**Explanation:** The benchmark uses factual questions (including humanities topics) to evaluate generic short-form factual recall and hallucination rates, rather than testing specialized disciplinary methodologies or interpretation.
**Relevant ASJC areas:** Multidisciplinary
**CSV Humanities?:** Yes
**CSV ASJC code:** Multidisciplinary

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | It is a specialized benchmark focusing strictly on short-form factuality and hallucination rather than a broad, multi-task general evaluation. |
| Evaluates generative LLM | YES | Evaluates frontier generative models including OpenAI's GPT-4, o1, and o3 series, Anthropic's Claude 3.5, Google's Gemini, and Meta's Llama 3.1. |
| Quantitative performance metrics | YES | Evaluates models using quantitative metrics including accuracy and hallucination rates. |
| Published after Mar 2023 | YES | Published in late 2024, alongside evaluation scripts updated through 2025. |

## Benchmark Modalities

**Modality Types:** text

**Description:** Evaluates models in a text-only modality by presenting short-form questions and evaluating the textual answers.

## Analytical Tasks

**Task Types:** factual recall, open ended qa, calibration and uncertainty

**Detailed Description:** Evaluates short-form factual open-ended question answering where the model must retrieve specific declarative knowledge. It tests calibration by measuring factuality versus hallucination rates and the model's ability to decline answering when uncertain.

## Summary

SimpleQA is a specialized benchmark designed to measure the short-form factuality of language models. It tests the ability of models to accurately recall specific factual information and correctly calibrate their responses by acknowledging a lack of knowledge to avoid hallucinations.

## Key Findings

State-of-the-art frontier models historically struggle with highly specific factual questions and exhibit notable hallucination rates. However, newer reasoning-optimized models (such as OpenAI's o-series) demonstrate improved accuracy and calibration.

## Reviewer Notes

- Agreed on most fields. Dropped 'generation' from Cip's analytical_tasks, as short-form QA is better captured by 'open_ended_qa' and does not fit the standard generation of free text. Restricted relevant_asjc_areas to 'Multidisciplinary' as strictly stated in the CSV metadata, dropping analyst-inferred disciplines not found in the text. Changed dataset_size to null since the exact item count (4326/4301) is not present in the provided text. Set primary_evaluation_setting to 'mix' because the text explicitly states the repository uses 'zero-shot, chain-of-thought', which triggers the 'mix' adjudication rule.
- Ciop inferred dataset construction details (gold_source as 'crowd_annotation', plurality_treatment as 'noise', answer_multiplicity as 'single_answer', gold_community_dependent and gold_concerns_genesis as 'no') likely from external knowledge of the official OpenAI SimpleQA paper. However, these details are completely absent from the provided GitHub README text. Following the adjudication rules to prefer 'not_stated' over unsupported inference, I resolved all such fields to 'not_stated' / 'not_addressed' in alignment with Cip's reading. Both analysts correctly agreed on gold_beyond_stimulus as 'yes' due to the zero-shot factual QA nature of the benchmark.

## Additional Fields

**Dataset Size:** None

**Primary Evaluation Setting:** mix

**Gold Source:** not_stated

**Gold Beyond Stimulus:** yes

**Gold Community Dependent:** not_stated

**Gold Concerns Genesis:** not_stated

**Answer Multiplicity:** not_stated

**Plurality Treatment:** not_addressed

**Facets Explanation:** The provided text is a GitHub repository README that introduces SimpleQA as an evaluation for 'short-form factuality' but does not contain details about its construction. Because it tests factuality in a zero-shot setting without providing retrieved context passages, answering correctly requires knowledge beyond the prompt stimulus. All other dataset construction and scoring details (such as the gold source, answer multiplicity, and treatment of annotator plurality) are omitted from this document.
