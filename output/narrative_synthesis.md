# Survey Narrative Synthesis

# Benchmarking Large Language Models in the Arts and Humanities: A Narrative Synthesis and Survey Framework

## 1. Thematic Clusters

To synthesize the diverse landscape of AI benchmarking within the Arts and Humanities, the analyzed corpus of 38 benchmarks can be grouped into six distinct thematic clusters. These clusters cross-reference All Science Journal Classification (ASJC) subject areas, multimodal configurations, and analytical task complexities to map out the current boundaries of machine intelligence in humanistic domains.

```
       ┌────────────────────────────────────────────────────────┐
       │             HUMANITIES BENCHMARK LANDSCAPE             │
       └───────────────────────────┬────────────────────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         ▼                         ▼                         ▼
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│     HISTORY     │       │    PHILOLOGY    │       │  MULTICULTURAL  │
│   & ARCHIVES    │       │  & LINGUISTICS  │       │   & REGIONAL    │
│  (Cluster A)    │       │  (Cluster B)    │       │  (Cluster C)    │
└─────────────────┘       └─────────────────┘       └─────────────────┘
         ▲                         ▲                         ▲
         └─────────────────────────┼─────────────────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         ▼                         ▼                         ▼
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   VISUAL ART    │       │  LITERATURE &   │       │   MUSEOLOGY &   │
│  & AESTHETICS   │       │    NARRATIVE    │       │  ETHICAL CH     │
│  (Cluster D)    │       │  (Cluster E)    │       │  (Cluster F)    │
└─────────────────┘       └─────────────────┘       └─────────────────┘
```

### Cluster A: Global History, Archival Exploration, and Quantitative Historiography
*   **Included Papers:** *HiST-LLM* (2024), *DeepSearchQA* (2026), *BrowseComp* (2025), *C-Eval* (2023), *SuperGPQA* (2025), *FActScore* (2023), *LongFact* (2024), *SimpleQA* (2024).
*   **Common Thread:** This cluster centers on factual historical retrieval, multi-hop chronological reasoning, and open-web agentic exploration. Rather than treating history merely as static trivia, these benchmarks evaluate an AI's capacity to navigate complex archival constraints, reconcile conflicting records, and verify biographical details of historical figures. 
*   **ASJC Alignment:** History, Archaeology, History and Philosophy of Science.
*   **Modality:** Text-only (primarily), with emerging agentic web-browsing capabilities.
*   **Task Depth:** Ranging from closed-ended factual verification (*FActScore*, *SimpleQA*) to complex, multi-constraint search and synthesis across unstructured digital archives (*DeepSearchQA*, *BrowseComp*).

### Cluster B: Classical Philology, Historical Linguistics, and Diplomatic Document Digitization
*   **Included Papers:** *Evaluating LLMs for Historical Document OCR* (2025), *Overview of EvaHan2024* (2024), *LLM-based Machine Translation and Summarization for Latin* (2024), *Nostra Domina at EvaLatin 2024* (2024), *Leveraging LLMs for Post-OCR Correction of Historical Newspapers* (2024), *The RISE Humanities Data Benchmark* (2026), *CzechTopic* (2026).
*   **Common Thread:** These papers address the core technical workflows of digital humanities (DH) projects: converting physical archives into clean, structured, and translated digital assets. The common challenge is handling highly degraded primary source texts (such as OCR-damaged 19th-century newspapers, medieval Latin correspondence, or raw classical Chinese characters) while preserving historical orthography and avoiding modernizing hallucinations.
*   **ASJC Alignment:** Classics, Language and Linguistics, History, Literature and Literary Theory.
*   **Modality:** Text-only and Multimodal (Image-to-Text).
*   **Task Depth:** Character-level recognition, spelling and layout normalization, sentence segmentation, and morphological/syntactic preservation under deep historical constraints.

