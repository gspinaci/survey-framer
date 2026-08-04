# Vocabolari controllati nello schema di estrazione — modifiche e risultati

**Data:** 4 agosto 2026
**Stato:** modifiche applicate, corpus ri-estratto per intero e verificato.

Dopo il primo run multi-agente completo, il confronto sistematico fra gli output di `ciop` (persona umanista) e `cip` (persona tecnica) su 43 paper ha mostrato che alcuni campi non erano aggregabili. Questo documento descrive le quattro modifiche fatte per rimediare, i tre bug preesistenti emersi durante il re-run, e i risultati misurati.

## Esito

| | |
|---|---|
| Paper estratti con lo schema nuovo | **42/42** (tutti quelli con PDF disponibile) |
| Paper senza PDF, esclusi | 3 — EXAMS-V, IRLBench, MultiBLiMP 1.0 |
| Violazioni di vocabolario (`check_vocab`) | **0 su 42** |
| Termini della tassonomia effettivamente usati | **22 su 22** (nessuno morto) |
| Narrative + dashboard | rigenerati sul corpus di 42 |

---

## Parte A — le quattro modifiche allo schema

### 1. Vocabolario controllato per `analytical_tasks`

**Il problema.** Le due personae descrivevano lo stesso paper con etichette quasi disgiunte: **Jaccard medio 0.16**, con diversi casi a 0.00. Non era disaccordo sostanziale, era assenza di vocabolario: gli stessi task a granularità diverse. Esempio reale (2503.15358) — `ciop`: *figurative language classification, multimodal image-text ranking, next-image sequence prediction*; `cip`: *classification, ranking, sequential prediction*. La prova quantitativa: **235 etichette distinte su 337 menzioni**, cioè ogni paper ne inventava di nuove, con doppioni non normalizzati (`multiple-choice question answering` e `multiple-choice qa` conteggiati separatamente). Il campo era inutilizzabile per qualsiasi statistica di corpus.

**La soluzione.** Tassonomia chiusa di **22 identificatori** in `ANALYTICAL_TASK_VOCAB` ([src/fields.py](../src/fields.py)), derivata clusterizzando le 235 etichette osservate — non inventata a priori. Iniettata in tutti e tre i prompt tramite il nuovo token `<<TASK_VOCAB>>`, sostituito in [src/analyzer.py](../src/analyzer.py): unica fonte di verità, con una glossa per termine per disambiguare i casi vicini (`interpretation` vs `cultural_reasoning`).

Due termini sono stati aggiunti perché il corpus li richiedeva e altrimenti finivano in bucket sbagliati: `calibration_and_uncertainty` (calibration assessment, difficulty self-estimation) e `agentic_tool_use` (multi-step retrieval, context management, stopping criteria).

Il dettaglio fine non si perde: i prompt impongono di riportare la terminologia originale del paper in `analytical_tasks_explanation`.

### 2. Enum per `primary_evaluation_setting`

Solo `zero-shot | few-shot | fine-tuned | mix`, con la regola esplicita che più di un setting significa `mix` ([prompts/extra_fields.json](../prompts/extra_fields.json)). Eliminava 8 degli 11 disaccordi, tutti puramente formali: `"mix"` vs `"a mix"`, `"few-shot"` vs `"zero-shot and few-shot"`.

### 3. Disambiguazione di `both` in `humanities_role`

Era il campo con il disaccordo concettuale più forte: **accordo 27/43 (63%)**, e in 11 dei 16 disaccordi era `ciop` a scegliere `both` — l'agente umanista lo usava come default cauto, vedendo sempre *anche* una dimensione disciplinare.

Nuova regola, nello schema e in tutti e tre i prompt: `both` richiede **gruppi di item distinti o metriche distinte** per ciascun ruolo. Ai personae si dice esplicitamente che `both` non è l'opzione prudente; al reviewer che in caso di split fra `both` e un valore specifico il default è il valore specifico, salvo evidenza nel testo.

### 4. Potatura dei criteri di inclusione: 7 → 4

Sei criteri su sette avevano accordo perfetto, ma solo perché erano quasi tutti costanti: `arts_humanities_data`, `llm_is_primary_system` ed `english_language` risultavano `true` su 43/43 paper. Non discriminavano nulla — il corpus è già pre-filtrato a monte — e le loro note non contenevano informazione assente da `relevant_asjc_areas`. Rimossi.

