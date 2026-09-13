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
