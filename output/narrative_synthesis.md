# Survey Narrative Synthesis

# Synthesizing AI Benchmarks in the Arts & Humanities: A Survey Analysis

This document provides a comprehensive narrative synthesis of recent benchmark evaluations of Large Language Models (LLMs) and Multimodal Large Language Models (MLLMs) across Arts & Humanities tasks. 

---

## 1. Thematic Clusters

The analyzed papers can be grouped into five distinct thematic clusters based on ASJC subject areas, modality combinations, and analytical tasks.

### Cluster 1: Visual Arts, Heritage, and Aesthetics
*   **Papers:** MMMU-Pro, Christian Iconography, VQArt-Bench, VULCA-BENCH (x2), Appear2Meaning, EduArt, Hanfu-Bench, DRISHTIKON, CHVM-1K.
*   **Common Thread:** This cluster focuses on the **Visual Arts and Museology**. These benchmarks are predominantly **multimodal (image + text)** and move beyond basic object recognition to demand deep cultural, aesthetic, and art-historical reasoning. Tasks involve iconographic interpretation, cross-temporal reasoning (e.g., dynastic changes in *Hanfu-Bench*), generating expert-level art critiques (*VULCA-BENCH*), and inferring non-observable cultural metadata (*Appear2Meaning*). 

### Cluster 2: Historical Archival Processing and Philology
*   **Papers:** HistBench, LLMs4Subjects, CzechTopic, OfficeQA Pro, Al-Shamela, Hist Doc OCR, Finding the Plea, Post-OCR BLN600, RISE Humanities Data, Bullinger Letters.
*   **Common Thread:** Grounded heavily in **History, Classics, and Digital Humanities**, this cluster treats historical documents as philological artifacts. Operating across **text and text+image** modalities, the analytical tasks are highly structural and workflow-oriented: optical character recognition (OCR) of archaic fonts, diplomatic transcription, layout segmentation, cross-lingual summarization of historical dialects, and rhetorical sequence labeling. 

### Cluster 3: Cultural Nuance and Multilingual Reasoning
*   **Papers:** CulturalBench, MILU, Global-MMLU, MultiNRC, CulturALL, CaLMQA, C3B, MMLU-ProX.
*   **Common Thread:** Anchored in **Language and Linguistics, Religious Studies, and Area Studies**, this cluster assesses models on localized cultural intelligence. Mostly **text-only** (with the exception of *C3B*), these benchmarks test cross-lingual reasoning, multi-mode cultural behaviors, and the mitigation of Western-centric biases. Tasks include long-form culturally specific QA, cultural conflict detection, and resolving culturally grounded daily scenarios.

### Cluster 4: Linguistic Mechanics, Wordplay, and Rhetoric
*   **Papers:** LAMBADA, AdMIRe, JOKER Task 2, Humor Prompting, PSH v1.0.
*   **Common Thread:** Centered exclusively on **Literature and Linguistics**, this cluster isolates the mechanics of human language. It includes rare modality combinations like **text+audio** (*Humor Prompting*). The analytical tasks dive into the pragmatic and stylistic depths of language: semantic disambiguation of idioms, pun translation, humor explanation, and speaker-specific rhetorical mimicry. 

### Cluster 5: General Factual QA and Agentic Retrieval
*   **Papers:** MMLU, FActScore, LongFact, Humanity's Last Exam, SuperGPQA, BrowseComp, DeepSearchQA, HiST-LLM, M3Exam, SimpleQA.
*   **Common Thread:** These papers span **Broad Humanities** but treat humanistic disciplines as massive repositories of factual content to test general AI intelligence. Primarily **text-only**, they focus on multiple-choice question answering (MCQA), fact verification, calibration, and multi-hop agentic web retrieval. 

---

## 2. Modality & Task Landscape

