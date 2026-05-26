#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch SEO update:
  1. Add BlogPosting schema to 6 blog pages missing it
  2. Add Service + LocalBusiness schema to all 38 city pages
  3. Add og:image:width + og:image:height to all city & blog pages
  4. Add footer NAP to all city, blog and offer pages
  5. Fix copyright year 2025 → 2026 across all pages
  6. Update sitemap.xml (add missing page, refresh lastmod dates)
"""

import os
import re

BASE = "/home/user/33bots"
TODAY = "2026-05-26"

# ─────────────────────────────────────────────
# BLOG PAGES — metadata for BlogPosting schema
# ─────────────────────────────────────────────
BLOG_META = {
    "blog-robot-na-evencie.html": {
        "headline": "5 powodów, dla których Twój event potrzebuje humanoida",
        "description": "Dlaczego wynajem robota humanoidalnego Unitree G1 to najlepsza atrakcja eventowa? Więcej leadów, viralowy zasięg, efekt WOW.",
        "date": "2025-10-01",
    },
    "blog-robotyka-w-marketingu.html": {
        "headline": "Robotyka w nowoczesnym marketingu B2B",
        "description": "Jak roboty humanoidalne rewolucjonizują marketing w branży IT i przemyśle? Strategia wdrożenia humanoida w komunikacji marki.",
        "date": "2025-10-15",
    },
    "blog-atrakcja-na-event-firmowy.html": {
        "headline": "Atrakcja na event firmowy: robot vs inne opcje",
        "description": "Porównanie popularnych atrakcji eventowych według efektu WOW, zasięgu social media i wartości biznesowej.",
        "date": "2025-11-01",
    },
    "blog-ile-kosztuje-wynajem-robota.html": {
        "headline": "Ile kosztuje wynajem robota? Ceny i pakiety 2026",
        "description": "Transparentny przewodnik po kosztach wynajmu robota Unitree G1. Co wchodzi w cenę, jak wygląda wycena.",
        "date": "2025-11-15",
    },
    "blog-atrakcje-eventowe.html": {
        "headline": "Atrakcje eventowe 2026 — ranking i porównanie",
        "description": "Jakie atrakcje eventowe sprawdzają się najlepiej? Ranking i porównanie z robotem humanoidalnym na tle innych opcji.",
        "date": "2025-12-01",
    },
    "blog-robot-na-wesele.html": {
        "headline": "Wynajem robota na wesele — czy to ma sens?",
        "description": "Robot humanoidalny na weselu to gwarancja, że goście będą mówić o tym wydarzeniu latami. Sprawdź jak G1 sprawdza się na weselach.",
        "date": "2025-12-15",
    },
}

# ─────────────────────────────────────────────
# CITY PAGES
# ─────────────────────────────────────────────
CITIES_MAP = {
    "robot-wynajem-warszawa.html": "Warszawa",
    "robot-wynajem-krakow.html": "Kraków",
    "robot-wynajem-wroclaw.html": "Wrocław",
    "robot-wynajem-poznan.html": "Poznań",
    "robot-wynajem-gdansk.html": "Gdańsk",
    "robot-wynajem-katowice.html": "Katowice",
    "robot-wynajem-lodz.html": "Łódź",
    "robot-wynajem-szczecin.html": "Szczecin",
    "robot-wynajem-bydgoszcz.html": "Bydgoszcz",
    "robot-wynajem-lublin.html": "Lublin",
    "robot-wynajem-bialystok.html": "Białystok",
    "robot-wynajem-rzeszow.html": "Rzeszów",
    "robot-wynajem-torun.html": "Toruń",
    "robot-wynajem-olsztyn.html": "Olsztyn",
    "robot-wynajem-kielce.html": "Kielce",
    "robot-wynajem-opole.html": "Opole",
    "robot-wynajem-gliwice.html": "Gliwice",
    "robot-wynajem-czestochowa.html": "Częstochowa",
    "robot-wynajem-radom.html": "Radom",
    "robot-wynajem-zielona-gora.html": "Zielona Góra",
    "robot-wynajem-sosnowiec.html": "Sosnowiec",
    "robot-wynajem-plock.html": "Płock",
    "robot-wynajem-elblag.html": "Elbląg",
    "robot-wynajem-walbrzych.html": "Wałbrzych",
    "robot-wynajem-wloclawek.html": "Włocławek",
    "robot-wynajem-tarnow.html": "Tarnów",
    "robot-wynajem-koszalin.html": "Koszalin",
    "robot-wynajem-legnica.html": "Legnica",
    "robot-wynajem-kalisz.html": "Kalisz",
    "robot-wynajem-grudziadz.html": "Grudziądz",
    "robot-wynajem-zabrze.html": "Zabrze",
    "robot-wynajem-bytom.html": "Bytom",
    "robot-wynajem-rybnik.html": "Rybnik",
    "robot-wynajem-tychy.html": "Tychy",
    "robot-wynajem-dabrowa-gornicza.html": "Dąbrowa Górnicza",
    "robot-wynajem-chorzow.html": "Chorzów",
    "robot-wynajem-jaworzno.html": "Jaworzno",
    "robot-wynajem-slupsk.html": "Słupsk",
    "robot-wynajem-nowy-sacz.html": "Nowy Sącz",
    "robot-wynajem-pila.html": "Piła",
}

NAP_SNIPPET = (
    '<p class="footer__tagline">Wynajem robotów humanoidalnych · Polska</p>\n'
    '        <div class="footer__nap">\n'
    '          <a href="tel:+48531408004" class="footer__nap-item">+48 531 408 004</a>\n'
    '          <a href="mailto:kontakt@33bots.pl" class="footer__nap-item">kontakt@33bots.pl</a>\n'
    '        </div>\n'
    '      </div>'
)
NAP_SEARCH = '<p class="footer__tagline">Wynajem robotów humanoidalnych · Polska</p>\n      </div>'


def inject_before_head_close(content, snippet):
    return content.replace('</head>', snippet + '\n</head>', 1)


def add_og_image_dims(content):
    if 'og:image:width' in content:
        return content
    return content.replace(
        '<meta property="og:image:alt"',
        '<meta property="og:image:width" content="1200" />\n  <meta property="og:image:height" content="630" />\n  <meta property="og:image:alt"',
        1,
    )


def add_footer_nap(content):
    if 'footer__nap' in content:
        return content
    return content.replace(NAP_SEARCH, NAP_SNIPPET, 1)


def fix_copyright(content):
    return content.replace('© 2025 33bots.', '© 2026 33bots.')


# ─────────────────────────────────────────────
# 1. BLOG PAGES
# ─────────────────────────────────────────────
print("=== Blog pages ===")
all_blog_files = [f for f in os.listdir(BASE) if f.startswith('blog-') and f.endswith('.html')]

for filename in all_blog_files:
    filepath = os.path.join(BASE, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Extract canonical URL
    m = re.search(r'<link rel="canonical" href="([^"]+)"', content)
    url = m.group(1) if m else f"https://33bots.pl/{filename}"

    # Add BlogPosting schema if missing
    if '"BlogPosting"' not in content and '"Article"' not in content:
        meta = BLOG_META.get(filename)
        if meta:
            schema = f"""
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "{meta['headline']}",
    "description": "{meta['description']}",
    "datePublished": "{meta['date']}",
    "dateModified": "{TODAY}",
    "author": {{"@type": "Organization", "name": "33bots", "url": "https://33bots.pl"}},
    "publisher": {{
      "@type": "Organization",
      "name": "33bots",
      "url": "https://33bots.pl",
      "logo": {{"@type": "ImageObject", "url": "https://33bots.pl/favicon.svg"}}
    }},
    "image": "https://33bots.pl/robot-g1.jpg",
    "url": "{url}",
    "mainEntityOfPage": {{"@type": "WebPage", "@id": "{url}"}}
  }}
  </script>"""
            content = inject_before_head_close(content, schema)

    # Add og:article:published_time if og:type=article and missing
    if 'og:type" content="article"' in content and 'article:published_time' not in content:
        meta = BLOG_META.get(filename)
        if meta:
            og_extra = (
                f'  <meta property="article:published_time" content="{meta["date"]}T00:00:00+01:00" />\n'
                f'  <meta property="article:modified_time" content="{TODAY}T00:00:00+01:00" />\n'
                f'  <meta property="article:author" content="33bots" />\n'
            )
            if '<meta name="author"' in content:
                content = content.replace('<meta name="author"', og_extra + '  <meta name="author"', 1)
            else:
                content = inject_before_head_close(content, og_extra.strip())

    content = add_og_image_dims(content)
    content = add_footer_nap(content)
    content = fix_copyright(content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Updated: {filename}")
    else:
        print(f"  No change: {filename}")

# ─────────────────────────────────────────────
# 2. CITY PAGES
# ─────────────────────────────────────────────
print("\n=== City pages ===")
for filename, city_name in CITIES_MAP.items():
    filepath = os.path.join(BASE, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Add Service + LocalBusiness schema if missing
    if '"Service"' not in content:
        schema = f"""
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Service",
    "name": "Wynajem robota humanoidalnego — {city_name}",
    "description": "Wynajem robota Unitree G1 na eventy, konferencje i targi w {city_name}. Darmowy transport, certyfikowany operator.",
    "url": "https://33bots.pl/{filename}",
    "image": "https://33bots.pl/robot-g1.jpg",
    "provider": {{
      "@type": "LocalBusiness",
      "name": "33bots – Wynajem Robotów na Eventy i Targi",
      "url": "https://33bots.pl",
      "telephone": "+48531408004",
      "email": "kontakt@33bots.pl"
    }},
    "areaServed": {{
      "@type": "City",
      "name": "{city_name}"
    }},
    "serviceType": "Wynajem robotów humanoidalnych"
  }}
  </script>"""
        content = inject_before_head_close(content, schema)

    content = add_og_image_dims(content)
    content = add_footer_nap(content)
    content = fix_copyright(content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Updated: {filename}")
    else:
        print(f"  No change: {filename}")

# ─────────────────────────────────────────────
# 3. OTHER PAGES (oferta, wypozyczenie, etc.)
# ─────────────────────────────────────────────
print("\n=== Other pages ===")
OTHER_PAGES = [
    "oferta-targi.html",
    "oferta-konferencje.html",
    "oferta-dni-otwarte.html",
    "wypozyczenie-robota.html",
    "robot-na-impreze.html",
]
for filename in OTHER_PAGES:
    filepath = os.path.join(BASE, filename)
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    content = add_og_image_dims(content)
    content = add_footer_nap(content)
    content = fix_copyright(content)
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Updated: {filename}")
    else:
        print(f"  No change: {filename}")

# ─────────────────────────────────────────────
# 4. SITEMAP — add missing page + update lastmod
# ─────────────────────────────────────────────
print("\n=== sitemap.xml ===")
sitemap_path = os.path.join(BASE, "sitemap.xml")
with open(sitemap_path, 'r', encoding='utf-8') as f:
    sitemap = f.read()

# Add missing blog-atrakcje-eventowe.html
if 'blog-atrakcje-eventowe.html' not in sitemap:
    new_entry = f"""  <url>
    <loc>https://33bots.pl/blog-atrakcje-eventowe.html</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
</urlset>"""
    sitemap = sitemap.replace('</urlset>', new_entry)
    print("  Added: blog-atrakcje-eventowe.html")

# Update all lastmod dates to today
sitemap = re.sub(r'<lastmod>[\d-]+</lastmod>', f'<lastmod>{TODAY}</lastmod>', sitemap)

with open(sitemap_path, 'w', encoding='utf-8') as f:
    f.write(sitemap)
print("  Updated all lastmod dates")

print("\n✓ All done!")
