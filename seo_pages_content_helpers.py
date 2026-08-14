# -*- coding: utf-8 -*-
"""Buildery treści dla podstron typów wydarzeń, eventów branżowych i imprez prywatnych."""

from seo_pages_content import mk, faq_price, faq_safe, faq_operator, faq_transport, faq_book


def _seed(slug):
    return sum(ord(c) for c in slug)


def _pick(pool, slug, offset=0):
    return pool[(_seed(slug) + offset) % len(pool)]


def _pick2(pool, slug):
    s = _seed(slug)
    i = s % len(pool)
    j = (s + 1 + s % (len(pool) - 1)) % len(pool)
    if j == i:
        j = (i + 1) % len(pool)
    return [pool[i], pool[j]]


DESCS = [
    "Robot {na} — atrakcja, której goście nie zapomną. Unitree G1: powitanie gości, pokaz tańca, rozmowy z AI. Dojazd w całej Polsce, operator w cenie →",
    "Wynajmij robota humanoidalnego {na}. Unitree G1 wita gości, tańczy i rozmawia dzięki AI. Cała Polska, transport i operator w cenie →",
    "Robot humanoidalny {na}: pokaz choreografii, interakcje z gośćmi i strefa zdjęć. Unitree G1 z certyfikowanym operatorem, dojazd w całej Polsce →",
]

EYEBROWS = [
    "Wynajem robota · Atrakcja eventowa · Cała Polska",
    "Robot humanoidalny · Unitree G1 · Pokaz z operatorem",
    "Atrakcja premium · Unitree G1 · Cała Polska",
]

TILES_H2 = [
    "Atrakcja, o której<br />będą mówić latami",
    "Dlaczego robot<br />robi różnicę",
    "Efekt WOW<br />z gwarancją",
]

SCEN_INTROS = [
    "Program pokazu dopasowujemy do agendy i charakteru wydarzenia. Najczęściej łączymy trzy sprawdzone elementy:",
    "Robot nie musi być obecny cały czas — jego wejścia planujemy na najmocniejsze momenty wydarzenia:",
    "Scenariusz ustalamy wspólnie przed wydarzeniem. Oto elementy, które sprawdzają się najlepiej:",
]


def _tile_pool(Loc):
    loc = Loc[0].lower() + Loc[1:]
    return [
        ("Efekt WOW", "Moment, który zapamiętają",
         f"{Loc} większość gości pierwszy raz w życiu widzi humanoida na żywo. Robot buduje wokół siebie tłum w kilka minut — bez zapowiedzi i bez zaproszeń."),
        ("Viral", "Content robi się sam",
         "Każda interakcja z robotem kończy się nagraniem. Relacje i rolki z Twojego wydarzenia trafiają do sieci jeszcze w trakcie jego trwania."),
        ("Bez stresu", "Operator w cenie, dojazd według lokalizacji",
         "Przyjeżdżamy, rozstawiamy się i prowadzimy pokaz od A do Z. Certyfikowany operator czuwa nad wszystkim — Ty zajmujesz się gośćmi."),
        ("Zdjęcia", "Strefa foto, która nie pustoszeje",
         f"G1 pozuje, przybija piątki i gestykuluje — {loc} kolejka do zdjęcia z robotem to najdłużej działający punkt programu."),
    ]


def _scen_pool(Loc):
    loc = Loc[0].lower() + Loc[1:]
    return [
        ("Powitanie gości",
         f"Robot staje przy wejściu i wita przybywających gestem oraz głosem — {loc} od pierwszych minut czuć, że to nie będzie zwykłe wydarzenie."),
        ("Interakcje i strefa zdjęć",
         "G1 podchodzi do gości, przybija piątki i pozuje do zdjęć. Wokół robota przez cały czas gromadzi się tłum chętnych na wspólne ujęcie."),
        ("Pokaz choreografii",
         "Kulminacyjny moment: robot wykonuje układ taneczny zsynchronizowany z muzyką. To ten fragment wydarzenia, który generuje najwięcej nagrań i braw."),
    ]


def _extra_faq(slug):
    return _pick([faq_safe(), faq_operator(), faq_transport()], slug)


def ev(slug, crumb, na, Loc, sub, uniq_tile, uniq_scen, faq_uniq,
       video=None, guides="default", related=None, blog=None):
    loc = Loc[0].lower() + Loc[1:]
    d = mk(
        slug=slug, crumb=crumb,
        title=f"Robot {na} — wynajem robota humanoidalnego | 33bots",
        desc=_pick(DESCS, slug).format(na=na),
        keywords=f"robot {na}, wynajem robota {na}, atrakcja {na}, robot humanoidalny {na}, Unitree G1 {na}",
        eyebrow=_pick(EYEBROWS, slug),
        h1=f"{crumb} —<br />Unitree G1.",
        sub=sub,
        tiles_h2=_pick(TILES_H2, slug),
        tiles=[uniq_tile] + _pick2(_tile_pool(Loc), slug),
        scen_title=f"Jak robot sprawdza się {loc}?",
        scen_intro=_pick(SCEN_INTROS, slug),
        scens=[uniq_scen] + _pick2(_scen_pool(Loc), slug),
        faqs=[faq_uniq, faq_price(na), _extra_faq(slug), faq_book(na)],
        faq_h2=f"Pytania o robota<br />{na}",
        kontakt_h2=f"Zarezerwuj robota<br />{na}.",
        video=video or _pick(["gesty", "taniec", "powitanie", "spacer"], slug),
        guides=guides,
    )
    if blog:
        d["blog_link"] = blog
    if related:
        d["related"] = related
        d["_related_fixed"] = True
    return d


