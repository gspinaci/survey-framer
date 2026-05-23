# Survey Narrative Synthesis

# AI Benchmarks for Arts & Humanities: A Synthesis

## 1. Thematic Clusters

### Visual Arts & Cultural Heritage
**Papers**: MMMU-Pro, Christian Iconography Classification, VQArt-Bench, VULCA-BENCH (both versions), Appear2Meaning

**Common Thread**: These benchmarks center on visual analysis of cultural artifacts, requiring models to interpret artistic content, iconographic symbols, and cultural metadata. They span from basic visual recognition to sophisticated cultural understanding, with tasks ranging from saint identification in religious art to cross-cultural aesthetic critique generation.

### Linguistic & Literary Understanding
**Papers**: MILU, AdMIRe

**Common Thread**: Focus on language-specific cultural phenomena including idiomatic expressions, multilingual reasoning, and culturally embedded linguistic knowledge. These benchmarks test models' ability to navigate the semantic complexity of figurative language and culture-specific expressions across multiple languages.

### Historical Knowledge Assessment
**Papers**: HiST-LLM

**Common Thread**: Evaluates factual historical comprehension using expert-curated datasets, testing models on graduate-level historical knowledge across civilizations and time periods.

## 2. Modality & Task Landscape

### Modality Coverage
**Text-Only Dominance**: Text-only benchmarks (MILU, HiST-LLM) focus on knowledge assessment and multilingual understanding, representing the most straightforward evaluation approach for humanities content.

**Vision-Language Integration**: The majority of benchmarks (6/9) employ multimodal approaches combining images with text, reflecting the visual nature of much humanities scholarship, particularly in art history and cultural studies.

**Underrepresented Modalities**: Audio remains completely absent despite music being a core humanities domain. Temporal sequences appear only in AdMIRe's limited visual-temporal component.

### Task Types
**Factual Recognition Dominance**: Most benchmarks emphasize factual knowledge assessment through classification tasks (iconography identification, historical knowledge, cultural attribution).

**Emerging Generation Tasks**: VULCA-BENCH introduces sophisticated critique generation, representing a shift toward evaluating creative and analytical capabilities rather than mere recognition.

**Complex Reasoning Gap**: While VQArt-Bench includes "Visual-Inspired Reasoning," most benchmarks focus on surface-level recognition rather than the causal reasoning, interpretation, and synthesis central to humanities scholarship.

### Task-Domain Alignment
**Strong Alignment**: Visual arts benchmarks appropriately emphasize iconographic analysis and cultural interpretation. Historical benchmarks correctly focus on factual knowledge assessment.

**Potential Misalignment**: The emphasis on multiple-choice formats may not capture the discursive, interpretive nature of humanities scholarship. VULCA-BENCH's critique generation better aligns with authentic humanities practices.

## 3. Methodological Patterns

