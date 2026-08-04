# -*- coding: utf-8 -*-
"""
Buildery treści niemieckich podstron SEO.

Lustro seo_pages_content_helpers.py — te same struktury, te same pule,
ta sama logika losowania (seed liczony ze sluga PL, więc każda strona DE
dostaje dokładnie te same warianty kafelków, scenariuszy i wideo co jej
odpowiednik PL). Różni się wyłącznie język i realia rynku niemieckiego.
"""

# ── Stałe handlowe rynku DE ───────────────────────────────────────────
PRICE_RANGE = "1.290 – 1.590 €"
PRICE_LOW = "1290"
PRICE_HIGH = "1590"
DOG_PRICE = "450 €"


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


# ── Powtarzalne FAQ ───────────────────────────────────────────────────
def faq_price(x):
    return (f"Was kostet ein Roboter {x}?",
            f"Ein kompletter Veranstaltungstag kostet {PRICE_RANGE} — der endgültige Preis hängt ausschließlich "
            f"vom Veranstaltungsort ab. Anfahrt, zertifizierter Operator, Branding und Versicherung sind immer "
            f"enthalten. Schreiben Sie uns über das Formular oder rufen Sie an — Sie erhalten das Angebot "
            f"innerhalb von 24 Stunden.")


def faq_safe():
    return ("Ist der Roboter für die Gäste sicher?",
            "Ja — der Unitree G1 erkennt über LiDAR und Computer Vision Hindernisse und Personen in Echtzeit und "
            "weicht ihnen aus. Zusätzlich arbeitet er durchgehend unter Aufsicht eines zertifizierten "
            "33bots-Operators, der den Sicherheitsabstand kontrolliert. Eine Haftpflichtversicherung ist inklusive.")


def faq_operator():
    return ("Kommt der Roboter mit Betreuung?",
            "Ja — im Mietpreis ist immer ein zertifizierter Operator enthalten, der den Roboter steuert, für "
            "Sicherheit sorgt und die Interaktionen mit den Gästen begleitet. Sie müssen selbst nichts bedienen.")


def faq_transport():
    return ("Kommen Sie auch in unsere Stadt?",
            "Ja — wir sind deutschlandweit im Einsatz und die Anfahrt ist im Preis enthalten. Wir bedienen sowohl "
            "Großstädte als auch kleinere Orte, ohne Kilometerpauschale und ohne Mindestentfernung.")


def faq_book(x):
    return (f"Wie früh sollte man einen Roboter {x} buchen?",
            "Am besten mindestens 3–4 Wochen vor dem Termin. In der Hochsaison (Frühjahr und Herbst) sind die "
            "Termine schneller vergeben — fragen Sie also lieber früher an. Die Reservierung ist kostenlos und "
            "ohne Anzahlung.")


DEFAULTS = {
    "tiles_h2": "Eine Attraktion, die<br />auf Ihr Ziel einzahlt",
    "scen_title": "Wie sieht das in der Praxis aus?",
    "related_intro": "Suchen Sie etwas anderes? Sehen Sie sich das komplette Mietangebot an",
    "related": [("wypozyczenie-robota.html", "Roboter mieten"), ("atrakcje-na-event.html", "Alle Attraktionen")],
    "kontakt_h2": "Roboter für Ihre<br />Veranstaltung reservieren.",
    "video": "gesty",
    "guides": "default",
}


def mk(**kw):
    d = dict(DEFAULTS)
    d.update(kw)
    d.setdefault("schema_name", d["crumb"] + " — Unitree G1 mieten")
    d.setdefault("schema_desc", d["desc"].rstrip(" →"))
    d.setdefault("faq_h2", "Häufige<br />Fragen")
    return d


# ── Pule tekstowe ─────────────────────────────────────────────────────
DESCS = [
    "Roboter {na} — die Attraktion, die Ihre Gäste nicht vergessen. Unitree G1: Gästeempfang, Tanzshow, "
    "Gespräche dank KI. Anfahrt und Operator inklusive →",
    "Humanoiden Roboter {na} mieten. Der Unitree G1 begrüßt Gäste, tanzt und spricht dank KI. Deutschlandweit, "
    "Anfahrt und Operator im Preis →",
    "Humanoider Roboter {na}: Tanzchoreografie, Interaktion mit den Gästen und Fotobereich. Unitree G1 mit "
    "zertifiziertem Operator, Anfahrt inklusive →",
]

EYEBROWS = [
    "Roboter mieten · Event-Attraktion · Deutschlandweit",
    "Humanoider Roboter · Unitree G1 · Show mit Operator",
    "Premium-Attraktion · Unitree G1 · Anfahrt inklusive",
]

