#!/usr/bin/env python3
"""Kontrola na żywo po wdrożeniu z 23.11.2026 (raport Search Console)."""
import json, re, sys, time, urllib.request, urllib.error
from urllib.parse import urljoin


class BezPrzekierowan(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


OP = urllib.request.build_opener(BezPrzekierowan)


def jeden(url):
    try:
        r = OP.open(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (kontrola)'}), timeout=30)
        return r.status, dict(r.headers), r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read().decode('utf-8', 'replace')
    except Exception as e:  # noqa
        return 0, {}, str(e)


def czekaj(url, znacznik, minut=10):
    koniec = time.time() + minut * 60
    while time.time() < koniec:
        k, h, t = jeden(url + '?k=' + str(int(time.time())))
        if k == 200 and znacznik in t:
            return True
        time.sleep(20)
    return False


gotowe = {
    'pl': czekaj('https://33bots.pl/oferta-targi.html', 'https://33bots.de/angebot-messen.html" hreflang="de" lang="de" style="color:var(--text)'),
    'de': czekaj('https://33bots.de/weihnachtsfeier-ideen.html', 'noindex, follow'),
    'lt': czekaj('https://33bots.lt/robotas-parodoms.html', 'parodos-uzsienyje'),
}
# (adres, oczekiwany kod, oczekiwany Location albo None, [jest], [nie ma])
T = [
    ('https://33bots.de/weihnachtsfeier-ideen.html', 200, None, ['noindex, follow'], []),
    ('https://33bots.de/blog.html', 200, None, ['noindex, follow'], []),
    ('https://33bots.de/humanoiden-roboter-kaufen.html', 200, None, ['index, follow'], ['noindex']),
    ('https://33bots.de/', 200, None, ['unitree-g1-mieten.html', 'Wissen über den Roboter'], ['>Ratgeber<']),
    ('https://33bots.de/sitemap.xml', 200, None, ['roboter-mieten-preise.html'], ['weihnachtsfeier-ideen.html', 'teambuilding-ideen.html', 'blog.html']),
    ('https://33bots.pl/', 200, None, ['https://33bots.de/humanoiden-roboter-mieten.html', 'https://33bots.at/humanoider-roboter-mieten.html'], []),
    ('https://33bots.pl/case-study-women-in-tech.html', 200, None, ['https://33bots.de/case-study-women-in-tech.html'], []),
    ('https://33bots.pl/blog-unitree-g1-robot.html', 200, None, ['https://33bots.de/unitree-g1-mieten.html', 'https://33bots.at/unitree-g1-mieten.html'], []),
    ('https://33bots.pl/wypozyczenie-robota.html', 200, None, ['NIEMCY I AUSTRIA'], []),
    ('https://33bots.pl/blog.html', 200, None, [], ['hreflang="de" href="https://33bots.de/blog.html"']),
    ('https://33bots.pl/blog-unitree-g1-robot', 301, 'https://33bots.pl/blog-unitree-g1-robot.html', [], []),
    ('https://33bots.pl/blog-co-potrafi-robot-humanoidalny', 301, 'https://33bots.pl/blog-co-potrafi-robot-humanoidalny.html', [], []),
    ('https://33bots.pl/blog-co-potrafi-robot-humanoidalny-unitree-g1/', 301, 'https://33bots.pl/blog-co-potrafi-robot-humanoidalny.html', [], []),
    ('https://33bots.pl/blog-ile-kosztuje-robot-humanoidalne.html', 301, 'https://33bots.pl/blog-ile-kosztuje-robot-humanoidalny.html', [], []),
    ('https://33bots.pl/blog-jak-wynajac-checklist.html', 301, 'https://33bots.pl/blog-jak-wynajac-robota-checklist.html', [], []),
    ('https://33bots.pl/wypozyczenie-roba.html', 301, 'https://33bots.pl/wypozyczenie-robota.html', [], []),
    ('https://33bots.pl/wypozyczenie-robota-ca', 301, 'https://33bots.pl/wypozyczenie-robota.html', [], []),
    ('https://33bots.pl/nie-ma-takiej-strony', 404, None, [], []),
    ('https://33bots.pl/api/', 200, None, [], []),
    ('https://33bots.pl/wypozyczenie-robota.html', 200, None, [], []),
    ('https://33bots.lt/humanoidinio-roboto-nuoma.html', 200, None, ['https://33bots.de/humanoiden-roboter-mieten.html'], []),
    ('https://33bots.lt/blog.html', 200, None, [], ['hreflang="de" href="https://33bots.de/blog.html"']),
    ('https://33bots.at/', 200, None, ['Der Gast, mit dem alle ein Foto wollen'], []),
]
wyniki, bledy = [], []
for url, kod, loc, ma, nie in T:
    k, h, t = jeden(url)
    l = urljoin(url, h.get('Location', '')) if h.get('Location') else None
    brak = [x for x in ma if x not in t]
    jest = [x for x in nie if x in t]
    ok = k == kod and (loc is None or l in (loc, loc.replace('https://', 'http://'))) and not brak and not jest
    wyniki.append({'adres': url, 'kod': k, 'location': l, 'ok': ok, 'brak': brak, 'niechciane': jest})
    if not ok:
        bledy.append(url)
gh = {}
for u in ['https://oliwierels.github.io/33bots/', 'https://oliwierels.github.io/33bots/oferta-targi.html']:
    k, h, t = jeden(u)
    gh[u] = {'kod': k, 'location': h.get('Location')}
json.dump({'gotowe': gotowe, 'bledy': bledy, 'testy': wyniki, 'github_pages': gh}, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('gotowe', gotowe, 'bledy', bledy, gh)