### Cluster C: Multicultural, Multilingual, and Region-Specific Competency Evaluation
*   **Included Papers:** *MILU* (2024), *GMMLU* (2025), *SEA-HELM* (2025), *Taiwanese Hakka Cultural Knowledge Benchmark* (2024), *Benchmarking Open-Source LLMs for Persian* (2024), *Tracking the evolution of LLM capabilities for Belarusian with OpenAI Evals* (2026), *Evaluating Large Language Models on Lithuanian Grammatical Cases* (2026).
*   **Common Thread:** This cluster confronts the inherent Eurocentrism and English-language bias of baseline LLMs. These benchmarks assess how models handle regional histories, localized social customs, non-Western religions, and highly complex morphological features of low-resource or non-globalized languages (e.g., Belarusian *Taraškievica* orthography, Lithuanian case markings, and Southeast Asian linguistic nuances).
*   **ASJC Alignment:** Language and Linguistics, Literature and Literary Theory, History, Philosophy, Religious Studies.
*   **Modality:** Text-only.
*   **Task Depth:** Cross-lingual retrieval, cultural commonsense reasoning, dialectal acceptability judgments, and grammatical case-marking classification.

### Cluster D: Visual Art History, Iconography, and Cross-Cultural Aesthetic Interpretation
*   **Included Papers:** *VULCA-BENCH* (2026), *Christian Iconography* (2025), *VQArt-Bench* (2025), *Appear2Meaning* (2026).
*   **Common Thread:** Moving beyond basic object detection, this cluster benchmarks Vision-Language Models (VLMs) on their ability to interpret visual art. The unifying theme is the decoding of "unobservable" cultural attributes—identifying visual metaphors, mapping complex iconographic schemas (e.g., Christian saint symbols or *yijing* in Chinese paintings), and generating structured, expert-level aesthetic critiques across global artistic traditions.
*   **ASJC Alignment:** Visual Arts and Performing Arts, History, Philosophy, Religious Studies.
*   **Modality:** Multimodal (Image-to-Text).
*   **Task Depth:** Zero-shot stylistic classification, spatial and attribute-interaction reasoning, iconological analysis, and structured metadata inference (JSON mapping).

### Cluster E: Literary Analysis, Computational Poetics, and Narrative Representation
*   **Included Papers:** *SemEval-2025 Task 10: Multilingual Characterization and Extraction of Narratives* (2025), *AdMIRe* (2025), *Exploring Aspect-Based Sentiment Analysis for Literary-Historical Research (Travelogues ABSA)* (2024), *JOKER Task 1* (2025), *Exploring the Limits of Prompting LLMs with Speaker-Specific Rhetorical Fingerprints (PSH v1.0)* (2025), *GDPval-AA* (2025).
*   **Common Thread:** This cluster focuses on the abstract and metaphorical layers of human expression. The papers evaluate models on their capacity to process non-literal language (such as idioms, puns, and rhetorical figures), extract literary-historical themes (environmental aspects in historical travelogues), map narrative archetypes (martyrs, tyrants, and saboteurs in media), and mimic individual human stylistic profiles.
*   **ASJC Alignment:** Literature and Literary Theory, Language and Linguistics, Visual Arts and Performing Arts.
*   **Modality:** Text-only and Multimodal (sequential image-text narratives).
*   **Task Depth:** Non-literal figurative representation, aspect-based sentiment polarity mapping, rhetorical stylistic control, and multi-layered narrative framing.

### Cluster F: Library Science, Museology, and Cultural Heritage Ethics
*   **Included Papers:** *LLMs4Subjects* (2025), *CHVM-1K* (2024).
*   **Common Thread:** This cluster addresses the institutional structures of cultural heritage. It evaluates how LLMs organize metadata within standardized taxonomies (such as the German Integrated Authority File - GND) and looks at the ethical implications of using AI to generate narratives for museum visitors, focusing on historical bias, value alignment, and the misrepresentation of marginalized heritage.
*   **ASJC Alignment:** Museology, Conservation, History, Visual Arts and Performing Arts.
*   **Modality:** Text-only.
*   **Task Depth:** Extreme multi-label subject tagging, semantic taxonomy mapping, and cultural value alignment/ethical risk profiling.

*(Note: The benchmark "OfficeQA Pro" (2026) has been excluded from these primary humanities clusters as its core data corpus (U.S. Treasury Bulletins) and analytical tasks (inflation-adjusted financial reconciliation and OLS regression) align with Economics and Finance rather than Arts and Humanities.)*

