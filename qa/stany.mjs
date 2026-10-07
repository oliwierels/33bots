// Zrzuty stanów interaktywnych: szuflada realizacji i krok 2 formularza.
import { chromium } from '@playwright/test';
const katalog = process.argv[2];
const b = await chromium.launch();
for (const [w, h] of [[1440, 900], [375, 812]]) {
  const ctx = await b.newContext({ viewport: { width: w, height: h }, reducedMotion: 'reduce' });
  await ctx.addInitScript(() => localStorage.setItem('33bots-cookies', '1'));
  const p = await ctx.newPage();
  await p.goto('http://127.0.0.1:8080/');
  await p.evaluate(() => document.fonts.ready);
  await p.locator('.realizacja[data-cs="yeah-gym"]').scrollIntoViewIfNeeded();
  await p.locator('.realizacja[data-cs="yeah-gym"]').click();
  await p.waitForTimeout(300);
  await p.screenshot({ path: `${katalog}/szuflada-${w}.png` });
  await p.keyboard.press('Escape');
  await p.locator('#formularz').scrollIntoViewIfNeeded();
  await p.locator('label.chip:has-text("Gala")').click();
  await p.locator('#dalej').click();
  await p.locator('#wyslij').click();
  await p.locator('#formularz').scrollIntoViewIfNeeded();
  await p.screenshot({ path: `${katalog}/formularz-krok2-${w}.png` });
  await ctx.close();
}
await b.close();
