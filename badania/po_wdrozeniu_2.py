#!/usr/bin/env python3
"""Kontrola na żywo po wdrożeniu .de i .at z 14.11.2026 (runda 2): czy na domenach stoi to, co zostało wypchnięte.
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
    ('https://33bots.at/', 200, ['Der Gast, mit dem alle ein Foto wollen', 'Women in Tech Summit: ein Roboter unter', 'roboter-mieten-preise.html', 'roboter-kongress-gala.html', 'Warszawa', 'Grüß Gott'],
     ['"HowTo"', '"postalCode":"1010"', 'aggregateRating', 'zertifiziert']),
    ('https://33bots.at/roboter-mieten-preise.html', 200, ['3.910', 'hreflang="de" href="https://33bots.de/roboter-mieten-preise.html"'], ['noindex']),
    ('https://33bots.at/roboter-firmenfeier.html', 200, ['Firmenjubiläum von 18 bis 22 Uhr', 'Was der Roboter nicht macht'], ['noindex']),
    ('https://33bots.at/roboter-kongress-gala.html', 200, ['Einlage zu Mitternacht', 'Was wir mit Ihrer Regie abstimmen'], ['noindex']),
    ('https://33bots.at/unitree-g1-mieten.html', 200, ['etwa 35', 'Was der G1 nicht kann'], ['Millionen Views']),
    ('https://33bots.at/messe-roboter-mieten.html', 200, ['Ein Messetag mit Roboter', 'roboter-mieten-preise.html'], ['stärkste Stopper']),
    ('https://33bots.at/humanoider-roboter-mieten.html', 200, ['Was Sie buchen', 'roboter-firmenfeier.html'], []),
    ('https://33bots.at/roboter-mieten-wien.html', 200, ['roboter-kongress-gala.html', 'roboter-mieten-preise.html'], []),
    ('https://33bots.at/roboter-weihnachtsfeier.html', 200, ['roboter-firmenfeier.html', 'Der Dezember 2026 im Kalender', 'Weihnachtsfeier von 18 bis 22 Uhr'], ['Der erste Eindruck des Abends']),
    ('https://33bots.at/sitemap.xml', 200, ['roboter-mieten-preise.html', 'roboter-firmenfeier.html', 'roboter-kongress-gala.html'], ['video:video']),
    ('https://33bots.de/', 200, ['"legalName"', 'Warszawa', 'id="przeglad"'], ['aggregateRating']),
    ('https://33bots.de/roboter-fuer-eventagenturen.html', 200, ['Was Sie Ihrem Kunden nicht versprechen sollten', 'Briefing: Was wir von Ihnen wissen müssen'], []),
    ('https://33bots.de/angebot-konferenzen-galas.html', 200, ['hreflang="de-AT" href="https://33bots.at/roboter-kongress-gala.html"'], ['zuverlässig in der Berichterstattung']),
    ('https://33bots.de/roboter-mieten-preise.html', 200, ['https://33bots.at/roboter-mieten-preise.html'], []),
    ('https://33bots.de/roboter-firmenfeier.html', 200, ['https://33bots.at/roboter-firmenfeier.html'], []),
    ('https://33bots.de/angebot-tag-der-offenen-tuer.html', 200, ['Tag der offenen Tür von 10 bis 16 Uhr'], ['zuverlässiger als jede Anzeige']),
    ('https://33bots.de/roboter-werbung-film.html', 200, ['Was das Set braucht'], ['Zuschauer erkennen CGI']),
    ('https://33bots.de/impressum.html', 200, ['meist innerhalb von 30 Minuten'], ['24 Werkstunden']),
    ('https://33bots.pl/', 200, ['Sprawdź termin i cenę'], []),
    ('https://33bots.lt/', 200, ['id="przeglad"'], []),
]

gotowe = {d: czekaj(u, z) for d, u, z in [
    ('de', 'https://33bots.de/roboter-fuer-eventagenturen.html', 'Was Sie Ihrem Kunden nicht versprechen sollten'),
    ('at', 'https://33bots.at/roboter-weihnachtsfeier.html', 'Der Dezember 2026 im Kalender')]}
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
for d in ('33bots.de', '33bots.at'):
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
