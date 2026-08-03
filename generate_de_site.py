#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator niemieckiego serwisu 33bots — lustro 1:1 serwisu polskiego.

Serwis powstaje w katalogu ``de/`` i jest KOMPLETNYM, samodzielnym serwisem
przeznaczonym pod osobną domenę (33bots.de) — wgrywa się jako root tej domeny,
nie jako podkatalog 33bots.pl.

Zasada działania: strukturę (graf linków wewnętrznych, dobór wideo, poradniki,
kolejność sekcji) bierzemy wprost z generatorów polskich, a podmieniamy
wyłącznie język treści, nazwy plików (de_slugs.py) i merytorykę rynkową
(miasta, waluta, kalendarz świąt).

Uruchomienie:
    python3 generate_de_site.py
"""

import json
import os
import re
import shutil

import seo_pages_content as PL
import generate_seo_pages as PLGEN
import de_content_pages
import de_content_pages2
import de_cities
from de_slugs import SLUG_MAP, de

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "de")

# ── Konfiguracja rynku DE ─────────────────────────────────────────────
DOMAIN = "https://33bots.de"
EMAIL = "kontakt@33bots.pl"
PHONE_HUMAN = "+48 531 408 004"
PHONE_RAW = "+48531408004"
PHONE2_HUMAN = "+48 601 499 947"
PHONE2_RAW = "+48601499947"
GTM_ID = "GTM-MR7R7CJ3"
ALBACROSS_ID = "89159321"
LASTMOD = "2026-08-03"

PRICE_RANGE = "1.290 – 1.590 €"
PRICE_LOW = "1290"
PRICE_HIGH = "1590"
DOG_PRICE = "450 €"

DE_TEXT = {}
DE_TEXT.update(de_content_pages.TEXT)
DE_TEXT.update(de_content_pages2.TEXT)

# ── Wideo (opisy po niemiecku, te same pliki) ─────────────────────────
VIDEOS = {
    "taniec": dict(file="video/robot-taniec.mp4", poster="video/robot-taniec-poster.jpg",
                   duration="PT17S", w=324, h=576,
                   name="Humanoider Roboter tanzt — Choreografie-Show",
                   desc="Der Unitree G1 tanzt eine zur Musik synchronisierte Choreografie. Der Höhepunkt jeder Show.",
                   caption="Der Unitree G1 während der Choreografie. Live macht dieser Ablauf den größten Eindruck — die Gäste zücken innerhalb von Sekunden ihre Handys."),
    "powitanie": dict(file="video/robot-powitanie.mp4", poster="video/robot-powitanie-poster.jpg",
                      duration="PT12S", w=324, h=576,
                      name="Humanoider Roboter begrüßt die Gäste",
                      desc="Der Unitree G1 begrüßt die Gäste mit Geste und Stimme. So sieht ein erster Eindruck aus, den niemand vergisst.",
                      caption="Der Unitree G1 begrüßt die Gäste am Eingang. Der erste Eindruck, der die ganze Veranstaltung prägt."),
    "gesty": dict(file="video/robot-gesty.mp4", poster="video/robot-gesty-poster.jpg",
                  duration="PT14S", w=324, h=576,
                  name="Humanoider Roboter gestikuliert — Interaktion mit den Gästen",
                  desc="Der Unitree G1 gestikuliert und interagiert mit den Teilnehmenden — er winkt, gibt High Fives und posiert für Fotos.",
                  caption="Der Unitree G1 in der Interaktion — Gesten, High Fives, Posieren für Fotos. Genau darum sammeln sich die Teilnehmenden."),
    "spacer": dict(file="video/robot-spacer.mp4", poster="video/robot-spacer-poster.jpg",
                   duration="PT14S", w=324, h=576,
                   name="Humanoider Roboter in Bewegung",
                   desc="Der Unitree G1 läuft und geht auf Menschen zu. In Bewegung stoppt er Passanten und baut eine Traube um sich auf.",
                   caption="Der Unitree G1 in Bewegung. Ein laufender Humanoid ist ein Anblick, an dem niemand achtlos vorbeigeht."),
    "branding": dict(file="video/robot-branding.mp4", poster="video/robot-branding-poster.jpg",
                     duration="PT13S", w=324, h=576,
                     name="Humanoider Roboter mit Marken-Branding",
                     desc="Der Unitree G1 mit dem Branding des Kunden — Logo und Markenfarben auf dem Roboter, der zum Markenbotschafter wird.",
                     caption="Der Unitree G1 mit dem Branding des Kunden. Ein Roboter in den Farben Ihrer Marke ist das meistfotografierte Element der Veranstaltung."),
}

# ── Poradniki (etykiety niemieckie, pliki mapowane) ───────────────────
GUIDE_LABELS = {
    "blog-co-potrafi-robot-humanoidalny.html": "Was kann ein humanoider Roboter? 12 Fähigkeiten des G1 →",
    "blog-bezpieczenstwo-robota-na-evencie.html": "Ist ein Roboter auf dem Event sicher? →",
    "blog-ile-kosztuje-wynajem-robota.html": "Was kostet die Miete eines Roboters? Preise und Faktoren →",
    "blog-jak-wynajac-robota-checklist.html": "Roboter mieten — Checkliste für Veranstalter →",
    "blog-robot-na-stoisko-targowe.html": "Roboter am Messestand — so entstehen Leads →",
    "blog-robot-zamiast-hostessy.html": "Roboter statt Hostess? Der Vergleich →",
    "blog-robot-viral-marketing-event.html": "Der Roboter als Viral — Eventmarketing →",
    "blog-robot-ambasador-marki.html": "Der Roboter als Markenbotschafter →",
    "blog-robot-na-event-dla-dzieci.html": "Roboter auf Kinderveranstaltungen — der Leitfaden →",
    "blog-robot-z-ai-rozmawiajacy-po-polsku.html": "KI-Roboter, der Deutsch spricht →",
}

H3 = 'style="font-size:1.1rem; font-weight:700; letter-spacing:-0.01em; margin:var(--s6) 0 var(--s2); color:var(--text);"'
CHIP = ('padding:0.35rem 0.8rem; border:1px solid var(--border); border-radius:999px; '
        'font-size:0.8rem; color:var(--text-2); text-decoration:none; transition:border-color 0.2s')

# 10 miast w stopce/chipsach — odpowiedniki polskiej listy CHIP_CITIES
CHIP_CITIES = [
    "robot-wynajem-warszawa.html", "robot-wynajem-krakow.html", "robot-wynajem-wroclaw.html",
    "robot-wynajem-poznan.html", "robot-wynajem-gdansk.html", "robot-wynajem-katowice.html",
    "robot-wynajem-lodz.html", "robot-wynajem-szczecin.html", "robot-wynajem-lublin.html",
    "robot-wynajem-rzeszow.html",
]


def city_name(pl_file):
    return de_cities.CITIES[pl_file]["name"]


# ── Wspólne fragmenty HTML ────────────────────────────────────────────
def gtm_head():
    return (f"""  <!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{GTM_ID}');</script>
