#!/usr/bin/env bash
#
# Budowanie strony przed zatwierdzeniem zmian.
#
# Kompiluje arkusz Tailwinda i oznacza go w każdej stronie sumą kontrolną
# jego własnej treści. Dzięki temu numer wersji zmienia się dokładnie
# wtedy, gdy zmieni się wygląd — ani razu więcej, ani razu mniej —
# a przeglądarka nigdy nie poda starego arkusza z pamięci podręcznej.
#
# UŻYCIE
#     ./buduj.sh
#
# Uruchom po każdej zmianie w stronach i przed zatwierdzeniem commita.
# Strony do oznaczenia wyszukiwane są same — wystarczy, że nowa podstrona
# odwołuje się do assets-redesign.css. Pamiętaj tylko dopisać ją do
# tailwind.config.js, inaczej jej klasy nie trafią do arkusza.

set -euo pipefail
cd "$(dirname "$0")"

# Artykuły poradnika: tresci/artykuly/*.html → strony w katalogu głównym.
if [ -f tresci/buduj_artykuly.py ]; then
  echo "Składam artykuły poradnika…"
  python3 tresci/buduj_artykuly.py
fi

echo "Kompiluję arkusz stylów…"
npx --yes tailwindcss@3.4.17 \
  -c tailwind.config.js \
  -i tw-input.css \
  -o assets-redesign.css \
  --minify

WERSJA=$(md5sum assets-redesign.css | cut -c1-8)

echo "Arkusz: $(du -h assets-redesign.css | cut -f1), wersja ${WERSJA}"

STRONY=$(grep -rl 'assets-redesign\.css' --include='*.html' . | sed 's|^\./||' | sort)
for STRONA in ${STRONY}; do
  sed -i -E "s|href=\"assets-redesign\.css(\?v=[^\"]*)?\"|href=\"assets-redesign.css?v=${WERSJA}\"|g" "${STRONA}"
  echo "  ${STRONA} → $(grep -o 'href="assets-redesign\.css[^"]*"' "${STRONA}" | head -1)"
done

# css/site.css — nowy system wizualny. Tak samo jak arkusz Tailwinda dostaje
# w adresie sumę kontrolną treści, żeby przeglądarka nie podała starej wersji.
WERSJA_SITE=$(md5sum css/site.css | cut -c1-8)
for STRONA in $(grep -rl 'css/site\.css' --include='*.html' . | sed 's|^\./||' | sort); do
  sed -i -E "s|href=\"css/site\.css(\?v=[^\"]*)?\"|href=\"css/site.css?v=${WERSJA_SITE}\"|g" "${STRONA}"
  echo "  ${STRONA} → css/site.css?v=${WERSJA_SITE}"
done

# main.js — skrypt starych podstron. Wersja w adresie z tego samego powodu:
# stara kopia z pamięci przeglądarki nie pasowałaby do nowego HTML.
WERSJA_JS=$(md5sum main.js | cut -c1-8)
for STRONA in $(grep -rl 'src="main\.js' --include='*.html' . | sed 's|^\./||' | sort); do
  sed -i -E "s|src=\"main\.js(\?v=[^\"]*)?\"|src=\"main.js?v=${WERSJA_JS}\"|g" "${STRONA}"
done
echo "  main.js?v=${WERSJA_JS} na $(grep -rl 'src="main\.js' --include='*.html' . | wc -l) stronach"

# js/strona.js — wspólny skrypt podstron w nowym systemie (artykuły).
WERSJA_STRONA=$(md5sum js/strona.js | cut -c1-8)
for STRONA in $(grep -rl 'src="js/strona\.js' --include='*.html' . | sed 's|^\./||' | sort); do
  sed -i -E "s|src=\"js/strona\.js(\?v=[^\"]*)?\"|src=\"js/strona.js?v=${WERSJA_STRONA}\"|g" "${STRONA}"
done
echo "  js/strona.js?v=${WERSJA_STRONA} na $(grep -rl 'src="js/strona\.js' --include='*.html' . | wc -l) stronach"
