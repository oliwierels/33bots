#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator obrazów Open Graph serwisu AT.

Dla każdej strony HTML w katalogu wdrożeniowym tworzy kartę 1200×630 z
niemieckim tytułem strony. Tło: zdjęcie robota (og-image.jpg) przyciemnione
gradientem od lewej, akcentowa kreska, stopka z domeną.

Uruchomienie (po generate_site.py):
    cd build && python3 make_og.py
"""

import glob
import os
import re

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OG_DIR = os.path.join(BASE, "og")
BG = os.path.join(BASE, "og-image.jpg")
FOOTER = "33bots.at — humanoide Roboter für Events"
ACCENT = (111, 214, 255)
W, H = 1200, 630

FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

SKIP = {"index-redesign.html", "404.html", "vorlage-case-study.html"}


def page_title(path):
    html = open(path, encoding="utf-8").read(4000)
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    if not m:
        return None
    title = re.sub(r"\s+", " ", m.group(1)).strip()
    title = title.split(" | ")[0].split(" — 33bots")[0].strip()
    return title


def wrap(draw, text, font, max_w):
    words, lines, line = text.split(), [], ""
    for w in words:
        probe = f"{line} {w}".strip()
        if draw.textlength(probe, font=font) <= max_w:
            line = probe
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def card(title, out_path):
    img = Image.open(BG).convert("RGB").resize((W, H))
    # gradient przyciemniający lewą połowę — tekst musi być czytelny
    overlay = Image.new("L", (W, 1))
    for x in range(W):
        overlay.putpixel((x, 0), int(max(0, 235 - x * 0.26)))
    mask = overlay.resize((W, H))
    img = Image.composite(Image.new("RGB", (W, H), (5, 7, 10)), img, mask)

    draw = ImageDraw.Draw(img)
    draw.rectangle([72, 132, 152, 140], fill=ACCENT)

    size = 62
    while size > 34:
        font = ImageFont.truetype(FONT_BOLD, size)
        lines = wrap(draw, title, font, 620)
        if len(lines) <= 4:
            break
        size -= 4
    y = 176
    for line in lines[:4]:
        draw.text((72, y), line, font=font, fill=(255, 255, 255))
        y += int(size * 1.22)

    draw.text((72, H - 84), FOOTER, font=ImageFont.truetype(FONT_REG, 26),
              fill=(150, 158, 168))
    img.save(out_path, "JPEG", quality=86, optimize=True, progressive=True)


def main():
    os.makedirs(OG_DIR, exist_ok=True)
    pages = sorted(glob.glob(os.path.join(BASE, "*.html")))
    made = 0
    for page in pages:
        name = os.path.basename(page)
        if name in SKIP:
            continue
        title = page_title(page)
        if not title:
            print(f"  bez <title>: {name}")
            continue
        card(title, os.path.join(OG_DIR, name.replace(".html", ".jpg")))
        made += 1
    # stare karty bez odpowiadającej strony (np. po zmianie slugów)
    valid = {os.path.basename(p).replace(".html", ".jpg") for p in pages}
    for old in glob.glob(os.path.join(OG_DIR, "*.jpg")):
        if os.path.basename(old) not in valid:
            os.remove(old)
            print(f"  usunięto nieaktualną kartę: {os.path.basename(old)}")
    print(f"Wygenerowano {made} kart OG w og/")


if __name__ == "__main__":
    main()