<!-- End Google Tag Manager -->""")


def gtm_body():
    return (f"""  <!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->""")


def nav_html(home="index.html"):
    return f"""  <div class="cursor-glow" id="cursorGlow" aria-hidden="true"></div>
  <div class="scroll-progress" id="scrollProgress" aria-hidden="true"></div>

  <header class="nav" id="nav">
    <div class="nav__inner">
      <a href="index.html" class="logo">33BOTS</a>
      <nav class="nav__links">
        <div class="nav__dropdown">
          <button class="nav__dropdown-toggle" aria-haspopup="true" aria-expanded="false" type="button">Angebot <svg viewBox="0 0 10 6" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
          <div class="nav__dropdown-menu">
            <a href="{de('oferta-targi.html')}">Messen</a>
            <a href="{de('oferta-konferencje.html')}">Konferenzen &amp; Galas</a>
            <a href="{de('oferta-dni-otwarte.html')}">Tage der offenen Tür</a>
            <a href="{de('atrakcje-na-event.html')}">Alle Attraktionen</a>
          </div>
        </div>
        <a href="{home}#ueber-uns">Über uns</a>
        <a href="{home}#events">Events</a>
        <a href="{de('blog.html')}">Blog</a>
        <a href="#kontakt">Kontakt</a>
      </nav>
      <button class="hamburger" id="hamburger" aria-label="Menü"><span></span><span></span></button>
    </div>
  </header>
  <main>
"""


def mobile_menu(home="index.html"):
    return f"""  <div class="mobile-menu" id="mobileMenu">
    <span class="mobile-menu__label">Angebot</span>
    <a href="{de('oferta-targi.html')}" class="mobile-menu__sub">Messen</a>
    <a href="{de('oferta-konferencje.html')}" class="mobile-menu__sub">Konferenzen &amp; Galas</a>
    <a href="{de('oferta-dni-otwarte.html')}" class="mobile-menu__sub">Tage der offenen Tür</a>
    <a href="{de('atrakcje-na-event.html')}" class="mobile-menu__sub">Alle Attraktionen</a>
    <a href="{home}#ueber-uns">Über uns</a>
    <a href="{home}#events">Events</a>
    <a href="{de('blog.html')}">Blog</a>
    <a href="#kontakt">Kontakt</a>
  </div>
"""


def crumbs(label):
    return (f'  <nav class="crumbs" aria-label="Brotkrümel" style="max-width:1200px; margin:0 auto; '
            f'padding:calc(var(--s8) + 48px) var(--s5) 0; font-size:0.78rem; letter-spacing:0.02em;">\n'
            f'    <a href="index.html" style="color:var(--text-3); text-decoration:none;">Startseite</a> '
            f'<span aria-hidden="true" style="color:var(--text-3);">›</span> '
            f'<span style="color:var(--text-2);">{label}</span>\n  </nav>\n')


def contact_form(location_ph="z. B. Berlin", date_text=False):
    date_field = ('<input id="f-date" type="text" name="date" placeholder="z. B. 14. Juni 2026" />'
                  if date_text else '<input id="f-date" type="date" name="date" />')
    return f"""        <form id="contactForm" class="form" novalidate>
          <div class="form-steps-header">
            <span class="form-step-ind active" id="stepInd1">01 — Kontaktdaten</span>
            <span class="form-step-sep">/</span>
            <span class="form-step-ind" id="stepInd2">02 — Ihre Veranstaltung</span>
          </div>
          <div class="form-step" id="formStep1">
            <div class="form-row">
              <div class="form-field">
                <label for="f-name">Vor- und Nachname *</label>
                <input id="f-name" type="text" name="name" placeholder="Max Mustermann" autocomplete="name" required />
                <span class="form-field__err" aria-live="polite"></span>
              </div>
              <div class="form-field">
                <label for="f-company">Unternehmen (optional)</label>
                <input id="f-company" type="text" name="company" placeholder="Firmenname" autocomplete="organization" />
              </div>
            </div>
            <div class="form-row">
              <div class="form-field">
                <label for="f-email">E-Mail *</label>
                <input id="f-email" type="email" name="email" placeholder="kontakt@firma.de" autocomplete="email" required />
                <span class="form-field__err" aria-live="polite"></span>
              </div>
              <div class="form-field">
                <label for="f-phone">Telefon</label>
                <input id="f-phone" type="tel" name="phone" placeholder="+49 30 1234567" autocomplete="tel" />
              </div>
            </div>
            <button type="button" id="btnNext" class="btn-submit">Weiter — Ihre Veranstaltung →</button>
          </div>
          <div class="form-step form-step--hidden" id="formStep2" aria-hidden="true">
            <div class="form-row">
              <div class="form-field">
                <label for="f-date">Veranstaltungsdatum</label>
                {date_field}
              </div>
              <div class="form-field">
                <label for="f-location">Ort / Stadt</label>
                <input id="f-location" type="text" name="location" placeholder="{location_ph}" autocomplete="address-level2" />
              </div>
            </div>
            <div class="form-field">
              <label for="f-message">Beschreiben Sie Ihre Veranstaltung *</label>
              <textarea id="f-message" name="message" rows="6" placeholder="Gästezahl, Dauer, Art der Veranstaltung …" required></textarea>
              <div class="form-field__footer">
                <span class="form-field__err" aria-live="polite"></span>
                <span class="char-counter"><span id="charCount">0</span> / 600</span>
              </div>
            </div>
            <div class="form-step__nav">
              <button type="button" id="btnBack" class="btn-back">← Zurück</button>
              <button type="submit" class="btn-submit">Anfrage senden →</button>
            </div>
          </div>
        </form>"""


def contact_section(h2, area="Deutschlandweit — Anfahrt inklusive", location_ph="z. B. Berlin", date_text=False):
    return f"""  <section class="section" id="kontakt">
    <div class="contact-layout">
      <div class="contact-left">
        <span class="tag">Kontakt</span>
        <h2 class="section-title">{h2}</h2>
        <p class="body-text">Schreiben Sie uns — Sie erhalten innerhalb eines Werktags ein Angebot inklusive Verfügbarkeit.</p>
        <div class="contact-details">
          <a href="mailto:{EMAIL}" class="contact-detail">
            <span class="contact-detail__label">E-Mail</span>
            <span class="contact-detail__val">{EMAIL}</span>
          </a>
          <a href="tel:{PHONE_RAW}" class="contact-detail">
            <span class="contact-detail__label">Telefon</span>
            <span class="contact-detail__val">{PHONE_HUMAN}</span>
          </a>
          <a href="tel:{PHONE2_RAW}" class="contact-detail">
            <span class="contact-detail__label">Telefon</span>
            <span class="contact-detail__val">{PHONE2_HUMAN}</span>
          </a>
          <div class="contact-detail">
            <span class="contact-detail__label">Einsatzgebiet</span>
            <span class="contact-detail__val">{area}</span>
          </div>
        </div>
      </div>
      <div class="contact-right">
{contact_form(location_ph, date_text)}
      </div>
    </div>
  </section>
