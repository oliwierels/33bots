# -*- coding: utf-8 -*-
"""Podstrony 33bots.de, 33bots.at i 33bots.lt w nowym systemie wizualnym — tym samym co strona główna
rynku i artykuły poradnika na 33bots.pl (css/site.css).

Każdy plik tresci/zagranica/podstrony/<rynek>/<adres>.html zaczyna się komentarzem z danymi
(JSON), a dalej ma treść strony: nagłówki <h2 id="…">, akapity, listy, tabele i zdjęcia.
Nawigacja, stopka, panel dostępności (.de), baner cookie, GTM i Albacross (.at) biorą się wprost
ze strony głównej rynku, więc podstrona nie rozjedzie się z nią wyglądem ani zachowaniem.

Skróty w treści (jak w artykułach .pl):
  <foto plik="realizacja-x" alt="…" podpis="…"/>              zdjęcie na szerokość tekstu
  <para podpis="…"><kadr plik="…" alt="…"/><kadr …/></para>   dwa zdjęcia obok siebie
  <wideo/>                                                     film z danych „wideo” w nagłówku
  <wideo plik="video/x"/>                                      jeden z kilku filmów z danych „filmy”

Opcjonalnie w danych: „rodzic” [adres, nazwa] — strona nadrzędna w okruszkach (np. Blog).

Adres, tytuł, opis, hreflang, obraz og i dane strukturalne usługi przechodzą z dotychczasowej
wersji strony bez zmian — zmienia się wygląd, nie to, co widzi wyszukiwarka.

Użycie (z katalogu głównego 33bots):
    python3 tresci/zagranica/buduj_podstrony.py de|at|lt <katalog repozytorium rynku>
"""
import hashlib
import html
import json
import re
import struct
import sys
from pathlib import Path

import bez_komentarzy

PL = Path(__file__).resolve().parents[2]
ZRODLA = Path(__file__).resolve().parent / 'podstrony'
# Po tym znaczniku podstrony.py rozpoznaje strony z tego generatora i ich nie przerabia.
ZNACZNIK = 'Erzeugt von tresci/zagranica/buduj_podstrony.py'

RYNKI = {
    'de': {
        'baza': 'https://33bots.de', 'lang': 'de', 'og_locale': 'de_DE', 'kraj': 'Deutschland',
        'analityka': False, 'dostepnosc': True,
        'kontakt': [('mailto:kontakt@33bots.de', 'kontakt@33bots.de', 'data-mail')],
    },
    'at': {
        'baza': 'https://33bots.at', 'lang': 'de-AT', 'og_locale': 'de_AT', 'kraj': 'Österreich', 'geo': 'AT',
        'analityka': True, 'dostepnosc': False,
        'kontakt': [('tel:+48531408004', '+48 531 408 004', 'data-tel'),
                    ('mailto:kontakt@33bots.at', 'kontakt@33bots.at', 'data-mail')],
    },
    'lt': {
        'baza': 'https://33bots.lt', 'lang': 'lt', 'og_locale': 'lt_LT', 'kraj': 'Lietuva',
        'analityka': True, 'dostepnosc': False,
        'kontakt': [('mailto:kontakt@33bots.lt', 'kontakt@33bots.lt', 'data-mail')],
    },
}
TEKSTY_DE = {
    'start': 'Startseite', 'okruchy': 'Brotkrumen', 'skip': 'Zum Hauptinhalt springen',
    'spis': 'Auf dieser Seite', 'faq': 'Häufige Fragen', 'czytaj': 'Weiterlesen',
    'cta_tytul': 'Prüfen Sie, ob Ihr Termin frei ist',
    'cta_tekst': 'Beschreiben Sie Ihre Veranstaltung in ein paar Sätzen. Sie erhalten das Angebot innerhalb von 24 Werkstunden.',
    'cta_przycisk': 'Verfügbarkeit prüfen', 'pasek': 'Termin prüfen',
    'menu': ("'Schließen' : 'Menü'"),
    'rss_opis': 'Wissen über humanoide Roboter auf Veranstaltungen, Messen und Konferenzen.', 'rss_jezyk': 'de-DE',
}
TEKSTY_LT = {
    'start': 'Pradžia', 'okruchy': 'Naršymo kelias', 'skip': 'Pereiti prie turinio',
    'spis': 'Šiame puslapyje', 'faq': 'Dažniausi klausimai', 'czytaj': 'Skaitykite toliau',
    'cta_tytul': 'Patikrinkite, ar jūsų data laisva',
    'cta_tekst': 'Keliais sakiniais aprašykite savo renginį. Pasiūlymą atsiųsime per 24 darbo valandas.',
    'cta_przycisk': 'Patikrinti datą', 'pasek': 'Patikrinti datą',
    'menu': ("'Uždaryti' : 'Meniu'"),
    'rss_opis': 'Renginių gidas: pramogos, vedėjai, idėjos ir humanoidinis robotas renginyje.', 'rss_jezyk': 'lt-LT',
}
RYNKI['de']['teksty'] = RYNKI['at']['teksty'] = TEKSTY_DE
RYNKI['lt']['teksty'] = TEKSTY_LT


