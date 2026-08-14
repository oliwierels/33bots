#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# All 40 cities for "inne miasta" links
ALL_CITIES = [
    ("robot-wynajem-warszawa.html", "Warszawa"),
    ("robot-wynajem-krakow.html", "Kraków"),
    ("robot-wynajem-wroclaw.html", "Wrocław"),
    ("robot-wynajem-poznan.html", "Poznań"),
    ("robot-wynajem-gdansk.html", "Gdańsk / Trójmiasto"),
    ("robot-wynajem-katowice.html", "Katowice"),
    ("robot-wynajem-lodz.html", "Łódź"),
    ("robot-wynajem-szczecin.html", "Szczecin"),
    ("robot-wynajem-bydgoszcz.html", "Bydgoszcz"),
    ("robot-wynajem-lublin.html", "Lublin"),
    ("robot-wynajem-bialystok.html", "Białystok"),
    ("robot-wynajem-rzeszow.html", "Rzeszów"),
    ("robot-wynajem-torun.html", "Toruń"),
    ("robot-wynajem-olsztyn.html", "Olsztyn"),
    ("robot-wynajem-kielce.html", "Kielce"),
    ("robot-wynajem-opole.html", "Opole"),
    ("robot-wynajem-gliwice.html", "Gliwice"),
    ("robot-wynajem-czestochowa.html", "Częstochowa"),
    ("robot-wynajem-radom.html", "Radom"),
    ("robot-wynajem-zielona-gora.html", "Zielona Góra"),
    # New 20:
    ("robot-wynajem-plock.html", "Płock"),
    ("robot-wynajem-elblag.html", "Elbląg"),
    ("robot-wynajem-walbrzych.html", "Wałbrzych"),
    ("robot-wynajem-wloclawek.html", "Włocławek"),
    ("robot-wynajem-tarnow.html", "Tarnów"),
    ("robot-wynajem-koszalin.html", "Koszalin"),
    ("robot-wynajem-legnica.html", "Legnica"),
    ("robot-wynajem-kalisz.html", "Kalisz"),
    ("robot-wynajem-grudziadz.html", "Grudziądz"),
    ("robot-wynajem-rybnik.html", "Rybnik"),
    ("robot-wynajem-slupsk.html", "Słupsk"),
    ("robot-wynajem-nowy-sacz.html", "Nowy Sącz"),
    ("robot-wynajem-pila.html", "Piła"),
]

