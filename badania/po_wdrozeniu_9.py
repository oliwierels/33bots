#!/usr/bin/env python3
"""Kontrola na żywo: podstrony .pl w nowej ramie (25.11.2026). Tytuły i H1 bez zmian."""
import html, json, re, sys, time, urllib.request, urllib.error

def pobierz(url):
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (kontrola)'}), timeout=30)
        return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, ''
    except Exception as e:  # noqa
        return 0, str(e)

ocz = json.load(open('badania/oczekiwane-uklad.json'))
wynik = {}
koniec = time.time() + 12 * 60
for s, o in ocz.items():
    u = 'https://33bots.pl/' + s
    while True:
        k, t = pobierz(u + '?k=' + str(int(time.time())))
        rama = 'css/podstrony.css' in t and 'navPrzycisk' in t and 'style.css' not in t
        if (k == 200 and rama) or time.time() > koniec:
            break
        time.sleep(30)
    tyt = (re.search(r'<title>(.*?)</title>', t, re.S) or [None, ''])[1].strip()
    h1 = re.sub(r'<[^>]+>', '', (re.search(r'<h1[^>]*>(.*?)</h1>', t, re.S) or [None, ''])[1]).strip()[:60]
    wynik[s] = {'kod': k, 'nowa_rama': rama, 'tytul_ok': tyt == o['title'], 'h1_ok': h1 == o['h1'],
                'canonical_ok': f'<link rel="canonical" href="{u}"' in t, 'gtm': 'GTM-MR7R7CJ3' in t}
for z in ['css/podstrony.css', 'css/site.css', 'js/strona.js', 'main.js']:
    wynik[z] = pobierz('https://33bots.pl/' + z)[0]
json.dump(wynik, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(json.dumps(wynik, ensure_ascii=False))
