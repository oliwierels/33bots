#!/usr/bin/env bash
# Zgłasza podane URL-e (lub domyślny zestaw kluczowych stron) do IndexNow (Bing/Yandex/Seznam).
# Użycie: ./scripts/indexnow-submit.sh [url1 url2 ...]
# Uruchamiaj po każdym wdrożeniu zmian na produkcję.
KEY="9209ab0a2e014f2c808446b0b4b4271a"
HOST="33bots.pl"
URLS=("$@")
if [ ${#URLS[@]} -eq 0 ]; then
  URLS=(
    "https://33bots.pl/"
    "https://33bots.pl/wypozyczenie-robota.html"
    "https://33bots.pl/oferta-targi.html"
    "https://33bots.pl/oferta-konferencje.html"
    "https://33bots.pl/case-study-lexai.html"
    "https://33bots.pl/case-study-wallstreet.html"
    "https://33bots.pl/realizacje-wideo.html"
    "https://33bots.pl/blog.html"
  )
fi
LIST=$(printf '"%s",' "${URLS[@]}"); LIST="[${LIST%,}]"
curl -s -X POST "https://api.indexnow.org/indexnow" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "{\"host\":\"$HOST\",\"key\":\"$KEY\",\"keyLocation\":\"https://$HOST/$KEY.txt\",\"urlList\":$LIST}" \
  -w "\nHTTP %{http_code}\n"
