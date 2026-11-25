# -*- coding: utf-8 -*-
"""Stare podstrony (style.css) → rama nowego systemu wizualnego (css/site.css).

Zmienia wyłącznie ramę strony: arkusz stylów, nagłówek z menu, stopkę i pasek mobilny,
oraz dopisuje pod przyciskiem w hero obietnicę i telefon (element .hero__kontakt, który
rejestr lastmod pomija jak każdy blok kontaktowy). Nie rusza <head> poza arkuszem,
ani treści <main>: tytuł, opis, canonical, hreflang, dane strukturalne, H1–H6, tekst,
obrazy i linki w treści zostają co do znaku.

Każdy link, który był w starym nagłówku, menu mobilnym albo stopce, jest w nowej ramie
(jeśli nie ma go w nagłówku ani stopce strony głównej, trafia do kolumny „Więcej” w stopce).
Skrypt jest idempotentny: strona już przeniesiona nie ma style.css i jest pomijana.

Użycie (z katalogu głównego):  python3 tresci/podstrony/przeszczep.py
Uruchamia go ./buduj.sh po złożeniu artykułów i okazji.
"""
import re
from pathlib import Path

KORZEN = Path(__file__).resolve().parents[2]
TU = Path(__file__).resolve().parent
INDEX = (KORZEN / 'index.html').read_text(encoding='utf-8')


def wycinek(tekst, od, do):
    i = tekst.index(od)
    return tekst[i:tekst.index(do, i) + len(do)]


STOPKA_GLOWNA = wycinek(INDEX, '<footer class="stopka">', '</footer>')

MENU = [('oferta-targi.html', 'Targi'), ('oferta-konferencje.html', 'Konferencje i gale'),
        ('roboty-na-eventy-firmowe.html', 'Eventy firmowe'), ('realizacje-wideo.html', 'Realizacje'),
        ('blog.html', 'Blog')]
PANEL = [('oferta-targi.html', 'Targi'), ('oferta-konferencje.html', 'Konferencje i gale'),
         ('oferta-dni-otwarte.html', 'Dni otwarte i showroomy'), ('roboty-na-eventy-firmowe.html', 'Eventy firmowe'),
         ('atrakcje-na-event.html', 'Wszystkie atrakcje'), ('realizacje-wideo.html', 'Realizacje'),
         ('blog.html', 'Blog'), ('wdrozenia.html', 'Zakup i wdrożenia')]


def biezaca(href, adres):
    return ' aria-current="page"' if href == adres else ''


def naglowek(adres, kontakt):
    menu = '\n'.join(f'      <a href="{h}"{biezaca(h, adres)}>{n}</a>' for h, n in MENU)
    panel = '\n'.join(f'      <li><a href="{h}"{biezaca(h, adres)}>{n}</a></li>' for h, n in PANEL)
    return f'''<header class="nav" id="nav">
  <div class="nav__in">
    <a class="nav__logo" href="index.html" aria-label="33bots – strona główna">33BOTS</a>
    <nav class="nav__menu" aria-label="Główna">
{menu}
      <a class="nav__drugi" href="wdrozenia.html"{biezaca('wdrozenia.html', adres)}>Zakup i wdrożenia</a>
    </nav>
    <div class="nav__akcje">
      <a class="nav__tel" href="tel:+48531408004" data-tel="nav">+48 531 408 004</a>
      <a class="link nav__cta link--akcja" href="{kontakt}" data-cta="nav">Sprawdź termin</a>
      <button class="nav__przycisk" id="navPrzycisk" type="button" aria-expanded="false" aria-controls="navPanel">Menu</button>
    </div>
  </div>
  <div class="nav__panel" id="navPanel" hidden>
    <ul>
{panel}
    </ul>
    <a class="nav__tel" href="tel:+48531408004" data-tel="menu">+48 531 408 004</a>
    <a class="btn btn--akcja" href="{kontakt}" data-cta="nav">Sprawdź termin i cenę <span aria-hidden="true">→</span></a>
  </div>
</header>'''


def linki(fragment):
    """Adresy linków bez kotwic: dla wyszukiwarki index.html#o-nas to ten sam adres co index.html."""
    wynik = []
    for h in re.findall(r'<a\b[^>]*?href="([^"]+)"', fragment):
        h = h.split('#')[0]
        if h and h not in wynik:
            wynik.append(h)
    return wynik


def etykiety(fragment):
    return {h.split('#')[0]: re.sub(r'<[^>]+>|\s+', ' ', t).strip()
            for h, t in re.findall(r'<a\b[^>]*?href="([^"]+)"[^>]*>(.*?)</a>', fragment, re.S)}


def stopka(stara, adres, nag):
    """Stopka strony głównej + odnośniki do odpowiedników tej strony w innych językach + brakujące linki."""
    s = STOPKA_GLOWNA
    jezyki = re.search(r'<p class="footer__tagline" data-jezyki>(.*?)</p>', stara, re.S)
    if jezyki:
        wlasne = re.sub(r' style="[^"]*"', '', jezyki.group(1))
        # Odpowiedniki tej strony: krótkie etykiety, żeby nie powtarzać linii z domenami poniżej.
        wlasne = re.sub(r'>([^<–]+) – 33bots\.(lt|de|at)</a>', lambda m: '>' + {'lt': 'Lietuviškai', 'de': 'Deutsch', 'at': 'Österreich'}[m.group(2)] + '</a>', wlasne)
        wlasne = 'Ta strona w innych językach: ' + wlasne
        domeny = re.search(r'<p data-jezyki>(.*?)</p>', s, re.S).group(1)
        s = s.replace(f'<p data-jezyki>{domeny}</p>', f'<p data-jezyki>{wlasne}</p>\n      <p>{domeny}</p>', 1)
    jest = set(linki(s)) | set(linki(nag))
    opisy = etykiety(stara)
    brak = [h for h in linki(stara) if h not in jest and not h.startswith(('tel:', 'mailto:'))]
    if brak:
        pozycje = '\n'.join(f'      <li><a href="{h}">{(opisy.get(h) or h).lstrip("↗ ")}</a></li>' for h in brak)
        s = s.replace('    <ul class="stopka__kol" aria-label="Dokumenty">',
                      f'    <ul class="stopka__kol" aria-label="Więcej">\n{pozycje}\n    </ul>\n    <ul class="stopka__kol" aria-label="Dokumenty">', 1)
    return s


