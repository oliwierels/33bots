# Podpowiedzi wyszukiwarek dla Polski: co ludzie wpisują, szukając atrakcji na eventy, wesela, imprezy firmowe.
# Google (client=chrome — z oceną trafności, hl=pl, gl=pl) i Bing (rynek pl-PL). Wynik: badania/wyniki/podpowiedzi_pl.json i .txt
import json, time, urllib.parse, urllib.request, os, random

FRAZY = """
atrakcje na event
atrakcje eventowe
atrakcje na event firmowy
atrakcje na imprezę firmową
atrakcje na imprezę integracyjną
atrakcje na integrację firmową
atrakcje na piknik firmowy
atrakcje na wigilię firmową
atrakcje na galę
atrakcje na konferencję
atrakcje na targi
atrakcje na stoisko targowe
jak przyciągnąć ludzi na stoisko
atrakcje na dni miasta
atrakcje na festyn
atrakcje na piknik rodzinny
atrakcje na dzień dziecka
atrakcje na otwarcie sklepu
atrakcje na wesele
atrakcje weselne
atrakcje na wesele dla gości
atrakcje na poprawiny
atrakcje na urodziny
atrakcje na urodziny dla dorosłych
atrakcje na 18 urodziny
atrakcje na 40 urodziny
atrakcje na 50 urodziny
atrakcje na urodziny dziecka
atrakcje na studniówkę
atrakcje na bal
atrakcje na andrzejki firmowe
atrakcje na sylwestra firmowego
nowoczesne atrakcje na event
nowoczesne atrakcje eventowe
technologiczne atrakcje na event
atrakcje vr na event
wynajem atrakcji na imprezy
wynajem atrakcji eventowych
wypożyczalnia atrakcji
impreza firmowa pomysły
pomysły na imprezę firmową
pomysł na imprezę firmową
pomysły na integrację firmową
integracja firmowa pomysły
integracja pracowników pomysły
wyjazd integracyjny pomysły
impreza integracyjna pomysły
wigilia firmowa pomysły
pomysły na wigilię firmową
wigilia firmowa atrakcje
wigilia firmowa program
wigilia firmowa zabawy
spotkanie wigilijne w firmie pomysły
impreza świąteczna w firmie
piknik firmowy pomysły
piknik firmowy atrakcje
piknik rodzinny firmowy
dzień dziecka w firmie pomysły
jubileusz firmy pomysły
jubileusz firmy atrakcje
gala firmowa pomysły
gala firmowa atrakcje
gala firmowa program
konferencja pomysły
konferencja atrakcje dla uczestników
jak urozmaicić konferencję
jak zorganizować imprezę firmową
jak zorganizować event firmowy
jak zorganizować event
organizacja eventów
organizacja imprez firmowych
agencja eventowa
event firmowy
impreza firmowa
eventy firmowe
team building pomysły
teambuilding pomysły
gry integracyjne dla pracowników
zabawy integracyjne dla dorosłych
zabawy na imprezę firmową
zabawy na wigilię firmową
konkursy na imprezę firmową
quiz na imprezę firmową
stoisko targowe pomysły
stoisko targowe atrakcje
jak wyróżnić stoisko na targach
gadżety na targi
hostessy na targi
otwarcie sklepu pomysły
otwarcie salonu pomysły
otwarcie firmy atrakcje
premiera produktu event
dni miasta atrakcje
dni miasta program
festyn pomysły
festyn atrakcje
piknik pomysły
imprezy plenerowe atrakcje
atrakcje plenerowe
show na event
pokaz na event
pokazy na imprezy firmowe
artyści na event
artyści na imprezy firmowe
występy na imprezy firmowe
występ artystyczny na galę
gwiazda na imprezę firmową
kabaret na imprezę firmową
iluzjonista na event
iluzjonista na imprezę firmową
iluzjonista na wesele
iluzjonista cena
pokaz iluzji
magik na imprezę
mentalista na event
pokaz ognia
pokaz ognia na wesele
pokaz ognia cena
fireshow
pokaz laserowy
pokaz laserowy cena
pokaz dronów
pokaz dronów cena
pokaz fajerwerków cena
pokaz pirotechniczny
pokaz tańca na event
tancerze na event
tancerze na wesele
akrobaci na event
pokaz akrobatyczny
szczudlarze
żywe posągi
mim na event
karykaturzysta na event
karykaturzysta na wesele
karykaturzysta cena
barman show
barman show cena
pokaz barmański
mobilny bar na event
mobilny bar na wesele
drink bar na wesele cena
dj na imprezę firmową
dj na event
dj na wesele
dj na wesele cena
wodzirej
wodzirej na wesele
wodzirej na wesele cena
wodzirej na imprezę firmową
konferansjer
konferansjer na event
konferansjer cena
prowadzący event
prowadzący galę
prowadzący imprezę firmową
zespół na wesele
zespół na wesele cena
zespół coverowy na event
zespół na imprezę firmową
saksofonista na wesele
saksofonista na event
skrzypaczka na wesele
fotobudka
fotobudka na wesele
fotobudka na wesele cena
fotobudka wynajem
fotobudka wynajem cena
fotobudka 360
fotobudka 360 cena
fotolustro
fotobudka na imprezę firmową
fotograf na event
fotograf na event firmowy cena
dmuchańce
dmuchańce wynajem
dmuchańce wynajem cena
dmuchany zamek wynajem
wynajem dmuchańców cena
zjeżdżalnia dmuchana wynajem
byk rodeo wynajem
piłkarzyki ludzkie wynajem
symulator vr wynajem
gogle vr na event
symulator rajdowy wynajem
symulator lotu wynajem
kasyno na imprezę
kasyno na imprezę firmową
mobilne kasyno
kasyno na wesele
escape room na event
escape room mobilny
quiz pubowy na imprezę firmową
karaoke wynajem
wata cukrowa wynajem
maszyna do popcornu wynajem
fontanna czekoladowa wynajem
candy bar na wesele
słodki stół na wesele
food truck na event
food truck na imprezę firmową
food truck na wesele
food truck na wesele cena
catering na imprezę firmową
catering na imprezę firmową cena
catering na event cena za osobę
ciężki dym na wesele
ciężki dym cena
fontanny iskier na wesele
napis love na wesele wynajem
animator dla dzieci
animator dla dzieci na wesele
animator dla dzieci cena
animacje dla dzieci na imprezę firmową
kącik dla dzieci na weselu
malowanie twarzy na imprezę
clown na urodziny
wesele pomysły
pomysły na wesele
zabawy weselne
zabawy na wesele
zabawy na wesele dla gości
zabawy weselne bez wodzireja
oczepiny zabawy
pierwszy taniec pomysły
harmonogram wesela
plan wesela
przebieg wesela
ile kosztuje wesele
ile kosztuje wesele 2026
koszt wesela
budżet weselny
wieczór panieński pomysły
wieczór kawalerski pomysły
poprawiny pomysły
urodziny pomysły
pomysły na urodziny
pomysły na urodziny dla dorosłych
pomysły na 30 urodziny
pomysły na 40 urodziny
pomysły na 50 urodziny
pomysły na 18 urodziny
impreza niespodzianka pomysły
pomysły na urodziny dziecka
urodziny dziecka atrakcje
urodziny dziecka w domu zabawy
studniówka pomysły
studniówka atrakcje
bal ósmoklasisty pomysły
bal gimnazjalny
komers pomysły
półmetek pomysły
pożegnanie pracownika pomysły
impreza pożegnalna pomysły
robot na event
robot na imprezę
robot humanoidalny
robot humanoidalny wynajem
wynajem robota
wynajem robota humanoidalnego
robot na wesele
robot na targi
robot na konferencję
robot konferansjer
robot tańczący
robot na stoisko
roboty na eventy
robot humanoidalny cena
robot humanoidalny kupić
pies robot wynajem
""".strip().splitlines()

