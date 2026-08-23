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

import de_structure
import de_content_pages
import de_content_pages2
import de_cities
from de_slugs import SLUG_MAP, de

# Skrypt leży w build/, a serwis budowany jest w katalogu nadrzędnym (root repo),
# który jest jednocześnie katalogiem wdrożeniowym domeny.
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = BASE

# ── Konfiguracja rynku DE ─────────────────────────────────────────────
DOMAIN = "https://33bots.de"
EMAIL = "kontakt@33bots.de"
# Kontakt wyłącznie mailowy. Numer telefonu nie jest w Impressum obowiązkowy,
# o ile dostępny jest drugi kanał szybkiej komunikacji — tu formularz kontaktowy
# na każdej stronie (TSUE C-298/07, Deutsche Internet Versicherung).
# Analityka wyłączona do czasu założenia własnego kontenera dla domeny .de.
# Kontener polskiej strony celowo nie jest tu wpisany: mieszałby dane obu rynków,
# a jego tagi nie są ujawnione w niemieckiej Datenschutzerklärung, czego wymaga
# art. 13 ust. 1 lit. e RODO. Po wpisaniu ID wraca baner zgody i sekcje o
# analityce w Datenschutz — bez ID strona nie ustawia żadnych cookies poza
# niezbędnymi, więc zgoda nie jest w ogóle potrzebna.
GTM_ID = ""
ALBACROSS_ID = ""
ANALYTICS = bool(GTM_ID or ALBACROSS_ID)
# Bei inhaltlichen Aenderungen hochsetzen — steht als <lastmod> in der Sitemap.
LASTMOD = "2026-08-16"

# ── Dane rejestrowe do Impressum i Datenschutz ────────────────────────
# Wymagane przez § 5 DDG, § 18 ust. 2 MStV i art. 13 DSGVO. Puste pole zostaje
# na stronie oznaczone żółtym markerem — serwisu nie wolno publikować, dopóki
# którekolwiek jest puste (niekompletne Impressum jest w Niemczech abmahnfähig).
COMPANY = {
    # ── uzupełnione ──────────────────────────────────────────────────
    "street": "Plac Jana Henryka Dąbrowskiego 12",
    "postcode_city": "00-055 Warszawa",
    "country": "Polen",
    # Polski organ nadzorczy — siedziba zmieniona w lipcu 2025 r.
    "supervisory_authority": (
        "Prezes des Amts für den Schutz personenbezogener Daten "
        "(Prezes Urzędu Ochrony Danych Osobowych), ul. Moniuszki 1A, "
        "00-014 Warszawa, Polen, uodo.gov.pl"),
    # Organ nadzoru rynku ds. dostępności wg BFSG (16 krajów związkowych)
    "market_surveillance": (
        "Marktüberwachungsstelle der Länder für die Barrierefreiheit von "
        "Produkten und Dienstleistungen (MLBF), Carl-Miller-Straße 6, "
        "39112 Magdeburg, kontakt@mlbf-barrierefrei.de"),
    "formspree_note": (
        "Formspree betreibt seine Dienste auf Servern von Amazon Web Services "
        "in den Vereinigten Staaten und ist nach SOC 2 Typ 2 zertifiziert. Für "
        "die Verarbeitung in unserem Auftrag besteht ein Vertrag zur "
        "Auftragsverarbeitung nach Art. 28 DSGVO. Die Übermittlung in die USA "
        "stützt sich auf Art. 49 Abs. 1 lit. b DSGVO, da sie zur Beantwortung "
        "Ihrer Anfrage erforderlich ist."),

    "legal_name": "33Bots Bartosz Wysocki",
    "represented_by": "Bartosz Wysocki",
    # Jednoosobowa działalność gospodarcza — rejestr CEIDG, nie sąd rejestrowy
    "register": ("Eingetragen im Zentralregister für Wirtschaftstätigkeit der Republik Polen "
                 "(CEIDG, Centralna Ewidencja i Informacja o Działalności Gospodarczej) · "
                 "REGON: 544792095"),
    # NIP zweryfikowany sumą kontrolną. Formę PL… podajemy jako USt-IdNr tylko
    # przy rejestracji do transakcji wewnątrzunijnych (VAT-UE) — patrz README.
    "vat_id": "PL5253090645 (NIP: 5253090645)",
    "content_responsible": ("Bartosz Wysocki, Plac Jana Henryka Dąbrowskiego 12, "
                            "00-055 Warszawa, Polen"),

    # ── do uzupełnienia przez właściciela ────────────────────────────
    "gtm_services": "",      # usługi faktycznie wyzwalane w kontenerze GTM
}


def company(field):
    """Wartość pola albo widoczny marker do uzupełnienia."""
    value = COMPANY.get(field, "").strip()
    return value or MISSING


MISSING = ('<mark style="background:#ffe08a; color:#000; padding:0 4px;">'
           '[BITTE AUSFÜLLEN]</mark>')


# Komunikacja cenowa: stawka wyjściowa bez górnej granicy.
PRICE_FROM = "ab 2.499 €"      # do zdań typu „kostet ab 2.499 €"
PRICE_MIN = "2.499 €"          # sama kwota
PRICE_LOW = "2499"             # dane strukturalne (lowPrice)
DOG_PRICE = "850 €"

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

