#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lastmod w mapie witryny = dzień ostatniej zmiany treści strony.

Google korzysta z <lastmod> tylko wtedy, gdy jest konsekwentnie prawdziwy
(Search Central, „Build and submit a sitemap”). Dlatego data nie może się
zmieniać przy przebudowie arkusza stylów ani przy zmianie stopki.

Rejestr seo/lastmod/<rynek>.json trzyma dla każdej strony odcisk treści
(tytuł, opis meta, tekst główny bez nawigacji i stopki, dane strukturalne)
oraz dzień, w którym ten odcisk ostatnio się zmienił.

Użycie:
  python3 seo/lastmod.py <rynek> <katalog>             aktualizuje rejestr; na .pl przepisuje też daty w sitemap.xml
  python3 seo/lastmod.py <rynek> <katalog> --sprawdz   kod 1, gdy rejestr albo mapa nie zgadzają się z treścią
  python3 seo/lastmod.py <rynek> <katalog> --zasiej <audyt.json> [<katalog ze stanem wdrożonym>]
                                                       jednorazowo: daty z historii git (pole zmiana_tresci z audyt_pelny.py)
"""
import hashlib
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audyt_pelny as A  # noqa: E402

TU = Path(__file__).resolve().parent
DATA_WIDOCZNA = re.compile(r'<(\w+)[^>]*class="[^"]*\bdata-zmiany\b[^"]*"[^>]*>.*?</\1>', re.S)
CZAS = re.compile(r'<time\b[^>]*>.*?</time>', re.S)
DATA_LD = re.compile(r'"dateModified"\s*:\s*"[^"]*"\s*,?')


def odcisk(surowe):
    """Odcisk tego, co Google nazywa istotną zmianą: treść główna, tytuł, opis, dane strukturalne.
    Widoczna data aktualizacji i dateModified są wyłączone — wynikają z rejestru, więc nie mogą go zmieniać."""
    s = DATA_WIDOCZNA.sub('', surowe)
    s = CZAS.sub('', s)
    p = A.Strona()
    p.feed(s)
    p._zrzut()
    ld = []
    for blok in p.jsonld:
        blok = DATA_LD.sub('', blok)
        try:
            ld.append(json.dumps(json.loads(blok), sort_keys=True, ensure_ascii=False))
        except ValueError:
            ld.append(re.sub(r'\s+', ' ', blok))
    czesci = [p.tytul or '', p.meta.get('description', ''), '\n'.join(t for _, t in p.bloki), '\n'.join(sorted(ld))]
    return hashlib.md5('\x00'.join(czesci).encode('utf-8')).hexdigest()


def strony(katalog):
    for plik in sorted(Path(katalog).glob('*.html')):
        if plik.name in A.POMIJANE_PLIKI:
            continue
        yield plik.name, plik.read_text(encoding='utf-8', errors='replace')


def rejestr_sciezka(rynek):
    return TU / 'lastmod' / f'{rynek}.json'


def wczytaj(rynek):
    p = rejestr_sciezka(rynek)
    return json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}


def zapisz(rynek, rej):
    p = rejestr_sciezka(rynek)
    p.parent.mkdir(exist_ok=True)
    p.write_text(json.dumps(rej, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')


def aktualizuj(rynek, katalog, dzis=None):
    """Zwraca rejestr po aktualizacji: nowa data tylko tam, gdzie zmienił się odcisk."""
    dzis = dzis or date.today().isoformat()
    rej = wczytaj(rynek)
    nowy = {}
    zmienione = []
    for nazwa, surowe in strony(katalog):
        o = odcisk(surowe)
        stary = rej.get(nazwa)
        if stary and stary['odcisk'] == o:
            nowy[nazwa] = stary
        else:
            nowy[nazwa] = {'odcisk': o, 'data': dzis}
            zmienione.append(nazwa)
    return nowy, zmienione


def daty(rynek):
    return {k: v['data'] for k, v in wczytaj(rynek).items()}


WPIS = re.compile(r'(<loc>https://[^/<]+/([^<]*)</loc>\s*<lastmod>)([^<]+)(</lastmod>)')


def przepisz_mape(katalog, rej):
    mapa = Path(katalog) / 'sitemap.xml'
    t = mapa.read_text(encoding='utf-8')

    def pod(m):
        nazwa = m.group(2) or 'index.html'
        return m.group(1) + (rej[nazwa]['data'] if nazwa in rej else m.group(3)) + m.group(4)
    n = WPIS.sub(pod, t)
    if n != t:
        mapa.write_text(n, encoding='utf-8')
    return n != t


def niezgodne_w_mapie(katalog, rej):
    t = (Path(katalog) / 'sitemap.xml').read_text(encoding='utf-8')
    zle = []
    for m in WPIS.finditer(t):
        nazwa = m.group(2) or 'index.html'
        if nazwa in rej and rej[nazwa]['data'] != m.group(3):
            zle.append((nazwa, m.group(3), rej[nazwa]['data']))
    return zle


def main():
    rynek, katalog = sys.argv[1], sys.argv[2]
    if '--zasiej' in sys.argv:
        i = sys.argv.index('--zasiej')
        audyt = json.load(open(sys.argv[i + 1], encoding='utf-8'))['strony']
        zrodlo = sys.argv[i + 2] if len(sys.argv) > i + 2 else katalog
        rej = {}
        for nazwa, surowe in strony(zrodlo):
            d = (audyt.get(nazwa) or {}).get('zmiana_tresci')
            if d:
                rej[nazwa] = {'odcisk': odcisk(surowe), 'data': d}
        zapisz(rynek, rej)
        print(f'{rynek}: zasiano {len(rej)} stron z historii git')
        return
    if '--sprawdz' in sys.argv:
        nowy, zmienione = aktualizuj(rynek, katalog)
        zle = niezgodne_w_mapie(katalog, wczytaj(rynek))
        for n in zmienione:
            print(f'  treść zmieniona, a rejestr nieodświeżony: {n}')
        for n, a, b in zle:
            print(f'  mapa: {n} ma {a}, rejestr {b}')
        print(f'{rynek}: lastmod {"zgodny" if not (zmienione or zle) else "NIEZGODNY"} ({len(nowy)} stron)')
        sys.exit(1 if (zmienione or zle) else 0)
    nowy, zmienione = aktualizuj(rynek, katalog)
    zapisz(rynek, nowy)
    przepisana = przepisz_mape(katalog, nowy) if rynek == 'pl' else False
    print(f'{rynek}: {len(nowy)} stron w rejestrze, nowa data dla {len(zmienione)}' + (', sitemap.xml przepisana' if przepisana else ''))


if __name__ == '__main__':
    main()
