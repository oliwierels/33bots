# Skille projektowe

Skille Claude'a do pracy nad wyglądem 33bots.pl. Ładują się same w każdej sesji
Claude'a otwartej na tym repozytorium. Na serwer nie trafiają (`.deployignore`,
`narzedzia-serwer/deploy.php`, reguła 404 w `.htaccess`).

| Skill | Źródło | Wersja | Do czego |
|---|---|---|---|
| `impeccable` | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) (Apache 2.0) | 4.7.0, commit `dad8dbb` | Przegląd UX, audyt techniczny, polerka, typografia, układ. Komendy: `/impeccable critique`, `/impeccable audit`, `/impeccable polish` |
| `design-taste-frontend` | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) (MIT) | v2, commit `6010f91` | Kierunek wizualny stron marketingowych, lista „objawów AI-slopu”, krytyka na zrzutach |
| `emil-design-eng` | [emilkowalski/skills](https://github.com/emilkowalski/skills) (MIT) | commit `2d22863` | Filozofia polerki interfejsu i decyzji o animacjach |
| `review-animations`, `improve-animations`, `animate`, `animation-performance`, `find-animation-opportunities`, `animation-vocabulary` | jw. | jw. | Przegląd, plan i budowa animacji |
| `apple-design`, `mobile-native`, `break-ui` | jw. | jw. | Ruch i materiały w stylu Apple, zachowanie na telefonie, testy skrajnych danych |
| `pick-ui-library`, `prototype` | jw. | jw. | Tylko na wyraźne wywołanie |

Pominięte z zestawu Emila: `write-swift`, `animate-expo`, `ask-sonner` (iOS, React Native
i biblioteka Reacta — nie dotyczą tej strony).

Z `impeccable` dodany jest sam skill, bez hooków wtyczki (te uruchamiały skrypt po każdej
edycji pliku). Skrypt `scripts/impeccable` przy pierwszym uruchomieniu pobiera swój program
z sieci; gdy to się nie uda, skill działa dalej na samych instrukcjach.

## Aktualizacja

Skopiuj na nowo folder skilla z repozytorium źródłowego, np.:

```bash
git clone --depth 1 https://github.com/emilkowalski/skills /tmp/emil
cp -r /tmp/emil/skills/emil-design-eng .claude/skills/
```

Dla `impeccable` folderem do skopiowania jest `plugin/skills/impeccable`, dla taste-skill
`skills/taste-skill` (zapisany tu jako `design-taste-frontend`).