# ── Zdjęcia z realizacji ──────────────────────────────────────────────
# Ten sam zestaw plików co w serwisie PL (index-redesign.html), przeniesiony
# do layoutu produkcyjnego. Kolejność dobrana tak, by od razu było widać skalę
# i różnorodność wydarzeń: gale, summity, ulica, plener, noc, deszcz.
GALLERY = [
    ("realizacja-women-in-tech-tlum", "wide", "Alle zücken ihr Handy",
     "Teilnehmerinnen des Women in Tech Summit filmen den humanoiden Roboter mit ihren Handys"),
    ("realizacja-gala-czerwony-dywan", "", "Roter Teppich",
     "Humanoider Roboter im Paillettensmoking auf dem roten Teppich einer Gala"),
    ("realizacja-women-in-tech-wybieg", "", "Women in Tech Summit",
     "Humanoider Roboter auf dem pinken Laufsteg des Women in Tech Summit vor Publikum"),
    ("realizacja-lexai-starowka", "wide", "Die Straße bleibt stehen",
     "Humanoider Roboter im LEX-AI-Shirt in der Altstadt, Passanten fotografieren ihn"),
    ("realizacja-gala-detal", "narrow", "Bis ins Detail",
     "Nahaufnahme des humanoiden Roboters mit Krone und Paillettensmoking"),
    ("realizacja-gala-zdjecia-gosci", "wide", "Schlange am Fotobereich",
     "Galagäste fotografieren den humanoiden Roboter an der Sponsorenwand"),
    ("realizacja-robot-gala-dresden", "", "Gala in Dresden",
     "Humanoider Roboter Unitree G1 bei einer Gala in Dresden zwischen den Gästen"),
    ("realizacja-gala-palac", "", "Ballsaal",
     "Humanoider Roboter im Smoking im Inneren eines Palais-Ballsaals"),
    ("realizacja-gala-wsrod-gosci", "wide", "Mitten unter den Gästen",
     "Humanoider Roboter zwischen gut gelaunten Galagästen mit Sektgläsern"),
    ("realizacja-event-nad-woda", "", "Outdoor am Wasser",
     "Humanoider Roboter winkt auf einer Terrasse über einem Yachthafen"),
    ("realizacja-nocny-pokaz", "narrow", "Nachtshows",
     "Humanoider Roboter im roten Umhang bei einer Nachtshow vor einem historischen Gebäude"),
    ("realizacja-lexai-ulica", "", "Unterwegs für LEX AI",
     "Humanoider Roboter für LEX AI mit Aktentasche in der Altstadtgasse"),
    ("realizacja-spotkanie-biznesowe", "", "Business-Termin",
     "Humanoider Roboter im Firmenshirt auf der Terrasse bei einem Geschäftstermin"),
    ("robot-pies-branding-klienta", "", "Roboterhund im Kunden-Branding",
     "Roboterhund im Firmenshirt des Kunden bei einer Promotionaktion im Autohaus"),
    ("realizacja-robot-w-deszczu", "narrow", "Auch bei Regen",
     "Humanoider Roboter im roten Shirt hält bei Regen einen Regenschirm"),
    ("realizacja-robot-gala-portret", "", "Porträt",
     "Porträtaufnahme des humanoiden Roboters Unitree G1 im Galaoutfit"),
]

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


def og_for(out_file):
    """Obraz OG strony; gdy nie ma dedykowanego, wraca obraz domyślny serwisu."""
    candidate = f"og/{out_file.replace('.html', '.jpg')}"
    return candidate if os.path.exists(os.path.join(BASE, candidate)) else "og-image.jpg"


def city_name(pl_file):
    return de_cities.CITIES[pl_file]["name"]


# ── Wspólne fragmenty HTML ────────────────────────────────────────────
def gtm_head():
    """Tagi analityczne ładowane WYŁĄCZNIE po zgodzie użytkownika.

    Wymóg § 25 TDDDG (dawniej TTDSG) i art. 6 DSGVO: skrypty analityczne oraz
    identyfikatory w urządzeniu użytkownika wymagają uprzedniej, aktywnej zgody.
    Dlatego brak tu bezwarunkowego wstrzyknięcia GTM i brak wariantu <noscript>
    (ten ładowałby się bez zgody). Ładowanie realizuje consent.js.
    """
    if not ANALYTICS:
        return ("  <!-- Keine Analyse-Dienste eingebunden: Diese Seite setzt ausschließlich\n"
                "       technisch notwendige Cookies, eine Einwilligung ist nicht erforderlich. -->")
    return (f"""  <!-- Einwilligung (TDDDG/DSGVO): Analyse-Tags laden erst nach Zustimmung -->
  <script>window.dataLayer=window.dataLayer||[];window.__gtmId={GTM_ID!r};window.__albacrossId={ALBACROSS_ID!r};</script>
  <script src="consent.js" defer></script>""")


def gtm_body():
    return "  <!-- Kein GTM-noscript: würde ohne Einwilligung laden (§ 25 TDDDG) -->"


def nav_html(home="index.html"):
    return f"""  <a href="#hauptinhalt" class="skip-link">Zum Hauptinhalt springen</a>
  <div class="cursor-glow" id="cursorGlow" aria-hidden="true"></div>
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
  <main id="hauptinhalt" tabindex="-1">
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


def contact_section(h2, area="Deutschlandweit im Einsatz", location_ph="z. B. Berlin", date_text=False):
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
    consent_link = ('\n        <button type="button" class="footer__consent-link" '
                    'id="consentReopen">Datenschutz-Einstellungen</button>') if ANALYTICS else ""
    return f"""  </main>
  <footer class="footer">
    <div class="footer__inner">
      <div class="footer__brand">
        <span class="logo">33BOTS</span>
        <p class="footer__tagline"><a href="index.html" style="color:inherit; text-decoration:underline; text-underline-offset:2px;">Humanoide Roboter mieten</a> · Deutschlandweit</p>
        <div class="footer__nap">
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
        <a href="impressum.html">Impressum</a>
        <a href="datenschutz.html">Datenschutz</a>
        <a href="barrierefreiheit.html">Barrierefreiheit</a>{consent_link}
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

{consent_banner() if ANALYTICS else ""}
{a11y_widget()}
  <div class="sticky-cta">
    <a href="#kontakt" class="btn-primary">Termin anfragen →</a>
  </div>

  <script src="main.js" defer></script>
  <script src="a11y.js" defer></script>
</body>
</html>
"""


def consent_banner():
    """Baner zgody w modelu opt-in — równorzędne przyciski akceptacji i odrzucenia."""
    return """  <div class="consent" id="consentBanner" role="dialog" aria-modal="false"
       aria-labelledby="consentTitle" aria-describedby="consentText" hidden>
    <div class="consent__box">
      <h2 class="consent__title" id="consentTitle">Datenschutz-Einstellungen</h2>
      <p class="consent__text" id="consentText">
        Wir verwenden technisch notwendige Cookies, damit diese Website funktioniert. Zusätzlich möchten wir
        Analyse-Dienste (Google Tag Manager, Albacross) einsetzen, um die Nutzung der Website auszuwerten.
        Diese setzen wir nur mit Ihrer Einwilligung ein. Sie können Ihre Entscheidung jederzeit über den Link
        „Datenschutz-Einstellungen“ im Seitenfuß ändern.
        <a href="datenschutz.html" class="consent__link">Datenschutzerklärung</a> ·
        <a href="impressum.html" class="consent__link">Impressum</a>
      </p>
      <div class="consent__options" id="consentOptions" hidden>
        <label class="consent__opt">
          <input type="checkbox" checked disabled /> <span><strong>Notwendig</strong> — für den Betrieb der Website
          erforderlich, immer aktiv.</span>
        </label>
        <label class="consent__opt">
          <input type="checkbox" id="consentAnalytics" /> <span><strong>Analyse</strong> — Google Tag Manager und
          Albacross zur Auswertung der Websitenutzung.</span>
        </label>
      </div>
      <div class="consent__actions">
        <button type="button" class="consent__btn consent__btn--primary" id="consentAcceptAll">Alle akzeptieren</button>
        <button type="button" class="consent__btn" id="consentRejectAll">Nur notwendige</button>
        <button type="button" class="consent__btn consent__btn--ghost" id="consentSettings">Einstellungen</button>
        <button type="button" class="consent__btn consent__btn--primary" id="consentSave" hidden>Auswahl speichern</button>
      </div>
    </div>
  </div>
