#!/usr/bin/env bash
set -e

BASE_WORKSPACE="/home/openclaw/.openclaw/workspace"

echo "Creo le cartelle workspace..."
mkdir -p "$BASE_WORKSPACE/caporedattore"
mkdir -p "$BASE_WORKSPACE/news-immobiliari"
mkdir -p "$BASE_WORKSPACE/seo-blog"
mkdir -p "$BASE_WORKSPACE/repurposer"
mkdir -p "$BASE_WORKSPACE/researcher"

echo "Copio i prompt versionati..."
cp setup/editorial-agents/caporedattore.AGENTS.md "$BASE_WORKSPACE/caporedattore/AGENTS.md"
cp setup/editorial-agents/news-immobiliari.AGENTS.md "$BASE_WORKSPACE/news-immobiliari/AGENTS.md"
cp setup/editorial-agents/seo-blog.AGENTS.md "$BASE_WORKSPACE/seo-blog/AGENTS.md"
cp setup/editorial-agents/repurposer.AGENTS.md "$BASE_WORKSPACE/repurposer/AGENTS.md"
cp setup/editorial-agents/researcher.AGENTS.md "$BASE_WORKSPACE/researcher/AGENTS.md"

echo "Creo gli agenti OpenClaw..."
oc agents add caporedattore --workspace /home/node/.openclaw/workspace/caporedattore --non-interactive || true
oc agents add news-immobiliari --workspace /home/node/.openclaw/workspace/news-immobiliari --non-interactive || true
oc agents add seo-blog --workspace /home/node/.openclaw/workspace/seo-blog --non-interactive || true
oc agents add repurposer --workspace /home/node/.openclaw/workspace/repurposer --non-interactive || true
oc agents add researcher --workspace /home/node/.openclaw/workspace/researcher --non-interactive || true

echo "Fatto."
