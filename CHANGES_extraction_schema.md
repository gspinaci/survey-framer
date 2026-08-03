# Modifiche allo schema di estrazione — vocabolari controllati

**Data:** 3 agosto 2026
**Contesto:** dopo il primo run multi-agente completo (43 paper × 2 personae + reviewer), il confronto fra gli output di `ciop` e `cip` ha mostrato che alcuni campi non erano aggregabili. Queste modifiche intervengono sulle quattro cause individuate. Richiedono un re-run completo con `--force` per avere effetto.

---

## Modifiche

**1. Vocabolario controllato per `analytical_tasks`** — [src/fields.py](src/fields.py)

Tassonomia chiusa di **22 identificatori** in `ANALYTICAL_TASK_VOCAB`, derivata clusterizzando le 235 etichette libere del primo run (non inventata). Iniettata in tutti e tre i prompt via un nuovo token `<<TASK_VOCAB>>` (sostituito in [src/analyzer.py:39](src/analyzer.py#L39)) — unica fonte di verità, con una glossa per termine per evitare confusioni tipo `interpretation` vs `cultural_reasoning`.

Sono stati aggiunti due termini che il corpus richiedeva e che altrimenti finivano in bucket sbagliati: `calibration_and_uncertainty` (calibration assessment, difficulty self-estimation) e `agentic_tool_use` (multi-step retrieval, context management, stopping criteria). Il fine-grained non si perde: i prompt ora impongono di riportare la terminologia originale del paper in `analytical_tasks_explanation`.

**2. Enum per `primary_evaluation_setting`** — [prompts/extra_fields.json](prompts/extra_fields.json)

Solo `zero-shot | few-shot | fine-tuned | mix`, con la regola esplicita che più di un setting → `mix`. Eliminava gli 8 disaccordi puramente formali (`"mix"` vs `"a mix"`).

**3. Disambiguazione di `both` in `humanities_role`** — schema + tutti e tre i prompt

Regola: `both` solo con **gruppi di item distinti o metriche distinte** per ciascun ruolo. Ai due personae si dice che `both` non è l'opzione prudente; al reviewer che in caso di split `both` vs valore specifico il default è il valore specifico salvo evidenza.

**4. Potatura dei criteri di inclusione** — 7 → 4

Rimossi `llm_is_primary_system`, `arts_humanities_data`, `english_language` (43/43 true, zero potere discriminante; le ASJC erano già in `relevant_asjc_areas`).

**Una deviazione rispetto alla proposta iniziale:** `quantitative_metrics` è stato tenuto nonostante sia costante, perché [src/dashboard.py:238](src/dashboard.py#L238) mina il suo campo `note` per il breakdown delle metriche — rimuoverlo avrebbe fatto crollare la copertura da 37 paper a quella della sola colonna CSV. Quindi 4 criteri, non 3. Il motivo è documentato nel commento in `fields.py`.

**Extra non richiesti ma necessari perché i vincoli siano reali:**

- `check_vocab()` in `fields.py`, chiamato in [main.py:119](main.py#L119): stampa `VOCAB: <id> — ...` per ogni valore fuori vocabolario. Case-insensitive, salta le chiavi assenti (funziona anche sui run incrementali). Segnala, non solleva — un'etichetta fuori vocabolario è un problema di aderenza al prompt, non un motivo per buttare un'estrazione buona.
- Nuove istruzioni al reviewer: **vietato risolvere per unione** su `analytical_tasks` e `relevant_asjc_areas` (prima faceva union: 4.37 task medi contro 3.88/3.95 dei personae), più la divisione di competenza che l'analisi aveva evidenziato — dare peso a Cip sul verificabile, a Ciop sul giudizio disciplinare.
- `report_writer` mostra ancora i 3 criteri ritirati **se presenti nel JSON**, così i 41 report vecchi si rigenerano senza perdere righe; e rende gli identificatori snake_case con gli spazi.

---

## Smoke test reale (2 paper, quelli con Jaccard 0.00)

| | `analytical_tasks` J | `humanities_role` | altri campi |
|---|---|---|---|
| **2503.15358** (AdMIRe) | 0.00 → **1.00** | both/domain → **domain/domain** | nome, setting, dataset_size: accordo pieno |
| **2409.02813** (MMMU-Pro) | 0.00 → **0.62** | → **domain/domain** | nome, setting, dataset_size identici |

Zero warning `VOCAB`. I criteri nei nuovi JSON sono i 4 attesi. Le `review_notes` mostrano adjudication motivata, non union cieca — su MMMU-Pro il reviewer rimappa `information_extraction` → `transcription_and_correction` perché "OCR accuracy is an explicitly evaluated metric". Verificato anche che dashboard e report rendering funzionano su schema vecchio e nuovo.

---

## Due cose da sapere prima di lanciare

**Il corpus è in stato misto:** 2 paper con il nuovo schema, 41 con il vecchio. Non aggregare finché non è stato fatto un `--force` completo — dashboard e narrative mescolerebbero snake_case e testo libero.

**`output/pdfs/` è vuota** — sono stati scaricati solo i 2 PDF del test. Un re-run completo richiede prima `--step fetch` per tutti i 45 paper, poi `--step analyze --force`: **~135 chiamate API** (45 × 3 agenti).

```bash
source .venv/bin/activate
python main.py --input input/papers.csv --step fetch
python main.py --input input/papers.csv --step analyze --force
```

Serve un `.env` con la propria `GEMINI_API_KEY` (vedi `.env.example`); il modello reviewer/narrative è `gemini-3.1-pro-preview`, i personae girano su `gemini-3.5-flash` (vedi `config.py`).

Prima di spendere le chiamate vale la pena rivedere la tassonomia a 22 termini in [src/fields.py:14-40](src/fields.py#L14-L40) — è il pezzo che beneficia più di un controllo disciplinare, perché una volta che il corpus è stato estratto con questi label cambiarli costa un altro run completo.