---

## 2. Modality & Task Landscape

An analysis of the corpus reveals a clear divide in modality coverage, task distributions, and how well these benchmarks align with the actual requirements of humanities research.

```
       MODALITY DISTRIBUTION                  TASK TYPE DOMINANCE
  ┌──────────────────────────────┐       ┌──────────────────────────────┐
  │ ████████████████████  73%    │       │ ████████████████    55%      │
  │ Text-Only                    │       │ Closed MCQ & QA              │
  ├──────────────────────────────┤       ├──────────────────────────────┤
  │ █████  19%                   │       │ ████████  25%                │
  │ Multimodal Image+Text        │       │ Extraction & Normalization   │
  ├──────────────────────────────┤       ├──────────────────────────────┤
  │ █  8%                        │       │ ████  15%                    │
  │ Multi-Doc / Spreadsheet / Agent│     │ Agentic Web & Multi-Hop      │
  └──────────────────────────────┘       ├──────────────────────────────┤
                                         │ █  5%                        │
                                         │ Open-Ended Critique & Theory │
                                         └──────────────────────────────┘
```

### Modality Coverage: Text-Only Dominance vs. Multi-Modal Gaps
*   **Text-Only Dominance:** Roughly 73% of the analyzed benchmarks operate strictly in the text-only domain. While highly effective for linguistic analysis, parsing translations, and evaluating factual recall, this setup fails to capture the multi-sensory and physical reality of humanities materials.
*   **Multimodal (Image + Text):** Approximately 19% of the benchmarks (*MMMU-Pro*, *VULCA-BENCH*, *The RISE Benchmark*, *Appear2Meaning*, *Historical Document OCR*, *Christian Iconography*, *VQArt-Bench*) pair images with text. These are highly concentrated in **Visual Art History** (decoding styles and iconology) and **Digital Humanities Digitization** (converting scanned pages/manuscripts into text).
*   **The Unrepresented Modalities:** There is a major lack of audio, video, and physical material modalities in these benchmarks. Despite *GDPval-AA* introducing basic multi-format task routing, there are zero dedicated benchmarks evaluating **Musicology** through raw audio, **Performative Arts** through video, or **Conservation/Archaeology** through 3D spatial or material data. Music evaluation remains limited to sheet-music OCR (*MMMU-Pro*) or text-only musicology trivia (*SuperGPQA*).

### Task Types: From Trivia to Agentic Inquiry
The analytical tasks embedded in the benchmarks show a clear evolutionary progression:

1.  **Fact-Seeking & Closed MCQ (High Volume):** Legacy and general-purpose benchmarks (*C-Eval*, *SuperGPQA*, *MILU*, *GMMLU*) rely on multiple-choice questions. While easy to grade, they treat the humanities as a static collection of facts, overlooking the interpretation and debate that define the field.
2.  **Structural Extraction & Normalization (Workflow-Aligned):** Benchmarks like *EvaHan2024*, *LLMs4Subjects*, *CzechTopic*, and *Historical Document OCR* evaluate actual research tasks: segmenting raw historical text, tagging library records, and correcting transcription errors.
3.  **Agentic Multi-Step Research (Emerging):** Benchmarks like *BrowseComp* and *DeepSearchQA* evaluate an model's ability to act as an autonomous researcher. These tasks require models to query search engines, resolve naming discrepancies across sources, and decide when they have gathered enough evidence to stop.
4.  **Generative Interpretation & Theory (Rare but Crucial):** *VULCA-BENCH* represents the highest level of task complexity. It requires models to generate structured, paragraph-length critiques evaluated against qualitative, theoretical frameworks (like Panofsky’s Iconological Method).

### Task-Domain Alignment: Reality vs. Proxy Evaluations
The alignment between benchmark tasks and the actual research methods of humanities scholars varies significantly:

