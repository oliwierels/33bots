#!/usr/bin/env python3
"""Kontrola na żywo: Abiball (.de) po usunięciu 301, strony miast i B11 (.pl), 25.11.2026."""
import json, sys, time, urllib.request, urllib.error


class Bez(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def pobierz(url):
    try:
        r = urllib.request.build_opener(Bez).open(urllib.request.Request(url + '?k=' + str(int(time.time())), headers={'User-Agent': 'Mozilla/5.0 (kontrola)'}), timeout=30)
        return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, ''
    except Exception as e:  # noqa
        return 0, str(e)


TEST = [('https://33bots.de/roboter-abiball.html', 'Abikomitee', None),
        ('https://33bots.pl/robot-wynajem-gdansk.html', 'trzy wydarzenia firmowe', 'Nasze realizacje'),
        ('https://33bots.pl/robot-wynajem-wroclaw.html', 'obok trenerów', 'Realizujemy eventy'),
        ('https://33bots.pl/blog-kreatywne-sposoby-wykorzystania-robota.html', 'Robot ogłasza laureatów', 'Robot wręcza nagrody')]
wynik = {}
koniec = time.time() + 12 * 60
for u, jest, nie in TEST:
    while True:
        k, t = pobierz(u)
        ok = k == 200 and jest in t and (nie is None or nie not in t)
        if ok or time.time() > koniec:
            break
        time.sleep(30)
    wynik[u] = {'kod': k, 'ok': ok}
json.dump(wynik, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(json.dumps(wynik, ensure_ascii=False))
