#!/usr/bin/env python3
"""Kontrola na żywo: scalenie stron .pl (301) i strony B2B (25.11.2026)."""
import json, re, sys, time, urllib.request, urllib.error


class BezPrzekierowan(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


BEZ = urllib.request.build_opener(BezPrzekierowan)


def jeden(url, otwieracz=None):
    try:
        r = (otwieracz or urllib.request.build_opener()).open(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (kontrola)'}), timeout=30)
        return r.status, r.read().decode('utf-8', 'replace'), r.headers.get('Location')
    except urllib.error.HTTPError as e:
        return e.code, '', e.headers.get('Location')
    except Exception as e:  # noqa
        return 0, str(e), None


def czekaj(url, znak, minut=12):
    koniec = time.time() + minut * 60
    while time.time() < koniec:
        k, t, _ = jeden(url + '?k=' + str(int(time.time())))
        if k == 200 and znak in t:
            return True
        time.sleep(30)
    return False


NOWE = [('https://33bots.pl/robot-na-dzien-bhp.html', 'tydzień bezpieczeństwa'),
        ('https://33bots.pl/robot-na-event-w-zakladzie-pracy.html', 'jedno spotkanie dla każdej zmiany'),
        ('https://33bots.pl/roboty-na-eventy-firmowe.html', 'dla HR, BHP, marketingu i agencji'),
        ('https://33bots.pl/oferta-targi.html', 'Ile kosztuje robot na targach kilkudniowych')]
wynik = {'nowe': {}, 'przekierowania': {}, 'abiball': {}}
_, mapa, _ = jeden('https://33bots.pl/sitemap.xml')
for u, z in NOWE:
    ok = czekaj(u, z)
    k, t, _ = jeden(u)
    wynik['nowe'][u] = {'zywa': ok, 'w_mapie': u in mapa,
                        'canonical': bool(re.search(r'<link rel="canonical" href="' + re.escape(u) + '"', t)),
                        'tytul': (re.search(r'<title>([^<]*)', t) or [None, ''])[1]}
for stary, cel in [('robot-na-targi.html', '/oferta-targi.html'), ('robot-na-konferencje.html', '/oferta-konferencje.html'),
                   ('wynajem-robotow.html', '/'), ('robot-na-event-it.html', '/oferta-konferencje.html'),
                   ('robot-na-event-korporacyjny.html', '/roboty-na-eventy-firmowe.html'), ('robot-na-event-modowy.html', '/roboty-na-eventy-firmowe.html')]:
    k, _, loc = jeden('https://33bots.pl/' + stary, BEZ)
    wynik['przekierowania'][stary] = {'kod': k, 'cel': loc, 'zgodny': k == 301 and (loc or '').rstrip('/').endswith(cel.rstrip('/'))}
wynik['mapa_liczba_url'] = mapa.count('<loc>')
wynik['mapa_bez_starych'] = not any(s in mapa for s in ['robot-na-targi.html', 'robot-na-event-it.html', 'wynajem-robotow.html'])
k, t, loc = jeden('https://33bots.de/roboter-abiball.html?k=' + str(int(time.time())))
wynik['abiball'] = {'kod': k, 'location': loc, 'abikomitee': 'Abikomitee' in t, 'tytul': (re.search(r'<title>([^<]*)', t) or [None, ''])[1], 'bajty': len(t)}
k2, t2, _ = jeden('https://33bots.de/sitemap.xml')
wynik['abiball']['w_mapie_de'] = 'roboter-abiball.html' in t2
json.dump(wynik, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(json.dumps(wynik, ensure_ascii=False))
