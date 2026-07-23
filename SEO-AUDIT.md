# Audyt SEO — 33bots.pl

**Data:** 2026-07-23 · **Zakres:** 194 pliki HTML (statyczny serwis), sitemap.xml, robots.txt, feed.xml, llms.txt, _redirects

## Podsumowanie

Serwis jest technicznie w bardzo dobrym stanie — fundamenty SEO (title, description, canonical, Open Graph, JSON-LD, sitemap, robots.txt, hreflang, RSS, llms.txt) są kompletne i spójne na praktycznie wszystkich podstronach. Audyt nie wykazał żadnych braków krytycznych typu „brak meta", duplikaty title czy zepsute canonicale.

Główne ryzyka są trzy i wszystkie dotyczą **jakości, nie braków**:

1. **Ryzyko kary za spamerskie dane strukturalne** — `lowPrice: 1` PLN i ten sam `aggregateRating` (5.0, 3 opinie) powielony na 147 podstronach.
2. **Ryzyko klasyfikacji stron miejskich jako doorway pages** — 42 strony `robot-wynajem-*` mają ~62–64% wspólnej treści.
3. **Podwójne śledzenie analityki** — GTM i osobny tag GA4 na każdej stronie (nie wpływa na ranking, ale zafałszowuje dane, na których opiera się strategia SEO).

---

## Co działa dobrze ✅

| Obszar | Stan |
|---|---|
| Title / meta description | 100% pokrycia, zero duplikatów na 193 indeksowalnych stronach |
| Canonical | Poprawny i zgodny z URL na każdej stronie (1 wyjątek: szablon, patrz niżej) |
| Open Graph + Twitter Cards | Komplet na 192 stronach, z wymiarami obrazka i og:video na stronie głównej |
| JSON-LD | Bogaty zestaw: Product, FAQPage, HowTo, VideoObject, BreadcrumbList (192 str.), BlogPosting na wszystkich 39 wpisach bloga z `datePublished` |
| Sitemap.xml | 192 URL-e, wszystkie wskazują istniejące pliki; sekcja video:video dla strony głównej; aktualne `lastmod` |
| Robots.txt | Poprawny, z sitemapą i jawnym dopuszczeniem crawlerów AI (GPTBot, ClaudeBot, PerplexityBot…) |
| llms.txt + feed.xml (42 wpisy) | Rzadko spotykana, dobra praktyka pod AI search |
| Hreflang | pl + x-default na 192 stronach |
| Nagłówki | Dokładnie jeden `<h1>` na każdej stronie |
| Obrazy | Wszystkie `<img>` mają `alt`; hero w `<picture>` z WebP, `preload` + `fetchpriority="high"` + responsywne `srcset` |
| Przekierowania | www→bez-www i http→https (301) w `_redirects` |
| 404.html i szablon | Poprawnie oznaczone `noindex` i wykluczone z sitemapy |
| Linki wewnętrzne | Zero martwych linków na stronach indeksowalnych |

---

## Problemy do naprawy

### 1. 🔴 Dane strukturalne z ryzykiem ręcznej kary (priorytet: wysoki)

