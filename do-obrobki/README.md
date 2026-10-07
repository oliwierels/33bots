# Surowe materiały do obróbki

Tu wrzucasz zdjęcia i nagrania prosto z telefonu, aparatu albo z Dysku Google.
**Nic z tego katalogu nie trafia na serwer** — jest wykluczony i w `.deployignore`,
i w `deploy.php`, więc możesz wrzucać bez obaw, że strona spuchnie.

## Jak wrzucić

Na GitHubie: wejdź do tego katalogu → **Add file** → **Upload files** → przeciągnij
pliki → **Commit changes**.

Przeglądarka przyjmuje pliki **do 25 MB**. Zdjęcia z telefonu mieszczą się
spokojnie. Gdyby nagranie było większe, patrz niżej.

Nazwy nie mają znaczenia — i tak nadaję własne przy konwersji.

## Co się dzieje dalej

Napisz, że pliki są. Wtedy:

1. Konwertuję zdjęcia do WebP i JPG w rozmiarze galerii plus wariant 400 px
   na telefony (`dodaj-zdjecia.py` i `warianty-zdjec.py`).
2. Nadaję nazwy opisowe dla SEO i piszę teksty alternatywne.
3. Wstawiam je na stronę — do pasów realizacji, do case study, gdzie trzeba.
4. Kasuję stąd surowe pliki tym samym commitem.

Na stronę idą wyłącznie wersje webowe: zdjęcie z telefonu waży 3–12 MB,
po obróbce około 50–250 KB. Przy kilkudziesięciu zdjęciach to różnica między
stroną, która się wczytuje, a taką, która się wlecze.

## Nagrania — przeczytaj, zanim wrzucisz

**Pełne materiały wideo wrzucaj na YouTube, nie tutaj.** Osadzam je potem na
stronie i nic nie waży. Tak działa już relacja z finału Eco Studio
i nagrania w case study LEX AI.

Powody są dwa. Repozytorium trzyma historię na zawsze — raz wrzucone 200 MB
nagrań zostaje w nim, nawet gdy skasujesz pliki, a każde wdrożenie pobiera
całą paczkę z GitHuba. Drugi powód: YouTube sam dobiera jakość do łącza
odwiedzającego, a plik z naszego serwera zawsze leci w całości.

Wyjątek to **krótkie pętle bez dźwięku** w tle sekcji — takie jak te
w katalogu `video/`. Mają po 1,5–5 MB i tylko dlatego mogą leżeć u nas.
Jeśli masz surowy materiał na taką pętlę, wrzuć go tutaj — skompresuję
go ffmpegiem do tego rozmiaru.

## Plik większy niż 25 MB

Przeglądarka go nie przyjmie. Wtedy albo wrzuć na YouTube i podaj link,
albo prześlij go przez `git push` z komputera — tam limit to 100 MB na plik.
