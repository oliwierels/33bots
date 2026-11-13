#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Strony okazji pisane od nowa (11.2026): tresci/okazje/<adres>.html → <adres>.html w katalogu głównym.

Źródło to nagłówek JSON w komentarzu i treść HTML. Rama (nawigacja, formularz, stopka, GTM)
jest w tresci/okazje/_rama.html i pochodzi 1:1 z dotychczasowych stron okazji, więc formularz,
identyfikatory i skrypty zostają bez zmian. Każda strona ma własną strukturę: plan godzinowy,
wymagania techniczne, cenę zgodną z cennikiem i ograniczenia — bez wspólnych bloków opinii.

Widoczna data aktualizacji i dateModified pochodzą z rejestru seo/lastmod/pl.json, czyli
zmieniają się tylko wtedy, gdy zmieniła się treść.

Użycie: python3 tresci/buduj_okazje.py
"""
import html
import json
import re
import sys
from datetime import date
from pathlib import Path

TU = Path(__file__).resolve().parent
REPO = TU.parent
sys.path.insert(0, str(REPO / 'seo'))
import lastmod  # noqa: E402

BAZA = 'https://33bots.pl/'
MIESIACE = ['stycznia', 'lutego', 'marca', 'kwietnia', 'maja', 'czerwca', 'lipca', 'sierpnia', 'września', 'października', 'listopada', 'grudnia']


def bez_tagow(s):
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s))).replace('\xa0', ' ').strip()


def data_slownie(iso):
    r, m, d = iso.split('-')
    return f'{int(d)} {MIESIACE[int(m) - 1]} {r}'


def ld(obiekt):
    return '  <script type="application/ld+json">\n' + json.dumps(obiekt, ensure_ascii=False, indent=2) + '\n  </script>\n'


def glowa(d, adres, data_zmiany):
    url = BAZA + adres
    opis = d['opis']
    assert len(opis) <= 160, f'{adres}: opis ma {len(opis)} znaków'
    hreflang = d.get('hreflang') or [['pl', url], ['x-default', url]]
    w = [f'  <title>{d["tytul"]}</title>',
         f'  <meta name="description" content="{html.escape(opis)}" />']
    if d.get('slowa_kluczowe'):
        w.append(f'  <meta name="keywords" content="{html.escape(d["slowa_kluczowe"])}" />')
    w += ['  <meta name="robots" content="index, follow" />',
          f'  <link rel="canonical" href="{url}" />']
    w += [f'  <link rel="alternate" hreflang="{j}" href="{h}" />' for j, h in hreflang]
    w += ['', '  <!-- Open Graph -->',
          '  <meta property="og:type" content="website" />',
          f'  <meta property="og:url" content="{url}" />',
          f'  <meta property="og:title" content="{d["tytul"]}" />',
          f'  <meta property="og:description" content="{html.escape(opis)}" />',
          f'  <meta property="og:image" content="{BAZA}{d["og"]["obraz"]}" />',
          '  <meta property="og:image:width" content="1200" />',
          '  <meta property="og:image:height" content="630" />',
          f'  <meta property="og:image:alt" content="{html.escape(d["og"]["alt"])}" />',
          '  <meta property="og:locale" content="pl_PL" />',
          '  <meta property="og:site_name" content="33bots" />', '',
          '  <!-- Twitter / X Card -->',
          '  <meta name="twitter:card" content="summary_large_image" />',
          f'  <meta name="twitter:title" content="{d["tytul"]}" />',
          f'  <meta name="twitter:description" content="{html.escape(opis)}" />', '',
          '  <meta name="theme-color" content="#000000" />', '']
    dostawca = {'@type': 'Organization', 'name': '33bots', 'url': BAZA, 'email': 'kontakt@33bots.pl', 'telephone': '+48 531 408 004'}
    u = d.get('usluga') or {'name': bez_tagow(d['h1'])}
    usluga = {'@context': 'https://schema.org', '@type': 'Service', 'name': u['name'], 'description': opis, 'url': url,
              'image': BAZA + u.get('image', 'robot-g1.jpg'), 'serviceType': 'Wynajem robota humanoidalnego na wydarzenia',
              'provider': dostawca, 'areaServed': {'@type': 'Country', 'name': 'Polska'},
              'offers': {'@type': 'AggregateOffer', 'priceCurrency': 'PLN', 'lowPrice': '5500', 'availability': 'https://schema.org/InStock', 'url': url + '#cena'}}
    strona = {'@context': 'https://schema.org', '@type': 'WebPage', 'url': url, 'name': bez_tagow(d['h1']), 'inLanguage': 'pl',
              'datePublished': d['opublikowano'], 'dateModified': data_zmiany,
              'publisher': {'@type': 'Organization', 'name': '33bots', 'url': BAZA}}
    okruszki = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Strona główna', 'item': BAZA},
        {'@type': 'ListItem', 'position': 2, 'name': d['okruch'], 'item': url}]}
    faq = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': bez_tagow(q), 'acceptedAnswer': {'@type': 'Answer', 'text': bez_tagow(a)}} for q, a in d['faq']]}
    bloki = [strona, okruszki, faq] if d.get('hub') else [usluga, strona, okruszki, faq]
    if d.get('wideo'):
        v = d['wideo']
        bloki.append({'@context': 'https://schema.org', '@type': 'VideoObject', 'name': v['name'], 'description': v['description'],
                      'thumbnailUrl': BAZA + v['poster'], 'contentUrl': BAZA + v['plik'], 'uploadDate': v['uploadDate'], 'duration': v['duration'],
                      'inLanguage': 'pl', 'publisher': {'@type': 'Organization', 'name': '33bots', 'url': BAZA.rstrip('/'),
                                                       'logo': {'@type': 'ImageObject', 'url': BAZA + 'logo.png'}}})
    return '\n'.join(w) + '\n' + '\n'.join(ld(b) for b in bloki)


def hero(d):
    return f'''  <section class="hero">
    <div class="hero__content">
      <p class="hero__eyebrow">{d["nadtytul"]}</p>
      <h1 class="hero__title">{d["h1"]}</h1>
      <p class="hero__sub">{d["lead"]}</p>
      <div class="hero__ctas">
        <a href="#kontakt" class="btn-primary">{d.get("cta", "Zapytaj o termin")}</a>
        <a href="{d["cta2"][0]}" class="btn-ghost">{d["cta2"][1]}</a>
      </div>
    </div>
  </section>
'''


def faq_html(d):
    w = [f'''  <section class="section faq-section" id="pytania">
    <div class="section-header">
      <span class="tag">Pytania</span>
      <h2 class="section-title">{d["faq_h2"]}</h2>
    </div>
    <div class="faq">''']
    for q, a in d['faq']:
        w.append(f'''      <div class="faq-item">
        <button class="faq-q" aria-expanded="false">
          <span>{q}</span>
          <span class="faq-q__icon" aria-hidden="true">+</span>
        </button>
        <div class="faq-a" hidden><p>{a}</p></div>
      </div>''')
    w.append('    </div>\n  </section>\n')
    return '\n'.join(w)


def zbuduj(zrodlo, rama, rejestr, dzis):
    s = zrodlo.read_text(encoding='utf-8')
    m = re.match(r'\s*<!--\s*(\{.*?\})\s*-->\s*', s, re.S)
    d = json.loads(m.group(1))
    tresc = s[m.end():]
    adres = zrodlo.name

    def zloz(data_zmiany):
        stopka_daty = (f'  <section class="section" style="padding-top:0;">\n    <div class="ok-wrap">\n'
                       f'      <p class="data-zmiany">Treść strony zaktualizowano {data_slownie(data_zmiany)}. Autor: zespół 33bots.</p>\n    </div>\n  </section>\n')
        srodek = hero(d) + '\n' + tresc.rstrip().replace('<section class="section"', '<section class="section ok-sekcja"') + '\n\n' + faq_html(d) + '\n' + stopka_daty
        return (rama.replace('{{GLOWA}}', glowa(d, adres, data_zmiany)).replace('{{OKRUCH}}', d['okruch'])
                .replace('{{TRESC}}', srodek).replace('{{KONTAKT_H2}}', d['kontakt_h2']).replace('{{KONTAKT_LEAD}}', d['kontakt_lead']))

    probna = zloz(dzis)
    stary = rejestr.get(adres)
    data_zmiany = stary['data'] if stary and stary['odcisk'] == lastmod.odcisk(probna) else dzis
    wynik = zloz(data_zmiany)
    assert '{{' not in wynik, re.findall(r'\{\{\w+\}\}', wynik)
    (REPO / adres).write_text(wynik, encoding='utf-8')
    slowa = len(bez_tagow(tresc).split()) + sum(len(bez_tagow(q + ' ' + a).split()) for q, a in d['faq'])
    print(f'  {adres} ({slowa} słów treści, data {data_zmiany})')


def main():
    rama = (TU / 'okazje' / '_rama.html').read_text(encoding='utf-8')
    rejestr = lastmod.wczytaj('pl')
    dzis = date.today().isoformat()
    for zrodlo in sorted((TU / 'okazje').glob('*.html')):
        if zrodlo.name.startswith('_'):
            continue
        zbuduj(zrodlo, rama, rejestr, dzis)


if __name__ == '__main__':
    main()
