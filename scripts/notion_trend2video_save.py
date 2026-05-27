#!/usr/bin/env python3
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import date

NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN")
DATABASE_ID = os.getenv("NOTION_TREND2VIDEO_DATABASE_ID")

if not NOTION_API_TOKEN:
    print("ERRORE: NOTION_API_TOKEN mancante", file=sys.stderr)
    sys.exit(1)

if not DATABASE_ID:
    print("ERRORE: NOTION_TREND2VIDEO_DATABASE_ID mancante", file=sys.stderr)
    sys.exit(1)

def rich_text(value: str, limit: int = 1900):
    value = "" if value is None else str(value)
    return [{"text": {"content": value[:limit]}}]

def title_text(value: str):
    value = value or "Trend2Video AI"
    return [{"text": {"content": str(value)[:200]}}]

def select_value(value: str):
    if not value:
        return None
    return {"name": str(value)}

def multi_select_value(values):
    if not values:
        return []

    if isinstance(values, str):
        raw_items = [item.strip() for item in values.replace(";", ",").split(",")]
    elif isinstance(values, list):
        raw_items = [str(item).strip() for item in values]
    else:
        raw_items = [str(values).strip()]

    return [{"name": item} for item in raw_items if item]

def url_value(value):
    if not value:
        return None
    return str(value)

def date_value(value):
    if not value:
        return None
    return {"start": str(value)}

def normalize_label(label: str):
    label = str(label or "").strip().lower()
    label = label.replace("à", "a").replace("è", "e").replace("é", "e").replace("ì", "i").replace("ò", "o").replace("ù", "u")
    return label

def parse_note_fields(note_text: str):
    """
    Estrae campi estesi quando il modello li mette per errore dentro Note,
    per esempio:
    Tipo: Video Reels (5 scene)
    Target: ristoranti locali
    Piattaforma: Instagram Reels, TikTok, YouTube Shorts
    Tool: LTX Studio, Magnific, Freepik, Easy-Peasy AI
    """
    result = {}
    if not note_text:
        return result

    aliases = {
        "tipo": "tipo",
        "target": "target",
        "piattaforma": "piattaforma",
        "piattaforme": "piattaforma",
        "tool": "tool",
        "tools": "tool",
        "priorita": "priorita",
        "priorità": "priorita",
        "potenziale": "potenziale",
        "difficolta": "difficolta",
        "difficoltà": "difficolta",
        "fonte": "fonte",
        "stato produzione": "stato_produzione",
        "stato_produzione": "stato_produzione",
        "data pubblicazione": "data_pubblicazione",
        "data_pubblicazione": "data_pubblicazione",
        "link output": "link_output",
        "link_output": "link_output",
    }

    for raw_line in str(note_text).splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue

        label, value = line.split(":", 1)
        key = aliases.get(normalize_label(label))
        value = value.strip()

        if not key or not value:
            continue

        if key in {"piattaforma", "tool"}:
            items = [item.strip() for item in value.replace(";", ",").split(",") if item.strip()]
            result[key] = items
        else:
            result[key] = value

    return result

def clean_note_text(note_text: str):
    """
    Rimuove dal campo Note le righe tecniche che sono state estratte
    nelle proprietà Notion, lasciando solo la sintesi leggibile.
    """
    if not note_text:
        return note_text

    technical_labels = {
        "tipo", "target", "piattaforma", "piattaforme", "tool", "tools",
        "priorita", "priorità", "potenziale", "difficolta", "difficoltà",
        "fonte", "stato produzione", "stato_produzione",
        "data pubblicazione", "data_pubblicazione",
        "link output", "link_output",
    }

    kept = []
    for raw_line in str(note_text).splitlines():
        line = raw_line.strip()
        if ":" in line:
            label = normalize_label(line.split(":", 1)[0])
            if label in {normalize_label(x) for x in technical_labels}:
                continue
        kept.append(raw_line)

    cleaned = "\n".join(x for x in kept if str(x).strip()).strip()
    return cleaned or note_text

def paragraph(text: str):
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": rich_text(text, 1900)
        }
    }

def heading(text: str, level: int = 2):
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

def chunks(text: str, size: int = 1800):
    text = "" if text is None else str(text)
    return [text[i:i + size] for i in range(0, len(text), size)] or [""]

payload_input = sys.stdin.read().strip()

if not payload_input:
    print("ERRORE: payload JSON mancante. Non creo pagine Notion vuote.", file=sys.stderr)
    sys.exit(1)

try:
    data = json.loads(payload_input)
except json.JSONDecodeError as e:
    print(f"ERRORE: payload JSON non valido: {e}", file=sys.stderr)
    sys.exit(1)

if not isinstance(data, dict):
    print("ERRORE: il payload JSON deve essere un oggetto.", file=sys.stderr)
    sys.exit(1)

required_signal = any([
    data.get("name"),
    data.get("Name"),
    data.get("trend"),
    data.get("Trend"),
    data.get("details"),
    data.get("sections"),
    data.get("sezioni"),
])

if not required_signal:
    print("ERRORE: payload troppo vuoto. Servono almeno name/trend/details/sections.", file=sys.stderr)
    sys.exit(1)

name = data.get("name") or data.get("Name") or "Trend2Video AI - nuova idea"
trend = data.get("trend") or data.get("Trend") or "Trend da completare"
status = data.get("stato") or data.get("Stato") or "Idea"
note_raw = data.get("note") or data.get("Note") or "Scheda creata da OpenClaw."
note_fields = parse_note_fields(note_raw)
note = clean_note_text(note_raw)
day = data.get("data") or data.get("Data") or date.today().isoformat()