### Modality Coverage
*   **Dominant:** **Text-only** remains the default modality for assessing historical knowledge, cultural reasoning, and factual retrieval. **Text + Image** is rapidly maturing, particularly for Visual Arts (paintings, artifacts, comics) and archival History (scanned manuscripts, historic newspapers).
*   **Rare/Underrepresented:** **Audio and Video** are severely underrepresented. Only *Humor Prompting* utilized TTS audio to test phonetic ambiguity, and *HistBench* incorporated oral histories and video clips. Given the importance of Musicology, Performing Arts, and oral traditions in the humanities, the lack of time-based media benchmarks is a glaring gap.

### Task Types
*   **Dominant:** **Factual recognition and MCQA** dominate general-purpose benchmarks (e.g., MMLU, MILU, SuperGPQA). In multimodal datasets, **Visual Question Answering (VQA)** and fine-grained visual recognition are the standard. 
*   **Emerging:** **Generative reasoning and agentic workflows** are gaining traction. Benchmarks like *BrowseComp*, *DeepSearchQA*, and *HistBench* evaluate autonomous agents navigating archives, while *VULCA-BENCH* and *CaLMQA* assess complex, long-form generative interpretation.

### Task-Domain Alignment
There is a stark contrast in how well analytical tasks align with true humanistic methodology:
*   **Poor Alignment (The "Flattening" Effect):** General benchmarks (e.g., *MMLU, MMMU-Pro, LongFact*) often flatten deeply interpretive humanities disciplines into multiple-choice trivia or rigid atomic fact verification. They test *content recall* rather than *humanistic critique*.
*   **Strong Alignment:** Newer, domain-specific benchmarks exhibit excellent methodological alignment. *VULCA-BENCH* uses Panofsky’s art-historical theories to grade critiques; *Hist Doc OCR* measures "over-historicization" (anachronistic insertion of archaic letters); and *Finding the Plea* evaluates rhetorical segmentation of 18th-century petitions exactly as a digital humanist would.

---

## 3. Methodological Patterns

*   **Models Tested:** The frontier proprietary models (GPT-4o, Claude 3.5 Sonnet, Gemini 1.5/2.0 Pro) are universally tested. Notably, the recent wave of papers (late 2024–2026) heavily evaluates **reasoning models** (OpenAI o1/o3, DeepSeek-R1), finding that Chain-of-Thought (CoT) improves structural tasks but can occasionally degrade subjective/aesthetic interpretation.
*   **Standard vs. Novel Metrics:** 
    *   *Standard:* Accuracy, F1, BLEU, and Exact Match remain staples. 
    *   *Novel:* We see a rise in bespoke humanistic metrics. Examples include *Historical Character Preservation Rate (HCPR)* for archival OCR, *Dimension Coverage Rate (DCR)* for multi-layered art critiques, and *pun location-based* scoring for translated humor. 
    *   *Evaluation Mechanisms:* **LLM-as-a-Judge** is standardizing the evaluation of generative humanities tasks, though papers like *VULCA-BENCH* warn that judges require complex sigmoid calibration against human experts to avoid generic biases.
*   **Task Complexity Variances:** Tasks range from Level 1 perceptual/factual recall to Level 5 philosophical synthesis. Almost all papers report a massive performance cliff when moving from surface-level identification (e.g., recognizing a saint) to deep causal or cultural reasoning (e.g., explaining the symbolic meaning of the saint within a specific temporal era).

---

## 4. Narrative Framing Options

Depending on the target audience of the survey paper, this corpus supports three distinct narrative framings:

