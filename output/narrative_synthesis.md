# Survey Narrative Synthesis

Here is a comprehensive narrative synthesis document designed for an academic survey paper on AI benchmarking in the digital humanities.

***

# Evaluating AI in the Humanities: A Synthesis of Current Benchmarks, Methodologies, and Gaps

## 1. Thematic Clusters

The recent explosion of humanities-centric LLM benchmarking can be taxonomized into five distinct thematic clusters. These clusters reveal a bifurcation between benchmarks that use humanities texts merely as "content" to test general NLP capabilities, and those that evaluate deep "domain" competence in humanistic methodologies.

### Cluster 1: Encyclopedic Knowledge & General Academic Reasoning
* **Papers**: MMLU, Global-MMLU, MMLU-ProX, SuperGPQA, Humanity's Last Exam (HLE), HiST-LLM, LongFact, SimpleQA, FActScore, M3Exam.
* **Common Thread**: These benchmarks treat humanities as a repository of declarative facts. Predominantly text-only, they focus heavily on **factual recall** and **multiple-choice QA**. They aim to establish the baseline encyclopedic knowledge of frontier models (often pitting STEM vs. Humanities subjects) rather than requiring domain-specific hermeneutic methodologies.

### Cluster 2: Visual Heritage & Art Historical Critique
* **Papers**: VQArt-Bench, VULCA-BENCH (x2), Christian Iconography, EduArt, Appear2Meaning, Hanfu-Bench, MMMU-Pro.
* **Common Thread**: Grounded in **Visual Arts**, **History**, and **Museology**, this cluster tests multimodal VLMs (image+text) on visual recognition, stylistic analysis, and aesthetic interpretation. The best benchmarks here (like VULCA-BENCH and Appear2Meaning) evaluate true disciplinary competence, requiring models to move beyond surface-level image description to infer latent cultural metadata (attribution) and apply art-theoretical frameworks (e.g., Panofsky’s iconology).

### Cluster 3: Cultural Nuance, Localization, and Multilingualism
* **Papers**: CulturalBench, MILU, CaLMQA, CulturALL, DRISHTIKON, C3B, MultiNRC.
* **Common Thread**: Operating primarily in **Cultural Studies**, **Anthropology**, and **Language/Linguistics**, these benchmarks expose the Western-centric biases of current LLMs. By testing localized traditions, regional norms, and cross-cultural reasoning in low-resource languages, they challenge models with **cultural reasoning** and **normative judgment**.

### Cluster 4: Archival Processing & Historical Document Analysis
* **Papers**: HistBench, The RISE Humanities Data Benchmark, OfficeQA Pro, CzechTopic, Historical Document OCR (Russian Civil Font), Post-OCR Correction (Historical Newspapers), DeepSearchQA, BrowseComp.
* **Common Thread**: These benchmarks focus on the gritty realities of digital humanities research: parsing complex, noisy, historical artifacts. Tasks blend **transcription/OCR**, **information extraction**, and **agentic tool use**. They evaluate whether models or autonomous agents can persistently search archives, resolve temporal historical constraints, and reconstruct degraded texts.

### Cluster 5: Linguistic Stylistics, Rhetoric, and Philology
* **Papers**: AdMIRe, JOKER 2025 (Puns), PSH v1.0 (Parole Hearings), Swedish Petitions (Rhetorical Structure), LLM-based MT for Latin, Text Is Not All You Need (Humor/Audio), Al-Shamela Translation.
* **Common Thread**: Focused on **Language, Linguistics, and Classics**, this cluster probes the limits of semantic representation. Tasks involve **translation**, **stylistic analysis**, and **interpretation** of non-literal language (idioms, wordplay, rhetorical impersonation). They prove that while LLMs generate fluent text, they struggle to capture distinct human stylistic fingerprints or untangle deep phonetic/semantic ambiguities.

---

## 2. Modality & Task Landscape

