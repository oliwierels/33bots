#!/usr/bin/env python3
"""Kontrola na żywo po wdrożeniu z 14.11.2026: czy na czterech domenach stoi to, co zostało wypchnięte.
Użycie: python3 badania/po_wdrozeniu.py <plik wynikowy.json>"""
import json, re, sys, time, urllib.request, urllib.error

UA = {'User-Agent': 'Mozilla/5.0 (kontrola po wdrozeniu)'}


def pobierz(url):
    for proba in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return r.status, r.read().decode('utf-8', 'replace')
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode('utf-8', 'replace')
        except Exception as e:  # noqa: BLE001
            blad = str(e); time.sleep(3)
    return 0, blad


def czekaj(url, znacznik, minut=8):
    """Wdrożenie trwa do kilku minut — czekaj, aż strona pokaże nową treść."""
    koniec = time.time() + minut * 60
    while time.time() < koniec:
        kod, t = pobierz(url + ('&' if '?' in url else '?') + 'k=' + str(int(time.time())))
        if kod == 200 and znacznik in t:
            return True
        time.sleep(20)
    return False


# (adres, oczekiwany kod, [teksty, które mają być], [teksty, których ma nie być])
TESTY = [
    ('https://33bots.pl/', 200, ['Sprawdź termin i cenę'], ['aggregateRating', 'AggregateRating']),
    ('https://33bots.pl/koniec-roku-z-robotem.html', 200, ['Kalendarz sezonu 2026/27', 'robot-na-mikolajki.html'], []),
    ('https://33bots.pl/robot-na-mikolajki.html', 200, ['Plan mikołajek firmowych godzina po godzinie', 'od 5 500 zł netto', 'Czego robot nie zrobi'], ['1,5 godziny', 'Mówią o nas', 'Efekt WOW']),
    ('https://33bots.pl/robot-na-impreze-firmowa.html', 200, ['Wigilia firmowa z robotem: plan wieczoru'], ['1,5 godziny', 'Mówią o nas']),
    ('https://33bots.pl/robot-na-sylwestra.html', 200, ['Plan nocy sylwestrowej godzina po godzinie'], ['1,5 godziny', 'Mówią o nas']),
    ('https://33bots.pl/robot-dla-agencji-eventowych.html', 200, ['Rider techniczny w skrócie'], ['1,5 godziny']),
    ('https://33bots.pl/robot-na-rocznice-firmy.html', 200, ['Co przygotować: historia firmy w pigułce'], ['tort']),
    ('https://33bots.pl/robot-na-gale.html', 200, ['Co ustalamy z reżyserem gali'], ['Mówią o nas']),
    ('https://33bots.pl/robot-na-karnawal.html', 200, ['Karnawał 2027 w kalendarzu'], ['Mówią o nas']),
    ('https://33bots.pl/robot-wynajem-elblag.html', 200, ['Transport w cenie', 'zwykle w ciągu 30 minut'], ['Darmowy transport', 'Najniższe ceny', '24 godzin', 'dzień przed eventem', '30–45 minut']),
    ('https://33bots.pl/blog-logistyka-robota-w-dniu-eventu.html', 200, ['Kiedy przyjeżdżacie na miejsce?', 'Opublikowano'], ['1,5 godziny', 'H-1:30']),
    ('https://33bots.pl/wigilia-firmowa-pomysly.html', 200, ['koniec-roku-z-robotem.html', 'zaktualizowano'], []),
    ('https://33bots.pl/nie-ma-takiej-strony-kontrola.html', 404, ['Robot nie znalazł tej strony'], ['Error 404 Nie znaleziono strony']),
    ('https://33bots.pl/seo/lastmod.py', 404, [], ['def odcisk']),
    ('https://33bots.pl/sklep.html', 200, ['https://33bots.lt/parduotuve.html'], []),
    ('https://33bots.de/', 200, ['id="przeglad"', 'Antwort meist in 30 Minuten', 'roboter-mieten-berlin.html'], ['aggregateRating', 'Angebot in 24 h', '30–45 Minuten']),
    ('https://33bots.de/zauberer-buchen.html', 200, ['noindex'], []),
    ('https://33bots.de/hochzeit-kosten.html', 200, ['noindex'], []),
    ('https://33bots.de/weihnachtsfeier-ideen.html', 200, ['Aktualisiert am', 'roboter-mieten-preise.html', 'roboter-firmenfeier.html'], ['noindex']),
    ('https://33bots.de/roboter-mieten-berlin.html', 200, ['unitree-g1-mieten.html'], ['Operator, Anfahrt und Branding sind im Preis.', '30–45 Minuten', 'noindex']),
    ('https://33bots.de/humanoiden-roboter-mieten.html', 200, ['Die Ankunftszeit stimmen wir mit Ihnen ab'], ['1,5 Stunden', '30–45 Minuten']),
    ('https://33bots.at/', 200, ['id="przeglad"', 'roboter-mieten-wien.html'], ['aggregateRating']),
    ('https://33bots.lt/', 200, ['id="przeglad"', 'per 30 min', 'robotu-nuoma-vilnius.html'], ['aggregateRating', 'per 24 val']),
    ('https://33bots.lt/galerija.html', 200, ['Daugiau nei 100'], ['Daugiau nei 40']),
    ('https://33bots.lt/robotu-nuoma-vilnius.html', 200, [], ['pusantros valandos', '30–45 minu']),
    ('https://33bots.lt/unitree-g1-nuoma.html', 200, ['https://33bots.de/unitree-g1-mieten.html'], ['30–45 minu']),
]

gotowe = {d: czekaj(u, z) for d, u, z in [
    ('pl', 'https://33bots.pl/robot-na-karnawal.html', 'Karnawał 2027 w kalendarzu'),
    ('de', 'https://33bots.de/', 'id="przeglad"'),
    ('at', 'https://33bots.at/', 'id="przeglad"'),
    ('lt', 'https://33bots.lt/robotu-nuoma.html', 'per 30 min')]}
wyniki, bledy = [], []
for url, kod_ocz, ma, nie_ma in TESTY:
    kod, t = pobierz(url)
    brak = [x for x in ma if x not in t]
    jest = [x for x in nie_ma if x in t]
    ok = kod == kod_ocz and not brak and not jest
    wyniki.append({'adres': url, 'kod': kod, 'ok': ok, 'brak': brak, 'niechciane': jest})
    if not ok:
        bledy.append(url)
mapy = {}
for d in ('33bots.pl', '33bots.de', '33bots.at', '33bots.lt'):
    kod, t = pobierz(f'https://{d}/sitemap.xml')
    daty = {}
    for x in re.findall(r'<lastmod>([^<]+)</lastmod>', t):
        daty[x] = daty.get(x, 0) + 1
    adresy = re.findall(r'<loc>([^<]+)</loc>', t)
    kody = {}
    for a in adresy:
        k, tt = pobierz(a)
        kody[str(k)] = kody.get(str(k), 0) + 1
        if k == 200 and re.search(r'<meta name="robots" content="[^"]*noindex', tt):
            kody['noindex_w_mapie'] = kody.get('noindex_w_mapie', 0) + 1
    mapy[d] = {'kod': kod, 'adresow': len(adresy), 'lastmod': dict(sorted(daty.items(), reverse=True)[:5]), 'kody_adresow': kody}
json.dump({'gotowe_po_czekaniu': gotowe, 'bledy': bledy, 'testy': wyniki, 'mapy': mapy}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('gotowe:', gotowe, '| błędów:', len(bledy), bledy)
print(json.dumps(mapy, ensure_ascii=False))
