# Analisi dei risultati — 42 benchmark LLM in Arts & Humanities

**Data:** 4 agosto 2026
**Corpus:** 42 paper estratti, zero violazioni di vocabolario. 3 paper del CSV esclusi per PDF non reperibile (EXAMS-V, IRLBench, MultiBLiMP 1.0).
**Strumento:** vedi [METHODOLOGY_facets.md](METHODOLOGY_facets.md) per il disegno delle sfaccettature e [CHANGES_extraction_schema.md](CHANGES_extraction_schema.md) per lo schema di estrazione.

Tutti i numeri qui sono ricalcolabili senza chiamate API con `python scripts/facet_report.py`.

---

## 1. Il risultato che vale il survey

**Su 42 benchmark che valutano LLM su materiale umanistico, uno solo tratta la divergenza interpretativa come informazione.**

| `plurality_treatment` | n | % |
|---|---:|---:|
| `not_stated` — il paper non affronta la questione | 22 | **52%** |
| `noise` — divergenza filtrata, risolta a maggioranza, o riportata come accordo inter-annotatore da minimizzare | 19 | **45%** |
| `signal` — divergenza preservata come informativa sul materiale | **1** | **2%** |

Il 45% che tratta il disaccordo come rumore non è un difetto tecnico: è una scelta epistemologica, e nella maggior parte dei casi non dichiarata come tale. Il 52% di `not_stated` non è un dato mancante — è la misura di quanti paper non considerano la questione degna di menzione.

E il singolo caso `signal` peggiora il quadro invece di attenuarlo. È **CzechTopic**, un benchmark di topic detection, i cui task sono `classification` e `information_extraction`. La pluralità viene preservata dove è metodologicamente economica — etichette tematiche su cui annotatori possono legittimamente divergere senza che nulla di teorico sia in gioco — e non dove è epistemologicamente costitutiva. Nessun benchmark di interpretazione iconografica, attribuzione o critica d'arte tratta la divergenza come segnale.

### Il corollario quantitativo

La crosstab che il campo unico `analytical_tasks` non poteva esprimere, e per ottenere la quale l'asse del formato è stato separato da quello dell'operazione:

| | `gold_beyond_stimulus`=no | =not_stated | **=yes** | tot |
|---|---:|---:|---:|---:|
| `answer_set` | 1 | 0 | 4 | 5 |
| `graded_human_judgment` | 0 | 0 | 5 | 5 |
| `not_stated` | 0 | 2 | 2 | 4 |
| **`single_answer`** | 7 | 0 | **21** | **28** |

**21 paper su 42 — metà esatta del corpus — pongono domande che richiedono conoscenza esterna allo stimolo e le valutano contro una chiave unica.** Richiedono inferenza e accettano una sola risposta. È la riduzione che il survey argomenta, quantificata.

Complessivamente `single_answer` copre 28 paper su 42 (67%). Il giudizio umano graduato, l'unico formato che ammette gradazione, ne copre 5 (12%).

---

## 2. Narrative estraibili dai dati

### A. La chiusura non diminuisce col tempo, aumenta

| anno | n | `noise` | `not_stated` | `signal` | % noise |
|---|---:|---:|---:|---:|---:|
| 2023 | 2 | 1 | 1 | 0 | 50% |
| 2024 | 9 | 3 | 6 | 0 | **33%** |
| 2025 | 19 | 7 | 12 | 0 | **37%** |
| 2026 | 11 | 8 | 2 | 1 | **73%** |

Nel 2026 il silenzio quasi scompare (2 su 11) e viene sostituito da un trattamento esplicito della divergenza come rumore (8 su 11). La lettura ovvia — il campo matura, la consapevolezza metodologica cresce — porta a una conclusione scomoda: **la maturazione metodologica si sta incanalando nella minimizzazione della divergenza, non nella sua valorizzazione.** I paper recenti sanno di dover parlare dell'accordo inter-annotatore, e ne parlano come di un problema da ridurre.

È la narrativa più forte che i dati permettono, perché è controintuitiva e ha una direzione temporale.

### B. Il monolite general-purpose

Gli 8 benchmark general-purpose del corpus hanno **una sola forma**, senza variazione:

