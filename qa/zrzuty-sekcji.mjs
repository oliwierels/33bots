// Zrzuty pojedynczych sekcji strony (do przeglądu szczegółów).
//   node qa/zrzuty-sekcji.mjs <katalog> <adres strony> <prefiks> <szerokość> <selektor> [...]
import { chromium } from '@playwright/test';
import { przewinCala } from './odstepy.mjs';
const [katalog, adres, prefiks, szer, ...selektory] = process.argv.slice(2);
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: Number(szer), height: 900 }, reducedMotion: 'reduce' });
await p.goto(adres);
await p.evaluate(() => document.fonts.ready);
await przewinCala(p);
for (const [i, sel] of selektory.entries()) {
  const el = p.locator(sel).first();
  await el.scrollIntoViewIfNeeded();
  await p.waitForTimeout(150);
  const plik = `${katalog}/${prefiks}-${szer}-${String(i + 1).padStart(2, '0')}.png`;
  await el.screenshot({ path: plik });
  console.log(plik, sel);
}
await b.close();
