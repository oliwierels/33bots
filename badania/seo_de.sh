#!/bin/bash
# Diagnoza widoczności 33bots.de: odpowiedzi serwera dla Googlebota, przekierowania, nagłówki, indeks Binga.
GB='Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
GBM='Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
for d in 33bots.de 33bots.at 33bots.lt 33bots.pl; do
  echo "################ $d"
  echo "DNS: $(dig +short $d A | tr '\n' ' ') | NS: $(dig +short $d NS | tr '\n' ' ')"
  for u in "http://$d/" "http://www.$d/" "https://www.$d/" "https://$d/index.html"; do
    echo "-- $u → $(curl -s -o /dev/null -A "$GB" -w '%{http_code} %{redirect_url}' "$u")"
  done
  for p in / /robots.txt /sitemap.xml; do
    echo "== https://$d$p (Googlebot)"; curl -s -o /dev/null -D - -A "$GB" "https://$d$p" | grep -iE '^(HTTP|x-robots|location|content-type|server|cache-control|link|cf-|x-)' 
  done
  echo "== smartfon Googlebot: $(curl -s -o /dev/null -A "$GBM" -w '%{http_code} %{size_download}B %{time_total}s' https://$d/)"
  echo "== zwykła przeglądarka: $(curl -s -o /dev/null -A 'Mozilla/5.0' -w '%{http_code} %{size_download}B' https://$d/)"
  echo "== robots.txt:"; curl -s -A "$GB" "https://$d/robots.txt" | head -8
  echo "== w HTML: $(curl -s -A "$GB" https://$d/ | grep -oE '<meta name="robots"[^>]*>|<link rel="canonical"[^>]*>' | tr '\n' ' ')"
  echo "== Bing site: $(curl -s -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36' "https://www.bing.com/search?q=site%3A$d&setlang=en&cc=DE" | grep -oE '[0-9.,]+ results' | head -1)"
  echo "== DuckDuckGo site: $(curl -s -A 'Mozilla/5.0' "https://html.duckduckgo.com/html/?q=site%3A$d" | grep -c 'result__a')"
done
echo "################ podstrony .de (Googlebot)"
for p in humanoiden-roboter-mieten.html roboter-mieten-preise.html unitree-g1-mieten.html roboter-mieten-berlin.html roboter-mieten-muenchen.html angebot-messen.html blog.html; do
  echo "$p → $(curl -s -o /dev/null -A "$GB" -w '%{http_code} %{size_download}B' https://33bots.de/$p) $(curl -s -D - -o /dev/null -A "$GB" https://33bots.de/$p | grep -i x-robots)"
done
echo "################ sitemap .de: $(curl -s https://33bots.de/sitemap.xml | grep -c '<loc>') adresów; sprawdzam kody"
curl -s https://33bots.de/sitemap.xml | grep -oE '<loc>[^<]+' | sed 's/<loc>//' | while read u; do echo "$(curl -s -o /dev/null -A "$GB" -w '%{http_code}' "$u") $u"; done | sort | uniq -c -w3 | head
echo "################ .de a .at — podobieństwo stron głównych"
python3 - <<'PY'
import re,urllib.request,difflib
def t(u):
    s=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read().decode('utf-8','ignore')
    s=re.sub(r'<(script|style)[^>]*>.*?</\1>','',s,flags=re.S); m=re.search(r'<main.*?</main>',s,re.S)
    return re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',m.group(0) if m else s)).split()
for a,b in (('https://33bots.de/','https://33bots.at/'),('https://33bots.de/unitree-g1-mieten.html','https://33bots.at/unitree-g1-mieten.html')):
    try:
        x,y=t(a),t(b); print(a,'vs',b,'podobieństwo %.2f'%difflib.SequenceMatcher(None,x,y,autojunk=False).ratio(),len(x),len(y))
    except Exception as e: print(a,b,'błąd',e)
PY
