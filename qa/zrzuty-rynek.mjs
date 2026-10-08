// Pełne zrzuty 375 i 1440 px strony z dowolnego serwera (rynki zagraniczne).
//   node qa/zrzuty-rynek.mjs <katalog na zrzuty> <adres bazowy> <prefiks> /strona.html [...]
import { chromium } from '@playwright/test';
import { przewinCala } from './odstepy.mjs';
const [katalog, baza, prefiks, ...strony] = process.argv.slice(2);
const b = await chromium.launch();
for (const adres of strony) {
  for (const [w, h] of [[375, 812], [1440, 900]]) {
    const p = await b.newPage({ viewport: { width: w, height: h }, reducedMotion: 'reduce' });
    const bledy = [];
    p.on('pageerror', (e) => bledy.push(e.message));
    p.on('console', (m) => { if (m.type() === 'error') bledy.push(m.text()); });
    await p.goto(baza + adres);
    await p.evaluate(() => document.fonts.ready);
    await przewinCala(p);
    const nazwa = `${prefiks}-` + (adres === '/' ? 'index' : adres.replace(/^\/|\.html$/g, '')) + `-${w}.png`;
    await p.screenshot({ path: `${katalog}/${nazwa}`, fullPage: true });
    console.log(nazwa, await p.evaluate(() => document.body.scrollHeight), bledy.length ? bledy : '');
    await p.close();
  }
}
await b.close();
