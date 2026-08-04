#!/usr/bin/env bash
# Meldet URLs dieser Website an IndexNow (Bing/Yandex/Seznam).
# Aufruf: ./build/scripts/indexnow-submit.sh [url1 url2 ...]
# Nach jedem Deployment ausführen.
#
# WICHTIG: Der IndexNow-Key gilt immer nur für eine Domain. Der Key der
# polnischen Seite ist hier bewusst NICHT übernommen. Vor der ersten Nutzung:
#   1. Neuen Key erzeugen (32 Hex-Zeichen), z. B.:  openssl rand -hex 16
#   2. Datei <KEY>.txt mit dem Key als Inhalt ins Wurzelverzeichnis legen
#   3. KEY unten eintragen
KEY="BITTE_NEUEN_KEY_EINTRAGEN"
HOST="33bots.de"

if [ "$KEY" = "BITTE_NEUEN_KEY_EINTRAGEN" ]; then
  echo "Fehler: Es ist noch kein IndexNow-Key für ${HOST} hinterlegt." >&2
  echo "Key erzeugen mit: openssl rand -hex 16" >&2
  exit 1
fi

URLS=("$@")
if [ ${#URLS[@]} -eq 0 ]; then
  URLS=(
    "https://${HOST}/"
    "https://${HOST}/humanoiden-roboter-mieten.html"
    "https://${HOST}/angebot-messen.html"
    "https://${HOST}/angebot-konferenzen-galas.html"
    "https://${HOST}/case-study-lexai.html"
    "https://${HOST}/case-study-wallstreet.html"
    "https://${HOST}/referenzen-videos.html"
    "https://${HOST}/blog.html"
  )
fi

LIST=$(printf '"%s",' "${URLS[@]}"); LIST="[${LIST%,}]"
curl -sS -X POST "https://api.indexnow.org/indexnow" \
  -H "Content-Type: application/json" \
  -d "{\"host\":\"${HOST}\",\"key\":\"${KEY}\",\"keyLocation\":\"https://${HOST}/${KEY}.txt\",\"urlList\":${LIST}}" \
  -w "\nHTTP %{http_code}\n"
