#!/usr/bin/env python3
import json
import os
import sys
import urllib.request
import urllib.error


NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN")
PARENT_PAGE_ID = os.getenv("NOTION_OPENCLAW_PARENT_PAGE_ID")
NOTION_VERSION = "2022-06-28"


if not NOTION_API_TOKEN:
    print("ERRORE: NOTION_API_TOKEN mancante", file=sys.stderr)
    sys.exit(1)

if not PARENT_PAGE_ID:
    print("ERRORE: NOTION_OPENCLAW_PARENT_PAGE_ID mancante", file=sys.stderr)
    print("Imposta questa variabile con l'ID della pagina Notion dove creare i 4 database.", file=sys.stderr)
    sys.exit(1)


def title_schema():
    return {"title": {}}


def rich_text_schema():
    return {"rich_text": {}}


def date_schema():
    return {"date": {}}


def url_schema():
    return {"url": {}}


def number_schema():
    return {"number": {"format": "number"}}


def select_schema(options):
    return {
        "select": {
            "options": [{"name": str(option)} for option in options]
        }
    }


def multi_select_schema(options):
    return {
        "multi_select": {
            "options": [{"name": str(option)} for option in options]
        }
    }


def notion_request(path, payload):
    req = urllib.request.Request(
        f"https://api.notion.com/v1/{path}",
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {NOTION_API_TOKEN}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"ERRORE Notion HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"ERRORE Notion URL: {e}", file=sys.stderr)
        sys.exit(1)


def create_database(title, properties):
    payload = {
        "parent": {"type": "page_id", "page_id": PARENT_PAGE_ID},
        "title": [{"type": "text", "text": {"content": title}}],
        "properties": properties,
    }
    return notion_request("databases", payload)


DATABASES = [
    {
        "key": "NOTION_PRESTIGE_EDITORIAL_DATABASE_ID",
        "title": "Prestige Editorial",
        "properties": {
            "Name": title_schema(),
            "Data Creazione": date_schema(),
            "Data Pubblicazione": date_schema(),
            "Tipo Contenuto": select_schema([
                "Fonte", "News", "Breaking News", "Articolo Blog", "Post Social",
                "Carosello", "Preview", "Email Approvazione", "Piano Editoriale"
            ]),
            "Categoria": select_schema([
                "Economia", "Finanza", "Immobiliare", "Mercato Casa", "Mutui",
                "Prezzi", "Normative", "Territorio", "Biellese", "Piemonte",
                "Investimenti"
            ]),
            "Area Geografica": multi_select_schema([
                "Italia", "Piemonte", "Biella", "Biellese", "Lombardia", "Europa", "Globale"
            ]),
            "Fonte": rich_text_schema(),
            "Link Fonte": url_schema(),
            "Fonti Citate": rich_text_schema(),
            "Stato Revisione": select_schema([
                "Bozza", "Da verificare", "In revisione", "Approvato", "Da modificare", "Bloccato"
            ]),
            "Stato Pubblicazione": select_schema([
                "Non pubblicato", "Programmato", "Pubblicato", "Archiviato"
            ]),
            "Priorità": select_schema(["Alta", "Media", "Bassa"]),
            "Agente": select_schema([
                "Editorial Hub", "Editorial Research", "Editorial Writer",
                "Editorial Social", "Editorial Approval"
            ]),
            "SEO Keyword": rich_text_schema(),
            "Titolo SEO": rich_text_schema(),
            "Meta Description": rich_text_schema(),
            "Slug": rich_text_schema(),
            "Link Bozza": url_schema(),
            "Link Pubblicazione": url_schema(),
            "Note Revisione": rich_text_schema(),
            "Prossima Azione": rich_text_schema(),
        },
    },
    {
        "key": "NOTION_RESEARCH_RADAR_DATABASE_ID",
        "title": "Research Radar",
        "properties": {
            "Name": title_schema(),
            "Data": date_schema(),
            "Tipo": select_schema([
                "Business Plan", "Trend", "Market Scan", "Landing Plan", "Funnel Plan", "MVP Plan"
            ]),
            "Categoria": select_schema([
                "AI", "Immobiliare", "Finanza", "Creator Economy", "SaaS",
                "Local Business", "E-commerce", "Education", "Healthcare",
                "Productivity", "Marketing", "Altro"
            ]),
            "Target": rich_text_schema(),
            "Trend": rich_text_schema(),
            "Problema": rich_text_schema(),
            "Soluzione": rich_text_schema(),
            "Mercato": rich_text_schema(),
            "Modello Ricavo": select_schema([
                "Subscription", "One-shot", "Commissione", "Lead generation",
                "Servizio", "Marketplace", "Sponsorship", "Altro"
            ]),
            "Priorità": select_schema(["Alta", "Media", "Bassa"]),
            "Potenziale": select_schema(["1", "2", "3", "4", "5"]),
            "Difficoltà": select_schema(["1", "2", "3", "4", "5"]),
            "Stato Produzione": select_schema([
                "Idea", "Da validare", "In test", "Validato", "Scartato", "Da produrre"
            ]),
            "Fonte": rich_text_schema(),
            "Link Fonte": url_schema(),
            "Fonti da Verificare": rich_text_schema(),
            "Link Output": url_schema(),
            "Prossima Azione": rich_text_schema(),
        },
    },
    {
        "key": "NOTION_VIDEO_INTELLIGENCE_DATABASE_ID",
        "title": "Video Intelligence",
        "properties": {
            "Name": title_schema(),
            "Data": date_schema(),
            "Tipo": select_schema([
                "Viral Video Scan", "Viral Remix", "LTX Flow", "Production Flow",
                "Script", "Storyboard", "Asset Plan", "Manus Research"
            ]),
            "Target": rich_text_schema(),
            "Trend": rich_text_schema(),
            "Piattaforma": multi_select_schema([
                "TikTok", "Instagram Reels", "YouTube Shorts", "YouTube", "LinkedIn", "Facebook"
            ]),
            "Tool": multi_select_schema([
                "LTX Studio", "Easy-Peasy AI", "Manus", "Magnific", "Freepik",
                "Notion", "CapCut", "Canva"
            ]),
            "Fonte Video": rich_text_schema(),
            "Link Fonte Video": url_schema(),
            "Copyright Risk": select_schema(["Basso", "Medio", "Alto", "Da verificare"]),
            "Priorità": select_schema(["Alta", "Media", "Bassa"]),
            "Potenziale": select_schema(["1", "2", "3", "4", "5"]),
            "Difficoltà": select_schema(["1", "2", "3", "4", "5"]),
            "Stato Produzione": select_schema([
                "Idea", "Da produrre", "In produzione", "Prodotto", "Pubblicato", "Archiviato"
            ]),
            "Link Output": url_schema(),
            "Prossima Azione": rich_text_schema(),
        },
    },
    {
        "key": "NOTION_WEEKLY_ORCHESTRATOR_DATABASE_ID",
        "title": "Weekly Orchestrator",
        "properties": {
            "Name": title_schema(),
            "Data Report": date_schema(),
            "Settimana": rich_text_schema(),
            "Tipo Report": select_schema([
                "Weekly Business Radar", "Trend2Video Weekly", "Weekly Opportunities", "Strategic Report"
            ]),
            "Stato": select_schema(["Generato", "Da verificare", "Approvato", "Archiviato"]),
            "Migliore Opportunità": rich_text_schema(),
            "Numero Opportunità": number_schema(),
            "Link Opportunità 1": url_schema(),
            "Link Opportunità 2": url_schema(),
            "Link Opportunità 3": url_schema(),
            "Link Video Strategy": url_schema(),
            "Priorità Settimana": select_schema(["Alta", "Media", "Bassa"]),
            "Note": rich_text_schema(),
            "Prossima Azione": rich_text_schema(),
        },
    },
]


def main():
    created = {}

    for db in DATABASES:
        print(f"Creo database: {db['title']}...", file=sys.stderr)
        result = create_database(db["title"], db["properties"])
        created[db["key"]] = {
            "id": result.get("id"),
            "url": result.get("url"),
            "title": db["title"],
        }

    print(json.dumps({
        "ok": True,
        "parent_page_id": PARENT_PAGE_ID,
        "databases": created,
        "env_lines": [
            f"{key}={value['id']}" for key, value in created.items()
        ],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
