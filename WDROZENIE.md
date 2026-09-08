# Automatyczne wdrożenie na cyber_Folks

Po skonfigurowaniu każda zmiana zatwierdzona na gałęzi produkcyjnej
(`claude/33bots-website-T0REs`) trafia na `33bots.pl` w ciągu ok. minuty.
Bez wgrywania plików ręcznie, bez ZIP-ów.

---

## Konfiguracja — jednorazowo, ok. 10 minut

### Krok 1. Załóż konto FTP tylko do wdrożeń

W panelu cyber_Folks: **Konta FTP → Utwórz konto FTP**.

Zalecam osobne konto, a nie główne konto hostingu — jeśli hasło kiedykolwiek
wycieknie, dostęp ograniczy się do katalogu strony, a nie całego serwera.

Ustaw katalog domowy na `public_html` domeny 33bots.pl. Zapisz login i hasło,
bo za chwilę będą potrzebne.

### Krok 2. Sprawdź adres serwera FTP

W panelu, w sekcji konta FTP, znajdziesz nazwę hosta — zwykle `ftp.33bots.pl`
albo adres serwera typu `ttxywfrxaf.cfolks.pl`. Zapisz go.

### Krok 3. Dodaj dane dostępowe do GitHuba

Wejdź na `github.com/oliwierels/33bots` → **Settings** → **Secrets and variables**
→ **Actions** → przycisk **New repository secret**.

Dodaj cztery sekrety (nazwy muszą się zgadzać co do znaku):

| Nazwa | Wartość |
|---|---|
| `FTP_SERVER` | `ttxywfrxaf.cyber-folks.pl` — patrz uwaga niżej |
| `FTP_USERNAME` | login konta FTP z kroku 1 |
| `FTP_PASSWORD` | hasło konta FTP z kroku 1 |
| `FTP_DIR` | patrz niżej — zależy od ścieżki konta |

**Uwaga o adresie serwera.** Certyfikat TLS serwera wystawiony jest na
`*.cyber-folks.pl` — z myślnikiem. Panel pokazuje serwer jako
`ttxywfrxaf.cfolks.pl`, bez myślnika, i pod tym adresem szyfrowane
połączenie zostanie odrzucone (niezgodność nazwy w certyfikacie).
Dlatego w sekrecie ma być `ttxywfrxaf.cyber-folks.pl`.

Gdyby ta nazwa nie działała, można zejść do nieszyfrowanego FTP: dodaj
zmienną repozytorium (zakładka **Variables**, nie Secrets) o nazwie
`FTP_PROTOCOL` i wartości `ftp`. To ostateczność — hasło leci wtedy
otwartym tekstem.

**Jak ustalić `FTP_DIR`:** w panelu, w tabeli kont FTP, sprawdź kolumnę
„Ścieżka na serwerze". Po zalogowaniu przez FTP ta ścieżka jest widziana
jako katalog główny, więc do `FTP_DIR` wpisujesz to, co zostaje **po niej**:

| Ścieżka konta w panelu | Wartość `FTP_DIR` |
|---|---|
| `/domains/33bots.pl/` | `/public_html/` |
| `/domains/33bots.pl/public_html/` | `/` |
| `/` (konto administratora) | `/domains/33bots.pl/public_html/` |

Gdyby pierwsze wdrożenie zwróciło błąd `550`, ścieżka jest nietrafiona —
wystarczy poprawić ten jeden sekret i uruchomić wdrożenie ponownie.

Sekrety są szyfrowane. Nikt — łącznie ze mną — ich nie zobaczy, nie pojawiają
się też w logach wdrożenia.

### Krok 4. Pierwsze uruchomienie

Zakładka **Actions** → **Wdrożenie na cyber_Folks** → **Run workflow**.

Pierwsze wdrożenie trwa dłużej, bo wysyła komplet plików. Kolejne wysyłają
już tylko to, co się zmieniło — zwykle kilka sekund.

**Przed pierwszym uruchomieniem zrób kopię `public_html`** (Manager plików →
zaznacz wszystko → Kompresuj). Standardowa ostrożność przy pierwszym
automatycznym wdrożeniu.

---

## Jak to działa na co dzień

```
zmiana w repozytorium  →  GitHub Actions  →  33bots.pl
```

Przy każdym wdrożeniu dzieje się po kolei:

1. **Budowanie stylów** — Tailwind kompiluje `assets-redesign.css` z aktualnego
   `index.html`. Arkusz nie może się już rozjechać z treścią strony.
2. **Wersjonowanie** — link do arkusza dostaje numer wersji równy skrótowi
   commita (`assets-redesign.css?v=9e60d04`). To rozwiązuje problem, przez który
   przeglądarka podawała starego CSS-a z pamięci podręcznej i ikony puchły na
   całą kartę.
3. **Kontrola przed wysyłką** — sprawdzane jest, czy HTML ma domknięte znaczniki,
   czy wszystkie bloki danych strukturalnych są poprawnym JSON-em i czy w pliku
   nie zniknął Google Tag Manager, arkusz stylów ani formularz kontaktowy.
   **Gdy któryś warunek nie jest spełniony, wdrożenie się zatrzymuje** i na
   serwer nie trafia nic.
4. **Wysyłka** — przez FTPS (połączenie szyfrowane), tylko zmienione pliki.

### Co nie trafia na serwer

Narzędzia deweloperskie zostają w repozytorium: skrypty `.py`, `tailwind.config.js`,
`tw-input.css`, katalog `og/`, surowe zdjęcia z aparatu, pliki `.md` i katalog `.git`.

### Czego wdrożenie nie kasuje

Pliki wgrane przez Ciebie ręcznie, których nie ma w repozytorium, zostają
nietknięte. Wdrożenie usuwa tylko to, co samo wcześniej wysłało, a co zniknęło
z repozytorium.

---

## Uruchomienie ręczne

Zakładka **Actions** → **Wdrożenie na cyber_Folks** → **Run workflow**.
Przydaje się, gdy chcesz wypchnąć stan repozytorium bez wprowadzania zmian.

## Gdy coś pójdzie nie tak

Wejdź w **Actions** i otwórz nieudane uruchomienie — czerwony krok pokazuje
przyczynę. Najczęstsze przypadki:

- **`530 Login incorrect`** — zły login lub hasło w sekretach.
- **`550` przy wysyłce** — zła wartość `FTP_DIR`. Sprawdź, czy konto FTP jest
  zamknięte w `public_html` (wtedy `/`), czy widzi cały serwer
  (wtedy pełna ścieżka do katalogu domeny).
- **Zatrzymanie na kroku kontroli** — w `index.html` jest błąd. Log wypisuje
  dokładnie który. Na serwer nic nie poszło, strona działa dalej po staremu.

## Wycofanie zmiany

W repozytorium cofnij commit (`git revert`) i zatwierdź. Wdrożenie uruchomi się
samo i przywróci poprzedni stan strony.
