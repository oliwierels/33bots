# -*- coding: utf-8 -*-
"""Strony miast 33bots.at pisane osobno, nie z szablonu (11.2026).

Jedenaście stron miast 33bots.at powstało z jednego
szablonu (35–40% tekstu wspólnego z innymi podstronami, Wien–Graz 59% podobieństwa). Tutaj pięć
największych rynków — Wien, Graz, Salzburg, Linz, Innsbruck — ma własną treść: lokalne targi
i kongresy, sale, typowy przebieg i pytania. Pozostałe sześć stron miast dostaje noindex i wypada
z mapy strony, dopóki nie zostaną napisane osobno.

Fakty o 33bots wyłącznie z rynki.py (AT): od 2.300 € netto za dzień, −15% od dwóch dni, transport
w całej Austrii, operator, branding (logo, kod QR) i OC w cenie, bez zaliczki, faktura po wydarzeniu.
Targi i sale — powszechnie znane, bez twierdzeń, że na nich pracowaliśmy.

    python3 tresci/zagranica/miasta_at.py     # potem buduj_glowna.py at, buduj_podstrony.py at, buduj_mape.py
"""
import json
import re
from pathlib import Path

ZRODLA = Path(__file__).resolve().parent / 'podstrony' / 'at'

ALT = {
    'realizacja-gala-palac': 'Humanoider Roboter im Smoking im Ballsaal eines Palais',
    'realizacja-gala-wsrod-gosci': 'Humanoider Roboter zwischen Gala-Gästen',
    'realizacja-gala-detal': 'Nahaufnahme des humanoiden Roboters mit Krone und Pailletten-Smoking',
    'realizacja-gala-czerwony-dywan': 'Humanoider Roboter im Pailletten-Smoking auf dem roten Teppich einer Gala',
    'realizacja-gala-zdjecia-gosci': 'Galagäste fotografieren den humanoiden Roboter an der Sponsorenwand',
    'realizacja-women-in-tech-tlum': 'Publikum filmt den humanoiden Roboter mit Handys',
    'realizacja-women-in-tech-wybieg': 'Humanoider Roboter auf dem rosa Laufsteg des Women in Tech Summit',
    'realizacja-lexai-starowka': 'Humanoider Roboter auf der Straße, Passanten fotografieren',
    'realizacja-grupa-rekord-mspo': 'Humanoider Roboter in den Farben der Rekord-Gruppe am Stand der Messe MSPO in Kielce',
    'realizacja-dream-med-expo': 'Humanoider Roboter am Stand von Dream-Med auf der Warsaw Medical Expo',
    'realizacja-matys-stoisko': 'Humanoider Roboter im Matys-T-Shirt am Stand des Bauträgers',
    'realizacja-kopernik-noc': 'Humanoider Roboter in der Ausstellung des Kopernikus-Wissenschaftszentrums bei einem Abend für Erwachsene',
    'realizacja-przelewice-noc-bajek': 'Humanoider Roboter in beleuchteten Arkaden während der Märchennacht in Przelewice',
    'realizacja-jednorozec-zachod': 'Humanoider Roboter bei einer Parade im Freien bei Sonnenuntergang',
    'realizacja-spotkanie-biznesowe': 'Humanoider Roboter bei einem Business-Meeting auf der Terrasse',
    'realizacja-event-nad-woda': 'Humanoider Roboter winkt auf einer Terrasse über einem Jachthafen',
}


def para(podpis, a, b):
    return (f'<para podpis="{podpis}"><kadr plik="{a}" alt="{ALT[a]}"/>'
            f'<kadr plik="{b}" alt="{ALT[b]}"/></para>')


SCHLOESSERNACHT = '<b>Dresdner Schlössernacht</b> · Dresden'
ANFRAGE = '<a href="index.html#kontakt">Termin und Preis anfragen</a>'

