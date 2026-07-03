# Survey Narrative Synthesis

Here is a narrative synthesis document designed for an academic survey paper at the intersection of AI benchmarking and Digital Humanities (DH).

---

# AI Benchmarking in the Arts & Humanities: A Synthesis of Current Landscapes and Future Directions

## 1. Thematic Clusters
The current corpus of AI benchmarks in the Arts and Humanities can be grouped into five distinct thematic clusters, reflecting a gradient from general factual knowledge to highly specialized methodological reasoning.

### Cluster 1: Encyclopedic Knowledge and Global Cultural Alignment
*   **Papers:** *MMLU, FActScore, LongFact, MILU, CulturalBench, Global-MMLU, CaLMQA, CulturALL, SimpleQA, MMLU-ProX, M3Exam, HiST-LLM.*
*   **Common Thread:** This is the largest and most established cluster. It treats humanities disciplines (History, Literature, Religion) primarily as repositories of factual content. Modally restricted to text (with rare exceptions like *M3Exam*), these benchmarks evaluate LLMs on broad cultural competency, factual recall, and cross-cultural alignment, heavily utilizing multiple-choice question (MCQ) answering or short-form factual generation.

### Cluster 2: Visual Arts, Material Culture, and Aesthetics
*   **Papers:** *MMMU-Pro, Christian Iconography, C3B, VQArt-Bench, VULCA-BENCH (x2), Appear2Meaning, Hanfu-Bench, DRISHTIKON.*
*   **Common Thread:** Focused on Visual Arts, Museology, and Archaeology, this multimodal (image+text) cluster evaluates Vision-Language Models (VLMs). Unlike general vision tasks (e.g., object detection), these benchmarks require fine-grained cultural reasoning, such as decoding religious symbolism, recognizing dynastic clothing (*Hanfu-Bench*), and performing expert-level philosophical/aesthetic critiques (*VULCA-BENCH*). 

### Cluster 3: Digital Humanities Workflows and Philology
*   **Papers:** *LLMs4Subjects, CzechTopic, Russian OCR, Swedish Petitions, Post-OCR Llama, The RISE Humanities Data Benchmark.*
*   **Common Thread:** These papers treat AI not as a subject-matter expert, but as a methodological tool for historians and archivists. Spanning text and image modalities, they focus on structural tasks like transcription, post-OCR error correction of 19th-century newspapers, layout segmentation, and topic localization in historical archives.

### Cluster 4: Linguistic Nuance, Translation, and Rhetoric
*   **Papers:** *LAMBADA, AdMIRe, MultiNRC, Al-Shamela, CLEF JOKER Task 2, Latin Translation, PSH v1.0, Multimodal Humor.*
*   **Common Thread:** Centered on Language and Linguistics and Literature, this cluster tests deep semantic processing. Tasks range from translating classical Islamic texts (*Al-Shamela*) and 16th-century Neo-Latin correspondence to preserving phonetic wordplay (*JOKER, Multimodal Humor*) and replicating speaker-specific rhetorical fingerprints (*PSH v1.0*). 

### Cluster 5: Complex Reasoning and Agentic Archival Retrieval
*   **Papers:** *Humanity's Last Exam, SuperGPQA, BrowseComp, HistBench, DeepSearchQA, OfficeQA Pro.*
*   **Common Thread:** This cutting-edge cluster moves beyond static datasets to evaluate multi-hop reasoning and autonomous agentic workflows. By utilizing historical and financial archives, these benchmarks test an AI’s ability to navigate epistemic uncertainty, resolve entity variations over time, and construct complex historical narratives via search.

---

## 2. Modality & Task Landscape

### Modality Coverage
*   **Dominant:** **Text-only** remains the most ubiquitous modality, driven by the legacy of NLP research and the text-heavy nature of historical and literary archives. **Image+Text (Multimodal)** is rapidly maturing, particularly for Visual Arts, Museology, and manuscript digitization.
*   **Rare/Underrepresented:** **Audio and Video** are severely underrepresented. Only *Multimodal Humor* (audio TTS for puns) and *HistBench* (oral histories/video clips) incorporate time-based media, leaving fields like ethnomusicology, performing arts, and linguistic phonetics largely unbenchmarked.

### Task Types
*   **Dominant:** **Factual Recognition (MCQs)** still dominates the landscape (*MMLU, HiST-LLM*). However, there is a strong shift toward **Structured Extraction/Classification** (*Appear2Meaning, LLMs4Subjects*) and **Generative Verification** (*FActScore, LongFact*).
*   **Emerging:** **Agentic Retrieval** (*DeepSearchQA, BrowseComp*) and **Complex Visual Reasoning** (*VQArt-Bench*).

### Task-Domain Alignment
Historically, benchmarks suffered from poor task-domain alignment—reducing deep humanities interpretation to trivial MCQs (flattening hermeneutics into trivia). However, recent papers show excellent alignment: *VULCA-BENCH* uses Panofsky’s established art-historical framework; *Russian OCR* measures period-specific archaic character insertion; and *RISE* uses exact XML workflows demanded by real-world archivists.

---

## 3. Methodological Patterns