def br(suffix, nom, na, Loc, aud, uniq, faq,
       guides="default", video=None, blog=None):
    slug = "robot-na-event-" + suffix
    crumb = "Robot na " + nom
    Nom = nom[0].upper() + nom[1:]
    uniq_tile = ("Branża", "Program pod Twoją publiczność",
                 f"{Nom} ma swoją dynamikę — i my ją znamy. Ton pokazu, momenty wejść i treści, o których robot mówi dzięki AI, dopasowujemy do specyfiki wydarzenia.")
    uniq_scen = ("Rola w programie wydarzenia",
                 f"Robot może otworzyć wydarzenie, pracować w strefie partnera albo poprowadzić pokaz sceniczny — {Loc[0].lower() + Loc[1:]} sprawdzają się wszystkie te warianty.")
    sub = f"{uniq} Pokaz robota humanoidalnego Unitree G1 przyciąga {aud} — i zamienia Twoje wydarzenie w temat rozmów całej branży."
    return ev(slug, crumb, na, Loc, sub, uniq_tile, uniq_scen, faq,
              video=video, guides=guides, blog=blog)


PRIV_DESCS = [
    "Robot {na} — niespodzianka, o której będzie mówić cała rodzina. Unitree G1 tańczy, składa życzenia i pozuje do zdjęć. Operator w cenie →",
    "Wynajmij robota humanoidalnego {na}. Taniec, życzenia, wspólne zdjęcia — atrakcja, której nie zapomni żaden gość. Cała Polska →",
    "Robot humanoidalny {na}: pokaz tańca, interakcje z gośćmi i pamiątkowe zdjęcia. Z certyfikowanym operatorem, dojazd w całej Polsce →",
]


def _priv_tile_pool(Loc):
    loc = Loc[0].lower() + Loc[1:]
    return [
        ("Niespodzianka", "Efekt, którego nikt się nie spodziewa",
         f"Wejście prawdziwego robota to niespodzianka, której nie przebije żaden inny pomysł — {loc} reakcje gości są bezcenne, a nagrania z nich jeszcze lepsze."),
        ("Pamiątka", "Zdjęcia i nagrania na lata",
         "Każdy gość wychodzi z materiałem w telefonie, a Wy — ze wspomnieniem, do którego będziecie wracać przy każdej rodzinnej okazji."),
        ("Bez stresu", "Operator zajmuje się wszystkim",
         "Przyjeżdżamy, prowadzimy pokaz i czuwamy nad bezpieczeństwem. Wy świętujecie — my dbamy, żeby robot był gwiazdą wieczoru."),
        ("Pokolenia", "Atrakcja dla każdego gościa",
         "Od dzieci po dziadków — robot bawi wszystkich naraz. To jedna z niewielu atrakcji, która naprawdę łączy pokolenia przy jednym stole."),
    ]


def priv(slug, crumb, na, Loc, sub, uniq_scen, faq_uniq, guides_override=None):
    loc = Loc[0].lower() + Loc[1:]
    d = mk(
        slug=slug, crumb=crumb,
        title=f"{crumb} — wynajem robota humanoidalnego | 33bots",
        desc=_pick(PRIV_DESCS, slug).format(na=na),
        keywords=f"robot {na}, wynajem robota {na}, atrakcja {na}, robot humanoidalny {na}, niespodzianka {na}",
        eyebrow=_pick(EYEBROWS, slug),
        h1=f"{crumb} —<br />Unitree G1.",
        sub=sub,
        tiles_h2=_pick(TILES_H2, slug),
        tiles=_pick2(_priv_tile_pool(Loc), slug) + [_priv_tile_pool(Loc)[(_seed(slug) + 2) % 4]],
        scen_title=f"Jak robot sprawdza się {loc}?",
        scen_intro=_pick(SCEN_INTROS, slug),
        scens=[uniq_scen] + _pick2(_scen_pool(Loc), slug),
        faqs=[faq_uniq, faq_price(na), _extra_faq(slug), faq_book(na)],
        faq_h2=f"Pytania o robota<br />{na}",
        kontakt_h2=f"Zarezerwuj robota<br />{na}.",
        video=_pick(["taniec", "gesty", "powitanie"], slug),
        guides=guides_override or "default",
    )
    return d


def chain_related(pages):
    """Linkowanie wewnętrzne: każda strona bez własnych related linkuje do sąsiadów w kategorii."""
    n = len(pages)
    for i, p in enumerate(pages):
        if p.get("_related_fixed"):
            continue
        nxt = pages[(i + 1) % n]
        prv = pages[(i - 1) % n]
        p["related"] = [
            (nxt["slug"] + ".html", nxt["crumb"]),
            (prv["slug"] + ".html", prv["crumb"]),
        ]
        p["related_intro"] = "Organizujesz inne wydarzenie? Zobacz podobne scenariusze"
    return pages
