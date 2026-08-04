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

**1. Google-Tag-Manager-Dienste — letzte offene Angabe**

Im Block `COMPANY` oben in `build/generate_site.py` fehlt noch ein Feld:

```python
"gtm_services": "",   # z. B. "Google Analytics 4" oder "keine weiteren Dienste"
```

Die DSGVO verlangt, die Empfänger personenbezogener Daten zu benennen. Prüfen
Sie im GTM-Container, welche Tags tatsächlich ausgespielt werden, tragen Sie
diese ein und bauen Sie neu:

```bash
cd build && python3 generate_site.py
```

Sobald das Feld gefüllt ist, verschwinden der gelbe Marker auf der Seite, die
Redaktionshinweise und die Build-Warnung automatisch.

Alle übrigen Pflichtangaben sind hinterlegt: Firmierung, Anschrift, Vertretung,
CEIDG-Eintrag mit REGON, Steuernummer, inhaltlich Verantwortlicher,
Datenschutz-Aufsichtsbehörde (UODO) und Marktüberwachungsstelle (MLBF).

**2. Umsatzsteuer-Identifikationsnummer prüfen**

Im Impressum steht `PL5253090645` als USt-IdNr. Das ist die korrekte Form der
NIP für innergemeinschaftliche Umsätze — **sofern eine Registrierung als
EU-Umsatzsteuerzahler (VAT-UE) besteht.** Ist das nicht der Fall, darf die
Nummer nicht als USt-IdNr. geführt werden; dann in `COMPANY["vat_id"]` auf
`Steuernummer (NIP): 5253090645` ändern.

Prüfbar über das VIES-Portal der EU-Kommission:
<https://ec.europa.eu/taxation_customs/vies/>

Die Datenschutzerklärung bildet den technischen Stand dieser Website korrekt
ab, sollte aber vor der Veröffentlichung juristisch gegengelesen werden.

**3. Telefonnummern**

Die E-Mail-Adresse ist auf `kontakt@33bots.de` gesetzt. Die Rufnummern sind
weiterhin die polnischen (+48) — sie funktionieren, wirken auf einer .de-Domain
aber ungewohnt. Anpassung in `build/generate_site.py`, Konstanten
`PHONE_HUMAN`, `PHONE_RAW`, `PHONE2_HUMAN`, `PHONE2_RAW`.

**4. Google Tag Manager**

Derzeit derselbe Container wie die polnische Seite (`GTM_ID`). Für eine saubere
Auswertung einen eigenen Container anlegen und die ID eintragen. Läuft der
deutsche Traffic weiter über den polnischen Container, vermischen sich die
Daten beider Märkte.

## Nach dem Deployment

IndexNow-Meldung an Bing, Yandex und Seznam:

```bash
./build/scripts/indexnow-submit.sh
```

Der Key liegt als `<key>.txt` im Wurzelverzeichnis und muss mit deployt werden.