MIASTA = {
    'wien': {
        'opis': 'Humanoiden Roboter Unitree G1 in Wien mieten: für Messe Wien, Austria Center, Hofburg und Firmenevents. Ab 2.300 € netto pro Tag, Transport inklusive.',
        'lead': 'Der Unitree G1 kommt zu Ihrer Veranstaltung in Wien: auf die Messe im Prater, zum Kongress im Austria Center, zur Gala in der Hofburg. Operator, Transport und Branding sind im Preis.',
        'foto': ('realizacja-gala-wsrod-gosci', SCHLOESSERNACHT),
        'czytaj': [['roboter-mieten-graz.html', 'Roboter mieten in Graz'], ['roboter-mieten-linz.html', 'Roboter mieten in Linz'],
                   ['messe-roboter-mieten.html', 'Messe-Roboter mieten'], ['humanoider-roboter-mieten.html', 'Humanoiden Roboter mieten in Österreich'],
                   ['roboter-weihnachtsfeier.html', 'Roboter für die Weihnachtsfeier']],
        'pytania': [
            ['Was kostet es, einen Roboter in Wien zu mieten?', 'Ein ganzer Veranstaltungstag kostet ab 2.300 € netto. Operator, Transport, Branding und Haftpflichtversicherung sind enthalten. Ab zwei Tagen, etwa bei einer Messe im Prater, gibt es 15 % Rabatt auf jeden Tag. Einen kürzeren Auftritt kalkulieren wir individuell.'],
            ['Kommen Sie auch ins Wiener Umland?', 'Ja. Neben allen 23 Wiener Gemeindebezirken kommen wir auch nach Schwechat, Mödling, Klosterneuburg, Baden oder Korneuburg. Einen Aufschlag pro Kilometer gibt es nicht.'],
            ['Kann der Roboter auf einem Kongress Englisch sprechen?', 'Ja. Der Roboter spricht Deutsch, Englisch und jede andere Sprache und wechselt während der Veranstaltung. Auf internationalen Kongressen begrüßt er die Teilnehmenden in ihrer Sprache und beantwortet Fragen zum Programm.'],
            ['Passt ein Roboter auf einen Wiener Ball?', 'Ja. Für festliche Anlässe legen wir einen eleganten Auftritt fest. Bei der Dresdner Schlössernacht trat der Roboter im Pailletten-Smoking mit Krone auf, auf dem roten Teppich und im Ballsaal.'],
        ],
        'tresc': f'''
<h2 id="wien">Wien: Kongressstadt mit internationalem Publikum</h2>

<p>In Wien treffen sich Fachgesellschaften, Verbände und Konzerne aus aller Welt. Wer hier einlädt, hat Gäste vor sich, die viele Kongresse und viele Empfänge kennen. Ein humanoider Roboter, der frei durch das Foyer geht, jeden Gast in seiner Sprache begrüßt und Ihr Logo auf der Brust trägt, gehört selten dazu.</p>

<p>Wir kommen mit dem Unitree G1, einem Operator und einem abgestimmten Drehbuch nach Wien. Ein ganzer Veranstaltungstag kostet ab 2.300&nbsp;€ netto, Transport, Branding und Haftpflichtversicherung eingeschlossen. Was der Roboter kann, steht auf der Seite <a href="humanoider-roboter-mieten.html">Humanoiden Roboter mieten in Österreich</a>.</p>

<h2 id="messe-wien">Messe Wien und Austria Center: Welche Aufgabe der Roboter übernimmt</h2>

<p>Die Beispiele zeigen, welche Rolle der Roboter je nach Format übernehmen kann.</p>

<ul>
  <li><strong>Fachmessen in der Messe Wien</strong> — Der G1 arbeitet an der Kante zum Gang, spricht Vorbeigehende an und übergibt an Ihr Standteam.</li>
  <li><strong>Publikumsmessen wie die Ferien-Messe oder die Vienna Autoshow</strong> — Der Roboter gibt die Hand, posiert für Fotos und sorgt für die Traube vor Ihrem Stand.</li>
  <li><strong>Kongresse im Austria Center Vienna</strong> — Begrüßung an der Registrierung, Ansage der Keynote, Fotomoment in der Kaffeepause.</li>
  <li><strong>Bildungs- und Karrieremessen in der Wiener Stadthalle</strong> — Der Roboter holt junge Besucher an den Stand und beantwortet Fragen zu Ihrem Unternehmen.</li>
</ul>

<p>Wie ein Messeauftritt geplant wird, beschreibt die Seite <a href="messe-roboter-mieten.html">Messe-Roboter mieten</a>.</p>

<wideo/>

<h2 id="locations-wien">Locations: von der Hofburg bis zur Marx Halle</h2>

<ul>
  <li><strong>Hofburg Vienna</strong> — Kongresse, Galas und Bälle in den Festsälen. Der Roboter im eleganten Branding als Gastgeber am Eingang.</li>
  <li><strong>Marx Halle</strong> — Produktlaunches, Markenevents und Firmenfeiern in der früheren Rinderhalle.</li>
  <li><strong>MuseumsQuartier</strong> — Empfänge und Abendveranstaltungen im Zentrum.</li>
  <li><strong>Palais in der Innenstadt</strong> — Jubiläen und Kundenabende in historischem Rahmen.</li>
  <li><strong>Konferenzhotels im gesamten Stadtgebiet</strong> — Tagungen, Kick-offs und Weihnachtsfeiern.</li>
</ul>

<p>Vor Ort braucht der Roboter einige Quadratmeter ebene Fläche und eine gewöhnliche Steckdose. Der Operator hat Ersatzakkus dabei, die Show läuft den ganzen Tag.</p>

<h2 id="ballsaison">Ballsaison und Galas</h2>

<p>Zwischen November und Fasching ist in Wien Ballsaison, und viele Unternehmen laden in dieser Zeit zu eigenen Festabenden. Der Roboter begrüßt die Gäste beim Einzug, steht für das Foto an der Sponsorenwand bereit und bewegt sich später durch den Saal. Charakter, Texte und Wege legen wir vorher gemeinsam fest.</p>

<h2 id="einsaetze">Referenzen: Ball in Dresden, Konferenz mit 14.000 Gästen</h2>

{para('Dresdner Schlössernacht (Dresden) und Women in Tech Summit (Warschau).', 'realizacja-gala-czerwony-dywan', 'realizacja-women-in-tech-tlum')}

<p>Bei der Dresdner Schlössernacht stand der Roboter im Pailletten-Smoking mit Krone auf dem roten Teppich, im Ballsaal und mitten unter den Gästen. Für Wiener Kongressformate ist der Women in Tech Summit in Warschau der passende Vergleich: rund 14.000 Teilnehmende, der Roboter auf dem Laufsteg und im Publikum.</p>

<p>Sie planen eine Veranstaltung in Wien? {ANFRAGE}.</p>
''',
    },

    'graz': {
        'opis': 'Humanoiden Roboter Unitree G1 in Graz mieten: für Messe Graz, Stadthalle, Helmut List Halle und Firmenevents in der Steiermark. Ab 2.300 € netto pro Tag.',
        'lead': 'Der Unitree G1 kommt nach Graz und in die Steiermark: auf das Messegelände, in die Stadthalle, in die Helmut List Halle oder zu Ihrem Firmenevent. Operator, Transport und Branding sind im Preis.',
        'foto': ('realizacja-gala-czerwony-dywan', SCHLOESSERNACHT),
        'czytaj': [['roboter-mieten-wien.html', 'Roboter mieten in Wien'], ['roboter-mieten-linz.html', 'Roboter mieten in Linz'],
                   ['messe-roboter-mieten.html', 'Messe-Roboter mieten'], ['unitree-g1-mieten.html', 'Unitree G1 mieten in Österreich'],
                   ['humanoider-roboter-mieten.html', 'Humanoiden Roboter mieten in Österreich']],
        'pytania': [
            ['Was kostet ein Roboter für ein Event in Graz?', 'Ein ganzer Veranstaltungstag kostet ab 2.300 € netto, mit Operator, Transport, Branding und Haftpflichtversicherung. Bei zwei und mehr Tagen gibt es 15 % Rabatt auf jeden Tag.'],
            ['Kommen Sie auch nach Leoben, Kapfenberg oder Leibnitz?', 'Ja. Wir kommen nach Graz und in die gesamte Steiermark, nach Leoben, Kapfenberg, Weiz, Gleisdorf oder Leibnitz. Der Transport ist im Preis enthalten.'],
            ['Passt ein humanoider Roboter zu einem Technologieunternehmen?', 'Gerade dort. Fachpublikum aus Fahrzeugtechnik und Maschinenbau will Technik in Bewegung sehen. Der G1 läuft frei, hält das Gleichgewicht und erklärt in Ihren Worten, was Ihr Unternehmen macht.'],
            ['Wie früh sollten wir für Graz reservieren?', 'Am besten zwei bis vier Wochen vor dem Termin. Die Reservierung erfolgt ohne Anzahlung, die Rechnung kommt nach der Veranstaltung.'],
        ],
        'tresc': f'''
<h2 id="graz">Graz: Technik, Hochschulen und ein Messegelände mitten in der Stadt</h2>

<p>Die Steiermark ist ein Industrie- und Forschungsland: Fahrzeugbau, Maschinenbau, Elektronik, dazu mehrere Universitäten und Fachhochschulen in Graz. Auf Firmenveranstaltungen sitzt hier ein Publikum, das Technik beurteilen kann. Ein humanoider Roboter, der wirklich läuft und frei spricht, überzeugt dieses Publikum mehr als ein Video auf dem Bildschirm.</p>

<p>Den Unitree G1 bringen wir mit Operator nach Graz. Ein Veranstaltungstag kostet ab 2.300&nbsp;€ netto. Transport, Branding mit Logo und QR-Code und die Haftpflichtversicherung sind enthalten. Die technischen Daten stehen unter <a href="unitree-g1-mieten.html">Unitree G1 mieten in Österreich</a>.</p>

<h2 id="messe-graz">Messe Congress Graz: wo der Roboter passt</h2>

<h3>Messe Graz und Stadthalle</h3>

<p>Auf Fachmessen und Kongressen in der Stadthalle arbeitet der Roboter als Gastgeber am Stand: Er spricht Besucher im Gang an und bringt sie zu Ihrem Team. Auf Publikumsmessen wie der Grazer Herbstmesse ist er der Fotopunkt für Familien.</p>

<h3>Congress Graz</h3>

<p>Im historischen Kongresshaus in der Altstadt begrüßt der Roboter die Gäste im Foyer und kündigt Rednerinnen und Redner an. Bei Abendveranstaltungen tritt er im eleganten Branding auf.</p>

<h3>Helmut List Halle und Seifenfabrik</h3>

<p>Industriehallen für Produktpräsentationen, Kick-offs und Firmenfeiern, mit Platz für eine Tanzchoreografie auf der Bühne.</p>

<wideo/>

<h2 id="unternehmen-graz">Für Unternehmen und Hochschulen</h2>

<p>Werkseröffnung, Tag der offenen Tür, Karrieremesse an der Universität oder Empfang für eine Delegation: Der Roboter begrüßt die Gäste, wechselt zwischen Deutsch, Englisch und jeder anderen Sprache und beantwortet Fragen zu Ihrem Unternehmen. Was er wissen soll, spielen wir ihm vor der Veranstaltung ein: Informationen über das Event, die Firma, ihr Angebot und die häufigsten Fragen der Gäste.</p>

<h2 id="praxis-graz">Praktisches</h2>

<p>Der Roboter braucht einige Quadratmeter ebene Fläche und eine gewöhnliche Steckdose. Der Operator kommt mit ihm, baut auf und bleibt die ganze Zeit dabei. Er hat Ersatzakkus mit, die Show unterbricht nicht zum Laden. Im Freien tritt der Roboter nur auf trockener, ebener Fläche auf.</p>

<h2 id="einsaetze">Referenzen: Dresdner Schlössernacht und zwei Messestände</h2>

{para('Rekord-Gruppe auf der Messe MSPO (Kielce) und Dream-Med auf der Warsaw Medical Expo (Warschau).', 'realizacja-grupa-rekord-mspo', 'realizacja-dream-med-expo')}

<p>Auf der Industriemesse MSPO stellte der Roboter zwei Tage lang die Unternehmen der Rekord-Gruppe vor und lud Besucher aus dem Gang zur Vorführung ein. Im deutschsprachigen Raum war er bei der Dresdner Schlössernacht im Einsatz, im Pailletten-Smoking mit Krone.</p>

<p>Sie planen eine Veranstaltung in Graz? {ANFRAGE}.</p>
''',
    },

    'salzburg': {
        'opis': 'Humanoiden Roboter Unitree G1 in Salzburg mieten: für Messezentrum, Salzburg Congress, Galas und Firmenevents. Ab 2.300 € netto pro Tag, Transport inklusive.',
        'lead': 'Der Unitree G1 kommt nach Salzburg: ins Messezentrum, in den Salzburg Congress, in ein Schloss oder ein Tagungshotel im Salzburger Land. Operator, Transport und Branding sind im Preis.',
        'foto': ('realizacja-gala-palac', SCHLOESSERNACHT),
        'czytaj': [['roboter-mieten-innsbruck.html', 'Roboter mieten in Innsbruck'], ['roboter-mieten-linz.html', 'Roboter mieten in Linz'],
                   ['messe-roboter-mieten.html', 'Messe-Roboter mieten'], ['roboter-weihnachtsfeier.html', 'Roboter für die Weihnachtsfeier'],
                   ['humanoider-roboter-mieten.html', 'Humanoiden Roboter mieten in Österreich']],
        'pytania': [
            ['Was kostet ein Roboter für ein Event in Salzburg?', 'Ab 2.300 € netto für einen ganzen Veranstaltungstag. Operator, Transport, Branding und Haftpflichtversicherung sind enthalten. Einen kürzeren Auftritt, etwa nur zum Empfang, kalkulieren wir individuell.'],
            ['Kommen Sie auch nach Zell am See, Hallein oder ins Salzkammergut?', 'Ja. Wir kommen in die Stadt Salzburg und ins gesamte Bundesland, nach Hallein, Wals-Siezenheim, Zell am See oder in ein Seminarhotel im Salzkammergut. Einen Aufschlag pro Kilometer gibt es nicht.'],
            ['Passt ein Roboter in ein historisches Schloss?', 'Ja. Er braucht nur einige Quadratmeter ebene Fläche und eine Steckdose. Den Weg durch das Haus stimmen wir vorher mit Ihnen ab, und der Operator bleibt die ganze Zeit beim Roboter.'],
            ['In welchen Sprachen begrüßt der Roboter internationale Gäste?', 'In jeder. Der Roboter spricht Deutsch, Englisch und jede andere Sprache und wechselt während der Veranstaltung.'],
        ],
        'tresc': f'''
<h2 id="salzburg">Salzburg: Gäste aus aller Welt</h2>

<p>Salzburg lebt von Gästen: Festspielpublikum, Tagungsteilnehmer, Urlauber und die Kunden einer starken Tourismus- und Handelsbranche. Veranstaltungen sind hier oft international und finden in Räumen statt, die selbst schon Eindruck machen. Der Roboter ergänzt diese Kulisse um einen Moment, den niemand erwartet.</p>

<p>Wir kommen mit dem Unitree G1 und einem Operator nach Salzburg. Der Preis beginnt bei 2.300&nbsp;€ netto pro Veranstaltungstag, Transport, Branding und Haftpflichtversicherung eingeschlossen. Die Rechnung stellen wir nach der Veranstaltung.</p>

<h2 id="messezentrum-salzburg">Messezentrum Salzburg und Salzburg Congress</h2>

<ul>
  <li><strong>„Alles für den Gast“</strong> — Auf der Fachmesse für Gastronomie und Hotellerie zeigt ein Roboter, der Gäste begrüßt, wie Empfang in Zukunft aussehen kann.</li>
  <li><strong>Fach- und Publikumsmessen im Messezentrum</strong> — Der G1 holt Besucher aus dem Gang an den Stand und übergibt an Ihr Team.</li>
  <li><strong>Salzburg Congress</strong> — Begrüßung im Foyer am Mirabellgarten, Ansage der Vortragenden, Fotomoment in der Pause.</li>
  <li><strong>Salzburgarena</strong> — Großveranstaltungen und Firmenfeiern mit Bühne.</li>
</ul>

<wideo/>

<h2 id="locations-salzburg">Schlösser, Hangar und Brauerei</h2>

<p>Für Galas und Jubiläen stehen in Salzburg Säle bereit, die es so nur hier gibt: die <strong>Residenz</strong> in der Altstadt, <strong>Schloss Leopoldskron</strong> am Weiher, das <strong>Kavalierhaus Klessheim</strong>. Dort tritt der Roboter im eleganten Branding auf und arbeitet als Gastgeber am Eingang. Für Produktpräsentationen und Kundenabende werden häufig der <strong>Hangar-7</strong> am Flughafen und die <strong>Stiegl-Brauwelt</strong> gebucht.</p>

<h2 id="hotellerie">Für Hotellerie und Tourismus</h2>

<p>Saisoneröffnung, Hausmesse eines Lieferanten oder Mitarbeiterfest nach der Saison: Der Roboter begrüßt die Gäste, weist den Weg und beantwortet Fragen in mehreren Sprachen. Für die Feier im Dezember gibt es eine eigene Seite: <a href="roboter-weihnachtsfeier.html">Roboter für die Weihnachtsfeier</a>.</p>

<h2 id="praxis-salzburg">Praktisches</h2>

<p>Einige Quadratmeter ebene Fläche und eine gewöhnliche Steckdose genügen. Der Operator baut auf, steuert den Roboter und achtet auf die Sicherheit der Gäste. Bei Veranstaltungen im Freien, etwa im Schlosspark, braucht der Roboter eine trockene, ebene Fläche und für den Regenfall einen überdachten Platz.</p>

<h2 id="einsaetze">Referenzen: ein Ball in einem Palais</h2>

{para('Dresdner Schlössernacht (Dresden): im Ballsaal und unter den Gästen.', 'realizacja-gala-palac', 'realizacja-gala-wsrod-gosci')}

<p>Bei der Dresdner Schlössernacht war der Roboter Gastgeber eines Balls in einem Dresdner Palais: im Pailletten-Smoking mit Krone, auf dem roten Teppich, im Ballsaal und mitten unter den Gästen. Genau diese Rolle passt zu Salzburger Schlössern und Festsälen.</p>

<p>Sie planen eine Veranstaltung in Salzburg? {ANFRAGE}.</p>
''',
    },

    'linz': {
        'opis': 'Humanoiden Roboter Unitree G1 in Linz mieten: für Design Center, Brucknerhaus, Tabakfabrik und Firmenevents in Oberösterreich. Ab 2.300 € netto pro Tag.',
        'lead': 'Der Unitree G1 kommt nach Linz und Oberösterreich: ins Design Center, ins Brucknerhaus, in die Tabakfabrik oder direkt in Ihr Werk. Operator, Transport und Branding sind im Preis.',
        'foto': ('realizacja-gala-zdjecia-gosci', SCHLOESSERNACHT),
        'czytaj': [['roboter-mieten-wien.html', 'Roboter mieten in Wien'], ['roboter-mieten-salzburg.html', 'Roboter mieten in Salzburg'],
                   ['messe-roboter-mieten.html', 'Messe-Roboter mieten'], ['unitree-g1-mieten.html', 'Unitree G1 mieten in Österreich'],
                   ['humanoider-roboter-mieten.html', 'Humanoiden Roboter mieten in Österreich']],
        'pytania': [
            ['Was kostet ein Roboter für ein Event in Linz?', 'Ein ganzer Veranstaltungstag kostet ab 2.300 € netto, mit Operator, Transport, Branding und Haftpflichtversicherung. Bei Einsätzen ab zwei Tagen gibt es 15 % Rabatt auf jeden Tag.'],
            ['Kommen Sie auch nach Wels, Steyr oder Leonding?', 'Ja. Wir kommen nach Linz und in ganz Oberösterreich, nach Wels, Steyr, Leonding, Traun oder Enns. Der Transport ist im Preis enthalten.'],
            ['Kann der Roboter in einer Werkshalle auftreten?', 'Ja, auf ebenem, trockenem Boden. Der Roboter braucht einige Quadratmeter freie Fläche und eine gewöhnliche Steckdose. Den Platz und die Wege stimmen wir vorher mit Ihnen ab.'],
            ['Passt der Roboter zu einer Industrieveranstaltung?', 'Ja. Für Fachpublikum legen wir einen sachlichen Auftritt fest und spielen dem Roboter Wissen über Ihr Unternehmen ein. Er begrüßt Kunden und Delegationen auf Deutsch, Englisch und in jeder anderen Sprache.'],
        ],
        'tresc': f'''
<h2 id="linz">Linz: Industrie trifft Medienkunst</h2>

<p>Linz ist Stahlstadt und zugleich die Stadt, in der seit Jahrzehnten über das Verhältnis von Mensch und Maschine nachgedacht wird. Oberösterreich ist das Industriebundesland: Stahl, Maschinenbau, Fahrzeugteile, Kunststoff. Für einen humanoiden Roboter ist das ein Publikum mit Vorwissen. Wer ihn hier einsetzt, zeigt Kunden und Mitarbeitenden, dass Automatisierung im eigenen Haus ein Thema ist.</p>

<p>Der Unitree G1 kommt mit Operator, Drehbuch und Ihrem Branding. Ein Veranstaltungstag kostet ab 2.300&nbsp;€ netto, Transport und Haftpflichtversicherung eingeschlossen.</p>

<h2 id="design-center-linz">Design Center, Brucknerhaus, Tabakfabrik</h2>

<ul>
  <li><strong>Design Center Linz</strong> — Fachmessen und Kongresse unter dem Glasdach. Der Roboter arbeitet am Stand und holt Besucher aus dem Gang.</li>
  <li><strong>Brucknerhaus</strong> — Festakte, Jubiläen und Preisverleihungen an der Donau, der Roboter als Gastgeber im Foyer.</li>
  <li><strong>Tabakfabrik Linz</strong> — Produktpräsentationen, Start-up-Events und Firmenfeiern in Industriearchitektur.</li>
  <li><strong>voestalpine Stahlwelt</strong> — Kundenveranstaltungen, bei denen Technik das Thema ist.</li>
</ul>

<p>Auf Automatisierungs- und Industriemessen ist ein Humanoid am Stand kein Fremdkörper, sondern das Thema selbst. Wie ein Messeauftritt abläuft, steht unter <a href="messe-roboter-mieten.html">Messe-Roboter mieten</a>.</p>

<wideo/>

<h2 id="werk-linz">Im Werk: Tag der offenen Tür, Jubiläum, Lehrlingstag</h2>

<p>Viele Veranstaltungen in Oberösterreich finden nicht in einer Eventlocation statt, sondern im Betrieb. Der Roboter begrüßt die Besucher am Werkstor, begleitet die Führung und steht am Ende für Fotos bereit. Beim Lehrlingstag oder auf der Karrieremesse zieht er junge Leute an den Stand und beantwortet Fragen zum Unternehmen, die wir ihm vorher einspielen.</p>

<h2 id="praxis-linz">Praktisches</h2>

<p>Der Roboter braucht einige Quadratmeter ebene Fläche und eine gewöhnliche Steckdose. Der Operator ist die ganze Zeit dabei, achtet auf Abstände und wechselt die Akkus, ohne dass die Show unterbricht. Der Roboter erkennt Personen und Hindernisse über LiDAR und Computer Vision.</p>

<h2 id="einsaetze">Referenzen: Industriemesse und Wissenschaftszentrum</h2>

{para('Rekord-Gruppe auf der Messe MSPO (Kielce) und Kopernikus-Wissenschaftszentrum (Warschau).', 'realizacja-grupa-rekord-mspo', 'realizacja-kopernik-noc')}

<p>Auf der Industriemesse MSPO arbeitete der Roboter zwei Tage lang als Botschafter einer Unternehmensgruppe. Im Kopernikus-Wissenschaftszentrum in Warschau stand er bei einem Abend für Erwachsene zum Thema Robotik und künstliche Intelligenz in der Ausstellung. Im deutschsprachigen Raum war er bei der Dresdner Schlössernacht im Einsatz.</p>

<p>Sie planen eine Veranstaltung in Linz? {ANFRAGE}.</p>
''',
    },

    'innsbruck': {
        'opis': 'Humanoiden Roboter Unitree G1 in Innsbruck mieten: für Congress, Messe Innsbruck und Firmenevents in Tirol. Ab 2.300 € netto pro Tag, Transport inklusive.',
        'lead': 'Der Unitree G1 kommt nach Innsbruck und Tirol: in den Congress am Rennweg, auf das Messegelände, in ein Tagungshotel oder zu Ihrem Firmenevent. Operator, Transport und Branding sind im Preis.',
        'foto': ('realizacja-gala-detal', SCHLOESSERNACHT),
        'czytaj': [['roboter-mieten-salzburg.html', 'Roboter mieten in Salzburg'], ['roboter-mieten-wien.html', 'Roboter mieten in Wien'],
                   ['messe-roboter-mieten.html', 'Messe-Roboter mieten'], ['roboter-weihnachtsfeier.html', 'Roboter für die Weihnachtsfeier'],
                   ['humanoider-roboter-mieten.html', 'Humanoiden Roboter mieten in Österreich']],
        'pytania': [
            ['Was kostet ein Roboter für ein Event in Innsbruck?', 'Ab 2.300 € netto für einen ganzen Veranstaltungstag, mit Operator, Transport, Branding und Haftpflichtversicherung. Bei mehrtägigen Messen oder Kongressen gibt es ab zwei Tagen 15 % Rabatt auf jeden Tag.'],
            ['Kommen Sie auch nach Kufstein, Hall oder Seefeld?', 'Ja. Wir kommen nach Innsbruck und in ganz Tirol, nach Hall, Wattens, Schwaz, Kufstein oder Seefeld. Der Transport ist im Preis enthalten.'],
            ['Kann der Roboter bei einer Veranstaltung am Berg auftreten?', 'In Innenräumen ja, sofern wir den Roboter hinaufbringen können. Im Freien braucht er eine trockene, ebene und befestigte Fläche. Schnee, Wiese und Schotter scheiden aus. Das klären wir vorab mit Ihnen.'],
            ['Spricht der Roboter auch Italienisch und Englisch?', 'Ja. Der Roboter spricht Deutsch und jede andere Sprache und wechselt während der Veranstaltung, etwa für Gäste aus Italien oder für internationale Kongressteilnehmer.'],
        ],
        'tresc': f'''
<h2 id="innsbruck">Innsbruck: Kongresse zwischen den Bergen</h2>

<p>Innsbruck ist Universitätsstadt, Kongressstadt und das Zentrum einer Region, die vom Tourismus und von alpiner Technik lebt. Zu Tagungen kommen Gäste aus dem ganzen Alpenraum, viele aus Italien, Deutschland und der Schweiz. Ein Roboter, der sie in ihrer Sprache begrüßt, ist der Moment, über den am Abend im Hotel gesprochen wird.</p>

<p>Wir bringen den Unitree G1 mit Operator nach Tirol. Ein Veranstaltungstag kostet ab 2.300&nbsp;€ netto, mit Transport, Branding und Haftpflichtversicherung. Eine Anzahlung gibt es nicht.</p>

<h2 id="congress-messe-innsbruck">Congress und Messe Innsbruck</h2>

<h3>Congress Innsbruck</h3>

<p>Im Kongresshaus am Rennweg begrüßt der Roboter die Teilnehmenden im Foyer, kündigt Vortragende an und steht in den Pausen für Fotos bereit. Bei wissenschaftlichen Kongressen legen wir einen sachlichen Auftritt fest.</p>

<h3>Messe Innsbruck</h3>

<p>Auf Fachmessen für Seilbahn- und Alpintechnik oder für Gastronomie und Hotellerie arbeitet der Roboter am Stand: Er spricht Besucher an, nennt in einem Satz, was es zu sehen gibt, und übergibt an Ihr Team. Auf den Publikumsmessen im Frühjahr und Herbst ist er der Fotopunkt für Familien.</p>

<h3>Olympiaworld</h3>

<p>Großveranstaltungen, Sportevents und Firmenfeiern mit Bühne, auf der der Roboter eine Choreografie tanzt.</p>

<wideo/>

<h2 id="tourismus-tirol">Für Tourismus, Handel und Industrie in Tirol</h2>

<p>Saisoneröffnung eines Hotels, Jubiläum eines Familienbetriebs, Kundentag eines Herstellers: Der Roboter empfängt die Gäste, wechselt zwischen Deutsch, Italienisch und Englisch und trägt Ihr Logo mit QR-Code auf der Brust. Für Kundenabende mit besonderer Kulisse wird in Tirol gern in die <strong>Swarovski Kristallwelten</strong> in Wattens oder in die <strong>Hofburg Innsbruck</strong> eingeladen.</p>

<h2 id="praxis-innsbruck">Praktisches für Veranstaltungen in den Bergen</h2>

<p>Der Roboter braucht einige Quadratmeter ebene Fläche und eine gewöhnliche Steckdose. In Innenräumen arbeitet er überall, wo wir ihn hinbringen können, vom Tagungshotel im Tal bis zum Restaurant an der Bergstation. Im Freien braucht er einen trockenen, befestigten Untergrund. Der Operator ist die ganze Zeit dabei und hat Ersatzakkus mit.</p>

<h2 id="einsaetze">Referenzen: Ball in Dresden und ein Abend im Freien</h2>

{para('Dresdner Schlössernacht (Dresden) und Märchennacht im Dendrologischen Garten Przelewice.', 'realizacja-gala-detal', 'realizacja-przelewice-noc-bajek')}

<p>Bei der Dresdner Schlössernacht trug der Roboter Pailletten-Smoking und Krone und bewegte sich den Abend über zwischen den Gästen. Bei der Märchennacht im Dendrologischen Garten Przelewice arbeitete er nach Einbruch der Dunkelheit im Freien, im Licht von Scheinwerfern.</p>

<p>Sie planen eine Veranstaltung in Innsbruck? {ANFRAGE}.</p>
''',
    },
}