"""


def footer_html(home="index.html"):
    return f"""  </main>
  <footer class="footer">
    <div class="footer__inner">
      <div class="footer__brand">
        <span class="logo">33BOTS</span>
        <p class="footer__tagline"><a href="index.html" style="color:inherit; text-decoration:underline; text-underline-offset:2px;">Humanoide Roboter mieten</a> · Deutschlandweit</p>
        <div class="footer__nap">
          <a href="tel:{PHONE_RAW}" class="footer__nap-item">{PHONE_HUMAN}</a>
          <a href="mailto:{EMAIL}" class="footer__nap-item">{EMAIL}</a>
        </div>
      </div>
      <div class="footer__links">
        <a href="{de('oferta.html')}">Leistungen &amp; Angebot</a>
        <a href="{de('atrakcje-na-event.html')}">Event-Attraktionen</a>
        <a href="{de('realizacje-wideo.html')}">Referenzen</a>
        <a href="{de('case-study-lexai.html')}">Case Study</a>
        <a href="{home}#ueber-uns">Über uns</a>
        <a href="{de('blog.html')}">Blog</a>
        <a href="#kontakt">Kontakt</a>
      </div>
      <div class="footer__right">
        <div class="footer__socials">
          <a href="https://www.instagram.com/33bots_/" target="_blank" rel="noopener noreferrer" class="footer__social">↗ Instagram</a>
          <a href="https://www.tiktok.com/@aimforum" target="_blank" rel="noopener noreferrer" class="footer__social">↗ TikTok</a>
          <a href="https://www.facebook.com/33bots" target="_blank" rel="noopener noreferrer" class="footer__social">↗ Facebook</a>
          <a href="https://www.linkedin.com/company/33bots" target="_blank" rel="noopener noreferrer" class="footer__social">↗ LinkedIn</a>
        </div>
        <span class="footer__copy">© 2026 33bots. Alle Rechte vorbehalten.</span>
      </div>
    </div>
  </footer>

  <div class="cookie-banner" id="cookieBanner" aria-live="polite">
    <p class="cookie-banner__text">Diese Website verwendet Cookies zu Analysezwecken. <a href="#" class="cookie-banner__link">Datenschutzerklärung</a></p>
    <button class="cookie-banner__btn" id="cookieAccept">Verstanden</button>
  </div>

  <div class="sticky-cta">
    <a href="#kontakt" class="btn-primary">Termin anfragen →</a>
  </div>

  <script src="main.js"></script>
  <!-- Albacross -->
  <script>window._nQc="{ALBACROSS_ID}";</script>
  <script async src="https://serve.albacross.com/track.js"></script>
</body>
</html>
"""


def head_common(title, desc, keywords, out_file, og_image, og_alt, extra_style=""):
    url = f"{DOMAIN}/{out_file}" if out_file != "index.html" else f"{DOMAIN}/"
    return f"""  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="keywords" content="{keywords}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{url}" />

  <meta property="og:type" content="website" />
  <meta property="og:url" content="{url}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:image" content="{DOMAIN}/{og_image}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="{og_alt}" />
  <meta property="og:locale" content="de_DE" />
  <meta property="og:site_name" content="33bots" />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />

  <meta name="theme-color" content="#000000" />
  <link rel="alternate" hreflang="de" href="{url}" />
  <link rel="alternate" hreflang="x-default" href="{url}" />"""


def head_assets(extra_style=""):
    return f"""  <script>history.scrollRestoration = 'manual';</script>
  <link rel="icon" type="image/svg+xml" href="favicon.svg" />
  <link rel="stylesheet" href="style.css?v=1" />
  <link rel="dns-prefetch" href="//serve.albacross.com" />
  <link rel="preconnect" href="https://www.googletagmanager.com" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="preload" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'" />
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" /></noscript>{extra_style}"""


HERO_STYLE = """
  <style>
    .hero { grid-template-columns: 1fr; min-height: 70vh; }
    .hero__content { max-width: none; padding: var(--s12) 0 var(--s8); }
    .hero__title { text-wrap: unset; }
  </style>"""


# ── Renderery bloków ──────────────────────────────────────────────────
def strip_tags(s):
    return re.sub(r"<[^>]+>", " ", s).replace("  ", " ").strip()


def render_tiles(tiles):
    out = []
    for i, (tag, title, desc) in enumerate(tiles):
        cls = "tile tile--light" if i == 1 else "tile"
        out.append(f'      <div class="{cls}">\n'
                   f'        <div class="tile__top"><span class="tile__tag">{tag}</span></div>\n'
                   f'        <h3 class="tile__title">{title}</h3>\n'
                   f'        <p class="tile__desc">{desc}</p>\n'
                   f'        <a href="#kontakt" class="tile__link">Termin anfragen →</a>\n'
                   f'      </div>')
    return "\n".join(out)


def render_scens(scens):
    return "\n\n".join(f'        <h3 {H3}>{h}</h3>\n        <p class="body-text">{p}</p>' for h, p in scens)


def render_related(related):
    out = []
    for href, label in related:
        de_href = de(href)
        de_label = DE_TEXT.get(href.replace(".html", ""), {}).get("crumb", label)
        if href in ("wypozyczenie-robota.html",):
            de_label = "Roboter mieten"
        elif href in ("atrakcje-na-event.html",):
            de_label = "Alle Attraktionen"
        elif href == "oferta-targi.html":
            de_label = "Messe-Angebot"
        elif href == "oferta-konferencje.html":
            de_label = "Konferenzen & Galas"
        elif href == "oferta-dni-otwarte.html":
            de_label = "Tage der offenen Tür"
        elif href == "realizacje-wideo.html":
            de_label = "Referenzen"
        elif href.startswith("case-study"):
            de_label = "Case Study"
        out.append(f'          <a href="{de_href}" style="color:var(--text); font-size:0.85rem; font-weight:600; '
                   f'text-decoration:underline; text-underline-offset:3px; white-space:nowrap;">{de_label} →</a>')
    return "\n".join(out)


