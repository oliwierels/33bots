# -*- coding: utf-8 -*-
"""Ile tekstu podstrony powtarza się na innych podstronach rynku (6-gramy słów).

Google pomija w indeksie strony, których treść w dużej części jest kopią innych stron serwisu
(„zeskanowana — obecnie niezindeksowana”). Skrypt liczy dla każdej podstrony udział 6-gramów,
które występują także na co najmniej jednej innej indeksowanej podstronie, oraz liczbę słów.

    python3 tresci/zagranica/powtorzenia.py de [próg]
    python3 tresci/zagranica/powtorzenia.py de --strona roboter-eroeffnung.html   # które zdania i z kim
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path


def tekst(plik):
    s = plik.read_text(encoding='utf-8')
    m = re.match(r'<!--\s*(\{.*?\})\s*-->', s, re.S)
    d = json.loads(m.group(1))
    cialo = s[m.end():]
    dodatki = ' '.join([d.get('lead', '')] + [p + ' ' + o for p, o in d.get('pytania', [])])
    t = re.sub(r'<[^>]+>', ' ', cialo + ' ' + dodatki)
    t = re.sub(r'&nbsp;', ' ', t).lower()
    return d, re.findall(r'[\wäöüß]+', t)


def szczegoly(rynek, nazwa):
    kat = Path(__file__).resolve().parent / 'podstrony' / rynek
    inne = {}
    for plik in sorted(kat.glob('*.html')):
        d, slowa = tekst(plik)
        if 'noindex' in d.get('robots', '') or plik.name == nazwa:
            continue
        for i in range(len(slowa) - 5):
            inne.setdefault(tuple(slowa[i:i + 6]), set()).add(plik.name)
    s = (kat / nazwa).read_text(encoding='utf-8')
    m = re.match(r'<!--\s*(\{.*?\})\s*-->', s, re.S)
    d = json.loads(m.group(1))
    bloki = re.findall(r'<(?:p|li|h2|h3)[^>]*>(.*?)</(?:p|li|h2|h3)>', s[m.end():], re.S)
    bloki += [d.get('lead', '')] + [p + ' ' + o for p, o in d.get('pytania', [])]
    for b in bloki:
        t = re.sub(r'&nbsp;', ' ', re.sub(r'<[^>]+>', ' ', b))
        slowa = re.findall(r'[\wäöüß]+', t.lower())
        gr = [tuple(slowa[i:i + 6]) for i in range(len(slowa) - 5)]
        if not gr:
            continue
        wsp = [g for g in gr if g in inne]
        if len(wsp) / len(gr) >= 0.3:
            z = Counter(n for g in wsp for n in inne[g])
            print(f'{len(wsp) / len(gr):4.2f} {len(slowa):3d} sł. | {" ".join(t.split())[:110]} | {", ".join(n.replace(".html", "") for n, _ in z.most_common(3))}')


def main():
    rynek = sys.argv[1]
    if len(sys.argv) > 3 and sys.argv[2] == '--strona':
        return szczegoly(rynek, sys.argv[3])
    prog = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
    kat = Path(__file__).resolve().parent / 'podstrony' / rynek
    strony = {}
    for plik in sorted(kat.glob('*.html')):
        d, slowa = tekst(plik)
        if 'noindex' in d.get('robots', ''):
            continue
        strony[plik.name] = slowa
    gramy = {n: set(tuple(s[i:i + 6]) for i in range(len(s) - 5)) for n, s in strony.items()}
    licznik = Counter(g for zb in gramy.values() for g in zb)
    wyniki = []
    for n, zb in gramy.items():
        wsp = sum(1 for g in zb if licznik[g] > 1) / max(1, len(zb))
        wyniki.append((wsp, len(strony[n]), n))
    for wsp, ile, n in sorted(wyniki, reverse=True):
        if wsp >= prog:
            print(f'{wsp:5.2f}  {ile:5d} słów  {n}')
    print(f'— stron w indeksie: {len(wyniki)}, średni udział powtórzeń: {sum(w for w, _, _ in wyniki) / len(wyniki):.2f}')


if __name__ == '__main__':
    main()
