# -*- coding: utf-8 -*-
"""Strony zastosowań 33bots.de bez wspólnych bloków szablonu (11.2026).

Pomiar powtorzenia.py: strony „Roboter für …” miały 33–43% tekstu wspólnego z innymi podstronami —
te same akapity korzyści („Der Moment, der hängen bleibt”, „Interaktion und Fotobereich”,
„Tanzchoreografie”) i te same trzy odpowiedzi w FAQ (cena, dojazd, termin rezerwacji). Google widzi
wtedy jedną stronę w kilkunastu kopiach i pomija je w indeksie.

Tutaj każda strona dostaje własną górną część (przed filmem), własne FAQ, własny opis meta i własną
sekcję realizacji z niemieckim wydarzeniem (Dresdner Schlössernacht) na początku. Unikalne poradniki
pod filmem zostają. Fakty wyłącznie z rynki.py i dotychczasowych stron .de.

    python3 tresci/zagranica/zastosowania_de.py     # potem buduj_podstrony.py de <repo>
"""
import json
import re
from pathlib import Path

ZRODLA = Path(__file__).resolve().parent / 'podstrony' / 'de'

ALT = {
    'realizacja-gala-palac': 'Humanoider Roboter im Smoking im Ballsaal eines Palais',
    'realizacja-gala-wsrod-gosci': 'Humanoider Roboter unter den Gästen einer Gala',
    'realizacja-gala-czerwony-dywan': 'Humanoider Roboter im Paillettensmoking mit Krone auf dem roten Teppich vor der Sponsorenwand',
    'realizacja-gala-zdjecia-gosci': 'Galagäste fotografieren den humanoiden Roboter an der Sponsorenwand',
    'realizacja-robot-w-deszczu': 'Humanoider Roboter im roten T-Shirt mit Regenschirm vor einem Autohaus',
    'realizacja-yeah-gym-koszulka': 'Humanoider Roboter im T-Shirt des Clubs YEAH GYM winkt zur Begrüßung',
    'realizacja-yeah-gym-silownia': 'Humanoider Roboter im Trainingsbereich des Clubs YEAH GYM',
    'realizacja-jednorozec-zachod': 'Humanoider Roboter bei einer Parade im Freien bei Sonnenuntergang',
    'realizacja-przelewice-noc-bajek': 'Humanoider Roboter in beleuchteten Arkaden während der Märchennacht in Przelewice',
    'realizacja-tet-trung-thu-tlum': 'Gäste des Mittherbstfests rund um den humanoiden Roboter',
    'realizacja-tet-trung-thu': 'Humanoider Roboter im festlichen Branding beim Mittherbstfest',
    'realizacja-lexai-starowka': 'Humanoider Roboter im LEX-AI-T-Shirt in der Altstadt, Passanten machen Fotos',
    'realizacja-lexai-ulica': 'Humanoider Roboter LEX AI geht mit einer Aktentasche durch die Altstadt',
    'realizacja-matys-silver-garden': 'Humanoider Roboter an der Wand des Projekts Silver Garden am Stand von Matys Development',
    'realizacja-dream-med-expo': 'Humanoider Roboter am Stand von Dream-Med auf der Warsaw Medical Expo',
    'realizacja-wesele-konfetti': 'Humanoider Roboter im Nebel auf der Tanzfläche einer Hochzeit',
    'realizacja-szkola-kosmos-majaland': 'Humanoider Roboter in der Schürze der Kosmos-Schule beim Schuljahresbeginn',
    'realizacja-spotkanie-biznesowe': 'Humanoider Roboter im T-Shirt der Unternehmerloge auf einer Terrasse',
    'realizacja-event-nad-woda': 'Humanoider Roboter winkt auf einer Terrasse über einem Jachthafen',
    'realizacja-women-in-tech-tlum': 'Teilnehmerinnen des Women in Tech Summit filmen den humanoiden Roboter mit dem Handy',
    'realizacja-eco-studio-scena': 'Humanoider Roboter auf der Bühne des Eco-Studio-Finales in rotem Licht',
}


def para(podpis, a, b):
    return (f'<para podpis="{podpis}"><kadr plik="{a}" alt="{ALT[a]}"/>'
            f'<kadr plik="{b}" alt="{ALT[b]}"/></para>')


