# -*- coding: utf-8 -*-
"""
Strony ręczne serwisu DE: strona główna, strony ofertowe, case studies,
referencje, hub blogowy i pliki pomocnicze.

Moduł jest wywoływany przez generate_de_site.py i korzysta z jego funkcji
pomocniczych (nawigacja, stopka, formularz, sekcja kontaktowa), więc szata
graficzna i struktura są identyczne jak w serwisie polskim.
"""

from de_slugs import de

G = {}


def _(name):
    return G[name]


# ── Wspólny szkielet podstrony ────────────────────────────────────────
def simple_page(out_file, crumb, title, desc, keywords, eyebrow, h1, sub,
                sections, faqs=None, kontakt_h2="Termin für Ihre<br />Veranstaltung sichern.",
                schema_type="Service", gallery=True):
    import json
    DOMAIN, H3 = _("DOMAIN"), _("H3")
    url = f"{DOMAIN}/{out_file}"
    og_image = f"og/{out_file.replace('.html', '.jpg')}"

    ld = [json.dumps({
        "@context": "https://schema.org", "@type": schema_type,
        "name": title.split(" | ")[0], "description": desc.rstrip(" →"), "url": url,
        "image": f"{DOMAIN}/robot-g1.jpg",
        "provider": {"@type": "Organization", "name": "33bots", "url": f"{DOMAIN}/",
                     "email": _("EMAIL"), "telephone": _("PHONE_HUMAN")},
        "areaServed": {"@type": "Country", "name": "Deutschland"},
    }, ensure_ascii=False, indent=2)]

    ld.append(json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Startseite", "item": f"{DOMAIN}/"},
            {"@type": "ListItem", "position": 2, "name": crumb, "item": url},
        ]}, ensure_ascii=False, indent=2))

    faq_block = ""
    if faqs:
        ld.append(json.dumps({
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": _("strip_tags")(q),
                            "acceptedAnswer": {"@type": "Answer", "text": _("strip_tags")(a)}}
                           for q, a in faqs]}, ensure_ascii=False, indent=2))
        faq_block = f"""  <section class="section faq-section">
    <div class="section-header">
      <span class="tag">FAQ</span>
      <h2 class="section-title">Häufige<br />Fragen</h2>
    </div>
    <div class="faq">
{_("render_faq")(faqs)}
    </div>
  </section>
"""

    ld_html = "\n".join(f'  <script type="application/ld+json">\n{j}\n  </script>\n' for j in ld)

    gallery_block = ""
    if gallery:
        gallery_block = f"""  <section class="section" style="padding-top:0;">
    <div class="shots-wrap">
      <p style="font-size:0.75rem; color:var(--text-3); text-transform:uppercase; letter-spacing:0.1em; font-weight:700; margin-bottom:var(--s3);">Aus echten Einsätzen</p>
      <div class="shots shots--strip">
{_("gallery_items")(8)}
      </div>
      <div class="shots__more">
        <a href="{de('realizacje-wideo.html')}" class="btn-ghost" style="display:inline-flex;">Alle Referenzen ansehen →</a>
      </div>
    </div>
  </section>
"""

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
{_("gtm_head")()}
{_("head_common")(title, desc, keywords, out_file, og_image, crumb)}

{ld_html}
{_("head_assets")(_("HERO_STYLE"))}
</head>
<body>
{_("gtm_body")()}

{_("nav_html")()}
{_("crumbs")(crumb)}
{_("mobile_menu")()}
  <section class="hero">
    <div class="hero__content">
      <p class="hero__eyebrow">{eyebrow}</p>
      <h1 class="hero__title">{h1}</h1>
      <p class="hero__sub">{sub}</p>
      <div class="hero__ctas">
        <a href="#kontakt" class="btn-primary">Termin anfragen</a>
        <a href="index.html#preise" class="btn-ghost">Preise ansehen ↓</a>
      </div>
      <div class="hero__trust">
        <span class="hero__trust-item">✓ Anfahrt inklusive</span>
        <span class="hero__trust-item">✓ Operator inklusive</span>
        <span class="hero__trust-item">✓ Branding ohne Aufpreis</span>
        <span class="hero__trust-item">✓ Keine Anzahlung</span>
      </div>
    </div>
  </section>

{sections}
{gallery_block}
  <section class="section" style="padding-block:var(--s6) var(--s4); background:var(--surface-1)">
    <div class="container" style="max-width:1140px; margin-inline:auto; padding-inline:var(--s4)">
      <h2 style="font-size:clamp(1rem,2vw,1.4rem); font-weight:700; margin-bottom:var(--s3); color:var(--text-1)">Roboter mieten in Ihrer Stadt</h2>
      <div style="display:flex; flex-wrap:wrap; gap:0.5rem;">
{_("render_city_chips")()}
      </div>
    </div>
  </section>

{faq_block}
{_("contact_section")(kontakt_h2, date_text=True)}
{_("footer_html")()}"""


def tiles_section(tag, h2, tiles):
    return f"""  <section class="section tiles-section">
    <div class="section-header">
      <span class="tag">{tag}</span>
      <h2 class="section-title">{h2}</h2>
    </div>
    <div class="tiles">
{_("render_tiles")(tiles)}
    </div>
  </section>
"""


def text_section(h2, lead, paragraphs, subheads=(), cta=True):
    H3 = _("H3")
    body = "\n".join(f'        <p class="body-text">{p}</p>' for p in paragraphs)
    subs = "".join(f'\n        <h3 {H3}>{h}</h3>\n        <p class="body-text">{t}</p>' for h, t in subheads)
    cta_html = ('\n        <a href="#kontakt" class="btn-primary" style="margin-top:var(--s5); '
                'display:inline-flex;">Angebot anfordern →</a>') if cta else ""
    return f"""  <section class="section">
    <div class="onas-body" style="max-width:860px; margin:0 auto;">
      <div class="onas-text">
        <h2 class="section-title" style="font-size:clamp(1.8rem,3vw,2.8rem); margin-bottom:var(--s4);">{h2}</h2>
        <p class="lead-text">{lead}</p>
{body}{subs}{cta_html}
      </div>
    </div>
  </section>
"""


def video_section(key, copy):
    v = _("VIDEOS")[key]
    return f"""  <section class="section" id="video" style="padding-top:0;">
    <div style="display:flex; flex-wrap:wrap; gap:var(--s6); align-items:center; justify-content:center; max-width:900px; margin:0 auto;">
      <video controls muted playsinline preload="none" poster="{v['poster']}" width="300" height="533"
             style="width:min(300px,80vw); border-radius:16px; border:1px solid var(--border-mid); background:var(--surface-2);"
             aria-label="{v['name']}">
        <source src="{v['file']}" type="video/mp4" />
        Ihr Browser unterstützt kein HTML5-Video.
      </video>
      <div style="max-width:400px; display:flex; flex-direction:column; gap:var(--s4); text-align:left;">
        <p style="color:var(--text-2); font-size:1rem; line-height:1.8; margin:0;">{copy}</p>
        <a href="#kontakt" class="btn-primary" style="display:inline-flex; align-self:flex-start;">Show reservieren →</a>
      </div>
    </div>
  </section>
