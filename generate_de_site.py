#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator niemieckiej wersji serwisu 33bots (osobna domena, osobny serwis).

Wynik trafia do katalogu ``de/`` — jest to samodzielny, kompletny serwis,
który wgrywa się jako ROOT domeny .de (nie jako podkatalog 33bots.pl).

Uruchomienie:
    python3 generate_de_site.py
"""

import os
import shutil

# ── Konfiguracja serwisu ──────────────────────────────────────────────
OUT = "de"
DOMAIN = "https://33bots.de"
EMAIL = "kontakt@33bots.pl"
PHONE_HUMAN = "+48 531 408 004"
PHONE_RAW = "+48531408004"
PHONE2_HUMAN = "+48 601 499 947"
PHONE2_RAW = "+48601499947"
GTM_ID = "GTM-MR7R7CJ3"
ALBACROSS_ID = "89159321"

PRICE_LOW = "1.290"
PRICE_HIGH = "1.590"
PRICE_RANGE = f"{PRICE_LOW} – {PRICE_HIGH} €"
PRICE_LOW_NUM = "1290"
PRICE_HIGH_NUM = "1590"
DOG_PRICE = "450 €"

TODAY = "2026-08-03"

# Pliki statyczne kopiowane z serwisu PL (identyczna szata graficzna)
ASSETS = [
    "favicon.svg",
    "logo.png",
    "og-image.jpg",
    "robot-g1.jpg",
    "robot-g1.webp",
    "robot-g1-960.webp",
    "robot-g1-action.jpg",
    "robot-g1-action.webp",
    "robot-g1-studio.jpg",
    "robot-g1-studio.webp",
    "realizacja-robot-gala-dresden.jpg",
    "realizacja-robot-gala-dresden.webp",
]
VIDEO_ASSETS = [
    "33bots-robot-event.mp4",
    "33bots-robot-event-poster.jpg",
    "robot-taniec.mp4",
    "robot-taniec-poster.jpg",
]

# ── Strony ofertowe ───────────────────────────────────────────────────
OFFER_PAGES = [
    ("roboter-mieten.html", "Humanoiden Roboter mieten"),
    ("messen.html", "Messen & Ausstellungen"),
    ("konferenzen.html", "Konferenzen & Galas"),
    ("tag-der-offenen-tuer.html", "Tage der offenen Tür"),
]

# ── Miasta ────────────────────────────────────────────────────────────
# slug, Stadt, Bundesland/Region, Kurz-Claim, Venues (lista), Umland (str)
CITIES = [
    dict(
        slug="berlin", city="Berlin", city_gen="Berlins", region="Berlin und Brandenburg",
        claim="Hauptstadt-Events, Tech-Konferenzen und Produktlaunches",
        lead="Berlin ist der dichteste Event-Markt Deutschlands: Tech-Konferenzen, Startup-Summits, "
             "Markenlaunches und Corporate-Galas laufen hier oft am selben Wochenende parallel. "
             "Genau deshalb entscheidet Aufmerksamkeit — und ein humanoider Roboter liefert sie sofort.",
        venues=[
            ("Messe Berlin & CityCube", "Internationale Leitmessen und Kongresse unter dem Funkturm."),
            ("Estrel Congress Center", "Großkongresse, Galas und Award-Nächte in Neukölln."),
            ("Station Berlin", "Industrie-Loft-Flächen für Tech-Konferenzen und Produktlaunches."),
            ("Flughafen Tempelhof", "Großformatige Marken-Events und Roadshows in den Hangars."),
        ],
        around="Mitte, Kreuzberg, Prenzlauer Berg, Charlottenburg, Adlershof sowie Potsdam und das Berliner Umland",
        faq=[
            ("Fahren Sie auch zu Locations außerhalb des Berliner Rings?",
             "Ja. Wir bedienen ganz Berlin und Brandenburg ohne Anfahrtsaufschlag — von Adlershof über Spandau "
             "bis nach Potsdam, Oranienburg oder Königs Wusterhausen. Der genannte Preis ist der Endpreis."),
            ("Eignet sich der Roboter für eine Tech-Konferenz in Berlin?",
             "Absolut. Der Unitree G1 ist genau in diesem Umfeld zu Hause: Er läuft frei über die Fläche, begrüßt "
             "Gäste am Registration Desk und liefert den Gesprächsanlass, den Sie sich für Ihre Keynote wünschen."),
        ],
    ),
    dict(
        slug="muenchen", city="München", city_gen="Münchens", region="München und Oberbayern",
        claim="Messen, Automotive-Events und Premium-Galas",
        lead="München verbindet internationale Leitmessen mit einem der stärksten Corporate-Märkte Europas. "
             "Automotive, Tech, Pharma und Finance treffen sich hier — und erwarten auf dem Stand mehr als eine Videowand.",
        venues=[
            ("Messe München & ICM", "Leitmessen wie bauma, electronica oder EXPO REAL."),
            ("MOC Veranstaltungscenter", "Fachmessen und Corporate-Events im Norden der Stadt."),
            ("Olympiahalle & Kleine Olympiahalle", "Großveranstaltungen, Galas und Firmenjubiläen."),
            ("Hotel Bayerischer Hof", "Premium-Bankette, VIP-Abende und Pressekonferenzen."),
        ],
        around="Schwabing, Riem, Bogenhausen, Sendling sowie Garching, Unterföhring, Ingolstadt und das Münchner Umland",
        faq=[
            ("Kommen Sie auch zur Messe München auf den Stand?",
             "Ja — Standeinsätze auf der Messe München und im ICM sind unser Standardgeschäft. Wir stimmen Aufbauzeiten "
             "und Standordnung vorab mit Ihnen ab und sind rund 30–45 Minuten vor Türöffnung einsatzbereit."),
            ("Ist der Roboter für ein Automotive-Event geeignet?",
             "Sehr gut sogar. Der G1 läuft neben dem Fahrzeug, übernimmt die Enthüllung oder führt Gäste zum Exponat — "
             "ein Format, das im Automotive-Umfeld extrem gut funktioniert und zuverlässig gefilmt wird."),
        ],
    ),
    dict(
        slug="hamburg", city="Hamburg", city_gen="Hamburgs", region="Hamburg und Umland",
        claim="Kongresse, Logistik-Events und Hafen-Locations",
        lead="Hamburg ist Logistik-, Medien- und Kongressstadt zugleich. Vom CCH bis zur Fischauktionshalle "
             "gilt hier dasselbe: Wer auffallen will, braucht ein Format, das die Gäste selbst weitererzählen.",
        venues=[
            ("Hamburg Messe und Congress (CCH)", "Kongresse, Fachmessen und Verbandstagungen in der City."),
            ("Elbphilharmonie & HafenCity", "Repräsentative Abendveranstaltungen mit Signature-Kulisse."),
            ("Fischauktionshalle", "Firmenfeiern und Markenevents direkt an der Elbe."),
            ("Hotel Atlantic & Grand Elysée", "Galadinner, Awards und Corporate-Bankette."),
        ],
        around="HafenCity, Altona, St. Pauli, Bahrenfeld sowie Norderstedt, Ahrensburg, Lübeck und das Hamburger Umland",
        faq=[
            ("Funktioniert der Roboter auch in einer Hafen-Location?",
             "Ja. Der G1 läuft auf Asphalt, Estrich, Teppich und Hallenboden gleichermaßen sicher. Für Außenflächen "
             "brauchen wir lediglich eine trockene, ebene Fläche — bei Regen weichen wir in den überdachten Bereich aus."),
            ("Wie schnell bekomme ich ein Angebot für ein Event in Hamburg?",
             "In der Regel innerhalb von 24 Stunden. Sie erhalten einen konkreten Betrag ohne Sternchen — genau diese "
             "Summe steht später auf der Rechnung."),
        ],
    ),
    dict(
        slug="koeln", city="Köln", city_gen="Kölns", region="Köln und das Rheinland",
        claim="Leitmessen, Karnevalsevents und Markenauftritte",
        lead="Köln lebt von Leitmessen wie der gamescom, der Anuga oder der IMM — und von Marken, die auf dem Stand "
             "sichtbarer sein wollen als der Nachbar. Ein humanoider Roboter löst genau dieses Problem.",
        venues=[
            ("Koelnmesse", "gamescom, Anuga, IMM und weitere internationale Leitmessen."),
            ("Flora Köln", "Galas, Award-Abende und Hochzeiten im historischen Rahmen."),
            ("LANXESS arena", "Großveranstaltungen, Kick-offs und Mitarbeiterevents."),
            ("Motorworld Köln Rheinland", "Produktpremieren und Markenevents mit Industriecharme."),
        ],
        around="Deutz, Ehrenfeld, Mülheim, die Innenstadt sowie Leverkusen, Bergisch Gladbach, Hürth und das Rheinland",
        faq=[
            ("Sind Sie schon auf der gamescom oder Anuga im Einsatz gewesen?",
             "Wir betreuen Messestände in genau diesem Format: hohe Besucherfrequenz, enge Standflächen, langer "
             "Messetag. Der G1 arbeitet den kompletten Tag über — mit unserem Operator durchgehend vor Ort."),
            ("Kostet die Anfahrt nach Köln extra?",
             "Nein. Die Anfahrt ist deutschlandweit im Preis enthalten — ohne Kilometerpauschale und ohne Mindestdistanz."),
        ],
    ),
    dict(
        slug="frankfurt", city="Frankfurt am Main", city_gen="Frankfurts", region="Frankfurt und Rhein-Main",
        claim="Finance-Events, Leitmessen und Kongresse",
        lead="Frankfurt ist Finanzplatz und Messestadt in einem. Banken, Beratungen und Tech-Unternehmen konkurrieren "
             "hier um dieselben Gäste — mit einem humanoiden Roboter gewinnen Sie die Aufmerksamkeit vor dem Pitch.",
        venues=[
            ("Messe Frankfurt & Kap Europa", "Leitmessen und internationale Kongresse mitten in der Stadt."),
            ("Jahrhunderthalle", "Firmenjubiläen, Galas und Mitarbeiterveranstaltungen."),
            ("Festhalle Frankfurt", "Großformatige Marken- und Konzernevents."),
            ("Klassikstadt & Union Halle", "Produktlaunches und Networking-Abende mit Industrieflair."),
        ],
        around="Bankenviertel, Ostend, Niederrad, das Europaviertel sowie Offenbach, Eschborn, Wiesbaden, Mainz und Rhein-Main",
        faq=[
            ("Passt ein Roboter zu einem konservativen Finance-Event?",
             "Ja — wenn er richtig eingesetzt wird. Im Finance-Umfeld arbeiten wir mit ruhigen Formaten: Empfang der "
             "Gäste, Begleitung zur Keynote, Branding auf der Brustplatte. Das wirkt souverän statt verspielt."),
            ("Können Sie unser Logo auf dem Roboter platzieren?",
             "Ja, und zwar ohne Aufpreis. Ihr Logo und ein QR-Code kommen auf die Brustplatte des G1 — bei uns ist das "
             "Branding Teil des Standardpakets."),
        ],
    ),
    dict(
        slug="stuttgart", city="Stuttgart", city_gen="Stuttgarts", region="Stuttgart und Baden-Württemberg",
        claim="Industrie-Events, Automotive und Fachmessen",
        lead="Stuttgart ist Industrie- und Engineering-Hochburg. Hier verstehen die Gäste sofort, was ein humanoider "
             "Roboter technisch bedeutet — und genau deshalb bleiben sie am Stand stehen.",
        venues=[
            ("Messe Stuttgart & ICS", "Fachmessen und Kongresse direkt am Flughafen."),
            ("Liederhalle Stuttgart", "Kongresse, Preisverleihungen und Verbandstagungen."),
            ("Porsche Arena & Hanns-Martin-Schleyer-Halle", "Großveranstaltungen und Konzernevents."),
            ("Wagenhallen", "Kreative Markenevents und Produktpremieren im Industrieambiente."),
        ],
        around="Vaihingen, Feuerbach, Bad Cannstatt sowie Sindelfingen, Ludwigsburg, Esslingen, Böblingen und die Region Stuttgart",
        faq=[
            ("Eignet sich der G1 für ein technisches Fachpublikum?",
             "Besonders gut. Ingenieure fragen nach Freiheitsgraden, Sensorik und Regelung — unser Operator kann diese "
             "Fragen fundiert beantworten, was aus dem Showeffekt ein echtes Fachgespräch macht."),
            ("Welche technischen Voraussetzungen brauchen Sie vor Ort?",
             "Eine normale 230-V-Steckdose und rund 2×2 m freie, ebene Fläche. Internet ist nicht erforderlich. "
             "Der Aufbau dauert 30–45 Minuten."),
        ],
    ),
    dict(
        slug="duesseldorf", city="Düsseldorf", city_gen="Düsseldorfs", region="Düsseldorf und Nordrhein-Westfalen",
        claim="Leitmessen, Mode-Events und Corporate-Galas",
        lead="Düsseldorf verbindet internationale Leitmessen mit einer starken Mode- und Agenturszene. "
             "Wer hier auffallen will, braucht ein Format, das schon beim Vorbeigehen gefilmt wird.",
        venues=[
            ("Messe Düsseldorf & CCD", "drupa, MEDICA, boot und internationale Kongresse."),
            ("Areal Böhler", "Markenevents, Fashion Shows und Produktlaunches in denkmalgeschützten Hallen."),
            ("Classic Remise Düsseldorf", "Premieren und Abendveranstaltungen mit Automobil-Kulisse."),
            ("Rheinterrasse Düsseldorf", "Galadinner und Firmenfeiern direkt am Rhein."),
        ],
        around="Medienhafen, Oberkassel, Golzheim sowie Neuss, Duisburg, Krefeld, Wuppertal und das gesamte Ruhrgebiet",
        faq=[
            ("Können Sie den Roboter auf einer Fashion Show einsetzen?",
             "Ja. Der G1 kann über den Laufsteg gehen, eine Choreografie tanzen oder als Blickfang am Eingang stehen. "
             "Ablauf und Timing stimmen wir vorher mit Ihrer Regie ab."),
            ("Wie lange kann der Roboter am Tag im Einsatz sein?",
             "Wir buchen grundsätzlich den kompletten Veranstaltungstag. Der G1 arbeitet in Intervallen mit kurzen "
             "Akkuwechseln — für die Gäste bleibt er durchgehend verfügbar."),
        ],
    ),
    dict(
        slug="leipzig", city="Leipzig", city_gen="Leipzigs", region="Leipzig und Sachsen",
        claim="Messen, Kongresse und Kulturevents",
        lead="Leipzig hat sich zur wichtigsten Messe- und Kongressstadt Ostdeutschlands entwickelt. "
             "Buchmesse, Fachkongresse und Corporate-Events treffen hier auf ein neugieriges Publikum.",
        venues=[
            ("Leipziger Messe & CCL", "Buchmesse, Fachmessen und internationale Kongresse."),
            ("Kongresshalle am Zoo", "Tagungen, Galas und Verbandsveranstaltungen."),
            ("Kohlrabizirkus & Werk 2", "Markenevents und Partys mit Industriecharakter."),
            ("Quarterback Immobilien Arena", "Großveranstaltungen und Mitarbeiterevents."),
        ],
        around="Plagwitz, Zentrum-Süd, das Graphische Viertel sowie Halle (Saale), Chemnitz, Jena und Mitteldeutschland",
        faq=[
            ("Fahren Sie von Polen aus nach Leipzig ohne Aufschlag?",
             "Ja. Die Anfahrt ist deutschlandweit inklusive — die Entfernung spielt für den Preis keine Rolle."),
            ("Passt der Roboter zu einer Kulturveranstaltung?",
             "Sehr gut. Wir haben den G1 bereits bei Galas und Bühnenauftritten eingesetzt — er kann eine Choreografie "
             "tanzen, gemeinsam mit einem Künstler auftreten oder das Publikum begrüßen."),
        ],
    ),
    dict(
        slug="dresden", city="Dresden", city_gen="Dresdens", region="Dresden und Sachsen",
        claim="Galas, Halbleiter-Industrie und Kongresse",
        lead="Dresden verbindet Hightech — Silicon Saxony, Halbleiter, Forschung — mit einer der schönsten "
             "Gala-Kulissen Deutschlands. Beides passt hervorragend zu einem humanoiden Roboter.",
        venues=[
            ("Messe Dresden", "Fachmessen, Firmenevents und Ausstellungen in der Ostragehege."),
            ("Internationales Congress Center Dresden", "Kongresse und Tagungen direkt an der Elbe."),
            ("Gläserne Manufaktur", "Produktpremieren und Technologie-Events."),
            ("Schloss Albrechtsberg & Hotel Taschenbergpalais", "Galadinner und repräsentative Abendveranstaltungen."),
        ],
        around="Neustadt, Johannstadt, Ostragehege sowie Freiberg, Meißen, Chemnitz und die Region Sachsen",
        faq=[
            ("Haben Sie bereits in Dresden gearbeitet?",
             "Ja — eine unserer Gala-Realisierungen fand in Dresden statt. Bilder davon finden Sie auf dieser Seite."),
            ("Eignet sich der Roboter für ein Event der Halbleiter- oder Forschungsbranche?",
             "Ja. Bei technischem Publikum funktioniert der G1 doppelt: als Blickfang und als fachlicher Gesprächsanlass "
             "über Sensorik, Aktuatorik und Embodied AI."),
        ],
    ),
    dict(
        slug="hannover", city="Hannover", city_gen="Hannovers", region="Hannover und Niedersachsen",
        claim="Industriemessen, HANNOVER MESSE und B2B-Events",
        lead="Hannover ist der Ort, an dem Industrie 4.0 jedes Jahr neu verhandelt wird. Auf der HANNOVER MESSE "
             "oder der IAA Transportation zählt am Stand vor allem eines: Wer bleibt stehen?",
        venues=[
            ("Deutsche Messe Hannover", "HANNOVER MESSE, IAA Transportation, DOMOTEX und mehr."),
            ("Hannover Congress Centrum (HCC)", "Kongresse, Tagungen und Preisverleihungen."),
            ("Expo Plaza & Design Center", "Markenevents und Konferenzen im Expo-Areal."),
            ("Schloss Herrenhausen", "Repräsentative Abendveranstaltungen und Empfänge."),
        ],
        around="Mitte, Laatzen, List sowie Braunschweig, Wolfsburg, Hildesheim, Celle und Niedersachsen",
        faq=[
            ("Wie funktioniert ein Roboter auf einem Messestand mit hoher Frequenz?",
             "Genau dafür ist das Format gemacht. Der G1 zieht Besucher aus mehreren Metern Entfernung an, Ihr Team "
             "übernimmt das Gespräch. In der Praxis steigt die Standfrequenz spürbar."),
            ("Können wir den Roboter für mehrere Messetage buchen?",
             "Ja — und ab zwei Tagen erhalten Sie 15 % Rabatt auf jeden Tag. Bei Messen ist das der Regelfall."),
        ],
    ),
    dict(
        slug="nuernberg", city="Nürnberg", city_gen="Nürnbergs", region="Nürnberg und Franken",
        claim="Fachmessen, Embedded-Tech und Firmenevents",
        lead="Nürnberg ist Heimat von Leitmessen wie der embedded world und der Spielwarenmesse — ein Publikum, "
             "das Technik erkennt und Roboter ernst nimmt.",
        venues=[
            ("NürnbergMesse & NCC", "embedded world, Spielwarenmesse, BrauBeviale und Kongresse."),
            ("Meistersingerhalle", "Tagungen, Galas und Verbandsveranstaltungen."),
            ("Z-Bau & Kulturwerkstatt Auf AEG", "Markenevents und Partys im Industrieambiente."),
            ("Kaiserburg & Historischer Rathaussaal", "Repräsentative Empfänge und Abendveranstaltungen."),
        ],
        around="Südstadt, Gostenhof, Langwasser sowie Fürth, Erlangen, Bamberg, Würzburg und die Metropolregion Nürnberg",
        faq=[
            ("Ist der Roboter auf der embedded world ein Thema?",
             "Definitiv. Ein realer humanoider Roboter am Stand ist auf einer Embedded-Messe der stärkste denkbare "
             "Demonstrator — technisch anschlussfähig und trotzdem publikumswirksam."),
            ("Ist der Roboter für Besucher sicher?",
             "Ja. Der G1 erkennt über LiDAR und Kameras Hindernisse und Menschen in Echtzeit, zusätzlich überwacht "
             "unser Operator den Einsatz durchgehend. Wir sind haftpflichtversichert."),
        ],
    ),
    dict(
        slug="bremen", city="Bremen", city_gen="Bremens", region="Bremen und Nordwestdeutschland",
        claim="Kongresse, Luft- und Raumfahrt und Firmenfeiern",
        lead="Bremen verbindet Luft- und Raumfahrt, Logistik und Wissenschaft. Ein humanoider Roboter passt hier "
             "sowohl auf den Fachkongress als auch auf die Weihnachtsfeier.",
        venues=[
            ("Messe Bremen & ÖVB-Arena", "Fachmessen, Kongresse und Großveranstaltungen."),
            ("Congress Centrum Bremen", "Tagungen, Konferenzen und Preisverleihungen."),
            ("Kulturzentrum Schlachthof", "Markenevents und Firmenfeiern mit Charakter."),
            ("Rathaus & Obere Rathaushalle", "Repräsentative Empfänge in historischem Rahmen."),
        ],
        around="Überseestadt, Neustadt, Vegesack sowie Oldenburg, Delmenhorst, Bremerhaven und Nordwestdeutschland",
        faq=[
            ("Kommen Sie auch nach Bremerhaven oder Oldenburg?",
             "Ja — die gesamte Region wird ohne Anfahrtsaufschlag bedient. Sagen Sie uns einfach die Location."),
            ("Was passiert, wenn unser Event draußen stattfindet?",
             "Kein Problem, solange die Fläche eben und trocken ist. Für den Regenfall stimmen wir vorab eine "
             "überdachte Alternative ab."),
        ],
    ),
    dict(
        slug="essen", city="Essen", city_gen="Essens", region="Essen und das Ruhrgebiet",
        claim="Messen, Energiewirtschaft und Industrie-Locations",
        lead="Essen ist Messestadt und Energie-Zentrale des Ruhrgebiets. Zwischen Zeche Zollverein und Messe Essen "
             "trifft Industriegeschichte auf sehr gegenwärtige Technologie.",
        venues=[
            ("Messe Essen", "Fachmessen wie E-world, IPM und Techno-Classica."),
            ("Grugahalle", "Großveranstaltungen, Kongresse und Firmenevents."),
            ("Zeche Zollverein", "Markenevents und Galas im UNESCO-Welterbe."),
            ("Colosseum Theater", "Preisverleihungen und Abendveranstaltungen."),
        ],
        around="Rüttenscheid, Kettwig, Altenessen sowie Duisburg, Bochum, Gelsenkirchen, Mülheim und das Ruhrgebiet",
        faq=[
            ("Funktioniert der Roboter auf Industrieböden wie in Zollverein?",
             "Ja. Der G1 bewältigt Asphalt, Estrich, Kopfsteinpflaster in Maßen sowie Hallenböden. Bei sehr unebenem "
             "Untergrund legen wir mit Ihnen gemeinsam eine geeignete Showfläche fest."),
            ("Passt der Roboter zu einem Event der Energiewirtschaft?",
             "Sehr gut. Automatisierung und Robotik sind dort strategische Themen — der G1 macht sie am Stand greifbar."),
        ],
    ),
    dict(
        slug="dortmund", city="Dortmund", city_gen="Dortmunds", region="Dortmund und Westfalen",
        claim="Messen, Logistik-Events und Firmenveranstaltungen",
        lead="Dortmund ist Logistik- und Technologiestandort mit einer der größten Messeflächen Westfalens. "
             "Ein humanoider Roboter ist hier der Gesprächsanlass, der Ihren Stand vom Nachbarstand trennt.",
        venues=[
            ("Messe Westfalenhallen", "Fachmessen, Kongresse und Publikumsmessen."),
            ("Kongresszentrum Westfalenhallen", "Tagungen, Konferenzen und Verbandsevents."),
            ("Signal Iduna Park (Business-Bereiche)", "Firmenevents und Netzwerkabende."),
            ("DASA & Depot Dortmund", "Technologie-Events und kreative Markenauftritte."),
        ],
        around="Hörde, Innenstadt, das Technologiezentrum sowie Bochum, Hagen, Hamm, Münster und Westfalen",
        faq=[
            ("Können wir den Roboter für eine Logistik-Fachmesse buchen?",
             "Ja. Gerade in der Logistik ist Robotik ein Kernthema — der G1 verbindet die inhaltliche Botschaft mit "
             "einem sichtbaren Publikumsmagneten."),
            ("Wann sollten wir buchen?",
             "So früh wie möglich, besonders in der Messesaison. Die Terminreservierung ist bei uns kostenlos und ohne "
             "Anzahlung — es spricht also nichts dagegen, den Termin früh zu sichern."),
        ],
    ),
    dict(
        slug="karlsruhe", city="Karlsruhe", city_gen="Karlsruhes", region="Karlsruhe und die TechnologieRegion",
        claim="IT-Events, Forschung und Fachmessen",
        lead="Karlsruhe ist eine der forschungsstärksten Städte Deutschlands — KIT, ZKM und eine dichte IT-Szene. "
             "Ein humanoider Roboter trifft hier auf ein Publikum, das genau hinschaut.",
        venues=[
            ("Messe Karlsruhe", "Fachmessen und Kongresse in Rheinstetten."),
            ("Schwarzwaldhalle & Stadthalle", "Tagungen, Galas und Preisverleihungen."),
            ("ZKM | Zentrum für Kunst und Medien", "Technologie- und Kultur-Events."),
            ("Gartenhalle & Festplatz", "Firmenfeiern und Publikumsveranstaltungen."),
        ],
        around="Oststadt, Durlach, Rheinstetten sowie Pforzheim, Bruchsal, Baden-Baden und die TechnologieRegion Karlsruhe",
        faq=[
            ("Eignet sich der Roboter für eine Hochschul- oder Forschungsveranstaltung?",
             "Ja — bei Tagen der offenen Tür, Science Slams und Forschungskongressen ist der G1 regelmäßig der "
             "meistfotografierte Programmpunkt."),
            ("Bekommen wir den Roboter auch für einen halben Tag günstiger?",
             "Wir kalkulieren grundsätzlich pro Veranstaltungstag — das ist in Summe fast immer günstiger als "
             "Stundenmodelle mit Anfahrtszuschlägen. Fragen Sie uns nach Ihrem konkreten Ablauf."),
        ],
    ),
    dict(
        slug="mannheim", city="Mannheim", city_gen="Mannheims", region="Mannheim und die Metropolregion Rhein-Neckar",
        claim="Kongresse, Chemie- und Softwarebranche",
        lead="Mannheim, Heidelberg und Ludwigshafen bilden zusammen eine der stärksten Wirtschaftsregionen Deutschlands. "
             "Kongresse und Corporate-Events laufen hier auf hohem Niveau — und suchen entsprechend starke Formate.",
        venues=[
            ("Congress Center Rosengarten", "Kongresse, Tagungen und Galaveranstaltungen."),
            ("SAP Arena", "Großveranstaltungen und Konzernevents."),
            ("Maimarkt Mannheim", "Publikums- und Fachmessen."),
            ("Alte Feuerwache & Eventwerkstatt", "Markenevents mit Industriecharme."),
        ],
        around="Innenstadt, Neckarau, Käfertal sowie Heidelberg, Ludwigshafen, Speyer, Worms und die Metropolregion Rhein-Neckar",
        faq=[
            ("Passt der Roboter zu einem Kongress im Rosengarten?",
             "Ja. Im Kongressumfeld setzen wir den G1 gerne im Foyer ein: Er empfängt Teilnehmende, sorgt in den Pausen "
             "für Gesprächsstoff und lenkt nicht vom Programm im Saal ab."),
            ("Können wir den Roboter zusätzlich zum Roboterhund buchen?",
             f"Ja. Der Roboterhund kostet {DOG_PRICE} pro Veranstaltungstag und ist als Ergänzung buchbar — Operator inklusive."),
        ],
    ),
    dict(
        slug="bonn", city="Bonn", city_gen="Bonns", region="Bonn und die Region Köln/Bonn",
        claim="Internationale Konferenzen, NGOs und Wissenschaft",
        lead="Bonn ist UN-Standort und Kongressstadt mit internationalem Publikum. Ein humanoider Roboter ist hier "
             "ein Statement zu Technologie — und ein sehr verlässlicher Foto-Anlass.",
        venues=[
            ("World Conference Center Bonn", "Internationale Konferenzen und Kongresse."),
            ("Telekom Dome", "Großveranstaltungen und Firmenevents."),
            ("Universitätsclub & Post Tower Lounge", "Repräsentative Empfänge und Netzwerkabende."),
            ("Kunstmuseum Bonn", "Kultur- und Markenevents."),
        ],
        around="Bad Godesberg, Beuel, das Regierungsviertel sowie Köln, Siegburg, Koblenz und die Region Köln/Bonn",
        faq=[
            ("Kann der Roboter auf einer internationalen Konferenz eingesetzt werden?",
             "Ja. Das Format funktioniert sprachunabhängig — die Wirkung entsteht über Bewegung und Präsenz, nicht über "
             "Sprache. Ihr Branding auf der Brustplatte bleibt in jedem Foto sichtbar."),
            ("Wie läuft die Abrechnung?",
             "Terminreservierung kostenlos, keine Anzahlung, Rechnung erst nach der Veranstaltung. Bei Bedarf "
             "vereinbaren wir ein längeres Zahlungsziel."),
        ],
    ),
    dict(
        slug="muenster", city="Münster", city_gen="Münsters", region="Münster und das Münsterland",
        claim="Fachmessen, Hochschulevents und Firmenfeiern",
        lead="Münster ist Hochschulstadt und Messestandort im Herzen des Münsterlands — ein Publikum, das neugierig "
             "ist und Innovation gerne teilt.",
        venues=[
            ("Messe und Congress Centrum Halle Münsterland", "Fachmessen, Kongresse und Publikumsmessen."),
            ("Schloss Münster", "Hochschulveranstaltungen und repräsentative Empfänge."),
            ("Jovel & Skaters Palace", "Firmenfeiern und Markenevents."),
            ("Speicherstadt Münster", "Tagungen und Corporate-Events im Industrieambiente."),
        ],
        around="Innenstadt, Hafen, Gievenbeck sowie Osnabrück, Bielefeld, Dortmund, Rheine und das Münsterland",
        faq=[
            ("Eignet sich der Roboter für einen Hochschul-Event?",
             "Sehr gut. Bei Tagen der offenen Tür, Karrieremessen und Erstsemesterbegrüßungen ist der G1 zuverlässig "
             "der Programmpunkt mit den meisten Handykameras."),
            ("Wie viel Platz braucht der Roboter?",
             "Rund 2×2 m ebene Fläche und eine 230-V-Steckdose. Mehr Fläche ist willkommen, aber nicht Bedingung."),
        ],
    ),
    dict(
        slug="wiesbaden", city="Wiesbaden", city_gen="Wiesbadens", region="Wiesbaden und Rhein-Main",
        claim="Kongresse, Versicherungsbranche und Galaabende",
        lead="Wiesbaden steht für Kongresse und repräsentative Abendveranstaltungen. Ein humanoider Roboter setzt "
             "hier einen bewusst modernen Kontrapunkt zum klassischen Rahmen.",
        venues=[
            ("RheinMain CongressCenter", "Kongresse, Tagungen und Fachmessen."),
            ("Kurhaus Wiesbaden", "Galadinner, Bälle und Preisverleihungen."),
            ("Schlachthof Wiesbaden", "Firmenfeiern und Markenevents."),
            ("Casino-Gesellschaft & Villa Clementine", "Empfänge und exklusive Abendformate."),
        ],
        around="Innenstadt, Biebrich, Erbenheim sowie Mainz, Frankfurt, Rüsselsheim, Darmstadt und Rhein-Main",
        faq=[
            ("Passt ein Roboter zu einem klassischen Galaabend im Kurhaus?",
             "Ja — genau dieser Kontrast wirkt. Der G1 empfängt Gäste beim Sektempfang oder übernimmt einen kurzen "
             "Bühnenmoment; den Rest des Abends bleibt er dezent im Hintergrund."),
            ("Ist die Anfahrt nach Wiesbaden inklusive?",
             "Ja, deutschlandweit — ohne Kilometerpauschale, ohne Mindestentfernung, ohne Nachberechnung."),
        ],
    ),
    dict(
        slug="augsburg", city="Augsburg", city_gen="Augsburgs", region="Augsburg und Schwaben",
        claim="Robotik-Industrie, Fachmessen und Firmenevents",
        lead="Augsburg ist einer der wichtigsten Robotikstandorte Europas. Ein humanoider Roboter ist hier kein "
             "Fremdkörper, sondern genau die Sprache, die das Publikum spricht.",
        venues=[
            ("Messe Augsburg", "Fachmessen, Kongresse und Firmenveranstaltungen."),
            ("Kongress am Park", "Tagungen, Galas und Preisverleihungen."),
            ("Gaswerk Augsburg", "Technologie- und Kreativevents im Industriedenkmal."),
            ("Goldener Saal im Rathaus", "Repräsentative Empfänge und Festakte."),
        ],
        around="Innenstadt, Lechhausen, Göggingen sowie München, Ulm, Ingolstadt, Landsberg und die Region Schwaben",
        faq=[
            ("Sind die Gäste in Augsburg nicht schon an Roboter gewöhnt?",
             "An Industrieroboter ja — an einen frei laufenden Humanoiden, der Gäste begrüßt und tanzt, praktisch nicht. "
             "Genau darin liegt der Effekt."),
            ("Können wir den Roboter für eine Firmenfeier buchen?",
             "Ja. Firmenfeiern, Jubiläen und Weihnachtsfeiern gehören zu unseren häufigsten Einsätzen."),
        ],
    ),
]


# ── Bausteine ─────────────────────────────────────────────────────────
def gtm_head():
    return f"""  <!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->"""


def gtm_body():
    return f"""  <!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""


