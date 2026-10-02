# -*- coding: utf-8 -*-
"""Wersje językowe 33bots: hreflang i przełącznik w stopce.

33bots prowadzi cztery witryny: 33bots.pl, 33bots.de, 33bots.lt i 33bots.at. Żeby Google traktował je
jako jedną rodzinę, a nie trzy niepowiązane serwisy, każda strona musi wskazywać pozostałe
wersje — i musi to być **wzajemne**. Jednostronną deklarację hreflang wyszukiwarki pomijają.

Skrypt robi dwie rzeczy i można go uruchamiać wielokrotnie (jest idempotentny):

1. przepisuje blok `<link rel="alternate" hreflang=...>` w `<head>` każdej strony,
2. dopisuje w stopce widoczny wiersz z odnośnikami do pozostałych wersji — to on przekazuje
   realny sygnał linkowy, czego sam hreflang nie robi.

Strony bez odpowiednika w innym języku dostają wyłącznie własny `pl` i `x-default` — lepiej
nie deklarować nic, niż wskazywać stronę o innej treści.

Uruchomienie:  python3 jezyki.py
"""
import glob
import re

SITE = "https://33bots.pl"
ZNACZNIK = "data-jezyki"          # po nim poznajemy, że stopka już ma przełącznik

# Odpowiedniki treści. Klucz to plik polskiej wersji, wartość to adresy tych samych treści
# w pozostałych językach. Wpisujemy wyłącznie realne odpowiedniki — „podobna strona" to za
# mało, bo wtedy Google i tak zignoruje deklarację, a użytkownik trafia nie tam, gdzie chciał.
ODPOWIEDNIKI = {
    "index.html": {
        "lt": "https://33bots.lt/",
        "de": "https://33bots.de/",
        "de-AT": "https://33bots.at/",
    },
    "wypozyczenie-robota.html": {
        "lt": "https://33bots.lt/humanoidinio-roboto-nuoma.html",
        "de": "https://33bots.de/humanoiden-roboter-mieten.html",
        "de-AT": "https://33bots.at/humanoider-roboter-mieten.html",
    },
    "oferta-targi.html": {
        "lt": "https://33bots.lt/robotas-parodoms.html",
        "de": "https://33bots.de/angebot-messen.html",
        "de-AT": "https://33bots.at/messe-roboter-mieten.html",
    },
    "oferta-konferencje.html": {
        "lt": "https://33bots.lt/robotas-konferencijai.html",
        "de": "https://33bots.de/angebot-konferenzen-galas.html",
    },
    "robot-na-event.html": {
        "lt": "https://33bots.lt/robotas-renginiui.html",
        "de": "https://33bots.de/roboter-event.html",
    },
    "robot-na-wesele.html": {
        "lt": "https://33bots.lt/robotas-vestuvems.html",
        "de": "https://33bots.de/roboter-hochzeit.html",
    },
    "realizacje-wideo.html": {
        "lt": "https://33bots.lt/video-realizacijos.html",
        "de": "https://33bots.de/referenzen-videos.html",
    },
    "blog.html": {
        "lt": "https://33bots.lt/blog.html",
        "de": "https://33bots.de/blog.html",
    },
}

# Strony, których nie ruszamy: 404 nie jest indeksowana, szablon to materiał roboczy.
POMIJANE = {"404.html", "szablon-case-study.html"}

NAZWY = {"lt": "Lietuvių — 33bots.lt", "de": "Deutsch — 33bots.de",
         "de-AT": "Österreich — 33bots.at"}


def wlasny_adres(plik):
    return f"{SITE}/" if plik == "index.html" else f"{SITE}/{plik}"


def blok_hreflang(plik):
    wlasny = wlasny_adres(plik)
    pary = [("pl", wlasny)]
    pary += list(ODPOWIEDNIKI.get(plik, {}).items())
    pary.append(("x-default", wlasny))
    return "\n".join(f'  <link rel="alternate" hreflang="{lang}" href="{href}" />'
                     for lang, href in pary)


def przepisz_head(tresc, plik):
    nowy = blok_hreflang(plik)
    # Usuwamy tylko własne linie starych deklaracji — bez zjadania pustych linii obok,
    # żeby plik nie zmieniał formatowania przy każdym uruchomieniu.
    wzor = re.compile(r'[ \t]*<link rel="alternate" hreflang="[^"]*" href="[^"]*"[ \t]*/?>[ \t]*\n?')
    if wzor.search(tresc):
        return wzor.sub("", tresc, count=0).replace(
            f'<link rel="canonical" href="{wlasny_adres(plik)}" />',
            f'<link rel="canonical" href="{wlasny_adres(plik)}" />\n{nowy}', 1)
    # brak jakiegokolwiek hreflang — dokładamy zaraz po adresie kanonicznym
    return re.sub(r'(<link rel="canonical" href="[^"]*"\s*/?>)',
                  r'\1\n' + nowy.replace('\\', '\\\\'), tresc, count=1)


def wiersz_stopki(plik, klasa, styl):
    """Widoczny przełącznik języków. Pokazuje tylko te wersje, które mają odpowiednik."""
    odp = ODPOWIEDNIKI.get(plik, {})
    if not odp:
        return None
    linki = " · ".join(
        f'<a href="{href}" hreflang="{lang}" lang="{lang.split("-")[0]}" {styl}>{NAZWY[lang]}</a>'
        for lang, href in odp.items())
    return f'<p class="{klasa}" {ZNACZNIK}>{linki}</p>'


def dopisz_stopke(tresc, plik):
    # Jeśli przełącznik już jest, przepisujemy go od nowa — inaczej zmiana mapy
    # odpowiedników zostawałaby w <head>, a w stopce zostawałby stary zestaw linków.
    if ZNACZNIK in tresc:
        tresc = re.sub(r'\s*<p class="[^"]*" ' + ZNACZNIK + r'>.*?</p>', "", tresc, flags=re.S)

    # Nowy dizajn (Tailwind): linia pod hasłem w stopce.
    wzor_nowy = re.compile(
        r'(<p class="mt-2 text-\[13px\] text-neutral-500">Wynajem robot[^<]*</p>)')
    wiersz = wiersz_stopki(plik, "mt-2 text-[13px] text-neutral-500",
                           'class="underline underline-offset-2 transition hover:text-white"')
    if wiersz and wzor_nowy.search(tresc):
        return wzor_nowy.sub(r"\1\n        " + wiersz.replace("\\", "\\\\"), tresc, count=1)

    # Stary dizajn (style.css): linia pod hasłem w bloku footer__brand.
    wzor_stary = re.compile(r'(<p class="footer__tagline">.*?</p>)', re.S)
    wiersz = wiersz_stopki(plik, "footer__tagline", 'style="color:inherit;"')
    if wiersz and wzor_stary.search(tresc):
        return wzor_stary.sub(r"\1\n        " + wiersz.replace("\\", "\\\\"), tresc, count=1)

    return tresc


def main():
    zmienione = 0
    for plik in sorted(glob.glob("*.html")):
        if plik in POMIJANE:
            continue
        tresc = open(plik, encoding="utf-8").read()
        nowa = dopisz_stopke(przepisz_head(tresc, plik), plik)
        if nowa != tresc:
            open(plik, "w", encoding="utf-8").write(nowa)
            zmienione += 1
    powiazane = len(ODPOWIEDNIKI)
    print(f"Zaktualizowane strony: {zmienione}")
    print(f"Strony z odpowiednikami w innych językach: {powiazane}")


if __name__ == "__main__":
    main()
