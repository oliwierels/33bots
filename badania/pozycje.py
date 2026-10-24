# Pozycje 33bots w Google, Bing i DuckDuckGo dla fraz z czterech rynków oraz liczba zaindeksowanych
# stron. Uruchamiane z GitHub Actions (sesja Claude nie ma dostępu do internetu). Tylko odczyt,
# ok. 150 zapytań z odstępami. Wynik: tabele w logu.
import base64
import html
import re
import time
import urllib.error
import urllib.parse
import urllib.request

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
RYNKI = {
    'pl': dict(domena='33bots.pl', hl='pl', gl='pl', cc='PL', jezyk='pl-PL', ddg='pl-pl', frazy=[
        'wynajem robota humanoidalnego', 'robot humanoidalny na event', 'robot na event', 'robot na targi',
        'robot na konferencję', 'robot na imprezę firmową', 'atrakcje na event firmowy', 'atrakcje na imprezę firmową',
        'nowoczesne atrakcje eventowe', 'atrakcje eventowe', 'atrakcje na event', 'robot na wesele', 'robot na dni miasta',
        'robot konferansjer', 'wynajem robota cena', 'robot do wynajęcia', 'atrakcje na wigilię firmową', 'pomysły na imprezę firmową']),
    'de': dict(domena='33bots.de', hl='de', gl='de', cc='DE', jezyk='de-DE', ddg='de-de', frazy=[
        'roboter mieten event', 'humanoider roboter mieten', 'roboter für events mieten', 'roboter mieten messe',
        'roboter weihnachtsfeier', 'weihnachtsfeier ideen', 'weihnachtsfeier ideen firma', 'weihnachtsfeier spiele',
        'firmenfeier ideen', 'teambuilding ideen', 'event attraktionen', 'attraktionen mieten', 'showact buchen',
        'messestand ideen', 'hochzeitsspiele', 'fotobox mieten', 'betriebsveranstaltung 110 euro', 'unitree g1 mieten',
        'roboter moderator event', 'sommerfest ideen firma', 'humanoiden roboter kaufen', 'event planen checkliste']),
    'at': dict(domena='33bots.at', hl='de', gl='at', cc='AT', jezyk='de-AT', ddg='at-de', frazy=[
        'roboter mieten österreich', 'roboter mieten wien', 'humanoider roboter mieten österreich',
        'roboter für events österreich', 'roboter weihnachtsfeier wien']),
    'lt': dict(domena='33bots.lt', hl='lt', gl='lt', cc='LT', jezyk='lt-LT', ddg='lt-lt', frazy=[
        'robotų nuoma renginiams', 'humanoidinis robotas nuoma', 'robotas renginiams', 'pramogos renginiams',
        'atrakcijos renginiams', 'renginių vedėjas', 'kalėdinio vakarėlio idėjos', 'įmonės renginio organizavimas',
        'fotobūdelė nuoma', 'vestuvių pramogos', 'gimtadienio idėjos', 'robotas vedėjas', 'parodos stendo idėjos',
        'renginio idėjos', 'robotas šokėjas renginiams']),
}
# Czy Google zaindeksował już nowe strony (po IndexNow i wdrożeniach z 24.10).
INDEKS = ['https://33bots.de/weihnachtsfeier-ideen.html', 'https://33bots.de/betriebsveranstaltung-steuer.html',
          'https://33bots.de/event-attraktionen.html', 'https://33bots.de/hochzeitsspiele.html', 'https://33bots.de/blog.html',
          'https://33bots.lt/renginio-idejos.html', 'https://33bots.lt/pramogos-renginiams.html',
          'https://33bots.lt/kaledinio-vakarelio-idejos.html', 'https://33bots.pl/blog-atrakcje-eventowe.html']
q = urllib.parse.quote_plus
blokady = {'google': 0, 'bing': 0, 'ddg': 0}


def pobierz(url, naglowki=None, jezyk='de-DE'):
    n = {'User-Agent': UA, 'Accept-Language': f'{jezyk},{jezyk[:2]};q=0.8,en;q=0.5', 'Accept': 'text/html,*/*;q=0.8'}
    n.update(naglowki or {})
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=n), timeout=40) as r:
            return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'replace')[:3000]
    except Exception as e:  # noqa: BLE001
        return 0, str(e)


def domena_z(u):
    return urllib.parse.urlparse(u).netloc.lower().removeprefix('www.')


