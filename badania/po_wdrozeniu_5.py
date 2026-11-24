#!/usr/bin/env python3
"""Kontrola na żywo .pl po porządkach w stylu tekstów (24.11.2026)."""
import json, re, sys, time, urllib.request, urllib.error


def jeden(url):
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (kontrola)'}), timeout=30)
        return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, ''
    except Exception as e:  # noqa
        return 0, str(e)


koniec = time.time() + 15 * 60
while time.time() < koniec:
    k, t = jeden('https://33bots.pl/pomysly-na-stoisko-targowe.html?k=' + str(int(time.time())))
    if k == 200 and 'sam poczęstunek' in t:
        break
    time.sleep(30)
_, mapa = jeden('https://33bots.pl/sitemap.xml')
adresy = re.findall(r'<loc>(https://33bots\.pl/[^<]*)</loc>', mapa)
wynik = {'nowy_poradnik': k, 'mapa': len(adresy), 'bledy': [], 'pauzy': 0, 'opinie': 0, 'certyfikowany': 0}
for u in adresy:
    k2, t2 = jeden(u)
    if k2 != 200:
        wynik['bledy'].append([u, k2])
    tresc = re.sub(r'<script(?! type="application/ld).*?</script>|<style.*?</style>', '', t2, flags=re.S)
    wynik['pauzy'] += len(re.findall(r'\s—\s', tresc))
    wynik['opinie'] += t2.count('Magdalena T.')
    wynik['certyfikowany'] += len(re.findall(r'certyfikowan\w* operator', t2, re.I))
json.dump(wynik, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(json.dumps(wynik, ensure_ascii=False))