| | valore | n/8 |
|---|---|---:|
| `answer_multiplicity` | `single_answer` | **8/8** |
| `gold_beyond_stimulus` | `yes` | **8/8** |
| `gold_source` | `authored_answer_key` | 7/8 |

Zero varianza sulle prime due. Sono i benchmark grandi e citati (MMLU, MILU, M3Exam, MMLU-ProX e affini): il materiale umanistico vi entra come contenuto incidentale, la ground truth viene da chiavi di esami preesistenti, la valutazione è a risposta singola.

I 34 purpose-built mostrano invece dispersione su tutto: `single_answer` 20, `graded_human_judgment` 5, `answer_set` 5, `not_stated` 4; e sette diverse provenienze del gold.

**La narrativa:** la visibilità sta dove le humanities sono materia prima e la forma è rigida; la sperimentazione sui formati sta in benchmark piccoli, recenti, che nessuno usa come riferimento comparativo. L'asimmetria fra prestigio e adeguatezza disciplinare è strutturale.

### C. Due economie della verità

`humanities_role` × `gold_source` divide il corpus in due regimi:

| | `domain_expert` | `existing_metadata` | `authored_answer_key` | `crowd_annotation` | tot |
|---|---:|---:|---:|---:|---:|
| `domain` (competenza disciplinare) | **8** | 5 | 5 | 1 | 23 |
| `content` (materiale come dato) | 1 | 1 | 3 | **7** | 17 |

I benchmark che dichiarano di valutare competenza disciplinare **pagano per l'expertise**: annotatori formati nella disciplina o metadati curatoriali (13 su 23). Quelli che usano le humanities come contenuto ricorrono a crowd e chiavi d'esame (10 su 17).

Questo è anche una **validazione interna dello strumento**: `humanities_role` è un giudizio interpretativo, `gold_source` è una proprietà osservabile della costruzione del dataset, ed erano estratti in passate indipendenti. Che convergano suggerisce che `humanities_role` non era arbitrario.

### D. L'universalismo residuo

`gold_community_dependent` è `no` in **35 casi su 42 (83%)**. Solo 4 benchmark trattano la risposta corretta come variabile per comunità: CulturalBench, VULCA-BENCH, CulturALL, Cultural Long-form Multilingual QA.

Il dato pesa perché il corpus è ricco di benchmark dichiaratamente multilingui e cross-culturali. Essere multilingue e mantenere una chiave universale è la norma: si traduce la domanda, non si ammette che la risposta cambi. Delle 10 aree marcate come Cultural Studies, solo 3-4 arrivano a una correttezza relativa alla comunità.

**La narrativa:** il cross-culturale del campo è prevalentemente *traduttivo*, non *relativista*. Misura se il modello sa la risposta in più lingue, non se riconosce che la risposta dipenda da chi la dà.

### E. Dove la pluralità è costitutiva, è trattata come errore

Il pattern per tipo di task, incrociato con il trattamento della divergenza:

| task | n | % `single_answer` | `noise` |
|---|---:|---:|---:|
| `transcription_and_correction` | 6 | **100%** | 2 |
| `multiple_choice_qa` | 16 | 93% | 8 |
| `logical_and_quantitative_reasoning` | 14 | 92% | 8 |
| `causal_and_temporal_reasoning` | 11 | 90% | 6 |
| `translation` | 7 | 85% | 3 |
| `interpretation` | 11 | 72% | 5 |
| `attribution` | 5 | 40% | **4/5** |
| `generation` | 12 | **33%** | 6 |

Tre letture si sovrappongono qui.

**La trascrizione diplomatica al 100% di risposta singola.** Sei benchmark su sei valutano trascrizione e correzione OCR/HTR contro un'unica lettura corretta. È il caso in cui la pratica disciplinare è più esplicitamente pluralista: la paleografia convive con letture alternative, e le edizioni critiche registrano varianti proprio perché la lettura singola non esiste.

**L'attribuzione: 4 casi su 5 trattano la divergenza come rumore.** Datazione, autore, provenienza sono precisamente le questioni su cui il disaccordo fra specialisti è permanente e produttivo.

