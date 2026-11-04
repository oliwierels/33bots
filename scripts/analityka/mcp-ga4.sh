#!/usr/bin/env bash
# Oficjalny serwer MCP Google Analytics (Google, pakiet analytics-mcp) na koncie usługi.
# Klucz bierze ze zmiennej środowiska GOOGLE_SA_JSON (ustawienia środowiska Claude Code),
# zapisuje go do pliku tymczasowego dostępnego tylko dla tego użytkownika i usuwa przy wyjściu.
# Tylko odczyt: bez flagi --allow-write serwer nie ma narzędzi zmieniających GA4.
set -euo pipefail
if [ -z "${GOOGLE_SA_JSON:-}" ] && [ -z "${GOOGLE_APPLICATION_CREDENTIALS:-}" ]; then
  echo "Google Analytics MCP: brak GOOGLE_SA_JSON w ustawieniach środowiska — serwer nie wystartuje." >&2
  exit 1
fi
if [ -n "${GOOGLE_SA_JSON:-}" ]; then
  umask 077
  KLUCZ=$(mktemp "${TMPDIR:-/tmp}/ga-mcp-XXXXXX.json")
  trap 'rm -f "$KLUCZ"' EXIT
  case "$GOOGLE_SA_JSON" in
    \{*) printf '%s' "$GOOGLE_SA_JSON" > "$KLUCZ" ;;
    *)   printf '%s' "$GOOGLE_SA_JSON" | base64 -d > "$KLUCZ" ;;
  esac
  export GOOGLE_APPLICATION_CREDENTIALS="$KLUCZ"
fi
# Bez exec, żeby trap usunął klucz po zakończeniu serwera.
uvx --quiet analytics-mcp==1.0.0
