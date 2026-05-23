# Survey Narrative Synthesis

# Benchmarking LLMs in Arts & Humanities: A Systematic Analysis

## 1. Thematic Clusters

### **Visual Arts & Cultural Heritage Analysis**
**Papers:** VQArt-Bench, VULCA-BENCH, Christian Iconography Classification, Appear2Meaning

**Common Thread:** These benchmarks focus on visual interpretation of artistic and cultural heritage objects, requiring models to understand iconographic symbols, cultural contexts, and art-historical knowledge. They emphasize the gap between visual perception and deep cultural interpretation, testing capabilities from basic object recognition to sophisticated aesthetic and symbolic analysis.

### **Language & Linguistic Phenomena**
**Papers:** LAMBADA, AdMIRe, MILU

**Common Thread:** These evaluate models' understanding of complex linguistic structures and cultural language use, from discourse comprehension and idiomatic expressions to multilingual cultural knowledge. They highlight the challenge of non-compositional meaning and culturally-embedded linguistic phenomena.

### **Historical Knowledge Systems**
**Papers:** HiST-LLM, MILU (historical components)

**Common Thread:** Focus on factual historical knowledge and temporal reasoning across different cultural contexts. These benchmarks test expert-level domain knowledge rather than interpretive skills, emphasizing the breadth of historical coverage and cultural representation.

### **Multimodal Cross-Cultural Understanding**
**Papers:** MMMU-Pro, VULCA-BENCH, VQArt-Bench

**Common Thread:** These represent the most sophisticated benchmarks, combining multiple modalities with cultural interpretation tasks. They test whether models can integrate visual and textual information while navigating cultural specificity and avoiding Western-centric biases.

## 2. Modality & Task Landscape

### **Modality Coverage**
- **Text-only dominance:** Traditional benchmarks (LAMBADA, HiST-LLM, MILU) remain text-centric, focusing on linguistic and factual knowledge
- **Image+Text emergence:** The majority of recent benchmarks (6/10) incorporate visual elements, reflecting the importance of visual culture in humanities
- **Underrepresented modalities:** Audio is completely absent despite music being a core humanities domain. Video/temporal sequences appear only in AdMIRe's comic-style progressions
- **Multimodal complexity:** Advanced benchmarks like VULCA-BENCH test true integration rather than parallel processing of modalities

