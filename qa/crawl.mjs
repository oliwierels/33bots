// Lokalny crawl: wszystkie strony .html — błędy JS, brakujące pliki i martwe linki wewnętrzne.
import { chromium } from '@playwright/test';
import { readdirSync, existsSync } from 'node:fs';
const strony = readdirSync('..').filter((f) => f.endsWith('.html'));
const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } });
const bledyJs = [], braki = new Set(), martwe = new Set();
for (const s of strony) {
  const p = await ctx.newPage();
  p.on('pageerror', (e) => bledyJs.push(`${s}: ${e.message}`));
  p.on('response', (r) => { const u = r.url(); if (u.startsWith('http://127.0.0.1:8080') && r.status() >= 400) braki.add(`${s} → ${u.replace('http://127.0.0.1:8080/', '')} ${r.status()}`); });
  await p.goto('http://127.0.0.1:8080/' + s, { waitUntil: 'load' });
  const linki = await p.evaluate(() => [...document.querySelectorAll('a[href]')].map((a) => a.getAttribute('href')));
  for (const h of linki) {
    if (/^(https?:|mailto:|tel:|#|javascript:)/.test(h)) continue;
    const plik = h.split('#')[0].split('?')[0].replace(/^\//, '') || 'index.html';
    if (!existsSync('../' + plik)) martwe.add(`${s} → ${h}`);
  }
  await p.close();
}
await b.close();
console.log(`stron: ${strony.length}`);
console.log(`błędy JS: ${bledyJs.length}`); bledyJs.slice(0, 10).forEach((x) => console.log('  ' + x));
console.log(`brakujące zasoby: ${braki.size}`); [...braki].slice(0, 10).forEach((x) => console.log('  ' + x));
console.log(`martwe linki wewnętrzne: ${martwe.size}`); [...martwe].slice(0, 10).forEach((x) => console.log('  ' + x));
