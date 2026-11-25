# -*- coding: utf-8 -*-
"""Jednorazowo: teksty lokalne stron miast w źródłach tresci/landing/strony/.

Zastępuje akapity powielane na wszystkich miastach (ten sam szablon z podmienioną nazwą)
tekstem pisanym dla miasta. Nagłówki zostają; fakty tylko sprawdzalne (realizacje z CRM
i case studies, obiekty, które istnieją). Każda zmiana to dokładne „stare → nowe”;
skrypt zatrzymuje się, jeśli stary tekst nie występuje dokładnie raz.
"""
import re
from pathlib import Path

TU = Path(__file__).resolve().parent / 'strony'

DLACZEGO = {
    # cztery wersje rotacyjnie zamiast jednego akapitu kopiowanego na każde miasto
    1: 'Nie jesteśmy pośrednikiem: robot to nasz własny sprzęt, a operator to nasz człowiek, który zna go od podszewki. Transport i branding są w cenie.',
    2: 'Robot jest nasz, nie z wypożyczalni pośrednika. Przyjeżdża z certyfikowanym operatorem, a w cenie masz też transport i branding z Twoim logo.',
    3: 'Pracujemy na własnym sprzęcie i z własnymi operatorami. Dzięki temu cena jest jedna, bez dopłat za dojazd, a odpowiedź z kwotą dostajesz zwykle w ciągu 30 minut.',
    4: 'Bez pośredników: własny robot, certyfikowany operator i transport w cenie. Rezerwujesz bez zaliczki, fakturę dostajesz po wydarzeniu.',
}
STARE_DLACZEGO = re.compile(r'<p>Nie jesteśmy pośrednikiem: robot to nasz własny sprzęt\. Certyfikowany operator i transport są w cenie w całej Polsce, także (?:do|w) [^.]+\.(?: Skontaktuj się z nami, a wycenę podamy zwykle w ciągu 30 minut\.| Wycenę podajemy zwykle w ciągu 30 minut\.)</p>')
STARE_DOJAZD_KONIEC = re.compile(r' Robot potrzebuje na miejscu ok\. 2×2 m równej przestrzeni i dostępu do gniazdka 230 V; wnosimy go i uruchamiamy sami przed startem wydarzenia\. Napisz, gdzie odbywa się Twój event (?:w|we) [^,]+, a konkretną wycenę podamy zwykle w ciągu 30 minut\.')