PASEK = '''<div class="pasek" id="pasekMobilny">
  <a class="btn btn--akcja" href="{kontakt}" data-cta="sticky">Sprawdź termin <span aria-hidden="true">→</span></a>
  <a class="pasek__tel" href="tel:+48531408004" data-tel="sticky" aria-label="Zadzwoń: +48 531 408 004">Zadzwoń</a>
</div>
<div class="pasek-odstep"></div>'''

OBIETNICA = ('<p class="hero__kontakt"><b>Bez zaliczki, płacisz po wydarzeniu.</b> Odpowiadamy zwykle w ciągu 30 minut. '
             'Wolisz zadzwonić? <a href="tel:+48531408004" data-tel="hero">+48 531 408 004</a></p>')


def przenies(sciezka):
    t = sciezka.read_text(encoding='utf-8')
    if 'href="style.css' not in t:
        return False
    adres = sciezka.name
    kontakt = '#kontakt' if 'id="kontakt"' in t else 'index.html#kontakt'
    stary_nag = re.search(r'<header class="nav" id="nav">.*?</header>', t, re.S)
    stare_menu = re.search(r'\s*<div class="mobile-menu" id="mobileMenu">.*?</div>', t, re.S)
    stara_stopka = re.search(r'<footer class="footer">.*?</footer>', t, re.S)
    assert stary_nag, f'{adres}: brak nagłówka w znanym formacie'
    stare_linki = (stary_nag.group(0) + (stare_menu.group(0) if stare_menu else '') + (stara_stopka.group(0) if stara_stopka else ''))

    nag = naglowek(adres, kontakt)
    t = t.replace(stary_nag.group(0), nag, 1)
    if stare_menu:
        assert '<div' not in stare_menu.group(0)[stare_menu.group(0).index('<div') + 4:], f'{adres}: zagnieżdżony div w menu mobilnym'
        t = t.replace(stare_menu.group(0), '', 1)
    if stara_stopka:
        t = t.replace(stara_stopka.group(0), stopka(stare_linki, adres, nag) + '\n\n' + PASEK.format(kontakt=kontakt), 1)
    t = re.sub(r'\s*<!-- STICKY CTA \(mobile\) -->\s*<div class="sticky-cta">.*?</div>', '', t, count=1, flags=re.S)

    # Arkusze: nowy system + warstwa podstron zamiast style.css.
    t = re.sub(r'<link rel="stylesheet" href="style\.css[^"]*"\s*/?>',
               '<link rel="preload" as="font" type="font/woff2" crossorigin href="fonts/space-grotesk-latin-wght-normal.woff2" />\n'
               '  <script>document.documentElement.classList.add(\'js\');</script>\n'
               '  <link rel="stylesheet" href="css/site.css" />\n'
               '  <link rel="stylesheet" href="css/podstrony.css" />', t, count=1)
    t = re.sub(r'<body(\s[^>]*)?>', lambda m: '<body class="podstrona">' if not m.group(1) else
               ('<body' + (re.sub(r'class="', 'class="podstrona ', m.group(1)) if 'class="' in m.group(1)
                           else m.group(1) + ' class="podstrona"') + '>'), t, count=1)

    # Obietnica i telefon pod przyciskiem w hero (tylko tam, gdzie hero ma przycisk).
    if 'hero__kontakt' not in t:
        t = re.sub(r'(<div class="hero__ctas">.*?</div>)', lambda m: m.group(1) + '\n      ' + OBIETNICA, t, count=1, flags=re.S)

    # Skrypt ramy (menu, pasek mobilny) obok main.js, który dalej obsługuje formularz, FAQ i baner.
    if 'js/strona.js' not in t:
        t = re.sub(r'(\s*)(<script src="main\.js[^"]*"></script>)', r'\1<script src="js/strona.js" defer></script>\1\2', t, count=1)

    # Kontrola: wszystkie linki starej ramy są w nowej stronie.
    nowe = set(linki(t))
    zgubione = [h for h in linki(stare_linki) if h not in nowe]
    assert not zgubione, f'{adres}: zgubione linki {zgubione}'
    sciezka.write_text(t, encoding='utf-8')
    return True


def arkusz():
    (KORZEN / 'css' / 'podstrony.css').write_text(
        '/* Wygenerowane przez tresci/podstrony/przeszczep.py z tresc-stara.css i nowy-wyglad.css. Zmiany wprowadzaj tam. */\n'
        + (TU / 'tresc-stara.css').read_text(encoding='utf-8') + '\n'
        + (TU / 'nowy-wyglad.css').read_text(encoding='utf-8'), encoding='utf-8')


if __name__ == '__main__':
    arkusz()
    n = sum(przenies(p) for p in sorted(KORZEN.glob('*.html')))
    print(f'  przeniesione na nową ramę: {n}')
