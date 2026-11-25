#!/usr/bin/env python3
"""Kontrola na żywo: strony na sezon studniówek i balów (25.11.2026)."""
import json, re, sys, time, urllib.request, urllib.error


def jeden(url):
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (kontrola)'}), timeout=30)
        return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, ''
    except Exception as e:  # noqa
        return 0, str(e)


def czekaj(url, znak, minut=15):
    koniec = time.time() + minut * 60
    while time.time() < koniec:
        k, t = jeden(url + '?k=' + str(int(time.time())))
        if k == 200 and znak in t:
            return True
        time.sleep(30)
    return False


wynik = {
    'pl_poradnik': czekaj('https://33bots.pl/atrakcje-na-studniowke.html', 'Studniówki 2027'),
    'pl_robot': czekaj('https://33bots.pl/robot-na-bal-maturalny.html', 'sto dni przed maturą'),
    'at_maturaball': czekaj('https://33bots.at/roboter-maturaball.html', 'Mitternachtseinlage'),
}
for dom, u in (('pl', 'https://33bots.pl/atrakcje-na-studniowke.html'), ('at', 'https://33bots.at/roboter-maturaball.html')):
    _, mapa = jeden(f'https://33bots.{dom}/sitemap.xml')
    wynik[f'{dom}_w_mapie'] = u in mapa
    k, t = jeden(u)
    wynik[f'{dom}_canonical'] = bool(re.search(r'<link rel="canonical" href="' + re.escape(u) + '"', t))
    wynik[f'{dom}_noindex'] = 'noindex' in (re.search(r'<meta name="robots" content="([^"]*)"', t) or [None, ''])[1]
json.dump(wynik, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(json.dumps(wynik, ensure_ascii=False))