"""


# ── Strona główna ─────────────────────────────────────────────────────
def build_index():
    import json
    DOMAIN = _("DOMAIN")
    EMAIL, PHONE_RAW, PHONE_HUMAN = _("EMAIL"), _("PHONE_RAW"), _("PHONE_HUMAN")
    PHONE2_RAW, PHONE2_HUMAN = _("PHONE2_RAW"), _("PHONE2_HUMAN")
    PRICE_RANGE, PRICE_LOW, PRICE_HIGH = _("PRICE_RANGE"), _("PRICE_LOW"), _("PRICE_HIGH")
    DOG_PRICE = _("DOG_PRICE")
    cities = _("de_cities").CITIES

    title = "Humanoide Roboter für Events mieten — deutschlandweit | 33bots"
    desc = (f"Humanoiden Roboter Unitree G1 für Event, Messe und Konferenz mieten. Ganzer Tag ab "
            f"{PRICE_LOW.replace('1290', '1.290')} € — Anfahrt, Operator und Branding inklusive, keine Anzahlung, "
            f"Rechnung nach dem Event. Angebot in 24 h.")
    kw = ("humanoide roboter mieten, roboter mieten event, roboter für messe mieten, Unitree G1 mieten, "
          "roboter konferenz, event attraktion roboter, humanoider roboter Deutschland")

    faqs = [
        ("Was kostet die Miete eines humanoiden Roboters für ein Event?",
         f"Ein kompletter Veranstaltungstag kostet {PRICE_RANGE} — der endgültige Preis hängt ausschließlich vom "
         f"Veranstaltungsort ab. Im Preis ist alles enthalten: deutschlandweite Anfahrt, zertifizierter Operator, "
         f"Branding des Roboters und Versicherung. Optional buchen Sie den Roboterhund für {DOG_PRICE} pro Tag; "
         f"ab zwei Veranstaltungstagen erhalten Sie 15 % Rabatt auf jeden Tag."),
        ("Muss ich eine Anzahlung leisten, um einen Termin zu reservieren?",
         "Nein. Die Terminreservierung ist vollständig kostenlos — wir schließen einen einfachen Vertrag ohne "
         "Anzahlung und stellen die Rechnung erst nach der Veranstaltung. Bei Bedarf vereinbaren wir ein längeres "
         "Zahlungsziel."),
        ("Muss ich den Roboter selbst bedienen können?",
         "Nein. Ein zertifizierter Operator von 33bots ist den gesamten Veranstaltungstag vor Ort, übernimmt Aufbau, "
         "Konfiguration und Steuerung. Sie brauchen keinerlei technisches Vorwissen."),
        ("Kann der Roboter auch bei einem Tag der offenen Tür oder Betriebsfest eingesetzt werden?",
         "Selbstverständlich. Die Unitree-Roboter kommen mit unterschiedlichen Untergründen zurecht (Asphalt, Rasen, "
         "Teppich) und funktionieren daher sowohl im Bürogebäude als auch bei Outdoor-Veranstaltungen."),
        ("Kann ich mein Firmenlogo auf dem Roboter platzieren?",
         "Ja — und zwar kostenlos. Ihr Logo und ein QR-Code kommen auf die Brustplatte des Roboters. Bei uns ist das "
         "Branding Teil des Standardpakets und wird nicht extra berechnet."),
        ("Ist der Roboter für die Teilnehmenden sicher?",
         "Ja. Der Roboter verfügt über LiDAR und Computer Vision und weicht Hindernissen sowie Menschen in Echtzeit "
         "aus. Zusätzlich überwacht unser Operator den Einsatz durchgehend. Eine Haftpflichtversicherung ist inklusive."),
        ("Welche technischen Voraussetzungen brauchen Sie vor Ort?",
         "Eine gewöhnliche 230-V-Steckdose und rund 2×2 m freie Fläche. Internet oder besondere Beleuchtung sind "
         "nicht erforderlich. Unser Operator bringt die komplette Ausrüstung mit und ist in 30–45 Minuten "
         "einsatzbereit."),
        ("Kann der Roboter tanzen?",
         "Und wie. Der Unitree G1 beherrscht mehrere Choreografien, die auch ein professioneller Tänzer nicht "
         "verstecken müsste. Wenn bei Ihrer Veranstaltung ein DJ auflegt, übernimmt unser Roboter gerne die Tanzfläche."),
        ("Ist die Vermietung deutschlandweit verfügbar?",
         "Ja — 33bots ist in ganz Deutschland im Einsatz, mit kostenloser Anfahrt unabhängig von Stadt und "
         "Entfernung. Wir bedienen Berlin, München, Hamburg, Köln, Frankfurt, Stuttgart, Düsseldorf und Dutzende "
         "weitere Städte."),
        ("Welche Unternehmen haben bereits einen Roboter bei Ihnen gemietet?",
         "Unter anderem die Perspektywy Foundation (Women in Tech Summit — die größte Women-in-Tech-Konferenz "
         "Europas), der globale Logistikkonzern DSV, Cashify sowie LEX AI, dessen Show mit unserem Roboter im "
         "öffentlich-rechtlichen Fernsehen ausgestrahlt wurde."),
        ("Was unterscheidet 33bots von anderen Roboter-Vermietungen?",
         "Im Preis ist immer das Komplettpaket enthalten: Anfahrt ohne Kilometerbegrenzung, ein zertifizierter "
         "Operator für die gesamte Veranstaltung und kostenloses Branding des Roboters (Logo und QR-Code). Wir "
         "berechnen weder Anfahrt noch Zusatzoptionen nach."),
    ]

    ld = []
    ld.append(json.dumps({
        "@context": "https://schema.org", "@type": "Product",
        "name": "Miete eines humanoiden Roboters Unitree G1",
        "description": "Vermietung humanoider Roboter Unitree G1 für Events, Konferenzen und Messen in ganz Deutschland.",
        "url": DOMAIN, "image": f"{DOMAIN}/robot-g1.jpg",
        "brand": {"@type": "Brand", "name": "Unitree"},
        "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR", "lowPrice": PRICE_LOW,
                   "highPrice": PRICE_HIGH, "availability": "https://schema.org/InStock",
                   "url": f"{DOMAIN}/#preise",
                   "description": "Kompletter Veranstaltungstag inklusive Anfahrt, Operator und Branding. "
                                  "Keine Zusatzkosten, keine Anzahlung, Rechnung nach dem Event."},
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "3",
                            "bestRating": "5", "worstRating": "1"},
    }, ensure_ascii=False, indent=2))

    ld.append(json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": _("strip_tags")(q),
                        "acceptedAnswer": {"@type": "Answer", "text": _("strip_tags")(a)}} for q, a in faqs],
    }, ensure_ascii=False, indent=2))

    ld.append(json.dumps({
        "@context": "https://schema.org", "@type": "ProfessionalService",
        "name": "33bots – Humanoide Roboter für Events und Messen mieten", "alternateName": "33bots",
        "url": DOMAIN, "logo": f"{DOMAIN}/logo.png", "image": f"{DOMAIN}/robot-g1.jpg",
        "description": "Vermietung humanoider Roboter Unitree G1 für Events, Konferenzen und Messen in ganz "
                       "Deutschland. Anfahrt und zertifizierter Operator inklusive.",
        "telephone": PHONE_RAW, "email": EMAIL,
        "areaServed": {"@type": "Country", "name": "Deutschland"},
        "sameAs": ["https://www.facebook.com/33bots", "https://www.instagram.com/33bots_/",
                   "https://www.linkedin.com/company/33bots", "https://www.tiktok.com/@aimforum"],
        "contactPoint": {"@type": "ContactPoint", "telephone": PHONE_RAW, "email": EMAIL,
                         "contactType": "sales", "areaServed": "DE",
                         "availableLanguage": ["German", "English", "Polish"]},
        "knowsAbout": ["humanoiden Roboter mieten", "Roboter für Events", "Roboter für Messen",
                       "Roboter für Konferenzen", "Unitree G1", "Event-Attraktionen"],
        "priceRange": f"{PRICE_LOW}-{PRICE_HIGH} EUR",
    }, ensure_ascii=False, indent=2))

    ld.append(json.dumps({
        "@context": "https://schema.org", "@type": "WebSite", "name": "33bots",
        "alternateName": "33bots — humanoide Roboter mieten", "url": f"{DOMAIN}/", "inLanguage": "de-DE",
        "description": "Humanoide Roboter Unitree G1 für Events, Messen und Konferenzen in ganz Deutschland mieten.",
        "publisher": {"@type": "Organization", "name": "33bots", "url": f"{DOMAIN}/",
                      "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/logo.png"}},
    }, ensure_ascii=False, indent=2))

    ld_html = "\n".join(f'  <script type="application/ld+json">\n{j}\n  </script>\n' for j in ld)

    city_chips = "\n".join(
        f'        <a href="{de(f)}" class="tile__link" style="padding:8px 16px; background:var(--surface-2); '
        f'border:1px solid var(--border-mid); border-radius:8px;">{d["name"]}</a>'
        for f, d in cities.items())
    coverage = "\n".join(f'            <li><a href="{de(f)}">{d["name"]}</a></li>' for f, d in cities.items())

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
{_("gtm_head")()}
{_("head_common")(title, desc, kw, "index.html", "og-image.jpg", "Humanoider Roboter Unitree G1 — Miete für Events in Deutschland")}

{ld_html}
  <link rel="preload" as="image" href="robot-g1-960.webp" imagesrcset="robot-g1-960.webp 960w, robot-g1.webp 2390w" imagesizes="45vw" fetchpriority="high" type="image/webp" media="(min-width: 769px)" />
  <link rel="alternate" type="application/rss+xml" title="33bots — Blog RSS" href="{DOMAIN}/feed.xml" />
{_("head_assets")()}
</head>
<body>
{_("gtm_body")()}

{_("nav_html")("")}
{_("mobile_menu")("")}
  <!-- HERO -->
  <section class="hero">
    <div class="hero__content">
      <p class="hero__eyebrow">Humanoide Roboter mieten · Deutschlandweit · Bestpreis</p>
      <h1 class="hero__title">Humanoide Roboter<br />mieten —<br /><em>Unitree G1.</em></h1>
      <p class="hero__sub">Der Roboter, der Menschenmengen stoppt und Ihre Veranstaltung wochenlang zum Gesprächsthema macht. Ein kompletter Showtag mit Anfahrt, Operator und Branding im Preis — <strong>ohne Anzahlung und ohne versteckte Kosten</strong>.</p>
      <div class="hero__ctas">
        <a href="#kontakt" class="btn-cta">Kostenloses Angebot anfordern →</a>
        <a href="#preise" class="btn-cta--ghost">Preise ansehen ↓</a>
      </div>
      <p class="hero__cta-note">Angebot in 24 h · Keine Anzahlung · Rechnung erst nach dem Event</p>
      <div class="hero__trust">
        <span class="hero__trust-item">✓ Bester Preis am Markt</span>
        <span class="hero__trust-item">✓ Anfahrt inklusive</span>
        <span class="hero__trust-item">✓ Operator inklusive</span>
        <span class="hero__trust-item">✓ Branding ohne Aufpreis</span>
      </div>
    </div>
    <div class="hero__visual">
      <div class="hero__spotlight" aria-hidden="true"></div>
      <div class="hero__robot-wrap" id="robotWrap">
      <div class="hero__robot">
        <div class="robot-scan" aria-hidden="true"></div>
        <picture>
          <source srcset="robot-g1-960.webp 960w, robot-g1.webp 2390w" sizes="(min-width: 769px) 45vw, 1px" type="image/webp" />
          <img src="robot-g1.jpg" alt="Humanoider Roboter Unitree G1 — Attraktion für Events, Messen und Konferenzen in Deutschland" class="hero__robot-img" width="600" height="800" loading="eager" fetchpriority="high" />
        </picture>
      </div>
      </div>
      <div class="hero__tag hero__tag--1">Unitree G1</div>
      <div class="hero__tag hero__tag--2">23 DOF</div>
      <div class="hero__tag hero__tag--3">~132 cm</div>
    </div>
  </section>

  <!-- STATS -->
  <div class="stats-bar">
    <div class="stats-bar__inner">
      <div class="stat-item"><span class="stat-item__val" data-count="35" data-suffix="+">0</span><span class="stat-item__lbl">Städte in Deutschland</span></div>
      <div class="stat-item__div" aria-hidden="true"></div>
      <div class="stat-item"><span class="stat-item__val" data-count="5" data-suffix=".0 ★">0</span><span class="stat-item__lbl">Kundenbewertung</span></div>
      <div class="stat-item__div" aria-hidden="true"></div>
      <div class="stat-item"><span class="stat-item__val" data-count="24" data-suffix="h">0</span><span class="stat-item__lbl">bis zum Angebot</span></div>
      <div class="stat-item__div" aria-hidden="true"></div>
      <div class="stat-item"><span class="stat-item__val" data-count="0" data-suffix=" €">0</span><span class="stat-item__lbl">Anfahrt</span></div>
    </div>
  </div>

{_("gallery_section")(lead="Keine Renderings, keine Studioaufnahmen: Galas, Summits, Straßenaktionen, Outdoor-Events und Nachtshows — Bilder aus Veranstaltungen, die wir tatsächlich betreut haben.")}
  <!-- VERTRAUEN UNS -->
  <section class="section" id="referenzen" style="padding-top:var(--s8); padding-bottom:var(--s8);">
    <div style="max-width:1000px; margin:0 auto; text-align:center;">
      <h2 style="font-size:0.75rem; font-weight:700; letter-spacing:0.14em; text-transform:uppercase; color:var(--text-3); margin-bottom:var(--s5);">Vertrauen uns</h2>
      <div style="display:flex; flex-wrap:wrap; align-items:stretch; justify-content:center; gap:var(--s4);">
        <a href="{de('case-study-women-in-tech.html')}" style="display:flex; flex-direction:column; gap:4px; padding:var(--s4) var(--s6); background:var(--surface-2); border:1px solid var(--border-mid); border-radius:12px; text-decoration:none; min-width:220px; text-align:left;">
          <span style="font-size:0.7rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:var(--text-3);">Bildung · Women in Tech Summit</span>
          <span style="font-size:1.05rem; font-weight:700; color:var(--text);">Perspektywy Foundation →</span>
        </a>
        <div style="display:flex; flex-direction:column; gap:4px; padding:var(--s4) var(--s6); background:var(--surface-2); border:1px solid var(--border-mid); border-radius:12px; min-width:220px; text-align:left;">
          <span style="font-size:0.7rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:var(--text-3);">Transport &amp; Logistik</span>
          <span style="font-size:1.05rem; font-weight:700; color:var(--text);">DSV</span>
        </div>
        <div style="display:flex; flex-direction:column; gap:4px; padding:var(--s4) var(--s6); background:var(--surface-2); border:1px solid var(--border-mid); border-radius:12px; min-width:220px; text-align:left;">
          <span style="font-size:0.7rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:var(--text-3);">Technologie · Fintech</span>
          <span style="font-size:1.05rem; font-weight:700; color:var(--text);">Cashify</span>
        </div>
        <a href="{de('case-study-lexai.html')}" style="display:flex; flex-direction:column; gap:4px; padding:var(--s4) var(--s6); background:var(--surface-2); border:1px solid var(--border-mid); border-radius:12px; text-decoration:none; min-width:220px; text-align:left;">
          <span style="font-size:0.7rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:var(--text-3);">Legal Tech · TV-Beitrag</span>
          <span style="font-size:1.05rem; font-weight:700; color:var(--text);">LEX AI →</span>
        </a>
      </div>
      <p style="margin-top:var(--s5); color:var(--text-2); font-size:0.95rem; max-width:680px; margin-left:auto; margin-right:auto; line-height:1.7;">Unsere humanoiden Roboter waren unter anderem im Einsatz für die <strong style="color:var(--text);">Perspektywy Foundation</strong> (Veranstalter des Women in Tech Summit — der größten Women-in-Tech-Konferenz Europas), den globalen Logistikkonzern <strong style="color:var(--text);">DSV</strong>, <strong style="color:var(--text);">Cashify</strong> sowie <strong style="color:var(--text);">LEX AI</strong>.</p>
      <div style="display:flex; gap:var(--s5); justify-content:center; flex-wrap:wrap; margin-top:var(--s4);">
        <a href="{de('case-study-lexai.html')}" style="display:inline-flex; color:var(--text); font-size:0.9rem; font-weight:600; text-decoration:underline; text-underline-offset:3px;">Case Study LEX AI →</a>
        <a href="{de('case-study-wallstreet.html')}" style="display:inline-flex; color:var(--text); font-size:0.9rem; font-weight:600; text-decoration:underline; text-underline-offset:3px;">Case Study WallStreet 30 →</a>
        <a href="{de('realizacje-wideo.html')}" style="display:inline-flex; color:var(--text); font-size:0.9rem; font-weight:600; text-decoration:underline; text-underline-offset:3px;">Alle Referenzvideos →</a>
      </div>
    </div>
  </section>

  <!-- LEISTUNGEN -->
  <section class="section tiles-section" id="leistungen">
    <div class="section-header">
      <span class="tag">Leistungen</span>
      <h2 class="section-title">Was wir für Sie<br />übernehmen</h2>
    </div>
    <div class="tiles">
      <div class="tile">
        <div class="tile__top">
          <svg class="tile__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
          <span class="tile__tag">Der Star Ihres Events</span>
        </div>
        <h3 class="tile__title">Roboter<br />für Events</h3>
        <p class="tile__desc">Sie wollen, dass über Ihre Veranstaltung gesprochen wird? Der G1 kommt zu Ihrer Konferenz, Eröffnung oder Gala — und sorgt garantiert für Andrang. <a href="{de('robot-na-impreze.html')}" style="color:inherit; text-decoration:underline;">Roboter für Ihre Feier →</a></p>
        <a href="#kontakt" class="tile__link">Mehr erfahren →</a>
      </div>
      <div class="tile tile--light">
        <div class="tile__top">
          <svg class="tile__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
          <span class="tile__tag">Unsere Flotte</span>
        </div>
        <h3 class="tile__title">Roboter<br />mieten</h3>
        <p class="tile__desc">Wir verfügen über eine eigene Flotte von Unitree-G1-Robotern — für Messen, Logistik, Retail und Markenauftritte. Eigene Technik, keine Zwischenhändler.</p>
        <a href="#kontakt" class="tile__link">Mehr erfahren →</a>
      </div>
      <div class="tile">
        <div class="tile__top">
          <svg class="tile__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>
          <span class="tile__tag">Reichweite, die man nicht kauft</span>
        </div>
        <h3 class="tile__title">Social-Media-<br />Reichweite</h3>
        <p class="tile__desc">Ein Unitree-Roboter erzeugt mehr organische Reichweite als so mancher Top-Influencer — aus jedem einzelnen Gästehandy heraus.</p>
        <a href="#kontakt" class="tile__link">Mehr erfahren →</a>
      </div>
    </div>
  </section>

  <!-- ÜBER UNS -->
  <section class="section onas-section" id="ueber-uns">
    <div class="onas-head">
      <span class="tag">Über uns</span>
      <h2 class="section-title">Spezialisten für<br />Event-Robotik</h2>
    </div>
    <div class="onas-body">
      <div class="onas-text">
        <p class="lead-text">33bots ist auf die <a href="{de('wypozyczenie-robota.html')}" style="color:var(--text); text-decoration:underline; text-underline-offset:3px;">Vermietung humanoider Roboter Unitree G1</a> für Events, Messen und Technologie-Shows spezialisiert. Das ist unser einziges Geschäft — wir sind keine Agentur, die alles ein bisschen macht.</p>
        <p class="body-text">Die Miete eines humanoiden Roboters bei 33bots bedeutet immer Rundum-Betreuung: Wir bringen den Roboter zu Ihnen, stellen einen Operator für die gesamte Veranstaltungsdauer und kümmern uns um alles — vom Aufbau bis zur finalen Show. Wir sind in Berlin, München, Hamburg, Köln, Frankfurt, Stuttgart, Düsseldorf und in jeder weiteren deutschen Stadt im Einsatz.</p>
        <p class="body-text">Sehen Sie sich unsere spezialisierten Angebote an: <a href="{de('oferta-targi.html')}" style="color:var(--text); text-decoration:underline; text-underline-offset:3px;">Roboter für Messen und Ausstellungen</a> sowie <a href="{de('oferta-konferencje.html')}" style="color:var(--text); text-decoration:underline; text-underline-offset:3px;">Roboter für Konferenzen und Galas</a>.</p>
      </div>
      <ul class="onas-usps">
        <li>Eigene Technik — keine Zwischenhändler, keine Überraschungen</li>
        <li>Dedizierter Operator für die gesamte Veranstaltungsdauer</li>
        <li>Vollständiger Haftpflichtschutz — Sicherheit auf beiden Seiten</li>
        <li>Einsätze in jeder deutschen Stadt</li>
        <li>Bester Preis für die Miete eines humanoiden Roboters am Markt</li>
      </ul>
    </div>

    <div class="transport-callout">
      <div class="transport-callout__glow" aria-hidden="true"></div>
      <div class="transport-callout__left">
        <span class="transport-callout__eyebrow">Bei uns Standard</span>
        <p class="transport-callout__claim"><em>Anfahrt inklusive</em><br />in ganz<br />Deutschland.</p>
      </div>
      <div class="transport-callout__right">
        <p class="transport-callout__note">Keine Kilometerpauschale, keine Mindestentfernung, keine versteckten Kosten. Wir bringen den Roboter zu jeder Veranstaltung — von Hamburg bis München, von Köln bis Dresden — und berechnen dafür keinen Cent extra.</p>
        <ul class="transport-callout__stats">
          <li><strong>0 €</strong><span>pro Kilometer</span></li>
          <li><strong>100 %</strong><span>Deutschland abgedeckt</span></li>
          <li><strong>24 h</strong><span>bis zum Angebot</span></li>
        </ul>
        <a href="#kontakt" class="btn-primary">Termin mit Anfahrt sichern →</a>
      </div>
    </div>
  </section>

  <!-- GALERIE -->
  <section class="section robot-gallery-section">
    <div class="section-header">
      <span class="tag">Roboter</span>
      <h2 class="section-title">Unitree G1 —<br />Humanoid neuer Generation</h2>
    </div>
    <div class="robot-gallery">
      <figure class="robot-gallery__main">
        <picture><source srcset="robot-g1-960.webp 960w, robot-g1.webp 2390w" sizes="(min-width: 769px) 800px, 92vw" type="image/webp" />
          <img src="robot-g1.jpg" alt="Humanoider Roboter Unitree G1 — silberner Humanoid mit blauem Visier" width="800" height="800" loading="lazy" /></picture>
        <figcaption>Unitree G1 · 132 cm · 35 kg · 23 Freiheitsgrade</figcaption>
      </figure>
      <div class="robot-gallery__side">
        <figure class="robot-gallery__action">
          <picture><source srcset="robot-g1-action.webp" type="image/webp" />
            <img src="robot-g1-action.jpg" alt="Unitree G1 in einer Tanzchoreografie — Aufnahme von einer echten 33bots-Show" width="600" height="600" loading="lazy" /></picture>
          <figcaption>Dynamische Choreografien und Live-Shows</figcaption>
        </figure>
        <div class="robot-gallery__specs">
          <div class="robot-spec"><span class="robot-spec__val">132 cm</span><span class="robot-spec__lbl">Größe</span></div>
          <div class="robot-spec"><span class="robot-spec__val">35 kg</span><span class="robot-spec__lbl">Gewicht</span></div>
          <div class="robot-spec"><span class="robot-spec__val">23</span><span class="robot-spec__lbl">DOF</span></div>
          <div class="robot-spec"><span class="robot-spec__val">2 m/s</span><span class="robot-spec__lbl">Geschwindigkeit</span></div>
        </div>
      </div>
    </div>
  </section>

  <!-- VIDEO -->
  <section class="section" id="video">
    <div class="section-header">
      <span class="tag">Video</span>
      <h2 class="section-title">Der Roboter<br />im Einsatz</h2>
    </div>
    <div style="display:flex; flex-wrap:wrap; gap:var(--s6); align-items:center; justify-content:center; max-width:1000px; margin:0 auto;">
      <video controls muted playsinline preload="none" poster="video/33bots-robot-event-poster.jpg" width="360" height="640"
             style="width:min(360px,90vw); border-radius:16px; border:1px solid var(--border-mid); background:var(--surface-2);"
             aria-label="Humanoider Roboter Unitree G1 im Einsatz">
        <source src="video/33bots-robot-event.mp4" type="video/mp4" />
        Ihr Browser unterstützt kein HTML5-Video.
      </video>
      <div style="max-width:420px; display:flex; flex-direction:column; gap:var(--s4); text-align:left;">
        <p style="color:var(--text-2); font-size:1rem; line-height:1.8; margin:0;">So sieht der <strong style="color:var(--text);">Unitree G1</strong> live aus: Er läuft, gestikuliert, begrüßt Gäste und tanzt. Auf der Brustplatte sehen Sie unseren Standard — <strong style="color:var(--text);">kostenloses Branding</strong> mit Logo und QR-Code Ihrer Marke.</p>
        <a href="{de('realizacje-wideo.html')}" style="display:inline-flex; align-items:center; gap:8px; color:var(--text); font-size:0.9rem; font-weight:600; text-decoration:underline; text-underline-offset:3px;">Mehr Aufnahmen aus Einsätzen →</a>
        <a href="#kontakt" class="btn-primary" style="display:inline-flex; align-self:flex-start;">Show reservieren →</a>
      </div>
    </div>
  </section>

  <!-- STATEMENT -->
  <div class="statement">
    <div class="statement__inner">
      <blockquote class="statement__quote">„Wenn der Roboter den Saal betritt —<br />zücken alle ihr Handy."</blockquote>
      <p class="statement__sub">Das ist keine Metapher, sondern der Bericht von jeder Veranstaltung, die wir betreut haben.</p>
      <a href="#kontakt" class="btn-cta">Termin auf Verfügbarkeit prüfen →</a>
    </div>
  </div>

  <!-- PREISE -->
  <span id="events" aria-hidden="true"></span>
  <section class="section pricing-section" id="preise">
    <div class="section-header">
      <span class="tag">Preise</span>
      <h2 class="section-title">Ein Preis.<br />Alles inklusive.</h2>
      <p class="pricing-lead">Ein transparenter Tagessatz und alles ist enthalten. Keine Sternchen, keine Aufschläge, keine „Zusatzkosten“, die in der letzten Mail auftauchen.</p>
    </div>
    <div class="pricing-grid">
      <article class="price-card price-card--main">
        <span class="price-card__badge">Komplettpaket — alles inklusive</span>
        <h3 class="price-card__name">Humanoider Roboter Unitree G1</h3>
        <p class="price-card__for">Der Star Ihrer Veranstaltung — Messe, Konferenz, Gala oder Eröffnung. Den ganzen Tag.</p>
        <div class="price-card__price">
          <span class="price-card__amount">{PRICE_RANGE}</span>
          <span class="price-card__period">pro Veranstaltungstag</span>
        </div>
        <p class="price-card__note">Der endgültige Preis hängt ausschließlich vom Veranstaltungsort ab. Wir nennen den Betrag sofort — und genau dieser Betrag steht später auf der Rechnung.</p>
        <ul class="price-card__list">
          <li>Roboter-Show über den gesamten Veranstaltungstag</li>
          <li>Zertifizierter Operator von Anfang bis Ende</li>
          <li>Anfahrt deutschlandweit inklusive — ohne Kilometerlimit</li>
          <li>Kostenloses Branding: Ihr Logo und QR-Code auf dem Roboter</li>
          <li>Choreografien, Interaktion mit Gästen und Tanz-Shows</li>
          <li>Haftpflichtversicherung und technische Betreuung vor Ort</li>
        </ul>
        <p class="price-card__zero">Der Preis enthält absolut alles. <strong>KEINE Zusatzkosten.</strong></p>
        <a href="#kontakt" class="btn-cta">Kostenloses Angebot anfordern →</a>
      </article>
      <aside class="price-card price-card--addon">
        <span class="price-card__badge price-card__badge--addon">Zusatzoption</span>
        <h3 class="price-card__name">Roboterhund</h3>
        <p class="price-card__for">Das perfekte Duo: Der Humanoid macht die Show, der Roboterhund erobert die Herzen der Gäste.</p>
        <div class="price-card__price">
          <span class="price-card__amount">{DOG_PRICE}</span>
          <span class="price-card__period">pro Veranstaltungstag</span>
        </div>
        <ul class="price-card__list">
          <li>Dynamische Shows, Tricks und Interaktionen</li>
          <li>Magnet für Fotos und Videos der Gäste</li>
          <li>Operator im Preis enthalten</li>
        </ul>
        <a href="#kontakt" class="tile__link">Zum Angebot hinzufügen →</a>
      </aside>
    </div>
    <div class="pricing-promo">
      <span class="pricing-promo__badge">Aktion</span>
      <p class="pricing-promo__text"><strong>−15 % auf jeden Tag</strong> ab zwei Veranstaltungstagen. Messen, Festivals, Roadshows — je länger der Roboter bleibt, desto weniger zahlen Sie pro Tag.</p>
      <a href="#kontakt" class="btn-primary">Angebot für Ihren Termin anfragen →</a>
    </div>
  </section>

{_("TESTIMONIALS")}
  <!-- EINSATZBEREICHE -->
  <section class="section" id="einsatzbereiche">
    <div class="section-header">
      <span class="tag">Einsatzbereiche</span>
      <h2 class="section-title">Wo der G1<br />überzeugt</h2>
    </div>
    <div class="use-grid">
      <div class="use-item"><span class="use-num">01</span><h3>Konferenzen &amp; Summits</h3><p>Der Roboter als Gastgeber, Guide oder Attraktion am Registration Desk.</p><a href="{de('oferta-konferencje.html')}" class="tile__link" style="margin-top:var(--s2);display:inline-flex;">Konferenz-Angebot →</a></div>
      <div class="use-item"><span class="use-num">02</span><h3>Messen &amp; Ausstellungen</h3><p>Ziehen Sie zehnmal mehr Aufmerksamkeit an den Stand als mit jedem Banner.</p><a href="{de('oferta-targi.html')}" class="tile__link" style="margin-top:var(--s2);display:inline-flex;">Mehr erfahren →</a></div>
      <div class="use-item"><span class="use-num">03</span><h3>Firmenfeiern &amp; Hochzeiten</h3><p>Sommerfeste, Jubiläen, Galas, Hochzeiten — Gesprächsstoff weit über den Abend hinaus.</p><a href="{de('robot-na-wesele.html')}" class="tile__link" style="margin-top:var(--s2);display:inline-flex;">Roboter zur Hochzeit →</a></div>
      <div class="use-item"><span class="use-num">04</span><h3>Tage der offenen Tür &amp; Bildung</h3><p>Schulen, Hochschulen, Science Center — Technologie, die die Welt verändert.</p><a href="{de('oferta-dni-otwarte.html')}" class="tile__link" style="margin-top:var(--s2);display:inline-flex;">Mehr erfahren →</a></div>
      <div class="use-item"><span class="use-num">05</span><h3>Foto- &amp; Videoproduktion</h3><p>Werbematerial mit einem Humanoiden. Aufmerksamkeit garantiert.</p></div>
      <div class="use-item"><span class="use-num">06</span><h3>Produktlaunch</h3><p>Store-Eröffnung oder Imagekampagne — der G1 macht die Show.</p></div>
    </div>
  </section>

  <!-- ABLAUF -->
  <section class="section process-section" id="ablauf">
    <div class="section-header">
      <span class="tag">So arbeiten wir</span>
      <h2 class="section-title">Zusammenarbeit ohne Stress<br />und ohne Anzahlung</h2>
      <p class="process-lead">Sie reservieren den Termin kostenlos und erhalten die Rechnung erst nach der erfolgreichen Veranstaltung. Das Risiko tragen wir — Sie wählen nur das Datum.</p>
    </div>
    <div class="process">
      <div class="process-step"><span class="process-step__n">01</span><div><h3>Schneller Kontakt</h3><p>Sie füllen ein kurzes Formular aus oder schreiben eine E-Mail. Das dauert zwei Minuten.</p></div></div>
      <div class="process-step"><span class="process-step__n">02</span><div><h3>Rückruf von uns</h3><p>Wir rufen zurück, lernen Ihre Veranstaltung kennen und empfehlen das passende Showformat.</p></div></div>
      <div class="process-step"><span class="process-step__n">03</span><div><h3>Angebot in 24 Stunden</h3><p>Ein konkreter Betrag ohne Sternchen — meist noch am selben Tag.</p></div></div>
      <div class="process-step process-step--key"><span class="process-step__n">04</span><div><h3>Einfacher Vertrag</h3><p><strong>Kostenlose Terminreservierung, KEINE Anzahlung.</strong> Sie brauchen ein längeres Zahlungsziel? Wir richten es ein.</p></div></div>
      <div class="process-step"><span class="process-step__n">05</span><div><h3>Wir übernehmen alles</h3><p>Anfahrt, Aufbau, Operator und eine Show auf höchstem Niveau.</p></div></div>
      <div class="process-step process-step--key"><span class="process-step__n">06</span><div><h3>Zahlung nach dem Event</h3><p>Die Rechnung stellen wir <strong>erst nach der Veranstaltung</strong>. Zuerst das Ergebnis, dann die Zahlung.</p></div></div>
    </div>
    <div class="process-cta">
      <a href="#kontakt" class="btn-cta">Mit dem kostenlosen Angebot starten →</a>
      <p class="hero__cta-note">Unverbindlich · Antwort innerhalb von 24 h</p>
    </div>
  </section>

  <div class="video-teaser">
    <div class="video-teaser__content">
      <span class="tag">Live</span>
      <h2 class="video-teaser__title">Sie wollen den G1<br />live erleben?</h2>
      <a href="#kontakt" class="btn-cta">Kostenloses Angebot anfordern →</a>
      <p class="video-teaser__note">Unverbindlich · Keine Anzahlung · Antwort in 24 h</p>
    </div>
  </div>

  <section class="section faq-section">
    <div class="section-header">
      <span class="tag">FAQ</span>
      <h2 class="section-title">Häufige<br />Fragen</h2>
    </div>
    <div class="faq">
{_("render_faq")(faqs)}
    </div>
  </section>

  <!-- BLOG -->
  <section class="section" id="blog">
    <div class="section-header">
      <span class="tag">Blog</span>
      <h2 class="section-title">Wissen über<br />Event-Robotik</h2>
    </div>
    <div class="tiles tiles--blog">
{_("blog_cards")(4)}
    </div>
    <div style="text-align:center; margin:0 0 var(--s10);">
      <a href="{de('blog.html')}" class="btn-ghost" style="display:inline-flex;">Alle Artikel ansehen →</a>
    </div>

    <div style="margin-top:var(--s8); max-width:900px; margin-left:auto; margin-right:auto;">
      <p style="font-size:0.75rem; color:var(--text-3); text-transform:uppercase; letter-spacing:0.1em; font-weight:700; margin-bottom:var(--s3);">Roboter mieten in Ihrer Stadt</p>
      <div style="display:flex; flex-wrap:wrap; gap:var(--s2);">
{city_chips}
      </div>
    </div>
  </section>

  <!-- KONTAKT -->
  <section class="section contact-section" id="kontakt">
    <div class="contact-layout">
      <div class="contact-left">
        <span class="tag">Kontakt</span>
        <h2 class="section-title">Kostenloses Angebot<br />für Ihr Event.</h2>
        <p class="body-text">Schreiben Sie uns — wir rufen zurück und erstellen umgehend ein konkretes Angebot. Die Terminreservierung ist kostenlos und ohne Anzahlung, die Rechnung stellen wir erst nach der Veranstaltung.</p>
        <div class="contact-details" itemscope itemtype="https://schema.org/ProfessionalService">
          <meta itemprop="name" content="33bots – Humanoide Roboter mieten" />
          <meta itemprop="url" content="{DOMAIN}" />
          <div class="contact-detail">
            <span class="contact-detail__label">Unternehmen</span>
            <span class="contact-detail__val" itemprop="name">33bots – Humanoide Roboter mieten</span>
          </div>
          <a href="mailto:{EMAIL}" class="contact-detail" itemprop="email" content="{EMAIL}">
            <span class="contact-detail__label">E-Mail</span><span class="contact-detail__val">{EMAIL}</span>
          </a>
          <a href="tel:{PHONE_RAW}" class="contact-detail" itemprop="telephone" content="{PHONE_RAW}">
            <span class="contact-detail__label">Telefon</span><span class="contact-detail__val">{PHONE_HUMAN}</span>
          </a>
          <a href="tel:{PHONE2_RAW}" class="contact-detail">
            <span class="contact-detail__label">Telefon</span><span class="contact-detail__val">{PHONE2_HUMAN}</span>
          </a>
          <div class="contact-detail">
            <span class="contact-detail__label">Einsatzgebiet</span>
            <span class="contact-detail__val" itemprop="areaServed">Deutschlandweit</span>
          </div>
        </div>

        <nav class="coverage" aria-label="Roboter mieten — bediente Städte">
          <p class="coverage__label">Wir kommen ohne Aufpreis nach:</p>
          <ul class="coverage__cities">
{coverage}
          </ul>
          <p class="coverage__note">und überall sonst — die Anfahrt ist im Preis enthalten</p>
        </nav>
      </div>
      <div class="contact-right">
{_("contact_form")("z. B. Berlin, Messe Halle 3")}
      </div>
    </div>
  </section>

{_("footer_html")("")}"""


