// Strony główne 33bots.de i 33bots.at w układzie strony PL.
// SEO i fakty rynku bez zmian, całość po niemiecku, zachowanie jak na .pl.
// Formularz testowany na przechwyconym requeście — nic nie trafia do Formspree
// ani do FormSubmit. Zapytania do innych serwerów (GTM, Albacross) są blokowane.
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { naruszeniaOdstepow, przewinCala } from './odstepy.mjs';

const RYNKI = [
  {
    kod: 'de', adres: 'http://127.0.0.1:8081/', lang: 'de',
    tytul: 'Humanoide Roboter für Events mieten — deutschlandweit | 33bots',
    kanoniczny: 'https://33bots.de/', h1: /humanoide roboter für events mieten/i,
    kotwice: ['top', 'hauptinhalt', 'referenzen', 'realisierungen', 'events', 'video', 'ueber-uns', 'auftritt',
      'leistungen', 'einsatzbereiche', 'case-study', 'preise', 'ablauf', 'faq', 'kontakt'],
    ldTypy: ['Product', 'FAQPage', 'ProfessionalService', 'WebSite'],
    ceny: ['ab 2.500 €', 'pro Veranstaltungstag', '850 €', '−15 %'],
    kontakt: ['kontakt@33bots.de'],
    nav: ['Referenzen', 'Auftritt', 'Preise', 'Ablauf', 'Blog'],
    formularz: 'https://formspree.io/f/mnjwvray', dodatkowe: {},
    blad: 'Senden fehlgeschlagen. Schreiben Sie uns an kontakt@33bots.de.',
    miejsce: 'Berlin, Messe Berlin',
    linkLexai: 'case-study-lexai.html',
    analityka: false, panel: true,
  },
  {
    kod: 'at', adres: 'http://127.0.0.1:8082/', lang: 'de-AT',
    tytul: 'Roboter mieten für Events in Österreich — ab 2.300 € | 33bots',
    kanoniczny: 'https://33bots.at/', h1: /roboter mieten für events in österreich/i,
    kotwice: ['top', 'hauptinhalt', 'referenzen', 'vertrauen', 'auftritt', 'moeglichkeiten', 'case-study',
      'preise', 'ablauf', 'faq', 'kontakt'],
    ldTypy: ['Product', 'FAQPage', 'ProfessionalService', 'HowTo', 'VideoObject', 'WebSite'],
    ceny: ['Individuelles Angebot', 'ab 2.300 €', 'netto', '−15 %'],
    kontakt: ['+48 531 408 004', 'kontakt@33bots.at'],
    nav: ['Referenzen', 'Auftritt', 'Preise', 'Ablauf', 'Angebot'],
    formularz: 'https://formsubmit.co/ajax/kontakt@33bots.at', dodatkowe: { _subject: 'Neue Anfrage über 33bots.at' },
    blad: 'Senden fehlgeschlagen. Rufen Sie an: +48 531 408 004 oder schreiben Sie an kontakt@33bots.at.',
    miejsce: 'Wien, Messe Wien',
    linkLexai: null,
    analityka: true, panel: false,
  },
];

const DESKTOP = { width: 1440, height: 900 };
const TELEFON = { width: 375, height: 812 };
const twarde = (t) => t.replace(/\u00a0/g, ' ').replace(/\u00ad/g, '');

// Cała treść elementu bez skryptów, ze zwiniętymi częściami, bez wielkich liter z CSS.
const tresc = (page, sel = 'body') => page.locator(sel).evaluate((el) => {
  const k = el.cloneNode(true);
  k.querySelectorAll('script, style, noscript').forEach((e) => e.remove());
  return k.textContent.replace(/\u00a0/g, ' ').replace(/\u00ad/g, '').replace(/\s+/g, ' ');
});

// Wszystko spoza serwera testowego (GTM, Albacross, formularze) jest blokowane.
async function zablokujZewnetrzne(page) {
  await page.route((url) => !url.href.startsWith('http://127.0.0.1'), (r) => r.abort());
}

async function nowaStrona(browser, m, { vp = DESKTOP, ruch = 'reduce', przed } = {}) {
  const ctx = await browser.newContext({ viewport: vp, reducedMotion: ruch });
  const page = await ctx.newPage();
  const bledy = [];
  page.on('pageerror', (e) => bledy.push(e.message));
  await zablokujZewnetrzne(page);
  if (przed) await przed(page);
  await page.goto(m.adres);
  await page.evaluate(() => document.fonts.ready);
  return { ctx, page, bledy };
}

