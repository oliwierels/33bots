"""Zgłoszenie adresów z mapy 33bots.de (i 33bots.at, jeśli ma klucz) do IndexNow (Bing i inne; nie Google)."""
import json, re, sys, urllib.request, urllib.error
def get(u):
    r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 kontrola'}), timeout=30)
    return r.status, r.read().decode('utf-8', 'replace')
W = {}
for dom, klucz in [('33bots.de', 'a2813e79cb1d1017ecf75f8b739153a3'), ('33bots.at', sys.argv[2] if len(sys.argv) > 2 else '')]:
    if not klucz:
        W[dom] = 'brak klucza, pominięto'; continue
    try:
        k, t = get(f'https://{dom}/{klucz}.txt')
    except Exception as e:
        W[dom] = f'plik klucza niedostępny: {e}'; continue
    if k != 200 or t.strip() != klucz:
        W[dom] = f'plik klucza niezgodny ({k})'; continue
    _, mapa = get(f'https://{dom}/sitemap.xml')
    adresy = re.findall(r'<loc>([^<]+)</loc>', mapa)
    adresy = [a for a in adresy if a.startswith(f'https://{dom}/') and not re.search(r'\.(mp4|jpg|webp|png)$', a)]
    dane = json.dumps({'host': dom, 'key': klucz, 'keyLocation': f'https://{dom}/{klucz}.txt', 'urlList': adresy}).encode()
    try:
        r = urllib.request.urlopen(urllib.request.Request('https://api.indexnow.org/indexnow', data=dane,
                                   headers={'Content-Type': 'application/json; charset=utf-8'}), timeout=60)
        W[dom] = {'http': r.status, 'adresow': len(adresy)}
    except urllib.error.HTTPError as e:
        W[dom] = {'http': e.code, 'odp': e.read().decode('utf-8', 'replace')[:300], 'adresow': len(adresy)}
json.dump(W, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(json.dumps(W, ensure_ascii=False, indent=1))
