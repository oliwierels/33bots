# -*- coding: utf-8 -*-
"""Sprachversionen von 33bots: hreflang und Umschalter in der Fußzeile.

33bots betreibt vier Websites: 33bots.de, 33bots.pl, 33bots.lt und 33bots.at. Damit Google
sie als eine Familie behandelt und nicht als vier unabhängige Auftritte, muss jede Seite auf
die übrigen Versionen verweisen — und zwar **gegenseitig**. Einseitige hreflang-Angaben
ignorieren Suchmaschinen; genau daran lag es, dass die jüngeren Domains in der Search Console
als „entdeckt — zurzeit nicht indexiert" hängen blieben.

Das Skript ist idempotent und erledigt zwei Dinge:

1. es schreibt den Block `<link rel="alternate" hreflang=...>` im `<head>` jeder Seite neu,
2. es ergänzt in der Fußzeile eine sichtbare Zeile mit Links zu den anderen Versionen —
   erst dieser sichtbare Link überträgt ein Linksignal, hreflang allein tut das nicht.

Seiten ohne echte Entsprechung behalten nur ihr eigenes `de` und `x-default`.

Aufruf:  python3 sprachen.py
"""
import glob
import re

SITE = "https://33bots.de"
MARKER = "data-sprachen"

# Echte inhaltliche Entsprechungen. Schlüssel: Datei der deutschen Version.
ENTSPRECHUNGEN = {
    "index.html": {
        "pl": "https://33bots.pl/",
        "lt": "https://33bots.lt/",
        "de-AT": "https://33bots.at/",
    },
    "humanoiden-roboter-mieten.html": {
        "pl": "https://33bots.pl/wypozyczenie-robota.html",
        "lt": "https://33bots.lt/humanoidinio-roboto-nuoma.html",
        "de-AT": "https://33bots.at/humanoider-roboter-mieten.html",
    },
    "angebot-messen.html": {
        "pl": "https://33bots.pl/oferta-targi.html",
        "lt": "https://33bots.lt/robotas-parodoms.html",
        "de-AT": "https://33bots.at/messe-roboter-mieten.html",
    },
    "angebot-konferenzen-galas.html": {
        "pl": "https://33bots.pl/oferta-konferencje.html",
        "lt": "https://33bots.lt/robotas-konferencijai.html",
    },
    "roboter-event.html": {
        "pl": "https://33bots.pl/robot-na-event.html",
        "lt": "https://33bots.lt/robotas-renginiui.html",
    },
    "roboter-hochzeit.html": {
        "pl": "https://33bots.pl/robot-na-wesele.html",
        "lt": "https://33bots.lt/robotas-vestuvems.html",
    },
    "referenzen-videos.html": {
        "pl": "https://33bots.pl/realizacje-wideo.html",
        "lt": "https://33bots.lt/video-realizacijos.html",
    },
    "blog.html": {
        "pl": "https://33bots.pl/blog.html",
        "lt": "https://33bots.lt/blog.html",
    },
}

# 404 wird nicht indexiert, index-redesign ist ein Entwurf.
UEBERSPRUNGEN = {"404.html", "index-redesign.html"}

NAMEN = {"pl": "Polski — 33bots.pl", "lt": "Lietuvių — 33bots.lt",
         "de-AT": "Österreich — 33bots.at"}


def eigene_adresse(datei):
    return f"{SITE}/" if datei == "index.html" else f"{SITE}/{datei}"


def hreflang_block(datei):
    eigen = eigene_adresse(datei)
    entsprechungen = ENTSPRECHUNGEN.get(datei, {})
    paare = [("de", eigen)] + list(entsprechungen.items())
    # x-default zeigt auf die polnische Version, wo es sie gibt — sie ist die älteste und
    # umfangreichste der vier. Sonst auf die eigene Seite.
    paare.append(("x-default", entsprechungen.get("pl", eigen)))
    return "\n".join(f'  <link rel="alternate" hreflang="{lang}" href="{href}" />'
                     for lang, href in paare)


def head_neu_schreiben(inhalt, datei):
    neu = hreflang_block(datei)
    muster = re.compile(r'[ \t]*<link rel="alternate" hreflang="[^"]*" href="[^"]*"[ \t]*/?>[ \t]*\n?')
    ohne_alte = muster.sub("", inhalt)
    return re.sub(r'(<link rel="canonical" href="[^"]*"\s*/?>)',
                  lambda m: m.group(1) + "\n" + neu, ohne_alte, count=1)


def fusszeile_ergaenzen(inhalt, datei):
    if MARKER in inhalt:
        return inhalt
    entsprechungen = ENTSPRECHUNGEN.get(datei, {})
    if not entsprechungen:
        return inhalt
    links = " · ".join(
        f'<a href="{href}" hreflang="{lang}" lang="{lang.split("-")[0]}" '
        f'style="color:inherit;">{NAMEN[lang]}</a>'
        for lang, href in entsprechungen.items())
    zeile = f'<p class="footer__tagline" {MARKER}>{links}</p>'
    muster = re.compile(r'(<p class="footer__tagline">.*?</p>)', re.S)
    if muster.search(inhalt):
        return muster.sub(lambda m: m.group(1) + "\n        " + zeile, inhalt, count=1)
    return inhalt


def main():
    geaendert = 0
    for datei in sorted(glob.glob("*.html")):
        if datei in UEBERSPRUNGEN:
            continue
        inhalt = open(datei, encoding="utf-8").read()
        neu = fusszeile_ergaenzen(head_neu_schreiben(inhalt, datei), datei)
        if neu != inhalt:
            open(datei, "w", encoding="utf-8").write(neu)
            geaendert += 1
    print(f"Aktualisierte Seiten: {geaendert}")
    print(f"Seiten mit Entsprechungen in anderen Sprachen: {len(ENTSPRECHUNGEN)}")


if __name__ == "__main__":
    main()