### Modality Coverage
* **Dominance of Text**: Text remains the bedrock of AI benchmarking. Even in multimodal exams, text often does the heavy lifting via multiple-choice framing. 
* **Rapid Rise of Vision**: The integration of Image + Text has matured significantly, driven by VLMs. Benchmarks now routinely test complex visual layouts (OfficeQA Pro), historical manuscripts (RISE), and fine arts (EduArt, VQArt-Bench).
* **The Missing Senses**: **Audio and Video are severely underrepresented.** Out of this corpus, only *HistBench* includes video/audio (oral histories, documentary clips), and only the humor benchmark (*Text Is Not All You Need*) leverages audio to provide phonetic cues for puns.

### Task Types
* **Dominant Tasks**: **Factual Recall** and **Multiple-Choice QA** still heavily dominate the landscape due to their ease of automated evaluation. 
* **Emerging Paradigms**: There is a notable shift toward **Generation** evaluated by LLM-as-a-judge frameworks (VULCA-BENCH, FActScore), and **Agentic Tool Use**. Benchmarks like *HistBench*, *BrowseComp*, and *DeepSearchQA* require models to behave like researchers—initiating web searches, writing Python scripts, and recursively digging through archives to synthesize historical answers.

### Task-Domain Alignment
A critical tension exists in how well tasks map to actual humanistic inquiry. 
* **Misaligned (Content Role)**: Many datasets (e.g., SimpleQA, LongFact, CzechTopic) use historical or cultural data merely as challenging fodder to test general reasoning or extraction capabilities.
* **Highly Aligned (Domain Role)**: A new wave of benchmarks specifically formalizes disciplinary methodologies. *VULCA-BENCH* requires layered art critique; *HistBench* requires source criticism and dating; *Appear2Meaning* tests museological cataloging. These demonstrate high task-domain alignment, pushing AI beyond trivia into genuine scholarly analysis.

---

## 3. Methodological Patterns

* **Evaluation Paradigms**: While exact-match accuracy remains standard for multiple-choice and OCR, **LLM-as-a-Judge** (using GPT-4o or Claude) has become the de facto standard for evaluating free-text generation, translation, and cultural critique. 
* **Standard vs. Novel Metrics**: Standard metrics (Accuracy, F1, BLEU, CER) are being supplemented by highly creative, domain-specific metrics. Examples include *FActScore* (atomic fact verification), *Historical Character Preservation Rate* (historical OCR), and *Dimension Coverage Rate* (art critique depth).
* **Models Tested**: OpenAI (GPT-4o, o1, o3), Anthropic (Claude 3.5/4.5), and Google (Gemini 1.5/2.0 Pro) form the proprietary baseline. Among open weights, DeepSeek (V3/R1), Qwen (especially Qwen2.5-VL for vision), and Llama 3 are ubiquitous.
* **Analytical Complexity**: Complexity ranges from basic **L1 surface perception** (OCR transcription, literal translation) to **L5 interpretative synthesis** (multi-hop causal reasoning in *HistBench*, multi-step financial/historical math in *OfficeQA Pro*, and philosophical aesthetic critique in *VULCA-BENCH*). Current models perform at ceiling on L1/L2 but degrade drastically on L4/L5 tasks.

---

## 4. Narrative Framing Options for a Survey Paper

Depending on the target venue, this survey could be framed in three distinct ways:

### Option 1: For Newcomers (Interdisciplinary Researchers & Students)
**Title Concept: "The Turing Test Meets the Humanities: What AI Can and Cannot Read."**
* **Framing**: An accessible overview distinguishing between AI as a *tool* (OCR, translation, data extraction) and AI as an *analyst* (critique, cultural reasoning). 
* **Emphasis**: Focus on the shift from factual trivia (MMLU) to multimodal and cultural benchmarks. Highlight clear, practical boundaries: models can accurately transcribe a 19th-century newspaper, but they fail to grasp localized cultural conflict (C3B) or native idioms (MultiNRC).

### Option 2: For Experts (Digital Humanities Scholars)
**Title Concept: "From Distant Reading to Agentic Assistants: Benchmarking Disciplinary Competence in AI."**
* **Framing**: A critical, methodologically rigorous review of how AI benchmarks map to humanistic epistemology. 
* **Emphasis**: Focus on the *Domain vs. Content* divide. Critique multiple-choice formats as insufficient for hermeneutic disciplines. Spotlight "next-gen" DH benchmarks like *HistBench* (source criticism agents) and *Appear2Meaning* (latent cultural attribution) that align closely with professional archival and cataloging methodologies.

