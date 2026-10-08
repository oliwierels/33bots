# -*- coding: utf-8 -*-
"""Strona główna 33bots.de / 33bots.at w układzie polskiej strony głównej.

Układ, klasy, kolejność kadrów w pasach i cały skrypt strony biorą się z
index.html (PL), więc zmiana układu na .pl przenosi się na rynki zagraniczne
przy następnym uruchomieniu. Treść rynku jest w rynki.py, a część <head>
z SEO (tytuł, opisy, canonical, hreflang, og, dane strukturalne) w
glowa-<rynek>.html — tu nic się w niej nie wymyśla, poza FAQPage, który
powstaje z pytań widocznych na stronie.

Skrypt kopiuje też do repozytorium rynku arkusz css/site.css, fonty i zdjęcia,
których strona potrzebuje.

Użycie (z katalogu głównego repozytorium 33bots.pl):
  python3 tresci/zagranica/buduj_glowna.py de ../33bots-de
  python3 tresci/zagranica/buduj_glowna.py at ../strona-austria
"""
import filecmp
import hashlib
import html
import json
import re
import shutil
import struct
import sys
from pathlib import Path

TU = Path(__file__).resolve().parent
PL = TU.parent.parent
sys.path.insert(0, str(TU))
from rynki import RYNKI  # noqa: E402

INDEX_PL = (PL / 'index.html').read_text(encoding='utf-8')
FONTY = ['space-grotesk-latin-wght-normal.woff2', 'space-grotesk-latin-ext-wght-normal.woff2',
         'plus-jakarta-sans-latin-wght-normal.woff2', 'plus-jakarta-sans-latin-ext-wght-normal.woff2',
         'OFL-space-grotesk.txt', 'OFL-plus-jakarta-sans.txt']
STRZALKA = ' <span aria-hidden="true">→</span>'
NIE_PRZECIAGAJ = ' draggable="false"'


def e(s):
    """Tekst do atrybutu albo treści — bez encji i znaczników z danych."""
    return html.escape(s, quote=True)


def wycinek(od, do, zrodlo=INDEX_PL):
    i = zrodlo.index(od)
    return zrodlo[i:zrodlo.index(do, i) + len(do)]


def wymiary(plik):
    """Szerokość i wysokość JPG z nagłówka pliku — bez zewnętrznych bibliotek."""
    dane = (PL / f'{plik}.jpg').read_bytes()
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
    raise ValueError(f'{plik}.jpg: nie znaleziono wymiarów')


