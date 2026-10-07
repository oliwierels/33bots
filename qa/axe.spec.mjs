// Kontrast tekstu na stronie głównej: zero naruszeń reguły color-contrast.
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { przewinCala } from './odstepy.mjs';

for (const vp of [{ width: 1440, height: 900 }, { width: 375, height: 812 }]) {
  test(`axe color-contrast ${vp.width}`, async ({ page }) => {
    await page.setViewportSize(vp);
    await page.goto('http://localhost:8080/');
    await page.evaluate(() => document.fonts.ready);
    await przewinCala(page);
    const wynik = await new AxeBuilder({ page }).withRules(['color-contrast']).analyze();
    const naruszenia = wynik.violations.flatMap((v) => v.nodes.map((n) => ({
      cel: n.target.join(' '), opis: n.failureSummary?.split('\n').slice(1, 2).join(' ').trim(),
    })));
    expect(naruszenia, JSON.stringify(naruszenia, null, 1)).toEqual([]);
  });
}