STRONY = {
    'roboter-eroeffnung': {
        'opis': 'Humanoiden Roboter für die Eröffnung mieten: Begrüßung vor der Tür, Banddurchschnitt, Tanzshow. Unitree G1 mit Operator und Branding, ab 2.500 € pro Tag →',
        'cta_tekst': 'Nennen Sie uns Eröffnungstermin und Adresse. Sie erhalten meist innerhalb von 30 Minuten eine Antwort mit Preis und Verfügbarkeit.',
        'pytania': [
            ['Wie früh sollte man den Roboter für eine Eröffnung planen?', 'Den Eröffnungstermin kennt man meist im Voraus — reservieren Sie den Roboter 3–4 Wochen vorher, dann helfen wir auch bei der Kommunikation, die die Attraktion ankündigt. Eine Anzahlung ist dafür nicht nötig.'],
            ['Was kostet ein Roboter zur Eröffnung?', 'Ein kompletter Eröffnungstag kostet ab 2.500 €, mit Operator, Anfahrt, Branding und Haftpflichtversicherung. Soll der Roboter nur zur Zeremonie kommen, kalkulieren wir den kürzeren Auftritt individuell. Für ein Eröffnungswochenende oder mehrere Filialen gilt ab zwei Tagen ein Rabatt von 15 % auf jeden Tag.'],
            ['Kann der Roboter draußen vor dem Geschäft stehen?', 'Ja, auf ebener, trockener Fläche wie dem Gehweg oder Vorplatz. Bei Regen zieht er in den Eingangsbereich um, das planen wir vorher ein. Auf öffentlichen Flächen braucht es die Zustimmung des Flächenbetreibers; bei der Organisation helfen wir.'],
            ['Trägt der Roboter zur Eröffnung unser Logo?', 'Ja. Logo und QR-Code auf der Brust sind im Preis enthalten, der Code kann zum Eröffnungsangebot oder zur Terminbuchung führen. Wie der Auftritt in den Farben eines Hauses aussieht, zeigt der Fitnessclub YEAH GYM: Dort trug der Roboter das Shirt des Clubs.'],
        ],
        'gora': '''
<h2 id="programmpunkt">Was der Roboter am Eröffnungstag übernimmt</h2>

<p>Eine Eröffnung hat zwei Aufgaben. Die geladenen Gäste sollen sich willkommen fühlen, und die Nachbarschaft soll merken, dass es einen neuen Ort gibt. Der Roboter arbeitet an beiden: Vor der Tür bleibt stehen, wer sonst vorbeigegangen wäre, und drinnen bekommt die Zeremonie einen Moment, den alle filmen.</p>

<h3>Vor der Tür</h3>

<p>Der G1 steht am Eingang, winkt, spricht Passanten an und lädt sie hinein. Auf der Brust trägt er Ihr Logo und einen QR-Code, zum Beispiel zum Eröffnungsangebot.</p>

<h3>Beim Banddurchschnitt</h3>

<p>Zur Zeremonie kommt er mit nach vorn. Er begrüßt die Gäste, sagt die Rednerin oder den Redner an und steht beim Durchschneiden des Bandes neben der Geschäftsführung. Für Lokalredaktionen ist das ein dankbares Motiv. Garantieren lässt sich ein Bericht nicht, aber eine Einladung mit Bild erhöht die Chance.</p>

<h3>Den Rest des Tages</h3>

<p>Danach wechselt der Roboter in den Alltag eines Eröffnungstags: kurze Tanzeinlagen, Fotos mit den ersten Kundinnen und Kunden und Antworten auf Fragen zu Sortiment oder Öffnungszeiten, die wir ihm vorher einspielen.</p>

<h2 id="wie-ueberzeugt-der-roboter-fuer">Zeitplan für einen Eröffnungstag</h2>

<ol>
  <li><strong>Rund 1,5 Stunden vorher:</strong> Anreise, Aufbau und Testlauf auf der Fläche am Eingang.</li>
  <li><strong>Zur Türöffnung:</strong> Begrüßung der ersten Gäste und der Passanten.</li>
  <li><strong>Zur Zeremonie:</strong> Ansage, Banddurchschnitt, Gruppenfoto.</li>
  <li><strong>Bis zum Abend:</strong> Blöcke aus Tanz, Fotos und Gesprächen, dazwischen kurze Akkuwechsel.</li>
</ol>

<p>Planen Sie die Feier noch, hilft der Ratgeber <a href="eroeffnung-ideen.html">Ideen für die Eröffnungsfeier</a>. Verwandte Formate sind der <a href="angebot-tag-der-offenen-tuer.html">Tag der offenen Tür</a> und der <a href="roboter-produktlaunch.html">Produktlaunch</a>.</p>
''',
        'zamiany': [
            ('''<h3>Band, Foto, Show</h3>

<p>Der Roboter ist beim Banddurchschnitt dabei, begrüßt die ersten Kunden und führt zwischendurch kurze Shows durch.</p>

''', ''),
        ],
        'einsaetze': f'''<h2 id="einsaetze">Aus echten Einsätzen</h2>

{para('Autohaus Gonia und YEAH GYM in Breslau.', 'realizacja-robot-w-deszczu', 'realizacja-yeah-gym-koszulka')}

<p>Vor dem Autohaus Gonia stand der Roboter im roten T-Shirt mit Regenschirm am Eingang. Im Fitnessclub YEAH GYM in Breslau trug er das Shirt des Clubs und begrüßte die Mitglieder im Trainingsbereich.</p>

{para('Dresdner Schlössernacht (Dresden) und Matys Development auf der Immobilienmesse in Stettin.', 'realizacja-gala-czerwony-dywan', 'realizacja-matys-silver-garden')}

<p>In Deutschland war der Roboter bei der Dresdner Schlössernacht als Gastgeber auf dem roten Teppich im Einsatz. Alle Aufnahmen stehen unter <a href="referenzen-videos.html">Referenzen und Videos</a>.</p>
''',
    },

    'roboter-stadtfest': {
        'opis': 'Humanoiden Roboter für das Stadtfest mieten: Bühnenshow, Rundgang über den Festplatz, Fotos für Familien. Für Kommunen, Rechnung nach dem Fest →',
        'cta_tekst': 'Nennen Sie uns Festtermin, Ort und Bühnenzeiten. Die Antwort mit konkretem Preis kommt meist innerhalb von 30 Minuten.',
        'pytania': [
            ['Arbeiten Sie mit Kommunen zusammen?', 'Ja — wir betreuen städtische und kommunale Veranstaltungen, stellen Rechnungen für öffentliche Auftraggeber und richten uns nach den Vorgaben des Vergabeverfahrens.'],
            ['Was kostet ein Roboter für ein Stadtfest?', 'Ein kompletter Festtag kostet ab 2.500 €, mit Operator, Anfahrt, Branding und Haftpflichtversicherung. Dauert das Fest zwei oder mehr Tage, gibt es 15 % Rabatt auf jeden Tag. Einen kürzeren Auftritt, etwa nur zur Eröffnung des Fests, kalkulieren wir individuell.'],
            ['Was passiert bei Regen?', 'Der Roboter ist nicht wetterfest. Bei Regen weichen wir auf eine überdachte Fläche aus, zum Beispiel die Bühne oder ein Zelt. Diese Alternative legen wir vor dem Fest gemeinsam fest.'],
            ['Auf welchem Untergrund kann der Roboter laufen?', 'Auf Pflaster, Asphalt, Bühnenboden oder einem Podest. Rasen, Kies und Sand gehen nicht. Auf einer Festwiese legen wir die Showfläche deshalb auf ein Podest oder eine Platte.'],
            ['Wie lange ist der Roboter am Festtag im Einsatz?', 'Den ganzen Veranstaltungstag, in Blöcken mit kurzen Akkuwechseln. Der Operator hat Ersatzakkus dabei. Die Zeiten der Auftritte stimmen wir auf das Bühnenprogramm ab.'],
        ],
        'gora': '''
<h2 id="warum-ein-roboter-den-unterschied">Ein Programmpunkt für das ganze Fest</h2>

<p>Ein Stadtfest muss allen etwas bieten: Familien am Nachmittag, Vereinen auf der Bühne, Jugendlichen am Abend. Die meisten Attraktionen erreichen eine dieser Gruppen. Vor einem Roboter, der läuft, winkt und antwortet, stehen Kita-Kinder neben ihren Großeltern, und beide holen das Handy heraus.</p>

<h3>Auf der Bühne</h3>

<p>Die Auftritte flechten wir in das Bühnenprogramm ein, zwischen Konzerten, Vereinsvorführungen und Wettbewerben. Die Moderation sagt den Roboter an, er begrüßt die Stadt, tanzt eine Choreografie und verabschiedet sich bis zum nächsten Block.</p>

<h3>Auf dem Festplatz</h3>

<p>Zwischen den Bühnenblöcken geht der G1 mit dem Operator über den Platz, gibt die Hand, beantwortet Fragen der Kinder und stellt sich für Familienfotos auf. Auch die Eröffnung des Fests an der Seite der Bürgermeisterin oder des Bürgermeisters kann er mit übernehmen.</p>

<h3>Im Zeichen der Stadt</h3>

<p>Auf der Brust trägt der Roboter das Wappen oder Logo der Stadt, auf Wunsch mit einem QR-Code zum Festprogramm. Bei der Einhorn-Parade der Gemeinde Jednorozec trat er im T-Shirt der Gemeinde auf und war bis in die Abenddämmerung im Freien unterwegs.</p>

<h2 id="wie-ueberzeugt-der-roboter-fuer">Für Kommunen und Veranstalter</h2>

<p>Wir arbeiten mit Städten, Gemeinden und Stadtmarketing zusammen. Eine Anzahlung gibt es nicht, die Rechnung stellen wir nach der Veranstaltung, und bei öffentlichen Auftraggebern richten wir uns nach den Vorgaben des Vergabeverfahrens. Im Preis ab 2.500&nbsp;€ pro Veranstaltungstag sind Operator, Anfahrt, Branding und Haftpflichtversicherung enthalten. Dauert das Fest ein ganzes Wochenende, gibt es ab zwei Tagen 15&nbsp;% Rabatt auf jeden Tag.</p>

<p>Für die Planung des gesamten Fests gibt es den Ratgeber <a href="stadtfest-organisieren.html">Stadtfest organisieren</a>. Die Bausteine eines Bühnenauftritts beschreibt die Seite <a href="roboter-show.html">Roboter-Show</a>.</p>
''',
        'zamiany': [
            ('<p>Stadtfeste, Betriebsfeste und Familienveranstaltungen — siehe <a href="roboter-stadtfest.html">Roboter für Outdoor-Events</a>.</p>',
             '<p>Stadtfeste, Betriebsfeste und Familienveranstaltungen. Für das Fest eines Unternehmens gibt es eine eigene Beschreibung: <a href="roboter-firmenfeier.html#roboter-auf-dem-betriebsfest">Roboter auf dem Betriebsfest</a>.</p>'),
        ],
        'einsaetze': f'''<h2 id="einsaetze">Aus echten Einsätzen</h2>

{para('Einhorn-Parade der Gemeinde Jednorozec und Märchennacht im Dendrologischen Garten Przelewice.', 'realizacja-jednorozec-zachod', 'realizacja-przelewice-noc-bajek')}

<p>Im öffentlichen Raum war der Roboter unter anderem bei der Einhorn-Parade der Gemeinde Jednorozec und bei der Märchennacht im Dendrologischen Garten Przelewice im Einsatz, beschrieben in der <a href="case-study-ogrod-przelewice.html">Case Study Przelewice</a>.</p>

{para('Mittherbstfest Tết Trung Thu und LEX AI am Langen Markt in Danzig.', 'realizacja-tet-trung-thu-tlum', 'realizacja-lexai-starowka')}

<p>In Deutschland arbeitete er bei der Dresdner Schlössernacht in Dresden. Weitere Aufnahmen stehen unter <a href="referenzen-videos.html">Referenzen und Videos</a>.</p>
''',
    },

    'roboter-produktlaunch': {
        'opis': 'Roboter für den Produktlaunch: Enthüllung, Kernbotschaften, Fragerunde und Fotopunkt. Unitree G1 mit Operator und Ihrem Branding, deutschlandweit →',
        'cta_tekst': 'Beschreiben Sie Produkt, Termin und Ort. Wir schlagen eine Inszenierung vor und nennen den Preis, meist innerhalb von 30 Minuten.',
        'pytania': [
            ['Kann der Roboter unser Produkt halten und präsentieren?', 'Je nach Größe — der G1 kann leichtere Gegenstände halten, auf das Produkt zeigen und damit posieren. Die Details klären wir, sobald wir das Produkt kennen.'],
            ['Was kostet ein Roboter für einen Produktlaunch?', 'Ab 2.500 € pro Veranstaltungstag, mit Operator, Anfahrt, Branding und Haftpflichtversicherung. Dauert die Premiere nur einen Abend, kalkulieren wir den kürzeren Auftritt individuell. Für eine Roadshow gilt ab zwei Tagen ein Rabatt von 15 % auf jeden Tag.'],
            ['Kann der Roboter Fragen zu unserem Produkt beantworten?', 'Ja. Vor der Veranstaltung spielen wir ihm ein, was er wissen soll: Informationen über das Produkt, Ihr Unternehmen, Ihr Angebot und die häufigsten Fragen. Er antwortet auf Deutsch, Englisch und in jeder anderen Sprache.'],
            ['Wie nah dürfen Gäste und Fotografen an den Roboter?', 'Nah genug für ein gemeinsames Foto. Der G1 erkennt Hindernisse und Personen über LiDAR und Computer Vision, und der Operator ist die ganze Zeit dabei und achtet auf Abstände. Die Haftpflichtversicherung ist im Preis enthalten.'],
            ['Wie viel Vorlauf braucht ein Launch mit Roboter?', 'Am besten mindestens 3–4 Wochen. Produktinformationen und Ablaufplan brauchen wir etwa zwei Wochen vor dem Termin. Die Reservierung erfolgt ohne Anzahlung.'],
        ],
        'gora': '''
<h2 id="die-attraktion-ueber-die-noch">Drei Aufgaben bei einer Produktpremiere</h2>

<p>Bei einem Launch sitzen Presse, Kunden und das eigene Team im selben Raum, und alle sollen dasselbe Bild mitnehmen. Der Roboter liefert dieses Bild und hält die Aufmerksamkeit dort, wo Ihr Produkt steht.</p>

<h3>Die Enthüllung</h3>

<p>Der G1 zieht das Tuch weg, bringt das Produkt auf die Bühne oder zeigt darauf, während das Licht angeht. Leichtere Gegenstände kann er selbst halten. Was möglich ist, klären wir, sobald wir das Produkt kennen.</p>

<h3>Die Kernbotschaften</h3>

<p>Nach der Enthüllung nennt der Roboter die wichtigsten Eigenschaften, mit vorbereitetem Text und Gestik. Danach beantwortet er Fragen aus dem Publikum. Dafür spielen wir ihm vorab das Wissen über Produkt, Unternehmen und Angebot ein.</p>

<h3>Der Fotopunkt danach</h3>

<p>Wenn der offizielle Teil endet, bleibt der Roboter neben dem Produkt stehen. Gäste, die ein Foto mit ihm machen, haben auch die Neuheit im Bild, und dazu Ihr Logo auf seiner Brust.</p>

<h2 id="wie-ueberzeugt-der-roboter-fuer">Was wir vor der Premiere brauchen</h2>

<ul>
  <li><strong>Produktinformationen und Ablaufplan</strong>, am besten zwei Wochen vorher. Daraus entstehen der Text des Roboters und sein Wissen für die Fragerunde.</li>
  <li><strong>Zeit für einen Durchlauf.</strong> Wir kommen in der Regel rund 1,5 Stunden vor Beginn, bei aufwendiger Inszenierung nach Absprache früher, und stimmen Ablauf und Timing mit Ihrer Regie ab.</li>
  <li><strong>Rund 2×2&nbsp;m ebene Fläche und eine 230-V-Steckdose.</strong> Internet oder besondere Beleuchtung braucht der Roboter nicht.</li>
</ul>

<p>Soll die Neuheit nach der Premiere auf Tour gehen, wiederholen wir das Format an mehreren Orten. Verwandte Formate sind <a href="roboter-eroeffnung.html">Eröffnungen</a>, <a href="angebot-messen.html">Messeauftritte</a> und <a href="roboter-werbung-film.html">Werbung und Film</a>.</p>
''',
        'srodek': '''<h2 id="roboter-beim-produktlaunch">Wenn das Produkt nicht auf eine Bühne passt</h2>

<p>Nicht jede Neuheit lässt sich enthüllen. Eine Software, eine Dienstleistung oder ein Bauprojekt haben keine Verpackung, die man öffnen kann. Dann trägt der Roboter selbst die Botschaft.</p>

<h3>Der Roboter in einer Rolle</h3>

<p>Für die App LEX AI trat der Roboter als KI-Anwalt auf dem Langen Markt in Danzig auf, mit Aktentasche und im T-Shirt der Marke. Aus dem Auftritt wurden ein Beitrag in der Nachrichtensendung Teleexpress (TVP) und eine Reportage von TVP Danzig. Die ganze Geschichte steht in der <a href="case-study-lexai.html">Case Study LEX AI</a>.</p>

<h3>Der Roboter am Projekt</h3>

<p>Am Stand von Matys Development auf der Immobilienmesse in Stettin stand der Roboter an der Wand des Projekts Silver Garden, mit den Materialien zum Projekt in Reichweite.</p>

<h3>Medien: Chance, keine Garantie</h3>

<p>Ein Roboter in einer ungewöhnlichen Rolle ist ein starkes Motiv für Redaktionen. Garantieren lässt sich ein Bericht nicht. Planen lassen sich der Moment, das Bild und eine Einladung, die beides ankündigt.</p>

''',
        'einsaetze': f'''<h2 id="einsaetze">Aus echten Einsätzen</h2>

{para('Dresdner Schlössernacht (Dresden) und LEX AI (Danzig).', 'realizacja-gala-czerwony-dywan', 'realizacja-lexai-ulica')}

<p>Bei der Dresdner Schlössernacht stand der Roboter im Paillettensmoking mit Krone vor der Sponsorenwand: das Bild, vor dem sich die Gäste des Abends fotografierten.</p>

{para('Matys Development (Immobilienmesse Stettin) und Dream-Med auf der Warsaw Medical Expo (Warschau).', 'realizacja-matys-silver-garden', 'realizacja-dream-med-expo')}

<p>Weitere Aufnahmen und Videos stehen unter <a href="referenzen-videos.html">Referenzen und Videos</a>.</p>
''',
    },

    'roboter-privatfeier': {
        'opis': 'Humanoiden Roboter für Geburtstag, Jubiläum oder Gartenfest mieten: persönliche Rede, Tanz, Fotos mit den Gästen. Operator und Anfahrt im Preis →',
        'cta_tekst': 'Schreiben Sie uns Anlass, Datum und Ort. Wir melden uns meist innerhalb von 30 Minuten mit einem konkreten Betrag.',
        'pytania': [
            ['Wie viel Platz braucht der Roboter auf einer Privatfeier?', 'Ein paar Quadratmeter ebener Boden genügen — Wohnzimmer, Terrasse oder Partyzelt reichen völlig aus.'],
            ['Was kostet ein Roboter für eine private Feier?', 'Ein kompletter Veranstaltungstag kostet ab 2.500 €. Für einen Geburtstag oder ein Jubiläum genügt meist ein kürzerer Auftritt, den wir individuell kalkulieren, immer günstiger als ein ganzer Tag. Operator, Anfahrt und Haftpflichtversicherung sind enthalten.'],
            ['Kann der Roboter dem Geburtstagskind persönlich gratulieren?', 'Ja. Den Text schreiben wir vorher mit Ihnen: Name, Anlass, ein paar persönliche Sätze. Der Roboter trägt ihn vor und beantwortet danach Fragen der Gäste.'],
            ['Ist der Roboter für Kinder sicher?', 'Ja. Der Operator ist die ganze Zeit beim Roboter und lässt Interaktionen nur unter Aufsicht zu. Bei Feiern mit vielen Kindern markieren wir einen Bereich und arbeiten in kurzen Blöcken von etwa 15 Minuten.'],
            ['Müssen wir eine Anzahlung leisten?', 'Nein. Die Reservierung erfolgt ohne Anzahlung, die Rechnung kommt nach der Feier. Am besten melden Sie sich 3–4 Wochen vor dem Termin.'],
        ],
        'gora': '''
<h2 id="warum-ein-roboter-den-unterschied">Die Überraschung des Abends</h2>

<p>Einen runden Geburtstag, ein Jubiläum oder ein Gartenfest plant man lange, und am Ende soll es einen Moment geben, mit dem niemand gerechnet hat. Ein humanoider Roboter, der zur Tür hereinkommt, das Geburtstagskind beim Namen nennt und gratuliert, ist so ein Moment.</p>

<h3>Der Auftritt</h3>

<p>Der Roboter kommt als unangekündigter Gast. Er begrüßt die Gastgeber, hält eine kurze Rede, die wir vorher mit Ihnen schreiben, und tanzt. Danach bleibt er bei den Gästen: für Fotos, Gespräche und eine Runde über die Tanzfläche.</p>

<h3>Persönlich statt von der Stange</h3>

<p>Vor der Feier spielen wir dem Roboter ein, was er wissen soll: Namen, Anekdoten, den Anlass. Er spricht Deutsch und jede andere Sprache, auch wenn die Familie aus mehreren Ländern anreist.</p>

<h3>Sie feiern, wir kümmern uns</h3>

<p>Der Operator bringt den Roboter, baut auf, steuert den Auftritt und achtet auf die Sicherheit. Sie brauchen nur ein paar Quadratmeter ebenen Boden und eine Steckdose, im Wohnzimmer, auf der Terrasse oder im Partyzelt.</p>

<h2 id="wie-ueberzeugt-der-roboter-fuer">Für welche privaten Anlässe?</h2>

<ul>
  <li><strong>Runde Geburtstage</strong> — der Roboter als Gratulant. Ideen für das Programm stehen im Ratgeber <a href="geburtstag-feiern-ideen.html">Geburtstag feiern</a>.</li>
  <li><strong>Hochzeiten</strong> — vom Sektempfang bis zur Tanzfläche, beschrieben unter <a href="roboter-hochzeit.html">Roboter für die Hochzeit</a>.</li>
  <li><strong>Kindergeburtstage und Familienfeste</strong> — mit eigenen Regeln, siehe unten und im Ratgeber <a href="kindergeburtstag-ideen.html">Kindergeburtstag-Ideen</a>.</li>
  <li><strong>Jubiläen und Gartenfeste</strong> — draußen auf Terrasse oder Pflaster, bei Regen unter Dach.</li>
</ul>

<p>Für private Feiern reicht oft ein kürzerer Auftritt statt eines ganzen Veranstaltungstags. Den kalkulieren wir individuell.</p>
''',
        'zamiany': [],
        'einsaetze': f'''<h2 id="einsaetze">Aus echten Einsätzen</h2>

{para('Eine Hochzeitsfeier und die Dresdner Schlössernacht (Dresden).', 'realizacja-wesele-konfetti', 'realizacja-gala-wsrod-gosci')}

<p>Auf einer Hochzeit stand der Roboter im Nebel auf der Tanzfläche. Bei der Dresdner Schlössernacht bewegte er sich im Paillettensmoking zwischen den Gästen eines Balls.</p>

{para('Mittherbstfest Tết Trung Thu und Schuljahresbeginn der Kosmos-Schule (Majaland).', 'realizacja-tet-trung-thu', 'realizacja-szkola-kosmos-majaland')}

<p>Wie der Roboter mit Kindern arbeitet, zeigen das Mittherbstfest Tết Trung Thu und der Schuljahresbeginn der Kosmos-Schule. Mehr unter <a href="referenzen-videos.html">Referenzen und Videos</a>.</p>
''',
    },

    'roboter-firmenfeier': {
        'opis': 'Humanoiden Roboter für die Firmenfeier mieten: Begrüßung, Preisübergabe, Tanzshow. Unitree G1 mit Operator, deutschlandweit, ab 2.500 € pro Tag →',
        'cta_tekst': 'Nennen Sie uns Datum, Ort und Anlass der Feier. Sie erhalten meist innerhalb von 30 Minuten eine Antwort mit Preis und Verfügbarkeit.',
        'pytania': [
            ['Passt der Roboter sowohl zur eleganten Gala als auch zur lockeren Feier?', 'Ja — den Charakter der Show passen wir an: vom eleganten Galaprogramm bis zur energiegeladenen Show mit Tanz-Battle auf der lockeren Teamfeier.'],
            ['Was kostet ein Roboter für die Firmenfeier?', 'Ein kompletter Veranstaltungstag kostet ab 2.500 €, mit Operator, Anfahrt, Branding und Haftpflichtversicherung. Für eine Abendfeier kalkulieren wir einen kürzeren Auftritt individuell. Die Rechnung stellen wir nach der Feier, bei Bedarf mit längerem Zahlungsziel.'],
            ['Kann der Roboter Auszeichnungen an Mitarbeitende überreichen?', 'Ja. Er sagt die Namen an, kommt mit auf die Bühne und übergibt die Auszeichnung zusammen mit der Geschäftsführung. Namen und Texte spielen wir ihm vorher ein.'],
            ['Funktioniert der Roboter beim Sommerfest im Freien?', 'Ja, auf ebenem, festem Boden wie Pflaster, Terrasse oder Podest. Auf Rasen arbeitet er nicht. Für den Regenfall vereinbaren wir vorher eine überdachte Alternative.'],
            ['Wie früh sollten wir für die Feier reservieren?', 'Am besten 3–4 Wochen vorher. Für Termine in der Eventsaison im Frühjahr und Herbst und für den Dezember lohnt sich eine frühere Anfrage. Eine Anzahlung ist nicht nötig.'],
        ],
        'gora': '''
<h2 id="warum-ein-roboter-den-unterschied">Was der Roboter auf einer Firmenfeier verändert</h2>

<p>Viele Betriebsfeiern laufen gleich ab: Rede, Buffet, Musik, und jede Abteilung bleibt an ihrem Tisch. Ein Roboter bricht dieses Muster auf, ohne dass jemand zu einem Spiel aufgefordert wird. Buchhaltung, IT und Vertrieb stehen in derselben Traube und lachen über dieselben Momente.</p>

<h3>Am Eingang</h3>

<p>Der G1 begrüßt die Kolleginnen und Kollegen mit Geste und Stimme, auf Wunsch mit einem Satz zum Jahr oder zum Anlass, den wir vorher mit Ihnen schreiben.</p>

<h3>Im offiziellen Teil</h3>

<p>Er sagt die Geschäftsführung an und übergibt mit ihr die Auszeichnungen für Jubilare oder das beste Team. So wird auch der Teil des Abends gefilmt, bei dem sonst viele aufs Handy schauen.</p>

<h3>Auf der Tanzfläche</h3>

<p>Später tanzt er eine Choreografie zur Musik, bei lockeren Feiern als Tanz-Battle mit den Mutigsten aus dem Team. Danach steht er für Fotos bereit.</p>

<h2 id="wie-ueberzeugt-der-roboter-fuer">Elegant oder locker: Der Charakter wird vorher festgelegt</h2>

<p>Derselbe Roboter passt zur Jubiläumsgala im Festsaal und zum Sommerfest im Hof. Den Unterschied machen Drehbuch und Branding. Bei der Dresdner Schlössernacht trat er im Paillettensmoking mit Krone auf, bei der Unternehmerloge in Nikolaiken im T-Shirt der Gastgeber auf einer Terrasse über dem Jachthafen. Ihr Logo und ein QR-Code auf der Brust sind im Preis enthalten.</p>

<p>Ideen für das restliche Programm stehen in den Ratgebern <a href="firmenfeier-ideen.html">Firmenfeier-Ideen</a> und <a href="sommerfest-ideen.html">Sommerfest-Ideen</a>. Für die Feier im Dezember gibt es eine eigene Seite: <a href="roboter-weihnachtsfeier.html">Roboter für die Weihnachtsfeier</a>. Wie sich der Roboter gegen Fotobox, Zauberer und Casino-Abend schlägt, steht im Vergleich <a href="roboter-firmenevents.html#attraktion-fuer-das-firmenevent-roboter">Roboter vs. Alternativen</a>.</p>
''',
        'zamiany': [],
        'einsaetze': f'''<h2 id="einsaetze">Aus echten Einsätzen</h2>

{para('Dresdner Schlössernacht (Dresden): Gäste fotografieren den Roboter, der Roboter im Ballsaal.', 'realizacja-gala-zdjecia-gosci', 'realizacja-gala-palac')}

<p>Bei der Dresdner Schlössernacht war der Roboter den Abend über zwischen den Gästen unterwegs: auf dem roten Teppich, im Ballsaal und an der Sponsorenwand.</p>

{para('Unternehmerloge in Nikolaiken: auf der Terrasse und über dem Jachthafen.', 'realizacja-spotkanie-biznesowe', 'realizacja-event-nad-woda')}

<p>Weitere Aufnahmen und Videos stehen unter <a href="referenzen-videos.html">Referenzen und Videos</a>.</p>
''',
    },

    'roboter-firmenevents': {
        'opis': 'Humanoider Roboter für Firmenevents: Kick-off, Kundentag, Sommerfest, Jubiläum. Rahmenangebot für mehrere Termine, Operator und Anfahrt im Preis →',
        'cta_tekst': 'Schicken Sie uns Ihren Eventkalender oder den ersten Termin. Wir antworten meist innerhalb von 30 Minuten mit Preis und Verfügbarkeit.',
        'pytania': [
            ['Arbeiten Sie auch dauerhaft mit Unternehmen zusammen?', 'Ja — bei mehreren Veranstaltungen im Jahr erstellen wir ein Rahmenangebot mit festen Konditionen und reservierten Terminen für Ihren gesamten Eventkalender.'],
            ['Was kostet ein Roboter für ein Firmenevent?', 'Ein Veranstaltungstag kostet ab 2.500 €, mit Operator, Anfahrt, Branding und Haftpflichtversicherung. Kürzere Auftritte kalkulieren wir individuell. Für mehrere Termine im Jahr erhalten Sie ein Rahmenangebot mit festen Konditionen.'],
            ['Kann der Roboter bei jeder Veranstaltung etwas anderes machen?', 'Ja. Für jeden Termin legen wir Rolle, Texte und Ablauf neu fest: Empfang beim Kick-off, Tanzshow beim Sommerfest, Preisübergabe beim Jubiläum. Auch das Wissen des Roboters passen wir an den Anlass an.'],
            ['Kommen Sie auch an Standorte außerhalb der Großstädte?', 'Ja. Wir sind deutschlandweit im Einsatz, auch am Werk auf dem Land oder im Tagungshotel. Die Anfahrt ist im Preis enthalten, eine Kilometerpauschale gibt es nicht.'],
            ['Wie läuft die Abrechnung für Unternehmen?', 'Die Reservierung erfolgt ohne Anzahlung. Die Rechnung stellen wir nach der Veranstaltung, bei Bedarf mit längerem Zahlungsziel.'],
        ],
        'gora': '''
<h2 id="programmpunkt">Ein Roboter für das ganze Eventjahr</h2>

<p>Unternehmen laden nicht einmal im Jahr ein, sondern vier- oder fünfmal: Kick-off, Kundentag, Sommerfest, Jubiläum, Weihnachtsfeier. Für jede Veranstaltung eine neue Attraktion zu suchen kostet Zeit. Der Roboter kommt jedes Mal in einer anderen Rolle.</p>

<ul>
  <li><strong>Kick-off:</strong> Er begrüßt die Mannschaft am Eingang und kündigt die Geschäftsführung an. Mehr im Ratgeber <a href="kick-off-veranstaltung.html">Kick-off-Veranstaltung planen</a>.</li>
  <li><strong>Kundenveranstaltung und Hausmesse:</strong> Er empfängt die Gäste, erklärt in Ihren Worten, was es zu sehen gibt, und weist den Weg zum Vortrag.</li>
  <li><strong>Sommerfest und Familientag:</strong> Tanzshow, Fotos mit den Kindern, Auftritte in Blöcken über den Nachmittag.</li>
  <li><strong>Jubiläum und Gala:</strong> elegantes Branding, Ansage der Redner, Übergabe der Auszeichnungen.</li>
  <li><strong>Weihnachtsfeier:</strong> der Programmpunkt zwischen Essen und Tanzfläche, beschrieben unter <a href="roboter-weihnachtsfeier.html">Roboter für die Weihnachtsfeier</a>.</li>
</ul>

<h2 id="wie-ueberzeugt-der-roboter-fuer">Rahmenangebot für mehrere Termine</h2>

<p>Bei mehreren Veranstaltungen im Jahr erstellen wir ein Rahmenangebot mit festen Konditionen und reservierten Terminen für Ihren gesamten Eventkalender. Das Drehbuch schreiben wir für jede Veranstaltung neu, das Branding bleibt Ihres: Logo und QR-Code auf der Brust sind im Preis. Für Unternehmen mit mehreren Standorten wiederholen wir ein Format als Roadshow. Ab zwei Veranstaltungstagen gibt es 15&nbsp;% Rabatt auf jeden Tag.</p>

<p>Was der Roboter wissen soll, spielen wir ihm vor jedem Termin ein: Informationen über die Veranstaltung, das Unternehmen, sein Angebot und die Fragen, die Gäste am häufigsten stellen. Planen Sie eine einzelne Feier, lesen Sie weiter unter <a href="roboter-firmenfeier.html">Roboter für Firmenfeiern</a>.</p>
''',
        'zamiany': [
            ('Das gilt für Messen ebenso wie für <a href="roboter-firmenevents.html">Corporate Events</a>.',
             'Das gilt für Messen ebenso wie für Kundenveranstaltungen.'),
        ],
        'einsaetze': f'''<h2 id="einsaetze">Aus echten Einsätzen</h2>

{para('Dresdner Schlössernacht (Dresden) und Women in Tech Summit (Warschau).', 'realizacja-gala-wsrod-gosci', 'realizacja-women-in-tech-tlum')}

<p>Zwei Formate, ein Roboter: Bei der Dresdner Schlössernacht arbeitete er als Gastgeber eines Balls, auf dem <a href="case-study-women-in-tech.html">Women in Tech Summit</a> mit rund 14.000 Teilnehmenden auf dem Laufsteg und im Publikum.</p>

{para('Unternehmerloge (Nikolaiken) und Finale Eco Studio (Warschau).', 'realizacja-event-nad-woda', 'realizacja-eco-studio-scena')}

<p>Beim Finale von Eco Studio stand er auf der Bühne, beschrieben in der <a href="case-study-eco-studio-electro-system.html">Case Study Eco Studio</a>. Weitere Aufnahmen unter <a href="referenzen-videos.html">Referenzen und Videos</a>.</p>
''',
    },
}


