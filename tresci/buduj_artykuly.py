# -*- coding: utf-8 -*-
"""Buduje artykuły poradnika z plików w tresci/artykuly/ do stron w katalogu głównym.

Każdy plik tresci/artykuly/<adres>.html zaczyna się komentarzem z danymi
(JSON), a dalej ma treść artykułu: nagłówki <h2 id="…">, akapity, listy,
tabele i zdjęcia. Skrypt dokleja do tego wspólny szablon — nagłówek strony,
menu i stopkę biorą się wprost z index.html, więc nie rozjadą się ze stroną
główną — i dane strukturalne (BlogPosting, BreadcrumbList, FAQPage).

Skróty w treści:
  <foto plik="realizacja-x" alt="…" podpis="…"/>          zdjęcie na szerokość tekstu
  <para podpis="…"><kadr plik="…" alt="…"/><kadr …/></para>   dwa zdjęcia obok siebie

Użycie (z katalogu głównego):  python3 tresci/buduj_artykuly.py
Uruchamia go też ./buduj.sh, przed oznaczeniem wersji arkuszy.
"""
import html
import json
import os
import re
import struct
from pathlib import Path

BAZA = 'https://33bots.pl'
KORZEN = Path(__file__).resolve().parent.parent
os.chdir(KORZEN)
INDEX = Path('index.html').read_text(encoding='utf-8')


def wycinek(od, do):
    i = INDEX.index(od)
    return INDEX[i:INDEX.index(do, i) + len(do)]


GTM_HEAD = wycinek('<!-- Google Tag Manager -->', '<!-- End Google Tag Manager -->')
GTM_BODY = wycinek('<!-- Google Tag Manager (noscript) -->', '<!-- End Google Tag Manager (noscript) -->')
STOPKA = wycinek('<footer class="stopka">', '</footer>')
COOKIES = wycinek('<!-- Baner cookie -->', '</div>')
ALBACROSS = wycinek('<!-- Albacross -->', '</script>\n<script async src="https://serve.albacross.com/track.js"></script>')
# Menu strony głównej prowadzi do kotwic — z podstrony te same linki idą na index.html.
NAV = wycinek('<header class="nav" id="nav">', '</header>')
NAV = NAV.replace('href="#top"', 'href="index.html"').replace('href="#', 'href="index.html#')


def wymiary(plik):
    """Szerokość i wysokość JPG z nagłówka pliku — bez zewnętrznych bibliotek."""
    with open(plik + '.jpg', 'rb') as f:
        dane = f.read()
    i = 2
    while i < len(dane):
        if dane[i] != 0xFF:
            i += 1
            continue
        znacznik = dane[i + 1]
        if znacznik in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h, w = struct.unpack('>HH', dane[i + 5:i + 9])
            return w, h
        dlugosc = struct.unpack('>H', dane[i + 2:i + 4])[0]
        i += 2 + dlugosc
    raise ValueError(f'{plik}.jpg: nie znaleziono wymiarów')


def zdjecie(plik, alt, sizes, ladowanie='lazy', priorytet=False):
    w, h = wymiary(plik)
    warianty = []
    if Path(f'{plik}-400.webp').exists():
        warianty.append(f'{plik}-400.webp 400w')
    if Path(f'{plik}.webp').exists():
        warianty.append(f'{plik}.webp {w}w')
    zrodlo = f'<source type="image/webp" srcset="{", ".join(warianty)}" sizes="{sizes}" />' if warianty else ''
    extra = ' fetchpriority="high"' if priorytet else ''
    return (f'<picture>{zrodlo}<img src="{plik}.jpg" alt="{html.escape(alt)}" width="{w}" height="{h}" '
            f'loading="{ladowanie}" decoding="async"{extra} /></picture>')


def bez_tagow(s):
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s))).strip()


def atrybuty(s):
    return dict(re.findall(r'(\w+)="([^"]*)"', s))


