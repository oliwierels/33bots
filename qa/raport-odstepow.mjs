// Zestawienie naruszeń odstępów pogrupowane po elemencie — pomocnicze przy poprawkach.
//   node qa/raport-odstepow.mjs /strona.html [/inna.html ...]
import { chromium } from '@playwright/test';
import { naruszeniaOdstepow, przewinCala } from './odstepy.mjs';

const strony = process.argv.slice(2);
const b = await chromium.launch();
for (const adres of strony) {
  for (const [w, h, min] of [[375, 812, 24], [1440, 900, 32]]) {
    const p = await b.newPage({ viewport: { width: w, height: h }, reducedMotion: 'reduce' });
    await p.goto('http://127.0.0.1:8080' + adres);
    await p.evaluate(() => document.fonts.ready);
    await przewinCala(p);
    const n = await naruszeniaOdstepow(p, min);
    const grupy = {};
    for (const x of n) (grupy[x.element] ??= []).push(`${x.strona}:${x.odstep} «${x.tekst}»`);
    console.log(`\n═══ ${adres} @${w} — ${n.length} naruszeń, ${Object.keys(grupy).length} elementów`);
    for (const [el, s] of Object.entries(grupy)) console.log(`  ${el.slice(0, 70).padEnd(70)} ${[...new Set(s)].slice(0, 3).join('  ')}`);
    await p.close();
  }
}
await b.close();
