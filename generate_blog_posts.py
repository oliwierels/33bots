#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator artykułów blogowych — wzorowany na blog-robot-na-wesele.html.
Uruchomienie: python3 generate_blog_posts.py
Tworzy pliki blog-*.html, dodaje karty do blog.html, wpisy do feed.xml i sitemap.xml.
"""

import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://33bots.pl"

LINK = 'style="color:var(--text);text-decoration:underline;text-underline-offset:3px;"'

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
  <!-- Google Analytics 4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-MNE9Y0S9QV"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-MNE9Y0S9QV');
  </script>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="keywords" content="{keywords}" />
    <meta property="article:published_time" content="{date}T08:00:00+02:00" />
  <meta property="article:modified_time" content="{date}T08:00:00+02:00" />
  <meta property="article:author" content="33bots" />
  <meta name="author" content="33bots" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{url}" />

  <!-- Open Graph -->
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{url}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:image" content="https://33bots.pl/og-image.jpg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:image:alt" content="Robot humanoidalny Unitree G1 — 33bots" />
  <meta property="og:locale" content="pl_PL" />
  <meta property="og:site_name" content="33bots" />

  <!-- Twitter / X Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />

  <!-- Mobile -->
  <meta name="theme-color" content="#000000" />

  <!-- Hreflang -->
  <link rel="alternate" hreflang="pl" href="{url}" />
  <link rel="alternate" hreflang="x-default" href="{url}" />

  <script type="application/ld+json">
{breadcrumb_json}
  </script>

  <script type="application/ld+json">
{blogposting_json}
  </script>

  <script type="application/ld+json">
{faq_json}
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
    .hero {{ grid-template-columns: 1fr; min-height: 55vh; }}
    .hero__content {{ max-width: none; padding: var(--s12) 0 var(--s6); }}
    .hero__title {{ text-wrap: unset; }}
    .article-body {{ max-width: 760px; margin: 0 auto; }}
    .article-body h2 {{
      font-size: clamp(1.4rem, 2.5vw, 1.9rem);
      font-weight: 800;
      letter-spacing: -0.025em;
      margin: var(--s8) 0 var(--s3);
      color: var(--text);
    }}
    .article-body h2:first-child {{ margin-top: 0; }}
    .article-body h3 {{
      font-size: 1.1rem;
      font-weight: 700;
      color: var(--text);
      margin: var(--s5) 0 var(--s2);
    }}
    .article-body p {{ font-size: 1rem; color: var(--text-2); line-height: 1.85; margin-bottom: var(--s3); }}
    .article-body strong {{ color: var(--text); font-weight: 600; }}
    .article-body ul {{ margin: var(--s3) 0 var(--s4) var(--s4); }}
    .article-body ul li {{ color: var(--text-2); line-height: 1.8; margin-bottom: 6px; list-style: disc; }}
    .article-body ol {{ margin: var(--s3) 0 var(--s4) var(--s4); }}
    .article-body ol li {{ color: var(--text-2); line-height: 1.8; margin-bottom: 6px; list-style: decimal; }}
    .article-body .article-cta {{ display: inline-flex; margin-top: var(--s6); }}
    .article-num {{
      display: inline-block;
      font-size: 0.65rem;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--text-3);
      border: 1px solid var(--border-mid);
      border-radius: 4px;
      padding: 3px 8px;
      margin-bottom: var(--s2);
    }}
    .faq-item {{
      border-bottom: 1px solid var(--border);
      padding: var(--s4) 0;
    }}
    .faq-item:last-child {{ border-bottom: none; }}
    .faq-item__q {{
      font-size: 1rem;
      font-weight: 700;
      color: var(--text);
      margin-bottom: var(--s2);
    }}
    .faq-item__a {{
      font-size: 0.95rem;
      color: var(--text-2);
      line-height: 1.75;
      margin: 0;
    }}
  </style>
</head>
<body>
  <!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-MR7R7CJ3"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->

  <div class="cursor-glow" id="cursorGlow" aria-hidden="true"></div>
  <div class="scroll-progress" id="scrollProgress" aria-hidden="true"></div>

  <!-- NAV -->
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
      <button class="hamburger" id="hamburger" aria-label="Menu">
        <span></span><span></span>
      </button>
    </div>
  </header>
  <main>

  <nav class="crumbs" aria-label="Okruszki" style="max-width:1200px; margin:0 auto; padding:calc(var(--s8) + 48px) var(--s5) 0; font-size:0.78rem; letter-spacing:0.02em;">
    <a href="index.html" style="color:var(--text-3); text-decoration:none;">Strona główna</a> <span aria-hidden="true" style="color:var(--text-3);">›</span> <a href="blog.html" style="color:var(--text-3); text-decoration:none;">Blog</a> <span aria-hidden="true" style="color:var(--text-3);">›</span> <span style="color:var(--text-2);">{crumb}</span>
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

  <!-- HERO -->
  <section class="hero">
    <div class="hero__content">
      <p class="hero__eyebrow">{eyebrow}</p>
      <h1 class="hero__title">{h1}</h1>
      <p class="hero__sub">{sub}</p>
    </div>
  </section>

  <!-- ARTYKUŁ -->
  <section class="section">
    <div class="article-body">

{body}

      <div style="margin-top:var(--s8); padding:var(--s6); background:var(--surface-2); border:1px solid var(--border-mid); border-radius:12px;">
        <p style="color:var(--text); font-size:1rem; font-weight:700; margin-bottom:var(--s2);">{cta_title}</p>
        <p style="color:var(--text-2); font-size:0.95rem; margin-bottom:var(--s5);">{cta_text}</p>
        <a href="#kontakt" class="btn-primary article-cta">Zapytaj o termin →</a>
      </div>

      <!-- FAQ -->
      <span class="article-num" style="margin-top:var(--s8); display:inline-block;">FAQ</span>
      <h2>Najczęstsze pytania</h2>

{faq_html}

      <!-- ZOBACZ RÓWNIEŻ -->
      <div style="margin-top:var(--s10); border-top:1px solid var(--border); padding-top:var(--s6);">
        <p style="font-size:0.75rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:var(--text-3); margin-bottom:var(--s4);">Zobacz również</p>
        <div style="display:grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap:var(--s4);">
{related_html}
        </div>
      </div>

    </div>
  </section>

  <!-- KONTAKT -->
  <section class="section" id="kontakt">
    <div class="section-header">
      <span class="tag">Kontakt</span>
      <h2 class="section-title">Zarezerwuj robota<br />na swoje wydarzenie</h2>
    </div>
    <div class="contact-wrap">
      <div class="contact-left">
        <p class="contact-lead">Napisz do nas — odpiszemy w ciągu 24 godzin roboczych i dobierzemy najlepszy scenariusz dla Twojego wydarzenia.</p>
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
            <span class="contact-detail__val">Cała Polska</span>
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

          <!-- STEP 1 -->
          <div class="form-step" id="formStep1">
            <div class="form-row">
              <div class="form-field">
                <label for="f-name">Imię i nazwisko *</label>
                <input id="f-name" type="text" name="name" required placeholder="Jan Kowalski" autocomplete="name" />
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
                <input id="f-email" type="email" name="email" required placeholder="jan@email.pl" autocomplete="email" />
                <span class="form-field__err" aria-live="polite"></span>
              </div>
              <div class="form-field">
                <label for="f-phone">Telefon</label>
                <input id="f-phone" type="tel" name="phone" placeholder="+48 531 408 004" autocomplete="tel" />
              </div>
            </div>
            <div class="form-actions">
              <button type="button" class="btn-primary" id="btnNext">Dalej →</button>
            </div>
          </div>

          <!-- STEP 2 -->
          <div class="form-step form-step--hidden" id="formStep2" aria-hidden="true">
            <div class="form-row">
              <div class="form-field">
                <label for="f-date">Data wydarzenia</label>
                <input id="f-date" type="text" name="date" placeholder="np. 14 czerwca 2026" />
              </div>
              <div class="form-field">
                <label for="f-location">Miejsce / Miasto</label>
                <input id="f-location" type="text" name="location" placeholder="np. Kraków" />
              </div>
            </div>
            <div class="form-field">
              <label for="f-message">Opis / czego potrzebujesz *</label>
              <textarea id="f-message" name="message" required rows="4" placeholder="Liczba gości, czas trwania, charakter wydarzenia..."></textarea>
              <span class="form-field__err" aria-live="polite"></span>
              <div class="char-counter"><span id="charCount">0</span> / 600</div>
            </div>
            <div class="form-actions form-actions--split">
              <button type="button" class="btn-ghost" id="btnBack">← Wróć</button>
              <button type="submit" class="btn-primary">Wyślij zapytanie</button>
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
        <a href="robot-wynajem-warszawa.html" style="padding:0.35rem 0.8rem; border:1px solid var(--border); border-radius:999px; font-size:0.8rem; color:var(--text-2); text-decoration:none; transition:border-color 0.2s">Warszawa</a>
        <a href="robot-wynajem-krakow.html" style="padding:0.35rem 0.8rem; border:1px solid var(--border); border-radius:999px; font-size:0.8rem; color:var(--text-2); text-decoration:none; transition:border-color 0.2s">Kraków</a>
        <a href="robot-wynajem-wroclaw.html" style="padding:0.35rem 0.8rem; border:1px solid var(--border); border-radius:999px; font-size:0.8rem; color:var(--text-2); text-decoration:none; transition:border-color 0.2s">Wrocław</a>
        <a href="robot-wynajem-poznan.html" style="padding:0.35rem 0.8rem; border:1px solid var(--border); border-radius:999px; font-size:0.8rem; color:var(--text-2); text-decoration:none; transition:border-color 0.2s">Poznań</a>
        <a href="robot-wynajem-gdansk.html" style="padding:0.35rem 0.8rem; border:1px solid var(--border); border-radius:999px; font-size:0.8rem; color:var(--text-2); text-decoration:none; transition:border-color 0.2s">Gdańsk</a>
        <a href="robot-wynajem-katowice.html" style="padding:0.35rem 0.8rem; border:1px solid var(--border); border-radius:999px; font-size:0.8rem; color:var(--text-2); text-decoration:none; transition:border-color 0.2s">Katowice</a>
        <a href="robot-wynajem-lodz.html" style="padding:0.35rem 0.8rem; border:1px solid var(--border); border-radius:999px; font-size:0.8rem; color:var(--text-2); text-decoration:none; transition:border-color 0.2s">Łódź</a>
        <a href="robot-wynajem-szczecin.html" style="padding:0.35rem 0.8rem; border:1px solid var(--border); border-radius:999px; font-size:0.8rem; color:var(--text-2); text-decoration:none; transition:border-color 0.2s">Szczecin</a>
        <a href="robot-wynajem-lublin.html" style="padding:0.35rem 0.8rem; border:1px solid var(--border); border-radius:999px; font-size:0.8rem; color:var(--text-2); text-decoration:none; transition:border-color 0.2s">Lublin</a>
        <a href="robot-wynajem-rzeszow.html" style="padding:0.35rem 0.8rem; border:1px solid var(--border); border-radius:999px; font-size:0.8rem; color:var(--text-2); text-decoration:none; transition:border-color 0.2s">Rzeszów</a>
      </div>
    </div>
  </section>

  <!-- FOOTER -->
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
        <a href="index.html#eventy">Eventy</a>
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

  <!-- COOKIE BANNER -->
  <div class="cookie-banner" id="cookieBanner" aria-live="polite">
    <p class="cookie-banner__text">
      Ta strona używa plików cookie do celów analitycznych.
      <a href="#" class="cookie-banner__link">Polityka prywatności</a>
    </p>
    <button class="cookie-banner__btn" id="cookieAccept">Rozumiem</button>
  </div>

  <script src="main.js"></script>
  <!-- Albacross -->
  <script>window._nQc="89159321";</script>
  <script async src="https://serve.albacross.com/track.js"></script>
</body>
</html>
"""


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s).strip()


