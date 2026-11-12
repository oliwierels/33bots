#!/bin/bash
# Stan na żywo po zmianach z 12.11.2026: 33bots.de (miasta, noindex, mapa, stopka) i 33bots.at (język, tytuły, indeksowanie).
GB='Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
strona() {  # adres → kod, lang, robots, canonical, tytuł, rozmiar
  local u=$1 s
  s=$(curl -s -A "$GB" --max-time 30 "$u")
  echo "$(curl -s -o /dev/null -A "$GB" -w '%{http_code}' --max-time 30 "$u") | $(printf '%s' "$s" | grep -oE '<html[^>]*>' | head -1) | $(printf '%s' "$s" | grep -oE '<meta name="robots"[^>]*>' | head -1 | sed 's/.*content="//;s/".*//') | canonical: $(printf '%s' "$s" | grep -oE '<link rel="canonical"[^>]*>' | head -1 | sed 's/.*href="//;s/".*//') | $(printf '%s' "$s" | wc -c)B | $(printf '%s' "$s" | grep -oE '<title>[^<]*' | head -1 | sed 's/<title>//')"
}
echo "################ 33bots.de po wdrożeniu"
for p in / roboter-mieten-berlin.html roboter-mieten-dresden.html roboter-mieten-bremen.html roboter-mieten-stuttgart.html roboter-stadtfest.html humanoiden-roboter-mieten.html angebot-messen.html angebot-konferenzen-galas.html blog-psychologie-humanoider-roboter.html; do
  echo "$p → $(strona "https://33bots.de/${p#/}")"
done
echo "sitemap .de: $(curl -s https://33bots.de/sitemap.xml | grep -c '<loc>') adresów; miasta: $(curl -s https://33bots.de/sitemap.xml | grep -oE 'roboter-mieten-[a-z]+\.html' | sort -u | tr '\n' ' ')"
echo "stopka .de — miasta: $(curl -s -A "$GB" https://33bots.de/ | grep -oE 'href="roboter-mieten-[a-z]+\.html"' | sort -u | tr '\n' ' ')"
echo "Dresden — nowa treść: $(curl -s -A "$GB" https://33bots.de/roboter-mieten-dresden.html | grep -c 'unser Einsatz in Dresden')"
echo "Stadtfest — nowa treść: $(curl -s -A "$GB" https://33bots.de/roboter-stadtfest.html | grep -c 'Ein Programmpunkt für das ganze Fest')"
echo "llms.txt — Referenz: $(curl -s https://33bots.de/llms.txt | grep -c 'Referenz in Deutschland')"
echo "IndexNow klucz: $(curl -s -o /dev/null -w '%{http_code}' https://33bots.de/a2813e79cb1d1017ecf75f8b739153a3.txt)"
echo "sitemap .de — kody: $(curl -s https://33bots.de/sitemap.xml | grep -oE '<loc>[^<]+' | sed 's/<loc>//' | while read u; do curl -s -o /dev/null -A "$GB" -w '%{http_code}\n' "$u"; done | sort | uniq -c | tr '\n' ' ')"
echo "################ 33bots.at — każda strona z mapy"
echo "nagłówki /: $(curl -s -o /dev/null -D - -A "$GB" https://33bots.at/ | grep -iE '^(HTTP|server|x-robots|content-type|content-language|last-modified|cache-control)' | tr '\r\n' '  ')"
echo "sha256 index: $(curl -s -A "$GB" https://33bots.at/ | sha256sum | cut -c1-16)  zwykła przeglądarka: $(curl -s -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0' https://33bots.at/ | sha256sum | cut -c1-16)"
echo "robots.txt:"; curl -s https://33bots.at/robots.txt | head -12
echo "/ → $(strona https://33bots.at/)"
curl -s https://33bots.at/sitemap.xml | grep -oE '<loc>[^<]+' | sed 's/<loc>//' | while read u; do echo "${u#https://33bots.at} → $(strona "$u")"; done
echo "hreflang /: $(curl -s -A "$GB" https://33bots.at/ | grep -oE '<link rel="alternate" hreflang[^>]*>' | tr '\n' ' ')"
echo "og:locale: $(curl -s -A "$GB" https://33bots.at/ | grep -oE '<meta property="og:locale"[^>]*>')  inLanguage: $(curl -s -A "$GB" https://33bots.at/ | grep -oE '"inLanguage": ?"[^"]*"' | sort -u | tr '\n' ' ')"
for p in www http; do :; done
echo "przekierowania: http → $(curl -s -o /dev/null -A "$GB" -w '%{http_code} %{redirect_url}' http://33bots.at/) | www → $(curl -s -o /dev/null -A "$GB" -w '%{http_code} %{redirect_url}' https://www.33bots.at/) | index.html → $(curl -s -o /dev/null -A "$GB" -w '%{http_code} %{redirect_url}' https://33bots.at/index.html)"
echo "stare adresy AT: $(for p in roboter-mieten.html angebot.html blog.html referenzen.html preise.html; do echo -n "$p=$(curl -s -o /dev/null -A "$GB" -w '%{http_code}' https://33bots.at/$p) "; done)"
echo "################ .de a .at — podobieństwo"
python3 - <<'PY'
import re,urllib.request,difflib
def t(u):
    s=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read().decode('utf-8','ignore')
    s=re.sub(r'<(script|style)[^>]*>.*?</\1>','',s,flags=re.S); m=re.search(r'<main.*?</main>',s,re.S)
    return re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',m.group(0) if m else s)).split()
for a,b in (('https://33bots.de/','https://33bots.at/'),('https://33bots.de/unitree-g1-mieten.html','https://33bots.at/unitree-g1-mieten.html'),('https://33bots.de/humanoiden-roboter-mieten.html','https://33bots.at/humanoider-roboter-mieten.html'),('https://33bots.at/roboter-mieten-wien.html','https://33bots.at/roboter-mieten-graz.html'),('https://33bots.at/roboter-mieten-wien.html','https://33bots.at/roboter-mieten-salzburg.html')):
    try:
        x,y=t(a),t(b); print(a,'vs',b,'podobieństwo %.2f'%difflib.SequenceMatcher(None,x,y,autojunk=False).ratio(),len(x),len(y))
    except Exception as e: print(a,b,'błąd',e)
PY
