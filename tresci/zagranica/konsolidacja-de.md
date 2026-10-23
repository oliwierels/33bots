# Konsolidacja 33bots.de (23.10.2026)

Na 33bots.de było 190 stron, w tym 96 z jednego szablonu „Roboter für X” (mediana 50% wspólnej treści
między dwiema stronami, np. Taufe i Kommunion 73%) i 35 miast (~60% wspólnej treści). Takie strony
Google traktuje jak masowo generowane; dla młodej domeny bez linków to hamulec dla całego serwisu.
Konkurencja z pierwszych miejsc (roboticrental.de, robotollern.de, roboter-mieten.at) ma 20–140 stron.

Zostało 84 stron: oferty, 15 stron tematycznych, 14 największych rynków eventowych, poradniki, case
studies i strony prawne. Pozostałe 106 adresów przekierowuje 301 na najbliższą mocną stronę
(reguły w `.htaccess` repozytorium 33bots.de, sekcja „Konsolidacja 2026-10-23”). Linki wewnętrzne
prowadzą od razu do celu; linki do usuniętych miast zniknęły z list miast.

Cofnięcie: usunąć regułę z `.htaccess` i przywrócić plik z historii git (commit przed konsolidacją).

| Cel (strona, która zostaje) | Przekierowane adresy |
|---|---|
| `/roboter-firmenevents.html` | `roboter-automotive-event`, `roboter-bau-event`, `roboter-beauty-event`, `roboter-corporate-event`, `roboter-energie-event`, `roboter-finanz-event`, `roboter-franchise`, `roboter-fuer-unternehmen-mieten`, `roboter-gaming-event`, `roboter-gastro-event`, `roboter-immobilien-event`, `roboter-industrie-event`, `roboter-it-event`, `roboter-legal-event`, `roboter-logistik-event`, `roboter-nachhaltigkeits-event`, `roboter-roadshow`, `roboter-startup-event`, `roboter-telekom-event`, `roboter-tourismus-event` |
| `/angebot-konferenzen-galas.html` | `roboter-bankett`, `roboter-charity-event`, `roboter-convention`, `roboter-gala`, `roboter-hybrid-event`, `roboter-konferenz`, `roboter-medizin-event`, `roboter-pharma-event`, `roboter-tech-konferenz`, `roboter-vip-event`, `roboter-zeremonie` |
| `/roboter-privatfeier.html` | `roboter-abiball`, `roboter-fuer-kinder`, `roboter-gartenparty`, `roboter-geburtstag`, `roboter-halloween`, `roboter-kinderfest`, `roboter-kommunion`, `roboter-party`, `roboter-silvester`, `roboter-taufe`, `roboter-valentinstag` |
| `/roboter-stadtfest.html` | `roboter-festival`, `roboter-karneval`, `roboter-kultur-event`, `roboter-oktoberfest`, `roboter-outdoor-event`, `roboter-sport-event`, `roboter-stadt-event` |
| `/roboter-firmenfeier.html` | `roboter-betriebsfest`, `roboter-firmenjubilaeum`, `roboter-jubilaeum`, `roboter-teambuilding`, `roboter-teamevent` |
| `/roboter-eroeffnung.html` | `roboter-einkaufszentrum`, `roboter-einzelhandel`, `roboter-handel-event`, `roboter-shoppingcenter` |
| `/roboter-mieten-duesseldorf.html` | `roboter-mieten-duisburg`, `roboter-mieten-krefeld`, `roboter-mieten-moenchengladbach`, `roboter-mieten-wuppertal` |
| `/angebot-messen.html` | `roboter-ausstellung`, `roboter-expo`, `roboter-messe` |
| `/` | `leistungen`, `roboter-event`, `roboter-mieten` |
| `/roboter-gaesteempfang.html` | `roboter-hotel`, `roboter-restaurant`, `roboter-rezeptionist` |
| `/roboter-mieten-frankfurt.html` | `roboter-mieten-mainz`, `roboter-mieten-mannheim`, `roboter-mieten-wiesbaden` |
| `/roboter-mieten-leipzig.html` | `roboter-mieten-chemnitz`, `roboter-mieten-halle`, `roboter-mieten-magdeburg` |
| `/roboter-produktlaunch.html` | `roboter-fashion-event`, `roboter-marketing`, `roboter-praesentator` |
| `/roboter-eventmoderation.html` | `roboter-moderator`, `roboter-redner` |
| `/roboter-hochschule.html` | `roboter-bildungs-event`, `roboter-schulung` |
| `/roboter-hochzeit.html` | `roboter-junggesellinnenabschied`, `roboter-polterabend` |
| `/roboter-mieten-dortmund.html` | `roboter-mieten-bielefeld`, `roboter-mieten-muenster` |
| `/roboter-mieten-hamburg.html` | `roboter-mieten-kiel`, `roboter-mieten-luebeck` |
| `/roboter-mieten-koeln.html` | `roboter-mieten-aachen`, `roboter-mieten-bonn` |
| `/roboter-mieten-stuttgart.html` | `roboter-mieten-freiburg`, `roboter-mieten-karlsruhe` |
| `/roboter-show.html` | `roboter-buehnenshow`, `roboter-taenzer` |
| `/roboter-werbung-film.html` | `roboter-fotoshooting`, `roboter-musikvideo` |
| `/angebot-tag-der-offenen-tuer.html` | `roboter-tag-der-offenen-tuer` |
| `/event-attraktionen.html` | `moderne-event-attraktionen` |
| `/humanoiden-roboter-mieten.html` | `humanoider-roboter-event` |
| `/roboter-employer-branding.html` | `roboter-karrieremesse` |
| `/roboter-mieten-essen.html` | `roboter-mieten-bochum` |
| `/roboter-mieten-hannover.html` | `roboter-mieten-braunschweig` |
| `/roboter-mieten-muenchen.html` | `roboter-mieten-augsburg` |
| `/roboter-weihnachtsfeier.html` | `roboter-nikolaus` |