"""


def a11y_widget():
    """Panel dostępności — wymóg BFSG (Barrierefreiheitsstärkungsgesetz)."""
    return """  <button type="button" class="a11y-toggle" id="a11yToggle"
          aria-expanded="false" aria-controls="a11yPanel" aria-label="Barrierefreiheit-Einstellungen öffnen">
    <svg viewBox="0 0 24 24" aria-hidden="true" width="24" height="24" fill="currentColor">
      <circle cx="12" cy="4" r="2"/>
      <path d="M19 8h-5v13h-2v-6h-0.9v6H9V8H4V6h15v2z"/>
    </svg>
  </button>
  <div class="a11y-panel" id="a11yPanel" role="dialog" aria-labelledby="a11yTitle" hidden>
    <h2 class="a11y-panel__title" id="a11yTitle">Barrierefreiheit</h2>

    <fieldset class="a11y-group">
      <legend class="a11y-group__label">Textgrösse</legend>
      <div class="a11y-opts" role="group">
        <button type="button" class="a11y-opt" data-a11y="font" data-value="normal">Standard</button>
        <button type="button" class="a11y-opt" data-a11y="font" data-value="large">Gross</button>
        <button type="button" class="a11y-opt" data-a11y="font" data-value="xlarge">Sehr gross</button>
      </div>
    </fieldset>

    <fieldset class="a11y-group">
      <legend class="a11y-group__label">Darstellung</legend>
      <div class="a11y-opts" role="group">
        <button type="button" class="a11y-opt" data-a11y="theme" data-value="dark">Dunkel</button>
        <button type="button" class="a11y-opt" data-a11y="theme" data-value="light">Hell</button>
      </div>
    </fieldset>

    <fieldset class="a11y-group">
      <legend class="a11y-group__label">Kontrast</legend>
      <div class="a11y-opts" role="group">
        <button type="button" class="a11y-opt" data-a11y="contrast" data-value="normal">Standard</button>
        <button type="button" class="a11y-opt" data-a11y="contrast" data-value="high">Hoch</button>
      </div>
    </fieldset>

    <fieldset class="a11y-group">
      <legend class="a11y-group__label">Animationen</legend>
      <div class="a11y-opts" role="group">
        <button type="button" class="a11y-opt" data-a11y="motion" data-value="on">An</button>
        <button type="button" class="a11y-opt" data-a11y="motion" data-value="off">Aus</button>
      </div>
    </fieldset>

    <button type="button" class="a11y-reset" id="a11yReset">Zurücksetzen</button>
  </div>
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
    # Preload des Latin-Subsets: fonts/inter.css ist ein verketteter Request
    # (HTML -> CSS -> woff2). Der Preload holt die Datei parallel zum CSS,
    # damit der Textwechsel nach dem font-display:swap frueher passiert.
    # Deutsche Umlaute liegen komplett im Latin-Subset (U+0000-00FF).
    return f"""  <script>history.scrollRestoration = 'manual';</script>
  <link rel="icon" type="image/svg+xml" href="favicon.svg" />
  <link rel="preload" as="font" type="font/woff2" crossorigin
        href="fonts/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7.woff2" />
  <link rel="stylesheet" href="style.css?v=1" />
  <link rel="stylesheet" href="a11y.css?v=1" />
  <link rel="stylesheet" href="gallery.css?v=1" />
  <!-- Keine Verbindungen zu Dritten vor der Einwilligung: Analyse-Tags sind
       consent-gated, die Schrift Inter wird lokal ausgeliefert. -->
  <link rel="stylesheet" href="fonts/inter.css" />{extra_style}"""


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


def jpeg_size(path):
    """Liest Breite/Hoehe direkt aus dem JPEG-Header (kein Pillow noetig).

    Wird fuer width/height an den Galeriebildern gebraucht: ohne die Attribute
    kennt der Browser das Seitenverhaeltnis erst nach dem Laden und schiebt das
    Layout nach (CLS). Faellt eine Datei weg, liefern wir None und geben das
    Bild wie bisher ohne Attribute aus, statt den Build zu brechen.
    """
    import struct
    try:
        with open(path, 'rb') as f:
            if f.read(2) != b'\xff\xd8':
                return None
            while True:
                b = f.read(1)
                while b and b != b'\xff':
                    b = f.read(1)
                m = f.read(1)
                while m == b'\xff':
                    m = f.read(1)
                if not m:
                    return None
                if m in (b'\xc0', b'\xc1', b'\xc2', b'\xc3', b'\xc5', b'\xc6',
                         b'\xc7', b'\xc9', b'\xca', b'\xcb', b'\xcd', b'\xce', b'\xcf'):
                    f.read(3)
                    h, w = struct.unpack('>HH', f.read(4))
                    return w, h
                ln = struct.unpack('>H', f.read(2))[0]
                f.read(ln - 2)
    except (OSError, struct.error):
        return None


def gallery_items(limit=None):
    items = GALLERY[:limit] if limit else GALLERY
    out = []
    for slug, mod, cap, alt in items:
        cls = f"shot shot--{mod}" if mod else "shot"
        size = jpeg_size(os.path.join(OUT, f"{slug}.jpg"))
        dim = f' width="{size[0]}" height="{size[1]}"' if size else ""
        out.append(f"""        <figure class="{cls}">
          <picture>
            <source srcset="{slug}.webp" type="image/webp" />
            <img src="{slug}.jpg" alt="{alt}"{dim} loading="lazy" decoding="async" class="shot__img" />
          </picture>
          <figcaption class="shot__cap">{cap}</figcaption>
        </figure>""")
    return "\n".join(out)


def gallery_section(limit=None, tag="Realisierungen",
                    heading="Aufnahmen aus<br />echten Einsätzen",
                    lead=None, more_link=True):
    lead_html = f'\n      <p class="shots__lead">{lead}</p>' if lead else ""
    more = (f'\n      <div class="shots__more">\n'
            f'        <a href="{de("realizacje-wideo.html")}" class="btn-ghost" style="display:inline-flex;">'
            f'Alle Referenzen ansehen →</a>\n      </div>' if more_link else "")
    return f"""  <section class="section shots-section" id="realisierungen">
    <div class="section-header">
      <span class="tag">{tag}</span>
      <h2 class="section-title">{heading}</h2>
    </div>
    <div class="shots-wrap">{lead_html}
      <div class="shots">
{gallery_items(limit)}
      </div>{more}
    </div>
  </section>
"""


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
                     "email": EMAIL},
        "areaServed": {"@type": "Country", "name": "Deutschland"},
        "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR",
                   "lowPrice": PRICE_LOW,
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

    og_image = og_for(out_file)

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
{render_guides(de_structure.GUIDES[p.get('guides', 'default')])}
      </div>
    </div>
  </section>

  <!-- REALISIERUNGEN -->
  <section class="section" style="padding-top:0;">
    <div class="shots-wrap">
      <p style="font-size:0.75rem; color:var(--text-3); text-transform:uppercase; letter-spacing:0.1em; font-weight:700; margin-bottom:var(--s3);">Aus echten Einsätzen</p>
      <div class="shots shots--strip">
{gallery_items(6)}
      </div>
      <div class="shots__more">
        <a href="{de('realizacje-wideo.html')}" class="btn-ghost" style="display:inline-flex;">Alle Referenzen ansehen →</a>
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