def head_meta(title, description, keywords, path, og_image="og-image.jpg"):
    url = f"{DOMAIN}/{path}" if path else f"{DOMAIN}/"
    return f"""  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta name="keywords" content="{keywords}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{url}" />

  <!-- Open Graph -->
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{url}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:image" content="{DOMAIN}/{og_image}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="{title}" />
  <meta property="og:locale" content="de_DE" />
  <meta property="og:site_name" content="33bots" />

  <!-- Twitter / X Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{description}" />

  <meta name="theme-color" content="#000000" />

  <!-- Hreflang -->
  <link rel="alternate" hreflang="de" href="{url}" />
  <link rel="alternate" hreflang="x-default" href="{url}" />"""


def head_assets(extra_style=""):
    return f"""  <script>history.scrollRestoration = 'manual';</script>
  <link rel="icon" type="image/svg+xml" href="favicon.svg" />
  <link rel="stylesheet" href="style.css?v=1" />
  <link rel="dns-prefetch" href="//serve.albacross.com" />
  <link rel="preconnect" href="https://www.googletagmanager.com" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="preload" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'" />
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" /></noscript>{extra_style}"""


def nav(home_prefix="index.html"):
    """home_prefix: '' na stronie głównej (kotwice lokalne), 'index.html' na podstronach."""
    p = home_prefix
    return f"""  <div class="cursor-glow" id="cursorGlow" aria-hidden="true"></div>
  <div class="scroll-progress" id="scrollProgress" aria-hidden="true"></div>

  <header class="nav" id="nav">
    <div class="nav__inner">
      <a href="index.html" class="logo">33BOTS</a>
      <nav class="nav__links">
        <div class="nav__dropdown">
          <button class="nav__dropdown-toggle" aria-haspopup="true" aria-expanded="false" type="button">Angebot <svg viewBox="0 0 10 6" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
          <div class="nav__dropdown-menu">
            <a href="roboter-mieten.html">Humanoiden Roboter mieten</a>
            <a href="messen.html">Messen &amp; Ausstellungen</a>
            <a href="konferenzen.html">Konferenzen &amp; Galas</a>
            <a href="tag-der-offenen-tuer.html">Tage der offenen Tür</a>
          </div>
        </div>
        <a href="{p}#preise">Preise</a>
        <a href="{p}#ueber-uns">Über uns</a>
        <a href="{p}#staedte">Städte</a>
        <a href="#kontakt">Kontakt</a>
      </nav>
      <button class="hamburger" id="hamburger" aria-label="Menü öffnen" aria-expanded="false">
        <span></span><span></span>
      </button>
    </div>
  </header>
  <main>

  <div class="mobile-menu" id="mobileMenu">
    <span class="mobile-menu__label">Angebot</span>
    <a href="roboter-mieten.html" class="mobile-menu__sub">Humanoiden Roboter mieten</a>
    <a href="messen.html" class="mobile-menu__sub">Messen &amp; Ausstellungen</a>
    <a href="konferenzen.html" class="mobile-menu__sub">Konferenzen &amp; Galas</a>
    <a href="tag-der-offenen-tuer.html" class="mobile-menu__sub">Tage der offenen Tür</a>
    <a href="{p}#preise">Preise</a>
    <a href="{p}#ueber-uns">Über uns</a>
    <a href="{p}#staedte">Städte</a>
    <a href="#kontakt">Kontakt</a>
  </div>
"""


