# Survey Narrative Synthesis

Here is a narrative synthesis document designed for an academic survey paper, based on the provided corpus of AI benchmarking and digital humanities (DH) research.

***

# Evaluating AI in the Arts & Humanities: A Synthesis of Current Benchmarks

## 1. Thematic Clusters
The analyzed corpus reveals a distinct evolution in how AI models are evaluated on Arts & Humanities tasks, moving from broad, general-knowledge trivia to highly specialized, culturally situated evaluations. The papers can be grouped into five primary thematic clusters:

### Cluster 1: Digital Philology and Computational Linguistics
* **Common Thread:** Focuses on the structural, syntactic, and historical nuances of language. These benchmarks treat texts not just as data, but as historical artifacts requiring specialized parsing, translation, and error correction.
* **Modalities:** Text-only (with minor image/text OCR tasks).
* **Analytical Tasks:** OCR correction, diplomatic transcription, syntactic acceptability, machine translation of historical languages.
* **Representative Papers:** *CzechTopic*, *Automated Translation of Islamic Literature*, *Historical Document OCR*, *Evaluating LLMs on Lithuanian*, *JOKER Task 1*, *LLM-based MT for Latin*, *Leveraging LLMs for Post-OCR*, *EvaHan2024*, *Tracking Belarusian*.

### Cluster 2: Visual Arts, Iconography, and Cultural Heritage
* **Common Thread:** Evaluates multimodal systems on their capacity to process, identify, and interpret visual culture. These benchmarks push beyond basic object recognition to demand aesthetic judgment, symbolic decoding, and cross-cultural contextualization.
* **Modalities:** Multimodal (Image + Text).
* **Analytical Tasks:** Generative art critique, iconography classification, visual reasoning, cultural metadata inference.
* **Representative Papers:** *MMMU-Pro*, *Christian Iconography*, *VQArt-Bench*, *VULCA-BENCH*, *Appear2Meaning*.

### Cluster 3: Historical Knowledge and Factual Reasoning
* **Common Thread:** Assesses models on their retrieval and synthesis of historical facts, chronological reasoning, and global historical comprehension. This cluster ranges from generalized multiple-choice trivia to complex, multi-hop archival search tasks.
* **Modalities:** Text-only.
* **Analytical Tasks:** Factual QA, multi-hop reasoning, open-domain web search, constraint solving.
* **Representative Papers:** *TriviaQA*, *MMLU*, *LongFact*, *MILU*, *Global-MMLU*, *SuperGPQA*, *HiST-LLM*, *Hakka Cultural Knowledge Benchmark*, *SimpleQA*, *DeepSearchQA*, *BrowseComp*.

### Cluster 4: Literary, Narrative, and Stylistic Analysis
* **Common Thread:** Moves beyond literal meaning to evaluate how models handle figurative language, narrative framing, emotional polarity, and human stylistic mimicry.
* **Modalities:** Primarily Text-only (with *AdMIRe* integrating images).
* **Analytical Tasks:** Aspect-based sentiment analysis, rhetorical mimicry, narrative extraction, idiom representation.
* **Representative Papers:** *LAMBADA*, *Travelogues ABSA*, *Rhetorical Fingerprints*, *SemEval-2025 Task 10*, *Nostra Domina at EvaLatin*, *AdMIRe*, *GDPval* (Creative occupations subset).

### Cluster 5: Epistemology, Bias, and Cultural Alignment
* **Common Thread:** Investigates the ethical and epistemic limitations of LLMs when applied to humanities contexts, focusing on Western-centric biases, stereotyping, and historical distortion.
* **Modalities:** Text-only.
* **Analytical Tasks:** Bias detection, value alignment assessment, cultural sensitivity classification.
* **Representative Papers:** *BBQ*, *FActScore*, *CHVM-1K*, *SEA-HELM*.

---

## 2. Modality & Task Landscape

