# -*- coding: utf-8 -*-
"""
Treści niemieckich podstron SEO — część 2: typy wydarzeń, eventy branżowe,
imprezy prywatne.

Lustro seo_pages_content2.py. Pierwszy argument buildera to slug PL — służy
jako klucz treści oraz jako seed, dzięki czemu warianty kafelków, scenariuszy
i wideo są identyczne jak na odpowiedniku polskim.

Kalendarz imprez prywatnych dopasowany do realiów niemieckich: w miejsce
imienin — Polterabend, w miejsce andrzejek — Oktoberfest.
"""

from de_content_helpers import ev, br, priv, DOG_PRICE, PRICE_RANGE

TEXT = {}


def _add(pages):
    for d in pages:
        TEXT[d["slug"]] = d


# ================================================= TYPY WYDARZEŃ (biznes)

EVENTS = [
    ev("robot-na-event", "Roboter für Events", "für Events", "Auf einem Event",
       sub="Eine Attraktion, die auf jeder Veranstaltung funktioniert: Der humanoide Roboter Unitree G1 begrüßt Gäste, tanzt, spricht dank KI und posiert für Fotos. Was immer Sie organisieren — der Roboter macht daraus ein Event, über das gesprochen wird.",
       uniq_tile=("Vielseitigkeit", "Funktioniert bei jeder Veranstaltung", "Messe, Gala, Sommerfest oder Premiere — das Showkonzept passen wir an Charakter und Agenda Ihres Events an. Ein Roboter, Dutzende erprobte Varianten."),
       uniq_scen=("Ein maßgeschneidertes Programm", "Vor der Veranstaltung legen wir gemeinsam den Plan fest: wann der Roboter auftritt, was er zeigt, mit wem er interagiert. Sie bekommen ein Drehbuch Minute für Minute — und die Gewissheit, dass alles sitzt."),
       faq_uniq=("Für welche Events wird der Roboter am häufigsten gebucht?", "Am häufigsten betreuen wir Messen, Konferenzen, Galas und Firmenfeiern, aber der Roboter bewährt sich ebenso auf Hochzeiten, Stadtfesten oder bei Eröffnungen. Wenn Sie eine ungewöhnliche Veranstaltung planen — schreiben Sie uns, uns fällt sicher etwas ein.")),

    ev("robot-na-targi", "Roboter für Messen", "für Messen", "Auf einer Messe",
       sub="Auf einer Messe haben Sie drei Sekunden, um einen Vorbeigehenden zu stoppen. Ein humanoider Roboter am Stand erledigt das für Sie — er baut eine Traube auf, sammelt Kontakte und sorgt dafür, dass die ganze Halle über Ihren Stand spricht.",
       uniq_tile=("Leads", "Eine Menge, die Kontakte hinterlässt", "Der Roboter zieht Besucher an, und Ihr Vertrieb spricht mit Menschen, die von selbst gekommen sind. Der Lead-Scanner kommt nicht hinterher — das beste Problem, das man auf einer Messe haben kann."),
       uniq_scen=("Arbeit am Stand", "Der Roboter arbeitet vor Ihrem Stand in Blöcken: Choreografie-Shows ziehen eine Welle von Besuchern an, dazwischen begrüßt der G1 Gäste und posiert für Fotos vor Ihrem Branding."),
       faq_uniq=("Passt der Roboter auf unseren Stand?", "Der G1 braucht nur wenige Quadratmeter freie Fläche. Wir arbeiten sowohl auf großen Inselständen als auch bei Reihenbebauung — die Anordnung legen wir anhand Ihres Standplans fest.")),

    ev("robot-na-konferencje", "Roboter für Konferenzen", "für Konferenzen", "Auf einer Konferenz",
       sub="Eine erinnerte Konferenz ist eine gelungene Konferenz. Der humanoide Roboter eröffnet die Veranstaltung, moderiert die Agenda mit oder tritt als Redner auf — und gibt den Teilnehmenden einen Grund, noch lange danach über Ihr Event zu sprechen.",
       uniq_tile=("Agenda", "Ein Programmpunkt, keine Dekoration", "Der Roboter kann die Konferenz eröffnen, Speaker ankündigen oder einen eigenen Vortrag mit Q&A halten. Das ist ein vollwertiger Agendapunkt, der den Rang der gesamten Veranstaltung hebt."),
       uniq_scen=("Eröffnung der Konferenz", "Der Roboter betritt aus eigener Kraft die Bühne und begrüßt die Teilnehmenden — eine Eröffnung, nach der der Saal bis zum letzten Slot voll bleibt."),
       faq_uniq=("Kann der Roboter als Redner auftreten?", "Ja — der G1 kann einen gemeinsam vorbereiteten Vortrag halten und dank KI Fragen aus dem Saal beantworten. Sehen Sie sich dazu unsere Seite zum Roboter als Redner an.")),

    ev("robot-na-konferencje-technologiczna", "Roboter für Tech-Konferenzen", "für Tech-Konferenzen", "Auf einer Tech-Konferenz",
       sub="Ein technisches Publikum hat schon alles gesehen — außer einem laufenden Humanoiden live. Ein Roboter auf der Tech-Konferenz ist das thematisch stimmige Highlight, das selbst das anspruchsvollste Publikum in filmende Fans verwandelt.",
       uniq_tile=("Substanz", "Technologie, kein Gadget", "Für ein Tech-Publikum ist der Roboter nicht nur Show — er ist eine Demonstration des Stands von Robotik und KI. Die Vorführung lässt sich mit einer Erläuterung zu Lokomotion und Sprachmodell-Integration verbinden."),
       uniq_scen=("Demo auf der Hauptbühne", "Eine Demonstration der G1-Fähigkeiten mit technischem Kommentar: zweibeinige Lokomotion, Balance, KI. Das Ingenieurspublikum schätzt die Details — und filmt alles mit."),
       faq_uniq=("Kann die Show einen technischen Charakter haben?", "Ja — für Technologieveranstaltungen bereiten wir eine Variante mit fachlichem Kommentar zu Robotik und KI vor, abgestimmt auf das Niveau des Publikums.")),

    ev("robot-na-gale", "Roboter für Galas", "für Galas", "Auf einer Gala",
       sub="Eine Gala ist ein Abend, der in Erinnerung bleiben soll. Der humanoide Roboter in eleganter Ausführung: Er begrüßt Gäste auf dem roten Teppich, überreicht Trophäen und führt die Abschlussshow. Klasse trifft Zukunft.",
       uniq_tile=("Zeremonie", "Er überreicht Preise und Auszeichnungen", "Eine Trophäe, die von einem Roboter überreicht wird, behält jeder Preisträger — und jeder Fotograf hält sie fest. Die Zeremonie gewinnt eine Dramaturgie, von der Bühnenbildner nur träumen."),
       uniq_scen=("Roter Teppich", "Der Roboter begrüßt die Gäste am Eingang zur Gala — ein eleganter Empfang, bei dem jeder für ein Foto stehen bleibt, bevor er den Saal betritt."),
       faq_uniq=("Kann der Roboter auf der Gala Preise überreichen?", "Ja — der G1 kann Trophäen reichen, Preisträger auf die Bühne bitten und die Zeremonie begleiten. Das ist eines der wirkungsvollsten Gala-Szenarien.")),

    ev("robot-na-bankiet", "Roboter für Bankette", "für Bankette", "Auf einem Bankett",
       sub="Ein Bankett hat eigene Gesetze: elegante Gespräche, Networking, das Glas in der Hand. Der humanoide Roboter zieht seine Kreise durch die Gäste — als Thema, das das Eis besser bricht als jeder Small Talk.",
       uniq_tile=("Networking", "Der beste Eisbrecher des Abends", "Am Roboter beginnen Fremde ganz natürlich miteinander zu sprechen — gemeinsames Staunen ist der schnellste Weg zum Kontakt. Networking passiert von selbst."),
       uniq_scen=("Unterwegs zwischen den Gästen", "Der Roboter geht in Begleitung des Operators zwischen Tischen und Bereichen umher — er begrüßt, gestikuliert, posiert. Wo immer er auftaucht, entsteht ein Gespräch."),
       faq_uniq=("Passt der Roboter zum eleganten Charakter eines Banketts?", "Ja — wir führen die Show in einem zurückhaltenden, eleganten Stil: ruhige Interaktionen, diskrete Präsenz des Operators und Showmomente genau dort, wo der Gastgeber sie wünscht.")),

    ev("robot-na-impreze-firmowa", "Roboter für Firmenfeiern", "für Firmenfeiern", "Auf einer Firmenfeier",
       sub="Eine Firmenfeier, zu der die Mitarbeitenden wirklich kommen wollen? Der humanoide Roboter erledigt Teilnahme, Teamgefühl und Content für die Firmenkanäle mit einer einzigen Show. Und die Personalabteilung sammelt die Komplimente ein.",
       uniq_tile=("Teamgefühl", "Ein gemeinsames Thema für alle Abteilungen", "Buchhaltung, IT und Vertrieb — am Roboter stehen alle in derselben Traube und lachen über dieselben Momente. So sieht Teambuilding ohne Zwang aus."),
       uniq_scen=("Der Höhepunkt des Abends", "Die Tanzshow mitten in der Feier setzt die Energie zurück und gibt dem Abend einen Moment, auf den in den Montagsgesprächen alle zurückkommen."),
       faq_uniq=("Passt der Roboter sowohl zur eleganten Gala als auch zur lockeren Feier?", "Ja — den Charakter der Show passen wir an: vom eleganten Galaprogramm bis zur energiegeladenen Show mit Tanz-Battle auf der lockeren Teamfeier.")),

    ev("roboty-na-eventy-firmowe", "Roboter für Firmenevents", "für Firmenevents", "Auf einem Firmenevent",
       sub="Vom Familienfest bis zur Vorstandsgala: Humanoide Roboter bedienen das komplette Spektrum betrieblicher Veranstaltungen. Ein erprobter Eventpartner, der den WOW-Effekt immer liefert — und dazu Material für die interne Kommunikation.",
       uniq_tile=("Kalender", "Ein Partner fürs ganze Eventjahr", "Weihnachtsfeier, Kick-off, Sommerfest, Jubiläum — bei laufender Zusammenarbeit tritt der Roboter auf den Veranstaltungen Ihres Unternehmens in immer neuen Rollen auf. Die Mitarbeitenden warten darauf, was wir uns diesmal ausdenken."),
       uniq_scen=("Ein Format für jeden Anlass", "Für jede Veranstaltung im Jahr wählen wir eine andere Rolle: Empfang beim Kick-off, Tanzshow beim Sommerfest, Preisübergabe beim Jubiläum. Dieselbe Attraktion, jedes Mal neu."),
       faq_uniq=("Arbeiten Sie auch dauerhaft mit Unternehmen zusammen?", "Ja — bei mehreren Veranstaltungen im Jahr erstellen wir ein Rahmenangebot mit festen Konditionen und reservierten Terminen für Ihren gesamten Eventkalender.")),

    ev("robot-na-integracje-firmowa", "Roboter für Teamevents", "für Teamevents", "Auf einem Teamevent",
       sub="Statt noch einer Runde Paintball — die Begegnung mit einem echten Roboter. Auf dem Teamevent gibt der G1 der Mannschaft ein gemeinsames Erlebnis, ein Tanz-Battle und Hunderte Fotos, die monatelang durch die Firmenchats wandern.",
       uniq_tile=("Team", "Ein Erlebnis, das verbindet", "Gemeinsames Staunen verbindet schneller als erzwungene Teamspiele. Der Roboter gibt allen — vom Praktikanten bis zur Geschäftsführung — denselben Grund zu lachen."),
       uniq_scen=("Tanz-Battle der Abteilungen", "Die Abteilungen schicken ihre Vertreter in ein Tanzduell mit dem Roboter — Anfeuerung, Gelächter und Aufnahmen, die das ganze Unternehmen sieht."),
       faq_uniq=("Funktioniert der Roboter auch bei einem Teamevent im Freien?", "Ja — bei trockenem Wetter und einigermaßen ebenem Untergrund arbeitet der Roboter draußen hervorragend. Für den Regenfall vereinbaren wir eine überdachte Variante.")),

    ev("robot-na-piknik-firmowy", "Roboter für Betriebsfeste", "für Betriebsfeste", "Auf einem Betriebsfest",
       sub="Ein Betriebsfest ist ein Event für Mitarbeitende und ihre Familien — und der humanoide Roboter ist die einzige Attraktion, die auf eine Fünfjährige genauso stark wirkt wie auf die Geschäftsführung. Shows, gemeinsames Tanzen und High Fives über den ganzen Nachmittag.",
       uniq_tile=("Familien", "Der Hit bei den Kindern der Belegschaft", "Die Kinder kommen mit der Geschichte vom echten Roboter nach Hause — und die Mitarbeitenden mit dem Gefühl, dass ihr Unternehmen etwas wirklich Besonderes organisiert hat. So entsteht Bindung."),
       uniq_scen=("Showblöcke über das ganze Fest", "Der Roboter arbeitet im Rhythmus des Fests: Shows im Stundentakt, dazwischen Foto- und Interaktionsbereich. Jede Familie findet ihren Moment mit dem Roboter."),
       faq_uniq=("Kann der Roboter auf Rasen auftreten?", "Der Roboter arbeitet am besten auf befestigtem, ebenem Untergrund — bei Festen legen wir die Showfläche auf ein Podest, Pflaster oder eine Platte. Wir beraten Sie, wie sich das organisieren lässt.")),

    ev("robot-na-team-building", "Roboter fürs Teambuilding", "fürs Teambuilding", "Beim Teambuilding",
       sub="Teambuilding mit einem humanoiden Roboter ist kein Workshop am Flipchart. Das Team entdeckt gemeinsam die Fähigkeiten des G1, misst sich in Challenges mit dem Roboter und geht mit einem Erlebnis nach Hause, das wirklich zusammenschweißt.",
       uniq_tile=("Aktivität", "Team-Challenges mit dem Roboter", "Tanzwettbewerbe, KI-Quiz, Reaktionsspiele — das Teambuilding-Programm bauen wir rund um Interaktionen mit dem Roboter, bei denen Zusammenarbeit zählt und nicht Einzelleistung."),
       uniq_scen=("Workshop mit Zukunft", "Den Showteil verbinden wir mit einem Gespräch über KI und Robotik in der Arbeitswelt — das Team hat nicht nur Spaß, sondern fasst die Technologie an, über die alle diskutieren."),
       faq_uniq=("Für wie große Gruppen ist das Teambuilding geeignet?", "Von kleinen Teams mit einem Dutzend Personen bis zu ganzen Bereichen mit mehreren Hundert — das Programm skalieren wir auf Gruppengröße und Fläche.")),

    ev("robot-na-szkolenie", "Roboter für Schulungen", "für Schulungen", "Bei einer Schulung",
       sub="Der schwierigste Moment jeder Schulung? Die Aufmerksamkeit nach dem Mittagessen. Ein humanoider Roboter als Unterbrecher oder Leitmotiv der Schulung hebt die Energie im Raum — und sorgt dafür, dass die Botschaft hängen bleibt.",
       uniq_tile=("Aufmerksamkeit", "Die Energie im Raum unter Kontrolle", "Eine kurze Roboter-Show zwischen den Schulungsblöcken wirkt wie ein Neustart — die Teilnehmenden kehren mit frischer Energie und positiver Haltung zum Inhalt zurück."),
       uniq_scen=("Modul zu KI und der Zukunft der Arbeit", "Bei Schulungen zur digitalen Transformation wird der Roboter zur lebenden Fallstudie — die Teilnehmenden sprechen mit der KI, statt Folien über sie anzusehen."),
       faq_uniq=("Passt der Roboter zu einem ernsten Schulungsthema?", "Ja — die Präsenz des Roboters dosieren wir so, dass sie das Programm unterstützt und nicht ablenkt. Vom kurzen Akzent zur Eröffnung bis zum vollen interaktiven Modul.")),

    ev("robot-na-rocznice-firmy", "Roboter für Firmenjubiläen", "für Firmenjubiläen", "Auf einem Firmenjubiläum",
       sub="Ein Firmenjubiläum blickt in zwei Richtungen: auf das Erreichte und auf die Zukunft. Der humanoide Roboter verbindet beides symbolisch — und beschert den Gästen nebenbei einen Abend, von dem sie beim nächsten Jubiläum erzählen werden.",
       uniq_tile=("Symbol", "Zukunft beim Geburtstag des Unternehmens", "Ein Humanoid beim Jubiläum ist eine klare Botschaft an Mitarbeitende und Partner: Dieses Unternehmen feiert nicht die Vergangenheit — es baut das nächste Jahrzehnt."),
       uniq_scen=("Toast und Torte mit dem Roboter", "Der Roboter kann den Toast auf das Unternehmen ausbringen, die Jubiläumstorte enthüllen oder verdiente Mitarbeitende auszeichnen — die Zeremonie bekommt einen Moment, der zur Firmenlegende wird."),
       faq_uniq=("Kann der Roboter auf die Geschichte unseres Unternehmens eingehen?", "Ja — dank KI kann der Roboter von den Meilensteinen des Unternehmens erzählen, Anekdoten aufgreifen und Erinnerungen wecken. Die Inhalte bereiten wir gemeinsam vor der Veranstaltung vor.")),

    ev("robot-na-premiere-produktu", "Roboter für Produktlaunches", "für Produktlaunches", "Bei einem Produktlaunch",
       sub="Eine Produktpremiere braucht den Moment, in dem der Saal den Atem anhält. Der humanoide Roboter enthüllt die Neuheit, präsentiert sie und posiert mit ihr für Fotos — und die Medien bekommen das Bild, das sie veröffentlichen wollen.",
       uniq_tile=("Enthüllung", "Der Premierenmoment mit Dramaturgie", "Der Roboter zieht das Tuch weg, trägt das Produkt auf die Bühne oder startet es zum ersten Mal öffentlich. Die Fotografen haben ihr Bild, die Journalisten ihren Aufhänger."),
       uniq_scen=("Präsentation der Neuheit", "Nach der Enthüllung präsentiert der Roboter die wichtigsten Eigenschaften des Produkts — mit vorbereitetem Skript und Gestik — und beantwortet dank KI Fragen."),
       faq_uniq=("Kann der Roboter unser Produkt halten und präsentieren?", "Je nach Größe — der G1 kann leichtere Gegenstände halten, auf das Produkt zeigen und damit posieren. Die Details klären wir, sobald wir das Produkt kennen.")),

    ev("robot-na-otwarcie", "Roboter für Eröffnungen", "für Eröffnungen", "Bei einer Eröffnung",
       sub="Die Eröffnung eines Geschäfts, Büros, Showrooms oder Restaurants hat ein Ziel: Die Umgebung soll es sofort erfahren. Der humanoide Roboter durchschneidet das Band, begrüßt die ersten Gäste und sorgt dafür, dass der Eröffnungstag in die Lokalmedien kommt.",
       uniq_tile=("Aufmerksamkeit", "Die Lokalmedien kommen von selbst", "Eine Eröffnung mit Roboter ist ein fertiges Thema für lokale Portale und Fernsehsender — und jeder Passant mit Handy wird zu Ihrem Werbekanal."),
       uniq_scen=("Eröffnungszeremonie", "Der Roboter ist beim Banddurchschnitt dabei, begrüßt die ersten Kunden und führt vor dem Eingang die Show durch — ein stärkeres Signal für einen neuen Ort in der Nachbarschaft gibt es kaum."),
       faq_uniq=("Wie früh sollte man den Roboter für eine Eröffnung planen?", "Den Eröffnungstermin kennt man meist im Voraus — reservieren Sie den Roboter 3–4 Wochen vorher, dann helfen wir auch bei der Kommunikation, die die Attraktion ankündigt.")),

    ev("robot-na-dzien-otwarty", "Roboter für Tage der offenen Tür", "für Tage der offenen Tür", "Beim Tag der offenen Tür",
       sub="Ein Tag der offenen Tür soll dafür sorgen, dass Menschen kommen — und mit einem guten Eindruck gehen. Der humanoide Roboter erledigt beides: Er zieht Besucher mit der Ankündigung an und macht vor Ort aus dem Rundgang eine Veranstaltung.",
       uniq_tile=("Besucherzahl", "Eine Ankündigung, die Menschen anzieht", "Die Information über eine Roboter-Show in der Vorab-Kommunikation hebt die Besucherzahl spürbar — die Leute kommen wegen des Roboters und bleiben wegen Ihres Angebots."),
       uniq_scen=("Führer durch das Gelände", "Der Roboter begrüßt die Besucher und lädt in die nächsten Bereiche ein — der Rundgang durch Showroom oder Werk bekommt Erzählung und Rhythmus."),
       faq_uniq=("Kann der Roboter über unser Angebot sprechen?", "Ja — wir statten die KI mit Wissen über Ihr Unternehmen aus, und der Roboter beantwortet Besucherfragen zu Produkten, Leistungen oder offenen Stellen.")),

    ev("robot-na-targi-pracy", "Roboter für Karrieremessen", "für Karrieremessen", "Auf einer Karrieremesse",
       sub="Auf einer Karrieremesse sagen alle Recruiter dasselbe. Ein humanoider Roboter an Ihrem Stand spricht für Sie — und zwar so, dass sich die Kandidatinnen und Kandidaten von selbst anstellen, um über eine Stelle bei Ihnen zu sprechen.",
       uniq_tile=("Kandidaten", "Die Bewerbungen kommen von selbst", "Die Frequenz an einem Stand mit Roboter ist um ein Vielfaches höher als bei den Nachbarn — die Recruiter sprechen mit Menschen, die aus Neugier kamen und aus Interesse blieben."),
       uniq_scen=("Der Roboter im Recruiting-Team", "Der G1 begrüßt Kandidaten, erzählt dank KI vom Unternehmen und lädt zum Gespräch mit dem Recruiter ein — ein erster Markenkontakt, den kein Roll-up liefert."),
       faq_uniq=("Was kann der Roboter den Kandidaten erzählen?", "Alles, was wir festlegen: über Unternehmenskultur, Benefits, offene Stellen und den Bewerbungsprozess. Die Inhalte bereiten wir gemeinsam mit Ihrem HR-Team vor.")),

    ev("robot-na-roadshow", "Roboter für Roadshows", "für Roadshows", "Auf einer Roadshow",
       sub="Eine Roadshow lebt vom wiederholbaren Effekt in jeder Stadt der Route. Der humanoide Roboter ist die Attraktion, die in Hamburg genauso stark wirkt wie in München — und die Logistik übernehmen wir.",
       uniq_tile=("Route", "Ganz Deutschland in einem Projekt", "Wir planen die Präsenz des Roboters auf der gesamten Route: Termine, Transport, dasselbe Team und derselbe Showstandard in jeder Stadt. Sie haben einen Ansprechpartner und null Überraschungen."),
       uniq_scen=("Dasselbe Drehbuch, neue Stadt", "An jedem Standort spielt der Roboter das erprobte Programm: Shows, Interaktionen, Fotobereich mit Branding. Eine Konsistenz, die jeder Brand Manager zu schätzen weiß."),
       faq_uniq=("Wie wird eine Tour durch mehrere Städte abgerechnet?", "Für Roadshows erstellen wir ein Paketangebot für die gesamte Route — günstiger als die Summe der Einzeleinsätze. Schreiben Sie uns mit der geplanten Städteliste.")),

    ev("robot-na-wystawe", "Roboter für Ausstellungen", "für Ausstellungen", "Auf einer Ausstellung",
       sub="Eine Ausstellung zieht Besucher mit ihren Exponaten an — aber das Exponat, das läuft und spricht, sammelt die größten Trauben. Ein humanoider Roboter in der Ausstellung ist eine lebende Installation, die keine Vitrine braucht.",
       uniq_tile=("Exposition", "Ein Exponat, das Fragen beantwortet", "Die Besucher können mit dem Roboter sprechen — über die Ausstellung, über Technologie, über alles. Kein anderes Exponat bietet dieses Erlebnis."),
       uniq_scen=("Lebende Installation", "Der Roboter arbeitet in einem festgelegten Ausstellungsbereich in Showblöcken — die Besucher planen ihren Besuch nach seinen Auftrittszeiten."),
       faq_uniq=("Kann der Roboter über mehrere Tage Teil der Ausstellung sein?", "Ja — wir realisieren einzelne Tage ebenso wie längere Präsenzen mit einem festgelegten Zeitplan der Showblöcke.")),

    ev("robot-na-expo", "Roboter für Expos", "für Expos", "Auf einer Expo",
       sub="Auf großen Expo-Veranstaltungen konkurrieren Sie mit Hunderten Ausstellern um Aufmerksamkeit. Ein humanoider Roboter ist der kürzeste Weg dahin, dass Ihre Fläche zu dem Punkt wird, auf den alle Besucher zusteuern.",
       uniq_tile=("Maßstab", "Sichtbarkeit in der großen Halle", "Auf einer Expo gewinnt, über wen in den Gängen gesprochen wird. Ein laufender Humanoid erzeugt genau den Buzz, der Besucher direkt zu Ihrer Fläche führt."),
       uniq_scen=("Magnet für Besucher", "Der Roboter arbeitet an Ihrer Fläche in wiederkehrenden Blöcken — jede Show erzeugt eine Besucherwelle, die Ihr Team abarbeitet."),
       faq_uniq=("Betreuen Sie auch internationale Veranstaltungen?", "Ja — der Roboter führt Interaktionen auch auf Englisch, was auf internationalen Expos ein großer Vorteil ist.")),

    ev("robot-na-konwent", "Roboter für Conventions", "für Conventions", "Auf einer Convention",
       sub="Eine Convention — ob Branche, Franchise oder Fan-Community — braucht Momente, die die Teilnehmenden verbinden. Der humanoide Roboter schenkt Hunderten Menschen gleichzeitig ein gemeinsames Erlebnis und wird zum inoffiziellen Symbol des ganzen Treffens.",
       uniq_tile=("Treffen", "Das Thema Nummer eins in den Gängen", "Von der Registrierung bis zum Bankett — der Roboter zieht sich durch die gesamte Convention und wird zum gemeinsamen Bezugspunkt aller Teilnehmenden."),
       uniq_scen=("Präsenz über die ganze Convention", "Der Roboter taucht in den Schlüsselmomenten auf: Eröffnung, Networking-Pausen, Abendgala. Die Teilnehmenden suchen ihn zwischen den Agendapunkten."),
       faq_uniq=("Funktioniert der Roboter auch auf einer Fan-Convention?", "Auf jeden Fall — ein popkulturaffines Publikum reagiert auf einen Humanoiden begeistert. Der Roboter kann dabei auf das Leitthema der Convention Bezug nehmen.")),

    ev("robot-na-festiwal", "Roboter für Festivals", "für Festivals", "Auf einem Festival",
       sub="Ein Festival sind Tausende Menschen auf der Suche nach Erlebnissen. Ein humanoider Roboter in der Festivalzone zieht zwischen den Konzerten Menschenmengen an und gibt Sponsoren eine Aktivierung, die das Publikum wirklich mag.",
       uniq_tile=("Zone", "Eine Aktivierung, die nicht nervt", "Festivalbesucher machen einen Bogen um aufdringliche Stände — aber zum Roboter stellen sie sich von selbst an. Das ist eine Sponsoring-Aktivierung, an die man sich gern erinnert."),
       uniq_scen=("Roboterzone zwischen den Bühnen", "In den Pausen zwischen den Auftritten führt der Roboter Shows und Interaktionen durch — er füllt genau die Zeit, in der die Besucher nach Attraktionen suchen."),
       faq_uniq=("Arbeitet der Roboter auch auf Open-Air-Festivals?", "Ja — bei überdachter Zone oder gutem Wetter arbeitet der Roboter draußen hervorragend. Wir brauchen einen ebenen Untergrund; die Details stehen im Rider.")),

    ev("robot-na-dni-miasta", "Roboter für Stadtfeste", "für Stadtfeste", "Auf einem Stadtfest",
       sub="Ein Stadtfest bringt ganze Familien zusammen — und für die ist der humanoide Roboter die Attraktion Nummer eins. Bühnenshows, Spaziergänge zwischen den Bürgerinnen und Bürgern und Menschentrauben am Fotobereich: Die Stadt wird bis zum nächsten Jahr darüber sprechen.",
       uniq_tile=("Bürgerinnen und Bürger", "Eine Attraktion für jede Generation", "Von Kita-Kindern bis zu Seniorinnen — der Roboter wirkt auf alle gleichermaßen. Das ist im Programm städtischer Veranstaltungen eine Seltenheit."),
       uniq_scen=("Shows auf der Stadtbühne", "Die Auftritte des Roboters flechten wir in das Bühnenprogramm des Stadtfests ein — zwischen Konzerten und Wettbewerben, mit Ansage durch die Moderation."),
       faq_uniq=("Arbeiten Sie mit Kommunen zusammen?", "Ja — wir betreuen städtische und kommunale Veranstaltungen, stellen Rechnungen für öffentliche Auftraggeber und richten uns nach den Vorgaben des Vergabeverfahrens.")),

    ev("robot-na-wystep-sceniczny", "Roboter für Bühnenshows", "für Bühnenshows", "Bei einer Bühnenshow",
       sub="Die Bühne ist die natürliche Umgebung des G1. Der Bühnenauftritt des Roboters — solo oder im Duett mit Künstlerin, Tänzer oder Moderation — ist ein mehrminütiges Spektakel, nach dem das Publikum aufsteht.",
       uniq_tile=("Spektakel", "Regie und Licht", "Wir arbeiten mit Licht- und Tontechnik zusammen, damit der Auftritt des Roboters eine vollwertige Bühnennummer wird — mit Dramaturgie, nicht nur mit Neuheitseffekt."),
       uniq_scen=("Duett mit einem Künstler", "Der Roboter tritt mit Sängerin, Tänzer oder Magier auf — der Kontrast von Mensch und Maschine auf der Bühne ergibt ein Spektakel, das das Publikum ab der ersten Sekunde filmt."),
       faq_uniq=("Was braucht der Roboter auf der Bühne?", "Eine ebene, stabile Bühne, ein paar Meter Fläche und einen Moment für die technische Probe. Den vollständigen technischen Rider senden wir nach der Terminreservierung.")),

    ev("robot-na-ceremonie", "Roboter für Zeremonien", "für Zeremonien", "Bei einer Zeremonie",
       sub="Grundsteinlegung, Stapellauf, Zertifikatsübergabe, Festakt zum Jubiläum — jede Zeremonie gewinnt an Rang, wenn ein humanoider Roboter daran teilnimmt. Würde und Zukunft in einem Bild.",
       uniq_tile=("Rang", "Eine Zeremonie, die man behält", "Die Teilnahme des Roboters hebt den Rang des Festakts und zieht Medien an — der zeremonielle Moment bekommt eine Inszenierung, die sich nicht kopieren lässt."),
       uniq_scen=("Teil des Rituals", "Der Roboter kann überreichen, enthüllen, durchschneiden und reichen — jede Geste der Zeremonie proben wir vorher, damit sie perfekt abläuft."),
       faq_uniq=("Wahrt der Roboter die Würde des Festakts?", "Ja — das Drehbuch der Zeremonie führen wir in dem Ton, den der Anlass verlangt. Der Roboter kann spektakulär sein, ohne die Würde der Veranstaltung zu verletzen.")),
]

