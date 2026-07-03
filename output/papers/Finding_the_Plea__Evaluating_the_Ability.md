# Finding the Plea: Evaluating the Ability of LLMs to Identify Rhetorical Structure in Swedish and English Historical Petitions

**Paper name:** Finding the Plea: Evaluating the Ability of LLMs to Identify Rhetorical Structure in Swedish and English Historical Petitions
**DOI:** None
**arXiv ID:** None
**Year:** 2025
**Article URL:** https://acl-bg.org/proceedings/2025/LM4DH%202025/pdf/2025.lm4dh-1.8.pdf
**Publication year (from analysis):** 2025

## Humanities Role

**Classification:** domain
**Explanation:** Evaluates LLM performance on rhetorical structure annotation of historical 18th-century petitions, designed directly for digital humanities workflows and historical research.
**Relevant ASJC areas:** History, Language and Linguistics
**CSV Humanities?:** Yes
**CSV ASJC code:** Language and Linguistics

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | Specifically designed as a domain-specific digital humanities evaluation of 18th-century historical texts, not a broad, general-purpose benchmark. |
| Evaluates generative LLM | YES | Evaluates GPT-4, Gemini 1.5 Pro, Mixtral 8x22B, Mistral 7B, LLaMA-3 70B, and LLaMA-3 8B. |
| LLM is primary evaluated system | YES | The LLMs themselves are the primary systems evaluated on their annotation accuracy. |
| Arts & Humanities data/tasks | YES | Historical Swedish and English legal/administrative petitions from the 18th century, mapping to History and Language and Linguistics. |
| Quantitative performance metrics | YES | Evaluated using token-level precision, recall, F1-score, normalized Levenshtein distance (mean token-level edit distance), Mean Error, and Spearman's rank correlation. |
| Published after Mar 2023 | YES | Published at the RANLP 2025 workshop in September 2025. |
| English language | YES | The paper is written in English, and the benchmark evaluates both English and Swedish texts. |

## Benchmark Modalities

**Modality Types:** text

**Description:** Monomodal evaluation using text transcriptions of historical 18th-century Swedish and English petitions.

## Analytical Tasks

**Task Types:** rhetorical structure identification, sequence labeling, difficulty estimation

**Detailed Description:** Models are evaluated on identifying and segmenting fine-grained classical rhetorical sections (Salutatio, Petitio, Conclusio) in historical texts, and self-estimating document annotation difficulty to compare with human uncertainty.

## Summary

This study evaluates the ability of various LLMs to identify and annotate key rhetorical structures (Salutatio, Petitio, and Conclusio) in 18th-century Swedish and English historical petitions. The authors construct a dataset of 200 annotated petitions and assess commercial and open-source models using few-shot prompting across variations in prompt complexity and language. Additionally, the study contrasts model-assigned difficulty ratings with human-assessed text difficulty to analyze alignment in confidence and uncertainty.

## Key Findings

Larger models (e.g., GPT-4, LLaMA-3 70B, Gemini) perform exceptionally well on identifying the opening greeting (Salutatio), achieving F1 scores in the high 90s. However, identifying the request (Petitio) and conclusion (Conclusio) sections proves more challenging, especially for smaller models and Swedish-language texts. Furthermore, models systematically underestimate document difficulty compared to human annotators, demonstrating weak or negative correlation with human difficulty rankings.

## Reviewer Notes

- humanities_role: Ciop chose 'domain', Cip chose 'both'. Resolved to 'domain' because the task is specifically designed as a digital humanities tool for historical text processing rather than a general knowledge test. relevant_asjc_areas: Ciop included 'Literature and Literary Theory', Cip did not. Resolved to exclude Literature, as historical legal/administrative petitions align better with History and Language & Linguistics. analytical_tasks: Merged Ciop and Cip's lists to include 'rhetorical structure identification', 'sequence labeling', and 'difficulty estimation'.

## Additional Fields

**Dataset Size:** 200

**Primary Evaluation Setting:** few-shot
