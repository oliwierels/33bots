// Formularz: walidacja, przejście krok 1 → 2 i treść wysyłanego zgłoszenia.
// Request do Formspree jest przechwytywany i NIE wychodzi na produkcję.
import { chromium } from '@playwright/test';
const b = await chromium.launch();
async function sprawdz(adres, wypelnij) {
  const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
  const bledy = []; p.on('pageerror', (e) => bledy.push(e.message));
  let wyslane = null;
  await p.route('https://formspree.io/**', async (r) => { wyslane = r.request().postDataJSON(); await r.fulfill({ status: 200, contentType: 'application/json', body: '{"ok":true}' }); });
  await p.goto('http://127.0.0.1:8080' + adres);
  const wynik = await wypelnij(p);
  await p.waitForTimeout(800);
  console.log(`${adres}: ${wynik}; wysłano: ${wyslane ? JSON.stringify(wyslane) : 'NIE'}; błędy JS: ${bledy.length}`);
  await p.close();
}
await sprawdz('/', async (p) => {
  await p.locator('#contactForm').scrollIntoViewIfNeeded();
  await p.locator('#formStep1 button[type=button]').first().click();
  const zatrzymany = await p.locator('#formStep2').isHidden();
  await p.fill('input[name=name]', 'Jan Testowy');
  await p.fill('input[name=email]', 'jan@test.pl');
  await p.fill('input[name=company]', 'Firma Test');
  await p.locator('#formStep1 button[type=button]').first().click();
  await p.fill('input[name=location]', 'Warszawa');
  await p.fill('textarea[name=message]', 'Gala firmowa, 300 osób.');
  await p.locator('#formStep2 button[type=submit]').click();
  return `walidacja zatrzymała pusty krok 1: ${zatrzymany ? 'tak' : 'NIE'}`;
});
await sprawdz('/case-study-lexai.html', async (p) => {
  await p.fill('#contactForm input[name=name]', 'Jan Testowy');
  await p.fill('#contactForm input[name=email]', 'jan@test.pl');
  await p.locator('#btnNext').click();
  await p.fill('#contactForm textarea', 'Konferencja, 500 osób.');
  await p.locator('#contactForm [type=submit]').click();
  return 'stara podstrona (main.js)';
});
await b.close();