TILES_H2 = [
    "Die Attraktion, über die<br />noch Jahre gesprochen wird",
    "Warum ein Roboter<br />den Unterschied macht",
    "WOW-Effekt<br />mit Garantie",
]

SCEN_INTROS = [
    "Das Showprogramm passen wir an Agenda und Charakter Ihrer Veranstaltung an. Meist kombinieren wir drei "
    "bewährte Elemente:",
    "Der Roboter muss nicht durchgehend präsent sein — seine Auftritte planen wir für die stärksten Momente "
    "Ihrer Veranstaltung:",
    "Das Drehbuch legen wir gemeinsam vor der Veranstaltung fest. Diese Elemente funktionieren am besten:",
]


def _tile_pool(Loc):
    loc = Loc[0].lower() + Loc[1:]
    return [
        ("WOW-Effekt", "Der Moment, der hängen bleibt",
         f"{Loc} sehen die meisten Gäste zum ersten Mal im Leben einen Humanoiden live. Der Roboter bildet "
         f"innerhalb weniger Minuten eine Menschentraube um sich — ohne Ankündigung und ohne Einladung."),
        ("Viral", "Der Content entsteht von selbst",
         "Jede Interaktion mit dem Roboter endet mit einer Aufnahme. Stories und Clips von Ihrer Veranstaltung "
         "landen im Netz, während sie noch läuft."),
        ("Stressfrei", "Operator und Anfahrt inklusive",
         "Wir kommen, bauen auf und führen die Show von A bis Z durch. Ein zertifizierter Operator behält alles "
         "im Blick — Sie kümmern sich um Ihre Gäste."),
        ("Fotos", "Ein Fotobereich, der nicht leer wird",
         f"Der G1 posiert, gibt High Fives und gestikuliert — {loc} ist die Schlange für ein Foto mit dem Roboter "
         f"der am längsten wirkende Programmpunkt."),
    ]


def _scen_pool(Loc):
    loc = Loc[0].lower() + Loc[1:]
    return [
        ("Begrüßung der Gäste",
         f"Der Roboter steht am Eingang und begrüßt die Ankommenden mit Geste und Stimme — {loc} ist von der "
         f"ersten Minute an spürbar, dass dies keine gewöhnliche Veranstaltung wird."),
        ("Interaktion und Fotobereich",
         "Der G1 geht auf die Gäste zu, gibt High Fives und posiert für Fotos. Um den Roboter herum steht "
         "durchgehend eine Traube von Menschen, die ein gemeinsames Bild wollen."),
        ("Tanzchoreografie",
         "Der Höhepunkt: Der Roboter tanzt eine zur Musik synchronisierte Choreografie. Genau dieser Teil "
         "erzeugt die meisten Aufnahmen und den meisten Applaus."),
    ]


def _extra_faq(slug):
    return _pick([faq_safe(), faq_operator(), faq_transport()], slug)


def ev(slug, crumb, na, Loc, sub, uniq_tile, uniq_scen, faq_uniq,
       video=None, guides="default", related=None, blog=None):
    """slug = slug PL (klucz treści + seed), crumb/na/Loc = niemieckie."""
    loc = Loc[0].lower() + Loc[1:]
    d = mk(
        slug=slug, crumb=crumb,
        title=f"Roboter {na} — humanoiden Roboter mieten | 33bots",
        desc=_pick(DESCS, slug).format(na=na),
        keywords=(f"roboter {na}, roboter mieten {na}, attraktion {na}, humanoider roboter {na}, "
                  f"Unitree G1 {na}"),
        eyebrow=_pick(EYEBROWS, slug),
        h1=f"{crumb} —<br />Unitree G1.",
        sub=sub,
        tiles_h2=_pick(TILES_H2, slug),
        tiles=[uniq_tile] + _pick2(_tile_pool(Loc), slug),
        scen_title=f"Wie überzeugt der Roboter {na}?",
        scen_intro=_pick(SCEN_INTROS, slug),
        scens=[uniq_scen] + _pick2(_scen_pool(Loc), slug),
        faqs=[faq_uniq, faq_price(na), _extra_faq(slug), faq_book(na)],
        faq_h2=f"Fragen zum Roboter<br />{na}",
        kontakt_h2=f"Roboter {na}<br />reservieren.",
        video=video or _pick(["gesty", "taniec", "powitanie", "spacer"], slug),
        guides=guides,
    )
    if blog:
        d["blog_link"] = blog
    if related:
        d["related"] = related
        d["_related_fixed"] = True
    return d


