// Tekst nie dotyka ramek ani krawędzi tła — na każdej zmienionej podstronie.
// Przy każdej kolejnej zmianie dopisz tu podstronę, którą ruszasz.
import { test, expect } from '@playwright/test';
import { naruszeniaOdstepow, przewinCala, fontyZRepo } from './odstepy.mjs';

const STRONY = [
  '/',
  '/case-study-eco-studio-electro-system.html',
  '/case-study-lexai.html',
  '/oferta-konferencje.html',
  '/oferta-targi.html',
  '/sklep.html',
  '/wdrozenia.html',
];
const EKRANY = [
  { width: 375, height: 812, minimum: 24 },
  { width: 1440, height: 900, minimum: 32 },
];

test.use({ reducedMotion: 'reduce' });

for (const adres of STRONY) {
  for (const ekran of EKRANY) {
    test(`odstępy ${adres} @${ekran.width}`, async ({ page }) => {
      await page.setViewportSize({ width: ekran.width, height: ekran.height });
      await fontyZRepo(page);
      await page.goto('http://localhost:8080' + adres);
      await page.evaluate(() => document.fonts.ready);
      await przewinCala(page);
      const naruszenia = await naruszeniaOdstepow(page, ekran.minimum);
      expect(naruszenia, JSON.stringify(naruszenia, null, 1)).toEqual([]);
    });
  }
}