# Długie złożenia w nagłówkach dzielimy miękko (&shy;), żeby na telefonach 320 px nie wychodziły
# poza ekran; słowa z łącznikiem łamią się same. Podział według członów złożenia.
DZIELENIE = {
    'Verbraucherstreitbeilegung': 'Verbraucher&shy;streit&shy;beilegung', 'Haftpflichtversicherung': 'Haftpflicht&shy;versicherung',
    'Durchsetzungsverfahren': 'Durchsetzungs&shy;verfahren', 'Hochschulveranstaltung': 'Hochschul&shy;veranstaltung',
    'Unternehmensgegenstand': 'Unternehmens&shy;gegenstand', 'Kinderveranstaltungen': 'Kinder&shy;veranstaltungen',
    'Datenschutzerklärung': 'Datenschutz&shy;erklärung', 'Attraktionslieferant': 'Attraktions&shy;lieferant',
    'Kulturveranstaltung': 'Kultur&shy;veranstaltung', 'Eröffnungszeremonie': 'Eröffnungs&shy;zeremonie',
    'Interaktionsbereich': 'Interaktions&shy;bereich', 'Technologiestandort': 'Technologie&shy;standort',
    'Weihnachtsplaylist': 'Weihnachts&shy;playlist', 'Agenturkonditionen': 'Agentur&shy;konditionen',
    'Reichweitenmessung': 'Reichweiten&shy;messung', 'Veranstaltungstag': 'Veranstaltungs&shy;tag',
    'Energiewirtschaft': 'Energie&shy;wirtschaft', 'Produktionsbudget': 'Produktions&shy;budget',
    'Konferenzprogramm': 'Konferenz&shy;programm', 'Sicherheitsfragen': 'Sicherheits&shy;fragen',
    'Markenbotschafter': 'Marken&shy;botschafter', 'Forschungsbranche': 'Forschungs&shy;branche',
    'Unternehmensdaten': 'Unternehmens&shy;daten', 'Tanzchoreografie': 'Tanz&shy;choreografie',
    'Verantwortlicher': 'Verantwort&shy;licher', 'Geschäftsführung': 'Geschäfts&shy;führung',
    'Barrierefreiheit': 'Barriere&shy;freiheit', 'Tagesnachrichten': 'Tages&shy;nachrichten',
    'Niederösterreich': 'Nieder&shy;österreich', 'Unternehmensgruppe': 'Unternehmens&shy;gruppe',
    'Wissenschaftszentrum': 'Wissenschafts&shy;zentrum', 'Gefechtsfeldmedizin': 'Gefechtsfeld&shy;medizin',
}


def podziel(t):
    for slowo, z_podzialem in DZIELENIE.items():
        t = re.sub(rf'\b{slowo}\b', z_podzialem, t)
    return t


def wycinek(tekst, od, do):
    i = tekst.index(od)
    return tekst[i:tekst.index(do, i) + len(do)]


