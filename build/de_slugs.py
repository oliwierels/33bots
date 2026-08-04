# -*- coding: utf-8 -*-
"""
Mapa plików serwis PL → serwis DE.

Serwis niemiecki jest lustrem 1:1 serwisu polskiego: ta sama liczba stron,
ta sama struktura, ten sam graf linków wewnętrznych i te same zdjęcia.
Różni się wyłącznie językiem treści i merytoryką dopasowaną do rynku
niemieckiego (miasta, lokalizacje eventowe, święta, waluta).

Klucz  = nazwa pliku w serwisie PL (i jednocześnie klucz treści DE)
Wartość = nazwa pliku w serwisie DE
"""

# ── Strony rdzeniowe i ręczne ─────────────────────────────────────────
CORE = {
    "index.html": "index.html",
    "404.html": "404.html",
    "index-redesign.html": "index-redesign.html",
    "oferta.html": "leistungen.html",
    "oferta-targi.html": "angebot-messen.html",
    "oferta-konferencje.html": "angebot-konferenzen-galas.html",
    "oferta-dni-otwarte.html": "angebot-tag-der-offenen-tuer.html",
    "realizacje-wideo.html": "referenzen-videos.html",
    "blog.html": "blog.html",
    "case-study-lexai.html": "case-study-lexai.html",
    "case-study-wallstreet.html": "case-study-wallstreet.html",
    "case-study-women-in-tech.html": "case-study-women-in-tech.html",
    "szablon-case-study.html": "vorlage-case-study.html",
    "wypozyczenie-robota.html": "humanoiden-roboter-mieten.html",
    "robot-na-wesele.html": "roboter-hochzeit.html",
    "robot-na-impreze.html": "roboter-party.html",
}

