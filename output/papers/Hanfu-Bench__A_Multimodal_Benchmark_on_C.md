# Hanfu-Bench

**Paper name:** Hanfu-Bench: A Multimodal Benchmark on Cross-Temporal Cultural Understanding and Transcreation
**DOI:** None
**arXiv ID:** None
**Year:** 2025
**Article URL:** https://aclanthology.org/2025.emnlp-main.1251.pdf
**Publication year (from analysis):** 2025

## Humanities Role

**Classification:** domain
**Explanation:** Designed to assess domain-specific competence in Chinese costume history and material culture, requiring models to classify garment features, identify historical styles, and attribute garments to specific historical dynasties (e.g., Qin-Han, Tang, Ming).
**Relevant ASJC areas:** Visual Arts and Performing Arts, History, Conservation
**CSV Humanities?:** 
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | Scoped exclusively to Chinese traditional clothing (Hanfu), its historical evolution, and modern design transcreation. |
| Evaluates generative LLM | YES | Evaluates vision-language models (e.g., GPT-4o, Doubao-1.5-V, MiniCPM-V 2.6, Qwen2.5-VL-7B-Instruct, InternVL2.5) and image generators using LLM-generated captions. |
| Quantitative performance metrics | YES | Classification accuracy for VQA tasks and human evaluation scores on a 5-point Likert scale across six criteria for image transcreation. |
| Published after Mar 2023 | YES | Published at EMNLP 2025. |

## Benchmark Modalities

**Modality Types:** text, image

**Description:** Combines curated datasets of historical Hanfu clothing images with natural language questions for single and multi-image VQA, as well as descriptive transcreation tasks using text-guided image translation.

## Analytical Tasks

**Task Types:** multiple choice qa, classification, generation, visual recognition, attribution, causal and temporal reasoning, cultural reasoning, stylistic analysis

**Detailed Description:** Includes single-image and multi-image multiple-choice VQA for visual recognition and classification of garment components (e.g., sleeves, collars, lapels), chronological attribution to historical dynasties, cross-temporal reasoning across different periods, stylistic analysis of Hanfu variations, and creative text generation for describing modern transcreations of traditional styles.

## Summary

Hanfu-Bench is an expert-curated multimodal benchmark designed to evaluate vision-language models on the cross-temporal understanding and creative transcreation of traditional Chinese garments. It challenges models with fine-grained visual attribute recognition across historical dynasties and evaluates their capacity to adapt traditional designs into modern contexts. The evaluation highlights significant model performance gaps in comparative cross-image reasoning and adaptive design when compared to human domain experts.

## Key Findings

Closed-source VLMs like Doubao-1.5-V achieve up to 82.28% on single-image VQA and 75.95% on multi-image VQA, matching non-experts but lagging behind human costume experts by roughly 10%. VLMs perform particularly poorly on multi-image tasks where humans excel at cross-image comparative reasoning. For the generative image transcreation task, the best-performing model (Stable Diffusion) achieves a compliance success rate of only 42% under multi-dimensional human expert evaluation.

## Reviewer Notes

- Minor disagreements on analytical_tasks: Ciop included 'classification' and 'stylistic_analysis', while Cip included 'factual_recall'. I retained 'classification' and 'stylistic_analysis' because the benchmark tests visual classification of garment components and styles rather than declarative text-based retrieval, making 'factual_recall' less precise here. Dataset size of 4186 was agreed upon (corresponding to the total sum of SVQA and MVQA test items).
- Both analysts agreed on all fields but reported the format gap as 34 points based on the overall dataset score. The final report corrects this to 49 points (InternVL2.5 on the 'Jin' attribute dropping from 78.01% to 29.35%) to capture the largest reported gap.

## Additional Fields

**Dataset Size:** 4186

**Primary Evaluation Setting:** mix

**Gold Source:** domain_expert

**Gold Beyond Stimulus:** yes

**Gold Community Dependent:** no

**Gold Concerns Genesis:** yes

**Answer Multiplicity:** single_answer

**Plurality Treatment:** noise

**Facets Explanation:** The dataset was annotated by nine domain experts (four paper authors and five university Hanfu club members). Features like historical dynasty and specific clothing styles (e.g., collar or sleeve types) were labeled, requiring external historical and cultural knowledge not visually present in the image itself. During annotation, disagreement was treated as noise: features were only retained if all three assigned annotators reached uniform agreement, while unresolved disagreements were marked 'unsure'. The primary visual question answering (VQA) task utilizes multiple-choice questions with exactly one correct option, making the evaluation single_answer.

**Reported Format Gap:** yes

**Reported Format Gap Points:** 49

**Human Baseline Reported:** yes

**Human Gap Points:** 9

**Reported Best Score:** 82.28

**Reported Best Metric:** accuracy

**Reported Cultural Asymmetry:** yes

**Results Explanation:** The paper reports a format gap between single-image (SVQA) and multi-image (MVQA) setups on the same benchmark. The largest such gap occurs for InternVL2.5 on the 'Jin' attribute, where accuracy drops from 78.01% on SVQA to 29.35% on MVQA, a difference of 49 percentage points (Table 1). A human expert baseline of 83.54% is reported on the MVQA subset, outperforming the best model (Doubao-1.5-V at 74.48%) by 9 points (Table 2). The best overall model score is 82.28% accuracy by Doubao-1.5-V on the SVQA task (Table 1). The paper reports a cultural asymmetry, finding that English prompts consistently degrade model performance on SVQA compared to Chinese prompts due to difficulties in aligning culturally specific terms (Section 4.3).
