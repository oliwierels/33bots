#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Analityka 33bots: raporty i archiwum z Google Analytics 4, Search Console i Microsoft Clarity.

Klucze bierze wyłącznie ze zmiennych środowiska (ustawienia środowiska Claude Code w chmurze),
nigdy z repozytorium:
  GOOGLE_SA_JSON          treść klucza JSON konta usługi Google (jedna linia albo base64)
                          — alternatywnie GOOGLE_APPLICATION_CREDENTIALS ze ścieżką do pliku
  GA4_PROPERTY_ID         numer usługi GA4 (np. 123456789); bez niego bierze pierwszą dostępną
  CLARITY_API_TOKEN       token Data Export API z ustawień projektu Clarity
  BQ_DATASET              (opcjonalnie) projekt:zbiór w BigQuery na archiwum, np. 33bots-analityka:archiwum

Dane NIE trafiają do repozytorium (jest publiczne) ani do logów GitHub Actions (też publiczne).
Archiwum ląduje w katalogu poza repo (domyślnie ~/33bots-analityka-dane) i — jeśli ustawiono
BQ_DATASET — w BigQuery.

Przykłady:
  python3 scripts/analityka/analityka.py sprawdz
  python3 scripts/analityka/analityka.py ga4 --od 28daysAgo --wymiary sessionDefaultChannelGroup --metryki sessions,keyEvents
  python3 scripts/analityka/analityka.py gsc --witryna sc-domain:33bots.pl --od 2026-10-01 --wymiary query --limit 50
  python3 scripts/analityka/analityka.py clarity --dni 3 --wymiary URL
  python3 scripts/analityka/analityka.py archiwum            # GA4 od początku + GSC 16 mies. + Clarity 3 dni
  python3 scripts/analityka/analityka.py historia-zmian      # daty wdrożeń i zmienione strony (bez kluczy)
