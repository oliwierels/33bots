# Podpowiedzi wyszukiwarek dla Niemiec: co ludzie wpisują, szukając atrakcji na eventy, wesela, firmowe imprezy.
# Google (client=chrome — z oceną trafności, hl=de, gl=de) i Bing (rynek de-DE). Wynik: badania/wyniki/podpowiedzi_de.json i .txt
import json, time, urllib.parse, urllib.request, os, random

FRAZY = """
event attraktionen
eventattraktionen
attraktionen für events
attraktion firmenfeier
firmenevent ideen
firmenfeier ideen
betriebsfeier ideen
mitarbeiterevent ideen
mitarbeiterfest
firmenjubiläum ideen
weihnachtsfeier ideen
weihnachtsfeier firma ideen
weihnachtsfeier programm
weihnachtsfeier spiele
weihnachtsfeier mitarbeiter
weihnachtsfeier location
sommerfest ideen
sommerfest firma
sommerfest attraktionen
teambuilding ideen
teamevent ideen
teamevent
teambuilding
kick off veranstaltung ideen
incentive ideen
eventagentur
event planen
firmenfeier planen
tagung organisieren
konferenz organisieren
messestand ideen
messestand attraktion
besucher messestand
messe besucher anlocken
messe give aways
tag der offenen tür ideen
eröffnung ideen
geschäftseröffnung ideen
eröffnungsfeier
produktlaunch event
stadtfest attraktionen
stadtfest organisieren
vereinsfest ideen
straßenfest ideen
showact buchen
showacts für events
walking act
stelzenläufer
feuershow
feuershow hochzeit
feuershow kosten
zauberer buchen
zauberer hochzeit
zauberer kosten
close up zauberer
comedian buchen
akrobatik show
lasershow mieten
drohnenshow
drohnenshow kosten
feuerwerk hochzeit
feuerwerk kosten
lichtshow
tänzer buchen
tanzshow buchen
sängerin hochzeit
saxophonist hochzeit
hochzeitsband
band hochzeit
coverband buchen
dj buchen
dj hochzeit
dj hochzeit kosten
dj firmenfeier
moderator buchen
eventmoderator
moderator hochzeit
moderator kosten
trauredner
karikaturist
schnellzeichner
live painting hochzeit
ballonkünstler
kinderschminken
fotobox mieten
fotobox hochzeit
fotobox kosten
photobooth mieten
360 grad fotobox
spiegel fotobox
magic mirror fotobox
hüpfburg mieten
hüpfburg kosten
eventverleih
partyverleih
karaoke mieten
karaoke anlage mieten
vr brille mieten
casino mieten
casino abend
krimidinner
escape room teamevent
popcornmaschine mieten
zuckerwattemaschine mieten
schokobrunnen mieten
candybar hochzeit
cocktailbar mieten
mobile bar mieten
food truck mieten
eiswagen mieten
glücksrad mieten
torwand mieten
bullriding mieten
sumo anzüge mieten
menschenkicker mieten
kinderprogramm hochzeit
kinderbetreuung hochzeit
hochzeit ideen
hochzeitsspiele
hochzeitsspiele lustig
hochzeitsspiele ohne brautpaar
hochzeit unterhaltung
hochzeit programmpunkte
hochzeit ablauf
tagesablauf hochzeit
hochzeit kosten
was kostet eine hochzeit
hochzeit budget
hochzeitsplaner
hochzeitsplaner kosten
polterabend ideen
jga ideen
junggesellenabschied ideen
junggesellinnenabschied ideen
hochzeitstanz
hochzeitsfotograf kosten
freie trauung
geburtstag ideen
30. geburtstag ideen
40. geburtstag ideen
50. geburtstag ideen
60. geburtstag ideen
18. geburtstag ideen
geburtstag feiern ideen
überraschungsparty
mottoparty ideen
kindergeburtstag ideen
kindergeburtstag spiele
kindergeburtstag ab 10
kindergeburtstag zuhause
partyspiele
jubiläum feiern ideen
goldene hochzeit ideen
silberhochzeit ideen
abiball ideen
abifeier
abschlussfeier ideen
abschiedsfeier kollegen
abschied ruhestand ideen
taufe feier ideen
roboter mieten
humanoider roboter mieten
roboter für events
roboter hochzeit
roboter show
ki roboter
roboter messe
roboter tanzen
roboterhund mieten
humanoider roboter kaufen
humanoider roboter preis
""".strip().splitlines()

