# -*- coding: utf-8 -*-
"""Strona główna rynku a .pl: ten sam układ znaczników w <main>, różni się tylko tekst.

Porównuje drzewo znaczników (znacznik, klasy, atrybuty data-*, typy pól) bez tekstów, adresów,
opisów zdjęć i identyfikatorów. Różnice, które wynikają z treści rynku (np. liczba pytań w FAQ,
dawne kotwice), wypisuje, a skrypt kończy się błędem, gdy jest jakakolwiek inna.

Użycie: python3 tresci/zagranica/porownaj_uklad.py ../33bots-de/index.html [...]
"""
import difflib
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

PL = Path(__file__).resolve().parent.parent.parent / 'index.html'
POMIJANE = {'data-faq', 'data-cs', 'data-licz'}


class Uklad(HTMLParser):
    def __init__(self):
        super().__init__()
        self.w_main = False
        self.glebokosc = 0
        self.linie = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'main':
            self.w_main = True
            return
        if not self.w_main:
            return
        if 'kotwica' in (a.get('class') or ''):
            return
        opis = [tag]
        if a.get('class'):
            opis.append('.' + '.'.join(sorted(a['class'].split())))
        for k in sorted(a):
            if (k.startswith('data-') and k not in POMIJANE) or k in ('type', 'role', 'hidden', 'required', 'name'):
                opis.append(f'[{k}={a[k]}]' if k != 'name' or tag != 'input' else f'[{k}]')
        self.linie.append(' '.join(opis))

    def handle_endtag(self, tag):
        if tag == 'main':
            self.w_main = False


def uklad(plik):
    u = Uklad()
    u.feed(Path(plik).read_text(encoding='utf-8'))
    return u.linie


def main():
    pl = uklad(PL)
    zle = 0
    for plik in sys.argv[1:]:
        obce = uklad(plik)
        rozne = [l for l in difflib.unified_diff(pl, obce, 'pl', plik, n=0, lineterm='') if not l.startswith('@@')]
        print(f'{plik}: {len(obce)} znaczników (PL: {len(pl)}), różnic: {max(0, len(rozne) - 2)}')
        for l in rozne[2:]:
            print('   ', l)
        zle += len(rozne) > 2
    sys.exit(1 if zle else 0)


if __name__ == '__main__':
    main()