def wczytaj(plik):
    s = plik.read_text(encoding='utf-8')
    m = re.match(r'(<!--\s*)(\{.*?\})(\s*-->)', s, re.S)
    return json.loads(m.group(2)), s[m.end():]


def zapisz(plik, dane, tresc):
    plik.write_text('<!--\n' + json.dumps(dane, ensure_ascii=False, indent=2) + '\n-->\n' + tresc.strip('\n') + '\n', encoding='utf-8')


def main():
    for nazwa, m in STRONY.items():
        plik = ZRODLA / f'{nazwa}.html'
        d, tresc = wczytaj(plik)
        assert tresc.count('<wideo/>') == 1 and tresc.count('<h2 id="einsaetze">') == 1, nazwa
        po = tresc.split('<wideo/>', 1)[1]
        srodek = po.split('<h2 id="einsaetze">', 1)[0].strip('\n') + '\n\n'
        if 'srodek' in m:
            srodek = m['srodek']
        for stare, nowe in m.get('zamiany', []):
            # Drugi przebieg: stary tekst już zamieniony — wtedy nowy musi być na miejscu.
            assert srodek.count(stare) == 1 or (stare not in srodek and nowe in srodek), (nazwa, stare[:50])
            srodek = srodek.replace(stare, nowe)
        d['opis'] = m['opis']
        d['cta_tekst'] = m['cta_tekst']
        d['pytania'] = m['pytania']
        nowa = m['gora'].strip('\n') + '\n\n<wideo/>\n\n' + srodek + m['einsaetze']
        zapisz(plik, d, nowa)
        print(f'{plik.name}: {len(re.sub(r"<[^>]+>", " ", nowa).split())} słów')