def render_guides(guides):
    out = []
    for href, _pl_label in guides:
        label = GUIDE_LABELS.get(href, "Leitfaden →")
        out.append(f'        <a href="{de(href)}" style="display:flex; flex-direction:column; gap:4px; '
                   f'padding:var(--s4) var(--s5); background:var(--surface-2); border:1px solid var(--border-mid); '
                   f'border-radius:10px; text-decoration:none;">\n'
                   f'          <span style="font-size:0.7rem; font-weight:600; letter-spacing:0.08em; '
                   f'text-transform:uppercase; color:var(--text-3);">Leitfaden</span>\n'
                   f'          <span style="font-size:0.95rem; font-weight:700; color:var(--text); '
                   f'letter-spacing:-0.015em; line-height:1.35;">{label}</span>\n        </a>')
    return "\n".join(out)


def render_faq(faqs):
    out = []
    for q, a in faqs:
        out.append('      <div class="faq-item">\n'
                   '        <button class="faq-q" aria-expanded="false">\n'
                   f'          <span>{q}</span>\n'
                   '          <span class="faq-q__icon" aria-hidden="true">+</span>\n'
                   '        </button>\n'
                   f'        <div class="faq-a" hidden><p>{a}</p></div>\n'
                   '      </div>')
    return "\n".join(out)


def render_city_chips():
    return "\n".join(f'        <a href="{de(f)}" style="{CHIP}">{city_name(f)}</a>' for f in CHIP_CITIES)


TESTIMONIALS = """  <section class="section testimonials-section">
    <div class="section-header">
      <span class="tag">Stimmen</span>
      <h2 class="section-title">Was Kunden sagen</h2>
    </div>
    <div class="testimonials">
      <div class="testimonial">
        <p class="testimonial__quote">„Der Effekt hat unsere kühnsten Erwartungen übertroffen. Das Interesse war während der gesamten Veranstaltung enorm — ich hätte nicht gedacht, dass wir so viel Aufmerksamkeit bekommen."</p>
        <div class="testimonial__meta">
          <span class="testimonial__name">Karolina M.</span>
          <span class="testimonial__role">Marketing · IT-Branche</span>
        </div>
      </div>
      <div class="testimonial">
        <p class="testimonial__quote">„Das war eine der besten organisatorischen Entscheidungen. Die positiven Reaktionen der Teilnehmenden und ihr Engagement sind für uns die beste Bewertung des gesamten Projekts."</p>
        <div class="testimonial__meta">
          <span class="testimonial__name">Piotr Z.</span>
          <span class="testimonial__role">Veranstalter · Firmengala</span>
        </div>
      </div>
      <div class="testimonial">
        <p class="testimonial__quote">„Die Zusammenarbeit hat zu unglaublicher Reichweite in den sozialen Medien geführt. Das ist die Art von echtem Interesse, die man nicht einfach kaufen kann."</p>
        <div class="testimonial__meta">
          <span class="testimonial__name">Magdalena T.</span>
          <span class="testimonial__role">PR-Managerin · Technologiemesse</span>
        </div>
      </div>
    </div>
  </section>
"""


# ── Strona SEO (98 sztuk) ─────────────────────────────────────────────
def build_seo_page(p):
    """p — słownik strony PL (struktura). Treść bierzemy z DE_TEXT[slug]."""
    t = DE_TEXT[p["slug"]]
    out_file = SLUG_MAP[p["slug"] + ".html"]
    url = f"{DOMAIN}/{out_file}"
    video = VIDEOS[p.get("video", "gesty")]
    schema_name = t.get("schema_name", t["crumb"] + " — Unitree G1 mieten")
    schema_desc = t.get("schema_desc", t["desc"].rstrip(" →"))

    product_json = json.dumps({
        "@context": "https://schema.org", "@type": "Service",
        "name": schema_name, "description": schema_desc, "url": url,
        "image": f"{DOMAIN}/robot-g1.jpg",
        "serviceType": "Vermietung humanoider Roboter für Events",
        "provider": {"@type": "Organization", "name": "33bots", "url": f"{DOMAIN}/",
                     "email": EMAIL, "telephone": PHONE_HUMAN},
        "areaServed": {"@type": "Country", "name": "Deutschland"},
        "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR",
                   "lowPrice": PRICE_LOW, "highPrice": PRICE_HIGH,
                   "availability": "https://schema.org/InStock"},
    }, ensure_ascii=False, indent=2)

    breadcrumb_json = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Startseite", "item": f"{DOMAIN}/"},
            {"@type": "ListItem", "position": 2, "name": t["crumb"], "item": url},
        ],
    }, ensure_ascii=False, indent=2)

    faq_json = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": strip_tags(q),
                        "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
                       for q, a in t["faqs"]],
    }, ensure_ascii=False, indent=2)

    video_json = json.dumps({
        "@context": "https://schema.org", "@type": "VideoObject",
        "name": video["name"], "description": video["desc"],
        "thumbnailUrl": f"{DOMAIN}/{video['poster']}", "contentUrl": f"{DOMAIN}/{video['file']}",
        "uploadDate": "2026-07-02", "duration": video["duration"], "inLanguage": "de",
        "publisher": {"@type": "Organization", "name": "33bots", "url": DOMAIN,
                      "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/logo.png"}},
    }, ensure_ascii=False, indent=2)

    blog_para = ""
    if p.get("blog_link"):
        href, _ = p["blog_link"]
        label = GUIDE_LABELS.get(href, "unserem Leitfaden").rstrip(" →")
        blog_para = (f'\n        <p class="body-text">Mehr dazu lesen Sie in unserem Artikel: '
                     f'<a href="{de(href)}" style="color:var(--text); text-decoration:underline; '
                     f'text-underline-offset:3px;">{label}</a></p>\n')

    og_image = f"og/{out_file.replace('.html', '.jpg')}"

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
{gtm_head()}
{head_common(t['title'], t['desc'], t['keywords'], out_file, og_image, schema_name)}

  <script type="application/ld+json">
{product_json}
</script>

  <script type="application/ld+json">
{breadcrumb_json}
  </script>

  <script type="application/ld+json">
{faq_json}
  </script>

  <script type="application/ld+json">
{video_json}
  </script>

{head_assets(HERO_STYLE)}
</head>
<body>
{gtm_body()}

