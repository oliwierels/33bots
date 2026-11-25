# -*- coding: utf-8 -*-
"""Jednorazowo: strona miasta (stary szablon) → źródło tresci/landing/strony/<adres>.html.

Każdy tekst, nagłówek i link starej strony przechodzi do nowego układu; nagłówki H1–H3
zostają w tej samej kolejności i z tą samą treścią. Potem źródło poprawia się ręcznie.

Użycie:  python3 tresci/landing/migruj_miasto.py robot-wynajem-warszawa.html [...]
"""
import html
import json
import re
import sys
from pathlib import Path

KORZEN = Path(__file__).resolve().parents[2]
TU = Path(__file__).resolve().parent


def czysc(s):
    s = re.sub(r'\s+style="[^"]*"', '', s)
    s = re.sub(r'\s+class="(body-text|lead-text)"', '', s)
    return s.strip()


def tekst(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


def sekcje(main):
    return [(kom or '', attr, body) for kom, attr, body in
            re.findall(r'(?:<!--\s*([^>]*?)\s*-->\s*)?<section\b([^>]*)>(.*?)</section>', main, re.S)]


def migruj(adres):
    t = (KORZEN / adres).read_text(encoding='utf-8')
    main = re.search(r'<main>.*?</main>', t, re.S).group(0)
    stopka = re.search(r'<footer class="stopka">.*?</footer>', t, re.S).group(0)
    okruch = tekst(re.search(r'<nav class="crumbs".*?</nav>', main, re.S).group(0)).split('›')[-1].strip()
    S = sekcje(main)
    uzyte = set()

    def znajdz(warunek):
        for i, (kom, attr, body) in enumerate(S):
            if i not in uzyte and warunek(kom, attr, body):
                uzyte.add(i)
                return kom, attr, body
        return None

    hero = znajdz(lambda k, a, b: 'hero__title' in b)[2]
    eyebrow = re.search(r'<p class="hero__eyebrow">(.*?)</p>', hero, re.S).group(1)
    h1 = re.search(r'<h1 class="hero__title">(.*?)</h1>', hero, re.S).group(1)
    sub = re.search(r'<p class="hero__sub">(.*?)</p>', hero, re.S).group(1)
    ufnosc = [x.replace('✓', '').strip() for x in re.findall(r'<span class="hero__trust-item">(.*?)</span>', hero, re.S)]

    kor = znajdz(lambda k, a, b: 'id="korzysci"' in a)[2]
    kor_h2 = re.search(r'<h2[^>]*>(.*?)</h2>', kor, re.S).group(1)
    kafle = re.findall(r'<span class="tile__tag">(.*?)</span>.*?<h3 class="tile__title">(.*?)</h3>\s*<p class="tile__desc">(.*?)</p>\s*<a href="([^"]+)"[^>]*>(.*?)</a>', kor, re.S)

    onas = znajdz(lambda k, a, b: 'onas-text' in b and 'id=' not in a)[2]
    onas_h2 = re.search(r'<h2[^>]*>(.*?)</h2>', onas, re.S).group(1)
    onas_el = re.findall(r'<(p|h3|ul)\b[^>]*>(.*?)</\1>', onas.split('</h2>', 1)[1], re.S)
    onas_cta = re.search(r'<a href="(#kontakt)" class="btn-primary"[^>]*>(.*?)</a>', onas, re.S)

    oferty = znajdz(lambda k, a, b: 'Sprawdź nasze oferty' in b)[2]
    oferty_p = czysc(re.search(r'<p\b[^>]*>(.*?)</p>', oferty, re.S).group(1))
    oferty_a = [(h, czysc(x)) for h, x in re.findall(r'<a href="([^"]+)"[^>]*>(.*?)</a>', oferty, re.S)]

    wideo = znajdz(lambda k, a, b: 'id="wideo"' in a)
    dowody = znajdz(lambda k, a, b: 'DOWODY' in k)[2]
    dowody_l = re.search(r'<p\b[^>]*>(.*?)</p>', dowody, re.S).group(1)
    dowody_a = re.findall(r'<a href="([^"]+)"[^>]*>(.*?)</a>', dowody, re.S)
    miasta = znajdz(lambda k, a, b: 'Wynajem robota w innych miastach' in b)[2]
    miasta_a = re.findall(r'<a href="([^"]+)"[^>]*>(.*?)</a>', miasta, re.S)
    case = znajdz(lambda k, a, b: k.startswith('CASE STUDY'))
    scen = znajdz(lambda k, a, b: 'id="scenariusze-miasto"' in a)[2]
    scen_h2 = re.search(r'<h2[^>]*>(.*?)</h2>', scen, re.S).group(1)
    scen_p = re.search(r'</h2>\s*<p\b[^>]*>(.*?)</p>', scen, re.S).group(1)
    scen_a = re.findall(r'<a href="([^"]+)"[^>]*>(.*?)</a>', scen, re.S)
    faq = znajdz(lambda k, a, b: 'faq-item' in b)[2]
    faq_h2 = re.search(r'<h2[^>]*>(.*?)</h2>', faq, re.S).group(1)
    faq_i = re.findall(r'<button class="faq-q"[^>]*>\s*<span>(.*?)</span>.*?<div class="faq-a" hidden>(.*?)</div>', faq, re.S)
    lok = znajdz(lambda k, a, b: 'id="lokalnie"' in a)[2]
    lok_h2 = re.search(r'<h2[^>]*>(.*?)</h2>', lok, re.S).group(1)
    lok_el = re.findall(r'<(p|h3|ul)\b[^>]*>(.*?)</\1>', lok.split('</h2>', 1)[1], re.S)
    kon = znajdz(lambda k, a, b: 'id="kontakt"' in a)[2]
    kon_h2 = re.search(r'<h2[^>]*>(.*?)</h2>', kon, re.S).group(1)
    reszta = [i for i in range(len(S)) if i not in uzyte]
    assert not reszta, f'{adres}: nieprzeniesione sekcje {reszta}'

    def proza(elementy, pierwszy_wstep):
        out = []
        for i, (tag, x) in enumerate(elementy):
            x = czysc(x)
            if tag == 'p':
                klasa = ' class="l-wstep"' if (i == 0 and pierwszy_wstep) else ''
                out.append(f'<p{klasa}>{x}</p>')
            elif tag == 'h3':
                out.append(f'<h3>{x}</h3>')
            else:
                out.append(f'<ul>{x}</ul>')
        return '\n          '.join(out)

    miasto = re.sub(r'^Wynajem robota\s+', '', okruch)
    kafle_html = '\n'.join(
        f'''      <li class="zasada">
        <span class="l-nr" aria-hidden="true">{i + 1:02d}</span>
        <p class="label">{czysc(tag)}</p>
        <h3 class="h3">{czysc(h3)}</h3>
        <p class="body">{czysc(desc)}</p>
        <a class="link" href="{href}">{czysc(a)}</a>
      </li>''' for i, (tag, h3, desc, href, a) in enumerate(kafle))

    case_html = ''
    if case:
        cb = case[2]
        ps = [czysc(x) for x in re.findall(r'<p\b[^>]*>(.*?)</p>', cb, re.S)]
        link = re.search(r'<a href="([^"]+)"[^>]*>(.*?)</a>', cb, re.S)
        case_html = f'''
<section class="sec" id="realizacja-w-miescie" aria-label="{tekst(ps[0])}">
  <div class="wrap grid12 l-miejscowa">
    <figure class="l-miejscowa__foto wejscie"><img src="ZDJECIE.jpg" alt="ALT" loading="lazy" width="1200" height="900" /></figure>
    <div class="l-miejscowa__tekst wejscie">
      <p class="label">{ps[0]}</p>
      <p class="h3">{ps[1]}</p>
      <p class="body">{ps[2]}</p>
      <p><a class="link" href="{link.group(1)}">{czysc(link.group(2))}</a></p>
    </div>
  </div>
</section>'''

    wideo_html = ''
    if wideo:
        wb = wideo[2]
        video = czysc(re.search(r'<video.*?</video>', wb, re.S).group(0))
        p = czysc(re.search(r'</video>.*?<p\b[^>]*>(.*?)</p>', wb, re.S).group(1))
        a = re.search(r'<a href="([^"]+)" class="btn-primary"[^>]*>(.*?)</a>', wb, re.S)
        wideo_html = f'''
<section class="sec" id="wideo" aria-label="Robot w akcji">
  <div class="wrap grid12 l-wideo">
    <figure class="l-wideo__film wejscie">{video}</figure>
    <div class="l-wideo__tekst wejscie">
      <p class="label">Na żywo</p>
      <p class="body">{p}</p>
      <a class="btn btn--akcja" href="{a.group(1)}" data-cta="wideo">{czysc(a.group(2)).replace('→', '<span aria-hidden="true">→</span>')}</a>
    </div>
  </div>
</section>'''

    dowody_html = '\n'.join(
        f'      <li><a href="{h}"><span class="l-dowod__liczba">{tekst(x).split("·")[1].replace("→", "").strip()}</span>'
        f'<span class="l-dowod__opis">{tekst(x).split("·")[0].strip()} →</span></a></li>' for h, x in dowody_a)

    faq_html = '\n'.join(
        f'''      <div class="faq__item">
        <h3 class="faq__h"><button class="faq__q" type="button" id="faq-{i}-q" aria-expanded="false" aria-controls="faq-{i}">{czysc(q)}<span class="faq__znak" aria-hidden="true"><span></span><span></span></span></button></h3>
        <div class="faq__a" id="faq-{i}" role="region" aria-labelledby="faq-{i}-q" hidden>{czysc(a)}</div>
      </div>''' for i, (q, a) in enumerate(faq_i, 1))

    linki = lambda lista: '\n'.join(f'      <li><a href="{h}">{czysc(x)}</a></li>' for h, x in lista)
    cta = onas_cta.group(2).replace('→', '<span aria-hidden="true">→</span>') if onas_cta else ''

    zrodlo = f'''<!-- landing {json.dumps({"kontakt_h2": kon_h2, "miejsce": miasto, "slajdy": []}, ensure_ascii=False)} -->
<main>
<section class="hero l-hero" aria-labelledby="strona-h1">
  <div class="hero__text">
    <nav class="l-okruchy" aria-label="Okruszki"><a href="index.html">Strona główna</a> <span aria-hidden="true">›</span> <span>{okruch}</span></nav>
    <p class="label">{eyebrow}</p>
    <h1 id="strona-h1" class="l-h1">{h1}</h1>
    <p class="lead">{czysc(sub)}</p>
    <div class="hero__actions hero__actions--termin">
      <div class="termin">
        <label class="label" for="heroData">Kiedy jest Twoje wydarzenie?</label>
        <div class="termin__rzad">
          <input class="termin__data" type="date" id="heroData" />
          <a class="btn btn--akcja" href="#kontakt" data-cta="hero">Sprawdź&nbsp;termin i&nbsp;cenę <span aria-hidden="true">→</span></a>
        </div>
        <p class="termin__obietnica"><strong>Bez zaliczki, płacisz po wydarzeniu.</strong> Odpowiadamy zwykle w&nbsp;ciągu 30 minut.</p>
        <p class="termin__telefon">Wolisz zadzwonić? <a href="tel:+48531408004" data-tel="hero">+48 531 408 004</a></p>
      </div>
    </div>
    <ul class="l-ufnosc">
{chr(10).join(f"      <li>{x}</li>" for x in ufnosc)}
    </ul>
  </div>
  <figure class="hero__media" id="heroMedia">
    <img src="HERO.jpg" alt="HERO_ALT" fetchpriority="high" decoding="async" width="900" height="1200">
    <figcaption class="hero__podpis">
      <span class="label" id="heroLicznik">01 / 06</span>
      <span class="hero__opis" id="heroOpis">HERO_OPIS</span>
      <button class="hero__pauza" id="heroPauza" type="button" aria-pressed="false" hidden>Pauza</button>
    </figcaption>
  </figure>
</section>
<!-- wspolne:skala -->

<section id="korzysci" class="sec l-korzysci" aria-labelledby="korzysci-h">
  <div class="wrap">
    <div class="sec__glowa wejscie">
      <p class="label sec__meta">Dlaczego robot</p>
      <h2 id="korzysci-h" class="h2">{kor_h2}</h2>
    </div>
    <ul class="zasady wejscie">
{kafle_html}
    </ul>
  </div>
</section>

<section id="miasto" class="sec" aria-labelledby="miasto-h">
  <div class="wrap grid12 l-tekst">
    <div class="l-tekst__glowa wejscie">
      <p class="label">{miasto}</p>
      <h2 id="miasto-h" class="h2">{onas_h2}</h2>
    </div>
    <div class="l-tekst__tresc wejscie">
      <div class="l-proza">
          {proza(onas_el, True)}
          {f'<a href="#kontakt" class="btn btn--akcja" data-cta="tekst">{cta}</a>' if cta else ''}
      </div>
    </div>
  </div>
  <div class="wrap">
    <div class="l-oferty wejscie">
      <p class="body">{oferty_p}</p>
      <ul class="l-linki">
{linki(oferty_a)}
      </ul>
    </div>
  </div>
</section>
{case_html}
<section id="realizacje" class="sec" aria-labelledby="realizacje-h">
  <div class="wrap">
    <div class="sec__glowa wejscie">
      <p class="label sec__meta">Realizacje</p>
      <h2 id="realizacje-h" class="h2">{czysc(dowody_l)}</h2>
    </div>
    <ul class="l-dowody wejscie">
{dowody_html}
    </ul>
    <div class="pasy__glowa">
      <p class="label">Więcej realizacji, kliknij kadr</p>
      <button class="pasy__pauza" type="button" aria-pressed="false" data-pasy="zdjecia" hidden>Zatrzymaj ruch</button>
    </div>
  </div>
  <!-- wspolne:pasy -->
  <div class="wrap">
    <p class="realizacje__wiecej"><a class="link" href="realizacje-wideo.html">Wszystkie realizacje i&nbsp;nagrania <span aria-hidden="true">→</span></a></p>
  </div>
</section>
{wideo_html}
<!-- wspolne:formaty -->

<section id="scenariusze-miasto" class="sec" aria-labelledby="scenariusze-h">
  <div class="wrap">
    <div class="sec__glowa wejscie">
      <p class="label sec__meta">Scenariusze</p>
      <h2 id="scenariusze-h" class="h2">{scen_h2}</h2>
      <p class="body">{czysc(scen_p)}</p>
    </div>
    <ul class="l-linki l-linki--duze wejscie">
{linki(scen_a)}
    </ul>
  </div>
</section>

<section id="faq" class="sec" aria-labelledby="faq-h">
  <div class="wrap grid12">
    <div class="faq__glowa wejscie">
      <p class="label sec__meta">FAQ</p>
      <h2 id="faq-h" class="h2">{faq_h2}</h2>
    </div>
    <div class="faq wejscie">
{faq_html}
    </div>
  </div>
</section>

<section id="lokalnie" class="sec" aria-labelledby="lokalnie-h">
  <div class="wrap grid12 l-tekst">
    <div class="l-tekst__glowa wejscie">
      <p class="label">Na miejscu</p>
      <h2 id="lokalnie-h" class="h2">{lok_h2}</h2>
    </div>
    <div class="l-tekst__tresc wejscie">
      <div class="l-proza">
          {proza(lok_el, False)}
      </div>
    </div>
  </div>
</section>
<!-- wspolne:proces -->

<section id="miasta" class="sec" aria-label="Wynajem robota w innych miastach">
  <div class="wrap">
    <p class="label l-linki__opis">Wynajem robota w innych miastach</p>
    <ul class="l-linki l-linki--male">
{linki(miasta_a)}
    </ul>
  </div>
</section>
<!-- rezerwacja -->
</main>
<!-- stopka -->
{stopka}
'''
    (TU / 'strony').mkdir(exist_ok=True)
    (TU / 'strony' / adres).write_text(zrodlo, encoding='utf-8')
    print('  →', adres)


if __name__ == '__main__':
    for a in sys.argv[1:]:
        migruj(a)
