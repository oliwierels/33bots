# Automatyczny deploy na hosting cyber-folks

Każdy push na gałąź domyślną automatycznie wysyła stronę na `s126.cyber-folks.pl`.
Nie trzeba niczego podmieniać ręcznie przez FTP.

Workflow: [`.github/workflows/deploy.yml`](workflows/deploy.yml)

## Konfiguracja jednorazowa

**Sekrety** — `Settings` → `Secrets and variables` → `Actions` → zakładka `Secrets`:

| Nazwa      | Wartość                                    |
| ---------- | ------------------------------------------ |
| `FTP_USER` | login konta FTP z panelu cyber-folks       |
| `FTP_PASS` | hasło tego konta                           |

Konto FTP zakłada się w [panelu cyber-folks](https://s126.cyber-folks.pl:2223/CMD_FTP?domain=33bots.pl).

**Zmienne** (opcjonalne) — ta sama strona, zakładka `Variables`. Wszystkie mają
sensowne wartości domyślne, ustawia się je tylko gdy coś nie działa:

| Nazwa             | Domyślnie                          | Kiedy zmienić                                                                 |
| ----------------- | ---------------------------------- | ----------------------------------------------------------------------------- |
| `FTP_SERVER_DIR`  | `/domains/33bots.pl/public_html/`  | Gdy konto FTP loguje się od razu w `public_html` — wtedy ustaw `./`            |
| `FTP_PROTOCOL`    | `ftps`                             | Gdy serwer odrzuca szyfrowane połączenie — wtedy `ftp`                         |
| `FTP_HOST`        | `s126.cyber-folks.pl`              | Po przeniesieniu na inny serwer                                               |

## Uruchomienie ręczne i próba na sucho

`Actions` → `Deploy na hosting (FTP)` → `Run workflow`. Zaznaczenie **dry run**
wypisuje listę plików do wysłania, ale niczego nie wysyła — przydatne przy
pierwszym uruchomieniu i po zmianie `FTP_SERVER_DIR`.

## Co NIE trafia na serwer

Wysyłana jest tylko strona. Pomijane są:

- surowe zdjęcia z aparatu (`IMG_*.HEIC/DNG/JPG/PNG`) — ok. 78 MB, nieużywane przez stronę
- skrypty generujące (`*.py`, `scripts/`)
- pliki źródłowe Tailwinda (`tailwind.config.js`, `tw-input.css`) — na serwer idzie
  gotowy `assets-redesign.css`
- dokumentacja (`*.md`) i pliki gita (`.git*`, `.github/`)

Lista jest w kluczu `exclude` w `deploy.yml`.

## Jak to działa

Akcja trzyma na serwerze plik `.ftp-deploy-sync-state.json` ze spisem wysłanych
plików. Przy kolejnych deployach wysyła **tylko to, co się zmieniło**, więc
publikacja poprawki w jednym HTML-u trwa kilkanaście sekund. Dostęp do tego pliku
z zewnątrz jest zablokowany regułą w `.htaccess`.

Przy pierwszym uruchomieniu tego pliku jeszcze nie ma, więc wysyłana jest całość.
Pliki leżące już na serwerze, a nieobecne w repozytorium, **nie są kasowane** —
jeśli trzeba je usunąć, robi się to ręcznie przez FTP.
