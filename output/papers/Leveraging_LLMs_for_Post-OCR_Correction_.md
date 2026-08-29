# Leveraging LLMs for Post-OCR Correction of Historical Newspapers

**Paper name:** Leveraging LLMs for Post-OCR Correction of Historical Newspapers
**DOI:** None
**arXiv ID:** None
**Year:** 2024
**Article URL:** https://aclanthology.org/2024.lt4hala-1.14.pdf
**Publication year (from analysis):** 2024

## Humanities Role

**Classification:** content
**Explanation:** Uses 19th-century British newspaper articles as content for post-OCR correction, evaluating a general NLP capability of text reconstruction and error correction rather than domain-specific historical analysis.
**Relevant ASJC areas:** History, Language and Linguistics
**CSV Humanities?:** Yes
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | Strictly scoped to the task of post-OCR correction on a dataset of historical newspapers. |
| Evaluates generative LLM | YES | Evaluates Llama 2 (7B and 13B models) alongside BART. |
| Quantitative performance metrics | YES | Evaluates using percentage reduction in Character Error Rate (CER), computed using Levenshtein distance. |
| Published after Mar 2023 | YES | Published in May 2024 at LT4HALA. |

## Benchmark Modalities

**Modality Types:** text

**Description:** Text-only parallel corpus consisting of OCR-generated text as source inputs and manually re-keyed human transcriptions as target outputs.

## Analytical Tasks

**Task Types:** transcription and correction

**Detailed Description:** Post-OCR correction and error repair on historical newspapers, mapping erroneous OCR character sequences to accurate reference texts, including handling substitutions, insertions, deletions, and misnamed entities.

## Summary

This paper evaluates the performance of generative Large Language Models, specifically Llama 2, on the task of post-OCR correction for historical newspapers. Comparing an instruction-tuned Llama 2 against a fine-tuned sequence-to-sequence BART baseline on the BLN600 dataset, the authors demonstrate that LLMs can effectively reconstruct noisy OCR text and achieve superior error reduction even with limited training data.

## Key Findings

The instruction-tuned Llama 2 13B model significantly outperformed the fine-tuned BART baseline, achieving a 54.51% reduction in Character Error Rate (CER) compared to BART's 23.30% reduction. Furthermore, Llama 2 demonstrated strong correction capabilities even when trained on very small data subsets, highlighting its data efficiency.

## Reviewer Notes

- Ciop correctly set benchmark_name to null because the BLN600 dataset was introduced by a different paper (Booth et al., 2024), which is cited in the text; Cip's extraction of 'BLN600' was therefore rejected in favor of the null instruction. Both analysts were otherwise in complete agreement on all fields, including the choice of 'fine-tuned' for LoRA instruction tuning.
- gold_source: Cip inferred 'existing_metadata' under the assumption that the manual transcriptions were a product of the British Library Newspapers digitisation project itself. However, the text only states that the OCR is from that project and the ground truth consists of 'manually re-keyed human transcriptions' from the BLN600 corpus, without detailing their origin. Resolved to 'not_stated' as per Ciop's reading. All other fields were in agreement.

## Additional Fields

**Dataset Size:** 13192

**Primary Evaluation Setting:** fine-tuned

**Gold Source:** not_stated

**Gold Beyond Stimulus:** no

**Gold Community Dependent:** no

**Gold Concerns Genesis:** no

**Answer Multiplicity:** single_answer

**Plurality Treatment:** not_stated

**Facets Explanation:** The reference answers are sourced from the BLN600 corpus, which pairs OCR excerpts with 'manually re-keyed human transcriptions' from the source images, though the paper does not specify who authored these transcriptions or under what conditions (hence 'not_stated'). Post-OCR correction relies on reconstructing the text segment itself, requiring no external knowledge beyond the stimulus. Model performance is evaluated quantitatively by calculating Character Error Rate against a single ground-truth target sequence per item. The paper does not address annotator disagreement or the possibility of alternative valid transcriptions.

**Reported Format Gap:** no

**Reported Format Gap Points:** None

**Human Baseline Reported:** no

**Human Gap Points:** None

**Reported Best Score:** 54.51

**Reported Best Metric:** other

**Reported Cultural Asymmetry:** not_stated

**Results Explanation:** The best-performing model, 'Llama 2' '13B', achieves a headline score of '54.51' on the 'CER Reduction (%)' metric ('achieving a 54.51% reduction in the character error rate'). No quantified human baseline is reported for this task. There is no comparison of format or difficulty gaps. Cultural asymmetry is 'not_stated' because the BLN600 benchmark is monolingual, consisting entirely of 19th-century British newspaper articles written in English.
