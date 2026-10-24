# sitemap.xml z gotowych stron rynku: każda indeksowana strona z adresem kanonicznym, hreflang, obrazem og,
# wideo z danych VideoObject i datą zmiany. Data: dziś dla stron zmienionych względem HEAD, inaczej z poprzedniej mapy.
# Użycie: python3 buduj_mape.py <repo> <domena>     np. python3 buduj_mape.py /home/user/litwa-strona 33bots.lt
import html
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

repo, domena = Path(sys.argv[1]), sys.argv[2]
baza = f'https://{domena}/'
dzis = date.today().isoformat()

stare_daty = {}
if (repo / 'sitemap.xml').exists():
    for loc, mod in re.findall(r'<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>', (repo / 'sitemap.xml').read_text(encoding='utf-8')):
        stare_daty[loc] = mod


def zmieniona(plik):
    """Plik zmieniony względem HEAD albo jeszcze nieśledzony."""
    st = subprocess.run(['git', '-C', str(repo), 'status', '--porcelain', '--', plik.name], capture_output=True, text=True).stdout
    return bool(st.strip())


def meta(s, wzor):
    m = re.search(wzor, s)
    return html.unescape(m.group(1)) if m else None


def sekundy(iso):
    m = re.fullmatch(r'PT(?:(\d+)M)?(?:(\d+)S)?', iso or '')
    return (int(m.group(1) or 0) * 60 + int(m.group(2) or 0)) if m else None


def wideo(s):
    for blok in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            d = json.loads(blok)
        except ValueError:
            continue
        for x in (d.get('@graph', [d]) if isinstance(d, dict) else d):
            if isinstance(x, dict) and x.get('@type') == 'VideoObject' and x.get('contentUrl', '').startswith(baza):
                yield x


wpisy = []
for plik in sorted(repo.glob('*.html'), key=lambda p: (p.name != 'index.html', p.name)):
    s = plik.read_text(encoding='utf-8')
    if 'noindex' in (meta(s, r'<meta name="robots" content="([^"]*)"') or ''):
        continue
    loc = meta(s, r'<link rel="canonical" href="([^"]*)"')
    if not loc or not loc.startswith(baza):
        continue
    kanon = loc.replace(baza, '') or 'index.html'
    if kanon != plik.name:
        continue  # strona wskazuje inny adres kanoniczny — w mapie tylko ten adres
    mod = dzis if zmieniona(plik) else stare_daty.get(loc, dzis)
    linie = [f'    <loc>{escape(loc)}</loc>', f'    <lastmod>{mod}</lastmod>']
    for jezyk, href in re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', s):
        linie.append(f'    <xhtml:link rel="alternate" hreflang="{jezyk}" href="{escape(html.unescape(href))}" />')
    obraz = meta(s, r'<meta property="og:image" content="([^"]*)"')
    if obraz and obraz.startswith(baza):
        tytul = meta(s, r'<meta property="og:image:alt" content="([^"]*)"') or meta(s, r'<title>([^<]*)</title>')
        linie += ['    <image:image>', f'      <image:loc>{escape(obraz)}</image:loc>',
                  f'      <image:title>{escape(tytul)}</image:title>', '    </image:image>']
    for v in wideo(s):
        linie += ['    <video:video>',
                  f'      <video:thumbnail_loc>{escape(v["thumbnailUrl"])}</video:thumbnail_loc>',
                  f'      <video:title>{escape(v["name"])}</video:title>',
                  f'      <video:description>{escape(v["description"][:2048])}</video:description>',
                  f'      <video:content_loc>{escape(v["contentUrl"])}</video:content_loc>']
        if sekundy(v.get('duration')):
            linie.append(f'      <video:duration>{sekundy(v["duration"])}</video:duration>')
        linie += ['      <video:family_friendly>yes</video:family_friendly>', '    </video:video>']
    wpisy.append('  <url>\n' + '\n'.join(linie) + '\n  </url>')

(repo / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                                  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
                                  '        xmlns:xhtml="http://www.w3.org/1999/xhtml"\n'
                                  '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"\n'
                                  '        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">\n'
                                  + '\n'.join(wpisy) + '\n</urlset>\n', encoding='utf-8')
print(f'{repo}/sitemap.xml: {len(wpisy)} adresów')
