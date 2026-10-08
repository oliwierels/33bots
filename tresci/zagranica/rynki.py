# -*- coding: utf-8 -*-
"""Treść stron głównych rynków zagranicznych w układzie polskiej strony głównej.

WSPOLNE_DE — niemiecka treść wspólna dla 33bots.de i 33bots.at: fakty firmy
(robot, realizacje, klienci, proces), przetłumaczone z polskiej strony głównej.
DE i AT dokładają fakty swojego rynku: ceny, formaty, kontakt, formularz,
analitykę, stopkę. Fakty rynkowe pochodzą wyłącznie z dotychczasowych stron
danego rynku — niczego tu nie dopisujemy.

Kolejność kadrów w pasach i nazw klientów bierze się z polskiego index.html;
tutaj są tylko ich niemieckie opisy. Nowy kadr na stronie PL bez opisu tutaj
zatrzyma generator — tak ma być.
"""

KRAJE_DE = 'in Polen, Litauen, Deutschland, Tschechien und Rumänien'

# Zdjęcia do rotacji w hero: plik, alt, klient, miejsce.
SLAJDY_DE = [
    ('realizacja-gala-wsrod-gosci', 'Humanoider Roboter unter den Gästen einer Gala', 'Dresdner Schlössernacht', 'Dresden'),
    ('realizacja-eco-studio-wywiad', 'Eine Journalistin interviewt den humanoiden Roboter an der Sponsorenwand von Eco Studio', 'Finale Eco Studio ELECTRO-SYSTEM', 'Warschau'),
    ('realizacja-przelewice-arkady', 'Humanoider Roboter in beleuchteten Arkaden während der Märchennacht', 'Dendrologischer Garten Przelewice', 'Märchennacht'),
    ('realizacja-yeah-gym-koszulka', 'Humanoider Roboter im T-Shirt des Clubs YEAH GYM winkt zur Begrüßung', 'YEAH GYM', 'Breslau'),
    ('realizacja-matys-silver-garden', 'Humanoider Roboter an der Wand des Projekts Silver Garden am Stand von Matys Development', 'Matys Development', 'Stettin'),
    ('realizacja-szkola-kosmos-majaland', 'Humanoider Roboter in der Schürze der Szkoła Kosmos beim Schuljahresbeginn', 'Szkoła Kosmos', 'Majaland'),
]

# Trzy duże kadry na początku sekcji: klucz realizacji, plik, alt, klient, miejsce.
WYROZNIONE_DE = [
    ('drezno', 'realizacja-gala-palac', 'Humanoider Roboter im Smoking im Ballsaal eines Palais', 'Dresdner Schlössernacht', 'Dresden'),
    ('women-in-tech', 'realizacja-women-in-tech-wybieg', 'Humanoider Roboter auf dem rosa Laufsteg des Women in Tech Summit', 'Women in Tech Summit', 'EXPO XXI, Warschau · 2026'),
    ('lexai', 'realizacja-lexai-starowka', 'Humanoider Roboter im LEX-AI-T-Shirt in der Altstadt, Passanten machen Fotos', 'LEX AI', 'Langer Markt, Danzig'),
]

# Kadry w pasach: plik → (alt, klient, opis). Klucz realizacji (data-cs) jak na .pl.
KADRY_DE = {
    'realizacja-eco-studio-scena': ('Humanoider Roboter auf der Bühne des Eco-Studio-Finales in rotem Licht', 'ELECTRO-SYSTEM · Eco Studio', 'Finale der 7. Staffel · Warschau · 2026'),
    'realizacja-grupa-rekord-mspo': ('Humanoider Roboter in den Farben der Grupa Rekord am Stand der Messe MSPO in Kielce', 'Grupa Rekord', 'MSPO · Messe Kielce · 2026'),
    'realizacja-przelewice-noc-bajek': ('Humanoider Roboter in beleuchteten Arkaden während der Märchennacht in Przelewice', 'Dendrologischer Garten Przelewice', 'Märchennacht der Generationen'),
    'realizacja-event-nad-woda': ('Humanoider Roboter winkt auf einer Terrasse über einem Jachthafen', 'Loża Przedsiębiorców', 'Mikołajki'),
    'realizacja-yeah-gym-silownia': ('Humanoider Roboter im Trainingsbereich des Clubs YEAH GYM', 'YEAH GYM', 'Fitnessclub · Breslau'),
    'realizacja-jednorozec-parada': ('Humanoider Roboter im T-Shirt der Gemeinde Jednorożec unter den Teilnehmern der Parade', 'Gemeinde Jednorożec', 'Einhorn-Parade'),
    'realizacja-wesele-konfetti': ('Humanoider Roboter im Nebel auf der Tanzfläche einer Hochzeit', 'Hochzeit', 'Hochzeitsfeier'),
    'realizacja-women-in-tech-tlum': ('Teilnehmerinnen des Women in Tech Summit filmen den humanoiden Roboter mit dem Handy', 'Women in Tech Summit', 'EXPO XXI · Warschau · 2026'),
    'realizacja-kopernik-noc': ('Humanoider Roboter in der Ausstellung des Centrum Nauki Kopernik bei einem Abend für Erwachsene', 'Centrum Nauki Kopernik', '„Wovon Roboter träumen“ · Warschau'),
    'realizacja-tet-trung-thu-tlum': ('Gäste des Mittherbstfests rund um den humanoiden Roboter', 'Tết Trung Thu', 'Mittherbstfest'),
    'realizacja-robot-w-deszczu': ('Humanoider Roboter im roten T-Shirt mit Regenschirm vor einem Autohaus', 'Gonia Auto', 'Autohaus'),
    'realizacja-dream-med-expo': ('Humanoider Roboter am Stand von Dream-Med auf der Warsaw Medical Expo', 'Dream-Med', 'Warsaw Medical Expo · 2026'),
    'realizacja-lexai-ulica': ('Humanoider Roboter LEX AI geht mit einer Aktentasche durch die Altstadt', 'LEX AI', 'Langer Markt · Danzig'),
    'realizacja-matys-stoisko': ('Humanoider Roboter im Matys-T-Shirt am Stand des Bauträgers', 'Matys Development', 'Immobilienmesse · Stettin'),
    'realizacja-jednorozec-zachod': ('Humanoider Roboter bei einer Parade im Freien bei Sonnenuntergang', 'Gemeinde Jednorożec', 'Einhorn-Parade'),
    'realizacja-spotkanie-biznesowe': ('Humanoider Roboter im T-Shirt der Loża Przedsiębiorców auf einer Terrasse', 'Loża Przedsiębiorców', 'Mikołajki'),
    'realizacja-szkola-kosmos-scena': ('Humanoider Roboter auf der Bühne der Szkoła Kosmos vor Schülern', 'Szkoła Kosmos', 'Schuljahresbeginn · Majaland'),
    'realizacja-yeah-gym-trening': ('Humanoider Roboter neben einer Trainerin im Fitnessclub', 'YEAH GYM', 'Fitnessclub · Breslau'),
    'realizacja-tet-trung-thu': ('Humanoider Roboter im festlichen Branding beim Mittherbstfest', 'Tết Trung Thu', 'Mittherbstfest'),
}