def render_faq(faqs):
    return "\n".join(
        '      <div class="faq-item">\n'
        f'        <p class="faq-item__q">{q}</p>\n'
        f'        <p class="faq-item__a">{a}</p>\n'
        '      </div>\n'
        for q, a in faqs
    )


def render_related(related):
    out = []
    for href, tag, title, desc in related:
        out.append(
            f'          <a href="{href}" style="display:flex; flex-direction:column; gap:4px; padding:var(--s4) var(--s5); background:var(--surface-2); border:1px solid var(--border-mid); border-radius:10px; text-decoration:none; transition:border-color 0.18s;">\n'
            f'            <span style="font-size:0.7rem; font-weight:600; letter-spacing:0.08em; text-transform:uppercase; color:var(--text-3);">{tag}</span>\n'
            f'            <span style="font-size:1rem; font-weight:700; color:var(--text); letter-spacing:-0.015em;">{title} →</span>\n'
            f'            <span style="font-size:0.88rem; color:var(--text-2);">{desc}</span>\n'
            f'          </a>'
        )
    return "\n".join(out)


def build_article(a):
    url = f"{DOMAIN}/{a['slug']}.html"
    headline = strip_tags(a["h1"].replace("<br />", " "))
    breadcrumb = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Strona główna", "item": "https://33bots.pl/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://33bots.pl/blog.html"},
            {"@type": "ListItem", "position": 3, "name": headline, "item": url},
        ],
    }, ensure_ascii=False, indent=2)
    blogposting = json.dumps({
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": headline,
        "description": a["desc"],
        "url": url,
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "image": "https://33bots.pl/robot-g1.jpg",
        "datePublished": a["date"],
        "dateModified": a["date"],
        "inLanguage": "pl",
        "keywords": a["keywords"],
        "wordCount": len(strip_tags(a["body"]).split()),
        "author": {"@type": "Organization", "name": "33bots", "url": "https://33bots.pl"},
        "publisher": {"@type": "Organization", "name": "33bots", "url": "https://33bots.pl",
                      "logo": {"@type": "ImageObject", "url": "https://33bots.pl/logo.png"}},
    }, ensure_ascii=False, indent=2)
    faq = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(ans)}}
            for q, ans in a["faqs"]
        ],
    }, ensure_ascii=False, indent=2)

    return TEMPLATE.format(
        title=a["title"], desc=a["desc"], keywords=a["keywords"], url=url,
        date=a["date"], crumb=headline, eyebrow=a["eyebrow"], h1=a["h1"], sub=a["sub"],
        body=a["body"], cta_title=a["cta_title"], cta_text=a["cta_text"],
        faq_html=render_faq(a["faqs"]), related_html=render_related(a["related"]),
        breadcrumb_json=breadcrumb, blogposting_json=blogposting, faq_json=faq,
    )


