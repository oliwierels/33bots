# -*- coding: utf-8 -*-
"""Pełny audyt SEO jednej witryny statycznej 33bots (11.2026).

Robi to, czego audyt.py / audit.py / auditas.py nie robią: liczy słowa treści własnej (bez bloków
powtarzanych na innych stronach), porównuje parami tekst główny stron, wypisuje bloki powtarzane
dosłownie, sprawdza szkielety nagłówków, wzajemność hreflang między czterema domenami, graf linków
wewnętrznych (sieroty, głębokość), dane strukturalne (typy, opinie własne), spójność faktów
(ceny, netto/brutto, parametry G1, czas odpowiedzi, liczba wydarzeń, telefony) i datę ostatniej
realnej zmiany treści z historii gita.

    python3 seo/audyt_pelny.py <rynek> <katalog witryny> <katalog wyników> [--git <repo> <ref>]

rynek: pl | de | at | lt. Wynik: <katalog wyników>/<rynek>.json (wszystko) i krótkie podsumowanie.
"""
import glob
import hashlib
import html
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

DOMENY = {'pl': 'https://33bots.pl/', 'de': 'https://33bots.de/', 'at': 'https://33bots.at/', 'lt': 'https://33bots.lt/'}
POMIJANE_PLIKI = {'szablon-case-study.html', 'vorlage-case-study.html', 'index-redesign.html'}
BLOKOWE = {'p', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div', 'section', 'article', 'td', 'th', 'tr', 'figcaption', 'blockquote',
           'summary', 'details', 'dt', 'dd', 'br', 'ul', 'ol', 'table', 'figure', 'main', 'label', 'caption', 'time'}
POMIJANE_TAGI = {'script', 'style', 'noscript', 'svg', 'template', 'nav', 'footer', 'header', 'form', 'select', 'button', 'video', 'iframe'}
# Sekcje, które są ramą serwisu, a nie treścią strony: formularz kontaktowy, pasek, baner cookie, stopka z miastami.
POMIJANE_ATRYBUTY = re.compile(r'(^|[\s_-])(kontakt|contact|cookie|cookies|pasek|stopka|footer|nav|crumbs|okruszki|a11y|dostepnosc|skip|sr-only|modal|toc|spis|menu|dropdown)([\s_-]|$)', re.I)
BEZ_ZAMKNIECIA = {'br', 'img', 'meta', 'link', 'input', 'hr', 'source', 'area', 'base', 'col', 'embed', 'track', 'wbr'}


