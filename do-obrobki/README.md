# Surowe materiały do obróbki

**Nie wrzucaj tu plików na gałęzi produkcyjnej.** Surowe zdjęcia i nagrania
idą na osobną gałąź **`materialy`** — serwer jej nie pobiera, więc nic
przypadkiem nie wyląduje na stronie.

Instrukcja krok po kroku leży w tym samym pliku, ale na tamtej gałęzi:
[github.com/oliwierels/33bots/tree/materialy/do-obrobki](https://github.com/oliwierels/33bots/tree/materialy/do-obrobki)

## Dlaczego osobna gałąź

Serwer przy każdej publikacji pobiera paczkę **wyłącznie z gałęzi
`claude/33bots-website-T0REs`**. Cokolwiek leży na innej gałęzi, jest dla
niego niewidoczne — i o to chodzi.

Ten katalog jest co prawda wykluczony z wdrożenia w `.deployignore`
i w `deploy.php`, ale kopia `deploy.php` działająca na serwerze została
wgrana ręcznie i nie aktualizuje się razem z repozytorium. Dopóki nie
zostanie wgrana ponownie, wykluczenie tam nie obowiązuje. Osobna gałąź
działa niezależnie od tego i nie wymaga niczego robić na hostingu.
