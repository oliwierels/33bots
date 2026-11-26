"""Kontrola na żywo 33bots.de pod indeksację (26.11): mapa witryny, każdy adres z mapy jako Googlebot
(kod, przekierowania, robots, X-Robots-Tag, canonical, hreflang, czas odpowiedzi), adresy z raportu GSC z 23.11,
linki wewnętrzne prowadzące do przekierowań lub 404, warianty http/www, robots.txt, kopia na GitHub Pages."""
import json, re, sys, time, urllib.request, urllib.error, xml.etree.ElementTree as ET
from urllib.parse import urljoin
UA = 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
class Bez(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
OP = urllib.request.build_opener(Bez)
def jeden(url, ua=UA):
    t0 = time.time()
    try:
        r = OP.open(urllib.request.Request(url, headers={'User-Agent': ua}), timeout=30)
        return r.status, dict(r.headers), r.read().decode('utf-8', 'replace'), round(time.time() - t0, 2)
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read().decode('utf-8', 'replace'), round(time.time() - t0, 2)
    except Exception as e:
        return 0, {}, str(e), round(time.time() - t0, 2)
def lancuch(url):
    kroki = []
    for _ in range(6):
        kod, h, t, s = jeden(url)
        kroki.append([url, kod])
        if kod in (301, 302, 303, 307, 308) and h.get('Location'):
            url = urljoin(url, h['Location']); continue
        m = re.search(r'<meta[^>]+name="robots"[^>]+content="([^"]+)"', t, re.I)
        k = re.search(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', t, re.I)
        return {'kroki': kroki, 'kod': kod, 'robots': m.group(1) if m else None, 'x_robots': h.get('X-Robots-Tag'),
                'canonical': k.group(1) if k else None, 'hreflang': len(re.findall(r'hreflang=', t)), 'czas': s,
                'typ': h.get('Content-Type'), 'tekst': t}
    return {'kroki': kroki, 'kod': 'petla'}
W = {'mapa': {}, 'strony_z_mapy': {}, 'gsc_23_11': {}, 'linki_wewn_zle': {}, 'warianty': {}, 'github_pages': {}}
kod, h, t, _ = jeden('https://33bots.de/sitemap.xml')
root = ET.fromstring(t.encode())
NS = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
locs = [(u.find(NS + 'loc').text, (u.find(NS + 'lastmod').text if u.find(NS + 'lastmod') is not None else None)) for u in root.iter(NS + 'url')]
W['mapa'] = {'kod': kod, 'typ': h.get('Content-Type'), 'adresow': len(locs)}
linki = {}
for u, lm in locs:
    r = lancuch(u)
    tekst = r.pop('tekst', '')
    r['lastmod'] = lm
    r['problem'] = r['kod'] != 200 or len(r['kroki']) > 1 or bool(r.get('robots') and 'noindex' in r['robots']) or bool(r.get('x_robots')) or r.get('canonical') != u
    W['strony_z_mapy'][u] = r
    for href in set(re.findall(r'href="([^"#?]+)', tekst)):
        a = urljoin(u, href)
        if a.startswith('https://33bots.de/') and not re.search(r'\.(css|js|png|jpe?g|webp|svg|ico|xml|txt|pdf|mp4|woff2)$', a):
            linki.setdefault(a, set()).add(u)
mapa = {u for u, _ in locs}
for a, zrodla in sorted(linki.items()):
    if a in mapa: continue
    kod, h, _, _ = jeden(a)
    if kod != 200:
        W['linki_wewn_zle'][a] = {'kod': kod, 'cel': h.get('Location'), 'z_stron': sorted(zrodla)[:5], 'ile_stron': len(zrodla)}
    else:
        r = lancuch(a); r.pop('tekst', None)
        W['linki_wewn_zle'][a] = {'kod': 200, 'robots': r.get('robots'), 'uwaga': 'link do strony spoza mapy', 'ile_stron': len(zrodla)}
for a in [x.strip() for x in open('badania/de_adresy_gsc.txt') if x.strip()]:
    r = lancuch(a); r.pop('tekst', None)
    W['gsc_23_11'][a] = {'kroki': r['kroki'], 'kod': r['kod'], 'robots': r.get('robots'), 'canonical': r.get('canonical'), 'w_mapie': r['kroki'][-1][0] in mapa}
for u in ['http://33bots.de/', 'https://www.33bots.de/', 'http://www.33bots.de/roboter-mieten-preise.html', 'https://33bots.de/index.html', 'https://33bots.de/nie-ma-takiej-strony.html']:
    W['warianty'][u] = lancuch(u)['kroki']
W['warianty']['robots.txt'] = jeden('https://33bots.de/robots.txt')[2][:300]
for u in ['https://oliwierels.github.io/33bots/roboter-firmenfeier.html', 'https://oliwierels.github.io/33bots/']:
    kod, h, t, _ = jeden(u, 'Mozilla/5.0')
    k = re.search(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', t, re.I)
    W['github_pages'][u] = {'kod': kod, 'canonical': k.group(1) if k else None}
W['podsumowanie'] = {'mapa_problemy': [u for u, r in W['strony_z_mapy'].items() if r['problem']],
                     'linki_zle': len([1 for v in W['linki_wewn_zle'].values() if v['kod'] != 200]),
                     'gsc_koncowe_kody': {str(k): sum(1 for v in W['gsc_23_11'].values() if v['kod'] == k) for k in {v['kod'] for v in W['gsc_23_11'].values()}},
                     'gsc_lancuchy_dluzsze_niz_1_skok': [a for a, v in W['gsc_23_11'].items() if len(v['kroki']) > 2],
                     'sredni_czas': round(sum(r['czas'] for r in W['strony_z_mapy'].values()) / max(1, len(locs)), 2)}
json.dump(W, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(json.dumps(W['podsumowanie'], ensure_ascii=False, indent=1))
