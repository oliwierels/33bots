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


STRONY = [('pl', 'https://33bots.pl/dzien-kobiet-w-firmie.html', 'ZFŚS'),
          ('pl', 'https://33bots.pl/robot-na-komunie.html', 'niespodzianka na przyjęciu'),
          ('pl', 'https://33bots.pl/robot-na-dzien-dziecka.html', 'dla firm, gmin i szkół'),
          ('pl', 'https://33bots.pl/robot-na-rozpoczecie-roku-szkolnego.html', 'Szkoła Kosmos'),
          ('de', 'https://33bots.de/roboter-abiball.html', 'Abikomitee')]
wynik = {u: {'zywa': czekaj(u, z)} for d, u, z in STRONY}
for dom, u, _ in STRONY:
    _, mapa = jeden(f'https://33bots.{dom}/sitemap.xml')
    k, t = jeden(u)
    wynik[u].update({'w_mapie': u in mapa, 'canonical': bool(re.search(r'<link rel="canonical" href="' + re.escape(u) + '"', t)),
                     'noindex': 'noindex' in (re.search(r'<meta name="robots" content="([^"]*)"', t) or [None, ''])[1]})
json.dump(wynik, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(json.dumps(wynik, ensure_ascii=False))