# ============================================================== BRANŻE

BRANCHEN = [
    br("it", "IT-Event", "für IT-Events", "Auf einem IT-Event",
       "Entwickler, Ingenieurinnen und CTOs",
       "Ein IT-Publikum schätzt den Roboter doppelt: als großartige Show und als reales Demo zum Stand von Robotik und KI — inklusive Fragen zum Technologie-Stack.",
       ("Interessiert der Roboter auch erfahrene Ingenieure?", "Ja — gerade das technische Publikum stellt die spannendsten Fragen und bleibt am längsten beim Roboter. Auf Wunsch führt ein Operator die Show, der für ein technisches Q&A bereit ist.")),

    br("gamingowy", "Gaming-Event", "für Gaming-Events", "Auf einem Gaming-Event",
       "Gamer, Streamer und Creator",
       "Die Gaming-Community lebt von Content — und ein humanoider Roboter ist fertiges Material für Clips, Streams und Shorts. Der G1 kann in Motiven auftreten, die an Games und E-Sport anknüpfen.",
       ("Kann der Roboter im Stream auftreten?", "Ja — der Roboter macht sich live in Übertragungen hervorragend. Gern stimmen wir seine Präsenz auf den Zeitplan der Streams und Creator-Aktivitäten Ihres Events ab.")),

    br("korporacyjny", "Corporate Event", "für Corporate Events", "Auf einem Corporate Event",
       "Mitarbeitende, Geschäftsführung und Geschäftspartner",
       "Im Konzernkalender findet der Roboter überall seinen Platz: vom Townhall über den Vertriebs-Kick-off bis zum Treffen mit Schlüsselkunden — immer im Ton, der dem Rang des Termins entspricht.",
       ("Lässt sich die Show an unsere Corporate Guidelines anpassen?", "Ja — wir arbeiten mit Brand Books, Compliance-Abteilungen und minutengenauen Agenden. Das Drehbuch geben Sie vor der Veranstaltung frei.")),

    br("medyczny", "Medizin-Event", "für Medizin-Events", "Auf einem Medizin-Event",
       "Ärztinnen, Apotheker und Gesundheitsmanagement",
       "Medizinkongresse sprechen über die Zukunft der Behandlung — ein humanoider Roboter macht diese Zukunft greifbar und eröffnet Gespräche über Technologie in der Medizin besser als so mancher Vortrag.",
       ("Passt der Roboter zur Ernsthaftigkeit einer Medizinveranstaltung?", "Ja — bei medizinischen Veranstaltungen führen wir die Show in zurückhaltendem, professionellem Ton, mit Fokus auf Technologie und ihre Anwendungen statt auf Unterhaltung.")),

    br("farmaceutyczny", "Pharma-Event", "für Pharma-Events", "Auf einem Pharma-Event",
       "Vertreterinnen und Vertreter der Pharmabranche",
       "Wiederkehrende Pharmatagungen und -kongresse ähneln einander oft — ein humanoider Roboter hebt Ihre Veranstaltung heraus und gibt den Teilnehmenden ein Thema, das bis zur nächsten Ausgabe hält.",
       ("Kann der Roboter die wissenschaftliche Botschaft der Veranstaltung unterstützen?", "Ja — die Inhalte, die der Roboter dank KI vermittelt, bereiten wir gemeinsam mit dem Veranstalter vor, auch auf Basis der fachlichen Unterlagen der Veranstaltung.")),

    br("finansowy", "Finanz-Event", "für Finanz-Events", "Auf einem Finanz-Event",
       "Bankerinnen, Investoren und Fintech-Vertreter",
       "Die Finanzbranche spricht auf jeder Konferenz über KI — der humanoide Roboter erlaubt den Gästen, dieser KI buchstäblich die Hand zu geben. Ein starker Akzent auf Bilanzgalas und Fintech-Kongressen.",
       ("Funktioniert der Roboter auf einer eleganten Finanzveranstaltung?", "Ja — vom Empfang der Gäste im VIP-Bereich bis zum Vortrag über die Zukunft der Finanzen: Das Drehbuch halten wir im Premium-Ton, passend zur Seriosität der Branche.")),

    br("prawniczy", "Legal-Event", "für Legal-Events", "Auf einem Legal-Event",
       "Anwältinnen, Justiziare und Kanzleivertreter",
       "Legal Tech ist das heißeste Thema der Branche — und ein KI-Roboter auf einem Legal-Event verwandelt die Diskussion über die Zukunft des Berufs in ein Erlebnis, das die Teilnehmenden mit einer konkreten Kanzlei oder Konferenz verbinden.",
       ("Worüber kann der Roboter auf einer Rechtsveranstaltung sprechen?", "Zum Beispiel über KI in der anwaltlichen Arbeit, Automatisierung und die Zukunft juristischer Dienstleistungen — den Inhalt bereiten wir gemeinsam vor, mit Humor, der zum Publikum passt.")),

    br("nieruchomosci", "Immobilien-Event", "für Immobilien-Events", "Auf einem Immobilien-Event",
       "Projektentwickler, Makler und Investoren",
       "Auf Immobilienmessen und bei Projektpremieren zieht der Roboter Kunden an den Stand des Bauträgers — und macht aus der Projektpräsentation ein Ereignis, über das die Käufer sprechen.",
       ("Kann der Roboter im Vertriebsbüro eines Projekts arbeiten?", "Ja — der Roboter bewährt sich bei Eröffnungen von Vertriebsbüros und Tagen der offenen Tür, wo er Familien anzieht, die sich Wohnungen ansehen.")),

    br("budowlany", "Bau-Event", "für Bau-Events", "Auf einem Bau-Event",
       "Bauunternehmer, Hersteller und Bauingenieure",
       "Die Baubranche schätzt Handfestes — und der Roboter liefert Handfestes: Technologie, die man sieht, hört und testen kann. Auf Baumessen sammelt der Stand mit Humanoid die größte Frequenz der Halle.",
       ("Kann der Roboter in einer Messehalle der Baubranche arbeiten?", "Ja — typische Messehallenböden sind für den Roboter ideal. Wir brauchen lediglich einige Meter freie Fläche am Stand.")),

    br("przemyslowy", "Industrie-Event", "für Industrie-Events", "Auf einem Industrie-Event",
       "Ingenieure und Produktionsverantwortliche",
       "Industrie 4.0 und Robotisierung sind die Leitthemen der Branche — ein Humanoid auf dem Industrie-Event ist ihre beste Illustration und der natürliche Einstieg in Gespräche über Automatisierung in Ihrem Angebot.",
       ("Lässt sich die Show mit dem Thema Automatisierung verbinden?", "Ja — der Roboter kann die Diskussion über die Robotisierung der Produktion eröffnen, und der Operator kann über die realen Möglichkeiten heutiger Humanoide sprechen.")),

    br("energetyczny", "Energie-Event", "für Energie-Events", "Auf einem Energie-Event",
       "Vertreterinnen und Vertreter des Energiesektors",
       "Die Energiewende ist eine Erzählung über die Zukunft — der humanoide Roboter gibt dieser Erzählung auf Kongressen, Energiemessen und Branchengalas ein Gesicht.",
       ("Tritt der Roboter auch auf einem Branchenkongress mit vielen Partnern auf?", "Ja — wir haben Erfahrung mit Veranstaltungen mit komplexer Partnerstruktur; Branding und Rolle des Roboters stimmen wir vollständig mit dem Veranstalter ab.")),

    br("logistyczny", "Logistik-Event", "für Logistik-Events", "Auf einem Logistik-Event",
       "Logistik- und Supply-Chain-Verantwortliche",
       "Die Logistik automatisiert sich schneller als jede andere Branche — ein humanoider Roboter auf dem Logistik-Event zeigt die Richtung dieser Veränderung und zieht Teilnehmende an Stände und Partnerflächen.",
       ("Kann der Roboter auf die Automatisierung von Lägern eingehen?", "Ja — die Inhalte der Show können wir gemeinsam mit Ihrem Fachteam in der Thematik von Intralogistik und Automatisierung verankern.")),

    br("motoryzacyjny", "Automotive-Event", "für Automotive-Events", "Auf einem Automotive-Event",
       "Autofans und Kunden der Autohäuser",
       "Modellpremiere, Autohauseröffnung, Motorshow — der Roboter neben dem Fahrzeug ist die Kombination, die die Objektive anzieht. Der technologische Charakter des Humanoiden passt perfekt zur Botschaft moderner Mobilität.",
       ("Kann der Roboter an einer Fahrzeugpremiere teilnehmen?", "Ja — der Roboter kann das Auto enthüllen, die Kernmerkmale des Modells präsentieren und damit für Fotos posieren. Das ist eines unserer Lieblingsszenarien.")),

    br("telekomunikacyjny", "Telko-Event", "für Telko-Events", "Auf einem Telko-Event",
       "Vertreterinnen der Telko- und Technologiebranche",
       "Die Telko-Branche verkauft Konnektivität und Zukunft — ein in Echtzeit gesteuerter Roboter ist die eindrucksvolle Demonstration beider Dinge auf Messen, Konferenzen und Events der Netzbetreiber.",
       ("Kann der Roboter die Leistungsfähigkeit des Netzes demonstrieren?", "Die Show lässt sich erzählerisch mit dem Thema Konnektivität und niedriger Latenz verbinden — die Details des Drehbuchs erarbeiten wir mit Ihrem Marketing.")),

    br("handlowy", "Handels-Event", "für Handels-Events", "Auf einem Handels-Event",
       "Einkäufer, Distributoren und Handelspartner",
       "Systemkongresse, Partnertagungen und Ordermessen haben ein Ziel: Beziehungen. Der humanoide Roboter schenkt den Teilnehmenden ein gemeinsames Erlebnis, das Verkaufsgespräche besser öffnet als jedes Give-away.",
       ("Kann der Roboter die Vertriebsziele der Veranstaltung unterstützen?", "Ja — der Roboter kann in Angebotszonen einladen, Produktpremieren begleiten und Teilnehmende zu Ihrem Vertriebsteam lotsen.")),

    br("gastronomiczny", "Gastro-Event", "für Gastro-Events", "Auf einem Gastro-Event",
       "Köchinnen, Gastronomen und Foodies",
       "Genussfestivals und Gastro-Messen leben von Sinneseindrücken — der humanoide Roboter fügt ihnen einen technologischen hinzu: Er begrüßt Gäste, kündigt Kochshows an und posiert mit den Köstlichkeiten für Fotos.",
       ("Kann der Roboter eine Kochshow mitmoderieren?", "Ja — der Roboter kann Küchenchefs ankündigen, die Vorführungen kommentieren und das Publikum zwischen den Verkostungen einbinden.")),

    br("turystyczny", "Tourismus-Event", "für Tourismus-Events", "Auf einem Tourismus-Event",
       "die Tourismusbranche und Reisende",
       "Auf Reisemessen lockt jeder Stand mit einem Strand — Ihrer kann mit der Begegnung mit einem Roboter locken. Der Humanoid stoppt die Besucher und verschafft Ihrem Team Zeit für das Gespräch über Ihre Reiseangebote.",
       ("Kann der Roboter Fremdsprachen sprechen?", "Ja — neben Deutsch führt der Roboter Interaktionen auf Englisch, was auf internationalen Reisemessen ein großer Vorteil ist.")),

    br("sportowy", "Sport-Event", "für Sport-Events", "Auf einem Sport-Event",
       "Fans, Athletinnen und Sponsoren",
       "Spiel, Turnier, Sportgala oder Volkslauf — der humanoide Roboter heizt das Publikum an, macht das Aufwärmen mit den Fans und gibt Sponsoren eine Aktivierung, die das Stadion mit Applaus belohnt.",
       ("Kann der Roboter in der Halbzeitpause auftreten?", "Ja — eine mehrminütige Show in der Pause ist das ideale Format: dynamisch, spektakulär und bereit für die Videowand.")),

    br("kulturalny", "Kultur-Event", "für Kultur-Events", "Auf einem Kultur-Event",
       "das Publikum von Festivals und Kulturinstitutionen",
       "Kunst trifft Technologie: Der humanoide Roboter bei einer Vernissage, einem Festival oder im Theater wird zum performativen Kommentar auf die Zeit — und für die Institution zum Publikumsmagneten.",
       ("Kann der Roboter an einer künstlerischen Performance teilnehmen?", "Ja — wir arbeiten mit Künstlerinnen und Kuratoren zusammen; Choreografie und Rolle des Roboters entwickeln wir passend zum künstlerischen Konzept der Veranstaltung.")),

    br("modowy", "Fashion-Event", "für Fashion-Events", "Auf einem Fashion-Event",
       "Designerinnen, Modemedien und Showgäste",
       "Ein Roboter auf dem Laufsteg oder in der ersten Reihe ist das Bild, das durch die Modemedien geht. Der G1 kann die Show eröffnen, ein Element der Kollektion präsentieren und bei den Shootings rund um die Show auftreten.",
       ("Kann der Roboter Kleidung oder Accessoires tragen?", "In begrenztem Umfang ja — leichte Styling-Elemente sind möglich. Die Details klären wir vor der Veranstaltung mit dem Designteam.")),

    br("beauty", "Beauty-Event", "für Beauty-Events", "Auf einem Beauty-Event",
       "die Kosmetikbranche und Beauty-Influencer",
       "Die Beauty-Branche lebt in den sozialen Medien — und nichts erzeugt so viele Reels wie ein Humanoid bei einer Kosmetikpremiere oder auf einer Beauty-Messe. Der Roboter begrüßt Gäste, präsentiert Neuheiten und posiert mit den Produkten.",
       ("Kann der Roboter Kosmetikprodukte präsentieren?", "Ja — der Roboter kann leichte Produkte halten und zeigen, Neuheiten präsentieren und in Fotobereichen mit dem Branding der Marke mitwirken.")),

    br("edukacyjny", "Bildungs-Event", "für Bildungs-Events", "Auf einem Bildungs-Event",
       "Schülerinnen, Studierende und Lehrkräfte",
       "Es gibt keine bessere Lektion über die Zukunft als die Begegnung mit ihr von Angesicht zu Angesicht. Auf Wissenschaftspicknicks, Bildungsfestivals und in Schulen macht der Roboter aus den abstrakten Begriffen KI und Robotik ein Erlebnis.",
       ("Hat die Show eine Bildungsdimension?", "Ja — der Operator erklärt, wie der Roboter läuft, die Balance hält und Sprache versteht. Das Niveau der Erzählung passen wir an das Alter der Zielgruppe an.")),

    br("ekologiczny", "Nachhaltigkeits-Event", "für Nachhaltigkeits-Events", "Auf einem Nachhaltigkeits-Event",
       "Teilnehmende von Nachhaltigkeitsveranstaltungen",
       "Klima- und ESG-Veranstaltungen sprechen über die Technologien von morgen — der humanoide Roboter zeigt sie heute. Elektrisch, leise und wiederverwendbar: eine Attraktion, die zur Nachhaltigkeitsbotschaft passt.",
       ("Passt der Roboter zur ökologischen Botschaft der Veranstaltung?", "Ja — der G1 ist vollständig elektrisch und leise, und seine Präsenz passt gut zur Erzählung über verantwortungsvolle Zukunftstechnologien.")),

    br("charytatywny", "Charity-Event", "für Charity-Events", "Auf einem Charity-Event",
       "Spenderinnen und Auktionsgäste",
       "Auf einem Charity-Ball oder einer Benefizauktion hebt der Roboter Teilnahme und Gebote: Er kann die Sammlung moderieren, Auktionsobjekte ankündigen und den Spendern auf eine Weise danken, die niemand vergisst.",
       ("Bieten Sie besondere Konditionen für gemeinnützige Organisationen?", "Ja — Charity-Veranstaltungen behandeln wir besonders. Schreiben Sie uns mit einer Beschreibung der Initiative, dann erstellen wir ein individuelles Angebot.")),

    br("startupowy", "Startup-Event", "für Startup-Events", "Auf einem Startup-Event",
       "Gründerinnen, Investoren und die Startup-Community",
       "Demo Day, Meetup oder Startup-Konferenz: Der humanoide Roboter zieht Investoren und Medien auf Ihre Bühne — und gibt dem Networking das Thema, das jedes Gespräch eröffnet.",
       ("Kann der Roboter den Pitch unseres Startups unterstützen?", "Ja — der Roboter kann Ihren Pitch ankündigen, im Demo auftreten oder während einer Startup-Messe Frequenz an Ihren Stand ziehen.")),

    br("miejski", "Stadt-Event", "für Stadt-Events", "Auf einem Stadt-Event",
       "Bürgerinnen, Bürger und Familien",
       "Straßenfeste, Stadtteilpicknicks und Open-Air-Veranstaltungen der Kommunen gewinnen mit dem Roboter eine Attraktion, die Menschen jeden Alters anzieht — und die Stadt als offen für Moderne zeigt.",
       ("Übernehmen Sie auch öffentliche Aufträge?", "Ja — wir arbeiten mit Kommunen und städtischen Einrichtungen zusammen, stellen Rechnungen und richten uns nach den formalen Anforderungen der Vergabe.")),

    br("outdoor", "Outdoor-Event", "für Outdoor-Events", "Auf einem Outdoor-Event",
       "Teilnehmende von Open-Air-Veranstaltungen",
       "Der humanoide Roboter arbeitet auch unter freiem Himmel: Picknicks, Straßenfeste und Open-Air-Zonen sind seine natürliche Umgebung, solange wir ihm ebenen Untergrund und trockenes Wetter sichern — um den Rest kümmern wir uns.",
       ("Welche Bedingungen muss die Fläche im Freien erfüllen?", "Einen ebenen, befestigten Untergrund (Podest, Pflaster, Asphalt) und einen Schutz für den Regenfall. Wir schicken einen einfachen Rider, der alle Zweifel ausräumt.")),

    br("hybrydowy", "Hybrid-Event", "für Hybrid-Events", "Auf einem Hybrid-Event",
       "Teilnehmende im Saal und online",
       "Ein Hybrid-Event muss zwei Publika gleichzeitig einbinden — der humanoide Roboter wirkt auf beide: Im Saal baut er die Traube, und in der Übertragung liefert er der Regie die attraktivste Einstellung der ganzen Veranstaltung.",
       ("Macht sich der Roboter in der Online-Übertragung gut?", "Hervorragend — dynamische Einstellungen des Roboters heben die Zuschauerzahlen des Streams. Gern stimmen wir die Shows mit der Regie der Übertragung ab.")),

    br("vip", "VIP-Event", "für VIP-Events", "Auf einem VIP-Event",
       "besondere Gäste und Premium-Kunden",
       "Eine exklusive Veranstaltung für ausgewählte Gäste verlangt eine Attraktion der höchsten Kategorie. Eine private Humanoiden-Show — mit namentlicher Begrüßung und maßgeschneiderten Interaktionen — ist ein Erlebnis, das wenigen vorbehalten bleibt.",
       ("Gewährleisten Sie Diskretion bei geschlossenen Veranstaltungen?", "Ja — wir betreuen vertrauliche Veranstaltungen, unterzeichnen NDAs und veröffentlichen kein Material ohne Zustimmung des Veranstalters.")),
]

