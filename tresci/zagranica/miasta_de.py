# -*- coding: utf-8 -*-
"""Strony miast 33bots.de pisane osobno, nie z szablonu (11.2026).

Strony miast powstawały z jednego szablonu (ok. 50% wspólnego tekstu), co Google traktuje jak
doorway pages. Tutaj siedem najważniejszych miast ma własną treść: lokalne targi i kongresy, sale,
typowy przebieg i referencję dobraną do profilu miasta; niemiecka realizacja (Dresdner Schlössernacht)
jest na pierwszym planie. Pozostałe strony miast dostają noindex i wypadają z mapy strony —
do czasu, aż też zostaną napisane osobno.

Fakty o 33bots wyłącznie z rynki.py i dotychczasowych stron .de; targi i sale — powszechnie znane,
bez twierdzeń, że na nich pracowaliśmy.

Użycie (z katalogu głównego repozytorium 33bots.pl):
    python3 tresci/zagranica/miasta_de.py
potem buduj_podstrony.py de <repo>, buduj_mape.py de <repo>.
"""
import json
import re
from pathlib import Path

ZRODLA = Path(__file__).resolve().parent / 'podstrony' / 'de'

ALT = {
    'realizacja-gala-palac': 'Humanoider Roboter im Smoking im Ballsaal eines Palais',
    'realizacja-gala-wsrod-gosci': 'Humanoider Roboter unter den Gästen einer Gala',
    'realizacja-gala-detal': 'Nahaufnahme des humanoiden Roboters mit Krone und Paillettensmoking',
    'realizacja-gala-czerwony-dywan': 'Humanoider Roboter im Paillettensmoking mit Krone auf dem roten Teppich vor der Sponsorenwand',
    'realizacja-gala-zdjecia-gosci': 'Gäste der Gala fotografieren sich mit dem humanoiden Roboter im Paillettensmoking',
    'realizacja-women-in-tech-tlum': 'Teilnehmerinnen des Women in Tech Summit filmen den humanoiden Roboter mit dem Handy',
    'realizacja-matys-stoisko': 'Humanoider Roboter im Matys-T-Shirt am Stand des Bauträgers',
    'realizacja-lexai-starowka': 'Humanoider Roboter im LEX-AI-T-Shirt in der Altstadt, Passanten machen Fotos',
    'realizacja-yeah-gym-silownia': 'Humanoider Roboter im Trainingsbereich des Clubs YEAH GYM',
    'realizacja-grupa-rekord-mspo': 'Humanoider Roboter in den Farben der Rekord-Gruppe am Stand der Messe MSPO in Kielce',
    'realizacja-dream-med-expo': 'Humanoider Roboter am Stand von Dream-Med auf der Warsaw Medical Expo',
    'realizacja-kopernik-noc': 'Humanoider Roboter in der Ausstellung des Kopernikus-Wissenschaftszentrums bei einem Abend für Erwachsene',
}


def para(podpis, a, b):
    return (f'<para podpis="{podpis}"><kadr plik="{a}" alt="{ALT[a]}"/>'
            f'<kadr plik="{b}" alt="{ALT[b]}"/></para>')


SCHLOESSERNACHT = '<b>Dresdner Schlössernacht</b> · Dresden'