### Framing 1: For AI Researchers (Focus: The Humanities as the Ultimate Reasoning Frontier)
*   *Narrative:* The Arts & Humanities are no longer just "soft data." They represent the most complex, unstructured, and culturally nuanced reasoning environments available. As STEM benchmarks (like GSM8K or MATH) saturate, humanities benchmarks (*Humanity's Last Exam*, *VULCA-BENCH*, *BrowseComp*) expose critical flaws in modern LLMs: severe Western-centric biases, failure in deep multi-hop qualitative reasoning, and a lack of grounding in localized, multi-modal cultural contexts.

### Framing 2: For Digital Humanities Scholars (Focus: LLMs as Epistemological Tools)
*   *Narrative:* How do LLMs change the praxis of digital humanities? This framing emphasizes the shift from using LLMs as simple OCR or translation utilities (though they excel there, e.g., *RISE Humanities Data*, *Al-Shamela*) to acting as analytical partners. It highlights how benchmarks are operationalizing humanities theory (e.g., rhetorical analysis, Panofsky's iconology) into computable metrics, while warning of temporal and cultural hallucinations.

### Framing 3: For Newcomers (Focus: Bridging the Cultural Divide)
*   *Narrative:* An accessible overview of how AI interacts with human culture. This framing would organize the survey by cultural artifacts—how AI reads ancient texts, looks at Renaissance art, understands a joke, or navigates a cultural faux pas. It emphasizes the journey from basic factual recall to genuine multicultural understanding.

---

## 5. Gaps and Opportunities

*   **Underrepresented Modalities & Domains:** 
    *   **Music and Performing Arts:** Music is rarely tested beyond multiple-choice theory questions. Audio-based analysis of musical structure, ethnomusicology, or video analysis of dance and theater are entirely absent.
    *   **3D / Spatial Reasoning:** Architecture and archaeological site analysis are largely reduced to 2D image recognition. 
*   **Gaps in Analytical Complexity:** We lack benchmarks evaluating **longitudinal causal reasoning** (e.g., "Trace the economic factors leading to the French Revolution across these ten primary sources") and **subjective hermeneutics** (e.g., navigating conflicting interpretations of a literary text without enforcing a single "correct" ground truth).
*   **The "Next-Generation" Humanities Benchmark:** A next-gen benchmark would be an **interactive, agentic, multi-modal sandbox**. An AI would be dropped into an uncurated, multi-lingual digital archive containing corrupted texts, audio recordings, and images. The task would be to synthesize a coherent historical narrative or exhibition catalog, evaluated not by a binary "True/False" metric, but by a panel of expert LLM-judges on creativity, historical fidelity, citation accuracy, and avoidance of cultural anachronism.

---

## 6. Suggested Survey Structure

To effectively synthesize these findings for an academic audience, the survey paper should be structured methodologically, tracking the evolution from capability evaluation to domain-specific application.

**Title:** *Beyond the Factoid: A Survey of Large Language Model Benchmarks in the Arts and Humanities*

1.  **Introduction**
    *   The saturation of STEM benchmarks and the pivot to Cultural/Humanities evaluation.
    *   Defining the scope: General Intelligence vs. Domain-Specific DH tools.
2.  **The Modality Landscape in Cultural Data**
    *   *Textual Foundations:* Multilingualism, historical philology, and long-form QA.
    *   *The Visual Turn:* Heritage imaging, art history, and multimodal layout processing.
    *   *The Missing Senses:* The dearth of audio, video, and spatial humanities benchmarks.
3.  **Domain-Specific Advancements (Thematic Analysis)**
    *   *History and Archives:* From OCR denoising to agentic historical retrieval.
    *   *Art and Aesthetics:* Moving from object recognition to philosophical critique.
    *   *Linguistics and Culture:* Humor, idioms, and localized cultural reasoning.
4.  **Methodological Evolutions in Evaluation**
    *   The "Flattening" Problem: The limits of multiple-choice formats for interpretive fields.
    *   Operationalizing Theory: Integrating Panofsky, Goodman, and classical rhetoric into AI metrics.
    *   Novel Metrics: Measuring "over-historicization," semantic drift, and temporal bias.
5.  **The Limits of Current Models**
    *   Western-centric biases and low-resource language collapse.
    *   The failure of reasoning models (o1, DeepSeek-R1) in subjective aesthetic spaces.
6.  **Future Directions: Towards an Agentic Digital Humanities**
    *   Embracing epistemic uncertainty and conflicting interpretations.
    *   Proposals for the next generation of multi-modal, archive-grounded AI benchmarks.
7.  **Conclusion**