#!/usr/bin/env python3
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import date


NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN")
DATABASE_ID = os.getenv("NOTION_WEEKLY_ORCHESTRATOR_DATABASE_ID")

if not NOTION_API_TOKEN:
    print("ERRORE: NOTION_API_TOKEN mancante", file=sys.stderr)
    sys.exit(1)

if not DATABASE_ID:
    print("ERRORE: NOTION_WEEKLY_ORCHESTRATOR_DATABASE_ID mancante", file=sys.stderr)
    sys.exit(1)


NOTION_VERSION = "2022-06-28"


def rich_text(value, limit=1900):
    value = "" if value is None else str(value)
    return [{"text": {"content": value[:limit]}}]


def title_text(value):
    value = value or "Weekly Orchestrator"
    return [{"text": {"content": str(value)[:200]}}]


def select_value(value):
    if not value:
        return None
    return {"name": str(value)[:100]}


def number_value(value):
    if value is None or value == "":
        return None
    try:
        return int(value)
    except Exception:
        return None


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
        "name": data.get("name") or data.get("titolo") or data.get("title") or "Weekly Business Radar",
        "data_report": data.get("data_report") or data.get("data") or str(date.today()),
        "settimana": data.get("settimana") or "",
        "tipo_report": data.get("tipo_report") or data.get("tipo") or "Trend2Video Weekly",
        "stato": data.get("stato") or "Generato",
        "migliore_opportunita": data.get("migliore_opportunita") or data.get("migliore_opportunità") or "",
        "numero_opportunita": data.get("numero_opportunita") or data.get("numero_opportunità") or 0,
        "link_opportunita_1": data.get("link_opportunita_1"),
        "link_opportunita_2": data.get("link_opportunita_2"),
        "link_opportunita_3": data.get("link_opportunita_3"),
        "link_video_strategy": data.get("link_video_strategy"),
        "priorita_settimana": data.get("priorita_settimana") or data.get("priorità_settimana") or "Media",
        "note": data.get("note") or "",
        "prossima_azione": data.get("prossima_azione") or "",
        "details": data.get("details") or "",
        "sections": data.get("sections") or {},
    }


def build_properties(data):
    props = {
        "Name": {"title": title_text(data["name"])},
        "Data Report": {"date": date_value(data["data_report"])},
        "Settimana": {"rich_text": rich_text(data["settimana"])},
        "Tipo Report": {"select": select_value(data["tipo_report"])},
        "Stato": {"select": select_value(data["stato"])},
        "Migliore Opportunità": {"rich_text": rich_text(data["migliore_opportunita"])},
        "Priorità Settimana": {"select": select_value(data["priorita_settimana"])},
        "Note": {"rich_text": rich_text(data["note"])},
        "Prossima Azione": {"rich_text": rich_text(data["prossima_azione"])},
    }

    num = number_value(data.get("numero_opportunita"))
    if num is not None:
        props["Numero Opportunità"] = {"number": num}

    if data.get("link_opportunita_1"):
        props["Link Opportunità 1"] = {"url": url_value(data["link_opportunita_1"])}

    if data.get("link_opportunita_2"):
        props["Link Opportunità 2"] = {"url": url_value(data["link_opportunita_2"])}

    if data.get("link_opportunita_3"):
        props["Link Opportunità 3"] = {"url": url_value(data["link_opportunita_3"])}

    if data.get("link_video_strategy"):
        props["Link Video Strategy"] = {"url": url_value(data["link_video_strategy"])}

    return props


def build_children(data):
    children = [
        heading("Executive summary settimanale"),
        paragraph(data["details"] or data["note"] or "Report Weekly Orchestrator."),
    ]

    required = {
        "Macro trend globali": "",
        "5 opportunità candidate": "",
        "Ranking delle 3 migliori": "",
        "Scheda sintetica opportunità 1": "",
        "Scheda sintetica opportunità 2": "",
        "Scheda sintetica opportunità 3": "",
        "Link alle schede complete": "",
        "Video strategy migliore opportunità": "",
        "Piano operativo settimanale": "",
        "Rischi": "",
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
        "database": "Weekly Orchestrator",
        "page_id": result.get("id"),
        "url": result.get("url"),
        "name": data["name"],
        "tipo_report": data["tipo_report"],
        "stato": data["stato"],
        "migliore_opportunita": data["migliore_opportunita"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