# ── Strony ofertowe i pozostałe ───────────────────────────────────────
def build(gen_globals):
    """Wywoływane z generate_de_site.main()."""
    global G
    G = gen_globals
    write = _("write")

    import de_blog
    G["blog_cards"] = de_blog.make_cards(G)

    write("index.html", build_index())
    build_offer_pages(write)
    build_case_studies(write)
    build_legal_pages(write)
    de_blog.build(G)


# ── Strony prawne (wymagane w Niemczech) ──────────────────────────────
def legal_page(out_file, crumb, title, desc, h1, sub, body):
    """Layout stron prawnych — bez CTA marketingowych, z pełną szerokością tekstu."""
    DOMAIN = _("DOMAIN")
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
{_("gtm_head")()}
{_("head_common")(title, desc, "impressum, datenschutz, barrierefreiheit, 33bots", out_file, "og-image.jpg", crumb)}
{_("head_assets")(_("HERO_STYLE"))}
</head>
<body>
{_("gtm_body")()}

{_("nav_html")()}
{_("crumbs")(crumb)}
{_("mobile_menu")()}
  <section class="hero">
    <div class="hero__content" style="max-width:820px;">
      <p class="hero__eyebrow">{crumb}</p>
      <h1 class="hero__title">{h1}</h1>
      <p class="hero__sub">{sub}</p>
    </div>
  </section>

  <section class="section" style="padding-top:0;">
    <div class="onas-body" style="max-width:820px; margin:0 auto;">
      <div class="onas-text">
{body}
      </div>
    </div>
  </section>