*   **High Alignment (Methodologically Authentic):** Benchmarks designed in collaboration with digital humanists and domain experts show excellent alignment. For example, *VULCA-BENCH* uses a five-tier interpretative hierarchy that mirrors actual art-historical training. Similarly, *Evaluating LLMs for Historical Document OCR* introduces metrics like the Historical Character Preservation Rate (HCPR) and Archaic Insertion Rate (AIR). These metrics are highly relevant to philologists, as they flag "over-historicization" errors (such as models incorrectly inserting obsolete characters into texts).
*   **Low Alignment (Superficial Proxies):** Many general-purpose benchmarks use simplistic proxies. For instance, using sentiment analysis on Latin poetry (*EvaLatin*) or travelogues (*Travelogues ABSA*) simplifies complex literary works into basic positive/negative scores. This approach ignores the layered meanings, irony, and historical context that literary scholars actually study.

---

## 3. Methodological Patterns

```
┌────────────────────────────────────────────────────────────────────────┐
│                        METHODOLOGICAL TRENDS                           │
├───────────────────────────────────┬────────────────────────────────────┤
│ EVALUATION STRATEGIES             │ MODEL TESTING COHORTS              │
│ • Shift to LLM-as-a-Judge         │ • Proprietary: GPT-5, GPT-4o,      │
│   (e.g., SAFE agent, Sigmoid-     │   Claude 4.5 Sonnet, Gemini 2.5    │
│   calibrated metrics in VULCA)    │ • Open-Weights: Llama 4, Qwen 3,   │
│ • Verification against ground-    │   DeepSeek-R1, specialized models  │
│   truth Pydantic schemas (RISE)   │   (Xunzi, EuroLLM)                 │
├───────────────────────────────────┴────────────────────────────────────┤
│ METRICS MATRIX                                                         │
│ • Standard: F1-score, BLEU, Character Error Rate (CER)                 │
│   Novel: Archaic Insertion Rate (AIR), Dimension Coverage (DCR)        │
└────────────────────────────────────────────────────────────────────────┘
```

### Evaluation Strategies: The Rise of Hybrid and Agentic Judges
The evaluation of humanities benchmarks has shifted away from simple string matching:
*   **LLM-as-a-Judge with Expert Calibration:** For open-ended generative tasks like art criticism or historical synthesis, benchmarks now use advanced models as judges, calibrated against human evaluations. For example, *VULCA-BENCH* uses sigmoid-calibrated scores validated against expert ratings using the Intraclass Correlation Coefficient (ICC).
*   **Search-Augmented Agentic Evaluators:** *LongFact* uses the SAFE (Search-Augmented Factuality Evaluator) pipeline. SAFE utilizes an LLM to break responses down into individual atomic facts, which it then verifies by systematically querying Google Search. This approach replaces static answer keys with live, external verification.
*   **Schema-Enforced Pydantic Verification:** *The RISE Benchmark* enforces structured JSON outputs using Pydantic schemas. This allows evaluations to run fuzzy string matching and schema-conformance checks, making it much easier to automate the grading of complex data-extraction tasks.

### Tested Models: Proprietary Frontiers vs. Specialized Open-Weights
The benchmarking papers consistently test two tiers of models:
*   **The Proprietary Frontier:** Evaluated across almost all benchmarks are OpenAI's GPT-4o/o1/o3-mini/GPT-5 series, Anthropic's Claude 3.5/3.7/4.5 Sonnet & Opus, and Google's Gemini 1.5/2.0/2.5 Pro. These models set the performance ceilings, especially in reasoning-heavy tasks (*HLE*, *BrowseComp*, *SuperGPQA*).
*   **The Open-Weights Alternatives:** Llama 3/3.1/3.2/4, Qwen 2.5/3, and DeepSeek-R1 are frequently tested. While they perform well, they often require task-specific fine-tuning to match proprietary models.
*   **Domain-Specific and Regional Models:** Benchmarks like *EvaHan2024* evaluate specialized models like *XunziALLM* (for ancient Chinese). Similarly, *Evaluating LLMs on Lithuanian Grammatical Cases* tests regional models like *EuroLLM* and *Neurotechnology LLM*, showing that regional pre-training can sometimes outperform pure model scale.

### Metrics: Standard NLP vs. Novel Humanities Analytics
To capture the nuances of humanities data, researchers are moving beyond generic NLP metrics:

