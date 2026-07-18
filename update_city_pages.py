#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aktualizacja podstron miast (robot-wynajem-*.html):
1. Title / og:title / twitter:title — dodanie frazy „robot na event”
2. Sekcja „Robot na event w {mieście} — wybierz scenariusz” z linkami
   do podstron scenariuszowych (linkowanie krzyżowe miasta × scenariusze)
Skrypt jest idempotentny — można go uruchamiać wielokrotnie.
"""

import glob
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))

# slug -> (mianownik, miejscownik z przyimkiem)
CITIES = {
    "warszawa": ("Warszawa", "w Warszawie"), "krakow": ("Kraków", "w Krakowie"),
    "wroclaw": ("Wrocław", "we Wrocławiu"), "poznan": ("Poznań", "w Poznaniu"),
    "gdansk": ("Gdańsk", "w Gdańsku"), "katowice": ("Katowice", "w Katowicach"),
    "lodz": ("Łódź", "w Łodzi"), "szczecin": ("Szczecin", "w Szczecinie"),
    "bydgoszcz": ("Bydgoszcz", "w Bydgoszczy"), "lublin": ("Lublin", "w Lublinie"),
    "bialystok": ("Białystok", "w Białymstoku"), "rzeszow": ("Rzeszów", "w Rzeszowie"),
    "torun": ("Toruń", "w Toruniu"), "olsztyn": ("Olsztyn", "w Olsztynie"),
    "kielce": ("Kielce", "w Kielcach"), "opole": ("Opole", "w Opolu"),
    "gliwice": ("Gliwice", "w Gliwicach"), "czestochowa": ("Częstochowa", "w Częstochowie"),
    "radom": ("Radom", "w Radomiu"), "zielona-gora": ("Zielona Góra", "w Zielonej Górze"),
    "sosnowiec": ("Sosnowiec", "w Sosnowcu"), "plock": ("Płock", "w Płocku"),
    "elblag": ("Elbląg", "w Elblągu"), "walbrzych": ("Wałbrzych", "w Wałbrzychu"),
    "wloclawek": ("Włocławek", "we Włocławku"), "tarnow": ("Tarnów", "w Tarnowie"),
    "koszalin": ("Koszalin", "w Koszalinie"), "legnica": ("Legnica", "w Legnicy"),
    "kalisz": ("Kalisz", "w Kaliszu"), "grudziadz": ("Grudziądz", "w Grudziądzu"),
    "zabrze": ("Zabrze", "w Zabrzu"), "bytom": ("Bytom", "w Bytomiu"),
    "rybnik": ("Rybnik", "w Rybniku"), "tychy": ("Tychy", "w Tychach"),
    "dabrowa-gornicza": ("Dąbrowa Górnicza", "w Dąbrowie Górniczej"),
    "chorzow": ("Chorzów", "w Chorzowie"), "jaworzno": ("Jaworzno", "w Jaworznie"),
    "slupsk": ("Słupsk", "w Słupsku"), "nowy-sacz": ("Nowy Sącz", "w Nowym Sączu"),
    "pila": ("Piła", "w Pile"), "karpacz": ("Karpacz", "w Karpaczu"),
    "mikolajki": ("Mikołajki", "w Mikołajkach"),
}

SCENARIOS = [
    ("robot-na-targi.html", "Targi"),
    ("robot-na-konferencje.html", "Konferencja"),
    ("robot-na-gale.html", "Gala"),
    ("robot-na-impreze-firmowa.html", "Impreza firmowa"),
    ("robot-na-integracje-firmowa.html", "Integracja"),
    ("robot-na-piknik-firmowy.html", "Piknik firmowy"),
    ("robot-na-wesele.html", "Wesele"),
    ("robot-na-urodziny.html", "Urodziny"),
    ("robot-na-otwarcie.html", "Otwarcie"),
    ("robot-na-dni-miasta.html", "Dni miasta"),
    ("robot-na-targi-pracy.html", "Targi pracy"),
    ("robot-do-hotelu.html", "Hotel"),
    ("robot-do-galerii-handlowej.html", "Galeria handlowa"),
    ("atrakcje-na-event.html", "Wszystkie scenariusze"),
]

CHIP_STYLE = ('padding:0.35rem 0.8rem; border:1px solid var(--border); border-radius:999px; '
              'font-size:0.8rem; color:var(--text-2); text-decoration:none; transition:border-color 0.2s')

SECTION_TPL = """  <section class="section" style="padding-top:0;" id="scenariusze-miasto">
    <div class="container" style="max-width:1140px; margin-inline:auto; padding-inline:var(--s4)">
      <h2 style="font-size:clamp(1rem,2vw,1.4rem); font-weight:700; margin-bottom:var(--s2); color:var(--text-1)">Robot na event {loc} — wybierz scenariusz</h2>
      <p style="color:var(--text-2); font-size:0.9rem; margin-bottom:var(--s3);">Obsługujemy {loc} każdy typ wydarzenia — od targów i konferencji po imprezy prywatne. Zobacz, jak robot sprawdza się w konkretnym scenariuszu:</p>
      <div style="display:flex; flex-wrap:wrap; gap:0.5rem;">
{chips}
      </div>
    </div>
  </section>

"""


def main():
    updated_titles = 0
    added_sections = 0
    for fn in sorted(glob.glob(os.path.join(BASE, "robot-wynajem-*.html"))):
        slug = re.sub(r".*robot-wynajem-(.+)\.html$", r"\1", fn)
        if slug not in CITIES:
            print("POMINIĘTO (brak odmiany):", slug)
            continue
        nom, loc = CITIES[slug]
        s = open(fn, encoding="utf-8").read()
        orig = s

        # 1. Title: „— Unitree G1 | 33bots” -> „— robot na event | 33bots”
        old_t = f"Wynajem robota humanoidalnego {nom} — Unitree G1 | 33bots"
        new_t = f"Wynajem robota humanoidalnego {nom} — robot na event | 33bots"
        if old_t in s:
            s = s.replace(old_t, new_t)
            updated_titles += 1

        # 2. Sekcja scenariuszy przed FAQ
        if 'id="scenariusze-miasto"' not in s and '<section class="section faq-section">' in s:
            chips = "\n".join(
                f'        <a href="{href}" style="{CHIP_STYLE}">{label}</a>'
                for href, label in SCENARIOS
            )
            section = SECTION_TPL.format(loc=loc, chips=chips)
            s = s.replace('  <section class="section faq-section">',
                          section + '  <section class="section faq-section">', 1)
            added_sections += 1

        if s != orig:
            open(fn, "w", encoding="utf-8").write(s)
    print(f"Tytuły zaktualizowane: {updated_titles}, sekcje dodane: {added_sections}")


if __name__ == "__main__":
    main()