{_("footer_html")()}"""


def legal_block(h2, paragraphs, items=()):
    H3 = _("H3")
    out = [f'        <h2 {H3} style="font-size:1.25rem; margin-top:var(--s7);">{h2}</h2>']
    for p in paragraphs:
        out.append(f'        <p class="body-text">{p}</p>')
    if items:
        out.append('        <ul class="body-text" style="margin:0 0 var(--s4); padding-left:1.2em; '
                   'display:grid; gap:var(--s2);">')
        out += [f"          <li>{i}</li>" for i in items]
        out.append("        </ul>")
    return "\n".join(out)


TODO = ('<mark style="background:#ffe08a; color:#000; padding:0 4px;">[BITTE AUSFÜLLEN]</mark>')


def build_legal_pages(write):
    EMAIL, PHONE_HUMAN, DOMAIN = _("EMAIL"), _("PHONE_HUMAN"), _("DOMAIN")

    # ── Impressum (§ 5 DDG) ───────────────────────────────────────────
    imp = "\n".join([
        legal_block("Angaben gemäß § 5 DDG",
                    [f"Diensteanbieter: {TODO} (vollständige Firmierung laut Handelsregister)",
                     f"Anschrift: {TODO} (Straße, Hausnummer, PLZ, Ort, Land)",
                     f"Vertretungsberechtigte Person: {TODO}",
                     f"Registergericht und Registernummer: {TODO}",
                     f"Umsatzsteuer-Identifikationsnummer gemäß § 27 a UStG: {TODO}"]),
        legal_block("Kontakt",
                    [f"E-Mail: <a href=\"mailto:{EMAIL}\" style=\"color:var(--text); text-decoration:underline; "
                     f"text-underline-offset:3px;\">{EMAIL}</a>",
                     f"Telefon: {PHONE_HUMAN}"]),
        legal_block("Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV",
                    [f"{TODO} (Name und vollständige Anschrift der verantwortlichen Person)"]),
        legal_block("Verbraucherstreitbeilegung",
                    ["Wir sind nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer "
                     "Verbraucherschlichtungsstelle teilzunehmen.",
                     "Plattform der EU-Kommission zur Online-Streitbeilegung: "
                     "<a href=\"https://ec.europa.eu/consumers/odr\" target=\"_blank\" rel=\"noopener noreferrer\" "
                     "style=\"color:var(--text); text-decoration:underline; text-underline-offset:3px;\">"
                     "ec.europa.eu/consumers/odr</a>"]),
        legal_block("Haftung für Inhalte und Links",
                    ["Als Diensteanbieter sind wir für eigene Inhalte auf diesen Seiten nach den allgemeinen "
                     "Gesetzen verantwortlich. Wir sind jedoch nicht verpflichtet, übermittelte oder gespeicherte "
                     "fremde Informationen zu überwachen oder nach Umständen zu forschen, die auf eine "
                     "rechtswidrige Tätigkeit hinweisen.",
                     "Unser Angebot enthält Links zu externen Websites Dritter, auf deren Inhalte wir keinen "
                     "Einfluss haben. Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter "
                     "verantwortlich. Bei Bekanntwerden von Rechtsverletzungen entfernen wir derartige Links "
                     "umgehend."]),
        legal_block("Urheberrecht",
                    ["Die durch die Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten unterliegen dem "
                     "deutschen Urheberrecht. Beiträge Dritter sind als solche gekennzeichnet."]),
        '        <p class="body-text" style="margin-top:var(--s7); padding:var(--s4) var(--s5); '
        'background:var(--surface-2); border:1px solid var(--border-mid); border-radius:12px;">'
        '<strong>Hinweis für die Redaktion:</strong> Die gelb markierten Felder müssen vor der Veröffentlichung '
        'mit den tatsächlichen Unternehmensdaten befüllt werden. Ein unvollständiges Impressum ist in Deutschland '
        'abmahnfähig.</p>',
    ])
    write("impressum.html", legal_page(
        "impressum.html", "Impressum", "Impressum | 33bots",
        "Impressum von 33bots — Anbieterkennzeichnung gemäß § 5 DDG.",
        "Impressum.", "Anbieterkennzeichnung gemäß § 5 Digitale-Dienste-Gesetz (DDG).", imp))

    # ── Datenschutzerklärung (DSGVO) ──────────────────────────────────
    ds = "\n".join([
        legal_block("1. Verantwortlicher",
                    [f"Verantwortlich für die Datenverarbeitung auf dieser Website ist: {TODO} "
                     f"(vollständige Firmierung und Anschrift, siehe "
                     f"<a href=\"impressum.html\" style=\"color:var(--text); text-decoration:underline; "
                     f"text-underline-offset:3px;\">Impressum</a>).",
                     f"Kontakt: <a href=\"mailto:{EMAIL}\" style=\"color:var(--text); text-decoration:underline; "
                     f"text-underline-offset:3px;\">{EMAIL}</a>, Telefon {PHONE_HUMAN}"]),
        legal_block("2. Hosting und Server-Logfiles",
                    ["Beim Aufruf dieser Website erhebt der Hosting-Anbieter automatisch Informationen, die Ihr "
                     "Browser übermittelt (Server-Logfiles). Dazu gehören insbesondere:"],
                    ["IP-Adresse des anfragenden Endgeräts",
                     "Datum und Uhrzeit des Zugriffs",
                     "Name und URL der abgerufenen Datei",
                     "übertragene Datenmenge und Meldung über den Abruferfolg",
                     "verwendeter Browsertyp und dessen Version sowie das Betriebssystem"]),
        legal_block("",
                    ["Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO. Unser berechtigtes Interesse liegt im "
                     "sicheren, stabilen Betrieb der Website. Diese Daten werden nicht mit anderen Datenquellen "
                     "zusammengeführt und nach kurzer Zeit gelöscht."]),
        legal_block("3. Kontaktformular und Kontaktaufnahme",
                    ["Wenn Sie uns über das Kontaktformular oder per E-Mail kontaktieren, verarbeiten wir die von "
                     "Ihnen angegebenen Daten (Name, Unternehmen, E-Mail-Adresse, Telefonnummer, Angaben zu Ihrer "
                     "Veranstaltung), um Ihre Anfrage zu beantworten und ein Angebot zu erstellen.",
                     "Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO (vorvertragliche Maßnahmen) und, soweit es um "
                     "allgemeine Anfragen geht, Art. 6 Abs. 1 lit. f DSGVO. Die Daten werden gelöscht, sobald sie "
                     "für den Zweck nicht mehr erforderlich sind und keine gesetzlichen Aufbewahrungsfristen "
                     "entgegenstehen.",
                     f"Die Übermittlung des Formulars erfolgt über den Dienstleister Formspree "
                     f"(Formspree, Inc., USA). Dabei werden die von Ihnen eingegebenen Daten an dessen Server "
                     f"übertragen. {TODO} — bitte prüfen und ergänzen Sie, ob ein Auftragsverarbeitungsvertrag "
                     f"besteht und auf welcher Grundlage die Übermittlung in die USA erfolgt "
                     f"(z. B. EU-US Data Privacy Framework oder Standardvertragsklauseln)."]),
        legal_block("4. Cookies und Einwilligung",
                    ["Wir setzen technisch notwendige Cookies ein, die für den Betrieb der Website erforderlich "
                     "sind. Rechtsgrundlage ist § 25 Abs. 2 Nr. 2 TDDDG.",
                     "Alle weiteren Dienste — insbesondere die unten genannten Analyse-Dienste — setzen wir "
                     "ausschließlich nach Ihrer ausdrücklichen Einwilligung ein (§ 25 Abs. 1 TDDDG, Art. 6 Abs. 1 "
                     "lit. a DSGVO). Ohne Einwilligung werden diese Dienste nicht geladen.",
                     "Ihre Einwilligung können Sie jederzeit mit Wirkung für die Zukunft widerrufen — über den "
                     "Link „Datenschutz-Einstellungen“ im Seitenfuß."]),
        legal_block("5. Google Tag Manager und Google-Dienste",
                    ["Nach Ihrer Einwilligung laden wir den Google Tag Manager (Google Ireland Limited, Gordon "
                     "House, Barrow Street, Dublin 4, Irland). Der Tag Manager selbst erstellt keine Profile, "
                     "steuert aber das Laden weiterer Tags.",
                     f"{TODO} — bitte listen Sie hier die im Tag Manager tatsächlich ausgespielten Dienste auf "
                     f"(z. B. Google Analytics, Google Ads) samt Zweck, Speicherdauer und Empfängern.",
                     "Eine Übermittlung personenbezogener Daten in die USA kann nicht ausgeschlossen werden. "
                     "Rechtsgrundlage ist Ihre Einwilligung nach Art. 6 Abs. 1 lit. a DSGVO und Art. 49 Abs. 1 "
                     "lit. a DSGVO."]),
        legal_block("6. Albacross",
                    ["Nach Ihrer Einwilligung laden wir Albacross (Albacross Nordic AB, Schweden). Der Dienst "
                     "erkennt anhand der IP-Adresse Unternehmen, die unsere Website besuchen, um uns Hinweise auf "
                     "geschäftliches Interesse zu geben.",
                     "Rechtsgrundlage ist Ihre Einwilligung nach Art. 6 Abs. 1 lit. a DSGVO. Ohne Einwilligung "
                     "wird der Dienst nicht geladen."]),
        legal_block("7. Eingebettete Videos",
                    ["Die auf dieser Website eingebundenen Videos werden direkt von unserem eigenen Server "
                     "ausgeliefert. Es findet keine Einbindung von YouTube, Vimeo oder vergleichbaren Diensten "
                     "statt, sodass beim Abspielen keine Daten an Dritte übertragen werden."]),
        legal_block("8. Schriftarten",
                    ["Die verwendete Schriftart „Inter“ wird ausschließlich von unserem eigenen Server "
                     "ausgeliefert. Es besteht keine Einbindung von Google Fonts, sodass beim Aufruf der Seite "
                     "keine Verbindung zu Servern von Google aufgebaut und keine IP-Adresse an Google "
                     "übertragen wird."]),
        legal_block("9. Barrierefreiheit-Einstellungen",
                    ["Die von Ihnen im Barrierefreiheit-Panel gewählten Einstellungen (Textgröße, Darstellung, "
                     "Kontrast, Animationen) werden ausschließlich lokal in Ihrem Browser gespeichert und nicht an "
                     "uns übertragen."]),
        legal_block("10. Ihre Rechte",
                    ["Sie haben jederzeit das Recht auf Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16 DSGVO), "
                     "Löschung (Art. 17 DSGVO), Einschränkung der Verarbeitung (Art. 18 DSGVO), "
                     "Datenübertragbarkeit (Art. 20 DSGVO) sowie ein Widerspruchsrecht (Art. 21 DSGVO).",
                     "Eine erteilte Einwilligung können Sie jederzeit mit Wirkung für die Zukunft widerrufen.",
                     f"Zudem steht Ihnen ein Beschwerderecht bei einer Datenschutz-Aufsichtsbehörde zu. Zuständig "
                     f"ist die Aufsichtsbehörde am Sitz des Verantwortlichen: {TODO}"]),
        '        <p class="body-text" style="margin-top:var(--s7); padding:var(--s4) var(--s5); '
        'background:var(--surface-2); border:1px solid var(--border-mid); border-radius:12px;">'
        '<strong>Hinweis für die Redaktion:</strong> Diese Datenschutzerklärung bildet den technischen Stand '
        'dieser Website ab. Die gelb markierten Stellen müssen mit Ihren tatsächlichen Unternehmens- und '
        'Vertragsdaten befüllt und vor der Veröffentlichung juristisch geprüft werden.</p>',
    ])
    write("datenschutz.html", legal_page(
        "datenschutz.html", "Datenschutzerklärung", "Datenschutzerklärung | 33bots",
        "Datenschutzerklärung von 33bots — Informationen zur Verarbeitung personenbezogener Daten nach DSGVO.",
        "Datenschutz-<br />erklärung.",
        "Informationen zur Verarbeitung Ihrer personenbezogenen Daten gemäß Art. 13 und 14 DSGVO.", ds))

    # ── Barrierefreiheitserklärung (BFSG) ─────────────────────────────
    bf = "\n".join([
        legal_block("Unser Anspruch",
                    ["Wir möchten, dass diese Website von möglichst allen Menschen genutzt werden kann — "
                     "unabhängig von Einschränkungen des Sehens, Hörens, der Motorik oder der Kognition. "
                     "Grundlage unserer Arbeit sind die Web Content Accessibility Guidelines (WCAG) 2.1 auf "
                     "Stufe AA sowie die Anforderungen des Barrierefreiheitsstärkungsgesetzes (BFSG)."]),
        legal_block("Umgesetzte Maßnahmen",
                    ["Folgende Bedienhilfen stehen Ihnen auf jeder Seite zur Verfügung:"],
                    ["<strong>Barrierefreiheit-Panel</strong> — unten links: Textgröße in drei Stufen, helle und "
                     "dunkle Darstellung, erhöhter Kontrast sowie das Abschalten von Animationen. Ihre Auswahl "
                     "bleibt beim Seitenwechsel erhalten.",
                     "<strong>Tastaturbedienung</strong> — alle interaktiven Elemente sind per Tabulator "
                     "erreichbar und haben einen deutlich sichtbaren Fokusrahmen.",
                     "<strong>Sprunglink</strong> — mit der ersten Tabulator-Eingabe springen Sie direkt zum "
                     "Hauptinhalt und überspringen die Navigation.",
                     "<strong>Semantische Struktur</strong> — durchgehende Überschriftenhierarchie, "
                     "beschriftete Formularfelder, Alternativtexte für Bilder und ARIA-Attribute für "
                     "aufklappbare Bereiche.",
                     "<strong>Reduzierte Bewegung</strong> — die Systemeinstellung „prefers-reduced-motion“ "
                     "wird automatisch berücksichtigt.",
                     "<strong>Videos ohne Ton-Automatik</strong> — Videos starten nicht selbstständig und sind "
                     "über Standardbedienelemente steuerbar."]),
        legal_block("Bekannte Einschränkungen",
                    ["Wir sind mit der Umsetzung noch nicht am Ende. Derzeit bekannt sind uns folgende Punkte:"],
                    ["Für die eingebundenen Videos liegen noch keine Untertitel und keine Audiodeskription vor. "
                     "Die Inhalte sind rein visuell und ohne gesprochene Sprache; eine textliche Beschreibung "
                     "finden Sie jeweils neben dem Video.",
                     "Einzelne dekorative Effekte sind in der hellen Darstellung abgeschaltet, um die "
                     "Lesbarkeit zu sichern.",
                     f"{TODO} — bitte ergänzen Sie hier das Ergebnis Ihrer abschließenden Prüfung "
                     f"(z. B. durch einen externen Barrierefreiheits-Test) und das Datum der Erstellung "
                     f"dieser Erklärung."]),
        legal_block("Feedback und Kontakt",
                    [f"Ihnen sind Barrieren aufgefallen oder Sie benötigen Informationen in einem anderen Format? "
                     f"Schreiben Sie uns an <a href=\"mailto:{EMAIL}\" style=\"color:var(--text); "
                     f"text-decoration:underline; text-underline-offset:3px;\">{EMAIL}</a> oder rufen Sie an unter "
                     f"{PHONE_HUMAN}. Wir antworten innerhalb eines Werktags und stellen Ihnen die gewünschten "
                     f"Inhalte auf einem für Sie zugänglichen Weg zur Verfügung."]),
        legal_block("Durchsetzungsverfahren",
                    [f"Wenn Sie mit unserer Antwort nicht zufrieden sind, können Sie sich an die zuständige "
                     f"Marktüberwachungsstelle für Barrierefreiheit wenden: {TODO} (zuständige Stelle nach "
                     f"Sitz des Unternehmens)."]),
        '        <p class="body-text" style="margin-top:var(--s7); padding:var(--s4) var(--s5); '
        'background:var(--surface-2); border:1px solid var(--border-mid); border-radius:12px;">'
        '<strong>Hinweis für die Redaktion:</strong> Ob das BFSG für Ihr Angebot verbindlich gilt, hängt von '
        'Unternehmensgröße und Art der angebotenen Dienstleistung ab. Die technischen Maßnahmen sind umgesetzt; '
        'die gelb markierten Angaben müssen Sie ergänzen.</p>',
    ])
    write("barrierefreiheit.html", legal_page(
        "barrierefreiheit.html", "Barrierefreiheit", "Erklärung zur Barrierefreiheit | 33bots",
        "Erklärung zur Barrierefreiheit dieser Website nach BFSG — umgesetzte Maßnahmen, bekannte "
        "Einschränkungen und Kontakt für Rückmeldungen.",
        "Erklärung zur<br />Barrierefreiheit.",
        "Was wir umgesetzt haben, woran wir noch arbeiten und wie Sie uns Barrieren melden können.", bf))


def build_offer_pages(write):
    PRICE_RANGE, DOG_PRICE = _("PRICE_RANGE"), _("DOG_PRICE")

    # oferta.html → leistungen.html
    write(de("oferta.html"), simple_page(
        de("oferta.html"), "Leistungen & Angebot",
        "Leistungen und Angebot — humanoide Roboter mieten | 33bots",
        "Das komplette Angebot von 33bots: humanoide Roboter für Messen, Konferenzen, Galas, Firmenfeiern und Tage "
        "der offenen Tür. Anfahrt und Operator deutschlandweit inklusive →",
        "roboter mieten angebot, leistungen roboter vermietung, roboter für events angebot, 33bots leistungen",
        "Leistungen · Angebot · Deutschlandweit",
        "Unser Angebot —<br />ein Roboter, jede Bühne.",
        "Wir vermieten humanoide Roboter Unitree G1 für alles, was eine Bühne, einen Stand oder einen Saal hat. "
        "Hier finden Sie das komplette Leistungsspektrum — mit dem, was in jedem Paket immer enthalten ist.",
        tiles_section("Kernangebote", "Drei Formate,<br />die am häufigsten gebucht werden", [
            ("Messen", "Roboter am Messestand", "Mehr Standfrequenz, mehr Gespräche, mehr Leads. Der G1 arbeitet "
                                                "den kompletten Messetag vor Ihrem Stand."),
            ("Konferenzen", "Roboter auf der Bühne", "Eröffnung, Co-Moderation oder eigener Vortrag mit Q&A — der "
                                                     "Roboter wird zum Agendapunkt, den niemand verpasst."),
            ("Feiern", "Roboter auf der Firmenfeier", "Sommerfest, Jubiläum, Weihnachtsfeier — eine Show, über die "
                                                      "die Belegschaft wochenlang spricht."),
        ]) + text_section(
            "Was in jedem Paket enthalten ist",
            f"Ein kompletter Veranstaltungstag kostet {PRICE_RANGE} — und in diesem Preis ist bereits alles "
            f"enthalten, was Sie für die Show brauchen.",
            ["Wir kalkulieren keine Anfahrt nach, berechnen kein Branding und rechnen keine Zusatzoptionen ab. Der "
             "Betrag, den Sie im Angebot sehen, ist der Betrag auf der Rechnung."],
            subheads=[
                ("Immer inklusive", "Anfahrt deutschlandweit ohne Kilometerlimit, zertifizierter Operator für den "
                                    "gesamten Tag, Branding mit Logo und QR-Code auf der Brustplatte, "
                                    "Haftpflichtversicherung und technische Betreuung vor Ort."),
                ("Optionen", f"Der Roboterhund ist für {DOG_PRICE} pro Veranstaltungstag zubuchbar, inklusive "
                             f"Operator. Ab zwei Veranstaltungstagen erhalten Sie 15 % Rabatt auf jeden Tag."),
                ("Konditionen", "Terminreservierung kostenlos, keine Anzahlung, Rechnung erst nach der "
                                "Veranstaltung. Auf Wunsch mit längerem Zahlungsziel."),
            ]),
        faqs=[
            ("Wie schnell bekomme ich ein Angebot?",
             "In der Regel innerhalb von 24 Stunden, oft noch am selben Tag. Sie erhalten einen konkreten Betrag "
             "ohne Sternchen."),
            ("Arbeiten Sie auch mit Eventagenturen zusammen?",
             "Ja — wir liefern die Roboter-Show als Modul im Subauftrag, inklusive Präsentationsmaterial und "
             "technischem Rider. Bei fester Zusammenarbeit gibt es Partnerkonditionen."),
            ("Können wir mehrere Roboter gleichzeitig buchen?",
             "Für größere Formate stellen wir mehrere Einheiten plus zusätzliche Operator. Fragen Sie das früh an, "
             "damit wir die Termine sichern können."),
        ]))

    # oferta-targi.html
    write(de("oferta-targi.html"), simple_page(
        de("oferta-targi.html"), "Messen & Ausstellungen",
        "Roboter für Messen mieten — mehr Standbesucher | 33bots",
        "Humanoiden Roboter für Ihren Messestand mieten. Mehr Standfrequenz, mehr Gespräche, mehr Leads — Anfahrt "
        "und Operator deutschlandweit inklusive →",
        "roboter messe mieten, messestand attraktion, publikumsmagnet messestand, roboter messestand, Unitree G1 messe",
        "Messen · Standfrequenz · Leadgenerierung",
        "Roboter für Messen<br />und Ausstellungen.",
        "Auf einer Messe entscheidet sich alles in drei Sekunden: Bleibt der Besucher stehen oder geht er weiter? "
        "Ein frei laufender humanoider Roboter beantwortet diese Frage zu Ihren Gunsten.",
        tiles_section("Auf dem Stand", "Was der Roboter<br />für Sie leistet", [
            ("Frequenz", "Besucher bleiben stehen", "Der G1 wirkt aus mehreren Metern Entfernung. Ihr Team muss "
                                                    "niemanden mehr ansprechen — die Gäste kommen von selbst."),
            ("Leads", "Aus Aufmerksamkeit werden Gespräche", "Der QR-Code auf der Brustplatte führt direkt zu Ihrem "
                                                             "Formular, Ihrer Landingpage oder Ihrem Gewinnspiel."),
            ("Reichweite", "Jeder Besucher filmt", "Ihr Stand erscheint in Hunderten Stories und Clips — ohne "
                                                   "Mediabudget und ohne Agenturhonorar."),
        ]) + text_section(
            "Roboter auf dem Messestand — so funktioniert es in der Praxis",
            "Messestände konkurrieren nicht um Inhalte, sondern um Blicke. Wer auf einer Leitmesse mit tausenden "
            "Ausstellern sichtbar sein will, braucht ein Element, das sich bewegt und das man nicht ignorieren kann.",
            ["Der Unitree G1 läuft über Ihre Standfläche, begrüßt Vorbeigehende, posiert für Fotos und übergibt das "
             "Gespräch dann an Ihr Team. Unser Operator ist den ganzen Messetag vor Ort und steuert die Intensität — "
             "ruhiger am Vormittag, aktiver zu den Stoßzeiten."],
            subheads=[
                ("Standgröße und Aufbau", "Rund 2×2 m freie Fläche reichen für den Betrieb. Wir stimmen Aufbauzeiten, "
                                          "Standordnung und Sicherheitsvorgaben vorab mit Ihnen und dem "
                                          "Messeveranstalter ab."),
                ("Mehrtägige Messen", "Ab zwei Veranstaltungstagen erhalten Sie 15 % Rabatt auf jeden Tag — bei einer "
                                      "viertägigen Leitmesse ist das ein spürbarer Unterschied."),
                ("Branding", "Ihr Logo und ein QR-Code kommen kostenlos auf die Brustplatte. Auf jedem Besucherfoto "
                             "ist damit Ihre Marke im Bild."),
            ]) + video_section("spacer",
                               'So sieht der <strong style="color:var(--text);">Unitree G1</strong> in Bewegung aus — '
                               'genau dieser Anblick stoppt Besucher im Messegang.'),
        faqs=[
            ("Wie viel mehr Standfrequenz bringt ein Roboter?",
             "Das hängt von Halle, Standposition und Messeformat ab. Was wir zuverlässig beobachten: Besucher bleiben "
             "stehen, filmen und sprechen Ihr Team an — der schwierigste Teil der Standarbeit ist damit erledigt."),
            ("Klärt der Veranstalter Sicherheitsfragen mit Ihnen?",
             "Ja. Wir liefern die nötigen Angaben zu Gerät, Stromversorgung und Betrieb, damit Sie die Freigabe beim "
             "Messeveranstalter problemlos einholen können. Eine Haftpflichtversicherung besteht."),
            ("Was kostet ein Messetag?",
             f"{PRICE_RANGE} pro Tag inklusive Anfahrt, Operator, Branding und Versicherung. Ab zwei Tagen 15 % "
             f"Rabatt pro Tag."),
        ]))

    # oferta-konferencje.html
    write(de("oferta-konferencje.html"), simple_page(
        de("oferta-konferencje.html"), "Konferenzen & Galas",
        "Roboter für Konferenzen und Galas mieten | 33bots",
        "Humanoiden Roboter für Konferenz, Kongress oder Gala mieten. Empfang, Bühnenmoment und Fotoanlass — "
        "Operator und Anfahrt deutschlandweit inklusive →",
        "roboter konferenz mieten, roboter gala, kongress attraktion, roboter bühne event, Unitree G1 konferenz",
        "Konferenzen · Galas · Award-Abende",
        "Roboter für Konferenzen<br />und Galas.",
        "Auf einer Konferenz erinnern sich die Gäste selten an die Agenda — aber immer an den Moment, in dem ein "
        "humanoider Roboter den Saal betreten hat.",
        tiles_section("Formate", "Drei Rollen,<br />ein Roboter", [
            ("Empfang", "Gastgeber am Eingang", "Der G1 begrüßt Ankommende, weist den Weg zur Registrierung und "
                                                "setzt den Ton für den ganzen Tag."),
            ("Bühne", "Der Moment, der bleibt", "Ein kurzer Auftritt vor der Keynote oder zur Preisverleihung — der "
                                                "Roboter übernimmt die Bühne und übergibt an Ihre Speaker."),
            ("Pausen", "Gesprächsstoff im Foyer", "In den Pausen steht der Roboter im Foyer, posiert für Fotos und "
                                                  "liefert das Netzwerk-Thema des Tages."),
        ]) + text_section(
            "Konferenz, Kongress, Gala — was jeweils funktioniert",
            "Nicht jedes Format verträgt dieselbe Inszenierung. Auf einem Fachkongress arbeiten wir dezenter als auf "
            "einer Award-Nacht — die Wirkung bleibt in beiden Fällen dieselbe.",
            ["Bei Konferenzen setzen wir den G1 typischerweise im Foyer und am Registration Desk ein: Er stört das "
             "Programm nicht und sorgt trotzdem für Gesprächsstoff in jeder Pause. Bei Galas und Award-Abenden "
             "übernimmt er den Sektempfang oder einen kurzen Bühnenmoment — inklusive Tanzchoreografie, wenn Sie es "
             "wünschen."],
            subheads=[
                ("Abstimmung mit Ihrer Regie", "Timing, Auftrittslänge und Positionen legen wir vorab gemeinsam fest. "
                                               "Unser Operator ist während der gesamten Veranstaltung ansprechbar."),
                ("Internationales Publikum", "Der Effekt funktioniert sprachunabhängig — er entsteht über Bewegung "
                                             "und Präsenz. Ihr Branding bleibt in jedem Foto sichtbar."),
                ("Konditionen", f"{PRICE_RANGE} pro Veranstaltungstag, alles inklusive. Kostenlose "
                                f"Terminreservierung, keine Anzahlung, Rechnung erst nach dem Event."),
            ]) + video_section("taniec",
                               'Der <strong style="color:var(--text);">Unitree G1</strong> im Gala-Einsatz — Empfang, '
                               'Bühnenmoment und Fotoanlass in einem.'),
        faqs=[
            ("Stört der Roboter das Konferenzprogramm?",
             "Nein — wenn er richtig platziert ist. Auf Fachkongressen arbeiten wir bewusst im Foyer und in den "
             "Pausen. Der Ablauf wird vorher mit Ihnen abgestimmt."),
            ("Kann der Roboter auf der Bühne auftreten?",
             "Ja. Ein kurzer Auftritt vor der Keynote oder bei der Preisverleihung ist eines der wirkungsvollsten "
             "Formate. Timing und Ablauf stimmen wir mit Ihrer Regie ab."),
            ("Wie lange dauert der Aufbau?",
             "30–45 Minuten vor Veranstaltungsbeginn. Unser Operator bringt die komplette Ausrüstung mit."),
        ]))

    # oferta-dni-otwarte.html
    write(de("oferta-dni-otwarte.html"), simple_page(
        de("oferta-dni-otwarte.html"), "Tage der offenen Tür",
        "Roboter für den Tag der offenen Tür mieten | 33bots",
        "Humanoiden Roboter für Tag der offenen Tür, Showroom oder Karrieremesse mieten. Der Programmpunkt, über den "
        "alle sprechen — Operator und Anfahrt inklusive →",
        "roboter tag der offenen tür, roboter showroom, employer branding roboter, karrieremesse attraktion",
        "Tage der offenen Tür · Showrooms · Employer Branding",
        "Roboter für Tage<br />der offenen Tür.",
        "Ein Tag der offenen Tür lebt davon, dass Menschen kommen — und bleiben. Ein humanoider Roboter erledigt "
        "beides zuverlässiger als jede Anzeige.",
        tiles_section("Einsatzfelder", "Wo es besonders<br />gut funktioniert", [
            ("Unternehmen", "Tag der offenen Tür", "Familien, Nachbarschaft, Bewerberinnen und Bewerber — der "
                                                   "Roboter ist der Programmpunkt, der auf dem Plakat steht."),
            ("Bildung", "Hochschulen und Schulen", "Bei Studieninformationstagen und Science Slams ist der G1 "
                                                   "zuverlässig die meistfotografierte Station."),
            ("Recruiting", "Employer Branding", "Auf Karrieremessen bringt der Roboter Ihren Stand ins Gespräch — "
                                                "und Ihre Recruiter in echte Dialoge."),
        ]) + text_section(
            "Warum ein Roboter beim Tag der offenen Tür funktioniert",
            "Bei einem Tag der offenen Tür konkurrieren Sie nicht mit anderen Unternehmen, sondern mit dem "
            "Wochenende. Es braucht einen Grund zu kommen, der sich in einem Satz weitererzählen lässt.",
            ["„Da läuft ein echter humanoider Roboter herum“ ist genau so ein Satz. Der G1 begrüßt Besucher am "
             "Eingang, führt Gruppen durch das Gelände, posiert für Fotos und tanzt zum Programmhöhepunkt. Besonders "
             "bei Familien und jungem Publikum ist der Effekt sofort messbar — an den Handykameras."],
            subheads=[
                ("Indoor und outdoor", "Der G1 kommt mit Asphalt, Rasen, Hallenboden und Teppich zurecht. Für "
                                       "Außeneinsätze brauchen wir eine trockene, ebene Fläche und stimmen für den "
                                       "Regenfall vorab eine überdachte Alternative ab."),
                ("Sicherheit bei viel Publikum", "LiDAR und Computer Vision lassen den Roboter Personen in Echtzeit "
                                                 "ausweichen; unser Operator begleitet den Einsatz durchgehend. "
                                                 "Gerade bei Kindern ist diese doppelte Absicherung wichtig."),
                ("Kosten", f"{PRICE_RANGE} für den kompletten Veranstaltungstag, inklusive Anfahrt, Operator, "
                           f"Branding und Versicherung. Optional ergänzt der Roboterhund für {DOG_PRICE} pro Tag "
                           f"das Programm."),
            ]) + video_section("gesty",
                               'Der <strong style="color:var(--text);">Unitree G1</strong> in der Interaktion — '
                               'High Fives, Gesten und Fotos. Genau das passiert den ganzen Tag.'),
        faqs=[
            ("Ist der Roboter für Kinder geeignet?",
             "Ja. Der G1 weicht Personen selbstständig aus, zusätzlich überwacht unser Operator jeden Kontakt. Für "
             "Kinder ist der Roboter erfahrungsgemäß der Höhepunkt des Tages."),
            ("Kann der Roboter draußen eingesetzt werden?",
             "Ja, auf trockener und ebener Fläche. Bei Regen weichen wir in einen überdachten Bereich aus — das "
             "planen wir vorher gemeinsam."),
            ("Wie früh sollten wir buchen?",
             "So früh wie möglich — die Terminreservierung ist kostenlos und ohne Anzahlung, es entsteht Ihnen also "
             "kein Risiko durch frühes Buchen."),
        ]))

    # wypozyczenie-robota.html
    write(de("wypozyczenie-robota.html"), simple_page(
        de("wypozyczenie-robota.html"), "Humanoiden Roboter mieten",
        "Humanoiden Roboter mieten — Unitree G1 für Ihr Event | 33bots",
        f"Humanoiden Roboter Unitree G1 mieten: {PRICE_RANGE} pro Veranstaltungstag, Anfahrt, Operator und Branding "
        f"inklusive. Keine Anzahlung, Rechnung nach dem Event →",
        "humanoiden roboter mieten, roboter mieten, Unitree G1 mieten, roboter vermietung, event roboter",
        "Roboter mieten · Deutschlandweit · Alles inklusive",
        "Humanoiden Roboter<br />mieten.",
        "Ein kompletter Showtag mit dem Unitree G1 — Anfahrt, zertifizierter Operator, Branding und Versicherung "
        "sind im Preis enthalten. Sie buchen einmal und bekommen alles.",
        tiles_section("Was Sie bekommen", "Ein Paket,<br />keine Extras", [
            ("Ganzer Tag", "Showtag statt Stundentakt", "Der Roboter ist den kompletten Veranstaltungstag im "
                                                        "Einsatz — kein Stundenzähler, keine Verlängerungsaufschläge."),
            ("Operator", "Zertifizierter Operator inklusive", "Unser Operator baut auf, steuert den Roboter und "
                                                              "beantwortet die Fragen Ihrer Gäste."),
            ("Branding", "Ihr Logo ohne Aufpreis", "Logo und QR-Code kommen auf die Brustplatte des G1 — in jedem "
                                                   "Foto Ihrer Gäste sichtbar."),
        ]) + text_section(
            "Was der Unitree G1 auf Ihrer Veranstaltung macht",
            "Der G1 ist ein 132 cm großer, frei laufender Humanoid mit 23 Freiheitsgraden — kein Roboter auf Rädern "
            "und keine ferngesteuerte Puppe. Genau dieser Unterschied ist der Grund, warum Gäste stehen bleiben.",
            ["Er begrüßt Ankommende am Eingang, begleitet Gäste zum Stand, posiert für Fotos, gestikuliert im "
             "Gespräch und tanzt eine Choreografie, wenn der Moment passt. Ablauf und Intensität stimmen wir vorab "
             "mit Ihnen ab — vom dezenten Empfangsformat bis zum Bühnenauftritt."],
            subheads=[
                ("Technische Voraussetzungen vor Ort", "Eine 230-V-Steckdose und rund 2×2 m ebene Fläche genügen. "
                                                       "Unser Operator ist 30–45 Minuten vor Türöffnung "
                                                       "einsatzbereit."),
                ("Sicherheit", "LiDAR und Computer Vision lassen den G1 Hindernissen und Personen in Echtzeit "
                               "ausweichen. Eine Haftpflichtversicherung ist im Preis enthalten."),
                ("Preis und Konditionen", f"{PRICE_RANGE} pro Veranstaltungstag, abhängig ausschließlich vom Ort. Ab "
                                          f"zwei Tagen 15 % Rabatt auf jeden Tag. Der Roboterhund ist optional für "
                                          f"{DOG_PRICE} pro Tag buchbar."),
            ]) + video_section("branding",
                               'Der <strong style="color:var(--text);">Unitree G1</strong> mit dem Branding des '
                               'Kunden — Logo und QR-Code auf der Brustplatte, ohne Aufpreis.'),
        faqs=[
            ("Wie schnell bekomme ich ein Angebot?",
             "In der Regel innerhalb von 24 Stunden, oft noch am selben Tag."),
            ("Kann ich einen Termin reservieren, ohne sofort zu zahlen?",
             "Ja. Die Terminreservierung ist kostenlos und ohne Anzahlung. Die Rechnung stellen wir erst nach der "
             "Veranstaltung."),
            ("Ist der Roboterhund einzeln buchbar?",
             f"Der Roboterhund ist als Ergänzung zum humanoiden Roboter konzipiert und kostet {DOG_PRICE} pro "
             f"Veranstaltungstag inklusive Operator."),
        ]))

    # robot-na-wesele.html
    write(de("robot-na-wesele.html"), simple_page(
        de("robot-na-wesele.html"), "Roboter zur Hochzeit",
        "Roboter zur Hochzeit mieten — Attraktion für Ihren Tag | 33bots",
        "Humanoiden Roboter zur Hochzeit mieten: Er begrüßt die Gäste, tanzt mit dem Brautpaar und posiert für "
        "Fotos. Operator und Anfahrt deutschlandweit inklusive →",
        "roboter hochzeit, roboter zur hochzeit mieten, hochzeit attraktion, roboter tanzt hochzeit, hochzeitsüberraschung",
        "Hochzeit · Überraschung · Tanzfläche",
        "Roboter zur Hochzeit —<br />die Überraschung des Abends.",
        "Ihre Gäste haben schon jede Fotobox und jede Feuershow gesehen. Einen laufenden, tanzenden humanoiden "
        "Roboter noch nicht. Der G1 begrüßt die Gäste, tanzt mit dem Brautpaar und liefert die Aufnahmen, die noch "
        "Jahre später herumgezeigt werden.",
        tiles_section("Auf der Hochzeit", "Drei Momente,<br />die bleiben", [
            ("Empfang", "Begrüßung der Gäste", "Der Roboter empfängt die Gäste vor der Location — bevor der erste "
                                               "Sekt ausgeschenkt ist, sind die ersten Fotos gemacht."),
            ("Tanzfläche", "Der Tanz mit dem Brautpaar", "Nach dem Eröffnungstanz übernimmt der G1 die Fläche — der "
                                                         "Moment, in dem alle Handys hochgehen."),
            ("Fotos", "Ein Andenken für jeden Gast", "Jeder Tisch bekommt sein Foto mit dem Roboter. Ein Andenken, "
                                                     "das jede Gastgeschenktüte schlägt."),
        ]) + text_section(
            "Wie der Roboter in den Hochzeitsablauf passt",
            "Eine Hochzeit hat ihren eigenen Rhythmus — und der Roboter fügt sich ein, statt ihn zu stören. Wir "
            "planen die Auftritte gemeinsam mit Ihnen oder Ihrer Hochzeitsplanung.",
            ["Typisch sind drei kurze Blöcke: Empfang vor der Trauung oder dem Sektempfang, ein Auftritt nach dem "
             "Eröffnungstanz und eine freie Fotorunde am Abend. Dazwischen bleibt der Roboter im Hintergrund — "
             "sichtbar, aber nicht im Weg."],
            subheads=[
                ("Location und Untergrund", "Der G1 arbeitet auf Parkett, Estrich, Teppich und befestigten "
                                            "Außenflächen. Für Gartenhochzeiten legen wir gemeinsam eine ebene "
                                            "Showfläche fest — ein Podest genügt."),
                ("Musik", "Die Choreografie synchronisieren wir mit Ihrem Wunschtitel, sofern Sie ihn rechtzeitig "
                          "durchgeben. Alternativ übernimmt der Roboter die Playlist Ihres DJs."),
                ("Preis", f"{PRICE_RANGE} für den kompletten Tag, inklusive Anfahrt, Operator, Branding und "
                          f"Versicherung. Terminreservierung kostenlos, Rechnung erst nach der Hochzeit."),
            ]) + video_section("taniec",
                               'So sieht der <strong style="color:var(--text);">Unitree G1</strong> auf der '
                               'Tanzfläche aus. Genau dieser Ablauf funktioniert auf jeder Hochzeit.'),
        faqs=[
            ("Passt ein Roboter überhaupt zu einer Hochzeit?",
             "Wenn er dosiert eingesetzt wird, ja — und zwar hervorragend. Wir arbeiten mit kurzen Auftritten statt "
             "Dauerpräsenz, damit der Roboter die Überraschung bleibt und nicht zur Dekoration wird."),
            ("Können wir den Roboter als Überraschung für das Brautpaar buchen?",
             "Ja, das ist eines unserer häufigsten Szenarien. Wir stimmen den Auftritt diskret mit der Trauzeugin "
             "oder dem Trauzeugen ab und kommen erst zum vereinbarten Moment in Sicht."),
            ("Tanzt der Roboter zu unserem Lied?",
             "In vielen Fällen ja — geben Sie uns den Titel rechtzeitig durch, dann prüfen wir die Synchronisation "
             "der Choreografie."),
        ], kontakt_h2="Roboter für Ihre<br />Hochzeit reservieren."))

    # robot-na-impreze.html
    write(de("robot-na-impreze.html"), simple_page(
        de("robot-na-impreze.html"), "Roboter für Ihre Feier",
        "Roboter für Ihre Feier mieten — Party mit Humanoid | 33bots",
        "Humanoiden Roboter für Ihre Feier mieten: Tanzshow, Interaktion mit den Gästen und Fotobereich. Operator "
        "und Anfahrt deutschlandweit inklusive →",
        "roboter party mieten, roboter feier, party attraktion, roboter tanzt party, humanoider roboter feier",
        "Party · Tanzfläche · Fotobereich",
        "Roboter für Ihre Feier —<br />die Party wird zur Legende.",
        "Egal ob Firmenfeier, Geburtstag oder private Party: Ein humanoider Roboter ist die Attraktion, nach der die "
        "Gäste noch monatelang fragen. Tanzshow, Interaktion, Fotobereich — alles mit Operator.",
        tiles_section("Auf der Feier", "Was passiert,<br />wenn der G1 kommt", [
            ("Ankunft", "Der Moment der Überraschung", "Der Roboter kommt unangekündigt herein — die Reaktion der "
                                                       "Gäste ist der beste Teil des Abends."),
            ("Tanzfläche", "Er übernimmt das Parkett", "Eine Choreografie zur Musik Ihres DJs, danach tanzen die "
                                                       "Gäste mit. Ab da wird die Fläche nicht mehr leer."),
            ("Fotos", "Die Schlange reißt nicht ab", "High Fives, Posen, kurze Gespräche dank KI — der Fotobereich "
                                                     "arbeitet bis zum Ende des Abends."),
        ]) + text_section(
            "Welche Feiern wir am häufigsten betreuen",
            "Der Roboter funktioniert bei fast jedem Format — entscheidend ist nur, wie wir ihn einsetzen.",
            ["Bei Firmenfeiern setzen wir auf einen Showblock im Hauptteil des Abends, bei privaten Feiern eher auf "
             "einen Überraschungsauftritt. Bei Familienfesten arbeiten wir behutsamer und beziehen Kinder und ältere "
             "Gäste gezielt mit ein."],
            subheads=[
                ("Platzbedarf", "Ein paar Quadratmeter ebener Boden genügen — Saal, Terrasse oder Partyzelt reichen "
                                "völlig aus. Dazu eine 230-V-Steckdose."),
                ("Ablauf", "Wir stimmen die Auftritte vorab ab, damit sie zum Rhythmus Ihres Abends passen. Der "
                           "Operator bleibt den ganzen Abend vor Ort."),
                ("Preis", f"{PRICE_RANGE} für den kompletten Tag. Optional der Roboterhund für {DOG_PRICE} pro Tag."),
            ]) + video_section("taniec",
                               'Der <strong style="color:var(--text);">Unitree G1</strong> auf der Tanzfläche — '
                               'genau das passiert, wenn er auf Ihrer Feier auftritt.'),
        faqs=[
            ("Wie lange ist der Roboter auf der Feier?",
             "Wir buchen grundsätzlich den kompletten Veranstaltungstag. Wie Sie die Auftritte über den Abend "
             "verteilen, legen wir gemeinsam fest."),
            ("Kann der Roboter mit den Gästen sprechen?",
             "Ja — dank KI-Integration führt er Gespräche auf Deutsch, beantwortet Fragen und macht Witze."),
            ("Ist der Roboter auch für Kinder auf der Feier sicher?",
             "Ja. Der G1 weicht Personen selbstständig aus, und unser Operator begleitet jede Interaktion mit "
             "Kindern."),
        ], kontakt_h2="Roboter für Ihre<br />Feier reservieren."))

    # realizacje-wideo.html
    write(de("realizacje-wideo.html"), build_referenzen())


def build_referenzen():
    DOMAIN = _("DOMAIN")
    VIDEOS = _("VIDEOS")
    out_file = de("realizacje-wideo.html")

    cards = []
    for key in ("taniec", "powitanie", "gesty", "spacer", "branding"):
        v = VIDEOS[key]
        cards.append(f"""      <figure style="background:var(--surface-2); border:1px solid var(--border-mid); border-radius:16px; overflow:hidden; margin:0;">
        <video controls muted playsinline preload="none" poster="{v['poster']}" width="{v['w']}" height="{v['h']}"
               style="width:100%; display:block; background:var(--surface-2);" aria-label="{v['name']}">
          <source src="{v['file']}" type="video/mp4" />
          Ihr Browser unterstützt kein HTML5-Video.
        </video>
        <figcaption style="padding:var(--s4);">
          <p style="font-size:0.95rem; font-weight:700; color:var(--text); margin:0 0 4px;">{v['name']}</p>
          <p style="font-size:0.85rem; color:var(--text-2); margin:0; line-height:1.6;">{v['desc']}</p>
        </figcaption>
      </figure>""")

    sections = _("gallery_section")(
        tag="Fotos",
        heading="Bilder aus<br />echten Einsätzen",
        lead="Jede Aufnahme stammt von einer realen Veranstaltung — vom Sektempfang auf dem roten Teppich "
             "über den Summit mit 14 000 Gästen bis zur Straßenaktion in der Altstadt.",
        more_link=False)
    sections += f"""  <section class="section">
    <div class="section-header">
      <span class="tag">Videos</span>
      <h2 class="section-title">Der Roboter<br />in Bewegung</h2>
    </div>
    <div style="max-width:1100px; margin:0 auto;">
      <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:var(--s5);">
{chr(10).join(cards)}
      </div>
    </div>
  </section>