class Strona:
    def __init__(self, r, cel):
        self.r = r
        self.cel = Path(cel)
        self.zdjecia = set()          # pliki bazowe zdjęć do skopiowania

    # ——— drobne klocki ———
    def zdjecie(self, plik, alt, sizes, extra=''):
        self.zdjecia.add(plik)
        w, h = wymiary(plik)
        return (f'<picture><source type="image/webp" srcset="{plik}-400.webp 400w, {plik}.webp {w}w" sizes="{sizes}" />'
                f'<img src="{plik}.jpg" alt="{e(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async"{extra} /></picture>')

    @staticmethod
    def link(href, tekst, klasa=''):
        zewn = href.startswith('http')
        k = f' class="{klasa}"' if klasa else ''
        cel = ' target="_blank" rel="noopener"' if zewn else ''
        return f'<a{k} href="{href}"{cel}>{tekst}</a>'

    @staticmethod
    def dowod(tekst, nota):
        return e(tekst) + (f' <span class="proof__note">{nota}</span>' if nota else '')

    def kotwice(self, sekcja):
        return ''.join(f'<span class="kotwica" id="{k}"></span>' for k in self.r['kotwice'].get(sekcja, []))

    # ——— sekcje ———
    def nawigacja(self):
        r = self.r
        menu = '\n'.join(f'      <a href="{h}">{t}</a>' for h, t in r['nav'])
        panel = '\n'.join(f'      <li><a href="{h}">{t}</a></li>' for h, t in r['nav'])
        dh, dt = r['nav_drugi']
        kh, kt, katr = r['kontakt_nav']
        return f'''<!-- ══════════ 01 NAWIGACJA ══════════ -->
<header class="nav" id="nav">
  <div class="nav__in">
    <a class="nav__logo" href="#top" aria-label="{e(r['logo_aria'])}">33BOTS</a>
    <nav class="nav__menu" aria-label="{e(r['nav_aria'])}">
{menu}
      <a class="nav__drugi" href="{dh}">{dt}</a>
    </nav>
    <div class="nav__akcje">
      <a class="nav__tel" href="{kh}" {katr}="nav">{kt}</a>{self.panel_dostepnosci() if r['panel_dostepnosci'] else ''}
      <a class="link nav__cta" href="#kontakt" data-cta="nav">{r['cta_krotki']}</a>
      <button class="nav__przycisk" id="navPrzycisk" type="button" aria-expanded="false" aria-controls="navPanel">{r['menu']}</button>
    </div>
  </div>
  <div class="nav__panel" id="navPanel" hidden>
    <ul>
{panel}
      <li><a href="{dh}">{dt}</a></li>
    </ul>
    <a class="nav__tel" href="{kh}" {katr}="menu">{kt}</a>
    <a class="btn" href="#kontakt" data-cta="nav">{r['cta']}{STRZALKA}</a>
  </div>
</header>'''

    def hero(self):
        r = self.r
        plik, alt, klient, gdzie = r['slajdy'][0]
        w, h = wymiary(plik)
        self.zdjecia.update(s[0] for s in r['slajdy'])
        lh, lt = r['hero_link']
        return f'''<!-- ══════════ HERO ══════════ -->
<section class="hero" aria-labelledby="hero-label">
  <div class="hero__text">
    <h1 id="hero-label" class="label">{r['h1']}</h1>
    <p class="display">{r['display']}</p>
    <p class="lead">{r['lead']}</p>
    <div class="hero__actions">
      <a class="btn" href="#kontakt" data-cta="hero">{r['cta']}{STRZALKA}</a>
      <a class="link" href="{lh}">{lt}</a>
    </div>
  </div>
  <figure class="hero__media" id="heroMedia">
    <img src="{plik}.jpg" alt="{e(alt)}" fetchpriority="high" decoding="async" width="{w}" height="{h}">
    <figcaption class="hero__podpis">
      <span class="label" id="heroLicznik">01 / {len(r['slajdy']):02d}</span>
      <span class="hero__opis" id="heroOpis"><b>{e(klient)}</b> · {e(gdzie)}</span>
      <button class="hero__pauza" id="heroPauza" type="button" aria-pressed="false" hidden>{r['pauza']}</button>
    </figcaption>
  </figure>
</section>

<section class="proof" aria-label="{e(r['proof_label'])}">
  <p class="label proof__label">{r['proof_label']}</p>
  <ul class="proof__list">
''' + '\n'.join(f'    <li>{self.link(href, self.dowod(tekst, nota))}</li>' for href, tekst, nota in r['proof']) + '''
  </ul>
</section>'''

    def pasy_pl(self):
        """Rzędy kadrów z polskiej strony: prędkość, kierunek, pliki i klucze realizacji."""
        grupa = wycinek('<div class="pasy wejscie" data-grupa="zdjecia">', '\n  </div>\n')
        rzedy = []
        for m in re.finditer(r'<div class="pas" data-predkosc="(\d+)" data-kierunek="(-?1)">(.*?)</ul>', grupa, re.S):
            kadry = re.findall(r'data-cs="([^"]+)"><picture><source type="image/webp" srcset="([a-z0-9-]+)-400\.webp', m.group(3))
            rzedy.append((m.group(1), m.group(2), kadry))
        assert len(rzedy) == 3 and all(k for _, _, k in rzedy), 'nie rozpoznano pasów na stronie PL'
        return rzedy

    def nazwy_pl(self):
        grupa = wycinek('<div class="pasy pasy--nazwy wejscie" data-grupa="nazwy">', '\n  </div>\n')
        rzedy = []
        for m in re.finditer(r'<div class="pas pas--nazwy" data-predkosc="(\d+)" data-kierunek="(-?1)">(.*?)</ul>', grupa, re.S):
            rzedy.append((m.group(1), m.group(2), [html.unescape(n) for n in re.findall(r'<li>(.*?)</li>', m.group(3))]))
        assert len(rzedy) == 3, 'nie rozpoznano pasów z nazwami klientów na stronie PL'
        return rzedy

    def realizacje(self):
        r = self.r
        duze = []
        for i, (klucz, plik, alt, klient, gdzie) in enumerate(r['wyroznione']):
            sizes = '(max-width: 1023px) 100vw, 55vw' if i == 0 else '(max-width: 1023px) 50vw, 30vw'
            duze.append(f'''        <figure>
          <button class="kadr" type="button" data-cs="{klucz}" aria-label="{e(r['zobacz_realizacje'])}: {e(klient)}">{self.zdjecie(plik, alt, sizes)}</button>
          <figcaption class="podpis"><b>{e(klient)}</b> · {e(gdzie)}</figcaption>
        </figure>''')

        pasy = []
        for predkosc, kierunek, kadry in self.pasy_pl():
            pozycje = []
            for klucz, plik in kadry:
                if plik not in r['kadry']:
                    raise SystemExit(f'Brak niemieckiego opisu kadru {plik} (rynki.py, KADRY_DE).')
                if klucz not in r['realizacje']:
                    raise SystemExit(f'Brak niemieckich danych realizacji „{klucz}” (rynki.py, REALIZACJE_DE).')
                alt, klient, opis = r['kadry'][plik]
                pozycje.append(f'        <li><button class="realizacja" type="button" data-cs="{klucz}">'
                               f'{self.zdjecie(plik, alt, "(max-width: 767px) 168px, 248px", NIE_PRZECIAGAJ)}'
                               f'<span class="realizacja__klient">{e(klient)}</span><span class="realizacja__opis">{e(opis)}</span></button></li>')
            pasy.append(f'''    <div class="pas" data-predkosc="{predkosc}" data-kierunek="{kierunek}">
      <ul class="pas__tor">
{chr(10).join(pozycje)}
      </ul>
    </div>''')

        nazwy = []
        for predkosc, kierunek, lista in self.nazwy_pl():
            pozycje = '\n'.join(f'        <li>{e(r["klienci"].get(n, n))}</li>' for n in lista)
            nazwy.append(f'''    <div class="pas pas--nazwy" data-predkosc="{predkosc}" data-kierunek="{kierunek}">
      <ul class="pas__tor">
{pozycje}
      </ul>
    </div>''')

        wiecej = ''
        if r['wszystkie_realizacje']:
            h, t = r['wszystkie_realizacje']
            wiecej = f'\n    <p class="realizacje__wiecej"><a class="link" href="{h}">{t}{STRZALKA}</a></p>\n'

        return f'''<!-- ══════════ 04 IM EINSATZ ══════════ -->
<section id="referenzen" class="sec" aria-labelledby="referenzen-h">
  {self.kotwice('referenzen')}
  <div class="wrap">
    <div class="sec__glowa wejscie">
      <p class="label sec__meta">{r['realizacje_meta']}</p>
      <h2 id="referenzen-h" class="h2">{r['realizacje_h2']}</h2>
      <p class="body">{r['realizacje_body']}</p>
    </div>
    <div class="nasali wejscie">
      <div class="nasali__duzy">
{duze[0]}
      </div>
      <div class="nasali__pion">
{duze[1]}
{duze[2]}
      </div>
    </div>

    <div class="pasy__glowa">
      <h3 class="label">{r['wiecej']}</h3>
      <button class="pasy__pauza" type="button" aria-pressed="false" data-pasy="zdjecia" hidden>{r['zatrzymaj_ruch']}</button>
    </div>
  </div>

  <div class="pasy wejscie" data-grupa="zdjecia">
{chr(10).join(pasy)}
  </div>

  <div class="wrap">{wiecej}
    <div class="klienci" id="klienci">
      <div class="pasy__glowa">
        <p class="label">{r['klienci_label']}</p>
        <button class="pasy__pauza" type="button" aria-pressed="false" data-pasy="nazwy" hidden>{r['zatrzymaj_ruch']}</button>
      </div>
    </div>
  </div>

  <div class="pasy pasy--nazwy wejscie" data-grupa="nazwy">
{chr(10).join(nazwy)}
  </div>

  <div class="wrap">
    <p class="body-sm klienci__kraje">{r['klienci_kraje']}</p>
  </div>
</section>'''

    def wystep(self):
        r = self.r
        wiersze = []
        for i, (tytul, tekst) in enumerate(r['wiersze'], 1):
            foto = ''
            if tytul == 'Branding':
                foto = (f'\n          <figure class="wiersz__foto">{self.zdjecie("realizacja-gala-detal", r["wystep_foto_alt"], "240px")}'
                        f'<figcaption class="podpis">{r["wystep_foto_podpis"]}</figcaption></figure>')
            wiersze.append(f'''      <li class="wiersz">
        <span class="label wiersz__nr">{i:02d}</span>
        <div><h3 class="h3">{tytul}</h3>
          <p class="body">{tekst}</p>{foto}</div>
      </li>''')
        return f'''<!-- ══════════ 05 AUFTRITT ══════════ -->
<section id="auftritt" class="sec" aria-labelledby="auftritt-h">
  {self.kotwice('auftritt')}
  <div class="wrap grid12">
    <div class="wystep__glowa wejscie">
      <p class="label sec__meta">{r['wystep_meta']}</p>
      <h2 id="auftritt-h" class="h2">{r['wystep_h2']}</h2>
      <p class="body">{r['wystep_body']}</p>
    </div>
    <ol class="wiersze wejscie">
{chr(10).join(wiersze)}
    </ol>
  </div>
</section>'''

    def case_study(self):
        r = self.r
        opis = '\n'.join(f'        <div><dt class="label">{dt}</dt>\n          <dd class="body">{dd}</dd></div>' for dt, dd in r['cs_opis'])
        fakty = []
        for href, fakt, etykieta in r['cs_fakty']:
            srodek = f'<span class="cs__fakt">{fakt}</span><span class="label">{etykieta}</span>'
            fakty.append(f'      <li>{self.link(href, srodek) if href else srodek}</li>')
        lh, lt = r['cs_cytat_link']
        return f'''<!-- ══════════ 06 CASE STUDY — jedyna jasna sekcja ══════════ -->
<section id="case-study" class="sec sec--jasna" aria-labelledby="cs-h">
  <div class="wrap grid12">
    <div class="cs__tekst wejscie">
      <p class="label sec__meta">{r['cs_meta']}</p>
      <h2 id="cs-h" class="h2">{r['cs_h2']}</h2>
      <dl class="cs__opis">
{opis}
      </dl>
    </div>
    <figure class="cs__foto wejscie">
      {self.zdjecie('realizacja-eco-studio-eko-partner', r['cs_foto_alt'], '(max-width: 1023px) 100vw, 45vw')}
      <figcaption class="podpis">{r['cs_foto_podpis']}</figcaption>
    </figure>
    <ul class="cs__fakty wejscie">
{chr(10).join(fakty)}
    </ul>
    <blockquote class="cs__cytat wejscie">
      <p>{r['cs_cytat']}</p>
      <footer class="label">{r['cs_cytat_zrodlo']} · {self.link(lh, lt)}</footer>
    </blockquote>
  </div>
</section>'''

    def formaty(self):
        r = self.r
        karty = '\n'.join(f'''      <li class="format">
        <h3 class="h3">{nazwa}</h3>
        <p class="body">{opis}</p>
        <p class="num">{cena}</p>
        <p class="label format__cena-opis">{cena_opis}</p>
      </li>''' for nazwa, opis, cena, cena_opis in r['formaty'])
        return f'''<!-- ══════════ 07 FORMATE UND PREISE ══════════ -->
<section id="preise" class="sec" aria-labelledby="preise-h">
  <div class="wrap">
    <div class="sec__glowa wejscie">
      <p class="label sec__meta">{r['formaty_meta']}</p>
      <h2 id="preise-h" class="h2">{r['formaty_h2']}</h2>
      <p class="body">{r['formaty_body']}</p>
    </div>
    <ul class="formaty wejscie">
{karty}
    </ul>
    <p class="body formaty__wcenie">{r['formaty_wcenie']}</p>
    <p class="formaty__cta"><a class="btn" href="#kontakt" data-cta="formaty">{r['cta']}{STRZALKA}</a></p>
  </div>
</section>'''

    def proces(self):
        r = self.r
        kroki = '\n'.join(f'''      <li class="krok">
        <span class="label">{i:02d}</span>
        <h3 class="h3">{tytul}</h3>
        <p class="label krok__czas">{czas}</p>
        <p class="body">{tekst}</p>
      </li>''' for i, (tytul, czas, tekst) in enumerate(r['kroki'], 1))
        return f'''<!-- ══════════ 08 ABLAUF ══════════ -->
<section id="ablauf" class="sec" aria-labelledby="ablauf-h">
  <div class="wrap">
    <div class="sec__glowa wejscie">
      <p class="label sec__meta">{r['proces_meta']}</p>
      <h2 id="ablauf-h" class="h2">{r['proces_h2']}</h2>
    </div>
    <ol class="kroki wejscie">
{kroki}
    </ol>
    <p class="proces__akcent wejscie">{r['proces_akcent']}</p>
  </div>
</section>'''

    def faq(self):
        r = self.r
        pozycje = '\n'.join(f'''      <div class="faq__item">
        <h3 class="faq__h"><button class="faq__q" type="button" id="faq-{i}-q" aria-expanded="false" aria-controls="faq-{i}" data-faq="{e(q)}">{e(q)}<span class="faq__znak" aria-hidden="true"><span></span><span></span></span></button></h3>
        <div class="faq__a" id="faq-{i}" role="region" aria-labelledby="faq-{i}-q" hidden><p>{e(a)}</p></div>
      </div>''' for i, (q, a) in enumerate(r['faq'], 1))
        return f'''<!-- ══════════ 09 FAQ ══════════ -->
<section id="faq" class="sec" aria-labelledby="faq-h">
  <div class="wrap grid12">
    <div class="faq__glowa wejscie">
      <p class="label sec__meta">{r['faq_meta']}</p>
      <h2 id="faq-h" class="h2">{r['faq_h2']}</h2>
    </div>
    <div class="faq wejscie">
{pozycje}
    </div>
  </div>
</section>'''

    def kontakt(self):
        r, f = self.r, self.r['form']
        osoby = []
        for etykieta, href, tekst in r['kontakt_lista']:
            if href.startswith('tel:'):
                osoby.append(f'        <li class="osoba"><p class="label">{etykieta}</p>\n'
                             f'          <a class="osoba__tel" href="{href}" data-tel="kontakt">{tekst}</a></li>')
            else:
                osoby.append(f'        <li class="osoba"><p class="label">{etykieta}</p>\n'
                             f'          <a class="link osoba__mail" href="{href}" data-mail="kontakt">{tekst}</a></li>')
        typy = '\n'.join(f'            <label class="chip"><input type="radio" name="event_type" value="{e(t)}" required /><span>{t}</span></label>' for t in f['typy'])
        goscie = '\n'.join(f'            <label class="chip"><input type="radio" name="guests" value="{e(g)}" /><span>{g}</span></label>' for g in f['goscie_opcje'])
        return f'''<!-- ══════════ 10 RESERVIERUNG ══════════
     Formular: Schritt 1 — Veranstaltung (Klick), Schritt 2 — Kontakt. Feldnamen wie bisher
     (name, company, email, phone, date, location, message) plus event_type und guests. -->
<section id="kontakt" class="sec sec--powierzchnia" aria-labelledby="kontakt-h">
  <div class="wrap grid12">
    <div class="rez__lewa wejscie">
      <p class="label sec__meta">{r['kontakt_meta']}</p>
      <h2 id="kontakt-h" class="h2">{r['kontakt_h2']}</h2>
      <ul class="osoby">
{chr(10).join(osoby)}
      </ul>
      <p class="body-sm">{r['kontakt_tekst']}</p>
    </div>

    <form class="rez__form wejscie" id="formularz" novalidate>
      <div class="kroki-form" aria-hidden="true">
        <span class="label" data-krok-etykieta="1" aria-current="step">{f['krok1']}</span>
        <span class="label" data-krok-etykieta="2">{f['krok2']}</span>
      </div>

      <div class="krok-form" id="krok1">
        <fieldset class="pole" id="pole-typ">
          <legend>{f['typ']}</legend>
          <div class="chipy">
{typy}
          </div>
          <p class="pole__blad" id="blad-typ" hidden>{f['typ_blad']}</p>
        </fieldset>
        <div class="dwa">
          <div class="pole">
            <label for="pole-data">{f['data']}</label>
            <input type="date" id="pole-data" name="date" />
            <div class="chipy"><label class="chip"><input type="checkbox" id="data-nieustalona" /><span>{f['data_nieustalona']}</span></label></div>
          </div>
          <div class="pole">
            <label for="pole-miejsce">{f['miejsce']}</label>
            <input type="text" id="pole-miejsce" name="location" placeholder="{e(r['miejsce_ph'])}" autocomplete="address-level2" />
          </div>
        </div>
        <fieldset class="pole">
          <legend>{f['goscie']}</legend>
          <div class="chipy">
{goscie}
          </div>
        </fieldset>
        <div class="form-akcje">
          <button class="btn" type="button" id="dalej">{f['dalej']}{STRZALKA}</button>
        </div>
      </div>

      <div class="krok-form" id="krok2" hidden>
        <div class="dwa">
          <div class="pole" id="pole-imie">
            <label for="pole-name">{f['imie']}</label>
            <input type="text" id="pole-name" name="name" required autocomplete="name" />
            <p class="pole__blad" hidden>{f['imie_blad']}</p>
          </div>
          <div class="pole" id="pole-mail">
            <label for="pole-email">{f['mail']}</label>
            <input type="email" id="pole-email" name="email" required autocomplete="email" />
            <p class="pole__blad" hidden>{f['mail_blad']}</p>
          </div>
          <div class="pole">
            <label for="pole-company">{f['firma']}</label>
            <input type="text" id="pole-company" name="company" autocomplete="organization" />
          </div>
          <div class="pole">
            <label for="pole-phone">{f['telefon']}</label>
            <input type="tel" id="pole-phone" name="phone" autocomplete="tel" />
          </div>
        </div>
        <div class="pole">
          <label for="pole-message">{f['opis']}</label>
          <textarea id="pole-message" name="message" maxlength="600" rows="4" placeholder="{e(f['opis_ph'])}"></textarea>
          <span class="pole__licznik"><span id="licznik">0</span> / 600</span>
        </div>
        <div class="form-akcje">
          <button class="wstecz" type="button" id="wstecz">{f['wstecz']}</button>
          <button class="btn" type="submit" id="wyslij">{r['cta']}{STRZALKA}</button>
        </div>
        <p class="pole__blad" id="blad-wysylki" role="alert" hidden></p>
      </div>
    </form>
  </div>
</section>'''

    def stopka(self):
        r = self.r
        kolumny = []
        social_w_kolumnie = False
        for tytul, linki in r['stopka_kolumny']:
            if linki is None:
                social_w_kolumnie = True
                pozycje = '\n'.join(f'      <li><a href="{h}" target="_blank" rel="noopener">{t}</a></li>' for h, t in r['stopka_social'])
            else:
                pozycje = '\n'.join(f'      <li><a href="{h}">{t}</a></li>' for h, t in linki)
            kolumny.append(f'    <ul class="stopka__kol" aria-label="{e(html.unescape(tytul))}">\n{pozycje}\n    </ul>')
        kontakt = ' · '.join(f'<a href="{h}" {atr}="stopka">{t}</a>' for h, t, atr in r['stopka_kontakt'])
        jezyki = ' · '.join(f'<a href="{h}" hreflang="{hl}" lang="{hl}">{t}</a>' for h, hl, t in r['stopka_jezyki'])
        marka_social = ''
        if not social_w_kolumnie:
            marka_social = '\n      <p>' + ' · '.join(f'<a href="{h}" target="_blank" rel="noopener">{t}</a>' for h, t in r['stopka_social']) + '</p>'
        poradnik = ''
        if r['stopka_poradnik']:
            tytul, linki = r['stopka_poradnik']
            poradnik = f'''
    <div class="stopka__poradnik">
      <p>{tytul}</p>
      <div>
{chr(10).join(f'        <a href="{h}">{t}</a>' for h, t in linki)}
      </div>
    </div>'''
        miasta = '\n'.join(f'        <a href="roboter-mieten-{k}.html">{n}</a>' for k, n in r['miasta'])
        return f'''<!-- ══════════ 11 FUSSZEILE ══════════ -->
<footer class="stopka">
  <div class="wrap grid12">
    <div class="stopka__marka">
      <p class="stopka__logo">33BOTS</p>
      <p>{r['stopka_opis']}</p>
      <p>{kontakt}</p>{marka_social}
      <p data-jezyki>{jezyki}</p>
    </div>
{chr(10).join(kolumny)}{poradnik}
    <details class="stopka__miasta">
      <summary>{r['stopka_miasta_tytul']}</summary>
      <div>
{miasta}
      </div>
    </details>
    <p class="stopka__prawa">{r['stopka_prawa']}</p>
  </div>
</footer>'''

    def panel_dostepnosci(self):
        a = self.r['a11y']
        grupy = []
        for etykieta, klucz, opcje in a['grupy']:
            przyciski = '\n'.join(f'            <button type="button" class="a11y-opt" data-a11y="{klucz}" data-value="{w}">{t}</button>' for w, t in opcje)
            grupy.append(f'''        <fieldset class="a11y-group">
          <legend class="a11y-group__label">{etykieta}</legend>
          <div class="a11y-opts" role="group">
{przyciski}
          </div>
        </fieldset>''')
        return f'''
      <!-- Barrierefreiheit (BFSG): Einstellungen nur lokal im Browser (a11y.js) -->
      <button type="button" class="a11y-toggle" id="a11yToggle" aria-expanded="false" aria-controls="a11yPanel" aria-label="{e(a['otworz'])}">
        <svg viewBox="0 0 24 24" aria-hidden="true" width="24" height="24" fill="currentColor"><circle cx="12" cy="4" r="2"/><path d="M19 8h-5v13h-2v-6h-0.9v6H9V8H4V6h15v2z"/></svg>
      </button>
      <div class="a11y-panel" id="a11yPanel" role="dialog" aria-labelledby="a11yTitle" hidden>
        <h2 class="a11y-panel__title" id="a11yTitle">{a['tytul']}</h2>
{chr(10).join(grupy)}
        <button type="button" class="a11y-reset" id="a11yReset">{a['reset']}</button>
      </div>'''

    def dodatki(self):
        """Pasek mobilny, baner cookie, szuflada realizacji."""
        r = self.r
        cookies = ''
        if r['cookies']:
            tekst, przycisk = r['cookies']
            cookies = f'''
<!-- Baner cookie -->
<div class="cookies" id="cookies" aria-live="polite">
  <p class="cookies__text">
    {tekst}
  </p>
  <button id="cookiesOk" class="btn btn--sm">
    {przycisk}
  </button>
</div>
'''
        return f'''<!-- ══════════ Pasek mobilny: pojawia się po minięciu hero ══════════ -->
<div class="pasek" id="pasekMobilny">
  <a class="btn" href="#kontakt" data-cta="sticky">{r['pasek']}{STRZALKA}</a>
</div>
<div class="pasek-odstep"></div>
{cookies}
<div class="szuflada-tlo" id="szufladaTlo" hidden></div>
<aside class="szuflada" id="szuflada" role="dialog" aria-modal="true" aria-labelledby="szufladaTytul" hidden>
  <div class="szuflada__glowa">
    <div>
      <p class="label" id="szufladaPodpis"></p>
      <h2 class="h3" id="szufladaTytul"></h2>
    </div>
    <button class="szuflada__zamknij" id="szufladaZamknij" type="button">{r['szuflada_zamknij']}</button>
  </div>
  <dl class="szuflada__liczby" id="szufladaLiczby"></dl>
  <p class="body" id="szufladaOpis"></p>
  <div class="szuflada__zdjecia" id="szufladaZdjecia"></div>
  <p><a class="link" id="szufladaLink" href="#">{r['szuflada_link']}{STRZALKA}</a></p>
</aside>'''

    # ——— skrypt: polski 1:1, podmienione tylko teksty, dane i adres formularza ———
    def skrypt(self):
        r, f = self.r, self.r['form']
        s = wycinek('<script>\n(() => {', '</script>')
        js = lambda t: json.dumps(t, ensure_ascii=False)  # noqa: E731

        def zamien(stare, nowe):
            nonlocal s
            n = s.count(stare)
            assert n == 1, f'skrypt PL: „{stare[:60]}” występuje {n}×, oczekiwano 1 — sprawdź generator'
            s = s.replace(stare, nowe)

        def zamien_re(wzor, nowe):
            nonlocal s
            s, n = re.subn(wzor, lambda _: nowe, s, flags=re.S)
            assert n == 1, f'skrypt PL: wzorzec {wzor[:40]} trafiony {n}×'

        slajdy = ',\n'.join(f'    {{ src: {js(p + ".jpg")}, alt: {js(a)}, klient: {js(k)}, gdzie: {js(g)} }}' for p, a, k, g in r['slajdy'])
        zamien_re(r'const SLAJDY = \[\n.*?\n  \];', f'const SLAJDY = [\n{slajdy},\n  ];')
        realizacje = {k: {**v, 'link': r['linki_realizacji'].get(k), 'zdjecia': []} for k, v in r['realizacje'].items()}
        zamien_re(r'const REALIZACJE = \{\n.*?\n  \};', 'const REALIZACJE = ' + json.dumps(realizacje, ensure_ascii=False, indent=2).replace('\n', '\n  ') + ';')

        zamien("heroPauza.textContent = 'Następne zdjęcie';", f"heroPauza.textContent = {js(r['nastepne'])};")
        zamien("zatrzymane ? 'Wznów' : 'Pauza'", f"zatrzymane ? {js(r['wznow'])} : {js(r['pauza'])}")
        zamien("otworz ? 'Zamknij' : 'Menu'", f"otworz ? {js(r['menu_zamknij'])} : {js(r['menu'])}")
        zamien("grupa.zatrzymana ? 'Wznów ruch' : 'Zatrzymaj ruch'", f"grupa.zatrzymana ? {js(r['wznow_ruch'])} : {js(r['zatrzymaj_ruch'])}")
        zamien("nieustalona.checked ? 'nieustalony'", f"nieustalona.checked ? {js(f['data_wartosc'])}")
        zamien("btn.textContent = 'Wysyłanie…';", f"btn.textContent = {js(f['wysylanie'])};")
        zamien("t.textContent = 'Mamy Twoje zgłoszenie.';", f"t.textContent = {js(f['sukces'])};")
        zamien("p.append('Odezwiemy się na ', ", f"p.append({js(f['sukces_1'])}, ")
        zamien("'. Odpowiadamy w ciągu 24 godzin roboczych, zwykle tego samego dnia.');", f"{js(r['sukces_2'])});")
        zamien("blad.textContent = 'Nie udało się wysłać. Zadzwoń: +48 531 408 004 albo napisz na kontakt@33bots.pl.';",
               f"blad.textContent = {js(r['blad_wysylki'])};")
        fo = r['formularz']
        zamien("fetch('https://formspree.io/f/mnjwvray', {", f"fetch({js(fo['adres'])}, {{")
        if 'formspree' not in fo['adres']:
            zamien('wysyłka na Formspree', 'wysyłka przez FormSubmit')
        for klucz, wartosc in fo['dodatkowe'].items():
            zamien("      guests:     d.get('guests')     || '—',\n    };",
                   f"      guests:     d.get('guests')     || '—',\n      {klucz}: {js(wartosc)},\n    }};")
        if fo['gtag']:
            zamien("      const sukces = document.createElement('div');",
                   "      if (typeof gtag === 'function') {\n"
                   "        gtag('event', 'form_submit', { event_category: 'contact', event_label: 'Kontaktformular' });\n"
                   "      }\n"
                   "      const sukces = document.createElement('div');")
        if not r['cookies']:
            zamien(wycinek('  /* ——— Baner cookie (logika bez zmian) ——— */', '  });\n\n', s), '')
        if r['panel_dostepnosci']:
            zamien("const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;",
                   "// „Animationen: Aus” w panelu dostępności działa jak ograniczony ruch w systemie.\n"
                   "  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches\n"
                   "    || document.documentElement.getAttribute('data-a11y-motion') === 'off';")
            zamien('\n})();\n</script>', '''

  /* ——— Panel dostępności: przełączenie „Animationen” w trakcie wizyty ———
     Naciska te same przyciski pauzy, które ma użytkownik — zdjęcia w hero i pasy
     stają, a po ponownym włączeniu ruszają tylko te, które zatrzymał panel.
     Kliknięcie bez bąbelkowania: panel nie bierze go za kliknięcie obok i zostaje otwarty. */
  const nacisnij = (b) => b.dispatchEvent(new MouseEvent('click'));
  new MutationObserver(() => {
    const wylacz = document.documentElement.getAttribute('data-a11y-motion') === 'off';
    document.querySelectorAll('#heroPauza[aria-pressed], .pasy__pauza:not([hidden])').forEach((b) => {
      const wcisniety = b.getAttribute('aria-pressed') === 'true';
      if (wylacz && !wcisniety) { b.dataset.panel = ''; nacisnij(b); }
      else if (!wylacz && wcisniety && 'panel' in b.dataset) { delete b.dataset.panel; nacisnij(b); }
    });
  }).observe(document.documentElement, { attributes: true, attributeFilter: ['data-a11y-motion'] });
})();
</script>''')
        # Poza danymi (nazwy własne) i komentarzami w skrypcie nie może zostać polski tekst.
        kod = re.sub(r'const (SLAJDY|REALIZACJE) = .*?\n  [\]}];', '', s, flags=re.S)
        kod = re.sub(r'/\*.*?\*/|//[^\n]*', '', kod, flags=re.S)
        polskie = re.findall(r'[^\n]*[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ][^\n]*', kod)
        assert not polskie, f'w skrypcie zostały polskie teksty: {polskie[:3]}'
        return s

    def faq_jsonld(self):
        dane = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in self.r['faq']]}
        return '<script type="application/ld+json">\n' + json.dumps(dane, ensure_ascii=False, indent=2) + '\n</script>'

    # ——— całość ———
    def zloz(self, wersja_css):
        r = self.r
        glowa = (TU / f'glowa-{r["kod"]}.html').read_text(encoding='utf-8')
        style = [
            '<link rel="preload" as="font" type="font/woff2" crossorigin href="fonts/space-grotesk-latin-wght-normal.woff2" />',
            "<script>document.documentElement.classList.add('js');</script>",
        ]
        if r['panel_dostepnosci']:
            # Ustawienia panelu przed pierwszym malowaniem — bez mignięcia ciemnego motywu.
            style.append("<script>try{var p=JSON.parse(localStorage.getItem('a11y-prefs')||'{}');"
                         "['font','theme','contrast','motion'].forEach(function(k){if(p[k])"
                         "document.documentElement.setAttribute('data-a11y-'+k,p[k]);});}catch(e){}</script>")
        style.append(f'<link rel="stylesheet" href="css/site.css?v={wersja_css}" />')
        glowa = glowa.replace('{{STYLE}}', '\n'.join(style)).replace('{{FAQ}}', self.faq_jsonld())

        gtm_body = ''
        if r['analityka']:
            gtm_body = '\n' + wycinek('<!-- Google Tag Manager (noscript) -->', '<!-- End Google Tag Manager (noscript) -->') + '\n'
        else:
            gtm_body = '\n<!-- Kein GTM: ohne Analyse-Dienste ist keine Einwilligung nötig (§ 25 TDDDG). -->\n'

        czesci = [
            '<!DOCTYPE html>',
            f'<html lang="{r["lang"]}">',
            '<head>',
            glowa.rstrip('\n'),
            '</head>',
            '',
            f'<body id="top">{gtm_body}',
            f'<a href="#hauptinhalt" class="skip-link">{r["skip"]}</a>',
            '',
            self.nawigacja(),
            '',
            '<main id="hauptinhalt" tabindex="-1">',
            '',
            self.hero(), '',
            self.realizacje(), '',
            self.wystep(), '',
            self.case_study(), '',
            self.formaty(), '',
            self.proces(), '',
            self.faq(), '',
            self.kontakt(), '',
            '</main>',
            '',
            self.stopka(),
            '',
        ]
        czesci += [self.dodatki(), '', self.skrypt()]
        if r['panel_dostepnosci']:
            czesci.append('<script src="a11y.js" defer></script>')
        if r['analityka']:
            czesci.append(wycinek('<!-- Albacross -->', '<script async src="https://serve.albacross.com/track.js"></script>'))
        czesci += ['</body>', '</html>', '']
        return '\n'.join(czesci)

    # ——— pliki pomocnicze ———
    def kopiuj(self, zrodlo, cel):
        cel.parent.mkdir(parents=True, exist_ok=True)
        if not cel.exists() or not filecmp.cmp(zrodlo, cel, shallow=False):
            shutil.copy2(zrodlo, cel)
            return 1
        return 0

    def buduj(self):
        nowe = self.kopiuj(PL / 'css/site.css', self.cel / 'css/site.css')
        for plik in FONTY:
            nowe += self.kopiuj(PL / 'fonts' / plik, self.cel / 'fonts' / plik)
        wersja = hashlib.md5((self.cel / 'css/site.css').read_bytes()).hexdigest()[:8]
        strona = self.zloz(wersja)
        for plik in sorted(self.zdjecia):
            for wariant in (f'{plik}.jpg', f'{plik}.webp', f'{plik}-400.webp'):
                nowe += self.kopiuj(PL / wariant, self.cel / wariant)
        (self.cel / 'index.html').write_text(strona, encoding='utf-8')
        return nowe


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in RYNKI:
        raise SystemExit(f'Użycie: python3 {sys.argv[0]} {"|".join(RYNKI)} <katalog repozytorium rynku>')
    s = Strona(RYNKI[sys.argv[1]], sys.argv[2])
    nowe = s.buduj()
    print(f'{sys.argv[2]}/index.html zbudowany; skopiowane pliki pomocnicze: {nowe}')


if __name__ == '__main__':
    main()
