import { test, expect } from '@playwright/test';

for (const vp of [{ width: 1440, height: 900 }, { width: 375, height: 812 }]) {
  test(`hero ${vp.width}`, async ({ page }) => {
    await page.setViewportSize(vp);
    await page.goto('http://localhost:8080/'); // dopasuj adres lokalnego serwera
    await page.evaluate(async () => { await document.fonts.ready; return true; });

    // 1. fonty naprawdę załadowane
    expect(await page.evaluate(() => document.fonts.check('300 64px "Space Grotesk"'))).toBe(true);
    expect(await page.evaluate(() => document.fonts.check('400 17px "Plus Jakarta Sans"'))).toBe(true);

    // 2. przycisk w kolorze sygnału (cyjan), ciemny tekst, bez zaokrągleń — jedyny kolor na pierwszym ekranie
    const btn = page.locator('.hero .btn');
    await expect(btn).toHaveClass(/btn--akcja/);
    await expect(btn).toHaveCSS('background-color', 'rgb(111, 214, 255)');
    await expect(btn).toHaveCSS('color', 'rgb(5, 5, 5)');
    await expect(btn).toHaveCSS('border-radius', '0px');

    // 3. właściwe zdjęcie, brak renderu i chipów
    await expect(page.locator('.hero img')).toHaveAttribute('src', /realizacja-gala-wsrod-gosci/);
    expect(await page.locator('img[src*="robot-g1"]').count()).toBe(0);
    const bodyText = await page.locator('body').innerText();
    expect(bodyText).not.toMatch(/\bDOF\b|M\/S|132\s?CM|✓|darmow|Najlepsze ceny|10×/i);

    // 4. hero i pasek dowodu: ostre narożniki, bez cieni tekstu i filtrów; kolor daje gradient
    //    najważniejszego zdania, poświata zdjęcia i mgła w tle (body::before z magentą)
    const offenders = await page.evaluate(() => {
      const bad = [];
      for (const el of document.querySelectorAll('.hero, .hero *, .proof, .proof *')) {
        for (const pseudo of [null, '::before', '::after']) {
          const s = getComputedStyle(el, pseudo);
          if (pseudo && s.content !== 'none' && s.content !== 'normal') bad.push([el.className, pseudo, 'content']);
          if (s.textShadow !== 'none') bad.push([el.className, pseudo, 'text-shadow']);
          if (s.filter !== 'none') bad.push([el.className, pseudo, 'filter']);
          if (parseFloat(s.borderTopLeftRadius) > 0) bad.push([el.className, pseudo, 'radius']);
        }
      }
      return bad;
    });
    expect(offenders).toEqual([]);
    expect(await page.evaluate(() => getComputedStyle(document.querySelector('.hero .display')).backgroundClip)).toBe('text');
    expect(await page.evaluate(() => getComputedStyle(document.body, '::before').backgroundImage)).toContain('255, 61, 205');

    // 5. brak poziomego przewijania
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);

    // 6. nagłówek się mieści (żadne słowo nie wychodzi poza kolumnę)
    expect(await page.evaluate(() => {
      const d = document.querySelector('.display');
      return d.scrollWidth <= d.clientWidth;
    })).toBe(true);

    await page.screenshot({ path: `qa/hero-${vp.width}.png`, fullPage: false });
  });
}
