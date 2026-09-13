#!/usr/bin/env bash
# Meldet URLs dieser Website an IndexNow (Bing/Yandex/Seznam).
# Aufruf: ./build/scripts/indexnow-submit.sh [url1 url2 ...]
# Nach jedem Deployment ausführen.
#
# Der Key gilt nur für diese Domain und liegt als <KEY>.txt im Wurzelverzeichnis.
# Beides muss zusammen deployt werden, sonst weist IndexNow die Meldung ab.
KEY="18194c63f5aaa95b830d36b384ea91c0"
HOST="33bots.at"

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
