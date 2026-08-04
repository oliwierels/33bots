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
`a11y.js`, `robots.txt`, `sitemap.xml`, `feed.xml`, `llms.txt` und `_redirects`
ins Wurzelverzeichnis. Bilder, Videos, Schriften und
`style.css` liegen dort fest und werden nur auf Vollständigkeit geprüft.

Texte werden **nicht** in den HTML-Dateien geändert, sondern in den Modulen
unter `build/` — sonst überschreibt der nächste Lauf die Änderung.

Zentrale Einstellungen (Domain, Kontaktdaten, Preise, GTM- und Albacross-ID)
stehen oben in `build/generate_site.py`.

## Rechtliche Konformität

- **Keine Analyse-Dienste aktiv**: Die Seite setzt ausschließlich technisch
  notwendige Cookies. Es werden keine Nutzungsprofile erstellt und keine Daten
  an Dritte übermittelt — eine Cookie-Einwilligung ist daher nicht erforderlich
  und es wird kein Banner ausgespielt.
- **Einwilligung vorbereitet** (§ 25 TDDDG, Art. 6 DSGVO): Sobald in
  `build/generate_site.py` eine `GTM_ID` oder `ALBACROSS_ID` eingetragen wird,
  erscheinen automatisch der Opt-in-Banner, `consent.js` und die passenden
  Abschnitte der Datenschutzerklärung. Tags laden dann erst nach Zustimmung.
- **Inter lokal gehostet** statt Google Fonts (LG München I, 3 O 17493/20).
  Beim Seitenaufruf werden keinerlei Verbindungen zu Dritten aufgebaut.
- **Impressum** (§ 5 DDG), **Datenschutzerklärung** (Art. 13 DSGVO),
  **Erklärung zur Barrierefreiheit** (BFSG), jeweils im Seitenfuß verlinkt.
- **Barrierefreiheit** (BFSG): Panel für Schriftgröße, helle Darstellung, hohen
  Kontrast und das Abschalten von Animationen; Sprunglink zum Hauptinhalt,
  sichtbarer Tastaturfokus, Unterstützung von `prefers-reduced-motion`.

### Status: bereit zum Deployment

Alle Pflichtangaben sind hinterlegt, es sind keine Platzhalter mehr offen.
Der Build läuft ohne Warnung durch.

| Punkt | Stand |
|---|---|
| Impressum § 5 DDG | vollständig |
| Datenschutzerklärung Art. 13 DSGVO | vollständig, bildet den technischen Stand ab |
| Erklärung zur Barrierefreiheit (BFSG) | vollständig |
| Cookies / Einwilligung | keine nicht notwendigen Cookies, kein Banner nötig |
| Verbindungen zu Dritten | keine |
| Kontakt | `kontakt@33bots.de` + Kontaktformular auf jeder Seite |

### Deployment

Alles im Wurzelverzeichnis **außer `build/`** wird ausgeliefert:

```
*.html  *.css  *.js  fonts/  og/  video/  *.jpg  *.webp  *.png  *.svg
robots.txt  sitemap.xml  feed.xml  llms.txt  _redirects
<indexnow-key>.txt
```

Bei Netlify genügt es, den Branch zu verbinden — `_redirects` erzwingt die
Weiterleitung von `www` und `http` auf `https://33bots.de`. Ein Build-Command
wird nicht benötigt, die Seite ist statisch.

### Optional, nach dem Livegang

**Telefonnummer.** Es ist bewusst keine hinterlegt. Nach § 5 DDG ist das
zulässig, solange ein zweiter Kanal für schnelle Kommunikation existiert — das
ist hier das Kontaktformular auf jeder Seite (EuGH C-298/07, Deutsche Internet
Versicherung). Soll doch eine Nummer erscheinen, muss sie in `contact_section`,
im Footer-NAP und in den JSON-LD-Blöcken ergänzt werden.

**Umsatzsteuer-Identifikationsnummer.** Im Impressum steht `PL5253090645`. Das
ist die korrekte Form der NIP für innergemeinschaftliche Umsätze — **sofern
eine Registrierung als EU-Umsatzsteuerzahler (VAT-UE) besteht.** Falls nicht,
in `COMPANY["vat_id"]` auf `Steuernummer (NIP): 5253090645` ändern. Prüfbar
über <https://ec.europa.eu/taxation_customs/vies/>.

**Analytics aktivieren.** Einen eigenen GTM-Container für die .de-Domain
anlegen (nicht den polnischen verwenden — sonst vermischen sich die Daten
beider Märkte und die ausgespielten Tags stehen nicht in der deutschen
Datenschutzerklärung). Dann in `build/generate_site.py`:

```python
GTM_ID = "GTM-XXXXXXX"
COMPANY["gtm_services"] = "Google Analytics 4"   # tatsächlich ausgespielte Dienste
```

Nach dem Neubau erscheinen Consent-Banner und die Analyse-Abschnitte der
Datenschutzerklärung automatisch.

## Nach dem Deployment

IndexNow-Meldung an Bing, Yandex und Seznam:

```bash
./build/scripts/indexnow-submit.sh
```

Der Key liegt als `<key>.txt` im Wurzelverzeichnis und muss mit deployt werden.
