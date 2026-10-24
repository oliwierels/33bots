# llms.txt rynku: fakty o usłudze i spis stron z tytułami i opisami wziętymi z gotowych stron.
# Grupy stron jak w stopce (rynki.py), FAQ jak na stronie głównej — llms.txt nie może mówić czego innego niż strona.
# Użycie: python3 buduj_llms.py lt /home/user/litwa-strona
import html
import re
import sys
from pathlib import Path

from rynki import RYNKI, KRAJE_LT

FAKTY = {
    'lt': {
        'domena': '33bots.lt',
        'naglowek': '33bots — humanoidinių robotų nuoma renginiams Lietuvoje',
        'santrauka': ('33bots nuomoja humanoidinį robotą Unitree G1 renginiams, parodoms, konferencijoms, įmonių šventėms ir '
                      'vestuvėms visoje Lietuvoje — visada su sertifikuotu operatoriumi, scenarijumi ir ženklinimu. Robotas gali '
                      'pasitikti svečius, vesti programos dalį kaip robotas vedėjas, šokti ir būti renginio fotozona. '
                      f'Daugiau nei 40 renginių penkiose šalyse: {KRAJE_LT}.'),
        'fakty': [
            'Kaina: visa renginio diena — nuo 2 100 € be PVM; galutinė suma priklauso nuo renginio vietos ir trukmės',
            'Trumpesnis pasirodymas (kelios valandos): kaina individuali, visada mažesnė nei visos dienos',
            'Nuo dviejų renginio dienų: −15 % kiekvienai dienai',
            'Į kainą įeina: sertifikuotas operatorius, atvykimas visoje Lietuvoje, ženklinimas (logotipas ir QR kodas), '
            'scenarijaus derinimas, civilinės atsakomybės draudimas',
            'Rezervacija be avanso, sąskaita tik po renginio',
            'Robotas: Unitree G1 — 132 cm, 35 kg, 23 laisvės laipsniai, iki 2 m/s, LiDAR ir kompiuterinė rega',
            'Kalba lietuviškai ir bet kuria kita kalba, renginio metu perjungia kalbas',
            'Vietoje reikia: maždaug 2×2 m laisvos vietos ir 230 V lizdo; operatorius pasiruošia per 30–45 min.',
            'Atsakymas į užklausą per 24 darbo valandas, dažniausiai tą pačią dieną',
            'Kontaktai: kontakt@33bots.lt',
            'Kalbų versijos: lietuvių (https://33bots.lt), lenkų (https://33bots.pl), vokiečių (https://33bots.de), '
            'austriška (https://33bots.at)',
        ],
        'naglowki': {'artykuly': 'Kiti renginių gido puslapiai', 'miasta': 'Miestai', 'inne': 'Kiti puslapiai',
                     'faq': 'Dažni klausimai', 'fakty': 'Pagrindiniai faktai'},
    },
}

rynek, repo = sys.argv[1], Path(sys.argv[2])
f, r = FAKTY[rynek], RYNKI[rynek]
baza = f'https://{f["domena"]}/'


def czysty(t):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', t))).strip()


def strona(plik):
    s = (repo / plik).read_text(encoding='utf-8')
    tytul = czysty(re.search(r'<title>([^<]*)</title>', s).group(1))
    tytul = re.sub(r'\s*\|\s*33bots$', '', tytul)
    opis = re.search(r'<meta name="description" content="([^"]*)"', s)
    return tytul, czysty(opis.group(1)) if opis else ''


def wiersz(plik):
    tytul, opis = strona(plik)
    adres = baza if plik == 'index.html' else baza + plik
    return f'- [{tytul}]({adres})' + (f' — {opis}' if opis else '')


wypisane = {'index.html', '404.html'}
grupy = []
for tytul, linki in r['stopka_kolumny'] + ([r['stopka_poradnik']] if r.get('stopka_poradnik') else []):
    pliki = [p for p, _ in linki if p not in wypisane and (repo / p).exists()]
    wypisane.update(pliki)
    if pliki:
        grupy.append((tytul, pliki))
wszystkie = sorted(p.name for p in repo.glob('*.html'))
# Pozostałe gidy i artykuły w kolejności spisu bloga (blog.html), potem reszta wpisów blog-*.
spis = (repo / 'blog.html').read_text(encoding='utf-8') if (repo / 'blog.html').exists() else ''
spis = spis[spis.find('<main'):spis.find('</main>')]
artykuly = []
for p in re.findall(r'<a href="([a-z0-9-]+\.html)"', spis) + [p for p in wszystkie if p.startswith('blog-')]:
    if p not in wypisane and p not in artykuly and (repo / p).exists():
        artykuly.append(p)
wypisane.update(artykuly)
miasta = [f'{r.get("miasta_prefiks", "roboter-mieten-")}{k}.html' for k, _ in r['miasta']]
miasta = [p for p in miasta if (repo / p).exists() and p not in wypisane]
wypisane.update(miasta)
inne = [p for p in wszystkie if p not in wypisane and 'noindex' not in (repo / p).read_text(encoding='utf-8')[:6000]]

n = f['naglowki']
czesci = [f'# {f["naglowek"]}', '', '> ' + f['santrauka'], '', f'## {n["fakty"]}', '']
czesci += [f'- {x}' for x in f['fakty']]
czesci += ['', f'- [{strona("index.html")[0]}]({baza})']
for tytul, pliki in grupy:
    czesci += ['', f'## {tytul}', ''] + [wiersz(p) for p in pliki]
if artykuly:
    czesci += ['', f'## {n["artykuly"]}', ''] + [wiersz(p) for p in artykuly]
if miasta:
    czesci += ['', f'## {n["miasta"]}', ''] + [wiersz(p) for p in miasta]
if inne:
    czesci += ['', f'## {n["inne"]}', ''] + [wiersz(p) for p in inne]
czesci += ['', f'## {n["faq"]}', ''] + [f'- {czysty(q)} {czysty(a)}' for q, a in r['faq']]
(repo / 'llms.txt').write_text('\n'.join(czesci) + '\n', encoding='utf-8')
print(f'{repo}/llms.txt: grup {len(grupy)}, artykułów {len(artykuly)}, miast {len(miasta)}, innych {len(inne)}')