### Evaluation Approaches
**Accuracy-Based Metrics**: Nearly universal use of accuracy scores for classification tasks, with some benchmarks introducing sophisticated rubrics (VULCA-BENCH's 225-dimension framework).

**LLM-as-Judge Framework**: Emerging pattern in Appear2Meaning and VULCA-BENCH for evaluating complex generative tasks, addressing the challenge of assessing open-ended humanities outputs.

**Multi-Shot Learning**: Consistent evaluation across zero-shot, few-shot, and chain-of-thought prompting strategies.

### Model Coverage
**Dominant Models**: GPT-4 variants, Gemini series, and Claude models appear across most benchmarks, establishing these as standard evaluation targets.

**Multimodal Focus**: Strong emphasis on Vision-Language Models (VLMs) reflecting the visual nature of cultural heritage and arts domains.

**Specialized Models**: Limited evaluation of humanities-specific or culturally-adapted models, with most benchmarks testing general-purpose systems.

### Analytical Complexity
**Hierarchical Frameworks**: VULCA-BENCH's five-layer framework (L1-L5) and VQArt-Bench's seven-dimension approach represent sophisticated attempts to capture varying levels of analytical sophistication.

**Cultural Specificity**: Increasing attention to culture-specific knowledge (MILU's Indic languages, VULCA-BENCH's cross-cultural approach) rather than Western-centric evaluation.

## 4. Narrative Framing Options

### For Newcomers: "Multimodal AI Meets Cultural Understanding"
Frame around the challenge of moving beyond text-only AI to systems that can interpret visual culture, historical artifacts, and cross-cultural knowledge. Emphasize the progression from basic recognition to sophisticated cultural interpretation, using concrete examples like identifying saints in paintings or understanding idiomatic expressions across languages.

### For Experts: "Evaluating Computational Approaches to Cultural Analysis"
Frame around methodological challenges of quantifying humanities scholarship - how do we measure aesthetic judgment, cultural interpretation, or historical reasoning? Focus on the tension between standardized metrics and the interpretive, discursive nature of humanities work, highlighting innovations like VULCA-BENCH's critique generation.

### For AI Researchers: "Beyond Classification: Reasoning and Generation in Cultural Domains"
Frame around technical challenges: multimodal fusion for cultural content, handling low-resource languages/cultures, evaluating generated cultural analysis, and the need for hierarchical reasoning frameworks that capture increasing analytical sophistication from perception to philosophical aesthetics.

## 5. Gaps and Opportunities

### Underrepresented Modalities
- **Audio**: Complete absence of music, oral history, or linguistic audio analysis
- **Temporal Media**: No evaluation of film, performance, or time-based arts
- **3D/Spatial**: Missing archaeological, architectural, and sculptural analysis

### Task Complexity Gaps
- **Comparative Analysis**: No benchmarks require comparing works across periods, cultures, or media
- **Argumentation**: Missing evaluation of thesis development, evidence synthesis, or scholarly debate
- **Creative Generation**: Limited evaluation of creative or interpretive writing in humanities contexts

### Cultural and Linguistic Limitations
- **Geographic Bias**: Limited representation of African, Oceanic, and Indigenous knowledge systems
- **Temporal Scope**: Heavy focus on established canonical works rather than contemporary cultural production
- **Methodological Diversity**: Missing evaluation of different humanities methodologies (formalist, marxist, postcolonial approaches)

### Next-Generation Benchmark Vision
A comprehensive humanities AI benchmark would include:
1. **Multimodal Integration**: Audio-visual-textual analysis of cultural productions
2. **Temporal Reasoning**: Understanding cultural change, influence, and historical development
3. **Argumentative Tasks**: Generating and evaluating scholarly arguments with evidence
4. **Collaborative Analysis**: Multi-perspective interpretation reflecting humanities' interpretive plurality
5. **Ethical Reasoning**: Evaluating cultural sensitivity and power dynamics in interpretation

## 6. Suggested Survey Structure

### Option A: Modality-Driven Organization
1. **Introduction**: The Challenge of Humanities AI Evaluation
2. **Text-Only Benchmarks**: Knowledge Assessment and Linguistic Understanding
3. **Vision-Language Benchmarks**: Visual Culture and Multimodal Interpretation
4. **Emerging Modalities**: Toward Audio-Visual-Temporal Integration
5. **Evaluation Methodologies**: From Accuracy to Interpretive Assessment
6. **Cultural Representation and Bias**: Geographic and Temporal Scope
7. **Future Directions**: Toward Comprehensive Humanities AI Evaluation

### Option B: Analytical Complexity Organization
1. **Introduction**: Operationalizing Humanities Scholarship for AI Evaluation
2. **Level 1: Recognition and Classification**: Basic Cultural Knowledge
3. **Level 2: Analysis and Interpretation**: Understanding Cultural Meaning
4. **Level 3: Synthesis and Critique**: Generating Humanities Scholarship
5. **Cross-Cutting Concerns**: Multimodality, Cultural Specificity, Bias
6. **Methodological Innovations**: LLM-as-Judge, Hierarchical Frameworks
7. **Research Agenda**: Gaps and Future Benchmark Development

### Option C: Domain-Task Matrix Organization
1. **Introduction**: Mapping AI Capabilities Across Humanities Domains
2. **Visual Arts**: From Iconography to Aesthetic Critique
3. **Historical Studies**: Knowledge Assessment and Temporal Reasoning
4. **Linguistic Studies**: Multilingual and Cross-Cultural Understanding
5. **Methodological Synthesis**: Evaluation Approaches Across Domains
6. **Cultural Representation**: Geographic and Temporal Coverage Analysis
7. **Future Trajectories**: Toward Comprehensive Humanities AI Assessment

**Recommendation**: Option B (Analytical Complexity) best captures the progression from basic recognition to sophisticated interpretation that characterizes humanities scholarship, while allowing discussion of methodological innovations and cultural considerations at each level.