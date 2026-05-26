#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final SEO & accessibility fixes:
  1. Fix blog title years 2025 → 2026 (blog-atrakcje-eventowe, blog-wypozyczenie-robota-przewodnik)
  2. Add city internal-links section to all blog pages
  3. Add GTM preconnect to all HTML pages
  4. Add <main> landmark to all pages
  5. Fix hamburger aria-label on index.html
  6. Add aria-label to FAQ buttons
"""

import os
import re
import glob

BASE = "/home/user/33bots"

# ─────────────────────────────────────────────
# CITY LINKS SNIPPET (top 10 cities)
# ─────────────────────────────────────────────
CITY_LINKS_SECTION = """
  <section class="section" style="padding-block:var(--s6) var(--s4); background:var(--surface-1)">
    <div class="container" style="max-width:1140px; margin-inline:auto; padding-inline:var(--s4)">
      <h2 style="font-size:clamp(1rem,2vw,1.4rem); font-weight:700; margin-bottom:var(--s3); color:var(--text-1)">Wynajem robota w Twoim mieście</h2>
      <div style="display:flex; flex-wrap:wrap; gap:0.5rem;">
        <a href="robot-wynajem-warszawa.html" style="padding:0.35rem 0.8rem; border:1px solid var(--border); border-radius:999px; font-size:0.8rem; color:var(--text-2); text-decoration:none; transition:border-color 0.2s">Warszawa</a>
        <a href="robot-wynajem-krakow.html" style="padding:0.35rem 0.8rem; border:1px solid var(--border); border-radius:999px; font-size:0.8rem; color:var(--text-2); text-decoration:none; transition:border-color 0.2s">Kraków</a>
        <a href="robot-wynajem-wroclaw.html" style="padding:0.35rem 0.8rem; border:1px solid var(--border); border-radius:999px; font-size:0.8rem; color:var(--text-2); text-decoration:none; transition:border-color 0.2s">Wrocław</a>
        <a href="robot-wynajem-poznan.html" style="padding:0.35rem 0.8rem; border:1px solid var(--border); border-radius:999px; font-size:0.8rem; color:var(--text-2); text-decoration:none; transition:border-color 0.2s">Poznań</a>
        <a href="robot-wynajem-gdansk.html" style="padding:0.35rem 0.8rem; border:1px solid var(--border); border-radius:999px; font-size:0.8rem; color:var(--text-2); text-decoration:none; transition:border-color 0.2s">Gdańsk</a>
        <a href="robot-wynajem-katowice.html" style="padding:0.35rem 0.8rem; border:1px solid var(--border); border-radius:999px; font-size:0.8rem; color:var(--text-2); text-decoration:none; transition:border-color 0.2s">Katowice</a>
        <a href="robot-wynajem-lodz.html" style="padding:0.35rem 0.8rem; border:1px solid var(--border); border-radius:999px; font-size:0.8rem; color:var(--text-2); text-decoration:none; transition:border-color 0.2s">Łódź</a>
        <a href="robot-wynajem-szczecin.html" style="padding:0.35rem 0.8rem; border:1px solid var(--border); border-radius:999px; font-size:0.8rem; color:var(--text-2); text-decoration:none; transition:border-color 0.2s">Szczecin</a>
        <a href="robot-wynajem-lublin.html" style="padding:0.35rem 0.8rem; border:1px solid var(--border); border-radius:999px; font-size:0.8rem; color:var(--text-2); text-decoration:none; transition:border-color 0.2s">Lublin</a>
        <a href="robot-wynajem-rzeszow.html" style="padding:0.35rem 0.8rem; border:1px solid var(--border); border-radius:999px; font-size:0.8rem; color:var(--text-2); text-decoration:none; transition:border-color 0.2s">Rzeszów</a>
      </div>
    </div>
  </section>

  <!-- FOOTER -->"""

GTM_PRECONNECT = '  <link rel="preconnect" href="https://www.googletagmanager.com" />\n'
FONTS_PRECONNECT = '  <link rel="preconnect" href="https://fonts.googleapis.com" />'

html_files = sorted(glob.glob(os.path.join(BASE, "*.html")))
updated = 0

for filepath in html_files:
    filename = os.path.basename(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    original = content

    # ── 1. Fix blog title years (only 2 specific files) ──────────────────
    if filename == "blog-atrakcje-eventowe.html":
        # Title/meta/og/twitter/schema headline — replace year but NOT in datePublished/Published_time
        content = re.sub(
            r'((?:content|title)="[^"]*?)(\b2025\b)([^"]*?(?:event|atrakcj)[^"]*?")',
            r'\g<1>2026\g<3>',
            content,
        )
        # h1 and h2 headings with 2025
        content = re.sub(r'(<h[12][^>]*>.*?)(\b2025\b)(.*?</h[12]>)', r'\g<1>2026\g<3>', content, flags=re.DOTALL)

    if filename == "blog-wypozyczenie-robota-przewodnik.html":
        content = re.sub(
            r'((?:content|title)="[^"]*?(?:przewodnik|Przewodnik)[^"]*?)(\b2025\b)([^"]*?")',
            r'\g<1>2026\g<3>',
            content,
        )
        content = re.sub(r'(<h[12][^>]*>.*?)(\b2025\b)(.*?</h[12]>)', r'\g<1>2026\g<3>', content, flags=re.DOTALL)

    # ── 2. Add city links to blog pages ───────────────────────────────────
    if filename.startswith("blog-") and "robot-wynajem-warszawa.html" not in content:
        content = content.replace("  <!-- FOOTER -->", CITY_LINKS_SECTION, 1)

    # ── 3. GTM preconnect ─────────────────────────────────────────────────
    if "googletagmanager.com" in content and "preconnect" not in content.split("googletagmanager")[0][-200:]:
        if FONTS_PRECONNECT in content:
            content = content.replace(FONTS_PRECONNECT, GTM_PRECONNECT + FONTS_PRECONNECT, 1)

    # ── 4. <main> landmark ────────────────────────────────────────────────
    if "<main" not in content and "</header>" in content:
        content = content.replace("</header>", "</header>\n  <main>", 1)
        # Close before footer
        content = re.sub(r'(\n  <footer\b)', r'\n  </main>\1', content, count=1)

    # ── 5. aria-label on hamburger (index.html only) ──────────────────────
    if filename == "index.html":
        content = content.replace(
            '<button class="hamburger" id="hamburger">',
            '<button class="hamburger" id="hamburger" aria-label="Otwórz menu" aria-expanded="false">',
            1,
        )

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        updated += 1
        print(f"  Updated: {filename}")

print(f"\n✓ {updated} files updated")