def update_blog_index(articles):
    path = os.path.join(BASE, "blog.html")
    s = open(path, encoding="utf-8").read()
    # Karty na górze siatki
    anchor = '<div class="tiles tiles--blog">'
    cards = []
    for a in articles:
        if a["slug"] + ".html" in s:
            continue
        headline = strip_tags(a["h1"].replace("<br />", " "))
        cards.append(
            '      <div class="tile">\n'
            '        <div class="tile__top">\n'
            f'          <span class="tile__tag">{a["date"]}</span>\n'
            '        </div>\n'
            f'        <h2 class="tile__title" style="font-size:1.15rem;">{headline}</h2>\n'
            f'        <p class="tile__desc">{a["desc"].rstrip(" →")}</p>\n'
            f'        <a href="{a["slug"]}.html" class="tile__link">Czytaj artykuł →</a>\n'
            '      </div>\n'
        )
    if cards:
        s = s.replace(anchor, anchor + "\n" + "".join(cards), 1)
    # ItemList — przebuduj z nowymi URL-ami na początku
    m = re.search(r'<script type="application/ld\+json">\s*(\{[^<]*"ItemList"[^<]*\})\s*</script>', s, re.S)
    if m:
        data = json.loads(m.group(1))
        urls = [it["url"] for it in data["itemListElement"]]
        new_urls = [f"{DOMAIN}/{a['slug']}.html" for a in articles if f"{DOMAIN}/{a['slug']}.html" not in urls]
        urls = new_urls + urls
        data["itemListElement"] = [
            {"@type": "ListItem", "position": i + 1, "url": u} for i, u in enumerate(urls)
        ]
        s = s[:m.start(1)] + json.dumps(data, ensure_ascii=False, indent=2) + s[m.end(1):]
    open(path, "w", encoding="utf-8").write(s)


