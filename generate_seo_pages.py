#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator podstron SEO (usługi, role robota, miejsca, typy eventów, eventy
branżowe, imprezy prywatne) — wzorowany na robot-na-wesele.html.
Uruchomienie: python3 generate_seo_pages.py
Generuje pliki .html w katalogu repo i dopisuje nowe URL-e do sitemap.xml.
"""

import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://33bots.pl"
LASTMOD = "2026-07-17"

# ---------------------------------------------------------------- wideo
VIDEOS = {
    "taniec": {
        "file": "video/robot-taniec.mp4", "poster": "video/robot-taniec-poster.jpg",
        "duration": "PT17S", "w": 324, "h": 576,
        "name": "Robot humanoidalny tańczy — pokaz choreografii",
        "desc": "Robot Unitree G1 wykonuje układ choreograficzny zsynchronizowany z muzyką. Kulminacyjny moment każdego pokazu.",
        "caption": "Unitree G1 w trakcie choreografii. Ten układ na żywo robi największe wrażenie — goście wyciągają telefony w kilka sekund.",
    },
    "powitanie": {
        "file": "video/robot-powitanie.mp4", "poster": "video/robot-powitanie-poster.jpg",
        "duration": "PT12S", "w": 324, "h": 576,
        "name": "Robot humanoidalny wita gości",
        "desc": "Robot Unitree G1 wita gości gestem i głosem. Tak wygląda pierwsze wrażenie, którego nikt nie zapomina.",
        "caption": "Unitree G1 wita gości przy wejściu. Pierwsze wrażenie, które ustawia całe wydarzenie.",
    },
    "gesty": {
        "file": "video/robot-gesty.mp4", "poster": "video/robot-gesty-poster.jpg",
        "duration": "PT14S", "w": 324, "h": 576,
        "name": "Robot humanoidalny gestykuluje — interakcja z gośćmi",
        "desc": "Robot Unitree G1 gestykuluje i wchodzi w interakcje z uczestnikami wydarzenia — macha, przybija piątki, pozuje do zdjęć.",
        "caption": "Unitree G1 w interakcji — gesty, piątki, pozowanie do zdjęć. To wokół tego gromadzą się uczestnicy.",
    },
    "spacer": {
        "file": "video/robot-spacer.mp4", "poster": "video/robot-spacer-poster.jpg",
        "duration": "PT14S", "w": 324, "h": 576,
        "name": "Robot humanoidalny w ruchu",
        "desc": "Robot Unitree G1 chodzi i podchodzi do ludzi. W ruchu zatrzymuje przechodniów i buduje tłum wokół siebie.",
        "caption": "Unitree G1 w ruchu. Chodzący humanoid to widok, obok którego nikt nie przechodzi obojętnie.",
    },
    "branding": {
        "file": "video/robot-branding.mp4", "poster": "video/robot-branding-poster.jpg",
        "duration": "PT13S", "w": 324, "h": 576,
        "name": "Robot humanoidalny z brandingiem marki",
        "desc": "Robot Unitree G1 z brandingiem klienta — logo i kolory marki na robocie, który staje się ambasadorem brandu.",
        "caption": "Unitree G1 z brandingiem klienta. Robot w barwach Twojej marki to najczęściej fotografowany element wydarzenia.",
    },
}

# ------------------------------------------------------- pule poradników
GUIDES = {
    "default": [
        ("blog-co-potrafi-robot-humanoidalny.html", "Co potrafi robot humanoidalny? 12 umiejętności G1 →"),
        ("blog-bezpieczenstwo-robota-na-evencie.html", "Czy robot na evencie jest bezpieczny? →"),
    ],
    "cena": [
        ("blog-ile-kosztuje-wynajem-robota.html", "Ile kosztuje wynajem robota? Cennik i czynniki →"),
        ("blog-jak-wynajac-robota-checklist.html", "Jak wynająć robota — checklista organizatora →"),
    ],
    "targi": [
        ("blog-robot-na-stoisko-targowe.html", "Robot na stoisku targowym — jak zebrać leady →"),
        ("blog-robot-zamiast-hostessy.html", "Robot zamiast hostessy? Porównanie →"),
    ],
    "marketing": [
        ("blog-robot-viral-marketing-event.html", "Robot jako viral — marketing eventowy →"),
        ("blog-robot-ambasador-marki.html", "Robot jako ambasador marki →"),
    ],
    "dzieci": [
        ("blog-robot-na-event-dla-dzieci.html", "Robot na evencie dla dzieci — poradnik →"),
        ("blog-bezpieczenstwo-robota-na-evencie.html", "Czy robot na evencie jest bezpieczny? →"),
    ],
    "ai": [
        ("blog-robot-z-ai-rozmawiajacy-po-polsku.html", "Robot z AI rozmawiający po polsku →"),
        ("blog-czy-robot-moze-prowadzic-event.html", "Czy robot może prowadzić event? →"),
    ],
}

TEMPLATE = """<!DOCTYPE html>
<html lang="pl">
<head>
  <!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','GTM-MR7R7CJ3');</script>