tipo = data.get("tipo") or data.get("Tipo") or note_fields.get("tipo")
target = data.get("target") or data.get("Target") or note_fields.get("target")
piattaforma = data.get("piattaforma") or data.get("Piattaforma") or note_fields.get("piattaforma")
tool = data.get("tool") or data.get("Tool") or note_fields.get("tool")
priorita = data.get("priorita") or data.get("Priorità") or data.get("Priorita") or note_fields.get("priorita")
potenziale = data.get("potenziale") or data.get("Potenziale") or note_fields.get("potenziale")
difficolta = data.get("difficolta") or data.get("Difficoltà") or data.get("Difficolta") or note_fields.get("difficolta")
fonte = data.get("fonte") or data.get("Fonte") or note_fields.get("fonte")
stato_produzione = data.get("stato_produzione") or data.get("Stato Produzione") or data.get("statoProduzione") or note_fields.get("stato_produzione")
data_pubblicazione = data.get("data_pubblicazione") or data.get("Data Pubblicazione") or data.get("dataPubblicazione") or note_fields.get("data_pubblicazione")
link_output = data.get("link_output") or data.get("Link Output") or data.get("linkOutput") or note_fields.get("link_output")

details = data.get("details") or data.get("dettagli") or data.get("content") or ""
sections = data.get("sections") or data.get("sezioni") or {}

if not details and note_raw and len(str(note_raw)) > 180:
    details = str(note_raw)

children = [
    heading("Trend2Video AI - Scheda operativa", 2),
    paragraph(f"Trend: {trend}"),
    paragraph(f"Stato: {status}"),
    paragraph(f"Tipo: {tipo or 'Non specificato'}"),
    paragraph(f"Target: {target or 'Non specificato'}"),
    paragraph(f"Piattaforme: {piattaforma or 'Non specificate'}"),
    paragraph(f"Tool: {tool or 'Non specificati'}"),
    paragraph(f"Priorità: {priorita or 'Non specificata'}"),
    paragraph(f"Potenziale: {potenziale or 'Non specificato'}"),
    paragraph(f"Difficoltà: {difficolta or 'Non specificata'}"),
    paragraph(f"Fonte: {fonte or 'Non specificata'}"),
    paragraph(f"Stato produzione: {stato_produzione or 'Non specificato'}"),
    paragraph(f"Data pubblicazione: {data_pubblicazione or 'Non programmata'}"),
    paragraph(f"Link output: {link_output or 'Non disponibile'}"),
    paragraph(f"Note sintetiche: {note}"),
    divider(),
]

if details:
    children.append(heading("Dettaglio completo", 2))
    for part in chunks(details):
        children.append(paragraph(part))
    children.append(divider())

if isinstance(sections, dict) and sections:
    for section_title, section_content in sections.items():
        children.append(heading(str(section_title), 2))
        if isinstance(section_content, list):
            for item in section_content:
                children.append(paragraph(f"- {item}"))
        elif isinstance(section_content, dict):
            for key, value in section_content.items():
                children.append(paragraph(f"{key}: {value}"))
        else:
            for part in chunks(str(section_content)):
                children.append(paragraph(part))
        children.append(divider())

children.append(heading("Regola copyright e remix", 2))
children.append(paragraph(
    "Usare video, immagini e contenuti virali solo come riferimento creativo. "
    "Non copiare, non fare reupload, non rimuovere watermark, non usare asset protetti senza autorizzazione. "
    "Creare sempre script, visual, voce, montaggio e messaggio originali."
))

properties = {
    "Name": {"title": title_text(name)},
    "Data": {"date": {"start": day}},
    "Trend": {"rich_text": rich_text(trend)},
    "Stato": {"select": {"name": status}},
    "Note": {"rich_text": rich_text(note)},
}

optional_properties = {
    "Tipo": ("select", tipo),
    "Target": ("rich_text", target),
    "Piattaforma": ("multi_select", piattaforma),
    "Tool": ("multi_select", tool),
    "Priorità": ("select", priorita),
    "Potenziale": ("select", potenziale),
    "Difficoltà": ("select", difficolta),
    "Fonte": ("rich_text", fonte),
    "Stato Produzione": ("select", stato_produzione),
    "Data Pubblicazione": ("date", data_pubblicazione),
    "Link Output": ("url", link_output),
}

for prop_name, (prop_type, value) in optional_properties.items():
    if value in (None, "", []):
        continue

    if prop_type == "select":
        properties[prop_name] = {"select": select_value(value)}
    elif prop_type == "multi_select":
        properties[prop_name] = {"multi_select": multi_select_value(value)}
    elif prop_type == "rich_text":
        properties[prop_name] = {"rich_text": rich_text(value)}
    elif prop_type == "date":
        properties[prop_name] = {"date": date_value(value)}
    elif prop_type == "url":
        properties[prop_name] = {"url": url_value(value)}

payload = {
    "parent": {"database_id": DATABASE_ID},
    "properties": properties,
    "children": children[:90],
}

req = urllib.request.Request(
    "https://api.notion.com/v1/pages",
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {NOTION_API_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    },
    method="POST",
)

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    body = e.read().decode("utf-8", errors="replace")
    print("ERRORE NOTION:", body, file=sys.stderr)
    sys.exit(1)

print(json.dumps({
    "ok": True,
    "page_id": result.get("id"),
    "url": result.get("url"),
    "name": name,
    "tipo": tipo,
    "target": target,
    "piattaforma": piattaforma,
    "tool": tool,
}, ensure_ascii=False, indent=2))
