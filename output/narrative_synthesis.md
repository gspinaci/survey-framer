# Survey Narrative Synthesis

# AI Benchmarking in Arts & Humanities: A Synthesis

## 1. Thematic Clusters

### Language & Linguistic Phenomena Cluster
**Papers**: LAMBADA, AdMIRe, MILU
**Common Thread**: These benchmarks focus on sophisticated linguistic understanding beyond surface-level pattern matching. LAMBADA tests discourse-level context understanding in literary narratives, AdMIRe evaluates multimodal comprehension of idiomatic expressions, and MILU assesses culturally-grounded linguistic competence across Indian languages. All require models to demonstrate deep semantic understanding rather than factual recall.

### Multimodal Cultural Understanding Cluster  
**Papers**: VULCA-BENCH, MMMU-Pro
**Common Thread**: These benchmarks combine visual and textual modalities to test sophisticated cultural reasoning. VULCA-BENCH specifically targets cross-cultural art interpretation across six traditions, while MMMU-Pro includes humanities disciplines within its broader college-level reasoning framework. Both emphasize genuine multimodal integration over exploiting single-modality shortcuts.

### Culturally-Grounded Knowledge Assessment Cluster
**Papers**: MILU, VULCA-BENCH
**Common Thread**: These benchmarks prioritize cultural authenticity and regional specificity over universal knowledge. MILU tests understanding of Indian regional traditions, while VULCA-BENCH evaluates interpretation across distinct cultural art traditions. Both reveal systematic biases in current models toward dominant cultural frameworks.

## 2. Modality & Task Landscape

### Modality Coverage
**Well-Covered**: Text-only benchmarks remain prevalent (LAMBADA, MILU), with growing emphasis on text+image combinations (MMMU-Pro, VULCA-BENCH, AdMIRe). The multimodal approaches show increasing sophistication, moving from simple visual question answering to complex cultural interpretation tasks.

**Underrepresented**: Audio modalities are completely absent from this corpus, despite their centrality to music, oral traditions, and performance studies. Video sequences appear only minimally in AdMIRe's temporal image sequences, missing opportunities for narrative analysis or performance evaluation.

**Emerging Sophistication**: Advanced multimodal integration appears in VULCA-BENCH's five-level cultural understanding hierarchy and AdMIRe's figurative language comprehension, suggesting evolution toward tasks requiring genuine cross-modal reasoning.

### Task Types
**Dominant Tasks**: Multiple-choice question answering dominates (MILU, MMMU-Pro), with ranking tasks (AdMIRe) and word prediction (LAMBADA) appearing less frequently. Generation tasks are limited to VULCA-BENCH's art critique generation.

**Task Complexity Distribution**: Simple factual recognition appears mainly in MILU's cultural knowledge assessment, while complex reasoning spans VULCA-BENCH's five-level hierarchy and MMMU-Pro's college-level problem solving. Most sophisticated tasks require synthesis of cultural context with analytical interpretation.

### Task-Domain Alignment
**Strong Alignment**: VULCA-BENCH's art critique generation closely matches actual humanities scholarly practice. AdMIRe's idiomaticity tasks align well with linguistic analysis requirements. MILU's cultural knowledge assessment reflects authentic regional examination practices.

**Weaker Alignment**: LAMBADA uses literary content but tests general language modeling rather than literary analysis capabilities. MMMU-Pro includes humanities domains but within a broader STEM-oriented evaluation framework rather than discipline-specific methodologies.

## 3. Methodological Patterns

### Evaluation Approaches
**Automated Metrics**: Accuracy dominates across benchmarks, with VULCA-BENCH introducing more sophisticated measures (DCR, CSA, CDS, LQS) and AdMIRe using ranking-based metrics (DCG). Human evaluation appears only in VULCA-BENCH through expert rating alignment.

**Model Selection**: GPT-4 variants appear consistently across recent benchmarks, with growing inclusion of multimodal models (LLaVA, BLIP, Gemini) and specialized multilingual models reflecting increasing recognition of modality and language diversity requirements.

**Complexity Scaling**: Benchmarks show progression from binary correctness (LAMBADA, MILU) toward graduated evaluation schemes (VULCA-BENCH's five levels, AdMIRe's ranking tasks), suggesting growing sophistication in capturing nuanced humanities understanding.

### Recurring Methodological Choices
**Cross-lingual Evaluation**: Appears in MILU (11 Indic languages), AdMIRe (English/Portuguese), and VULCA-BENCH (Chinese/English), indicating recognition that cultural understanding cannot be divorced from linguistic diversity.

**Cultural Bias Analysis**: VULCA-BENCH and MILU explicitly test for cultural bias, revealing systematic preferences for Western/dominant cultural frameworks—a crucial consideration largely absent from earlier benchmarks.

## 4. Narrative Framing Options