| Metric Category | Metric Name | Definition / Use Case | Benchmark |
| :--- | :--- | :--- | :--- |
| **Standard** | CER / WER | Character/Word Error Rate for transcribing historical texts. | *Historical OCR*, *RISE* |
| **Standard** | Exact Match | Demands 100% character agreement on highly challenging questions. | *HLE*, *SimpleQA* |
| **Novel** | **AIR** (Archaic Insertion Rate) | Measures how often a model hallucinates obsolete characters (e.g., pre-Petrine Russian). | *Historical OCR* |
| **Novel** | **HCPR** (Historical Character Preservation Rate) | Measures a model's accuracy in retaining legitimate historical orthography. | *Historical OCR* |
| **Novel** | **DCR** (Dimension Coverage Rate) | Measures how thoroughly an art critique covers cultural, historical, and aesthetic dimensions. | *VULCA-BENCH* |
| **Novel** | **F1@K** | Balances factual precision with preferred length constraints in long-form generation. | *LongFact* |

---

## 4. Narrative Framing Options

To present a comprehensive survey of these benchmarks in an academic paper, the synthesis can be structured using one of three alternative narrative framings. Each framing targets a different audience and highlights different aspects of the corpus.

### Framing 1: For Newcomers (The Pragmatic Workflow Approach)
*   **Title:** *Automating the Archive: A Practical Guide to AI Benchmarks for Digital Humanities Workflows*
*   **Core Theme:** This framing positions LLMs as powerful assistants for digital humanities. It focuses on practical applications, showing how models can automate tedious, manual tasks like transcription, cataloging, and metadata organization.
*   **Emphasized Areas:** Cluster B (Philology/Digitization) and Cluster F (Library Science).
*   **Key Benchmarks:** *Historical Document OCR*, *The RISE Benchmark*, *LLMs4Subjects*, *EvaHan2024*.
*   **Analytical Task Complexity:** Low to Medium. It highlights how models handle structured character recognition, spelling correction, and automatic subject tagging, showing newcomers how these tools can speed up their archival research.

```
PRAGMATIC DH WORKFLOW (FRAMING 1)
[Analog Archive] ──► [Historical OCR] ──► [RISE Schema Mapping] ──► [LLMs4Subjects Cataloging] ──► [Clean Research Dataset]
```

---

### Framing 2: For DH Experts (The Epistemological Critique)
*   **Title:** *Beyond Retrieval: Epistemological Limits and Cultural Bias in Large Language Model Evaluations*
*   **Core Theme:** This framing takes a critical look at AI through a humanities lens. It argues that while LLMs are excellent at retrieving facts, they struggle with the interpretive, cultural, and philosophical analysis that defines advanced humanities research. It also addresses how Western bias is embedded in standard benchmarks.
*   **Emphasized Areas:** Cluster D (Visual Arts/Aesthetics), Cluster C (Multicultural Competency), and Cluster E (Literary Analysis).
*   **Key Benchmarks:** *VULCA-BENCH*, *GMMLU*, *Humanity's Last Exam*, *Appear2Meaning*, *CHVM-1K*.
*   **Analytical Task Complexity:** High. It focuses on the drop-off in model performance when moving from surface-level descriptions to deep symbolic, cultural, and ethical interpretations. It highlights how models rely on Eurocentric assumptions and struggle with non-Western traditions.

```
EPISTEMOLOGICAL BREAKDOWN (FRAMING 2)
[Surface Perception (L1-L2)]  ───► OK (Gemini 2.5 / GPT-4o score > 85%)
[Symbolic Decoding (L3)]      ───► WEAK (Loss of contextual nuance)
[Philosophical Aesthetics (L5)] ──► FAILURE (Systemic Western stylistic shortcuts & hallucination)
```

---