def na_strone_glowna(fragment):
    """Kotwice strony głównej (#referenzen…) z podstrony prowadzą na stronę główną."""
    fragment = fragment.replace('href="#top"', 'href="index.html"')
    return re.sub(r'href="#([^"]+)"', r'href="index.html#\1"', fragment)


def wymiary(plik):
    """Szerokość i wysokość JPG z nagłówka pliku — bez zewnętrznych bibliotek."""
    dane = plik.read_bytes()
    i = 2
    while i < len(dane):
        if dane[i] != 0xFF:
            i += 1
            continue
        znacznik = dane[i + 1]
        if znacznik in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h, w = struct.unpack('>HH', dane[i + 5:i + 9])
            return w, h
        i += 2 + struct.unpack('>H', dane[i + 2:i + 4])[0]
    raise ValueError(f'{plik}: nie znaleziono wymiarów')


def bez_tagow(s):
    t = html.unescape(re.sub(r'<[^>]+>', ' ', s)).replace('\xa0', ' ')
    return re.sub(r'\s+', ' ', t).strip()


def atrybuty(s):
    return dict(re.findall(r'(\w+)="([^"]*)"', s))


def md5(plik):
    return hashlib.md5(plik.read_bytes()).hexdigest()[:8]


class Rynek:
    def __init__(self, kod, cel):
        self.kod, self.cel, self.k = kod, Path(cel), RYNKI[kod]
        glowna = (self.cel / 'index.html').read_text(encoding='utf-8')
        self.nav = na_strone_glowna(wycinek(glowna, '<header class="nav" id="nav">', '</header>'))
        self.stopka = na_strone_glowna(wycinek(glowna, '<footer class="stopka">', '</footer>'))
        self.css = re.search(r'<link rel="stylesheet" href="(css/site\.css\?v=[0-9a-f]+)" />', glowna).group(1)
        if self.k['analityka']:
            self.gtm_head = wycinek(glowna, '<!-- Google Tag Manager -->', '<!-- End Google Tag Manager -->')
            self.gtm_body = wycinek(glowna, '<!-- Google Tag Manager (noscript) -->', '<!-- End Google Tag Manager (noscript) -->')
            self.ciasteczka = wycinek(glowna, '<!-- Baner cookie -->', '</div>')
            self.albacross = wycinek(glowna, '<!-- Albacross -->', '<script async src="https://serve.albacross.com/track.js"></script>')
            self.bezpieczenstwo = '\n'.join(re.findall(r'<meta [^>]*data-sicherheit />', glowna))
        if self.k['dostepnosc']:
            self.a11y_prefs = re.search(r"<script>try\{var p=JSON\.parse\(localStorage\.getItem\('a11y-prefs'\).*?</script>", glowna).group(0)
            self.a11y_js = re.search(r'<script src="a11y\.js\?v=[0-9a-f]+" defer></script>', glowna).group(0)
        # Formularz rezerwacji ze strony głównej: ten sam kod, adres Formspree i pola — dla strony kontaktowej.
        # Bez numeru sekcji z głównej i bez klasy „wejscie” (ukrywa element do animacji, której tu nie ma).
        sekcja = wycinek(glowna, '<section id="kontakt"', '</section>')
        self.formularz = re.sub(r'(<p class="label sec__meta">)\d+ / \d+ · ', r'\1', sekcja).replace(' wejscie"', '"')
        assert 'wejscie' not in self.formularz
        # Początek kodu formularza (komentarz nad nim znika ze stron zagranicznych razem z innymi polskimi).
        js = wycinek(glowna, "const form = document.getElementById('formularz');", '\n})();')[:-len('\n})();')]
        self.formularz_js = f'<script>\n(() => {{\n  const el = (id) => document.getElementById(id);\n  {js}\n}})();\n</script>'
        self.skrypt = self.kopiuj_skrypt()

    def kopiuj_skrypt(self):
        """js/strona.js z .pl — te same zachowania, przycisk menu w języku rynku."""
        s = (PL / 'js/strona.js').read_text(encoding='utf-8')
        for stare, nowe in (("'Zamknij' : 'Menu'", self.k['teksty']['menu']),):
            assert s.count(stare) == 1, stare
            s = s.replace(stare, nowe)
        s = bez_komentarzy.js(s)
        (self.cel / 'js').mkdir(exist_ok=True)
        cel = self.cel / 'js/strona.js'
        if not cel.exists() or cel.read_text(encoding='utf-8') != s:
            cel.write_text(s, encoding='utf-8')
        return f'js/strona.js?v={md5(cel)}'

    def zdjecie(self, plik, alt, sizes, ladowanie='lazy', priorytet=False):
        w, h = wymiary(self.cel / f'{plik}.jpg')
        warianty = []
        if (self.cel / f'{plik}-400.webp').exists():
            warianty.append(f'{plik}-400.webp 400w')
        if (self.cel / f'{plik}.webp').exists():
            warianty.append(f'{plik}.webp {w}w')
        zrodlo = f'<source type="image/webp" srcset="{", ".join(warianty)}" sizes="{sizes}" />' if warianty else ''
        extra = ' fetchpriority="high"' if priorytet else ''
        return (f'<picture>{zrodlo}<img src="{plik}.jpg" alt="{html.escape(alt)}" width="{w}" height="{h}" '
                f'loading="{ladowanie}" decoding="async"{extra} /></picture>')

    def zbuduj(self, zrodlo):
        surowe = zrodlo.read_text(encoding='utf-8')
        m = re.match(r'\s*<!--\s*(\{.*?\})\s*-->\s*', surowe, re.S)
        assert m, f'{zrodlo}: brak danych w komentarzu na początku pliku'
        d = json.loads(m.group(1))
        tresc = surowe[m.end():].strip()
        k, baza = self.k, self.k['baza']
        TEKSTY = k['teksty']
        adres = zrodlo.stem + '.html'
        url = f'{baza}/{adres}'

        def foto(mf):
            a = atrybuty(mf.group(1))
            podpis = f'<figcaption class="podpis">{a["podpis"]}</figcaption>' if a.get('podpis') else ''
            return f'<figure>{self.zdjecie(a["plik"], a["alt"], "(max-width: 1023px) 100vw, 640px")}{podpis}</figure>'
        tresc = re.sub(r'<foto ([^>]*?)/?>', foto, tresc)

        def para(mp):
            kadry = [self.zdjecie(a['plik'], a['alt'], '(max-width: 1023px) 50vw, 320px')
                     for a in map(atrybuty, re.findall(r'<kadr ([^>]*?)/?>', mp.group(2)))]
            podpis = atrybuty(mp.group(1)).get('podpis')
            pp = f'<figcaption class="podpis">{podpis}</figcaption>' if podpis else ''
            return f'<figure><div class="foto-para">{"".join(kadry)}</div>{pp}</figure>'
        tresc = re.sub(r'<para([^>]*)>(.*?)</para>', para, tresc, flags=re.S)

        def film(f):
            return (f'<figure><video controls muted playsinline preload="none" poster="{f["plik"]}-poster.jpg" '
                    f'width="{f["szer"]}" height="{f["wys"]}" aria-label="{html.escape(f["etykieta"])}">'
                    f'<source src="{f["plik"]}.mp4" type="video/mp4" /></video>'
                    f'<figcaption class="podpis">{f["podpis"]}</figcaption></figure>')
        # Jeden film z „wideo” (<wideo/>) albo kilka z „filmy” (<wideo plik="video/…"/>).
        w = d.get('wideo')
        if w:
            tresc = tresc.replace('<wideo/>', film(w))
        filmy = {f['plik']: f for f in d.get('filmy', [])}
        tresc = re.sub(r'<wideo plik="([^"]+)"\s*/>', lambda m: film(filmy[m.group(1)]), tresc)
        assert '<wideo' not in tresc, f'{zrodlo}: <wideo/> bez danych „wideo” w nagłówku'

        tresc = re.sub(r'(<h[23]\b[^>]*>)(.*?)(</h[23]>)', lambda m: m.group(1) + podziel(m.group(2)) + m.group(3), tresc)
        naglowki = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', tresc)
        pytania = d.get('pytania', [])
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
          <h2 class="h2" id="faq-h">{TEKSTY["faq"]}</h2>
          <div class="faq">
{elementy}
          </div>
        </section>'''
        czytaj = '\n'.join(f'            <li><a href="{h}">{t}</a></li>' for h, t in d.get('czytaj', []))
        kontakty = '\n'.join(f'            <a class="link" href="{h}" {atr}="seite">{t}</a>' for h, t, atr in k['kontakt'])
        # Strona z formularzem prowadzi do własnego formularza, pozostałe do formularza na stronie głównej.
        do_formularza = '#kontakt' if d.get('formularz') else 'index.html#kontakt'

        # Usługa: pola z nagłówka źródła (jak na dotychczasowej stronie); bez własnego opisu — opis strony.
        ld = []
        if d.get('usluga'):
            usluga = {'@context': 'https://schema.org', '@type': 'Service', **d['usluga']}
            usluga.setdefault('description', d['opis'])
            usluga.setdefault('url', url)
            ld.append(usluga)
        # Okruszki: Startseite › (strona nadrzędna, np. Blog) › strona.
        okruszki = [(TEKSTY['start'], f'{baza}/')]
        if d.get('rodzic'):
            okruszki.append((d['rodzic'][1], f'{baza}/{d["rodzic"][0]}'))
        okruszki.append((d['okruch'], url))
        ld.append({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': n, 'name': nazwa, 'item': adres_ok}
            for n, (nazwa, adres_ok) in enumerate(okruszki, 1)]})
        ld += [{'@context': 'https://schema.org', **x} for x in d.get('ld', [])]
        if pytania:
            ld.append({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
                {'@type': 'Question', 'name': bez_tagow(q), 'acceptedAnswer': {'@type': 'Answer', 'text': bez_tagow(a)}}
                for q, a in pytania]})
        for f in ([w] if w else []) + list(filmy.values()):
            if f.get('ld'):
                ld.append({'@context': 'https://schema.org', '@type': 'VideoObject', **f['ld'],
                           'thumbnailUrl': f'{baza}/{f["plik"]}-poster.jpg', 'contentUrl': f'{baza}/{f["plik"]}.mp4',
                           'inLanguage': k['lang'],
                           'publisher': {'@type': 'Organization', 'name': '33bots', 'url': baza,
                                         'logo': {'@type': 'ImageObject', 'url': f'{baza}/logo.png'}}})
        ld_html = '\n'.join(f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False, indent=2)}\n</script>' for x in ld)
        hreflang = '\n'.join(f'<link rel="alternate" hreflang="{j}" href="{h}" />' for j, h in d['hreflang'])
        meta = f'\n        <p class="art__meta">{d["meta"]}</p>' if d.get('meta') else ''
        og = d.get('og', {})
        og_obraz = og.get('obraz', 'og-image.jpg')
        og_w, og_h = wymiary(self.cel / og_obraz)
        og_alt = f'\n<meta property="og:image:alt" content="{html.escape(og["alt"])}" />' if og.get('alt') else ''
        slowa = f'\n<meta name="keywords" content="{html.escape(d["slowa_kluczowe"])}" />' if d.get('slowa_kluczowe') else ''
        geo = f'\n<meta name="geo.region" content="{k["geo"]}" />' if k.get('geo') else ''

        glowa_analityka = f'{self.gtm_head}\n' if k['analityka'] else (
            '<!-- Keine Analyse-Dienste eingebunden: Diese Seite setzt ausschließlich\n'
            '     technisch notwendige Cookies, eine Einwilligung ist nicht erforderlich. -->\n')
        bezp = f'{self.bezpieczenstwo}\n' if k['analityka'] else ''
        a11y_prefs = f'{self.a11y_prefs}\n' if k['dostepnosc'] else ''
        cialo_analityka = f'{self.gtm_body}\n' if k['analityka'] else '<!-- Kein GTM: ohne Analyse-Dienste ist keine Einwilligung nötig (§ 25 TDDDG). -->\n'
        ciasteczka = f'\n{self.ciasteczka}\n' if k['analityka'] else ''
        skrypty_koniec = ((f'\n{self.formularz_js}' if d.get('formularz') else '')
                          + (f'\n{self.a11y_js}' if k['dostepnosc'] else '') + (f'\n{self.albacross}' if k['analityka'] else ''))

        # Części nagłówka i treści, których strona może nie mieć (strony prawne, 404, kontakt).
        posredni = ''
        if d.get('rodzic'):
            posredni = f'\n        <li><a href="{d["rodzic"][0]}">{d["rodzic"][1]}</a></li><li aria-hidden="true">/</li>'
        akcje = ''
        if d.get('akcje'):
            linki = '\n'.join(f'          <a class="{kl}" href="{h}">{t}</a>' for h, t, kl in d['akcje'])
            akcje = f'\n        <div class="art__cta-akcje">\n{linki}\n        </div>'
        foto_glowy = ''
        if d.get('foto'):
            fg = d['foto']
            foto_glowy = f'''
      <figure class="art__foto">
        {self.zdjecie(fg['plik'], fg['alt'], '(max-width: 1023px) 100vw, 400px', ladowanie='eager', priorytet=True)}
        <figcaption class="podpis">{fg['podpis']}</figcaption>
      </figure>'''
        spis_html = f'''
      <nav class="spis" aria-labelledby="spis-h">
        <p class="label" id="spis-h">{TEKSTY['spis']}</p>
        <ol>
{spis}
        </ol>
      </nav>
