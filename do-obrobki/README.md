# Surowe zdjęcia i nagrania

Tu wrzucasz materiały prosto z telefonu, aparatu albo z Dysku Google.

**Ta gałąź nie trafia na stronę.** Serwer pobiera wyłącznie gałąź
`claude/33bots-website-T0REs`, więc cokolwiek tu wrzucisz, jest dla niego
niewidoczne. Możesz wrzucać bez żadnych obaw.

## Jak wrzucić

1. Upewnij się, że u góry strony na GitHubie wybrana jest gałąź **`materialy`**
   (lista rozwijana po lewej, nad spisem plików).
2. Wejdź do katalogu `do-obrobki`.
3. **Add file** → **Upload files** → przeciągnij pliki.
4. W polu zatwierdzania zostaw **Commit directly to the `materialy` branch**.

Przeglądarka przyjmuje pliki **do 25 MB**. Zdjęcia z telefonu mieszczą się
spokojnie — nawet te z iPhone'a w HEIC.

Nazwy nie mają znaczenia, nadaję własne przy obróbce. Jeśli wiesz, z jakiego
wydarzenia są które zdjęcia, napisz to w wiadomości albo wrzuć je w podkatalogi
z nazwą wydarzenia — ułatwi to opisanie ich na stronie.

## Co się dzieje dalej

Napisz, że pliki są. Wtedy:

1. Konwertuję zdjęcia do WebP i JPG w rozmiarze galerii plus wariant 400 px
   na telefony.
2. Nadaję nazwy opisowe pod SEO i piszę teksty alternatywne.
3. Wstawiam je na stronę — do pasów realizacji, do case study, gdzie trzeba.
4. Gotowe wersje trafiają na gałąź produkcyjną, surowe zostają tutaj.

Na stronę idą wyłącznie wersje webowe: zdjęcie z telefonu waży 3–12 MB,
po obróbce około 50–250 KB. Przy kilkudziesięciu zdjęciach to różnica między
stroną, która się wczytuje, a taką, która się wlecze.

## Nagrania — przeczytaj, zanim wrzucisz

**Pełne materiały wideo wrzucaj na YouTube, nie tutaj.** Osadzam je potem
na stronie i nie ważą nic. Tak działa już relacja z finału Eco Studio
i nagrania w case study LEX AI.

Powody są dwa. Repozytorium trzyma historię na zawsze — raz wrzucone 200 MB
nagrań zostaje w nim, nawet gdy pliki skasujesz. Drugi: YouTube sam dobiera
jakość do łącza odwiedzającego, a plik z naszego serwera zawsze leci w całości.

Wyjątek to **krótkie pętle bez dźwięku** w tle sekcji, takie jak te
w katalogu `video/`. Mają po 1,5–5 MB i tylko dlatego mogą leżeć u nas.
Jeśli masz surowy materiał na taką pętlę, wrzuć go tutaj — skompresuję
go ffmpegiem do tego rozmiaru.

## Plik większy niż 25 MB

Przeglądarka go nie przyjmie. Wrzuć wtedy na YouTube i podaj link albo
prześlij przez `git push` z komputera — tam limit to 100 MB na plik.