def contact_form(location_placeholder="z. B. Berlin, Messe Halle 3"):
    return f"""        <form id="contactForm" class="form" novalidate>
          <div class="form-steps-header">
            <span class="form-step-ind active" id="stepInd1">01 — Kontaktdaten</span>
            <span class="form-step-sep">/</span>
            <span class="form-step-ind" id="stepInd2">02 — Ihre Veranstaltung</span>
          </div>

          <div class="form-step" id="formStep1">
            <div class="form-row">
              <div class="form-field">
                <label for="f-name">Vor- und Nachname *</label>
                <input id="f-name" type="text" name="name" placeholder="Max Mustermann" autocomplete="name" required />
                <span class="form-field__err" aria-live="polite"></span>
              </div>
              <div class="form-field">
                <label for="f-company">Unternehmen</label>
                <input id="f-company" type="text" name="company" placeholder="Firmenname" autocomplete="organization" />
              </div>
            </div>
            <div class="form-row">
              <div class="form-field">
                <label for="f-email">E-Mail *</label>
                <input id="f-email" type="email" name="email" placeholder="kontakt@firma.de" autocomplete="email" required />
                <span class="form-field__err" aria-live="polite"></span>
              </div>
              <div class="form-field">
                <label for="f-phone">Telefon</label>
                <input id="f-phone" type="tel" name="phone" placeholder="+49 30 1234567" autocomplete="tel" />
              </div>
            </div>
            <button type="button" id="btnNext" class="btn-submit">Weiter — Ihre Veranstaltung →</button>
          </div>

          <div class="form-step form-step--hidden" id="formStep2" aria-hidden="true">
            <div class="form-row">
              <div class="form-field">
                <label for="f-date">Geplantes Veranstaltungsdatum</label>
                <input id="f-date" type="date" name="date" />
              </div>
              <div class="form-field">
                <label for="f-location">Stadt / Location</label>
                <input id="f-location" type="text" name="location" placeholder="{location_placeholder}" autocomplete="address-level2" />
              </div>
            </div>
            <div class="form-field">
              <label for="f-message">Beschreiben Sie Ihre Veranstaltung *</label>
              <textarea id="f-message" name="message" rows="6"
                placeholder="Art der Veranstaltung (Messe, Konferenz, Gala …), ungefähre Gästezahl, gewünschte Einsatzdauer und alles, was Ihnen sonst wichtig ist." required></textarea>
              <div class="form-field__footer">
                <span class="form-field__err" aria-live="polite"></span>
                <span class="char-counter"><span id="charCount">0</span> / 600</span>
              </div>
            </div>
            <div class="form-step__nav">
              <button type="button" id="btnBack" class="btn-back">← Zurück</button>
              <button type="submit" class="btn-submit">Kostenloses Angebot anfordern →</button>
            </div>
          </div>
        </form>"""


def footer(home_prefix="index.html"):
    p = home_prefix
    return f"""  </main>
  <footer class="footer">
    <div class="footer__inner">
      <div class="footer__brand">
        <span class="logo">33BOTS</span>
        <p class="footer__tagline"><a href="index.html" style="color:inherit; text-decoration:underline; text-underline-offset:2px;">Humanoide Roboter mieten</a> · Deutschlandweit</p>
        <div class="footer__nap">
          <a href="tel:{PHONE_RAW}" class="footer__nap-item">{PHONE_HUMAN}</a>
          <a href="mailto:{EMAIL}" class="footer__nap-item">{EMAIL}</a>
        </div>
      </div>
      <div class="footer__links">
        <a href="roboter-mieten.html">Roboter mieten</a>
        <a href="messen.html">Messen</a>
        <a href="konferenzen.html">Konferenzen &amp; Galas</a>
        <a href="tag-der-offenen-tuer.html">Tage der offenen Tür</a>
        <a href="{p}#preise">Preise</a>
        <a href="{p}#ueber-uns">Über uns</a>
        <a href="{p}#staedte">Städte</a>
        <a href="#kontakt">Kontakt</a>
      </div>
      <div class="footer__right">
        <div class="footer__socials">
          <a href="https://www.instagram.com/33bots_/" target="_blank" rel="noopener noreferrer" class="footer__social">↗ Instagram</a>
          <a href="https://www.tiktok.com/@aimforum" target="_blank" rel="noopener noreferrer" class="footer__social">↗ TikTok</a>
          <a href="https://www.facebook.com/33bots" target="_blank" rel="noopener noreferrer" class="footer__social">↗ Facebook</a>
          <a href="https://www.linkedin.com/company/33bots" target="_blank" rel="noopener noreferrer" class="footer__social">↗ LinkedIn</a>
        </div>
        <span class="footer__copy">© 2026 33bots. Alle Rechte vorbehalten.</span>
      </div>
    </div>
  </footer>

  <div class="cookie-banner" id="cookieBanner" aria-live="polite">
    <p class="cookie-banner__text">
      Diese Website verwendet Cookies zu Analysezwecken.
      <a href="#" class="cookie-banner__link">Datenschutzerklärung</a>
    </p>
    <button class="cookie-banner__btn" id="cookieAccept">Verstanden</button>
  </div>

  <div class="sticky-cta">
    <a href="#kontakt" class="btn-cta">Kostenloses Angebot →</a>
  </div>

  <script src="main.js"></script>
  <!-- Albacross -->
  <script>window._nQc="{ALBACROSS_ID}";</script>
  <script async src="https://serve.albacross.com/track.js"></script>
</body>
</html>
"""


def city_links_block(current_slug=None, style="chip"):
    items = []
    for c in CITIES:
        if c["slug"] == current_slug:
            continue
        items.append(
            f'        <a href="roboter-mieten-{c["slug"]}.html" style="color:var(--text); font-size:0.85rem; '
            f'font-weight:600; padding:6px 14px; background:var(--surface-2); border:1px solid var(--border-mid); '
            f'border-radius:8px; text-decoration:none;">{c["city"]}</a>'
        )
    return "\n".join(items)


FAQ_MAIN = [
    ("Was kostet die Miete eines humanoiden Roboters für ein Event?",
     f"Ein kompletter Veranstaltungstag kostet {PRICE_RANGE} — der endgültige Preis hängt ausschließlich vom "
     f"Veranstaltungsort ab. Im Preis ist alles enthalten: deutschlandweite Anfahrt, zertifizierter Operator, "
     f"Branding des Roboters und Versicherung — ohne Aufschläge. Optional buchen Sie den Roboterhund für "
     f"{DOG_PRICE} pro Tag; ab zwei Veranstaltungstagen erhalten Sie 15 % Rabatt auf jeden Tag."),
    ("Muss ich eine Anzahlung leisten, um einen Termin zu reservieren?",
     "Nein. Die Terminreservierung ist vollständig kostenlos — wir schließen einen einfachen Vertrag ohne Anzahlung "
     "und stellen die Rechnung erst nach der Veranstaltung. Bei Bedarf vereinbaren wir ein längeres Zahlungsziel."),
    ("Muss ich den Roboter selbst bedienen können?",
     "Nein. Ein zertifizierter Operator von 33bots ist den gesamten Veranstaltungstag vor Ort, übernimmt Aufbau, "
     "Konfiguration und Steuerung. Sie brauchen keinerlei technisches Vorwissen."),
    ("Kann der Roboter auch bei einem Tag der offenen Tür oder Betriebsfest eingesetzt werden?",
     "Selbstverständlich. Die Unitree-Roboter kommen mit unterschiedlichen Untergründen zurecht (Asphalt, Rasen, "
     "Teppich) und funktionieren daher sowohl im Bürogebäude als auch bei Outdoor-Veranstaltungen."),
    ("Kann ich mein Firmenlogo auf dem Roboter platzieren?",
     "Ja — und zwar kostenlos. Ihr Logo und ein QR-Code kommen auf die Brustplatte des Roboters. Bei uns ist das "
     "Branding Teil des Standardpakets und wird nicht extra berechnet."),
    ("Ist der Roboter für die Teilnehmenden sicher?",
     "Ja. Der Roboter verfügt über LiDAR und Computer Vision und weicht Hindernissen sowie Menschen in Echtzeit aus. "
     "Zusätzlich überwacht unser Operator den Einsatz durchgehend. Eine Haftpflichtversicherung ist inklusive."),
    ("Welche technischen Voraussetzungen brauchen Sie vor Ort?",
     "Eine gewöhnliche 230-V-Steckdose und rund 2×2 m freie Fläche. Internet oder besondere Beleuchtung sind nicht "
     "erforderlich. Unser Operator bringt die komplette Ausrüstung mit und ist in 30–45 Minuten einsatzbereit."),
    ("Kann der Roboter tanzen?",
     "Und wie. Der Unitree G1 beherrscht mehrere Choreografien, die auch ein professioneller Tänzer nicht verstecken "
     "müsste. Wenn bei Ihrer Veranstaltung ein DJ auflegt, übernimmt unser Roboter gerne die Tanzfläche."),
    ("Ist die Vermietung deutschlandweit verfügbar?",
     "Ja — 33bots ist in ganz Deutschland im Einsatz, mit kostenloser Anfahrt unabhängig von Stadt und Entfernung. "
     "Wir bedienen Berlin, München, Hamburg, Köln, Frankfurt, Stuttgart, Düsseldorf und Dutzende weitere Städte."),
    ("Welche Unternehmen haben bereits einen Roboter bei Ihnen gemietet?",
     "Unter anderem die Perspektywy Foundation (Women in Tech Summit — die größte Women-in-Tech-Konferenz Europas), "
     "der globale Logistikkonzern DSV, Cashify sowie LEX AI, dessen Show mit unserem Roboter im polnischen "
     "Fernsehen (TVP) ausgestrahlt wurde."),
    ("Was unterscheidet 33bots von anderen Roboter-Vermietungen?",
     "Im Preis ist immer das Komplettpaket enthalten: kostenlose Anfahrt ohne Kilometerbegrenzung, ein zertifizierter "
     "Operator für die gesamte Veranstaltung und kostenloses Branding des Roboters (Logo und QR-Code). Wir berechnen "
     "weder Anfahrt noch Zusatzoptionen nach."),
]


def json_ld_faq(pairs):
    entries = []
    for q, a in pairs:
        q_ = q.replace('"', '\\"')
        a_ = a.replace('"', '\\"')
        entries.append(
            '      {\n        "@type": "Question",\n'
            f'        "name": "{q_}",\n'
            '        "acceptedAnswer": {"@type": "Answer", "text": "'
            f'{a_}"'
            "}\n      }"
        )
    return (
        '  <script type="application/ld+json">\n  {\n'
        '    "@context": "https://schema.org",\n'
        '    "@type": "FAQPage",\n'
        '    "mainEntity": [\n' + ",\n".join(entries) + "\n    ]\n  }\n  </script>"
    )


