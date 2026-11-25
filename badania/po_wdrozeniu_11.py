"""Kontrola na żywo 25.11: 14 podstron w układzie strony głównej, B11 na stronach głównych .pl i .lt."""
import html, json, re, sys, time, urllib.request
B = 'https://33bots.pl/'
OCZ = json.load(open('badania/oczekiwane_11.json', encoding='utf-8'))
def get(u):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 kontrola'}), timeout=30)
        return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, ''
wynik = {}
for proba in range(12):
    wynik = {'strony': {}}
    for s, o in OCZ.items():
        k, t = get(B + s)
        tyt = html.unescape((re.search(r'<title>(.*?)</title>', t, re.S) or [0, ''])[1].strip())
        kan = (re.search(r'<link rel="canonical" href="([^"]+)"', t) or [0, ''])[1]
        wynik['strony'][s] = {'kod': k, 'landing': 'class="landing"' in t, 'tytul_ok': tyt == o['title'], 'canonical_ok': kan == o['canonical'],
                              'h1': len(re.findall(r'<h1\b', t)), 'formularz': 'id="formularz"' in t}
    k1, _ = get(B + 'css/landing.css'); k2, js = get(B + 'js/landing.js')
    wynik['zasoby'] = {'landing_css': k1, 'landing_js': k2, 'formspree_w_js': 'formspree.io/f/mnjwvray' in js}
    _, gl = get(B)
    wynik['pl_b11'] = 'ogłoszenie laureatów' in gl and 'wręczenie nagrody' not in gl
    _, lt = get('https://33bots.lt/')
    wynik['lt_b11'] = 'laureatų paskelbimas' in lt and 'apdovanojimo įteikimas' not in lt
    ok = all(v['kod'] == 200 and v['landing'] and v['tytul_ok'] and v['canonical_ok'] and v['h1'] == 1 for v in wynik['strony'].values())
    if ok and wynik['zasoby']['landing_css'] == 200 and wynik['pl_b11']:
        break
    time.sleep(60)
wynik['proby'] = proba + 1
json.dump(wynik, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(json.dumps(wynik, ensure_ascii=False, indent=1))