''' if naglowki else ''
        cta_html = '' if d.get('cta') is False else f'''

        <aside class="art__cta" aria-labelledby="cta-h">
          <h2 class="h2" id="cta-h">{podziel(d.get('cta_tytul', TEKSTY['cta_tytul']))}</h2>
          <p class="body">{d.get('cta_tekst', TEKSTY['cta_tekst'])}</p>
          <div class="art__cta-akcje">
            <a class="btn" href="{do_formularza}" data-cta="seite">{TEKSTY['cta_przycisk']} <span aria-hidden="true">→</span></a>
{kontakty}
          </div>
        </aside>'''
        czytaj_html = f'''

        <nav class="czytaj" aria-labelledby="czytaj-h">
          <p class="label" id="czytaj-h">{TEKSTY['czytaj']}</p>
          <ul>
{czytaj}
          </ul>
        </nav>''' if czytaj else ''
        tresc_html = f'''

    <div class="art__tresc">{spis_html}
      <div class="prose">
{tresc}
{faq_html}{cta_html}{czytaj_html}
      </div>
    </div>''' if (tresc or faq_html or cta_html or czytaj_html) else ''
        formularz = ''
        if d.get('formularz'):
            formularz = self.formularz
            if d.get('formularz_tytul'):
                formularz = re.sub(r'(<h2 id="kontakt-h" class="h2">)[^<]*(</h2>)', rf'\g<1>{d["formularz_tytul"]}\g<2>', formularz, count=1)
            formularz = f'\n\n{formularz}'

        strona = f'''<!DOCTYPE html>