### **Task Types**
- **Factual recognition tasks** dominate simpler benchmarks (HiST-LLM, MILU multiple-choice sections)
- **Cultural interpretation tasks** represent the most challenging category, requiring deep domain knowledge and cultural sensitivity
- **Generation tasks** (VULCA-BENCH art critiques) are less common but more aligned with humanities scholarship practices
- **Hybrid reasoning tasks** (VQArt-Bench's seven-dimensional framework) attempt to bridge perception and interpretation

### **Task-Domain Alignment**
Strong alignment exists in specialized domains (Christian iconography, art criticism) but gaps remain in:
- **Temporal reasoning** for historical analysis
- **Aesthetic judgment** beyond cultural attribution  
- **Comparative analysis** across traditions or periods
- **Methodological reasoning** reflecting humanities scholarship practices

## 3. Methodological Patterns

### **Model Selection**
- **GPT-4 variants** appear in 80% of benchmarks, serving as de facto baselines
- **Gemini and Claude** models increasingly tested for multimodal capabilities
- **Open-source models** (Llama, Qwen) consistently underperform but provide accessibility
- **Domain-specific fine-tuning** surprisingly rare despite humanities' specialized vocabularies

### **Evaluation Approaches**
- **Multiple-choice formats** dominate (7/10 benchmarks) for standardization but may not capture humanities reasoning
- **LLM-as-Judge frameworks** emerging for complex generation tasks (VULCA-BENCH, Appear2Meaning)
- **Human expert validation** present in cultural domains but scaling challenges evident
- **Hierarchical evaluation** (VULCA-BENCH's L1-L5 framework) represents methodological innovation

### **Metrics and Complexity**
- **Accuracy metrics** standard across factual tasks
- **Cultural bias measurement** increasingly important (VULCA-BENCH's systematic bias detection)
- **Interpretability challenges** in distinguishing visual perception from cultural knowledge
- **Cross-lingual evaluation** underexplored despite humanities' multilingual nature

## 4. Narrative Framing Options

### **For Newcomers: "Bridging AI and Cultural Understanding"**
Emphasize the unique challenges humanities poses to AI systems: non-factual knowledge, cultural specificity, interpretive reasoning, and multimodal integration. Frame around three progressive challenges: (1) Cultural Knowledge Acquisition, (2) Cross-Modal Cultural Interpretation, (3) Sophisticated Cultural Reasoning. Highlight how humanities benchmarks reveal fundamental limitations in current AI systems' cultural competence.

### **For Digital Humanities Experts: "Computational Methods Meet Cultural Analysis"**
Focus on methodological innovations in evaluation frameworks, particularly the development of hierarchical cultural understanding measures and bias detection in AI systems. Emphasize gaps in representing actual humanities scholarship practices and the need for benchmarks that reflect disciplinary methods (comparative analysis, close reading, historical contextualization) rather than just factual recall.

### **For AI Researchers: "Cultural Intelligence as a Frontier Challenge"**
Frame around technical challenges: non-compositional meaning, long-range contextual dependencies, cultural bias mitigation, and multimodal reasoning. Highlight how humanities benchmarks expose fundamental limitations in current architectures and training paradigms, particularly around cultural knowledge representation and cross-cultural generalization.

## 5. Gaps and Opportunities

### **Underrepresented Modalities**
- **Audio analysis:** Music theory, oral traditions, linguistic prosody completely absent
- **Temporal media:** Video analysis for film studies, performance documentation
- **3D/Spatial:** Archaeological artifacts, architectural analysis, sculpture
- **Archival materials:** Manuscript analysis, paleography, codicology

### **Missing Analytical Tasks**
- **Comparative analysis:** Cross-cultural, cross-temporal, cross-media comparisons
- **Argumentation:** Thesis construction, evidence evaluation, interpretive reasoning
- **Contextual synthesis:** Integrating multiple sources and perspectives
- **Creative generation:** Poetry, narrative, creative translation

### **Disciplinary Gaps**
- **Philosophy:** Logical reasoning, conceptual analysis, argumentation
- **Music:** Composition analysis, performance interpretation, cultural contexts  
- **Literature:** Close reading, narrative analysis, genre classification
- **Archaeology:** Material culture analysis, stratigraphic reasoning

### **Next-Generation Benchmark Vision**
A comprehensive humanities AI benchmark should integrate:
1. **Multi-temporal reasoning** across historical periods and cultural development
2. **Argumentative structure evaluation** reflecting actual humanities scholarship
3. **Cross-cultural comparative capabilities** with systematic bias measurement
4. **Creative-analytical tasks** combining interpretation with generation
5. **Collaborative reasoning** simulating scholarly discourse and peer review

## 6. Suggested Survey Structure

### **Proposed Table of Contents**

1. **Introduction: Cultural Intelligence as an AI Challenge**
   - Defining humanities AI evaluation
   - Unique challenges vs. STEM domains

2. **Modality-Centric Analysis**
   - 2.1 Text-Based Cultural Understanding
   - 2.2 Visual-Cultural Interpretation
   - 2.3 Multimodal Cultural Integration
   - 2.4 Missing Modalities and Future Directions

3. **Task Complexity Hierarchy**
   - 3.1 Factual Cultural Knowledge
   - 3.2 Interpretive Reasoning
   - 3.3 Comparative and Synthetic Analysis
   - 3.4 Creative-Analytical Integration

4. **Disciplinary Deep Dives**
   - 4.1 Visual Arts and Cultural Heritage
   - 4.2 Historical Analysis and Temporal Reasoning
   - 4.3 Language, Literature, and Linguistic Phenomena
   - 4.4 Cross-Cultural and Comparative Studies

5. **Methodological Innovations**
   - 5.1 Evaluation Framework Evolution
   - 5.2 Cultural Bias Detection and Mitigation
   - 5.3 Expert Validation and Scaling Challenges

6. **Critical Assessment and Future Directions**
   - 6.1 Alignment with Humanities Scholarship Practices
   - 6.2 Technical Limitations and Opportunities
   - 6.3 Toward Next-Generation Cultural AI Evaluation

This structure balances technical AI concerns with humanities domain expertise while providing clear progression from current capabilities to future challenges and opportunities.