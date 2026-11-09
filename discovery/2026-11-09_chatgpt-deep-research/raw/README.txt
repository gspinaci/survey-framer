Census update: generative language-model evaluations on humanities material
Window: 2026-05-01 to 2026-11-09 (inclusive)
Research cutoff: 2026-11-09

Files
- candidates.csv: 30 full-paper-checked candidates, of which 14 are explicitly borderline.
- near_misses.csv: 50 considered exclusions, including earlier first releases.
- unverified.csv: 71 leads whose full text, English use, new-version status or precise first-public date could not be established.
- search_log.csv: 194 recorded search/access batches, with exact queries where available and per-batch final-inventory lead matches.
- paper_checks.json: criterion notes, opened-source references and version/access caveats.

Method
The main table was constructed from opened PDF papers or full HTML papers, not abstract-only search results. English instructions count when actual evaluation instructions are shown or explicitly described. An English translation supplied only for readers does not count. Fixed quantitative evaluation studies and new evaluation protocols on existing corpora are retained where justified; borderline rows identify reproducibility or domain concerns.

Dates are earliest located dated public papers/overviews, not the year of a later venue. Where the only located publication is a proceedings PDF, its explicit proceedings date is used; no earlier preprint was found in title searches. Such rows are medium-confidence. This is not proof that an earlier unindexed public manuscript never existed. Known earlier public benchmark packages were checked where found. Exact-date failures (notably ICCC papers) remain unverified rather than substituting a conference opening date.

A blank PDF field means a direct retrievable PDF was not located; the DSH grammatical-use paper was read in full HTML. CULTURE-MT was checked in full arXiv HTML because its publisher PDF has a content-type retrieval problem. Model names are examples/families where the evaluated list is long; counts, when given, refer to the paper. A paper URL in the Resource column means the protocol is documented there but a standalone package was not established. Main-table inclusion does not guarantee unrestricted public access to every test item.

Scope limitations
The search covers every requested source family, with keyword/title searches and targeted proceedings screening. It is not an exhaustive title-by-title screen of all ACL/EMNLP/LREC 2026 papers or all system cards. NLP4DH (36 abstracts), CHum (8 abstracts), LT4HALA (50 abstracts) and the NakbaNLP (47 abstracts) index were screened. The sign-lang LREC index exposed page 1 (20/52 papers); LLMs4SSH was partial. Broad event indexes and named workshop queries supplement this. OpenReview often returned a browser-verification wall, some arXiv PDFs/HTML returned DisabledError, ACM returned 403, DHQ was inaccessible, and HELM returned no readable index. These are access failures, not evidence that no benchmark exists. NeurIPS 2026 proceedings were not yet available in the searched proceedings index; CHR has no located 2026 edition (next conference is January 2027). No 2026 NAACL/COLING edition was located in the searched indexes. EACL/LaTeCH-CLfL 2026 events were before May.

Search-log counts
Counts are deduplicated named lead matches within each batched retrieval, matched by paper identifier/URL or distinctive title alias to the final inventory. They are not search-engine hit totals and are not a claim that every unlisted search result is irrelevant. A lead can recur in many batches and sources. Queries batched by the search tool return a merged result list, so per-query exclusive attribution is unavailable; the exact batch and its union yield are retained. Source refs are retrieval provenance identifiers, not substitute paper URLs.

Already-known originals supplied in the task were suppressed. New editions (HLE-Diamond, RISE releases, VULCA v2.1 and ProHist-Bench-504) appear only as unverified new-version leads; no old original is counted as new.
