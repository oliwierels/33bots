"""Historia domen w Wayback Machine (33bots.de, .pl, .lt, robotivo.de) i obecna zawartość robotivo.de."""
import json, re, sys, socket, time, urllib.request, urllib.error, html
def get(u, t=60):
    for p in range(3):
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 kontrola'}), timeout=t)
            return r.status, r.read().decode('utf-8', 'replace'), r.geturl()
        except urllib.error.HTTPError as e:
            return e.code, '', u
        except Exception as e:
            err = str(e); time.sleep(5)
    return 0, err, u
W = {}
for d in ['33bots.de', '33bots.pl', '33bots.lt', 'robotivo.de']:
    k, t, _ = get(f'http://web.archive.org/cdx/search/cdx?url={d}&output=json&fl=timestamp,statuscode,mimetype&collapse=timestamp:6&limit=500', 120)
    try:
        rows = json.loads(t)[1:]
    except Exception:
        rows = []
    k2, t2, _ = get(f'http://web.archive.org/cdx/search/cdx?url={d}/*&output=json&fl=original&collapse=urlkey&limit=3000', 120)
    try:
        urls = [r[0] for r in json.loads(t2)[1:]]
    except Exception:
        urls = []
    wczesne = []
    for ts, sc, mt in rows[:3]:
        _, p, _ = get(f'http://web.archive.org/web/{ts}id_/http://{d}/', 60)
        tyt = (re.search(r'<title[^>]*>(.*?)</title>', p, re.S | re.I) or [0, ''])[1].strip()[:150]
        lang = (re.search(r'<html[^>]+lang="([^"]+)"', p, re.I) or [0, ''])[1]
        txt = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<script.*?</script>|<style.*?</style>', '', p, flags=re.S | re.I))))[:400]
        wczesne.append({'ts': ts, 'status': sc, 'title': html.unescape(tyt), 'lang': lang, 'tekst': txt})
    W[d] = {'cdx_kod': k, 'zrzutow_miesiecznych': len(rows), 'miesiace': [r[0][:6] + ':' + r[1] for r in rows],
            'adresow_w_archiwum': len(urls), 'najstarsze': wczesne,
            'adresy_probka': urls[:60]}
try:
    W['robotivo_dns'] = socket.gethostbyname('robotivo.de')
except Exception as e:
    W['robotivo_dns'] = 'brak: ' + str(e)
for u in ['https://robotivo.de/', 'http://robotivo.de/']:
    k, p, fin = get(u, 30)
    W['robotivo_' + u.split(':')[0]] = {'kod': k, 'koncowy': fin,
        'title': html.unescape((re.search(r'<title[^>]*>(.*?)</title>', p, re.S | re.I) or [0, ''])[1].strip()[:200]),
        'lang': (re.search(r'<html[^>]+lang="([^"]+)"', p, re.I) or [0, ''])[1],
        'canonical': (re.search(r'rel="canonical"[^>]+href="([^"]+)"', p) or [0, ''])[1],
        'robots': (re.search(r'name="robots"[^>]+content="([^"]+)"', p) or [0, ''])[1],
        '33bots': p.count('33bots'), 'linki': sorted(set(re.findall(r'href="(https?://[^"/]+)', p)))[:30],
        'tekst': re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<script.*?</script>|<style.*?</style>', '', p, flags=re.S | re.I))))[:1500]}
for u in ['https://33bots.de/', 'https://33bots.pl/']:
    _, p, _ = get(u, 30)
    W['ip_' + u.split('//')[1].strip('/')] = socket.gethostbyname(u.split('//')[1].strip('/'))
json.dump(W, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print(json.dumps({d: {k: W[d][k] for k in ('zrzutow_miesiecznych', 'adresow_w_archiwum')} for d in ['33bots.de', '33bots.pl', '33bots.lt', 'robotivo.de']}, indent=1))
