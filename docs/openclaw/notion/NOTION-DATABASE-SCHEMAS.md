# Notion Database Schemas — OpenClaw / Prestige / Trend2Video AI

Ultimo aggiornamento: 2026-05-27

Questo documento definisce i database Notion ufficiali per gli agenti OpenClaw.

I database devono restare separati per evitare confusione tra editoriale, business research, video production e report settimanali.

## Database 1 — Prestige Editorial

Nome consigliato:

Prestige Editorial

Scopo:

Archiviare materiali editoriali Prestige Immobiliare: fonti, news, articoli, blog, post social, preview, email di approvazione e stato pubblicazione.

Agenti collegati:

- editorial
- editorial-research
- editorial-writer
- editorial-social
- editorial-approval

Proprietà Notion:

- Name — Title
- Data Creazione — Date
- Data Pubblicazione — Date
- Tipo Contenuto — Select
  - Fonte
  - News
  - Breaking News
  - Articolo Blog
  - Post Social
  - Carosello
  - Preview
  - Email Approvazione
  - Piano Editoriale
- Categoria — Select
  - Economia
  - Finanza
  - Immobiliare
  - Mercato Casa
  - Mutui
  - Prezzi
  - Normative
  - Territorio
  - Biellese
  - Piemonte
  - Investimenti
- Area Geografica — Multi-select
  - Italia
  - Piemonte
  - Biella
  - Biellese
  - Lombardia
  - Europa
  - Globale
- Fonte — Rich text
- Link Fonte — URL
- Fonti Citate — Rich text
- Stato Revisione — Select
  - Bozza
  - Da verificare
  - In revisione
  - Approvato
  - Da modificare
  - Bloccato
- Stato Pubblicazione — Select
  - Non pubblicato
  - Programmato
  - Pubblicato
  - Archiviato
- Priorità — Select
  - Alta
  - Media
  - Bassa
- Agente — Select
  - Editorial Hub
  - Editorial Research
  - Editorial Writer
  - Editorial Social
  - Editorial Approval
- SEO Keyword — Rich text
- Titolo SEO — Rich text
- Meta Description — Rich text
- Slug — Rich text
- Link Bozza — URL
- Link Pubblicazione — URL
- Note Revisione — Rich text
- Prossima Azione — Rich text

Sections obbligatorie nella pagina:

- Executive summary
- Fonti verificate o da verificare
- Contesto editoriale
- Rilevanza per Prestige Immobiliare
- Rilevanza per Biellese/Piemonte
- Bozza contenuto
- Materiali social collegati
- Revisione e rischi
- Checklist pubblicazione
- Prossima azione

## Database 2 — Research Radar

Nome consigliato:

Research Radar

Scopo:

Archiviare opportunità business, trend globali, analisi mercato, landing page, funnel, MVP e monetizzazione.

Agenti collegati:

- research

Proprietà Notion:

- Name — Title
- Data — Date
- Tipo — Select
  - Business Plan
  - Trend
  - Market Scan
  - Landing Plan
  - Funnel Plan
  - MVP Plan
- Categoria — Select
  - AI
  - Immobiliare
  - Finanza
  - Creator Economy
  - SaaS
  - Local Business
  - E-commerce
  - Education
  - Healthcare
  - Productivity
  - Marketing
  - Altro
- Target — Rich text
- Trend — Rich text
- Problema — Rich text
- Soluzione — Rich text
- Mercato — Rich text
- Modello Ricavo — Select
  - Subscription
  - One-shot
  - Commissione
  - Lead generation
  - Servizio
  - Marketplace
  - Sponsorship
  - Altro
- Priorità — Select
  - Alta
  - Media
  - Bassa
- Potenziale — Select
  - 1
  - 2
  - 3
  - 4
  - 5
- Difficoltà — Select
  - 1
  - 2
  - 3
  - 4
  - 5
- Stato Produzione — Select
  - Idea
  - Da validare
  - In test
  - Validato
  - Scartato
  - Da produrre
- Fonte — Rich text
- Link Fonte — URL
- Fonti da Verificare — Rich text
- Link Output — URL
- Prossima Azione — Rich text

Sections obbligatorie nella pagina:

- Executive summary
- Trend intercettato
- Fonti verificate o da verificare
- Perché è rilevante adesso
- Mercato
- Target
- Problema
- Soluzione
- Offerta monetizzabile
- Modello di ricavo
- Pricing
- MVP in 7 giorni
- Landing page
- Funnel
- Canali di acquisizione
- Competitor o benchmark da verificare
- Rischi
- Metriche da misurare
- Piano operativo 7 giorni
- Prossima azione

