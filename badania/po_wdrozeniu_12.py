"""Kontrola na żywo 25.11 (2): cennik 8 h / 4 h / 2 h, rabat za dwa dni, licznik bez odliczania (.pl .de .at .lt), LEX AI w Warszawie."""
import html, json, re, sys, time, urllib.request
OCZ = json.load(open('badania/oczekiwane_11.json', encoding='utf-8'))
def get(u):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 kontrola'}), timeout=30)
        return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, ''
def glowna_js(dom):
    _, t = get(dom)
    src = (re.search(r'src="(js/glowna\.js\?v=[^"]+)"', t) or [0, ''])[1]
    k, js = get(dom + src) if src else (0, '')
    return {'src': src, 'kod': k, 'bez_odliczania': bool(js) and "querySelectorAll('[data-licz]')" not in js, 'licznik_100': 'data-licz="100">100' in t}, t, js
for proba in range(12):
    w = {}
    pl, gl, js = glowna_js('https://33bots.pl/')
    pl['faq_8h'] = 'Pełny dzień, czyli 8 godzin na miejscu, kosztuje od 5 500 zł netto' in gl
    pl['low_2750'] = '"lowPrice": "2750"' in gl or '"lowPrice":"2750"' in gl
    pl['kalk_rabat_2'] = 'RABAT_2 = 0.9' in js and 'WEJSCIE = DZIEN / 2' in js
    w['pl'] = pl
    for d in ['de', 'at', 'lt']:
        w[d] = glowna_js(f'https://33bots.{d}/')[0]
    _, t = get('https://33bots.pl/oferta-targi.html')
    w['targi'] = {'9900': 'od 9 900 zł netto' in t, 'bez_9350': '9 350' not in t, 'faq_name': 'Ile miejsca na stoisku potrzebuje robot?",' in t or '"name": "Ile miejsca na stoisku potrzebuje robot?"' in t}
    _, t = get('https://33bots.pl/robot-wynajem-warszawa.html')
    w['warszawa_lexai'] = 'case-study-lexai.html">LEX AI</a>' in t
    _, t = get('https://33bots.pl/blog-ile-kosztuje-wynajem-robota.html')
    w['blog_meta'] = '2 dni −10%, od 3 dni −15%' in t
    w['tytuly'] = {}
    for s, o in OCZ.items():
        k, t = get('https://33bots.pl/' + s)
        tyt = html.unescape((re.search(r'<title>(.*?)</title>', t, re.S) or [0, ''])[1].strip())
        kan = (re.search(r'<link rel="canonical" href="([^"]+)"', t) or [0, ''])[1]
        w['tytuly'][s] = k == 200 and tyt == o['title'] and kan == o['canonical'] and 'class="landing"' in t
    ok = all(w[d]['bez_odliczania'] and w[d]['licznik_100'] for d in ['pl', 'de', 'at', 'lt']) and all(w['tytuly'].values()) \
        and w['pl']['faq_8h'] and w['pl']['kalk_rabat_2'] and all(w['targi'].values()) and w['warszawa_lexai'] and w['blog_meta']
    w['wszystko_ok'] = ok
    if ok:
        break
    time.sleep(60)
w['proby'] = proba + 1
json.dump(w, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(json.dumps(w, ensure_ascii=False, indent=1))
