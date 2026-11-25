# -*- coding: utf-8 -*-
"""Najważniejsze podstrony .pl w układzie strony głównej.

Źródło strony: tresci/landing/strony/<adres>.html, czyli
    <!-- landing {"slajdy": [...]} -->     (opcjonalnie: zdjęcia hero tej strony)
    <main>…</main>                          treść strony
    <!-- stopka -->
    <footer class="stopka">…</footer>      stopka z linkami do wersji językowych tej strony

Strona w katalogu głównym = jej własny <head> (bez zmian, poza arkuszami stylów) + nawigacja
podstron + <main> ze źródła + stopka + pasek mobilny, baner cookie, szuflada realizacji
i skrypt strony głównej. Tytuł, opis, canonical, hreflang i dane strukturalne zostają
w <head> co do znaku. Formularz, baner cookie i szuflada są kopiowane ze strony głównej
przy każdym budowaniu, a js/landing.js to jej skrypt (ten sam formularz, ten sam adres
Formspree, te same zdarzenia pomiarowe), więc nic się nie rozjeżdża.

Użycie (z katalogu głównego):  python3 tresci/landing/buduj.py
Uruchamia go ./buduj.sh po przeniesieniu podstron na nową ramę.
"""
import json
import re
import sys
from pathlib import Path

KORZEN = Path(__file__).resolve().parents[2]
TU = Path(__file__).resolve().parent
sys.path.insert(0, str(KORZEN / 'tresci' / 'podstrony'))
from przeszczep import naglowek, PASEK  # noqa: E402  ta sama nawigacja i pasek co na podstronach

INDEX = (KORZEN / 'index.html').read_text(encoding='utf-8')


def wycinek(tekst, od, do):
    i = tekst.index(od)
    return tekst[i:tekst.index(do, i) + len(do)]


COOKIES = wycinek(INDEX, '<div class="cookies" id="cookies"', '</div>')
SZUFLADA = wycinek(INDEX, '<div class="szuflada-tlo"', '</aside>')
KONTAKT = wycinek(INDEX, '<section id="kontakt"', '</section>')
def bez_numeru(s):
    """„09 / 13 · Formaty” → „Formaty”: numeracja sekcji należy do strony głównej."""
    return re.sub(r'(<p class="label sec__meta">)\d\d / \d\d · ', r'\1', s)


# Skala i „Widziani w”, pasy zdjęć z realizacji, kalkulator ceny i proces — wprost ze strony głównej.
WSPOLNE = {
    'skala': wycinek(INDEX, '<section class="proof"', '</section>'),
    'pasy': wycinek(INDEX, '<div class="pasy wejscie" data-grupa="zdjecia">', '\n    </div>\n  </div>'),
    'formaty': bez_numeru(wycinek(INDEX, '<section id="formaty"', '</section>')),
    'proces': bez_numeru(wycinek(INDEX, '<section id="proces"', '</section>')),
}
# Kalkulator na stronie targów: od razu wariant „Targi” (dwa dni i więcej).
WSPOLNE['formaty-targi'] = (WSPOLNE['formaty']
                            .replace('name="kalk_format" value="dzien" checked', 'name="kalk_format" value="dzien"', 1)
                            .replace('name="kalk_format" value="dni" />', 'name="kalk_format" value="dni" checked />', 1))
assert WSPOLNE['formaty-targi'].count('checked') == 1 and 'value="dni" checked' in WSPOLNE['formaty-targi']
GTM_NOSCRIPT = ('<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-MR7R7CJ3"\n'
                'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n<!-- End Google Tag Manager (noscript) -->')
ALBACROSS = '<script>window._nQc="89159321";</script>\n<script async src="https://serve.albacross.com/track.js"></script>'


def skrypt_landing():
    """js/landing.js = skrypt strony głównej; zdjęcia w hero mogą być własne dla strony (window.SLAJDY)."""
    bloki = re.findall(r'<script>\n(\(\(\) => \{.*?)</script>', INDEX, re.S)
    kod = next(b for b in bloki if 'Formularz: krok 1' in b)
    assert 'const SLAJDY = [' in kod
    kod = kod.replace('const SLAJDY = [', 'const SLAJDY = (window.SLAJDY && window.SLAJDY.length) ? window.SLAJDY : [', 1)
    naglowek_pliku = ('/* Wygenerowane przez tresci/landing/buduj.py ze skryptu w index.html. Zmiany wprowadzaj tam.\n'
                      '   Podstrony w układzie strony głównej: hero, pasy realizacji, szuflada, FAQ, baner cookie,\n'
                      '   formularz rezerwacji (Formspree) i pomiar — ten sam kod co na stronie głównej. */\n')
    (KORZEN / 'js' / 'landing.js').write_text(naglowek_pliku + kod, encoding='utf-8')