# Nazwy klientów z pasów strony PL, które mają utarty niemiecki odpowiednik.
# Pozostałe nazwy własne zostają w oryginale.
KLIENCI_DE = {
    'Gmina Jednorożec': 'Gemeinde Jednorożec',
    'Fundacja Perspektywy · Women in Tech Summit': 'Perspektywy Foundation · Women in Tech Summit',
    'Drezdeńska Noc Zamków': 'Dresdner Schlössernacht',
    'Ogród Dendrologiczny w Przelewicach': 'Dendrologischer Garten Przelewice',
    'Uzdrowisko Ciechocinek': 'Kurort Ciechocinek',
    'ZTM · m.st. Warszawa': 'ZTM · Stadt Warschau',
}

# Szuflada realizacji. „link” dokłada rynek, który ma stronę case study.
REALIZACJE_DE = {
    'eco-studio': {'klient': 'ELECTRO-SYSTEM · Eco Studio', 'podpis': 'Finale der 7. Staffel · Warschau · 2026',
                   'liczby': [['15.09.2026', 'Finale der 7. Staffel'], ['Eko Partner 2026', 'Titel vom Veranstalter'], ['TVP2', '„Pytanie na śniadanie“']],
                   'opis': 'Der Roboter war eine der Attraktionen des Finales, neben Konzerten und dem offiziellen Teil. Er stand mit den Moderatoren und Finalisten auf der Bühne und an der Sponsorenwand, wo ein Interview mit ihm aufgenommen wurde.'},
    'women-in-tech': {'klient': 'Women in Tech Summit', 'podpis': 'EXPO XXI · Warschau · 2026',
                      'liczby': [['~14 000', 'Teilnehmerinnen und Teilnehmer'], ['10.–11.06.2026', 'EXPO XXI, Warschau']],
                      'opis': 'Die größte Women-in-Tech-Konferenz Europas. Der Roboter war auf dem Laufsteg und mitten unter den Teilnehmerinnen im Einsatz.'},
    'lexai': {'klient': 'LEX AI', 'podpis': 'Langer Markt · Danzig',
              'liczby': [['Teleexpress', 'Beitrag im TVP'], ['TVP Gdańsk', 'Reportage über die App LEX AI']],
              'opis': 'Der Roboter stand am Neptunbrunnen als Symbol der App — er begrüßte Passanten, gab ihnen die Hand, posierte für Fotos und beantwortete Fragen.'},
    'grupa-rekord': {'klient': 'Grupa Rekord', 'podpis': 'MSPO · Messe Kielce · 2026',
                     'liczby': [['8.–9. September', 'zwei Messetage'], ['3Z-05', 'Stand in Halle RFS']],
                     'opis': 'Der Roboter stellte nacheinander alle Gesellschaften der Gruppe vor und lud die Besucher im Gang zur Vorführung der Gefechtsfeldmedizin am Stand ein.'},
    'kopernik': {'klient': 'Centrum Nauki Kopernik', 'podpis': '„Wovon Roboter träumen“ · Warschau',
                 'liczby': [['17. September', 'Abend nur für Erwachsene'], ['19:00–22:00', 'drei Stunden Einsatz']],
                 'opis': 'Der Roboter stand am Luftbrunnen, sprach mit den Besuchern und posierte für Fotos.'},
    'przelewice': {'klient': 'Dendrologischer Garten Przelewice', 'podpis': 'Märchennacht der Generationen',
                   'liczby': [['12. September', 'Märchennacht der Generationen'], ['Mausoleum', 'Standort nach Einbruch der Dunkelheit']],
                   'opis': 'Der Roboter war nach Einbruch der Dunkelheit am Mausoleum der Familie von Prillwitz im Einsatz, im Licht der Scheinwerfer auf den Arkaden.'},
    'drezno': {'klient': 'Dresdner Schlössernacht', 'podpis': 'Dresden · Deutschland', 'liczby': [],
               'opis': 'Der Roboter im Paillettensmoking mit Krone auf dem Ball in einem Dresdner Palais — auf dem roten Teppich, im Ballsaal und mitten unter den Gästen.'},
    'gonia-auto': {'klient': 'Gonia Auto', 'podpis': 'Autohaus', 'liczby': [],
                   'opis': 'Der Roboter im Firmenrot vor dem Autohaus Gonia Auto.'},
    'loza': {'klient': 'Loża Przedsiębiorców', 'podpis': 'Mikołajki', 'liczby': [],
             'opis': 'Der Roboter im T-Shirt der Loża Przedsiębiorców bei einem Treffen in Mikołajki.'},
    'dream-med': {'klient': 'Dream-Med', 'podpis': 'Warsaw Medical Expo · 2026', 'liczby': [],
                  'opis': 'Der Roboter am Stand von Dream-Med auf der Warsaw Medical Expo 2026.'},
    'matys': {'klient': 'Matys Development', 'podpis': 'Immobilienmesse · Stettin', 'liczby': [],
              'opis': 'Der Roboter am Stand von Matys Development auf der Immobilienmesse in Stettin, mit Materialien zum Projekt Silver Garden.'},
    'szkola-kosmos': {'klient': 'Szkoła Kosmos', 'podpis': 'Schuljahresbeginn · Majaland', 'liczby': [],
                      'opis': 'Der Roboter in der Schürze der Szkoła Kosmos beim Schuljahresbeginn im Majaland.'},
    'yeah-gym': {'klient': 'YEAH GYM', 'podpis': 'Fitnessclub · Breslau', 'liczby': [],
                 'opis': 'Der Roboter im T-Shirt des Clubs YEAH GYM im Trainingsbereich in Breslau.'},
    'jednorozec': {'klient': 'Gemeinde Jednorożec', 'podpis': 'Einhorn-Parade', 'liczby': [],
                   'opis': 'Der Roboter im T-Shirt der Gemeinde bei der Einhorn-Parade, im Freien bis in die Abenddämmerung.'},
    'tet-trung-thu': {'klient': 'Tết Trung Thu', 'podpis': 'Mittherbstfest', 'liczby': [],
                      'opis': 'Der Roboter im festlichen Branding unter den Gästen des Mittherbstfests.'},
    'wesele': {'klient': 'Hochzeit', 'podpis': 'Hochzeitsfeier', 'liczby': [],
               'opis': 'Der Roboter auf der Tanzfläche im Abendteil einer Hochzeitsfeier.'},
}