{nav_html()}
{crumbs(t['crumb'])}
{mobile_menu()}
  <section class="hero">
    <div class="hero__content">
      <p class="hero__eyebrow">{t['eyebrow']}</p>
      <h1 class="hero__title">{t['h1']}</h1>
      <p class="hero__sub">{t['sub']}</p>
      <div class="hero__ctas">
        <a href="#kontakt" class="btn-primary">Termin anfragen</a>
        <a href="#szenarien" class="btn-ghost">Wie läuft das ab? ↓</a>
      </div>
    </div>
  </section>

  <section class="section" id="vorteile">
    <div class="section-header">
      <span class="tag">Warum ein Roboter?</span>
      <h2 class="section-title">{t['tiles_h2']}</h2>
    </div>
    <div class="tiles">
{render_tiles(t['tiles'])}
    </div>
  </section>

  <section class="section" id="szenarien">
    <div class="onas-body" style="max-width:860px; margin:0 auto;">
      <div class="onas-text">
        <h2 class="section-title" style="font-size:clamp(1.8rem,3vw,2.8rem); margin-bottom:var(--s4);">{t['scen_title']}</h2>
        <p class="lead-text">{t['scen_intro']}</p>
{render_scens(t['scens'])}
{blog_para}
        <a href="#kontakt" class="btn-primary" style="margin-top:var(--s5); display:inline-flex;">Termin anfragen →</a>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:0;">
    <div style="max-width:860px; margin:0 auto;">
      <div style="padding:var(--s5) var(--s6); background:var(--surface-2); border:1px solid var(--border-mid); border-radius:12px; display:flex; align-items:center; justify-content:space-between; gap:var(--s4); flex-wrap:wrap;">
        <p style="color:var(--text-2); font-size:0.9rem; margin:0;">{t['related_intro']}</p>
        <div style="display:flex; gap:var(--s3); flex-wrap:wrap;">
{render_related(p['related'])}
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
      <video controls muted playsinline preload="none"
             poster="{video['poster']}"
             width="{video['w']}" height="{video['h']}"
             style="width:min(324px,85vw); border-radius:16px; border:1px solid var(--border-mid); background:var(--surface-2);"
             aria-label="{video['name']}">
        <source src="{video['file']}" type="video/mp4" />
        Ihr Browser unterstützt kein HTML5-Video.
      </video>
      <div style="max-width:420px; display:flex; flex-direction:column; gap:var(--s4); text-align:left;">
        <p style="color:var(--text-2); font-size:1rem; line-height:1.8; margin:0;">{video['caption']}</p>
        <a href="#kontakt" class="btn-primary" style="display:inline-flex; align-self:flex-start;">Show reservieren →</a>
      </div>
    </div>
  </section>

  <!-- LEITFÄDEN -->
  <section class="section" style="padding-top:0;">
    <div style="max-width:1000px; margin:0 auto;">
      <p style="font-size:0.75rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:var(--text-3); margin-bottom:var(--s4);">Leitfäden vor der Buchung</p>
      <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(260px, 1fr)); gap:var(--s4);">
{render_guides(PLGEN.GUIDES[p.get('guides', 'default')])}
      </div>
    </div>
  </section>

{TESTIMONIALS}
  <section class="section faq-section">
    <div class="section-header">
      <span class="tag">FAQ</span>
      <h2 class="section-title">{t['faq_h2']}</h2>
    </div>
    <div class="faq">
{render_faq(t['faqs'])}
    </div>
  </section>

{contact_section(t['kontakt_h2'], date_text=True)}
  <section class="section" style="padding-block:var(--s6) var(--s4); background:var(--surface-1)">
    <div class="container" style="max-width:1140px; margin-inline:auto; padding-inline:var(--s4)">
      <h2 style="font-size:clamp(1rem,2vw,1.4rem); font-weight:700; margin-bottom:var(--s3); color:var(--text-1)">Roboter mieten in Ihrer Stadt</h2>
      <div style="display:flex; flex-wrap:wrap; gap:0.5rem;">
{render_city_chips()}
      </div>
    </div>
  </section>