# Strony miast z szablonu: poza indeksem, dopóki nie dostaną własnej treści.
POZA_INDEKSEM = ['dornbirn', 'eisenstadt', 'klagenfurt', 'st-poelten', 'villach', 'wels']
CTA = 'Schreiben Sie uns oder rufen Sie an. Eine Antwort mit Preis und Verfügbarkeit erhalten Sie meist innerhalb von 30 Minuten.'


def wczytaj(plik):
    s = plik.read_text(encoding='utf-8')
    m = re.match(r'(<!--\s*)(\{.*?\})(\s*-->)', s, re.S)
    return json.loads(m.group(2)), s[m.end():]


def zapisz(plik, dane, tresc):
    plik.write_text('<!--\n' + json.dumps(dane, ensure_ascii=False, indent=2) + '\n-->\n' + tresc.strip('\n') + '\n', encoding='utf-8')


def main():
    for miasto, m in MIASTA.items():
        assert len(m['opis']) <= 160, (miasto, len(m['opis']))
        plik = ZRODLA / f'roboter-mieten-{miasto}.html'
        d, _ = wczytaj(plik)
        d['opis'] = m['opis']
        d['robots'] = 'index, follow, max-image-preview:large'
        d['lead'] = m['lead']
        d['foto'] = {'plik': m['foto'][0], 'alt': ALT[m['foto'][0]], 'podpis': m['foto'][1]}
        d['pytania'] = m['pytania']
        d['czytaj'] = m['czytaj']
        d['cta_tekst'] = CTA
        zapisz(plik, d, m['tresc'])
        slowa = len(re.sub(r'<[^>]+>', ' ', m['tresc']).split())
        print(f'{plik.name}: własna treść, {slowa} słów')
    for miasto in POZA_INDEKSEM:
        plik = ZRODLA / f'roboter-mieten-{miasto}.html'
        d, tresc = wczytaj(plik)
        d['robots'] = 'noindex, follow'
        zapisz(plik, d, tresc)
        print(f'{plik.name}: noindex')