### Option 3: For AI & ML Researchers
**Title Concept: "Beyond Math and Code: The Hermeneutic Frontier for Reasoning Models."**
* **Framing**: Presenting the Humanities as the ultimate stress test for AGI, characterized by high ambiguity, epistemic uncertainty, and rich cultural context.
* **Emphasis**: Highlight the failures of current frontier models (including OpenAI o1/o3 and DeepSeek-R1) on subjective, multi-modal, and culturally localized reasoning (e.g., *SuperGPQA*, *Humanity's Last Exam*, *Hanfu-Bench*). Focus on agentic workflows and the necessity of improved calibration and uncertainty quantification when models face ambiguous historical data.

---

## 5. Gaps and Opportunities

While the landscape is maturing, several critical gaps remain:
* **Underrepresented Modalities**: The near-total absence of audio and video benchmarks is glaring. Fields like ethnomusicology, film and media studies, oral history, and performing arts (dance, theater) are effectively un-benchmarked. 3D spatial reasoning (crucial for archaeology and architecture) is also entirely missing.
* **Missing ASJC Areas**: **Literature and Literary Theory** is surprisingly underrepresented beyond basic linguistic stylistics. There are no benchmarks rigorously testing long-context literary criticism (e.g., tracking a thematic motif across a 500-page novel). **Musicology** and **Philosophy** (beyond basic ethics) are also sidelined.
* **Gaps in Task Complexity**: We lack benchmarks that evaluate true *synthetic argumentation*. Current tests evaluate whether a model can retrieve a fact or generate a descriptive critique, but not whether it can write a coherent, multi-page scholarly essay citing primary and secondary sources with valid historical methodologies.
* **The "Next-Generation" Humanities Benchmark**: The future lies in **Agentic Peer-Review Environments**. A next-gen benchmark would provide a model with raw archival data (images, audio, untranscribed text), ask an open-ended research question, and evaluate the model's multi-step research loop, source citation accuracy, and defense of a novel subjective thesis against an LLM-simulated academic reviewer.

---

## 6. Suggested Survey Structure

**Title: Benchmarking AI in the Digital Humanities: A Survey of Modalities, Tasks, and Epistemological Gaps**

1. **Introduction**
   * The evolution from general NLP to humanities-specific benchmarking.
   * The "Content" vs. "Domain" distinction in evaluating AI.
2. **The Modality Landscape**
   * *Textual Foundations*: Encyclopedic Knowledge, Translation, and Stylistics.
   * *The Visual Turn*: Art History, Museology, and Historical Document processing.
   * *The Multimodal Frontier*: Identifying gaps in Audio, Video, and Spatial analysis.
3. **Taxonomy of Analytical Tasks**
   * *Surface Perception*: OCR, HTR, and Visual Feature Recognition.
   * *Retrieval & Reasoning*: Factual Recall, Multiple-Choice QA, and Cross-cultural logic.
   * *Interpretative Generation*: Art Critique, Rhetorical Analysis, and Disciplinary Hermeneutics.
   * *The Rise of the Agent*: Multi-step search, tool use, and archival navigation.
4. **Methodological Trends & Evaluation Metrics**
   * The shift from classic metrics (Accuracy, BLEU) to LLM-as-a-Judge and domain-customized metrics (e.g., Dimension Coverage Rate, Historical Character Preservation Rate).
   * The limitations of current Reasoning (System 2) models in subjective cultural tasks.
5. **Cultural Representation & Western Biases**
   * Analysis of localization, multilingualism, and cultural reasoning benchmarks (e.g., CulturalBench, CaLMQA).
6. **Open Challenges and Future Directions**
   * Overcoming the multiple-choice bottleneck.
   * Incorporating time, sound, and moving images (Film Studies, Musicology).
   * Vision for "Next-Generation" agentic DH benchmarking.
7. **Conclusion**