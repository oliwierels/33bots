#!/usr/bin/env python3
"""
Przygotowanie zdjęć do galerii na stronie głównej.

Bierze zdjęcia z katalogu (HEIC z iPhone'a, JPG, PNG), konwertuje je do
WebP + JPG w rozmiarze odpowiednim dla pasów galerii, a na koniec wypisuje
gotowy HTML do wklejenia w index.html.

UŻYCIE
    python3 dodaj-zdjecia.py ~/zdjecia-z-eventow

    # własny prefiks nazw plików (domyślnie: realizacja)
    python3 dodaj-zdjecia.py ~/zdjecia --prefix gala

WYMAGANIA
    pip install pillow pillow-heif
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Brak biblioteki Pillow. Zainstaluj: pip install pillow pillow-heif")

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
    HEIC = True
except ImportError:
    HEIC = False

ROZSZERZENIA = {'.heic', '.heif', '.jpg', '.jpeg', '.png', '.webp'}
SZEROKOSC = 900          # wystarcza dla kafelka 260×340 na ekranach 2×
JAKOSC_WEBP = 74
JAKOSC_JPG = 78
LIMIT_KB = 260           # ostrzegamy, gdy plik wyjdzie cięższy


def zamien_na_slug(tekst: str) -> str:
    znaki = {'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n',
             'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z', ' ': '-', '_': '-'}
    wynik = ''.join(znaki.get(z, z) for z in tekst.lower())
    return ''.join(z for z in wynik if z.isalnum() or z == '-').strip('-')


def przetworz(plik: Path, nazwa: str) -> tuple[int, int, int]:
    obraz = ImageOps.exif_transpose(Image.open(plik)).convert('RGB')
    skala = SZEROKOSC / obraz.width
    if skala < 1:
        obraz = obraz.resize((SZEROKOSC, round(obraz.height * skala)), Image.LANCZOS)

    obraz.save(f'{nazwa}.webp', 'WEBP', quality=JAKOSC_WEBP, method=6)
    obraz.save(f'{nazwa}.jpg', 'JPEG', quality=JAKOSC_JPG, optimize=True, progressive=True)

    waga = Path(f'{nazwa}.webp').stat().st_size // 1024
    return obraz.width, obraz.height, waga


def main() -> None:
    parser = argparse.ArgumentParser(description='Konwersja zdjęć do galerii 33bots.')
    parser.add_argument('katalog', help='katalog ze zdjęciami do przetworzenia')
    parser.add_argument('--prefix', default='realizacja', help='przedrostek nazw plików wyjściowych')
    args = parser.parse_args()

    zrodlo = Path(args.katalog).expanduser()
    if not zrodlo.is_dir():
        sys.exit(f'Nie znaleziono katalogu: {zrodlo}')

    zdjecia = sorted(p for p in zrodlo.iterdir() if p.suffix.lower() in ROZSZERZENIA)
    if not zdjecia:
        sys.exit(f'Brak zdjęć w {zrodlo}. Obsługiwane formaty: {", ".join(sorted(ROZSZERZENIA))}')

    if any(p.suffix.lower() in {'.heic', '.heif'} for p in zdjecia) and not HEIC:
        sys.exit('Znaleziono pliki HEIC. Zainstaluj obsługę: pip install pillow-heif')

    print(f'Znaleziono {len(zdjecia)} zdjęć.\n')
    snippety = []

    for numer, plik in enumerate(zdjecia, start=1):
        nazwa = f'{zamien_na_slug(args.prefix)}-{numer:02d}'
        szer, wys, waga = przetworz(plik, nazwa)
        ostrzezenie = '  ⚠ ciężkie — rozważ mocniejszą kompresję' if waga > LIMIT_KB else ''
        print(f'  {plik.name}  →  {nazwa}.webp / .jpg   {szer}×{wys}, {waga} KB{ostrzezenie}')

        snippety.append(
            f'      <figure class="strip-item group">\n'
            f'        <picture><source srcset="{nazwa}.webp" type="image/webp" />\n'
            f'        <img src="{nazwa}.jpg" alt="OPISZ ZDJĘCIE" loading="lazy" class="strip-img" /></picture>\n'
            f'        <figcaption class="strip-cap">PODPIS</figcaption>\n'
            f'      </figure>'
        )

    print('\n' + '─' * 70)
    print('HTML do wklejenia w index.html')
    print('Każdy blok wklej DWA RAZY w tym samym pasie: raz w części')
    print('oznaczonej ORYGINAŁ, raz w części KOPIA (bezszwowa pętla).')
    print('Uzupełnij alt i figcaption — alt jest ważny dla SEO.')
    print('─' * 70 + '\n')
    print('\n'.join(snippety))

    print('\nNa koniec przebuduj arkusz stylów:')
    print('  npx tailwindcss -c tailwind.config.js -i tw-input.css -o assets-redesign.css --minify')


if __name__ == '__main__':
    main()
