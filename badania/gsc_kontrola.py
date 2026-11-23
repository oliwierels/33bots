#!/usr/bin/env python3
"""Kontrola na żywo adresów z raportu Search Console z 23.11.2026: kod odpowiedzi, przekierowanie,
robots (meta i nagłówek), canonical; mapy witryn (poprawność XML); kopie na GitHub Pages."""
import json, re, sys, urllib.request, urllib.error, xml.etree.ElementTree as ET
from urllib.parse import urljoin

UA_G = 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'


class BezPrzekierowan(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


OP = urllib.request.build_opener(BezPrzekierowan)


def jeden(url, ua=UA_G):
    try:
        r = OP.open(urllib.request.Request(url, headers={'User-Agent': ua}), timeout=30)
        return r.status, dict(r.headers), r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read().decode('utf-8', 'replace')
    except Exception as e:  # noqa
        return 0, {}, str(e)


def lancuch(url):
    kroki = []
    for _ in range(6):
        kod, h, t = jeden(url)
        kroki.append([url, kod])
        if kod in (301, 302, 303, 307, 308) and h.get('Location'):
            url = urljoin(url, h['Location'])
            continue
        meta = re.search(r'<meta[^>]+name="robots"[^>]+content="([^"]+)"', t, re.I)
        kan = re.search(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', t, re.I)
        return {'kroki': kroki, 'koncowy_kod': kod, 'robots': meta.group(1) if meta else None,
                'x_robots': h.get('X-Robots-Tag') or h.get('x-robots-tag'), 'canonical': kan.group(1) if kan else None,
                'bajty': len(t)}
    return {'kroki': kroki, 'koncowy_kod': 'petla'}


wynik = {'adresy': {}, 'mapy': {}, 'github_pages': {}, 'http': {}}
adresy = [a.strip() for a in open(sys.argv[1]) if a.strip()]
for a in adresy:
    wynik['adresy'][a] = lancuch(a.split('#')[0])
for d in ('33bots.pl', '33bots.de', '33bots.at', '33bots.lt'):
    kod, h, t = jeden(f'https://{d}/sitemap.xml')
    info = {'kod': kod, 'typ': h.get('Content-Type'), 'bajty': len(t)}
    try:
        root = ET.fromstring(t.encode('utf-8'))
        locs = [e.text for e in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        info['xml'] = 'ok'
        info['adresow'] = len(locs)
        zle = {}
        for u in locs:
            r = lancuch(u)
            if r['koncowy_kod'] != 200 or len(r['kroki']) > 1 or (r.get('robots') and 'noindex' in r['robots']) or (r.get('canonical') and r['canonical'] != u):
                zle[u] = r
        info['problemy'] = zle
        vids = [e.text for e in root.iter('{http://www.google.com/schemas/sitemap-video/1.1}content_loc')]
        thumbs = [e.text for e in root.iter('{http://www.google.com/schemas/sitemap-video/1.1}thumbnail_loc')]
        info['wideo'] = len(vids)
        info['wideo_kody'] = {u: jeden(u)[0] for u in sorted(set(vids + thumbs))}
    except ET.ParseError as e:
        info['xml'] = f'BŁĄD: {e}'
    wynik['mapy'][d] = info
for u in ['https://oliwierels.github.io/33bots/', 'https://oliwierels.github.io/33bots/index.html',
          'https://oliwierels.github.io/33bots/roboter-firmenfeier.html', 'https://oliwierels.github.io/33bots/angebot-messen.html',
          'https://oliwierels.github.io/Strona-austria/', 'https://oliwierels.github.io/litwa-strona/',
          'https://oliwierels.github.io/33bots/robots.txt']:
    kod, h, t = jeden(u, 'Mozilla/5.0')
    kan = re.search(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', t, re.I)
    tyt = re.search(r'<title>([^<]*)</title>', t)
    wynik['github_pages'][u] = {'kod': kod, 'location': h.get('Location'), 'canonical': kan.group(1) if kan else None,
                                'title': tyt.group(1) if tyt else None, 'lang': (re.search(r'<html[^>]+lang="([^"]+)"', t) or [None, None])[1]}
for d in ('33bots.de', '33bots.at'):
    for p in ('/', '/index.html', '/roboter-mieten-wien.html', '/angebot-messen.html', '/sitemap.xml', '/roboter-mieten-preise.html'):
        u = f'http://{d}{p}'
        wynik['http'][u] = lancuch(u)['kroki']
for d in ('33bots.de', '33bots.at'):
    wynik['http'][f'https://www.{d}/'] = lancuch(f'https://www.{d}/')['kroki']
    kod, h, t = jeden(f'https://{d}/robots.txt')
    wynik['http'][f'robots {d}'] = t[:400]
json.dump(wynik, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
print('gotowe')