# ——— Druga część: główne strony usług i pozostałe strony zastosowań ———
# Własne odpowiedzi w FAQ zamiast trzech wspólnych (cena, dojazd/operator/bezpieczeństwo, termin),
# własne wezwanie do kontaktu i niemiecka realizacja na początku sekcji z realizacjami.

FAQ = {
    'event-attraktionen': {
        'Was kostet ein Roboter für das Event?': 'Ein humanoider Roboter kostet bei 33bots ab 2.500 € pro Veranstaltungstag. Darin stecken Operator, Anfahrt innerhalb Deutschlands, Branding mit Logo und QR-Code sowie die Haftpflichtversicherung. Ab zwei Tagen gibt es 15 % Rabatt auf jeden Tag.',
    },
    'ki-roboter-veranstaltung': {
        'Was kostet ein Roboter mit KI?': 'Ein kompletter Veranstaltungstag mit dem sprechenden Roboter kostet ab 2.500 €, mit Operator, Anfahrt, Branding und Haftpflichtversicherung. Welches Wissen der Roboter für Ihre Veranstaltung braucht, klären wir im ersten Gespräch und nennen danach den konkreten Betrag.',
        'Kommt der Roboter mit Betreuung?': 'Ja. Der Operator ist während der gesamten Veranstaltung beim Roboter. Er achtet auf Abstände, wechselt die Akkus und wacht über den Verlauf der Gespräche, damit die Antworten zum Anlass passen.',
    },
    'roboter-employer-branding': {
        'Was kostet ein Roboter für eine Karrieremesse?': 'Ein Messetag kostet ab 2.500 €, mit Operator, Anfahrt, Branding und Haftpflichtversicherung. Dauert die Karrieremesse zwei Tage oder besuchen Sie mehrere Hochschulen nacheinander, gibt es ab zwei Tagen 15 % Rabatt auf jeden Tag.',
        'Kommt der Roboter mit Betreuung?': 'Ja. Der Operator steuert den Roboter, achtet im Gedränge auf Abstände und wechselt die Akkus. Ihr Recruiting-Team kann sich ganz auf die Gespräche mit den Kandidatinnen und Kandidaten konzentrieren.',
        'Wie früh sollte man einen Roboter für eine Karrieremesse buchen?': 'Sobald Ihr Messetermin feststeht, am besten 3–4 Wochen vorher. So bleibt Zeit, dem Roboter Wissen über Ihr Unternehmen und den Bewerbungsprozess einzuspielen. Eine Anzahlung ist nicht nötig.',
    },
    'roboter-eventmoderation': {
        'Was kostet ein Roboter zur Eventmoderation?': 'Ab 2.500 € pro Veranstaltungstag, mit Operator, Anfahrt, Branding und Haftpflichtversicherung. Übernimmt der Roboter nur einzelne Programmpunkte, etwa Eröffnung und Preisverleihung, kalkulieren wir den kürzeren Auftritt individuell.',
        'Kommt der Roboter mit Betreuung?': 'Ja. Der Operator ist den ganzen Tag vor Ort, steuert den Roboter und stimmt sich mit Regie und Moderation ab, damit die Einsätze auf das Stichwort kommen.',
        'Wie früh sollte man einen Roboter zur Moderation eines Events buchen?': 'Am besten 3–4 Wochen vorher. Die Texte für die Moderation schreiben wir meist 1–2 Wochen vor der Veranstaltung mit Ihnen. Reserviert wird ohne Anzahlung.',
    },
    'roboter-fuer-eventagenturen': {
        'Was kostet ein Roboter für das Event des Kunden?': 'Der Listenpreis beginnt bei 2.500 € pro Veranstaltungstag und enthält Operator, Anfahrt, Branding und Haftpflichtversicherung. Für Ihr Angebot an den Kunden nennen wir einen konkreten Betrag, meist innerhalb von 30 Minuten. Bei fester Zusammenarbeit gelten Partnerkonditionen.',
        'Kommen Sie auch in unsere Stadt?': 'Ja. Wir kommen zu Ihrer Produktion an jeden Ort in Deutschland, ohne Kilometerpauschale. Auf Wunsch schicken wir vorab einen Rider mit Platzbedarf, Stromversorgung und Zeitplan für Ihre Technikplanung.',
    },
    'roboter-gaesteempfang': {
        'Was kostet ein Roboter für den Gästeempfang?': 'Ein kompletter Veranstaltungstag kostet ab 2.500 €, mit Operator, Anfahrt, Branding und Haftpflichtversicherung. Soll der Roboter nur während des Einlasses arbeiten, kalkulieren wir diesen kürzeren Auftritt individuell.',
        'Ist der Roboter für die Gäste sicher?': 'Ja. Am Eingang, wo viele Menschen gleichzeitig ankommen, bleibt der Operator direkt am Roboter und achtet auf Abstände. Zusätzlich erkennt der G1 Personen und Hindernisse über LiDAR und Computer Vision und weicht aus.',
        'Kommen Sie auch in unsere Stadt?': 'Ja. Wir kommen deutschlandweit zu Hotels, Kongresszentren, Firmensitzen und Messehallen. Die Anfahrt ist im Preis enthalten.',
    },
    'roboter-hochschule': {
        'Was kostet ein Roboter für eine Hochschule?': 'Ein Veranstaltungstag kostet ab 2.500 €, mit Operator, Anfahrt, Branding und Haftpflichtversicherung. Für einen Vortrag oder eine kurze Vorführung im Hörsaal kalkulieren wir einen kürzeren Auftritt individuell. Die Rechnung kommt nach der Veranstaltung.',
        'Ist der Roboter für die Gäste sicher?': 'Ja. Der G1 erkennt Personen und Hindernisse über LiDAR und Computer Vision. Der Operator ist durchgehend dabei, auch wenn sich im Foyer oder auf dem Campus viele Studierende um den Roboter drängen.',
        'Wie früh sollte man einen Roboter für eine Hochschulveranstaltung buchen?': 'Am besten 3–4 Wochen vor dem Termin. Hochschulinformationstage und Semesterstart liegen oft in der Eventsaison im Frühjahr und Herbst, dann lohnt sich eine frühere Anfrage. Eine Anzahlung ist nicht nötig.',
    },
    'roboter-show': {
        'Was kostet ein Roboter für eine Show?': 'Ab 2.500 € für einen kompletten Veranstaltungstag mit mehreren Showblöcken, Operator, Anfahrt, Branding und Haftpflichtversicherung. Ein einzelner Bühnenauftritt wird individuell kalkuliert und ist immer günstiger als ein ganzer Tag.',
        'Ist der Roboter für die Gäste sicher?': 'Ja. Auf der Bühne bewegt sich der Roboter in einem vorher festgelegten Bereich, im Publikum begleitet ihn der Operator. Der G1 erkennt Personen und Hindernisse über LiDAR und Computer Vision.',
    },
    'roboter-weihnachtsfeier': {
        'Was kostet ein Roboter für die Weihnachtsfeier?': 'Ein kompletter Veranstaltungstag kostet ab 2.500&nbsp;€, mit Operator, Anfahrt, Branding und Haftpflichtversicherung. Für die Weihnachtsfeier am Abend genügt oft ein kürzerer Auftritt, den wir individuell kalkulieren. Die Rechnung kommt nach der Feier.',
        'Kommen Sie auch in unsere Stadt?': 'Ja. Wir kommen deutschlandweit ins Restaurant, ins Hotel, in die Eventlocation oder direkt in Ihre Firma. Die Anfahrt ist im Preis enthalten.',
    },
    'roboter-werbung-film': {
        'Was kostet ein Roboter für eine Produktion?': 'Ein kompletter Tag am Set kostet ab 2.500 €, mit Operator, Anfahrt und Haftpflichtversicherung. Bei mehreren Drehtagen gibt es ab zwei Tagen 15 % Rabatt auf jeden Tag. Den genauen Betrag nennen wir nach einem Blick auf Drehbuch und Drehplan.',
        'Kommen Sie auch in unsere Stadt?': 'Ja. Wir kommen deutschlandweit ans Set, ins Studio oder an den Drehort. Die Anfahrt ist im Preis enthalten.',
    },
}

