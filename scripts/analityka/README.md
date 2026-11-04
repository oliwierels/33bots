# Analityka 33bots — narzędzia dla Claude

Ruch, konwersje, frazy z Google, mapy cieplne i archiwum danych. Wszystko tylko do odczytu.
Katalog `scripts/` nie trafia na serwer (pomija go `deploy.php`), a pliki `.md` też nie.

## Co tu jest

| Plik | Do czego |
|---|---|
| `../../.mcp.json` | ładuje w każdej sesji Claude Code dwa oficjalne serwery MCP: Google Analytics i Microsoft Clarity |
| `mcp-ga4.sh` | serwer MCP Google Analytics (pakiet `analytics-mcp` od Google, wersja przypięta, bez narzędzi zapisu) |
| `mcp-clarity.sh` | serwer MCP Microsoft Clarity (pakiet `@microsoft/clarity-mcp-server`, wersja przypięta) |
| `analityka.py` | raporty i archiwum: GA4, Search Console, Clarity, historia wdrożeń strony; zapis do CSV i BigQuery |

Serwery bez kluczy kończą pracę z jednym zdaniem w logu — nic się nie psuje.

## Klucze (ustawienia środowiska Claude Code, nigdy repozytorium)

| Zmienna | Skąd | Uwagi |
|---|---|---|
| `GOOGLE_SA_JSON` | Google Cloud → konto usługi → klucz JSON | cała treść pliku w jednej linii albo base64 |
| `GA4_PROPERTY_ID` | GA4 → Administracja → Szczegóły usługi | sam numer; bez niej bierze pierwszą widoczną usługę |
| `CLARITY_API_TOKEN` | Clarity → Ustawienia → Eksport danych | token jednego projektu |
| `BQ_DATASET` | opcjonalnie, np. `33bots-analityka:archiwum` | archiwum w BigQuery |

Konto usługi dostaje dostęp: GA4 (Wyświetlający), Search Console (Ograniczony, każda witryna),
BigQuery (Edytujący dane + Użytkownik zadań) — jeśli archiwum ma iść do BigQuery.
Sieć środowiska musi przepuszczać `www.clarity.ms` (Google API są przepuszczane).

## Polecenia

```bash
python3 scripts/analityka/analityka.py sprawdz                      # co działa, do czego jest dostęp
python3 scripts/analityka/analityka.py ga4 --od 2026-10-01 --wymiary landingPage --metryki sessions,keyEvents
python3 scripts/analityka/analityka.py gsc --od 2026-10-01 --wymiary query,page --limit 200
python3 scripts/analityka/analityka.py clarity --dni 3 --wymiary URL,Device
python3 scripts/analityka/analityka.py archiwum                     # pełne archiwum + BigQuery, jeśli ustawione
python3 scripts/analityka/analityka.py historia-zmian --csv zmiany.csv   # bez kluczy
```

## Archiwum: co i na jak długo

- **GA4** — dane zagregowane od dnia założenia usługi: ruch dzienny wg kanału, źródła, urządzenia i kraju,
  strony wejścia, odsłony stron, zdarzenia (w tym `cta_click`, `generate_lead`), kampanie.
  W GA4 warto ustawić przechowywanie danych na 14 miesięcy (Administracja → Przechowywanie danych),
  bo eksploracje widzą tylko tyle. Surowe zdarzenia na przyszłość daje darmowe połączenie GA4 z BigQuery.
- **Search Console** — Google trzyma 16 miesięcy. Polecenie `archiwum` zrzuca je w całości
  (dni, strony, frazy × kraj × urządzenie) dla 33bots.pl, .de, .at i .lt. Starsze dane przepadają,
  dlatego pierwszy zrzut robimy od razu, a potem regularnie (albo włączamy eksport zbiorczy do BigQuery).
- **Clarity** — API oddaje tylko 1–3 ostatnie dni i 10 zapytań dziennie na projekt, więc archiwum
  powstaje wyłącznie przez codzienny zrzut. Mapy cieplne i nagrania są w panelu Clarity.
- **Historia zmian** — daty wdrożeń i zmienione strony z gałęzi produkcyjnej, do nakładania na wykresy ruchu.

## Bezpieczeństwo

- Repozytorium i logi GitHub Actions są publiczne: dane analityczne nie trafiają ani tu, ani do Actions.
  `.gitignore` blokuje `*.csv.gz`, `scripts/analityka/dane/` i pliki kluczy.
- Klucz Google trafia do pliku tymczasowego z prawami tylko dla właściciela i jest usuwany po zakończeniu serwera.
- Serwer GA4 działa bez `--allow-write`: nie ma narzędzi zmieniających konfigurację GA4.