# ── Textvarianten für Stadtseiten ───────────────────────────────────────
# 34 Stadtseiten teilten sich bisher wortgleiche Absätze (Kacheln, "einfachster
# Weg"-Satz, Anfahrt-Absatz, Szenario-Intro) — ~35 % identische Sätze zwischen
# je zwei Städten (gemessen). Reines Duplicate-Content-Risiko für nahezu
# identische lokale Landingpages. Rotation nach Stadt-Slug (deterministisch,
# gleiches Verfahren wie in de_content_helpers._pick) verteilt mehrere
# Formulierungen, ohne 34 Städte einzeln von Hand umschreiben zu müssen.
def _city_seed(slug):
    return sum(ord(c) for c in slug)


def _city_pick(pool, slug, offset=0):
    return pool[(_city_seed(slug) + offset) % len(pool)]


TILE1_POOL = [
    ("Sichtbarkeit", "Menschen bleiben stehen",
     "Der G1 zieht Aufmerksamkeit aus mehreren Dutzend Metern Entfernung an. Ihr Stand oder Ihre Veranstaltung wird zum meistbesuchten Punkt im Raum."),
    ("Sichtbarkeit", "Der Blickfang der Veranstaltung",
     "Kaum ist der G1 im Raum, richten sich die Blicke auf ihn. Für Standbesucher und Gäste wird er zum ersten Gesprächsthema des Tages."),
    ("Sichtbarkeit", "Publikum, das stehen bleibt",
     "Ein humanoider Roboter mitten im Geschehen sorgt für spontane Trauben von Neugierigen — genau der Effekt, den ein ruhiger Messestand allein nicht erzeugt."),
]
TILE2_POOL = [
    ("Reichweite", "Organisches Social Media",
     "Fotos und Clips mit dem Roboter landen noch während der Veranstaltung in den sozialen Medien. Ihre Marke erscheint in Hunderten Beiträgen — ohne Mediabudget."),
    ("Reichweite", "Content, der sich von selbst verbreitet",
     "Gäste filmen und fotografieren den Roboter aus eigenem Antrieb und teilen es sofort. Ihr Logo ist auf jedem dieser Beiträge zu sehen."),
    ("Reichweite", "Reichweite ohne Werbebudget",
     "Der Auftritt des Roboters erzeugt organischen Content: Storys, Reels und Posts der Gäste, die Ihre Marke ohne zusätzliche Kosten weitertragen."),
]
EINFACHSTER_WEG_POOL = [
    "Die Miete eines humanoiden Roboters Unitree G1 in {city} ist der einfachste Weg, sich in einem dichten Veranstaltungsmarkt abzuheben. Wir liefern den G1 direkt an Ihre Location. Bedient werden {around}.",
    "Wer sich in {city} von der üblichen Messe- und Eventkulisse abheben will, bucht den Unitree G1 als Showact. Wir bringen ihn direkt zu Ihrer Location — bedient werden {around}.",
    "In einem Markt voller ähnlicher Standkonzepte ist der Unitree G1 in {city} ein direkter Weg zu mehr Aufmerksamkeit. Anlieferung erfolgt direkt zur Location, bedient werden {around}.",
]
SZENARIO_INTRO_POOL = [
    "Wir betreuen in {city} jede Art von Veranstaltung — von Messen und Konferenzen bis zu privaten Feiern. Sehen Sie, wie sich der Roboter im konkreten Szenario schlägt:",
    "Ob Firmenevent, Messeauftritt oder private Feier — in {city} passen wir den Auftritt des Roboters an Ihren Anlass an. Ein Überblick nach Szenario:",
    "Vom Messestand bis zur Hochzeitsfeier: In {city} kommt der Roboter in ganz unterschiedlichen Formaten zum Einsatz. Wählen Sie Ihr Szenario:",
]
ANFAHRT_POOL = [
    "Zu jeder Location in {city} kommen wir mit eigener Technik — bedient werden {around}. Der Roboter braucht vor Ort rund 2×2 m ebene Fläche und eine 230-V-Steckdose; wir bringen ihn selbst herein und sind in der Regel 30–45 Minuten vor Veranstaltungsbeginn einsatzbereit. Schreiben Sie uns, wo Ihre Veranstaltung in {city} stattfindet, und Sie erhalten innerhalb von 24 Stunden ein konkretes Angebot.",
    "Wir reisen mit eigenem Equipment zu jeder Location in {city} an — dazu zählen {around}. Benötigt wird vor Ort eine ebene Fläche von rund 2×2 m und ein 230-V-Anschluss; Aufbau und Einrichtung übernehmen wir selbst, üblicherweise 30–45 Minuten vor Beginn. Teilen Sie uns den Ort Ihrer Veranstaltung in {city} mit — das Angebot folgt innerhalb von 24 Stunden.",
    "Die Anreise zu Ihrer Location in {city} organisieren wir komplett selbst — das gilt für {around} ebenso. Vor Ort braucht der Roboter etwa 2×2 m freie Fläche und eine 230-V-Steckdose; Aufbau und Funktionstest dauern rund 30–45 Minuten vor Veranstaltungsbeginn. Nennen Sie uns den Veranstaltungsort in {city}, das Angebot erhalten Sie binnen 24 Stunden.",
]