ROZWIJANE = [
    'atrakcje na event', 'atrakcje na imprezę firmową', 'atrakcje na wesele', 'atrakcje na urodziny', 'atrakcje na dni miasta',
    'pomysły na imprezę firmową', 'wigilia firmowa', 'integracja firmowa', 'piknik firmowy', 'gala firmowa', 'stoisko targowe',
    'zabawy weselne', 'wesele pomysły', 'pomysły na urodziny', 'fotobudka', 'dmuchańce', 'iluzjonista', 'pokaz ognia',
    'wodzirej', 'dj na wesele', 'konferansjer', 'food truck', 'kasyno na imprezę', 'wynajem atrakcji', 'robot na event',
    'ile kosztuje wesele', 'studniówka', 'show na event',
]
LITERY = list('abcdefghijklmnopqrstuvwxyząćęłńóśźż')

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'


def pobierz(url, proby=4):
    for i in range(proby):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'pl-PL,pl;q=0.9'})
            with urllib.request.urlopen(req, timeout=15) as r:
                return r.read().decode('utf-8', 'replace')
        except Exception as e:
            time.sleep(2 * (i + 1) + random.random())
            blad = e
    print('BŁĄD', url, blad)
    return None


def google(q):
    t = pobierz('https://suggestqueries.google.com/complete/search?client=chrome&hl=pl&gl=pl&q=' + urllib.parse.quote(q))
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
    t = pobierz('https://api.bing.com/osjson.aspx?market=pl-PL&query=' + urllib.parse.quote(q))
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
json.dump(wynik, open('badania/wyniki/podpowiedzi_pl.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
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
with open('badania/wyniki/podpowiedzi_pl.txt', 'w', encoding='utf-8') as f:
    for s, (n, r) in sorted(licz.items(), key=lambda x: (-x[1][0], -x[1][1], x[0])):
        f.write(f'{n}\t{r}\t{s}\n')
print('unikalnych podpowiedzi:', len(licz))
print('puste frazy Google:', [q for q, l in wynik['google'].items() if not l])