# ── 98 podstron SEO (generowane z seo_pages_content) ──────────────────
SEO = {
    # usługi
    "atrakcje-na-event.html": "event-attraktionen.html",
    "nowoczesne-atrakcje-eventowe.html": "moderne-event-attraktionen.html",
    "show-robotow.html": "roboter-show.html",
    "wynajem-robota-do-firmy.html": "roboter-fuer-unternehmen-mieten.html",
    "wynajem-robotow.html": "roboter-mieten.html",
    "robot-dla-agencji-eventowych.html": "roboter-fuer-eventagenturen.html",
    "robot-employer-branding.html": "roboter-employer-branding.html",
    # role robota
    "robot-humanoidalny-na-event.html": "humanoider-roboter-event.html",
    "robot-ai-na-wydarzenie.html": "ki-roboter-veranstaltung.html",
    "robot-konferansjer.html": "roboter-moderator.html",
    "robot-prezenter.html": "roboter-praesentator.html",
    "robot-prelegent.html": "roboter-redner.html",
    "robot-prowadzacy-event.html": "roboter-eventmoderation.html",
    "robot-witajacy-gosci.html": "roboter-gaesteempfang.html",
    "robot-recepcjonista.html": "roboter-rezeptionist.html",
    "robot-tancerz.html": "roboter-taenzer.html",
    # miejsca
    "robot-do-centrum-handlowego.html": "roboter-einkaufszentrum.html",
    "robot-do-galerii-handlowej.html": "roboter-shoppingcenter.html",
    "robot-do-hotelu.html": "roboter-hotel.html",
    "robot-do-restauracji.html": "roboter-restaurant.html",
    "robot-do-marketingu.html": "roboter-marketing.html",
    "robot-do-reklamy-i-filmu.html": "roboter-werbung-film.html",
    "robot-do-teledysku.html": "roboter-musikvideo.html",
    "robot-do-sesji-zdjeciowej.html": "roboter-fotoshooting.html",
    "robot-dla-dzieci.html": "roboter-fuer-kinder.html",
    "robot-dla-sklepow.html": "roboter-einzelhandel.html",
    "robot-dla-franczyzy.html": "roboter-franchise.html",
    "robot-na-uczelnie.html": "roboter-hochschule.html",
    # typy wydarzeń
    "robot-na-event.html": "roboter-event.html",
    "robot-na-targi.html": "roboter-messe.html",
    "robot-na-konferencje.html": "roboter-konferenz.html",
    "robot-na-konferencje-technologiczna.html": "roboter-tech-konferenz.html",
    "robot-na-gale.html": "roboter-gala.html",
    "robot-na-bankiet.html": "roboter-bankett.html",
    "robot-na-impreze-firmowa.html": "roboter-firmenfeier.html",
    "roboty-na-eventy-firmowe.html": "roboter-firmenevents.html",
    "robot-na-integracje-firmowa.html": "roboter-teamevent.html",
    "robot-na-piknik-firmowy.html": "roboter-betriebsfest.html",
    "robot-na-team-building.html": "roboter-teambuilding.html",
    "robot-na-szkolenie.html": "roboter-schulung.html",
    "robot-na-rocznice-firmy.html": "roboter-firmenjubilaeum.html",
    "robot-na-premiere-produktu.html": "roboter-produktlaunch.html",
    "robot-na-otwarcie.html": "roboter-eroeffnung.html",
    "robot-na-dzien-otwarty.html": "roboter-tag-der-offenen-tuer.html",
    "robot-na-targi-pracy.html": "roboter-karrieremesse.html",
    "robot-na-roadshow.html": "roboter-roadshow.html",
    "robot-na-wystawe.html": "roboter-ausstellung.html",
    "robot-na-expo.html": "roboter-expo.html",
    "robot-na-konwent.html": "roboter-convention.html",
    "robot-na-festiwal.html": "roboter-festival.html",
    "robot-na-dni-miasta.html": "roboter-stadtfest.html",
    "robot-na-wystep-sceniczny.html": "roboter-buehnenshow.html",
    "robot-na-ceremonie.html": "roboter-zeremonie.html",
    # eventy branżowe
    "robot-na-event-it.html": "roboter-it-event.html",
    "robot-na-event-gamingowy.html": "roboter-gaming-event.html",
    "robot-na-event-korporacyjny.html": "roboter-corporate-event.html",
    "robot-na-event-medyczny.html": "roboter-medizin-event.html",
    "robot-na-event-farmaceutyczny.html": "roboter-pharma-event.html",
    "robot-na-event-finansowy.html": "roboter-finanz-event.html",
    "robot-na-event-prawniczy.html": "roboter-legal-event.html",
    "robot-na-event-nieruchomosci.html": "roboter-immobilien-event.html",
    "robot-na-event-budowlany.html": "roboter-bau-event.html",
    "robot-na-event-przemyslowy.html": "roboter-industrie-event.html",
    "robot-na-event-energetyczny.html": "roboter-energie-event.html",
    "robot-na-event-logistyczny.html": "roboter-logistik-event.html",
    "robot-na-event-motoryzacyjny.html": "roboter-automotive-event.html",
    "robot-na-event-telekomunikacyjny.html": "roboter-telekom-event.html",
    "robot-na-event-handlowy.html": "roboter-handel-event.html",
    "robot-na-event-gastronomiczny.html": "roboter-gastro-event.html",
    "robot-na-event-turystyczny.html": "roboter-tourismus-event.html",
    "robot-na-event-sportowy.html": "roboter-sport-event.html",
    "robot-na-event-kulturalny.html": "roboter-kultur-event.html",
    "robot-na-event-modowy.html": "roboter-fashion-event.html",
    "robot-na-event-beauty.html": "roboter-beauty-event.html",
    "robot-na-event-edukacyjny.html": "roboter-bildungs-event.html",
    "robot-na-event-ekologiczny.html": "roboter-nachhaltigkeits-event.html",
    "robot-na-event-charytatywny.html": "roboter-charity-event.html",
    "robot-na-event-startupowy.html": "roboter-startup-event.html",
    "robot-na-event-miejski.html": "roboter-stadt-event.html",
    "robot-na-event-outdoor.html": "roboter-outdoor-event.html",
    "robot-na-event-hybrydowy.html": "roboter-hybrid-event.html",
    "robot-na-event-vip.html": "roboter-vip-event.html",
    # imprezy prywatne (dopasowane do kalendarza niemieckiego)
    "robot-na-urodziny.html": "roboter-geburtstag.html",
    "robot-na-imieniny.html": "roboter-polterabend.html",
    "robot-na-rocznice.html": "roboter-jubilaeum.html",
    "robot-na-impreze-prywatna.html": "roboter-privatfeier.html",
    "robot-na-wieczor-panienski.html": "roboter-junggesellinnenabschied.html",
    "robot-na-bal-maturalny.html": "roboter-abiball.html",
    "robot-na-komunie.html": "roboter-kommunion.html",
    "robot-na-chrzciny.html": "roboter-taufe.html",
    "robot-na-dzien-dziecka.html": "roboter-kinderfest.html",
    "robot-na-mikolajki.html": "roboter-nikolaus.html",
    "robot-na-andrzejki.html": "roboter-oktoberfest.html",
    "robot-na-halloween.html": "roboter-halloween.html",
    "robot-na-sylwestra.html": "roboter-silvester.html",
    "robot-na-karnawal.html": "roboter-karneval.html",
    "robot-na-walentynki.html": "roboter-valentinstag.html",
    "robot-na-garden-party.html": "roboter-gartenparty.html",
}