*   **Evaluation Approaches:** The field is transitioning from static zero-shot/few-shot comparisons against human baselines toward **LLM-as-a-Judge** paradigms (*CulturALL, SimpleQA*). Agentic tool-use (web search, OCR tools) is becoming standard for high-complexity tasks (*HistAgent*).
*   **Tested Models:** Benchmarks uniformly test frontier proprietary models (GPT-4o, Claude 3.5 Sonnet, Gemini 1.5/2.0 Pro) against high-performing open-weights (Llama 3, Qwen2.5/3, DeepSeek-R1). 
*   **Metrics (Standard vs. Novel):** While BLEU, F1, and Accuracy are standard, researchers are increasingly inventing domain-specific metrics. Examples include *Historical Character Preservation Rate (HCPR)* for OCR, *Dimension Coverage Rate (DCR)* for art critique, and *Pun-Location Overlap* for humor translation.
*   **Task Complexity:** Complexity has scaled aggressively. Models have saturated basic factual recall; modern benchmarks now test *epistemic limits*—such as solving multi-constraint historical puzzles (*BrowseComp*), translating low-resource archaic languages (*MultiNRC*), and identifying cultural co-occurrence conflicts in visual narratives (*C3B*).

---

## 4. Narrative Framing Options

Depending on the target audience for the survey paper, this corpus supports three distinct narrative framings:

### Framing 1: For AI Researchers (Focus: "The Ultimate Reasoning Frontier")
*   **The Hook:** Humanities data is unstructured, culturally biased, multimodal, and full of epistemic uncertainty.
*   **Emphasis:** Highlight how humanities benchmarks expose the limits of frontier reasoning models. Focus on agentic workflows (*DeepSearchQA*), multi-hop historical retrieval, and the failure of LLMs to handle non-Western cultural common sense (*CulturalBench, MMLU-ProX*). Humanities are framed as the ultimate stress test for Artificial General Intelligence (AGI).

### Framing 2: For Digital Humanities (DH) Scholars (Focus: "AI as a Methodological Tool")
*   **The Hook:** Moving beyond chatbots, AI is ready to be integrated into rigorous DH pipelines.
*   **Emphasis:** Focus heavily on *Cluster 3 (Workflows)*. Frame the survey around utility and methodological alignment. Highlight how LLMs perform on transcription, XML correction (*RISE*), structural rhetorical annotation (*Swedish Petitions*), and the novel philological metrics used to catch AI hallucinations like "over-historicization."

### Framing 3: For Interdisciplinary Newcomers (Focus: "Evaluating Machine Culture")
*   **The Hook:** Can machines understand human culture, art, and humor?
*   **Emphasis:** A broad, accessible overview of ASJC domains. Trace the evolution from simple factual recall (*MMLU*) to deep aesthetic critique (*VULCA-BENCH*). Highlight the multimodal capabilities of VLMs looking at historical artifacts, and the challenges of translating cultural nuances (*Al-Shamela, JOKER*).

---

## 5. Gaps and Opportunities

### Missing Modalities & Task Types
*   **Audio/Video/3D:** There is a glaring lack of benchmarks for Ethnomusicology, Performing Arts, and 3D Archaeological artifacts. 
*   **Interpretive Conflict:** Current benchmarks mostly assume a single "ground truth." There are no benchmarks evaluating how an LLM handles conflicting primary sources or engages in historiographical debate.

### Missing ASJC Sub-domains
While History and Visual Arts are well-represented, **Musicology**, **Performing Arts**, **Digital Sociology**, and **Non-Western Philosophy** remain sparse. Furthermore, evaluations of indigenous or heavily localized material cultures are often limited to translation tasks rather than deep cultural reasoning.

### The "Next-Generation" Humanities Benchmark
A next-generation benchmark—call it *HermeneuticBench*—would be:
1.  **Agentic & Multimodal:** Providing an LLM agent with an archive of raw, untranscribed, multimodal primary sources (e.g., messy handwritten letters, audio recordings, and photographs).
2.  **Epistemic/Argumentative:** Tasking the model to synthesize a coherent historical argument or aesthetic critique that accounts for biases in the sources.
3.  **Humanist-Graded:** Evaluated not by an automated LLM-as-a-judge, but via double-blind peer review by domain experts assessing narrative coherence, historiographical awareness, and avoidance of anachronism.

---

## 6. Suggested Survey Structure

**Title:** *From Trivia to Hermeneutics: A Survey of AI Benchmarking in the Arts and Humanities*

**Table of Contents:**
1.  **Introduction**
    *   The rise of LLMs/MLLMs and the need for domain-specific evaluation.
    *   Scope of the survey (ASJC Arts & Humanities classifications).
2.  **The Evolution of Task Complexity in Humanities AI**
    *   *Phase 1:* Factual Recall and Encyclopedic Knowledge (MMLU, FActScore).
    *   *Phase 2:* Cultural Alignment and Native Reasoning (MultiNRC, CulturALL).
    *   *Phase 3:* Expert-Level Critique and Aesthetics (VULCA-BENCH, Humanity's Last Exam).
3.  **Methodological Alignment: AI in Digital Humanities Workflows**
    *   Post-OCR, Transcription, and Philology (Russian OCR, RISE Benchmark).
    *   Linguistics, Rhetoric, and Translation (Al-Shamela, AdMIRe).
    *   Agentic Archival Retrieval (DeepSearchQA, HistAgent).
4.  **The Multimodal Frontier in Cultural Heritage**
    *   Vision-Language Models in Visual Arts and Museology.
    *   The missing modalities: Audio, Video, and Spatial data.
5.  **Evaluation Paradigms and Novel Metrics**
    *   Moving beyond Accuracy/F1: Introducing humanities-aligned metrics.
    *   The role (and limits) of LLM-as-a-judge in subjective domains.
6.  **Gaps, Biases, and Future Directions**
    *   Western-centric biases in cultural evaluation.
    *   Designing the next generation of argumentative/hermeneutic benchmarks.
7.  **Conclusion**