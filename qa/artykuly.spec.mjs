// Artykuły poradnika (tresci/artykuly → strony w katalogu głównym): SEO, dane
// strukturalne zgodne z treścią, wspólne menu i stopka, kontrast, słownictwo.
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { readdirSync } from 'node:fs';
import { fontyZRepo } from './odstepy.mjs';

const ARTYKULY = readdirSync(new URL('../tresci/artykuly/', import.meta.url)).filter((f) => f.endsWith('.html'));
const BAZA = 'http://localhost:8080/';

test.use({ contextOptions: { reducedMotion: 'reduce' } });

for (const plik of ARTYKULY) {
  test(`artykuł ${plik}: SEO, dane strukturalne, menu, słownictwo`, async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await fontyZRepo(page);
    const bledy = [];
    page.on('pageerror', (e) => bledy.push(e.message));
    await page.goto(BAZA + plik);
    await page.evaluate(() => document.fonts.ready);

    // podstawy SEO
    await expect(page.locator('h1')).toHaveCount(1);
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute('href', `https://33bots.pl/${plik}`);
    const tytul = await page.title();
    expect(tytul.length).toBeLessThanOrEqual(65);
    const opis = await page.locator('meta[name="description"]').getAttribute('content');
    expect(opis.length).toBeGreaterThan(80);
    expect(opis.length).toBeLessThanOrEqual(160);
    expect(await page.locator('script[src*="googletagmanager"], script:not([src])').evaluateAll((s) => s.some((x) => x.textContent.includes('GTM-MR7R7CJ3')))).toBe(true);

    // dane strukturalne zgodne z tym, co widać
    const ld = await page.evaluate(() => [...document.querySelectorAll('script[type="application/ld+json"]')].map((s) => JSON.parse(s.textContent)));
    const typy = ld.map((d) => d['@type']);
    expect(typy).toEqual(expect.arrayContaining(['BlogPosting', 'BreadcrumbList']));
    const wpis = ld.find((d) => d['@type'] === 'BlogPosting');
    expect(wpis.headline).toBe((await page.locator('h1').innerText()).replace(/\s+/g, ' ').trim());
    expect(wpis.mainEntityOfPage['@id']).toBe(`https://33bots.pl/${plik}`);
    const faq = ld.find((d) => d['@type'] === 'FAQPage');
    const pytania = (await page.locator('.faq__q').allInnerTexts()).map((t) => t.replace(/\s+/g, ' ').trim());
    if (faq) expect(pytania).toEqual(faq.mainEntity.map((q) => q.name));
    else expect(pytania).toEqual([]);

    // spis treści prowadzi do istniejących nagłówków
    const kotwice = await page.locator('.spis a').evaluateAll((a) => a.map((x) => x.getAttribute('href').slice(1)));
    expect(kotwice.length).toBeGreaterThanOrEqual(4);
    for (const id of kotwice) expect(await page.locator(`[id="${id}"]`).count(), id).toBe(1);

    // menu i stopka jak na stronie głównej, linki menu prowadzą na index.html
    expect(await page.locator('.nav__menu a').evaluateAll((a) => a.every((x) => x.getAttribute('href').startsWith('index.html#') || x.getAttribute('href').endsWith('.html')))).toBe(true);
    await expect(page.locator('.stopka__poradnik a')).toHaveCount(6);
    await expect(page.locator('#cookies')).toHaveCount(1);

    // przycisk w bloku rezerwacji: ciemny tekst na jasnym tle
    await expect(page.locator('.art__cta .btn')).toHaveCSS('color', 'rgb(5, 5, 5)');
    await expect(page.locator('.art__cta .btn')).toHaveCSS('background-color', 'rgb(240, 240, 240)');

    // zdjęcia mają opisy i się wczytują
    await page.evaluate(async () => { for (const i of document.images) { i.loading = 'eager'; } await Promise.all([...document.images].map((i) => i.decode().catch(() => {}))); });
    const obrazy = await page.evaluate(() => [...document.images].map((i) => ({ src: i.getAttribute('src'), alt: i.getAttribute('alt'), ok: i.naturalWidth > 0 })));
    for (const o of obrazy) { expect(o.alt, o.src).toBeTruthy(); expect(o.ok, o.src).toBe(true); }

    // słownictwo: branding zamiast stroju, bez „darmowy/bezpłatny”
    const tekst = await page.locator('body').innerText();
    expect(tekst).not.toMatch(/\bstr[óo]j(u|em|e)?\b|kostium|garderob|darmow|bezpłatn/i);
    expect(bledy).toEqual([]);
  });
}

test('artykuły @375: bez poziomego przewijania, menu i FAQ działają', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 });
  await fontyZRepo(page);
  for (const plik of ARTYKULY) {
    await page.goto(BAZA + plik);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), plik).toBe(true);
  }
  const p = page.locator('#navPrzycisk');
  await p.click();
  await expect(page.locator('#navPanel')).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(page.locator('#navPanel')).toBeHidden();
  const q = page.locator('.faq__q').first();
  await q.click();
  await expect(q).toHaveAttribute('aria-expanded', 'true');
  await expect(page.locator('#faq-1')).toBeVisible();
});

for (const vp of [{ width: 1440, height: 900 }, { width: 375, height: 812 }]) {
  test(`artykuły: axe color-contrast @${vp.width}`, async ({ page }) => {
    await page.setViewportSize(vp);
    await fontyZRepo(page);
    for (const plik of ['blog-atrakcje-eventowe.html', 'blog-ile-kosztuje-wynajem-robota.html']) {
      await page.goto(BAZA + plik);
      await page.evaluate(() => document.fonts.ready);
      const wynik = await new AxeBuilder({ page }).withRules(['color-contrast']).analyze();
      const naruszenia = wynik.violations.flatMap((v) => v.nodes.map((n) => n.target.join(' ')));
      expect(naruszenia, plik).toEqual([]);
    }
  });
}
