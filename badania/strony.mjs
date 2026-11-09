// Badanie stron konkurencji z sieci GitHuba (sesja Claude nie ma do nich dostępu):
// zrzuty ekranu w kolejnych punktach przewijania, wideo przewijania, struktura, biblioteki animacji.
// Użycie: node badania/strony.mjs <adres> <katalog-wyników>
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

const [adres, katalog] = process.argv.slice(2);
fs.mkdirSync(katalog, { recursive: true });
const przegladarka = await chromium.launch();

async function badaj(nazwa, viewport, wideo) {
  const opcje = { viewport, deviceScaleFactor: 1, locale: 'pl-PL' };
  if (nazwa === 'telefon') Object.assign(opcje, { isMobile: true, hasTouch: true, userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1' });
  if (wideo) opcje.recordVideo = { dir: path.join(katalog, 'wideo-' + nazwa), size: { width: 1280, height: 800 } };
  const ctx = await przegladarka.newContext(opcje);
  const page = await ctx.newPage();
  const zasoby = [];
  page.on('response', (r) => { try { zasoby.push({ url: r.url().slice(0, 200), typ: r.request().resourceType(), status: r.status() }); } catch {} });
  await page.goto(adres, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(4000);
  // zgody cookie: klik w przycisk akceptacji, jeśli jest (żeby baner nie zasłaniał zrzutów)
  for (const t of ['Akceptuj', 'Zaakceptuj', 'Accept', 'Zgadzam', 'Akceptuję', 'OK', 'Rozumiem']) {
    const b = page.getByRole('button', { name: new RegExp(t, 'i') }).first();
    if (await b.isVisible().catch(() => false)) { await b.click().catch(() => {}); break; }
  }
  const wysokosc = await page.evaluate(() => document.documentElement.scrollHeight);
  const krok = Math.round(viewport.height * 0.8);
  let i = 0;
  for (let y = 0; y < wysokosc && i < 40; y += krok, i++) {
    await page.evaluate((y) => window.scrollTo({ top: y, behavior: 'instant' }), y);
    await page.waitForTimeout(wideo ? 1400 : 900);
    await page.screenshot({ path: path.join(katalog, `${nazwa}-${String(i).padStart(2, '0')}.jpg`), type: 'jpeg', quality: 55 });
  }
  const info = await page.evaluate(() => {
    const tekst = (e) => (e.innerText || e.textContent || '').replace(/\s+/g, ' ').trim();
    const g = window;
    return {
      tytul: document.title,
      opis: document.querySelector('meta[name="description"]')?.content || '',
      naglowki: [...document.querySelectorAll('h1,h2,h3')].map((h) => h.tagName + ': ' + tekst(h)).slice(0, 120),
      nawigacja: [...document.querySelectorAll('nav a, header a')].map((a) => tekst(a) + ' → ' + a.getAttribute('href')).slice(0, 60),
      przyciski: [...document.querySelectorAll('a.btn, a[class*="button"], button, a[class*="btn"], a[class*="cta"]')].map(tekst).filter(Boolean).slice(0, 80),
      skrypty: [...document.scripts].map((s) => s.src).filter(Boolean),
      style: [...document.querySelectorAll('link[rel="stylesheet"]')].map((l) => l.href),
      biblioteki: Object.fromEntries(['gsap', 'ScrollTrigger', 'THREE', 'lottie', 'bodymovin', 'Lenis', 'lenis', 'Swiper', 'Webflow', 'Framer', 'barba', 'LocomotiveScroll', 'AOS', 'anime', 'Splitting', 'SplitType', 'Spline', 'jQuery', 'elementorFrontend', 'wp'].map((k) => [k, typeof g[k] !== 'undefined'])),
      generator: document.querySelector('meta[name="generator"]')?.content || '',
      liczniki: { img: document.images.length, video: document.querySelectorAll('video').length, canvas: document.querySelectorAll('canvas').length, svg: document.querySelectorAll('svg').length, iframe: document.querySelectorAll('iframe').length, formularze: document.forms.length, sekcje: document.querySelectorAll('section').length },
      animacjeCSS: document.getAnimations ? document.getAnimations().length : -1,
      fonty: [...new Set([...document.fonts].map((f) => f.family))].slice(0, 12),
      tekstStrony: tekst(document.body).slice(0, 30000),
      wysokosc: document.documentElement.scrollHeight,
    };
  });
  info.zasobyPodsumowanie = zasoby.reduce((a, z) => { a[z.typ] = (a[z.typ] || 0) + 1; return a; }, {});
  info.zasobyObce = [...new Set(zasoby.map((z) => { try { return new URL(z.url).host; } catch { return ''; } }))];
  fs.writeFileSync(path.join(katalog, `${nazwa}.json`), JSON.stringify(info, null, 1));
  await page.screenshot({ path: path.join(katalog, `${nazwa}-calosc.jpg`), type: 'jpeg', quality: 45, fullPage: true }).catch((e) => console.log('pełny zrzut:', e.message));
  if (wideo) {
    // płynne przewinięcie od góry do dołu do wideo
    await page.evaluate(() => window.scrollTo({ top: 0, behavior: 'instant' }));
    await page.waitForTimeout(1500);
    for (let y = 0; y < wysokosc; y += 120) { await page.mouse.wheel(0, 120); await page.waitForTimeout(110); }
    await page.waitForTimeout(1500);
  }
  await ctx.close();
  console.log(`${nazwa}: ${i} zrzutów, wysokość ${wysokosc}px, biblioteki: ${Object.entries(info.biblioteki).filter(([, v]) => v).map(([k]) => k).join(', ') || 'brak'}`);
}

await badaj('komputer', { width: 1440, height: 900 }, true);
await badaj('telefon', { width: 390, height: 844 }, false);
await przegladarka.close();
