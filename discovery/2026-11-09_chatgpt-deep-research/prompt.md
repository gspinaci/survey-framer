# Prompt for ChatGPT Deep Research — census update

*Paste everything below the line into a Deep Research session. Window: 1 May 2026 (three weeks of overlap with the last systematic search, closed 22 May 2026) to 9 November 2026. Adjust the end date if run later.*

---

## Task

I am updating a census of **benchmarks that evaluate generative large language models on digital humanities material**. Find every benchmark that meets ALL the criteria below and was **first made public (preprint, proceedings, journal, or shared-task overview) between 1 May 2026 and 9 November 2026**. Report each benchmark only after you have opened the paper itself and checked the criteria against its text, not against a title or a summary.

Recall matters more than precision: include borderline cases and mark them as borderline. I will screen every candidate by hand. Do not invent anything: every row needs a working URL to the paper, and a candidate you could not open goes in the "unverified" list, not in the main table.

## Inclusion criteria (all four must hold)

1. **It is a benchmark.** It defines a fixed evaluation set together with a scoring procedure that yields quantitative metrics, so that an independent party could re-run the evaluation and obtain a comparable number. Shared tasks qualify: the task definition plus the scoring script is the benchmark. The paper does not need to use the word "benchmark". An evaluation study qualifies if it fixes its test set and scoring and reports numbers on it. **Excluded:** qualitative probes and demonstrations, datasets released without an evaluation protocol, papers that only report scores on an existing benchmark without defining a new evaluation set or protocol, and surveys.
2. **It evaluates at least one generative language model**, meaning a model that produces text, including text conditioned on images, audio or video. Vision-language models count. Encoder-only classifiers (BERT-style models with a classification head) do not count on their own: a generative model must be among the systems the benchmark is designed to assess.
3. **Its material belongs to the humanities (domain reading).** The test is whether the *material* the model reasons over belongs to a humanities subject area, not whether the method is computational. Reference areas (Scopus ASJC "Arts and Humanities" plus neighbours): History; Language and Linguistics; Visual Arts and Performing Arts; Religious Studies; Cultural Studies; Philosophy; Literature and Literary Theory; Music; Classics; Museology; Archaeology; Conservation; History and Philosophy of Science. Cultural-heritage material (manuscripts, archives, artworks, historical newspapers, museum collections, iconography, epigraphy, historical languages, folklore, oral history) is in scope. **General-purpose benchmarks are in scope if they contain an identifiable humanities component** (for example an MMLU-style exam with history, philosophy or art subsets, or a cultural-knowledge benchmark). Report what share or which subsets are humanities. Benchmarks that are purely about law, medicine, STEM, finance, coding or social-media sentiment are out, unless a substantial part of the material is historical or cultural.
4. **English is among the evaluated languages.** Multilingual and non-English-centred benchmarks are in, provided English is one of the evaluated languages (including English prompts or English as a source or target language in translation).

## Already in the census — do NOT report these (or other versions of them)

MMLU / MMMLU (arXiv 2009.03300); MMMU-Pro (2409.02813); Global-MMLU (2412.03304); MILU (2411.02538); BrowseComp (2504.12516); SimpleQA (2411.04368); LongFact (2403.18802); FActScore (2305.14251); Humanity's Last Exam (2501.14249); DeepSearchQA (2601.20975); VQArt-Bench (2510.12750); VULCA-Bench (2601.07986 and 2601.07984); HiST-LLM (NeurIPS 2024); JOKER 2025 Task 2 (pun translation EN→FR, CLEF 2025); AdMIRe (SemEval 2025, 2503.15358); Christian Iconography (2509.18839); Appear2Meaning (2604.07338); Post-OCR correction of historical newspapers (LT4HALA 2024); Islamic literature translation, Al-Shamela (CLRel 2025); "Text Is Not All You Need" multimodal prompting (CHum 2025); LLM translation and summarization for Latin (LT4HALA 2024); CzechTopic (2603.03884); historical document OCR methodological framework (LM4DH 2025); "Finding the Plea" rhetorical structure (LM4DH 2025); parole suitability hearings, PSH v1.0 (LM4DH 2025); CHVM-1K (2501.02039); OfficeQA Pro (2603.08655); CulturalBench (2410.02677); LLMs4Subjects (SemEval 2025, 2504.07199); SuperGPQA (2502.14739); RISE Humanities Data Benchmark (JOHD 2026); EXAMS-V (2403.10378); IRLBench (2505.13498); MMLU-ProX (EMNLP 2025); MultiNRC (2507.17476); DRISHTIKON (EMNLP 2025); CaLMQA (ACL 2025); CulturALL (2604.19262); C3B, Culture In a Frame (2510.00041); HistBench / HistAgent (2505.20246); MultiBLiMP 1.0 (2504.02768); Hanfu-Bench (EMNLP 2025); M3Exam (NeurIPS 2023); EduArt (2607.02007). Also already known to us, not yet catalogued: HSSBench (2506.03922).