ROZWIJANE = [
    'event attraktionen', 'weihnachtsfeier ideen', 'firmenfeier ideen', 'teambuilding ideen', 'sommerfest ideen',
    'fotobox mieten', 'hochzeitsspiele', 'hochzeit ideen', 'jga ideen', 'geburtstag ideen', 'kindergeburtstag ideen',
    'dj hochzeit', 'zauberer', 'feuershow', 'showact', 'moderator', 'hüpfburg mieten', 'messestand', 'roboter mieten',
    'attraktionen mieten', 'hochzeit kosten', 'polterabend', 'abiball', 'mitarbeiterevent', 'weihnachtsfeier',
]
LITERY = list('abcdefghijklmnopqrstuvwxyzäöü')

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'


def pobierz(url, proby=4):
    for i in range(proby):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'de-DE,de;q=0.9'})
            with urllib.request.urlopen(req, timeout=15) as r:
                return r.read().decode('utf-8', 'replace')
        except Exception as e:
            time.sleep(2 * (i + 1) + random.random())
            blad = e
    print('BŁĄD', url, blad)
    return None


def google(q):
    t = pobierz('https://suggestqueries.google.com/complete/search?client=chrome&hl=de&gl=de&q=' + urllib.parse.quote(q))
    if not t:
        return []
    try:
        d = json.loads(t)
        sug = d[1]
        rel = d[4].get('google:suggestrelevance', [0] * len(sug)) if len(d) > 4 and isinstance(d[4], dict) else [0] * len(sug)
        typ = d[4].get('google:suggesttype', [''] * len(sug)) if len(d) > 4 and isinstance(d[4], dict) else [''] * len(sug)
        return [[s, r] for s, r, ty in zip(sug, rel, typ) if ty in ('QUERY', '')]
    except Exception as e:
        print('JSON?', q, e, t[:200])
        return []


def bing(q):
    t = pobierz('https://api.bing.com/osjson.aspx?market=de-DE&query=' + urllib.parse.quote(q))
    try:
        return json.loads(t)[1] if t else []
    except Exception:
        return []


wynik = {'google': {}, 'bing': {}, 'rozwiniecia': {}}
for i, q in enumerate(FRAZY):
    wynik['google'][q] = google(q)
    wynik['bing'][q] = bing(q)
    time.sleep(0.35)
    if i % 25 == 0:
        print(f'frazy: {i}/{len(FRAZY)}', flush=True)
for j, q in enumerate(ROZWIJANE):
    for l in LITERY:
        s = google(f'{q} {l}')
        if s:
            wynik['rozwiniecia'][f'{q} {l}'] = s
        time.sleep(0.3)
    print(f'rozwinięcia: {j + 1}/{len(ROZWIJANE)}', flush=True)

os.makedirs('badania/wyniki', exist_ok=True)
json.dump(wynik, open('badania/wyniki/podpowiedzi_de.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
# Zbiorcza lista unikalnych podpowiedzi z liczbą wystąpień i najwyższą trafnością Google
licz = {}
for zrodlo in ('google', 'rozwiniecia'):
    for q, lista in wynik[zrodlo].items():
        for s, r in lista:
            a = licz.setdefault(s, [0, 0])
            a[0] += 1
            a[1] = max(a[1], r)
for q, lista in wynik['bing'].items():
    for s in lista:
        a = licz.setdefault(s, [0, 0])
        a[0] += 1
with open('badania/wyniki/podpowiedzi_de.txt', 'w', encoding='utf-8') as f:
    for s, (n, r) in sorted(licz.items(), key=lambda x: (-x[1][0], -x[1][1], x[0])):
        f.write(f'{n}\t{r}\t{s}\n')
print('unikalnych podpowiedzi:', len(licz))
print('puste frazy Google:', [q for q, l in wynik['google'].items() if not l])
