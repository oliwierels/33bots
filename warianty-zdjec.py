# -*- coding: utf-8 -*-
"""Mniejsze warianty zdjęć do galerii (400 px szerokości, WebP).

Na telefonie pasy zdjęć mają około 380 px szerokości, a przeglądarka pobierała
pełne pliki po 150–270 KB. Wariant 400 px waży kilkanaście–kilkadziesiąt KB, więc
strona główna schudła z 3,8 MB odwołań do około 1 MB na wąskim ekranie.

Uruchomienie:  python3 warianty-zdjec.py
Wymaga Pillow. Zapisuje pliki <nazwa>-400.webp obok oryginałów.
"""
import glob
import os

from PIL import Image

SZEROKOSC = 400
WZORCE = ("realizacja-*.jpg", "robot-pies-*.jpg", "robot-g1-studio.jpg")


def main():
    zrobione = 0
    for wzorzec in WZORCE:
        for zrodlo in sorted(glob.glob(wzorzec)):
            cel = zrodlo.rsplit(".", 1)[0] + "-400.webp"
            if os.path.exists(cel) and os.path.getmtime(cel) >= os.path.getmtime(zrodlo):
                continue
            obraz = Image.open(zrodlo)
            if obraz.width > SZEROKOSC:
                wysokosc = round(obraz.height * SZEROKOSC / obraz.width)
                obraz = obraz.resize((SZEROKOSC, wysokosc), Image.LANCZOS)
            obraz.convert("RGB").save(cel, "WEBP", quality=82, method=6)
            zrobione += 1
            print(f"  ✓ {cel} ({os.path.getsize(cel)//1024} KB)")
    print(f"Wariantów zapisanych: {zrobione}")


if __name__ == "__main__":
    main()