def faq_html(pairs, heading="Häufige<br />Fragen"):
    items = []
    for q, a in pairs:
        items.append(f"""      <div class="faq-item">
        <button class="faq-q" aria-expanded="false">
          <span>{q}</span>
          <span class="faq-q__icon" aria-hidden="true">+</span>
        </button>
        <div class="faq-a" hidden><p>{a}</p></div>
      </div>""")
    return f"""  <section class="section faq-section">
    <div class="section-header">
      <span class="tag">FAQ</span>
      <h2 class="section-title">{heading}</h2>
    </div>
    <div class="faq">
{chr(10).join(items)}
    </div>
  </section>"""


# ── Strona główna ─────────────────────────────────────────────────────
def build_index():
    title = "Humanoide Roboter mieten für Events — deutschlandweit | 33bots"
    desc = (f"Humanoiden Roboter Unitree G1 für Event, Messe und Konferenz mieten. Ganzer Tag ab {PRICE_LOW} € — "
            f"Anfahrt, Operator und Branding inklusive, keine Anzahlung, Rechnung nach dem Event. "
            f"Kostenloses Angebot in 24 h.")
    kw = ("humanoiden roboter mieten, roboter mieten event, roboter für messe mieten, Unitree G1 mieten, "
          "roboter konferenz, event attraktion roboter, humanoider roboter Deutschland")

    city_chips = "\n".join(
        f'        <a href="roboter-mieten-{c["slug"]}.html" class="tile__link" style="padding:8px 16px; '
        f'background:var(--surface-2); border:1px solid var(--border-mid); border-radius:8px;">{c["city"]}</a>'
        for c in CITIES
    )
    coverage = "\n".join(
        f'            <li><a href="roboter-mieten-{c["slug"]}.html">{c["city"]}</a></li>' for c in CITIES
    )

    faq_ld = json_ld_faq(FAQ_MAIN)

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
{gtm_head()}
{head_meta(title, desc, kw, "")}

  <!-- JSON-LD -->
  <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Miete eines humanoiden Roboters Unitree G1",
  "description": "Vermietung humanoider Roboter Unitree G1 für Events, Konferenzen und Messen in ganz Deutschland.",
  "url": "{DOMAIN}",
  "image": "{DOMAIN}/robot-g1.jpg",
  "brand": {{"@type": "Brand", "name": "Unitree"}},
  "offers": {{
    "@type": "AggregateOffer",
    "priceCurrency": "EUR",
    "lowPrice": "{PRICE_LOW_NUM}",
    "highPrice": "{PRICE_HIGH_NUM}",
    "availability": "https://schema.org/InStock",
    "url": "{DOMAIN}/#preise",
    "description": "Kompletter Veranstaltungstag inklusive Anfahrt, Operator und Branding. Keine Zusatzkosten, keine Anzahlung, Rechnung nach dem Event."
  }},
  "aggregateRating": {{
    "@type": "AggregateRating",
    "ratingValue": "5.0",
    "reviewCount": "3",
    "bestRating": "5",
    "worstRating": "1"
  }}
}}
  </script>

{faq_ld}

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    "name": "33bots – Humanoide Roboter für Events und Messen mieten",
    "alternateName": "33bots",
    "url": "{DOMAIN}",
    "logo": "{DOMAIN}/logo.png",
    "image": "{DOMAIN}/robot-g1.jpg",
    "description": "Vermietung humanoider Roboter Unitree G1 für Events, Konferenzen und Messen in ganz Deutschland. Kostenlose Anfahrt, zertifizierter Operator inklusive.",
    "telephone": "{PHONE_RAW}",
    "email": "{EMAIL}",
    "areaServed": {{"@type": "Country", "name": "Germany"}},
    "sameAs": [
      "https://www.facebook.com/33bots",
      "https://www.instagram.com/33bots_/",
      "https://www.linkedin.com/company/33bots",
      "https://www.tiktok.com/@aimforum"
    ],
    "contactPoint": {{
      "@type": "ContactPoint",
      "telephone": "{PHONE_RAW}",
      "email": "{EMAIL}",
      "contactType": "sales",
      "areaServed": "DE",
      "availableLanguage": ["German", "English", "Polish"]
    }},
    "knowsAbout": [
      "humanoiden Roboter mieten",
      "Roboter für Events",
      "Roboter für Messen",
      "Roboter für Konferenzen",
      "Unitree G1",
      "Event-Attraktionen"
    ],
    "priceRange": "{PRICE_LOW_NUM}-{PRICE_HIGH_NUM} EUR"
  }}
  </script>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "VideoObject",
    "name": "Humanoider Roboter Unitree G1 im Einsatz — Miete für Events | 33bots",
    "description": "Der humanoide Roboter Unitree G1 live: Er läuft, gestikuliert, begrüßt Gäste und tanzt. Kostenloses Branding mit Logo und QR-Code Ihrer Marke.",
    "thumbnailUrl": "{DOMAIN}/video/33bots-robot-event-poster.jpg",
    "contentUrl": "{DOMAIN}/video/33bots-robot-event.mp4",
    "uploadDate": "2026-07-02",
    "duration": "PT35S",
    "inLanguage": "de",
    "publisher": {{
      "@type": "Organization",
      "name": "33bots",
      "url": "{DOMAIN}",
      "logo": {{"@type": "ImageObject", "url": "{DOMAIN}/logo.png"}}
    }}
  }}
  </script>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "HowTo",
    "name": "So mieten Sie einen humanoiden Roboter — in 6 Schritten ohne Anzahlung",
    "description": "Ablauf der Miete eines Unitree G1 für Ihr Event: Kontakt, Rückruf, schnelles Angebot, einfacher Vertrag ohne Anzahlung, Durchführung und Rechnung erst nach der Veranstaltung.",
    "image": "{DOMAIN}/robot-g1.jpg",
    "step": [
      {{"@type": "HowToStep", "position": 1, "name": "Schneller Kontakt", "text": "Sie füllen ein kurzes Formular aus oder schreiben eine E-Mail — zwei Minuten genügen.", "url": "{DOMAIN}/#kontakt"}},
      {{"@type": "HowToStep", "position": 2, "name": "Rückruf von uns", "text": "Wir rufen zurück, lernen Ihre Veranstaltung kennen und empfehlen das passende Showformat."}},
      {{"@type": "HowToStep", "position": 3, "name": "Angebot in 24 h", "text": "Sie erhalten einen konkreten Betrag ohne Sternchen — meist noch am selben Tag."}},
      {{"@type": "HowToStep", "position": 4, "name": "Einfacher Vertrag", "text": "Kostenlose Terminreservierung, keine Anzahlung. Auf Wunsch mit längerem Zahlungsziel."}},
      {{"@type": "HowToStep", "position": 5, "name": "Wir übernehmen alles", "text": "Anfahrt, Aufbau, Operator und Show auf höchstem Niveau."}},
      {{"@type": "HowToStep", "position": 6, "name": "Zahlung nach dem Event", "text": "Die Rechnung stellen wir erst nach der Veranstaltung."}}
    ]
  }}
  </script>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "33bots",
    "alternateName": "33bots — humanoide Roboter mieten",
    "url": "{DOMAIN}/",
    "inLanguage": "de-DE",
    "description": "Humanoide Roboter Unitree G1 für Events, Messen und Konferenzen in ganz Deutschland mieten.",
    "publisher": {{
      "@type": "Organization",
      "name": "33bots",
      "url": "{DOMAIN}/",
      "logo": {{"@type": "ImageObject", "url": "{DOMAIN}/logo.png"}}
    }}
  }}
  </script>

  <link rel="preload" as="image" href="robot-g1-960.webp" imagesrcset="robot-g1-960.webp 960w, robot-g1.webp 2390w" imagesizes="45vw" fetchpriority="high" type="image/webp" media="(min-width: 769px)" />
{head_assets()}
</head>
<body>
{gtm_body()}