# FAQ wspólne obu rynkom (fakty firmy). Pytania o cenę, płatność i dojazd są rynkowe.
FAQ_BATERIE = ('Wie arbeitet der Roboter den ganzen Tag, wenn ein Akku kürzer hält?',
               'Der Roboter arbeitet mit Wechselakkus. Der Operator hat einen Satz Ersatzakkus dabei und tauscht sie während der Veranstaltung — die Show unterbricht nicht zum Laden.')
FAQ_MOWA = ('Spricht der Roboter mit den Gästen?',
            'Ja. Der Roboter spricht Deutsch und jede andere Sprache, mit natürlicher Sprachsynthese — er begrüßt Gäste, beantwortet Fragen und kündigt Programmpunkte an. Vor der Veranstaltung legen wir seinen Charakter fest und spielen ihm Wissen über Ihr Unternehmen auf: Angebot, Produktnamen, häufige Kundenfragen und die Agenda. Die Konfiguration ist im Mietpreis enthalten.')
FAQ_ZALICZKA = ('Muss ich eine Anzahlung leisten?',
                'Nein. Die Reservierung erfolgt ohne Anzahlung. Die Rechnung stellen wir erst nach der Veranstaltung, bei Bedarf mit längerem Zahlungsziel.')
FAQ_OPERATOR = ('Muss ich den Roboter selbst bedienen können?',
                'Nein. Während der gesamten Veranstaltung ist unser zertifizierter Operator vor Ort — er ist für Konfiguration, Bedienung und Sicherheit der Show verantwortlich.')
FAQ_BEZPIECZENSTWO = ('Ist der Roboter für die Gäste sicher?',
                      'Ja. Dank LiDAR und Computer Vision weicht der Roboter Menschen und Hindernissen in Echtzeit aus, der Operator überwacht die Show, und jeder Einsatz ist haftpflichtversichert.')
FAQ_BRANDING = ('Kann ich mein Logo auf dem Roboter platzieren?',
                'Ja. Ihr Logo und ein QR-Code kommen auf die Brust des Roboters, der ganze Auftritt passt zum Charakter der Veranstaltung. Das Branding ist im Preis enthalten.')
FAQ_ZAGRANICA = ('Sind Sie auch international im Einsatz?',
                 f'Ja. Wir waren auf Veranstaltungen {KRAJE_DE} im Einsatz. Der Roboter spricht jede Sprache — auf einer internationalen Veranstaltung begrüßt er die Gäste in ihrer Sprache und beantwortet ihre Fragen.')