{footer_html()}"""


# ── Strona miasta (35 sztuk) ──────────────────────────────────────────
def build_city_page(pl_file):
    d = de_cities.CITIES[pl_file]
    out_file = SLUG_MAP[pl_file]
    url = f"{DOMAIN}/{out_file}"
    city = d["name"]
    video = VIDEOS["taniec"]

    faqs = list(d["faq"]) + [
        (f"Ist die Anfahrt nach {city} wirklich kostenlos?",
         f"Ja — die Anfahrt ist deutschlandweit im Preis enthalten, auch nach {city}. Es gibt keine "
         f"Kilometerpauschale und keine Nachberechnung. Der Preis im Angebot ist der Endpreis."),
        (f"Was kostet die Miete eines Roboters in {city}?",
         f"{PRICE_RANGE} pro kompletten Veranstaltungstag — inklusive Anfahrt, zertifiziertem Operator, "
         f"Branding und Versicherung. Ab zwei Tagen erhalten Sie 15 % Rabatt auf jeden Tag."),
    ]

    title = f"Humanoiden Roboter mieten {city} — Roboter für Events | 33bots"
    desc = (f"Humanoiden Roboter Unitree G1 in {city} mieten — Messen, Konferenzen, Galas. Anfahrt und "
            f"zertifizierter Operator inklusive. Angebot in 24 h →")

    service_json = json.dumps({
        "@context": "https://schema.org", "@type": "Service",
        "name": f"Humanoiden Roboter mieten — {city}",
        "description": f"Vermietung des Roboters Unitree G1 für Events, Konferenzen und Messen in {city}. "
                       f"Anfahrt und zertifizierter Operator inklusive.",
        "url": url, "image": f"{DOMAIN}/robot-g1.jpg",
        "serviceType": "Vermietung humanoider Roboter für Events",
        "provider": {"@type": "LocalBusiness", "name": "33bots – Humanoide Roboter mieten",
                     "url": DOMAIN, "telephone": PHONE_RAW, "email": EMAIL,
                     "sameAs": ["https://www.facebook.com/33bots", "https://www.instagram.com/33bots_/",
                                "https://www.linkedin.com/company/33bots", "https://www.tiktok.com/@aimforum"]},
        "areaServed": {"@type": "City", "name": city},
        "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR",
                   "lowPrice": PRICE_LOW, "highPrice": PRICE_HIGH,
                   "availability": "https://schema.org/InStock"},
    }, ensure_ascii=False, indent=2)

    breadcrumb_json = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Startseite", "item": f"{DOMAIN}/"},
            {"@type": "ListItem", "position": 2, "name": f"Roboter mieten {city}", "item": url},
        ],
    }, ensure_ascii=False, indent=2)

    faq_json = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": strip_tags(q),
                        "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in faqs],
    }, ensure_ascii=False, indent=2)

    video_json = json.dumps({
        "@context": "https://schema.org", "@type": "VideoObject",
        "name": f"Humanoider Roboter Unitree G1 im Einsatz — Miete in {city}",
        "description": f"Der humanoide Roboter Unitree G1 live: Er läuft, gestikuliert und tanzt. "
                       f"Miete für Events, Konferenzen und Messen in {city} und Umgebung.",
        "thumbnailUrl": f"{DOMAIN}/{video['poster']}", "contentUrl": f"{DOMAIN}/{video['file']}",
        "uploadDate": "2026-07-02", "duration": video["duration"], "inLanguage": "de",
        "publisher": {"@type": "Organization", "name": "33bots", "url": DOMAIN,
                      "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/logo.png"}},
    }, ensure_ascii=False, indent=2)

    other_cities = "\n".join(
        f'        <a href="{de(f)}" style="color:var(--text); font-size:0.85rem; font-weight:600; '
        f'padding:6px 14px; background:var(--surface-2); border:1px solid var(--border-mid); '
        f'border-radius:8px; text-decoration:none;">{city_name(f)}</a>'
        for f in de_cities.CITIES if f != pl_file)

    venue_items = "\n".join(f"          <li><strong>{n}</strong> — {t}</li>" for n, t in d["venues"])

    scenario_links = [
        ("robot-na-targi.html", "Messe"), ("robot-na-konferencje.html", "Konferenz"),
        ("robot-na-gale.html", "Gala"), ("robot-na-impreze-firmowa.html", "Firmenfeier"),
        ("robot-na-integracje-firmowa.html", "Teamevent"), ("robot-na-piknik-firmowy.html", "Betriebsfest"),
        ("robot-na-wesele.html", "Hochzeit"), ("robot-na-urodziny.html", "Geburtstag"),
        ("robot-na-otwarcie.html", "Eröffnung"), ("robot-na-dni-miasta.html", "Stadtfest"),
        ("robot-na-targi-pracy.html", "Karrieremesse"), ("robot-do-hotelu.html", "Hotel"),
        ("robot-do-galerii-handlowej.html", "Shoppingcenter"), ("atrakcje-na-event.html", "Alle Szenarien"),
    ]
    scenarios = "\n".join(f'        <a href="{de(h)}" style="{CHIP}">{lbl}</a>' for h, lbl in scenario_links)

    og_image = f"og/{out_file.replace('.html', '.jpg')}"

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
{gtm_head()}
{head_common(title, desc, d['keywords'], out_file, og_image, f"Humanoiden Roboter mieten {city} — 33bots")}

  <script type="application/ld+json">
{service_json}
</script>

  <script type="application/ld+json">
{breadcrumb_json}
  </script>

  <script type="application/ld+json">
{faq_json}
  </script>

  <script type="application/ld+json">
{video_json}
  </script>

{head_assets(HERO_STYLE)}
</head>
<body>
{gtm_body()}

{nav_html()}
{crumbs(f'Roboter mieten {city}')}
{mobile_menu()}
  <section class="hero">
    <div class="hero__content">
      <p class="hero__eyebrow">Roboter mieten · {city} · Events</p>
      <h1 class="hero__title">Humanoiden Roboter mieten<br />in {city} —<br />Unitree G1.</h1>
      <p class="hero__sub">{d['hero_sub']}</p>
      <div class="hero__ctas">
        <a href="#kontakt" class="btn-primary">Termin sichern</a>
        <a href="index.html#leistungen" class="btn-ghost">Angebot ansehen ↓</a>
      </div>
      <div class="hero__trust">
        <span class="hero__trust-item">✓ Bester Preis am Markt</span>
        <span class="hero__trust-item">✓ Anfahrt inklusive</span>
        <span class="hero__trust-item">✓ Operator inklusive</span>
        <span class="hero__trust-item">✓ Branding ohne Aufpreis</span>
      </div>
    </div>
  </section>

  <section class="section" id="vorteile">
    <div class="section-header">
      <span class="tag">Warum ein Roboter?</span>
      <h2 class="section-title">Was Sie in<br />{city} gewinnen</h2>
    </div>
    <div class="tiles">
      <div class="tile">
        <div class="tile__top"><span class="tile__tag">Sichtbarkeit</span></div>
        <h3 class="tile__title">Menschen bleiben stehen</h3>
        <p class="tile__desc">Der G1 zieht Aufmerksamkeit aus mehreren Dutzend Metern Entfernung an. Ihr Stand oder Ihre Veranstaltung wird zum meistbesuchten Punkt im Raum.</p>
        <a href="#kontakt" class="tile__link">Angebot anfragen →</a>
      </div>
      <div class="tile tile--light">
        <div class="tile__top"><span class="tile__tag">Reichweite</span></div>
        <h3 class="tile__title">Organisches Social Media</h3>
        <p class="tile__desc">Fotos und Clips mit dem Roboter landen noch während der Veranstaltung in den sozialen Medien. Ihre Marke erscheint in Hunderten Beiträgen — ohne Mediabudget.</p>
        <a href="#kontakt" class="tile__link">Angebot anfragen →</a>
      </div>
      <div class="tile">
        <div class="tile__top"><span class="tile__tag">Anfahrt</span></div>
        <h3 class="tile__title">Anfahrt inklusive</h3>
        <p class="tile__desc">Wir bringen den Roboter ohne Kilometeraufschlag nach {city}. Der genannte Preis ist der Endpreis — ohne Überraschungen.</p>
        <a href="#kontakt" class="tile__link">Angebot anfragen →</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="onas-body" style="max-width:860px; margin:0 auto;">
      <div class="onas-text">
        <h2 class="section-title" style="font-size:clamp(1.8rem,3vw,2.8rem); margin-bottom:var(--s4);">{d['section_title']}</h2>
        <p class="lead-text">{d['p1']}</p>
        <p class="body-text">Die Miete eines humanoiden Roboters Unitree G1 in {city} ist der einfachste Weg, sich in einem dichten Veranstaltungsmarkt abzuheben. Wir liefern den G1 direkt an Ihre Location — ohne Anfahrtsaufschlag. Bedient werden {d['around']}.</p>

        <h3 {H3}>{d['p2_header']}</h3>
        <p class="body-text">{d['p2']}</p>

        <h3 {H3}>Bewährte Locations in {city}</h3>
        <p class="body-text">{d['venues_line']}</p>

        <h3 {H3}>{d['p3_header']}</h3>
        <p class="body-text">{d['p3']}</p>
        <a href="#kontakt" class="btn-primary" style="margin-top:var(--s5); display:inline-flex;">Angebot anfordern →</a>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:0;">
    <div style="max-width:860px; margin:0 auto;">
      <div style="padding:var(--s5) var(--s6); background:var(--surface-2); border:1px solid var(--border-mid); border-radius:12px; display:flex; align-items:center; justify-content:space-between; gap:var(--s4); flex-wrap:wrap;">
        <p style="color:var(--text-2); font-size:0.9rem; margin:0;">Unsere Angebote: <strong style="color:var(--text);">Roboter für Messen</strong> und <strong style="color:var(--text);">Roboter für Konferenzen &amp; Galas</strong></p>
        <div style="display:flex; gap:var(--s3); flex-wrap:wrap;">
          <a href="{de('oferta-targi.html')}" style="color:var(--text); font-size:0.85rem; font-weight:600; text-decoration:underline; text-underline-offset:3px; white-space:nowrap;">Messen →</a>
          <a href="{de('oferta-konferencje.html')}" style="color:var(--text); font-size:0.85rem; font-weight:600; text-decoration:underline; text-underline-offset:3px; white-space:nowrap;">Konferenzen →</a>
        </div>
      </div>
    </div>
  </section>

  <!-- VIDEO -->
  <section class="section" id="video" style="padding-top:0;">
    <div style="display:flex; flex-wrap:wrap; gap:var(--s6); align-items:center; justify-content:center; max-width:900px; margin:0 auto;">
      <video controls muted playsinline preload="none"
             poster="{video['poster']}"
             width="300" height="533"
             style="width:min(300px,80vw); border-radius:16px; border:1px solid var(--border-mid); background:var(--surface-2);"
             aria-label="Humanoider Roboter Unitree G1 im Einsatz — Miete in {city}">
        <source src="{video['file']}" type="video/mp4" />
        Ihr Browser unterstützt kein HTML5-Video.
      </video>
      <div style="max-width:400px; display:flex; flex-direction:column; gap:var(--s4); text-align:left;">
        <p style="color:var(--text-2); font-size:1rem; line-height:1.8; margin:0;">So sieht der <strong style="color:var(--text);">Unitree G1</strong> live aus — er läuft, gestikuliert und tanzt. Genau diese Show können Sie bei Ihrer Veranstaltung in {city} haben, mit dem Branding Ihrer Marke auf der Brustplatte.</p>
        <a href="#kontakt" class="btn-primary" style="display:inline-flex; align-self:flex-start;">Show reservieren →</a>
      </div>
    </div>
  </section>

  <!-- REFERENZEN -->
  <section class="section" style="padding-top:0;">
    <div style="max-width:860px; margin:0 auto;">
      <p style="font-size:0.75rem; color:var(--text-3); text-transform:uppercase; letter-spacing:0.1em; font-weight:700; margin-bottom:var(--s3);">Erprobt bei großen Veranstaltungen</p>
      <div style="display:flex; flex-wrap:wrap; gap:var(--s3);">
        <a href="{de('case-study-wallstreet.html')}" style="color:var(--text); font-size:0.85rem; font-weight:600; padding:8px 16px; background:var(--surface-2); border:1px solid var(--border-mid); border-radius:10px; text-decoration:none;">WallStreet 30 · 2 253 Teilnehmende →</a>
        <a href="{de('case-study-women-in-tech.html')}" style="color:var(--text); font-size:0.85rem; font-weight:600; padding:8px 16px; background:var(--surface-2); border:1px solid var(--border-mid); border-radius:10px; text-decoration:none;">Women in Tech Summit · ~14 000 →</a>
        <a href="{de('case-study-lexai.html')}" style="color:var(--text); font-size:0.85rem; font-weight:600; padding:8px 16px; background:var(--surface-2); border:1px solid var(--border-mid); border-radius:10px; text-decoration:none;">LEX AI · TV-Beitrag →</a>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:0;">
    <div style="max-width:860px; margin:0 auto;">
      <p style="font-size:0.75rem; color:var(--text-3); text-transform:uppercase; letter-spacing:0.1em; font-weight:700; margin-bottom:var(--s3);">Roboter mieten in anderen Städten</p>
      <div style="display:flex; flex-wrap:wrap; gap:var(--s2);">
{other_cities}
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:0;" id="szenarien-stadt">
    <div class="container" style="max-width:1140px; margin-inline:auto; padding-inline:var(--s4)">
      <h2 style="font-size:clamp(1rem,2vw,1.4rem); font-weight:700; margin-bottom:var(--s2); color:var(--text-1)">Roboter für Events in {city} — wählen Sie Ihr Szenario</h2>
      <p style="color:var(--text-2); font-size:0.9rem; margin-bottom:var(--s3);">Wir betreuen in {city} jede Art von Veranstaltung — von Messen und Konferenzen bis zu privaten Feiern. Sehen Sie, wie sich der Roboter im konkreten Szenario schlägt:</p>
      <div style="display:flex; flex-wrap:wrap; gap:0.5rem;">
{scenarios}
      </div>
    </div>
  </section>

  <section class="section faq-section">
    <div class="section-header">
      <span class="tag">FAQ</span>
      <h2 class="section-title">Häufige Fragen<br />— {city}</h2>
    </div>
    <div class="faq">
{render_faq(faqs)}
    </div>
  </section>

  <section class="section" id="lokal">
    <div class="onas-body" style="max-width:860px; margin:0 auto;">
      <div class="onas-text">
        <h2 class="section-title" style="font-size:clamp(1.8rem,3vw,2.8rem); margin-bottom:var(--s4);">Eventlocations und Logistik in {city}</h2>
        <p class="body-text">{d['local_intro']}</p>
        <h3 {H3}>Bewährte Locations in {city}</h3>
        <ul class="body-text" style="margin:0 0 var(--s4); padding-left:1.2em; display:grid; gap:var(--s2);">
{venue_items}
        </ul>
        <h3 {H3}>Anfahrt und bediente Umgebung</h3>
        <p class="body-text">Zu jeder Location in {city} fahren wir ohne Kilometeraufschlag — bedient werden {d['around']}. Der Roboter braucht vor Ort rund 2×2 m ebene Fläche und eine 230-V-Steckdose; wir bringen ihn selbst herein und sind in der Regel 30–45 Minuten vor Veranstaltungsbeginn einsatzbereit. Schreiben Sie uns, wo Ihre Veranstaltung in {city} stattfindet, und Sie erhalten innerhalb von 24 Stunden ein konkretes Angebot.</p>
      </div>
    </div>
  </section>

{contact_section(f'Roboter in {city}<br />reservieren.', area=f'{city} und Umgebung', location_ph=f'z. B. {city}, {d["venues"][0][0]}')}
{footer_html()}"""