**`"lowPrice": 1`** (PLN) występuje w schemacie `AggregateOffer` na **147 stronach**. Cena 1 zł jest nierealistyczna — Google traktuje nieprawdziwe ceny w danych strukturalnych jako spam (ryzyko ręcznego działania „Structured data issue" i utraty wszystkich rich results w serwisie).
**Fix:** wpisać realną cenę minimalną pakietu (np. faktyczną cenę najtańszej opcji) albo usunąć `lowPrice` i zostawić samo `priceCurrency` + `offerCount`.

**Ten sam `aggregateRating` (5.0, reviewCount 3) skopiowany na 147 stron.** Wytyczne Google wymagają, by opinie dotyczyły konkretnej rzeczy opisanej na danej stronie — identyczny sitewide rating jest klasyfikowane jako „self-serving reviews" i w najlepszym razie ignorowany, w gorszym karany.
**Fix:** zostawić `aggregateRating` + `Review` tylko na stronie głównej / ofertowej, usunąć z podstron miejskich i scenariuszowych.

### 2. 🟠 Strony miejskie jako potencjalne doorway pages (priorytet: wysoki)

42 strony `robot-wynajem-<miasto>.html` mają **62–64% identycznej treści** (porównanie Warszawa/Kraków/Gdańsk po usunięciu nazw miast). To klasyczny wzorzec doorway pages — przy tej skali (42 miasta × ten sam szkielet) Google może zdeindeksować część z nich lub obniżyć ocenę całej domeny.
**Fix:** dodać do każdej strony realnie lokalny blok treści (min. 200–300 słów unikalnych): dojazd/logistyka w danym mieście, lokalne obiekty eventowe (hale, hotele konferencyjne), zrealizowane eventy w regionie, lokalne FAQ. Strony bez ruchu i pozycji po 3–6 miesiącach warto skonsolidować (301 do strony wojewódzkiej/hubowej).

### 3. 🟠 Podwójny pomiar GA4 (priorytet: średni)

Każda z 194 stron ładuje **jednocześnie GTM (`GTM-MR7R7CJ3`) i bezpośredni tag gtag.js (`G-MNE9Y0S9QV`)**. Jeśli GA4 jest też skonfigurowane w kontenerze GTM, każda odsłona liczy się podwójnie — zawyżone pageviews, zaniżony bounce rate, błędne dane do decyzji SEO. Dodatkowo to zbędne ~100 KB JS na każdej stronie.
**Fix:** zostawić wyłącznie GTM i serwować GA4 przez kontener; usunąć bezpośredni snippet gtag.js.

### 4. 🟡 Meta descriptions za długie (priorytet: niski)

~15 stron ma description powyżej 165 znaków (max: index.html — 182 zn.). Google utnie je w SERP-ach, zwykle ucinając CTA „Sprawdź dostępność →".
**Fix:** skrócić do 150–160 znaków, zaczynając od frazy kluczowej, CTA na końcu.

### 5. 🟡 Title powyżej 65 znaków (priorytet: niski)

~14 stron ma title 70–82 znaki (np. `blog-robot-na-stoisko-targowe.html` — 82). Końcówka „| 33bots" będzie ucinana — nie jest to błąd, ale fraza kluczowa musi być na początku (jest — OK). Warto skrócić tam, gdzie ucinana jest treść merytoryczna, nie brand.

### 6. 🟡 Jeden wspólny og:image na 192 stronach (priorytet: niski)

Wszystkie strony (poza główną) używają tego samego `og-image.jpg`. Działa, ale strony miejskie i wpisy blogowe udostępniane w social media wyglądają identycznie.
**Fix (opcjonalny):** wygenerować dedykowane OG images przynajmniej dla wpisów blogowych i głównych stron ofertowych.

### 7. 🟡 `loading="lazy"` tylko na 8 stronach (priorytet: niski)

Obrazy poniżej fold na pozostałych stronach ładują się eagerly. Wpływ mały (strony są lekkie, 20–76 KB HTML), ale to jednolinijkowy fix w generatorach (`generate_*.py`).

### 8. ⚪ Drobiazgi

- `szablon-case-study.html` linkuje do nieistniejącego `case-study-SZABLON.html` — strona jest `noindex`, więc bez wpływu na SEO; warto poprawić przy okazji.
- `atrakcje-na-event.html` (76 KB) i `index.html` (72 KB) to najcięższe dokumenty HTML — nadal w normie, ale warto pilnować, by dalsze rozbudowy nie inline'owały kolejnych kilobajtów CSS/JS.

---

## Rekomendowana kolejność działań

1. Usunąć/urealnić `lowPrice: 1` i ograniczyć `aggregateRating` do 1–2 stron (szybkie, największe ryzyko).
2. Wyłączyć podwójny pomiar GA4 (szybkie, naprawia dane).
3. Program unikalizacji stron miejskich — zacząć od 10 największych miast (największy potencjał ruchu).
4. Skrócić za długie descriptions/titles przy najbliższej edycji generatorów.
5. Opcjonalnie: dedykowane OG images dla bloga, `loading="lazy"` sitewide.
