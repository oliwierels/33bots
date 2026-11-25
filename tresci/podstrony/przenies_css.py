# -*- coding: utf-8 -*-
"""Jednorazowo: reguły treści ze style.css → tresci/podstrony/tresc-stara.css z zakresem .podstrona.

Nagłówek, menu, stopka, kursor, pasek postępu, ziarno i reset zostają w style.css (nowa rama
bierze je z css/site.css). Reguły treści (hero, sekcje, kafelki, FAQ, formularz, kontakt, case study)
dostają przedrostek .podstrona, żeby wygrywały z kolizjami w css/site.css (.hero, .faq).
"""
import re
from pathlib import Path

ZRODLO = Path('style.css').read_text(encoding='utf-8')
POMIN = re.compile(r'(^|[\s>+~,(])(html|body|:root|\*|a|img|svg|video|button|input|textarea|select|h[1-6]|p|ul|ol|li|section|main|::selection|::-webkit-scrollbar)\b(?![-\w])|'
                   r'\.(nav|logo|hamburger|mobile-menu|footer|sticky-cta|cursor|scroll-progress|grain|marquee)(?=$|[^\w-]|__|--)|(^|\s)\*|^$')


def bloki(css):
    """Dzieli CSS na (prelude, ciało) z obsługą zagnieżdżeń."""
    i, n, wynik = 0, len(css), []
    while i < n:
        j = css.find('{', i)
        if j < 0:
            break
        prelude = css[i:j].strip()
        g, k = 1, j + 1
        while g and k < n:
            g += {'{': 1, '}': -1}.get(css[k], 0)
            k += 1
        wynik.append((prelude, css[j + 1:k - 1]))
        i = k
    return wynik


# Klasy, których używają podstrony (cała treść <body>), plus te, które dopisują skrypty.
# Reguły dla komponentów, których nie ma już na żadnej stronie (cennik, galeria robota,
# testimoniale itd.), nie trafiają do arkusza — mniej CSS blokującego renderowanie.
UZYWANE = {'active', 'fade-up', 'form-step--hidden', 'form-step--entering', 'has-error', 'in', 'open', 'visible',
           'near-limit', 'scrolled', 'show', 'pasek--widoczny'}
for _p in Path('.').glob('*.html'):
    _t = _p.read_text(encoding='utf-8', errors='replace')
    if 'style.css' in _t or 'css/podstrony.css' in _t:
        for _c in re.findall(r'class="([^"]+)"', _t.split('<body', 1)[-1]):
            UZYWANE.update(_c.split())


def selektor_ok(sel):
    klasy = re.findall(r'\.([a-zA-Z][\w-]*)', sel)
    return not POMIN.search(sel.strip()) and all(k in UZYWANE for k in klasy)


def przenies(css):
    out = []
    for prelude, cialo in bloki(css):
        if prelude.startswith('@media') or prelude.startswith('@supports'):
            wew = przenies(cialo)
            if wew.strip():
                out.append(f'{prelude} {{\n{wew}}}\n')
        elif prelude.startswith('@keyframes'):
            out.append(f'{prelude} {{{cialo}}}\n')
        elif prelude.startswith('@'):
            continue
        else:
            sels = [s.strip() for s in prelude.split(',') if s.strip()]
            dobre = [s for s in sels if selektor_ok(s)]
            if dobre:
                out.append(',\n'.join('.podstrona ' + s for s in dobre) + f' {{{cialo}}}\n')
    return ''.join(out)


bez_komentarzy = re.sub(r'/\*.*?\*/', '', ZRODLO, flags=re.S)
Path('tresci/podstrony/tresc-stara.css').write_text(
    '/* Wygenerowane jednorazowo przez tresci/podstrony/przenies_css.py ze style.css: reguły treści starych podstron. */\n'
    + przenies(bez_komentarzy), encoding='utf-8')
