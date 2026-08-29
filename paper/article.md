# What Counts as Correct: A Census of Digital Humanities Benchmarks for Large Language Models

## Abstract

Evaluating a language model requires declaring, in advance, which answer is correct. On an arithmetic problem this is an innocuous requirement. On an iconographic attribution, a manuscript dating, the translation of a pun, or the reading of a damaged archival document, deciding which answer is correct *is already* the disciplinary act — the one specialists argue about, and sometimes continue to argue about productively. This paper reports a census of 42 benchmarks that make that decision: benchmarks published between 2021 and 2026 that evaluate generative language models on digital humanities material with quantitative metrics.

We describe each benchmark along two axes. The first records how the benchmark was *built*: where its reference answers came from, whether answering requires knowledge absent from the stimulus, whether correctness is treated as varying by cultural community, whether the target is a property of an artefact's genesis, how many answers the scoring accepts, and how the paper treats disagreement between defensible readings. The second records what the benchmark *found*: the headline score, whether a human baseline was measured, whether a systematic cross-cultural asymmetry was reported, and whether the paper measured the same material under two different scoring regimes.

Three results follow. First, twenty-one of the 42 benchmarks — exactly half — ask questions whose correct answer is not present in the stimulus shown to the model, and score the outcome against a single key. Second, nine benchmarks measured the same material two ways, changing only how the score was assigned; all nine obtained two different scores, with a median gap of 31 percentage points and a maximum of 88. Third, the benchmarks least likely to run that check are precisely those whose format is most closed: two of 28 single-answer benchmarks tested their own instrument, against seven of 14 among the rest (Fisher's exact, *p* = 0.003). Alongside these we report what the corpus does not ask: the genesis of artefacts — date, author, place of origin, provenance — is the target of three benchmarks out of 42.

We report the census with its limits stated as results rather than caveats, including a documented failure of our own pipeline that we did not correct before writing, and we describe the maintenance procedure by which the census can be kept current.

---

## 1. Introduction

The evaluation of large language models has converged on a particular epistemic form. A benchmark presents a stimulus, elicits a response, and compares that response to a reference answer that was fixed before the model was run. The comparison yields a number, numbers are averaged, and averages are compared across models. This form has been enormously productive, and its productivity depends on a condition that is rarely examined: that a single correct answer exists, is knowable in advance, and can be written down.

For a substantial part of the material the humanities work on, that condition is contestable. A benchmark that asks a model to date a manuscript, identify a saint from iconographic attributes, or determine the rhetorical structure of a petition is not merely posing a hard question; it is asserting that the question has one answer. Sometimes it does. Often the discipline that studies the object treats the disagreement between specialists not as a failure of measurement but as information about the object — the reason critical editions record variants, and catalogue records carry attributions with qualifiers.

This paper does not argue that benchmarks are wrong to fix reference answers. It asks a prior, empirical question: **when humanities material enters a benchmark, what happens to it?** Who produces the reference answers, how many answers does the scoring accept, what does the benchmark ask about, and — where the papers themselves provide the evidence — how much does the reported score depend on those choices rather than on the model?

Our contribution is threefold.

**A census.** We identify, screen and describe 42 benchmarks that evaluate generative language models on digital humanities material with quantitative metrics, published between 2021 and 2026. For each we record a fixed set of properties, chosen so that every one is something the paper *states* rather than something a coder must judge (Section 3.3).

**An empirical link between construction and result.** Existing critiques of benchmarking argue that benchmarks measure less than they claim (Raji et al., 2021; Bowman & Dahl, 2021), a maturing methodological literature works out when benchmark measurements are and are not valid (Hardt, 2026), and a parallel literature argues that annotator disagreement carries signal rather than noise (Uma et al., 2021; Plank, 2022). We connect the two using the benchmark papers' own experiments: nine of the 42 report what happens when the same models are scored on the same material under a different regime, and in all nine the score moves substantially (Section 4.3). The papers that never run this check are disproportionately the ones whose format is most closed.

**A declared method and a maintainable artefact.** The search strategy, the inclusion criteria and the extraction schema are reported in full, including the points at which they failed. Every figure in Section 4 is recomputable offline from the released records by a single script, and Section 6 describes how the census is updated as new benchmarks appear.

The paper proceeds as follows. Section 2 situates the work in the existing literature. Section 3 states the operational definitions and inclusion criteria (3.1), the search and screening procedure (3.2), and the extraction schema (3.3). Section 4 reports the findings, and Section 4.7 states what the data does not license. Section 5 concludes, and Section 6 describes maintenance.

---

## 2. State of the art

*[This section is intentionally left to be written. It should survey existing reviews and position papers on the evaluation of large language models for digital humanities, humanities and cultural heritage, and position the present census against them.*

*Two anchors are already identified. Hutchinson (2026) is the closest prior work: a discussion paper examining LLM performance on historical reasoning across five benchmarks, which proposes a four-dimensional framework — contamination resistance, content diversity, format diversity, epistemological sophistication — and reports a collapse from over 90% accuracy on multiple-choice items to 16% reliability on interpretive synthesis. Its "format diversity" dimension anticipates the finding we report in Section 4.3 from a different corpus and a different method, and the relationship between the two should be stated explicitly here. Kang et al. (2025) illustrates the second anchor: a humanities-and-social-sciences benchmark that our own search did not retrieve, and therefore evidence about the recall of the procedure in Section 3.2 rather than about the field.*

*The section should also address why a census of this kind has not previously been assembled, and whether the general benchmark-critique literature (Raji et al., 2021; Bowman & Dahl, 2021) has been taken up in digital humanities venues.]*

---

## 3. Methodology

### 3.1 Operational definitions and inclusion criteria

The census is delimited by four criteria. Each is stated here as it was applied, together with the decisions that the criterion left open and how those were resolved.

**Benchmark.** We include a resource only if it defines a fixed evaluation set together with a scoring procedure that yields quantitative metrics. This excludes qualitative probes, demonstrations, and datasets released without an evaluation protocol; it includes shared tasks, where the task definition and the scoring script constitute the benchmark. A resource qualifies whether or not its authors use the word "benchmark". The operative test is whether an independent party could re-run the evaluation and obtain a comparable number.

**Large language model.** We include a benchmark only if it evaluates at least one generative language model — a model that produces text (or text conditioned on other modalities) rather than assigning labels from a fixed head. Vision-language models are included on the same basis. Encoder-only classifiers appear in several of the included papers as baselines, which is not sufficient on its own: the generative model must be among the systems the benchmark is designed to assess.

**Digital humanities scope.** This is the criterion that required the most deliberation, because "digital humanities" can mean two different things, and the two select different corpora.

Read as a set of *methods*, DH names computational approaches to humanistic material — the sense in which humanities computing has historically been bound together by "a common interest in methods, methodology, tools and technology" rather than by shared subject matter (Svensson, 2009). Read as a *domain*, DH names the subject areas themselves: history, literature, philosophy, art history, classics, religious studies. The distinction is not merely terminological, and the tension between the two readings is long-standing in the field's self-definition (Terras et al., 2013).

We adopt the **domain** reading, for a reason internal to the object of study. A methods reading would have selected benchmarks by the techniques they employ, which for language-model evaluation is nearly constant across the corpus — the technique is prompting a model and scoring its output. It would have discriminated almost nothing. The domain reading asks instead whether the *material* being reasoned over belongs to the humanities, which is the property that the questions of this paper actually concern.

Operationally, a benchmark is in scope if its material falls in one or more of the subject areas that constitute the humanities. We took the reference vocabulary from the Scopus All Science Journal Classification (ASJC), a scheme of four broad areas subdivided into roughly 334 minor fields, assigned to serials by in-house experts on the basis of aims, scope and published content (Elsevier, 2025). Its relevant top-level area is named *Arts and Humanities*; we keep that label when naming the scheme, and use *digital humanities* for the field whose material and questions this census is about. The areas represented in the resulting corpus are History, Language and Linguistics, Visual and Performing Arts, Religious Studies, Cultural Studies, Philosophy, Literature and Literary Theory, Music, Classics, Museology, Archaeology and Conservation.

Two consequences of this choice must be stated. First, the domain reading admits general-purpose benchmarks that contain humanities material among much else — MMLU and its descendants (Hendrycks et al., 2020; Zhang et al., 2023; Singh et al., 2024) — and those turn out to behave as a distinct block (Section 4.4). Second, the subject labels recorded per paper are *not* usable as a count of disciplinary coverage, for reasons we set out in Section 4.7; they delimit the corpus but do not measure it.

**English language.** We include benchmarks that evaluate in English, whether monolingual or as one language among many. Multilingual and non-English-centred benchmarks are included when English is among the evaluated languages. This criterion was applied at screening and, having proved constant across every candidate that passed the other three, does not discriminate within the final corpus.

**Recency.** A fifth condition was applied with deliberate laxity. The census targets benchmarks published after March 2023, the point from which general-purpose generative models became the standard system under evaluation. One earlier benchmark, MMLU (Hendrycks et al., 2020), is retained despite failing this criterion because the corpus cannot be described without it: seven of the eight general-purpose benchmarks are its descendants. Its inclusion is a documented exception, not an oversight, and it contributes to all counts reported below.

### 3.2 Search and census

The corpus was assembled in three stages: source identification, machine-assisted screening, and independent double verification.

**Stage 1 — source identification.** Candidate records were drawn from three kinds of source, chosen to be complementary rather than exhaustive.

*Model system cards.* The evaluation suites reported in the system cards of frontier model providers were mined for benchmarks with humanities content. This source captures precisely the benchmarks that carry comparative weight — those a provider chooses to report — and it is the reason the general-purpose block is well represented.

*Digital humanities venues.* Programmes and proceedings of DH and computational-linguistics venues publishing humanities work were searched directly, including LT4HALA, the workshop on NLP and Language Models for Digital Humanities, CLEF/JOKER, SemEval, and CLRel. This source captures small, purpose-built benchmarks that provider system cards never mention.

*Keyword search.* Topic queries combining benchmark and evaluation terms with humanities and cultural-heritage terms were run against bibliographic indices, with records exported from OpenAlex — a fully open index of scholarly works whose coverage at the time of its release stood at 209 million works, and which was created as a replacement for the discontinued Microsoft Academic Graph (Priem et al., 2022). OpenAlex was chosen for its openness and its inclusion of book-form outputs, which matter disproportionately in the humanities. Its subject labelling is an automated hierarchical classifier over roughly 65,000 Wikidata concepts rather than a curated scheme like ASJC (Priem et al., 2022), so it was used to retrieve records, not to delimit them; the subject-area judgement was made by the reviewers.

**Stage 2 — machine-assisted screening.** The exported records were screened with ASReview, an open-source framework for active-learning-assisted systematic review (van de Schoot et al., 2021). ASReview implements a researcher-in-the-loop cycle: the reviewer labels one record as relevant or irrelevant, that label retrains a classifier, and the classifier re-ranks the remaining unlabelled records so that the next record presented is the one the model considers most likely to be relevant. Screening proceeds until the reviewer applies a stopping criterion; the software supplies no automatic stopping rule, so the criterion is a methodological choice that must be reported. In the simulations reported with the tool, this procedure retrieved 95% of eligible studies after screening between 8% and 33% of records (van de Schoot et al., 2021).

Two properties of this arrangement matter for the validity of what follows. Inclusion and exclusion decisions were made **manually** throughout: the classifier determines the *order* in which records are presented, never the outcome. No record was excluded on a machine assessment alone. This is the distinction that PRISMA 2020 item 8 requires reviewers to report — whether records were excluded on machine assessment alone, or whether machine output only prioritised human decisions (Page et al., 2021). Ours is the latter.

The cost of the arrangement is equally specific. Because screening stops before the pool is exhausted, ML-assisted screening trades recall for effort, and the recall achieved depends on a stopping decision. We did not pre-register a stopping rule, and this is a genuine limitation of the census rather than a formality: HSSBench (Kang et al., 2025), a humanities and social sciences benchmark for multimodal models, satisfies every inclusion criterion above and is absent from the corpus. It is direct evidence that the search has imperfect recall, and it is reported here rather than in a limitations paragraph because any claim of the form "the field does X" inherits that imperfection.

**Stage 3 — independent double verification.** Every record surviving screening was then read in full by two reviewers working independently, each recording an accept/reject decision and a free-text note against the criteria in Section 3.1. Disagreements were resolved by discussion against the paper text. This stage is the reason the corpus is small: it is bounded by reading capacity, not by search.

**Initial cataloguing metadata.** Each accepted record was catalogued with a fixed schema before any automated extraction, comprising: the benchmark name; the article URL; the publication year; the resource URL for the benchmark or dataset itself, where released; the modalities; a free-text description of the domain; the evaluation metrics as stated by the paper; a yes/no humanities judgement; the ASJC area or areas; the source through which the record was found; the identifier of the reviewer who found it; and the two independent accept decisions with their notes. This schema is deliberately thin. It records what a reader can establish from the paper's front matter and what the screening process itself produced — provenance and decisions — leaving every substantive property of the benchmark to the extraction stage, where it is recorded with a controlled vocabulary and an evidence field.

**Outcome.** Forty-five records passed double verification. Three could not be retrieved as full text (EXAMS-V, IRLBench, MultiBLiMP 1.0) and were excluded; all three are multilingual benchmarks, so their absence bears specifically on the community-dependence counts of Section 4.6. The census therefore describes **42 benchmarks**, of which at most 41 are distinct: VULCA-BENCH is represented by two separate papers, a duplication we retain deliberately and exploit in Section 4.7.

### 3.3 Information extraction

Descriptions were extracted from the full text of each paper by a three-agent procedure, then aggregated offline.

**Two readers and an adjudicator.** Each paper is read independently by two extraction agents given different backgrounds — one framed as a humanities scholar, one as a machine-learning researcher — which produce the same fields without seeing each other's output. A third agent adjudicates the two reports against the paper text and writes the final record, noting the disagreements it resolved. The two independent readings are retained alongside the adjudicated record, so inter-reader disagreement can be measured after the fact rather than being erased by adjudication.

**Properties, not categories.** The schema's central design decision was to stop asking for the judgement the survey exists to investigate. An early version asked the readers to assign each benchmark one or more *analytical task types*. Three pairs of terms proved impossible to separate non-arbitrarily — visual recognition against visual reasoning, interpretation against cultural reasoning, attribution against classification. Recognising Saint Jerome from the lion and the cardinal's hat is either visual recognition or iconographic inference depending on a theoretical position about where perception ends and interpretation begins.

Coding that boundary by stipulation would have been circular. If the instrument decides in advance that iconographic recognition is not interpretation, then finding that benchmarks test little interpretation is not a result: it is the definition, returned as a finding. There is also a performative problem specific to this paper. Its argument is that benchmarks reduce hermeneutic operations to closed categories and single-answer formats; measuring that with an instrument performing the same reduction weakens the form of the argument, not merely the data.

The schema therefore asks for **observable properties of construction** in place of contested categories. Rather than "is this task interpretation?", it asks where the reference answer came from; whether answering requires knowledge absent from the stimulus; whether the target is a property of the artefact's genesis rather than its content; whether correctness is treated as varying by community; how many answers the scoring accepts; and how the paper treats disagreement. Each is a fact the paper states. The contested boundaries are then recovered *a posteriori* by grouping benchmarks in the space of these properties, which makes the grouping revisable at no cost and inspectable by a reader who does not share it.

**Closed vocabularies with free-text evidence.** Fields that must aggregate use closed vocabularies; each is accompanied by a free-text field carrying the paper's own wording and the evidence for the values assigned. Task labels use a controlled list of 22 identifiers derived by clustering the 235 free-text labels an earlier ungoverned run produced, not specified a priori. All extracted values are checked against the closed vocabularies after extraction; the final corpus contains no vocabulary violations, and all 22 task identifiers are used.

The free-text evidence field is not ornamental. On one paper the readers selected `existing_metadata` for the source of the reference answers — the closest available value — while the evidence field correctly reported that the items came from practice exams and textbooks. A GRE answer key and a museum catalogue record do not carry the same kind of authority, and conflating them would have silently weakened the schema's most load-bearing variable. The distinction between `existing_metadata` and `authored_answer_key` was added in response, and the corpus re-extracted.

**`not_stated` is a measurement.** Every closed vocabulary distinguishes "the paper does not say" from "no". A benchmark that does not report how its ground truth was produced is itself a finding, and the rate of `not_stated` per property is a reportable result rather than missing data.

**Incremental extension.** New fields can be declared between runs; cached papers extract only the fields they lack and merge them, leaving established values untouched. The results axis reported in Section 4.3 was added this way, after the construction axis was complete, without re-extracting anything else.

**A failure of this procedure, uncorrected.** The extraction reads the full text of a retrieved PDF. For five of the 42 papers, the retrieved file is not the paper but a landing page: an IEEE Xplore record for CHVM-1K (892 characters of extractable text), a NeurIPS abstract page for HiST-LLM (3,225), a GitHub page for SimpleQA (10,913), an ACL Anthology record for DRISHTIKON (11,753), and a project page for the RISE benchmark (28,186). The median for the other 37 papers is 59,571 characters. These five were described from whatever the landing page contained. The consequences are traced in Section 4.7; we report the failure here, in the methods, because it is a property of the procedure and not of the field.

---

## 4. Findings

All figures below are recomputable from the released records without further model calls. Statistical tests are two-sided Fisher exact tests on 2×2 tables, with absolute counts always reported. With *n* = 42 these do not support inference to the field: a *p*-value here indicates whether a difference is distinguishable from chance within this corpus, not whether it generalises.

### 4.1 What the corpus contains

The 42 benchmarks are recent: one from 2021, two from 2023, nine from 2024, nineteen from 2025 and eleven from 2026. Thirty of the 42 appeared in the last two years.

Twenty-three are text-only and seventeen combine image and text. Audio appears in two and video in one. Multimodality has arrived, but almost entirely as still images.

Sizes span four orders of magnitude: the median benchmark has 3,028 items, the smallest 100 and the largest 589,764. Ten have fewer than a thousand items and four have more than a hundred thousand. Most are artisanal objects built by a single research group; a handful are infrastructure.

Grouping the 22 controlled task identifiers into seven families — a grouping we impose and report as such — declarative knowledge and cultural reading cover 25 benchmarks each, language 19, reasoning and document work 18 each, vision 16, and agentic tool use 3. The median benchmark exercises four of the 22 identifiers.

Accuracy is the headline metric in 21 of the 42, with F1 in three, BLEU in two, and a bespoke or composite metric in six; seven report no single headline figure. This matters for what follows: half the corpus reduces its outcome to a proportion of exactly-correct responses.

Evaluation is overwhelmingly of the model as it comes: nineteen benchmarks evaluate zero-shot, nineteen across multiple regimes, three few-shot, and exactly one principally evaluates models fine-tuned on the task.

The systems evaluated are concentrated. **Thirty-eight of the 42 benchmarks (90%) evaluate at least one OpenAI model**, against 23 for Google, 20 for Anthropic, 15 for Alibaba's Qwen family and 13 for Meta's Llama. What is known about the humanities capabilities of language models is largely what is known about one provider's models.

Across the 21 benchmarks reporting accuracy — the only directly comparable subset — the best model scores range from 13.4 (Humanity's Last Exam; Phan et al., 2025) to 93.0 (AdMIRe; Pickard et al., 2025), with a median of 61.8. The dispersion, not the ranking, is the finding: the field simultaneously produces evidence that models nearly saturate humanities tasks and evidence that they fail them, and what separates the extremes is not the difficulty of the material but how tightly the question is drawn.

[[figure:scores]]

**Figure 1.** Best reported model score on the 21 benchmarks whose headline metric is accuracy — the only subset on a common scale. The other 21 report F1, BLEU, CER, a bespoke metric, or no single figure. This is deliberately not a ranking: each benchmark defines its own task, and a 90% on Christian iconography and a 13% on Humanity's Last Exam measure incommensurable things. What the figure shows is the spread, and that the two ends of it are produced by the same field in the same two years.

Size is not merely a matter of cost, because it sets a floor on what a benchmark can detect at all. Distinguishing two models that differ by ε requires on the order of 1/ε² items, so a benchmark of *n* items resolves differences of roughly 1/√n and no finer (Hardt, 2026). Applied to this corpus: of the 40 benchmarks declaring a size, **14 are large enough to resolve a one-point difference** (10,000 items or more), 22 can resolve two points, and ten fall below a thousand items and therefore cannot distinguish differences smaller than about three points. The smallest, a 100-item corpus of parole hearings, resolves nothing finer than ten. This does not invalidate those benchmarks — a 100-item expert-annotated corpus can be exactly the right instrument for a question — but it does mean that model comparisons reported to one decimal place on small benchmarks are reporting noise, and it bears directly on how the dispersion in Figure 1 should be read.

[[figure:resolution]]

**Figure 2.** The ten benchmarks with fewer than a thousand items, showing what each can actually resolve. The bar is not a score: it is the smallest difference between two models the benchmark is capable of detecting, derived from its size alone. A one-point gap reported on the parole-hearings corpus is indistinguishable from no gap at all.

### 4.2 Where reference answers come from, and how many are accepted

Reference answers come from crowd annotators in nine benchmarks, from disciplinary experts in nine, from pre-existing exam or textbook answer keys in eight, and from curatorial or catalogue metadata in six. Three derive them from a model and one from the authors. **Six of the 42 do not state where their ground truth came from** — a substantial omission on material where the provenance of interpretive authority is the question at issue.

The choice tracks what the benchmark claims to measure. Where the benchmark is designed to assess disciplinary competence, 13 of 23 draw on experts or curatorial metadata; where humanities material serves as content for a general capability, 2 of 17 do (57% against 12%; *p* = 0.004). Restricting to the 32 purpose-built benchmarks, excluding the general-purpose block, strengthens the association rather than weakening it (12 of 18 against 2 of 14; 67% against 14%; *p* = 0.004). Conversely, content-role benchmarks fall back on crowd annotation and answer keys in 10 of 17 cases against 6 of 23 (*p* = 0.032). Two economies of truth operate side by side, and they produce objects that resemble one another only superficially.

This convergence is also the only internal evidence that the disciplinary-role judgement was not arbitrary: the role is an interpretive judgement made by the readers, the source of the gold is an observable property of dataset construction, and the two were extracted in independent passes under different schemas.

Turning to scoring: 28 of the 42 accept a single answer per item, five accept an enumerated set, five use graded human or model judgement, and four do not state. Crossing this with whether answering requires knowledge absent from the stimulus yields the central count of the census. **Twenty-one benchmarks — exactly half the corpus — pose questions whose correct answer must be inferred from outside the stimulus, and score the result against a single key.** They require interpretation and accept one interpretation.

[[figure:crosstab]]

**Figure 3.** How many answers the scoring accepts, against whether answering requires knowledge absent from the stimulus. Both properties are verifiable in the stated evaluation protocol, and neither asks the coder to judge whether a task is "really" interpretive. The top-left cell is the census's central count: the benchmarks that demand inference and admit one result.

Those 21 are not evenly distributed: they are 8 of the 8 general-purpose benchmarks and 13 of the 34 purpose-built ones (38%). This is a property of the large benchmarks rather than of the field as a whole, for reasons Section 4.4 makes explicit.

### 4.3 When the instrument changes, the score changes

Nine benchmarks in the corpus ran an experiment more decisive than any argument: they evaluated the same models on the same material while changing only how the score was assigned. **All nine obtained two different scores.** The median gap is 31 percentage points; the largest is 88.

The clearest case is EduArt (Spinaci et al., 2026), which evaluates models on art-history exercises drawn from Italian and United States secondary examinations. The same models exceed 94% when choosing among options, fall to 23.9% on open completion, and to 6.2% on error identification. The material did not change; the shape of the question did. That 94% does not measure a competence that subsequently evaporates — it measures recognition among alternatives, which is an easier and different thing. CulturalBench (Chiu et al., 2024) reports a 53-point drop between multiple-choice and binary formats on the same 1,696 questions; Appear2Meaning (Jiang et al., 2026) reports partial-match rates of 0.735 against exact-match rates of 0.000 on the same items; VULCA-BENCH (Yu et al., 2026a) reports a 40-point decline between surface perception and cultural interpretation tiers of its own taxonomy.

The result bears directly on the construction axis. **Among the 28 benchmarks that accept a single answer, two ran this check; among the 14 that already admit more than one answer, seven did** (7% against 50%; *p* = 0.003). The benchmarks whose format is most closed are also those least likely to test whether the format is doing the work.

Two qualifications constrain the claim. First, the 18 benchmarks that report no such comparison did not compare two instruments and find them equivalent; they did not compare. A null result would rarely be published, so "nine of nine" means nine of nine among those that looked, and is a lower bound in both directions. Second, a further twelve benchmarks report gaps of comparable magnitude (median 34 points) by varying the *items* — a harder subset — or the *input representation*, rather than the instrument. Those are findings about model fragility, not about measurement, and we keep them separate; the separation is our reading of the papers' own reported evidence and is documented as such.

**This is not a humanities peculiarity, and that matters.** The same sensitivity is documented in mainstream machine-learning evaluation, where changing a single delimiter in a prompt template has been reported to swing MMLU accuracy by 23 points, and where measured performance is held to depend substantially on evaluation design — prompt formatting, answer presentation, adaptation budget — rather than on a stable underlying capability (Hardt, 2026). Our contribution is not to discover the phenomenon but to locate it: on humanities material the choice that moves the score is not a formatting detail, it is a decision about how many readings of an object count as correct.

**A robustness check the previous paragraph requires.** If a benchmark is too small, a reported gap could be sampling noise rather than a property of the instrument. Taking each benchmark's own resolution floor from Section 4.1, all nine gaps exceed three times the smallest difference their benchmark can detect — the tightest case being CzechTopic, whose 10-point gap sits against a 2.3-point floor on 1,820 items. None of the nine is an artefact of a small test set.

[[figure:gaps]]

**Figure 4.** The nine benchmarks that measured the same material two ways, showing the gap each reports and what was varied to produce it. The dark tick on every bar is that benchmark's own noise floor from Figure 2: in all nine cases the gap clears it several times over, so none of these is a small-sample artefact. The task, the items and the models are held fixed throughout; only the rule for awarding the score changes.

A third observation belongs here. Only 13 of the 42 benchmarks measure a human baseline at all, and nine quantify the gap. In two of those nine the model exceeds the human — both agentic search tasks, where the human is constrained by time rather than by competence.

[[figure:human]]

**Figure 5.** The nine benchmarks that quantify a human baseline, as points separating the best model from the human. Two are negative. Both are agentic retrieval tasks in which the human reference was working under a time limit, which makes them measurements of patience rather than of judgement — a reminder that a human baseline is itself an instrument with a construction, and that most of the corpus does not build one at all.

### 4.4 The general-purpose block

Eight benchmarks in the corpus are general-purpose: MMLU (Hendrycks et al., 2020) and its descendants. They are the largest, the most cited, and the ones that appear in provider system cards and fix comparative rankings. They have one shape, with no variance.

Seven of the eight take their reference answers from pre-existing exam or textbook answer keys, against 1 of the other 34 — a difference of 85 percentage points and the largest effect in the corpus (*p* < 0.001). All eight accept a single answer, against 20 of 34 (*p* = 0.027). Their median size is 21,218 items against 1,758 for the purpose-built benchmarks that declare one.

Size alone, however, does not predict format: among benchmarks with at least 20,000 items, 67% accept a single answer, against 68% of the rest (*p* = 0.31). What is large is closed because it is general-purpose, not because it is large — a distinction that matters because it locates where intervention would be effective.

There is also a formal reason to distrust what these eight report. Aggregating many subject areas into one number is a voting problem — tasks are voters, models are candidates — and Arrow's impossibility theorem applies: a multi-task benchmark that satisfies unanimity and independence of irrelevant alternatives must be a single-task benchmark in disguise (Hardt, 2026). Empirically, the matrix of benchmark scores by model turns out to be close to low rank, with its first principal component tracking pretraining compute. A general-purpose benchmark that reports a humanities subscore is therefore doing something more fragile than it appears: the subscore is one voter in an aggregation with no non-arbitrary rule, over a corpus whose dominant axis of variation may not be subject competence at all.

The asymmetry this produces is structural. Comparative visibility concentrates where the reference answers come from assessment keys and the scoring accepts one response; experimentation with formats sits in small, recent benchmarks that nothing uses as a comparative reference.

### 4.5 What the corpus reports about models

Beyond individual scores, one pattern recurs across independent benchmarks. Among the 24 benchmarks covering more than one culture or language — those for which the question arises — **17 report a systematic performance asymmetry as a finding**: Western-centric bias, degradation on low-resource languages, or worse scores on a named region. Seven report no such difference.

The field, in other words, is capable of measuring cultural asymmetry and does so routinely. What does not follow is the further step: observing that a model performs worse on one culture is not the same as allowing that the correct answer might vary with culture. On that question the corpus stands at four benchmarks out of 42.

### 4.6 What the corpus does not ask

The preceding sections concern how benchmarks measure. This one concerns what they ask about, and it is read in the absences. These are counts, not associations: no tests, and the list is the evidence.

**The genesis of artefacts: 3 of 42.** Date, author, place of origin, provenance, material history — the operative core of philology, art history, archaeology and codicology — are the target of Appear2Meaning, EduArt and Hanfu-Bench. Every other benchmark evaluates the *content* of objects rather than their history. This is the largest gap in the corpus and also the most tractable: these are tasks where evidence is incomplete by nature and competing hypotheses are the norm, which is precisely the terrain on which single-answer formats do not function.

**Community-relative correctness: 4 of 42.** The corpus is full of avowedly multilingual and cross-cultural benchmarks, but being multilingual while maintaining a universal answer key is the norm: the question is translated, the answer is not permitted to change. The field's cross-cultural work is predominantly *translational* rather than relativist. Read alongside the 71% of benchmarks that *detect* cultural asymmetry (Section 4.5), the picture is sharp.

**Audio or video: 2 of 42.** Ethnomusicology, film studies, performance studies and oral history are outside the frame.

**Graded scoring: 5 of 42.** Graded human or model judgement is the only format that structurally admits degrees of correctness. It covers an eighth of the corpus, and all five cases are generative or critical tasks.

These are not defects of the individual benchmarks, none of which promised to cover attribution or ethnomusicology. They are the shape of the field seen in negative, and they indicate what to build rather than diagnosing what exists.

### 4.7 How far these numbers reach

**Disciplines are not countable from this data.** It would be natural to ask how many benchmarks cover art history, how many philosophy, how many archaeology. The recorded ASJC areas do not support that count, for two independent reasons. First, the labels are not commensurable: a general-purpose benchmark declares the dozens of examination subjects it contains, while a monothematic benchmark declares its single discipline. Summing them equates "contains music questions among 57 subjects" with "is a music benchmark". Concretely, the five occurrences of "Music" in the corpus belong to LongFact, MMMU-Pro, Humanity's Last Exam, SuperGPQA and BrowseComp; none is a music benchmark and three are general-purpose. Second, this is the one list field left outside the vocabulary check: it contains "Archaeology" and "Archeology" as distinct entries through a typographical error, alongside values outside the declared ASJC list. The two papers describing the same benchmark received one area and four respectively. Section 4.1 therefore describes what benchmarks *do* — task families, modalities, both drawn from validated closed vocabularies — and not which discipline they belong to.

**Half the corpus is silent on disagreement.** The most theoretically loaded property in the schema records how a paper treats divergence between annotators or between defensible readings. Twenty of the 42 address it: nineteen treat it as noise to be reduced, one as information about the material, and 22 do not mention it. Every crosstab involving this variable therefore runs on roughly twenty cases rather than 42, without the denominator saying so, which is why no percentage involving it appears in Sections 4.1–4.6. What does hold is that the silence is disappearing: in 2026, nine of eleven papers say something, against 11 of 31 in earlier years (*p* = 0.009). That it is being replaced principally by explicit minimisation is what the data show, but on eleven cases this is an observation rather than a trend.

**Five papers were described from landing pages, not papers.** As reported in Section 3.3, the extraction for CHVM-1K, DRISHTIKON, SimpleQA, HiST-LLM and the RISE benchmark ran over a retrieved landing page rather than the article. The effect is visible and consequential. CHVM-1K and DRISHTIKON are `not_stated` on all six construction properties and SimpleQA on five — and on the basis of that pattern they would appear to be unusually reticent papers. They are not; they were not read. Any reading of those three as evidence about disclosure practice is an artefact of our retrieval step. Because these three share the same value across every property, they also manufacture association: the relation between community-relative correctness and artefact genesis measures Cramér's *V* = 0.71 with them included and 0.10 with `not_stated` excluded. Net of that artefact the construction properties are largely independent of one another, which is what a multi-axis instrument should be. We have not re-run the extraction for these five, and the corrected values should be obtained before any of the affected counts are used further.

**The only external reliability estimate available is 4 of 6.** The corpus contains two distinct papers describing VULCA-BENCH (Yu et al., 2026a, 2026b). The pipeline read them as separate objects, producing an unintended test-retest. They diverge on two of the six construction properties — whether correctness is community-relative, and how many answers the scoring accepts — as well as on the evaluation regime, the declared size (6,804 against 7,410 items) and the disciplinary areas (one against four). Agreement: four of six. This should be read against the agreement between the two extraction readers, which runs at 36 to 41 of 42 depending on the property — but the two figures measure different things. The two readers process the *same text*, so their agreement measures how far two prompts converge, and a closed vocabulary obliges them to converge. The two VULCA papers are *different texts about the same object*, so their divergence measures how far the coding depends on how a paper is written. It is a single case and an anecdote, but it is the only external reliability estimate the project has, and it suggests the true figure is nearer 4 of 6 than 40 of 42.

**Corpus integrity and upstream limits.** Forty-two files describe at most 41 distinct benchmarks. Seven papers name no benchmark and are recorded under the title assigned at cataloguing. MMLU is included although it predates the recency criterion (Section 3.1). Three verified records were excluded for want of full text, all three multilingual, which bears specifically on Section 4.6. Above all, the search has documented imperfect recall (Section 3.2), and the extraction has **not** been validated against human coding: two readers agreeing with each other is not two readers being right, and a closed vocabulary can make them converge on an error. A hand-coded subset compared against the pipeline output is the step that remains before any percentage here is used as an established figure.

---

## 5. Conclusions

The census supports three claims and one recommendation.

**The measured competence of a model on humanities material is a joint property of the model and the format that interrogates it.** This is not an inference from theory but a report of experiments the benchmark papers ran themselves: nine benchmarks measured the same material under two scoring regimes and all nine obtained different results, by a median of 31 points. Where the field reports that models perform well on humanities tasks, the format is doing part of that work, and the amount is measurable — but only where someone measures it. The benchmarks least likely to measure it are those whose format is most closed (*p* = 0.003). Reporting a single headline number without a second regime is, on this evidence, reporting an unknown quantity.

**The strongest objection to the first claim, and our answer to it.** There is a principled defence of benchmarking that our result appears to threaten and does not. Absolute benchmark numbers are known not to replicate; what replicates is the *ordering* of models, and that ordering is enough to run competitive empirical testing, which is what benchmarks are for (Hardt, 2026). On this view a 31-point swing in a reported score is unsurprising and largely harmless, because nobody should have believed the cardinal number in the first place.

We accept the distinction and think it fails to rescue this corpus, for three reasons. The first is empirical: ordinal stability is itself conditional on equalising what each model brought to the test, and none of the 42 benchmarks does this — the same source identifies the large-language-model era, where preparation differs wildly across competitors, as precisely where ranking stability broke down. The second is about use: these benchmarks do not circulate as rankings. Twenty-one of the 42 report a headline accuracy, and those cardinal numbers are what gets quoted as evidence of what models can do with humanities material. A defence that concedes the absolute numbers while the field reports and cites them is a defence of a practice nobody is following. The third is the one we care about. The ordinal defence is *metrological*: it concerns whether a measurement is stable. Our claim is *epistemic*. A perfectly stable ranking computed against a gold standard that fixed one reading of an iconographic attribution as correct is stable and is still not a measurement of disciplinary competence — it measures agreement with whoever wrote the key. That same source draws the line in the same place, warning that benchmarks should not be used to measure latent constructs such as ability or skill (Hardt, 2026). A benchmark claiming to assess disciplinary competence is doing exactly that.

Two further points of contact are worth recording, one supporting and one limiting. The formal framework underlying benchmark evaluation assumes a single label per item — the target *y* determined jointly with the features *x* — an assumption its own author grants is met by almost no real dataset. Our plurality facet is a survey of how often that assumption is defensible on humanities material, and half the corpus does not discuss it. Against that, the chapter of that book devoted to labelling and annotation is not available in the open edition we consulted; it is the chapter closest to the question we raise, and we cannot report whether it anticipates or contradicts us.

**Two economies of truth are operating, and prestige is attached to the wrong one.** Benchmarks that set out to assess disciplinary competence pay for disciplinary expertise; those that use humanities material as content for a general capability fall back on crowd annotation and examination keys. The association is robust and survives every stratification we applied. But comparative visibility sits almost entirely with the second economy: the eight general-purpose benchmarks are twelve times larger by median, take their answers from assessment keys in seven cases of eight, and accept a single answer in all eight. Experimentation with evaluation formats is happening in small, recent, purpose-built benchmarks that nothing uses as a comparative reference.

**The operations that define the historical disciplines are almost absent.** Dating, attribution, provenance and material history — what philology, art history, archaeology and codicology actually do — are the target of three benchmarks out of 42. The field has imported from the humanities those questions that resemble reading comprehension and visual recognition, and left out those requiring inference about how an object came to be.

The recommendation follows from the conjunction of the first and third claims. The gap is not merely a matter of coverage. Attribution and dating are tasks where the evidence is incomplete by construction and where competing hypotheses are the normal state of knowledge — exactly the conditions under which a single-answer format misdescribes the task. A benchmark for artefact genesis that scored against one key would reproduce, on the most epistemically delicate material available, the reduction this paper documents. Building in this space therefore requires the two moves together: taking on the operations the field has avoided, *and* adopting scoring that admits enumerated answer sets, graded judgement, or explicitly plural gold — the arrangements that a substantial literature on annotator disagreement has already worked out (Uma et al., 2021; Plank, 2022), and that five benchmarks in this corpus already use.

We add one methodological conclusion drawn from our own procedure. The most useful thing the schema did was to stop asking whether a task is "interpretive" and start asking where its reference answers came from. The first question is the one the survey exists to investigate, and coding it directly would have returned the definition as a finding. The second is a fact the paper states. That substitution — closed vocabularies for what must aggregate, free-text evidence beside it for what must not be lost, and contested boundaries recovered afterwards by grouping — is transferable to other surveys whose object is contested in the same way.

---

## 6. Maintenance

This census is designed to be a living resource rather than a snapshot, because its object is moving: thirty of the 42 benchmarks appeared in the two years before writing. Maintenance has four components.

**Adding a benchmark.** A new record is appended to the input catalogue with the Stage 3 metadata of Section 3.2 — name, article URL, year, resource URL, modalities, domain, metrics, humanities judgement, ASJC areas, source, finder, and the two independent accept decisions. Running the pipeline then fetches, extracts and describes only the new record: existing descriptions are cached and untouched. The reporting script recomputes every figure in Section 4 from the full corpus without further model calls.

**Adding a property.** New extraction fields are declared in the schema file and take effect on the next run. Cached papers extract *only* the fields they lack and merge them into their existing records; established values are never recomputed. This is how the results axis of Section 4.3 was added after the construction axis was complete. The exception is a change to the *value set* of an existing field: a distinction absent from a vocabulary cannot be recovered from values already assigned under it, so redefining a vocabulary requires re-extracting the corpus. This happened once, for the distinction between curatorial metadata and authored answer keys (Section 3.3), and it is the only kind of change that carries that cost.

**Re-verification.** Three checks should run on every update. The vocabulary check must report no violations. The retrieved full text of each new paper must be confirmed to be the paper — the failure documented in Section 3.3 was silent, and a simple length and content check catches it. Bibliographic records must be verified against the paper itself rather than accepted from a title match; in assembling this article, four of 38 automatically resolved records were matched to the wrong work, and were caught only by comparing the resolved author and title against the paper's own first page.

**Outstanding maintenance.** Three items are known and open at the time of writing. The five landing-page extractions (Section 3.3) should be re-fetched and re-described, and the counts they affect recomputed. The ASJC area field should be brought under vocabulary control, at which point disciplinary coverage becomes reportable. And a hand-coded subset should be compared against the pipeline output to give the extraction an external validity estimate, which it currently lacks.

---

## References

Bowman, S. R., & Dahl, G. E. (2021). What will it take to fix benchmarking in natural language understanding? *Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies* (2021.naacl-main.385). https://aclanthology.org/2021.naacl-main.385/

Chiu, Y. Y., Jiang, L., Lin, B. Y., et al. (2024). CulturalBench: A robust, diverse, and challenging cultural benchmark by human-AI CulturalTeaming. *arXiv preprint* arXiv:2410.02677. https://arxiv.org/abs/2410.02677

Elsevier. (2025). *Scopus subject areas and All Science Journal Classification (ASJC) codes*. Elsevier Support Center. https://service.elsevier.com/app/answers/detail/a_id/15181/

Hardt, M. (2026). *The emerging science of machine learning benchmarks*. Princeton University Press. https://mlbenchmarks.org/

Hendrycks, D., Burns, C., Basart, S., et al. (2020). Measuring massive multitask language understanding. *arXiv preprint* arXiv:2009.03300. https://arxiv.org/abs/2009.03300

Hutchinson, D. (2026). Benchmarking as source criticism: From recognition to reasoning in LLM assessment. *Journal of Open Humanities Data*. https://doi.org/10.5334/johd.489

Jiang, X., et al. (2026). Appear2Meaning. *arXiv preprint* arXiv:2604.07338. https://arxiv.org/abs/2604.07338

Kang, Z., Gong, J., Yan, J., et al. (2025). HSSBench: Benchmarking humanities and social sciences ability for multimodal large language models. *arXiv preprint* arXiv:2506.03922. https://arxiv.org/abs/2506.03922

Page, M. J., Moher, D., Bossuyt, P. M., Boutron, I., Hoffmann, T. C., Mulrow, C. D., et al. (2021). PRISMA 2020 explanation and elaboration: Updated guidance and exemplars for reporting systematic reviews. *BMJ*, 372, n160. https://doi.org/10.1136/bmj.n160

Phan, L., Gatti, A., Han, Z., Li, N., Hu, J., et al. (2025). Humanity's Last Exam. *arXiv preprint* arXiv:2501.14249. https://arxiv.org/abs/2501.14249

Pickard, T., et al. (2025). AdMIRe: Advancing multimodal idiomaticity representation. *arXiv preprint* arXiv:2503.15358. https://arxiv.org/abs/2503.15358

Plank, B. (2022). The "problem" of human label variation: On ground truth in data, modeling and evaluation. *Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing*, 10671–10682. https://doi.org/10.18653/v1/2022.emnlp-main.731

Priem, J., Piwowar, H., & Orr, R. (2022). OpenAlex: A fully-open index of scholarly works, authors, venues, institutions, and concepts. *arXiv preprint* arXiv:2205.01833. https://arxiv.org/abs/2205.01833

Raji, I. D., Denton, E., Bender, E. M., Hanna, A., & Paullada, A. (2021). AI and the everything in the whole wide world benchmark. *Proceedings of the Neural Information Processing Systems Track on Datasets and Benchmarks 1*. https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/084b6fbb10729ed4da8c3d3f5a3ae7c9-Abstract-round2.html

Singh, S., et al. (2024). Global-MMLU. *arXiv preprint* arXiv:2412.03304. https://arxiv.org/abs/2412.03304

Spinaci, G., et al. (2026). EduArt. *arXiv preprint* arXiv:2607.02007. https://arxiv.org/abs/2607.02007

Svensson, P. (2009). Humanities computing as digital humanities. *Digital Humanities Quarterly*, 3(3). https://dhq.digitalhumanities.org/vol/3/3/000065/000065.html

Terras, M., Nyhan, J., & Vanhoutte, E. (Eds.). (2013). *Defining digital humanities: A reader*. Ashgate.

Uma, A. N., Fornaciari, T., Hovy, D., Paun, S., Plank, B., & Poesio, M. (2021). Learning from disagreement: A survey. *Journal of Artificial Intelligence Research*, 72. https://doi.org/10.1613/jair.1.12752

van de Schoot, R., de Bruin, J., Schram, R., Zahedi, P., de Boer, J., Weijdema, F., Kramer, B., Huijts, M., Hoogerwerf, M., Ferdinands, G., Harkema, A., Willemsen, J., Ma, Y., Fang, Q., Hindriks, S., Tummers, L., & Oberski, D. L. (2021). An open source machine learning framework for efficient and transparent systematic reviews. *Nature Machine Intelligence*, 3(2), 125–133. https://doi.org/10.1038/s42256-020-00287-7

Yu, X., et al. (2026a). VULCA-BENCH: Cross-cultural expert-level art critique evaluation with vision-language models. *arXiv preprint* arXiv:2601.07986. https://arxiv.org/abs/2601.07986

Yu, X., et al. (2026b). VULCA-BENCH: A multicultural art-critique benchmark. *arXiv preprint* arXiv:2601.07984. https://arxiv.org/abs/2601.07984

Zhang, W., et al. (2023). M3Exam: A multilingual, multimodal, multilevel benchmark for examining large language models. *arXiv preprint* arXiv:2306.05179. https://arxiv.org/abs/2306.05179