""" + text_section(
        "Aufnahmen aus echten Einsätzen",
        "Alle Aufnahmen auf dieser Seite stammen von realen Veranstaltungen — nichts davon ist im Studio "
        "nachgestellt oder animiert.",
        ["Was Sie sehen, ist der Standardablauf: Der Roboter begrüßt Gäste, geht durch die Fläche, gestikuliert, "
         "posiert für Fotos und tanzt eine Choreografie zur Musik. Auf der Brustplatte ist bei Kundeneinsätzen das "
         "Branding der jeweiligen Marke zu sehen — bei uns ohne Aufpreis.",
         "Wenn Sie sehen möchten, wie das bei Ihrer Veranstaltung aussehen würde, schreiben Sie uns kurz, worum es "
         "geht. Sie bekommen innerhalb von 24 Stunden einen Vorschlag für den Ablauf und ein konkretes Angebot."])

    return simple_page(
        out_file, "Referenzen",
        "Referenzen und Videos — humanoider Roboter im Einsatz | 33bots",
        "Videoaufnahmen aus echten Einsätzen des humanoiden Roboters Unitree G1: Begrüßung, Tanzshow, Interaktion "
        "und Branding. Sehen Sie, wie es bei Ihrer Veranstaltung aussehen kann →",
        "roboter referenzen, roboter video einsatz, humanoider roboter video, Unitree G1 einsatz video",
        "Referenzen · Videos · Echte Einsätze",
        "Referenzen —<br />der Roboter im Einsatz.",
        "Aufnahmen von echten Veranstaltungen: So läuft, gestikuliert und tanzt der Unitree G1 vor Publikum. Kein "
        "Studio, keine Animation.",
        sections,
        faqs=[
            ("Sind das echte Aufnahmen?",
             "Ja — alle Videos stammen von realen Kundeneinsätzen. Wir arbeiten weder mit Animationen noch mit "
             "gestellten Studioaufnahmen."),
            ("Bekommen wir nach unserer Veranstaltung auch Aufnahmen?",
             "Ja — nach dem Event übergeben wir Ihnen Aufnahmen mit dem Roboter, die Sie für Ihre eigene "
             "Kommunikation nutzen können."),
        ], kontakt_h2="Ihre Show<br />reservieren.")


# ── Case studies ──────────────────────────────────────────────────────
def build_case_studies(write):
    cases = [
        ("case-study-lexai.html", "Case Study: LEX AI",
         "Case Study LEX AI — humanoider Roboter im TV-Beitrag | 33bots",
         "Case Study LEX AI: Wie ein humanoider Roboter auf einer Legal-Tech-Veranstaltung für einen Beitrag im "
         "öffentlich-rechtlichen Fernsehen sorgte →",
         "case study roboter legal tech, roboter event referenz, LEX AI roboter, roboter im fernsehen",
         "Legal Tech · TV-Beitrag · Markenwirkung",
         "LEX AI —<br />vom Event in die Tagesnachrichten.",
         "Ein Legal-Tech-Unternehmen wollte für seine Veranstaltung mehr als eine Keynote. Am Ende lief der Beitrag "
         "im öffentlich-rechtlichen Fernsehen.",
         [("Die Ausgangslage",
           "LEX AI arbeitet an KI-Werkzeugen für die juristische Praxis — ein Thema, das erklärungsbedürftig ist und "
           "sich schwer bebildern lässt. Für die eigene Veranstaltung suchte das Unternehmen ein Element, das die "
           "abstrakte Botschaft „KI verändert die juristische Arbeit“ physisch erfahrbar macht.",
           ["Die Herausforderung war klar: Ein Vortrag über KI erzeugt keine Bilder. Ohne Bilder gibt es keine "
            "Berichterstattung, und ohne Berichterstattung bleibt die Reichweite auf den Saal beschränkt."]),
          ("Was wir gemacht haben",
           "Wir haben den Unitree G1 als physischen Stellvertreter für das Thema eingesetzt — mit einem Ablauf, der "
           "auf Kamerabilder hin konzipiert war.",
           ["Der Roboter empfing die Gäste am Eingang, war während der Veranstaltung in der Fläche unterwegs und "
            "übernahm einen kurzen Bühnenmoment. Unser Operator war den gesamten Tag vor Ort und steuerte die "
            "Auftritte nach dem Programmablauf.",
            "Auf der Brustplatte trug der Roboter das Branding des Kunden — sichtbar in jeder Aufnahme, ob von "
            "Gästen oder von Kamerateams."]),
          ("Das Ergebnis",
           "Die Show mit unserem Roboter wurde vom Fernsehen aufgegriffen und ausgestrahlt.",
           ["Aus einer Fachveranstaltung wurde ein Beitrag mit überregionaler Reichweite. Zusätzlich entstanden "
            "Hunderte Gästeaufnahmen, die das Branding des Kunden weitertrugen — ohne zusätzliches Mediabudget.",
            "Genau das ist der Mechanismus, den wir bei jeder Veranstaltung anstreben: Der Roboter erzeugt Bilder, "
            "und Bilder erzeugen Reichweite."])]),

        ("case-study-wallstreet.html", "Case Study: WallStreet 30",
         "Case Study WallStreet 30 — Roboter auf einer Investorenkonferenz | 33bots",
         "Case Study WallStreet 30: humanoider Roboter auf einer Konferenz mit 2 253 Teilnehmenden — Empfang, "
         "Bühnenmoment und Fotobereich →",
         "case study roboter konferenz, roboter investorenkonferenz, roboter event referenz",
         "Konferenz · 2 253 Teilnehmende · Foyer und Bühne",
         "WallStreet 30 —<br />2 253 Teilnehmende, ein Gesprächsthema.",
         "Eine der größten Investorenkonferenzen der Region — und die Frage, wie man bei diesem Publikum überhaupt "
         "noch auffällt.",
         [("Die Ausgangslage",
           "Bei einer Konferenz dieser Größenordnung konkurrieren Dutzende Partner um dieselbe Aufmerksamkeit. Roll-"
           "ups, Give-aways und Standflächen sehen für die Teilnehmenden nach kurzer Zeit alle gleich aus.",
           ["Gesucht war ein Element, das nicht in dieser Logik funktioniert — etwas, das sich bewegt, das man nicht "
            "übersehen kann und das die Teilnehmenden von sich aus fotografieren."]),
          ("Was wir gemacht haben",
           "Wir haben den Roboter dort platziert, wo bei Konferenzen die Gespräche tatsächlich stattfinden: im Foyer "
           "und in den Pausen.",
           ["Der G1 empfing die Teilnehmenden im Eingangsbereich, war während der Pausen im Foyer unterwegs und "
            "übernahm einen kurzen Bühnenmoment im Hauptprogramm. Die Auftrittszeiten waren so gelegt, dass sie den "
            "Ablauf im Saal nicht störten.",
            "Der Fotobereich am Roboter blieb über den gesamten Konferenztag besetzt — er war der Ort, an dem "
            "Teilnehmende ins Gespräch kamen."]),
          ("Das Ergebnis",
           "Der Roboter wurde zum inoffiziellen Treffpunkt der Konferenz.",
           ["Für die Veranstalter entstand daraus ein wiedererkennbares Element des Events, für die Partner ein "
            "Gesprächsanlass, der jedes Networking-Gespräch eröffnete — und für die Social-Media-Kanäle Material, "
            "das über die Konferenztage hinaus lief."])]),

        ("case-study-women-in-tech.html", "Case Study: Women in Tech Summit",
         "Case Study Women in Tech Summit — Roboter vor ~14 000 Gästen | 33bots",
         "Case Study Women in Tech Summit: humanoider Roboter auf der größten Women-in-Tech-Konferenz Europas mit "
         "rund 14 000 Teilnehmenden →",
         "case study roboter summit, roboter women in tech, roboter große konferenz referenz",
         "Summit · ~14 000 Gäste · Größte Konferenz ihrer Art in Europa",
         "Women in Tech Summit —<br />ein Roboter vor 14 000 Menschen.",
         "Die größte Women-in-Tech-Konferenz Europas, veranstaltet von der Perspektywy Foundation — und ein "
         "Publikum, das Technologie nicht erklärt bekommen muss.",
         [("Die Ausgangslage",
           "Bei rund 14 000 Teilnehmenden entscheidet nicht die Idee, sondern die Logistik. Eine Attraktion muss "
           "über viele Stunden funktionieren, große Menschenmengen aushalten und trotzdem sicher bleiben.",
           ["Hinzu kam der inhaltliche Anspruch: Bei einem technisch versierten Publikum reicht ein reiner Showeffekt "
            "nicht — der Roboter musste auch fachlichen Fragen standhalten."]),
          ("Was wir gemacht haben",
           "Wir haben den Einsatz in feste Showblöcke mit Interaktionsphasen gegliedert und den Operator durchgehend "
           "als Ansprechperson für technische Fragen eingesetzt.",
           ["Der G1 arbeitete in Blöcken: Choreografie-Shows zogen jeweils eine neue Besucherwelle an, dazwischen "
            "gab es Zeit für Fotos, High Fives und Gespräche. So blieb die Fläche über den ganzen Tag bespielt, ohne "
            "dass der Roboter durchgehend im Vollbetrieb lief.",
            "Für die Sicherheit sorgten die Hinderniserkennung des Roboters und ein fest definierter, betreuter "
            "Interaktionsbereich."]),
          ("Das Ergebnis",
           "Der Roboter gehörte zu den meistfotografierten Elementen des Summits.",
           ["Für die Veranstalter war er ein Programmpunkt, der ohne zusätzliche Moderation funktionierte; für die "
            "Teilnehmenden ein konkreter Anlass, über den Stand der Robotik zu sprechen.",
            "Diese Realisierung ist bis heute unsere Referenz für Veranstaltungen im fünfstelligen "
            "Besucherbereich — und der Beleg dafür, dass das Format auch bei sehr großen Formaten trägt."])]),
    ]

    for pl_file, crumb, title, desc, kw, eyebrow, h1, sub, blocks in cases:
        sections = "".join(text_section(h2, lead, paras, cta=False) for h2, lead, paras in blocks)
        sections += f"""  <section class="section" style="padding-top:0;">
    <div style="max-width:860px; margin:0 auto;">
      <p style="font-size:0.75rem; color:var(--text-3); text-transform:uppercase; letter-spacing:0.1em; font-weight:700; margin-bottom:var(--s3);">Weitere Case Studies</p>
      <div style="display:flex; flex-wrap:wrap; gap:var(--s3);">
{chr(10).join(f'        <a href="{de(o)}" style="color:var(--text); font-size:0.85rem; font-weight:600; padding:8px 16px; background:var(--surface-2); border:1px solid var(--border-mid); border-radius:10px; text-decoration:none;">{c}</a>' for o, c, *_rest in cases if o != pl_file)}
        <a href="{de('realizacje-wideo.html')}" style="color:var(--text); font-size:0.85rem; font-weight:600; padding:8px 16px; background:var(--surface-2); border:1px solid var(--border-mid); border-radius:10px; text-decoration:none;">Alle Referenzvideos</a>
      </div>
    </div>
  </section>