WSPOLNE_DE = {
    'skip': 'Zum Hauptinhalt springen',
    'logo_aria': '33bots — Startseite',
    'nav_aria': 'Hauptnavigation',
    'menu': 'Menü', 'menu_zamknij': 'Schließen',
    'cta': 'Verfügbarkeit prüfen', 'cta_krotki': 'Termin prüfen',
    # Miękkie dzielenie: długie niemieckie słowo nie wyjdzie poza kolumnę.
    'display': 'Der meist&shy;fotografierte Gast Ihrer Veranstaltung.',
    'pauza': 'Pause', 'wznow': 'Weiter', 'nastepne': 'Nächstes Foto',
    'slajdy': SLAJDY_DE,
    'proof_label': 'Bekannt aus',
    'realizacje_meta': '04 / 11 · Im Einsatz', 'realizacje_h2': 'Im Einsatz',
    'realizacje_body': 'Vom Ball in einem Dresdner Palais und der Messe MSPO bis zur Gemeindeparade und zur Hochzeit — Dutzende Veranstaltungen in fünf Ländern. Klicken Sie auf ein Bild, um zu sehen, was der Roboter gemacht hat.',
    'zobacz_realizacje': 'Einsatz ansehen',
    'wyroznione': WYROZNIONE_DE,
    'wiecej': 'Weitere Einsätze', 'zatrzymaj_ruch': 'Bewegung anhalten', 'wznow_ruch': 'Bewegung fortsetzen',
    'kadry': KADRY_DE,
    'klienci': KLIENCI_DE,
    'klienci_label': 'Für wen wir gearbeitet haben',
    'klienci_kraje': f'Konzerne und öffentliche Einrichtungen, Wissenschaftszentren, Gemeinden, Clubs und private Feiern — {KRAJE_DE}.',
    'wystep_meta': '05 / 11 · Auftritt', 'wystep_h2': 'Wie wir den Auftritt planen',
    'wystep_body': 'Dasselbe Robotermodell kann als Dekoration in der Ecke stehen oder eine Gala moderieren. Den Unterschied macht die Vorbereitung: Charakter, Gespräch und Reaktionen auf das Publikum, die wir auf Dutzenden Veranstaltungen verfeinert haben — von Firmenkonferenzen bis zu Picknicks.',
    'wiersze': [
        ('Charakter', 'Wir legen fest, wie sich der Roboter verhält: eleganter Moderator, locker und humorvoll oder sachlicher Experte. Am meisten beeindruckt meist der Moment, in dem er auf etwas eingeht, das gerade im Saal passiert.'),
        ('Stimme und Wissen', f'Er spricht Deutsch und jede andere Sprache — natürlich, ohne künstlichen Roboterklang. Wir waren auf Veranstaltungen {KRAJE_DE} im Einsatz. Er begrüßt Gäste, beantwortet Fragen und kündigt Programmpunkte an. Wir spielen ihm Wissen über die Veranstaltung auf: wer auftritt, was auf dem Programm steht und aus welchem Anlass Sie zusammenkommen.'),
        ('Drehbuch', 'Begrüßung der Gäste, Ankündigung der Redner, Countdown bis Mitternacht, Preisverleihung. Er beherrscht mehrere Choreografien — von ruhig bis dynamisch. Ein Roboter, der Teil des Programms ist, statt nur im Saal zu stehen.'),
        ('Branding', 'Logo und QR-Code auf der Brust und ein Auftritt, der zum Charakter der Veranstaltung passt — vom Firmen-T-Shirt bis zum Paillettensmoking mit Krone. Das Branding ist im Preis enthalten.'),
        ('Fotos und Videos', 'Der Roboter ist der Gast, den alle mit dem Handy filmen. Wir planen Momente für gute Bilder — Begrüßung an der Fotowand, Auftritt auf der Bühne, Tanz — und das Branding sorgt dafür, dass Ihre Marke in jedem Video zu sehen ist.'),
    ],
    'wystep_foto_alt': 'Nahaufnahme des humanoiden Roboters mit Krone und Paillettensmoking',
    'wystep_foto_podpis': 'Dresdner Schlössernacht',
    'cs_meta': '06 / 11 · Case Study', 'cs_h2': 'Großes Finale Eco Studio ELECTRO-SYSTEM',
    'cs_opis': [
        ('Veranstaltung', 'Finale der 7. Staffel eines landesweiten Bildungs- und Umweltprojekts für Schulen in Polen. Im Publikum Schülerinnen und Schüler aus dem ganzen Land, auf der Bühne Saszan, Antek Smykiewicz und Vicky.'),
        ('Rolle des Roboters', 'Eine der Attraktionen des Finales, neben Konzerten und dem offiziellen Teil — auf der Bühne mit den Moderatoren und Finalisten sowie an der Sponsorenwand.'),
        ('Ergebnis', 'Der Veranstalter verlieh 33&nbsp;Bots den Titel Eko Partner 2026, und das Team von „Pytanie na śniadanie“ (TVP2) berichtete über das Finale.'),
    ],
    'cs_foto_alt': 'Überreichung der Eko-Partner-Urkunde auf der Bühne des Eco-Studio-Finales, auf dem Bildschirm das Logo von 33bots',
    'cs_foto_podpis': 'Eko-Partner-Urkunde für 33bots, überreicht auf der Bühne des Finales.',
    'cs_fakty': [
        ('https://vod.tvp.pl/programy,88/pytanie-na-sniadanie-odcinki,2542729/odcinek-1287,S03E1287,3348151',
         '„Pytanie na śniadanie“ TVP2', 'Bericht vom Finale · 15.09.2026 · Roboter bei 0:35–1:00 und 2:00–2:10'),
        ('https://naszemiasto.pl/wielki-final-eco-studio-electro-system-z-okazji-sprzatania-swiata/ar/c1p2-29359081',
         'Eko Partner 2026', 'Titel von ELECTRO-SYSTEM'),
        (None, 'Finale der 7. Staffel Eco Studio', 'Terminal Kultury Gocław, Warschau'),
    ],
    'cs_cytat': '„Musik, Ökologie und ein humanoider Roboter haben junge Menschen verbunden.“',
    'cs_cytat_zrodlo': 'aus dem Titel des Berichts, übersetzt',
    'cs_cytat_link': ('https://4influ.pl/wielki-final-eco-studio-electro-system-muzyka-ekologia-i-robot-humanoidalny-polaczyly-mlodych-ludzi/', '4influ.pl'),
    'formaty_meta': '07 / 11 · Formate', 'formaty_h2': 'Formate und Preise',
    'formaty_body': 'Wir kalkulieren einen Auftritt, keine Gerätemiete. In jedem Format kommt der Roboter mit Operator, Drehbuch und Wissen über Ihre Veranstaltung.',
    'proces_meta': '08 / 11 · Ablauf', 'proces_h2': 'Vom Gespräch zur Rechnung',
    'proces_akcent': 'Sie zahlen nach der Veranstaltung.',
    'faq_meta': '09 / 11 · FAQ', 'faq_h2': 'Bevor Sie fragen',
    'kontakt_meta': '10 / 11 · Reservierung', 'kontakt_h2': 'Prüfen Sie, ob Ihr Termin frei ist.',
    'form': {
        'krok1': '01 Veranstaltung', 'krok2': '02 Kontakt',
        'typ': 'Art der Veranstaltung *', 'typy': ['Gala', 'Konferenz', 'Messe', 'Outdoor', 'Sonstiges'],
        'typ_blad': 'Wählen Sie die Art der Veranstaltung.',
        'data': 'Datum', 'data_nieustalona': 'Termin noch offen', 'data_wartosc': 'offen',
        'miejsce': 'Stadt oder Ort', 'goscie': 'Anzahl der Gäste', 'goscie_opcje': ['bis 100', '100–500', '500–2000', 'über 2000'],
        'dalej': 'Weiter', 'imie': 'Vor- und Nachname *', 'imie_blad': 'Bitte geben Sie Ihren Namen an.',
        'mail': 'E-Mail *', 'mail_blad': 'Bitte geben Sie eine gültige E-Mail-Adresse an.',
        'firma': 'Firma', 'telefon': 'Telefon', 'opis': 'Beschreibung der Veranstaltung',
        'opis_ph': 'Programm, Uhrzeiten, was Sie vom Roboter erwarten — falls Sie es schon wissen.',
        'wstecz': 'Zurück', 'wysylanie': 'Wird gesendet…', 'sukces': 'Ihre Anfrage ist bei uns angekommen.',
        'sukces_1': 'Wir melden uns unter ',
    },
    'pasek': 'Termin prüfen',
    'szuflada_zamknij': 'Schließen', 'szuflada_link': 'Zur Case Study',
    'realizacje': REALIZACJE_DE,
    'a11y': {
        'otworz': 'Einstellungen zur Barrierefreiheit öffnen', 'tytul': 'Barrierefreiheit',
        'grupy': [
            ('Textgröße', 'font', [('normal', 'Standard'), ('large', 'Groß'), ('xlarge', 'Sehr groß')]),
            ('Darstellung', 'theme', [('dark', 'Dunkel'), ('light', 'Hell')]),
            ('Kontrast', 'contrast', [('normal', 'Standard'), ('high', 'Hoch')]),
            ('Animationen', 'motion', [('on', 'An'), ('off', 'Aus')]),
        ],
        'reset': 'Zurücksetzen',
    },
}

