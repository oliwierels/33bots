# Automatyczne wdrożenie na cyber_Folks

Po skonfigurowaniu każda zmiana zatwierdzona na gałęzi `claude/33bots-website-T0REs`
trafia na `33bots.pl` w kilkanaście sekund.

## Jak to działa

```
zmiana w repozytorium  →  GitHub sprawdza stronę  →  puka do serwera
                                                          ↓
                                   serwer sam pobiera paczkę z GitHuba po HTTPS
```

**Kierunek jest odwrotny niż przy FTP — to serwer sięga po zmiany.** Wybraliśmy
tę drogę, bo hosting blokuje połączenia FTP z adresów serwerowni GitHuba
(połączenie po prostu wygasa, co potwierdziły testy). Pobieranie po HTTPS
z serwera na zewnątrz działa bez przeszkód i jest przy okazji bezpieczniejsze:
hasło FTP nie opuszcza hostingu.

## Konfiguracja — jednorazowo, ok. 10 minut

### Krok 1. Wgraj punkt wdrożeniowy na serwer

Plik `deploy.php` (wysłany osobno, z wpisanym już tokenem) wgraj przez
Managera plików do **`domains/33bots.pl/public_html`**.

### Krok 2. Sprawdź, czy serwer jest gotowy

Otwórz w przeglądarce, podstawiając swój token:

```
https://33bots.pl/deploy.php?token=TWOJ_TOKEN&test=1
```

Powinieneś zobaczyć listę potwierdzeń — wersję PHP, dostępność ZipArchive
i cURL oraz możliwość zapisu do katalogu. Gdyby czegoś brakowało, napisz —
dobierzemy inne rozwiązanie.

Bez tokenu albo z błędnym tokenem skrypt zwraca `Brak dostępu` i nic nie robi.

### Krok 3. Dodaj dwa sekrety na GitHubie

`github.com/oliwierels/33bots` → **Settings** → **Secrets and variables**
→ **Actions** → **New repository secret**

| Nazwa | Wartość |
|---|---|
| `DEPLOY_URL` | `https://33bots.pl/deploy.php` |
| `DEPLOY_TOKEN` | token wpisany w `deploy.php` |

Wcześniejsze sekrety FTP (`FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`, `FTP_DIR`)
nie są już potrzebne — możesz je usunąć.

### Krok 4. Uruchom

**Actions** → **Wdrożenie na cyber_Folks** → **Run workflow**.

Przed pierwszym uruchomieniem warto zrobić kopię `public_html`
(Manager plików → zaznacz wszystko → Kompresuj).

---

## Praca na co dzień

Po zmianie w `index.html` uruchom przed zatwierdzeniem:

```bash
./buduj.sh
```

Skrypt kompiluje arkusz Tailwinda i oznacza go w `index.html` sumą kontrolną
jego treści. Numer wersji zmienia się dokładnie wtedy, gdy zmienia się wygląd —
dzięki temu przeglądarka nigdy nie poda starego arkusza z pamięci podręcznej.
To właśnie ten mechanizm zapobiega sytuacji, w której nowa strona ładuje się
ze starymi stylami i rozjeżdża.

Zatwierdzenie zmian na gałęzi produkcyjnej uruchamia wdrożenie samo.

## Bramka bezpieczeństwa

Zanim GitHub poprosi serwer o cokolwiek, sprawdza `index.html`:

- czy znaczniki HTML są domknięte,
- czy wszystkie bloki danych strukturalnych to poprawny JSON,
- czy nie zniknął Google Tag Manager, arkusz stylów ani formularz kontaktowy,
- czy arkusz oznaczony w `index.html` odpowiada temu w repozytorium
  (wyłapuje pominięte `./buduj.sh`).

**Gdy którykolwiek warunek nie jest spełniony, wdrożenie się zatrzymuje**
i strona zostaje w poprzedniej, działającej wersji.

## Co nie trafia na serwer

Skrypty `.py`, konfiguracja Tailwinda, `buduj.sh`, katalog `og/`, surowe
zdjęcia z aparatu, pliki `.md`, katalog `.git` i sam `deploy.php`.
Listę wykluczeń trzyma `.deployignore` oraz stałe na górze `deploy.php`.

## Czego wdrożenie nie kasuje

Pliki wgrane ręcznie, których nie ma w repozytorium, zostają nietknięte.
Skrypt nadpisuje tylko to, co przychodzi z GitHuba, i pomija pliki o identycznej
treści — dzięki temu typowe wdrożenie dotyka kilku plików, a nie całej strony.

## Gdy coś pójdzie nie tak

Otwórz nieudane uruchomienie w zakładce **Actions** — odpowiedź serwera jest
wypisana w całości.

| Objaw | Przyczyna |
|---|---|
| `Brak dostępu` | Token w `deploy.php` różni się od sekretu `DEPLOY_TOKEN` |
| `Skrypt nie został skonfigurowany` | W `deploy.php` został placeholder zamiast tokenu |
| `Brak rozszerzenia ZipArchive` | Hosting nie ma tego rozszerzenia — napisz, zmienimy metodę |
| `Pobieranie nie powiodło się` | Serwer nie dosięgnął GitHuba — sprawdź, czy hosting nie blokuje ruchu wychodzącego |
| Zatrzymanie na bramce | Błąd w `index.html`; log podaje który. Na serwer nic nie poszło |

## Wycofanie zmiany

Cofnij commit (`git revert`) i zatwierdź — wdrożenie uruchomi się samo
i przywróci poprzedni stan strony.

## Bezpieczeństwo

`deploy.php` to punkt, który potrafi nadpisać pliki strony, więc:

- token ma 43 znaki i jest losowy — nie da się go zgadnąć,
- bez poprawnego tokenu skrypt kończy działanie na pierwszej instrukcji,
- pobiera wyłącznie z jednego, wpisanego na stałe repozytorium i gałęzi,
- gdybyś kiedyś zrezygnował z automatu, po prostu usuń plik z serwera.

Gdy zmienisz token, zmień go w obu miejscach naraz: w `deploy.php` na serwerze
i w sekrecie `DEPLOY_TOKEN` na GitHubie.
