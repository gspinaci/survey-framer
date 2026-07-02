# Taiwanese Hakka Cultural Knowledge Benchmark

**Paper name:** Taiwanese Hakka Cultural Knowledge Benchmark
**DOI:** None
**arXiv ID:** None
**Year:** 2024
**Article URL:** https://arxiv.org/html/2409.01556v2
**Publication year (from analysis):** 2024

## Humanities Role

**Classification:** both
**Explanation:** Evaluates LLMs on domain-specific Hakka cultural heritage (history, language, cuisine, architecture) using questions designed across Bloom's Taxonomy cognitive levels.
**Relevant ASJC areas:** History, Language and Linguistics, Visual Arts and Performing Arts
**CSV Humanities?:** Yes
**CSV ASJC code:** 

## Inclusion Criteria

| Criterion | Met? | Note |
|-----------|------|------|
| General-purpose benchmark | NO | Specifically designed for evaluating Taiwanese Hakka cultural knowledge, not general-purpose capabilities. |
| Evaluates generative LLM | YES | Evaluates several advanced LLMs including GPT-4o, Gemini 1.5 Pro, Claude 3.5 Sonnet, and Llama 3.1. |
| LLM is primary evaluated system | YES | LLMs are the primary systems being benchmarked to evaluate their performance across cognitive domains. |
| Arts & Humanities data/tasks | YES | Covers History, Language and Linguistics, and Visual Arts and Performing Arts (focusing on local customs, architecture, cuisine, festivals, and theater). |
| Quantitative performance metrics | YES | Evaluated using accuracy rates (%) across various categories and cognitive domains. |
| Published after Mar 2023 | YES | The paper references 2024 sources and was generated in September 2024. |
| English language | YES | The paper is written in English. |

## Benchmark Modalities

**Modality Types:** text

**Description:** Text-only multiple-choice question-and-answer format based on the Hakka Culture Encyclopedia and the Ministry of Education's Hakka Knowledge Base.

## Analytical Tasks

**Task Types:** multiple-choice question answering, factual recall, cultural reasoning, creative synthesis evaluation

**Detailed Description:** Tasks evaluate six hierarchical cognitive levels from Bloom's Taxonomy: Remembering (recalling Hakka settlements), Understanding (comprehending culinary practices), Applying (adapting clothing styles), Analyzing (comparing Hakka opera to other forms), Evaluating (assessing historical social status), and Creating (evaluating ideas for showcasing heritage).

## Summary

This paper introduces a specialized benchmark consisting of 10,158 multiple-choice questions designed to evaluate LLMs' understanding of Taiwanese Hakka culture. Using Bloom's Taxonomy, the authors structure the questions across six cognitive levels (from basic recall to creative synthesis) to systematically assess model reasoning. Additionally, the study demonstrates how integrating Retrieval-Augmented Generation (RAG) dramatically improves the cultural knowledge accuracy of lower-performing models like Llama 3.1.

## Key Findings

Claude 3.5 Sonnet (83.33% accuracy) outperformed GPT-4o (82.09%) and Gemini 1.5 Pro (79.25%) among baseline models. However, integrating RAG with Llama 3.1 achieved the highest overall accuracy of 90.20%, significantly boosting performance in factual recall (from 61.61% to 91.08%). In contrast, baseline models still excelled in the 'Creating' cognitive domain without RAG, with GPT-4o scoring highest at 87.89%.
