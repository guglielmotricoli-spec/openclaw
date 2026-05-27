# OpenClaw Architecture Lock

Ultimo aggiornamento: 2026-05-27

Questo file definisce i confini operativi del progetto OpenClaw / Prestige / Trend2Video AI.

Prima di modificare agenti, skill, cron, routing Telegram, Notion o automazioni, leggere questo file.

## Regola principale

Non mischiare i flussi.

Prestige Editorial, Trend2Video AI, Research Radar, Video Intelligence e Weekly Orchestrator sono domini separati.

Non spostare cron, skill o comandi tra domini senza backup e decisione esplicita dell'utente.

## Stato agenti

### main

Ruolo attuale:

- agente default;
- riceve Telegram di default;
- mantiene il flusso Prestige Editorial collaudato;
- mantiene compatibilità con comandi esistenti;
- non deve essere caricato ulteriormente con nuove logiche Trend2Video se non strettamente necessario.

Non rimuovere da main senza autorizzazione:

- prestige-editorial;
- cron editoriale Prestige;
- comandi editoriali già collaudati.

### research

Identità:

Research Radar

Ruolo:

- opportunità business globali;
- trend economici e di mercato;
- landing page;
- funnel;
- MVP;
- monetizzazione;
- fonti verificabili o fonti da verificare;
- salvataggio Notion solo quando richiesto o nei flussi operativi.

Skill principale:

- trend-research-agent

Non deve gestire:

- news editoriali Prestige;
- articoli immobiliari Prestige;
- video remix complessi;
- cron editoriale Prestige.

### video

Identità:

Video Intelligence

Ruolo:

- video virali;
- analisi fonti video;
- trascrizione o piano di trascrizione;
- remix originali;
- storyboard;
- script TikTok / Reels / Shorts;
- prompt LTX Studio;
- prompt Magnific / Freepik;
- prompt Easy-Peasy AI;
- task Manus;
- diagrammi e checklist produzione;
- salvataggio Notion completo dei flussi video.

Skill principale:

- trend-video-agent

Non deve gestire:

- news editoriali Prestige;
- business radar settimanale generale;
- cron editoriale Prestige.

### weekly

Identità:

Weekly Orchestrator

Ruolo:

- cron settimanale Trend2Video AI;
- ricerca opportunità globali;
- selezione opportunità migliori;
- landing / funnel / MVP;
- eventuale video strategy per opportunità migliore;
- salvataggio Notion completo;
- riepilogo breve Telegram.

Skill principali:

- trend-research-agent;
- trend-video-agent;
- trend-business-agent solo se ancora necessario per retrocompatibilità.

Non deve gestire:

- cron Prestige Editorial;
- articoli immobiliari Prestige;
- comandi /news, /fonti, /articolo, /social, /mercato, /prezzi.

## Prestige Editorial

Prestige Editorial è un flusso già collaudato.

Serve a:

- cercare notizie economiche, finanziarie, immobiliari e territoriali;
- selezionare fonti verificabili;
- produrre spunti editoriali;
- preparare articoli news, breaking news e blog;
- citare fonti;
- scrivere testo originale, non copiato;
- creare materiali social collegati;
- preparare preview;
- preparare email di approvazione;
- lavorare su Biellese, Piemonte, mercato immobiliare, economia, prezzi, trend e statistiche.

Comandi editoriali principali:

- /news
- /fonti
- /articolo
- /social
- /revisione
- /piano
- /statistiche
- /mercato
- /prezzi
- /preview
- /email_preview
- /mail_preview
- /approva
- /prestige

Regole:

- /news appartiene a Prestige Editorial.
- /fonti appartiene a Prestige Editorial.
- /articolo appartiene a Prestige Editorial.
- /mercato e /prezzi, se riferiti al contesto Prestige, appartengono a Prestige Editorial.
- Non usare /news per Trend2Video AI.
- Non modificare il flusso Prestige Editorial senza backup e conferma esplicita.

## Cron

### prestige-materiali-settimanale

Dominio:

Prestige Editorial

Stato:

- cron già collaudato;
- non spostare senza autorizzazione;
- resta su main finché non viene deciso diversamente.

Scopo:

- generare materiali editoriali settimanali Prestige;
- cercare notizie economiche, finanziarie, immobiliari e territoriali;
- produrre spunti per news, articoli, blog e social;
- mantenere fonti citabili;
- scrivere contenuti originali.

### trend2video-ai-settimanale

Dominio:

Trend2Video AI / Weekly Business Radar

Stato:

- cron aggiornato su agentId weekly;
- deve generare opportunità business globali;
- deve creare landing, funnel, MVP e video strategy opzionale;
- deve salvare in Notion con campi estesi e sections dettagliate;
- deve inviare su Telegram solo sintesi breve e link Notion.

## Notion

Notion è il centro archivio operativo.

Database esteso già predisposto con colonne:

- Name
- Data
- Trend
- Stato
- Note
- Tipo
- Target
- Piattaforma
- Tool
- Priorità
- Potenziale
- Difficoltà
- Fonte
- Stato Produzione
- Data Pubblicazione
- Link Output

Script principale:

/home/node/.openclaw/workspace/scripts/notion_trend2video_save.py

Copia versionata nel repo:

scripts/notion_trend2video_save.py

Regole:

- non creare pagine vuote;
- usare JSON completo;
- compilare campi estesi;
- usare sections dettagliate;
- salvare output lunghi in Notion, non solo in Telegram;
- Telegram deve ricevere sintesi e link.

## Fonti

Non inventare fonti.

Se un agente ha accesso reale al web/browser, deve indicare:

- titolo;
- URL o riferimento;
- data se disponibile;
- motivo di rilevanza;
- cosa supporta.

Se non ha accesso reale al web, deve scrivere:

Fonti da verificare

e fornire query precise per:

- Manus;
- browser;
- Google;
- Reddit;
- Product Hunt;
- TikTok;
- YouTube;
- newsletter;
- report di settore.

## Regole di sicurezza

Prima di modificare:

- openclaw.json;
- agenti;
- routing;
- cron;
- skill collaudate;
- script Notion;
- file .env;

fare backup locale.

Non committare mai:

- .env;
- .env.before-*;
- token;
- credenziali;
- backup .tar.gz;
- cartelle .openclaw complete.

## Regola anti-confusione

Non aggiungere nuove skill a main se appartengono a un dominio separato.

Non usare trend-business-agent come contenitore universale.

Non sovrapporre:

- Prestige Editorial;
- Business Radar;
- Video Intelligence;
- Weekly Orchestrator.

Se un comando è ambiguo, chiarire il dominio prima di modificare configurazioni.

## Stato blocco attuale

Al 2026-05-27:

- agenti creati: main, research, video, weekly;
- research funziona ma test generativi bloccati da quota Gemini 429;
- video creato e pronto per test futuri;
- weekly creato e collegato al cron Trend2Video AI;
- Prestige Editorial resta su main;
- cron Prestige Editorial resta su main;
- cron Trend2Video AI punta a weekly;
- script Notion avanzato versionato su Git;
- backup locale post-agenti e post-cron creato.