def br(suffix, nom, na, Loc, aud, uniq, faq, guides="default", video=None, blog=None):
    """nom = 'IT-Event', na = 'für IT-Events', Loc = 'Auf einem IT-Event'."""
    slug = "robot-na-event-" + suffix
    crumb = "Roboter " + na
    uniq_tile = ("Branche", "Ein Programm für Ihr Publikum",
                 f"Ein {nom} hat seine eigene Dynamik — und wir kennen sie. Tonfall der Show, Zeitpunkte der "
                 f"Auftritte und die Inhalte, über die der Roboter dank KI spricht, stimmen wir auf Ihre "
                 f"Veranstaltung ab.")
    uniq_scen = ("Die Rolle im Veranstaltungsprogramm",
                 f"Der Roboter kann die Veranstaltung eröffnen, in der Partnerfläche arbeiten oder eine "
                 f"Bühnenshow übernehmen — {Loc[0].lower() + Loc[1:]} funktionieren alle drei Varianten.")
    sub = (f"{uniq} Die Show des humanoiden Roboters Unitree G1 zieht {aud} an — und macht Ihre Veranstaltung "
           f"zum Gesprächsthema der ganzen Branche.")
    return ev(slug, crumb, na, Loc, sub, uniq_tile, uniq_scen, faq,
              video=video, guides=guides, blog=blog)


PRIV_DESCS = [
    "Roboter {na} — die Überraschung, über die die ganze Familie spricht. Der Unitree G1 tanzt, gratuliert und "
    "posiert für Fotos. Operator inklusive →",
    "Humanoiden Roboter {na} mieten. Tanz, Glückwünsche, gemeinsame Fotos — eine Attraktion, die kein Gast "
    "vergisst. Deutschlandweit →",
    "Humanoider Roboter {na}: Tanzshow, Interaktion mit den Gästen und Erinnerungsfotos. Mit zertifiziertem "
    "Operator, Anfahrt inklusive →",
]


def _priv_tile_pool(Loc):
    loc = Loc[0].lower() + Loc[1:]
    return [
        ("Überraschung", "Ein Effekt, mit dem niemand rechnet",
         f"Der Auftritt eines echten Roboters ist eine Überraschung, die keine andere Idee übertrifft — "
         f"{loc} sind die Reaktionen der Gäste unbezahlbar, und die Aufnahmen davon noch besser."),
        ("Erinnerung", "Fotos und Videos für Jahre",
         "Jeder Gast geht mit Material im Handy nach Hause, und Sie mit einer Erinnerung, auf die Sie bei jedem "
         "Familientreffen zurückkommen werden."),
        ("Stressfrei", "Der Operator kümmert sich um alles",
         "Wir kommen, führen die Show durch und achten auf die Sicherheit. Sie feiern — wir sorgen dafür, dass "
         "der Roboter der Star des Abends ist."),
        ("Generationen", "Eine Attraktion für jeden Gast",
         "Von den Kindern bis zu den Großeltern — der Roboter unterhält alle gleichzeitig. Eine der wenigen "
         "Attraktionen, die wirklich Generationen an einem Tisch verbindet."),
    ]


def priv(slug, crumb, na, Loc, sub, uniq_scen, faq_uniq, guides_override=None):
    loc = Loc[0].lower() + Loc[1:]
    d = mk(
        slug=slug, crumb=crumb,
        title=f"{crumb} — humanoiden Roboter mieten | 33bots",
        desc=_pick(PRIV_DESCS, slug).format(na=na),
        keywords=(f"roboter {na}, roboter mieten {na}, attraktion {na}, humanoider roboter {na}, "
                  f"überraschung {na}"),
        eyebrow=_pick(EYEBROWS, slug),
        h1=f"{crumb} —<br />Unitree G1.",
        sub=sub,
        tiles_h2=_pick(TILES_H2, slug),
        tiles=_pick2(_priv_tile_pool(Loc), slug) + [_priv_tile_pool(Loc)[(_seed(slug) + 2) % 4]],
        scen_title=f"Wie überzeugt der Roboter {na}?",
        scen_intro=_pick(SCEN_INTROS, slug),
        scens=[uniq_scen] + _pick2(_scen_pool(Loc), slug),
        faqs=[faq_uniq, faq_price(na), _extra_faq(slug), faq_book(na)],
        faq_h2=f"Fragen zum Roboter<br />{na}",
        kontakt_h2=f"Roboter {na}<br />reservieren.",
        video=_pick(["taniec", "gesty", "powitanie"], slug),
        guides=guides_override or "default",
    )
    return d


def chain_related(pages):
    """Linkowanie wewnętrzne — identyczne jak w serwisie PL."""
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
        p["related_intro"] = "Planen Sie eine andere Veranstaltung? Sehen Sie ähnliche Szenarien"
    return pages