for (const m of RYNKI) {
  test.describe(`33bots.${m.kod}`, () => {
    test('SEO bez zmian: tytuł, canonical, hreflang, jeden H1, dane strukturalne', async ({ browser }) => {
      const { ctx, page, bledy } = await nowaStrona(browser, m);
      await expect(page.locator('html')).toHaveAttribute('lang', m.lang);
      await expect(page).toHaveTitle(m.tytul);
      await expect(page.locator('link[rel="canonical"]')).toHaveAttribute('href', m.kanoniczny);
      const alternatywy = await page.evaluate(() => Object.fromEntries(
        [...document.querySelectorAll('link[rel="alternate"][hreflang]')].map((l) => [l.hreflang, l.href])));
      expect(alternatywy).toEqual({
        'de': 'https://33bots.de/', 'de-AT': 'https://33bots.at/', 'pl': 'https://33bots.pl/',
        'lt': 'https://33bots.lt/', 'x-default': 'https://33bots.pl/',
      });
      await expect(page.locator('h1')).toHaveCount(1);
      expect(await page.locator('h1').innerText()).toMatch(m.h1);
      const typy = await page.evaluate(() => [...document.querySelectorAll('script[type="application/ld+json"]')]
        .map((s) => JSON.parse(s.textContent)['@type']));
      expect(typy).toEqual(m.ldTypy);
      expect(await page.locator('meta[name="description"]').getAttribute('content')).toBeTruthy();
      expect(await page.locator('meta[property="og:image"]').getAttribute('content')).toContain(m.kanoniczny);
      expect(bledy).toEqual([]);
      await ctx.close();
    });

    test('struktura jak na .pl, dawne kotwice działają, identyfikatory unikalne', async ({ browser }) => {
      const { ctx, page } = await nowaStrona(browser, m);
      const kolejnosc = await page.evaluate(() => [...document.querySelectorAll('main > section')].map((s) => s.id || s.className));
      expect(kolejnosc).toEqual(['hero', 'proof', 'referenzen', 'auftritt', 'case-study', 'preise', 'ablauf', 'faq', 'kontakt']);
      const numery = await page.evaluate(() => [...document.querySelectorAll('.sec .sec__meta')].map((e) => e.textContent.trim().slice(0, 7)));
      expect(numery).toEqual(['04 / 11', '05 / 11', '06 / 11', '07 / 11', '08 / 11', '09 / 11', '10 / 11']);
      for (const id of m.kotwice) expect(await page.locator(`#${id}`).count(), `#${id}`).toBe(1);
      const duplikaty = await page.evaluate(() => {
        const ile = {};
        for (const e of document.querySelectorAll('[id]')) ile[e.id] = (ile[e.id] || 0) + 1;
        return Object.entries(ile).filter(([, n]) => n > 1).map(([id]) => id);
      });
      expect(duplikaty).toEqual([]);
      // Linki wewnątrz strony prowadzą do istniejących kotwic.
      const martwe = await page.evaluate(() => [...document.querySelectorAll('a[href^="#"]')]
        .map((a) => a.getAttribute('href').slice(1)).filter((id) => id && !document.getElementById(id)));
      expect(martwe).toEqual([]);
      expect((await page.locator('.nav__menu a').allInnerTexts()).map((t) => t.trim())).toEqual(m.nav);
      await ctx.close();
    });

    test('link „Zum Hauptinhalt springen” jako pierwszy element dla klawiatury', async ({ browser }) => {
      const { ctx, page } = await nowaStrona(browser, m);
      await page.keyboard.press('Tab');
      const skip = page.locator('.skip-link');
      await expect(skip).toBeFocused();
      await expect(skip).toHaveText('Zum Hauptinhalt springen');
      expect((await skip.boundingBox()).x).toBeGreaterThanOrEqual(0);
      await page.keyboard.press('Enter');
      await expect(page.locator('main#hauptinhalt')).toBeFocused();
      await ctx.close();
    });

    test('wszystko po niemiecku: bez polskich napisów, także w skrypcie i opisach zdjęć', async ({ browser }) => {
      const { ctx, page } = await nowaStrona(browser, m);
      const POLSKIE = /\b(Sprawdź|Zobacz|realizacj|wydarze|Płacisz|Wznów|Zatrzymaj|Następne|Zamknij|Wstecz|Dalej|Wysyłanie|Rezerwacja|Pełne case study|Wszystkie|Robot humanoidalny|Odpowiadamy|Gmina|Ogród|Drezdeńska)\w*/i;
      expect((await tresc(page)).match(POLSKIE)).toBeNull();
      const atrybuty = await page.evaluate(() => [...document.querySelectorAll('[alt], [aria-label], [placeholder], [data-faq]')]
        .flatMap((e) => ['alt', 'aria-label', 'placeholder', 'data-faq'].map((a) => e.getAttribute(a)).filter(Boolean)));
      expect(atrybuty.filter((a) => POLSKIE.test(a))).toEqual([]);
      // Teksty wstawiane przez skrypt: przycisk hero, przyciski pasów, menu, szuflada.
      await expect(page.locator('#heroPauza')).toHaveText('Nächstes Foto');
      await expect(page.locator('#navPrzycisk')).toHaveText('Menü');
      await page.locator('.realizacja[data-cs="drezno"], .kadr[data-cs="drezno"]').first().click();
      await expect(page.locator('#szufladaZamknij')).toHaveText('Schließen');
      expect(twarde(await page.locator('#szuflada').innerText()).match(POLSKIE)).toBeNull();
      await ctx.close();
    });

    test('treść: robot mówi po niemiecku i w każdym innym języku, branding w cenie, bez „Kostüm”', async ({ browser }) => {
      const { ctx, page } = await nowaStrona(browser, m);
      const lead = page.locator('.hero .lead');
      await expect(lead).toContainText('Er spricht Deutsch und jede andere Sprache');
      await expect(lead).toContainText('Branding im Preis');
      await expect(page.locator('#auftritt')).toContainText('Litauen, Deutschland, Tschechien und Rumänien');
      await expect(page.locator('#auftritt')).toContainText('wechselt während einer Veranstaltung zwischen den Sprachen');
      await expect(page.locator('#referenzen')).toContainText('über 40 Veranstaltungen in fünf Ländern');
      expect(await tresc(page, '.faq')).toContain('Der Roboter spricht Deutsch und jede andere Sprache');
      expect(await tresc(page)).not.toMatch(/Kostüm|Outfit|Garderobe|kostenlos|gratis/i);
      await ctx.close();
    });

    test('fakty rynku: ceny, kontakt, formularz rynku', async ({ browser }) => {
      const { ctx, page } = await nowaStrona(browser, m);
      const ceny = await tresc(page, '#preise');
      for (const c of m.ceny) expect(ceny, c).toContain(c);
      const kontakt = await tresc(page, '#kontakt');
      for (const k of m.kontakt) expect(kontakt, k).toContain(k);
      const telefony = await page.locator('a[href^="tel:"]').count();
      if (m.kod === 'de') {
        expect(telefony, '33bots.de nie podaje telefonu').toBe(0);
        expect(await tresc(page)).not.toMatch(/netto|\+48/);
      } else {
        expect(telefony).toBeGreaterThan(0);
        await expect(page.locator('a[href^="tel:"]').first()).toHaveAttribute('href', 'tel:+48531408004');
      }
      const skrypt = await page.evaluate(() => [...document.scripts].map((s) => s.textContent).join('\n'));
      expect(skrypt).toContain(`fetch("${m.formularz}"`);
      await ctx.close();
    });

    test('analityka i zgody jak dotąd', async ({ browser }) => {
      const { ctx, page } = await nowaStrona(browser, m, { przed: (p) => p.clock.install() });
      const html = await page.content();
      if (!m.analityka) {
        expect(html).not.toMatch(/googletagmanager|albacross|gtag\(/);
        await expect(page.locator('#cookies')).toHaveCount(0);
        expect(html).toContain('Keine Analyse-Dienste');
      } else {
        expect(html).toContain("'GTM-MR7R7CJ3'");
        // <noscript> przy włączonym JS to zwykły tekst — sprawdzamy źródło.
        expect(html).toMatch(/<noscript><iframe src="https:\/\/www\.googletagmanager\.com\/ns\.html\?id=GTM-MR7R7CJ3"/);
        await expect(page.locator('script[src="https://serve.albacross.com/track.js"]')).toHaveCount(1);
        const csp = await page.locator('meta[http-equiv="Content-Security-Policy"]').getAttribute('content');
        expect(csp).toContain('https://formsubmit.co');
        // Baner cookie: treść bez zmian, pojawia się sam, znika po kliknięciu i nie wraca.
        const baner = page.locator('#cookies');
        await expect(baner.locator('.cookies__text')).toHaveText('Wir verwenden Cookies zu Analysezwecken.');
        await expect(baner.locator('#cookiesOk')).toHaveText('Verstanden');
        await page.clock.runFor(1500);
        await expect(baner).toHaveClass(/show/);
        await expect(baner).toBeVisible();
        await baner.locator('#cookiesOk').click();
        await expect(baner).toBeHidden();
        expect(await page.evaluate(() => localStorage.getItem('33bots-cookies'))).toBe('1');
        await page.reload();
        await page.clock.runFor(3000);
        await expect(page.locator('#cookies')).toBeHidden();
      }
      await ctx.close();
    });

    for (const szer of [320, 375, 768, 1024, 1440]) {
      test(`układ ${szer}px: bez przewijania w bok, nagłówki i przyciski mieszczą się`, async ({ browser }) => {
        const { ctx, page } = await nowaStrona(browser, m, { vp: { width: szer, height: 900 } });
        await przewinCala(page);
        expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
        const wystaje = await page.evaluate(() => [...document.querySelectorAll('.h2, .h3, .display, .num, .btn, .label')]
          .filter((e) => e.offsetParent && e.scrollWidth > e.clientWidth + 1).map((e) => e.textContent.trim().slice(0, 40)));
        expect(wystaje).toEqual([]);
        // Tekst hero nie wchodzi na zdjęcie.
        const hero = await page.evaluate(() => {
          const t = document.querySelector('.hero__text').getBoundingClientRect();
          return [...document.querySelectorAll('.hero__text > *')].every((e) => e.getBoundingClientRect().right <= t.right + 1);
        });
        expect(hero).toBe(true);
        // Nawigacja: elementy w jednym rzędzie, w ekranie, bez nakładania.
        const nav = await page.evaluate(() => {
          const el = [...document.querySelectorAll('.nav__logo, .nav__akcje > *')].filter((e) => e.offsetParent && getComputedStyle(e).position !== 'fixed');
          const r = el.map((e) => e.getBoundingClientRect());
          const nakladaja = r.some((a, i) => r.some((b, j) => i < j && a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom));
          return { wEkranie: r.every((x) => x.left >= 0 && x.right <= innerWidth), nakladaja };
        });
        expect(nav).toEqual({ wEkranie: true, nakladaja: false });
        await ctx.close();
      });
    }

    for (const [vp, minimum] of [[TELEFON, 24], [DESKTOP, 32]]) {
      test(`odstępy tekstu od krawędzi ramek i teł ≥ ${minimum} px @${vp.width}`, async ({ browser }) => {
        const { ctx, page } = await nowaStrona(browser, m, { vp });
        await przewinCala(page);
        const naruszenia = await naruszeniaOdstepow(page, minimum);
        expect(naruszenia, JSON.stringify(naruszenia, null, 1)).toEqual([]);
        await ctx.close();
      });

      test(`axe: kontrast tekstu @${vp.width}`, async ({ browser }) => {
        const { ctx, page } = await nowaStrona(browser, m, { vp });
        await przewinCala(page);
        const wynik = await new AxeBuilder({ page }).withRules(['color-contrast']).analyze();
        const naruszenia = wynik.violations.flatMap((v) => v.nodes.map((n) => n.target.join(' ')));
        expect(naruszenia).toEqual([]);
        await ctx.close();
      });
    }

    test('axe: WCAG 2.1 A/AA bez naruszeń', async ({ browser }) => {
      const { ctx, page } = await nowaStrona(browser, m);
      await przewinCala(page);
      const wynik = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
      const naruszenia = wynik.violations.map((v) => `${v.id}: ${v.nodes.map((n) => n.target.join(' ')).slice(0, 3).join(' | ')}`);
      expect(naruszenia).toEqual([]);
      await ctx.close();
    });

    test('FAQ: 10 pytań zgodnych z FAQPage, akordeon działa', async ({ browser }) => {
      const { ctx, page } = await nowaStrona(browser, m);
      const widoczne = (await page.locator('.faq__q').allInnerTexts()).map((t) => t.trim());
      const ld = await page.evaluate(() => {
        for (const s of document.querySelectorAll('script[type="application/ld+json"]')) {
          const d = JSON.parse(s.textContent);
          if (d['@type'] === 'FAQPage') return d.mainEntity.map((q) => [q.name, q.acceptedAnswer.text]);
        }
        return [];
      });
      expect(widoczne).toEqual(ld.map(([q]) => q));
      expect(widoczne.length).toBe(10);
      const odpowiedzi = await page.locator('.faq__a', { includeHidden: true }).evaluateAll((a) => a.map((e) => e.textContent.trim()));
      expect(odpowiedzi.map(twarde)).toEqual(ld.map(([, a]) => twarde(a)));
      const q = page.locator('.faq__q').nth(2);
      await q.click();
      await expect(q).toHaveAttribute('aria-expanded', 'true');
      await expect(page.locator('#faq-3')).toBeVisible();
      await q.click();
      await expect(page.locator('#faq-3')).toBeHidden();
      await ctx.close();
    });

    test('szuflada realizacji: dane po niemiecku, fokus w środku, Esc zamyka', async ({ browser }) => {
      const { ctx, page } = await nowaStrona(browser, m);
      await expect(page.locator('.kadr[data-cs="drezno"]')).toHaveAttribute('aria-label', 'Einsatz ansehen: Dresdner Schlössernacht');
      const kafel = page.locator('.realizacja[data-cs="lexai"]');
      await kafel.click();
      await expect(page.locator('#szufladaTytul')).toHaveText('LEX AI');
      await expect(page.locator('#szufladaPodpis')).toHaveText('Langer Markt · Danzig');
      await expect(page.locator('#szufladaOpis')).toContainText('Neptunbrunnen');
      if (m.linkLexai) await expect(page.locator('#szufladaLink')).toHaveAttribute('href', m.linkLexai);
      else await expect(page.locator('#szufladaLink')).toBeHidden();
      await expect(page.locator('#szufladaZamknij')).toBeFocused();
      for (let i = 0; i < 5; i++) await page.keyboard.press('Tab');
      expect(await page.evaluate(() => document.getElementById('szuflada').contains(document.activeElement))).toBe(true);
      await page.keyboard.press('Escape');
      await expect(page.locator('#szuflada')).toBeHidden();
      await expect(kafel).toBeFocused();
      // Każda realizacja z pasów ma niemieckie dane w szufladzie.
      for (const klucz of await page.evaluate(() => [...new Set([...document.querySelectorAll('[data-cs]')].map((b) => b.dataset.cs))])) {
        await page.locator(`[data-cs="${klucz}"]`).first().click();
        await expect(page.locator('#szufladaTytul'), klucz).not.toBeEmpty();
        await expect(page.locator('#szufladaOpis'), klucz).toContainText(/Roboter/);
        await page.keyboard.press('Escape');
      }
      await ctx.close();
    });

    test('formularz: krok 1 → krok 2, walidacja po niemiecku, zgłoszenie (request przechwycony)', async ({ browser }) => {
      let wyslane = null;
      const { ctx, page } = await nowaStrona(browser, m, {
        przed: (p) => p.route(m.formularz, async (r) => {
          wyslane = r.request().postDataJSON();
          await r.fulfill({ status: 200, contentType: 'application/json', body: '{"ok":true}' });
        }),
      });
      await page.locator('#formularz').scrollIntoViewIfNeeded();
      await page.locator('#dalej').click();
      await expect(page.locator('#blad-typ')).toHaveText('Wählen Sie die Art der Veranstaltung.');
      await expect(page.locator('#krok2')).toBeHidden();
      expect((await page.locator('#pole-typ label.chip').allInnerTexts()).map((t) => t.trim()))
        .toEqual(['Gala', 'Konferenz', 'Messe', 'Outdoor', 'Sonstiges']);

      await page.locator('label.chip:has-text("Konferenz")').click();
      await expect(page.locator('#blad-typ')).toBeHidden();
      await page.locator('label.chip:has-text("Termin noch offen")').click();
      await expect(page.locator('#pole-data')).toBeDisabled();
      await expect(page.locator('#pole-miejsce')).toHaveAttribute('placeholder', `z. B. ${m.miejsce}`);
      await page.fill('#pole-miejsce', m.miejsce);
      await page.locator('label.chip:has-text("500–2000")').click();
      await page.locator('#dalej').click();
      await expect(page.locator('#krok2')).toBeVisible();
      await expect(page.locator('#pole-name')).toBeFocused();

      await page.locator('#wyslij').click();
      await expect(page.locator('#pole-imie .pole__blad')).toHaveText('Bitte geben Sie Ihren Namen an.');
      await page.fill('#pole-name', 'Max Test');
      await page.fill('#pole-email', 'kein-adresse');
      await page.locator('#wyslij').click();
      await expect(page.locator('#pole-mail .pole__blad')).toHaveText('Bitte geben Sie eine gültige E-Mail-Adresse an.');
      expect(wyslane).toBeNull();

      await page.fill('#pole-email', 'max@test.de');
      await page.fill('#pole-company', 'Test GmbH');
      await page.fill('#pole-message', 'Konferenz, zwei Tage.');
      await expect(page.locator('#licznik')).toHaveText('21');
      await page.locator('#wyslij').click();
      const sukces = page.locator('.form-sukces');
      await expect(sukces).toBeVisible();
      await expect(sukces).toContainText('Ihre Anfrage ist bei uns angekommen.');
      await expect(sukces).toContainText('Wir melden uns unter max@test.de.');
      expect(wyslane).toEqual({
        name: 'Max Test', company: 'Test GmbH', email: 'max@test.de', phone: '—', date: 'offen',
        location: m.miejsce, message: 'Konferenz, zwei Tage.', event_type: 'Konferenz', guests: '500–2000',
        ...m.dodatkowe,
      });
      await ctx.close();
    });

    test('formularz: błąd serwera — komunikat z kontaktem rynku, przycisk wraca', async ({ browser }) => {
      const { ctx, page } = await nowaStrona(browser, m, {
        przed: (p) => p.route(m.formularz, (r) => r.fulfill({ status: 500, body: '' })),
      });
      await page.locator('label.chip:has-text("Gala")').click();
      await page.locator('#dalej').click();
      await page.fill('#pole-name', 'Max Test');
      await page.fill('#pole-email', 'max@test.de');
      await page.locator('#wyslij').click();
      await expect(page.locator('#blad-wysylki')).toHaveText(m.blad);
      await expect(page.locator('#wyslij')).toBeEnabled();
      await expect(page.locator('#wyslij')).toContainText('Verfügbarkeit prüfen');
      await ctx.close();
    });

    test('hero: co 3 s kolejny kadr z niemieckim podpisem, pauza zatrzymuje', async ({ browser }) => {
      const { ctx, page } = await nowaStrona(browser, m, { ruch: 'no-preference', przed: (p) => p.clock.install() });
      await page.waitForLoadState('load');
      const licznik = page.locator('#heroLicznik');
      await expect(licznik).toHaveText('01 / 06');
      await expect(page.locator('#heroOpis')).toHaveText('Dresdner Schlössernacht · Dresden');
      await page.evaluate(() => {
        const el = document.getElementById('heroLicznik');
        window.__zmiany = [[Date.now(), el.textContent.trim()]];
        new MutationObserver(() => window.__zmiany.push([Date.now(), el.textContent.trim()]))
          .observe(el, { childList: true, characterData: true, subtree: true });
      });
      const dojdzDo = async (tekst) => {
        for (let i = 0; i < 40 && (await licznik.textContent()).trim() !== tekst; i++) {
          await page.clock.runFor(200); await page.waitForTimeout(20);
        }
        await expect(licznik).toHaveText(tekst);
      };
      await page.clock.runFor(2000); await page.waitForTimeout(50);
      await expect(licznik).toHaveText('01 / 06');
      await dojdzDo('02 / 06');
      await expect(page.locator('#heroOpis')).toHaveText('Finale Eco Studio ELECTRO-SYSTEM · Warschau');
      await expect(page.locator('.hero img')).toHaveAttribute('alt', /Journalistin interviewt/);
      for (let n = 3; n <= 6; n++) await dojdzDo(`0${n} / 06`);
      await dojdzDo('01 / 06');
      const zmiany = await page.evaluate(() => window.__zmiany);
      expect(zmiany.map(([, t]) => t)).toEqual(['01 / 06', '02 / 06', '03 / 06', '04 / 06', '05 / 06', '06 / 06', '01 / 06']);
      for (const d of zmiany.slice(2).map(([t], i) => t - zmiany[i + 1][0])) {
        expect(d).toBeGreaterThanOrEqual(3000);
        expect(d).toBeLessThan(4200);
      }
      const pauza = page.locator('#heroPauza');
      await expect(pauza).toHaveText('Pause');
      await pauza.click();
      await expect(pauza).toHaveAttribute('aria-pressed', 'true');
      await expect(pauza).toHaveText('Weiter');
      await page.mouse.move(5, 5);
      await page.evaluate(() => document.activeElement.blur());
      await page.clock.runFor(30000); await page.waitForTimeout(200);
      await expect(licznik).toHaveText('01 / 06');
      await ctx.close();
    });

    test('pasy: ruch bez końca, kopie poza dostępnością, pauza z niemieckim napisem', async ({ browser }) => {
      const { ctx, page } = await nowaStrona(browser, m, { ruch: 'no-preference' });
      await page.waitForLoadState('load');
      const zdjecia = page.locator('.pasy[data-grupa="zdjecia"]');
      await zdjecia.scrollIntoViewIfNeeded();
      await page.mouse.move(2, 2);
      const x = () => page.evaluate(() => [...document.querySelectorAll('.pas')].map((p) => new DOMMatrix(getComputedStyle(p.querySelector('.pas__tor')).transform).m41));
      const a = await x(); await page.waitForTimeout(1200); const b = await x();
      for (const i of [0, 1, 2]) expect(Math.abs(b[i] - a[i]), `rząd ${i + 1}`).toBeGreaterThan(10);
      const kopie = await page.evaluate(() => [...document.querySelectorAll('.pas__tor > [data-kopia]')]
        .every((li) => li.getAttribute('aria-hidden') === 'true' && [...li.querySelectorAll('button, a')].every((e) => e.tabIndex === -1)));
      expect(kopie).toBe(true);
      const pauza = page.locator('.pasy__pauza[data-pasy="zdjecia"]');
      await expect(pauza).toHaveText('Bewegung anhalten');
      await pauza.click();
      await expect(pauza).toHaveText('Bewegung fortsetzen');
      await expect(pauza).toHaveAttribute('aria-pressed', 'true');
      // Nazwy klientów: 40 bez powtórzeń (jak na .pl), utarte nazwy po niemiecku.
      const nazwy = await page.locator('.pasy[data-grupa="nazwy"] .pas__tor > li:not([data-kopia])').allInnerTexts();
      expect(nazwy.length).toBe(40);
      expect(new Set(nazwy).size).toBe(40);
      expect(nazwy).toContain('Cashify');
      expect(nazwy).toEqual(expect.arrayContaining(['Dresdner Schlössernacht', 'Gemeinde Jednorożec', 'Perspektywy Foundation · Women in Tech Summit']));
      await ctx.close();
    });

    test('menu mobilne: Menü / Schließen, Esc zamyka', async ({ browser }) => {
      const { ctx, page } = await nowaStrona(browser, m, { vp: TELEFON });
      const p = page.locator('#navPrzycisk');
      await p.click();
      await expect(p).toHaveText('Schließen');
      await expect(page.locator('#navPanel')).toBeVisible();
      await page.keyboard.press('Escape');
      await expect(page.locator('#navPanel')).toBeHidden();
      await expect(p).toHaveText('Menü');
      await expect(p).toBeFocused();
      await ctx.close();
    });

    test('zdjęcia: każdy plik istnieje, także kadry hero ładowane później', async ({ browser }) => {
      const brak = [];
      const { ctx, page } = await nowaStrona(browser, m, {
        przed: (p) => p.on('response', (r) => { if (r.status() >= 400) brak.push(`${r.status()} ${r.url()}`); }),
      });
      await przewinCala(page);
      const slajdy = await page.evaluate(() => [...document.scripts].map((s) => s.textContent).join('')
        .match(/src: "([^"]+\.jpg)"/g).map((s) => s.slice(6, -1)));
      expect(slajdy.length).toBe(6);
      for (const s of slajdy) expect((await page.request.get(m.adres + s)).status(), s).toBe(200);
      expect(brak).toEqual([]);
      await ctx.close();
    });
  });
}

// ——— Panel dostępności (tylko 33bots.de, BFSG) ———
const DE = RYNKI[0];
test.describe('33bots.de — panel dostępności', () => {
  for (const vp of [TELEFON, DESKTOP]) {
    test(`przycisk w nawigacji, panel w ekranie, ustawienia działają @${vp.width}`, async ({ browser }) => {
      const { ctx, page } = await nowaStrona(browser, DE, { vp });
      const przycisk = page.locator('#a11yToggle');
      await expect(przycisk).toBeVisible();
      expect(await przycisk.evaluate((b) => !!b.closest('header.nav'))).toBe(true);
      await przycisk.click();
      const panel = page.locator('#a11yPanel');
      await expect(panel).toBeVisible();
      await expect(przycisk).toHaveAttribute('aria-expanded', 'true');
      await expect(page.locator('.a11y-opt').first()).toBeFocused();
      const r = await panel.boundingBox();
      expect(r.x).toBeGreaterThanOrEqual(0);
      expect(r.x + r.width).toBeLessThanOrEqual(vp.width);
      expect(r.y + r.height).toBeLessThanOrEqual(vp.height);

      await panel.locator('[data-a11y="font"][data-value="large"]').click();
      await expect(page.locator('html')).toHaveAttribute('data-a11y-font', 'large');
      expect(await page.evaluate(() => getComputedStyle(document.documentElement).fontSize)).toBe('18px');
      await panel.locator('[data-a11y="theme"][data-value="light"]').click();
      await expect(page.locator('body')).toHaveCSS('background-color', 'rgb(255, 255, 255)');
      await expect(panel.locator('[data-a11y="theme"][data-value="light"]')).toHaveAttribute('aria-pressed', 'true');
      await page.locator('#a11yReset').click();
      await expect(page.locator('html')).toHaveAttribute('data-a11y-theme', 'dark');
      await expect(page.locator('html')).toHaveAttribute('data-a11y-font', 'normal');

      await page.keyboard.press('Escape');
      await expect(panel).toBeHidden();
      await expect(przycisk).toBeFocused();
      await expect(przycisk).toHaveAttribute('aria-label', 'Einstellungen zur Barrierefreiheit öffnen');
      await ctx.close();
    });
  }

  test('„Animationen: Aus” zatrzymuje hero i pasy, „An” wznawia', async ({ browser }) => {
    const { ctx, page } = await nowaStrona(browser, DE, { ruch: 'no-preference' });
    await page.waitForLoadState('load');
    await page.locator('#a11yToggle').click();
    await page.locator('[data-a11y="motion"][data-value="off"]').click();
    await expect(page.locator('#heroPauza')).toHaveAttribute('aria-pressed', 'true');
    for (const p of await page.locator('.pasy__pauza').all()) await expect(p).toHaveAttribute('aria-pressed', 'true');
    await page.locator('[data-a11y="motion"][data-value="on"]').click();
    await expect(page.locator('#heroPauza')).toHaveAttribute('aria-pressed', 'false');
    for (const p of await page.locator('.pasy__pauza').all()) await expect(p).toHaveAttribute('aria-pressed', 'false');
    await ctx.close();
  });

  test('zapisane ustawienia działają od pierwszego malowania; ruch wyłączony = nic nie jedzie', async ({ browser }) => {
    const { ctx, page } = await nowaStrona(browser, DE, {
      ruch: 'no-preference',
      przed: (p) => p.addInitScript(() => localStorage.setItem('a11y-prefs', JSON.stringify({ theme: 'light', motion: 'off' }))),
    });
    // atrybut ustawiony w <head>, zanim cokolwiek się narysowało
    expect(await page.evaluate(() => performance.getEntriesByType('paint').length === 0
      || document.documentElement.getAttribute('data-a11y-theme') === 'light')).toBe(true);
    await expect(page.locator('html')).toHaveAttribute('data-a11y-theme', 'light');
    await expect(page.locator('#heroPauza')).toHaveText('Nächstes Foto');
    expect(await page.locator('[data-kopia]').count()).toBe(0);
    await ctx.close();
  });

  for (const [nazwa, ustawienia] of [['jasny motyw', { theme: 'light' }], ['wysoki kontrast', { contrast: 'high' }],
    ['jasny + wysoki kontrast', { theme: 'light', contrast: 'high' }]]) {
    test(`axe: kontrast tekstu — ${nazwa}`, async ({ browser }) => {
      const { ctx, page } = await nowaStrona(browser, DE, {
        przed: (p) => p.addInitScript((u) => localStorage.setItem('a11y-prefs', JSON.stringify(u)), ustawienia),
      });
      await przewinCala(page);
      const wynik = await new AxeBuilder({ page }).withRules(['color-contrast']).analyze();
      const naruszenia = wynik.violations.flatMap((v) => v.nodes.map((n) => n.target.join(' ')));
      expect(naruszenia).toEqual([]);
      await ctx.close();
    });
  }
});

// ——— Podstrony: te same porządki co podstrony .pl (tresci/zagranica/podstrony.py) ———
// 33bots.de: przekrój szablonów (miasto, oferta, poradnik, case study, strony prawne);
// 33bots.at: wszystkie podstrony.
const PODSTRONY = [
  [RYNKI[0], ['/roboter-mieten-berlin.html', '/angebot-messen.html', '/angebot-konferenzen-galas.html', '/leistungen.html',
    '/referenzen-videos.html', '/case-study-lexai.html', '/case-study-women-in-tech.html', '/blog.html',
    '/blog-attraktion-firmenevent.html', '/blog-was-kostet-roboter-mieten.html', '/roboter-abiball.html',
    '/humanoider-roboter-event.html', '/event-attraktionen.html', '/impressum.html', '/404.html']],
  [RYNKI[1], ['/humanoider-roboter-mieten.html', '/messe-roboter-mieten.html', '/unitree-g1-mieten.html', '/kontakt.html',
    '/impressum.html', '/datenschutz.html', '/danke.html', '/404.html',
    ...['wien', 'graz', 'linz', 'salzburg', 'innsbruck', 'klagenfurt', 'villach', 'wels', 'st-poelten', 'dornbirn', 'eisenstadt']
      .map((m) => `/roboter-mieten-${m}.html`)]],
];
for (const [m, strony] of PODSTRONY) {
  for (const strona of strony) {
    for (const [vp, minimum] of [[TELEFON, 24], [DESKTOP, 32]]) {
      test(`33bots.${m.kod}${strona} @${vp.width}: odstępy ≥ ${minimum} px, bez przewijania w bok, kroje lokalne, bez błędów`, async ({ browser }) => {
        const ctx = await browser.newContext({ viewport: vp, reducedMotion: 'reduce' });
        const page = await ctx.newPage();
        const bledy = [];
        const obce = [];
        page.on('pageerror', (e) => bledy.push(e.message));
        page.on('request', (r) => { if (/fonts\.(googleapis|gstatic)\.com/.test(r.url())) obce.push(r.url()); });
        await zablokujZewnetrzne(page);
        await page.goto(m.adres.replace(/\/$/, '') + strona);
        await page.evaluate(() => document.fonts.ready);
        await przewinCala(page);
        expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
        const naruszenia = await naruszeniaOdstepow(page, minimum);
        expect(naruszenia, JSON.stringify(naruszenia, null, 1)).toEqual([]);
        const fonty = await page.evaluate(() => [...new Set([...document.fonts].filter((f) => f.status === 'loaded').map((f) => f.family))]);
        expect(fonty).toEqual(expect.arrayContaining(['Space Grotesk', 'Plus Jakarta Sans']));
        expect(obce, 'Google Fonts').toEqual([]);
        expect(await page.locator('#cursorGlow, #scrollProgress').count()).toBe(0);
        expect(bledy).toEqual([]);
        await ctx.close();
      });
    }
  }
}