def google(fraza, r):
    url = f'https://www.google.com/search?q={q(fraza)}&hl={r["hl"]}&gl={r["gl"]}&num=20&pws=0&gbv=1'
    kod, s = pobierz(url, {'Cookie': 'CONSENT=YES+cb; SOCS=CAISHAgBEhJnd3NfMjAyMzA4MTAtMF9SQzIaAmRlIAEaBgiA_LyaBg'}, r['jezyk'])
    if kod != 200 or 'unusual traffic' in s or '/sorry/' in s:
        blokady['google'] += 1
        return None, f'kod {kod}'
    linki = []
    for m in re.finditer(r'href="/url\?q=(https?://[^&"]+)', s):
        u = html.unescape(urllib.parse.unquote(m.group(1)))
        d = domena_z(u)
        if 'google' in d or 'googleusercontent' in d or 'youtube.com/redirect' in u:
            continue
        if u not in linki:
            linki.append(u)
    if not linki:
        for m in re.finditer(r'<a href="(https?://[^"]+)"[^>]*>(?:<br>)?<h3', s):
            u = html.unescape(m.group(1))
            if 'google' not in domena_z(u) and u not in linki:
                linki.append(u)
    liczba = re.search(r'([\d][\d\s.,\xa0]*)\s*(?:Ergebnisse|results|wynik|rezultat)', s)
    return linki, (liczba.group(1).strip() if liczba else '?')


def bing(fraza, r):
    url = f'https://www.bing.com/search?q={q(fraza)}&cc={r["cc"]}&setlang={r["hl"]}&count=20'
    kod, s = pobierz(url, None, r['jezyk'])
    if kod != 200:
        blokady['bing'] += 1
        return None, f'kod {kod}'
    linki = []
    for m in re.finditer(r'<li class="b_algo".*?<h2>\s*<a[^>]*href="([^"]+)"', s, re.S):
        u = html.unescape(m.group(1))
        if '/ck/a?' in u:
            mm = re.search(r'[&?]u=a1([A-Za-z0-9_-]+)', u)
            if mm:
                b = mm.group(1)
                try:
                    u = base64.urlsafe_b64decode(b + '=' * (-len(b) % 4)).decode('utf-8', 'replace')
                except Exception:  # noqa: BLE001
                    pass
        if u not in linki:
            linki.append(u)
    liczba = re.search(r'class="sb_count"[^>]*>([^<]*)<', s)
    return linki, (liczba.group(1).strip() if liczba else '?')


def ddg(fraza, r):
    url = f'https://html.duckduckgo.com/html/?q={q(fraza)}&kl={r["ddg"]}'
    kod, s = pobierz(url, None, r['jezyk'])
    if kod != 200:
        blokady['ddg'] += 1
        return None, f'kod {kod}'
    linki = []
    for m in re.finditer(r'class="result__a"[^>]*href="([^"]+)"', s):
        u = html.unescape(m.group(1))
        mm = re.search(r'uddg=([^&]+)', u)
        if mm:
            u = urllib.parse.unquote(mm.group(1))
        if 'duckduckgo.com' in domena_z(u):
            continue
        if u not in linki:
            linki.append(u)
    return linki, ''


def pozycja(linki, domena):
    if linki is None:
        return '—', ''
    for i, u in enumerate(linki, 1):
        if domena_z(u).endswith(domena):
            return str(i), urllib.parse.urlparse(u).path or '/'
    return f'>{len(linki)}' if linki else '0 wyników', ''


def top3(linki, domena):
    if not linki:
        return ''
    inne = []
    for u in linki:
        d = domena_z(u)
        if not d.endswith(domena) and d not in inne:
            inne.append(d)
    return ', '.join(inne[:3])


print('Pozycje 33bots — Google (gl/hl rynku, bez personalizacji), Bing (cc rynku), DuckDuckGo (region rynku).')
print('Uwaga: zapytania idą z serwera w USA, więc Google lokalne może się nieco różnić od tego, co widzi klient w kraju.\n')
for kod, r in RYNKI.items():
    print(f'## {r["domena"]}\n')
    print('| fraza | Google | Bing | DDG | nasza strona (Google/Bing) | top 3 Google (bez nas) |')
    print('|---|---|---|---|---|---|')
    for fraza in r['frazy']:
        g, _ = google(fraza, r); time.sleep(5)
        b, _ = bing(fraza, r); time.sleep(2)
        d, _ = ddg(fraza, r); time.sleep(2)
        pg, sg = pozycja(g, r['domena']); pb, sb = pozycja(b, r['domena']); pd, _ = pozycja(d, r['domena'])
        strona = sg or sb
        print(f'| {fraza} | {pg} | {pb} | {pd} | {strona} | {top3(g if g else b, r["domena"])} |')
    gi, lg = google(f'site:{r["domena"]}', r); time.sleep(5)
    bi, lb = bing(f'site:{r["domena"]}', r); time.sleep(2)
    print(f'\nIndeksacja site:{r["domena"]} — Google: {lg} (na 1. stronie {len(gi) if gi else "—"} adresów), Bing: {lb}\n')

print('## Czy Google ma już nowe strony\n')
for u in INDEKS:
    sciezka = urllib.parse.urlparse(u)
    r = RYNKI[sciezka.netloc.split('.')[-1]]
    g, _ = google(f'site:{u}', r); time.sleep(5)
    print(f'- {u}: {"TAK" if g and any(domena_z(x).endswith(r["domena"]) for x in g) else ("NIE" if g is not None else "blokada")}')

print(f'\nBlokady/odmowy: {blokady}')
