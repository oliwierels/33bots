// Zrzut ekranu przy pierwszej wizycie — z banerem cookies, bez przewijania.
import { chromium } from '@playwright/test';
const katalog = process.argv[2];
const b = await chromium.launch();
for (const [w, h] of [[1440, 900], [375, 812]]) {
  const p = await b.newPage({ viewport: { width: w, height: h } });
  await p.goto('http://127.0.0.1:8080/');
  await p.waitForSelector('#cookies.show', { timeout: 8000 });
  const kolizja = await p.evaluate(() => {
    const a = document.querySelector('#cookies').getBoundingClientRect();
    const b = document.querySelector('.hero .btn').getBoundingClientRect();
    return !(a.right <= b.left || a.left >= b.right || a.bottom <= b.top || a.top >= b.bottom);
  });
  console.log(`@${w}: baner zasłania przycisk hero: ${kolizja ? 'TAK' : 'nie'}`);
  await p.screenshot({ path: `${katalog}/pierwsza-wizyta-${w}.png` });
  await p.close();
}
await b.close();