# ——— Pozostałe strony .at: odpowiedź w ok. 30 minut (jak na stronie głównej), własne wezwania
# do kontaktu, linki tylko do miast z własną treścią, sekcja o targach w Austrii ———
CZAS = [
    ('innerhalb von 24 Werkstunden an Werktagen', 'meist innerhalb von 30 Minuten'),
    ('innerhalb von 24 Werkstunden mit einem konkreten Betrag, meist noch am selben Tag', 'meist innerhalb von 30 Minuten mit einem konkreten Betrag'),
    ('innerhalb von 24 Werkstunden', 'meist innerhalb von 30 Minuten'),
]
CTA_STRON = {
    'humanoider-roboter-mieten': 'Nennen Sie uns Datum, Ort und Anlass. Wir antworten meist innerhalb von 30 Minuten, am Telefon nennen wir den Preis sofort: +48 531 408 004.',
    'messe-roboter-mieten': 'Nennen Sie uns Messe, Standgröße und Termin. Die Antwort mit dem Preis für Ihre Messetage kommt meist innerhalb von 30 Minuten.',
    'roboter-weihnachtsfeier': 'Schreiben Sie uns Termin und Ort Ihrer Weihnachtsfeier. Sie erhalten meist innerhalb von 30 Minuten eine Antwort mit Preis und Verfügbarkeit.',
    'unitree-g1-mieten': 'Fragen Sie den Unitree G1 für Ihren Termin an. Wir prüfen die Verfügbarkeit und melden uns meist innerhalb von 30 Minuten.',
}
PIEC_MIAST = ('<a href="roboter-mieten-wien.html">Wien</a>, <a href="roboter-mieten-graz.html">Graz</a>, '
              '<a href="roboter-mieten-linz.html">Linz</a>, <a href="roboter-mieten-salzburg.html">Salzburg</a> '
              'und <a href="roboter-mieten-innsbruck.html">Innsbruck</a>')
