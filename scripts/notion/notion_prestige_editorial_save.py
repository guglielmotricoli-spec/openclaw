#!/usr/bin/env python3
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import date


NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN")
DATABASE_ID = os.getenv("NOTION_PRESTIGE_EDITORIAL_DATABASE_ID")


if not NOTION_API_TOKEN:
    print("ERRORE: NOTION_API_TOKEN mancante", file=sys.stderr)
    sys.exit(1)

if not DATABASE_ID:
    print("ERRORE: NOTION_PRESTIGE_EDITORIAL_DATABASE_ID mancante", file=sys.stderr)
    sys.exit(1)


NOTION_VERSION = "2022-06-28"


def rich_text(value, limit=1900):
    value = "" if value is None else str(value)
    return [{"text": {"content": value[:limit]}}]


def title_text(value):
    value = value or "Prestige Editorial"
    return [{"text": {"content": str(value)[:200]}}]


def select_value(value):
    if not value:
        return None
    return {"name": str(value)[:100]}


def multi_select_value(values):
    if not values:
        return []

    if isinstance(values, str):
        raw_items = [item.strip() for item in values.replace(";", ",").split(",")]
    elif isinstance(values, list):
        raw_items = [str(item).strip() for item in values]
    else:
        raw_items = [str(values).strip()]

    return [{"name": item[:100]} for item in raw_items if item]


def url_value(value):
    if not value:
        return None
    return str(value)


def date_value(value):
    if not value:
        return None
    return {"start": str(value)}


def paragraph(text):
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": rich_text(text, 1900)
        }
    }


def heading(text, level=2):
    block_type = "heading_2" if level == 2 else "heading_3"
    return {
        "object": "block",
        "type": block_type,
        block_type: {
            "rich_text": rich_text(text, 200)
        }
    }


def divider():
    return {
        "object": "block",
        "type": "divider",
        "divider": {}
    }


def normalize_payload(data):
    if not isinstance(data, dict):
        raise ValueError("Il payload JSON deve essere un oggetto.")

    name = (
        data.get("name")
        or data.get("titolo")
        or data.get("title")
        or "Prestige Editorial"
    )

    tipo_contenuto = (
        data.get("tipo_contenuto")
        or data.get("tipo")
        or data.get("content_type")
        or "News"
    )

    categoria = data.get("categoria") or "Immobiliare"
    area_geografica = data.get("area_geografica") or data.get("area") or "Biellese, Piemonte"

    stato_revisione = data.get("stato_revisione") or "Bozza"
    stato_pubblicazione = data.get("stato_pubblicazione") or "Non pubblicato"
    priorita = data.get("priorita") or data.get("priorità") or "Media"
    agente = data.get("agente") or "Editorial Hub"

    return {
        "name": name,
        "data_creazione": data.get("data_creazione") or data.get("data") or str(date.today()),
        "data_pubblicazione": data.get("data_pubblicazione"),
        "tipo_contenuto": tipo_contenuto,
        "categoria": categoria,
        "area_geografica": area_geografica,
        "fonte": data.get("fonte") or "",
        "link_fonte": data.get("link_fonte") or data.get("url_fonte"),
        "fonti_citate": data.get("fonti_citate") or data.get("fonti") or "",
        "stato_revisione": stato_revisione,
        "stato_pubblicazione": stato_pubblicazione,
        "priorita": priorita,
        "agente": agente,
        "seo_keyword": data.get("seo_keyword") or "",
        "titolo_seo": data.get("titolo_seo") or "",
        "meta_description": data.get("meta_description") or "",
        "slug": data.get("slug") or "",
        "link_bozza": data.get("link_bozza"),
        "link_pubblicazione": data.get("link_pubblicazione"),
        "note_revisione": data.get("note_revisione") or data.get("note") or "",
        "prossima_azione": data.get("prossima_azione") or "",
        "details": data.get("details") or data.get("contenuto") or data.get("body") or "",
        "sections": data.get("sections") or {},
    }