<!-- End Google Tag Manager -->
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="keywords" content="{keywords}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{url}" />

  <!-- Open Graph -->
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{url}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:image" content="https://33bots.pl/og-image.jpg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="{og_alt}" />
  <meta property="og:locale" content="pl_PL" />
  <meta property="og:site_name" content="33bots" />

  <!-- Twitter / X Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />

  <meta name="theme-color" content="#000000" />
  <link rel="alternate" hreflang="pl" href="{url}" />
  <link rel="alternate" hreflang="x-default" href="{url}" />

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

  <script>history.scrollRestoration = 'manual';</script>
  <link rel="icon" type="image/svg+xml" href="favicon.svg" />
  <link rel="stylesheet" href="style.css?v=19" />
    <link rel="dns-prefetch" href="//serve.albacross.com" />
<link rel="preconnect" href="https://www.googletagmanager.com" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="preload" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'" />
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" /></noscript>
  <style>
    .hero {{ grid-template-columns: 1fr; min-height: 70vh; }}
    .hero__content {{ max-width: none; padding: var(--s12) 0 var(--s8); }}
    .hero__title {{ text-wrap: unset; }}
  </style>
</head>
<body>
  <!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-MR7R7CJ3"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->

  <div class="cursor-glow" id="cursorGlow" aria-hidden="true"></div>
  <div class="scroll-progress" id="scrollProgress" aria-hidden="true"></div>

  <header class="nav" id="nav">
    <div class="nav__inner">
      <a href="index.html" class="logo">33BOTS</a>
      <nav class="nav__links">
        <div class="nav__dropdown">
          <button class="nav__dropdown-toggle" aria-haspopup="true" aria-expanded="false" type="button">Oferta <svg viewBox="0 0 10 6" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
          <div class="nav__dropdown-menu">
            <a href="oferta-targi.html">Targi</a>
            <a href="oferta-konferencje.html">Konferencje i Gale</a>
            <a href="oferta-dni-otwarte.html">Dni otwarte i showroomy</a>
            <a href="atrakcje-na-event.html">Wszystkie atrakcje</a>
          </div>
        </div>
        <a href="index.html#o-nas">O nas</a>
        <a href="index.html#eventy">Eventy</a>
        <a href="blog.html">Blog</a>
        <a href="#kontakt">Kontakt</a>
      </nav>
      <button class="hamburger" id="hamburger" aria-label="Menu"><span></span><span></span></button>
    </div>
  </header>
  <main>

  <nav class="crumbs" aria-label="Okruszki" style="max-width:1200px; margin:0 auto; padding:calc(var(--s8) + 48px) var(--s5) 0; font-size:0.78rem; letter-spacing:0.02em;">
    <a href="index.html" style="color:var(--text-3); text-decoration:none;">Strona główna</a> <span aria-hidden="true" style="color:var(--text-3);">›</span> <span style="color:var(--text-2);">{crumb}</span>
  </nav>

  <div class="mobile-menu" id="mobileMenu">
    <span class="mobile-menu__label">Oferta</span>
    <a href="oferta-targi.html" class="mobile-menu__sub">Targi</a>
    <a href="oferta-konferencje.html" class="mobile-menu__sub">Konferencje i Gale</a>
    <a href="oferta-dni-otwarte.html" class="mobile-menu__sub">Dni otwarte i showroomy</a>
    <a href="atrakcje-na-event.html" class="mobile-menu__sub">Wszystkie atrakcje</a>
    <a href="index.html#o-nas">O nas</a>
    <a href="index.html#eventy">Eventy</a>
    <a href="blog.html">Blog</a>
    <a href="#kontakt">Kontakt</a>
  </div>

  <section class="hero">
    <div class="hero__content">
      <p class="hero__eyebrow">{eyebrow}</p>
      <h1 class="hero__title">{h1}</h1>
      <p class="hero__sub">{sub}</p>
      <div class="hero__ctas">
        <a href="#kontakt" class="btn-primary">Zapytaj o termin</a>
        <a href="#scenariusze" class="btn-ghost">Jak to wygląda? ↓</a>
      </div>
    </div>
  </section>

  <section class="section" id="korzysci">
    <div class="section-header">
      <span class="tag">Dlaczego robot?</span>
      <h2 class="section-title">{tiles_h2}</h2>
    </div>
    <div class="tiles">
{tiles_html}
    </div>
  </section>

  <section class="section" id="scenariusze">
    <div class="onas-body" style="max-width:860px; margin:0 auto;">
      <div class="onas-text">
        <h2 class="section-title" style="font-size:clamp(1.8rem,3vw,2.8rem); margin-bottom:var(--s4);">{scen_title}</h2>
        <p class="lead-text">{scen_intro}</p>
{scens_html}
{blog_para}
        <a href="#kontakt" class="btn-primary" style="margin-top:var(--s5); display:inline-flex;">Zapytaj o termin →</a>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:0;">
    <div style="max-width:860px; margin:0 auto;">
      <div style="padding:var(--s5) var(--s6); background:var(--surface-2); border:1px solid var(--border-mid); border-radius:12px; display:flex; align-items:center; justify-content:space-between; gap:var(--s4); flex-wrap:wrap;">
        <p style="color:var(--text-2); font-size:0.9rem; margin:0;">{related_intro}</p>
        <div style="display:flex; gap:var(--s3); flex-wrap:wrap;">
{related_html}
        </div>
      </div>
    </div>
  </section>


  <!-- WIDEO -->
  <section class="section" id="wideo">
    <div class="section-header">
      <span class="tag">Wideo</span>
      <h2 class="section-title">Zobacz robota<br />w akcji</h2>
    </div>
    <div style="display:flex; flex-wrap:wrap; gap:var(--s6); align-items:center; justify-content:center; max-width:1000px; margin:0 auto;">
      <video controls muted playsinline preload="none"
             poster="{video_poster}"
             width="{video_w}" height="{video_h}"
             style="width:min(324px,85vw); border-radius:16px; border:1px solid var(--border-mid); background:var(--surface-2);"
             aria-label="{video_name}">
        <source src="{video_file}" type="video/mp4" />
        Twoja przeglądarka nie obsługuje wideo HTML5.
      </video>
      <div style="max-width:420px; display:flex; flex-direction:column; gap:var(--s4); text-align:left;">
        <p style="color:var(--text-2); font-size:1rem; line-height:1.8; margin:0;">{video_caption}</p>
        <a href="#kontakt" class="btn-primary" style="display:inline-flex; align-self:flex-start;">Zarezerwuj pokaz →</a>
      </div>
    </div>
  </section>

  <!-- PORADNIKI -->
  <section class="section" style="padding-top:0;">
    <div style="max-width:1000px; margin:0 auto;">
      <p style="font-size:0.75rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:var(--text-3); margin-bottom:var(--s4);">Poradniki przed wynajmem</p>
      <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(260px, 1fr)); gap:var(--s4);">
{guides_html}
      </div>
    </div>
  </section>

  <!-- TESTIMONIALE -->
  <section class="section testimonials-section">
    <div class="section-header">
      <span class="tag">Opinie</span>
      <h2 class="section-title">Mówią o nas</h2>
    </div>
    <div class="testimonials">
      <div class="testimonial">
        <p class="testimonial__quote">„Efekt przerósł nasze najśmielsze oczekiwania. Zainteresowanie było ogromne przez cały czas trwania wydarzenia – nie spodziewałam się, że aż tak przyciągniemy uwagę."</p>
        <div class="testimonial__meta">
          <span class="testimonial__name">Karolina M.</span>
          <span class="testimonial__role">Marketing · branża IT</span>
        </div>
      </div>
      <div class="testimonial">
        <p class="testimonial__quote">„To była jedna z najlepszych decyzji organizacyjnych. Pozytywne reakcje uczestników i ich pełne zaangażowanie to dla nas najlepsza recenzja całego przedsięwzięcia."</p>
        <div class="testimonial__meta">
          <span class="testimonial__name">Piotr Z.</span>
          <span class="testimonial__role">Organizator · gala firmowa</span>
        </div>
      </div>
      <div class="testimonial">
        <p class="testimonial__quote">„Współpraca przełożyła się na niesamowite zasięgi w mediach społecznościowych. To ten rodzaj autentycznego zainteresowania, którego nie da się po prostu kupić."</p>
        <div class="testimonial__meta">
          <span class="testimonial__name">Magdalena T.</span>
          <span class="testimonial__role">PR Manager · targi technologiczne</span>
        </div>
      </div>
    </div>
  </section>

  <section class="section faq-section">
    <div class="section-header">
      <span class="tag">FAQ</span>
      <h2 class="section-title">{faq_h2}</h2>
    </div>
    <div class="faq">
{faq_html}
    </div>
  </section>

  <section class="section" id="kontakt">
    <div class="contact-layout">
      <div class="contact-left">
        <span class="tag">Kontakt</span>
        <h2 class="section-title">{kontakt_h2}</h2>
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
            <span class="contact-detail__label">Zasięg</span>
            <span class="contact-detail__val">Cała Polska — dojazd w wycenie</span>
          </div>
        </div>
      </div>
      <div class="contact-right">
        <form id="contactForm" class="form" novalidate>
          <div class="form-steps-header">
            <span class="form-step-ind active" id="stepInd1">01 — Dane kontaktowe</span>
            <span class="form-step-sep">/</span>
            <span class="form-step-ind" id="stepInd2">02 — Twoje wydarzenie</span>
          </div>
          <div class="form-step" id="formStep1">
            <div class="form-row">
              <div class="form-field">
                <label for="f-name">Imię i nazwisko *</label>
                <input id="f-name" type="text" name="name" placeholder="Jan Kowalski" autocomplete="name" required />
                <span class="form-field__err" aria-live="polite"></span>
              </div>
              <div class="form-field">
                <label for="f-company">Firma (opcjonalnie)</label>
                <input id="f-company" type="text" name="company" placeholder="Nazwa firmy" autocomplete="organization" />
              </div>
            </div>
            <div class="form-row">
              <div class="form-field">
                <label for="f-email">E-mail *</label>
                <input id="f-email" type="email" name="email" placeholder="jan@email.pl" autocomplete="email" required />
                <span class="form-field__err" aria-live="polite"></span>
              </div>
              <div class="form-field">
                <label for="f-phone">Telefon</label>
                <input id="f-phone" type="tel" name="phone" placeholder="+48 531 408 004" autocomplete="tel" />
              </div>
            </div>
            <button type="button" id="btnNext" class="btn-submit">Dalej — Opowiedz o wydarzeniu →</button>
          </div>
          <div class="form-step form-step--hidden" id="formStep2" aria-hidden="true">
            <div class="form-row">
              <div class="form-field">
                <label for="f-date">Data wydarzenia</label>
                <input id="f-date" type="text" name="date" placeholder="np. 14 czerwca 2026" />
              </div>
              <div class="form-field">
                <label for="f-location">Miejsce / Miasto</label>
                <input id="f-location" type="text" name="location" placeholder="np. Kraków" autocomplete="address-level2" />
              </div>
            </div>
            <div class="form-field">
              <label for="f-message">Opisz wydarzenie *</label>
              <textarea id="f-message" name="message" rows="6" placeholder="Liczba gości, czas trwania, charakter wydarzenia..." required></textarea>
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

  <section class="section" style="padding-block:var(--s6) var(--s4); background:var(--surface-1)">
    <div class="container" style="max-width:1140px; margin-inline:auto; padding-inline:var(--s4)">
      <h2 style="font-size:clamp(1rem,2vw,1.4rem); font-weight:700; margin-bottom:var(--s3); color:var(--text-1)">Wynajem robota w Twoim mieście</h2>
      <div style="display:flex; flex-wrap:wrap; gap:0.5rem;">
{city_chips}
      </div>
    </div>
  </section>

  </main>
  <footer class="footer">
    <div class="footer__inner">
      <div class="footer__brand">
        <span class="logo">33BOTS</span>
        <p class="footer__tagline"><a href="index.html" style="color:inherit; text-decoration:underline; text-underline-offset:2px;">Wynajem robotów humanoidalnych</a> · Polska</p>
        <div class="footer__nap">
          <a href="tel:+48531408004" class="footer__nap-item">+48 531 408 004</a>
          <a href="mailto:kontakt@33bots.pl" class="footer__nap-item">kontakt@33bots.pl</a>
        </div>
      </div>
      <div class="footer__links">
        <a href="oferta.html">Usługi i oferta</a>
        <a href="atrakcje-na-event.html">Atrakcje na event</a>
        <a href="realizacje-wideo.html">Realizacje</a>
        <a href="case-study-lexai.html">Case study</a>
        <a href="index.html#o-nas">O nas</a>
        <a href="blog.html">Blog</a>
        <a href="#kontakt">Kontakt</a>
      </div>
      <div class="footer__right">
        <div class="footer__socials">
          <a href="https://www.instagram.com/33bots_/" target="_blank" rel="noopener noreferrer" class="footer__social">↗ Instagram</a>
          <a href="https://www.tiktok.com/@aimforum" target="_blank" rel="noopener noreferrer" class="footer__social">↗ TikTok</a>
          <a href="https://www.facebook.com/33bots" target="_blank" rel="noopener noreferrer" class="footer__social">↗ Facebook</a>
          <a href="https://www.linkedin.com/company/33bots" target="_blank" rel="noopener noreferrer" class="footer__social">↗ LinkedIn</a>
        </div>
        <span class="footer__copy">© 2026 33bots. Wszelkie prawa zastrzeżone.</span>
      </div>
    </div>
  </footer>

  <div class="cookie-banner" id="cookieBanner" aria-live="polite">
    <p class="cookie-banner__text">Ta strona używa plików cookie do celów analitycznych. <a href="#" class="cookie-banner__link">Polityka prywatności</a></p>
    <button class="cookie-banner__btn" id="cookieAccept">Rozumiem</button>
  </div>

  <div class="sticky-cta">
    <a href="#kontakt" class="btn-primary">Zapytaj o termin →</a>
  </div>

  <script src="main.js"></script>
  <!-- Albacross -->
  <script>window._nQc="89159321";</script>
  <script async src="https://serve.albacross.com/track.js"></script>