class Strona(HTMLParser):
    """Jedno przejście po dokumencie: metadane, nagłówki, obrazy, linki, bloki tekstu głównego."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stos = []                 # (tag, czy_pomijany)
        self.pomijanie = 0
        self.w_main = 0
        self.jest_main = False
        self.bufor = []
        self.blok_tag = 'p'
        self.bloki = []                # (tag, tekst) z treści głównej
        self.bloki_poza_main = []
        self.naglowki = []             # (poziom, tekst)
        self.tytul = None
        self._w_tytule = False
        self.meta = {}
        self.linki_head = []           # (rel, hreflang, href)
        self.obrazy = []
        self.linki = []                # (href, anchor, czy_w_tresci)
        self._link = None
        self.jsonld = []
        self._skrypt_ld = None
        self.lang = None
        self.czasy = []
        self.h1 = []

    def _zrzut(self):
        t = re.sub(r'\s+', ' ', ''.join(self.bufor)).strip()
        self.bufor = []
        if t:
            cel = self.bloki if (self.w_main or not self.jest_main) else self.bloki_poza_main
            if self.w_main or not self.jest_main:
                self.bloki.append((self.blok_tag, t))
            else:
                self.bloki_poza_main.append((self.blok_tag, t))

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html':
            self.lang = a.get('lang')
        if tag == 'title':
            self._w_tytule = True
            self.tytul = ''
        if tag == 'meta':
            k = a.get('name') or a.get('property') or a.get('http-equiv')
            if k:
                self.meta[k.lower()] = a.get('content', '')
        if tag == 'link':
            self.linki_head.append((a.get('rel', ''), a.get('hreflang'), a.get('href')))
        if tag == 'script' and (a.get('type') or '').lower() == 'application/ld+json':
            self._skrypt_ld = []
        if tag == 'img':
            self.obrazy.append({'src': a.get('src', ''), 'alt': a.get('alt'), 'w': a.get('width'), 'h': a.get('height'), 'loading': a.get('loading'),
                                'w_tresci': bool(self.w_main and not self.pomijanie)})
        if tag == 'time':
            self.czasy.append(a.get('datetime'))
        pomijany = (tag in POMIJANE_TAGI and not (tag == 'header' and self.w_main)) or bool(POMIJANE_ATRYBUTY.search(' '.join(filter(None, [a.get('id'), a.get('class')]))))
        if 'hidden' in a and tag not in ('div', 'p', 'dd'):      # ukryte odpowiedzi FAQ to treść; ukryte panele — nie
            pomijany = pomijany or tag in ('dialog', 'aside')
        if tag == 'main':
            self.jest_main = True
            self.w_main += 1
        if tag == 'a':
            self._link = {'href': a.get('href'), 'tekst': [], 'w_tresci': bool(self.w_main and not self.pomijanie and not pomijany), 'rel': a.get('rel')}
        if tag in BEZ_ZAMKNIECIA:
            if tag == 'br' and not self.pomijanie:
                self.bufor.append(' ')
            return
        if tag in BLOKOWE and not self.pomijanie:
            self._zrzut()
            self.blok_tag = tag if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'p', 'td', 'th', 'summary', 'figcaption', 'blockquote', 'dt', 'dd') else 'p'
        self.stos.append((tag, pomijany))
        if pomijany:
            self.pomijanie += 1

    def handle_endtag(self, tag):
        if tag == 'title':
            self._w_tytule = False
        if tag == 'script' and self._skrypt_ld is not None:
            self.jsonld.append(''.join(self._skrypt_ld))
            self._skrypt_ld = None
        if tag == 'a' and self._link is not None:
            self._link['tekst'] = re.sub(r'\s+', ' ', ''.join(self._link['tekst'])).strip()
            self.linki.append(self._link)
            self._link = None
        if tag in BEZ_ZAMKNIECIA:
            return
        # zdejmij ze stosu do pasującego znacznika (HTML bywa niedomknięty)
        for i in range(len(self.stos) - 1, -1, -1):
            if self.stos[i][0] == tag:
                for t, p in self.stos[i:]:
                    if p:
                        self.pomijanie -= 1
                del self.stos[i:]
                break
        if tag in BLOKOWE and not self.pomijanie:
            if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
                t = re.sub(r'\s+', ' ', ''.join(self.bufor)).strip()
                if t:
                    self.naglowki.append((int(tag[1]), t))
                    if tag == 'h1':
                        self.h1.append(t)
            self._zrzut()
            self.blok_tag = 'p'
        if tag == 'main':
            self.w_main = max(0, self.w_main - 1)

    def handle_data(self, data):
        if self._w_tytule:
            self.tytul += data
        if self._skrypt_ld is not None:
            self._skrypt_ld.append(data)
            return
        if self._link is not None:
            self._link['tekst'].append(data)
        if not self.pomijanie:
            self.bufor.append(data)
        elif any(t in ('h1',) for t, _ in self.stos):
            pass


def slowa(t):
    return re.findall(r'[^\W_]+', t.lower())


def gramy(sl, n=5):
    return {hash(' '.join(sl[i:i + n])) for i in range(max(0, len(sl) - n + 1))}


def norm_blok(t):
    return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', t.lower())).strip()


def typ_strony(rynek, plik):
    n = plik[:-5]
    prawne = {'polityka-prywatnosci', 'regulamin', 'impressum', 'datenschutz', 'barrierefreiheit', 'privatumo-politika', 'taisykles', 'danke', '404', 'kontakt', 'kontaktai', 'aciu'}
    if n == 'index':
        return 'główna'
    if n in prawne:
        return 'prawna/kontakt'
    if n.startswith('case-study'):
        return 'case study'
    if n.startswith('blog-'):
        return 'artykuł'
    if n in ('blog', 'realizacje-wideo', 'referenzen-videos', 'video-realizacijos', 'galerija', 'eventy'):
        return 'hub'
    if rynek == 'pl':
        if n.startswith('robot-wynajem-'):
            return 'miasto'
        if n.startswith('robot-na-event-'):
            return 'branża/typ'
        if n.startswith('robot-na-') or n in ('wigilia-firmowa-pomysly',):
            return 'okazja'
        if re.match(r'(atrakcje|pomysly|wynajem-atrakcji|pokazy|integracja|zabawy|wigilia)', n):
            return 'poradnik'
        if n in ('sklep', 'wdrozenia'):
            return 'inna oferta'
        return 'usługa'
    if rynek in ('de', 'at'):
        if re.match(r'roboter-mieten-(?!preise)', n):
            return 'miasto'
        if re.match(r'(roboter-|angebot-|unitree-|humanoide|ki-roboter|messe-roboter)', n):
            return 'usługa/okazja'
        return 'poradnik'
    if rynek == 'lt':
        if re.match(r'roboto-nuoma-(?!kaina)', n) or re.match(r'robotas-.*-(vilniuje|kaune|klaipedoje)', n):
            return 'miasto'
        if re.match(r'(robot|humanoidin|unitree|kainos|parduotuve|roboto)', n):
            return 'usługa/okazja'
        return 'poradnik'
    return '?'


# ── fakty: wzorce, które muszą być spójne w obrębie serwisu ──
FAKTY = {
    'cena_zl': r'(?<![\d ])(\d{1,2}[  ]?\d{3})[  ]?(?:zł|PLN)',
    'cena_eur': r'(?<![\d.,])(\d{1,2}[.  ]?\d{3})[  ]?(?:€|EUR|Euro\b|eur\b)',
    'netto_brutto': r'\b(netto|brutto|be PVM|su PVM|zzgl\.|inkl\. MwSt|\+ ?VAT|plus VAT)\b',
    'dof': r'\b(\d{2})[  ]?(?:stopni(?:e|ami)? swobody|DOF|DoF|Freiheitsgrade[n]?|laisvės laipsni\w*)',
    'wzrost_cm': r'\b(1[23]\d)[  ]?cm\b',
    'waga_kg': r'\b(\d{2})[  ]?kg\b',
    'odpowiedz': r'(24[  ]?(?:h|godzin\w*|Werkstunden|Stunden|val\w*)|30[  ]?(?:minut\w*|Minuten|Min\.|min\b)|(?:eines|einem) Werktags?|1 darbo dien\w*)',
    'liczba_wydarzen': r'(?:ponad|über|mehr als|daugiau nei|virš)[  ]?(\d{2,3})\+?[  ]?(?:wydarze\w*|event\w*|realizac\w*|Veranstaltungen|Einsätze\w*|rengini\w*|pokaz\w*)',
    'telefon': r'(\+\d{2}[  ]?\d{2,3}[  ]?\d{3}[  ]?\d{2,3}[  ]?\d{0,3})',
    'superlatywy': r'(najni[żz]sz\w* cen\w*|najta[ńn]sz\w*|nr[  ]?1\b|numer jeden|lider\w* rynku|najlepsz\w* cen\w*|gwarancj\w* najni\w*|g[üu]nstigste\w*|bester Preis|Marktf[üu]hrer|Nr\.[  ]?1|pigiausi\w*|žemiausi\w* kain\w*|geriausi\w* kain\w*)',
    'gratis': r'\b(darmow\w*|bezpłatn\w*|gratis|za darmo|kostenlos\w*|nemokam\w*)\b',
    'zaliczka': r'(bez zaliczki|zero zaliczki|ohne Anzahlung|be avanso|zaliczk\w* \d+ ?%|Anzahlung von \d+)',
}


def wczytaj(katalog, rynek):
    baza = DOMENY[rynek]
    strony = {}
    for plik in sorted(glob.glob(os.path.join(katalog, '*.html'))):
        nazwa = os.path.basename(plik)
        if nazwa in POMIJANE_PLIKI:
            continue
        surowe = Path(plik).read_text(encoding='utf-8', errors='replace')
        p = Strona()
        p.feed(surowe)
        p._zrzut()
        strony[nazwa] = (p, surowe)
    return baza, strony


def data_zmiany(repo, ref, plik, hash_teraz, pamiec):
    """Data commita, w którym tekst główny strony ostatnio się zmienił (pomija same przebudowy)."""
    try:
        log = subprocess.run(['git', '-C', repo, 'log', ref, '--format=%H %ad', '--date=short', '--', plik], capture_output=True, text=True).stdout.split('\n')
    except Exception:
        return None, None
    log = [l.split(' ') for l in log if l.strip()]
    if not log:
        return None, None
    ostatnia = log[0][1]
    for i, (commit, data) in enumerate(log):
        if i == 0:
            ostatnia = data
            continue
        klucz = (commit, plik)
        if klucz not in pamiec:
            r = subprocess.run(['git', '-C', repo, 'show', f'{commit}:{plik}'], capture_output=True)
            if r.returncode != 0:
                pamiec[klucz] = None
            else:
                q = Strona()
                try:
                    q.feed(r.stdout.decode('utf-8', 'replace'))
                    q._zrzut()
                    pamiec[klucz] = hashlib.md5(' '.join(t for _, t in q.bloki).encode()).hexdigest()
                except Exception:
                    pamiec[klucz] = None
        if pamiec[klucz] != hash_teraz:
            return ostatnia, log[-1][1]      # tekst różny w starszym commicie → zmiana nastąpiła w „ostatnia”
        ostatnia = data
    return ostatnia, log[-1][1]              # tekst bez zmian od pierwszego commita pliku


def main():
    rynek, katalog, wyniki = sys.argv[1], sys.argv[2], sys.argv[3]
    repo = ref = None
    if '--git' in sys.argv:
        i = sys.argv.index('--git')
        repo, ref = sys.argv[i + 1], sys.argv[i + 2]
    baza, strony = wczytaj(katalog, rynek)
    Path(wyniki).mkdir(parents=True, exist_ok=True)

    # ── mapa witryny ──
    mapa = {}
    sciezka_mapy = os.path.join(katalog, 'sitemap.xml')
    if os.path.exists(sciezka_mapy):
        for loc, lastmod in re.findall(r'<url>\s*<loc>([^<]+)</loc>(?:\s*<lastmod>([^<]+)</lastmod>)?', Path(sciezka_mapy).read_text(encoding='utf-8')):
            mapa[urlparse(loc).path.lstrip('/') or 'index.html'] = lastmod

    # ── bloki i treść własna ──
    wystapienia = defaultdict(set)
    for nazwa, (p, _) in strony.items():
        for tag, t in p.bloki:
            nb = norm_blok(t)
            if len(nb.split()) >= 6:
                wystapienia[nb].add(nazwa)
    dane = {}
    sl_stron = {}
    for nazwa, (p, surowe) in strony.items():
        tekst = ' '.join(t for _, t in p.bloki)
        sl = slowa(tekst)
        sl_stron[nazwa] = sl
        wlasne = wspolne = 0
        for tag, t in p.bloki:
            n = len(slowa(t))
            nb = norm_blok(t)
            if len(nb.split()) >= 6 and len(wystapienia[nb]) >= 3:
                wspolne += n
            else:
                wlasne += n
        ld_typy, ld_bledy, ld_flagi = [], [], []
        for blok in p.jsonld:
            try:
                d = json.loads(blok)
            except Exception as e:
                ld_bledy.append(str(e)[:80])
                continue

            def przejdz(o):
                if isinstance(o, dict):
                    t = o.get('@type')
                    if t:
                        ld_typy.extend(t if isinstance(t, list) else [t])
                    if 'aggregateRating' in o or o.get('@type') in ('AggregateRating', 'Review'):
                        ld_flagi.append('opinie_wlasne')
                    if 'review' in o:
                        ld_flagi.append('opinie_wlasne')
                    for v in o.values():
                        przejdz(v)
                elif isinstance(o, list):
                    for v in o:
                        przejdz(v)
            przejdz(d)
        canonical = next((h for rel, _, h in p.linki_head if 'canonical' in (rel or '')), None)
        hreflang = {hl: h for rel, hl, h in p.linki_head if hl}
        adres = baza if nazwa == 'index.html' else baza + nazwa
        robots = p.meta.get('robots', '')
        poziomy = [l for l, _ in p.naglowki]
        skoki = [f'h{a}→h{b}' for a, b in zip(poziomy, poziomy[1:]) if b - a > 1]
        fakty = {}
        caly_tekst = tekst + ' ' + (p.meta.get('description') or '') + ' ' + ' '.join(p.jsonld)
        for klucz, wz in FAKTY.items():
            znal = [m if isinstance(m, str) else m[0] for m in re.findall(wz, caly_tekst, re.I)]
            if znal:
                fakty[klucz] = dict(Counter(re.sub(r'[  .]', '', z) if klucz.startswith('cena') else z.lower() for z in znal))
        wewn, zewn = [], []
        for l in p.linki:
            h = (l['href'] or '').strip()
            if not h or h.startswith(('#', 'mailto:', 'tel:', 'javascript:')):
                continue
            pelny = urljoin(adres, h)
            u = urlparse(pelny)
            if u.netloc == urlparse(baza).netloc:
                cel = u.path.lstrip('/') or 'index.html'
                wewn.append({'cel': cel, 'kotwica': u.fragment, 'tekst': l['tekst'], 'w_tresci': l['w_tresci']})
            elif u.scheme in ('http', 'https'):
                zewn.append({'cel': pelny, 'tekst': l['tekst'], 'w_tresci': l['w_tresci'], 'rel': l['rel']})
        dane[nazwa] = {
            'adres': adres, 'typ': typ_strony(rynek, nazwa), 'tytul': re.sub(r'\s+', ' ', p.tytul or '').strip(), 'opis': p.meta.get('description', ''),
            'h1': p.h1, 'robots': robots, 'indeksowalna': 'noindex' not in robots, 'canonical': canonical, 'canonical_self': canonical == adres,
            'lang': p.lang, 'hreflang': hreflang, 'og_locale': p.meta.get('og:locale'), 'og_image_alt': p.meta.get('og:image:alt'),
            'slowa': len(sl), 'slowa_wlasne': wlasne, 'slowa_wspolne': wspolne,
            'naglowki': p.naglowki, 'skoki_naglowkow': skoki,
            'obrazy': len(p.obrazy), 'bez_alt': [o['src'] for o in p.obrazy if o['alt'] is None], 'pusty_alt_w_tresci': [o['src'] for o in p.obrazy if o['alt'] == '' and o['w_tresci']],
            'bez_wymiarow': [o['src'] for o in p.obrazy if not (o['w'] and o['h'])],
            'ld_typy': sorted(set(ld_typy)), 'ld_bledy': ld_bledy, 'ld_flagi': sorted(set(ld_flagi)),
            'w_mapie': nazwa in mapa, 'lastmod': mapa.get(nazwa), 'czasy': [c for c in p.czasy if c],
            'linki_wewn': wewn, 'linki_zewn': zewn, 'fakty': fakty,
            'hash_tekstu': hashlib.md5(tekst.encode()).hexdigest(), 'bajty': len(surowe.encode('utf-8')),
        }

    # ── podobieństwo parami (5-gramy słów tekstu głównego) ──
    g = {n: gramy(s) for n, s in sl_stron.items()}
    nazwy = sorted(g)
    pary = []
    for i, a in enumerate(nazwy):
        for b in nazwy[i + 1:]:
            if not g[a] or not g[b]:
                continue
            wsp = len(g[a] & g[b])
            if not wsp:
                continue
            j = wsp / len(g[a] | g[b])
            if j >= 0.25:
                pary.append((round(j, 3), a, b))
    pary.sort(reverse=True)
    for n in nazwy:
        naj = max(((j, b if a == n else a) for j, a, b in pary if n in (a, b)), default=(0, None))
        dane[n]['najblizsza'] = {'strona': naj[1], 'podobienstwo': naj[0]}
        inne = set().union(*(g[m] for m in nazwy if m != n)) if len(nazwy) > 1 else set()
        dane[n]['udzial_wspolnych_gramow'] = round(len(g[n] & inne) / max(1, len(g[n])), 3)

    def klastry(prog):
        rodzic = {n: n for n in nazwy}

        def znajdz(x):
            while rodzic[x] != x:
                rodzic[x] = rodzic[rodzic[x]]
                x = rodzic[x]
            return x
        for j, a, b in pary:
            if j >= prog:
                rodzic[znajdz(a)] = znajdz(b)
        gr = defaultdict(list)
        for n in nazwy:
            gr[znajdz(n)].append(n)
        return sorted((sorted(v) for v in gr.values() if len(v) > 1), key=len, reverse=True)

    # ── szkielety nagłówków ──
    szkielety = defaultdict(list)
    for n, d in dane.items():
        h2 = tuple(t for l, t in d['naglowki'] if l == 2)
        if len(h2) >= 3:
            szkielety[h2].append(n)
    h2_wyst = Counter(t for d in dane.values() for t in {t for l, t in d['naglowki'] if l in (2, 3)})
    for n, d in dane.items():
        hh = [t for l, t in d['naglowki'] if l in (2, 3)]
        d['udzial_wspolnych_naglowkow'] = round(sum(1 for t in hh if h2_wyst[t] >= 5) / max(1, len(hh)), 2)

    # ── linki ramy serwisu: ta sama para (cel, tekst) na co najmniej 40% stron ──
    pary_linkow = Counter()
    for d in dane.values():
        for para in {(l['cel'], l['tekst']) for l in d['linki_wewn']}:
            pary_linkow[para] += 1
    prog_ramy = max(8, int(0.4 * len(dane)))
    for d in dane.values():
        for l in d['linki_wewn']:
            if pary_linkow[(l['cel'], l['tekst'])] >= prog_ramy:
                l['w_tresci'] = False
                l['rama'] = True

    # ── graf linków ──
    przych = defaultdict(set)
    przych_tresc = defaultdict(set)
    for n, d in dane.items():
        for l in d['linki_wewn']:
            if l['cel'] != n and l['cel'] in dane:
                przych[l['cel']].add(n)
                if l['w_tresci']:
                    przych_tresc[l['cel']].add(n)
    glebokosc = {'index.html': 0}
    kolejka = ['index.html']
    while kolejka:
        x = kolejka.pop(0)
        for l in dane.get(x, {}).get('linki_wewn', []):
            if l['cel'] in dane and l['cel'] not in glebokosc:
                glebokosc[l['cel']] = glebokosc[x] + 1
                kolejka.append(l['cel'])
    martwe = defaultdict(list)
    for n, d in dane.items():
        for l in d['linki_wewn']:
            c = l['cel']
            if c.endswith('.html') and c not in dane and c not in POMIJANE_PLIKI and not os.path.exists(os.path.join(katalog, c)):
                martwe[c].append(n)
        d['linki_przychodzace'] = len(przych[n])
        d['linki_przychodzace_z_tresci'] = len(przych_tresc[n])
        d['glebokosc'] = glebokosc.get(n)
        d['linki_wychodzace_z_tresci'] = len({l['cel'] for l in d['linki_wewn'] if l['w_tresci'] and l['cel'] != n})

    # ── daty realnych zmian ──
    if repo:
        pamiec = {}
        for n, d in dane.items():
            d['zmiana_tresci'], d['pierwszy_commit'] = data_zmiany(repo, ref, n, d['hash_tekstu'], pamiec)

    powt = sorted(((len(v), k) for k, v in wystapienia.items() if len(v) >= 5), reverse=True)
    wynik = {
        'rynek': rynek, 'baza': baza, 'liczba_stron': len(dane), 'w_mapie': len(mapa),
        'mapa_bez_pliku': sorted(set(mapa) - set(dane)), 'strony_poza_mapa': sorted(n for n, d in dane.items() if d['indeksowalna'] and n not in mapa and n not in ('404.html',)),
        'noindex_w_mapie': sorted(n for n in mapa if n in dane and not dane[n]['indeksowalna']),
        'lastmod': dict(Counter(mapa.values()).most_common()),
        'strony': dane,
        'pary': pary[:4000],
        'klastry_050': klastry(0.5), 'klastry_035': klastry(0.35),
        'szkielety': sorted(([list(k), v] for k, v in szkielety.items() if len(v) > 1), key=lambda x: -len(x[1])),
        'powtarzane_bloki': [{'stron': n, 'slow': len(k.split()), 'tekst': k[:220], 'przyklady': sorted(wystapienia[k])[:4]} for n, k in powt[:120]],
        'martwe_linki': {k: v[:5] for k, v in martwe.items()},
        'duplikaty_tytulow': {t: v for t, v in ((t, [n for n, d in dane.items() if d['tytul'] == t]) for t in {d['tytul'] for d in dane.values()}) if len(v) > 1},
        'duplikaty_opisow': {t[:80]: v for t, v in ((t, [n for n, d in dane.items() if d['opis'] == t]) for t in {d['opis'] for d in dane.values() if d['opis']}) if len(v) > 1},
    }
    Path(wyniki, f'{rynek}.json').write_text(json.dumps(wynik, ensure_ascii=False), encoding='utf-8')
    ind = [d for d in dane.values() if d['indeksowalna']]
    print(f'{rynek}: stron {len(dane)}, indeksowalnych {len(ind)}, w mapie {len(mapa)}, par ≥0,5: {sum(1 for j, _, _ in pary if j >= 0.5)}, '
          f'klastrów ≥0,5: {len(wynik["klastry_050"])} (największy {len(wynik["klastry_050"][0]) if wynik["klastry_050"] else 0}), '
          f'bloków powtarzanych na ≥5 stronach: {len(powt)}, sierot: {sum(1 for d in ind if d["linki_przychodzace"] == 0 and d["typ"] != "główna")}')


if __name__ == '__main__':
    main()
