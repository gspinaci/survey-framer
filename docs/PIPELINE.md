# Pipeline del censimento: definizione generale

*v3, 9 novembre 2026. Sostituisce `DESIGN_skill_census.md`. Approvata nell'impianto (supervisor/reviewer, tabella = CSV versionato in git). Le parti già implementate sono segnate con ✅; il resto si costruisce fase per fase, ognuna con il suo giro di prova (§5).*

## 0. Principi

1. **La ricerca è dati, non codice.** Domande di ricerca, criteri di inclusione, schema di estrazione e agenti stanno in un *protocollo* dichiarativo (`census.toml` + `prompts/`). Un altro censimento si fa con un altro protocollo, senza toccare il motore.
2. **Ripetibile.** Ogni fase scrive su disco i propri risultati con un manifest: chi o cosa l'ha prodotta, quando, con quale prompt (hash) e con quale modello. Ogni numero del paper si ricalcola da quei file.
3. **Le decisioni restano umane.** Inclusione (GS e RG), casi `needs_human`, approvazione delle narrative. Gli agenti cercano, leggono e propongono; non escludono e non concludono.
4. **Provenienza ovunque.** Ogni record sa da quale strada e da quale run è entrato nella tabella, e da quale backend e modello è stato estratto.
5. **Modulare e distribuito.** Ogni agente è un passo eseguibile da solo, da qualunque operatore con il proprio account; i risultati si uniscono con git e il resto della pipeline riparte da lì (§7).

## 1. Le fasi

```
              ┌─ A. Fonti curate ──── system card, sedi DH, aggregatori (manuale)
DISCOVERY ────┼─ B. ASReview ──────── pool OpenAlex/arXiv/ACL/S2 → screening assistito
              └─ C. Ricerca agentica ─ scout per famiglia di fonti, verifica sul testo
                     │   ogni run → discovery/<run_id>/ con manifest.json
                     ▼   import → righe della tabella con provenienza   ✅
SCREENING      doppia verifica umana GS/RG → incluso | escluso | conflitto | in attesa   ✅ (gate)
                     ▼   solo gli inclusi proseguono
ACQUISIZIONE   fetch del PDF (✅ solo PDF veri; colonna PDF URL) + intake: è davvero il paper?
                     ▼
LETTURA        N lettori indipendenti (oggi Ciop e Cip), ognuno con il suo scopo; ogni valore ha una citazione
                     ▼
SUPERVISIONE   supervisor: controlla ogni lettura PRIMA del confronto (citazioni verificate,
               completezza, vocabolari, sezioni giuste); al massimo un rinvio al lettore
                     ▼
REVISIONE      reviewer: decide tra letture già validate → record finale, confidenza per campo,
               note di revisione, campi needs_human → coda per GS/RG
                     ▼
SINTESI        statistiche (script deterministici) → narratore: pattern e narrative candidate
               → critici: ogni affermazione verificata sui numeri, a maggioranza
                     ▼
PUBBLICAZIONE  article.md + findings.md + dati delle figure → pagina generata (✅ nessuna copia nel codice)
```

**Supervisor e reviewer (confermato).** Il *supervisor* lavora sui lettori: controlla che ogni lettura sia fatta bene e la rimanda indietro se non lo è. Il *reviewer* lavora sul contenuto: decide tra letture valide. Il vantaggio è che, quando arrivano al reviewer, i disaccordi tra Ciop e Cip sono **disaccordi di interpretazione** e non errori di lettura. Quindi l'accordo tra lettori misura qualcosa, e il reviewer resta l'agente che "adjudicates", come in §3.3 dell'articolo.

## 2. Agenti definiti per scopo e numero

Ogni agente è una voce in `census.toml` con **ruolo** (insieme chiuso), **scopo** (cosa copre), **numero** (quante istanze), **modello** e **backend**. Il motore legge la configurazione; aggiungere un lettore o uno scout non richiede codice, solo una voce e il suo prompt.

| Ruolo | Scopo = | Numero | Input → output | Strumenti |
|---|---|---|---|---|
| `scout` | famiglia di fonti (arxiv, acl-anthology, sedi DH, system card, shared task…) | una istanza per scopo | finestra + criteri → candidati con prove C1-C4 | web |
| `intake` | — | 1 | PDF + riga della tabella → identità verificata, mappa del paper | lettura PDF |
| `reader` | prospettiva (umanistica, tecnica, …) e sottoinsieme di campi | ≥ 2, con scopi diversi; oppure stesso scopo × k per stimare la stabilità | paper → lettura con citazioni | lettura PDF, ricerca nel testo |
| `supervisor` | — | 1 | lettura + paper → valida o rimanda | verifica citazioni (script) |
| `reviewer` | — | 1 | letture valide + paper → record finale | lettura PDF |
| `narrator` | asse o domanda di ricerca | 1 o uno per RQ | statistiche + record → narrative candidate | solo dati |
| `critic` | — | k (default 3) | affermazione + statistiche → regge / non regge | solo dati |