## Database 3 — Video Intelligence

Nome consigliato:

Video Intelligence

Scopo:

Archiviare flussi video, remix, fonti video, storyboard, prompt LTX, prompt Easy-Peasy AI, prompt Magnific/Freepik, task Manus e checklist produzione.

Agenti collegati:

- video

Proprietà Notion:

- Name — Title
- Data — Date
- Tipo — Select
  - Viral Video Scan
  - Viral Remix
  - LTX Flow
  - Production Flow
  - Script
  - Storyboard
  - Asset Plan
  - Manus Research
- Target — Rich text
- Trend — Rich text
- Piattaforma — Multi-select
  - TikTok
  - Instagram Reels
  - YouTube Shorts
  - YouTube
  - LinkedIn
  - Facebook
- Tool — Multi-select
  - LTX Studio
  - Easy-Peasy AI
  - Manus
  - Magnific
  - Freepik
  - Notion
  - CapCut
  - Canva
- Fonte Video — Rich text
- Link Fonte Video — URL
- Copyright Risk — Select
  - Basso
  - Medio
  - Alto
  - Da verificare
- Priorità — Select
  - Alta
  - Media
  - Bassa
- Potenziale — Select
  - 1
  - 2
  - 3
  - 4
  - 5
- Difficoltà — Select
  - 1
  - 2
  - 3
  - 4
  - 5
- Stato Produzione — Select
  - Idea
  - Da produrre
  - In produzione
  - Prodotto
  - Pubblicato
  - Archiviato
- Link Output — URL
- Prossima Azione — Rich text

Sections obbligatorie nella pagina:

- Obiettivo video
- Target
- Fonti video verificate o da verificare
- Query di ricerca video
- Analisi format
- Hook
- Script completo
- Storyboard scena per scena
- Shot list
- Prompt LTX Studio scena per scena
- Negative prompt scena per scena
- Prompt Magnific
- Prompt Freepik
- Prompt Easy-Peasy AI
- Task Manus
- Asset reference
- Diagramma Mermaid
- Caption e CTA
- Checklist produzione
- Nota copyright e originalità
- Prossima azione

## Database 4 — Weekly Orchestrator

Nome consigliato:

Weekly Orchestrator

Scopo:

Archiviare report settimanali, ranking opportunità, sintesi strategica, link alle schede Research Radar e Video Intelligence create nella settimana.

Agenti collegati:

- weekly

Proprietà Notion:

- Name — Title
- Data Report — Date
- Settimana — Rich text
- Tipo Report — Select
  - Weekly Business Radar
  - Trend2Video Weekly
  - Weekly Opportunities
  - Strategic Report
- Stato — Select
  - Generato
  - Da verificare
  - Approvato
  - Archiviato
- Migliore Opportunità — Rich text
- Numero Opportunità — Number
- Link Opportunità 1 — URL
- Link Opportunità 2 — URL
- Link Opportunità 3 — URL
- Link Video Strategy — URL
- Priorità Settimana — Select
  - Alta
  - Media
  - Bassa
- Note — Rich text
- Prossima Azione — Rich text

Sections obbligatorie nella pagina:

- Executive summary settimanale
- Macro trend globali
- 5 opportunità candidate
- Ranking delle 3 migliori
- Scheda sintetica opportunità 1
- Scheda sintetica opportunità 2
- Scheda sintetica opportunità 3
- Link alle schede complete
- Video strategy migliore opportunità
- Piano operativo settimanale
- Rischi
- Prossima azione

## Regole generali

Non mischiare database.

Prestige Editorial non deve salvare nel database Research Radar.
Research Radar non deve salvare nel database Prestige Editorial.
Video Intelligence non deve salvare nel database Prestige Editorial.
Weekly Orchestrator deve salvare il report nel proprio database e collegare le schede create negli altri database.

## Variabili ambiente consigliate

- NOTION_PRESTIGE_EDITORIAL_DATABASE_ID
- NOTION_RESEARCH_RADAR_DATABASE_ID
- NOTION_VIDEO_INTELLIGENCE_DATABASE_ID
- NOTION_WEEKLY_ORCHESTRATOR_DATABASE_ID

La variabile legacy NOTION_TREND2VIDEO_DATABASE_ID può restare per retrocompatibilità, ma i nuovi script devono usare database separati.

