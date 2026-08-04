# 33bots.de — deutschsprachige Website

Statische Website für den deutschen Markt: Vermietung humanoider Roboter
Unitree G1 für Events, Messen und Konferenzen.

Dieser Branch enthält **ausschließlich die deutsche Seite**. Sie liegt direkt im
Wurzelverzeichnis und wird als Root einer eigenen Domain deployt — nicht als
Unterverzeichnis der polnischen Seite.

> **Nicht nach `main` mergen.** Auf `main` liegt die polnische Seite (33bots.pl).
> Ein Merge würde sie löschen. Dieser Branch wird direkt auf die deutsche Domain
> ausgeliefert.

## Aufbau

```
/                     Deploy-Root der Domain
  *.html              192 Seiten
  style.css           Layout (identisch zur polnischen Seite)
  a11y.css            Barrierefreiheit-Panel, Kontrast-, Schriftgrößen-Modi
  gallery.css         Fotogalerie der Realisierungen
  main.js             Navigation, FAQ, Kontaktformular
  a11y.js             Logik des Barrierefreiheit-Panels
  consent.js          Cookie-Einwilligung, lädt Analyse-Tags erst nach Opt-in
  fonts/              Inter, lokal gehostet (kein Google Fonts)
  og/                 Open-Graph-Bilder je Seite
  video/              Videos der Roboter-Einsätze
  *.jpg *.webp        Fotos aus echten Einsätzen
  robots.txt sitemap.xml feed.xml llms.txt _redirects

build/                Generator (wird nicht deployt)
  generate_site.py    Baut alle Seiten ins Wurzelverzeichnis
  de_slugs.py         Dateinamen aller Seiten
  de_structure.py     Seitenreihenfolge, interne Verlinkung, Video-Zuordnung
  de_content_*.py     Texte der SEO-Unterseiten
  de_cities.py        35 Städte mit Locations und Umgebung
  de_pages_manual.py  Startseite, Angebotsseiten, Case Studies, Rechtsseiten
  de_blog.py          40 Blogartikel, Blog-Hub, RSS-Feed
  scripts/            IndexNow-Meldung nach dem Deployment
```

## Seiten

| Bereich | Anzahl |
|---|---|
| SEO-Unterseiten (Anlässe, Rollen, Branchen) | 98 |
| Städteseiten | 35 |
| Blogartikel | 40 |
| Startseite, Angebot, Case Studies, Referenzen, Blog-Hub | 16 |
| Impressum, Datenschutz, Barrierefreiheit | 3 |
| **Summe** | **192** |

## Website neu bauen

```bash
cd build && python3 generate_site.py
```

Der Generator schreibt alle HTML-Dateien sowie `a11y.css`, `gallery.css`,
`a11y.js`, `consent.js`, `robots.txt`, `sitemap.xml`, `feed.xml`, `llms.txt`
und `_redirects` ins Wurzelverzeichnis. Bilder, Videos, Schriften und
`style.css` liegen dort fest und werden nur auf Vollständigkeit geprüft.

Texte werden **nicht** in den HTML-Dateien geändert, sondern in den Modulen
unter `build/` — sonst überschreibt der nächste Lauf die Änderung.

Zentrale Einstellungen (Domain, Kontaktdaten, Preise, GTM- und Albacross-ID)
stehen oben in `build/generate_site.py`.

## Rechtliche Konformität

- **Cookies opt-in** (§ 25 TDDDG, Art. 6 DSGVO): Google Tag Manager und
  Albacross laden erst nach ausdrücklicher Einwilligung. Kein GTM-`noscript`,
  keine Preconnects zu Analyse-Diensten.
- **Inter lokal gehostet** statt Google Fonts (LG München I, 3 O 17493/20).
  Beim Seitenaufruf werden keinerlei Verbindungen zu Dritten aufgebaut.
- **Impressum** (§ 5 DDG), **Datenschutzerklärung** (Art. 13 DSGVO),
  **Erklärung zur Barrierefreiheit** (BFSG), jeweils im Seitenfuß verlinkt.
- **Barrierefreiheit** (BFSG): Panel für Schriftgröße, helle Darstellung, hohen
  Kontrast und das Abschalten von Animationen; Sprunglink zum Hauptinhalt,
  sichtbarer Tastaturfokus, Unterstützung von `prefers-reduced-motion`.

### Vor dem Livegang zu erledigen

1. **Gelb markierte Felder** in `impressum.html` und `datenschutz.html` mit den
   tatsächlichen Unternehmensdaten befüllen (Firmierung, Anschrift, Register,
   USt-IdNr., Aufsichtsbehörde). Ein unvollständiges Impressum ist abmahnfähig.
   Zu ändern in `build/de_pages_manual.py`, Funktion `build_legal_pages`.
2. **Kontaktdaten**: aktuell die polnische Adresse und Rufnummern. Nach
   Einrichtung eines deutschen Postfachs oben in `build/generate_site.py`
   anpassen.
3. **IndexNow-Key** für die neue Domain erzeugen, siehe
   `build/scripts/indexnow-submit.sh`.
4. **Google Tag Manager**: derzeit derselbe Container wie die polnische Seite.
   Für saubere Auswertung einen eigenen Container anlegen.
