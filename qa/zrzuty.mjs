// Pełne zrzuty 375 i 1440 px podanych podstron — do przeglądu przed raportem.
//   node qa/zrzuty.mjs <katalog> /strona.html [...]
import { chromium } from '@playwright/test';
import { przewinCala } from './odstepy.mjs';
const [katalog, ...strony] = process.argv.slice(2);
const b = await chromium.launch();
for (const adres of strony) {
  for (const [w, h] of [[375, 812], [1440, 900]]) {
    const p = await b.newPage({ viewport: { width: w, height: h }, reducedMotion: 'reduce' });
    await p.goto('http://127.0.0.1:8080' + adres);
    await p.evaluate(() => document.fonts.ready);
    await przewinCala(p);
    const nazwa = (adres === '/' ? 'index' : adres.replace(/^\/|\.html$/g, '')) + `-${w}.png`;
    await p.screenshot({ path: `${katalog}/${nazwa}`, fullPage: true });
    console.log(nazwa, await p.evaluate(() => document.body.scrollHeight));
    await p.close();
  }
}
await b.close();