# City data: slug, name_nom (mianownik), name_loc (miejscownik "w/we ..."), prep (w/we), loc_bare
CITIES = [

    {
        "slug": "plock",
        "filename": "robot-wynajem-plock.html",
        "name": "Płock",
        "loc": "w Płocku",
        "prep": "w",
        "loc_bare": "Płocku",
        "keywords": "wynajem robota Płock, robot humanoidalny Płock, Unitree G1 Płock, atrakcja eventowa Płock, wynajem robota na event Płock",
        "hero_sub": "Obsługujemy eventy w Płocku i regionie Mazowsza Płockiego. Robot Unitree G1 dotrze do Orlen Campus, Ratusza, Centrum Konferencyjnego Gostynin i każdego hotelu konferencyjnego w mieście.",
        "faq_q1": "Czy robot może wziąć udział w eventach przemysłowych i petrochemicznych w Płocku?",
        "faq_a1": "Tak — G1 świetnie sprawdza się jako atrakcja na konferencjach branżowych i eventach korporacyjnych w środowiskach przemysłowych. Robot może być elementem stoiska targowego, prezentacji innowacji lub gali pracowniczej w każdym obiekcie w Płocku.",
        "faq_q2": "Czy obsługujecie Płock i okolice?",
        "faq_a2": "Tak — dojeżdżamy do Płocka i całego regionu Mazowsza Płockiego, w tym Gostynina, Sierpca i Kutna. Cena wyceny to cena ostateczna, bez żadnych ukrytych kosztów.",
        "section_title": "Płock — miasto przemysłu i kultury nad Wisłą",
        "p1": "Płock to jedno z najważniejszych miast przemysłowych w Polsce, znane przede wszystkim z obecności Orlenu. Rozwijający się rynek eventów korporacyjnych, konferencji branżowych i gal dla pracowników sprawia, że zapotrzebowanie na unikatowe atrakcje stale rośnie.",
        "p2": "Wynajem robota humanoidalnego Unitree G1 w Płocku to doskonały sposób na wyróżnienie się podczas dni otwartych, eventów pracowniczych i konferencji innowacyjnych. G1 wzbudza zachwyt zarówno wśród pracowników przemysłowych, jak i gości targów i pokazów technologii.",
        "p2_header": "Gdzie w Płocku sprawdza się robot?",
        "p3": "33bots dostarczy robota do każdego miejsca w Płocku — czy to do sali konferencyjnej hotelu, centrum kultury, czy obiektu przemysłowego. Dojazd w całej Polsce, certyfikowany operator i własny sprzęt to nasza gwarancja bezproblemowej realizacji.",
        "p3_header": "Dlaczego 33bots?",
        "venues": "Orlen Campus, Płocki Dom Kultury, hotele konferencyjne, Ratusz Miejski i przestrzenie eventowe nad Wisłą",
        "region": "Płock i okolice",
    },
    {
        "slug": "elblag",
        "filename": "robot-wynajem-elblag.html",
        "name": "Elbląg",
        "loc": "w Elblągu",
        "prep": "w",
        "loc_bare": "Elblągu",
        "keywords": "wynajem robota Elbląg, robot humanoidalny Elbląg, Unitree G1 Elbląg, atrakcja eventowa Elbląg, wynajem robota na event Elbląg",
        "hero_sub": "Obsługujemy eventy w Elblągu i regionie Warmii i Mazur. Robot Unitree G1 dotrze do Centrum Spotkań Europejskich, lokalnych centrów konferencyjnych i każdego hotelu eventowego w mieście.",
        "faq_q1": "Czy robot może uczestniczyć w eventach związanych z przemysłem stoczniowym w Elblągu?",
        "faq_a1": "Oczywiście — G1 świetnie sprawdza się na konferencjach branżowych, pokazach innowacji i eventach korporacyjnych w środowisku przemysłowym. Robot może być elementem dnia otwartego zakładu lub gali pracowniczej.",
        "faq_q2": "Jak szybko robot może dotrzeć do Elbląga?",
        "faq_a2": "Elbląg leży w pobliżu Trójmiasta, skąd docieramy szybko. Dostarczamy robota standardowo dzień przed eventem, by operator mógł wszystko skonfigurować i przetestować na miejscu. Transport jest bezpłatny.",
        "section_title": "Elbląg — brama Żuław i centrum innowacji",
        "p1": "Elbląg to dynamicznie rozwijające się miasto Warmii i Mazur z silnym przemysłem i rosnącym sektorem usług. Miasto organizuje coraz więcej wydarzeń biznesowych, festiwali miejskich i konferencji, przyciągając uczestników z całego regionu.",
        "p2": "Wynajem robota humanoidalnego Unitree G1 w Elblągu to idealne rozwiązanie na eventy korporacyjne, dni otwarte uczelni i zakładów pracy, festiwale miejskie oraz imprezy targowe. G1 przyciąga tłumy i generuje content, który żyje w social mediach długo po zakończeniu wydarzenia.",
        "p2_header": "Gdzie w Elblągu sprawdza się robot?",
        "p3": "33bots oferuje kompleksową obsługę — własny sprzęt Unitree G1, certyfikowanego operatora i dojazd w całej Polsce do Elbląga. Skontaktuj się z nami, a wycenę otrzymasz w 24 godziny.",
        "p3_header": "Dlaczego 33bots?",
        "venues": "Centrum Spotkań Europejskich, hotele konferencyjne, przestrzenie eventowe w Starym Mieście i obiekty przemysłowe",
        "region": "Elbląg i okolice",
    },
    {
        "slug": "walbrzych",
        "filename": "robot-wynajem-walbrzych.html",
        "name": "Wałbrzych",
        "loc": "w Wałbrzychu",
        "prep": "w",
        "loc_bare": "Wałbrzychu",
        "keywords": "wynajem robota Wałbrzych, robot humanoidalny Wałbrzych, Unitree G1 Wałbrzych, atrakcja eventowa Wałbrzych, wynajem robota na event Wałbrzych",
        "hero_sub": "Obsługujemy eventy w Wałbrzychu i na Dolnym Śląsku. Robot Unitree G1 dotrze do Wałbrzyskiej Strefy Ekonomicznej, zamku Książ i każdego obiektu eventowego w regionie.",
        "faq_q1": "Czy robot sprawdzi się na eventach w zamku Książ w Wałbrzychu?",
        "faq_a1": "Tak — kontrast futurystycznego robota G1 i zabytkowej architektury zamku Książ tworzy niepowtarzalne wrażenie i gwarantuje wyjątkowe zdjęcia. Obsługujemy eventy zarówno w zamkowych salach, jak i na terenach zewnętrznych.",
        "faq_q2": "Czy obsługujecie Wałbrzyską Strefę Ekonomiczną i inne obiekty przemysłowe?",
        "faq_a2": "Tak — G1 świetnie sprawdza się na dniach otwartych zakładów produkcyjnych, konferencjach innowacyjnych i eventach korporacyjnych organizowanych przez firmy z Wałbrzyskiej Strefy Ekonomicznej i okolic.",
        "section_title": "Wałbrzych — miasto renesansu i innowacji",
        "p1": "Wałbrzych przeszedł imponującą transformację — z dawnego centrum górnictwa węglowego w nowoczesne centrum gospodarcze i kulturalne. Wałbrzyska Strefa Ekonomiczna przyciąga inwestorów z całego świata, a rozwijający się sektor turystyczny i eventowy tworzy nowe możliwości dla organizatorów imprez.",
        "p2": "Wynajem robota humanoidalnego Unitree G1 w Wałbrzychu to idealne rozwiązanie na gale korporacyjne, eventy dla pracowników stref ekonomicznych, festiwale miejskie i pokazy innowacji. G1 przyciąga uwagę gości i generuje zasięgi w social mediach.",
        "p2_header": "Gdzie w Wałbrzychu sprawdza się robot?",
        "p3": "33bots dostarczy robota do każdego miejsca w Wałbrzychu i okolicach — zamku Książ, hoteli konferencyjnych czy obiektów stref ekonomicznych. Dojazd w całej Polsce, certyfikowany operator i elastyczne terminy to nasza gwarancja.",
        "p3_header": "Dlaczego 33bots?",
        "venues": "Zamek Książ, Stara Kopalnia — Centrum Nauki i Sztuki, hotele konferencyjne, obiekty Wałbrzyskiej Strefy Ekonomicznej",
        "region": "Wałbrzych i okolice",
    },
    {
        "slug": "wloclawek",
        "filename": "robot-wynajem-wloclawek.html",
        "name": "Włocławek",
        "loc": "we Włocławku",
        "prep": "we",
        "loc_bare": "Włocławku",
        "keywords": "wynajem robota Włocławek, robot humanoidalny Włocławek, Unitree G1 Włocławek, atrakcja eventowa Włocławek, wynajem robota na event Włocławek",
        "hero_sub": "Obsługujemy eventy we Włocławku i regionie Kujaw. Robot Unitree G1 dotrze do centrum konferencyjnego, hoteli biznesowych i każdej sali eventowej w mieście.",
        "faq_q1": "Czy robot sprawdzi się na targach i wystawach we Włocławku?",
        "faq_a1": "Tak — G1 jest idealną atrakcją na lokalne targi branżowe, wystawy i eventy handlowe. Przyciąga odwiedzających do stoiska i sprawia, że prezentacja produktów lub usług jest niezapomniana.",
        "faq_q2": "Jak szybko robot może dotrzeć do Włocławka?",
        "faq_a2": "Włocławek leży przy autostradzie A1, co znacząco ułatwia dojazd. Standardowo dostarczamy robota dzień przed eventem. Transport jest bezpłatny dla klientów z całej Polski.",
        "section_title": "Włocławek — centrum Kujaw z rosnącym rynkiem eventowym",
        "p1": "Włocławek to największe miasto Kujaw i ważny ośrodek biznesowy regionu. Rozwijający się sektor przemysłowy, handlowy i edukacyjny tworzy stałe zapotrzebowanie na unikatowe atrakcje eventowe na gale, konferencje i dni otwarte.",
        "p2": "Wynajem robota humanoidalnego Unitree G1 we Włocławku to doskonały pomysł na wyróżnienie swojego eventu. G1 sprawdza się zarówno na dużych galach korporacyjnych, jak i mniejszych pokazach innowacji, targach lokalnych czy dniach otwartych szkół i uczelni.",
        "p2_header": "Gdzie we Włocławku sprawdza się robot?",
        "p3": "33bots zapewnia kompleksową obsługę — dowozimy robota do Włocławka, zapewniamy certyfikowanego operatora i dbamy o całą logistykę eventu. Wycenę wyślemy w ciągu 24 godzin.",
        "p3_header": "Dlaczego 33bots?",
        "venues": "Regionalne Centrum Kultury i Sztuki, hotele konferencyjne nad Wisłą, Centrum Handlowe Wzorcownia, lokalne obiekty sportowe",
        "region": "Włocławek i okolice",
    },
    {
        "slug": "tarnow",
        "filename": "robot-wynajem-tarnow.html",
        "name": "Tarnów",
        "loc": "w Tarnowie",
        "prep": "w",
        "loc_bare": "Tarnowie",
        "keywords": "wynajem robota Tarnów, robot humanoidalny Tarnów, Unitree G1 Tarnów, atrakcja eventowa Tarnów, wynajem robota na event Tarnów",
        "hero_sub": "Obsługujemy eventy w Tarnowie i Małopolsce. Robot Unitree G1 dotrze do Centrum Konferencyjnego Tarnowa, zamku, Muzeum Okręgowego i każdego hotelu eventowego w mieście.",
        "faq_q1": "Czy robot sprawdzi się podczas Tarnowskiego Festiwalu Kultury?",
        "faq_a1": "Tak — G1 jest atrakcją, która pasuje zarówno do wydarzeń kulturalnych, jak i biznesowych. Na festiwalach miejskich robot przyciąga setki zdjęć i relacji w mediach społecznościowych, budując zasięg organizatora.",
        "faq_q2": "Czy obsługujecie firmy z Tarnowa i okolicznych gmin?",
        "faq_a2": "Tak — dojeżdżamy do Tarnowa i całej Małopolski Wschodniej. Koszt dojazdu ustalamy przy wycenie. Obsługujemy eventy w samym Tarnowie, jak i w okolicznych miejscowościach przemysłowych i turystycznych.",
        "section_title": "Tarnów — małopolskie centrum biznesu i kultury",
        "p1": "Tarnów to ważny ośrodek biznesowy i kulturalny wschodniej Małopolski. Miasto łączy tradycję z nowoczesnością — obok historycznego centrum rozwijają się nowoczesne strefy przemysłowe i centra usługowe, a rynek eventowy dynamicznie rośnie.",
        "p2": "Wynajem robota humanoidalnego Unitree G1 w Tarnowie to hit na gale korporacyjne firm chemicznych i produkcyjnych, dni otwarte uczelni i szkół, festiwale miejskie oraz konferencje regionalne. G1 wzbudza zachwyt gości w każdym wieku i generuje content, który żyje w sieci długo po evencie.",
        "p2_header": "Gdzie w Tarnowie sprawdza się robot?",
        "p3": "33bots dostarczy robota do każdego miejsca w Tarnowie — od historycznych sal po nowoczesne centra konferencyjne. Dojazd w całej Polsce, certyfikowany operator i elastyczny harmonogram to nasza oferta.",
        "p3_header": "Dlaczego 33bots?",
        "venues": "Centrum Konferencyjne MCDN, hotele biznesowe, Centrum Handlowe Gemini Park, Park Miejski i historyczne obiekty tarnowskiego centrum",
        "region": "Tarnów i okolice",
    },
    {
        "slug": "koszalin",
        "filename": "robot-wynajem-koszalin.html",
        "name": "Koszalin",
        "loc": "w Koszalinie",
        "prep": "w",
        "loc_bare": "Koszalinie",
        "keywords": "wynajem robota Koszalin, robot humanoidalny Koszalin, Unitree G1 Koszalin, atrakcja eventowa Koszalin, wynajem robota na event Koszalin",
        "hero_sub": "Obsługujemy eventy w Koszalinie i Środkowym Pomorzu. Robot Unitree G1 dotrze do Forum Koszalin, hoteli konferencyjnych nad Bałtykiem i każdej sali eventowej w regionie.",
        "faq_q1": "Czy robot sprawdzi się na Festiwalu Filmów Fabularnych w Koszalinie?",
        "faq_a1": "Tak — G1 to doskonała atrakcja na festiwalach filmowych i kulturalnych. Robot przyciąga fanów kina i media, stając się ikoną eventu. Obsługujemy zarówno uroczyste otwarcia, jak i side-eventy.",
        "faq_q2": "Czy obsługujecie hotele nadmorskie w okolicach Koszalina?",
        "faq_a2": "Tak — dojeżdżamy do Koszalina i całego Środkowego Pomorza, w tym Mielna, Darłowa i Kołobrzegu. Dojazd obejmuje całą Polskę bez wyjątków.",
        "section_title": "Koszalin — centrum Środkowego Pomorza",
        "p1": "Koszalin to największe miasto Środkowego Pomorza i ważny ośrodek biznesowy, kulturalny i akademicki. Bliskość Bałtyku przyciąga korporacje organizujące eventy wyjazdowe i team-buildingowe, a rosnąca baza hotelowo-konferencyjna oferuje doskonałe warunki do organizacji eventów.",
        "p2": "Wynajem robota humanoidalnego Unitree G1 w Koszalinie to idealna atrakcja na eventy wyjazdowe, gale korporacyjne, festiwale miejskie i konferencje regionalne. G1 dostarcza niezapomnianych wrażeń i generuje viralowy content w mediach społecznościowych.",
        "p2_header": "Gdzie w Koszalinie sprawdza się robot?",
        "p3": "33bots to jedyna polska firma specjalizująca się wyłącznie w wynajmie robotów humanoidalnych. Dowozimy G1 do Koszalina bezpłatnie, zapewniamy certyfikowanego operatora i dbamy o każdy detal eventu.",
        "p3_header": "Dlaczego 33bots?",
        "venues": "Forum Koszalin, hotele konferencyjne, obiekty nadmorskie w Mielnie i Darłowie, Centrum Kultury 105 i miejsca targowe",
        "region": "Koszalin i okolice",
    },
    {
        "slug": "legnica",
        "filename": "robot-wynajem-legnica.html",
        "name": "Legnica",
        "loc": "w Legnicy",
        "prep": "w",
        "loc_bare": "Legnicy",
        "keywords": "wynajem robota Legnica, robot humanoidalny Legnica, Unitree G1 Legnica, atrakcja eventowa Legnica, wynajem robota na event Legnica",
        "hero_sub": "Obsługujemy eventy w Legnicy i na Dolnym Śląsku. Robot Unitree G1 dotrze do Centrum Wykładowo-Konferencyjnego PWSZ, zamku Piastów Śląskich i każdego obiektu eventowego w mieście.",
        "faq_q1": "Czy robot sprawdzi się na eventach Legnickiej Specjalnej Strefy Ekonomicznej?",
        "faq_a1": "Tak — G1 to idealna atrakcja na dni otwarte zakładów produkcyjnych, konferencje innowacyjne i gale korporacyjne firm z LSSE. Robot podkreśla nowoczesny charakter firm i przyciąga uwagę pracowników oraz gości.",
        "faq_q2": "Jak szybko dotrzecie do Legnicy?",
        "faq_a2": "Legnica leży przy autostradzie A4, co ułatwia szybki dojazd. Standardowo dostarczamy robota dzień przed eventem. Dojazd obejmuje całą Polskę.",
        "section_title": "Legnica — dolnośląskie centrum gospodarcze",
        "p1": "Legnica to jedno z największych miast Dolnego Śląska, z bogatą historią i dynamicznie rozwijającą się gospodarką. Legnicka Specjalna Strefa Ekonomiczna przyciąga inwestorów z całego świata, tworząc zapotrzebowanie na nowoczesne atrakcje eventowe na gale i konferencje korporacyjne.",
        "p2": "Wynajem robota humanoidalnego Unitree G1 w Legnicy to doskonały pomysł na eventy korporacyjne, dni otwarte firm ze stref ekonomicznych, targi branżowe i festiwale miejskie. G1 wzbudza zainteresowanie gości każdego eventu i zostawia trwałe wrażenie.",
        "p2_header": "Gdzie w Legnicy sprawdza się robot?",
        "p3": "33bots zapewnia bezproblemową obsługę w Legnicy — dojazd w całej Polsce, certyfikowany operator i własny sprzęt Unitree G1. Wycenę wyślemy w ciągu 24 godzin od pierwszego kontaktu.",
        "p3_header": "Dlaczego 33bots?",
        "venues": "Zamek Piastów Śląskich, PWSZ Legnica, hotele konferencyjne, Centrum Handlowe Galeria Piastów i obiekty LSSE",
        "region": "Legnica i okolice",
    },
    {
        "slug": "kalisz",
        "filename": "robot-wynajem-kalisz.html",
        "name": "Kalisz",
        "loc": "w Kaliszu",
        "prep": "w",
        "loc_bare": "Kaliszu",
        "keywords": "wynajem robota Kalisz, robot humanoidalny Kalisz, Unitree G1 Kalisz, atrakcja eventowa Kalisz, wynajem robota na event Kalisz",
        "hero_sub": "Obsługujemy eventy w Kaliszu i Wielkopolsce Południowej. Robot Unitree G1 dotrze do Centrum Kultury i Sztuki, hoteli konferencyjnych i każdego miejsca eventowego w mieście.",
        "faq_q1": "Czy robot sprawdzi się na Kaliskich Spotkaniach Teatralnych?",
        "faq_a1": "Tak — G1 jest atrakcją, która doskonale komponuje się z wydarzeniami kulturalnymi i teatralnymi. Na festiwalach i pokazach robot przyciąga uwagę mediów i publiczności, budując zasięg organizatora.",
        "faq_q2": "Czy obsługujecie firmy z Kalisza i Ostrowskiego Okręgu Przemysłowego?",
        "faq_a2": "Tak — dojeżdżamy do Kalisza i całego regionu Wielkopolski Południowej. Koszt dojazdu ustalamy przy wycenie. Obsługujemy eventy zarówno w centrum miasta, jak i w okolicznych strefach przemysłowych.",
        "section_title": "Kalisz — jedno z najstarszych miast Polski",
        "p1": "Kalisz to jedno z najstarszych miast Polski z bogatą tradycją i dynamicznym rynkiem biznesowym. Miasto jest ważnym centrum przemysłowym i handlowym Wielkopolski Południowej, a lokalni przedsiębiorcy coraz chętniej inwestują w nowoczesne eventy i konferencje.",
        "p2": "Wynajem robota humanoidalnego Unitree G1 w Kaliszu to unikalna atrakcja na gale firmowe, dni otwarte uczelni i zakładów pracy, targi regionalne oraz imprezy miejskie. G1 sprawdza się wszędzie tam, gdzie chcesz zrobić niezapomniane wrażenie.",
        "p2_header": "Gdzie w Kaliszu sprawdza się robot?",
        "p3": "33bots oferuje dojazd w całej Polsce do Kalisza, certyfikowanego operatora i własny sprzęt Unitree G1. Organizacja pokazu robota jest prosta — skontaktuj się z nami, a wycenę wyślemy w 24 godziny.",
        "p3_header": "Dlaczego 33bots?",
        "venues": "Centrum Kultury i Sztuki w Kaliszu, hotele biznesowe, Galeria Amber i Centrum Sportowo-Rekreacyjne Trójka",
        "region": "Kalisz i okolice",
    },
    {
        "slug": "grudziadz",
        "filename": "robot-wynajem-grudziadz.html",
        "name": "Grudziądz",
        "loc": "w Grudziądzu",
        "prep": "w",
        "loc_bare": "Grudziądzu",
        "keywords": "wynajem robota Grudziądz, robot humanoidalny Grudziądz, Unitree G1 Grudziądz, atrakcja eventowa Grudziądz, wynajem robota na event Grudziądz",
        "hero_sub": "Obsługujemy eventy w Grudziądzu i regionie Kujawsko-Pomorskim. Robot Unitree G1 dotrze do Centrum Kulturalno-Kongresowego, hoteli biznesowych i każdego miejsca eventowego w mieście.",
        "faq_q1": "Czy robot może uczestniczyć w eventach przemysłowych w Grudziądzu?",
        "faq_a1": "Tak — G1 świetnie sprawdza się na dniach otwartych zakładów produkcyjnych, konferencjach innowacyjnych i galach korporacyjnych. Robot podkreśla nowoczesny charakter firmy i przyciąga uwagę pracowników oraz mediów.",
        "faq_q2": "Jak szybko robot może dotrzeć do Grudziądza?",
        "faq_a2": "Grudziądz leży w pobliżu Torunia i Bydgoszczy, co ułatwia logistykę dojazdu. Standardowo dostarczamy robota dzień przed eventem. Dojazd obejmuje całą Polskę bez wyjątków.",
        "section_title": "Grudziądz — kujawsko-pomorski ośrodek przemysłowy",
        "p1": "Grudziądz to ważne miasto przemysłowe i handlowe Kujaw i Pomorza. Historyczne spichlerze nad Wisłą sąsiadują z nowoczesnymi zakładami produkcyjnymi, a rosnący sektor usługowy tworzy nowe możliwości dla organizatorów eventów i konferencji.",
        "p2": "Wynajem robota humanoidalnego Unitree G1 w Grudziądzu to doskonała atrakcja na eventy korporacyjne, dni otwarte uczelni i zakładów pracy, festiwale miejskie i regionalne targi branżowe. G1 wzbudza autentyczne zachwycenie i generuje organiczny zasięg w mediach społecznościowych.",
        "p2_header": "Gdzie w Grudziądzu sprawdza się robot?",
        "p3": "33bots dostarczy robota do Grudziądza bez żadnych ukrytych kosztów. Własny sprzęt Unitree G1, certyfikowany operator i dojazd w całej Polsce — skontaktuj się z nami i otrzymaj wycenę w 24 godziny.",
        "p3_header": "Dlaczego 33bots?",
        "venues": "Grudziądzkie Centrum Kultury, hotele konferencyjne, historyczne spichlerze nad Wisłą i obiekty GCOP",
        "region": "Grudziądz i okolice",
    },


    {
        "slug": "rybnik",
        "filename": "robot-wynajem-rybnik.html",
        "name": "Rybnik",
        "loc": "w Rybniku",
        "prep": "w",
        "loc_bare": "Rybniku",
        "keywords": "wynajem robota Rybnik, robot humanoidalny Rybnik, Unitree G1 Rybnik, atrakcja eventowa Rybnik, wynajem robota na event Rybnik",
        "hero_sub": "Obsługujemy eventy w Rybniku i Subregionie Zachodnim Śląska. Robot Unitree G1 dotrze do Centrum Kultury, hoteli konferencyjnych i każdego miejsca eventowego w mieście.",
        "faq_q1": "Czy robot sprawdzi się na Rybnickim Festiwalu Filmowym?",
        "faq_a1": "Tak — G1 to doskonała atrakcja na festiwalach filmowych i kulturalnych. Robot przyciąga uwagę mediów i fanów, stając się integralną częścią eventu i generując zasięg w social mediach.",
        "faq_q2": "Czy obsługujecie firmy z subregionu zachodniego Śląska?",
        "faq_a2": "Tak — dojeżdżamy do Rybnika i całego subregionu zachodniego, w tym Żor, Jastrzębia-Zdroju, Wodzisławia Śląskiego i Raciborza. Dojeżdżamy w całej aglomeracji.",
        "section_title": "Rybnik — centrum Subregionu Zachodniego Śląska",
        "p1": "Rybnik to dynamiczne miasto w zachodniej części Górnego Śląska, będące centrum administracyjnym i kulturalnym subregionu. Miasto systematycznie się modernizuje, rozwijając nowoczesną infrastrukturę eventową i konferencyjną.",
        "p2": "Wynajem robota humanoidalnego Unitree G1 w Rybniku to idealna atrakcja na gale korporacyjne, festiwale miejskie, dni otwarte firm i uczelni oraz targi regionalne. G1 wzbudza autentyczne zachwycenie i tworzy content, który żyje w mediach społecznościowych.",
        "p2_header": "Gdzie w Rybniku sprawdza się robot?",
        "p3": "33bots dostarczy robota do Rybnika bez ukrytych kosztów. Własny sprzęt, certyfikowany operator i dojazd w całej Polsce to nasza standardowa oferta. Skontaktuj się z nami — wycenę wyślemy w 24 godziny.",
        "p3_header": "Dlaczego 33bots?",
        "venues": "Rybnickie Centrum Kultury, Teatr Ziemi Rybnickiej, hotele konferencyjne i nowoczesne przestrzenie eventowe",
        "region": "Rybnik i okolice",
    },




    {
        "slug": "slupsk",
        "filename": "robot-wynajem-slupsk.html",
        "name": "Słupsk",
        "loc": "w Słupsku",
        "prep": "w",
        "loc_bare": "Słupsku",
        "keywords": "wynajem robota Słupsk, robot humanoidalny Słupsk, Unitree G1 Słupsk, atrakcja eventowa Słupsk, wynajem robota na event Słupsk",
        "hero_sub": "Obsługujemy eventy w Słupsku i Środkowym Pomorzu. Robot Unitree G1 dotrze do Słupskiego Centrum Kultury, hoteli nadmorskich i każdego miejsca eventowego w regionie.",
        "faq_q1": "Czy robot sprawdzi się na eventach nadmorskich w okolicach Słupska?",
        "faq_a1": "Tak — G1 to doskonała atrakcja na eventy wyjazdowe w nadmorskich hotelach w okolicach Ustki i Łeby. Dojeżdżamy na całym Środkowym Pomorzu, w tym do miejscowości nadmorskich.",
        "faq_q2": "Jak szybko robot może dotrzeć do Słupska?",
        "faq_a2": "Słupsk leży przy trasie S6, co ułatwia szybki dojazd. Standardowo dostarczamy robota dzień przed eventem. Transport jest bezpłatny dla klientów z całej Polski.",
        "section_title": "Słupsk — brama Środkowego Wybrzeża",
        "p1": "Słupsk to ważne centrum administracyjne i kulturalne Środkowego Pomorza. Miasto i okoliczne miejscowości nadmorskie — Ustka, Łeba — przyciągają korporacje organizujące eventy wyjazdowe i team-buildingowe, a rosnąca baza konferencyjna oferuje doskonałe warunki.",
        "p2": "Wynajem robota humanoidalnego Unitree G1 w Słupsku to atrakcja, która sprawdza się na galach korporacyjnych, festiwalach miejskich, eventach wyjazdowych i dniach otwartych. G1 wzbudza zachwyt zarówno lokalnych mieszkańców, jak i turystów odwiedzających region.",
        "p2_header": "Gdzie w Słupsku sprawdza się robot?",
        "p3": "33bots dostarczy robota do Słupska bez ukrytych kosztów. Własny sprzęt Unitree G1, certyfikowany operator i dojazd w całej Polsce — wycenę wyślemy w 24 godziny.",
        "p3_header": "Dlaczego 33bots?",
        "venues": "Słupskie Centrum Kultury, Zamek Książąt Pomorskich, hotele konferencyjne i obiekty nadmorskie w Ustce i Łebie",
        "region": "Słupsk i okolice",
    },
    {
        "slug": "nowy-sacz",
        "filename": "robot-wynajem-nowy-sacz.html",
        "name": "Nowy Sącz",
        "loc": "w Nowym Sączu",
        "prep": "w",
        "loc_bare": "Nowym Sączu",
        "keywords": "wynajem robota Nowy Sącz, robot humanoidalny Nowy Sącz, Unitree G1 Nowy Sącz, atrakcja eventowa Nowy Sącz, wynajem robota na event Nowy Sącz",
        "hero_sub": "Obsługujemy eventy w Nowym Sączu i Małopolsce. Robot Unitree G1 dotrze do Centrum Konferencyjnego NOVUM, Parku Strzeleckiego i każdego hotelu eventowego w mieście.",
        "faq_q1": "Czy robot sprawdzi się na Festiwalu Kultury Żydowskiej w Nowym Sączu?",
        "faq_a1": "Tak — G1 to atrakcja, która pasuje do różnych wydarzeń kulturalnych. Na festiwalach i eventach plenerowych robot przyciąga uwagę mediów i uczestników, budując zasięg organizatora.",
        "faq_q2": "Czy obsługujecie firmy z Nowego Sącza i Sądeckiego Parku Przemysłowego?",
        "faq_a2": "Tak — dojeżdżamy do Nowego Sącza i całego regionu Sądecczyzny. Koszt dojazdu ustalamy przy wycenie. Obsługujemy eventy zarówno w centrum miasta, jak i w strefach przemysłowych i turystycznych.",
        "section_title": "Nowy Sącz — centrum Sądecczyzny",
        "p1": "Nowy Sącz to największe miasto Sądecczyzny i ważny ośrodek biznesowy oraz kulturalny wschodniej Małopolski. Miasto łączy tradycję z nowoczesnością — obok zabytkowego centrum rozwijają się nowoczesne strefy przemysłowe i centra usługowe.",
        "p2": "Wynajem robota humanoidalnego Unitree G1 w Nowym Sączu to doskonała atrakcja na gale korporacyjne firm z SSE Nowy Sącz, dni otwarte uczelni, festiwale miejskie i regionalne eventy turystyczne. G1 wzbudza zachwyt i generuje content, który żyje w sieci.",
        "p2_header": "Gdzie w Nowym Sączu sprawdza się robot?",
        "p3": "33bots oferuje dojazd w całej Polsce do Nowego Sącza, certyfikowanego operatora i własny sprzęt Unitree G1. Organizacja pokazu jest prosta — skontaktuj się z nami, a wycenę wyślemy w 24 godziny.",
        "p3_header": "Dlaczego 33bots?",
        "venues": "Centrum Konferencyjne NOVUM, Ratusz Miejski, hotele konferencyjne, obiekty SSE Nowy Sącz i przestrzenie eventowe w centrum",
        "region": "Nowy Sącz i okolice",
    },
    {
        "slug": "pila",
        "filename": "robot-wynajem-pila.html",
        "name": "Piła",
        "loc": "w Pile",
        "prep": "w",
        "loc_bare": "Pile",
        "keywords": "wynajem robota Piła, robot humanoidalny Piła, Unitree G1 Piła, atrakcja eventowa Piła, wynajem robota na event Piła",
        "hero_sub": "Obsługujemy eventy w Pile i Wielkopolsce Północnej. Robot Unitree G1 dotrze do Pilskiego Centrum Kultury i Filmowego, hoteli konferencyjnych i każdego miejsca eventowego w mieście.",
        "faq_q1": "Czy robot sprawdzi się na eventach w Pilskiej Strefie Aktywności Gospodarczej?",
        "faq_a1": "Tak — G1 to idealna atrakcja na konferencje innowacyjne, dni otwarte firm i gale pracownicze organizowane przez firmy z PSAG. Robot podkreśla nowoczesny charakter firmy i wzbudza zachwyt gości.",
        "faq_q2": "Jak daleko jest z bazy do Piły?",
        "faq_a2": "Piła leży w Wielkopolsce Północnej — dojeżdżamy bez problemu i. Dojazd obejmuje całą Polskę, w tym Piłę i okoliczne gminy.",
        "section_title": "Piła — centrum Krajny i Noteci",
        "p1": "Piła to największe miasto Wielkopolski Północnej i ważny węzeł komunikacyjny regionu. Dynamicznie rozwijająca się baza przemysłowa i usługowa, rosnące uczelnie wyższe i aktywny sektor handlowy tworzą doskonałe warunki dla eventów biznesowych i kulturalnych.",
        "p2": "Wynajem robota humanoidalnego Unitree G1 w Pile to atrakcja, która sprawdza się na galach korporacyjnych, dniach otwartych uczelni, targach branżowych i festiwalach miejskich. G1 wzbudza autentyczny zachwyt i generuje zasięg w mediach społecznościowych.",
        "p2_header": "Gdzie w Pile sprawdza się robot?",
        "p3": "33bots dostarczy robota do Piły bez ukrytych kosztów — dojazd w całej Polsce, certyfikowany operator i własny sprzęt Unitree G1. Skontaktuj się z nami, a wycenę wyślemy w 24 godziny.",
        "p3_header": "Dlaczego 33bots?",
        "venues": "Pilskie Centrum Kultury i Filmowe, hotele konferencyjne, Galeria Vivo! Piła i obiekty Pilskiej Strefy Aktywności Gospodarczej",
        "region": "Piła i okolice",
    },
]