La configurazione vera è [`census.toml`](../census.toml) ✅: oggi dichiara Ciop e Cip (lettori), supervisor e reviewer, con modello e backend per ciascuno; contiene anche un esempio commentato di terzo lettore specializzato. `count = k` crea k istanze indipendenti dello stesso agente; una lista di scopi crea un'istanza per scopo (per esempio uno scout per famiglia di fonti). Scout, narratore e critici verranno aggiunti quando si costruiscono le loro fasi.

**Backend.** Ogni agente dichiara il proprio: `claude-cli` (`claude -p`, abbonamento Claude, ✅), `gemini` (API a chiave, ✅), `mock` (nessun modello: output finto ma conforme allo schema, per provare i meccanismi senza consumare quota, ✅; ammesso solo nei round `test-…`). L'account è quello di chi lancia il passo. In seguito si possono aggiungere l'API di Anthropic o di OpenAI, e i lettori con strumenti (pagine del PDF come immagini) tramite `claude -p` con lo strumento Read abilitato.

**Il narratore** nasce dal prompt che ha prodotto findings.html (28 agosto): insight che non si sovrappongono, differenze verificabili nei dati, criticità epistemologiche esplicite, linguaggio naturale. Si aggiunge la correzione del 29 agosto: un documento nuovo e autonomo, non un delta rispetto alla versione precedente. In più c'è un vincolo: **il narratore non calcola numeri**, cita solo quelli prodotti dagli script, e ogni affermazione passa dai critici.

## 3. Discovery: tre strade, un formato

Ogni run, di qualunque strada, produce gli stessi file in `discovery/<run_id>/`:

- `manifest.json`: strada, strumento, operatore, modello, prompt e suo hash, finestra temporale, data di esecuzione, data di import, hash dei file grezzi;
- `raw/`: l'output così com'è (per le strade agentiche: `candidates.csv` con le prove C1-C4, `near_misses.csv`, `unverified.csv`, `search_log.csv`).

L'importer (`scripts/import_discovery.py` ✅) trasforma i candidati in righe della tabella: deduplica rispetto ai record già presenti, lascia vuote le colonne Accept e aggiunge la provenienza.

| Strada | Cosa è un "run" | Stato |
|---|---|---|
| A. Fonti curate | una sessione di ricerca manuale su `input/Survey Benchmarks LLM+DH - Sources.csv` | ricostruita dalla storia git (maggio-luglio 2026) ✅ |
| B. ASReview | costruzione del pool (`../benchmark_llm_humanities_review/build_pool`) + progetto ASReview | ricostruita: pool del 22/05/2026 ✅ |
| C. Ricerca agentica | un'esecuzione degli scout su una finestra | 1° run: ChatGPT Deep Research del 9/11/2026, 30 candidati ✅ importati; la skill `census-discover` è da costruire |

**Stima del richiamo.** Quando due strade coprono la stessa finestra in modo indipendente, si stima quanti benchmark esistono in tutto con il metodo cattura-ricattura (Lincoln-Petersen: N ≈ n₁·n₂ / m, dove m sono i candidati trovati da entrambe). Per la finestra maggio-novembre 2026 basta un run della skill indipendente da quello di ChatGPT.

Ricostruendo la provenienza sono emersi due vincoli:
- **I seed non contano come ritrovamenti.** 28 record curati riportano "Source 2 = ASREVIEW", ma erano in tabella dal 23 maggio, prima dello screening, e sono stati caricati in ASReview come seed rilevanti. Il fatto che ASReview li ritrovi non è una scoperta indipendente. Per questo la loro strada è registrata come `curated`, con il segno ASREVIEW conservato in `Discovery ref`. Le strade A e B, così come sono state eseguite, non permettono una stima cattura-ricattura.
- **I record già noti vanno segnalati, non soppressi.** Il prompt di ChatGPT chiedeva di non riportare i 45 benchmark noti, quindi quel run non dice quanti ne avrebbe ritrovati. Il prompt aggiornato (`docs/deep_research_prompt.md`) li fa riportare in una tabella a parte; la copia usata il 9 novembre resta nel run (`prompt.md`, con il suo hash).

## 4. Provenienza e stato dei record ✅

Colonne aggiunte alla tabella `input/papers.csv`. Quelle preesistenti non cambiano.

