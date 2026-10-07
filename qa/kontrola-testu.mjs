// Kontrola samego testu: wstrzykuje starą regułę „FAQ jako karty” (ramka, tło,
// a boczny odstęp zerowany przez blok <style> case study) i sprawdza, że test ją łapie.
import { chromium } from '@playwright/test';
import { naruszeniaOdstepow, przewinCala } from './odstepy.mjs';
const b = await chromium.launch();
for (const [w, min] of [[375, 24], [1440, 32]]) {
  const p = await b.newPage({ viewport: { width: w, height: 900 }, reducedMotion: 'reduce' });
  await p.goto('http://127.0.0.1:8080/case-study-eco-studio-electro-system.html');
  await przewinCala(p);
  const czysto = (await naruszeniaOdstepow(p, min)).length;
  await p.addStyleTag({ content: '.faq-item{border:1px solid #1f1f1f;border-radius:16px;background:rgba(17,17,19,.45);padding-inline:0}' });
  const zBledem = await naruszeniaOdstepow(p, min);
  console.log(`@${w}: bez błędu ${czysto} naruszeń; ze starą regułą ${zBledem.length} —`,
    zBledem.slice(0, 2).map((x) => `${x.element} ${x.strona}:${x.odstep}px «${x.tekst}»`).join(' | '));
  await p.close();
}
await b.close();
