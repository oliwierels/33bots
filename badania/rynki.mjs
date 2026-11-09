// Strona główna na żywo: .pl, .de, .lt — robot gotowy, polecenie z dymkiem, kalkulator, telefon, bez błędów.
import { chromium } from 'playwright';
import fs from 'node:fs';
const RYNKI = [
  ['pl', 'https://33bots.pl/', 'Cześć! Miło Cię widzieć.'],
  ['de', 'https://33bots.de/', 'Hallo! Schön, Sie zu sehen.'],
  ['lt', 'https://33bots.lt/', 'Labas! Malonu jus matyti.'],
];
const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
const wynik = {};
for (const [kod, adres, machanie] of RYNKI) {
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  const bledy = []; p.on('pageerror', (e) => bledy.push(e.message));
  p.on('console', (m) => { if (m.type() === 'error') bledy.push('console: ' + m.text()); });
  const odp = await p.goto(adres + '?k=' + Date.now(), { waitUntil: 'load' });
  await p.evaluate(() => { document.getElementById('cookies')?.remove(); const r = document.getElementById('robot'); scrollTo({ top: scrollY + r.getBoundingClientRect().top + 10, behavior: 'instant' }); });
  let robot = 'brak sekcji';
  try { await p.waitForFunction(() => /gotowy|brak/.test(document.documentElement.dataset.robot || ''), null, { timeout: 40000 }); robot = await p.evaluate(() => document.documentElement.dataset.robot); } catch (e) { robot = 'timeout'; }
  let dymek = null;
  if (robot === 'gotowy') {
    await p.waitForTimeout(2500);
    await p.locator('[data-robot-gest="macha"]').click();
    await p.waitForTimeout(600);
    dymek = await p.locator('#robotDymek').textContent();
    await p.screenshot({ path: `badania/wyniki/zywo/robot-${kod}.png` });
  }
  const kalk = p.locator('#kalkulator');
  await kalk.scrollIntoViewIfNeeded();
  await kalk.locator('input[value="dni"]').check({ force: true });
  await kalk.locator('[data-dni="1"]').click();
  await p.waitForTimeout(900);
  const dane = await p.evaluate(() => ({
    sekcje: [...document.querySelectorAll('main > section')].map((s) => s.id || s.className),
    numery: [...document.querySelectorAll('.sec .sec__meta')].map((e) => e.textContent.trim().slice(0, 7)),
    kalk: [kalkEtykieta.textContent, kalkOd.textContent, kalkKwota.textContent + kalkZl.textContent, kalkOpis.textContent].join(' | '),
    tel: document.querySelector('a[href^="tel:"]')?.getAttribute('href'),
    obietnica: document.querySelector('.termin__obietnica')?.textContent.trim(),
    skrypty: [...document.scripts].map((s) => s.src).filter((s) => /glowna|robot3d/.test(s)),
    wiedza: [...document.querySelectorAll('[data-animacja="wiedza"] text')].map((t) => t.textContent),
  }));
  wynik[kod] = { http: odp.status(), robot, dymek, dymekOk: dymek === machanie, ...dane, bledy };
  await p.close();
  // telefon (iPhone 13): robot w sekcji „z bliska” — bez prześwietlenia
  const { devices } = await import('playwright');
  const t = await b.newContext({ ...devices['iPhone 13'] });
  const pt = await t.newPage();
  await pt.goto(adres + '?t=' + Date.now(), { waitUntil: 'load' });
  await pt.evaluate(() => { document.getElementById('cookies')?.remove(); const r = document.getElementById('robot'); scrollTo(0, r.getBoundingClientRect().top + scrollY + 10); });
  await pt.waitForTimeout(7000);
  await pt.screenshot({ path: `badania/wyniki/zywo/telefon-${kod}.png` });
  await t.close();
}
fs.writeFileSync('badania/wyniki/zywo/rynki.json', JSON.stringify(wynik, null, 1));
console.log(JSON.stringify(wynik, null, 1));
await b.close();
