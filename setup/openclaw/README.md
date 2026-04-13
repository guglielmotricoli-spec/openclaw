# OpenClaw setup versionato

Questa cartella contiene solo la parte sicura e riproducibile della configurazione OpenClaw usata per gli agenti editoriali.

## Cosa viene versionato

- prompt personalizzati degli agenti editoriali
- file di supporto per ricreare gli agenti
- documentazione operativa minima

## Cosa NON viene versionato

- ~/.openclaw/openclaw.json reale
- ~/.openclaw/.env
- credenziali, token, auth profiles
- sessioni agenti
- log runtime
- stato locale della macchina

## Agenti editoriali attuali

- caporedattore
- news-immobiliari
- seo-blog
- repurposer
- researcher

## Note operative

Gli AGENTS.md personalizzati sono salvati in:
setup/editorial-agents/

La configurazione locale reale resta fuori repo in:
~/.openclaw/