CTA = {
    'angebot-konferenzen-galas': 'Nennen Sie uns Datum, Location und Art der Veranstaltung. Wir schlagen eine Rolle für den Roboter vor und antworten meist innerhalb von 30 Minuten.',
    'angebot-messen': 'Nennen Sie uns Messe, Standgröße und Termin. Die Antwort mit dem Preis für Ihre Messetage kommt meist innerhalb von 30 Minuten.',
    'angebot-tag-der-offenen-tuer': 'Schreiben Sie uns Termin und Ort Ihres Tags der offenen Tür. Sie erhalten meist innerhalb von 30 Minuten eine Antwort mit Preis und Verfügbarkeit.',
    'humanoiden-roboter-mieten': 'Nennen Sie uns Datum, Ort und Anlass. Wir antworten meist innerhalb von 30 Minuten, am Telefon nennen wir den Preis sofort: +48 531 408 004.',
    'ki-roboter-veranstaltung': 'Schreiben Sie uns, worüber der Roboter sprechen soll, und nennen Sie Datum und Ort. Die Antwort kommt meist innerhalb von 30 Minuten.',
    'roboter-employer-branding': 'Nennen Sie uns Messe oder Hochschultag und den Termin. Wir antworten meist innerhalb von 30 Minuten mit Preis und Verfügbarkeit.',
    'roboter-eventmoderation': 'Schicken Sie uns Datum, Ort und den groben Ablauf. Wir schlagen vor, welche Programmpunkte der Roboter übernimmt, meist innerhalb von 30 Minuten.',
    'roboter-fuer-eventagenturen': 'Schreiben Sie uns Termin, Ort und das Briefing Ihres Kunden. Den Preis für Ihr Angebot nennen wir meist innerhalb von 30 Minuten.',
    'roboter-gaesteempfang': 'Nennen Sie uns Datum, Location und die Zeit des Einlasses. Sie erhalten meist innerhalb von 30 Minuten eine Antwort mit Preis und Verfügbarkeit.',
    'roboter-hochschule': 'Schreiben Sie uns Termin, Hochschule und Anlass. Die Antwort mit Preis und Verfügbarkeit kommt meist innerhalb von 30 Minuten.',
    'roboter-hochzeit': 'Schreiben Sie uns Hochzeitstermin und Location. Wir melden uns meist innerhalb von 30 Minuten mit einem konkreten Betrag.',
    'roboter-show': 'Nennen Sie uns Datum, Ort und die Bühnenzeiten. Wir schlagen Showblöcke vor und nennen den Preis, meist innerhalb von 30 Minuten.',
    'roboter-weihnachtsfeier': 'Schreiben Sie uns Termin und Ort Ihrer Weihnachtsfeier. Sie erhalten meist innerhalb von 30 Minuten eine Antwort mit Preis und Verfügbarkeit.',
    'roboter-werbung-film': 'Schicken Sie uns Drehtermin, Drehort und eine kurze Beschreibung der Szene. Wir antworten meist innerhalb von 30 Minuten.',
}
CTA_STARE = 'Schreiben Sie uns — Sie erhalten innerhalb eines Werktags ein Angebot inklusive Verfügbarkeit.'
CTA_OGOLNE = 'Schreiben Sie uns. Sie erhalten meist innerhalb von 30 Minuten eine Antwort mit Preis und Verfügbarkeit.'

