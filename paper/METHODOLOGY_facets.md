# Nota metodologica — dalle categorie alle proprietà osservabili

**Data:** 4 agosto 2026
**Stato:** strumento implementato, estrazione eseguita sul corpus di 42 paper.

Questa nota documenta una decisione metodologica sullo strumento di codifica del survey. Non è una nota tecnica: la scelta che descrive determina cosa il survey è in grado di affermare, e va riportata nella sezione metodo dell'articolo.

---

## 1. Il problema: confini che non esistono

La prima versione dello strumento chiedeva ai due agenti estrattori di assegnare a ogni benchmark uno o più *tipi di task analitico*, scelti da una lista chiusa di 22 termini derivata clusterizzando le 235 etichette libere di un run precedente (vedi [CHANGES_extraction_schema.md](CHANGES_extraction_schema.md)).

La lista chiusa ha risolto il problema per cui era stata introdotta — l'accordo fra le personae è passato da un Jaccard medio di 0.16 a zero violazioni su 42 paper — ma ne ha reso visibile un altro. Tre coppie di termini si sono rivelate non separabili in modo non arbitrario:

- `visual_recognition` (14 occorrenze) contro `visual_reasoning` (9)
- `interpretation` (11) contro `cultural_reasoning` (16)
- `attribution` (5) contro `classification` (7)

Il caso esemplare: riconoscere san Girolamo dal leone e dal cappello cardinalizio è riconoscimento visivo o è già inferenza iconografica? Datare un manoscritto dalla scrittura è attribuzione o classificazione? Ragionare su una norma culturale è distinguibile dall'interpretare un simbolo culturale?

Questi confini **non preesistono all'atto di codifica**. Sono continui, e dove si taglia dipende da una posizione teorica sul rapporto fra percezione e interpretazione.

## 2. Perché tagliarli sarebbe un bias, non una semplificazione

Un'assegnazione categoriale netta avrebbe iscritto nello strumento una risposta a priori a una domanda che il survey ha invece il compito di indagare. Il costo non sarebbe stato solo rumore nei dati: sarebbe stato circolare. Se lo strumento decide per stipulazione che il riconoscimento iconografico non è interpretazione, poi trovare che i benchmark testano poca interpretazione non è un risultato — è la definizione, restituita come reperto.

C'è inoltre una contraddizione performativa specifica di questo lavoro. La tesi centrale del survey è che i benchmark riducono operazioni ermeneutiche a categorie chiuse e a formati a risposta singola. Misurarlo con uno strumento che fa esattamente la stessa operazione sui benchmark indebolisce la forma dell'argomento, non solo il dato.

## 3. Il riorientamento: chiedere proprietà, non categorie

La soluzione adottata non è né tagliare i confini né rinunciare a codificare. È **spostare l'oggetto della domanda**.

Chiedere a un annotatore *«questo task è interpretazione o ragionamento culturale?»* significa chiedergli di applicare una categoria contestata. Chiedergli *«la risposta di riferimento è stata presa dai metadati esistenti o prodotta da un annotatore esperto?»* significa chiedergli un fatto che il paper dichiara.

Riformulati come proprietà della *risposta attesa* e della *costruzione del dataset*, i tre confini contestati diventano operazionalizzabili senza essere decisi:

| confine contestato | proprietà osservabile che lo sostituisce |
|---|---|
| riconoscimento vs inferenza visiva | la risposta corretta era già nei metadati della fonte, o è stata prodotta oltre i metadati? richiede conoscenza assente dallo stimolo? |
| attribuzione vs classificazione | il target è una proprietà della *genesi* dell'oggetto (data, autore, luogo, provenienza) o del suo contenuto? |
| interpretazione vs ragionamento culturale | il benchmark tratta la risposta corretta come variabile per comunità culturale o linguistica? |

Nessuna di queste domande decide se un task è interpretativo. Registrano come il benchmark è stato costruito e lasciano che la conseguenza emerga.

## 4. Le sette sfaccettature

Sei a valore chiuso più una di corredo in testo libero. Il criterio di inclusione è stato uno solo: **ogni sfaccettatura deve essere qualcosa che un paper dichiara**, non qualcosa che un lettore deve giudicare.