{nav("")}
  <!-- HERO -->
  <section class="hero">
    <div class="hero__content">
      <p class="hero__eyebrow">Humanoide Roboter mieten · Deutschlandweit · Bestpreis</p>
      <h1 class="hero__title">Humanoide Roboter<br />mieten —<br /><em>Unitree G1.</em></h1>
      <p class="hero__sub">Der Roboter, der Menschenmengen stoppt und Ihre Veranstaltung wochenlang zum Gesprächsthema macht. Ein kompletter Showtag mit Anfahrt, Operator und Branding im Preis — <strong>ohne Anzahlung und ohne versteckte Kosten</strong>.</p>
      <div class="hero__ctas">
        <a href="#kontakt" class="btn-cta">Kostenloses Angebot anfordern →</a>
        <a href="#preise" class="btn-cta--ghost">Preise ansehen ↓</a>
      </div>
      <p class="hero__cta-note">Angebot in 24 h · Keine Anzahlung · Rechnung erst nach dem Event</p>
      <div class="hero__trust">
        <span class="hero__trust-item">✓ Bester Preis am Markt</span>
        <span class="hero__trust-item">✓ Anfahrt inklusive</span>
        <span class="hero__trust-item">✓ Operator inklusive</span>
        <span class="hero__trust-item">✓ Branding ohne Aufpreis</span>
      </div>
    </div>
    <div class="hero__visual">
      <div class="hero__spotlight" aria-hidden="true"></div>
      <div class="hero__robot-wrap" id="robotWrap">
      <div class="hero__robot">
        <div class="robot-scan" aria-hidden="true"></div>
        <picture>
          <source srcset="robot-g1-960.webp 960w, robot-g1.webp 2390w" sizes="(min-width: 769px) 45vw, 1px" type="image/webp" />
          <img src="robot-g1.jpg"
               alt="Humanoider Roboter Unitree G1 — Attraktion für Events, Messen und Konferenzen in Deutschland"
               class="hero__robot-img"
               width="600" height="800"
               loading="eager"
               fetchpriority="high" />
        </picture>
      </div>
      </div>
      <div class="hero__tag hero__tag--1">Unitree G1</div>
      <div class="hero__tag hero__tag--2">23 DOF</div>
      <div class="hero__tag hero__tag--3">~132 cm</div>
    </div>
  </section>

  <!-- STATS BAR -->
  <div class="stats-bar">
    <div class="stats-bar__inner">
      <div class="stat-item">
        <span class="stat-item__val" data-count="20" data-suffix="+">0</span>
        <span class="stat-item__lbl">Städte in Deutschland</span>
      </div>
      <div class="stat-item__div" aria-hidden="true"></div>
      <div class="stat-item">
        <span class="stat-item__val" data-count="5" data-suffix=".0 ★">0</span>
        <span class="stat-item__lbl">Kundenbewertung</span>
      </div>
      <div class="stat-item__div" aria-hidden="true"></div>
      <div class="stat-item">
        <span class="stat-item__val" data-count="24" data-suffix="h">0</span>
        <span class="stat-item__lbl">bis zum Angebot</span>
      </div>
      <div class="stat-item__div" aria-hidden="true"></div>
      <div class="stat-item">
        <span class="stat-item__val" data-count="0" data-suffix=" €">0</span>
        <span class="stat-item__lbl">Anfahrt</span>
      </div>
    </div>
  </div>

  <!-- REFERENZEN -->
  <section class="section" id="referenzen" style="padding-top:var(--s8); padding-bottom:var(--s8);">
    <div style="max-width:1000px; margin:0 auto; text-align:center;">
      <h2 style="font-size:0.75rem; font-weight:700; letter-spacing:0.14em; text-transform:uppercase; color:var(--text-3); margin-bottom:var(--s5);">Vertrauen uns</h2>
      <div style="display:flex; flex-wrap:wrap; align-items:stretch; justify-content:center; gap:var(--s4);">
        <div style="display:flex; flex-direction:column; gap:4px; padding:var(--s4) var(--s6); background:var(--surface-2); border:1px solid var(--border-mid); border-radius:12px; min-width:220px; text-align:left;">
          <span style="font-size:0.7rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:var(--text-3);">Bildung · Women in Tech Summit</span>
          <span style="font-size:1.05rem; font-weight:700; color:var(--text);">Perspektywy Foundation</span>
        </div>
        <div style="display:flex; flex-direction:column; gap:4px; padding:var(--s4) var(--s6); background:var(--surface-2); border:1px solid var(--border-mid); border-radius:12px; min-width:220px; text-align:left;">
          <span style="font-size:0.7rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:var(--text-3);">Transport &amp; Logistik</span>
          <span style="font-size:1.05rem; font-weight:700; color:var(--text);">DSV</span>
        </div>
        <div style="display:flex; flex-direction:column; gap:4px; padding:var(--s4) var(--s6); background:var(--surface-2); border:1px solid var(--border-mid); border-radius:12px; min-width:220px; text-align:left;">
          <span style="font-size:0.7rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:var(--text-3);">Technologie · Fintech</span>
          <span style="font-size:1.05rem; font-weight:700; color:var(--text);">Cashify</span>
        </div>
        <div style="display:flex; flex-direction:column; gap:4px; padding:var(--s4) var(--s6); background:var(--surface-2); border:1px solid var(--border-mid); border-radius:12px; min-width:220px; text-align:left;">
          <span style="font-size:0.7rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:var(--text-3);">Legal Tech · TV-Beitrag</span>
          <span style="font-size:1.05rem; font-weight:700; color:var(--text);">LEX AI</span>
        </div>
      </div>
      <p style="margin-top:var(--s5); color:var(--text-2); font-size:0.95rem; max-width:680px; margin-left:auto; margin-right:auto; line-height:1.7;">Unsere humanoiden Roboter waren unter anderem im Einsatz für die <strong style="color:var(--text);">Perspektywy Foundation</strong> (Veranstalter des Women in Tech Summit — der größten Women-in-Tech-Konferenz Europas), den globalen Logistikkonzern <strong style="color:var(--text);">DSV</strong>, <strong style="color:var(--text);">Cashify</strong> sowie <strong style="color:var(--text);">LEX AI</strong>, dessen Show mit unserem Roboter im öffentlich-rechtlichen Fernsehen ausgestrahlt wurde.</p>
      <figure style="margin:var(--s7) auto 0; max-width:720px;">
        <picture>
          <source srcset="realizacja-robot-gala-dresden.webp" type="image/webp" />
          <img src="realizacja-robot-gala-dresden.jpg" alt="Humanoider Roboter Unitree G1 bei einer Gala in Dresden" width="720" height="480" loading="lazy" style="width:100%; height:auto; border-radius:16px; border:1px solid var(--border-mid);" />
        </picture>
        <figcaption style="margin-top:var(--s2); font-size:0.85rem; color:var(--text-3);">Gala-Einsatz in Dresden — der G1 zwischen den Gästen</figcaption>
      </figure>
    </div>
  </section>

  <!-- LEISTUNGEN -->
  <section class="section tiles-section" id="leistungen">
    <div class="section-header">
      <span class="tag">Leistungen</span>
      <h2 class="section-title">Was wir für Sie<br />übernehmen</h2>
    </div>
    <div class="tiles">
      <div class="tile">
        <div class="tile__top">
          <svg class="tile__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
          <span class="tile__tag">Der Star Ihres Events</span>
        </div>
        <h3 class="tile__title">Roboter<br />für Events</h3>
        <p class="tile__desc">Sie wollen, dass über Ihre Veranstaltung gesprochen wird? Der G1 kommt zu Ihrer Konferenz, Eröffnung oder Gala — und sorgt garantiert für Andrang. Die Gäste zücken die Handys, die Clips entstehen von selbst. <a href="roboter-mieten.html" style="color:inherit; text-decoration:underline;">Roboter für Events ansehen →</a></p>
        <a href="#kontakt" class="tile__link">Mehr erfahren →</a>
      </div>
      <div class="tile tile--light">
        <div class="tile__top">
          <svg class="tile__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
          <span class="tile__tag">Unsere Flotte</span>
        </div>
        <h3 class="tile__title">Roboter<br />mieten</h3>
        <p class="tile__desc">Wir verfügen über eine eigene Flotte von Unitree-G1-Robotern — für Messen, Logistik, Retail und Markenauftritte. Eigene Technik, keine Zwischenhändler.</p>
        <a href="#kontakt" class="tile__link">Mehr erfahren →</a>
      </div>
      <div class="tile">
        <div class="tile__top">
          <svg class="tile__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>
          <span class="tile__tag">Reichweite, die man nicht kauft</span>
        </div>
        <h3 class="tile__title">Social-Media-<br />Reichweite</h3>
        <p class="tile__desc">Ein Unitree-Roboter erzeugt mehr organische Reichweite und Aufmerksamkeit als so mancher Top-Influencer — und das aus jedem einzelnen Gästehandy heraus.</p>
        <a href="#kontakt" class="tile__link">Mehr erfahren →</a>
      </div>
    </div>
  </section>

  <!-- ÜBER UNS -->
  <section class="section onas-section" id="ueber-uns">
    <div class="onas-head">
      <span class="tag">Über uns</span>
      <h2 class="section-title">Spezialisten für<br />Event-Robotik</h2>
    </div>

    <div class="onas-body">
      <div class="onas-text">
        <p class="lead-text">33bots ist auf die <a href="roboter-mieten.html" style="color:var(--text); text-decoration:underline; text-underline-offset:3px;">Vermietung humanoider Roboter Unitree G1</a> für Events, Messen und Technologie-Shows spezialisiert. Das ist unser einziges Geschäft — wir sind keine Agentur, die alles ein bisschen macht.</p>
        <p class="body-text">Die Miete eines humanoiden Roboters bei 33bots bedeutet immer Rundum-Betreuung: Wir bringen den Roboter zu Ihnen, stellen einen Operator für die gesamte Veranstaltungsdauer und kümmern uns um alles — vom Aufbau bis zur finalen Show. Wir sind in Berlin, München, Hamburg, Köln, Frankfurt, Stuttgart, Düsseldorf und in jeder weiteren deutschen Stadt im Einsatz. Sie konzentrieren sich auf Ihre Gäste, wir auf den Roboter.</p>
        <p class="body-text">Sehen Sie sich unsere spezialisierten Angebote an: <a href="messen.html" style="color:var(--text); text-decoration:underline; text-underline-offset:3px;">Roboter für Messen und Ausstellungen</a> sowie <a href="konferenzen.html" style="color:var(--text); text-decoration:underline; text-underline-offset:3px;">Roboter für Konferenzen und Galas</a>.</p>
      </div>
      <ul class="onas-usps">
        <li>Eigene Technik — keine Zwischenhändler, keine Überraschungen</li>
        <li>Dedizierter Operator für die gesamte Veranstaltungsdauer</li>
        <li>Vollständiger Haftpflichtschutz — Sicherheit auf beiden Seiten</li>
        <li>Einsätze in jeder deutschen Stadt</li>
        <li>Bester Preis für die Miete eines humanoiden Roboters am Markt</li>
      </ul>
    </div>

    <div class="transport-callout">
      <div class="transport-callout__glow" aria-hidden="true"></div>
      <div class="transport-callout__left">
        <span class="transport-callout__eyebrow">Bei uns Standard</span>
        <p class="transport-callout__claim"><em>Anfahrt inklusive</em><br />in ganz<br />Deutschland.</p>
      </div>
      <div class="transport-callout__right">
        <p class="transport-callout__note">Keine Kilometerpauschale, keine Mindestentfernung, keine versteckten Kosten. Wir bringen den Roboter zu jeder Veranstaltung — von Hamburg bis München, von Köln bis Dresden — und berechnen dafür keinen Cent extra.</p>
        <ul class="transport-callout__stats">
          <li><strong>0 €</strong><span>pro Kilometer</span></li>
          <li><strong>100 %</strong><span>Deutschland abgedeckt</span></li>
          <li><strong>24 h</strong><span>bis zum Angebot</span></li>
        </ul>
        <a href="#kontakt" class="btn-primary">Termin mit kostenloser Anfahrt sichern →</a>
      </div>
    </div>
  </section>

  <!-- ROBOTER-GALERIE -->
  <section class="section robot-gallery-section">
    <div class="section-header">
      <span class="tag">Roboter</span>
      <h2 class="section-title">Unitree G1 —<br />Humanoid neuer Generation</h2>
    </div>
    <div class="robot-gallery">
      <figure class="robot-gallery__main">
        <picture>
          <source srcset="robot-g1-960.webp 960w, robot-g1.webp 2390w" sizes="(min-width: 769px) 800px, 92vw" type="image/webp" />
          <img src="robot-g1.jpg"
               alt="Humanoider Roboter Unitree G1 — silberner Humanoid mit blauem Visier, Miete für Events in Deutschland"
               width="800" height="800"
               loading="lazy" />
        </picture>
        <figcaption>Unitree G1 · 132 cm · 35 kg · 23 Freiheitsgrade</figcaption>
      </figure>
      <div class="robot-gallery__side">
        <figure class="robot-gallery__action">
          <picture>
            <source srcset="robot-g1-action.webp" type="image/webp" />
            <img src="robot-g1-action.jpg"
                 alt="Unitree G1 in einer Tanzchoreografie — Aufnahme von einer echten 33bots-Show"
                 width="600" height="600"
                 loading="lazy" />
          </picture>
          <figcaption>Dynamische Choreografien und Live-Shows</figcaption>
        </figure>
        <div class="robot-gallery__specs">
          <div class="robot-spec"><span class="robot-spec__val">132 cm</span><span class="robot-spec__lbl">Größe</span></div>
          <div class="robot-spec"><span class="robot-spec__val">35 kg</span><span class="robot-spec__lbl">Gewicht</span></div>
          <div class="robot-spec"><span class="robot-spec__val">23</span><span class="robot-spec__lbl">DOF</span></div>
          <div class="robot-spec"><span class="robot-spec__val">2 m/s</span><span class="robot-spec__lbl">Geschwindigkeit</span></div>
        </div>
      </div>
    </div>
  </section>

  <!-- VIDEO -->
  <section class="section" id="video">
    <div class="section-header">
      <span class="tag">Video</span>
      <h2 class="section-title">Der Roboter<br />im Einsatz</h2>
    </div>
    <div style="display:flex; flex-wrap:wrap; gap:var(--s6); align-items:center; justify-content:center; max-width:1000px; margin:0 auto;">
      <video controls muted playsinline preload="none"
             poster="video/33bots-robot-event-poster.jpg"
             width="360" height="640"
             style="width:min(360px,90vw); border-radius:16px; border:1px solid var(--border-mid); background:var(--surface-2);"
             aria-label="Humanoider Roboter Unitree G1 im Einsatz — er läuft, gestikuliert und tanzt">
        <source src="video/33bots-robot-event.mp4" type="video/mp4" />
        Ihr Browser unterstützt kein HTML5-Video.
      </video>
      <div style="max-width:420px; display:flex; flex-direction:column; gap:var(--s4); text-align:left;">
        <p style="color:var(--text-2); font-size:1rem; line-height:1.8; margin:0;">So sieht der <strong style="color:var(--text);">Unitree G1</strong> live aus: Er läuft, gestikuliert, begrüßt Gäste und tanzt. Auf der Brustplatte sehen Sie unseren Standard — <strong style="color:var(--text);">kostenloses Branding</strong> mit Logo und QR-Code Ihrer Marke.</p>
        <a href="#kontakt" class="btn-primary" style="display:inline-flex; align-self:flex-start;">Show reservieren →</a>
      </div>
    </div>
  </section>

  <!-- STATEMENT -->
  <div class="statement">
    <div class="statement__inner">
      <blockquote class="statement__quote">
        „Wenn der Roboter den Saal betritt —<br />zücken alle ihr Handy."
      </blockquote>
      <p class="statement__sub">Das ist keine Metapher, sondern der Bericht von jeder Veranstaltung, die wir betreut haben.</p>
      <a href="#kontakt" class="btn-cta">Termin auf Verfügbarkeit prüfen →</a>
    </div>
  </div>

  <!-- PREISE -->
  <section class="section pricing-section" id="preise">
    <div class="section-header">
      <span class="tag">Preise</span>
      <h2 class="section-title">Ein Preis.<br />Alles inklusive.</h2>
      <p class="pricing-lead">Ein transparenter Tagessatz und alles ist enthalten. Keine Sternchen, keine Aufschläge, keine „Zusatzkosten", die in der letzten Mail auftauchen.</p>
    </div>
    <div class="pricing-grid">
      <article class="price-card price-card--main">
        <span class="price-card__badge">Komplettpaket — alles inklusive</span>
        <h3 class="price-card__name">Humanoider Roboter Unitree G1</h3>
        <p class="price-card__for">Der Star Ihrer Veranstaltung — Messe, Konferenz, Gala oder Eröffnung. Den ganzen Tag.</p>
        <div class="price-card__price">
          <span class="price-card__amount">{PRICE_RANGE}</span>
          <span class="price-card__period">pro Veranstaltungstag</span>
        </div>
        <p class="price-card__note">Der endgültige Preis hängt ausschließlich vom Veranstaltungsort ab. Wir nennen den Betrag sofort — und genau dieser Betrag steht später auf der Rechnung.</p>
        <ul class="price-card__list">
          <li>Roboter-Show über den gesamten Veranstaltungstag</li>
          <li>Zertifizierter Operator von Anfang bis Ende</li>
          <li>Anfahrt deutschlandweit inklusive — ohne Kilometerlimit</li>
          <li>Kostenloses Branding: Ihr Logo und QR-Code auf dem Roboter</li>
          <li>Choreografien, Interaktion mit Gästen und Tanz-Shows</li>
          <li>Haftpflichtversicherung und technische Betreuung vor Ort</li>
        </ul>
        <p class="price-card__zero">Der Preis enthält absolut alles. <strong>KEINE Zusatzkosten.</strong></p>
        <a href="#kontakt" class="btn-cta">Kostenloses Angebot anfordern →</a>
      </article>
      <aside class="price-card price-card--addon">
        <span class="price-card__badge price-card__badge--addon">Zusatzoption</span>
        <h3 class="price-card__name">Roboterhund</h3>
        <p class="price-card__for">Das perfekte Duo: Der Humanoid macht die Show, der Roboterhund erobert die Herzen der Gäste.</p>
        <div class="price-card__price">
          <span class="price-card__amount">{DOG_PRICE}</span>
          <span class="price-card__period">pro Veranstaltungstag</span>
        </div>
        <ul class="price-card__list">
          <li>Dynamische Shows, Tricks und Interaktionen</li>
          <li>Magnet für Fotos und Videos der Gäste</li>
          <li>Operator im Preis enthalten</li>
        </ul>
        <a href="#kontakt" class="tile__link">Zum Angebot hinzufügen →</a>
      </aside>
    </div>
    <div class="pricing-promo">
      <span class="pricing-promo__badge">Aktion</span>
      <p class="pricing-promo__text"><strong>−15 % auf jeden Tag</strong> ab zwei Veranstaltungstagen. Messen, Festivals, Roadshows — je länger der Roboter bleibt, desto weniger zahlen Sie pro Tag.</p>
      <a href="#kontakt" class="btn-primary">Angebot für Ihren Termin anfragen →</a>
    </div>
  </section>

  <!-- STIMMEN -->
  <section class="section testimonials-section">
    <div class="section-header">
      <span class="tag">Stimmen</span>
      <h2 class="section-title">Was Kunden sagen</h2>
    </div>
    <div class="testimonials">
      <div class="testimonial">
        <p class="testimonial__quote">„Der Effekt hat unsere kühnsten Erwartungen übertroffen. Das Interesse war während der gesamten Veranstaltung enorm — ich hätte nicht gedacht, dass wir so viel Aufmerksamkeit bekommen."</p>
        <div class="testimonial__meta">
          <span class="testimonial__name">Karolina M.</span>
          <span class="testimonial__role">Marketing · IT-Branche</span>
        </div>
      </div>
      <div class="testimonial">
        <p class="testimonial__quote">„Das war eine der besten organisatorischen Entscheidungen. Die positiven Reaktionen der Teilnehmenden und ihr Engagement sind für uns die beste Bewertung des gesamten Projekts."</p>
        <div class="testimonial__meta">
          <span class="testimonial__name">Piotr Z.</span>
          <span class="testimonial__role">Veranstalter · Firmengala</span>
        </div>
      </div>
      <div class="testimonial">
        <p class="testimonial__quote">„Die Zusammenarbeit hat zu unglaublicher Reichweite in den sozialen Medien geführt. Das ist die Art von echtem Interesse, die man nicht einfach kaufen kann."</p>
        <div class="testimonial__meta">
          <span class="testimonial__name">Magdalena T.</span>
          <span class="testimonial__role">PR-Managerin · Technologiemesse</span>
        </div>
      </div>
    </div>
  </section>

  <!-- EINSATZBEREICHE -->
  <section class="section" id="einsatzbereiche">
    <div class="section-header">
      <span class="tag">Einsatzbereiche</span>
      <h2 class="section-title">Wo der G1<br />überzeugt</h2>
    </div>
    <div class="use-grid">
      <div class="use-item">
        <span class="use-num">01</span>
        <h3>Konferenzen &amp; Summits</h3>
        <p>Der Roboter als Gastgeber, Guide oder Attraktion am Registration Desk.</p>
        <a href="konferenzen.html" class="tile__link" style="margin-top:var(--s2);display:inline-flex;">Konferenz-Angebot ansehen →</a>
      </div>
      <div class="use-item">
        <span class="use-num">02</span>
        <h3>Messen &amp; Ausstellungen</h3>
        <p>Ziehen Sie zehnmal mehr Aufmerksamkeit an den Stand als mit jedem Banner.</p>
        <a href="messen.html" class="tile__link" style="margin-top:var(--s2);display:inline-flex;">Mehr erfahren →</a>
      </div>
      <div class="use-item">
        <span class="use-num">03</span>
        <h3>Firmenfeiern &amp; Jubiläen</h3>
        <p>Sommerfeste, Jubiläen, Galas — Gesprächsstoff weit über den Abend hinaus.</p>
        <a href="roboter-mieten.html" class="tile__link" style="margin-top:var(--s2);display:inline-flex;">Roboter mieten →</a>
      </div>
      <div class="use-item">
        <span class="use-num">04</span>
        <h3>Tage der offenen Tür &amp; Bildung</h3>
        <p>Schulen, Hochschulen, Science Center — Technologie, die die Welt verändert.</p>
        <a href="tag-der-offenen-tuer.html" class="tile__link" style="margin-top:var(--s2);display:inline-flex;">Mehr erfahren →</a>
      </div>
      <div class="use-item">
        <span class="use-num">05</span>
        <h3>Foto- &amp; Videoproduktion</h3>
        <p>Werbematerial mit einem Humanoiden. Aufmerksamkeit garantiert.</p>
      </div>
      <div class="use-item">
        <span class="use-num">06</span>
        <h3>Produktlaunch</h3>
        <p>Store-Eröffnung oder Imagekampagne — der G1 macht die Show.</p>
      </div>
    </div>
  </section>

  <!-- ABLAUF -->
  <section class="section process-section" id="ablauf">
    <div class="section-header">
      <span class="tag">So arbeiten wir</span>
      <h2 class="section-title">Zusammenarbeit ohne Stress<br />und ohne Anzahlung</h2>
      <p class="process-lead">Sie reservieren den Termin kostenlos und erhalten die Rechnung erst nach der erfolgreichen Veranstaltung. Das Risiko tragen wir — Sie wählen nur das Datum.</p>
    </div>
    <div class="process">
      <div class="process-step">
        <span class="process-step__n">01</span>
        <div>
          <h3>Schneller Kontakt</h3>
          <p>Sie füllen ein kurzes Formular aus oder schreiben eine E-Mail. Das dauert zwei Minuten.</p>
        </div>
      </div>
      <div class="process-step">
        <span class="process-step__n">02</span>
        <div>
          <h3>Rückruf von uns</h3>
          <p>Wir rufen zurück, lernen Ihre Veranstaltung kennen und empfehlen das passende Showformat.</p>
        </div>
      </div>
      <div class="process-step">
        <span class="process-step__n">03</span>
        <div>
          <h3>Angebot in 24 Stunden</h3>
          <p>Ein konkreter Betrag ohne Sternchen — meist noch am selben Tag.</p>
        </div>
      </div>
      <div class="process-step process-step--key">
        <span class="process-step__n">04</span>
        <div>
          <h3>Einfacher Vertrag</h3>
          <p><strong>Kostenlose Terminreservierung, KEINE Anzahlung.</strong> Sie brauchen ein längeres Zahlungsziel? Wir richten es ein.</p>
        </div>
      </div>
      <div class="process-step">
        <span class="process-step__n">05</span>
        <div>
          <h3>Wir übernehmen alles</h3>
          <p>Anfahrt, Aufbau, Operator und eine Show auf höchstem Niveau.</p>
        </div>
      </div>
      <div class="process-step process-step--key">
        <span class="process-step__n">06</span>
        <div>
          <h3>Zahlung nach dem Event</h3>
          <p>Die Rechnung stellen wir <strong>erst nach der Veranstaltung</strong>. Zuerst das Ergebnis, dann die Zahlung.</p>
        </div>
      </div>
    </div>
    <div class="process-cta">
      <a href="#kontakt" class="btn-cta">Mit dem kostenlosen Angebot starten →</a>
      <p class="hero__cta-note">Unverbindlich · Antwort innerhalb von 24 h</p>
    </div>
  </section>

  <!-- DEMO CTA -->
  <div class="video-teaser">
    <div class="video-teaser__content">
      <span class="tag">Live</span>
      <h2 class="video-teaser__title">Sie wollen den G1<br />live erleben?</h2>
      <a href="#kontakt" class="btn-cta">Kostenloses Angebot anfordern →</a>
      <p class="video-teaser__note">Unverbindlich · Keine Anzahlung · Antwort in 24 h</p>
    </div>
  </div>

