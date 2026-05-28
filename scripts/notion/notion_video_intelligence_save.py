#!/usr/bin/env python3
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import date


NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN")
DATABASE_ID = os.getenv("NOTION_VIDEO_INTELLIGENCE_DATABASE_ID")

if not NOTION_API_TOKEN:
    print("ERRORE: NOTION_API_TOKEN mancante", file=sys.stderr)
    sys.exit(1)

if not DATABASE_ID:
    print("ERRORE: NOTION_VIDEO_INTELLIGENCE_DATABASE_ID mancante", file=sys.stderr)
    sys.exit(1)


NOTION_VERSION = "2022-06-28"


def rich_text(value, limit=1900):
    value = "" if value is None else str(value)
    return [{"text": {"content": value[:limit]}}]


def title_text(value):
    value = value or "Video Intelligence"
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
        "name": data.get("name") or data.get("titolo") or data.get("title") or "Video Intelligence",
        "data": data.get("data") or str(date.today()),
        "tipo": data.get("tipo") or "Production Flow",
        "target": data.get("target") or "",
        "trend": data.get("trend") or "",
        "piattaforma": data.get("piattaforma") or data.get("platform") or ["TikTok", "Instagram Reels", "YouTube Shorts"],
        "tool": data.get("tool") or ["LTX Studio", "Easy-Peasy AI", "Manus", "Notion"],
        "fonte_video": data.get("fonte_video") or data.get("fonte") or "",
        "link_fonte_video": data.get("link_fonte_video") or data.get("link_fonte"),
        "copyright_risk": data.get("copyright_risk") or data.get("rischio_copyright") or "Da verificare",
        "priorita": data.get("priorita") or data.get("priorità") or "Media",
        "potenziale": str(data.get("potenziale") or "3"),
        "difficolta": str(data.get("difficolta") or data.get("difficoltà") or "3"),
        "stato_produzione": data.get("stato_produzione") or "Da produrre",
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
        "Target": {"rich_text": rich_text(data["target"])},
        "Trend": {"rich_text": rich_text(data["trend"])},
        "Piattaforma": {"multi_select": multi_select_value(data["piattaforma"])},
        "Tool": {"multi_select": multi_select_value(data["tool"])},
        "Fonte Video": {"rich_text": rich_text(data["fonte_video"])},
        "Copyright Risk": {"select": select_value(data["copyright_risk"])},
        "Priorità": {"select": select_value(data["priorita"])},
        "Potenziale": {"select": select_value(data["potenziale"])},
        "Difficoltà": {"select": select_value(data["difficolta"])},
        "Stato Produzione": {"select": select_value(data["stato_produzione"])},
        "Prossima Azione": {"rich_text": rich_text(data["prossima_azione"])},
    }

    if data.get("link_fonte_video"):
        props["Link Fonte Video"] = {"url": url_value(data["link_fonte_video"])}

    if data.get("link_output"):
        props["Link Output"] = {"url": url_value(data["link_output"])}

    return props


def build_children(data):
    children = [
        heading("Obiettivo video"),
        paragraph(data["details"] or "Scheda Video Intelligence."),
    ]

    required = {
        "Target": data.get("target") or "",
        "Fonti video verificate o da verificare": data.get("fonte_video") or "Fonti video da verificare.",
        "Query di ricerca video": "",
        "Analisi format": "",
        "Hook": "",
        "Script completo": "",
        "Storyboard scena per scena": "",
        "Shot list": "",
        "Prompt LTX Studio scena per scena": "",
        "Negative prompt scena per scena": "",
        "Prompt Magnific": "",
        "Prompt Freepik": "",
        "Prompt Easy-Peasy AI": "",
        "Task Manus": "",
        "Asset reference": "",
        "Diagramma Mermaid": "",
        "Caption e CTA": "",
        "Checklist produzione": "",
        "Nota copyright e originalità": "",
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
        "database": "Video Intelligence",
        "page_id": result.get("id"),
        "url": result.get("url"),
        "name": data["name"],
        "tipo": data["tipo"],
        "piattaforma": data["piattaforma"],
        "tool": data["tool"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