I quattro rimasti fanno tutti lavoro reale:

- `general_purpose_benchmark` — l'unico che divide il corpus, ed è anche l'unico su cui le personae litigavano
- `evaluates_generative_llm` e `published_after_march_2023` — ciascuno esclude almeno un paper, e le note portano la lista modelli e la data
- `quantitative_metrics` — **tenuto nonostante sia costante**, perché [src/dashboard.py](../src/dashboard.py) mina il suo campo `note` per il breakdown delle metriche; rimuoverlo avrebbe fatto crollare la copertura da 37 paper a quella della sola colonna CSV. Il motivo è documentato nel commento in `fields.py`.

### Enforcement

I vincoli sopra sono istruzioni di prompt, quindi da soli non garantiscono nulla. `check_vocab()` in [src/fields.py](../src/fields.py), chiamato da [main.py](../main.py) dopo ogni estrazione, stampa `VOCAB: <id> — ...` per ogni valore fuori vocabolario. È case-insensitive e salta le chiavi assenti, quindi funziona anche sui run incrementali su un sottoinsieme di campi. Segnala e non solleva: un'etichetta fuori vocabolario è un problema di aderenza al prompt, non un motivo per scartare un'estrazione per il resto buona.

Al reviewer è stato inoltre vietato **risolvere i disaccordi per unione**. Prima lo faceva: dei 188 task nei report finali, 95 venivano da `ciop`, 114 da `cip`, 19 erano nuovi — media 4.37 task contro i 3.88/3.95 delle personae. Ora deve includere un valore solo se il paper mostra che il benchmark lo valuta. Gli è stata anche codificata la divisione di competenza emersa dall'analisi: peso a `cip` su ciò che è verificabile nel testo (nome esatto, dimensione dataset, modelli, metriche, date — dove vinceva 6-1 sui nomi e 4-0 su `dataset_size`), peso a `ciop` sul giudizio disciplinare (dove vinceva 9-7 su `humanities_role`).

---

## Parte B — tre bug preesistenti, trovati durante il re-run

Nessuno dei tre è stato introdotto dalle modifiche di cui sopra.

### 1. `find_pdfs` perdeva 8 paper su 42 — silenziosamente

Gli id derivati dai titoli contengono `:`, che il fetcher sanitizza in `_` sul filesystem, producendo `CaLMQA__Exploring…`. `find_pdfs` invece cercava `CaLMQA:_Exploring…` con un match a sottostringa, che falliva.

**Effetto:** eseguendo `fetch` e `analyze` come step separati — cioè come documentato nel README — 8 paper con il PDF regolarmente scaricato venivano saltati senza errore. Funzionava solo con `--step all`, dove il dizionario dei path viene passato direttamente in memoria. Vale anche per il primo run: analizzava 34 paper anziché 42.

**Fix:** il nome canonico è ora una singola funzione pubblica, `pdf_filename()` in [src/pdf_fetcher.py](../src/pdf_fetcher.py), usata da entrambi i lati, con match esatto invece che a sottostringa.

### 2. Reviewer troncato nel 18% dei casi

6 risposte su 34 fallivano il parse JSON, sempre con la stessa firma (`Expecting ',' delimiter`). Non era escaping rotto, come sembrava a prima vista: i dump mostrano **6 graffe aperte e 5 chiuse**, con il taglio netto subito dopo `review_notes`, che è l'ultimo campo scritto. Era il limite di token in output — e le modifiche al prompt del reviewer avevano allungato proprio quel campo, quindi il problema è stato peggiorato dalla Parte A.

**Fix**, in [src/llm.py](../src/llm.py):
- `max_output_tokens = 8192` esplicito (i report finali stanno sui 3.5–4.5k caratteri)
- retry fino a 3 tentativi sul parse fallito: prima una risposta malformata bruciava tutte e tre le chiamate del paper senza restituire nulla
- dump delle risposte non parsabili in `output/malformed_replies/`, con label per paper e agente

Un tetto è stato messo anche su `generate_text` (narrativa). Lì è **precauzionale, non la correzione di un troncamento osservato**: un testo libero tagliato resterebbe testo valido e passerebbe silenzioso nel file di output invece di sollevare un errore.

### 3. Il narrative includeva un paper estraneo al corpus