# (plik, wzorzec, zamiennik, znacznik obecny po zamianie)
POPRAWKI = [
    ('humanoider-roboter-mieten',
     r'bis <a href="roboter-mieten-dornbirn\.html">Dornbirn</a>',
     'bis Dornbirn', 'bis Dornbirn</li>'),
    ('roboter-weihnachtsfeier',
     r'<p>Wir kommen in jede Stadt Österreichs, ohne Aufschlag und ohne Kilometerlimit\. Mehr zu einzelnen Städten:.*?</p>',
     f'<p>Wir kommen in jede Stadt Österreichs, ohne Aufschlag und ohne Kilometerlimit. Eigene Seiten gibt es für {PIEC_MIAST}.</p>',
     'Eigene Seiten gibt es für'),
    ('messe-roboter-mieten',
     r'<h2 id="im-einsatz-auf-oesterreichs-messen">.*?</h2>\s*<p>Wir liefern auf jedes Messegelände in Österreich.*?</p>',
     """<h2 id="im-einsatz-auf-oesterreichs-messen">Messen in Österreich: wo sich ein Roboter anbietet</h2>

<p>Wir kommen auf jedes Messegelände in Österreich. Für die fünf größten Messeplätze haben wir beschrieben, welche Aufgabe der Roboter dort übernehmen kann:</p>

<ul>
  <li><a href="roboter-mieten-wien.html">Wien</a> — Messe Wien im Prater und Austria Center Vienna: Fachmessen, Publikumsmessen und internationale Kongresse.</li>
  <li><a href="roboter-mieten-graz.html">Graz</a> — Messe Congress Graz mit Stadthalle: Fachmessen und die Grazer Herbstmesse.</li>
  <li><a href="roboter-mieten-salzburg.html">Salzburg</a> — Messezentrum Salzburg, unter anderem mit der Gastronomiefachmesse „Alles für den Gast“.</li>
  <li><a href="roboter-mieten-linz.html">Linz</a> — Design Center Linz: Industrie- und Automatisierungsmessen.</li>
  <li><a href="roboter-mieten-innsbruck.html">Innsbruck</a> — Messe Innsbruck: Fachmessen für Alpintechnik, Gastronomie und Hotellerie.</li>
</ul>

<p>Auch die Messe Wels, die Messe Dornbirn und das Messegelände Klagenfurt erreichen wir ohne Aufschlag. Auf- und Abbau erfolgen vor Messebeginn und nach Messeschluss, abgestimmt mit Ihrem Standbauer. Bei mehrtägigen Messen gibt es ab zwei Tagen 15&nbsp;% Rabatt auf jeden Tag.</p>""",
     'Messen in Österreich: wo sich ein Roboter anbietet'),
]


