#!/usr/bin/env python3
"""Kontrola na żywo po wdrożeniu z 24.11.2026 (natywne teksty .de, Über uns, Impressum)."""
import json, re, sys, time, urllib.request, urllib.error


class BezPrzekierowan(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


OP = urllib.request.build_opener(BezPrzekierowan)


def jeden(url):
    try:
        r = OP.open(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (kontrola)'}), timeout=30)
        return r.status, dict(r.headers), r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read().decode('utf-8', 'replace')
    except Exception as e:  # noqa
        return 0, {}, str(e)


def czekaj(url, znacznik, minut=15):
    koniec = time.time() + minut * 60
    while time.time() < koniec:
        k, h, t = jeden(url + '?k=' + str(int(time.time())))
        if k == 200 and znacznik in t:
            return True
        time.sleep(30)
    return False


wynik = {'czekanie': {
    'de_ueber_uns': czekaj('https://33bots.de/ueber-uns.html', 'Über 33bots'),
    'de_messen': czekaj('https://33bots.de/angebot-messen.html', 'Im Messegang bleiben Ihnen'),
    'at_impressum': czekaj('https://33bots.at/impressum.html', 'Rechtsform'),
}}
_, _, mapa = jeden('https://33bots.de/sitemap.xml')
adresy = re.findall(r'<loc>(https://33bots\.de/[^<]*)</loc>', mapa)
wynik['mapa_de'] = len(adresy)
bledy = []
for u in adresy:
    k, h, t = jeden(u)
    rob = re.search(r'<meta name="robots" content="([^"]*)"', t)
    kan = re.search(r'<link rel="canonical" href="([^"]*)"', t)
    zle = [z for z in ('Outfit', 'Kostüm', 'kostenlos', 'zertifiziert', 'ec.europa.eu/consumers/odr') if z in t]
    if k != 200 or (rob and 'noindex' in rob.group(1)) or not kan or kan.group(1) != u or zle:
        bledy.append({'url': u, 'kod': k, 'robots': rob and rob.group(1), 'canonical': kan and kan.group(1), 'zakazane': zle})
wynik['bledy_de'] = bledy
for u in ('https://33bots.de/impressum.html', 'https://33bots.at/impressum.html'):
    k, h, t = jeden(u)
    wynik[u] = {'kod': k, 'os_link': 'ec.europa.eu/consumers/odr' in t, 'rechtsform': 'Rechtsform' in t}
k, h, t = jeden('https://33bots.de/')
wynik['de_glowna'] = {'kod': k, 'ueber_uns_w_stopce': 'ueber-uns.html' in t, 'nowy_lead': 'Er spricht Deutsch und jede andere Sprache' in t}
json.dump(wynik, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(json.dumps({'czekanie': wynik['czekanie'], 'mapa_de': wynik['mapa_de'], 'bledy': len(bledy)}))
