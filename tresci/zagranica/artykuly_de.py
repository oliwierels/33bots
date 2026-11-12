# -*- coding: utf-8 -*-
"""Pełne wersje czterech artykułów 33bots.de, które miały po ok. 200 słów (11.2026).

Krótkie streszczenia nie mają czego wnieść do wyników wyszukiwania. Cztery artykuły były
streszczeniami polskich oryginałów (189–221 słów, bez FAQ). Tutaj dostają pełną treść opartą na
oryginałach z 33bots.pl (psychologia spotkania z robotem, business case dla zarządu, bezpieczeństwo,
trendy) oraz pytania i odpowiedzi. Fakty wyłącznie z polskich oryginałów i dotychczasowych stron .de.

    python3 tresci/zagranica/artykuly_de.py     # potem buduj_podstrony.py de <repo>
"""
import json
import re
from pathlib import Path

ZRODLA = Path(__file__).resolve().parent / 'podstrony' / 'de'

ARTYKULY = {
    'blog-psychologie-humanoider-roboter': {
        'lead': 'Auf jeder Veranstaltung läuft dieselbe Szene ab: Jemand sieht den Roboter aus dem Augenwinkel, bleibt stehen und zieht das Handy. Dahinter stehen gut beschriebene Mechanismen, die sich planen lassen.',
        'pytania': [
            ['Warum ziehen humanoide Roboter so viel Aufmerksamkeit auf sich?', 'Das menschliche Gehirn behandelt Reize bevorzugt, die bekannte Muster brechen. Eine Gestalt, die sich wie ein Mensch bewegt und doch eine Maschine ist, ist genau so ein Reiz. Deshalb zieht ein Humanoid Blicke an, ohne Ansage und ohne Werbung.'],
            ['Löst ein humanoider Roboter Unbehagen aus?', 'Das Uncanny Valley betrifft vor allem Androiden, die Gesicht und Haut des Menschen nachahmen. Der Unitree G1 sieht bei menschlicher Silhouette eindeutig wie ein Roboter aus und löst deshalb Faszination statt Unbehagen aus.'],
            ['Wie reagieren Kinder auf den Roboter?', 'Meist in derselben Abfolge: ein Moment Schüchternheit, dann schnell wachsende Begeisterung. Der Operator beginnt die ersten Begegnungen aus der Distanz, und nach wenigen Minuten winken die Kinder, geben High Fives und tanzen mit.'],
            ['Wie plant man die Begegnung der Gäste mit dem Roboter?', 'Am besten wirkt die Verbindung aus Bewegung und Kontakt: ein Roboter, der sich in einer festgelegten Zone bewegt, Momente der Begrüßung und Zeit für Fotos und kurze Gespräche. Eine rein statische Vorführung nutzt nur einen Bruchteil der Wirkung.'],
        ],
        'tresc': '''
<p>Die Reaktion auf einen humanoiden Roboter ist keine Glückssache. Auf unseren Veranstaltungen sehen wir immer wieder dieselbe Abfolge: ein Blick, Stehenbleiben, eine Sekunde Prüfung, ob da nicht doch ein Mensch drinsteckt, dann das Handy. Beim Bankvorstand läuft das genauso ab wie beim Sechsjährigen. Für Veranstalter ist das eine gute Nachricht, denn was vorhersehbar ist, lässt sich nutzen.</p>

<h2 id="neuheit">Neuheit: Das Gehirn kann nicht wegsehen</h2>

<p>Unser Gehirn sucht ständig nach Dingen, die nicht ins Muster passen. Eine Gestalt, die läuft und gestikuliert wie ein Mensch, aber keiner ist, hat für die Aufmerksamkeit höchste Priorität. Man kann an ihr nicht im Autopilot vorbeigehen, so wenig, wie man eine plötzliche Bewegung am Rand des Blickfelds ignorieren kann.</p>

<p>Für die Praxis heißt das: Der Roboter braucht keine Ansage, keinen Moderator und keine Pfeile auf dem Boden. Es genügt, dass er da ist und sich bewegt. Deshalb bringt er auf Messen schneller Betrieb an den Stand als ein Gewinnspiel.</p>

<h2 id="wir-sehen-absicht-wo-keine">Anthropomorphismus: Wir sehen Absicht, wo keine ist</h2>

<p>Das zweite Phänomen ist noch interessanter. Menschen schauen den Humanoiden nicht nur an, sie begrüßen ihn. Sie winken, sagen „Guten Tag“ und entschuldigen sich, wenn sie ihm in den Weg treten. Eine Gestalt mit menschlichen Proportionen löst soziale Reflexe aus, bevor der Verstand sich einschaltet.</p>

<p>Deshalb wirken Interaktionen mit dem G1 so stark: der Handschlag, das gemeinsame Foto, das kurze Gespräch. Der Gast besichtigt keine Technik, er knüpft für dreißig Sekunden eine Beziehung. Und Beziehungen merkt man sich anders als Exponate. Auf diesem Mechanismus beruht die Rolle des <a href="roboter-gaesteempfang.html">Roboters am Gästeempfang</a>.</p>

<h2 id="warum-der-g1-nicht-hineinfaellt">Uncanny Valley: Warum der G1 nicht hineinfällt</h2>

<p>Das „unheimliche Tal“ beschreibt, dass Roboter, die Menschen täuschend ähnlich sehen, Unbehagen auslösen. Je näher am menschlichen Gesicht, desto stärker stört jede Kleinigkeit, die nicht stimmt. Für Androiden mit Silikonhaut ist das ein echtes Problem.</p>

<p>Der Unitree G1 steht auf der sicheren Seite des Tals. Er hat eine menschliche Silhouette und menschliche Bewegungen, sieht aber eindeutig wie eine Maschine aus. Niemand zweifelt daran, was er vor sich hat, und deshalb entsteht Faszination statt Unbehagen. Auch kleine Kinder wechseln nach unserer Erfahrung in wenigen Minuten von Schüchternheit zu Begeisterung. Mehr dazu im <a href="roboter-privatfeier.html#roboter-auf-kinderveranstaltungen-der-leitfaden">Leitfaden für Kinderveranstaltungen</a>.</p>

<h2 id="warum-sich-trauben-bilden">Warum sich Trauben bilden</h2>

<p>Menschen bleiben stehen, weil andere stehen bleiben. Der Roboter startet diesen Effekt, die Gruppe verstärkt ihn. Wer eine Traube sieht, will wissen, was es dort gibt, und wer Handys in der Luft sieht, hebt sein eigenes.</p>

<h2 id="was-das-fuer-ihren-ablauf">Was das für Ihren Ablauf bedeutet</h2>

<ul>
  <li><strong>Geben Sie dem Roboter Bewegung und Platz.</strong> Ein laufender Roboter wirkt um ein Vielfaches stärker als ein stehender. Planen Sie eine Zone ein, in der er sich bewegen kann, und Raum für die Traube. Stellen Sie ihn nicht in eine Ecke.</li>
  <li><strong>Planen Sie Begegnung, nicht nur Vorführung.</strong> Die stärksten Emotionen entstehen im Kontakt: beim Handschlag, im Gespräch, beim gemeinsamen Foto.</li>
  <li><strong>Nutzen Sie die ersten 30 Sekunden.</strong> Die Begrüßung durch den Roboter setzt den emotionalen Ton der ganzen Veranstaltung.</li>
  <li><strong>Zeigen statt erklären.</strong> Der Roboter braucht keine Einführung. Je natürlicher die Begegnung, desto stärker die Reaktion.</li>
</ul>

<p>Wo der Roboter auf einem Messestand am besten steht, beschreibt der Abschnitt <a href="angebot-messen.html#roboter-am-messestand-so-entstehen">Roboter am Messestand</a>.</p>
''',
    },

    'blog-geschaeftsfuehrung-ueberzeugen': {
        'lead': '„Nett, aber wozu brauchen wir das?“ Wenn dieser Satz Ihre Idee blockiert, hilft diese Argumentation: Zielgrößen, Vergleichskosten und Antworten auf die drei häufigsten Einwände.',
        'pytania': [
            ['Wie begründe ich die Kosten eines Roboters vor der Geschäftsführung?', 'Verlagern Sie die Diskussion von den Kosten der Attraktion auf das Geschäftsziel: Zahl der Vertriebsgespräche, gesammelte Kontakte, Reichweite des Contents und Wirkung im Employer Branding. Vergleichen Sie die Kosten mit Alternativen, die das Unternehmen bereits finanziert, und legen Sie die Messgrößen vor der Veranstaltung fest.'],
            ['Welche Messgrößen sollte man vor der Veranstaltung festlegen?', 'Am häufigsten: die Zahl der gescannten Kontakte oder Gespräche am Stand, der geschätzte Betrieb in der Zone des Roboters, Reichweite und Interaktionen der Beiträge sowie Erwähnungen der Marke. Im Recruiting kommen Bewerbungen und Gespräche mit Kandidaten dazu.'],
            ['Gibt es Belege, dass ein Roboter auf Business-Veranstaltungen funktioniert?', 'Ja. Unser Roboter arbeitete unter anderem auf der Konferenz WallStreet 30 in Karpacz mit 2.253 Teilnehmenden und auf dem Women in Tech Summit in Warschau mit rund 14.000 Teilnehmenden. Beide Case Studies stehen auf dieser Website.'],
            ['Was bekomme ich für die Präsentation vor der Geschäftsführung?', 'Auf Wunsch schicken wir ein Paket: den Preis für Ihren Termin, Videomaterial von Einsätzen, Beispiele für Drehbücher und den technischen Rider.'],
        ],
        'tresc': '''
<p>Die Idee ist meist schnell verkauft, das Budget nicht. Die folgende Struktur funktioniert für Messen, Konferenzen, Galas und interne Veranstaltungen.</p>

<h2 id="nicht-als-attraktion-sondern-als">Das Problem ist nicht das Budget, sondern die Kategorie</h2>

<p>Wer der Geschäftsführung einen Roboter vorschlägt, landet in deren Köpfen in der Kategorie „Gag“. Und über Gags verläuft die Diskussion immer gleich: nett, aber verzichtbar. Ihre Aufgabe ist deshalb nicht, die Kosten zu verteidigen. Ihre Aufgabe ist, den Roboter in die richtige Kategorie zu verschieben: eine Marketingmaßnahme mit messbarem Ergebnis.</p>

<h2 id="aufmerksamkeit-und-leads">Argument 1: Aufmerksamkeit und Leads</h2>

<p>Beginnen Sie mit einem Problem, das die Geschäftsführung kennt: Auf Messen wird Aufmerksamkeit teurer. Standflächen kosten mehr, und ein Besucher schenkt einem Stand im Vorbeigehen wenige Sekunden. Ein humanoider Roboter löst genau dieses Problem, weil er Betrieb erzeugt, den man nicht mit Werbung einkaufen muss.</p>

<p>Zeigen Sie den Mechanismus: Der Roboter zieht an, die Traube hält weitere Besucher auf, und der Vertrieb spricht mit Menschen, die von selbst gekommen sind. Wie sich das in Kennzahlen übersetzen lässt, steht im Abschnitt <a href="angebot-messen.html#roi-eines-roboters-am-messestand">ROI eines Roboters am Messestand</a>.</p>

<h2 id="content">Argument 2: ein Event, wochenlang Material</h2>

<p>Das zweite Argument erreicht alle, die für Content-Produktion bezahlen. Aufnahmen mit dem Roboter, also Begrüßungen, Tanz und Reaktionen der Gäste, sind fertiges Material für die Kanäle des Unternehmens. Statt eines Beitrags „Wir waren auf der Messe“ entsteht eine Serie kurzer Videos, die über Wochen weiterläuft.</p>

<h2 id="employer-branding">Argument 3: Employer Branding als Beweis</h2>

<p>Jedes Unternehmen schreibt über Innovation, wenige können sie zeigen. Ein Humanoid auf der Karrieremesse oder beim Tag der offenen Tür ist ein greifbarer Beleg für den technologischen Anspruch, den Kandidatinnen und Kandidaten fotografieren und weitertragen. Mehr dazu unter <a href="roboter-employer-branding.html">Roboter im Employer Branding</a>.</p>

<h2 id="gegen-welche-kosten-sie-rechnen">Der Business Case in fünf Punkten</h2>

<ol>
  <li><strong>Geschäftsziel:</strong> zum Beispiel eine Zahl von Vertriebsgesprächen auf der Messe, Bewerbungen nach dem Tag der offenen Tür oder die Reichweite rund um eine Premiere.</li>
  <li><strong>Mechanismus:</strong> wie der Roboter dieses Ziel erreicht, über Standfrequenz, Content oder Teilnahme.</li>
  <li><strong>Kosten gegen Alternativen:</strong> Vergleichen Sie mit dem, was das Unternehmen ohnehin ausgibt: zusätzliche Standfläche, Gewinnspiele mit Preisen, bezahlte Reichweite oder ein prominenter Speaker.</li>
  <li><strong>Messgrößen:</strong> gescannte Kontakte, Betrieb am Stand, Reichweite der Beiträge, Erwähnungen. Legen Sie sie vor der Veranstaltung fest.</li>
  <li><strong>Risiken und Absicherung:</strong> Operator im Preis, Haftpflichtversicherung, technischer Rider und dokumentierte Einsätze.</li>
</ol>

<p>Ein Veranstaltungstag kostet ab 2.500&nbsp;€, ab zwei Tagen gibt es 15&nbsp;% Rabatt auf jeden Tag. Was darin enthalten ist, steht unter <a href="roboter-mieten-preise.html">Preise und Kosten</a>.</p>

<h2 id="die-drei-haeufigsten">Die drei häufigsten Einwände</h2>

<p><strong>„Das ist ein Gag, keine Investition.“</strong> Ein Gag erzeugt keine Schlange von Gesprächen am Stand. Zeigen Sie Case Studies und legen Sie Messgrößen fest. Nach der Veranstaltung rechnen Sie den Roboter ab wie jede andere Marketingmaßnahme.</p>

<p><strong>„Und wenn etwas schiefgeht?“</strong> Der Roboter arbeitet ausschließlich mit Operator, die Haftpflichtversicherung ist im Preis, und Drehbuch und Rider werden vor der Veranstaltung abgestimmt. Mehr dazu im Beitrag <a href="blog-sicherheit-roboter-event.html">Ist ein Roboter auf dem Event sicher?</a></p>

<p><strong>„In einem Jahr haben das alle.“</strong> Möglich. Genau deshalb ist der Vorsprung jetzt zu haben und nicht in einem Jahr.</p>

<h2 id="referenzen-zeigen">Referenzen zeigen</h2>

<p>Konkrete Fälle helfen mehr als Argumente. In Deutschland war der Roboter bei der Dresdner Schlössernacht im Einsatz. Für Business-Formate eignen sich zwei Case Studies: <a href="case-study-wallstreet.html">WallStreet 30</a>, das größte Treffen von Privatanlegern in Polen mit 2.253 Teilnehmenden, und der <a href="case-study-women-in-tech.html">Women in Tech Summit</a> mit rund 14.000 Teilnehmenden. Beide lassen sich direkt in eine Präsentation übernehmen.</p>
''',
    },

    'blog-sicherheit-roboter-event': {
        'lead': 'Diese Frage stellen jede Verwaltung und jeder Betreiber einer Location. Die Antwort besteht aus drei Teilen: Operator, Sensorik und Versicherung, dazu feste Abläufe bei jedem Einsatz.',
        'pytania': [
            ['Was passiert, wenn der Roboter in der Menge das Gleichgewicht verliert?', 'Der G1 stabilisiert seine Haltung aktiv, und die Pufferzone trennt ihn vom Publikum. Bei Bedarf hält der Operator den Roboter sofort an.'],
            ['Brauchen wir zusätzliche Genehmigungen für den Auftritt?', 'In geschlossenen Räumen genügt in der Regel die Zustimmung des Betreibers. Bei Veranstaltungen im Freien helfen wir, die Unterlagen zusammenzustellen.'],
            ['Ist der Roboter versichert?', 'Ja. Die Haftpflichtversicherung ist im Mietpreis enthalten und deckt Auftritte vor Publikum ab.'],
            ['Dürfen Gäste den Roboter anfassen?', 'Ja, unter Aufsicht. Handschlag, High Five und gemeinsames Foto gehören zum Programm und finden auf das Zeichen des Operators statt.'],
        ],
        'tresc': '''
<p>Bei Veranstaltungen mit Kindern oder großen Menschenmengen ist das die erste Frage, die uns Veranstalter stellen. Sie ist berechtigt: Der Unitree G1 ist rund 132&nbsp;cm groß, etwa 35&nbsp;kg schwer und bewegt sich frei zwischen Menschen.</p>

<h2 id="der-operator-als-zweite-instanz">Der Operator: immer und ohne Ausnahme</h2>

<p>Der Roboter arbeitet nie allein. Ein Operator von 33bots steuert ihn oder überwacht seine autonomen Modi während der gesamten Veranstaltung, kontrolliert den Abstand zu den Gästen und kann jede Bewegung sofort anhalten. Er entscheidet auch, was bei vollem Gang oder vollem Saal möglich ist.</p>

<h2 id="lidar-und-computer-vision">LiDAR und Computer Vision</h2>

<p>Der Roboter erkennt Hindernisse und Personen in Echtzeit und weicht ihnen aus. Das ist keine Zusatzoption, sondern Grundausstattung. Die Sensorik ist dabei die zweite Absicherung, nicht die erste. Die erste ist der Mensch, der neben dem Roboter steht.</p>

<h2 id="ablaeufe">Vier Abläufe, die bei jedem Einsatz gelten</h2>

<ul>
  <li><strong>Showfläche:</strong> Wir legen den Bewegungsbereich des Roboters fest und lassen einen Puffer zum Publikum.</li>
  <li><strong>Kontrolle des Bodens:</strong> Vor dem Auftritt prüfen wir den Untergrund auf Ebenheit und Halt. Rasen, Kies und Sand scheiden aus.</li>
  <li><strong>Sofortiger Stopp:</strong> Der Operator kann den Roboter jederzeit anhalten.</li>
  <li><strong>Kontrollierte Interaktionen:</strong> High Fives und Fotos finden auf das Zeichen des Operators statt.</li>
</ul>

<h2 id="haftpflichtversicherung">Haftpflichtversicherung und Unterlagen</h2>

<p>Eine Haftpflichtversicherung, die Auftritte vor Publikum abdeckt, ist im Preis enthalten. Auf Wunsch liefern wir Unterlagen für den Betreiber der Location und eine technische Beschreibung des Geräts, für Messeveranstalter die nötigen Angaben zu Gerät und Betrieb. In geschlossenen Räumen genügt in der Regel die Zustimmung des Betreibers. Für Auftritte im öffentlichen Raum braucht es die Zustimmung des Flächenbetreibers, bei der Organisation helfen wir.</p>

<h2 id="was-wir-zusaetzlich-beachten">Kinder: Was wir zusätzlich beachten</h2>

<p>Bei Kinderveranstaltungen arbeiten wir mit einem klar markierten Interaktionsbereich. Wir beginnen aus der Distanz, erklären die Regeln spielerisch und lassen Begegnungen nur unter Aufsicht zu. Kurze Blöcke von etwa 15 Minuten funktionieren besser als Dauerbetrieb. Details stehen im <a href="roboter-privatfeier.html#roboter-auf-kinderveranstaltungen-der-leitfaden">Leitfaden für Kinderveranstaltungen</a>.</p>

<h2 id="wetter-und-technik">Wetter und Technik</h2>

<p>Der G1 ist nicht wetterfest. Im Freien tritt er nur auf trockener, ebener Fläche auf, und für den Regenfall planen wir vorher eine überdachte Alternative. Vor Ort braucht er rund 2×2&nbsp;m und eine 230-V-Steckdose. Mehr zu Außeneinsätzen steht unter <a href="roboter-stadtfest.html#roboter-beim-outdoor-event">Roboter beim Outdoor-Event</a>, die technischen Daten unter <a href="unitree-g1-mieten.html">Unitree G1 mieten</a>.</p>
''',
    },

    'blog-trends-humanoide-roboter-events': {
        'lead': 'Vor zwei Jahren war ein Humanoid auf einer Veranstaltung Science-Fiction. Heute tritt er im Fernsehen und auf großen Konferenzen auf. Was sich geändert hat und was daraus für Veranstalter folgt.',
        'pytania': [
            ['Werden humanoide Roboter teurer oder günstiger?', 'Die Preise der Geräte sinken mit jeder Generation. Gleichzeitig wächst die Bedeutung dessen, was um das Gerät herum entsteht: Drehbuch, Choreografie und die Einbindung in Marketingziele. Der Roboter selbst ist ein immer kleinerer Teil des Werts eines Auftritts.'],
            ['Wann beeindruckt ein Roboter auf einer Veranstaltung nicht mehr?', 'Noch einige Jahre lang werden die meisten Menschen keinen Humanoiden live erlebt haben. Und ein gut inszenierter Auftritt beeindruckt auch diejenigen, die schon einen Roboter gesehen haben, so wie ein gutes Konzert trotz Tausender anderer Konzerte.'],
            ['Womit sollten Veranstalter heute anfangen?', 'Mit einer klaren Rolle für den Roboter: Gastgeber am Eingang, Assistent am Messestand oder Programmpunkt auf der Bühne. Dazu kommen ein Drehbuch, Branding und eine Messgröße, an der sich der Auftritt nach der Veranstaltung beurteilen lässt.'],
        ],
        'tresc': '''
<p>Wir sehen jedes Jahr, wie sich die Anfragen verändern. Diese Entwicklungen zeichnen sich klar ab.</p>

<h2 id="was-sich-geaendert-hat">Was sich geändert hat: niedrigere Preise, mehr Fähigkeiten</h2>

<p>Mit dem Unitree G1, dessen Einstiegspreis bei rund 16.000 US-Dollar liegt, ist die Schwelle zur humanoiden Robotik um ein Vielfaches gesunken. Die Folge: Humanoide haben die Labore verlassen und stehen auf Veranstaltungen, im Handel und in den Medien. Unser G1 war in der Nachrichtensendung Teleexpress (TVP) und in einer Reportage von TVP Danzig zu sehen, beschrieben in der <a href="case-study-lexai.html">Case Study LEX AI</a>.</p>

<h2 id="von-der-show-zur-funktion">Von der Show zur Funktion</h2>

<p>Immer mehr Kunden buchen den Roboter nicht als Attraktion, sondern für eine Aufgabe. Niemand will mehr einen Roboter, der nur dasteht. Gefragt ist ein Roboter mit Rolle: Er begrüßt, überreicht, moderiert mit. Was das konkret heißt, beschreiben die Seiten <a href="roboter-gaesteempfang.html">Gästeempfang</a> und <a href="roboter-eventmoderation.html">Eventmoderation</a>.</p>

<h2 id="branding-und-messbarkeit">Branding und Messbarkeit</h2>

<p>Der WOW-Effekt allein reicht Auftraggebern nicht mehr. Ein QR-Code auf der Brust des Roboters und gezählte Kontakte machen aus dem Auftritt eine Maßnahme, die sich abrechnen lässt. Wie man intern dafür argumentiert, steht im Beitrag <a href="blog-geschaeftsfuehrung-ueberzeugen.html">Die Geschäftsführung überzeugen</a>.</p>

<h2 id="sprachfunktion-wird-zum-standard">Sprachfunktion wird zum Standard</h2>

<p>Texte werden für die Marke und den Anlass geschrieben, und der Roboter beantwortet Fragen zu Veranstaltung, Unternehmen und Angebot. Vor dem Termin spielen wir ihm ein, was er wissen soll. Mehr dazu unter <a href="ki-roboter-veranstaltung.html#ki-roboter-der-deutsch-spricht">KI-Roboter, der Deutsch spricht</a>.</p>

<h2 id="oeffentlicher-raum">Auftritte im öffentlichen Raum</h2>

<p>Auftritte auf Plätzen und in Fußgängerzonen ziehen Passanten und Redaktionen an. Sie brauchen die Zustimmung des Flächenbetreibers und eine ebene, trockene Fläche. Was dabei zu beachten ist, steht unter <a href="roboter-stadtfest.html#roboter-beim-outdoor-event">Roboter beim Outdoor-Event</a>.</p>

<h2 id="mehrere-einheiten-pro-event">Mehrere Einheiten pro Event</h2>

<p>Bei großen Flächen fragen Kunden zunehmend zwei oder mehr Roboter an, um mehrere Zonen gleichzeitig zu bespielen.</p>

<h2 id="sinkende-neuheitspraemie">Sinkende Neuheitsprämie</h2>

<p>Der Vorsprung des Ersten wirkt noch: Die meisten Menschen haben einen Humanoiden nie live gesehen. Aber das Fenster schließt sich. Wenn Roboter alltäglich werden, gewinnt nicht mehr der Roboter selbst, sondern die Idee für seine Rolle in der Veranstaltung. Es lohnt sich, diese Erfahrung jetzt aufzubauen.</p>
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
    for nazwa, a in ARTYKULY.items():
        plik = ZRODLA / f'{nazwa}.html'
        d, _ = wczytaj(plik)
        d['lead'] = a['lead']
        d['pytania'] = a['pytania']
        zapisz(plik, d, a['tresc'])
        slowa = len(re.sub(r'<[^>]+>', ' ', a['tresc']).split()) + sum(len((p + ' ' + o).split()) for p, o in a['pytania'])
        print(f'{plik.name}: {slowa} słów z FAQ')


# ——— Case studies: wnioski dla organizatora i pytania (dotąd bez FAQ, ok. 340 słów) ———
CASE = {
    'case-study-centrum-nauki-kopernik': {
        'pytania': [
            ['Kann der Roboter in einer Ausstellung zwischen Exponaten arbeiten?', 'Ja. Im Kopernikus-Wissenschaftszentrum stand er an der Luftfontäne, einem der stark besuchten Exponate. Er braucht rund 2×2 m ebene Fläche und eine 230-V-Steckdose, und der Operator achtet auf den Abstand zu Exponaten und Gästen.'],
            ['Beantwortet der Roboter Fragen zur eigenen Technik?', 'Ja. Für den Abend „Wovon Roboter träumen“ haben wir ihn darauf vorbereitet, einem erwachsenen Publikum zu erklären, wie er funktioniert. Auf Wunsch verbinden wir den Auftritt mit einem fachlichen Teil.'],
            ['Eignet sich der Roboter für eine Museumsnacht?', 'Ja. Museumsnächte, Wissenschaftstage, Ausstellungseröffnungen und Abendformate für Erwachsene sind typische Einsätze. Einen Abend von wenigen Stunden kalkulieren wir individuell.'],
        ],
        'mitnehmen': """<h2 id="mitnehmen">Was Sie daraus mitnehmen können</h2>

<h3>Ein fester Standort genügt</h3>

<p>Der Roboter musste an diesem Abend nicht durch das Haus laufen. Ein Platz an einem stark besuchten Exponat reichte, damit die Besucher zu ihm kamen. Für Häuser mit engen Ausstellungsflächen ist das die einfachste Lösung.</p>

<h3>Das Wissen passt zum Publikum</h3>

<p>Vor der Veranstaltung spielen wir dem Roboter ein, worüber er sprechen soll. Für ein erwachsenes, technisch interessiertes Publikum heißt das: Antworten dazu, wie er läuft, das Gleichgewicht hält und seine Umgebung erkennt.</p>

<h3>Drei Stunden statt eines ganzen Tags</h3>

<p>Ein Abendformat braucht keinen kompletten Veranstaltungstag. Kürzere Einsätze kalkulieren wir individuell, immer günstiger als einen ganzen Tag. Für Bildungseinrichtungen gibt es eine eigene Seite: <a href="roboter-hochschule.html">Roboter für Hochschulen</a>.</p>
""",
    },
    'case-study-grupa-rekord-mspo': {
        'pytania': [
            ['Funktioniert ein Roboter auf einer reinen Fachmesse?', 'Ja. Auf der MSPO in Kielce, einer Rüstungsmesse mit reinem B2B-Publikum, arbeitete der Roboter zwei Tage lang als Botschafter einer Unternehmensgruppe. Seine Aufgabe war nicht Unterhaltung, sondern Besucher lange genug am Stand zu halten, damit der Vertrieb das Gespräch beginnen kann.'],
            ['Kann der Roboter mehrere Unternehmen oder Produkte vorstellen?', 'Ja. Für die Rekord-Gruppe stellte er die Unternehmen der Gruppe nacheinander vor. Was er über jedes sagen soll, spielen wir ihm vor der Messe ein.'],
            ['Was kostet ein Roboter für zwei Messetage?', 'Ein Veranstaltungstag kostet ab 2.500 €, und ab zwei Tagen gibt es 15 % Rabatt auf jeden Tag. Operator, Anfahrt, Branding und Haftpflichtversicherung sind enthalten.'],
        ],
        'mitnehmen': """<h2 id="mitnehmen">Was Sie daraus mitnehmen können</h2>

<h3>Eine Rolle statt einer Attraktion</h3>

<p>Der Roboter hatte auf der MSPO zwei klar benannte Aufgaben: die Unternehmen der Gruppe vorstellen und zur Vorführung einladen. Beides lässt sich nach der Messe beurteilen, anders als ein allgemeiner WOW-Effekt.</p>

<h3>Der Platz an der Gangkante</h3>

<p>Besucher entscheiden im Vorbeigehen, ob sie stehen bleiben. Deshalb arbeitet der Roboter dort, wo der Stand auf den Gang trifft, und nicht hinten an der Rückwand.</p>

<h3>Mehrere Tage planen</h3>

<p>Der Operator hat Wechselakkus dabei, der Roboter arbeitet den ganzen Messetag in Blöcken. Ab zwei Veranstaltungstagen gibt es 15&nbsp;% Rabatt auf jeden Tag. Wie wir einen Messeauftritt vorbereiten, beschreibt die Seite <a href="angebot-messen.html">Roboter für Messen</a>.</p>
""",
    },
    'case-study-ogrod-przelewice': {
        'pytania': [
            ['Kann der Roboter abends im Freien auftreten?', 'Ja. Bei der Märchennacht im Dendrologischen Garten Przelewice arbeitete er nach Einbruch der Dunkelheit im Licht von Scheinwerfern. Voraussetzung sind eine trockene, ebene Fläche und ausreichend Licht.'],
            ['Was passiert bei Regen?', 'Der Roboter ist nicht wetterfest. Für Außeneinsätze planen wir deshalb vorher einen überdachten Bereich ein, in den er ausweichen kann.'],
            ['Eignet sich der Roboter für Familienveranstaltungen?', 'Ja. Die Märchennacht war ein Abend mit Theaterprogramm für Familien. Der Operator ist die ganze Zeit beim Roboter und lässt Begegnungen mit Kindern nur unter Aufsicht zu.'],
        ],
        'mitnehmen': """<h2 id="mitnehmen">Was Sie daraus mitnehmen können</h2>

<h3>Licht einplanen</h3>

<p>Nach Einbruch der Dunkelheit braucht der Roboter eine beleuchtete Fläche, für die Sicherheit der Gäste und für die Bilder. In Przelewice übernahmen das die Scheinwerfer auf den Arkaden.</p>

<h3>Ein fester Platz im Gelände</h3>

<p>In einem weitläufigen Park läuft der Roboter den Gästen nicht hinterher. Er arbeitete an einem Ort, am Mausoleum, und die Besucher kamen zu ihm.</p>

<h3>Der Boden entscheidet</h3>

<p>Rasen, Kies und Sand scheiden aus. Der Roboter braucht einen ebenen, festen Untergrund wie Pflaster, Stein oder ein Podest. Mehr dazu unter <a href="roboter-stadtfest.html#roboter-beim-outdoor-event">Roboter beim Outdoor-Event</a>.</p>
""",
    },
}


def case_studies():
    for nazwa, c in CASE.items():
        plik = ZRODLA / f'{nazwa}.html'
        d, tresc = wczytaj(plik)
        d['pytania'] = c['pytania']
        if '<h2 id="mitnehmen">' not in tresc:
            tresc = tresc.rstrip('\n') + '\n\n' + c['mitnehmen']
        zapisz(plik, d, tresc)
        slowa = len(re.sub(r'<[^>]+>', ' ', tresc).split()) + sum(len((p + ' ' + o).split()) for p, o in c['pytania'])
        print(f'{plik.name}: {slowa} słów z FAQ')


if __name__ == '__main__':
    main()
    case_studies()