<html lang="{k['lang']}">
<head>
{glowa_analityka}<meta charset="UTF-8" />
{bezp}<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{d['tytul']}</title>
<meta name="description" content="{html.escape(d['opis'])}" />{slowa}
<meta name="robots" content="{d.get('robots', 'index, follow, max-image-preview:large')}" />
<link rel="canonical" href="{url}" />
{hreflang}
<meta name="theme-color" content="#050505" />{geo}
<meta property="og:type" content="website" />
<meta property="og:url" content="{url}" />
<meta property="og:title" content="{html.escape(d['tytul'])}" />
<meta property="og:description" content="{html.escape(d['opis'])}" />
<meta property="og:image" content="{baza}/{og_obraz}" />
<meta property="og:image:width" content="{og_w}" />
<meta property="og:image:height" content="{og_h}" />{og_alt}
<meta property="og:locale" content="{k['og_locale']}" />
<meta property="og:site_name" content="33bots" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{html.escape(d['tytul'])}" />
<meta name="twitter:description" content="{html.escape(d['opis'])}" />
<link rel="icon" type="image/svg+xml" href="favicon.svg" />
<link rel="preload" as="font" type="font/woff2" crossorigin href="fonts/space-grotesk-latin-wght-normal.woff2" />
<script>document.documentElement.classList.add('js');</script>
{a11y_prefs}<link rel="stylesheet" href="{self.css}" />
{ld_html}
</head>
<body>
{cialo_analityka}
<a href="#hauptinhalt" class="skip-link">{TEKSTY['skip']}</a>