{faq_html(FAQ_MAIN, "Häufige<br />Fragen")}

  <!-- STÄDTE -->
  <section class="section" id="staedte">
    <div class="section-header">
      <span class="tag">Städte</span>
      <h2 class="section-title">Roboter mieten<br />in Ihrer Stadt</h2>
    </div>
    <div style="max-width:900px; margin:0 auto;">
      <div style="display:flex; flex-wrap:wrap; gap:var(--s2);">
{city_chips}
      </div>
      <p style="margin-top:var(--s4); color:var(--text-2); font-size:0.95rem;">Ihre Stadt ist nicht dabei? Kein Problem — wir sind deutschlandweit im Einsatz, die Anfahrt ist immer inklusive.</p>
    </div>
  </section>

  <!-- KONTAKT -->
  <section class="section contact-section" id="kontakt">
    <div class="contact-layout">
      <div class="contact-left">
        <span class="tag">Kontakt</span>
        <h2 class="section-title">Kostenloses Angebot<br />für Ihr Event.</h2>
        <p class="body-text">Schreiben Sie uns — wir rufen zurück und erstellen umgehend ein konkretes Angebot. Die Terminreservierung ist kostenlos und ohne Anzahlung, die Rechnung stellen wir erst nach der Veranstaltung.</p>
        <div class="contact-details" itemscope itemtype="https://schema.org/ProfessionalService">
          <meta itemprop="name" content="33bots – Humanoide Roboter für Events und Messen mieten" />
          <meta itemprop="url" content="{DOMAIN}" />
          <div class="contact-detail">
            <span class="contact-detail__label">Unternehmen</span>
            <span class="contact-detail__val" itemprop="name">33bots – Humanoide Roboter mieten</span>
          </div>
          <a href="mailto:{EMAIL}" class="contact-detail" itemprop="email" content="{EMAIL}">
            <span class="contact-detail__label">E-Mail</span>
            <span class="contact-detail__val">{EMAIL}</span>
          </a>
          <a href="tel:{PHONE_RAW}" class="contact-detail" itemprop="telephone" content="{PHONE_RAW}">
            <span class="contact-detail__label">Telefon</span>
            <span class="contact-detail__val">{PHONE_HUMAN}</span>
          </a>
          <a href="tel:{PHONE2_RAW}" class="contact-detail">
            <span class="contact-detail__label">Telefon</span>
            <span class="contact-detail__val">{PHONE2_HUMAN}</span>
          </a>
          <div class="contact-detail">
            <span class="contact-detail__label">Einsatzgebiet</span>
            <span class="contact-detail__val" itemprop="areaServed">Deutschlandweit</span>
          </div>
        </div>

        <nav class="coverage" aria-label="Roboter mieten — bediente Städte">
          <p class="coverage__label">Wir kommen ohne Aufpreis nach:</p>
          <ul class="coverage__cities">
{coverage}
          </ul>
          <p class="coverage__note">und überall sonst — die Anfahrt ist im Preis enthalten</p>
        </nav>
      </div>
      <div class="contact-right">
{contact_form()}
      </div>
    </div>
  </section>

{footer("")}"""


# ── Podstrony ofertowe ────────────────────────────────────────────────
def build_offer_page(filename, h1, eyebrow, title, desc, kw, lead, sections, faq, crumb):
    body_sections = "\n\n".join(sections)
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
{gtm_head()}
{head_meta(title, desc, kw, filename)}

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Service",
    "name": "{h1}",
    "description": "{desc}",
    "url": "{DOMAIN}/{filename}",
    "image": "{DOMAIN}/robot-g1.jpg",
    "serviceType": "Vermietung humanoider Roboter",
    "provider": {{
      "@type": "Organization",
      "name": "33bots",
      "url": "{DOMAIN}/",
      "email": "{EMAIL}",
      "telephone": "{PHONE_RAW}"
    }},
    "areaServed": {{"@type": "Country", "name": "Germany"}},
    "offers": {{
      "@type": "AggregateOffer",
      "priceCurrency": "EUR",
      "lowPrice": "{PRICE_LOW_NUM}",
      "highPrice": "{PRICE_HIGH_NUM}",
      "availability": "https://schema.org/InStock"
    }}
  }}
  </script>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type": "ListItem", "position": 1, "name": "Startseite", "item": "{DOMAIN}/"}},
      {{"@type": "ListItem", "position": 2, "name": "{crumb}", "item": "{DOMAIN}/{filename}"}}
    ]
  }}
  </script>

{json_ld_faq(faq)}
{head_assets(chr(10) + '''  <style>
    .hero { grid-template-columns: 1fr; min-height: 60vh; }
    .hero__content { max-width: none; padding: var(--s12) 0 var(--s8); }
    .hero__title { text-wrap: unset; }
  </style>''')}
</head>
<body>
{gtm_body()}

{nav()}
  <nav class="crumbs" aria-label="Brotkrümel" style="max-width:1200px; margin:0 auto; padding:calc(var(--s8) + 48px) var(--s5) 0; font-size:0.78rem; letter-spacing:0.02em;">
    <a href="index.html" style="color:var(--text-3); text-decoration:none;">Startseite</a> <span aria-hidden="true" style="color:var(--text-3);">›</span> <span style="color:var(--text-2);">{crumb}</span>
  </nav>

  <section class="hero">
    <div class="hero__content">
      <p class="hero__eyebrow">{eyebrow}</p>
      <h1 class="hero__title">{h1}</h1>
      <p class="hero__sub">{lead}</p>
      <div class="hero__ctas">
        <a href="#kontakt" class="btn-cta">Kostenloses Angebot anfordern →</a>
        <a href="index.html#preise" class="btn-cta--ghost">Preise ansehen ↓</a>
      </div>
      <div class="hero__trust">
        <span class="hero__trust-item">✓ Anfahrt inklusive</span>
        <span class="hero__trust-item">✓ Operator inklusive</span>
        <span class="hero__trust-item">✓ Branding ohne Aufpreis</span>
        <span class="hero__trust-item">✓ Keine Anzahlung</span>
      </div>
    </div>
  </section>

{body_sections}

  <section class="section" style="padding-top:0;">
    <div style="max-width:900px; margin:0 auto;">
      <p style="font-size:0.75rem; color:var(--text-3); text-transform:uppercase; letter-spacing:0.1em; font-weight:700; margin-bottom:var(--s3);">Roboter mieten in Ihrer Stadt</p>
      <div style="display:flex; flex-wrap:wrap; gap:var(--s2);">
{city_links_block()}
      </div>
    </div>
  </section>

{faq_html(faq, "Häufige Fragen")}

  <section class="section contact-section" id="kontakt">
    <div class="contact-layout">
      <div class="contact-left">
        <span class="tag">Kontakt</span>
        <h2 class="section-title">Kostenloses Angebot<br />anfordern.</h2>
        <p class="body-text">Schreiben Sie uns — Sie erhalten innerhalb eines Werktags ein konkretes Angebot inklusive Verfügbarkeit.</p>
        <div class="contact-details">
          <a href="mailto:{EMAIL}" class="contact-detail">
            <span class="contact-detail__label">E-Mail</span>
            <span class="contact-detail__val">{EMAIL}</span>
          </a>
          <a href="tel:{PHONE_RAW}" class="contact-detail">
            <span class="contact-detail__label">Telefon</span>
            <span class="contact-detail__val">{PHONE_HUMAN}</span>
          </a>
          <a href="tel:{PHONE2_RAW}" class="contact-detail">
            <span class="contact-detail__label">Telefon</span>
            <span class="contact-detail__val">{PHONE2_HUMAN}</span>
          </a>
          <div class="contact-detail">
            <span class="contact-detail__label">Einsatzgebiet</span>
            <span class="contact-detail__val">Deutschlandweit</span>
          </div>
        </div>
      </div>
      <div class="contact-right">
{contact_form()}
      </div>
    </div>
  </section>

{footer()}"""


def text_section(heading, paragraphs, subheads=None, cta=True):
    subheads = subheads or []
    body = "\n".join(f'        <p class="body-text">{p}</p>' for p in paragraphs[1:])
    subs = ""
    for h, txt in subheads:
        subs += (f'\n        <h3 style="font-size:1.1rem; font-weight:700; letter-spacing:-0.01em; '
                 f'margin:var(--s6) 0 var(--s2); color:var(--text);">{h}</h3>\n'
                 f'        <p class="body-text">{txt}</p>')
    cta_html = ('\n        <a href="#kontakt" class="btn-primary" style="margin-top:var(--s5); '
                'display:inline-flex;">Angebot anfordern →</a>') if cta else ""
    return f"""  <section class="section">
    <div class="onas-body" style="max-width:860px; margin:0 auto;">
      <div class="onas-text">
        <h2 class="section-title" style="font-size:clamp(1.8rem,3vw,2.8rem); margin-bottom:var(--s4);">{heading}</h2>
        <p class="lead-text">{paragraphs[0]}</p>
{body}{subs}{cta_html}
      </div>
    </div>
  </section>"""


def tiles_section(tag, heading, tiles):
    items = []
    for i, (t_tag, t_title, t_desc) in enumerate(tiles):
        light = " tile--light" if i == 1 else ""
        items.append(f"""      <div class="tile{light}">
        <div class="tile__top"><span class="tile__tag">{t_tag}</span></div>
        <h3 class="tile__title">{t_title}</h3>
        <p class="tile__desc">{t_desc}</p>
        <a href="#kontakt" class="tile__link">Angebot anfragen →</a>
      </div>""")
    return f"""  <section class="section tiles-section">
    <div class="section-header">
      <span class="tag">{tag}</span>
      <h2 class="section-title">{heading}</h2>
    </div>
    <div class="tiles">
{chr(10).join(items)}
    </div>
  </section>"""


def video_section(alt, copy):
    return f"""  <section class="section" id="video" style="padding-top:0;">
    <div style="display:flex; flex-wrap:wrap; gap:var(--s6); align-items:center; justify-content:center; max-width:900px; margin:0 auto;">
      <video controls muted playsinline preload="none"
             poster="video/robot-taniec-poster.jpg"
             width="300" height="533"
             style="width:min(300px,80vw); border-radius:16px; border:1px solid var(--border-mid); background:var(--surface-2);"
             aria-label="{alt}">
        <source src="video/robot-taniec.mp4" type="video/mp4" />
        Ihr Browser unterstützt kein HTML5-Video.
      </video>
      <div style="max-width:400px; display:flex; flex-direction:column; gap:var(--s4); text-align:left;">
        <p style="color:var(--text-2); font-size:1rem; line-height:1.8; margin:0;">{copy}</p>
        <a href="#kontakt" class="btn-primary" style="display:inline-flex; align-self:flex-start;">Show reservieren →</a>
      </div>
    </div>
  </section>"""