def build_properties(data):
    properties = {
        "Name": {"title": title_text(data["name"])},
        "Data Creazione": {"date": date_value(data["data_creazione"])},
        "Tipo Contenuto": {"select": select_value(data["tipo_contenuto"])},
        "Categoria": {"select": select_value(data["categoria"])},
        "Area Geografica": {"multi_select": multi_select_value(data["area_geografica"])},
        "Fonte": {"rich_text": rich_text(data["fonte"])},
        "Fonti Citate": {"rich_text": rich_text(data["fonti_citate"])},
        "Stato Revisione": {"select": select_value(data["stato_revisione"])},
        "Stato Pubblicazione": {"select": select_value(data["stato_pubblicazione"])},
        "Priorità": {"select": select_value(data["priorita"])},
        "Agente": {"select": select_value(data["agente"])},
        "SEO Keyword": {"rich_text": rich_text(data["seo_keyword"])},
        "Titolo SEO": {"rich_text": rich_text(data["titolo_seo"])},
        "Meta Description": {"rich_text": rich_text(data["meta_description"])},
        "Slug": {"rich_text": rich_text(data["slug"])},
        "Note Revisione": {"rich_text": rich_text(data["note_revisione"])},
        "Prossima Azione": {"rich_text": rich_text(data["prossima_azione"])},
    }

    if data.get("data_pubblicazione"):
        properties["Data Pubblicazione"] = {"date": date_value(data["data_pubblicazione"])}

    if data.get("link_fonte"):
        properties["Link Fonte"] = {"url": url_value(data["link_fonte"])}

    if data.get("link_bozza"):
        properties["Link Bozza"] = {"url": url_value(data["link_bozza"])}

    if data.get("link_pubblicazione"):
        properties["Link Pubblicazione"] = {"url": url_value(data["link_pubblicazione"])}

    return properties


def build_children(data):
    children = []

    children.append(heading("Executive summary"))
    summary = data["details"] or data["note_revisione"] or "Scheda editoriale Prestige."
    children.append(paragraph(summary))

    sections = data.get("sections") or {}

    required_sections = {
        "Fonti verificate o da verificare": data.get("fonti_citate") or data.get("fonte") or "Fonti da verificare.",
        "Contesto editoriale": "",
        "Rilevanza per Prestige Immobiliare": "",
        "Rilevanza per Biellese/Piemonte": "",
        "Bozza contenuto": data.get("details") or "",
        "Materiali social collegati": "",
        "Revisione e rischi": data.get("note_revisione") or "",
        "Checklist pubblicazione": "",
        "Prossima azione": data.get("prossima_azione") or "",
    }

    merged_sections = dict(required_sections)
    merged_sections.update(sections)

    for title, content in merged_sections.items():
        children.append(divider())
        children.append(heading(str(title)))
        if isinstance(content, (dict, list)):
            content = json.dumps(content, ensure_ascii=False, indent=2)
        children.append(paragraph(str(content or "Da completare.")))

    return children[:100]


def notion_request(path, payload):
    url = f"https://api.notion.com/v1/{path}"
    body = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {NOTION_API_TOKEN}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(f"ERRORE Notion HTTP {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"ERRORE Notion URL: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    payload_input = sys.stdin.read().strip()

    if not payload_input:
        print("ERRORE: payload JSON mancante. Non creo pagine Notion vuote.", file=sys.stderr)
        sys.exit(1)

    try:
        raw_data = json.loads(payload_input)
    except json.JSONDecodeError as e:
        print(f"ERRORE: payload JSON non valido: {e}", file=sys.stderr)
        sys.exit(1)

    data = normalize_payload(raw_data)

    if not data["name"] or (not data["details"] and not data["sections"]):
        print("ERRORE: payload troppo vuoto. Servono almeno name e details/sections.", file=sys.stderr)
        sys.exit(1)

    page_payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": build_properties(data),
        "children": build_children(data),
    }

    result = notion_request("pages", page_payload)

    output = {
        "ok": True,
        "database": "Prestige Editorial",
        "page_id": result.get("id"),
        "url": result.get("url"),
        "name": data["name"],
        "tipo_contenuto": data["tipo_contenuto"],
        "categoria": data["categoria"],
        "agente": data["agente"],
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
