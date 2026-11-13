# Stan wyjściowy czterech domen na żywo (13.11.2026, przed zmianami): przekierowania, robots.txt,
# mapy witryn (kod każdego adresu, noindex, canonical, tytuł), stare adresy .de, strona 404, nagłówki.
import hashlib, json, re, subprocess, sys, urllib.parse
from collections import Counter
from pathlib import Path
GB = 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
kat = Path(sys.argv[1]); kat.mkdir(parents=True, exist_ok=True)
def curl(adres, *opcje):
    r = subprocess.run(['curl', '-s', '-A', GB, '--max-time', '40', *opcje, adres], capture_output=True)
    return r.stdout.decode('utf-8', 'ignore')
def kod(adres):
    return curl(adres, '-o', '/dev/null', '-w', '%{http_code} %{redirect_url}').strip()
def lancuch(adres):
    kroki = []
    for _ in range(6):
        k = kod(adres); kroki.append(f'{adres} → {k}')
        cz = k.split(' ', 1)
        if cz[0][:1] == '3' and len(cz) > 1 and cz[1]: adres = cz[1]
        else: break
    return kroki
STARE_DE = ['roboter-mieten-wiesbaden.html', 'roboter-mieten-mannheim.html', 'roboter-mieten-nuernberg.html', 'roboter-messe.html',
            'blog-roboter-auf-der-hochzeit.html', 'blog-roboter-fuer-event-auswaehlen.html', 'roboter-mieten-stuttgart.html', 'roboter-mieten-bonn.html',
            'preise.html', 'kontakt.html', 'angebot.html', 'roboter-mieten.html', 'index.html']
wynik = {}
for d in ['33bots.pl', '33bots.de', '33bots.at', '33bots.lt']:
    w = wynik[d] = {}
    b = f'https://{d}/'
    w['przekierowania'] = {n: lancuch(a) for n, a in {
        'http': f'http://{d}/', 'http_www': f'http://www.{d}/', 'https_www': f'https://www.{d}/', 'index_html': f'{b}index.html',
        'http_podstrona': f'http://{d}/sitemap.xml'}.items()}
    w['robots_txt'] = curl(b + 'robots.txt')[:1500]
    mapa = curl(b + 'sitemap.xml')
    wpisy = re.findall(r'<url>\s*<loc>([^<]+)</loc>(?:\s*<lastmod>([^<]+)</lastmod>)?', mapa)
    w['sitemap_liczba'] = len(wpisy)
    w['sitemap_lastmod'] = dict(Counter(m for _, m in wpisy).most_common())
    w['sitemap_naglowki'] = [l for l in curl(b + 'sitemap.xml', '-o', '/dev/null', '-D', '-').split('\r\n') if re.match(r'(?i)(HTTP|content-type|last-modified)', l)]
    strony = []
    for loc, lastmod in wpisy:
        naglowki = curl(loc, '-o', '/tmp/strona.html', '-D', '-')
        s = Path('/tmp/strona.html').read_text('utf-8', 'ignore')
        st = (re.search(r'HTTP/\S+ (\d+)', naglowki) or [0, '?'])[1]
        def m(wz):
            x = re.search(wz, s, re.S); return x.group(1).strip() if x else None
        tekst = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style|noscript)\b.*?</\1>', ' ', (re.search(r'<main.*?</main>', s, re.S) or [s])[0], flags=re.S)))
        strony.append({'adres': loc, 'lastmod': lastmod, 'kod': st, 'x_robots': m(r'') if False else (re.search(r'(?im)^x-robots-tag:\s*(.+)$', naglowki) or [None, None])[1],
            'robots': m(r'<meta name="robots" content="([^"]*)"'), 'canonical': m(r'<link rel="canonical" href="([^"]*)"'),
            'tytul': m(r'<title>(.*?)</title>'), 'opis_dl': len(m(r'<meta name="description" content="([^"]*)"') or ''), 'lang': m(r'<html[^>]*lang="([^"]*)"'),
            'h1': len(re.findall(r'<h1\b', s)), 'slowa_main': len(tekst.split()), 'bajty': len(s.encode()), 'sha': hashlib.sha256(s.encode()).hexdigest()[:12],
            'last_modified': (re.search(r'(?im)^last-modified:\s*(.+)$', naglowki) or [None, None])[1]})
    w['strony'] = strony
    w['kody'] = dict(Counter(x['kod'] for x in strony))
    w['canonical_inny'] = [x['adres'] for x in strony if x['canonical'] != x['adres']]
    w['noindex_w_mapie'] = [x['adres'] for x in strony if 'noindex' in (x['robots'] or '') or 'noindex' in (x['x_robots'] or '')]
    pierwsza = next((l for l, _ in wpisy if l.endswith('.html')), None)
    if pierwsza:
        bez = pierwsza[:-5]
        w['warianty'] = {'bez_html': lancuch(bez), 'ukosnik': lancuch(pierwsza + '/'), 'wielkie': lancuch(pierwsza.replace('.html', '.HTML')),
                         'parametr': kod(pierwsza + '?utm_source=test'), 'canonical_z_parametrem': (re.search(r'<link rel="canonical" href="([^"]*)"', curl(pierwsza + '?utm_source=test')) or [None, None])[1]}
    nie_ma = b + 'tej-strony-nie-ma-audyt-2026.html'
    cialo = curl(nie_ma)
    w['404'] = {'kod': kod(nie_ma), 'bajty': len(cialo), 'robots': (re.search(r'<meta name="robots" content="([^"]*)"', cialo) or [None, None])[1],
                'tytul': (re.search(r'<title>(.*?)</title>', cialo, re.S) or [None, None])[1], 'katalog': kod(b + 'nie-ma/tez-nie-ma/')}
    w['naglowki_glowna'] = [l for l in curl(b, '-o', '/dev/null', '-D', '-', '-H', 'Accept-Encoding: br, gzip').split('\r\n') if re.match(r'(?i)(HTTP|server|content-encoding|cache-control|strict-transport|x-robots|vary|content-type|last-modified|link)', l)]
    w['zasoby_dla_bota'] = {z: kod(b + z) for z in ['llms.txt', 'feed.xml', 'favicon.svg', 'favicon.ico', 'site.webmanifest', 'ads.txt']}
    if d == '33bots.de':
        w['stare_adresy'] = {}
        for p in STARE_DE:
            c = curl(b + p)
            w['stare_adresy'][p] = {'lancuch': lancuch(b + p), 'canonical': (re.search(r'<link rel="canonical" href="([^"]*)"', c) or [None, None])[1],
                                    'tytul': (re.search(r'<title>(.*?)</title>', c, re.S) or [None, None])[1], 'robots': (re.search(r'<meta name="robots" content="([^"]*)"', c) or [None, None])[1]}
    print(d, w['sitemap_liczba'], w['kody'], 'canonical inny:', len(w['canonical_inny']), 'noindex w mapie:', len(w['noindex_w_mapie']))
(kat / 'stan-wyjsciowy.json').write_text(json.dumps(wynik, ensure_ascii=False, indent=1), encoding='utf-8')