def poprawki():
    for plik in sorted(ZRODLA.glob('*.html')):
        s = plik.read_text(encoding='utf-8')
        n = s
        for a, b in CZAS:
            n = n.replace(a, b)
        if n != s:
            plik.write_text(n, encoding='utf-8')
    for nazwa, tekst in CTA_STRON.items():
        plik = ZRODLA / f'{nazwa}.html'
        d, tresc = wczytaj(plik)
        d['cta_tekst'] = tekst
        zapisz(plik, d, tresc)
    for nazwa, wzorzec, nowe, znacznik in POPRAWKI:
        plik = ZRODLA / f'{nazwa}.html'
        d, tresc = wczytaj(plik)
        if znacznik in tresc:
            continue
        nowa, ile = re.subn(wzorzec, lambda _m: nowe, tresc, count=1, flags=re.S)
        assert ile == 1 and znacznik in nowa, (nazwa, wzorzec[:60])
        zapisz(plik, d, nowa)
        print(f'{plik.name}: poprawka „{znacznik[:50]}”')
    reszta = [(f.name, m.group(0)) for f in sorted(ZRODLA.glob('*.html'))
              for m in re.finditer(r'.{0,40}24 Werkstunden', f.read_text(encoding='utf-8'))]
    assert not reszta, reszta[:3]


if __name__ == '__main__':
    main()
    poprawki()
