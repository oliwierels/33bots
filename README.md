# 33bots.at — Website für den österreichischen Markt

Statische Website für Österreich: Vermietung humanoider Roboter Unitree G1
für Events, Messen und Konferenzen.

Dieser Branch enthält **ausschließlich die österreichische Seite**. Sie liegt
direkt im Wurzelverzeichnis und wird als Root einer eigenen Domain deployt —
nicht als Unterverzeichnis der polnischen oder der deutschen Seite.

> **Nicht nach `main` mergen.** Auf `main` liegt die polnische Seite (33bots.pl),
> auf `claude/de-cena-2499-bez-doplat` die deutsche (33bots.de). Ein Merge würde
> sie überschreiben. Dieser Branch wird direkt auf die österreichische Domain
> ausgeliefert.

## Aufbau

```
/                     Deploy-Root der Domain
  *.html              178 Seiten
  style.css           Layout (identisch zur polnischen Seite)
  assets-redesign.css Tailwind-Build der Startseite
  a11y.css            Barrierefreiheit-Panel, Kontrast-, Schriftgrößen-Modi
  gallery.css         Fotogalerie der Realisierungen
  main.js             Navigation, FAQ, Kontaktformular
  a11y.js             Logik des Barrierefreiheit-Panels
  fonts/              Inter und Space Grotesk, lokal gehostet (kein Google Fonts)
  og/                 Open-Graph-Karten je Seite (deutschsprachig)
  video/              Videos der Roboter-Einsätze
  *.jpg *.webp        Fotos aus echten Einsätzen
  robots.txt sitemap.xml feed.xml llms.txt _redirects .htaccess
  <indexnow-key>.txt

build/                Generator (wird nicht deployt)
  generate_site.py    Baut alle Seiten ins Wurzelverzeichnis
  make_og.py          Baut die Open-Graph-Karten aus den Seitentiteln
  at_slugs.py         Dateinamen aller Seiten
  at_structure.py     Seitenreihenfolge, interne Verlinkung, Video-Zuordnung
  at_content_*.py     Texte der SEO-Unterseiten
  at_cities.py        35 österreichische Städte mit Locations und Umgebung
  at_pages_manual.py  Angebotsseiten, Case Studies, Rechtsseiten
  at_blog.py          40 Blogartikel, Blog-Hub, RSS-Feed
  scripts/            IndexNow-Meldung nach dem Deployment
```

Die Startseite `index.html` wird **nicht** vom Generator geschrieben: Sie läuft
auf dem Tailwind-Redesign und wird direkt im Wurzelverzeichnis gepflegt.

## Seiten

| Bereich | Anzahl |
|---|---|
| SEO-Unterseiten (Anlässe, Rollen, Branchen) | 84 |
| Städteseiten | 35 |
| Blogartikel | 40 |
| Startseite, Angebot, Case Studies, Referenzen, Blog-Hub | 16 |
| Impressum, Datenschutz, Barrierefreiheit | 3 |
| **Summe** | **178** |

## Website neu bauen

```bash
cd build && python3 generate_site.py && python3 make_og.py
```

Der Generator schreibt alle HTML-Dateien sowie `a11y.css`, `gallery.css`,
`a11y.js`, `robots.txt`, `sitemap.xml`, `feed.xml`, `llms.txt`, `_redirects`
und `.htaccess` ins Wurzelverzeichnis. `make_og.py` erzeugt daraus die
Open-Graph-Karten (benötigt Pillow). Bilder, Videos, Schriften, `style.css`
und `index.html` liegen dort fest.

Texte werden **nicht** in den HTML-Dateien geändert, sondern in den Modulen
unter `build/` — sonst überschreibt der nächste Lauf die Änderung. Die
Startseite ist die Ausnahme: Sie wird direkt in `index.html` gepflegt.

Zentrale Einstellungen (Domain, Kontaktdaten, Preise `PRICE_FROM`/`DOG_PRICE`,
GTM- und Albacross-ID) stehen oben in `build/generate_site.py`.

## Städte

Wien, Graz, Linz, Salzburg, Innsbruck, Klagenfurt, Villach, Wels, St. Pölten,
Dornbirn, Wiener Neustadt, Steyr, Bregenz, Feldkirch, Leoben, Krems, Baden,
Eisenstadt, Klosterneuburg, Mödling, Schwechat, Amstetten, Kufstein, Schwaz,
Hallein, Traun, Leonding, Spittal an der Drau, Wolfsberg, Braunau am Inn,
Tulln, Bad Ischl, Zell am See, Kitzbühel, Velden am Wörthersee.