# ── Zapis ─────────────────────────────────────────────────────────────
WRITTEN = []


def write(rel, content):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    WRITTEN.append(rel)


def copy_assets():
    """Kopiuje wszystkie zasoby graficzne i wideo — te same zdjęcia co serwis PL."""
    os.makedirs(OUT, exist_ok=True)

    # arkusz stylów 1:1
    shutil.copyfile(os.path.join(BASE, "style.css"), os.path.join(OUT, "style.css"))
    WRITTEN.append("style.css")

    # pojedyncze pliki w rootcie
    for name in os.listdir(BASE):
        src = os.path.join(BASE, name)
        if not os.path.isfile(src):
            continue
        if name.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".svg", ".heic", ".dng")):
            shutil.copyfile(src, os.path.join(OUT, name))
            WRITTEN.append(name)

    # katalog video 1:1
    src_video = os.path.join(BASE, "video")
    dst_video = os.path.join(OUT, "video")
    os.makedirs(dst_video, exist_ok=True)
    for name in os.listdir(src_video):
        shutil.copyfile(os.path.join(src_video, name), os.path.join(dst_video, name))
        WRITTEN.append(f"video/{name}")

    # obrazy OG — te same pliki, nazwy dopasowane do stron DE
    src_og = os.path.join(BASE, "og")
    dst_og = os.path.join(OUT, "og")
    os.makedirs(dst_og, exist_ok=True)
    for pl_file, de_file in SLUG_MAP.items():
        pl_og = os.path.join(src_og, pl_file.replace(".html", ".jpg"))
        if os.path.exists(pl_og):
            shutil.copyfile(pl_og, os.path.join(dst_og, de_file.replace(".html", ".jpg")))
            WRITTEN.append(f"og/{de_file.replace('.html', '.jpg')}")