MIASTA = {
 'gdansk': dict(dlaczego=2, dojazd=' Na miejscu wystarczy robotowi ok. 2×2 m równej podłogi i gniazdko 230 V. Plener nad morzem też wchodzi w grę, o ile podłoże jest utwardzone.', zmiany=[
  ('Wynajem robota humanoidalnego Unitree G1 w Gdańsku i Trójmieście to szansa na wyróżnienie eventu w regionie, który coraz odważniej sięga po innowacyjne atrakcje. Dowozimy G1 do każdego miejsca w Trójmieście bez dopłat: Gdańsk, Gdynia, Sopot, Rumia, Reda.',
   'Robot dojeżdża do każdego miejsca w Trójmieście bez dopłat: do Gdańska, Gdyni, Sopotu, Rumi i Redy.'),
  ('Typowe zastosowania robota w Trójmieście to: konferencje technologiczne i morskie na Amberexpo, gale i eventy korporacyjne w hotelach w Sopocie, eventy startupowe w Gdyni, dni otwarte uczelni (Politechnika Gdańska, UG) oraz plenerowe festiwale technologiczne. Innowacyjny, otwarty na świat klimat Trójmiasta dobrze pasuje do robotyki.',
   'Na konferencjach technologicznych i morskich w AmberExpo, na galach w sopockich hotelach, na eventach startupowych w Gdyni i na dniach otwartych Politechniki Gdańskiej czy UG. Latem dochodzą plenerowe festiwale.'),
  ('Robot dojedzie m.in. do takich obiektów jak: Amberexpo Gdańsk, Europejskie Centrum Solidarności, Gdynia Arena, Sopot Congress, hotele Hilton, Sofitel, Radisson, a także do każdego innego miejsca, które wskażesz.',
   'AmberExpo, Europejskie Centrum Solidarności, Gdynia Arena, hotele w Sopocie i na Głównym Mieście (Hilton, Radisson, Sofitel). Pracujemy też na ulicy: pokaz LEX AI odbył się na Długim Targu.'),
  ('<li><strong>Długi Targ i Główne Miasto</strong>, plenerowe akcje promocyjne, to tu robot 33bots doradzał prawnie dla LEX AI, o czym mówił Teleexpress TVP.</li>',
   '<li><strong>Długi Targ i Główne Miasto</strong>: plenerowe akcje promocyjne. Tu robot promował aplikację LEX AI, o czym mówił Teleexpress TVP.</li>'),
 ]),
 'wroclaw': dict(dlaczego=3, dojazd=' Robot potrzebuje ok. 2×2 m równej podłogi i gniazdka 230 V. Wnosimy go i uruchamiamy sami, zanim wpuścisz gości.', zmiany=[
  ('Wynajem robota humanoidalnego Unitree G1 we Wrocławiu to naturalny wybór dla firm chcących budować wizerunek innowatora. Dowozimy G1 bezpośrednio do każdego obiektu we Wrocławiu, bez dopłat za transport. Obsługujemy centrum, Fabryczną, Krzyki i okolice.',
   'Dowozimy robota do każdego obiektu we Wrocławiu bez dopłat za transport, od centrum po Fabryczną i Krzyki.'),
  ('Typowe zastosowania robota we Wrocławiu to: konferencje IT i game dev, eventy korporacyjne w Hali Stulecia, stoiska na Wrocław Expo, dni otwarte firm technologicznych, inauguracje biur i showroomów w centrum oraz eventy studenckie na uczelniach. Wrocław to miasto, które kocha technologię, więc robot G1 dobrze się tu odnajduje.',
   'Na konferencjach IT i game dev, na eventach firmowych w Hali Stulecia, na dniach otwartych firm technologicznych, przy otwarciu biura albo showroomu i na wydarzeniach studenckich.'),
  ('Robot dojedzie m.in. do takich obiektów jak: Hala Stulecia, Wrocław Expo, Centrum Kongresowe, Targi Wrocław, hotele DoubleTree, Sofitel, Radisson, a także do każdego innego miejsca, które wskażesz.',
   'Hala Stulecia, Wrocławskie Centrum Kongresowe, Narodowe Forum Muzyki, Tarczyński Arena, a z hoteli m.in. DoubleTree, Sofitel i Radisson. Każde inne miejsce też, wystarczy adres.'),
 ]),
 'poznan': dict(dlaczego=4, dojazd=' Na stoisku wystarczy robotowi ok. 2×2 m i gniazdko 230 V. Przy targach kilkudniowych robot zostaje z operatorem przez wszystkie dni, a każdy kolejny dzień jest 15% tańszy.', zmiany=[
  ('Wynajem robota humanoidalnego Unitree G1 w Poznaniu to idealne rozwiązanie dla wystawców na targach MTP i organizatorów konferencji. Dowozimy G1 bezpośrednio na teren targów lub do każdego innego obiektu w Poznaniu bez dopłat za transport.',
   'Najczęściej piszą do nas wystawcy MTP i organizatorzy konferencji. Robota dowozimy na teren targów albo do każdego innego obiektu w Poznaniu, bez dopłat za transport.'),
  ('Typowe zastosowania robota w Poznaniu to: stoiska targowe na MTP (motoryzacja, budownictwo, przemysł, tech), ale też konferencje korporacyjne w Centrum Kongresowym, eventy branżowe w hotelach, otwarcia firm i gale pracownicze. Robot G1 jest szczególnie skuteczny na targach, bo zatrzymuje tłumy i generuje leady dla Twojego działu sprzedaży.',
   'Przede wszystkim na stoiskach MTP: motoryzacja, budownictwo, przemysł, technologie. Na targach robot zatrzymuje ludzi w alejce, a Twoi handlowcy mają z kim rozmawiać. Poza targami pracuje na konferencjach w Poznań Congress Center, na galach pracowniczych i przy otwarciach firm.'),
  ('Robot dojedzie m.in. do takich obiektów jak: Targi Poznańskie MTP, Centrum Kongresowe Poznań, Poznań Congress Center, hotele Sheraton, Blow Up Hall, IQ Hotel, a także do każdego innego miejsca, które wskażesz.',
   'Międzynarodowe Targi Poznańskie z Poznań Congress Center, Stary Browar z hotelem Blow Up Hall, Sheraton przy Bukowskiej i każde inne miejsce, które wskażesz.'),
 ]),
 'katowice': dict(dlaczego=1, dojazd=' Na miejscu robot potrzebuje ok. 2×2 m równej podłogi i gniazdka 230 V.', zmiany=[
  ('Unitree G1 przyjeżdża na wydarzenia w Katowicach z operatorem, a transport jest w cenie. Dowozimy G1 bezpośrednio na miejsce eventu, bez dopłat za transport. Obsługujemy centrum Katowic, dzielnice i całą aglomerację śląską.',
   'Robot przyjeżdża z operatorem, a transport jest w cenie dla Katowic i całej aglomeracji śląskiej.'),
  ('Typowe zastosowania robota na Śląsku to: stoiska targowe na EXPO Silesia, konferencje branżowe w MCK i Spodku, gale korporacyjne oraz otwarcia showroomów. G1 sprawdza się wszędzie tam, gdzie chcesz przyciągnąć uwagę gości.',
   'Na stoiskach w Expo Silesia w Sosnowcu, na konferencjach branżowych w MCK i w Spodku, na galach firmowych i przy otwarciach showroomów.'),
  ('Robot dojedzie m.in. do takich obiektów jak: EXPO Silesia, MCK Katowice, Spodek, hotele Qubus, Angelo, Mercure, a także do każdego innego miejsca, które wskażesz.',
   'MCK, Spodek, NOSPR, Expo Silesia, a z hoteli m.in. Qubus, Angelo i Mercure. Dojedziemy też do zakładu pracy, jeśli event odbywa się na hali.'),
 ]),
 'lodz': dict(dlaczego=2, dojazd=' Robot potrzebuje ok. 2×2 m równej podłogi i gniazdka 230 V; w halach pofabrycznych sprawdzamy wcześniej nawierzchnię.', zmiany=[
  ('Unitree G1 przyjeżdża na wydarzenia w Łodzi z operatorem, a transport jest w cenie. Dowozimy G1 bezpośrednio na miejsce eventu bez dopłat za transport. Obsługujemy centrum Łodzi oraz całe województwo łódzkie.',
   'Do Łodzi i całego województwa łódzkiego przyjeżdżamy z robotem i operatorem, bez dopłat za transport.'),
  ('Typowe zastosowania robota w Łodzi to: eventy w przestrzeniach EC1 i Manufaktury, konferencje IT i e-commerce, gale branżowe oraz targi. G1 sprawdza się wszędzie tam, gdzie chcesz przyciągnąć uwagę i zostać w pamięci gości.',
   'W przestrzeniach EC1 i Manufaktury, na konferencjach IT i e-commerce, na galach branżowych i na targach w hali EXPO-Łódź.'),
  ('Robot dojedzie m.in. do takich obiektów jak: Hala Expo Łódź, EC1, OFF Piotrkowska, Manufaktura, hotele Andel\'s, DoubleTree, a także do każdego innego miejsca, które wskażesz.',
   'EC1, OFF Piotrkowska, Manufaktura, Monopolis, hala EXPO-Łódź, Atlas Arena, a z hoteli m.in. andel\'s i DoubleTree.'),
  ('Chętnie wykorzystują to ekipy produkcyjne przy sesjach i teledyskach.',
   'To gotowe tło do sesji zdjęciowej albo teledysku.'),
 ]),
 'krakow': dict(dlaczego=4, dojazd=' Na miejscu wystarczy ok. 2×2 m równej podłogi i gniazdko 230 V. W zabytkowych wnętrzach Starego Miasta sprawdzamy wcześniej wejście i schody.', zmiany=[
  ('Wynajem robota humanoidalnego Unitree G1 w Krakowie to doskonały sposób na wyróżnienie eventu w bardzo konkurencyjnym środowisku. Dowozimy G1 bezpośrednio na miejsce, bez dopłat za transport. Obsługujemy Stare Miasto, Kazimierz, Zabłocie, Nową Hutę i okolice Krakowa.',
   'W mieście, w którym kongres goni kongres, trudno się wyróżnić. Robota dowozimy bez dopłat na Stare Miasto, Kazimierz, Zabłocie, do Nowej Huty i pod Kraków.'),
  ('Typowe zastosowania robota w Krakowie to: konferencje technologiczne na ICE Kraków, stoiska wystawiennicze na EXPO Kraków, gale studenckie i korporacyjne, otwarcia biur i showroomów w centrum miasta oraz eventy startupowe. Robot G1 wzbudza ogromne zainteresowanie zarówno wśród uczestników konferencji naukowych, jak i gości eventów biznesowych.',
   'Na konferencjach technologicznych w ICE Kraków, na stoiskach w EXPO Kraków, na galach studenckich i firmowych, przy otwarciu biura w centrum i na eventach startupowych.'),
  ('Robot dojedzie m.in. do takich obiektów jak: ICE Kraków Congress Centre, EXPO Kraków, Tauron Arena, Centrum Kongresowe, hotele Sheraton, Radisson, Hilton, a także do każdego innego miejsca, które wskażesz.',
   'ICE Kraków, EXPO Kraków, Tauron Arena, a z hoteli m.in. Sheraton, Radisson i Hilton. Do kameralnej sali na Kazimierzu też.'),
 ]),
 'lublin': dict(dlaczego=3, dojazd=' Robot potrzebuje ok. 2×2 m równej podłogi i gniazdka 230 V. Na plenerze, np. na juwenaliach, wystarczy utwardzony fragment terenu i zadaszenie.', zmiany=[
  ('Unitree G1 przyjeżdża na wydarzenia w Lublinie z operatorem, a transport jest w cenie. Dowozimy G1 bezpośrednio na miejsce eventu bez dopłat. Obsługujemy centrum Lublina oraz całe województwo lubelskie.',
   'Do Lublina i całego województwa lubelskiego jedziemy z robotem i operatorem bez dopłat za transport.'),
  ('Typowe zastosowania robota w Lublinie to: targi, konferencje akademickie i biznesowe, gale firmowe oraz eventy dla studentów. G1 sprawdza się wszędzie tam, gdzie chcesz przyciągnąć uwagę i zostać w pamięci gości.',
   'Na targach, konferencjach akademickich i biznesowych, galach firmowych i wydarzeniach dla studentów.'),
  ('Robot dojedzie m.in. do takich obiektów jak: Targi Lublin, Centrum Kongresowe Uniwersytetu Przyrodniczego, CH Tarasy, hotele Hampton by Hilton, Campanile, a także do każdego innego miejsca, które wskażesz.',
   'Targi Lublin, Centrum Spotkania Kultur, Centrum Kongresowe Uniwersytetu Przyrodniczego, Arena Lublin, a z hoteli m.in. Hampton by Hilton.'),
  ('Najdłuższe kolejki do zdjęć z G1 ustawiają się tu na juwenaliach, festiwalach nauki i targach pracy.',
   'Juwenalia, festiwale nauki i targi pracy przyciągają tu tysiące studentów, a to publiczność, która nagrywa robota od pierwszej minuty.'),
 ]),
 'szczecin': dict(dlaczego=1, dojazd=' Robot potrzebuje ok. 2×2 m równej podłogi i gniazdka 230 V.', zmiany=[
  ('Unitree G1 przyjeżdża na wydarzenia w Szczecinie z operatorem, a transport jest w cenie. Dowozimy G1 bezpośrednio na miejsce eventu bez dopłat. Obsługujemy centrum Szczecina oraz całe Pomorze Zachodnie.',
   'Robot przyjeżdża z operatorem do Szczecina i na całe Pomorze Zachodnie, bez dopłat za transport. Pracował już tu na targach nieruchomości, przy stoisku Matys Development.'),
  ('Typowe zastosowania robota w Szczecinie to: targi, konferencje branżowe, gale korporacyjne w Zamku Książąt Pomorskich oraz eventy w Pomerania Convention Center. G1 sprawdza się wszędzie tam, gdzie chcesz przyciągnąć uwagę gości.',
   'Na targach (także nieruchomości), na konferencjach branżowych, na galach w Zamku Książąt Pomorskich i na wydarzeniach w Netto Arenie.'),
  ('Robot dojedzie m.in. do takich obiektów jak: Pomerania Convention Center, Netto Arena, Zamek Książąt Pomorskich, hotele Radisson Blu, Sheraton, a także do każdego innego miejsca, które wskażesz.',
   'Netto Arena, Zamek Książąt Pomorskich, Filharmonia, Stara Rzeźnia, a z hoteli m.in. Radisson Blu i Sheraton.'),
 ]),
 'bydgoszcz': dict(dlaczego=2, dojazd=' Robot potrzebuje ok. 2×2 m równej podłogi i gniazdka 230 V.', zmiany=[
  ('Unitree G1 przyjeżdża na wydarzenia w Bydgoszczy z operatorem, a transport jest w cenie. Dowozimy G1 bezpośrednio na miejsce eventu bez dopłat za transport. Obsługujemy centrum Bydgoszczy oraz całe województwo kujawsko-pomorskie.',
   'Do Bydgoszczy i całego województwa kujawsko-pomorskiego jedziemy z robotem i operatorem, bez dopłat za transport.'),
  ('Typowe zastosowania robota w Bydgoszczy to: konferencje w BKCC, gale korporacyjne, eventy branżowe oraz otwarcia salonów i showroomów. G1 sprawdza się wszędzie tam, gdzie chcesz przyciągnąć uwagę i zostać w pamięci gości.',
   'Na konferencjach w BKCC, galach firmowych, eventach branżowych, dniach otwartych zakładów i przy otwarciach salonów.'),
  ('Robot dojedzie m.in. do takich obiektów jak: BKCC Bydgoszcz, Filharmonia Pomorska, Myślęcinek, hotele Holiday Inn, Focus, a także do każdego innego miejsca, które wskażesz.',
   'BKCC, Opera Nova, Filharmonia Pomorska, Młyny Rothera, Łuczniczka, park w Myślęcinku, a z hoteli m.in. Holiday Inn.'),
  ('Bydgoski przemysł narzędziowy i sektor IT chętnie sięgają po robota na dni otwarte zakładów i targi pracy. W tym regionie technologiczny wizerunek pracodawcy realnie przekłada się na rekrutację.',
   'Bydgoski przemysł narzędziowy i sektor IT szukają ludzi. Na dniu otwartym zakładu albo na targach pracy robot pomaga pokazać pracodawcę od nowoczesnej strony.'),
 ]),
 'bialystok': dict(dlaczego=3, dojazd=' Robot potrzebuje ok. 2×2 m równej podłogi i gniazdka 230 V.', zmiany=[
  ('Unitree G1 przyjeżdża na wydarzenia w Białymstoku z operatorem, a transport jest w cenie. Dowozimy G1 bezpośrednio na miejsce eventu bez dopłat. Obsługujemy centrum Białegostoku oraz całe województwo podlaskie.',
   'Do Białegostoku i na całe Podlasie przyjeżdżamy z robotem i operatorem, bez dopłat za transport.'),
  ('Typowe zastosowania robota w Białymstoku to: gale w Operze i Filharmonii Podlaskiej, konferencje branżowe, eventy korporacyjne i akademickie. G1 sprawdza się wszędzie tam, gdzie chcesz przyciągnąć uwagę i zostać w pamięci gości.',
   'Na galach w Operze i Filharmonii Podlaskiej, konferencjach branżowych, eventach firmowych i uczelnianych.'),
  ('Robot dojedzie m.in. do takich obiektów jak: Opera i Filharmonia Podlaska, Podlaskie Centrum Kultury, Branicki Palace, hotele Qubus, Hampton by Hilton, a także do każdego innego miejsca, które wskażesz.',
   'Opera i Filharmonia Podlaska, Pałac Branickich, Stadion Miejski, a z hoteli m.in. Qubus i Hampton by Hilton.'),
  ('Wystąpienie G1 w regionie regularnie kończy się materiałem w lokalnych mediach, co organizatorzy wliczają w wartość wynajmu.',
   'A nowość łatwiej trafia do relacji gości i do lokalnych mediów.'),
 ]),
}

for miasto, d in MIASTA.items():
    f = TU / f'robot-wynajem-{miasto}.html'
    t = f.read_text(encoding='utf-8')
    for a, b in d['zmiany']:
        assert t.count(a) == 1, (miasto, a[:60])
        t = t.replace(a, b)
    assert len(STARE_DLACZEGO.findall(t)) == 1, (miasto, 'dlaczego')
    t = STARE_DLACZEGO.sub(f'<p>{DLACZEGO[d["dlaczego"]]}</p>', t)
    assert len(STARE_DOJAZD_KONIEC.findall(t)) == 1, (miasto, 'dojazd')
    t = STARE_DOJAZD_KONIEC.sub(d['dojazd'], t)
    f.write_text(t, encoding='utf-8')
    print('  ✓', miasto)