def offer_pages():
    pages = {}

    # 1. roboter-mieten.html
    pages["roboter-mieten.html"] = build_offer_page(
        filename="roboter-mieten.html",
        h1="Humanoiden Roboter<br />mieten.",
        eyebrow="Roboter mieten · Deutschlandweit · Alles inklusive",
        title="Humanoiden Roboter mieten — Unitree G1 für Ihr Event | 33bots",
        desc=(f"Humanoiden Roboter Unitree G1 mieten: {PRICE_RANGE} pro Veranstaltungstag, Anfahrt, Operator und "
              f"Branding inklusive. Keine Anzahlung, Rechnung nach dem Event."),
        kw="humanoiden roboter mieten, roboter mieten, Unitree G1 mieten, roboter vermietung, event roboter",
        lead=("Ein kompletter Showtag mit dem Unitree G1 — Anfahrt, zertifizierter Operator, Branding und "
              "Versicherung sind im Preis enthalten. Sie buchen einmal und bekommen alles."),
        crumb="Roboter mieten",
        sections=[
            tiles_section("Was Sie bekommen", "Ein Paket,<br />keine Extras", [
                ("Ganzer Tag", "Showtag statt Stundentakt",
                 "Der Roboter ist den kompletten Veranstaltungstag im Einsatz — kein Stundenzähler, keine Verlängerungsaufschläge."),
                ("Operator", "Zertifizierter Operator inklusive",
                 "Unser Operator baut auf, steuert den Roboter und beantwortet die Fragen Ihrer Gäste. Sie müssen nichts können."),
                ("Branding", "Ihr Logo ohne Aufpreis",
                 "Logo und QR-Code kommen auf die Brustplatte des G1 — in jedem Foto Ihrer Gäste sichtbar."),
            ]),
            text_section(
                "Was der Unitree G1 auf Ihrer Veranstaltung macht",
                [("Der G1 ist ein 132 cm großer, frei laufender Humanoid mit 23 Freiheitsgraden — kein Roboter auf "
                  "Rädern und keine ferngesteuerte Puppe. Genau dieser Unterschied ist der Grund, warum Gäste stehen "
                  "bleiben."),
                 ("Er begrüßt Ankommende am Eingang, begleitet Gäste zum Stand, posiert für Fotos, gestikuliert im "
                  "Gespräch und tanzt eine Choreografie, wenn der Moment passt. Ablauf und Intensität stimmen wir vorab "
                  "mit Ihnen ab — vom dezenten Empfangsformat bis zum Bühnenauftritt."),
                 ],
                subheads=[
                    ("Technische Voraussetzungen vor Ort",
                     "Eine 230-V-Steckdose und rund 2×2 m ebene Fläche genügen. Internet oder besondere Beleuchtung "
                     "sind nicht nötig. Unser Operator ist 30–45 Minuten vor Türöffnung einsatzbereit."),
                    ("Sicherheit",
                     "LiDAR und Computer Vision lassen den G1 Hindernissen und Personen in Echtzeit ausweichen. "
                     "Zusätzlich überwacht unser Operator den Einsatz durchgehend; eine Haftpflichtversicherung ist "
                     "im Preis enthalten."),
                    ("Preis und Konditionen",
                     f"{PRICE_RANGE} pro Veranstaltungstag, abhängig ausschließlich vom Ort. Ab zwei Tagen 15 % Rabatt "
                     f"auf jeden Tag. Der Roboterhund ist optional für {DOG_PRICE} pro Tag buchbar. Terminreservierung "
                     f"kostenlos, keine Anzahlung, Rechnung nach dem Event."),
                ]),
            video_section("Humanoider Roboter Unitree G1 im Einsatz",
                          "So sieht der <strong style=\"color:var(--text);\">Unitree G1</strong> live aus — er läuft, "
                          "gestikuliert und tanzt. Genau diese Show können Sie bei Ihrer Veranstaltung haben, mit Ihrem "
                          "Branding auf der Brustplatte."),
        ],
        faq=[
            ("Wie schnell bekomme ich ein Angebot?",
             "In der Regel innerhalb von 24 Stunden, oft noch am selben Tag. Sie erhalten einen konkreten Betrag ohne "
             "Sternchen."),
            ("Kann ich einen Termin reservieren, ohne sofort zu zahlen?",
             "Ja. Die Terminreservierung ist kostenlos und ohne Anzahlung. Die Rechnung stellen wir erst nach der "
             "Veranstaltung."),
            ("Wie viele Roboter können Sie gleichzeitig stellen?",
             "Wir arbeiten mit einer eigenen Flotte. Für größere Formate stellen wir mehrere Einheiten plus zusätzliche "
             "Operator — bitte fragen Sie das früh an, damit wir die Termine sichern können."),
            ("Ist der Roboterhund einzeln buchbar?",
             f"Der Roboterhund ist als Ergänzung zum humanoiden Roboter konzipiert und kostet {DOG_PRICE} pro "
             f"Veranstaltungstag inklusive Operator."),
        ],
    )

    # 2. messen.html
    pages["messen.html"] = build_offer_page(
        filename="messen.html",
        h1="Roboter für Messen<br />und Ausstellungen.",
        eyebrow="Messen · Standfrequenz · Leadgenerierung",
        title="Roboter für Messen mieten — mehr Standbesucher | 33bots",
        desc=("Humanoiden Roboter für Ihren Messestand mieten. Mehr Standfrequenz, mehr Gespräche, mehr Leads — "
              "Anfahrt und Operator deutschlandweit inklusive."),
        kw="roboter messe mieten, messestand attraktion, publikumsmagnet messestand, roboter messestand, Unitree G1 messe",
        lead=("Auf einer Messe entscheidet sich alles in drei Sekunden: Bleibt der Besucher stehen oder geht er weiter? "
              "Ein frei laufender humanoider Roboter beantwortet diese Frage zu Ihren Gunsten."),
        crumb="Messen & Ausstellungen",
        sections=[
            tiles_section("Auf dem Stand", "Was der Roboter<br />für Sie leistet", [
                ("Frequenz", "Besucher bleiben stehen",
                 "Der G1 wirkt aus mehreren Metern Entfernung. Ihr Team muss niemanden mehr ansprechen — die Gäste kommen von selbst."),
                ("Leads", "Aus Aufmerksamkeit werden Gespräche",
                 "Der QR-Code auf der Brustplatte des Roboters führt direkt zu Ihrem Formular, Ihrer Landingpage oder Ihrem Gewinnspiel."),
                ("Reichweite", "Jeder Besucher filmt",
                 "Ihr Stand erscheint in hunderten Stories und Clips — ohne Mediabudget und ohne Agenturhonorar."),
            ]),
            text_section(
                "Roboter auf dem Messestand — so funktioniert es in der Praxis",
                [("Messestände konkurrieren nicht um Inhalte, sondern um Blicke. Wer auf einer Leitmesse mit tausenden "
                  "Ausstellern sichtbar sein will, braucht ein Element, das sich bewegt und das man nicht ignorieren kann."),
                 ("Der Unitree G1 läuft über Ihre Standfläche, begrüßt Vorbeigehende, posiert für Fotos und übergibt "
                  "das Gespräch dann an Ihr Team. Unser Operator ist den ganzen Messetag vor Ort und steuert die "
                  "Intensität — ruhiger am Vormittag, aktiver zu den Stoßzeiten."),
                 ],
                subheads=[
                    ("Standgröße und Aufbau",
                     "Rund 2×2 m freie Fläche reichen für den Betrieb. Wir stimmen Aufbauzeiten, Standordnung und "
                     "Sicherheitsvorgaben vorab mit Ihnen und dem Messeveranstalter ab."),
                    ("Mehrtägige Messen",
                     "Ab zwei Veranstaltungstagen erhalten Sie 15 % Rabatt auf jeden Tag — bei einer viertägigen "
                     "Leitmesse ist das ein spürbarer Unterschied."),
                    ("Branding",
                     "Ihr Logo und ein QR-Code kommen kostenlos auf die Brustplatte. Auf jedem Besucherfoto ist damit "
                     "Ihre Marke im Bild."),
                ]),
        ],
        faq=[
            ("Wie viel mehr Standfrequenz bringt ein Roboter?",
             "Das hängt von Halle, Standposition und Messeformat ab. Was wir zuverlässig beobachten: Besucher bleiben "
             "stehen, filmen und sprechen Ihr Team an — der schwierigste Teil der Standarbeit ist damit erledigt."),
            ("Klärt der Veranstalter Sicherheitsfragen mit Ihnen?",
             "Ja. Wir liefern die nötigen Angaben zu Gerät, Stromversorgung und Betrieb, damit Sie die Freigabe beim "
             "Messeveranstalter problemlos einholen können. Eine Haftpflichtversicherung besteht."),
            ("Können wir den Roboter auf mehreren Messen im Jahr einsetzen?",
             "Ja — gerne mit Rahmenvereinbarung. Sprechen Sie uns auf Ihre Messeplanung an, dann blocken wir die "
             "Termine frühzeitig."),
            ("Was kostet ein Messetag?",
             f"{PRICE_RANGE} pro Tag inklusive Anfahrt, Operator, Branding und Versicherung. Ab zwei Tagen 15 % Rabatt "
             f"pro Tag."),
        ],
    )

    # 3. konferenzen.html
    pages["konferenzen.html"] = build_offer_page(
        filename="konferenzen.html",
        h1="Roboter für Konferenzen<br />und Galas.",
        eyebrow="Konferenzen · Galas · Award-Abende",
        title="Roboter für Konferenzen und Galas mieten | 33bots",
        desc=("Humanoiden Roboter für Konferenz, Kongress oder Gala mieten. Empfang, Bühnenmoment und Fotoanlass — "
              "Operator und Anfahrt deutschlandweit inklusive."),
        kw="roboter konferenz mieten, roboter gala, kongress attraktion, roboter bühne event, Unitree G1 konferenz",
        lead=("Auf einer Konferenz erinnern sich die Gäste selten an die Agenda — aber immer an den Moment, in dem "
              "ein humanoider Roboter den Saal betreten hat."),
        crumb="Konferenzen & Galas",
        sections=[
            tiles_section("Formate", "Drei Rollen,<br />ein Roboter", [
                ("Empfang", "Gastgeber am Eingang",
                 "Der G1 begrüßt Ankommende, weist den Weg zur Registrierung und setzt den Ton für den ganzen Tag."),
                ("Bühne", "Der Moment, der bleibt",
                 "Ein kurzer Auftritt vor der Keynote oder zur Preisverleihung — der Roboter übernimmt die Bühne und übergibt an Ihre Speaker."),
                ("Pausen", "Gesprächsstoff im Foyer",
                 "In den Pausen steht der Roboter im Foyer, posiert für Fotos und liefert das Netzwerk-Thema des Tages."),
            ]),
            text_section(
                "Konferenz, Kongress, Gala — was jeweils funktioniert",
                [("Nicht jedes Format verträgt dieselbe Inszenierung. Auf einem Fachkongress arbeiten wir dezenter als "
                  "auf einer Award-Nacht — die Wirkung bleibt in beiden Fällen dieselbe."),
                 ("Bei Konferenzen setzen wir den G1 typischerweise im Foyer und am Registration Desk ein: Er stört das "
                  "Programm nicht und sorgt trotzdem für Gesprächsstoff in jeder Pause. Bei Galas und Award-Abenden "
                  "übernimmt er den Sektempfang oder einen kurzen Bühnenmoment — inklusive Tanzchoreografie, wenn Sie "
                  "es wünschen."),
                 ],
                subheads=[
                    ("Abstimmung mit Ihrer Regie",
                     "Timing, Auftrittslänge und Positionen legen wir vorab gemeinsam fest. Unser Operator ist während "
                     "der gesamten Veranstaltung ansprechbar und passt sich an Programmverschiebungen an."),
                    ("Internationales Publikum",
                     "Der Effekt funktioniert sprachunabhängig — er entsteht über Bewegung und Präsenz. Ihr Branding "
                     "auf der Brustplatte bleibt in jedem Foto sichtbar."),
                    ("Konditionen",
                     f"{PRICE_RANGE} pro Veranstaltungstag, alles inklusive. Kostenlose Terminreservierung, keine "
                     f"Anzahlung, Rechnung erst nach dem Event."),
                ]),
            video_section("Humanoider Roboter Unitree G1 auf einer Gala",
                          "Der <strong style=\"color:var(--text);\">Unitree G1</strong> im Gala-Einsatz — Empfang, "
                          "Bühnenmoment und Fotoanlass in einem. Auf Wunsch mit Tanzchoreografie zur passenden Musik."),
        ],
        faq=[
            ("Stört der Roboter das Konferenzprogramm?",
             "Nein — wenn er richtig platziert ist. Auf Fachkongressen arbeiten wir bewusst im Foyer und in den Pausen. "
             "Der Ablauf wird vorher mit Ihnen abgestimmt."),
            ("Kann der Roboter auf der Bühne auftreten?",
             "Ja. Ein kurzer Auftritt vor der Keynote oder bei der Preisverleihung ist eines der wirkungsvollsten "
             "Formate. Timing und Ablauf stimmen wir mit Ihrer Regie ab."),
            ("Kann der Roboter tanzen?",
             "Ja, mehrere Choreografien sind einprogrammiert. Wenn ein DJ auflegt, übernimmt der G1 gerne die Tanzfläche."),
            ("Wie lange dauert der Aufbau?",
             "30–45 Minuten vor Veranstaltungsbeginn. Unser Operator bringt die komplette Ausrüstung mit."),
        ],
    )

    # 4. tag-der-offenen-tuer.html
    pages["tag-der-offenen-tuer.html"] = build_offer_page(
        filename="tag-der-offenen-tuer.html",
        h1="Roboter für Tage der<br />offenen Tür.",
        eyebrow="Tage der offenen Tür · Showrooms · Employer Branding",
        title="Roboter für den Tag der offenen Tür mieten | 33bots",
        desc=("Humanoiden Roboter für Tag der offenen Tür, Showroom oder Karrieremesse mieten. Der Programmpunkt, "
              "über den alle sprechen — Operator und Anfahrt inklusive."),
        kw=("roboter tag der offenen tür, roboter showroom, employer branding roboter, karrieremesse attraktion, "
            "roboter hochschule event"),
        lead=("Ein Tag der offenen Tür lebt davon, dass Menschen kommen — und bleiben. Ein humanoider Roboter "
              "erledigt beides zuverlässiger als jede Anzeige."),
        crumb="Tage der offenen Tür",
        sections=[
            tiles_section("Einsatzfelder", "Wo es besonders<br />gut funktioniert", [
                ("Unternehmen", "Tag der offenen Tür",
                 "Familien, Nachbarschaft, Bewerberinnen und Bewerber — der Roboter ist der Programmpunkt, der auf dem Plakat steht."),
                ("Bildung", "Hochschulen und Schulen",
                 "Bei Studieninformationstagen und Science Slams ist der G1 zuverlässig die meistfotografierte Station."),
                ("Recruiting", "Employer Branding",
                 "Auf Karrieremessen bringt der Roboter Ihren Stand ins Gespräch — und Ihre Recruiter in echte Dialoge."),
            ]),
            text_section(
                "Warum ein Roboter beim Tag der offenen Tür funktioniert",
                [("Bei einem Tag der offenen Tür konkurrieren Sie nicht mit anderen Unternehmen, sondern mit dem "
                  "Wochenende. Es braucht einen Grund zu kommen, der sich in einem Satz weitererzählen lässt."),
                 ("„Da läuft ein echter humanoider Roboter herum" ist genau so ein Satz. Der G1 begrüßt Besucher am "
                  "Eingang, führt Gruppen durch das Gelände, posiert für Fotos und tanzt zum Programmhöhepunkt. "
                  "Besonders bei Familien und jungem Publikum ist der Effekt sofort messbar — an den Handykameras."),
                 ],
                subheads=[
                    ("Indoor und outdoor",
                     "Der G1 kommt mit Asphalt, Rasen, Hallenboden und Teppich zurecht. Für Außeneinsätze brauchen wir "
                     "eine trockene, ebene Fläche und stimmen für den Regenfall vorab eine überdachte Alternative ab."),
                    ("Sicherheit bei viel Publikum",
                     "LiDAR und Computer Vision lassen den Roboter Personen in Echtzeit ausweichen; unser Operator "
                     "begleitet den Einsatz durchgehend. Gerade bei Kindern ist diese doppelte Absicherung wichtig."),
                    ("Kosten",
                     f"{PRICE_RANGE} für den kompletten Veranstaltungstag, inklusive Anfahrt, Operator, Branding und "
                     f"Versicherung. Optional ergänzt der Roboterhund für {DOG_PRICE} pro Tag das Programm."),
                ]),
        ],
        faq=[
            ("Ist der Roboter für Kinder geeignet?",
             "Ja. Der G1 weicht Personen selbstständig aus, zusätzlich überwacht unser Operator jeden Kontakt. Für "
             "Kinder ist der Roboter erfahrungsgemäß der Höhepunkt des Tages."),
            ("Kann der Roboter draußen eingesetzt werden?",
             "Ja, auf trockener und ebener Fläche. Bei Regen weichen wir in einen überdachten Bereich aus — das planen "
             "wir vorher gemeinsam."),
            ("Können wir den Roboter mit dem Roboterhund kombinieren?",
             f"Ja. Der Roboterhund kostet {DOG_PRICE} pro Veranstaltungstag inklusive Operator und ist besonders bei "
             f"Familienveranstaltungen ein starker Zusatz."),
            ("Wie früh sollten wir buchen?",
             "So früh wie möglich — die Terminreservierung ist kostenlos und ohne Anzahlung, es entsteht Ihnen also "
             "kein Risiko durch frühes Buchen."),
        ],
    )

    return pages