# ── 40 artykułów blogowych ────────────────────────────────────────────
BLOG = {
    "blog-robot-na-evencie.html": "blog-roboter-auf-dem-event.html",
    "blog-robotyka-w-marketingu.html": "blog-robotik-im-marketing.html",
    "blog-atrakcja-na-event-firmowy.html": "blog-attraktion-firmenevent.html",
    "blog-ile-kosztuje-wynajem-robota.html": "blog-was-kostet-roboter-mieten.html",
    "blog-atrakcje-eventowe.html": "blog-event-attraktionen-ranking.html",
    "blog-robot-na-wesele.html": "blog-roboter-auf-der-hochzeit.html",
    "blog-jak-wybrac-robota-na-event.html": "blog-roboter-fuer-event-auswaehlen.html",
    "blog-robot-humanoidalny-vs-mobilny.html": "blog-humanoider-vs-mobiler-roboter.html",
    "blog-robot-na-stoisko-targowe.html": "blog-roboter-am-messestand.html",
    "blog-jak-wynajac-robota-checklist.html": "blog-roboter-mieten-checkliste.html",
    "blog-co-potrafi-robot-humanoidalny.html": "blog-was-kann-ein-humanoider-roboter.html",
    "blog-bezpieczenstwo-robota-na-evencie.html": "blog-sicherheit-roboter-event.html",
    "blog-robot-z-ai-rozmawiajacy-po-polsku.html": "blog-ki-roboter-spricht-deutsch.html",
    "blog-robot-viral-marketing-event.html": "blog-roboter-viral-marketing.html",
    "blog-robot-ambasador-marki.html": "blog-roboter-als-markenbotschafter.html",
    "blog-robot-zamiast-hostessy.html": "blog-roboter-statt-hostess.html",
    "blog-robot-targi-vs-konferencja.html": "blog-roboter-messe-vs-konferenz.html",
    "blog-robot-na-event-dla-dzieci.html": "blog-roboter-kinderveranstaltung.html",
    "blog-unitree-g1-robot.html": "blog-unitree-g1-roboter.html",
    "blog-wypozyczenie-robota-przewodnik.html": "blog-roboter-mieten-leitfaden.html",
    "blog-ile-kosztuje-robot-humanoidalny.html": "blog-was-kostet-humanoider-roboter.html",
    "blog-jak-wybrac-firme-do-wynajmu-robota.html": "blog-anbieter-roboter-vermietung-waehlen.html",
    "blog-jak-przekonac-zarzad-do-robota.html": "blog-geschaeftsfuehrung-ueberzeugen.html",
    "blog-czy-robot-moze-prowadzic-event.html": "blog-kann-roboter-event-moderieren.html",
    "blog-branding-robota-na-event.html": "blog-roboter-branding-event.html",
    "blog-logistyka-robota-w-dniu-eventu.html": "blog-logistik-am-eventtag.html",
    "blog-psychologia-robota-humanoidalnego.html": "blog-psychologie-humanoider-roboter.html",
    "blog-kreatywne-sposoby-wykorzystania-robota.html": "blog-kreative-einsatzideen-roboter.html",
    "blog-robot-i-artysta-na-scenie.html": "blog-roboter-und-kuenstler-auf-der-buehne.html",
    "blog-robot-recepcjonista-witajacy-gosci.html": "blog-roboter-als-empfang.html",
    "blog-robot-na-stoisku-targowym-roi.html": "blog-roi-roboter-messestand.html",
    "blog-robot-na-targi-pracy.html": "blog-roboter-karrieremesse.html",
    "blog-robot-na-premiere-produktu.html": "blog-roboter-produktlaunch.html",
    "blog-robot-na-otwarcie-sklepu.html": "blog-roboter-store-eroeffnung.html",
    "blog-robot-na-piknik-firmowy.html": "blog-roboter-betriebsfest.html",
    "blog-robot-na-event-plenerowy.html": "blog-roboter-outdoor-event.html",
    "blog-robot-na-juwenalia-festiwal.html": "blog-roboter-campusfest.html",
    "blog-atrakcja-na-gale-firmowa.html": "blog-attraktion-firmengala.html",
    "blog-atrakcje-technologiczne-na-imprezy-firmowe.html": "blog-technologische-attraktionen-firmenfeier.html",
    "blog-roboty-humanoidalne-na-eventach-trendy.html": "blog-trends-humanoide-roboter-events.html",
}