SIEDEM_MIAST = ('<a href="roboter-mieten-berlin.html">Berlin</a>, <a href="roboter-mieten-muenchen.html">München</a>, '
                '<a href="roboter-mieten-hamburg.html">Hamburg</a>, <a href="roboter-mieten-koeln.html">Köln</a>, '
                '<a href="roboter-mieten-frankfurt.html">Frankfurt am Main</a>, <a href="roboter-mieten-duesseldorf.html">Düsseldorf</a> '
                'und <a href="roboter-mieten-dresden.html">Dresden</a>')

ALT.update({
    'realizacja-women-in-tech-wybieg': 'Humanoider Roboter auf dem rosa Laufsteg des Women in Tech Summit',
})

# (plik, wzorzec regex albo tekst, zamiennik, znacznik obecny po zamianie)
POPRAWKI = [
    ('humanoiden-roboter-mieten',
     r'<p>Wir kommen in jede Stadt in Deutschland, ohne Kilometerpauschale\. Mehr zu einzelnen Städten:.*?</p>',
     f'<p>Wir kommen in jede Stadt in Deutschland, ohne Kilometerpauschale. Für sieben Städte gibt es eigene Seiten mit Messen, Locations und Beispielen: {SIEDEM_MIAST}.</p>',
     'Für sieben Städte gibt es eigene Seiten'),
    ('humanoiden-roboter-mieten',
     r'<h2 id="einsaetze">Aus echten Einsätzen</h2>\s*(?=<para podpis="Women in Tech Summit)',
     f'''<h2 id="einsaetze">Aus echten Einsätzen</h2>

<p>Über 100 Veranstaltungen in fünf Ländern, in Deutschland zum Beispiel die Dresdner Schlössernacht: Dort trat der Roboter im Paillettensmoking mit Krone auf, auf dem roten Teppich, im Ballsaal und unter den Gästen.</p>

{para('Dresdner Schlössernacht (Dresden): auf dem roten Teppich und unter den Gästen.', 'realizacja-gala-czerwony-dywan', 'realizacja-gala-wsrod-gosci')}

''',
     'Dresdner Schlössernacht (Dresden): auf dem roten Teppich und unter den Gästen.'),
    ('roboter-weihnachtsfeier',
     r'<p>Wir sind deutschlandweit im Einsatz, die Anfahrt ist im Preis enthalten\. Mehr zu einzelnen Städten:.*?</p>',
     f'<p>Wir sind deutschlandweit im Einsatz, die Anfahrt ist im Preis enthalten. Eigene Seiten gibt es für {SIEDEM_MIAST}.</p>',
     'Eigene Seiten gibt es für'),
    ('unitree-g1-mieten',
     r'(<h2 id="ablauf">So läuft die Miete ab</h2>)\s*<ol>.*?</ol>',
     r'''\1

<p>Die Miete läuft in vier Schritten ab: Anfrage, Drehbuch und Vertrag, Veranstaltung, Rechnung. Eine Anzahlung gibt es nicht, und um die Technik kümmert sich der Operator. Die einzelnen Schritte beschreibt die Seite <a href="humanoiden-roboter-mieten.html#ablauf">Humanoiden Roboter mieten</a>.</p>''',
     'Die Miete läuft in vier Schritten ab'),
    ('angebot-messen',
     r'(?=<h2 id="einsaetze">)',
     '''<h2 id="messen-in-deutschland">Messen in Deutschland: wo sich ein Roboter anbietet</h2>

<p>Deutschland ist das Land der Leitmessen, und an jedem großen Messeplatz gibt es Formate, zu denen ein humanoider Roboter passt. Für sechs Standorte haben wir die Messen und die jeweilige Aufgabe des Roboters beschrieben:</p>

<ul>
  <li><a href="roboter-mieten-berlin.html">Berlin</a> — IFA, ITB, InnoTrans und Grüne Woche auf dem Messegelände unter dem Funkturm.</li>
  <li><a href="roboter-mieten-muenchen.html">München</a> — automatica, bauma, EXPO REAL und electronica in Riem.</li>
  <li><a href="roboter-mieten-frankfurt.html">Frankfurt am Main</a> — Automechanika, Light + Building, Buchmesse und Ambiente.</li>
  <li><a href="roboter-mieten-koeln.html">Köln</a> — gamescom, DMEXCO, FIBO und Anuga auf der Koelnmesse.</li>
  <li><a href="roboter-mieten-duesseldorf.html">Düsseldorf</a> — MEDICA, EuroShop, boot und K.</li>
  <li><a href="roboter-mieten-hamburg.html">Hamburg</a> — SMM, INTERNORGA, WindEnergy und das OMR Festival.</li>
</ul>

<p>Für Messen über mehrere Tage gibt es ab zwei Veranstaltungstagen 15&nbsp;% Rabatt auf jeden Tag. Die Anfahrt ist deutschlandweit im Preis enthalten, und beim Aufbau richten wir uns nach den Zeiten des Veranstalters.</p>

''',
     '<h2 id="messen-in-deutschland">'),
    ('angebot-messen',
     r'<p>Weitere Aufnahmen und Videos finden Sie unter <a href="referenzen-videos\.html">Referenzen</a>\.</p>',
     '<p>Wie ein zweitägiger Messeeinsatz abläuft, beschreibt die <a href="case-study-grupa-rekord-mspo.html">Case Study MSPO</a>. Weitere Aufnahmen und Videos stehen unter <a href="referenzen-videos.html">Referenzen</a>.</p>',
     'Wie ein zweitägiger Messeeinsatz abläuft'),
    ('angebot-konferenzen-galas',
     r'<h3>Was mit dem Roboter geht</h3>\s*<p>.*?</p>',
     '''<h3>Festliches Branding</h3>

<p>Bei der Dresdner Schlössernacht trug der Roboter Paillettensmoking und Krone. Was zu Ihrem Abend passt, stimmen wir vorher ab. Logo und QR-Code auf der Brust sind im Preis enthalten.</p>''',
     '<h3>Festliches Branding</h3>'),
    ('angebot-konferenzen-galas',
     r'<p>Timing und Positionen legen wir vorab mit Ihrer Regie fest — Details bei <a href="angebot-konferenzen-galas\.html">Roboter für Galas</a>\.</p>',
     '<p>Timing und Positionen legen wir vorab mit Ihrer Regie fest. Die Bausteine eines Bühnenauftritts beschreibt die Seite <a href="roboter-show.html">Roboter-Show</a>.</p>',
     'Die Bausteine eines Bühnenauftritts beschreibt die Seite'),
    ('angebot-konferenzen-galas',
     r'<h2 id="einsaetze">Aus echten Einsätzen</h2>.*\Z',
     f'''<h2 id="dresdner-schloessernacht">Beispiel aus Deutschland: Dresdner Schlössernacht</h2>

<p>Bei der Dresdner Schlössernacht war der Roboter Gastgeber eines Balls in einem Dresdner Palais. Im Paillettensmoking mit Krone stand er auf dem roten Teppich vor der Sponsorenwand, bewegte sich durch den Ballsaal und war den Abend über zwischen den Gästen unterwegs. Das Branding folgte dem Anlass: festlich statt technisch.</p>

{para('Dresdner Schlössernacht (Dresden): roter Teppich und Ballsaal.', 'realizacja-gala-czerwony-dywan', 'realizacja-gala-palac')}

{para('Dresdner Schlössernacht (Dresden): unter den Gästen des Abends.', 'realizacja-gala-wsrod-gosci', 'realizacja-gala-zdjecia-gosci')}

<p>Was eine Veranstaltung in Dresden und Sachsen braucht, steht auf der Seite <a href="roboter-mieten-dresden.html">Roboter mieten in Dresden</a>.</p>

<h2 id="einsaetze">Weitere Einsätze: Konferenz und Bühne</h2>

{para('Women in Tech Summit (Warschau) und Finale Eco Studio (Warschau).', 'realizacja-women-in-tech-wybieg', 'realizacja-eco-studio-scena')}

<p>Auf dem <a href="case-study-women-in-tech.html">Women in Tech Summit</a> mit rund 14.000 Teilnehmenden war der Roboter auf dem Laufsteg und mitten unter den Teilnehmerinnen im Einsatz. Für Finanz- und Fachkonferenzen ist die <a href="case-study-wallstreet.html">Case Study WallStreet 30</a> der passende Vergleich. Weitere Aufnahmen stehen unter <a href="referenzen-videos.html">Referenzen und Videos</a>.</p>
''',
     '<h2 id="dresdner-schloessernacht">'),
    ('barrierefreiheit',
     r'oder rufen Sie an unter Wir antworten',
     'oder rufen Sie an unter <a href="tel:+48531408004">+48&nbsp;531&nbsp;408&nbsp;004</a>. Wir antworten',
     'rufen Sie an unter <a href="tel:+48531408004">'),
]


