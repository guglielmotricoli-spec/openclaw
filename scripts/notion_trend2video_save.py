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

def rich_text(value: str):
    value = value or ""
    return [{"text": {"content": value[:1900]}}]

def title_text(value: str):
    value = value or "Trend2Video AI"
    return [{"text": {"content": value[:200]}}]

payload_input = sys.stdin.read().strip()

if payload_input:
    data = json.loads(payload_input)
else:
    data = {}

name = data.get("name") or data.get("Name") or "Trend2Video AI - nuova idea"
trend = data.get("trend") or data.get("Trend") or "Trend da completare"
status = data.get("stato") or data.get("Stato") or "Idea"
note = data.get("note") or data.get("Note") or "Scheda creata da OpenClaw."
day = data.get("data") or data.get("Data") or date.today().isoformat()

payload = {
    "parent": {"database_id": DATABASE_ID},
    "properties": {
        "Name": {"title": title_text(name)},
        "Data": {"date": {"start": day}},
        "Trend": {"rich_text": rich_text(trend)},
        "Stato": {"select": {"name": status}},
        "Note": {"rich_text": rich_text(note)},
    },
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
}, ensure_ascii=False, indent=2))
