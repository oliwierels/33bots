"""Kontrola na żywo po poprawkach tekstu i odstępów (25.11): treść, tytuły i reguły CSS."""
import json, re, sys, time, urllib.request
B = 'https://33bots.pl/'
def get(u):
    r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 kontrola'}), timeout=30)
    return r.status, r.read().decode('utf-8', 'replace')
SPR = {
  'blog-unitree-g1-robot.html': ['Nie szura nogami. Kroczy.'],
  'blog-co-potrafi-robot-humanoidalny.html': ['8. Ogłasza laureatów'],
  'case-study-grupa-rekord-mspo.html': ['Na targach obronnych nikt nie przychodzi po atrakcje.</p>'],
  'oferta-targi.html': ['pakietami →</a>. Większość stoisk'],
  'wigilia-firmowa-pomysly.html': ['pozuje do zdjęć i tańczy'],
}
TYTULY = {
  'oferta-targi.html': 'Wynajem robota na targi – humanoid na stoisko od 5500 zł | 33bots',
  'blog-robot-targi-vs-konferencja.html': None,
}
wynik = {}
for proba in range(12):
    wynik = {}
    for s, frazy in SPR.items():
        k, t = get(B + s)
        wynik[s] = {'kod': k, 'frazy': all(f in t for f in frazy),
                    'tytul': re.search(r'<title>(.*?)</title>', t, re.S).group(1),
                    'myslnik_wrecza': 'Wręcza</strong>' in t or 'rozdaje upominki' in t}
    k, t = get(B + 'blog-unitree-g1-robot.html')
    css = re.search(r'css/podstrony\.css\?v=([0-9a-f]+)', t)
    _, c = get(B + 'css/podstrony.css' + ('?v=' + css.group(1) if css else ''))
    wynik['css'] = {'article_num': '.article-num + h2' in c, 'body_text_p': '.body-text > p + p' in c}
    k, t = get(B + 'blog-robot-targi-vs-konferencja.html')
    wynik['faq_pytanie_bez_zmian'] = 'Na jaki event lepiej wynająć robota – targi czy konferencja?' in t
    wynik['tytul_targi_ok'] = wynik['oferta-targi.html']['tytul'] == TYTULY['oferta-targi.html']
    if all(v['frazy'] for k2, v in wynik.items() if k2 in SPR) and all(wynik['css'].values()):
        break
    time.sleep(60)
wynik['proby'] = proba + 1
json.dump(wynik, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(json.dumps(wynik, ensure_ascii=False, indent=1))