MIASTA = {
    'berlin': {
        'opis': 'Humanoiden Roboter Unitree G1 in Berlin mieten: für IFA, ITB, Kongresse im CityCube und Galas. Operator, Anfahrt und Branding im Preis, ab 2.500 € pro Tag.',
        'lead': 'Der Unitree G1 kommt zu Ihrer Veranstaltung in Berlin und Brandenburg: auf die Messe unter dem Funkturm, zum Kongress im CityCube oder Estrel, zum Launch in der STATION Berlin.',
        'foto': ('realizacja-gala-wsrod-gosci', SCHLOESSERNACHT),
        'czytaj': [['roboter-mieten-dresden.html', 'Roboter mieten in Dresden'], ['roboter-mieten-hamburg.html', 'Roboter mieten in Hamburg'],
                   ['humanoiden-roboter-mieten.html', 'Humanoiden Roboter mieten'], ['angebot-konferenzen-galas.html', 'Roboter für Konferenzen und Galas'],
                   ['roboter-mieten-preise.html', 'Preise und Kosten']],
        'pytania': [
            ['Fahren Sie auch zu Locations außerhalb des Berliner Rings?', 'Ja. Wir kommen nach ganz Berlin und Brandenburg, von Adlershof über Spandau bis nach Potsdam, Oranienburg oder Königs Wusterhausen. Eine Kilometerpauschale gibt es nicht: Die Anfahrt ist im Angebot enthalten.'],
            ['Kann der Roboter auf einer Berliner Tech-Konferenz Englisch sprechen?', 'Ja. Der Roboter spricht Deutsch, Englisch und jede andere Sprache und wechselt mitten im Gespräch. Auf internationalen Konferenzen begrüßt er die Teilnehmenden in ihrer Sprache und beantwortet Fragen zum Programm.'],
            ['Wie früh sollten wir für die IFA oder die ITB reservieren?', 'Je früher, desto besser: am besten mindestens 3–4 Wochen vor dem Termin, für Messewochen lieber früher. Die Reservierung erfolgt ohne Anzahlung, die Rechnung kommt nach der Veranstaltung.'],
            ['Was kostet ein Robotereinsatz in Berlin?', 'Ein kompletter Veranstaltungstag kostet ab 2.500 €, mit Operator, Anfahrt, Branding und Haftpflichtversicherung. Bei zwei und mehr Tagen, etwa einer ganzen Messewoche, sinkt der Preis um 15 % pro Tag.'],
        ],
        'tresc': f'''
<h2 id="berlin">Berlin: viel Programm, wenig Aufmerksamkeit</h2>

<p>In Berlin konkurriert fast jede Veranstaltung mit drei anderen am selben Abend: die Tech-Konferenz in Kreuzberg, der Verbandsempfang an der Spree, der Markenlaunch in einer alten Industriehalle. Das Publikum hat vieles schon gesehen. Ein humanoider Roboter, der frei durch den Raum geht, Gäste auf Deutsch und Englisch anspricht und Ihr Logo auf der Brust trägt, gehört selten dazu.</p>

<p>Wir kommen mit dem Unitree G1 nach Berlin und Brandenburg, mit eigenem Operator, abgestimmtem Drehbuch und Branding. Ein kompletter Veranstaltungstag kostet ab 2.500&nbsp;€, die Anfahrt ist darin enthalten. Was der Roboter kann und wie eine Buchung abläuft, steht auf der Seite <a href="humanoiden-roboter-mieten.html">Humanoiden Roboter mieten</a>.</p>

<h2 id="messen-berlin">Berliner Messen und Kongresse, zu denen ein Roboter passt</h2>

<p>Die Beispiele zeigen, welche Aufgabe der Roboter auf der jeweiligen Messe übernehmen kann.</p>

<ul>
  <li><strong>IFA</strong> — Auf der Messe für Unterhaltungselektronik und Hausgeräte ist Technik ohnehin das Thema. Der G1 holt die Besucher an den Stand, die an der zehnten Bildschirmwand vorbeigehen.</li>
  <li><strong>ITB Berlin</strong> — Auf der Reisemesse arbeitet der Roboter als mehrsprachiger Gastgeber: Er begrüßt Fachbesucher in ihrer Sprache und wechselt mitten im Gespräch.</li>
  <li><strong>InnoTrans</strong> — Zwischen Schienenfahrzeugen und Leittechnik zeigt ein laufender Humanoid Automatisierung zum Anfassen und überbrückt die Zeit bis zum nächsten Fachgespräch.</li>
  <li><strong>Grüne Woche</strong> — Eine Publikumsmesse mit vielen Familien: Der Roboter gibt die Hand, posiert für Fotos und sorgt für die Traube vor Ihrem Stand.</li>
  <li><strong>Kongresse im CityCube, im bcc und im Estrel</strong> — Begrüßung am Registration Desk, Ankündigung der Keynote, Fotomoment in der Kaffeepause.</li>
</ul>

<p>Wie wir einen Messeauftritt planen, von der Standposition über das Drehbuch bis zum QR-Code auf der Brust, beschreibt die Seite <a href="angebot-messen.html">Roboter für Messen</a>.</p>

<wideo/>

<h2 id="locations-berlin">Locations: vom Funkturm bis zum Kraftwerk</h2>

<ul>
  <li><strong>Messe Berlin und CityCube</strong> — Leitmessen und Kongresse unter dem Funkturm, mit breiten Gängen, in denen der Roboter laufen kann.</li>
  <li><strong>Estrel Congress Center</strong> — Großkongresse, Galas und Award-Nächte in Neukölln.</li>
  <li><strong>STATION Berlin</strong> — Hallen des früheren Postbahnhofs am Gleisdreieck, gefragt für Tech-Konferenzen und Produktlaunches.</li>
  <li><strong>Flughafen Tempelhof</strong> — Hangars für großformatige Markenevents und Roadshows.</li>
  <li><strong>Kraftwerk Berlin und AXICA</strong> — Abendveranstaltungen mit Bühne: Der Roboter eröffnet den Abend oder überreicht einen Preis.</li>
</ul>

<p>Was der Roboter vor Ort braucht, steht gesammelt auf der Seite <a href="unitree-g1-mieten.html">Unitree G1: technische Daten und Anforderungen</a>. Ersatzakkus hat der Operator dabei, die Show läuft den ganzen Messetag.</p>

<h2 id="ablauf-berlin">So läuft ein Tag auf einer Berliner Konferenz ab</h2>

<p>Ein typischer Ablauf: Morgens steht der G1 am Eingang, begrüßt die Teilnehmenden und weist auf die erste Session hin. Vor der Keynote kündigt er die Rednerin an. In den Pausen geht er mit dem Operator durch das Foyer, beantwortet Fragen zum Programm und stellt sich für Fotos auf. Am Abend eröffnet er den Empfang. Was er sagt, legen wir vorher gemeinsam fest: Agenda, Sprecher und das Wichtigste über Ihr Unternehmen spielen wir ihm ein.</p>

<h2 id="referenzen">Referenzen: Ball in Dresden, Tech-Konferenz mit 14.000 Gästen</h2>

{para('Dresdner Schlössernacht (Dresden) und Women in Tech Summit (Warschau).', 'realizacja-gala-czerwony-dywan', 'realizacja-women-in-tech-tlum')}

<p>Bei der Dresdner Schlössernacht stand der Roboter im Paillettensmoking mit Krone auf dem roten Teppich, im Ballsaal und mitten unter den Gästen. Für Berliner Konferenzformate ist der <a href="case-study-women-in-tech.html">Women in Tech Summit</a> der passende Vergleich: rund 14.000 Teilnehmende, der Roboter auf dem Laufsteg und mitten unter den Teilnehmerinnen. Weitere Einsätze zeigen die <a href="referenzen-videos.html">Referenzen und Videos</a>.</p>
''',
    },

    'muenchen': {
        'opis': 'Humanoiden Roboter Unitree G1 in München mieten: für automatica, bauma, EXPO REAL, Kongresse im ICM und Firmenfeiern. Ab 2.500 € pro Tag, Anfahrt inklusive.',
        'lead': 'Der Unitree G1 kommt nach München und Oberbayern: auf das Messegelände in Riem, ins ICM, in die BMW Welt oder zu Ihrer Firmenfeier.',
        'foto': ('realizacja-gala-czerwony-dywan', SCHLOESSERNACHT),
        'czytaj': [['roboter-mieten-frankfurt.html', 'Roboter mieten in Frankfurt'], ['roboter-mieten-berlin.html', 'Roboter mieten in Berlin'],
                   ['angebot-messen.html', 'Roboter für Messen'], ['roboter-firmenfeier.html', 'Roboter für die Firmenfeier'],
                   ['roboter-mieten-preise.html', 'Preise und Kosten']],
        'pytania': [
            ['Kommen Sie auch nach Garching, Freising oder Augsburg?', 'Ja. Wir fahren nach München und ins gesamte Umland, zum Forschungscampus Garching, zum Flughafen bei Freising, nach Augsburg, Ingolstadt oder Rosenheim. Die Anfahrt ist im Preis enthalten, ohne Kilometerpauschale.'],
            ['Passt ein humanoider Roboter auf eine Industriemesse wie die automatica?', 'Gerade dort. Auf einer Messe für Automation und Robotik erwartet das Fachpublikum Technik in Bewegung. Der G1 läuft frei über die Standfläche, spricht Besucher an und erklärt in Ihren Worten, was Ihr Unternehmen macht.'],
            ['Können wir den Roboter für eine Firmenfeier zur Wiesn-Zeit buchen?', 'Ja, auch für wenige Stunden. Kürzere Auftritte kalkulieren wir individuell und immer günstiger als einen ganzen Tag. Für die Wochen rund um das Oktoberfest empfehlen wir eine frühe Reservierung.'],
            ['Was kostet der Roboter für eine Messewoche in München?', 'Ein Veranstaltungstag kostet ab 2.500 €. Ab zwei Tagen gilt ein Rabatt von 15 % auf jeden Tag, das betrifft die meisten Münchner Fachmessen. Operator, Anfahrt, Branding und Haftpflichtversicherung sind enthalten.'],
        ],
        'tresc': f'''
<h2 id="muenchen">München: Fachpublikum, das Technik beurteilen kann</h2>

<p>München ist Industrie- und Hightech-Standort: Fahrzeugbau, Halbleiter, Maschinenbau, Versicherungen, dazu zwei Universitäten mit eigener Robotikforschung. Wer hier ausstellt oder einlädt, hat ein Publikum vor sich, das Technik einordnen kann. Ein humanoider Roboter, der wirklich läuft, das Gleichgewicht hält und frei spricht, überzeugt dieses Publikum mehr als ein Video auf dem Standmonitor.</p>

<p>Den Unitree G1 bringen wir mit Operator nach München und in ganz Oberbayern zum Einsatz. Die Eckdaten: ab 2.500&nbsp;€ pro Veranstaltungstag, Anfahrt, Branding und Haftpflichtversicherung inklusive. Die technischen Daten des Roboters stehen auf der Seite <a href="unitree-g1-mieten.html">Unitree G1 mieten</a>.</p>

<h2 id="messen-muenchen">Messegelände Riem: Welche Messen sich anbieten</h2>

<p>Zu diesen Messen passt ein humanoider Roboter besonders gut, jeweils mit einer anderen Aufgabe.</p>

<ul>
  <li><strong>automatica</strong> — Die Messe für intelligente Automation und Robotik. Ein Humanoid am Stand ist hier kein Fremdkörper, sondern das Thema selbst.</li>
  <li><strong>bauma</strong> — Zwischen tonnenschweren Maschinen fällt ein 132&nbsp;cm großer Roboter gerade deshalb auf. Er führt Besucher vom Freigelände an Ihren Stand.</li>
  <li><strong>EXPO REAL</strong> — Auf der Immobilienmesse stellt der G1 Projekte vor und holt Gesprächspartner aus dem Gang, bevor Ihr Team übernimmt.</li>
  <li><strong>IAA MOBILITY</strong> — Im Summit auf dem Messegelände und in den Open Spaces der Innenstadt arbeitet der Roboter als Gastgeber, der Passanten anspricht.</li>
  <li><strong>electronica und productronica</strong> — Fachmessen der Elektronik: Der Roboter erklärt Ihre Produktbotschaft in zwei Sätzen und leitet an die Fachleute weiter.</li>
</ul>

<wideo/>

<h2 id="locations-muenchen">Kongress, Showroom, Festsaal</h2>

<ul>
  <li><strong>ICM – International Congress Center Messe München</strong> — Kongresse und Hauptversammlungen: Begrüßung im Foyer, Anmoderation im Saal.</li>
  <li><strong>MOC</strong> — Ordertage und Fachveranstaltungen in Freimann, kurze Wege zwischen den Showrooms.</li>
  <li><strong>BMW Welt und Motorworld München</strong> — Produktpräsentationen und Kundenabende in Automobilkulisse.</li>
  <li><strong>Zenith und Kesselhaus</strong> — Industriehallen für Firmenfeiern, Kick-offs und Jubiläen.</li>
  <li><strong>Paulaner am Nockherberg</strong> — Festsäle für Weihnachts- und Jahresabschlussfeiern.</li>
</ul>

<p>Für alle genannten Locations gelten dieselben technischen Anforderungen; sie stehen auf der Seite <a href="unitree-g1-mieten.html">Unitree G1</a>. Der Roboter kommt immer mit dem Operator.</p>

<h2 id="firmenfeier-muenchen">Firmenfeier in München: Der Roboter als Programmpunkt</h2>

<p>Nicht jede Veranstaltung in München ist eine Messe. Zum Sommerfest im Biergarten, zum Jubiläum oder zur Weihnachtsfeier kommt der Roboter als Programmpunkt: Der G1 begrüßt die Kolleginnen und Kollegen am Eingang, überreicht mit der Geschäftsführung die Auszeichnungen und tanzt später eine Choreografie auf der Bühne. Den Charakter, förmlich oder locker, legen wir vorher fest. Mehr dazu unter <a href="roboter-firmenfeier.html">Roboter für die Firmenfeier</a> und <a href="roboter-weihnachtsfeier.html">Roboter für die Weihnachtsfeier</a>.</p>

<h2 id="referenzen">Referenzen: Dresdner Schlössernacht und Immobilienmesse</h2>

{para('Dresdner Schlössernacht (Dresden) und Matys Development auf der Immobilienmesse in Stettin.', 'realizacja-gala-palac', 'realizacja-matys-stoisko')}

<p>In Deutschland war der Roboter bei der Dresdner Schlössernacht im Einsatz: auf dem roten Teppich, im Ballsaal und unter den Gästen. Für die EXPO REAL ist der Stand von Matys Development der nächste Vergleich. Dort stellte der Roboter auf einer Immobilienmesse das Projekt Silver Garden vor. Insgesamt waren es bisher über 100 Veranstaltungen in fünf Ländern, zu sehen unter <a href="referenzen-videos.html">Referenzen und Videos</a>.</p>
''',
    },

    'hamburg': {
        'opis': 'Humanoiden Roboter Unitree G1 in Hamburg mieten: für OMR, SMM, INTERNORGA, Kongresse im CCH und Events am Hafen. Ab 2.500 € pro Tag, Anfahrt inklusive.',
        'lead': 'Der Unitree G1 kommt nach Hamburg und in die Metropolregion: in die Messehallen am Fernsehturm, ins CCH, in die Fischauktionshalle oder in die HafenCity.',
        'foto': ('realizacja-gala-zdjecia-gosci', SCHLOESSERNACHT),
        'czytaj': [['roboter-mieten-berlin.html', 'Roboter mieten in Berlin'], ['roboter-mieten-koeln.html', 'Roboter mieten in Köln'],
                   ['humanoiden-roboter-mieten.html', 'Humanoiden Roboter mieten'], ['roboter-produktlaunch.html', 'Roboter für den Produktlaunch'],
                   ['roboter-mieten-preise.html', 'Preise und Kosten']],
        'pytania': [
            ['Kommen Sie auch nach Lübeck, Kiel oder Lüneburg?', 'Ja. Wir fahren nach Hamburg und in die gesamte Metropolregion, nach Norderstedt, Lüneburg, Lübeck oder Kiel. Die Anfahrt ist im Angebot enthalten, es gibt keinen Aufschlag pro Kilometer.'],
            ['Kann der Roboter draußen am Hafen auftreten?', 'Ja, auf trockener und ebener Fläche, etwa auf einer Terrasse oder einem Platz am Wasser. Bei Regen tritt der Roboter nicht im Freien auf. Für Außeneinsätze planen wir deshalb vorab einen überdachten Bereich ein.'],
            ['Eignet sich der Roboter für ein Marketing-Festival wie die OMR?', 'Ja. Auf Veranstaltungen, bei denen jeder Stand um Aufmerksamkeit kämpft, liefert der Roboter den Grund zum Stehenbleiben und das Motiv für Fotos und Videos. Ihr Logo und ein QR-Code auf der Brust führen direkt zu Ihrer Kampagne.'],
            ['Wie viel Vorlauf brauchen Sie für einen Termin in Hamburg?', 'Am besten melden Sie sich mindestens 3–4 Wochen vor dem Termin. Drehbuch und Vertrag stehen meist 1–2 Wochen vor der Veranstaltung. Eine Antwort mit konkretem Preis erhalten Sie in der Regel innerhalb von 30 Minuten.'],
        ],
        'tresc': f'''
<h2 id="hamburg">Hamburg: Hafen, Medien, Handel</h2>

<p>Hamburg lebt vom Hafen, von der Luftfahrt, vom Handel und von einer Medien- und Digitalbranche, die jedes Jahr Zehntausende in die Messehallen zieht. Veranstaltungen sind hier oft international besetzt: Reedereien, Zulieferer, Agenturen, Start-ups. Der Roboter spricht Deutsch, Englisch und jede andere Sprache und begrüßt die Gäste so, dass sie stehen bleiben.</p>

<p>Wir bringen den Unitree G1 mit Operator in die Hansestadt. Im Preis ab 2.500&nbsp;€ pro Veranstaltungstag sind Anfahrt, Branding mit Logo und QR-Code sowie die Haftpflichtversicherung enthalten.</p>

<h2 id="messen-hamburg">Messen und Locations in Hamburg, zu denen der Roboter passt</h2>

<h3>Messehallen und CCH</h3>

<p>Auf dem Messegelände zwischen Fernsehturm und Planten un Blomen finden die großen Hamburger Fachmessen statt. Auf der <strong>SMM</strong>, der Leitmesse der maritimen Wirtschaft, kann der G1 für die Automatisierung stehen, über die an den Ständen gesprochen wird. Auf der <strong>INTERNORGA</strong> begrüßt er Gastronomen und Hoteliers und zeigt, wie ein Roboter als Gastgeber wirkt. Auf der <strong>WindEnergy Hamburg</strong> holt er Fachbesucher aus dem Gang an Ihren Stand. Das <strong>CCH – Congress Center Hamburg</strong> nebenan ist der Ort für Kongresse und Hauptversammlungen: Hier kündigt der Roboter Redner an und moderiert Übergänge.</p>

<h3>OMR Festival</h3>

<p>Beim Treffen der Digital- und Marketingbranche zählt, wer gefilmt wird. Ein Roboter mit Ihrem Branding ist ein Motiv, das Besucher von selbst aufnehmen und teilen. Wir planen dafür feste Zeiten am Stand und Wege durch die Halle, auf denen er Besucher zu Ihnen führt.</p>

<h3>Hafen und Elbe</h3>

<p><strong>Fischauktionshalle</strong>, <strong>Schuppen 52</strong> und die Kreuzfahrtterminals sind die Kulissen für Firmenfeiern, Produktpremieren und Jubiläen. Der G1 empfängt die Gäste am Eingang, eröffnet den Abend auf der Bühne und geht danach durch die Reihen. In der <strong>Handelskammer Hamburg</strong> und in den Konferenzhotels an der Alster übernimmt er Begrüßung und Programmansage.</p>

<wideo/>

<h2 id="praxis-hamburg">Praktisches für Veranstalter</h2>

<p>Der Roboter braucht eine ebene Fläche von etwa 2×2&nbsp;m und eine 230-V-Steckdose, mehr nicht. Internet oder besondere Beleuchtung sind nicht nötig. Der Operator bringt Ersatzakkus mit und wechselt sie während der Veranstaltung, ohne dass die Show unterbricht. Er ist die ganze Zeit beim Roboter, achtet auf Abstände und hält sich im Hintergrund, wenn es ruhiger wird. Wie eine Buchung von der Anfrage bis zur Rechnung abläuft, beschreibt die Seite <a href="humanoiden-roboter-mieten.html">Humanoiden Roboter mieten</a>.</p>

<h2 id="referenzen">Referenzen: Dresden und eine Hafenstadt an der Ostsee</h2>

{para('Dresdner Schlössernacht (Dresden) und LEX AI am Langen Markt in Danzig.', 'realizacja-gala-zdjecia-gosci', 'realizacja-lexai-starowka')}

<p>Bei der Dresdner Schlössernacht fotografierten sich die Gäste des Balls mit dem Roboter im Paillettensmoking. Wie ein Einsatz im öffentlichen Raum aussieht, zeigt die <a href="case-study-lexai.html">Case Study LEX AI</a>: In der Danziger Altstadt begrüßte der Roboter Passanten am Neptunbrunnen, gab ihnen die Hand und beantwortete Fragen. Daraus wurden ein Beitrag in der Nachrichtensendung Teleexpress (TVP) und eine Reportage von TVP Danzig. Mehr unter <a href="referenzen-videos.html">Referenzen und Videos</a>.</p>
''',
    },

    'koeln': {
        'opis': 'Humanoiden Roboter Unitree G1 in Köln mieten: für gamescom, DMEXCO, FIBO, Anuga und Firmenevents. Operator und Anfahrt im Preis, ab 2.500 € pro Tag.',
        'lead': 'Der Unitree G1 kommt nach Köln und ins Rheinland: auf die Koelnmesse in Deutz, ins Confex, in die Flora oder ins Palladium.',
        'foto': ('realizacja-gala-detal', SCHLOESSERNACHT),
        'czytaj': [['roboter-mieten-duesseldorf.html', 'Roboter mieten in Düsseldorf'], ['roboter-mieten-frankfurt.html', 'Roboter mieten in Frankfurt'],
                   ['angebot-messen.html', 'Roboter für Messen'], ['roboter-show.html', 'Roboter-Show'],
                   ['roboter-mieten-preise.html', 'Preise und Kosten']],
        'pytania': [
            ['Kommen Sie auch nach Bonn, Leverkusen oder Aachen?', 'Ja. Wir fahren nach Köln und ins gesamte Rheinland, nach Bonn, Leverkusen, Bergisch Gladbach oder Aachen. Die Anfahrt ist im Preis enthalten.'],
            ['Hält der Roboter einen ganzen gamescom-Tag durch?', 'Ja. Der Roboter arbeitet mit Wechselakkus. Der Operator tauscht sie während des Messetags, die Show unterbricht nicht zum Laden. Bei sehr vollen Gängen bleibt der Operator direkt am Roboter und achtet auf Abstände.'],
            ['Kann der Roboter auf einer Karnevalssitzung auftreten?', 'Ja. Er zieht mit ein, begrüßt den Saal, kündigt den nächsten Programmpunkt an und tanzt eine Choreografie. Branding und Auftritt stimmen wir auf Ihre Gesellschaft oder Ihr Unternehmen ab.'],
            ['Was kostet der Roboter für mehrere Messetage in Köln?', 'Ab 2.500 € pro Veranstaltungstag. Ab zwei Tagen gibt es 15 % Rabatt auf jeden Tag. Operator, Anfahrt, Branding und Haftpflichtversicherung sind enthalten.'],
        ],
        'tresc': f'''
<h2 id="koeln">Köln: Publikum, das mitmacht</h2>

<p>Köln ist Medienstadt, Messestadt und die Stadt, in der Menschen ohne Umschweife auf etwas Neues zugehen. Für einen Roboter, der Hände schüttelt, tanzt und für Fotos posiert, ist das die beste Voraussetzung: Die Traube bildet sich hier schneller als anderswo. Dazu kommen Publikumsmessen mit Hunderttausenden Besuchern, auf denen genau diese Fähigkeit zählt.</p>

<p>Der Unitree G1 kommt mit Operator, Drehbuch und Ihrem Branding nach Köln. Ein Veranstaltungstag kostet ab 2.500&nbsp;€, Anfahrt und Haftpflichtversicherung sind enthalten.</p>

<h2 id="koelnmesse">Koelnmesse: fünf Messen, fünf Aufgaben</h2>

<p>Je nach Messe übernimmt der Roboter eine andere Aufgabe. So kann sie aussehen:</p>

<ul>
  <li><strong>gamescom</strong> — Das Publikum kommt, um zu filmen. Der G1 tanzt, gibt High Fives und wird zum Motiv, das Ihren Stand in die Feeds der Besucher bringt.</li>
  <li><strong>DMEXCO</strong> — Auf der Digitalmesse ist der Roboter der Gesprächseinstieg: Er spricht Besucher im Gang an und übergibt an Ihr Vertriebsteam.</li>
  <li><strong>FIBO</strong> — Auf der Fitnessmesse macht er Übungen mit, fordert zum Mitmachen auf und steht mitten im Trainingsbereich.</li>
  <li><strong>Anuga und ISM</strong> — Auf den Lebensmittelmessen begrüßt er Einkäufer aus vielen Ländern in ihrer Sprache und lädt zur Verkostung ein.</li>
  <li><strong>ORGATEC</strong> — Zwischen Büromöbeln und Arbeitswelten steht er für die Frage, wie Menschen und Maschinen künftig zusammenarbeiten.</li>
</ul>

<p>Für Kongresse neben der Messe gibt es das <strong>Confex</strong>, das Konferenzzentrum der Koelnmesse. Dort übernimmt der Roboter Begrüßung und Programmansagen.</p>

<wideo/>

<h2 id="locations-koeln">Abendveranstaltungen und Firmenevents</h2>

<p>Für Galas und Preisverleihungen stehen in Köln die <strong>Flora</strong>, der <strong>Gürzenich</strong> und die <strong>Wolkenburg</strong> bereit. Dort arbeitet der Roboter im eleganten Branding als Gastgeber am Eingang und auf der Bühne. Für Kick-offs, Sommerfeste und Produktshows werden häufig das <strong>Palladium</strong>, das <strong>E-Werk</strong> und die <strong>XPOST</strong> gebucht, Industriehallen mit Platz für eine Choreografie. In der <strong>LANXESS arena</strong> und in den Business-Bereichen des Stadions kann er vor großem Publikum auftreten.</p>

<p>Die technischen Anforderungen sind überall gleich und auf der Seite <a href="unitree-g1-mieten.html">Unitree G1</a> beschrieben. Der Operator bleibt während des gesamten Einsatzes beim Roboter.</p>

<h2 id="karneval">Karneval und Session</h2>

<p>Zwischen dem 11.11. und Aschermittwoch suchen Gesellschaften und Unternehmen Programmpunkte, die es so noch nicht gab. Der Roboter zieht in den Saal ein, begrüßt das Publikum, sagt den nächsten Auftritt an und tanzt. Das Drehbuch schreiben wir gemeinsam, das Branding richtet sich nach Ihren Farben. Die Bausteine einer Bühnennummer stehen auf der Seite <a href="roboter-show.html">Roboter-Show</a>.</p>

<h2 id="referenzen">Referenzen: Dresdner Schlössernacht und Fitnessclub</h2>

{para('Dresdner Schlössernacht (Dresden) und YEAH GYM in Breslau.', 'realizacja-gala-detal', 'realizacja-yeah-gym-silownia')}

<p>Bei der Dresdner Schlössernacht trug der Roboter Paillettensmoking und Krone und bewegte sich den ganzen Abend zwischen den Gästen. Für die FIBO ist der Einsatz im Fitnessclub YEAH GYM der passende Vergleich: der Roboter im Club-Shirt mitten im Trainingsbereich. Über 100 Veranstaltungen in fünf Ländern stehen unter <a href="referenzen-videos.html">Referenzen und Videos</a>.</p>
''',
    },

    'frankfurt': {
        'opis': 'Humanoiden Roboter Unitree G1 in Frankfurt mieten: für Automechanika, Light + Building, Buchmesse und Kongresse. Ab 2.500 € pro Tag, Anfahrt inklusive.',
        'lead': 'Der Unitree G1 kommt nach Frankfurt und ins Rhein-Main-Gebiet: auf das Messegelände, ins Kap Europa, in die Alte Oper oder in den Palmengarten.',
        'foto': ('realizacja-gala-palac', SCHLOESSERNACHT),
        'czytaj': [['roboter-mieten-koeln.html', 'Roboter mieten in Köln'], ['roboter-mieten-muenchen.html', 'Roboter mieten in München'],
                   ['angebot-konferenzen-galas.html', 'Roboter für Konferenzen und Galas'], ['roboter-gaesteempfang.html', 'Roboter für den Gästeempfang'],
                   ['roboter-mieten-preise.html', 'Preise und Kosten']],
        'pytania': [
            ['Kommen Sie auch nach Wiesbaden, Mainz oder Darmstadt?', 'Ja. Wir fahren ins gesamte Rhein-Main-Gebiet, zum RheinMain CongressCenter in Wiesbaden, nach Mainz, Darmstadt, Offenbach, Eschborn oder Bad Homburg. Die Anfahrt ist im Preis enthalten.'],
            ['Passt ein Roboter zu einer Veranstaltung einer Bank oder Kanzlei?', 'Ja, wenn der Charakter stimmt. Für förmliche Anlässe legen wir einen zurückhaltenden, sachlichen Auftritt fest: Begrüßung am Empfang, Ansage der Redner, Fotomoment. Was der Roboter sagt, stimmen wir vorher mit Ihnen ab.'],
            ['In welchen Sprachen begrüßt der Roboter internationale Gäste?', 'In jeder. Der Roboter spricht Deutsch, Englisch und jede andere Sprache und wechselt während der Veranstaltung. Für Gäste, die über den Flughafen anreisen, ist das oft der erste Eindruck Ihrer Veranstaltung.'],
            ['Wie läuft die Bezahlung ab?', 'Die Reservierung erfolgt ohne Anzahlung. Die Rechnung stellen wir erst nach der Veranstaltung, bei Bedarf mit längerem Zahlungsziel. Ein Veranstaltungstag kostet ab 2.500 €, ab zwei Tagen 15 % weniger pro Tag.'],
        ],
        'tresc': f'''
<h2 id="frankfurt">Frankfurt: internationale Gäste, knappe Zeit</h2>

<p>Nach Frankfurt kommen Menschen für zwei Tage Messe, einen Kongress oder ein Abendessen und fliegen danach weiter. Banken, Kanzleien, Beratungen und Industrieunternehmen laden hier Gäste aus aller Welt ein. Was von einer Veranstaltung bleibt, entscheidet sich in wenigen Momenten. Ein humanoider Roboter, der jeden Gast in seiner Sprache begrüßt, ist ein solcher Moment.</p>

<p>Den Unitree G1 bringen wir mit Operator, Drehbuch und Branding ins Rhein-Main-Gebiet. Ein Veranstaltungstag kostet ab 2.500&nbsp;€. Anfahrt, Logo und QR-Code auf der Brust sowie die Haftpflichtversicherung sind enthalten. Die Rechnung kommt nach der Veranstaltung.</p>

<h2 id="messe-frankfurt">Messe Frankfurt: Aufgaben nach Messe</h2>

<p>Was der Roboter an Ihrem Stand übernehmen kann, hängt von der Messe ab. Vier Beispiele:</p>

<h3>Automechanika</h3>
<p>Werkstattausrüster und Zulieferer zeigen Technik, die man anfassen kann. Der G1 geht über die Standfläche, spricht Besucher an und führt sie zur Vorführung.</p>

<h3>Light + Building und ISH</h3>
<p>Auf den Messen für Gebäudetechnik stehen Automatisierung und Vernetzung im Mittelpunkt. Der Roboter erklärt Ihre Kernbotschaft in zwei Sätzen und übergibt an die Fachberater.</p>

<h3>Frankfurter Buchmesse</h3>
<p>Fachbesucher an den ersten Tagen, Publikum am Wochenende: Der Roboter kündigt Lesungen an, begrüßt Gäste am Stand und wird am Publikumswochenende zum Fotomotiv.</p>

<h3>Ambiente und Heimtextil</h3>
<p>Einkäufer aus vielen Ländern laufen an Hunderten Ständen vorbei. Der G1 spricht sie in ihrer Sprache an und lädt in den Showroom ein.</p>

<p>Die Planung eines Messeauftritts, vom Platz am Stand bis zur Übergabe an den Vertrieb, beschreibt die Seite <a href="angebot-messen.html">Roboter für Messen</a>.</p>

<wideo/>

<h2 id="locations-frankfurt">Kongresse, Galas, Empfänge</h2>

<ul>
  <li><strong>Kap Europa und Congress Center Messe Frankfurt</strong> — Kongresse und Hauptversammlungen: Der Roboter begrüßt im Foyer und kündigt die Redner an.</li>
  <li><strong>Alte Oper</strong> — Galas und Preisverleihungen in festlichem Rahmen, der Roboter im eleganten Branding.</li>
  <li><strong>Gesellschaftshaus Palmengarten</strong> — Jubiläen, Bälle und Abendveranstaltungen mit Bühne.</li>
  <li><strong>Jahrhunderthalle</strong> — Mitarbeiterveranstaltungen und Kick-offs mit großem Publikum.</li>
  <li><strong>Klassikstadt</strong> — Kundenabende und Produktpräsentationen zwischen Oldtimern.</li>
</ul>

<p>Die Anforderungen an den Ort sind an allen genannten Adressen dieselben (<a href="unitree-g1-mieten.html">technische Daten des Unitree G1</a>). Mehr dazu, wie der Roboter durch einen Abend führt, steht unter <a href="angebot-konferenzen-galas.html">Roboter für Konferenzen und Galas</a>.</p>

<h2 id="empfang-frankfurt">Der Roboter am Empfang</h2>

<p>Bei Veranstaltungen mit internationalen Gästen ist der Eingang der wichtigste Platz für den Roboter. Er begrüßt, weist den Weg zum Saal und beantwortet Fragen zum Programm. Vor der Veranstaltung spielen wir ihm ein, wer spricht, was auf der Agenda steht und aus welchem Anlass Sie zusammenkommen.</p>

<h2 id="referenzen">Referenzen: Ball in Dresden, Anlegerkonferenz</h2>

{para('Dresdner Schlössernacht: der Roboter im Ballsaal und unter den Gästen.', 'realizacja-gala-palac', 'realizacja-gala-wsrod-gosci')}

<p>In Deutschland arbeitete der Roboter bei der Dresdner Schlössernacht, im Paillettensmoking mit Krone, auf dem roten Teppich und im Ballsaal. Für Finanzveranstaltungen ist die <a href="case-study-wallstreet.html">Case Study WallStreet 30</a> der passende Vergleich, eine Konferenz für Privatanleger. Alle Einsätze zeigen die <a href="referenzen-videos.html">Referenzen und Videos</a>.</p>
''',
    },

    'duesseldorf': {
        'opis': 'Humanoiden Roboter Unitree G1 in Düsseldorf mieten: für MEDICA, EuroShop, boot, Kongresse im CCD und Galas. Ab 2.500 € pro Tag, Anfahrt inklusive.',
        'lead': 'Der Unitree G1 kommt nach Düsseldorf und an den Niederrhein: auf das Messegelände in Stockum, ins CCD, ins Areal Böhler oder auf die Rheinterrasse.',
        'foto': ('realizacja-gala-wsrod-gosci', SCHLOESSERNACHT),
        'czytaj': [['roboter-mieten-koeln.html', 'Roboter mieten in Köln'], ['roboter-mieten-frankfurt.html', 'Roboter mieten in Frankfurt'],
                   ['angebot-messen.html', 'Roboter für Messen'], ['ki-roboter-veranstaltung.html', 'KI-Roboter, der Deutsch spricht'],
                   ['roboter-mieten-preise.html', 'Preise und Kosten']],
        'pytania': [
            ['Kommen Sie auch nach Neuss, Duisburg oder Essen?', 'Ja. Wir fahren nach Düsseldorf, an den Niederrhein und ins Ruhrgebiet, nach Neuss, Ratingen, Duisburg, Essen, Krefeld oder Wuppertal. Die Anfahrt ist im Preis enthalten.'],
            ['Kann der Roboter japanische Gäste auf Japanisch begrüßen?', 'Ja. Der Roboter spricht jede Sprache und wechselt während der Veranstaltung. Für Düsseldorfer Unternehmen mit japanischen Partnern oder Gästen stimmen wir Begrüßung und Ansagen auf Japanisch, Deutsch und Englisch ab.'],
            ['Darf der Roboter in den Messehallen frei herumlaufen?', 'Er bewegt sich auf Ihrer Standfläche und, wo es der Veranstalter erlaubt, in den Gängen davor. Der Operator ist durchgehend dabei, achtet auf Abstände und entscheidet, was bei vollem Gang möglich ist. Die Haftpflichtversicherung ist im Preis enthalten.'],
            ['Was kostet der Roboter für die vier Tage der MEDICA?', 'Ab 2.500 € pro Veranstaltungstag, bei mehreren Tagen 15 % weniger pro Tag. Den genauen Betrag nennen wir Ihnen nach einem kurzen Gespräch, meist innerhalb von 30 Minuten.'],
        ],
        'tresc': f'''
<h2 id="duesseldorf">Düsseldorf: Messestadt mit kurzen Wegen</h2>

<p>Das Düsseldorfer Messegelände liegt zwischen Rhein, Flughafen und Arena, und ein großer Teil der Wirtschaft in der Stadt lebt vom Messegeschäft: Medizintechnik, Handel, Kunststoff, Verpackung, Mode. Aussteller kommen aus der ganzen Welt, die Gänge sind voll, die Gespräche kurz. Ein Roboter, der Besucher anspricht und an Ihren Stand bringt, verschafft Ihrem Team die ersten Sekunden, auf die es ankommt.</p>

<p>Wir kommen mit dem Unitree G1, einem Operator und Ihrem Branding. Der Preis beginnt bei 2.500&nbsp;€ pro Veranstaltungstag, Anfahrt und Haftpflichtversicherung eingeschlossen. Bei Messen über mehrere Tage sinkt der Tagespreis um 15&nbsp;%.</p>

<h2 id="messe-duesseldorf">Messe Düsseldorf: Welche Rolle der Roboter übernehmen kann</h2>

<ul>
  <li><strong>MEDICA</strong> — Auf der Medizinmesse arbeitet der Roboter als mehrsprachiger Gastgeber: Er begrüßt Fachbesucher aus vielen Ländern und nennt in einem Satz, was es an Ihrem Stand zu sehen gibt.</li>
  <li><strong>EuroShop</strong> — Auf der Messe des Handels ist ein Roboter, der Kunden empfängt und berät, selbst ein Exponat: So kann Begrüßung im Geschäft aussehen.</li>
  <li><strong>boot</strong> — Publikumsmesse mit Familien und Wassersportfans. Der G1 gibt die Hand, posiert für Fotos und sorgt für Betrieb vor dem Stand.</li>
  <li><strong>K und interpack</strong> — Zwischen Maschinen für Kunststoff und Verpackung führt er Besucher zur Live-Vorführung und überbrückt die Wartezeit.</li>
  <li><strong>ProWein und CARAVAN SALON</strong> — Der Roboter lädt zur Verkostung oder zur Fahrzeugbesichtigung ein und spricht Besucher an, die sonst vorbeigehen.</li>
</ul>

<wideo/>

<h2 id="japan">Düsseldorf und Japan</h2>

<p>In Düsseldorf sitzen besonders viele japanische Unternehmen, und zu Firmenveranstaltungen kommen regelmäßig Gäste und Delegationen aus Japan. Der Roboter begrüßt sie auf Japanisch, wechselt für die deutschen Kolleginnen und Kollegen ins Deutsche und für alle anderen ins Englische. Wie die Sprachfunktion arbeitet und was der Roboter über Ihr Unternehmen wissen kann, steht auf der Seite <a href="ki-roboter-veranstaltung.html">KI-Roboter, der Deutsch spricht</a>.</p>

<h2 id="locations-duesseldorf">Locations außerhalb der Messe</h2>

<ul>
  <li><strong>CCD Congress Center Düsseldorf</strong> — Kongresse direkt am Messegelände: Begrüßung im Foyer, Ansage der Redner.</li>
  <li><strong>Areal Böhler</strong> — Industriehallen für Markenevents, Kick-offs und Produktshows mit Platz für eine Choreografie.</li>
  <li><strong>Rheinterrasse</strong> — Galas, Bälle und Jubiläen mit Blick auf den Rhein.</li>
  <li><strong>Classic Remise</strong> — Kundenabende zwischen Oldtimern im alten Ringlokschuppen.</li>
  <li><strong>Merkur Spiel-Arena</strong> — Großveranstaltungen und Business-Bereiche für Firmenevents.</li>
</ul>

<p>Was der Roboter am Einsatzort braucht, haben wir auf der Seite <a href="unitree-g1-mieten.html">Unitree G1</a> zusammengefasst. Der Operator bleibt die ganze Zeit dabei.</p>

<h2 id="referenzen">Referenzen: Dresden und zwei Messestände</h2>

{para('Rekord-Gruppe auf der Messe MSPO (Kielce) und Dream-Med auf der Warsaw Medical Expo (Warschau).', 'realizacja-grupa-rekord-mspo', 'realizacja-dream-med-expo')}

<p>In Deutschland war der Roboter bei der Dresdner Schlössernacht im Einsatz. Für Düsseldorfer Messen sind zwei Stände der passende Vergleich: Auf der Industriemesse MSPO stellte der Roboter zwei Tage lang die Gesellschaften der Rekord-Gruppe vor und lud Besucher aus dem Gang zur Vorführung ein, beschrieben in der <a href="case-study-grupa-rekord-mspo.html">Case Study MSPO</a>. Auf der Warsaw Medical Expo arbeitete er am Stand von Dream-Med. Weitere Einsätze unter <a href="referenzen-videos.html">Referenzen und Videos</a>.</p>
''',
    },

    'dresden': {
        'opis': 'Humanoiden Roboter Unitree G1 in Dresden mieten, bekannt von der Dresdner Schlössernacht. Für Galas, Kongresse und Firmenevents, ab 2.500 € pro Tag.',
        'lead': 'In Dresden war unser Roboter schon im Einsatz: bei der Dresdner Schlössernacht, im Paillettensmoking mit Krone. Der Unitree G1 kommt zu Ihrer Veranstaltung in Dresden und ganz Sachsen, mit Operator, Anfahrt und Branding im Preis.',
        'foto': ('realizacja-gala-palac', SCHLOESSERNACHT),
        'czytaj': [['roboter-mieten-berlin.html', 'Roboter mieten in Berlin'], ['roboter-mieten-muenchen.html', 'Roboter mieten in München'],
                   ['angebot-konferenzen-galas.html', 'Roboter für Konferenzen und Galas'], ['referenzen-videos.html', 'Referenzen und Videos'],
                   ['roboter-mieten-preise.html', 'Preise und Kosten']],
        'pytania': [
            ['War der Roboter schon in Dresden im Einsatz?', 'Ja, bei der Dresdner Schlössernacht. Der Roboter trug Paillettensmoking und Krone und war auf dem roten Teppich, im Ballsaal und mitten unter den Gästen unterwegs.'],
            ['Kommen Sie auch nach Chemnitz, Meißen oder Görlitz?', 'Ja. Wir fahren nach Dresden und in ganz Sachsen, nach Radebeul, Meißen, Pirna, Freiberg, Chemnitz, Bautzen oder Görlitz. Die Anfahrt ist im Preis enthalten.'],
            ['Passt ein Roboter in ein historisches Schloss oder Palais?', 'Ja. Der Roboter braucht nur eine ebene Fläche von rund 2×2 m und eine Steckdose. Er bewegt sich auf Teppich, Parkett und Hotelböden. Den Weg durch das Haus stimmen wir vorher mit Ihnen ab, und der Operator bleibt die ganze Zeit dabei.'],
            ['Eignet sich der Roboter für Veranstaltungen der Halbleiterbranche?', 'Ja. Für Fachpublikum legen wir einen sachlichen Auftritt fest und spielen dem Roboter Wissen über Ihr Unternehmen ein. Er begrüßt Gäste und Delegationen auf Deutsch, Englisch und in jeder anderen Sprache.'],
        ],
        'tresc': f'''
<h2 id="schloessernacht">Dresdner Schlössernacht: unser Einsatz in Dresden</h2>

<p>Bei der Dresdner Schlössernacht stand der Roboter nicht am Rand, sondern mitten im Geschehen. Im Paillettensmoking mit Krone begrüßte er die Gäste auf dem roten Teppich, bewegte sich durch den Ballsaal und stand bis in die Nacht vor dem Palais für Fotos bereit. Das Branding war auf den Anlass abgestimmt: festlich statt technisch.</p>

{para('Dresdner Schlössernacht: auf dem roten Teppich und im Gespräch mit den Gästen.', 'realizacja-gala-czerwony-dywan', 'realizacja-gala-zdjecia-gosci')}

<p>Der Abend zeigt, was den Unterschied macht. Derselbe Roboter kann als Dekoration in der Ecke stehen oder Teil des Programms sein. Charakter, Texte und Wege durch den Raum legen wir vor jeder Veranstaltung mit dem Auftraggeber fest.</p>

{para('Im Ballsaal und im Detail: Paillettensmoking und Krone als Branding des Abends.', 'realizacja-gala-palac', 'realizacja-gala-detal')}

<h2 id="dresden">Dresden: Barockkulisse und Chipindustrie</h2>

<p>Dresden hat zwei Seiten, und beide laden ein. Die eine sind Schlösser, Palais und Säle, in denen Bälle, Jubiläen und Preisverleihungen stattfinden. Die andere ist der Hightech-Standort: Im Norden der Stadt arbeiten die Halbleiterwerke, dazu kommen die Technische Universität und zahlreiche Forschungsinstitute. Für beide Seiten haben wir den passenden Auftritt, festlich im Smoking oder sachlich im Firmen-Shirt.</p>

<wideo/>

<h2 id="locations-dresden">Wo der Roboter in Dresden auftreten kann</h2>

<ul>
  <li><strong>Elbschlösser</strong> — Schloss Albrechtsberg, Lingnerschloss und Schloss Eckberg: Empfänge, Bälle und Hochzeiten über der Elbe.</li>
  <li><strong>Internationales Congress Center Dresden</strong> — Kongresse am Elbufer: Begrüßung im Foyer, Ansage der Redner.</li>
  <li><strong>MESSE DRESDEN</strong> — Fach- und Publikumsmessen im Ostragehege: Der Roboter holt Besucher an den Stand.</li>
  <li><strong>Gläserne Manufaktur</strong> — Kundenabende und Produktpräsentationen, bei denen Technik das Thema ist.</li>
  <li><strong>Deutsches Hygiene-Museum und Kulturpalast</strong> — Tagungen, Festakte und Abendveranstaltungen im Zentrum.</li>
</ul>

<p>Die technischen Anforderungen stehen auf der Seite <a href="unitree-g1-mieten.html">Unitree G1</a>. Der Operator bleibt den ganzen Einsatz über beim Roboter.</p>

<h2 id="silicon-saxony">Für Unternehmen im Silicon Saxony</h2>

<p>Werkseröffnung, Tag der offenen Tür, Karrieremesse oder Empfang für eine Delegation: Der Roboter begrüßt die Gäste, erklärt in Ihren Worten, was das Unternehmen macht, und wechselt zwischen Deutsch, Englisch und jeder anderen Sprache. Für Recruiting-Formate beschreibt die Seite <a href="roboter-employer-branding.html">Roboter für Karrieremessen</a> den Ablauf, für Eröffnungen die Seite <a href="roboter-eroeffnung.html">Roboter für Eröffnungen</a>.</p>

<h2 id="preis-dresden">Preis und Buchung</h2>

<p>Ein kompletter Veranstaltungstag kostet ab 2.500&nbsp;€, mit Operator, Anfahrt, Branding und Haftpflichtversicherung. Kürzere Auftritte, etwa zwei Stunden zum Empfang, kalkulieren wir individuell und immer günstiger als einen ganzen Tag. Eine Anzahlung gibt es nicht, die Rechnung kommt nach der Veranstaltung. Alle Details stehen unter <a href="roboter-mieten-preise.html">Preise und Kosten</a>.</p>
''',
    },
}

