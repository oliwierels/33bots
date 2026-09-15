# Automatyczne wdrożenie 33bots.de

Ten sam mechanizm, co na `33bots.pl` i `33bots.lt`. Po skonfigurowaniu każda zmiana
zatwierdzona na gałęzi `claude/identical-pages-germany-rg6dzh` trafia na `33bots.de`
w kilkanaście sekund — bez ręcznego wgrywania plików przez FTP.

## Jak to działa

```
zmiana w repozytorium  →  GitHub sprawdza stronę  →  puka do serwera
                                                          ↓
                                   serwer sam pobiera paczkę z GitHuba po HTTPS
```

Kierunek jest odwrotny niż przy FTP — to serwer sięga po zmiany. Hosting blokuje
połączenia FTP z adresów serwerowni GitHuba, a pobieranie po HTTPS działa bez przeszkód
i hasło nigdzie nie wyjeżdża.

Pliki:

- `.github/workflows/wdrozenie.yml` — sprawdzenie strony i sygnał do serwera
- `narzedzia-serwer/deploy.php` — punkt wdrożeniowy, wgrywany na hosting raz

## Konfiguracja — jednorazowo

### Krok 1. Wpisz token do `deploy.php`

```bash
openssl rand -base64 32 | tr -d '/+=' | cut -c1-40
```

Wstaw wynik w `narzedzia-serwer/deploy.php` w stałej `TOKEN`. **Tej wersji z tokenem nie
zatwierdzaj w repozytorium** — plik z tokenem wgrywasz tylko na serwer.

### Krok 2. Wgraj `deploy.php` na serwer

Do katalogu, w którym leży `index.html` strony 33bots.de (zwykle
`domains/33bots.de/public_html`). Skrypt rozpakowuje stronę **do katalogu, w którym sam
leży**, więc to jego umiejscowienie decyduje, gdzie wyląduje strona.

### Krok 3. Sprawdź gotowość serwera

```
https://33bots.de/deploy.php?token=TWOJ_TOKEN&test=1
```

Zobaczysz wersję PHP, dostępność `ZipArchive` i cURL oraz możliwość zapisu do katalogu.
Bez tokenu skrypt zwraca `Brak dostępu` i nic nie robi.

### Krok 4. Dodaj sekrety na GitHubie

`github.com/oliwierels/33bots` → **Settings** → **Secrets and variables** → **Actions**

| Nazwa | Wartość |
|---|---|
| `DEPLOY_URL_DE` | `https://33bots.de/deploy.php` |
| `DEPLOY_TOKEN_DE` | token wpisany w `deploy.php` |

Nazwy mają przyrostek `_DE`, bo to repozytorium obsługuje dwie witryny — sekrety bez
przyrostka należą do 33bots.pl.

### Krok 5. Uruchom

Zatwierdź dowolną zmianę na gałęzi produkcyjnej — push uruchamia wdrożenie sam. Bez
nowego commita: `Actions` → ostatnie uruchomienie → **Re-run all jobs**.

Przed pierwszym uruchomieniem warto zrobić kopię katalogu strony
(Manager plików → zaznacz wszystko → Kompresuj).

## Bramka bezpieczeństwa

Zanim GitHub poprosi serwer o cokolwiek, sprawdza wszystkie 192 strony:

- domknięte znaczniki HTML i poprawny JSON w danych strukturalnych,
- adres kanoniczny w domenie `33bots.de`, obecny i nigdzie nie powtórzony,
- hreflang: obca wersja językowa nie może wskazywać na 33bots.de,
- **reguły serwera (`.htaccess`, `_redirects`) nie mogą przekierowywać na obcą domenę** —
  do września 2026 leżała tu kopia polskiego `.htaccess`, która każde wejście po HTTP
  przenosiła na `https://33bots.pl`. Dla Google 33bots.de było wtedy przekierowaniem na
  cudzy serwis i nie miało szans trafić do indeksu,
- odwołania do plików, których nie ma w repozytorium,
- `sitemap.xml` jako poprawny XML, z adresami w domenie 33bots.de i realnymi plikami,
- `main.js` nie zgubił adresu formularza kontaktowego.

Gdy którykolwiek warunek nie jest spełniony, wdrożenie się zatrzymuje, a strona zostaje
w poprzedniej, działającej wersji.

## Co nie trafia na serwer

Katalog `build/` (generatory strony), `.github/`, `narzedzia-serwer/`, pliki `.md`,
`.gitignore`, `_redirects` (konfiguracja Netlify — Apache czyta `.htaccess`) i sam
`deploy.php`. Wysyłane są za to `og/`, `fonts/` i zdjęcia — tych plików nie ma na serwerze
z żadnego innego źródła.

## Gdy coś pójdzie nie tak

Log wdrożenia tłumaczy kod odpowiedzi serwera na przyczynę:

| Objaw | Przyczyna |
|---|---|
| HTTP 404 | Brak `deploy.php` pod adresem z `DEPLOY_URL_DE` |
| HTTP 403 | Token w pliku różni się od sekretu `DEPLOY_TOKEN_DE` |
| HTTP 500 | Placeholder zamiast tokenu albo brak `ZipArchive` na hostingu |
| HTTP 502 | Hosting nie dosięgnął GitHuba |
| Zatrzymanie na bramce | Błąd w którejś stronie; log podaje który. Na serwer nic nie poszło |

## Wycofanie zmiany

`git revert` i zatwierdzenie — wdrożenie uruchomi się samo i przywróci poprzedni stan.