def kontakt(h2_html, miejsce, zasieg=None):
    """Rezerwacja ze strony głównej, z nagłówkiem tej podstrony (H2 strony zostaje bez zmian)."""
    s = KONTAKT
    s = re.sub(r'<h2 id="kontakt-h" class="h2">.*?</h2>', f'<h2 id="kontakt-h" class="h2">{h2_html}</h2>', s, count=1, flags=re.S)
    s = re.sub(r'<p class="label sec__meta">[^<]*</p>', '<p class="label sec__meta">Rezerwacja</p>', s, count=1)
    if zasieg:
        stare = 'Rezerwacja bez zaliczki, cała Polska.'
        assert stare in s
        s = s.replace(stare, f'Rezerwacja bez zaliczki. Zasięg: {zasieg}, a poza nim cała Polska.', 1)
    if miejsce:
        s = s.replace('placeholder="np. Warszawa, EXPO XXI"', f'placeholder="np. {miejsce}"', 1)
    return s


def arkusze(glowa):
    """Bez warstwy starych podstron; po site.css arkusz strony głównej i landing.css."""
    glowa = re.sub(r'\s*<link rel="stylesheet" href="css/podstrony\.css[^"]*"\s*/?>', '', glowa)
    # Wbudowane style starego szablonu (np. hero w jednej kolumnie) — wygląd, nie treść.
    glowa = re.sub(r'\s*<style>.*?</style>', '', glowa, flags=re.S)
    glowa = re.sub(r'\s*<link rel="stylesheet" href="css/(glowna|landing)\.css[^"]*"\s*/?>', '', glowa)
    m = re.search(r'<link rel="stylesheet" href="css/site\.css[^"]*"\s*/?>', glowa)
    assert m, 'brak css/site.css w <head>'
    return glowa[:m.end()] + '\n  <link rel="stylesheet" href="css/glowna.css" />\n  <link rel="stylesheet" href="css/landing.css" />' + glowa[m.end():]


def zbuduj(zrodlo):
    adres = zrodlo.name
    cel = KORZEN / adres
    t = zrodlo.read_text(encoding='utf-8')
    meta = {}
    m = re.match(r'\s*<!-- landing (\{.*?\}) -->', t, re.S)
    if m:
        meta = json.loads(m.group(1))
    main = re.search(r'<main>.*?</main>', t, re.S).group(0)
    stopka = re.search(r'<footer class="stopka">.*?</footer>', t, re.S).group(0)
    stara = cel.read_text(encoding='utf-8')
    glowa, sep, _ = stara.partition('</head>')
    assert sep, f'{adres}: brak </head>'
    glowa = arkusze(glowa)
    # Sekcje wspólne ze stroną główną: <!-- wspolne:nazwa --> w źródle.
    for nazwa, blok in WSPOLNE.items():
        main = main.replace(f'<!-- wspolne:{nazwa} -->', blok)
    # Rezerwacja: <!-- rezerwacja --> w źródle zastępuje sekcja ze strony głównej.
    if '<!-- rezerwacja -->' in main:
        main = main.replace('<!-- rezerwacja -->', kontakt(meta['kontakt_h2'], meta.get('miejsce'), meta.get('zasieg')), 1)
    slajdy = ''
    if meta.get('slajdy'):
        slajdy = '<script>window.SLAJDY = ' + json.dumps(meta['slajdy'], ensure_ascii=False) + ';</script>\n'
    strona = (glowa + sep + '\n<body class="landing">\n' + GTM_NOSCRIPT + '\n\n' + naglowek(adres, '#kontakt') + '\n\n'
              + main + '\n\n' + stopka + '\n\n' + PASEK.format(kontakt='#kontakt') + '\n\n' + COOKIES + '\n\n' + SZUFLADA + '\n\n'
              + slajdy + '<script src="js/landing.js" defer></script>\n<script src="js/glowna.js" defer></script>\n'
              + ALBACROSS + '\n</body>\n</html>\n')
    if strona != stara:
        cel.write_text(strona, encoding='utf-8')
        return True
    return False


if __name__ == '__main__':
    skrypt_landing()
    zrodla = sorted((TU / 'strony').glob('*.html'))
    n = sum(zbuduj(z) for z in zrodla)
    print(f'  strony w układzie strony głównej: {len(zrodla)} (zmienione: {n})')
