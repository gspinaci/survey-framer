# History Seshat Test for LLMs (HiST-LLM)

**Paper name:** HiST-LLM
**DOI:** None
**arXiv ID:** None
**Year:** 2024
**Article URL:** https://neurips.cc/virtual/2024/poster/97439
**Publication year (from analysis):** 2024

## Humanities Role

**Classification:** domain
**Explanation:** Designed to evaluate graduate-level and expert-level historical knowledge and comprehension, explicitly targeting disciplinary competence in global history.
**Relevant ASJC areas:** History
**CSV Humanities?:** Yes
**CSV ASJC code:** History

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | Specifically scoped to the domain of global history rather than general-purpose multi-task evaluation. |
| Evaluates generative LLM | YES | Evaluates seven models from the Gemini, OpenAI (GPT-4-Turbo), and Llama (Llama-3.1-8B) families. |
| Quantitative performance metrics | YES | Evaluates model performance using balanced accuracy. |
| Published after Mar 2023 | YES | Published at NeurIPS 2024. |

## Benchmark Modalities

**Modality Types:** text

**Description:** Textual questions and answers presented in a four-option multiple-choice format.

## Analytical Tasks

**Task Types:** factual recall, multiple choice qa

**Detailed Description:** Testing factual recall of expert-level global history, specifically societal structures and temporal-regional facts, through a four-choice multiple-choice QA format.

## Summary

This paper introduces the History Seshat Test for LLMs (HiST-LLM), a benchmark derived from the Seshat Global History Databank to evaluate models on expert graduate-level historical knowledge. Spanning 36,000 data points across 600 historical societies, the benchmark reveals that current LLMs outperform random guessing but still fall significantly short of human expert comprehension.

## Key Findings

The evaluated LLMs achieved balanced accuracies ranging from 33.6% (Llama-3.1-8B) to 46.0% (GPT-4-Turbo), outperforming the 25% random baseline. Models demonstrated better performance on earlier historical periods and exhibited regional imbalances, performing best on the Americas and worst on Oceania and Sub-Saharan Africa.

## Reviewer Notes

- Cip's benchmark name was used as it includes the full expansion provided in the text. No other significant disagreements.

## Additional Fields

**Dataset Size:** 36000

**Primary Evaluation Setting:** zero-shot

**Gold Source:** existing_metadata

**Gold Beyond Stimulus:** yes

**Gold Community Dependent:** no

**Gold Concerns Genesis:** no

**Answer Multiplicity:** single_answer

**Plurality Treatment:** not_stated

**Facets Explanation:** The HiST-LLM benchmark is constructed from a subset of the Seshat Global History Databank, a pre-existing structured database of historical data reviewed and assembled by history experts and graduate research assistants. Answering the questions requires domain-specific historical knowledge not present in the prompt stimulus. The evaluation uses a four-choice multiple-choice format, and the treatment of annotator disagreement is not addressed in the provided text.

**Reported Format Gap:** no

**Reported Format Gap Points:** None

**Human Baseline Reported:** no

**Human Gap Points:** None

**Reported Best Score:** 46

**Reported Best Metric:** accuracy

**Reported Cultural Asymmetry:** yes

**Results Explanation:** The paper reports that 'GPT-4-Turbo' achieved the best performance with a balanced accuracy of '46%' ('ranging from 33.6% (Llama-3.1-8B) to 46% (GPT-4-Turbo)') on a 'four-choice format' benchmark. The format gap and human gap fields are null because the paper evaluates a single multiple-choice format and reports no quantified human baseline, only noting that models fall 'short of expert comprehension'. Regional asymmetry is explicitly identified as a finding, with performance being 'better for the Americas and lowest in Oceania and Sub-Saharan Africa for the more advanced models'.