def update_feed(articles):
    path = os.path.join(BASE, "feed.xml")
    s = open(path, encoding="utf-8").read()
    items = []
    for a in articles:
        link = f"{DOMAIN}/{a['slug']}.html"
        if link in s:
            continue
        day = a["date"]
        import datetime
        dt = datetime.datetime.strptime(day, "%Y-%m-%d")
        pub = dt.strftime("%a, %d %b %Y 08:00:00 +0000")
        headline = strip_tags(a["h1"].replace("<br />", " "))
        items.append(
            "    <item>\n"
            f"      <title>{headline}</title>\n"
            f"      <link>{link}</link>\n"
            f'      <guid isPermaLink="true">{link}</guid>\n'
            f"      <pubDate>{pub}</pubDate>\n"
            f"      <description>{a['desc'].rstrip(' →')}</description>\n"
            "    </item>\n"
        )
    if items:
        s = s.replace("    <item>", "".join(items) + "    <item>", 1)
        open(path, "w", encoding="utf-8").write(s)


def update_sitemap(articles):
    path = os.path.join(BASE, "sitemap.xml")
    s = open(path, encoding="utf-8").read()
    entries = []
    for a in articles:
        loc = f"{DOMAIN}/{a['slug']}.html"
        if loc in s:
            continue
        entries.append(
            "  <url>\n"
            f"    <loc>{loc}</loc>\n"
            f"    <lastmod>{a['date']}</lastmod>\n"
            "    <changefreq>monthly</changefreq>\n"
            "    <priority>0.6</priority>\n"
            "  </url>\n"
        )
    if entries:
        s = s.replace("</urlset>", "".join(entries) + "</urlset>")
        open(path, "w", encoding="utf-8").write(s)


def main():
    from blog_articles_content import ARTICLES
    for a in ARTICLES:
        html = build_article(a)
        with open(os.path.join(BASE, a["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(html)
    update_blog_index(ARTICLES)
    update_feed(ARTICLES)
    update_sitemap(ARTICLES)
    print(f"Wygenerowano {len(ARTICLES)} artykułów + zaktualizowano blog.html, feed.xml, sitemap.xml")


if __name__ == "__main__":
    main()