# ==================================================== IMPREZY PRYWATNE

PRIVATE = [
    priv("robot-na-urodziny", "Roboter für Geburtstage", "für Geburtstage", "Auf einem Geburtstag",
         sub="Geburtstag mit einem echten Roboter — für ein Kind ein wahr gewordener Traum, für Erwachsene eine Feier, über die der ganze Freundeskreis spricht. Der G1 tanzt, gratuliert, gibt High Fives und posiert für Fotos mit dem Geburtstagskind.",
         uniq_scen=("Glückwünsche vom Roboter", "Der Roboter gratuliert dem Geburtstagskind mit Stimme — namentlich, mit Humor, in die Kamera. Dieser Moment bleibt für immer im Familienarchiv."),
         faq_uniq=("Funktioniert der Roboter beim Kindergeburtstag und bei Erwachsenen?", "Ja — wir haben Showvarianten für Kinder (Spiele, High Fives, gemeinsames Tanzen) und für Erwachsene (Show, Glückwünsche, Fotobereich). Sagen Sie uns, wer feiert, und wir stellen das Programm zusammen.")),

    priv("robot-na-imieniny", "Roboter für den Polterabend", "für den Polterabend", "Auf einem Polterabend",
         sub="Ein Polterabend mit einer Überraschung, die die Familie noch nie gesehen hat: Der humanoide Roboter gratuliert dem Brautpaar, tanzt mit den Gästen und macht aus der Feier im Hof das Ereignis des Jahres in der ganzen Verwandtschaft.",
         uniq_scen=("Überraschung fürs Brautpaar", "Der Roboter kommt unangekündigt herein, geht auf das Brautpaar zu und gratuliert — die Reaktion ist unbezahlbar, und die Aufnahme davon wandert anschließend durch die ganze Familie."),
         faq_uniq=("Kann der Roboter zu Hause oder im Garten auftreten?", "Ja — wir brauchen nur ebenen Untergrund und etwas Platz. Wir betreuen Feiern in Häusern, Gärten und angemieteten Sälen.")),

    priv("robot-na-rocznice", "Roboter für Jubiläen", "für Jubiläen", "Auf einem Jubiläum",
         sub="Hochzeitstag, Beziehungsjubiläum oder ein anderer wichtiger Jahrestag verdient eine Inszenierung, mit der niemand rechnet. Der humanoide Roboter gratuliert, bringt den Toast aus und führt den Tanz an — und die Jubilare bekommen eine Erinnerung für die nächsten Jahrzehnte.",
         uniq_scen=("Toast auf die Jubilare", "Der Roboter bringt den Toast aus und hält eine vorbereitete Rede über das Paar — Rührung und Lachen in perfekter Dosierung."),
         faq_uniq=("Kann der Roboter die Geschichte des Paares erzählen?", "Ja — wir bereiten mit Ihnen eine kurze Erzählung vor (wie sie sich kennengelernt haben, gemeinsame Anekdoten), die der Roboter in die Glückwünsche einflicht. Die Gäste sind begeistert.")),

    priv("robot-na-impreze-prywatna", "Roboter für Privatfeiern", "für Privatfeiern", "Auf einer Privatfeier",
         sub="Premium-Hausparty, Geburtstag in der gemieteten Villa, private Feier im Garten — der humanoide Roboter ist die Attraktion, nach der Ihre Feier im Freundeskreis zur Legende wird.",
         uniq_scen=("Der Ehrengast des Abends", "Der Roboter taucht als unangekündigter Gast auf — er begrüßt die Gastgeber, tanzt und spricht dank KI. Für den Rest des Abends redet niemand über etwas anderes."),
         faq_uniq=("Wie viel Platz braucht der Roboter auf einer Privatfeier?", "Ein paar Quadratmeter ebener Boden genügen — Wohnzimmer, Terrasse oder Partyzelt reichen völlig aus.")),

    priv("robot-na-wieczor-panienski", "Roboter für den Junggesellinnenabschied", "für den Junggesellinnenabschied", "Auf einem Junggesellinnenabschied",
         sub="Ein Junggesellinnenabschied, den keine andere Gruppe übertrifft: Der humanoide Roboter tanzt mit der Braut, moderiert die Spiele und posiert für Fotos, die den Gruppenchat zum Glühen bringen.",
         uniq_scen=("Tanz mit der Braut", "Der Roboter bittet die künftige Braut zum Tanz — eine Choreografie zu zweit, angefeuert von der Gruppe, und eine Aufnahme, die auf der Hochzeit der Hit wird."),
         faq_uniq=("Moderiert der Roboter die Spiele beim Junggesellinnenabschied?", "Ja — der Roboter kann Quizze über das Paar, Tanz-Challenges und Toasts übernehmen. Das Programm stellen wir mit der Organisatorin zusammen.")),

    priv("robot-na-bal-maturalny", "Roboter für den Abiball", "für den Abiball", "Auf einem Abiball",
         sub="Ein Abiball mit humanoidem Roboter ist die Veranstaltung, die in die Schulgeschichte eingeht. Der G1 eröffnet den Ball, tanzt mit dem Abschlussjahrgang und posiert für Fotos, die noch in derselben Nacht Instagram fluten.",
         uniq_scen=("Eröffnung des Balls", "Nach dem Eröffnungstanz betritt der Roboter mit einer eigenen Choreografie die Tanzfläche — der Moment, in dem der ganze Saal zum Handy greift. Der DJ hat es danach den Rest der Nacht leichter."),
         faq_uniq=("Kann der Roboter zum Motto des Balls auftreten?", "Ja — die Show können wir auf das Ballmotto und die Playlist des DJs abstimmen. Die Details klären wir mit dem Organisationskomitee.")),

    priv("robot-na-komunie", "Roboter für die Kommunion", "für die Kommunion", "Auf einer Kommunionsfeier",
         sub="Eine Kommunionsfeier mit einer Attraktion, die Kinder begeistert und Erwachsene überrascht: Der humanoide Roboter tanzt, gibt High Fives und posiert für Fotos — im Ton, der zum familiären Charakter des Anlasses passt.",
         uniq_scen=("Attraktion für die Kinder am Tisch der Erwachsenen", "Während die Erwachsenen am Tisch feiern, kümmert sich der Roboter um die jüngeren Gäste: Spiele, Tanz und High Fives unter Aufsicht des Operators. Die Eltern haben Ruhe, die Kinder den besten Tag des Jahres."),
         faq_uniq=("Passt die Show zum Charakter des Anlasses?", "Ja — bei Kommunionsfeiern führen wir das Programm in ruhigem, familiärem Ton, mit Schwerpunkt auf Spielen für die Kinder.")),

    priv("robot-na-chrzciny", "Roboter für die Taufe", "für die Taufe", "Auf einer Tauffeier",
         sub="Eine Taufe bringt die ganze Familie zusammen — und der humanoide Roboter gibt allen Generationen eine gemeinsame Attraktion: von den Großeltern bis zu den älteren Geschwistern. Ein behutsames Familienprogramm mit Erinnerungsfotos für die Gäste.",
         uniq_scen=("Erinnerungsfotos der Familie", "Der Roboter posiert mit jeder Familie einzeln für Fotos — nach der Feier hat jeder Gast ein besonderes Andenken an den Tag."),
         faq_uniq=("Erschreckt der Roboter die Kleinsten nicht?", "Der Operator führt die Interaktionen sehr behutsam und beginnt aus der Distanz — die Kinder wechseln schnell von Schüchternheit zu Begeisterung. Säuglinge beobachten aus der sicheren Entfernung der Eltern.")),

    priv("robot-na-dzien-dziecka", "Roboter fürs Kinderfest", "fürs Kinderfest", "Auf einem Kinderfest",
         sub="Ein Kinderfest mit echtem Roboter schlägt jede Hüpfburgzone: Tanzshows, gemeinsame Spiele und High Fives mit dem Humanoiden sind die Attraktion, an die sich die Kinder das ganze Jahr erinnern — in der Schule, im Unternehmen oder im Viertel.",
         uniq_scen=("Spiele mit der ganzen Gruppe", "Der Roboter leitet Bewegungsspiele mit den Kindern an: Gesten nachmachen, gemeinsam tanzen, Reaktionsspiele — die Energie der Gruppe steigt von Minute zu Minute."),
         faq_uniq=("Betreuen Sie auch Kinderfeste von Unternehmen?", "Ja — das Familienfest für die Kinder der Belegschaft ist eines unserer häufigsten Formate. Das Programm verbindet Shows für die Kinder mit Attraktionen für die Eltern.")),

    priv("robot-na-mikolajki", "Roboter zum Nikolaus", "zum Nikolaus", "Beim Nikolausfest",
         sub="Den Robo-Nikolaus gibt es wirklich: Der G1 verteilt Geschenke, tanzt zu Weihnachtshits und posiert für Fotos am Baum. Nikolausfeiern in Unternehmen, Schulen oder im Viertel bekommen eine Attraktion, bei der die Kinder ihren Wunschzettel vergessen.",
         uniq_scen=("Geschenkübergabe", "Der Roboter überreicht den Kindern ihre Geschenke — jede Übergabe ist eine kleine Show für sich und ein Foto, das die Eltern über Jahre aufheben."),
         faq_uniq=("Kann der Roboter einen weihnachtlichen Akzent bekommen?", "Ja — Nikolausmütze und weihnachtliche Inszenierung der Show sind im Dezember Standard. Die Weihnachtsplaylist übernehmen wir ebenfalls.")),

    priv("robot-na-andrzejki", "Roboter fürs Oktoberfest", "fürs Oktoberfest", "Auf einem Oktoberfest",
         sub="Oktoberfest mit humanoidem Roboter: Der G1 begrüßt die Gäste im Festzelt, tanzt zur Blaskapelle und zur Party-Playlist und posiert in Tracht-Kulisse für Fotos — die Wiesn-Feier, über die bis zur nächsten Saison gesprochen wird.",
         uniq_scen=("Der Roboter im Festzelt", "Der Roboter zieht durch das Festzelt, begrüßt die Tische und übernimmt zwischen den Musikblöcken die Tanzfläche — ein Anblick, den auf keiner anderen Wiesn-Feier jemand hatte."),
         faq_uniq=("Kann der Roboter zur Blasmusik tanzen?", "Ja — die Choreografien synchronisieren wir mit der Playlist der Kapelle oder des DJs; die Titel stimmen wir einfach vorher ab.")),

    priv("robot-na-halloween", "Roboter zu Halloween", "zu Halloween", "Auf einer Halloween-Party",
         sub="Ein Roboter zu Halloween ist eine Attraktion an der Grenze von Science-Fiction und Horror — genau so, wie es sein soll. Der G1 in düsterem Styling begrüßt die Gäste, tanzt zu Halloween-Hits und macht mehr Eindruck als jedes Kostüm.",
         uniq_scen=("Düstere Begrüßung", "Der Roboter tritt aus dem Halbdunkel und begrüßt die Gäste — Gänsehaut garantiert, und gleich danach Gelächter und eine Schlange für Fotos."),
         faq_uniq=("Kann der Roboter ein Halloween-Styling bekommen?", "Ja — leichte Styling-Elemente und die passende Licht- und Musikinszenierung machen aus der Show ein perfekt stimmiges Spektakel.")),

    priv("robot-na-sylwestra", "Roboter zu Silvester", "zu Silvester", "In der Silvesternacht",
         sub="Silvester mit humanoidem Roboter heißt, buchstäblich mit der Zukunft ins neue Jahr zu gehen: Countdown mit dem Roboter, Toast um Mitternacht und Tanz bis zum Morgen. Die Feier, mit der alle Neujahrsgespräche beginnen.",
         uniq_scen=("Countdown bis Mitternacht", "Der Roboter führt den Countdown der letzten Sekunden des Jahres an und stößt mit den Gästen an — ein Jahresbeginn, den niemand aus Ihrem Freundeskreis hatte."),
         faq_uniq=("Arbeitet der Roboter in der Silvesternacht?", "Ja — Silvester ist unsere Hochsaison. Die Termine sind am schnellsten im Jahr vergeben, fragen Sie also möglichst früh an.")),

    priv("robot-na-karnawal", "Roboter für den Karneval", "für den Karneval", "Auf einer Karnevalsfeier",
         sub="Ein Karnevalsball braucht einen Star der Tanzfläche — und niemand tanzt so wie ein humanoider Roboter. Der G1 führt Tanzshows auf, reiht sich in den Zug ein und posiert für Fotos in Karnevalskulisse.",
         uniq_scen=("Star der Tanzfläche", "Der Roboter eröffnet die Tanzfläche mit einer eigenen Choreografie und lädt die Gäste zum Mittanzen ein — ab diesem Moment wird die Fläche bis zum Ende des Balls nicht mehr leer."),
         faq_uniq=("Tanzt der Roboter auch zu Live-Musik?", "Ja — die Choreografien synchronisieren wir mit der Playlist des DJs oder dem Repertoire der Band; es reicht, die Titel vorher abzustimmen.")),

    priv("robot-na-walentynki", "Roboter zum Valentinstag", "zum Valentinstag", "Am Valentinstag",
         sub="Die Valentinsüberraschung, die kein Blumenstrauß übertrifft: Der humanoide Roboter macht die Liebeserklärung in Ihrem Namen, überreicht das Geschenk und bittet zum Tanz. Für Paare — und für Locations, die Valentins-Buzz wollen.",
         uniq_scen=("Eine Erklärung aus der Zukunft", "Der Roboter geht auf die ausgewählte Person zu, trägt die vorbereitete Erklärung vor und überreicht Blumen oder ein Geschenk — ein Moment wie aus einem Science-Fiction-Film, nur live."),
         faq_uniq=("Hilft der Roboter bei einem Heiratsantrag?", "Ja — wir helfen bei der Planung eines Antrags mit Roboter: vom Drehbuch bis zur diskreten Aufnahme der gesamten Überraschung.")),

    priv("robot-na-garden-party", "Roboter für die Gartenparty", "für die Gartenparty", "Auf einer Gartenparty",
         sub="Gartenparty mit Stil und mit Zukunft: Der humanoide Roboter zieht seine Kreise zwischen den Gästen auf der Terrasse, führt Shows auf dem Podest im Rasen auf und gibt dem Fest im Garten einen Charakter, von dem die Nachbarn nur träumen können.",
         uniq_scen=("Nachmittag im Garten", "Der Roboter arbeitet im Rhythmus der Feier: Begrüßung am Eingang, Show auf dem Podest, lockere Interaktionen an den Tischen — alles im sommerlich unaufgeregten Tempo."),
         faq_uniq=("Was braucht der Roboter im Garten?", "Eine ebene, befestigte Fläche (Terrasse, Podest, Pflaster) und trockenes Wetter. Für den Regenfall vereinbaren wir eine überdachte Variante.")),
]

_add(EVENTS)
_add(BRANCHEN)
_add(PRIVATE)

assert len(TEXT) == 70, f"oczekiwano 70 stron, jest {len(TEXT)}"