# Strony miast z szablonu: poza indeksem, dopóki nie dostaną własnej treści.
POZA_INDEKSEM = ['bremen', 'dortmund', 'essen', 'hannover', 'leipzig', 'nuernberg', 'stuttgart']


def wczytaj(plik):
    s = plik.read_text(encoding='utf-8')
    m = re.match(r'(<!--\s*)(\{.*?\})(\s*-->)', s, re.S)
    return json.loads(m.group(2)), s[m.end():]


def zapisz(plik, dane, tresc):
    plik.write_text('<!--\n' + json.dumps(dane, ensure_ascii=False, indent=2) + '\n-->\n' + tresc.strip('\n') + '\n', encoding='utf-8')


def main():
    for miasto, m in MIASTA.items():
        plik = ZRODLA / f'roboter-mieten-{miasto}.html'
        d, _ = wczytaj(plik)
        d['opis'] = m['opis']
        d['robots'] = 'index, follow'
        d['lead'] = m['lead']
        d['foto'] = {'plik': m['foto'][0], 'alt': ALT[m['foto'][0]], 'podpis': m['foto'][1]}
        d['pytania'] = m['pytania']
        d['czytaj'] = m['czytaj']
        d['cta_tekst'] = 'Schreiben Sie uns oder rufen Sie an. Eine Antwort mit Preis und Verfügbarkeit erhalten Sie meist innerhalb von 30 Minuten.'
        zapisz(plik, d, m['tresc'])
        slowa = len(re.sub(r'<[^>]+>', ' ', m['tresc']).split())
        print(f'{plik.name}: własna treść, {slowa} słów')
    for miasto in POZA_INDEKSEM:
        plik = ZRODLA / f'roboter-mieten-{miasto}.html'
        d, tresc = wczytaj(plik)
        d['robots'] = 'noindex, follow'
        zapisz(plik, d, tresc)
        print(f'{plik.name}: noindex')


if __name__ == '__main__':
    main()