**La generazione è l'unica via di fuga.** Con il 33% di risposta singola è il solo formato in cui i benchmark ammettono strutturalmente più esiti validi — e non a caso i 5 casi di `graded_human_judgment` sono tutti su task generativi o di critica.

Per disciplina l'effetto è ancora più netto: **Music 5/5 `noise`**, **Philosophy 5/6**, **Religious Studies 7/10**. Le tre aree dove l'interpretazione è meno riducibile a chiave sono quelle dove la divergenza è più esplicitamente trattata come difetto.

### F. La genesi degli oggetti non interessa

`gold_concerns_genesis` è `yes` in **3 casi su 42 (7%)**: Appear2Meaning, EduArt, Hanfu-Bench.

Datazione, attribuzione autoriale, luogo d'origine, provenienza, storia materiale — cioè il nucleo operativo di filologia, storia dell'arte, archeologia, codicologia — sono il bersaglio di tre benchmark su quarantadue. Il resto valuta il *contenuto* degli oggetti, non la loro storia.

**La narrativa:** il campo ha importato dalle humanities le domande che somigliano a comprensione del testo e riconoscimento visivo, e ha lasciato fuori quelle che richiedono ragionamento inferenziale su come un oggetto è venuto all'esistenza. È un vuoto identificabile e argomentabile come programma di ricerca.

### G. Il multimodale investe in competenza

| modalità | n | `domain_expert` | `crowd_annotation` |
|---|---:|---:|---:|
| solo `text` | 23 | 2 | **7** |
| `image`+`text` | 17 | **6** | 2 |

E il trattamento della divergenza: nel testuale `not_stated` 13 su 23 (silenzio), nel multimodale `noise` 10 su 17 (esplicito).

I benchmark visuali costano più da costruire, coinvolgono più spesso specialisti, e affrontano più spesso il problema dell'accordo. Il testuale può appoggiarsi a chiavi preesistenti e crowd, e tace più spesso sulla questione.

Audio e video restano quasi assenti: **1 paper** con audio+immagine+testo+video, **1** con audio+testo. Etnomusicologia, studi cinematografici, arti performative sono fuori dal quadro — che è il gap-paper più immediato del corpus.

### H. La scala si paga in chiusura

`dataset_size` per formato di risposta:

| formato | n | mediana | massimo |
|---|---:|---:|---:|
| `single_answer` | 27 | 3.445 | **589.764** |
| `graded_human_judgment` | 5 | 5.444 | 51.698 |
| `answer_set` | 5 | 1.696 | 123.589 |

Le mediane sono comparabili, gli estremi no: i dataset più grandi di un ordine di grandezza sono tutti a risposta singola. La scala si ottiene rinunciando alla gradazione, perché solo la chiave unica è automatizzabile senza costo marginale.

### I. Il silenzio come reperto

Sommando i `not_stated` per sfaccettatura:

| sfaccettatura | `not_stated` | % |
|---|---:|---:|
| `plurality_treatment` | 22 | 52% |
| `gold_source` | 6 | 14% |
| `answer_multiplicity` | 4 | 10% |
| `gold_community_dependent` | 3 | 7% |
| `gold_concerns_genesis` | 3 | 7% |
| `gold_beyond_stimulus` | 2 | 5% |

**Sei paper su 42 non dichiarano da dove viene la loro ground truth.** Su materiale umanistico, dove la provenienza dell'autorità interpretativa è la questione, è un'omissione sostanziale — e riportabile come risultato, non come limite dell'estrazione. Il valore `not_stated` è stato progettato come misura esplicita e distinguibile da `no` proprio per rendere questo conteggio possibile.

---

## 3. Il disaccordo fra le personae come misura

Accordo fra la persona umanista (`ciop`) e quella tecnica (`cip`), calcolato offline dai report persistiti:

| sfaccettatura | accordo | contesi |
|---|---:|---:|
| `gold_concerns_genesis` | 41/42 | 1 |
| `gold_community_dependent` | 40/42 | 2 |
| `gold_beyond_stimulus` | 39/42 | 3 |
| `answer_multiplicity` | 37/42 | 5 |
| `gold_source` | 36/42 | 6 |
| `plurality_treatment` | 36/42 | 6 |

