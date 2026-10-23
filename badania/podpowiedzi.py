# Podpowiedzi wyszukiwarek dla Litwy: co ludzie wpisują, szukając atrakcji na eventy, wesela i imprezy.
# Google (client=chrome — z oceną trafności) i Bing (rynek lt-LT). Wynik: badania/wyniki/podpowiedzi.json i .txt
import json, time, urllib.parse, urllib.request, os, random

FRAZY = """
pramogos renginiams
renginių pramogos
pramogos įmonės renginiams
pramogos įmonių renginiams
pramogos šventėms
pramogos vestuvėms
vestuvių pramogos
pramogos vestuvėse
pramogos gimtadieniui
pramogos suaugusiems
pramogos vaikams
pramogos jubiliejui
netradicinės pramogos
originalios pramogos
išskirtinės pramogos
atrakcionai renginiams
atrakcionai vestuvėms
atrakcionų nuoma
pramogų nuoma
atrakcijos renginiams
renginio idėjos
šventės idėjos
vestuvių idėjos
gimtadienio idėjos
jubiliejaus idėjos
įmonės renginio idėjos
kalėdinio vakarėlio idėjos
kalėdinis vakarėlis
kalėdinis vakarėlis įmonei
kalėdiniai renginiai įmonėms
kalėdinių vakarėlių organizavimas
įmonės kalėdinis vakarėlis
komandos formavimas
komandos formavimo renginiai
komandos formavimo idėjos
team building
įmonės šventė
įmonės renginiai
įmonių renginių organizavimas
renginių organizavimas
renginių agentūra
darbuotojų šventė
vasaros šventė įmonei
įmonės gimtadienis
konferencijos organizavimas
konferencijų pramogos
parodos stendas
parodos stendo idėjos
produkto pristatymas renginys
atidarymo šventė
parduotuvės atidarymas
miesto šventė
festivalis
vedėjas
vedėjas vestuvėms
vestuvių vedėjas
vestuvių vedėjai
vestuvių vedėjas kaina
renginių vedėjas
renginio vedėjas
šventės vedėjas
vedėjas gimtadieniui
vedėjas jubiliejui
vedėjas įmonės renginiui
kalėdinio vakarėlio vedėjas
vedėjas ir dj
dj vestuvėms
dj nuoma
muzikantai vestuvėms
gyva muzika vestuvėms
vestuvių muzikantai
vestuvių žaidimai
vestuvių žaidimai svečiams
vestuvių programa
vestuvių scenarijus
vestuvių tradicijos
jaunųjų sutikimas
antroji vestuvių diena
vestuvių sodyba
vestuvių planavimas
vestuvių kaina
vestuvių biudžetas
pirmasis šokis
sunkūs dūmai
sunkūs dūmai vestuvėms
fotobūdelė
fotobūdelės nuoma
fotobūdelė vestuvėms
foto būdelė
fotobūdelė kaina
360 fotobūdelė
360 video platforma
magic mirror
veidrodis fotobūdelė
fotosienelė
foto zona
fotografas vestuvėms
šokėjai renginiams
šokių šou
ugnies šou
burbulų šou
iliuzionistas
magas renginiams
fokusininkas
sniego šou
pripučiami batutai
batutų nuoma
cukraus vata
saldainių baras
saldus stalas
šokolado fontanas
kokteilių baras
barmenų šou
mobilus baras
karaoke nuoma
vr akinių nuoma
virtualios realybės pramogos
lazerių kovos
kazino vakarėlis
protmūšis įmonei
protmūšis
escape room
žaidimai renginiams
žaidimai įmonės vakarėliui
karikatūristas
gyvos skulptūros
klounas
animatoriai
animatoriai vaikams
vaikų gimtadienis
vaikų gimtadienio pramogos
vaikų šventės organizavimas
gimtadienio šventė
50 metų jubiliejus
krikštynos
mergvakaris
mergvakario idėjos
bernvakaris
bernvakario idėjos
šimtadienis
šimtadienio idėjos
išleistuvės
abiturientų išleistuvės
išleistuvių pramogos
fejerverkai
šviesų šou
dronų šou
lazerių šou
hologramos
robotas
robotai
robotas renginiams
robotų nuoma
roboto nuoma
humanoidinis robotas
roboto šou
šokantis robotas
robotas šuo
dirbtinis intelektas renginiuose
""".strip().splitlines()

ROZWIJANE = [
    'pramogos renginiams', 'pramogos vestuvėms', 'vestuvių vedėjas', 'renginių vedėjas', 'vedėjas',
    'fotobūdelė', 'fotobūdelės nuoma', 'atrakcionai', 'atrakcionų nuoma', 'pramogos įmonės renginiams',
    'kalėdinio vakarėlio', 'kalėdinis vakarėlis', 'komandos formavimo', 'gimtadienio pramogos', 'vaikų gimtadienio',
    'vestuvių idėjos', 'vestuvių žaidimai', 'jubiliejaus', 'šventės idėjos', 'renginio idėjos', 'robotas',
    'robotų nuoma', 'pramogos', 'šimtadienio', 'išleistuvių', 'mergvakario', 'įmonės renginiai', 'renginių organizavimas',
]
LITERY = list('aąbcčdeęėfghiįyjklmnoprsštuųūvzž')

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'


def pobierz(url, proby=4):
    for i in range(proby):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'lt-LT,lt;q=0.9'})
            with urllib.request.urlopen(req, timeout=15) as r:
                return r.read().decode('utf-8', 'replace')
        except Exception as e:
            time.sleep(2 * (i + 1) + random.random())
            blad = e
    print('BŁĄD', url, blad)
    return None


def google(q):
    t = pobierz('https://suggestqueries.google.com/complete/search?client=chrome&hl=lt&gl=lt&q=' + urllib.parse.quote(q))
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
    t = pobierz('https://api.bing.com/osjson.aspx?market=lt-LT&query=' + urllib.parse.quote(q))
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
json.dump(wynik, open('badania/wyniki/podpowiedzi.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
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
with open('badania/wyniki/podpowiedzi.txt', 'w', encoding='utf-8') as f:
    for s, (n, r) in sorted(licz.items(), key=lambda x: (-x[1][0], -x[1][1], x[0])):
        f.write(f'{n}\t{r}\t{s}\n')
print('unikalnych podpowiedzi:', len(licz))
print('puste frazy Google:', [q for q, l in wynik['google'].items() if not l])