def build_main_js():
    src = open(os.path.join(BASE, "main.js"), encoding="utf-8").read()
    repl = [
        ("'To pole jest wymagane'", "'Dieses Feld ist erforderlich'"),
        ("'Nieprawidłowy format'", "'Ungültiges Format'"),
        ("'Sprawdź to pole'", "'Bitte prüfen Sie dieses Feld'"),
        ("'Wysyłanie...'", "'Wird gesendet …'"),
        ("'Spróbuj ponownie'", "'Erneut versuchen'"),
        ("'Coś poszło nie tak. Napisz bezpośrednio na kontakt@33bots.pl'",
         f"'Etwas ist schiefgelaufen. Schreiben Sie uns direkt an {EMAIL}'"),
        ("'Formularz kontaktowy'", "'Kontaktformular'"),
        ("<h3>Wiadomość wysłana</h3>", "<h3>Nachricht gesendet</h3>"),
        ("<p>Odezwiemy się na <strong>${payload.email}</strong><br>w ciągu 24 godzin roboczych.</p>",
         "<p>Wir melden uns an <strong>${payload.email}</strong><br>innerhalb von 24 Werkstunden.</p>"),
    ]
    for old, new in repl:
        if old not in src:
            raise SystemExit(f"main.js: brak fragmentu do tłumaczenia: {old}")
        src = src.replace(old, new)
    return src


def build_robots():
    return f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n"


def build_redirects():
    host = DOMAIN.replace("https://", "")
    return (f"https://www.{host}/* {DOMAIN}/:splat 301!\n"
            f"http://www.{host}/* {DOMAIN}/:splat 301!\n"
            f"http://{host}/* {DOMAIN}/:splat 301!\n")


def build_sitemap(pages):
    urls = []
    for path, prio in pages:
        loc = f"{DOMAIN}/" if path == "index.html" else f"{DOMAIN}/{path}"
        urls.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{LASTMOD}</lastmod>\n"
                    f"    <priority>{prio}</priority>\n  </url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</urlset>\n")


def build_404():
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
{gtm_head()}
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Seite nicht gefunden — 33bots</title>
  <meta name="description" content="Die aufgerufene Seite existiert nicht. Zurück zur Startseite von 33bots — humanoide Roboter für Events mieten." />
  <meta name="robots" content="noindex, follow" />
{head_assets(HERO_STYLE)}
</head>
<body>
{gtm_body()}

{nav_html()}
{mobile_menu()}
  <section class="hero">
    <div class="hero__content" style="max-width:720px;">
      <p class="hero__eyebrow">Fehler 404</p>
      <h1 class="hero__title">Diese Seite<br />gibt es nicht.</h1>
      <p class="hero__sub">Der Link ist veraltet oder enthält einen Tippfehler. Zurück zur Startseite — oder direkt zum Angebot.</p>
      <div class="hero__ctas">
        <a href="index.html" class="btn-primary">Zur Startseite →</a>
        <a href="{de('wypozyczenie-robota.html')}" class="btn-ghost">Roboter mieten →</a>
      </div>
    </div>
  </section>
{footer_html()}"""


def main():
    os.makedirs(OUT, exist_ok=True)
    copy_assets()
    write("main.js", build_main_js())

    # 98 podstron SEO
    for p in PL.ALL_PAGES:
        write(SLUG_MAP[p["slug"] + ".html"], build_seo_page(p))

    # 35 stron miast
    for pl_file in de_cities.CITIES:
        write(SLUG_MAP[pl_file], build_city_page(pl_file))

    # strony ręczne, blog i strona główna — moduł uzupełniający
    try:
        import de_pages_manual
        de_pages_manual.build(globals())
    except ImportError:
        print("UWAGA: brak de_pages_manual.py — strona główna, oferta, case studies i blog nie zostały wygenerowane")

    write("404.html", build_404())
    write("robots.txt", build_robots())
    write("_redirects", build_redirects())

    html_pages = sorted(f for f in WRITTEN if f.endswith(".html") and f != "404.html")
    prio = {}
    for f in html_pages:
        if f == "index.html":
            prio[f] = "1.0"
        elif f.startswith("blog-"):
            prio[f] = "0.7"
        elif f.startswith("roboter-mieten-"):
            prio[f] = "0.8"
        else:
            prio[f] = "0.9"
    write("sitemap.xml", build_sitemap([(f, prio[f]) for f in html_pages]))

    html_count = len([f for f in WRITTEN if f.endswith(".html")])
    print(f"Wygenerowano {len(WRITTEN)} plików w {OUT}/ (w tym {html_count} stron HTML)")


if __name__ == "__main__":
    main()
