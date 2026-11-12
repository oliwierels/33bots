#!/bin/bash
# Kontrola na żywo API i serwera MCP 33bots.pl. Żadne poprawne zapytanie nie jest wysyłane:
# do /api/zapytania idą wyłącznie dane, które odpadają na walidacji (przed przekazaniem dalej).
B=https://33bots.pl
echo "################ strona po zmianie .htaccess"
for p in / wypozyczenie-robota.html blog-robot-na-event-miedzynarodowy.html robots.txt llms.txt sitemap.xml; do echo "/$p → $(curl -s -o /dev/null -w '%{http_code} %{size_download}B' --max-time 30 "$B/${p#/}")"; done
echo "################ źródła i testy"
for p in tresci/artykuly/blog-robot-na-event-miedzynarodowy.html tresci/zagranica/podstrony/de/roboter-mieten-berlin.html qa/package.json qa/api/router.php tresci/; do echo "/$p → $(curl -s -o /dev/null -w '%{http_code}' --max-time 30 "$B/$p")"; done
echo "################ API"
echo "GET /api/ → $(curl -s -o /tmp/a.json -D /tmp/h.txt -w '%{http_code}' --max-time 30 "$B/api/")"; grep -iE '^(content-type|x-robots-tag|access-control-allow-origin|x-powered-by|cache-control)' /tmp/h.txt | tr -d '\r' | tr '\n' ' '; echo; head -c 420 /tmp/a.json; echo
echo "GET /api (bez ukośnika) → $(curl -s -o /dev/null -w '%{http_code} %{redirect_url}' --max-time 30 "$B/api")"
echo "GET /api/wycena?dni=2 → $(curl -s --max-time 30 "$B/api/wycena?dni=2" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["kwota_od"], d["waluta"], d["podatek"], "|", d["opis"])')"
echo "GET /api/wycena?rynek=de&dni=3 → $(curl -s --max-time 30 "$B/api/wycena?rynek=de&dni=3" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["kwota_od"], d["waluta"])')"
echo "GET /api/wycena?rynek=xx → $(curl -s -o /dev/null -w '%{http_code}' --max-time 30 "$B/api/wycena?rynek=xx")"
echo "GET /api/openapi.json → $(curl -s -o /tmp/o.json -w '%{http_code} %{content_type}' --max-time 30 "$B/api/openapi.json") $(python3 -c 'import json; d=json.load(open("/tmp/o.json")); print(d["openapi"], list(d["paths"]))')"
echo "GET /api/nic → $(curl -s -w ' [%{http_code}]' --max-time 30 "$B/api/nic" | tr -d '\n' | cut -c1-160)"
echo "GET /api/zapytania → $(curl -s -o /dev/null -w '%{http_code}' --max-time 30 "$B/api/zapytania")"
echo "POST /api/zapytania (bez zgody, zły e-mail — odpada na walidacji) → $(curl -s -w ' [%{http_code}]' --max-time 30 -H 'Content-Type: application/json' -d '{"imie":"A","email":"nie-mail"}' "$B/api/zapytania" | tr -d '\n' | cut -c1-420)"
echo "POST /api/zapytania (zły JSON) → $(curl -s -o /dev/null -w '%{http_code}' --max-time 30 -H 'Content-Type: application/json' -d '{zle' "$B/api/zapytania")"
echo "################ MCP"
rpc() { curl -s --max-time 30 -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' -d "$1" "$B/mcp"; }
echo "initialize → $(rpc '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"kontrola","version":"1"}}}' | python3 -c 'import json,sys; d=json.load(sys.stdin)["result"]; print(d["protocolVersion"], d["serverInfo"], list(d["capabilities"]))')"
echo "notifications/initialized → $(curl -s -o /dev/null -w '%{http_code}' --max-time 30 -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","method":"notifications/initialized"}' "$B/mcp")"
echo "tools/list → $(rpc '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' | python3 -c 'import json,sys; print([t["name"] for t in json.load(sys.stdin)["result"]["tools"]])')"
echo "tools/call get_quote → $(rpc '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_quote","arguments":{"rynek":"at","dni":2}}}' | python3 -c 'import json,sys; d=json.load(sys.stdin)["result"]; print(d["isError"], d["content"][0]["text"][:200])')"
echo "tools/call request_quote bez zgody (nic nie wysyła) → $(rpc '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"request_quote","arguments":{"imie":"A","email":"x"}}}' | python3 -c 'import json,sys; d=json.load(sys.stdin)["result"]; print(d["isError"], list(d["structuredContent"]["pola"]))')"
echo "GET /mcp → $(curl -s -o /dev/null -w '%{http_code}' --max-time 30 "$B/mcp")  OPTIONS /mcp → $(curl -s -o /dev/null -w '%{http_code}' -X OPTIONS --max-time 30 "$B/mcp")"
echo "################ .de llms.txt"
echo "sekcja MCP: $(curl -s https://33bots.de/llms.txt | grep -c 'MCP-Server')  .pl llms: $(curl -s $B/llms.txt | grep -c 'serwer MCP')"