### Framing 3: For AI Researchers (The Hard Reasoning Frontier)
*   **Title:** *The Humanities as the Ultimate Frontier for AI: Evaluating Agentic Reasoning, Cultural Competence, and Multi-Modal Interpretation*
*   **Core Theme:** This framing targets machine learning researchers, arguing that humanities tasks are the ultimate test for frontier models. As standard STEM benchmarks become saturated, the nuance, ambiguity, and cultural variation of the humanities offer the best environment for testing advanced reasoning and agentic search.
*   **Emphasized Areas:** Cluster A (Quantitative Historiography) and Cluster E (Computational Poetics/Idiomaticity).
*   **Key Benchmarks:** *BrowseComp*, *DeepSearchQA*, *SuperGPQA*, *AdMIRe*, *Humanity's Last Exam*.
*   **Analytical Task Complexity:** Extreme. It highlights tasks that stump even the most advanced models (like *o3-mini* or *DeepSeek-R1*), such as multi-hop web searches under complex constraints (*BrowseComp*) and decoding non-literal figurative language (*AdMIRe*).

```
HARD REASONING PATHWAY (FRAMING 3)
[Complex Constraint] ──► [Multi-Hop Web Search] ──► [Entity Resolution Across Archives] ──► [Dynamic Stopping Choice]
                                                                                                    (BrowseComp / DeepSearchQA)
```

---

## 5. Gaps and Opportunities

An analysis of the current benchmark landscape highlights several gaps that present opportunities for future research.

```
       CURRENT BENCHMARKS                             NEXT-GENERATION BENCHMARK
┌──────────────────────────────┐              ┌──────────────────────────────┐
│ • Static Factual Trivia      │              │ • Multimodal Document Pack   │
│ • Text-Dominant Inputs       │   ════──────►│ • Dynamic Retrieval & Agents │
│ • Western-Centric Focus      │              │ • Scholarly Argument Gen     │
│ • Closed-Form Multiple-Choice│              │ • Interactive Audio & Vision │
└──────────────────────────────┘              └──────────────────────────────┘
```

### 1. Modality and Domain Gaps
*   **The Silence of Audio and Musicology:** There is a major lack of raw audio benchmarks. While *MMMU-Pro* includes sheet music, it treats it as a visual parsing task rather than evaluating musical reasoning. There are no benchmarks evaluating an AI's ability to analyze audio elements like performance styles, oral histories, regional dialects, or ethnomusicological recordings.
*   **Neglect of Material Culture and Conservation:** There are no benchmarks for physical materials, archaeological stratigraphy, or 3D object conservation. This leaves a massive gap in testing AI for museum conservation and archaeological site analysis.

### 2. Analytical and Task Complexity Gaps
*   **Factual Trivia vs. Historical Hermeneutics:** Many history benchmarks (*HiST-LLM*, *C-Eval*, *SimpleQA*) treat history as a series of indisputable facts. They fail to evaluate **historical reasoning**—the ability to analyze conflicting primary sources, identify bias in historical accounts, and construct persuasive historical arguments.
*   **Literalism and the Figuration Gap:** While benchmarks like *AdMIRe* and *JOKER* evaluate figurative language, they rarely test high-level literary interpretation. Models are rarely evaluated on their ability to analyze complex allegories, trace literary influences across centuries, or perform close readings of dense poetry.

### 3. Cultural Symmetry and Language Bias
*   **The "Translated Western Bias" Loop:** As *GMMLU* and *VULCA-BENCH* demonstrate, many multilingual benchmarks are simply translations of Western-centric questions. This distorts our evaluation of multilingual models, as they are tested on Western concepts translated into local languages rather than the regional histories and customs of those cultures.

### Defining a Next-Generation Benchmark: *Hermeneutic-Agent-Bench*
To address these gaps, a next-generation humanities benchmark must move beyond simple multiple-choice questions. It should evaluate an AI's ability to perform actual, scholarly inquiry.

```
                       HERMENEUTIC-AGENT-BENCH PIPELINE
                       
             ┌──────────────────────────────────────────────────┐
             │                 MULTIMODAL INPUT                 │
             │   Scanned Manuscript (Classics/Latin Image)      │
             │   Oral History Interview (Socio-Dialect Audio)   │
             │   Conflicting Archival Records (Unstructured)    │
             └────────────────────────┬─────────────────────────┘
                                      │
                                      ▼
             ┌──────────────────────────────────────────────────┐
             │                 AGENTIC WORKFLOW                 │
             │   1. Transcribe & correct raw text/audio         │
             │   2. Query external open-web historic catalogs   │
             │   3. Resolve conflicting dates & names           │
             └────────────────────────┬─────────────────────────┘
                                      │
                                      ▼
             ┌──────────────────────────────────────────────────┐
             │                 SYNTHESIS OUTPUT                 │
             │   Generate a structured, peer-reviewed-quality   │
             │   argument complete with verified citations.     │
             └────────────────────────┬─────────────────────────┘
                                      │
                                      ▼
             ┌──────────────────────────────────────────────────┐
             │                EVALUATION METRIC                 │
             │   Graded via a multi-model consensus judge       │
             │   enforcing logical consistency and factual      │
             │   grounding (eliminating hallucinations).        │
             └──────────────────────────────────────────────────┘
```