def druga_czesc():
    for nazwa, pary in FAQ.items():
        plik = ZRODLA / f'{nazwa}.html'
        d, tresc = wczytaj(plik)
        pytania = [p for p, _ in d['pytania']]
        for pyt, odp in pary.items():
            assert pytania.count(pyt) == 1, (nazwa, pyt)
            d['pytania'][pytania.index(pyt)][1] = odp
        zapisz(plik, d, tresc)
    for plik in sorted(ZRODLA.glob('*.html')):
        d, tresc = wczytaj(plik)
        if plik.stem in CTA:
            d['cta_tekst'] = CTA[plik.stem]
        elif d.get('cta_tekst') == CTA_STARE:
            d['cta_tekst'] = CTA_OGOLNE
        else:
            continue
        zapisz(plik, d, tresc)
    for nazwa, wzorzec, nowe, znacznik in POPRAWKI:
        plik = ZRODLA / f'{nazwa}.html'
        d, tresc = wczytaj(plik)
        if znacznik in tresc:
            continue
        nowa, ile = re.subn(wzorzec, nowe, tresc, count=1, flags=re.S)
        assert ile == 1 and znacznik in nowa, (nazwa, wzorzec[:60])
        zapisz(plik, d, nowa)
        print(f'{plik.name}: poprawka „{znacznik[:50]}”')


if __name__ == '__main__':
    main()
    druga_czesc()