Il gradiente è interpretabile. `gold_concerns_genesis` è quasi ispezionabile — o il benchmark chiede date e autori o non li chiede — e viene contestato una volta sola. `gold_source` e `plurality_treatment` richiedono di leggere cosa il paper *dichiara sulla propria pratica*, e sono i più contesi. **Il disaccordo si concentra dove il paper va interpretato, non dove va ispezionato.**

**SimpleQA è contestato su 5 sfaccettature su 6** — il caso estremo — e il suo `gold_source` finale è `not_stated`. Suggerisce un'ipotesi verificabile: il disaccordo fra le due letture traccia la sotto-documentazione. Dove il paper non dice, i due sguardi riempiono il vuoto in modi diversi, e il disaccordo diventa un indicatore automatico di quali paper descrivono male la propria costruzione. Con n=42 e un solo caso netto è un'ipotesi, non un risultato.

Nota su una decisione dello strumento: il reviewer risolve `not_stated` quando uno dei due ha inferito un valore che il paper non dà. Sui casi contesi di `gold_source`, 3 su 6 si risolvono così — il che significa che il conteggio dei `not_stated` è, se qualcosa, conservativo.

---

## 4. Cosa questi dati non dicono

**Non c'è validazione contro codifica umana.** Le due personae concordano fra loro su 36-41 casi su 42, che è cosa diversa dall'avere ragione: un vocabolario chiuso le vincola a convergere e può far convergere anche su un errore. Nessun numero qui è validato esternamente. Un subset di 10 paper codificati a mano è il passo che manca prima di pubblicare qualsiasi percentuale.

**`relevant_asjc_areas` non è a vocabolario controllato, e si vede.** L'analisi per disciplina contiene "Archaeology" (2) e "Archeology" (1) come aree distinte per un errore di battitura, più valori estranei alla lista ASJC dichiarata: "Cultural Studies" (10), "Law" (2), "Anthropology" (1), "Multidisciplinary" (1). I conteggi per disciplina in §2.E e §2.G sono quindi indicativi, non esatti. È l'unico campo di lista rimasto fuori da `check_vocab()`, e va chiuso prima di usare quelle cifre in un articolo.

**Le tre esclusioni per PDF mancante non sono casuali.** EXAMS-V, IRLBench e MultiBLiMP sono tutti benchmark multilingui, e la loro assenza potrebbe attenuare proprio i conteggi di §2.D sull'universalismo. Vanno recuperati a mano prima di chiudere i numeri.

**n=42 non regge inferenza statistica.** I trend temporali di §2.A si appoggiano su 9, 19 e 11 paper per anno; il salto 2026 su `noise` è vistoso ma su undici casi. Va presentato come pattern osservato, con i numeri assoluti sempre visibili accanto alle percentuali.

**Un limite di copertura del corpus a monte.** Non è documentata la strategia di ricerca che ha prodotto i 45 paper di partenza. Qualsiasi affermazione della forma "il campo fa X" dipende dalla recall di quella ricerca, non dalla qualità di questa estrazione.

---

## 5. Le tre affermazioni più difendibili

Ordinate per rapporto fra forza dell'evidenza e interesse dell'affermazione.

**1. Il campo tratta la divergenza interpretativa come difetto, e sempre più esplicitamente.** 19 paper su 42 la minimizzano, 22 la ignorano, 1 la valorizza — e nel 2026 la quota di minimizzazione esplicita sale al 73%. Regge perché è un conteggio su una proprietà dichiarata nei paper, non su un giudizio.

**2. Metà del corpus chiede inferenza e accetta una risposta sola.** 21 su 42 combinano `gold_beyond_stimulus`=yes con `single_answer`. Regge perché entrambe le sfaccettature sono verificabili nel protocollo di valutazione.

**3. Le operazioni fondanti delle discipline storiche sono quasi assenti.** Datazione, attribuzione e provenienza sono il bersaglio di 3 benchmark su 42. Regge come conteggio, e apre direttamente a un programma di ricerca invece di limitarsi a diagnosticare.