# ── Strona miasta (35 sztuk) ──────────────────────────────────────────
def build_city_page(pl_file):
    d = de_cities.CITIES[pl_file]
    out_file = SLUG_MAP[pl_file]
    url = f"{DOMAIN}/{out_file}"
    city = d["name"]
    video = VIDEOS["taniec"]

    tile1 = _city_pick(TILE1_POOL, pl_file)
    tile2 = _city_pick(TILE2_POOL, pl_file, offset=1)
    einfachster_weg = _city_pick(EINFACHSTER_WEG_POOL, pl_file, offset=2).format(city=city, around=d["around"])
    szenario_intro = _city_pick(SZENARIO_INTRO_POOL, pl_file, offset=3).format(city=city)
    anfahrt_text = _city_pick(ANFAHRT_POOL, pl_file, offset=4).format(city=city, around=d["around"])

    faqs = list(d["faq"]) + [
        (f"Kommen Sie auch nach {city}?",
         f"Ja — wir sind deutschlandweit im Einsatz, auch in {city}. Anfahrt und Logistik stimmen wir "
         f"vorab ab und halten sie im Angebot fest."),
        (f"Was kostet die Miete eines Roboters in {city}?",
         f"{PRICE_FROM} pro kompletten Veranstaltungstag. Der genaue Betrag hängt von Veranstaltungsort "
         f"und Umfang der Show ab; Sie erhalten ein individuelles Angebot. Ab zwei Tagen erhalten Sie "
         f"15 % Rabatt auf jeden Tag."),
    ]

    # Ohne den Zusatz „— Roboter für Events": mit langen Stadtnamen (Frankfurt am
    # Main, Mönchengladbach) lief der Titel sonst auf 71–73 Zeichen und wurde in
    # den Suchergebnissen abgeschnitten. Das lokale Keyword steht vorne.
    title = f"Humanoiden Roboter mieten {city} | 33bots"
    desc = (f"Humanoiden Roboter Unitree G1 in {city} mieten — Messen, Konferenzen, Galas. Mit "
            f"zertifiziertem Operator vor Ort. Angebot in 24 h →")

    service_json = json.dumps({
        "@context": "https://schema.org", "@type": "Service",
        "name": f"Humanoiden Roboter mieten — {city}",
        "description": f"Vermietung des Roboters Unitree G1 für Events, Konferenzen und Messen in {city}. "
                       f"Mit zertifiziertem Operator vor Ort.",
        "url": url, "image": f"{DOMAIN}/robot-g1.jpg",
        "serviceType": "Vermietung humanoider Roboter für Events",
        "provider": {"@type": "LocalBusiness", "name": "33bots – Humanoide Roboter mieten",
                     "url": DOMAIN, "email": EMAIL,
                     "sameAs": ["https://www.facebook.com/33bots", "https://www.instagram.com/33bots_/",
                                "https://www.linkedin.com/company/33bots", "https://www.tiktok.com/@aimforum"]},
        "areaServed": {"@type": "City", "name": city},
        "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR",
                   "lowPrice": PRICE_LOW,
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

    og_image = og_for(out_file)

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
        <span class="hero__trust-item">✓ Zertifizierter Operator vor Ort</span>
        <span class="hero__trust-item">✓ Deutschlandweit im Einsatz</span>
        <span class="hero__trust-item">✓ Angebot in 24 h</span>
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
        <div class="tile__top"><span class="tile__tag">{tile1[0]}</span></div>
        <h3 class="tile__title">{tile1[1]}</h3>
        <p class="tile__desc">{tile1[2]}</p>
        <a href="#kontakt" class="tile__link">Angebot anfragen →</a>
      </div>
      <div class="tile tile--light">
        <div class="tile__top"><span class="tile__tag">{tile2[0]}</span></div>
        <h3 class="tile__title">{tile2[1]}</h3>
        <p class="tile__desc">{tile2[2]}</p>
        <a href="#kontakt" class="tile__link">Angebot anfragen →</a>
      </div>
      <div class="tile">
        <div class="tile__top"><span class="tile__tag">Anfahrt</span></div>
        <h3 class="tile__title">Deutschlandweit vor Ort</h3>
        <p class="tile__desc">Wir bringen den Roboter zu Ihrer Location in {city}. Anfahrt und Logistik planen wir gemeinsam und halten sie im Angebot fest.</p>
        <a href="#kontakt" class="tile__link">Angebot anfragen →</a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="onas-body" style="max-width:860px; margin:0 auto;">
      <div class="onas-text">
        <h2 class="section-title" style="font-size:clamp(1.8rem,3vw,2.8rem); margin-bottom:var(--s4);">{d['section_title']}</h2>
        <p class="lead-text">{d['p1']}</p>
        <p class="body-text">{einfachster_weg}</p>

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
      <div class="shots shots--strip" style="margin-bottom:var(--s4);">
{gallery_items(6)}
      </div>
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
      <p style="color:var(--text-2); font-size:0.9rem; margin-bottom:var(--s3);">{szenario_intro}</p>
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
        <p class="body-text">{anfahrt_text}</p>
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


def check_assets():
    """Zasoby leżą w katalogu serwisu na stałe — sprawdzamy tylko kompletność."""
    required = ["style.css", "favicon.svg", "logo.png", "og-image.jpg",
                "robot-g1.jpg", "robot-g1.webp", "robot-g1-960.webp",
                "robot-g1-action.jpg", "robot-g1-action.webp",
                "fonts/inter.css", "video/33bots-robot-event.mp4"]
    required += [f"{slug}.jpg" for slug, _m, _c, _a in GALLERY]
    required += [f"{slug}.webp" for slug, _m, _c, _a in GALLERY]
    missing = [r for r in required if not os.path.exists(os.path.join(BASE, r))]
    if missing:
        raise SystemExit("Brakuje zasobów:\n  " + "\n  ".join(missing[:20]))


def build_gallery_css():
    """Galeria zdjęć z realizacji — mozaika w tokenach style.css."""
    return """/* ─────────────────────────────────────────────────────────────
   Realisierungen — Fotogalerie
   Nutzt ausschliesslich die Design-Tokens aus style.css, damit die
   Optik mit dem uebrigen Layout identisch bleibt.
   ───────────────────────────────────────────────────────────── */

.shots-wrap{max-width:1200px;margin:0 auto;padding:0 var(--s5);}
.shots__lead{color:var(--text-2);font-size:1rem;line-height:1.75;max-width:660px;
  margin:0 auto var(--s6);text-align:center;}

.shots{display:grid;gap:var(--s3);
  grid-template-columns:repeat(auto-fill,minmax(220px,1fr));
  grid-auto-flow:dense;}

.shot{position:relative;margin:0;overflow:hidden;border-radius:14px;
  border:1px solid var(--border-mid);background:var(--surface-2);
  aspect-ratio:4/5;}
.shot--wide{grid-column:span 2;aspect-ratio:16/10;}
.shot--narrow{aspect-ratio:3/4;}

.shot__img{width:100%;height:100%;object-fit:cover;display:block;
  transition:transform .5s ease;}
.shot:hover .shot__img,.shot:focus-within .shot__img{transform:scale(1.04);}

.shot__cap{position:absolute;left:0;right:0;bottom:0;
  padding:28px 14px 12px;font-size:.82rem;font-weight:600;color:#fff;
  background:linear-gradient(to top,rgba(0,0,0,.78),rgba(0,0,0,0));
  letter-spacing:-.01em;}

.shots__more{display:flex;justify-content:center;margin-top:var(--s6);}

/* Helle Darstellung: Rahmen etwas kraeftiger, damit die Kacheln stehen */
html[data-a11y-theme="light"] .shot{border-color:#c2c2cc;}

/* Hoher Kontrast: Bildunterschriften ohne Verlauf, voll deckend */
html[data-a11y-contrast="high"] .shot__cap{background:#000;padding:10px 14px;}
html[data-a11y-theme="light"][data-a11y-contrast="high"] .shot__cap{
  background:#000;color:#fff;}

/* Animationen aus: kein Zoom beim Hover */
html[data-a11y-motion="off"] .shot__img{transition:none;}
html[data-a11y-motion="off"] .shot:hover .shot__img{transform:none;}

/* Kompakter Streifen auf Stadt- und Unterseiten */
.shots--strip{grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:var(--s2);}
.shots--strip .shot{aspect-ratio:1/1;}
.shots--strip .shot--wide{grid-column:span 2;aspect-ratio:2/1;}
.shots--strip .shot--narrow{aspect-ratio:1/1;}
.shots--strip .shot__cap{font-size:.72rem;padding:22px 10px 9px;}

@media (max-width:900px){
  .shots{grid-template-columns:repeat(auto-fill,minmax(160px,1fr));}
}
@media (max-width:560px){
  .shots{grid-template-columns:repeat(2,1fr);}
  .shot--wide{grid-column:span 2;}
  .shots-wrap{padding:0 var(--s4);}
}
"""


def build_a11y_css():
    """Style panelu dostępności, banera zgody i trybów kontrastu/rozmiaru tekstu."""
    return """/* ─────────────────────────────────────────────────────────────
   Barrierefreiheit (BFSG) + Consent (TDDDG/DSGVO)
   Ergänzt style.css und überschreibt nur, was für die
   Bedienhilfen nötig ist.
   ───────────────────────────────────────────────────────────── */

/* Sprunglink für Tastaturnutzung */
.skip-link{position:absolute;left:-9999px;top:0;z-index:10000;padding:12px 20px;
  background:#fff;color:#000;font-weight:700;border-radius:0 0 8px 0;}
.skip-link:focus{left:0;}

/* Sichtbarer Fokus auf allen interaktiven Elementen */
a:focus-visible,button:focus-visible,input:focus-visible,textarea:focus-visible,
select:focus-visible,[tabindex]:focus-visible{
  outline:3px solid #ff6a3d;outline-offset:2px;border-radius:4px;}
main:focus{outline:none;}

/* ── Textgrösse ───────────────────────────────────────────── */
html[data-a11y-font="large"]{font-size:112.5%;}
html[data-a11y-font="xlarge"]{font-size:131.25%;}

/* ── Helles Erscheinungsbild ──────────────────────────────── */
html[data-a11y-theme="light"]{
  --bg:#ffffff;--surface-1:#f5f5f7;--surface-2:#ececef;
  --text:#101014;--text-1:#101014;--text-2:#3a3a42;--text-3:#5f5f6b;
  --border:#d3d3da;--border-mid:#c2c2cc;}
html[data-a11y-theme="light"] body{background:#fff;color:#101014;}
html[data-a11y-theme="light"] .cursor-glow,
html[data-a11y-theme="light"] .hero__spotlight,
html[data-a11y-theme="light"] .robot-scan{display:none;}
html[data-a11y-theme="light"] .tile--light{background:#101014;color:#fff;}

/* ── Hoher Kontrast ───────────────────────────────────────── */
html[data-a11y-contrast="high"]{--text-2:#f2f2f2;--text-3:#e2e2e2;--border-mid:#8a8a95;}
html[data-a11y-contrast="high"] body{background:#000;}
html[data-a11y-contrast="high"] .tile__desc,
html[data-a11y-contrast="high"] .body-text,
html[data-a11y-contrast="high"] p{color:#f2f2f2;}
html[data-a11y-contrast="high"] a{text-decoration:underline;}
html[data-a11y-theme="light"][data-a11y-contrast="high"]{--text-2:#000;--text-3:#1a1a1a;--border-mid:#555;}
html[data-a11y-theme="light"][data-a11y-contrast="high"] .tile__desc,
html[data-a11y-theme="light"][data-a11y-contrast="high"] .body-text,
html[data-a11y-theme="light"][data-a11y-contrast="high"] p{color:#000;}

/* ── Animationen aus ──────────────────────────────────────── */
html[data-a11y-motion="off"] *,
html[data-a11y-motion="off"] *::before,
html[data-a11y-motion="off"] *::after{
  animation-duration:0.001ms !important;animation-iteration-count:1 !important;
  transition-duration:0.001ms !important;scroll-behavior:auto !important;}
html[data-a11y-motion="off"] .cursor-glow,
html[data-a11y-motion="off"] .robot-scan{display:none !important;}
@media (prefers-reduced-motion: reduce){
  *,*::before,*::after{animation-duration:0.001ms !important;transition-duration:0.001ms !important;}
  .cursor-glow,.robot-scan{display:none !important;}
}

/* ── Panel Barrierefreiheit ───────────────────────────────── */
.a11y-toggle{position:fixed;left:20px;bottom:20px;z-index:9998;width:52px;height:52px;
  border-radius:50%;border:1px solid var(--border-mid,#333);background:var(--surface-2,#1a1a1f);
  color:var(--text,#fff);display:flex;align-items:center;justify-content:center;cursor:pointer;
  box-shadow:0 4px 18px rgba(0,0,0,.35);}
.a11y-toggle:hover{border-color:#ff6a3d;}
.a11y-panel{position:fixed;left:20px;bottom:84px;z-index:9999;width:min(340px,calc(100vw - 40px));
  padding:24px;border-radius:16px;border:1px solid var(--border-mid,#333);
  background:var(--surface-1,#151519);box-shadow:0 12px 40px rgba(0,0,0,.5);
  max-height:calc(100vh - 120px);overflow-y:auto;}
.a11y-panel[hidden]{display:none;}
.a11y-panel__title{font-size:1.15rem;font-weight:700;margin:0 0 18px;color:var(--text,#fff);}
.a11y-group{border:0;padding:0;margin:0 0 18px;}
.a11y-group__label{font-size:.72rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;
  color:var(--text-3,#8b8b95);padding:0;margin:0 0 8px;}
.a11y-opts{display:flex;gap:8px;flex-wrap:wrap;}
.a11y-opt{flex:1 1 auto;min-width:90px;padding:12px 10px;border-radius:10px;cursor:pointer;
  border:1px solid var(--border-mid,#333);background:transparent;color:var(--text,#fff);
  font-size:.95rem;font-weight:600;font-family:inherit;}
.a11y-opt:hover{border-color:#ff6a3d;}
.a11y-opt[aria-pressed="true"]{border-color:#ff6a3d;color:#ff6a3d;}
.a11y-reset{background:none;border:0;padding:0;cursor:pointer;font-family:inherit;
  color:var(--text,#fff);font-size:.9rem;text-decoration:underline;text-underline-offset:3px;}

/* ── Consent-Banner ───────────────────────────────────────── */
.consent{position:fixed;inset:auto 0 0 0;z-index:10000;padding:16px;display:flex;justify-content:center;}
.consent[hidden]{display:none;}
.consent__box{width:min(760px,100%);padding:24px;border-radius:16px;
  border:1px solid var(--border-mid,#333);background:var(--surface-1,#151519);
  box-shadow:0 -8px 40px rgba(0,0,0,.5);}
.consent__title{font-size:1.1rem;font-weight:700;margin:0 0 8px;color:var(--text,#fff);}
.consent__text{font-size:.9rem;line-height:1.65;color:var(--text-2,#c3c3cc);margin:0 0 16px;}
.consent__link{color:var(--text,#fff);text-decoration:underline;text-underline-offset:3px;}
.consent__options{display:grid;gap:10px;margin:0 0 16px;}
.consent__opt{display:flex;gap:10px;align-items:flex-start;font-size:.88rem;line-height:1.55;
  color:var(--text-2,#c3c3cc);}
.consent__opt strong{color:var(--text,#fff);}
.consent__actions{display:flex;gap:10px;flex-wrap:wrap;}
.consent__btn{padding:12px 20px;border-radius:10px;cursor:pointer;font-family:inherit;
  font-size:.92rem;font-weight:700;border:1px solid var(--border-mid,#333);
  background:transparent;color:var(--text,#fff);}
.consent__btn:hover{border-color:#ff6a3d;}
.consent__btn--primary{background:#ff6a3d;border-color:#ff6a3d;color:#0b0b0d;}
.consent__btn--ghost{border-style:dashed;}
.footer__consent-link{background:none;border:0;padding:0;cursor:pointer;font-family:inherit;
  font-size:inherit;color:inherit;text-align:left;text-decoration:underline;text-underline-offset:3px;}

@media (max-width:640px){
  .a11y-toggle{left:12px;bottom:12px;}
  .a11y-panel{left:12px;right:12px;bottom:74px;width:auto;}
  .consent__actions .consent__btn{flex:1 1 100%;}
}
"""


def build_a11y_js():
    """Logika panelu dostępności — ustawienia zapisywane lokalnie u użytkownika."""
    return """/* Barrierefreiheit-Panel (BFSG).
   Einstellungen werden ausschliesslich lokal im Browser gespeichert
   (localStorage) und nicht an den Server uebertragen. */
(function () {
  'use strict';
  var KEY = 'a11y-prefs';
  var DEFAULTS = { font: 'normal', theme: 'dark', contrast: 'normal', motion: 'on' };
  var root = document.documentElement;

  function load() {
    try { return Object.assign({}, DEFAULTS, JSON.parse(localStorage.getItem(KEY) || '{}')); }
    catch (e) { return Object.assign({}, DEFAULTS); }
  }
  function save(p) {
    try { localStorage.setItem(KEY, JSON.stringify(p)); } catch (e) { /* Speicher gesperrt */ }
  }
  function apply(p) {
    root.setAttribute('data-a11y-font', p.font);
    root.setAttribute('data-a11y-theme', p.theme);
    root.setAttribute('data-a11y-contrast', p.contrast);
    root.setAttribute('data-a11y-motion', p.motion);
    document.querySelectorAll('.a11y-opt').forEach(function (b) {
      b.setAttribute('aria-pressed', String(p[b.dataset.a11y] === b.dataset.value));
    });
  }

  var prefs = load();
  apply(prefs);

  var toggle = document.getElementById('a11yToggle');
  var panel = document.getElementById('a11yPanel');
  if (!toggle || !panel) return;

  function open(state) {
    panel.hidden = !state;
    toggle.setAttribute('aria-expanded', String(state));
    toggle.setAttribute('aria-label', state
      ? 'Barrierefreiheit-Einstellungen schliessen'
      : 'Barrierefreiheit-Einstellungen oeffnen');
    if (state) { var f = panel.querySelector('.a11y-opt'); if (f) f.focus(); }
  }

  toggle.addEventListener('click', function () { open(panel.hidden); });

  panel.addEventListener('click', function (e) {
    var btn = e.target.closest('.a11y-opt');
    if (!btn) return;
    prefs[btn.dataset.a11y] = btn.dataset.value;
    save(prefs);
    apply(prefs);
  });

  var reset = document.getElementById('a11yReset');
  if (reset) reset.addEventListener('click', function () {
    prefs = Object.assign({}, DEFAULTS);
    save(prefs);
    apply(prefs);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !panel.hidden) { open(false); toggle.focus(); }
  });
  document.addEventListener('click', function (e) {
    if (!panel.hidden && !panel.contains(e.target) && !toggle.contains(e.target)) open(false);
  });
})();
"""


def build_consent_js():
    """Zgoda na cookies w modelu opt-in — tagi ładowane dopiero po akceptacji."""
    return """/* Cookie-Einwilligung nach § 25 TDDDG und Art. 6 DSGVO.
   Analyse-Dienste (Google Tag Manager, Albacross) werden erst nach
   ausdruecklicher Einwilligung geladen. Ohne Einwilligung laeuft die
   Website vollstaendig ohne diese Dienste. */
(function () {
  'use strict';
  var KEY = 'consent-v1';
  var loaded = false;

  function read() {
    try { return JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) { return null; }
  }
  function write(v) {
    try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) { /* Speicher gesperrt */ }
  }

  function loadAnalytics() {
    if (loaded) return;
    loaded = true;
    var id = window.__gtmId;
    if (id) {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });
      var g = document.createElement('script');
      g.async = true;
      g.src = 'https://www.googletagmanager.com/gtm.js?id=' + id;
      document.head.appendChild(g);
    }
    if (window.__albacrossId) {
      window._nQc = window.__albacrossId;
      var a = document.createElement('script');
      a.async = true;
      a.src = 'https://serve.albacross.com/track.js';
      document.head.appendChild(a);
    }
  }

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  var stored = read();
  if (stored && stored.analytics) loadAnalytics();

  ready(function () {
    var banner = document.getElementById('consentBanner');
    if (!banner) return;
    var options = document.getElementById('consentOptions');
    var analytics = document.getElementById('consentAnalytics');
    var btnAll = document.getElementById('consentAcceptAll');
    var btnNone = document.getElementById('consentRejectAll');
    var btnSettings = document.getElementById('consentSettings');
    var btnSave = document.getElementById('consentSave');
    var reopen = document.getElementById('consentReopen');

    function show() {
      banner.hidden = false;
      var s = read();
      if (analytics) analytics.checked = !!(s && s.analytics);
    }
    function decide(useAnalytics) {
      write({ analytics: !!useAnalytics, ts: Date.now() });
      if (useAnalytics) loadAnalytics();
      banner.hidden = true;
    }

    if (!stored) show();

    if (btnAll) btnAll.addEventListener('click', function () { decide(true); });
    if (btnNone) btnNone.addEventListener('click', function () { decide(false); });
    if (btnSettings) btnSettings.addEventListener('click', function () {
      if (options) options.hidden = false;
      btnSettings.hidden = true;
      if (btnSave) btnSave.hidden = false;
    });
    if (btnSave) btnSave.addEventListener('click', function () {
      decide(analytics && analytics.checked);
    });
    if (reopen) reopen.addEventListener('click', function (e) {
      e.preventDefault();
      if (options) options.hidden = false;
      if (btnSettings) btnSettings.hidden = true;
      if (btnSave) btnSave.hidden = false;
      show();
      banner.scrollIntoView({ block: 'nearest' });
    });
  });
})();
"""


def build_robots():
    return f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n"


def build_redirects():
    host = DOMAIN.replace("https://", "")
    return (f"https://www.{host}/* {DOMAIN}/:splat 301!\n"
            f"http://www.{host}/* {DOMAIN}/:splat 301!\n"
            f"http://{host}/* {DOMAIN}/:splat 301!\n")


def build_htaccess():
    """Apache-Pendant zu _redirects (das nur auf Netlify greift).

    Wird mitgeneriert, damit die Datei nicht auf eine fremde Domain zeigen
    kann: die vorherige Version stammte aus dem polnischen Projekt und hat
    jeden Aufruf auf 33bots.pl umgeleitet. Zusaetzlich Kompression und
    Cache-Header — beides betrifft jede Seite und ist der groesste Hebel
    fuer die Ladezeit auf klassischem Apache-Hosting.
    """
    host = DOMAIN.replace("https://", "")
    # 14 schwache Branchen-Seiten wurden in event-attraktionen.html konsolidiert
    # (Duplicate-Content-Reduktion, siehe de_structure.py/de_content_pages2.py) —
    # alte URLs muessen dauerhaft (301) auf die neue Zielseite zeigen, statt 404.
    consolidated_target = SLUG_MAP["atrakcje-na-event.html"]
    consolidated_sources = [
        "roboter-medizin-event.html", "roboter-pharma-event.html", "roboter-bau-event.html",
        "roboter-energie-event.html", "roboter-telekom-event.html", "roboter-gastro-event.html",
        "roboter-tourismus-event.html", "roboter-kultur-event.html", "roboter-beauty-event.html",
        "roboter-nachhaltigkeits-event.html", "roboter-stadt-event.html", "roboter-outdoor-event.html",
        "roboter-hybrid-event.html", "roboter-vip-event.html",
    ]
    consolidated_rules = "\n".join(
        f"RewriteRule ^{src.replace('.', chr(92) + '.')}$ /{consolidated_target} [L,R=301]"
        for src in consolidated_sources
    )
    return f"""# Automatisch erzeugt von build/generate_site.py — nicht von Hand aendern.
RewriteEngine On

# Kanonische Adresse: HTTPS ohne www ({DOMAIN})
# Getrennte Regeln mit X-Forwarded-Proto: hinter einem Proxy/Load Balancer
# meldet %{{HTTPS}} dauerhaft "off" — kombiniert mit [OR] gibt das eine
# Redirect-Schleife.
RewriteCond %{{HTTPS}} off
RewriteCond %{{HTTP:X-Forwarded-Proto}} !https
RewriteRule ^(.*)$ {DOMAIN}/$1 [L,R=301]

RewriteCond %{{HTTP_HOST}} ^www\\.{host.replace('.', chr(92) + '.')}$ [NC]
RewriteRule ^(.*)$ {DOMAIN}/$1 [L,R=301]

# ── Konsolidierte Branchen-Seiten → {consolidated_target} ──────────────
{consolidated_rules}

ErrorDocument 404 /404.html

# ── Kompression ──────────────────────────────────────────────────────
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css text/plain text/xml
  AddOutputFilterByType DEFLATE application/javascript application/x-javascript
  AddOutputFilterByType DEFLATE application/json application/xml
  AddOutputFilterByType DEFLATE application/rss+xml image/svg+xml
</IfModule>
<IfModule mod_brotli.c>
  AddOutputFilterByType BROTLI_COMPRESS text/html text/css text/plain text/xml
  AddOutputFilterByType BROTLI_COMPRESS application/javascript application/json
  AddOutputFilterByType BROTLI_COMPRESS application/rss+xml image/svg+xml
</IfModule>

# ── Cache ────────────────────────────────────────────────────────────
# HTML kurz (Inhalte sollen nach dem Deploy sofort sichtbar sein), statische
# Dateien lang: CSS/JS haengen an ?v=, Bilder und Videos wechseln den Namen.
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/html                 "access plus 10 minutes"
  ExpiresByType text/css                  "access plus 1 year"
  ExpiresByType application/javascript    "access plus 1 year"
  ExpiresByType image/jpeg                "access plus 1 year"
  ExpiresByType image/png                 "access plus 1 year"
  ExpiresByType image/webp                "access plus 1 year"
  ExpiresByType image/svg+xml             "access plus 1 year"
  ExpiresByType video/mp4                 "access plus 1 year"
  ExpiresByType font/woff2                "access plus 1 year"
  ExpiresByType application/rss+xml       "access plus 1 hour"
</IfModule>
<IfModule mod_headers.c>
  <FilesMatch "\\.(css|js|jpg|jpeg|png|webp|svg|mp4|woff2)$">
    Header set Cache-Control "public, max-age=31536000, immutable"
  </FilesMatch>
  <FilesMatch "\\.html$">
    Header set Cache-Control "public, max-age=600, must-revalidate"
  </FilesMatch>
</IfModule>
"""


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
    check_assets()
    write("a11y.css", build_a11y_css())
    write("gallery.css", build_gallery_css())
    write("a11y.js", build_a11y_js())
    if ANALYTICS:
        write("consent.js", build_consent_js())

    # 98 podstron SEO
    for p in de_structure.PAGES:
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
    write(".htaccess", build_htaccess())

    # index.html wird nicht mehr von build_index() geschrieben (siehe
    # de_pages_manual.py) und steht damit nicht mehr in WRITTEN — für die
    # Sitemap zaehlt das nicht: die Startseite existiert weiterhin als Datei
    # und gehoert mit Prioritaet 1.0 hinein.
    html_pages = sorted({f for f in WRITTEN if f.endswith(".html") and f != "404.html"} | {"index.html"})
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

    required = dict(COMPANY)
    if not ANALYTICS:
        required.pop("gtm_services", None)
    empty = [k for k, v in required.items() if not v.strip()]
    if not ANALYTICS:
        print("\nAnalityka wyłączona (GTM_ID i ALBACROSS_ID puste) — strona nie ustawia\n"
              "żadnych cookies poza niezbędnymi, baner zgody nie jest renderowany.")
    if empty:
        print()
        print("!" * 72)
        print("NIE PUBLIKUJ JESZCZE — brak danych rejestrowych w Impressum/Datenschutz.")
        print(f"Nieuzupełnione pola ({len(empty)}) w COMPANY na górze build/generate_site.py:")
        for k in empty:
            print(f"  - {k}")
        print("Niekompletne Impressum jest w Niemczech abmahnfähig.")
        print("!" * 72)


if __name__ == "__main__":
    main()