def zbuduj(plik_zrodla):
    surowe = plik_zrodla.read_text(encoding='utf-8')
    m = re.match(r'\s*<!--\s*(\{.*?\})\s*-->\s*', surowe, re.S)
    assert m, f'{plik_zrodla}: brak danych w komentarzu na początku pliku'
    d = json.loads(m.group(1))
    tresc = surowe[m.end():].strip()
    adres = plik_zrodla.stem + '.html'
    url = f'{BAZA}/{adres}'

    def foto(mf):
        a = atrybuty(mf.group(1))
        podpis = f'<figcaption class="podpis">{a["podpis"]}</figcaption>' if a.get('podpis') else ''
        return f'<figure>{zdjecie(a["plik"], a["alt"], "(max-width: 1023px) 100vw, 640px")}{podpis}</figure>'
    tresc = re.sub(r'<foto ([^>]*?)/?>', foto, tresc)

    def para(mp):
        kadry = [zdjecie(a['plik'], a['alt'], '(max-width: 1023px) 50vw, 320px')
                 for a in map(atrybuty, re.findall(r'<kadr ([^>]*?)/?>', mp.group(2)))]
        podpis = atrybuty(mp.group(1)).get('podpis')
        pp = f'<figcaption class="podpis">{podpis}</figcaption>' if podpis else ''
        return f'<figure><div class="foto-para">{"".join(kadry)}</div>{pp}</figure>'
    tresc = re.sub(r'<para([^>]*)>(.*?)</para>', para, tresc, flags=re.S)

    naglowki = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', tresc)
    pytania = d.get('pytania', [])
    slowa = len(bez_tagow(tresc).split()) + sum(len(bez_tagow(q + ' ' + a).split()) for q, a in pytania)
    minuty = max(1, round(slowa / 200))

    spis = '\n'.join(f'          <li><a href="#{i}">{t}</a></li>' for i, t in naglowki)
    faq_html = ''
    if pytania:
        elementy = '\n'.join(
            f'''          <div class="faq__item">
            <h3 class="faq__h"><button class="faq__q" type="button" id="faq-{n}-q" aria-expanded="false" aria-controls="faq-{n}" data-faq="{html.escape(bez_tagow(q))}">{q}<span class="faq__znak" aria-hidden="true"><span></span><span></span></span></button></h3>
            <div class="faq__a" id="faq-{n}" role="region" aria-labelledby="faq-{n}-q" hidden><p>{a}</p></div>
          </div>''' for n, (q, a) in enumerate(pytania, 1))
        faq_html = f'''
        <section class="art__faq" aria-labelledby="faq-h">
          <h2 class="h2" id="faq-h">Najczęstsze pytania</h2>
          <div class="faq">
{elementy}
          </div>
        </section>'''

    czytaj = '\n'.join(f'            <li><a href="{h}">{t}</a></li>' for h, t in d.get('czytaj', []))
    fg = d['foto']

    ld = [
        {
            '@context': 'https://schema.org', '@type': 'BlogPosting',
            'headline': bez_tagow(d['h1']), 'description': d['opis'],
            'image': f"{BAZA}/{fg['plik']}.jpg",
            'datePublished': d['data'], 'dateModified': d.get('zmiana', d['data']),
            'inLanguage': 'pl-PL', 'wordCount': slowa,
            'author': {'@type': 'Organization', 'name': '33bots', 'url': BAZA},
            'publisher': {'@type': 'Organization', 'name': '33bots', 'url': BAZA,
                          'logo': {'@type': 'ImageObject', 'url': f'{BAZA}/logo.png'}},
            'mainEntityOfPage': {'@type': 'WebPage', '@id': url},
        },
        {
            '@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Strona główna', 'item': f'{BAZA}/'},
                {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': f'{BAZA}/blog.html'},
                {'@type': 'ListItem', 'position': 3, 'name': d['okruch'], 'item': url},
            ],
        },
    ]
    if pytania:
        ld.append({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': bez_tagow(q), 'acceptedAnswer': {'@type': 'Answer', 'text': bez_tagow(a)}}
            for q, a in pytania]})
    ld_html = '\n'.join(f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False, indent=2)}\n</script>' for x in ld)

    data_pl = '.'.join(reversed(d['data'].split('-')))
    strona = f'''<!DOCTYPE html>
<html lang="pl">
<head>
{GTM_HEAD}
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{d['tytul']}</title>
<meta name="description" content="{html.escape(d['opis'])}" />
<link rel="canonical" href="{url}" />
<meta name="theme-color" content="#050505" />
<meta property="og:type" content="article" />
<meta property="og:url" content="{url}" />
<meta property="og:title" content="{html.escape(d['tytul'])}" />
<meta property="og:description" content="{html.escape(d['opis'])}" />
<meta property="og:image" content="{BAZA}/og-image.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:locale" content="pl_PL" />
<meta property="og:site_name" content="33bots" />
<meta property="article:published_time" content="{d['data']}" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="alternate" type="application/rss+xml" title="33bots — blog RSS" href="https://33bots.pl/feed.xml" />
<link rel="icon" type="image/svg+xml" href="favicon.svg" />
<link rel="preload" as="font" type="font/woff2" crossorigin href="fonts/space-grotesk-latin-wght-normal.woff2" />
<script>document.documentElement.classList.add('js');</script>
<link rel="stylesheet" href="css/site.css" />
{ld_html}
</head>
<body>
{GTM_BODY}

<!-- Wygenerowane przez tresci/buduj_artykuly.py z tresci/artykuly/{plik_zrodla.name} — zmiany wprowadzaj tam. -->
{NAV}

<main class="art">
  <article>
    <header class="art__glowa">
      <ol class="okruchy" aria-label="Okruszki">
        <li><a href="index.html">Strona główna</a></li><li aria-hidden="true">/</li>
        <li><a href="blog.html">Blog</a></li><li aria-hidden="true">/</li>
        <li aria-current="page">{d['okruch']}</li>
      </ol>
      <div class="art__tekst">
        <p class="label">{d['kategoria']}</p>
        <h1 class="art__h1">{d['h1']}</h1>
        <p class="art__lead">{d['lead']}</p>
        <p class="art__meta"><time datetime="{d['data']}">{data_pl}</time> · {minuty} min czytania · 33bots</p>
      </div>
      <figure class="art__foto">
        {zdjecie(fg['plik'], fg['alt'], '(max-width: 1023px) 100vw, 400px', ladowanie='eager', priorytet=True)}
        <figcaption class="podpis">{fg['podpis']}</figcaption>
      </figure>
    </header>

    <div class="art__tresc">
      <nav class="spis" aria-labelledby="spis-h">
        <p class="label" id="spis-h">W&nbsp;artykule</p>
        <ol>
{spis}
        </ol>
      </nav>

      <div class="prose">
{tresc}
{faq_html}

        <aside class="art__cta" aria-labelledby="cta-h">
          <h2 class="h2" id="cta-h">{d.get('cta_tytul', 'Sprawdź, czy Twój termin jest wolny')}</h2>
          <p class="body">{d.get('cta_tekst', 'Opisz wydarzenie w kilku zdaniach. Oddzwaniamy w ciągu 24 godzin roboczych, zwykle tego samego dnia, z konkretną kwotą i propozycją scenariusza.')}</p>
          <div class="art__cta-akcje">
            <a class="btn" href="index.html#kontakt" data-cta="artykul">Sprawdź dostępność terminu <span aria-hidden="true">→</span></a>
            <a class="link" href="tel:+48531408004" data-tel="artykul">+48 531 408 004</a>
            <a class="link" href="tel:+48601499947" data-tel="artykul">+48 601 499 947</a>
          </div>
        </aside>

        <nav class="czytaj" aria-labelledby="czytaj-h">
          <p class="label" id="czytaj-h">Czytaj dalej</p>
          <ul>
{czytaj}
          </ul>
        </nav>
      </div>
    </div>
  </article>
</main>

{STOPKA}

<div class="pasek" id="pasekMobilny">
  <a class="btn" href="index.html#kontakt" data-cta="sticky">Sprawdź termin <span aria-hidden="true">→</span></a>
</div>
<div class="pasek-odstep"></div>

{COOKIES}

<script src="js/strona.js" defer></script>
{ALBACROSS}
</body>
</html>
'''
    Path(adres).write_text(strona, encoding='utf-8')
    return adres, slowa


if __name__ == '__main__':
    for zrodlo in sorted(Path('tresci/artykuly').glob('*.html')):
        adres, slowa = zbuduj(zrodlo)
        print(f'  {adres} ({slowa} słów)')