| Colonna | Contenuto |
|---|---|
| `ID` | identificatore stabile del record (arXiv id, DOI, id ACL Anthology o slug), fissato alla prima registrazione e mai più ricalcolato |
| `PDF URL` | link diretto al testo completo, quando l'Article URL non lo è (landing page, paywall, server irraggiungibile) |
| `Discovery route` | `curated` \| `asreview` \| `agentic` |
| `Discovery run` | `run_id`, che punta a `discovery/<run_id>/manifest.json` |
| `Discovery ref` | riferimento alla riga nel file grezzo del run, con il nome originale |
| `Added on` | data di ingresso nella tabella |

Per i 45 record esistenti `Added on` viene dal commit in cui la riga compare per la prima volta. La strada è ricavata dalle colonne `Source`, `Source 2` e `Hunter`.

**Ciclo di vita di un record:** `candidate` → screening → `included` (GS e RG entrambi TRUE) | `excluded` (almeno un FALSE) | `conflict` (TRUE/FALSE) | `pending` (manca una delle due decisioni). **Solo gli `included` vengono scaricati e analizzati** (✅ gate in `main.py`). I record estratti portano anche il timbro `extraction` (backend, modelli, data).

## 5. Giro di prova, fase per fase (prima del push)

Ogni fase si prova su pochi casi scelti apposta, con un criterio di accettazione fissato prima; si corregge e si ripete finché il criterio non è soddisfatto.

