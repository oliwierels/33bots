#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Performance & meta SEO fixes:
  1. Replace render-blocking Google Fonts with async preload pattern
  2. Trim meta descriptions > 160 chars to ≤ 155 chars
  3. Add dns-prefetch for Albacross (3rd-party tracking script)
"""

import os
import re
import glob

BASE = "/home/user/33bots"

# ──────────────────────────────────────────
# 1. ASYNC GOOGLE FONTS
# ──────────────────────────────────────────
FONTS_BLOCKING = (
    '<link href="https://fonts.googleapis.com/css2?family=Inter:'
    'wght@400;500;600;700;800&display=swap" rel="stylesheet" />'
)
FONTS_ASYNC = (
    '<link rel="preload" '
    'href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" '
    'as="style" onload="this.onload=null;this.rel=\'stylesheet\'" />\n'
    '  <noscript>'
    '<link rel="stylesheet" '
    'href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" />'
    '</noscript>'
)

DNS_PREFETCH = '  <link rel="dns-prefetch" href="//serve.albacross.com" />\n'
DNS_SEARCH   = '<link rel="preconnect" href="https://fonts.googleapis.com" />'

# ──────────────────────────────────────────
# 2. TRIMMED META DESCRIPTIONS (≤ 155 chars)
# ──────────────────────────────────────────
META_OVERRIDES = {
    "index.html": (
        "Wynajmij robota humanoidalnego Unitree G1 na event, targi lub konferencję w Polsce. "
        "Najniższe ceny, darmowy transport, certyfikowany operator. Sprawdź dostępność →"
    ),
    "blog-atrakcja-na-event-firmowy.html": (
        "Porównanie atrakcji eventowych: robot humanoidalny, artyści, food trucki, VR. "
        "Które rozwiązanie generuje największy efekt WOW i zwrot z inwestycji?"
    ),
    "blog-ile-kosztuje-wynajem-robota.html": (
        "Ile kosztuje wynajem robota humanoidalnego Unitree G1? Pakiety, co wchodzi w cenę, "
        "darmowy transport i jak wygląda wycena. Przewodnik 2026."
    ),
    "blog-robot-na-wesele.html": (
        "Robot humanoidalny na wesele — hit czy faux pas? Jak G1 sprawdza się jako atrakcja: "
        "powitanie gości, parkiet, viralowe zdjęcia i konkretne ceny."
    ),
    "blog-wypozyczenie-robota-przewodnik.html": (
        "Jak wypożyczyć robota humanoidalnego? Co zawiera usługa, ile kosztuje, "
        "na co zwrócić uwagę. Kompletny przewodnik dla organizatorów eventów."
    ),
    "oferta-dni-otwarte.html": (
        "Wynajem robota humanoidalnego na dzień otwarty lub showroom. "
        "G1 przyciąga tłumy i generuje viral w social mediach. Darmowy transport →"
    ),
    "oferta-targi.html": (
        "Wynajmij robota humanoidalnego Unitree G1 na stoisko targowe. "
        "Więcej leadów, viralowy zasięg w social mediach. Darmowy transport — zapytaj →"
    ),
    "robot-na-impreze.html": (
        "Wynajmij robota humanoidalnego na imprezę firmową, galę lub uroczystość. "
        "Unitree G1 — darmowy transport, certyfikowany operator. Wycena w 24h →"
    ),
    "robot-wynajem-dabrowa-gornicza.html": (
        "Wynajem robota humanoidalnego G1 w Dąbrowie Górniczej — eventy, konferencje, targi. "
        "Darmowy transport, certyfikowany operator. Sprawdź dostępność →"
    ),
    "robot-wynajem-gdansk.html": (
        "Wynajem robota humanoidalnego G1 w Gdańsku i Trójmieście — Amberexpo, konferencje, gale. "
        "Darmowy transport, certyfikowany operator →"
    ),
    "robot-wynajem-wroclaw.html": (
        "Wynajem robota humanoidalnego G1 we Wrocławiu — Hala Stulecia, targi, konferencje. "
        "Darmowy transport, certyfikowany operator. Sprawdź →"
    ),
    "wypozyczenie-robota.html": (
        "Wypożycz robota humanoidalnego Unitree G1 na event, targi lub konferencję. "
        "Robot do wynajęcia w Polsce — darmowy transport, operator w cenie →"
    ),
}

# ──────────────────────────────────────────
# PROCESS ALL HTML FILES
# ──────────────────────────────────────────
html_files = glob.glob(os.path.join(BASE, "*.html"))
updated = 0

for filepath in sorted(html_files):
    filename = os.path.basename(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    original = content

    # 1. Async fonts
    if FONTS_BLOCKING in content:
        content = content.replace(FONTS_BLOCKING, FONTS_ASYNC, 1)

    # 2. dns-prefetch for Albacross (only on pages that load it)
    if "albacross" in content and "dns-prefetch" not in content:
        content = content.replace(DNS_SEARCH, DNS_PREFETCH + DNS_SEARCH, 1)

    # 3. Trim meta description
    if filename in META_OVERRIDES:
        new_desc = META_OVERRIDES[filename]
        content = re.sub(
            r'(<meta name="description" content=")[^"]+(")',
            r'\g<1>' + new_desc + r'\g<2>',
            content,
            count=1,
        )
        # Also update OG description to match (trim to same)
        content = re.sub(
            r'(<meta property="og:description" content=")[^"]+(")',
            r'\g<1>' + new_desc + r'\g<2>',
            content,
            count=1,
        )
        # And twitter description
        content = re.sub(
            r'(<meta name="twitter:description" content=")[^"]+(")',
            r'\g<1>' + new_desc + r'\g<2>',
            content,
            count=1,
        )

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        updated += 1
        print(f"  Updated: {filename}")

print(f"\n✓ {updated} files updated")

# ──────────────────────────────────────────
# VERIFY — print lengths of updated descs
# ──────────────────────────────────────────
print("\n=== Verified meta desc lengths ===")
for filename, desc in META_OVERRIDES.items():
    print(f"  {len(desc):3d}c  {filename}")