## Rechtliche Konformität (Österreich)

- **Impressum** nach § 5 ECG samt **Offenlegung** nach § 25 MedienG,
  **Datenschutzerklärung** nach Art. 13 DSGVO und **Erklärung zur
  Barrierefreiheit** nach dem Barrierefreiheitsgesetz (BaFG, in Kraft seit
  28. Juni 2025) — jeweils im Seitenfuß verlinkt.
- **Keine Analyse-Dienste aktiv**: Die Seite setzt ausschließlich technisch
  notwendige Cookies, die nach § 165 Abs. 3 TKG 2021 einwilligungsfrei sind.
  Es werden keine Nutzungsprofile erstellt — ein Consent-Banner ist deshalb
  nicht erforderlich und wird nicht ausgespielt.
- **Einwilligung vorbereitet**: Sobald in `build/generate_site.py` eine
  `GTM_ID` oder `ALBACROSS_ID` eingetragen wird, erscheinen automatisch der
  Opt-in-Banner, `consent.js` und die passenden Abschnitte der
  Datenschutzerklärung. Tags laden dann erst nach Zustimmung.
- **Schriften lokal gehostet** statt Google Fonts. Beim Seitenaufruf werden
  keinerlei Verbindungen zu Dritten aufgebaut.
- **Kein Hinweis auf die EU-ODR-Plattform**: Sie wurde am 20. Juli 2025
  eingestellt; ein Link darauf wäre irreführend.

### Status: bereit zum Deployment

| Punkt | Stand |
|---|---|
| Impressum § 5 ECG | vollständig |
| Offenlegung § 25 MedienG | vollständig (inkl. Blattlinie) |
| Datenschutzerklärung Art. 13 DSGVO | vollständig, bildet den technischen Stand ab |
| Erklärung zur Barrierefreiheit (BaFG) | vollständig |
| Cookies / Einwilligung | keine nicht notwendigen Cookies, kein Banner nötig |
| Verbindungen zu Dritten | keine |
| Kontakt | `kontakt@33bots.at` + Kontaktformular auf jeder Seite |

### Deployment

Alles im Wurzelverzeichnis **außer `build/`** wird ausgeliefert. Bei Netlify
genügt es, den Branch zu verbinden — `_redirects` erzwingt die Weiterleitung
von `www` und `http` auf `https://33bots.at`. Ein Build-Command wird nicht
benötigt, die Seite ist statisch.

Vor dem Livegang zu prüfen:

- **E-Mail-Postfach** `kontakt@33bots.at` muss existieren; es steht im
  Impressum, in der Datenschutzerklärung und im Kontaktbereich jeder Seite.
- **Formspree-Endpoint** in `build/generate_site.py` — derzeit derselbe wie
  auf der deutschen Seite; für saubere Trennung der Märkte einen eigenen
  anlegen.
- **Umsatzsteuer-Identifikationsnummer.** Im Impressum steht `PL5253090645`.
  Das ist die korrekte Form der NIP für innergemeinschaftliche Umsätze —
  **sofern eine Registrierung als EU-Umsatzsteuerzahler (VAT-UE) besteht.**
  Falls nicht, in `COMPANY["vat_id"]` auf `Steuernummer (NIP): 5253090645`
  ändern. Prüfbar über <https://ec.europa.eu/taxation_customs/vies/>.
- **Analytics**: einen eigenen GTM-Container für die .at-Domain anlegen (nicht
  den polnischen oder deutschen verwenden — sonst vermischen sich die Daten der
  Märkte und die ausgespielten Tags stehen nicht in der österreichischen
  Datenschutzerklärung). Dann in `build/generate_site.py`:

```python
GTM_ID = "GTM-XXXXXXX"
COMPANY["gtm_services"] = "Google Analytics 4"   # tatsächlich ausgespielte Dienste
```

## Nach dem Deployment

IndexNow-Meldung an Bing, Yandex und Seznam:

```bash
./build/scripts/indexnow-submit.sh
```

Der Key liegt als `<key>.txt` im Wurzelverzeichnis und muss mit deployt werden.
Er gilt nur für 33bots.at — der Key der deutschen Seite funktioniert hier nicht.
