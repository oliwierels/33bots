// Baner cookie ustępuje ConsentBoard (baner zgód ładowany przez GTM). Cztery warianty kodu:
// strona główna, artykuły ze strona.js, stare podstrony z main.js i strony prawne z kodem w pliku.
// Bez ConsentBoard baner działa jak dawniej; z ConsentBoard znika i nie wraca, dopóki ten się ładuje.
import { test, expect } from '@playwright/test';

const STRONY = [
  ['/', '#cookies', 'show'],
  ['/blog-atrakcje-eventowe.html', '#cookies', 'show'],
  ['/robot-na-targi.html', '#cookieBanner', 'visible'],
  ['/polityka-prywatnosci.html', '#cookies', 'show'],
];
const SKRYPT_CMP = 'https://consentboard.com/cmp.js?id=test';

for (const [sciezka, baner, klasa] of STRONY) {
  test(`baner cookie ustępuje ConsentBoard: ${sciezka}`, async ({ page }) => {
    // Pomiar i prawdziwy kontener GTM wyłączone — test sam udaje ConsentBoard.
    await page.route(/googletagmanager\.com|albacross\.com|google-analytics\.com|googleadservices\.com|doubleclick\.net/, (r) => r.abort());
    await page.route('https://consentboard.com/**', (r) => r.fulfill({ status: 200, contentType: 'application/javascript', body: '' }));
    await page.clock.install();
    await page.goto('http://localhost:8080' + sciezka);
    await page.clock.runFor(1500);
    // bez ConsentBoard: baner pokazuje się jak dawniej
    await expect(page.locator(baner)).toHaveClass(new RegExp(`\\b${klasa}\\b`));
    // GTM dodaje skrypt ConsentBoard → nasz baner znika od razu
    await page.evaluate((src) => { const s = document.createElement('script'); s.src = src; document.head.appendChild(s); }, SKRYPT_CMP);
    await expect(page.locator(baner)).toHaveCount(0);
    expect(await page.evaluate(() => localStorage.getItem('33bots-cmp'))).toBe('1');
    expect(await page.evaluate(() => localStorage.getItem('33bots-cookies'))).toBeNull();
    // kolejne wejście: baner nie pokazuje się wcale, dopóki ConsentBoard się ładuje
    await page.reload();
    await page.clock.runFor(1500);
    await expect(page.locator(baner)).toHaveCount(1);
    await expect(page.locator(baner)).not.toHaveClass(new RegExp(`\\b${klasa}\\b`));
    // ConsentBoard zniknął ze strony (np. wyłączony w GTM): po 8 s wraca nasz baner
    await page.clock.runFor(7000);
    await expect(page.locator(baner)).toHaveClass(new RegExp(`\\b${klasa}\\b`));
    expect(await page.evaluate(() => localStorage.getItem('33bots-cmp'))).toBeNull();
    // „Rozumiem” działa jak dawniej
    await page.locator(`${baner} button`).click();
    await expect(page.locator(baner)).not.toHaveClass(new RegExp(`\\b${klasa}\\b`));
    expect(await page.evaluate(() => localStorage.getItem('33bots-cookies'))).toBe('1');
  });
}

test('skrypt ConsentBoard obecny już przy wejściu: baner nie pojawia się wcale', async ({ page }) => {
  await page.route(/googletagmanager\.com|albacross\.com/, (r) => r.abort());
  await page.route('https://consentboard.com/**', (r) => r.fulfill({ status: 200, contentType: 'application/javascript', body: '' }));
  // skrypt ConsentBoard ląduje w <head>, zanim uruchomi się kod strony (jak przy GTM z pamięci podręcznej)
  await page.addInitScript((src) => {
    const dodaj = () => { const s = document.createElement('script'); s.src = src; document.head.appendChild(s); };
    if (document.head) dodaj();
    else new MutationObserver((_, o) => { if (document.head) { o.disconnect(); dodaj(); } }).observe(document, { childList: true, subtree: true });
  }, SKRYPT_CMP);
  await page.clock.install();
  await page.goto('http://localhost:8080/');
  await page.clock.runFor(2000);
  await expect(page.locator('#cookies')).toHaveCount(0);
  expect(await page.evaluate(() => localStorage.getItem('33bots-cmp'))).toBe('1');
});