# ——— 33bots.de ———
DE = {**WSPOLNE_DE,
    'kod': 'de', 'lang': 'de',
    'analityka': False,          # strona celowo bez narzędzi analitycznych (§ 25 TDDDG)
    'panel_dostepnosci': True,   # BFSG
    'h1': 'Humanoide Roboter für Events mieten',
    'lead': 'Ein humanoider Roboter mit Charakter und Drehbuch für Ihre Gala, Konferenz oder Ihren Messestand. Er spricht Deutsch und jede andere Sprache. Operator, Anfahrt und Branding im Preis. <strong>Sie zahlen nach der Veranstaltung.</strong>',
    'hero_link': ('referenzen-videos.html', 'Referenzen ansehen'),
    'proof': [
        ('https://vod.tvp.pl/programy,88/pytanie-na-sniadanie-odcinki,2542729/odcinek-1287,S03E1287,3348151', 'Pytanie na śniadanie, TVP2', '0:35–1:00'),
        ('https://www.tiktok.com/@teleexpress.tvp/video/7654958168786619680', 'Teleexpress, TVP', None),
        ('case-study-women-in-tech.html', 'Women in Tech Summit', None),
        ('https://naszemiasto.pl/wielki-final-eco-studio-electro-system-z-okazji-sprzatania-swiata/ar/c1p2-29359081', 'Eko Partner 2026, ELECTRO-SYSTEM', None),
    ],
    'nav': [('#referenzen', 'Referenzen'), ('#auftritt', 'Auftritt'), ('#preise', 'Preise'), ('#ablauf', 'Ablauf')],
    'nav_drugi': ('blog.html', 'Blog'),
    'kontakt_nav': ('mailto:kontakt@33bots.de', 'kontakt@33bots.de', 'data-mail'),
    # Dawne kotwice strony głównej — prowadzą do nich linki z podstron.
    'kotwice': {'referenzen': ['realisierungen', 'events', 'video', 'ueber-uns'], 'auftritt': ['leistungen', 'einsatzbereiche']},
    'linki_realizacji': {'women-in-tech': 'case-study-women-in-tech.html', 'lexai': 'case-study-lexai.html'},
    'wszystkie_realizacje': ('referenzen-videos.html', 'Alle Referenzen und Videos'),
    'formaty': [
        ('Ganzer Tag', 'Der Roboter steht Ihnen den ganzen Veranstaltungstag zur Verfügung, mit Operator und Ersatzakkus.', 'ab 2.500&nbsp;€', 'pro Veranstaltungstag'),
        ('Mehrere Tage', 'Zwei Tage und mehr — Messen, Festivals, Roadshows.', '−15&nbsp;%', 'auf jeden Tag'),
        ('Roboterhund', 'Zusatzoption: Der Humanoid macht die Show, der Roboterhund erobert die Herzen der Gäste. Operator inklusive.', '850&nbsp;€', 'pro Veranstaltungstag'),
    ],
    'formaty_wcenie': 'Im Preis: Operator, Anfahrt in ganz Deutschland, Branding (Logo, QR-Code), Haftpflichtversicherung. <strong>Sie zahlen nach der Veranstaltung.</strong> Der endgültige Preis hängt von Veranstaltungsort und Umfang der Show ab.',
    'kroki': [
        ('Gespräch', 'innerhalb von 24 Werkstunden', 'Sie füllen das Formular aus oder schreiben uns eine E-Mail. Wir melden uns und nennen einen konkreten Betrag, meist noch am selben Tag.'),
        ('Drehbuch und Vertrag', 'meist 1–2 Wochen', 'Wir legen Drehbuch und Branding fest und bestätigen Ort und Termin. Reservierung ohne Anzahlung.'),
        ('Veranstaltung', 'am Veranstaltungstag', 'Wir kommen mit Roboter und Operator. Um Technisches müssen Sie sich nicht kümmern.'),
        ('Rechnung nach der Veranstaltung', 'nach der Veranstaltung', 'Die Rechnung stellen wir nach der Veranstaltung. Bei Bedarf vereinbaren wir ein längeres Zahlungsziel.'),
    ],
    'faq': [
        ('Was kostet die Miete genau?', 'Ein ganzer Veranstaltungstag kostet ab 2.500 €. Der endgültige Preis hängt von Veranstaltungsort und Umfang der Show ab. Ab zwei Veranstaltungstagen erhalten Sie 15 % Rabatt auf jeden Tag, den Roboterhund buchen Sie optional für 850 € pro Tag. Im Preis sind Anfahrt, Operator, Branding und Haftpflichtversicherung enthalten.'),
        FAQ_ZALICZKA,
        FAQ_BATERIE,
        ('Wie viel Platz und Technik braucht der Roboter?', 'Rund 2×2 m freie Fläche und eine gewöhnliche 230-V-Steckdose. Der Roboter arbeitet am Messestand, auf der Bühne und im Gang zwischen den Gästen. Internet oder besondere Beleuchtung sind nicht nötig — unser Operator bringt die komplette Ausrüstung mit und ist in 30–45 Minuten einsatzbereit.'),
        FAQ_MOWA,
        FAQ_BRANDING,
        FAQ_OPERATOR,
        FAQ_BEZPIECZENSTWO,
        ('Kommen Sie in meine Stadt?', 'Ja — nach Berlin, München, Hamburg, Köln, Frankfurt, Stuttgart, Düsseldorf und in jede andere Stadt in Deutschland. Die Anfahrt ist im Preis enthalten, ohne Kilometerpauschale.'),
        FAQ_ZAGRANICA,
    ],
    # „24 Werkstunden” jak w formularzach podstron .de (main.js), na .pl i .at.
    'kontakt_lista': [('E-Mail', 'mailto:kontakt@33bots.de', 'kontakt@33bots.de')],
    'kontakt_tekst': 'Wir antworten innerhalb von 24 Werkstunden, meist noch am selben Tag. Reservierung ohne Anzahlung, deutschlandweit.',
    'miejsce_ph': 'z. B. Berlin, Messe Berlin',
    'formularz': {'adres': 'https://formspree.io/f/mnjwvray', 'dodatkowe': {}, 'gtag': False},
    'sukces_2': '. Wir antworten innerhalb von 24 Werkstunden, meist noch am selben Tag.',
    'blad_wysylki': 'Senden fehlgeschlagen. Schreiben Sie uns an kontakt@33bots.de.',
    'stopka_opis': 'Humanoide Roboter mieten · deutschlandweit',
    'stopka_kontakt': [('mailto:kontakt@33bots.de', 'kontakt@33bots.de', 'data-mail')],
    'stopka_jezyki': [('https://33bots.pl/', 'pl', 'Polski — 33bots.pl'), ('https://33bots.lt/', 'lt', 'Lietuvių — 33bots.lt'), ('https://33bots.at/', 'de-AT', 'Österreich — 33bots.at')],
    'stopka_social': [('https://www.instagram.com/33bots_/', 'Instagram'), ('https://www.tiktok.com/@aimforum', 'TikTok'), ('https://www.facebook.com/33bots', 'Facebook'), ('https://www.linkedin.com/company/33bots', 'LinkedIn')],
    # Cztery kolumny mieszczą się w siatce stopki — linki społecznościowe idą wtedy pod kontakt.
    'stopka_kolumny': [
        ('Angebot', [('humanoiden-roboter-mieten.html', 'Humanoiden Roboter mieten'), ('leistungen.html', 'Leistungen'), ('angebot-messen.html', 'Messen'), ('angebot-konferenzen-galas.html', 'Konferenzen &amp; Galas'), ('angebot-tag-der-offenen-tuer.html', 'Tage der offenen Tür'), ('event-attraktionen.html', 'Event-Attraktionen'), ('blog.html', 'Blog')]),
        ('Einsatzbereiche', [('roboter-gala.html', 'Galas'), ('roboter-corporate-event.html', 'Corporate Events'), ('roboter-firmenfeier.html', 'Firmenfeiern'), ('roboter-konferenz.html', 'Konferenzen'), ('roboter-eroeffnung.html', 'Eröffnungen'), ('roboter-festival.html', 'Festivals'), ('roboter-party.html', 'Partys'), ('roboter-hochzeit.html', 'Hochzeiten')]),
        ('Referenzen', [('referenzen-videos.html', 'Referenzen und Videos'), ('case-study-lexai.html', 'Case Study LEX AI'), ('case-study-women-in-tech.html', 'Case Study Women in Tech'), ('case-study-wallstreet.html', 'Case Study WallStreet 30')]),
        ('Rechtliches', [('impressum.html', 'Impressum'), ('datenschutz.html', 'Datenschutz'), ('barrierefreiheit.html', 'Barrierefreiheit')]),
    ],
    'stopka_poradnik': ('Ratgeber für Veranstalter', [
        ('blog-was-kostet-roboter-mieten.html', 'Was kostet die Miete eines Roboters?'),
        ('blog-event-attraktionen-ranking.html', 'Event-Attraktionen im Vergleich'),
        ('blog-attraktion-firmenevent.html', 'Roboter oder Alternativen fürs Firmenevent'),
        ('blog-roboter-am-messestand.html', 'Roboter am Messestand'),
        ('blog-roboter-auf-dem-event.html', '5 Gründe für einen Humanoiden'),
        ('blog-robotik-im-marketing.html', 'Robotik im B2B-Marketing'),
        ('blog-ki-roboter-spricht-deutsch.html', 'KI-Roboter, der Deutsch spricht'),
        ('blog-sicherheit-roboter-event.html', 'Sicherheit auf dem Event'),
        ('blog.html', 'Alle Artikel'),
    ]),
    'stopka_miasta_tytul': 'Roboter mieten in Ihrer Stadt',
    'miasta': [('berlin', 'Berlin'), ('muenchen', 'München'), ('hamburg', 'Hamburg'), ('koeln', 'Köln'), ('frankfurt', 'Frankfurt am Main'),
               ('stuttgart', 'Stuttgart'), ('duesseldorf', 'Düsseldorf'), ('leipzig', 'Leipzig'), ('dortmund', 'Dortmund'), ('essen', 'Essen'),
               ('bremen', 'Bremen'), ('dresden', 'Dresden'), ('hannover', 'Hannover'), ('nuernberg', 'Nürnberg'), ('duisburg', 'Duisburg'),
               ('bochum', 'Bochum'), ('wuppertal', 'Wuppertal'), ('bielefeld', 'Bielefeld'), ('bonn', 'Bonn'), ('muenster', 'Münster'),
               ('karlsruhe', 'Karlsruhe'), ('mannheim', 'Mannheim'), ('augsburg', 'Augsburg'), ('wiesbaden', 'Wiesbaden'), ('moenchengladbach', 'Mönchengladbach'),
               ('braunschweig', 'Braunschweig'), ('kiel', 'Kiel'), ('chemnitz', 'Chemnitz'), ('aachen', 'Aachen'), ('halle', 'Halle (Saale)'),
               ('magdeburg', 'Magdeburg'), ('freiburg', 'Freiburg'), ('krefeld', 'Krefeld'), ('mainz', 'Mainz'), ('luebeck', 'Lübeck')],
    'stopka_prawa': '© 2026 33bots. Alle Rechte vorbehalten.',
    'cookies': None,
}