def build_cities_links_html(current_slug):
    """Build the inne miasta section HTML excluding current city."""
    links = []
    for filename, display_name in ALL_CITIES:
        # Exclude current city
        if filename == f"robot-wynajem-{current_slug}.html":
            continue
        link = f'        <a href="{filename}" style="color:var(--text); font-size:0.85rem; font-weight:600; padding:6px 14px; background:var(--surface-2); border:1px solid var(--border-mid); border-radius:8px; text-decoration:none;">{display_name}</a>'
        links.append(link)
    return "\n".join(links)


def generate_html(city):
    slug = city["slug"]
    filename = city["filename"]
    name = city["name"]
    loc = city["loc"]  # "w Sosnowcu"
    prep = city["prep"]  # "w" or "we"
    loc_bare = city["loc_bare"]  # "Sosnowcu"

    cities_links = build_cities_links_html(slug)

    html = f"""<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Wynajem robota humanoidalnego {name} — Unitree G1 | 33bots</title>
  <meta name="description" content="Wynajem robota humanoidalnego Unitree G1 {loc} — eventy, konferencje, targi. Dojazd w całej Polsce, certyfikowany operator. Sprawdź dostępność →" />
  <meta name="keywords" content="{city['keywords']}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://33bots.pl/{filename}" />

  <!-- Open Graph -->
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://33bots.pl/{filename}" />
  <meta property="og:title" content="Wynajem robota humanoidalnego {name} — Unitree G1 | 33bots" />
  <meta property="og:description" content="Wynajem robota humanoidalnego Unitree G1 {loc} — eventy, konferencje, targi. Dojazd w całej Polsce, certyfikowany operator. Sprawdź dostępność →" />
  <meta property="og:image" content="https://33bots.pl/robot-g1.jpg" />
  <meta property="og:image:alt" content="Robot humanoidalny Unitree G1 — wynajem {loc}" />
  <meta property="og:locale" content="pl_PL" />
  <meta property="og:site_name" content="33bots" />

  <!-- Twitter / X Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="Wynajem robota humanoidalnego {name} — Unitree G1 | 33bots" />
  <meta name="twitter:description" content="Wynajem robota humanoidalnego Unitree G1 {loc} — eventy, konferencje, targi. Dojazd w całej Polsce, certyfikowany operator. Sprawdź dostępność →" />

  <!-- Mobile -->
  <meta name="theme-color" content="#000000" />

  <!-- Hreflang -->
  <link rel="alternate" hreflang="pl" href="https://33bots.pl/{filename}" />
  <link rel="alternate" hreflang="x-default" href="https://33bots.pl/{filename}" />

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Service",
    "name": "Wynajem robota humanoidalnego {loc}",
    "description": "Wynajem robota Unitree G1 na eventy, konferencje i targi {loc}. Dojazd w całej Polsce, certyfikowany operator.",
    "url": "https://33bots.pl/{filename}",
    "image": "https://33bots.pl/robot-g1.jpg",
    "provider": {{
      "@type": "LocalBusiness",
      "name": "33bots",
      "url": "https://33bots.pl",
      "telephone": ["+48531408004", "+48601499947"],
      "email": "kontakt@33bots.pl"
    }},
    "areaServed": {{
      "@type": "City",
      "name": "{name}"
    }},
    "serviceType": "Wynajem robotów humanoidalnych",
    "offers": {{
      "@type": "Offer",
      "priceCurrency": "PLN",
      "description": "Cena na zapytanie — wycena indywidualna w 24h"
    }}
  }}
  </script>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type": "ListItem", "position": 1, "name": "Strona główna", "item": "https://33bots.pl/"}},
      {{"@type": "ListItem", "position": 2, "name": "Wynajem robota {name}", "item": "https://33bots.pl/{filename}"}}
    ]
  }}
  </script>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {{
        "@type": "Question",
        "name": "{city['faq_q1']}",
        "acceptedAnswer": {{"@type": "Answer", "text": "{city['faq_a1']}"}}
      }},
      {{
        "@type": "Question",
        "name": "Czy transport do {name} jest naprawdę bezpłatny?",
        "acceptedAnswer": {{"@type": "Answer", "text": "Tak — dojeżdżamy do każdego klienta w Polsce, w tym {loc}. Nie ma żadnych ukrytych kosztów dojazdu. Cena w wycenie jest ceną ostateczną."}}
      }}
    ]
  }}
  </script>

  <script>history.scrollRestoration = 'manual';</script>
  <link rel="icon" type="image/svg+xml" href="favicon.svg" />
  <link rel="stylesheet" href="style.css?v=18" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <style>
    .hero {{ grid-template-columns: 1fr; min-height: 70vh; }}
    .hero__content {{ max-width: none; padding: var(--s12) 0 var(--s8); }}
    .hero__title {{ text-wrap: unset; }}
  </style>
</head>
<body>

  <div class="cursor-glow" id="cursorGlow" aria-hidden="true"></div>
  <div class="scroll-progress" id="scrollProgress" aria-hidden="true"></div>

  <header class="nav" id="nav">
    <div class="nav__inner">
      <a href="index.html" class="logo">33BOTS</a>
      <nav class="nav__links">
        <div class="nav__dropdown">
          <span class="nav__dropdown-toggle">Oferta <svg viewBox="0 0 10 6" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
          <div class="nav__dropdown-menu">
            <a href="oferta-targi.html">Targi</a>
            <a href="oferta-konferencje.html">Konferencje i Gale</a>
            <a href="oferta-dni-otwarte.html">Dni otwarte i showroomy</a>
          </div>
        </div>
        <a href="index.html#o-nas">O nas</a>
        <a href="index.html#eventy">Eventy</a>
        <a href="index.html#blog">Blog</a>
        <a href="#kontakt">Kontakt</a>
      </nav>
      <button class="hamburger" id="hamburger" aria-label="Menu"><span></span><span></span></button>
    </div>
  </header>

  <div class="mobile-menu" id="mobileMenu">
    <span class="mobile-menu__label">Oferta</span>
    <a href="oferta-targi.html" class="mobile-menu__sub">Targi</a>
    <a href="oferta-konferencje.html" class="mobile-menu__sub">Konferencje i Gale</a>
    <a href="oferta-dni-otwarte.html" class="mobile-menu__sub">Dni otwarte i showroomy</a>
    <a href="index.html#o-nas">O nas</a>
    <a href="index.html#eventy">Eventy</a>
    <a href="index.html#blog">Blog</a>
    <a href="#kontakt">Kontakt</a>
  </div>

  <section class="hero">
    <div class="hero__content">
      <p class="hero__eyebrow">Wynajem robotów · {name} · Eventy</p>
      <h1 class="hero__title">Wynajem robota humanoidalnego<br />{loc} —<br />Unitree G1.</h1>
      <p class="hero__sub">{city['hero_sub']}</p>
      <div class="hero__ctas">
        <a href="#kontakt" class="btn-primary">Zarezerwuj termin</a>
        <a href="index.html#uslugi" class="btn-ghost">Zobacz ofertę ↓</a>
      </div>
      <div class="hero__trust">
        <span class="hero__trust-item">✓ Najniższe ceny na rynku</span>
        <span class="hero__trust-item">✓ Dojazd w całej Polsce</span>
        <span class="hero__trust-item">✓ Operator w cenie</span>
        <span class="hero__trust-item">✓ Branding bez dopłat</span>
      </div>
    </div>
  </section>

  <section class="section" id="korzysci">
    <div class="section-header">
      <span class="tag">Dlaczego robot?</span>
      <h2 class="section-title">Co zyskujesz<br />{loc}</h2>
    </div>
    <div class="tiles">
      <div class="tile">
        <div class="tile__top"><span class="tile__tag">Wyróżnienie</span></div>
        <h3 class="tile__title">Zatrzymaj tłumy</h3>
        <p class="tile__desc">G1 przyciąga uwagę z odległości kilkudziesięciu metrów. Twoje stoisko lub event będzie najbardziej rozpoznawalnym miejscem na sali.</p>
        <a href="#kontakt" class="tile__link">Zapytaj o wycenę →</a>
      </div>
      <div class="tile tile--light">
        <div class="tile__top"><span class="tile__tag">Zasięg</span></div>
        <h3 class="tile__title">Wiralowy marketing</h3>
        <p class="tile__desc">Zdjęcia i filmy z robotem trafiają na media społecznościowe jeszcze w trakcie eventu. Twoja marka pojawia się w setkach relacji — bezpłatnie.</p>
        <a href="#kontakt" class="tile__link">Zapytaj o wycenę →</a>
      </div>
      <div class="tile">
        <div class="tile__top"><span class="tile__tag">Dojazd</span></div>
        <h3 class="tile__title">Dojazd w całej Polsce</h3>
        <p class="tile__desc">Dowozimy robota {loc}, a koszt dojazdu ustalamy przy wycenie. Cena, którą podajemy, to cena ostateczna — bez niespodzianek.</p>
        <a href="#kontakt" class="tile__link">Zapytaj o wycenę →</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="onas-body" style="max-width:860px; margin:0 auto;">
      <div class="onas-text">
        <h2 class="section-title" style="font-size:clamp(1.8rem,3vw,2.8rem); margin-bottom:var(--s4);">{city['section_title']}</h2>
        <p class="lead-text">{city['p1']}</p>

        <h3 style="font-size:1.1rem; font-weight:700; letter-spacing:-0.01em; margin:var(--s6) 0 var(--s2); color:var(--text);">{city['p2_header']}</h3>
        <p class="body-text">{city['p2']} Realizujemy eventy m.in. w: {city['venues']}.</p>

        <h3 style="font-size:1.1rem; font-weight:700; letter-spacing:-0.01em; margin:var(--s6) 0 var(--s2); color:var(--text);">{city['p3_header']}</h3>
        <p class="body-text">{city['p3']}</p>
        <a href="#kontakt" class="btn-primary" style="margin-top:var(--s5); display:inline-flex;">Zapytaj o wycenę →</a>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:0;">
    <div style="max-width:860px; margin:0 auto;">
      <div style="padding:var(--s5) var(--s6); background:var(--surface-2); border:1px solid var(--border-mid); border-radius:12px; display:flex; align-items:center; justify-content:space-between; gap:var(--s4); flex-wrap:wrap;">
        <p style="color:var(--text-2); font-size:0.9rem; margin:0;">Sprawdź nasze oferty: <strong style="color:var(--text);">wynajem robota na targi</strong> i <strong style="color:var(--text);">wynajem robota na konferencje</strong></p>
        <div style="display:flex; gap:var(--s3); flex-wrap:wrap;">
          <a href="oferta-targi.html" style="color:var(--text); font-size:0.85rem; font-weight:600; text-decoration:underline; text-underline-offset:3px; white-space:nowrap;">Targi →</a>
          <a href="oferta-konferencje.html" style="color:var(--text); font-size:0.85rem; font-weight:600; text-decoration:underline; text-underline-offset:3px; white-space:nowrap;">Konferencje →</a>
        </div>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:0;">
    <div style="max-width:860px; margin:0 auto;">
      <p style="font-size:0.75rem; color:var(--text-3); text-transform:uppercase; letter-spacing:0.1em; font-weight:700; margin-bottom:var(--s3);">Wynajem robota w innych miastach</p>
      <div style="display:flex; flex-wrap:wrap; gap:var(--s2);">
{cities_links}
      </div>
    </div>
  </section>

  <section class="section faq-section">
    <div class="section-header">
      <span class="tag">FAQ</span>
      <h2 class="section-title">Często zadawane<br />pytania — {name}</h2>
    </div>
    <div class="faq">
      <div class="faq-item">
        <button class="faq-q" aria-expanded="false">
          <span>{city['faq_q1']}</span>
          <span class="faq-q__icon" aria-hidden="true">+</span>
        </button>
        <div class="faq-a" hidden><p>{city['faq_a1']}</p></div>
      </div>
      <div class="faq-item">
        <button class="faq-q" aria-expanded="false">
          <span>{city['faq_q2']}</span>
          <span class="faq-q__icon" aria-hidden="true">+</span>
        </button>
        <div class="faq-a" hidden><p>{city['faq_a2']}</p></div>
      </div>
      <div class="faq-item">
        <button class="faq-q" aria-expanded="false">
          <span>Czy transport do {name} jest naprawdę bezpłatny?</span>
          <span class="faq-q__icon" aria-hidden="true">+</span>
        </button>
        <div class="faq-a" hidden><p>Tak — dojeżdżamy do każdego klienta w Polsce, w tym {loc}. Nie ma żadnych ukrytych kosztów dojazdu. Cena w wycenie jest ceną ostateczną.</p></div>
      </div>
    </div>
  </section>

  <section class="section" id="kontakt">
    <div class="contact-layout">
      <div class="contact-left">
        <span class="tag">Kontakt</span>
        <h2 class="section-title">Zarezerwuj robota<br />{loc}.</h2>
        <p class="body-text">Napisz do nas — odpiszemy w ciągu jednego dnia roboczego z wyceną i dostępnością.</p>
        <div class="contact-details">
          <a href="mailto:kontakt@33bots.pl" class="contact-detail">
            <span class="contact-detail__label">E-mail</span>
            <span class="contact-detail__val">kontakt@33bots.pl</span>
          </a>
          <a href="tel:+48531408004" class="contact-detail">
            <span class="contact-detail__label">Telefon</span>
            <span class="contact-detail__val">+48 531 408 004</span>
          </a>
          <a href="tel:+48601499947" class="contact-detail">
            <span class="contact-detail__label">Telefon</span>
            <span class="contact-detail__val">+48 601 499 947</span>
          </a>
          <div class="contact-detail">
            <span class="contact-detail__label">Lokalizacja</span>
            <span class="contact-detail__val">{city['region']}</span>
          </div>
        </div>
      </div>
      <div class="contact-right">
        <form id="contactForm" class="form" novalidate>
          <div class="form-steps-header">
            <span class="form-step-ind active" id="stepInd1">01 — Dane kontaktowe</span>
            <span class="form-step-sep">/</span>
            <span class="form-step-ind" id="stepInd2">02 — Twój event</span>
          </div>
          <div class="form-step" id="formStep1">
            <div class="form-row">
              <div class="form-field">
                <label for="f-name">Imię i nazwisko *</label>
                <input id="f-name" type="text" name="name" placeholder="Jan Kowalski" autocomplete="name" required />
                <span class="form-field__err" aria-live="polite"></span>
              </div>
              <div class="form-field">
                <label for="f-company">Firma</label>
                <input id="f-company" type="text" name="company" placeholder="Nazwa firmy" autocomplete="organization" />
              </div>
            </div>
            <div class="form-row">
              <div class="form-field">
                <label for="f-email">E-mail *</label>
                <input id="f-email" type="email" name="email" placeholder="kontakt@firma.pl" autocomplete="email" required />
                <span class="form-field__err" aria-live="polite"></span>
              </div>
              <div class="form-field">
                <label for="f-phone">Telefon</label>
                <input id="f-phone" type="tel" name="phone" placeholder="+48 531 408 004" autocomplete="tel" />
              </div>
            </div>
            <button type="button" id="btnNext" class="btn-submit">Dalej — Opowiedz o evencie →</button>
          </div>
          <div class="form-step form-step--hidden" id="formStep2" aria-hidden="true">
            <div class="form-row">
              <div class="form-field">
                <label for="f-date">Planowana data eventu</label>
                <input id="f-date" type="date" name="date" />
              </div>
              <div class="form-field">
                <label for="f-location">Miasto / Miejsce</label>
                <input id="f-location" type="text" name="location" placeholder="np. {name}, obiekt X" autocomplete="address-level2" />
              </div>
            </div>
            <div class="form-field">
              <label for="f-message">Opisz swój event *</label>
              <textarea id="f-message" name="message" rows="6" placeholder="Rodzaj eventu, orientacyjna liczba gości, jak długo chcesz mieć robota..." required></textarea>
              <div class="form-field__footer">
                <span class="form-field__err" aria-live="polite"></span>
                <span class="char-counter"><span id="charCount">0</span> / 600</span>
              </div>
            </div>
            <div class="form-step__nav">
              <button type="button" id="btnBack" class="btn-back">← Wróć</button>
              <button type="submit" class="btn-submit">Wyślij zapytanie →</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </section>

  <footer class="footer">
    <div class="footer__inner">
      <div class="footer__brand">
        <span class="logo">33BOTS</span>
        <p class="footer__tagline">Wynajem robotów humanoidalnych · Polska</p>
      </div>
      <div class="footer__links">
        <a href="index.html#uslugi">Usługi</a>
        <a href="index.html#o-nas">O nas</a>
        <a href="index.html#eventy">Eventy</a>
        <a href="index.html#blog">Blog</a>
        <a href="#kontakt">Kontakt</a>
      </div>
      <div class="footer__right">
        <div class="footer__socials">
          <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" class="footer__social">↗ Instagram</a>
          <a href="https://tiktok.com" target="_blank" rel="noopener noreferrer" class="footer__social">↗ TikTok</a>
          <a href="https://www.facebook.com/33bots" target="_blank" rel="noopener noreferrer" class="footer__social">↗ Facebook</a>
          <a href="https://www.linkedin.com/company/33bots" target="_blank" rel="noopener noreferrer" class="footer__social">↗ LinkedIn</a>
        </div>
        <span class="footer__copy">© 2025 33bots. Wszelkie prawa zastrzeżone.</span>
      </div>
    </div>
  </footer>

  <div class="cookie-banner" id="cookieBanner" aria-live="polite">
    <p class="cookie-banner__text">Ta strona używa plików cookie do celów analitycznych. <a href="#" class="cookie-banner__link">Polityka prywatności</a></p>
    <button class="cookie-banner__btn" id="cookieAccept">Rozumiem</button>
  </div>

  <div class="sticky-cta">
    <a href="#kontakt" class="btn-primary">Zarezerwuj →</a>
  </div>

  <script src="main.js"></script>
</body>
</html>"""
    return html


output_dir = "/home/user/33bots"

for city in CITIES:
    filepath = os.path.join(output_dir, city["filename"])
    content = generate_html(city)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {city['filename']}")

print(f"\nDone! Created {len(CITIES)} files.")
