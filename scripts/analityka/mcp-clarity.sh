#!/usr/bin/env bash
# Oficjalny serwer MCP Microsoft Clarity (pakiet @microsoft/clarity-mcp-server) — mapy cieplne,
# nagrania sesji i metryki zachowań z Data Export API. Token z CLARITY_API_TOKEN (ustawienia środowiska).
set -euo pipefail
if [ -z "${CLARITY_API_TOKEN:-}" ]; then
  echo "Clarity MCP: brak CLARITY_API_TOKEN w ustawieniach środowiska — serwer nie wystartuje." >&2
  exit 1
fi
export NPM_CONFIG_UPDATE_NOTIFIER=false NPM_CONFIG_FUND=false
exec npx --yes --loglevel=error @microsoft/clarity-mcp-server@2.0.1 --clarity_api_token="$CLARITY_API_TOKEN"