### Modality Coverage
* **Dominance of Text-Only:** The vast majority of benchmarks remain text-centric. Even when dealing with visually rich fields like history, models are mostly tested via textual proxies (e.g., *MMLU*, *HiST-LLM*).
* **Growth in Image+Text:** Multimodal evaluation is rapidly maturing within Art History and Museology. Benchmarks like *VULCA-BENCH* and *Appear2Meaning* successfully integrate high-resolution visual art with complex textual critiques.
* **Underrepresented Modalities:** Audio is severely lacking. Only one paper (*Evaluating ASR for Holocaust Testimonies*) touches on audio processing (and does so via an ASR model, not a generative LLM). Evaluating musicology via raw audio or performing arts via video remains a massive blind spot.

### Task Types
* **The Dominance of MCQA:** Multiple-Choice Question Answering (MCQA) remains the default evaluation mechanism due to its ease of grading (e.g., *SuperGPQA*, *Humanity's Last Exam*).
* **Emergence of Generative Workflows:** There is a notable shift toward generative tasks. DH-specific benchmarks evaluate long-form generation (*LongFact*), structured data extraction (*RISE Humanities Data Benchmark*), and automated translation (*Al-Shamela Library*).
* **Agentic Reasoning:** A new frontier involves agentic tasks, where models must browse the web or perform multi-step archival research (*BrowseComp*, *DeepSearchQA*).

### Task-Domain Alignment
The alignment between AI tasks and actual humanities domain requirements is bifurcated:
1. **Superficial Alignment:** General benchmarks (like *MMLU* or *TriviaQA*) treat the humanities merely as a repository of static facts. 
2. **Deep Alignment:** Recently, researchers are designing benchmarks rooted in humanist methodologies. For example, *VULCA-BENCH* structures its evaluation around Panofsky’s iconological method (from visual description to philosophical interpretation); the *Hakka Cultural Knowledge Benchmark* utilizes Bloom's Taxonomy; and *RISE* evaluates Pydantic-schema XML outputs mirroring actual DH workflows.

---

## 3. Methodological Patterns

* **Dominant Models:** Across almost all recent papers (post-2023), OpenAI's GPT-4o, Anthropic's Claude 3.5 Sonnet, and Google's Gemini (1.5/2.0) are the de facto baselines. Open-weights models (Llama 3, Qwen 2.5) are increasingly tested, particularly for multilingual and low-resource tasks (*Persian LLMs*, *Belarusian*).
* **Evaluation Paradigms:** Because exact-match metrics (BLEU, ROUGE) are inadequate for the humanities, there is a widespread adoption of **LLM-as-a-judge**. To counteract the unreliability of AI judges, benchmarks are using rigorous human-in-the-loop validation, double-blind grading (*SimpleQA*), and calibrated rubric scoring (*VULCA-BENCH*).
* **Novel Metrics:** As tasks align closer to DH workflows, novel metrics have emerged. Examples include the *Historical Character Preservation Rate* (for measuring "over-historicization" in OCR), *Dimension Coverage Rate* (for art critique), and *Exact Match Ratio* for narrative framing.
* **Analytical Complexity:** There is a clear ceiling for current LLMs. While they easily master basic factual retrieval, they fail dramatically on tasks requiring deep reasoning. *Humanity's Last Exam* and *MMMU-Pro* demonstrate that when multiple-choice options are expanded or visual reasoning is required without text anchors, state-of-the-art models degrade to near-random performance. Furthermore, models struggle with negative transfer from high-resource languages when processing historical/low-resource dialects (*Lithuanian*, *Belarusian*, *18th-century Russian*).

---

## 4. Narrative Framing Options

Depending on the target audience of the survey paper, this corpus can be synthesized using one of three distinct narrative arcs:

### Option 1: For AI & ML Researchers – "The Humanities as the Ultimate Reasoning Frontier"
* **Emphasis:** Frame the Arts & Humanities not as "soft" subjects, but as the most rigorous stress tests for multimodal reasoning, ambiguity resolution, and constraint-solving.
* **Narrative:** ML models have conquered STEM benchmarks via logical determinism. However, humanities benchmarks (*VULCA-BENCH*, *Humanity's Last Exam*, *BrowseComp*) expose massive gaps in AI's ability to handle epistemic uncertainty, deep cultural context, and multi-layered symbolic reasoning. The humanities represent the next grand challenge for AGI.

### Option 2: For Digital Humanities Scholars – "From Parlor Tricks to Practical Workflows"
* **Emphasis:** Focus on utility, DH task-domain alignment, and the epistemic risks of automation.
* **Narrative:** Chart the evolution from AI treating the humanities as multiple-choice trivia (*MMLU*) to genuinely useful tools that integrate into DH pipelines (OCR correction, transcription, XML schema validation via *RISE* and *CzechTopic*). Critically evaluate the risks of deploying these models, emphasizing findings from *CHVM-1K* and *Global-MMLU* regarding Eurocentric biases, hallucinated historical artifacts, and "over-historicization."

### Option 3: For Newcomers – "The Three Waves of Humanities AI"
* **Emphasis:** A historical/chronological overview of AI capability development in cultural domains.
* **Narrative:** 
    * *Wave 1 (Representation):* Can models read the text? (*LAMBADA*, *TriviaQA*).
    * *Wave 2 (Knowledge):* Do models know the facts? (*MMLU*, *LongFact*).
    * *Wave 3 (Interpretation & Workflow):* Can models engage in aesthetic critique, multilingual historical archival research, and cultural reasoning? (*VULCA-BENCH*, *SuperGPQA*, *RISE*).

---

## 5. Gaps and Opportunities

Despite rapid advancements, several critical gaps remain in the current benchmarking landscape:

1. **Underrepresented Modalities (Audio & Video):** There are virtually no generative benchmarks for musicology (audio-in/audio-out), film studies (video interpretation), or the performing arts (dance choreography and theater).
2. **Missing Sub-Domains:** While History and Linguistics are well-covered, domains like Philosophy (specifically Ethics and Aesthetics, outside of basic logic), Archaeology, and advanced Literary Theory (e.g., deconstructionist critique) are largely absent.
3. **The "Generative Synthesis" Gap:** Current benchmarks heavily favor analytical breakdown (extraction, classification, multiple-choice). There is a gap in evaluating long-form, argumentative, synthetic writing. How well can an LLM act as a historian, reading three contradictory primary sources and writing a coherent historiographical essay?
4. **The "Next-Generation" Humanities Benchmark:** A future benchmark should be **Agentic and Interactive**. Instead of a static Q&A dataset, an AI would be given a simulated digital archive. The task: navigate the archive, cross-reference messy, un-transcribed historical documents in multiple languages, resolve entity deduplication, and produce a scholarly literature review with accurate citations.

---

## 6. Suggested Survey Structure

To effectively synthesize these findings for an academic journal, the following Table of Contents is proposed:

**Title: Beyond Trivia: A Survey of Large Language Model Benchmarks in the Arts and Humanities**

1. **Introduction**
    * The shift from general capabilities to domain-expert reasoning.
    * Defining the scope (ASJC Arts & Humanities areas).
2. **The Evolution of the Humanities Benchmark**
    * *Phase 1:* Humanities as General Knowledge (MMLU, TriviaQA)
    * *Phase 2:* Domain-Specific Competencies (C-Eval, SuperGPQA)
    * *Phase 3:* Methodological Alignment (Integrating Panofsky, Bloom, and DH workflows)
3. **Modality and Task Landscape**
    * *Textual Processing:* Philology, translation, and historical OCR (RISE, EvaHan2024).
    * *Multimodal Interpretation:* Visual arts, iconography, and cultural metadata (VULCA-BENCH, MMMU-Pro).
    * *The Missing Modalities:* Audio, musicology, and the performing arts.
4. **Evaluating DH Workflows: Practical Applications**
    * Automated transcription and post-OCR correction.
    * Archival search, structured metadata extraction, and agentic reasoning (DeepSearchQA).
5. **Epistemology, Bias, and Cultural Representation**
    * The Western-centric bias in translated benchmarks (Global-MMLU).
    * Value alignment and representation in cultural heritage (CHVM-1K, SEA-HELM).
6. **Methodological Challenges in Evaluation**
    * The limits of Multiple-Choice Question Answering.
    * The rise and risks of LLM-as-a-judge for subjective humanities evaluations.
7. **Gaps and Future Directions**
    * Pushing toward multi-document synthesis and historiography.
    * The need for interactive, archive-based agentic benchmarks.
8. **Conclusion**