# ── Strony miast ──────────────────────────────────────────────────────
def build_city(c):
    city = c["city"]
    slug = c["slug"]
    fn = f"roboter-mieten-{slug}.html"
    title = f"Humanoiden Roboter mieten {city} — Roboter für Events | 33bots"
    desc = (f"Humanoiden Roboter Unitree G1 in {city} mieten — Messen, Konferenzen, Galas. Anfahrt und "
            f"zertifizierter Operator inklusive. Angebot in 24 h →")
    kw = (f"roboter mieten {city}, humanoider roboter {city}, Unitree G1 {city}, event attraktion {city}, "
          f"roboter für messe {city}")

    venues_ld = ", ".join(v[0] for v in c["venues"])
    venue_items = "\n".join(
        f"          <li><strong>{name}</strong> — {d}</li>" for name, d in c["venues"]
    )

    faq_all = list(c["faq"]) + [
        (f"Ist die Anfahrt nach {city} wirklich kostenlos?",
         f"Ja — die Anfahrt ist deutschlandweit im Preis enthalten, auch nach {city}. Es gibt keine "
         f"Kilometerpauschale und keine Nachberechnung. Der Preis im Angebot ist der Endpreis."),
        (f"Was kostet die Miete eines Roboters in {city}?",
         f"{PRICE_RANGE} pro kompletten Veranstaltungstag — inklusive Anfahrt, zertifiziertem Operator, Branding "
         f"und Versicherung. Ab zwei Tagen erhalten Sie 15 % Rabatt auf jeden Tag."),
    ]

    return fn, f"""<!DOCTYPE html>
<html lang="de">
<head>
{gtm_head()}
{head_meta(title, desc, kw, fn)}

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Service",
    "name": "Humanoiden Roboter mieten — {city}",
    "description": "Vermietung des Roboters Unitree G1 für Events, Konferenzen und Messen in {city}. Anfahrt und zertifizierter Operator inklusive.",
    "url": "{DOMAIN}/{fn}",
    "image": "{DOMAIN}/robot-g1.jpg",
    "serviceType": "Vermietung humanoider Roboter für Events",
    "provider": {{
      "@type": "LocalBusiness",
      "name": "33bots – Humanoide Roboter für Events und Messen mieten",
      "url": "{DOMAIN}",
      "telephone": "{PHONE_RAW}",
      "email": "{EMAIL}",
      "sameAs": [
        "https://www.facebook.com/33bots",
        "https://www.instagram.com/33bots_/",
        "https://www.linkedin.com/company/33bots",
        "https://www.tiktok.com/@aimforum"
      ]
    }},
    "areaServed": {{"@type": "City", "name": "{city}"}},
    "offers": {{
      "@type": "AggregateOffer",
      "priceCurrency": "EUR",
      "lowPrice": "{PRICE_LOW_NUM}",
      "highPrice": "{PRICE_HIGH_NUM}",
      "availability": "https://schema.org/InStock"
    }}
  }}
  </script>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type": "ListItem", "position": 1, "name": "Startseite", "item": "{DOMAIN}/"}},
      {{"@type": "ListItem", "position": 2, "name": "Roboter mieten {city}", "item": "{DOMAIN}/{fn}"}}
    ]
  }}
  </script>

{json_ld_faq(faq_all)}

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "VideoObject",
    "name": "Humanoider Roboter Unitree G1 im Einsatz — Miete in {city}",
    "description": "Der humanoide Roboter Unitree G1 live: Er läuft, gestikuliert und tanzt. Miete für Events, Konferenzen und Messen in {city} und Umgebung.",
    "thumbnailUrl": "{DOMAIN}/video/robot-taniec-poster.jpg",
    "contentUrl": "{DOMAIN}/video/robot-taniec.mp4",
    "uploadDate": "2026-07-02",
    "duration": "PT17S",
    "inLanguage": "de",
    "publisher": {{"@type": "Organization", "name": "33bots", "url": "{DOMAIN}", "logo": {{"@type": "ImageObject", "url": "{DOMAIN}/logo.png"}}}}
  }}
  </script>

{head_assets(chr(10) + '''  <style>
    .hero { grid-template-columns: 1fr; min-height: 70vh; }
    .hero__content { max-width: none; padding: var(--s12) 0 var(--s8); }
    .hero__title { text-wrap: unset; }
  </style>''')}
</head>
<body>
{gtm_body()}

{nav()}
  <nav class="crumbs" aria-label="Brotkrümel" style="max-width:1200px; margin:0 auto; padding:calc(var(--s8) + 48px) var(--s5) 0; font-size:0.78rem; letter-spacing:0.02em;">
    <a href="index.html" style="color:var(--text-3); text-decoration:none;">Startseite</a> <span aria-hidden="true" style="color:var(--text-3);">›</span> <span style="color:var(--text-2);">Roboter mieten {city}</span>
  </nav>

  <section class="hero">
    <div class="hero__content">
      <p class="hero__eyebrow">Roboter mieten · {city} · Events</p>
      <h1 class="hero__title">Humanoiden Roboter mieten<br />in {city} —<br />Unitree G1.</h1>
      <p class="hero__sub">Wir betreuen Veranstaltungen in {c["region"]}: {c["claim"]}. Der Unitree G1 kommt zu Ihrer Location — Anfahrt, Operator und Branding sind im Preis enthalten.</p>
      <div class="hero__ctas">
        <a href="#kontakt" class="btn-primary">Termin sichern</a>
        <a href="index.html#preise" class="btn-ghost">Preise ansehen ↓</a>
      </div>
      <div class="hero__trust">
        <span class="hero__trust-item">✓ Bester Preis am Markt</span>
        <span class="hero__trust-item">✓ Anfahrt inklusive</span>
        <span class="hero__trust-item">✓ Operator inklusive</span>
        <span class="hero__trust-item">✓ Branding ohne Aufpreis</span>
      </div>
    </div>
  </section>

  <section class="section" id="vorteile">
    <div class="section-header">
      <span class="tag">Warum ein Roboter?</span>
      <h2 class="section-title">Was Sie in<br />{city} gewinnen</h2>
    </div>
    <div class="tiles">
      <div class="tile">
        <div class="tile__top"><span class="tile__tag">Sichtbarkeit</span></div>
        <h3 class="tile__title">Menschen bleiben stehen</h3>
        <p class="tile__desc">Der G1 zieht Aufmerksamkeit aus mehreren Dutzend Metern Entfernung an. Ihr Stand oder Ihre Veranstaltung wird zum meistbesuchten Punkt im Raum.</p>
        <a href="#kontakt" class="tile__link">Angebot anfragen →</a>
      </div>
      <div class="tile tile--light">
        <div class="tile__top"><span class="tile__tag">Reichweite</span></div>
        <h3 class="tile__title">Organisches Social Media</h3>
        <p class="tile__desc">Fotos und Clips mit dem Roboter landen noch während der Veranstaltung in den sozialen Medien. Ihre Marke erscheint in hunderten Beiträgen — ohne Mediabudget.</p>
        <a href="#kontakt" class="tile__link">Angebot anfragen →</a>
      </div>
      <div class="tile">
        <div class="tile__top"><span class="tile__tag">Anfahrt</span></div>
        <h3 class="tile__title">Anfahrt inklusive</h3>
        <p class="tile__desc">Wir bringen den Roboter ohne Kilometeraufschlag nach {city}. Der genannte Preis ist der Endpreis — ohne Überraschungen.</p>
        <a href="#kontakt" class="tile__link">Angebot anfragen →</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="onas-body" style="max-width:860px; margin:0 auto;">
      <div class="onas-text">
        <h2 class="section-title" style="font-size:clamp(1.8rem,3vw,2.8rem); margin-bottom:var(--s4);">{city} — {c["claim"]}</h2>
        <p class="lead-text">{c["lead"]}</p>
        <p class="body-text">Die Miete eines humanoiden Roboters Unitree G1 in {city} ist der einfachste Weg, sich in einem dichten Veranstaltungsmarkt abzuheben. Wir liefern den G1 direkt an Ihre Location — ohne Anfahrtsaufschlag. Bedient werden {c["around"]}.</p>

        <h3 style="font-size:1.1rem; font-weight:700; letter-spacing:-0.01em; margin:var(--s6) 0 var(--s2); color:var(--text);">Bewährte Locations in {city}</h3>
        <ul class="body-text" style="margin:0 0 var(--s4); padding-left:1.2em; display:grid; gap:var(--s2);">
{venue_items}
        </ul>

        <h3 style="font-size:1.1rem; font-weight:700; letter-spacing:-0.01em; margin:var(--s6) 0 var(--s2); color:var(--text);">Anfahrt und Logistik</h3>
        <p class="body-text">Zu jeder Location in {city} fahren wir ohne Kilometeraufschlag. Der Roboter braucht vor Ort rund 2×2 m ebene Fläche und eine 230-V-Steckdose; wir bringen ihn selbst herein und sind in der Regel 30–45 Minuten vor Veranstaltungsbeginn einsatzbereit. Schreiben Sie uns, wo Ihre Veranstaltung in {city} stattfindet — Sie erhalten innerhalb von 24 Stunden ein konkretes Angebot.</p>

        <h3 style="font-size:1.1rem; font-weight:700; letter-spacing:-0.01em; margin:var(--s6) 0 var(--s2); color:var(--text);">Warum 33bots?</h3>
        <p class="body-text">Wir sind auf die Vermietung humanoider Roboter spezialisiert — das ist unser einziges Geschäft. Eigene Technik, zertifizierter Operator und deutschlandweit inklusive Anfahrt, natürlich auch nach {city}. Ein kompletter Veranstaltungstag kostet {PRICE_RANGE}, ab zwei Tagen mit 15 % Rabatt pro Tag.</p>
        <a href="#kontakt" class="btn-primary" style="margin-top:var(--s5); display:inline-flex;">Angebot anfordern →</a>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:0;">
    <div style="max-width:860px; margin:0 auto;">
      <div style="padding:var(--s5) var(--s6); background:var(--surface-2); border:1px solid var(--border-mid); border-radius:12px; display:flex; align-items:center; justify-content:space-between; gap:var(--s4); flex-wrap:wrap;">
        <p style="color:var(--text-2); font-size:0.9rem; margin:0;">Unsere Angebote: <strong style="color:var(--text);">Roboter für Messen</strong> und <strong style="color:var(--text);">Roboter für Konferenzen &amp; Galas</strong></p>
        <div style="display:flex; gap:var(--s3); flex-wrap:wrap;">
          <a href="messen.html" style="color:var(--text); font-size:0.85rem; font-weight:600; text-decoration:underline; text-underline-offset:3px; white-space:nowrap;">Messen →</a>
          <a href="konferenzen.html" style="color:var(--text); font-size:0.85rem; font-weight:600; text-decoration:underline; text-underline-offset:3px; white-space:nowrap;">Konferenzen →</a>
          <a href="tag-der-offenen-tuer.html" style="color:var(--text); font-size:0.85rem; font-weight:600; text-decoration:underline; text-underline-offset:3px; white-space:nowrap;">Tag der offenen Tür →</a>
        </div>
      </div>
    </div>
  </section>

{video_section(f"Humanoider Roboter Unitree G1 im Einsatz — Miete in {city}",
               f'So sieht der <strong style="color:var(--text);">Unitree G1</strong> live aus — er läuft, '
               f'gestikuliert und tanzt. Genau diese Show können Sie bei Ihrer Veranstaltung in {city} haben, '
               f'mit dem Branding Ihrer Marke auf der Brustplatte.')}

  <section class="section" style="padding-top:0;">
    <div style="max-width:860px; margin:0 auto;">
      <p style="font-size:0.75rem; color:var(--text-3); text-transform:uppercase; letter-spacing:0.1em; font-weight:700; margin-bottom:var(--s3);">Erprobt bei großen Veranstaltungen</p>
      <div style="display:flex; flex-wrap:wrap; gap:var(--s3);">
        <span style="color:var(--text); font-size:0.85rem; font-weight:600; padding:8px 16px; background:var(--surface-2); border:1px solid var(--border-mid); border-radius:10px;">WallStreet 30 · 2 253 Teilnehmende</span>
        <span style="color:var(--text); font-size:0.85rem; font-weight:600; padding:8px 16px; background:var(--surface-2); border:1px solid var(--border-mid); border-radius:10px;">Women in Tech Summit · ~14 000</span>
        <span style="color:var(--text); font-size:0.85rem; font-weight:600; padding:8px 16px; background:var(--surface-2); border:1px solid var(--border-mid); border-radius:10px;">LEX AI · TV-Beitrag</span>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:0;">
    <div style="max-width:860px; margin:0 auto;">
      <p style="font-size:0.75rem; color:var(--text-3); text-transform:uppercase; letter-spacing:0.1em; font-weight:700; margin-bottom:var(--s3);">Roboter mieten in anderen Städten</p>
      <div style="display:flex; flex-wrap:wrap; gap:var(--s2);">
{city_links_block(slug)}
      </div>
    </div>
  </section>

{faq_html(faq_all, f"Häufige Fragen<br />— {city}")}

  <section class="section contact-section" id="kontakt">
    <div class="contact-layout">
      <div class="contact-left">
        <span class="tag">Kontakt</span>
        <h2 class="section-title">Roboter in {city}<br />reservieren.</h2>
        <p class="body-text">Schreiben Sie uns — Sie erhalten innerhalb eines Werktags ein Angebot inklusive Verfügbarkeit.</p>
        <div class="contact-details">
          <a href="mailto:{EMAIL}" class="contact-detail">
            <span class="contact-detail__label">E-Mail</span>
            <span class="contact-detail__val">{EMAIL}</span>
          </a>
          <a href="tel:{PHONE_RAW}" class="contact-detail">
            <span class="contact-detail__label">Telefon</span>
            <span class="contact-detail__val">{PHONE_HUMAN}</span>
          </a>
          <a href="tel:{PHONE2_RAW}" class="contact-detail">
            <span class="contact-detail__label">Telefon</span>
            <span class="contact-detail__val">{PHONE2_HUMAN}</span>
          </a>
          <div class="contact-detail">
            <span class="contact-detail__label">Einsatzgebiet</span>
            <span class="contact-detail__val">{city} und Umgebung</span>
          </div>
        </div>
      </div>
      <div class="contact-right">
{contact_form(f"z. B. {city}, {c["venues"][0][0]}")}
      </div>
    </div>
  </section>

{footer()}"""


# ── 404 / robots / sitemap / _redirects ───────────────────────────────
def build_404():
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Seite nicht gefunden — 33bots</title>
  <meta name="robots" content="noindex, follow" />
{head_assets()}
</head>
<body>
{nav()}
  <section class="hero">
    <div class="hero__content" style="max-width:720px; padding-top:var(--s12);">
      <p class="hero__eyebrow">Fehler 404</p>
      <h1 class="hero__title">Diese Seite<br />gibt es nicht.</h1>
      <p class="hero__sub">Der Link ist veraltet oder enthält einen Tippfehler. Zurück zur Startseite — oder direkt zum Angebot.</p>
      <div class="hero__ctas">
        <a href="index.html" class="btn-cta">Zur Startseite →</a>
        <a href="roboter-mieten.html" class="btn-cta--ghost">Roboter mieten →</a>
      </div>
    </div>
  </section>
{footer()}"""


def build_robots():
    return f"""User-agent: *
Allow: /

Sitemap: {DOMAIN}/sitemap.xml
"""


def build_sitemap(pages):
    urls = []
    for path, prio in pages:
        loc = f"{DOMAIN}/{path}" if path else f"{DOMAIN}/"
        urls.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <priority>{prio}</priority>
  </url>""")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</urlset>\n")


def build_redirects():
    host = DOMAIN.replace("https://", "")
    return f"""https://www.{host}/* {DOMAIN}/:splat 301!
http://www.{host}/* {DOMAIN}/:splat 301!
http://{host}/* {DOMAIN}/:splat 301!
"""


def build_main_js():
    """main.js z serwisu PL, przetłumaczony na niemiecki."""
    src = open("main.js", encoding="utf-8").read()
    replacements = [
        ("'To pole jest wymagane'", "'Dieses Feld ist erforderlich'"),
        ("'Nieprawidłowy format'", "'Ungültiges Format'"),
        ("'Sprawdź to pole'", "'Bitte prüfen Sie dieses Feld'"),
        ("'Wysyłanie...'", "'Wird gesendet …'"),
        ("'Spróbuj ponownie'", "'Erneut versuchen'"),
        ("'Coś poszło nie tak. Napisz bezpośrednio na kontakt@33bots.pl'",
         f"'Etwas ist schiefgelaufen. Schreiben Sie uns direkt an {EMAIL}'"),
        ("'Formularz kontaktowy'", "'Kontaktformular'"),
        ("<h3>Wiadomość wysłana</h3>", "<h3>Nachricht gesendet</h3>"),
        ("<p>Odezwiemy się na <strong>${payload.email}</strong><br>w ciągu 24 godzin roboczych.</p>",
         "<p>Wir melden uns an <strong>${payload.email}</strong><br>innerhalb von 24 Werkstunden.</p>"),
    ]
    for old, new in replacements:
        if old not in src:
            raise SystemExit(f"main.js: nie znaleziono fragmentu do tłumaczenia: {old}")
        src = src.replace(old, new)
    return src


# ── Main ──────────────────────────────────────────────────────────────
def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, "video"), exist_ok=True)

    written = []

    def write(rel, content):
        path = os.path.join(OUT, rel)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        written.append(rel)

    # Strona główna
    write("index.html", build_index())

    # Podstrony ofertowe
    for fn, content in offer_pages().items():
        write(fn, content)

    # Miasta
    for c in CITIES:
        fn, content = build_city(c)
        write(fn, content)

    # 404 + pliki serwisowe
    write("404.html", build_404())
    write("robots.txt", build_robots())
    write("_redirects", build_redirects())
    write("main.js", build_main_js())

    sitemap_pages = [("", "1.0")]
    sitemap_pages += [(fn, "0.9") for fn, _ in OFFER_PAGES]
    sitemap_pages += [(f"roboter-mieten-{c['slug']}.html", "0.8") for c in CITIES]
    write("sitemap.xml", build_sitemap(sitemap_pages))

    # CSS 1:1 z serwisu PL (identyczna szata graficzna)
    shutil.copyfile("style.css", os.path.join(OUT, "style.css"))
    written.append("style.css")

    for asset in ASSETS:
        shutil.copyfile(asset, os.path.join(OUT, asset))
        written.append(asset)

    for asset in VIDEO_ASSETS:
        shutil.copyfile(os.path.join("video", asset), os.path.join(OUT, "video", asset))
        written.append(f"video/{asset}")

    print(f"Wygenerowano {len(written)} plików w katalogu {OUT}/")
    for w in written:
        print(f"  {w}")


if __name__ == "__main__":
    main()