---

## 6. Suggested Survey Structure

To organize these findings into a comprehensive, publishable survey paper, the following Table of Contents is proposed:

### Table of Contents

#### 1. Introduction and Scope
*   1.1. The Confluence of AI Benchmarking and Digital Humanities (DH)
*   1.2. The Shift from Traditional NLP to Generative LLM/VLM Evaluations
*   1.3. Methodology of the Survey: Paper Selection and Inclusion Criteria
*   1.4. Exclusion of Non-Humanistic Domains (e.g., Enterprise/Finance Benchmarks like *OfficeQA Pro*)

#### 2. Taxonomy of Arts & Humanities Benchmarks
*   2.1. Classification by ASJC Subject Areas
    *   2.1.1. History and Archaeology
    *   2.1.2. Language, Linguistics, and Classics
    *   2.1.3. Literature and Literary Theory
    *   2.1.4. Visual Arts, Performing Arts, and Musicology
    *   2.1.5. Philosophy and Religious Studies
    *   2.1.6. Museology and Archival Conservation
*   2.2. Classification by Modality Configurations (Text-Only, Multimodal Image-Text, Agentic Web-Browsing)
*   2.3. Classification by Analytical Task Type and Cognitive Complexity

#### 3. Modality Landscape and Alignment Analysis
*   3.1. The Dominance of Text-Based Evaluations and the Multimodal Transition
*   3.2. Mapping Visual Arts: Style Identification, Iconography, and Generative Criticism
*   3.3. Underrepresented Modalities: The Critical Lack of Audio, Video, and 3D Material Benchmarks
*   3.4. Evaluating Task-Domain Alignment: Real-World Scholarly Workflows vs. Simplistic Proxies

#### 4. Methodological Patterns in Humanities Evaluation
*   4.1. The Evolution of Evaluation Paradigms: From String Matching to LLM-as-a-Judge
*   4.2. Incorporating External Search and Verification Agents (e.g., the SAFE Framework)
*   4.3. Standard vs. Novel Metrics in Humanities Benchmarks
    *   4.3.1. Error Rates and Orthographic Alignment in Historical OCR
    *   4.3.2. Fine-grained Character and Archaic Word Preservation Metrics (AIR, HCPR)
    *   4.3.3. Structural Quality Indicators: Dimension Coverage Rate (DCR) and Schema Conformance
*   4.4. Analysis of Model Testing Cohorts: Proprietary Leaders vs. Specialized Open-Source Architectures

#### 5. Cross-Linguistic and Multicultural Competency
*   5.1. Exposing Western Bias in Multilingual Evaluation Frameworks
*   5.2. Benchmarking Regional Histories and Localized Cultural Knowledge
*   5.3. Grammatical Case-Marking, Morphology, and Dialectal Acceptability in Low-Resource Languages

#### 6. Gaps, Challenges, and Future Horizons
*   6.1. Epistemological Limitations: The Gap Between Factual Recall and Causal Interpretation
*   6.2. Addressing the Lack of Dynamic, Agentic Digital Humanities Benchmarks
*   6.3. The Structural Western Bias in Translation-Based Datasets
*   6.4. Designing Next-Generation Evaluations: The Blueprint for a *Hermeneutic-Agent-Bench*

#### 7. Conclusion and Call to Action
*   7.1. Summary of Key Survey Insights
*   7.2. Recommendations for AI Researchers: Designing More Challenging Humanities Evaluations
*   7.3. Recommendations for Digital Humanists: Maintaining Epistemological Rigor in the Era of Automation