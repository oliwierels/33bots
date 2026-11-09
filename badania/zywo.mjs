// Kontrola na żywo strony głównej 33bots.pl: robot 3D, błędy, zrzuty. node badania/zywo.mjs <katalog>
import { chromium, devices } from 'playwright';
import fs from 'node:fs';
const kat = process.argv[2]; fs.mkdirSync(kat, { recursive: true });
const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
const raport = {};
for (const [nazwa, opcje] of [['komputer', { viewport: { width: 1440, height: 900 } }], ['telefon', devices['iPhone 13']]]) {
  const ctx = await b.newContext({ ...opcje, locale: 'pl-PL' });
  const p = await ctx.newPage();
  const bledy = [];
  p.on('pageerror', (e) => bledy.push('pageerror: ' + e.message));
  p.on('console', (m) => { if (m.type() === 'error') bledy.push('console: ' + m.text().slice(0, 200)); });
  const zasoby = [];
  p.on('response', (r) => { if (/robot|glowna/.test(r.url())) zasoby.push([r.status(), r.url().split('33bots.pl')[1]]); });
  await p.goto('https://33bots.pl/?kontrola=' + Date.now(), { waitUntil: 'load', timeout: 60000 });
  await p.waitForFunction(() => document.documentElement.dataset.robot, null, { timeout: 30000 }).catch(() => {});
  await p.waitForTimeout(4500);
  const stan = await p.evaluate(() => ({ robot: document.documentElement.dataset.robot || 'brak sygnału', klasy: document.documentElement.className,
    h1: document.querySelector('h1')?.textContent, cyfry: document.querySelector('.skala__cyfry')?.textContent, canvas: !!document.querySelector('canvas.robot3d'),
    cena: document.getElementById('kalkKwota')?.textContent, obietnica: document.querySelector('.termin__obietnica')?.textContent, zasady: !!document.getElementById('zasady') }));
  await p.screenshot({ path: `${kat}/${nazwa}-hero.png` });
  const tanczy = p.locator('[data-robot-gest="tanczy"]');
  if (await tanczy.isVisible().catch(() => false)) { await tanczy.click(); await p.waitForTimeout(1800); await p.screenshot({ path: `${kat}/${nazwa}-tanczy.png` }); await p.waitForTimeout(3500); }
  for (const [plik, sel] of [['skala', '.skala__liczba'], ['zasady', '#zasady'], ['kontakt-z-goscmi', '.zasady + .zasady__grupa'], ['wystep', '.wiersz[data-poza="mowi"]'], ['formaty', '#formaty']]) {
    await p.evaluate((s) => { const e = document.querySelector(s); scrollTo({ top: scrollY + e.getBoundingClientRect().top - innerHeight * 0.35, behavior: 'instant' }); }, sel);
    await p.waitForTimeout(1800);
    await p.screenshot({ path: `${kat}/${nazwa}-${plik}.png` });
  }
  raport[nazwa] = { ...stan, bledy, zasoby: zasoby.filter(([, u]) => /robot|glowna/.test(u.split('?')[0])) };
  await ctx.close();
}
fs.writeFileSync(`${kat}/raport.json`, JSON.stringify(raport, null, 1));
console.log(JSON.stringify(raport, null, 1));
await b.close();
