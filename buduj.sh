#!/usr/bin/env bash
#
# Budowanie strony przed zatwierdzeniem zmian.
#
# Kompiluje arkusz Tailwinda i oznacza go w index.html sumą kontrolną
# jego własnej treści. Dzięki temu numer wersji zmienia się dokładnie
# wtedy, gdy zmieni się wygląd — ani razu więcej, ani razu mniej —
# a przeglądarka nigdy nie poda starego arkusza z pamięci podręcznej.
#
# UŻYCIE
#     ./buduj.sh
#
# Uruchom po każdej zmianie w index.html i przed zatwierdzeniem commita.

set -euo pipefail
cd "$(dirname "$0")"

echo "Kompiluję arkusz stylów…"
npx --yes tailwindcss@3.4.17 \
  -c tailwind.config.js \
  -i tw-input.css \
  -o assets-redesign.css \
  --minify

WERSJA=$(md5sum assets-redesign.css | cut -c1-8)
sed -i -E "s|href=\"assets-redesign\.css(\?v=[^\"]*)?\"|href=\"assets-redesign.css?v=${WERSJA}\"|g" index.html

echo "Arkusz: $(du -h assets-redesign.css | cut -f1), oznaczony wersją ${WERSJA}"
grep -o 'href="assets-redesign\.css[^"]*"' index.html