"""
        write(de(pl_file), simple_page(
            de(pl_file), crumb, title, desc, kw, eyebrow, h1, sub, sections,
            kontakt_h2="Ähnliches Ergebnis<br />für Ihr Event?", schema_type="Article"))

    # szablon-case-study.html → vorlage-case-study.html
    write(de("szablon-case-study.html"), simple_page(
        de("szablon-case-study.html"), "Vorlage: Case Study",
        "Vorlage für Case Studies | 33bots",
        "Interne Vorlage für den Aufbau einer Case Study: Ausgangslage, Umsetzung, Ergebnis.",
        "case study vorlage", "Vorlage · Interne Nutzung",
        "Case-Study-Vorlage.",
        "Diese Seite dient als Gerüst für neue Case Studies: Ausgangslage, Umsetzung, Ergebnis — jeweils mit einem "
        "einleitenden Absatz und zwei bis drei erläuternden Absätzen.",
        text_section("Ausgangslage", "Welches Problem hatte der Kunde vor der Veranstaltung?",
                     ["Hier beschreiben wir die Situation, die Zielsetzung und die Randbedingungen."], cta=False)
        + text_section("Umsetzung", "Was genau haben wir gemacht?",
                       ["Ablauf, Auftrittszeiten, Rolle des Operators, Branding."], cta=False)
        + text_section("Ergebnis", "Was ist dabei herausgekommen?",
                       ["Messbare und beobachtete Effekte, Reichweite, Reaktionen."], cta=False),
        kontakt_h2="Termin für Ihre<br />Veranstaltung sichern.", gallery=False))

    # index-redesign.html — wariant roboczy strony głównej, jak w serwisie PL
    write(de("index-redesign.html"), simple_page(
        de("index-redesign.html"), "Startseite (Entwurf)",
        "Startseite — Entwurfsvariante | 33bots",
        "Entwurfsvariante der Startseite von 33bots — humanoide Roboter für Events mieten.",
        "33bots entwurf", "Entwurf · Interne Variante",
        "Humanoide Roboter<br />mieten — Unitree G1.",
        "Entwurfsvariante der Startseite. Die produktive Fassung finden Sie auf der Startseite des Serviceangebots.",
        text_section("Humanoide Roboter für Ihre Veranstaltung",
                     "Ein kompletter Showtag mit Anfahrt, Operator und Branding im Preis.",
                     ["Diese Seite spiegelt die Entwurfsvariante des polnischen Serviceangebots und dient dem "
                      "Vergleich von Layoutvarianten."]),
        kontakt_h2="Termin für Ihre<br />Veranstaltung sichern."))