A **new version** of one of these (for example a "v2" with a new evaluation set) counts as a new candidate: report it and say which benchmark it extends.

## Where to search (cover all of these and log what you searched)

- **arXiv**: cs.CL, cs.CV, cs.AI, cs.DL, cs.MM. Combine evaluation terms (benchmark, evaluation, leaderboard, test set, shared task) with domain terms (digital humanities, cultural heritage, history, historical, art history, artwork, painting, iconography, museum, archive, manuscript, palaeography, OCR/HTR, epigraphy, philology, classics, Latin, Ancient Greek, Sanskrit, classical Chinese, literature, poetry, literary, music, musicology, religion, philosophy, archaeology, folklore, culture/cultural).
- **ACL Anthology** (2026 events): ACL 2026, NAACL 2026, EACL 2026, EMNLP 2026 (and Findings), COLING, LREC 2026 and its workshops. DH and heritage workshops: LT4HALA 2026, NLP4DH, LaTeCH-CLfL 2026, LM4DH, ML4AL, CLRel/CHum, NakbaNLP, LoResLM, AfricaNLP, VarDial, sign-lang, LLM4SSH.
- **Machine-learning venues:** NeurIPS 2026 Datasets & Benchmarks track (OpenReview), ICLR 2026, ICML 2026, COLM 2026.
- **Vision venues:** CVPR 2026, ICCV/ECCV 2026 workshops on art and cultural heritage (VISART, AI4VA, SINT4CH, WCCA, VLMs-4-all and similar).
- **DH venues:** DH2026 conference, CHR 2026 (Computational Humanities Research), *Journal of Open Humanities Data* (including the "Benchmarking in Digital Humanities" collection), *Digital Humanities Quarterly*, *Digital Scholarship in the Humanities*, *ACM JOCCH*.
- **Shared tasks and evaluation campaigns:** CLEF 2026 (JOKER, PAN, other labs), SemEval 2026, EvaLatin, EvaHan, other 2026 campaigns on historical or literary text.
- **Model system cards and technical reports** published in the window (Anthropic, OpenAI, Google DeepMind, Meta, Alibaba Qwen, DeepSeek, Mistral, xAI and others). List the evaluation benchmarks they report that have humanities content and appeared in the window.
- **Leaderboards and aggregators:** Hugging Face datasets and leaderboards, HELM, Papers with Code successors.

## Output

### Table 1 — candidates (one row per benchmark, as CSV in a code block)

Columns, in this order:
`Name, Article URL, PDF URL, First public date (YYYY-MM-DD), Year, Venue or status, Modalities, Domain, Evaluation metrics, Humanities areas, Languages (is English included?), Generative models evaluated, Resource URL (Benchmark + Dataset), Found via, Evidence C1 benchmark, Evidence C2 generative LLM, Evidence C3 humanities material, Evidence C4 English, Borderline?, Confidence`

- **Article URL:** prefer the arXiv abs page or the DOI. **PDF URL:** a direct link to the full-text PDF (open-access version if one exists).
- **Modalities:** text, image, audio, video (combine as needed).
- **Humanities areas:** use only the area names listed in criterion 3.
- **Evidence C1-C4:** one short sentence each, quoting the paper where possible ("we release 2,400 multiple-choice items scored by exact match…").
- **Borderline?** yes/no, plus which criterion is doubtful and why. **Confidence:** high/medium/low.
- If a benchmark has both a preprint and a published version, use one row, give the published version as Article URL and mention the preprint in Venue or status.

### Table 2 — near misses
Benchmarks you considered and excluded, with name, URL and the criterion that failed (one line each). This list is as useful to me as Table 1.

### Table 3 — unverified
Candidates you found mentioned but could not open or check (name, where you saw it, why unverified).

### Search log
For each source above: what you searched (queries, proceedings volumes, pages), date range, and how many candidates each search yielded. Say explicitly if a source could not be accessed.