# ── 35 stron miast — miasta polskie zastąpione niemieckimi ────────────
CITIES = {
    "robot-wynajem-warszawa.html": "roboter-mieten-berlin.html",
    "robot-wynajem-krakow.html": "roboter-mieten-muenchen.html",
    "robot-wynajem-wroclaw.html": "roboter-mieten-hamburg.html",
    "robot-wynajem-poznan.html": "roboter-mieten-koeln.html",
    "robot-wynajem-gdansk.html": "roboter-mieten-frankfurt.html",
    "robot-wynajem-katowice.html": "roboter-mieten-stuttgart.html",
    "robot-wynajem-lodz.html": "roboter-mieten-duesseldorf.html",
    "robot-wynajem-szczecin.html": "roboter-mieten-leipzig.html",
    "robot-wynajem-bydgoszcz.html": "roboter-mieten-dortmund.html",
    "robot-wynajem-lublin.html": "roboter-mieten-essen.html",
    "robot-wynajem-bialystok.html": "roboter-mieten-bremen.html",
    "robot-wynajem-rzeszow.html": "roboter-mieten-dresden.html",
    "robot-wynajem-torun.html": "roboter-mieten-hannover.html",
    "robot-wynajem-olsztyn.html": "roboter-mieten-nuernberg.html",
    "robot-wynajem-kielce.html": "roboter-mieten-duisburg.html",
    "robot-wynajem-opole.html": "roboter-mieten-bochum.html",
    "robot-wynajem-gliwice.html": "roboter-mieten-wuppertal.html",
    "robot-wynajem-czestochowa.html": "roboter-mieten-bielefeld.html",
    "robot-wynajem-radom.html": "roboter-mieten-bonn.html",
    "robot-wynajem-zielona-gora.html": "roboter-mieten-muenster.html",
    "robot-wynajem-plock.html": "roboter-mieten-karlsruhe.html",
    "robot-wynajem-elblag.html": "roboter-mieten-mannheim.html",
    "robot-wynajem-walbrzych.html": "roboter-mieten-augsburg.html",
    "robot-wynajem-wloclawek.html": "roboter-mieten-wiesbaden.html",
    "robot-wynajem-tarnow.html": "roboter-mieten-moenchengladbach.html",
    "robot-wynajem-koszalin.html": "roboter-mieten-braunschweig.html",
    "robot-wynajem-legnica.html": "roboter-mieten-kiel.html",
    "robot-wynajem-kalisz.html": "roboter-mieten-chemnitz.html",
    "robot-wynajem-grudziadz.html": "roboter-mieten-aachen.html",
    "robot-wynajem-rybnik.html": "roboter-mieten-halle.html",
    "robot-wynajem-slupsk.html": "roboter-mieten-magdeburg.html",
    "robot-wynajem-nowy-sacz.html": "roboter-mieten-freiburg.html",
    "robot-wynajem-pila.html": "roboter-mieten-krefeld.html",
    "robot-wynajem-karpacz.html": "roboter-mieten-mainz.html",
    "robot-wynajem-mikolajki.html": "roboter-mieten-luebeck.html",
}

SLUG_MAP = {}
SLUG_MAP.update(CORE)
SLUG_MAP.update(SEO)
SLUG_MAP.update(BLOG)
SLUG_MAP.update(CITIES)


def de(pl_file, anchor=""):
    """Zamienia link do pliku PL na link do odpowiednika DE."""
    if pl_file.startswith(("http", "mailto:", "tel:", "#")):
        return pl_file
    base, _, frag = pl_file.partition("#")
    target = SLUG_MAP.get(base, base)
    return target + (("#" + frag) if frag else "") + anchor


if __name__ == "__main__":
    print(f"CORE   {len(CORE):>3}")
    print(f"SEO    {len(SEO):>3}")
    print(f"BLOG   {len(BLOG):>3}")
    print(f"CITIES {len(CITIES):>3}")
    print(f"RAZEM  {len(SLUG_MAP):>3}")
    assert len(SLUG_MAP) == len(CORE) + len(SEO) + len(BLOG) + len(CITIES), "kolizja kluczy"
    assert len(set(SLUG_MAP.values())) == len(SLUG_MAP), "zduplikowane nazwy plików DE"