# ——— 33bots.at ———
AT = {**WSPOLNE_DE,
    'kod': 'at', 'lang': 'de-AT',
    'analityka': True,           # GTM i Albacross jak dotąd, z banerem cookie
    'panel_dostepnosci': False,
    'h1': 'Humanoide Roboter mieten für Events in Österreich',
    'lead': 'Ein humanoider Roboter mit Charakter und Drehbuch für Ihre Gala, Konferenz oder Ihren Messestand. Er spricht Deutsch und jede andere Sprache. Operator, Transport und Branding im Preis. <strong>Sie zahlen nach der Veranstaltung.</strong>',
    'hero_link': ('#referenzen', 'Referenzen ansehen'),
    'proof': [
        ('https://vod.tvp.pl/programy,88/pytanie-na-sniadanie-odcinki,2542729/odcinek-1287,S03E1287,3348151', 'Pytanie na śniadanie, TVP2', '0:35–1:00'),
        ('https://www.tiktok.com/@teleexpress.tvp/video/7654958168786619680', 'Teleexpress, TVP', None),
        ('#referenzen', 'Women in Tech Summit', None),
        ('https://naszemiasto.pl/wielki-final-eco-studio-electro-system-z-okazji-sprzatania-swiata/ar/c1p2-29359081', 'Eko Partner 2026, ELECTRO-SYSTEM', None),
    ],
    'nav': [('#referenzen', 'Referenzen'), ('#auftritt', 'Auftritt'), ('#preise', 'Preise'), ('#ablauf', 'Ablauf')],
    'nav_drugi': ('humanoider-roboter-mieten.html', 'Angebot'),
    'kontakt_nav': ('tel:+48531408004', '+48 531 408 004', 'data-tel'),
    'kotwice': {'referenzen': ['vertrauen'], 'auftritt': ['moeglichkeiten']},
    'linki_realizacji': {},
    'wszystkie_realizacje': None,
    'formaty': [
        ('Einige Stunden', 'Ein paar Stunden im Programm — Eröffnung, Bühnenblock, Stoßzeiten am Messestand.', 'Individuelles Angebot', 'immer günstiger als ein ganzer Tag'),
        ('Ganzer Tag', 'Der Roboter steht Ihnen den ganzen Veranstaltungstag zur Verfügung, mit Operator und Ersatzakkus.', 'ab 2.300&nbsp;€', 'netto'),
        ('Mehrere Tage', 'Zwei Tage und mehr — Messen, Festivals, Roadshows.', '−15&nbsp;%', 'auf jeden Tag'),
    ],
    'formaty_wcenie': 'Im Preis: Operator, Transport in ganz Österreich, Branding (Logo, QR-Code), Haftpflichtversicherung. <strong>Sie zahlen nach der Veranstaltung.</strong> Den endgültigen Preis kalkulieren wir nach Dauer, Ort und Programm. Zusatzoption: Roboterhund, auf Anfrage.',
    'kroki': [
        ('Gespräch', 'innerhalb von 24 Werkstunden', 'Sie hinterlassen Ihre Kontaktdaten oder rufen an. Wir rufen zurück und nennen einen konkreten Betrag, meist noch am selben Tag.'),
        ('Drehbuch und Vertrag', 'meist 1–2 Wochen', 'Wir legen Drehbuch und Branding fest und bestätigen Ort und Termin. Reservierung ohne Anzahlung.'),
        ('Veranstaltung', 'am Veranstaltungstag', 'Wir kommen mit Roboter und Operator. Um Technisches müssen Sie sich nicht kümmern.'),
        ('Rechnung nach der Veranstaltung', 'nach der Veranstaltung', 'Die Rechnung stellen wir nach der Veranstaltung. Bei Bedarf vereinbaren wir ein längeres Zahlungsziel.'),
    ],
    'faq': [
        ('Was kostet die Miete genau?', 'Ab 2.300 € netto für einen ganzen Veranstaltungstag — den endgültigen Betrag kalkulieren wir nach Dauer, Ort und Programm. Sie können den Roboter auch für einen kürzeren Auftritt mieten, etwa für einige Stunden während einer Konferenzpause — dann kalkulieren wir individuell und immer günstiger als einen ganzen Tag. Bei Einsätzen ab zwei Tagen gewähren wir 15 % Rabatt auf jeden Tag. Transport, Operator, Branding und Haftpflichtversicherung sind inklusive; der Roboterhund ist auf Anfrage zubuchbar.'),
        ('Sind die Preise netto oder brutto?', 'Netto. Alle Beträge auf dieser Seite sind Nettopreise.'),
        FAQ_BATERIE,
        ('Wie viel Platz braucht der Roboter?', 'Einige Quadratmeter genügen. Der Roboter arbeitet am Messestand, auf der Bühne und im Gang zwischen den Gästen — ohne eigene Zone oder technisches Backoffice.'),
        FAQ_MOWA,
        FAQ_ZALICZKA,
        FAQ_OPERATOR,
        FAQ_BEZPIECZENSTWO,
        ('Kommen Sie auch in meine Stadt?', 'Ja — in jede Stadt Österreichs, ohne Aufschlag und ohne Kilometerlimit. Von Wien bis Dornbirn, von Innsbruck bis Eisenstadt.'),
        FAQ_ZAGRANICA,
    ],
    'kontakt_lista': [('Telefon', 'tel:+48531408004', '+48 531 408 004'), ('E-Mail', 'mailto:kontakt@33bots.at', 'kontakt@33bots.at')],
    'kontakt_tekst': 'Wir antworten innerhalb von 24 Werkstunden, meist noch am selben Tag. Reservierung ohne Anzahlung, in ganz Österreich.',
    'miejsce_ph': 'z. B. Wien, Messe Wien',
    'formularz': {'adres': 'https://formsubmit.co/ajax/kontakt@33bots.at', 'dodatkowe': {'_subject': 'Neue Anfrage über 33bots.at'}, 'gtag': True},
    'sukces_2': '. Wir antworten innerhalb von 24 Werkstunden, meist noch am selben Tag.',
    'blad_wysylki': 'Senden fehlgeschlagen. Rufen Sie an: +48 531 408 004 oder schreiben Sie an kontakt@33bots.at.',
    'stopka_opis': 'Humanoide Roboter mieten · ganz Österreich',
    'stopka_kontakt': [('tel:+48531408004', '+48 531 408 004', 'data-tel'), ('mailto:kontakt@33bots.at', 'kontakt@33bots.at', 'data-mail')],
    'stopka_jezyki': [('https://33bots.pl/', 'pl', 'Polski — 33bots.pl'), ('https://33bots.de/', 'de', 'Deutschland — 33bots.de'), ('https://33bots.lt/', 'lt', 'Lietuvių — 33bots.lt')],
    'stopka_social': [('https://www.instagram.com/robotollern', 'Instagram'), ('https://www.tiktok.com/@robotollern', 'TikTok'), ('https://www.youtube.com/@robotollern', 'YouTube')],
    # None w miejscu listy linków = kolumna z linkami społecznościowymi.
    'stopka_kolumny': [
        ('Angebot', [('humanoider-roboter-mieten.html', 'Humanoider Roboter mieten'), ('messe-roboter-mieten.html', 'Roboter für Messen'), ('unitree-g1-mieten.html', 'Unitree G1 mieten'), ('kontakt.html', 'Kontakt')]),
        ('Social Media', None),
        ('Rechtliches', [('impressum.html', 'Impressum'), ('datenschutz.html', 'Datenschutz')]),
    ],
    'stopka_poradnik': None,
    'stopka_miasta_tytul': 'Roboter mieten in Ihrer Stadt',
    'miasta': [('wien', 'Wien'), ('graz', 'Graz'), ('linz', 'Linz'), ('salzburg', 'Salzburg'), ('innsbruck', 'Innsbruck'), ('klagenfurt', 'Klagenfurt'),
               ('villach', 'Villach'), ('wels', 'Wels'), ('st-poelten', 'St. Pölten'), ('dornbirn', 'Dornbirn'), ('eisenstadt', 'Eisenstadt')],
    'stopka_prawa': '© 2026 33bots Österreich. Alle Rechte vorbehalten.',
    # Treść banera bez zmian względem dotychczasowej strony (zmienia się tylko wygląd).
    'cookies': ('Wir verwenden Cookies zu Analysezwecken.', 'Verstanden'),
}

RYNKI = {'de': DE, 'at': AT}