"""
import argparse
import base64
import csv
import datetime as dt
import gzip
import io
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.parse
from pathlib import Path

KORZEN = Path(__file__).resolve().parents[2]
DOMYSLNY_KATALOG = Path(os.environ.get('ANALITYKA_DANE', Path.home() / '33bots-analityka-dane'))
ZAKRESY = ['https://www.googleapis.com/auth/analytics.readonly',
           'https://www.googleapis.com/auth/webmasters.readonly']
WITRYNY_33BOTS = ['33bots.pl', '33bots.de', '33bots.at', '33bots.lt']
GALAZ_PRODUKCJI = 'claude/33bots-website-T0REs'


def blad(tekst, kod=1):
    print(f'BŁĄD: {tekst}', file=sys.stderr)
    sys.exit(kod)


# ——— uwierzytelnienie Google ———

def _zaladuj_biblioteki():
    try:
        import google.oauth2.service_account  # noqa: F401
        import requests  # noqa: F401
    except ImportError:
        print('Instaluję google-auth i requests (jednorazowo w tej sesji)…', file=sys.stderr)
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--quiet', '--user', 'google-auth>=2.30', 'requests>=2.31'],
                       check=True)
        import site
        sys.path.insert(0, site.getusersitepackages())


def info_klucza():
    surowe = os.environ.get('GOOGLE_SA_JSON', '').strip()
    if surowe:
        if not surowe.startswith('{'):
            try:
                surowe = base64.b64decode(surowe).decode('utf-8')
            except Exception:
                blad('GOOGLE_SA_JSON nie jest ani JSON-em, ani base64 z JSON-em.')
        try:
            return json.loads(surowe)
        except json.JSONDecodeError as e:
            blad(f'GOOGLE_SA_JSON: niepoprawny JSON ({e.msg}). Wklej cały plik klucza jako jedną linię.')
    sciezka = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if sciezka and Path(sciezka).exists():
        return json.loads(Path(sciezka).read_text(encoding='utf-8'))
    return None


_sesja = None


def sesja_google():
    """Sesja HTTP z tokenem konta usługi (tylko odczyt: GA4 i Search Console)."""
    global _sesja
    if _sesja is None:
        info = info_klucza()
        if not info:
            blad('Brak klucza Google. Dodaj zmienną GOOGLE_SA_JSON w ustawieniach środowiska i otwórz nową sesję.')
        _zaladuj_biblioteki()
        from google.oauth2 import service_account
        from google.auth.transport.requests import AuthorizedSession
        dane = service_account.Credentials.from_service_account_info(info, scopes=ZAKRESY)
        _sesja = AuthorizedSession(dane)
    return _sesja


def zapytanie(metoda, url, **kw):
    for proba in range(5):
        r = sesja_google().request(metoda, url, timeout=120, **kw)
        if r.status_code in (429, 500, 502, 503) and proba < 4:
            time.sleep(2 ** proba * 3)
            continue
        if r.status_code >= 400:
            try:
                tresc = r.json().get('error', {}).get('message', r.text[:400])
            except ValueError:
                tresc = r.text[:400]
            blad(f'{metoda} {url.split("?")[0]} → HTTP {r.status_code}: {tresc}')
        return r.json()


# ——— Google Analytics 4 (Data API v1beta, Admin API v1beta) ———

def ga4_uslugi():
    wynik, token = [], None
    while True:
        url = 'https://analyticsadmin.googleapis.com/v1beta/accountSummaries?pageSize=200'
        if token:
            url += '&pageToken=' + urllib.parse.quote(token)
        d = zapytanie('GET', url)
        for konto in d.get('accountSummaries', []):
            for u in konto.get('propertySummaries', []):
                wynik.append({'konto': konto.get('displayName', ''), 'usluga': u['property'].split('/')[-1],
                              'nazwa': u.get('displayName', '')})
        token = d.get('nextPageToken')
        if not token:
            return wynik


def ga4_id(podane=None):
    pid = podane or os.environ.get('GA4_PROPERTY_ID')
    if pid:
        return str(pid).replace('properties/', '')
    uslugi = ga4_uslugi()
    if not uslugi:
        blad('Konto usługi nie widzi żadnej usługi GA4. Dodaj jego e-mail w GA4 → Administracja → Zarządzanie dostępem (rola: Wyświetlający).')
    if len(uslugi) > 1:
        print(f'Uwaga: konto widzi {len(uslugi)} usługi GA4, biorę pierwszą ({uslugi[0]["nazwa"]}). Ustaw GA4_PROPERTY_ID.', file=sys.stderr)
    return uslugi[0]['usluga']


def ga4_raport(pid, od, do, wymiary, metryki, filtr_strony=None, limit=None):
    """Zwraca (nagłówki, wiersze). Stronicuje po 100 000 wierszy."""
    wiersze, przesuniecie = [], 0
    while True:
        cialo = {'dateRanges': [{'startDate': od, 'endDate': do}],
                 'dimensions': [{'name': w} for w in wymiary],
                 'metrics': [{'name': m} for m in metryki],
                 'limit': min(limit or 100000, 100000), 'offset': przesuniecie}
        if 'date' in wymiary:
            cialo['orderBys'] = [{'dimension': {'dimensionName': 'date'}}]
        if filtr_strony:
            cialo['dimensionFilter'] = {'filter': {'fieldName': 'pagePath', 'stringFilter': {'matchType': 'CONTAINS', 'value': filtr_strony}}}
        d = zapytanie('POST', f'https://analyticsdata.googleapis.com/v1beta/properties/{pid}:runReport', json=cialo)
        for r in d.get('rows', []):
            wiersze.append([v.get('value', '') for v in r.get('dimensionValues', [])] + [v.get('value', '') for v in r.get('metricValues', [])])
        przesuniecie += len(d.get('rows', []))
        if not d.get('rows') or przesuniecie >= int(d.get('rowCount', 0)) or (limit and przesuniecie >= limit):
            return wymiary + metryki, wiersze


RAPORTY_GA4 = {
    # nazwa: (wymiary, metryki) — dzienne, do archiwum i do porównań przed/po zmianach na stronie
    'ga4_ruch': (['date', 'hostName', 'sessionDefaultChannelGroup', 'sessionSource', 'sessionMedium', 'deviceCategory', 'country'],
                 ['sessions', 'totalUsers', 'newUsers', 'engagedSessions', 'userEngagementDuration', 'screenPageViews', 'keyEvents']),
    'ga4_wejscia': (['date', 'hostName', 'landingPage', 'sessionDefaultChannelGroup'],
                    ['sessions', 'engagedSessions', 'keyEvents', 'bounceRate']),
    'ga4_strony': (['date', 'hostName', 'pagePath'], ['screenPageViews', 'activeUsers', 'userEngagementDuration']),
    'ga4_zdarzenia': (['date', 'hostName', 'eventName'], ['eventCount', 'totalUsers', 'keyEvents']),
    'ga4_kampanie': (['date', 'sessionSourceMedium', 'sessionCampaignName'], ['sessions', 'engagedSessions', 'keyEvents']),
}


def ga4_poczatek(pid):
    d = zapytanie('GET', f'https://analyticsadmin.googleapis.com/v1beta/properties/{pid}')
    return d.get('createTime', '2015-08-14T00:00:00Z')[:10], d.get('displayName', '')


# ——— Search Console (searchAnalytics) ———

def gsc_witryny():
    d = zapytanie('GET', 'https://searchconsole.googleapis.com/webmasters/v3/sites')
    return [(s['siteUrl'], s.get('permissionLevel', '')) for s in d.get('siteEntry', [])]


def gsc_raport(witryna, od, do, wymiary, limit=None, typ='web'):
    url = f'https://searchconsole.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(witryna, safe="")}/searchAnalytics/query'
    wiersze, start = [], 0
    while True:
        cialo = {'startDate': od, 'endDate': do, 'dimensions': wymiary, 'type': typ,
                 'rowLimit': min(limit or 25000, 25000), 'startRow': start, 'dataState': 'all'}
        d = zapytanie('POST', url, json=cialo)
        porcja = d.get('rows', [])
        for r in porcja:
            wiersze.append(list(r.get('keys', [])) + [r['clicks'], r['impressions'], round(r['ctr'], 5), round(r['position'], 2)])
        start += len(porcja)
        if len(porcja) < cialo['rowLimit'] or (limit and start >= limit):
            return wymiary + ['clicks', 'impressions', 'ctr', 'position'], wiersze


def gsc_witryny_33bots():
    dostepne = [w for w, _ in gsc_witryny()]
    wybrane = [w for w in dostepne if any(d in w for d in WITRYNY_33BOTS)]
    if not wybrane:
        blad('Konto usługi nie ma dostępu do żadnej witryny 33bots w Search Console. Dodaj jego e-mail: Ustawienia → Użytkownicy i uprawnienia (Ograniczony).')
    # Gdy jest i usługa domeny, i prefiks URL, bierzemy domenę (pełniejsze dane).
    domeny = {w.split(':', 1)[1] for w in wybrane if w.startswith('sc-domain:')}
    return [w for w in wybrane if w.startswith('sc-domain:') or not any(d in w for d in domeny)]


# ——— Microsoft Clarity (Data Export API: 1–3 ostatnie dni, 10 zapytań dziennie na projekt) ———

def clarity(dni=1, wymiary=()):
    token = os.environ.get('CLARITY_API_TOKEN')
    if not token:
        blad('Brak CLARITY_API_TOKEN. Clarity → Ustawienia → Eksport danych → nowy token; dodaj go w ustawieniach środowiska.')
    _zaladuj_biblioteki()
    import requests
    parametry = {'numOfDays': max(1, min(3, int(dni)))}
    for i, w in enumerate(list(wymiary)[:3], 1):
        parametry[f'dimension{i}'] = w
    r = requests.get('https://www.clarity.ms/export-data/api/v1/project-live-insights', params=parametry,
                     headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}, timeout=60)
    if r.status_code >= 400:
        blad(f'Clarity → HTTP {r.status_code}: {r.text[:300]} (limit: 10 zapytań dziennie na projekt)')
    return r.json()


# ——— zapis ———

def wypisz(naglowki, wiersze, max_wierszy=60):
    print('\t'.join(naglowki))
    for w in wiersze[:max_wierszy]:
        print('\t'.join(str(x) for x in w))
    if len(wiersze) > max_wierszy:
        print(f'… i {len(wiersze) - max_wierszy} wierszy więcej (użyj --csv, żeby zapisać całość)')


def zapisz_csv(sciezka, naglowki, wiersze):
    sciezka = Path(sciezka)
    sciezka.parent.mkdir(parents=True, exist_ok=True)
    otworz = gzip.open if sciezka.suffix == '.gz' else open
    with otworz(sciezka, 'wt', encoding='utf-8', newline='') as f:
        z = csv.writer(f)
        z.writerow(naglowki)
        z.writerows(wiersze)
    print(f'  zapisano {sciezka} ({len(wiersze)} wierszy)')
    return sciezka


def do_bigquery(pliki, zbior):
    """Ładuje pliki CSV(.gz) do BigQuery narzędziem bq na koncie usługi (nazwa tabeli = nazwa pliku)."""
    info = info_klucza()
    if not info:
        blad('Brak klucza Google do BigQuery.')
    projekt = zbior.split(':')[0] if ':' in zbior else info.get('project_id')
    zbior = zbior if ':' in zbior else f'{projekt}:{zbior}'
    with tempfile.TemporaryDirectory() as tmp:
        klucz = Path(tmp, 'klucz.json')
        klucz.write_text(json.dumps(info), encoding='utf-8')
        os.chmod(klucz, 0o600)
        env = dict(os.environ, CLOUDSDK_CONFIG=str(Path(tmp, 'gcloud')))
        subprocess.run(['gcloud', 'auth', 'activate-service-account', f'--key-file={klucz}', '--quiet'], env=env, check=True,
                       stdout=subprocess.DEVNULL)
        subprocess.run(['bq', f'--project_id={projekt}', 'mk', '--force', '--dataset', '--location=EU', zbior],
                       env=env, check=False, stdout=subprocess.DEVNULL)
        for p in pliki:
            tabela = Path(p).name.split('.')[0]
            cel = f'{zbior}.{tabela}'
            subprocess.run(['bq', f'--project_id={projekt}', 'load', '--replace', '--source_format=CSV', '--skip_leading_rows=1',
                            '--autodetect', cel, str(p)], env=env, check=True)
            print(f'  BigQuery: {cel} ← {Path(p).name}')


# ——— historia zmian strony (bez kluczy: z historii gałęzi produkcyjnej) ———

def historia_zmian(od=None):
    subprocess.run(['git', '-C', str(KORZEN), 'fetch', '-q', 'origin', GALAZ_PRODUKCJI], check=False)
    ref = 'FETCH_HEAD'
    log = subprocess.run(['git', '-C', str(KORZEN), 'log', ref, '--reverse', '--date=short', '--name-status',
                          '--format=@@%ad|%h|%p|%s'] + ([f'--since={od}'] if od else []),
                         capture_output=True, text=True, check=True).stdout
    wiersze, biezacy = [], None
    for linia in log.splitlines():
        if linia.startswith('@@'):
            data, sha, rodzice, temat = linia[2:].split('|', 3)
            # Gałąź produkcyjna ma dwa początki historii (import całej strony) — to nie są nowe strony.
            biezacy = [data, sha, temat if rodzice else f'[początek historii: import całej strony] {temat}', [], [], [], bool(rodzice)]
            wiersze.append(biezacy)
        elif linia.strip() and biezacy:
            status, *sciezki = linia.split('\t')
            plik = sciezki[-1]
            if '/' in plik or not plik.endswith('.html'):
                continue
            {'A': biezacy[3], 'D': biezacy[5]}.get(status[0], biezacy[4]).append(plik)
    return (['data', 'commit', 'temat', 'strony_dodane', 'strony_zmienione', 'strony_usuniete'],
            [[d, s, t, ' '.join(a) if r else f'({len(a)} stron)', ' '.join(z), ' '.join(u)] for d, s, t, a, z, u, r in wiersze])


# ——— polecenia ———

def p_sprawdz(_):
    print('Zmienne środowiska:')
    for z in ['GOOGLE_SA_JSON', 'GOOGLE_APPLICATION_CREDENTIALS', 'GA4_PROPERTY_ID', 'CLARITY_API_TOKEN', 'BQ_DATASET']:
        print(f'  {z}: {"ustawiona" if os.environ.get(z) else "—"}')
    info = info_klucza()
    if info:
        print(f'Konto usługi: {info.get("client_email")} (projekt {info.get("project_id")})')
        for u in ga4_uslugi():
            print(f'  GA4: {u["usluga"]} — {u["nazwa"]} (konto: {u["konto"]})')
        for w, uprawnienia in gsc_witryny():
            print(f'  Search Console: {w} ({uprawnienia})')
    if os.environ.get('CLARITY_API_TOKEN'):
        print(f'  Clarity: odpowiedź z {len(clarity(1))} zestawami metryk (zużyto 1 z 10 dziennych zapytań)')


def p_ga4(a):
    pid = ga4_id(a.wlasciwosc)
    nagl, wiersze = ga4_raport(pid, a.od, a.do, a.wymiary.split(','), a.metryki.split(','), a.strona, a.limit)
    zapisz_csv(a.csv, nagl, wiersze) if a.csv else wypisz(nagl, wiersze)


def p_gsc(a):
    witryny = [a.witryna] if a.witryna else gsc_witryny_33bots()
    for w in witryny:
        print(f'# {w}')
        nagl, wiersze = gsc_raport(w, a.od, a.do, a.wymiary.split(','), a.limit)
        zapisz_csv(Path(a.csv).with_name(w.replace(':', '_').replace('/', '_') + '_' + Path(a.csv).name), nagl, wiersze) if a.csv else wypisz(nagl, wiersze)


def p_clarity(a):
    print(json.dumps(clarity(a.dni, a.wymiary.split(',') if a.wymiary else ()), ensure_ascii=False, indent=1))


def p_archiwum(a):
    katalog = Path(a.katalog)
    dzis = dt.date.today()
    pliki = []
    if info_klucza() and not a.bez_google:
        pid = ga4_id(a.wlasciwosc)
        poczatek, nazwa = ga4_poczatek(pid)
        print(f'GA4 {pid} ({nazwa}) od {poczatek}:')
        for tabela, (wym, met) in RAPORTY_GA4.items():
            nagl, wiersze = ga4_raport(pid, a.od or poczatek, 'yesterday', wym, met)
            pliki.append(zapisz_csv(katalog / f'{tabela}.csv.gz', nagl, wiersze))
        od_gsc = (dzis - dt.timedelta(days=486)).isoformat()   # Search Console trzyma 16 miesięcy
        for w in gsc_witryny_33bots():
            znacznik = w.replace('sc-domain:', '').replace('https://', '').replace('/', '').replace('.', '_')
            print(f'Search Console {w} od {od_gsc}:')
            for tabela, wym in [('dni', ['date']), ('strony', ['date', 'page', 'country', 'device']),
                                ('frazy', ['date', 'query', 'page', 'country', 'device'])]:
                nagl, wiersze = gsc_raport(w, od_gsc, dzis.isoformat(), wym)
                pliki.append(zapisz_csv(katalog / f'gsc_{znacznik}_{tabela}.csv.gz', nagl, wiersze))
    if os.environ.get('CLARITY_API_TOKEN') and not a.bez_clarity:
        print('Clarity (3 ostatnie dni — starszych danych API nie oddaje, stąd codzienne archiwum):')
        for wym in [(), ('URL',), ('Device', 'Channel')]:
            dane = clarity(3, wym)
            sciezka = katalog / 'clarity' / f'{dzis.isoformat()}_{"-".join(wym) or "ogolem"}.json'
            sciezka.parent.mkdir(parents=True, exist_ok=True)
            sciezka.write_text(json.dumps(dane, ensure_ascii=False), encoding='utf-8')
            print(f'  zapisano {sciezka}')
    nagl, wiersze = historia_zmian()
    pliki.append(zapisz_csv(katalog / 'historia_zmian.csv.gz', nagl, wiersze))
    zbior = a.bigquery or os.environ.get('BQ_DATASET')
    if zbior:
        do_bigquery(pliki, zbior)
    print(f'Archiwum: {katalog}')


def p_historia(a):
    nagl, wiersze = historia_zmian(a.od)
    zapisz_csv(a.csv, nagl, wiersze) if a.csv else wypisz(nagl, wiersze, 400)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest='polecenie', required=True)
    s.add_parser('sprawdz', help='co jest skonfigurowane i do czego konto ma dostęp').set_defaults(f=p_sprawdz)
    g = s.add_parser('ga4', help='dowolny raport GA4')
    g.add_argument('--wlasciwosc'); g.add_argument('--od', default='28daysAgo'); g.add_argument('--do', default='yesterday')
    g.add_argument('--wymiary', default='date'); g.add_argument('--metryki', default='sessions,totalUsers,keyEvents')
    g.add_argument('--strona', help='filtr: ścieżka strony zawiera…'); g.add_argument('--limit', type=int); g.add_argument('--csv')
    g.set_defaults(f=p_ga4)
    c = s.add_parser('gsc', help='raport Search Console (domyślnie wszystkie witryny 33bots)')
    c.add_argument('--witryna'); c.add_argument('--od', default=(dt.date.today() - dt.timedelta(days=30)).isoformat())
    c.add_argument('--do', default=dt.date.today().isoformat()); c.add_argument('--wymiary', default='query')
    c.add_argument('--limit', type=int, default=1000); c.add_argument('--csv')
    c.set_defaults(f=p_gsc)
    k = s.add_parser('clarity', help='Clarity: metryki z 1–3 ostatnich dni')
    k.add_argument('--dni', type=int, default=1); k.add_argument('--wymiary', help='do 3, np. URL,Device,Channel')
    k.set_defaults(f=p_clarity)
    r = s.add_parser('archiwum', help='pełne archiwum: GA4 od początku, Search Console 16 mies., Clarity, historia zmian')
    r.add_argument('--katalog', default=str(DOMYSLNY_KATALOG)); r.add_argument('--wlasciwosc'); r.add_argument('--od')
    r.add_argument('--bigquery', help='projekt:zbiór (domyślnie BQ_DATASET)'); r.add_argument('--bez-google', action='store_true')
    r.add_argument('--bez-clarity', action='store_true')
    r.set_defaults(f=p_archiwum)
    h = s.add_parser('historia-zmian', help='daty wdrożeń i zmienione strony z gałęzi produkcyjnej')
    h.add_argument('--od'); h.add_argument('--csv')
    h.set_defaults(f=p_historia)
    a = p.parse_args()
    a.f(a)


if __name__ == '__main__':
    main()