### For Newcomers: "Bridging AI and Human Culture"
Emphasize the fundamental challenge of encoding cultural understanding in computational systems. Structure around three core questions: How do we computationally represent cultural knowledge? What does it mean for AI to "understand" humanistic content? How do we evaluate cultural competence fairly across traditions?

**Focus**: Foundational concepts, accessibility of humanities domains to AI, basic modality combinations, clear examples of success/failure cases.

### For Experts: "Methodological Innovations in Computational Humanities"
Frame around sophisticated evaluation paradigms emerging from digital humanities practice. Emphasize novel metrics (VULCA-BENCH's five-level hierarchy), cultural authenticity concerns (MILU's regional specificity), and the evolution from factual assessment toward interpretive evaluation.

**Focus**: Methodological rigor, cultural representation issues, discipline-specific evaluation criteria, integration with existing digital humanities workflows.

### For AI Researchers: "Multimodal Reasoning in Cultural Domains"
Position as a frontier challenge in multimodal AI requiring novel architectures and training paradigms. Emphasize technical challenges: cross-cultural generalization, multimodal fusion for interpretive tasks, evaluation metric design for subjective domains.

**Focus**: Technical architectures, dataset construction challenges, novel evaluation metrics, benchmarking methodology innovations, bias detection and mitigation.

## 5. Gaps and Opportunities

### Underrepresented Modalities
**Audio**: Complete absence despite centrality to music studies, oral traditions, linguistic phonetics, and performance analysis. Next-generation benchmarks should incorporate speech, music, and soundscape analysis.

**Video/Temporal**: Limited to AdMIRe's image sequences. Missing opportunities for narrative analysis, performance studies, film/media studies, and temporal art forms.

**3D/Spatial**: No representation of architectural analysis, sculpture assessment, or spatial humanities applications.

### Missing ASJC Areas
**Philosophy**: Despite appearing in categorizations, no benchmarks directly test philosophical reasoning, argument analysis, or ethical interpretation.

**Archaeology**: Absent despite rich potential for multimodal (visual + textual + spatial) evaluation scenarios.

**Religious Studies**: Limited representation despite cultural importance and interpretive complexity.

### Analytical Task Complexity Gaps
**Interpretive Generation**: Only VULCA-BENCH attempts long-form interpretive generation. Missing opportunities for essay analysis, creative writing evaluation, critical interpretation tasks.

**Comparative Analysis**: No benchmarks test cross-cultural or cross-temporal comparative reasoning despite this being central to humanities scholarship.

**Source Criticism**: No evaluation of source analysis, authenticity assessment, or evidence evaluation skills crucial to historical and literary studies.

### Next-Generation Benchmark Vision
A comprehensive humanities AI benchmark should integrate: (1) Multimodal temporal analysis combining text, image, audio, and video; (2) Graduated cultural competence evaluation across multiple traditions; (3) Interpretive generation tasks with expert evaluation frameworks; (4) Cross-cultural comparative reasoning assessment; (5) Dynamic knowledge evaluation reflecting evolving cultural understanding rather than static factual knowledge.

## 6. Suggested Survey Structure

### Option A: Modality-Centered Structure
```
1. Introduction: AI Meets Cultural Understanding
2. Text-Only Foundations (LAMBADA, MILU linguistic components)
3. Text+Image Integration (MMMU-Pro, AdMIRe, VULCA-BENCH)
4. Temporal and Sequential Modalities (AdMIRe sequences, future directions)
5. Missing Modalities: Audio, Video, 3D (gap analysis)
6. Cross-Modal Cultural Reasoning (synthesis)
7. Future Directions: Toward Comprehensive Cultural AI
```

### Option B: Task Complexity Structure
```
1. Introduction: Evaluating Cultural Competence in AI
2. Factual and Recognition Tasks (MILU cultural knowledge)
3. Linguistic Understanding Tasks (LAMBADA, AdMIRe)
4. Interpretive and Analytical Tasks (VULCA-BENCH critique generation)
5. Cross-Cultural Reasoning Tasks (comparative analysis across benchmarks)
6. Methodological Innovations in Humanities Evaluation
7. Toward Sophisticated Cultural AI Assessment
```

### Option C: Cultural Authenticity Structure  
```
1. Introduction: Culture and Computation
2. Universal vs. Culturally-Specific Knowledge (MMMU-Pro vs. MILU)
3. Cultural Bias in AI Evaluation (VULCA-BENCH findings)
4. Authentic Cultural Representation (MILU regional specificity)
5. Cross-Cultural Competence Assessment (synthesis across benchmarks)
6. Methodological Considerations for Cultural AI
7. Building Culturally-Responsive Evaluation Frameworks
```

**Recommendation**: Option C (Cultural Authenticity Structure) best captures the emerging consensus that cultural understanding cannot be divorced from questions of representation, bias, and authentic engagement with diverse humanistic traditions—a theme running throughout the most sophisticated benchmarks in this corpus.