| Fase | Campione | Criterio di accettazione |
|---|---|---|
| Discovery C (skill) | 1 famiglia di fonti (per esempio gli atti LT4HALA/NLP4DH 2026) | ritrova i candidati di ChatGPT per quella famiglia, ogni candidato ha le prove C1-C4 dal testo |
| Import | i 30 candidati di ChatGPT | ✅ nessun duplicato, provenienza completa, nessun candidato analizzato prima dello screening |
| Acquisizione + intake | 5 paper, di cui 2 trappole (una landing page, un PDF sbagliato) | le trappole vengono fermate, i 3 buoni passano |
| Meccanica distribuita (backend mock, nessun modello) | 2 operatori simulati × 2 paper | ✅ file separati per agente, stato e dipendenze corretti dopo il merge, rifiuto di prompt diversi da quelli del round, segnalazione di lettori su PDF diversi, archiviazione con `--force` |
| Lettori | SimpleQA, BLN600 post-OCR (LT4HALA), Christian Iconography — round `pilot-2026-11` | ✅ 33/34 citazioni trovate alla lettera (l'unica mancata era una riga di tabella → verifica `table`); 0 valori fuori vocabolario. Correzione: i "no" che registrano un'assenza non richiedono citazione (`ABSENCE_VALUES`) |
| Supervisor | gli stessi 3 (+ citazione inventata nel mock) | ✅ intercetta citazioni riformulate, errori di definizione, numeri sbagliati. Prima versione troppo invasiva: rimandava scelte difendibili e dettava i valori → accordo tra lettori da 45/48 a 48/48 (convergenza artificiale). Corretta: solo errori dimostrabili, istruzioni senza valore suggerito → 45/48 → 44/48 |
| Reviewer | gli stessi 3 | ✅ controlli puliti (citazioni, vocabolari, confidenza completa); 1 campo passato agli umani con motivazione; note di revisione con pagine. Rispetto ai record Gemini 34/48 campi uguali: 9 scarti su SimpleQA sono l'artefatto della landing page; gli altri sono le questioni di schema in §6 |
| Secondo pilota (schema nuovo) | HiST-LLM, C3B, BLN600, Christian Iconography — `pilot-2026-11b` | ✅ controlli puliti; BLN600 13.192 / 2.792 sequenze (giusto); `existing_dataset` con traccia (HiST-LLM → Seshat, annotazioni di esperti); Christian Iconography gap `input` come nella classificazione di agosto. **Da decidere per l'articolo:** C3B — lettori e classificazione di agosto vedono un gap *scoring* (ACC 3,20 vs CACC 34,2), il reviewer lo scarta perché CACC è una media pesata che include altre domande (Sec. 4 del paper): se vale, i benchmark di §4.3 sono 8 |
| Sintesi | corpus attuale | ogni affermazione del narratore rimanda a un numero dell'output degli script; i critici ne bocciano almeno una (altrimenti il test è troppo facile) |
| Pubblicazione | build della pagina | ✅ l'articolo non è copiato nel repository |

## 6. Decisioni

Prese il 9 novembre:
- **Supervisor e reviewer**: come in §1.
- **Tabella master**: `input/papers.csv`, versionata in git; nessuna sincronizzazione con il Google Sheet.
- **Pilota accidentale**: cancellato; il pilota vero si fa sul round di prova (§7).
- **Esecuzione modulare**: sì, generalizzata a ogni agente (§7).

Aperte:
1. **EduArt** ha Accept GS/RG vuoti, quindi è `pending`: le nuove estrazioni lo saltano finché GS e RG non scrivono TRUE o FALSE. Se uno dei due è autore del paper, conviene che lo verifichi l'altro e annotarlo nelle Notes. Il suo record di agosto è ancora nel corpus letto da `findings_report.py`: la definizione di corpus per la sintesi va unificata con il gate quando si costruisce la fase di sintesi.
2. Numeri di default: 2 lettori, 6 scout, 3 critici?
3. ~~Definizioni da precisare~~ → **decise il 9 novembre e applicate allo schema** (dettaglio in `paper/CHANGES_extraction_schema.md`, sezione "round 2026-11"):
   - dimensione in due campi: `dataset_size` (tutto il benchmark) ed `evaluation_set_size` + `evaluation_unit` (ciò su cui si calcolano i punteggi);
   - tipo di gap estratto come dato (`reported_gap_kinds`, `reported_format_gap_kind`: scoring, format, depth, difficulty, input). Correzione: l'articolo **non** contava già Christian Iconography fra i 9 di §4.3 — la classificazione manuale in `findings_report.py` lo mette in `input` — quindi non cambia il conteggio, cambia solo dove vive la classificazione;
   - `gold_source = existing_dataset`, con la traccia `gold_upstream` / `gold_upstream_source`. Risalire al paper del dataset originario sarà un passo a parte, solo per questi record.
4. **Costo per paper:** circa 8 chiamate (2 letture, 2 controlli, ~1,7 rinvii e altrettanti ricontrolli, 1 reviewer su Opus), ~2 minuti in sequenza. Sui 45 paper sono ~380 chiamate, circa il triplo della pipeline vecchia. La causa principale sono i rinvii per citazioni deboli: si può ridurre migliorando le istruzioni ai lettori sulle citazioni delle facet.

## 7. Esecuzione modulare e distribuita ✅

**Obiettivo.** Ogni agente può essere eseguito separatamente, da operatori diversi e con account diversi. Per esempio GS lancia Cip e RG lancia Ciop, ognuno con il proprio abbonamento; si uniscono i risultati con git; più tardi chiunque lancia supervisor e reviewer.

**Come funziona.**
- **Un comando per passo:** `python census.py run <agente>`. Gli agenti sono quelli dichiarati in `census.toml`, quindi il meccanismo vale per qualunque agente aggiunto in futuro, non solo per Ciop e Cip.
- **Un file per agente per paper:** `output/rounds/<round>/papers/<paper>/<agente>.json`. Due operatori che lanciano agenti diversi non toccano mai lo stesso file, quindi `git pull` non richiede di risolvere conflitti. Se due persone lanciano lo stesso agente sullo stesso paper, git lo segnala come conflitto, ed è giusto così.
- **Il round congela il protocollo:** `python census.py round init`, lanciato una volta sola e poi committato, registra modello e hash del prompt di ogni agente. Un file prodotto con un prompt o un modello diverso viene rifiutato. Così due operatori non possono mescolare versioni diverse senza accorgersene; per cambiare un prompt si apre un nuovo round.
- **Provenienza per file:** operatore (`CENSUS_OPERATOR` in `.env`), backend, modello, hash del prompt e delle domande di ricerca, hash del PDF letto, durata, esito dei controlli (campi mancanti, vocabolari, citazioni verificate).
- **Stato e dipendenze:** `python census.py status` mostra per ogni paper e per ogni agente se il lavoro è fatto, manca, è bloccato o non è più valido, e chi l'ha fatto. Indica anche il prossimo comando eseguibile. Il supervisor diventa eseguibile su un paper solo quando ci sono tutti i lettori; il reviewer solo dopo il supervisor.
- **Stesso PDF per tutti:** arXiv restituisce l'ultima versione, quindi due operatori che scaricano a distanza di settimane possono leggere file diversi. `status` lo segnala confrontando gli hash dei PDF letti dai lettori.
- **Solo record inclusi:** `census.py` lavora soltanto sui record approvati da entrambi.

**Flusso tipico.**
```
una volta:   python census.py round init      → commit + push di round.json
RG:          python census.py run ciop        → git add output/rounds/ → commit → push
GS:          git pull; python census.py run cip → commit → push
più tardi:   git pull; python census.py status; python census.py run supervisor …
```

**Stato.** Lettori, supervisor e reviewer ✅, provati nel round `pilot-2026-11` (§5). Narratore, critici, scout, intake e la promozione dei record del round in `output/papers/`: da costruire, uno alla volta, ciascuno con il suo giro di prova. Il round `2026-11_claude` è **congelato dal 9 novembre**, dopo due piloti (`pilot-2026-11` e `pilot-2026-11b`, conservati in `output/rounds/` come documentazione del metodo).