**`gold_source`** — come sono state prodotte le risposte di riferimento.
`existing_metadata` (processo documentario che già descriveva l'oggetto: schede catalografiche, metadati di biblioteca o museo, strumenti di corredo archivistici, database strutturati) · `authored_answer_key` (materiale preesistente autorato come valutazione o riferimento: chiavi di esami e quiz, soluzioni di manuali, test standardizzati, voci enciclopediche) · `crowd_annotation` (annotatori senza formazione disciplinare, reclutati per il benchmark) · `domain_expert` (annotatori con formazione nella disciplina) · `paper_authors` (gli autori hanno scritto item e risposte) · `model_generated` (un modello ha prodotto, tradotto o filtrato le risposte) · `not_stated`

È il proxy singolo più informativo di quanta interpretazione è incorporata nella ground truth.

La distinzione fra `existing_metadata` e `authored_answer_key` è stata aggiunta **dopo i primi quattro paper della prima estrazione**, e il caso che l'ha imposta merita di essere riportato perché illustra come funziona questo strumento. Su MMLU l'agente aveva scelto `existing_metadata`, unica opzione vicina disponibile, ma la sua `facets_explanation` diceva la verità: gli item provengono da esami di pratica e manuali raccolti da studenti. Una chiave di risposta GRE e una scheda catalografica museale non hanno lo stesso statuto epistemico — la prima è autorata come item di test, la seconda è il prodotto di un processo documentario curatoriale — e conflagrarle avrebbe silenziosamente indebolito la variabile più portante dello schema.

Due conseguenze metodologiche. La prima: il campo di corredo in testo libero non è ornamentale, è il meccanismo che ha reso l'errore **visibile** invece di seppellirlo in una categoria plausibile. La seconda: l'estrazione è stata interrotta e ripresa da zero sui paper già fatti, perché una distinzione assente dal set di valori non è recuperabile a posteriori dai valori stessi — a differenza dei confini fra categorie di task, che per costruzione sono ricalcolabili offline. Il set di valori di una sfaccettatura è l'unica parte di questo disegno che costa una nuova estrazione se cambia.

**`gold_beyond_stimulus`** — rispondere richiede conoscenza non presente nello stimolo mostrato al modello?
`yes` · `no` · `not_stated`

Il criterio guarda la risposta di riferimento, non la difficoltà: identificare una figura da una didascalia già nell'input è `no`; identificarla da attributi iconografici da confrontare con una tradizione esterna è `yes`.

**`gold_community_dependent`** — il benchmark tratta la risposta corretta come variabile per comunità culturale o linguistica?
`yes` · `no` · `not_stated`

Richiede evidenza positiva: gold per regione o per lingua, split per locale, correttezza dichiaratamente relativa a una comunità. Un benchmark semplicemente multilingue con un'unica chiave universale è `no`.

**`gold_concerns_genesis`** — il target è una proprietà di come l'oggetto è venuto all'esistenza (data, autore, luogo d'origine, provenienza, storia materiale) anziché del suo contenuto?
`yes` · `no` · `not_stated`

**`answer_multiplicity`** — quante risposte accetta lo scoring per item.
`single_answer` (una chiave, exact match o un'opzione corretta) · `answer_set` (più risposte enumerate accettate) · `graded_human_judgment` (valutazione su scala da giudici umani o LLM anziché match con una chiave) · `not_stated`

È l'asse del *formato* separato da quello dell'*operazione* — la distinzione che rendeva incoerente il campo unico precedente, dove `multiple_choice_qa` (formato) e `interpretation` (operazione) convivevano come se fossero alternative sullo stesso asse.

**`plurality_treatment`** — come il paper tratta la divergenza fra annotatori o fra letture difendibili.
`noise` (filtrata, risolta a maggioranza, o riportata come basso accordo inter-annotatore da minimizzare) · `signal` (preservata e trattata come informativa sul materiale) · `not_addressed`

È la sfaccettatura che porta il peso teorico maggiore: misura se il campo riconosce la pluralità interpretativa o la tratta come errore di annotazione. Ed è un fatto testuale sulla posizione dichiarata del paper, non un giudizio di chi codifica.

**`facets_explanation`** — testo libero: l'evidenza nel paper per i valori sopra, con particolare attenzione ai casi in cui le fonti sono mescolate o il paper è ambiguo.

Il principio di design è lo stesso applicato altrove nello strumento: **vocabolario chiuso per ciò che deve essere aggregabile, testo libero accanto per ciò che non deve andare perduto.**

### Il valore `not_stated` non è un dato mancante

È una misura. Un benchmark che non dichiara come ha prodotto la ground truth su materiale umanistico è esso stesso un reperto, e il tasso di `not_stated` per sfaccettatura è un risultato riportabile. Per questo `not_stated` è un valore esplicito e distinguibile da `no`: il silenzio del paper non deve collassare in una negazione.

## 5. I confini diventano cluster derivati a posteriori

Conseguenza principale: le categorie contestate non vengono più dichiarate, vengono **ricavate** raggruppando i benchmark nello spazio delle sfaccettature.

Questo ha tre effetti.

**Il taglio è revisionabile a costo zero.** Cambiare idea su dove passa la linea fra interpretazione e ragionamento culturale non richiede una nuova estrazione: richiede un nuovo raggruppamento su dati già acquisiti, ripetibile quante volte serve. Nessun ripensamento sui confini costa più chiamate API.

**Il taglio è ispezionabile.** Riportando le sfaccettature grezze accanto ai cluster, un lettore che non condivide il raggruppamento può rifarlo con il proprio. L'argomento non dipende dall'accettazione della tassonomia di chi scrive.

**Il taglio è dichiarato come interpretazione.** Un cluster derivato si presenta per quello che è — una lettura dei dati — mentre una categoria dichiarata a monte si presenta come proprietà dell'oggetto.

## 6. Il disaccordo fra le personae come dato

Lo strumento fa leggere ogni paper a due agenti con retroterra diverso — `ciop`, formazione umanistica; `cip`, formazione ML/NLP — e a un terzo agente il compito di adjudicare. L'analisi del primo run aveva mostrato che il disaccordo era sistematico e leggibile: il reviewer dava ragione a `cip` su ciò che è verificabile nel testo (nome esatto del benchmark 6-1, dimensione del dataset 4-0) e a `ciop` sul giudizio disciplinare (`humanities_role` 9-7).

L'adjudication, però, **cancella** quel segnale. Ed è precisamente il segnale che il survey ha motivo di guardare: quali proprietà dei benchmark vengono lette in modo diverso da uno sguardo umanistico e da uno tecnico è una misura dello scarto epistemico di cui il survey parla.

La soluzione implementata non richiede un campo aggiuntivo né chiamate in più. I report delle due personae sono già persistiti separatamente in `output/papers/agents/{id}.ciop.json` e `{id}.cip.json`: il disaccordo per sfaccettatura si **calcola offline** confrontandoli, a costo zero e in modo riproducibile. Il reviewer continua ad adjudicare un valore finale — serve un corpus utilizzabile — ma le due letture originali restano disponibili accanto.

## 7. Limiti dichiarati

**I cluster potrebbero non essere disciplinarmente interessanti.** Nulla garantisce che raggruppare nello spazio delle sfaccettature produca regioni epistemologicamente significative anziché riflettere mode nella costruzione dei dataset. La mitigazione è riportare sempre le sfaccettature grezze accanto ai cluster, così il risultato non dipende dalla riuscita del raggruppamento.

**Le sfaccettature restano una scelta teorica.** Aver spostato la domanda da categorie a proprietà osservabili riduce l'arbitrio, non lo elimina: decidere che `gold_source` e `plurality_treatment` sono le proprietà rilevanti è già una posizione. La differenza è che ora la posizione è ispezionabile e criticabile in una riga, invece di essere sepolta in un giudizio caso per caso.

**L'estrazione non è validata contro codifica umana.** Le due personae concordano fra loro, che è cosa diversa dall'avere ragione: due agenti possono sbagliare insieme in modo sistematico, e un vocabolario chiuso *aumenta* questo rischio perché li vincola a convergere. Un subset codificato a mano e confrontato con l'output della pipeline è il passo che manca per la validità esterna.

**Il vecchio campo `analytical_tasks` è stato conservato.** Non è ridondanza involontaria: sui termini non contestati (`translation`, `transcription_and_correction`, `multiple_choice_qa`) resta valido, e la sovrapposizione con le nuove sfaccettature funziona da controllo di consistenza gratuito fra due codifiche indipendenti dello stesso materiale.