`step_narrative` fa glob su tutta `output/papers/` ignorando il CSV di input, e aveva sintetizzato **43 paper anziché 42**: il file in più era `1606.06031` (LAMBADA), residuo con schema vecchio di un run fatto con `test_papers.csv`. Compariva nei cluster tematici del narrative generato.

**Fix:** `step_validate` in [main.py](../main.py) filtra ora sugli id del CSV di input e logga `STALE: <id> — not in input CSV, excluded` per quello che scarta.

**Pulizia:** i quattro file di LAMBADA (JSON finale, markdown, due report persona) sono stati rimossi con `git rm`. Il paper non è in `papers.csv` né in `Sources.csv` — solo in `test_papers.csv`, la fixture di test — e falliva due criteri di inclusione del progetto (`published_after_march_2023` e `evaluates_generative_llm` entrambi `false`, essendo del 2016). Se lo si rivuole, va aggiunto a `papers.csv` e ri-analizzato; i file sono comunque recuperabili dalla storia git.

---

## Risultati misurati

**Zero violazioni di vocabolario su 42 paper.** Le tre liste chiuse hanno tenuto senza un solo caso fuori norma.

**La tassonomia è ben tarata:** tutti i 22 termini usati, nessuno morto, nessun overflow. Distribuzione su 191 menzioni:

| n | task | n | task |
|---:|---|---:|---|
| 19 | factual_recall | 6 | transcription_and_correction |
| 16 | multiple_choice_qa | 5 | calibration_and_uncertainty |
| 16 | cultural_reasoning | 5 | information_extraction |
| 14 | logical_and_quantitative_reasoning | 5 | attribution |
| 14 | visual_recognition | 4 | fact_verification |
| 12 | generation | 4 | retrieval_and_ranking |
| 11 | causal_and_temporal_reasoning | 3 | normative_judgment |
| 11 | interpretation | 3 | agentic_tool_use |
| 11 | open_ended_qa | 2 | sequence_prediction |
| 9 | visual_reasoning | 7 | translation / stylistic_analysis / classification |

Il confronto con il prima è il punto: 148 etichette distinte su 188 menzioni → **22 su 191**. Ora si può contare "quanti benchmark valutano il task X" e ottenere un numero difendibile.

**Effetto collaterale misurabile della Parte A.4:** la dashboard passa da **12 a 8** benchmark general-purpose su 42. La nota inasprita di `general_purpose_benchmark` (`false` per benchmark limitati a un task, dominio o framework) ha riclassificato 4 paper come purpose-built.

**Smoke test sui due paper peggiori** (quelli con Jaccard 0.00), prima di lanciare il run completo:

| | `analytical_tasks` J | `humanities_role` | resto |
|---|---|---|---|
| 2503.15358 (AdMIRe) | 0.00 → **1.00** | both/domain → **domain/domain** | nome, setting, dataset_size: accordo pieno |
| 2409.02813 (MMMU-Pro) | 0.00 → **0.62** | → **domain/domain** | identici |

---

## Riprodurre il run

```bash
source .venv/bin/activate
python main.py --input input/papers.csv --step fetch
python main.py --input input/papers.csv --step analyze --force
python main.py --input input/papers.csv --step narrative
python main.py --input input/papers.csv --step dashboard
```

Serve un `.env` con la propria `GEMINI_API_KEY` (vedi `.env.example`). Costo: ~126 chiamate API per l'analyze (42 paper × 3 agenti), più i retry sui parse falliti, più 1 chiamata per la narrativa.

I quattro step sono ora sicuri anche eseguiti separatamente — prima il bug B.1 li rendeva equivalenti a `--step all` solo per caso.

`output/malformed_replies/` non è tracciato: sono artefatti diagnostici, valutare se aggiungerlo a `.gitignore`.

## Decisione ancora aperta

La tassonomia a 22 termini in [src/fields.py](../src/fields.py) merita una revisione disciplinare. Ha superato 42 paper senza violazioni e senza termini morti, il che dice che è *praticabile*, non che i confini siano quelli giusti — per esempio se `interpretation` e `cultural_reasoning` vadano tenuti separati, o se `attribution` (datazione, autore, provenienza) debba assorbire parte di `classification`. Cambiarli dopo costa un altro run completo, quindi è il momento giusto per guardarli.