<!-- {ZNACZNIK} aus tresci/zagranica/podstrony/{self.kod}/{zrodlo.name} — Änderungen dort. -->
{self.nav}

<main class="art" id="hauptinhalt" tabindex="-1">
  <article>
    <header class="art__glowa">
      <ol class="okruchy" aria-label="{TEKSTY['okruchy']}">
        <li><a href="index.html">{TEKSTY['start']}</a></li><li aria-hidden="true">/</li>{posredni}
        <li aria-current="page">{d['okruch']}</li>
      </ol>
      <div class="art__tekst">
        <p class="label">{d['kategoria']}</p>
        <h1 class="art__h1">{podziel(d['h1'])}</h1>
        <p class="art__lead">{d['lead']}</p>{meta}{akcje}
      </div>{foto_glowy}
    </header>{tresc_html}
  </article>{formularz}
</main>

{self.stopka}

<div class="pasek" id="pasekMobilny">
  <a class="btn" href="{do_formularza}" data-cta="sticky">{TEKSTY['pasek']} <span aria-hidden="true">→</span></a>
</div>
<div class="pasek-odstep"></div>
{ciasteczka}
<script src="{self.skrypt}" defer></script>{skrypty_koniec}
</body>
</html>
'''
        (self.cel / adres).write_text(bez_komentarzy.strona(strona), encoding='utf-8')
        return adres


def kanal_rss(rynek, zrodla):
    """feed.xml z wpisów bloga (dane BlogPosting w źródłach), od najnowszego; bez wpisów — bez kanału."""
    from datetime import datetime
    from email.utils import format_datetime
    wpisy = []
    for zrodlo in zrodla:
        d = json.loads(re.match(r'\s*<!--\s*(\{.*?\})\s*-->', zrodlo.read_text(encoding='utf-8'), re.S).group(1))
        bp = next((x for x in d.get('ld', []) if x.get('@type') == 'BlogPosting'), None)
        if bp:
            wpisy.append((bp['datePublished'], zrodlo.stem + '.html', bez_tagow(d['h1']), d['opis']))
    if not wpisy:
        return
    baza = rynek.k['baza']
    elementy = '\n'.join(f'''    <item>
      <title>{html.escape(t, quote=False)}</title>
      <link>{baza}/{a}</link>
      <guid>{baza}/{a}</guid>
      <description>{html.escape(o, quote=False)}</description>
      <pubDate>{format_datetime(datetime.fromisoformat(dt))}</pubDate>
    </item>''' for dt, a, t, o in sorted(wpisy, reverse=True))
    (rynek.cel / 'feed.xml').write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>33bots — Blog</title>
    <link>{baza}/blog.html</link>
    <description>{rynek.k['teksty']['rss_opis']}</description>
    <language>{rynek.k['teksty']['rss_jezyk']}</language>
{elementy}
  </channel>
</rss>
''', encoding='utf-8')
    print(f'  feed.xml: {len(wpisy)} wpisów')


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in RYNKI:
        raise SystemExit(f'Użycie: python3 {sys.argv[0]} {"|".join(RYNKI)} <katalog repozytorium rynku>')
    r = Rynek(sys.argv[1], sys.argv[2])
    zrodla = sorted((ZRODLA / sys.argv[1]).glob('*.html'))
    for zrodlo in zrodla:
        print(f'  {r.zbuduj(zrodlo)}')
    kanal_rss(r, zrodla)


if __name__ == '__main__':
    main()
