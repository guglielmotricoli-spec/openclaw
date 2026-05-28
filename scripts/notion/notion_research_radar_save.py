#!/usr/bin/env python3
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import date


NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN")
DATABASE_ID = os.getenv("NOTION_RESEARCH_RADAR_DATABASE_ID")

if not NOTION_API_TOKEN:
    print("ERRORE: NOTION_API_TOKEN mancante", file=sys.stderr)
    sys.exit(1)

if not DATABASE_ID:
    print("ERRORE: NOTION_RESEARCH_RADAR_DATABASE_ID mancante", file=sys.stderr)
    sys.exit(1)


NOTION_VERSION = "2022-06-28"


def rich_text(value, limit=1900):
    value = "" if value is None else str(value)
    return [{"text": {"content": value[:limit]}}]


def title_text(value):
    value = value or "Research Radar"
    return [{"text": {"content": str(value)[:200]}}]


def select_value(value):
    if not value:
        return None
    return {"name": str(value)[:100]}


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
        "paragraph": {"rich_text": rich_text(text, 1900)}
    }


def heading(text, level=2):
    block_type = "heading_2" if level == 2 else "heading_3"
    return {
        "object": "block",
        "type": block_type,
        block_type: {"rich_text": rich_text(text, 200)}
    }


def divider():
    return {"object": "block", "type": "divider", "divider": {}}


def normalize_payload(data):
    if not isinstance(data, dict):
        raise ValueError("Il payload JSON deve essere un oggetto.")

    return {
        "name": data.get("name") or data.get("titolo") or data.get("title") or "Research Radar",
        "data": data.get("data") or str(date.today()),
        "tipo": data.get("tipo") or "Business Plan",
        "categoria": data.get("categoria") or "AI",
        "target": data.get("target") or "",
        "trend": data.get("trend") or "",
        "problema": data.get("problema") or "",
        "soluzione": data.get("soluzione") or "",
        "mercato": data.get("mercato") or "",
        "modello_ricavo": data.get("modello_ricavo") or data.get("modello ricavo") or "Servizio",
        "priorita": data.get("priorita") or data.get("priorità") or "Media",
        "potenziale": str(data.get("potenziale") or "3"),
        "difficolta": str(data.get("difficolta") or data.get("difficoltà") or "3"),
        "stato_produzione": data.get("stato_produzione") or "Idea",
        "fonte": data.get("fonte") or "",
        "link_fonte": data.get("link_fonte") or data.get("url_fonte"),
        "fonti_da_verificare": data.get("fonti_da_verificare") or "",
        "link_output": data.get("link_output"),
        "prossima_azione": data.get("prossima_azione") or "",
        "details": data.get("details") or data.get("note") or "",
        "sections": data.get("sections") or {},
    }


def build_properties(data):
    props = {
        "Name": {"title": title_text(data["name"])},
        "Data": {"date": date_value(data["data"])},
        "Tipo": {"select": select_value(data["tipo"])},
        "Categoria": {"select": select_value(data["categoria"])},
        "Target": {"rich_text": rich_text(data["target"])},
        "Trend": {"rich_text": rich_text(data["trend"])},
        "Problema": {"rich_text": rich_text(data["problema"])},
        "Soluzione": {"rich_text": rich_text(data["soluzione"])},
        "Mercato": {"rich_text": rich_text(data["mercato"])},
        "Modello Ricavo": {"select": select_value(data["modello_ricavo"])},
        "Priorità": {"select": select_value(data["priorita"])},
        "Potenziale": {"select": select_value(data["potenziale"])},
        "Difficoltà": {"select": select_value(data["difficolta"])},
        "Stato Produzione": {"select": select_value(data["stato_produzione"])},
        "Fonte": {"rich_text": rich_text(data["fonte"])},
        "Fonti da Verificare": {"rich_text": rich_text(data["fonti_da_verificare"])},
        "Prossima Azione": {"rich_text": rich_text(data["prossima_azione"])},
    }

    if data.get("link_fonte"):
        props["Link Fonte"] = {"url": url_value(data["link_fonte"])}

    if data.get("link_output"):
        props["Link Output"] = {"url": url_value(data["link_output"])}

    return props


def build_children(data):
    children = [
        heading("Executive summary"),
        paragraph(data["details"] or "Scheda Research Radar."),
    ]

    required = {
        "Trend intercettato": data.get("trend") or "",
        "Fonti verificate o da verificare": data.get("fonte") or data.get("fonti_da_verificare") or "Fonti da verificare.",
        "Perché è rilevante adesso": "",
        "Mercato": data.get("mercato") or "",
        "Target": data.get("target") or "",
        "Problema": data.get("problema") or "",
        "Soluzione": data.get("soluzione") or "",
        "Offerta monetizzabile": "",
        "Modello di ricavo": data.get("modello_ricavo") or "",
        "Pricing": "",
        "MVP in 7 giorni": "",
        "Landing page": "",
        "Funnel": "",
        "Canali di acquisizione": "",
        "Competitor o benchmark da verificare": "",
        "Rischi": "",
        "Metriche da misurare": "",
        "Piano operativo 7 giorni": "",
        "Prossima azione": data.get("prossima_azione") or "",
    }

    merged = dict(required)
    merged.update(data.get("sections") or {})

    for title, content in merged.items():
        children.append(divider())
        children.append(heading(str(title)))
        if isinstance(content, (dict, list)):
            content = json.dumps(content, ensure_ascii=False, indent=2)
        children.append(paragraph(str(content or "Da completare.")))

    return children[:100]


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
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"ERRORE Notion HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}", file=sys.stderr)
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
        raw = json.loads(payload_input)
    except json.JSONDecodeError as e:
        print(f"ERRORE: payload JSON non valido: {e}", file=sys.stderr)
        sys.exit(1)

    data = normalize_payload(raw)

    if not data["name"] or (not data["details"] and not data["sections"]):
        print("ERRORE: payload troppo vuoto. Servono almeno name e details/sections.", file=sys.stderr)
        sys.exit(1)

    result = notion_request("pages", {
        "parent": {"database_id": DATABASE_ID},
        "properties": build_properties(data),
        "children": build_children(data),
    })

    print(json.dumps({
        "ok": True,
        "database": "Research Radar",
        "page_id": result.get("id"),
        "url": result.get("url"),
        "name": data["name"],
        "tipo": data["tipo"],
        "categoria": data["categoria"],
        "target": data["target"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
