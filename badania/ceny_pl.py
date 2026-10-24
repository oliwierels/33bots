# Ceny atrakcji eventowych w Polsce ze stron publicznych: pobiera strony z listy, zdejmuje HTML
# i wypisuje zdania z kwotami w zł (do poradników .pl). Uruchamiane z GitHub Actions. Tylko odczyt.
import html
import re
import time
import urllib.request

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
ADRESY = [
    'https://cenauslug.pl/przewodnik/atrakcje-eventowe-wizualne-i-pokazy-artystyczne',
    'https://cenauslug.pl/przewodnik/wynajem-food-truckow-i-wozkow-gastronomicznych',
    'https://cenauslug.pl/przewodnik/catering-firmowy-eventowy-i-finger-food',
    'https://cenauslug.pl/przewodnik/uslugi-barmanskie-i-mobilne-bary',
    'https://cenauslug.pl/podroze-sport-i-rozrywka/animator-dla-dzieci-na-weselu',
    'https://cenauslug.pl/podroze-sport-i-rozrywka/pokaz-iluzjonisty-na-imprezie-firmowej',
    'https://cenauslug.pl/podroze-sport-i-rozrywka/wynajem-profesjonalnej-fotobudki-360',
    'https://cenauslug.pl/poradniki/fotobudka-360-cena-to-nie-wszystko-sprawdz-jak-madrze-wybrac-oferte-i-uniknac-5-pulapek',
    'https://cenauslug.pl/firma-i-biuro/wynajem-mobilnego-kasyna-na-impreze',
    'https://cenauslug.pl/poradniki/ile-kosztuje-wesele-dla-100-osob-kompletny-cennik-sala-fotograf-dj-catering',
    'https://cenauslug.pl/przewodnik/organizacja-wesel-i-poprawin',
    'https://cenauslug.pl/gastronomia-catering-i-eventy/obsluga-cateringowa-eventu-firmowego-50-osob',
    'https://kb.pl/ceny/imprezy-okolicznosciowe/cena-dj-lub-zespolu-na-wesele-sprawdzamy-aktualne-ceny-na-rynku/',
    'https://kb.pl/ceny/imprezy-okolicznosciowe/cena-fotobudki-zobacz-jaka-jest-cena-wynajmu-fotobudki/',
    'https://kb.pl/ceny/imprezy-okolicznosciowe/cennik-cateringu-zobacz-ile-kosztuja-rozne-wersje-cateringu-w-twojej-okolicy/',
    'https://aleo.com/pl/porady/dj-na-wesele/',
    'https://aleo.com/pl/porady/dj-na-impreze/',
    'https://www.eska.pl/news/ile-kosztuje-wesele-w-2026-roku-tyle-pary-mlode-wydadza-na-przyjecie-w-polsce-aa-XSKm-ypYP-GNao.html',
    'https://biznes.interia.pl/finanse/news-koszt-organizacji-wesela-w-2026-roku-zaplanuj-budzet-unikaja,nId,23478307',
    'https://freenance.io/budzetowanie/budzet-na-slub-2026/',
    'https://www.polsatnews.pl/wiadomosc/2026-05-26/koperta-na-wesele-w-2026-roku-mocno-urosla-ile-wypada-dac-rodzinie-a-ile-znajomym/',
    'https://www.wroclaw.pl/dla-mieszkanca/trendy-slubne-jaki-jest-koszt-wesela-ile-kosztuje-zespol-weselny',
    'https://forsal.pl/artykuly/569720,firmy-oszczedzaja-na-firmowych-przyjeciach-wigilijnych.html',
    'https://www.podatki.biz/artykuly/wigilia-firmowa-moze-byc-kosztem-podatkowym_34_42965.htm',
]
# Dodatkowe zapytania do OLX/Oferteo nie są potrzebne — to ogłoszenia, nie przewodniki.


def tekst(s):
    s = re.sub(r'<(script|style|noscript)\b.*?</\1>', ' ', s, flags=re.S | re.I)
    s = re.sub(r'<br\s*/?>|</(p|div|li|h\d|tr|td|th)>', '\n', s, flags=re.I)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s)
    return re.sub(r'[ \t\xa0]+', ' ', s)


for u in ADRESY:
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA, 'Accept-Language': 'pl-PL,pl;q=0.9'}), timeout=40) as r:
            s = r.read().decode('utf-8', 'replace'); kod = r.status
    except Exception as e:  # noqa: BLE001
        print(f'\n### {u}\nBŁĄD: {e}'); continue
    t = tekst(s)
    tytul = re.search(r'<title>([^<]*)', s)
    print(f'\n### {u}\nTYTUŁ: {html.unescape(tytul.group(1)).strip() if tytul else "?"} (HTTP {kod}, {len(t)} znaków)')
    data = re.findall(r'(20\d\d-\d\d-\d\d|\d{1,2}\.\d{1,2}\.20\d\d|\d{1,2} (?:stycznia|lutego|marca|kwietnia|maja|czerwca|lipca|sierpnia|września|października|listopada|grudnia) 20\d\d)', s)
    if data:
        print('DATY W KODZIE:', ', '.join(dict.fromkeys(data[:6])))
    zdania = []
    for linia in t.split('\n'):
        linia = linia.strip()
        if re.search(r'\d\s*(zł|PLN|złot)', linia) and len(linia) > 25:
            zdania.append(linia[:420])
    widziane = set()
    for z in zdania:
        if z not in widziane:
            widziane.add(z); print('-', z)
    print(f'(zdań z kwotami: {len(widziane)})')
    time.sleep(1.5)