</body>
</html>
"""

H3_STYLE = 'style="font-size:1.1rem; font-weight:700; letter-spacing:-0.01em; margin:var(--s6) 0 var(--s2); color:var(--text);"'

CHIP_CITIES = [
    ("robot-wynajem-warszawa.html", "Warszawa"), ("robot-wynajem-krakow.html", "Kraków"),
    ("robot-wynajem-wroclaw.html", "Wrocław"), ("robot-wynajem-poznan.html", "Poznań"),
    ("robot-wynajem-gdansk.html", "Gdańsk"), ("robot-wynajem-katowice.html", "Katowice"),
    ("robot-wynajem-lodz.html", "Łódź"), ("robot-wynajem-szczecin.html", "Szczecin"),
    ("robot-wynajem-lublin.html", "Lublin"), ("robot-wynajem-rzeszow.html", "Rzeszów"),
]

CHIP_STYLE = ('padding:0.35rem 0.8rem; border:1px solid var(--border); border-radius:999px; '
              'font-size:0.8rem; color:var(--text-2); text-decoration:none; transition:border-color 0.2s')


def render_city_chips():
    return "\n".join(
        f'        <a href="{href}" style="{CHIP_STYLE}">{name}</a>'
        for href, name in CHIP_CITIES
    )


def render_tiles(tiles):
    out = []
    for i, (tag, title, desc) in enumerate(tiles):
        cls = "tile tile--light" if i == 1 else "tile"
        out.append(
            f'      <div class="{cls}">\n'
            f'        <div class="tile__top"><span class="tile__tag">{tag}</span></div>\n'
            f'        <h3 class="tile__title">{title}</h3>\n'
            f'        <p class="tile__desc">{desc}</p>\n'
            f'        <a href="#kontakt" class="tile__link">Zapytaj o termin →</a>\n'
            f'      </div>'
        )
    return "\n".join(out)


def render_scens(scens):
    out = []
    for h, p in scens:
        out.append(f'        <h3 {H3_STYLE}>{h}</h3>\n        <p class="body-text">{p}</p>')
    return "\n\n".join(out)


def render_related(related):
    out = []
    for href, label in related:
        out.append(
            f'          <a href="{href}" style="color:var(--text); font-size:0.85rem; font-weight:600; '
            f'text-decoration:underline; text-underline-offset:3px; white-space:nowrap;">{label} →</a>'
        )
    return "\n".join(out)


def render_guides(guides):
    out = []
    for href, label in guides:
        out.append(
            f'        <a href="{href}" style="display:flex; flex-direction:column; gap:4px; padding:var(--s4) var(--s5); '
            f'background:var(--surface-2); border:1px solid var(--border-mid); border-radius:10px; text-decoration:none;">\n'
            f'          <span style="font-size:0.7rem; font-weight:600; letter-spacing:0.08em; text-transform:uppercase; color:var(--text-3);">Poradnik</span>\n'
            f'          <span style="font-size:0.95rem; font-weight:700; color:var(--text); letter-spacing:-0.015em; line-height:1.35;">{label}</span>\n'
            f'        </a>'
        )
    return "\n".join(out)


def render_faq_html(faqs):
    out = []
    for q, a in faqs:
        out.append(
            '      <div class="faq-item">\n'
            '        <button class="faq-q" aria-expanded="false">\n'
            f'          <span>{q}</span>\n'
            '          <span class="faq-q__icon" aria-hidden="true">+</span>\n'
            '        </button>\n'
            f'        <div class="faq-a" hidden><p>{a}</p></div>\n'
            '      </div>'
        )
    return "\n".join(out)


def strip_tags(s):
    return re.sub(r"<[^>]+>", " ", s).replace("  ", " ").strip()


def build_page(p):
    url = f"{DOMAIN}/{p['slug']}.html"
    video = VIDEOS[p.get("video", "gesty")]

    product_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "Service",
        "name": p["schema_name"],
        "description": p["schema_desc"],
        "url": url,
        "image": "https://33bots.pl/robot-g1.jpg",
        "serviceType": "Wynajem robota humanoidalnego na eventy",
        "provider": {
            "@type": "Organization",
            "name": "33bots",
            "url": "https://33bots.pl/",
            "email": "kontakt@33bots.pl",
            "telephone": "+48 531 408 004",
        },
        "areaServed": {"@type": "Country", "name": "Polska"},
    }, ensure_ascii=False, indent=2)

    breadcrumb_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Strona główna", "item": "https://33bots.pl/"},
            {"@type": "ListItem", "position": 2, "name": p["crumb"], "item": url},
        ],
    }, ensure_ascii=False, indent=2)

    faq_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
            for q, a in p["faqs"]
        ],
    }, ensure_ascii=False, indent=2)

    video_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "name": video["name"],
        "description": video["desc"],
        "thumbnailUrl": f"https://33bots.pl/{video['poster']}",
        "contentUrl": f"https://33bots.pl/{video['file']}",
        "uploadDate": "2026-07-02",
        "duration": video["duration"],
        "inLanguage": "pl",
        "publisher": {"@type": "Organization", "name": "33bots", "url": "https://33bots.pl",
                      "logo": {"@type": "ImageObject", "url": "https://33bots.pl/logo.png"}},
    }, ensure_ascii=False, indent=2)

    blog_para = ""
    if p.get("blog_link"):
        href, txt = p["blog_link"]
        blog_para = (f'\n        <p class="body-text">Więcej na ten temat przeczytasz w naszym artykule: '
                     f'<a href="{href}" style="color:var(--text); text-decoration:underline; text-underline-offset:3px;">{txt}</a></p>\n')

    html = TEMPLATE.format(
        title=p["title"], desc=p["desc"], keywords=p["keywords"], url=url,
        og_alt=p["schema_name"], crumb=p["crumb"],
        eyebrow=p["eyebrow"], h1=p["h1"], sub=p["sub"],
        tiles_h2=p["tiles_h2"], tiles_html=render_tiles(p["tiles"]),
        scen_title=p["scen_title"], scen_intro=p["scen_intro"],
        scens_html=render_scens(p["scens"]), blog_para=blog_para,
        related_intro=p["related_intro"], related_html=render_related(p["related"]),
        video_poster=video["poster"], video_file=video["file"], video_name=video["name"],
        video_caption=video["caption"], video_w=video["w"], video_h=video["h"],
        guides_html=render_guides(GUIDES[p.get("guides", "default")]),
        faq_h2=p["faq_h2"], faq_html=render_faq_html(p["faqs"]),
        kontakt_h2=p["kontakt_h2"],
        product_json=product_json, breadcrumb_json=breadcrumb_json,
        faq_json=faq_json, video_json=video_json,
        city_chips=render_city_chips(),
    )
    return html


def update_sitemap(slugs):
    path = os.path.join(BASE, "sitemap.xml")
    with open(path, "r", encoding="utf-8") as f:
        xml = f.read()
    entries = []
    for slug in slugs:
        loc = f"{DOMAIN}/{slug}.html"
        if loc in xml:
            continue
        entries.append(
            "  <url>\n"
            f"    <loc>{loc}</loc>\n"
            f"    <lastmod>{LASTMOD}</lastmod>\n"
            "    <changefreq>monthly</changefreq>\n"
            "    <priority>0.7</priority>\n"
            "  </url>\n"
        )
    if entries:
        xml = xml.replace("</urlset>", "".join(entries) + "</urlset>")
        with open(path, "w", encoding="utf-8") as f:
            f.write(xml)
    return len(entries)


def build_directory():
    """Katalog wszystkich podstron wstawiany na stronie-hubie atrakcje-na-event.html."""
    from seo_pages_content import SERVICES, ROLES, PLACES
    from seo_pages_content2 import EVENTS, BRANZE, PRIVATE
    groups = [
        ("Usługi i zastosowania", SERVICES),
        ("Role robota", ROLES),
        ("Miejsca i branże", PLACES),
        ("Typy wydarzeń", EVENTS),
        ("Eventy branżowe", BRANZE),
        ("Imprezy prywatne i okolicznościowe", PRIVATE),
    ]
    out = ['  <section class="section" id="katalog" style="padding-top:0;">',
           '    <div style="max-width:1100px; margin:0 auto;">',
           '      <h2 class="section-title" style="font-size:clamp(1.6rem,2.6vw,2.4rem); margin-bottom:var(--s6);">Robot na każdą okazję —<br />wybierz swój scenariusz</h2>']
    for label, pages in groups:
        out.append(f'      <p style="font-size:0.75rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:var(--text-3); margin:var(--s6) 0 var(--s3);">{label}</p>')
        out.append('      <div style="display:flex; flex-wrap:wrap; gap:var(--s2);">')
        for p in pages:
            if p["slug"] == "atrakcje-na-event":
                continue
            out.append(f'        <a href="{p["slug"]}.html" style="padding:6px 14px; background:var(--surface-2); border:1px solid var(--border-mid); border-radius:999px; font-size:0.82rem; font-weight:600; color:var(--text-2); text-decoration:none; white-space:nowrap;">{p["crumb"]}</a>')
        out.append('      </div>')
    out.append('    </div>')
    out.append('  </section>')
    return "\n".join(out)


def build_itemlist_json():
    """Schema ItemList dla strony-hubu — lista wszystkich podstron katalogu."""
    from seo_pages_content import ALL_PAGES
    items = [
        {"@type": "ListItem", "position": i + 1, "name": p["crumb"], "url": f"{DOMAIN}/{p['slug']}.html"}
        for i, p in enumerate(pp for pp in ALL_PAGES if pp["slug"] != "atrakcje-na-event")
    ]
    data = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Atrakcje na event — katalog scenariuszy wynajmu robota",
        "numberOfItems": len(items),
        "itemListElement": items,
    }
    return '  <script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2) + "\n  </script>\n"


def main():
    from seo_pages_content import ALL_PAGES
    slugs = []
    for p in ALL_PAGES:
        html = build_page(p)
        if p["slug"] == "atrakcje-na-event":
            html = html.replace("  <!-- WIDEO -->", build_directory() + "\n\n  <!-- WIDEO -->", 1)
            html = html.replace("</head>", build_itemlist_json() + "</head>", 1)
        fname = os.path.join(BASE, p["slug"] + ".html")
        with open(fname, "w", encoding="utf-8") as f:
            f.write(html)
        slugs.append(p["slug"])
    added = update_sitemap(slugs)
    print(f"Wygenerowano {len(slugs)} stron, dodano {added} wpisów do sitemap.xml")


if __name__ == "__main__":
    main()
