// Strona główna po etapie 3: struktura, system wizualny i zachowanie.
// Formularz testowany na przechwyconym requeście — nic nie trafia do Formspree.
import { test, expect } from '@playwright/test';

const ADRES = 'http://localhost:8080/';
const SEKCJE = ['realizacje', 'wystep', 'case-study', 'formaty', 'proces', 'faq', 'kontakt'];
const CYJAN = 'rgb(111, 214, 255)';

async function otworz(page, vp, opcje = {}) {
  await page.setViewportSize(vp);
  await page.goto(ADRES);
  await page.evaluate(() => document.fonts.ready);
  if (opcje.przewin) {
    await page.evaluate(async () => {
      for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo({ top: y, behavior: 'instant' }); await new Promise((r) => setTimeout(r, 40)); }
      scrollTo({ top: 0, behavior: 'instant' });
    });
  }
}

for (const vp of [{ width: 1440, height: 900 }, { width: 768, height: 1024 }, { width: 375, height: 812 }]) {
  test.describe(`strona główna @${vp.width}`, () => {
    test.use({ contextOptions: { reducedMotion: 'reduce' } });

    test('kolejność sekcji, numeracja i aliasy kotwic', async ({ page }) => {
      await otworz(page, vp);
      const kolejnosc = await page.evaluate(() => [...document.querySelectorAll('main > section')].map((s) => s.id || s.className));
      expect(kolejnosc).toEqual(['hero', 'proof', ...['realizacje', 'wystep', 'case-study', 'formaty', 'proces', 'faq', 'kontakt']]);
      const numery = await page.evaluate(() => [...document.querySelectorAll('.sec .sec__meta')].map((m) => m.textContent.trim().slice(0, 7)));
      expect(numery).toEqual(['04 / 11', '05 / 11', '06 / 11', '07 / 11', '08 / 11', '09 / 11', '10 / 11']);
      expect(await page.evaluate(() => document.querySelector('footer.stopka').parentElement.tagName)).toBe('BODY');
      for (const id of ['eventy', 'uslugi', 'cennik', 'mozliwosci', 'klienci', 'kontakt', 'top']) {
        expect(await page.locator(`#${id}`).count(), `#${id}`).toBe(1);
      }
      expect(await page.locator('h1').innerText()).toMatch(/wynajem robota humanoidalnego/i);
    });

    test('zero efektów: cienie, gradienty, filtry, animacje, zaokrąglenia', async ({ page }) => {
      await otworz(page, vp, { przewin: true });
      const zle = await page.evaluate(() => {
        const bad = [];
        for (const el of document.querySelectorAll('.nav, .nav *, .sec, .sec *, .stopka, .stopka *, .pasek, .pasek *, .cookies, .cookies *')) {
          for (const pseudo of [null, '::before', '::after']) {
            const s = getComputedStyle(el, pseudo);
            const nazwa = `${el.tagName.toLowerCase()}.${(el.getAttribute('class') || '').split(' ')[0]}${pseudo || ''}`;
            if (pseudo && s.content !== 'none' && s.content !== 'normal') bad.push([nazwa, 'content']);
            if (s.boxShadow !== 'none') bad.push([nazwa, 'box-shadow']);
            if (s.textShadow !== 'none') bad.push([nazwa, 'text-shadow']);
            if (s.backgroundImage !== 'none') bad.push([nazwa, 'background-image']);
            if (s.filter !== 'none' || (s.backdropFilter && s.backdropFilter !== 'none')) bad.push([nazwa, 'filter']);
            if (s.animationName !== 'none') bad.push([nazwa, 'animation']);
            if (parseFloat(s.borderTopLeftRadius) > 0) bad.push([nazwa, 'radius']);
          }
        }
        return bad;
      });
      expect(zle).toEqual([]);
    });

    test('cyjan tylko jako sygnał: w spoczynku nigdzie', async ({ page }) => {
      await otworz(page, vp, { przewin: true });
      const zle = await page.evaluate((C) => {
        const bad = [];
        for (const el of document.querySelectorAll('body *')) {
          const s = getComputedStyle(el);
          for (const w of ['color', 'backgroundColor', 'borderTopColor', 'borderRightColor', 'borderBottomColor', 'borderLeftColor', 'textDecorationColor']) {
            if (s[w] === C && !(w.startsWith('border') && parseFloat(s[w.replace('Color', 'Width')]) === 0)) {
              bad.push(`${el.tagName.toLowerCase()}.${(el.getAttribute('class') || '').split(' ')[0]} ${w}`);
            }
          }
        }
        return [...new Set(bad)];
      }, CYJAN);
      expect(zle).toEqual([]);
    });

    test('jedna jasna sekcja: case study w kolorach odwróconych', async ({ page }) => {
      await otworz(page, vp);
      const jasne = await page.evaluate(() => [...document.querySelectorAll('section')]
        .filter((s) => getComputedStyle(s).backgroundColor === 'rgb(240, 240, 240)').map((s) => s.id));
      expect(jasne).toEqual(['case-study']);
      await expect(page.locator('#case-study .h2')).toHaveCSS('color', 'rgb(5, 5, 5)');
      await expect(page.locator('#case-study .sec__meta')).toHaveCSS('color', 'rgb(92, 92, 92)');
    });

    test('każde zdjęcie raz w DOM, także przy otwartej szufladzie', async ({ page }) => {
      await otworz(page, vp);
      const zdjecia = async () => page.evaluate(() => [...document.images].filter((i) => !i.closest('[aria-hidden="true"]')).map((i) => i.getAttribute('src')));
      const przed = await zdjecia();
      expect(przed.length).toBe(new Set(przed).size);
      for (const klucz of ['yeah-gym', 'matys', 'eco-studio', 'drezno']) {
        await page.locator(`[data-cs="${klucz}"]`).first().click();
        await expect(page.locator('#szuflada')).toBeVisible();
        const teraz = await zdjecia();
        expect(teraz.length, klucz).toBe(new Set(teraz).size);
        await page.keyboard.press('Escape');
        await expect(page.locator('#szuflada')).toBeHidden();
      }
    });

    test('fonty, przycisk główny i nagłówki mieszczą się', async ({ page }) => {
      await otworz(page, vp);
      const fonty = await page.evaluate(() => [...document.fonts].filter((f) => f.status === 'loaded').map((f) => f.family));
      expect(fonty).toEqual(expect.arrayContaining(['Space Grotesk', 'Plus Jakarta Sans']));
      for (const sel of ['#formaty .btn']) {
        await expect(page.locator(sel)).toHaveCSS('background-color', 'rgb(240, 240, 240)');
        await expect(page.locator(sel)).toHaveCSS('color', 'rgb(5, 5, 5)');
      }
      const wystaje = await page.evaluate(() => [...document.querySelectorAll('.h2, .display, .num')]
        .filter((h) => h.scrollWidth > h.clientWidth + 1).map((h) => h.textContent.trim().slice(0, 30)));
      expect(wystaje).toEqual([]);
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
      const tekst = await page.locator('body').innerText();
      expect(tekst).not.toMatch(/\bDOF\b|M\/S|132\s?CM|✓|☎|✉|↗|darmow|za darmo|Najlepsze ceny|ZERO|10×|Karolina M|Clash Display|trojmiasto/i);
    });

    test('FAQ: 10 pytań, zgodne z danymi strukturalnymi, akordeon działa', async ({ page }) => {
      await otworz(page, vp);
      const widoczne = await page.locator('.faq__q').allInnerTexts();
      const ld = await page.evaluate(() => {
        for (const s of document.querySelectorAll('script[type="application/ld+json"]')) {
          const d = JSON.parse(s.textContent);
          if (d['@type'] === 'FAQPage') return d.mainEntity.map((q) => q.name);
        }
        return [];
      });
      expect(widoczne.map((t) => t.trim())).toEqual(ld);
      expect(widoczne.length).toBe(10);
      const q = page.locator('.faq__q').nth(2);
      await q.click();
      await expect(q).toHaveAttribute('aria-expanded', 'true');
      await expect(page.locator('#faq-3')).toBeVisible();
      await q.click();
      await expect(page.locator('#faq-3')).toBeHidden();
    });
  });
}

test.describe('nawigacja', () => {
  test.use({ contextOptions: { reducedMotion: 'reduce' } });

  test('desktop: 72 px, linki ze specyfikacji, tło i linia po przewinięciu', async ({ page }) => {
    await otworz(page, { width: 1440, height: 900 });
    await expect(page.locator('#nav')).toHaveCSS('height', '72px');
    expect((await page.locator('.nav__menu a').allInnerTexts()).map((t) => t.trim()))
      .toEqual(['Realizacje', 'Występ', 'Formaty', 'Proces', 'Zakup i wdrożenia']);
    await expect(page.locator('.nav__akcje .nav__tel')).toHaveAttribute('href', 'tel:+48531408004');
    await expect(page.locator('.nav__cta')).toHaveText('Sprawdź termin');
    await expect(page.locator('#nav')).toHaveCSS('background-color', 'rgba(0, 0, 0, 0)');
    await page.evaluate(() => scrollTo({ top: 1200, behavior: 'instant' }));
    await expect(page.locator('#nav')).toHaveCSS('background-color', 'rgb(5, 5, 5)');
    await expect(page.locator('#nav')).toHaveCSS('border-bottom-color', 'rgb(31, 31, 31)');
  });

  test('mobile: menu otwiera się, zamyka klawiszem Esc i po kliknięciu linku', async ({ page }) => {
    await otworz(page, { width: 375, height: 812 });
    await expect(page.locator('.nav__menu')).toBeHidden();
    const p = page.locator('#navPrzycisk');
    await p.click();
    await expect(p).toHaveAttribute('aria-expanded', 'true');
    await expect(page.locator('#navPanel')).toBeVisible();
    await page.keyboard.press('Escape');
    await expect(page.locator('#navPanel')).toBeHidden();
    await expect(p).toBeFocused();
    await p.click();
    await page.locator('#navPanel a[href="#formaty"]').click();
    await expect(page.locator('#navPanel')).toBeHidden();
  });

  test('pasek mobilny: ukryty na hero, widoczny dalej, znów ukryty na górze', async ({ page }) => {
    await otworz(page, { width: 375, height: 812 });
    const widoczny = () => page.evaluate(() => document.getElementById('pasekMobilny').classList.contains('pasek--widoczny'));
    expect(await widoczny()).toBe(false);
    await page.evaluate(() => scrollTo({ top: 2500, behavior: 'instant' }));
    await expect.poll(widoczny).toBe(true);
    await page.evaluate(() => scrollTo({ top: 0, behavior: 'instant' }));
    await expect.poll(widoczny).toBe(false);
  });
});

test.describe('szuflada realizacji', () => {
  test.use({ contextOptions: { reducedMotion: 'reduce' } });
  test('otwiera się z danymi, trzyma fokus, Esc zamyka i oddaje fokus', async ({ page }) => {
    await otworz(page, { width: 1440, height: 900 });
    const kafel = page.locator('.realizacja[data-cs="grupa-rekord"]');
    await kafel.click();
    await expect(page.locator('#szufladaTytul')).toHaveText('Grupa Rekord');
    await expect(page.locator('#szufladaLink')).toHaveAttribute('href', 'case-study-grupa-rekord-mspo.html');
    await expect(page.locator('#szufladaZamknij')).toBeFocused();
    for (let i = 0; i < 6; i++) await page.keyboard.press('Tab');
    expect(await page.evaluate(() => document.getElementById('szuflada').contains(document.activeElement))).toBe(true);
    await page.keyboard.press('Escape');
    await expect(page.locator('#szuflada')).toBeHidden();
    await expect(kafel).toBeFocused();
    // realizacja bez case study: bez linku, z opisem
    await page.locator('.realizacja[data-cs="gonia-auto"]').click();
    await expect(page.locator('#szufladaLink')).toBeHidden();
    await expect(page.locator('#szufladaOpis')).not.toBeEmpty();
  });
});

test.describe('formularz rezerwacji', () => {
  test.use({ contextOptions: { reducedMotion: 'reduce' } });
  test('krok 1 → krok 2, walidacja, nowe pola w zgłoszeniu (request przechwycony)', async ({ page }) => {
    let wyslane = null;
    await page.route('https://formspree.io/**', async (r) => {
      wyslane = r.request().postDataJSON();
      await r.fulfill({ status: 200, contentType: 'application/json', body: '{"ok":true}' });
    });
    await otworz(page, { width: 1440, height: 900 });
    await page.locator('#formularz').scrollIntoViewIfNeeded();

    // krok 1: bez typu wydarzenia nie przechodzi
    await page.locator('#dalej').click();
    await expect(page.locator('#blad-typ')).toBeVisible();
    await expect(page.locator('#krok2')).toBeHidden();

    await page.locator('label.chip:has-text("Konferencja")').click();
    await expect(page.locator('#blad-typ')).toBeHidden();
    await page.locator('label.chip:has-text("Termin jeszcze nieustalony")').click();
    await expect(page.locator('#pole-data')).toBeDisabled();
    await page.fill('#pole-miejsce', 'Kraków, ICE');
    await page.locator('label.chip:has-text("500–2000")').click();
    await page.locator('#dalej').click();
    await expect(page.locator('#krok2')).toBeVisible();
    await expect(page.locator('#pole-name')).toBeFocused();

    // krok 2: wymagane imię i poprawny e-mail
    await page.locator('#wyslij').click();
    await expect(page.locator('#pole-imie .pole__blad')).toBeVisible();
    await page.fill('#pole-name', 'Jan Testowy');
    await page.fill('#pole-email', 'zly-adres');
    await page.locator('#wyslij').click();
    await expect(page.locator('#pole-mail .pole__blad')).toBeVisible();
    expect(wyslane).toBeNull();

    await page.fill('#pole-email', 'jan@test.pl');
    await page.fill('#pole-company', 'Firma Test');
    await page.fill('#pole-message', 'Konferencja branżowa, dwa dni.');
    await expect(page.locator('#licznik')).toHaveText('30');
    await page.locator('#wyslij').click();
    await expect(page.locator('.form-sukces')).toBeVisible();
    expect(wyslane).toEqual({
      name: 'Jan Testowy', company: 'Firma Test', email: 'jan@test.pl', phone: '—', date: 'nieustalony',
      location: 'Kraków, ICE', message: 'Konferencja branżowa, dwa dni.', event_type: 'Konferencja', guests: '500–2000',
    });
  });
});

test.describe('ruch', () => {
  test('prefers-reduced-motion: wszystko widoczne od razu, bez przejść', async ({ browser }) => {
    const ctx = await browser.newContext({ reducedMotion: 'reduce', viewport: { width: 1440, height: 900 } });
    const page = await ctx.newPage();
    await page.goto(ADRES);
    const stan = await page.evaluate(() => ({
      ukryte: [...document.querySelectorAll('.wejscie')].filter((e) => getComputedStyle(e).opacity !== '1').length,
      przejscia: [...document.querySelectorAll('.wejscie, .btn, .nav')].filter((e) => getComputedStyle(e).transitionDuration.split(',').some((d) => parseFloat(d) > 0)).length,
    }));
    expect(stan).toEqual({ ukryte: 0, przejscia: 0 });
    await ctx.close();
  });

  test('bez ograniczenia ruchu: sekcja wchodzi raz, 12 px i 700 ms', async ({ browser }) => {
    const ctx = await browser.newContext({ reducedMotion: 'no-preference', viewport: { width: 1440, height: 900 } });
    const page = await ctx.newPage();
    await page.goto(ADRES);
    const przed = await page.evaluate(() => {
      const e = document.querySelector('#formaty .wejscie');
      const s = getComputedStyle(e);
      return { opacity: s.opacity, transform: s.transform, czas: s.transitionDuration };
    });
    expect(przed).toEqual({ opacity: '0', transform: 'matrix(1, 0, 0, 1, 0, 12)', czas: '0.7s, 0.7s' });
    await page.locator('#formaty').scrollIntoViewIfNeeded();
    await expect.poll(() => page.evaluate(() => document.querySelector('#formaty .wejscie').classList.contains('widoczne'))).toBe(true);
    await ctx.close();
  });
});

// Plik zdjęcia → realizacja (do sprawdzenia limitu trzech zdjęć na realizację).
const REALIZACJA = [
  [/gala-|nocny-pokaz/, 'drezno'], [/eco-studio/, 'eco-studio'], [/women-in-tech/, 'women-in-tech'], [/lexai/, 'lexai'],
  [/grupa-rekord/, 'grupa-rekord'], [/kopernik/, 'kopernik'], [/przelewice/, 'przelewice'], [/robot-w-deszczu/, 'gonia-auto'],
  [/event-nad-woda|spotkanie-biznesowe/, 'loza'], [/wesele/, 'wesele'], [/dream-med/, 'dream-med'], [/matys/, 'matys'],
  [/szkola-kosmos/, 'szkola-kosmos'], [/yeah-gym/, 'yeah-gym'], [/jednorozec/, 'jednorozec'], [/tet-trung-thu/, 'tet-trung-thu'],
];
const doRealizacji = (src) => (REALIZACJA.find(([r]) => r.test(src)) || [null, src])[1];
// Kopie kafli w pasach (aria-hidden) istnieją tylko po to, żeby pętla była bez szwu — nie liczą się jako powtórzenie.
const unikalne = (page) => page.evaluate(() => { const s = [...document.images].filter((i) => !i.closest('[aria-hidden="true"]')).map((i) => i.getAttribute('src')); return s.length === new Set(s).size; });

test.describe('hero — rotacja zdjęć z realizacji', () => {
  test('co 6 s kolejny kadr z podpisem, każde zdjęcie raz w DOM, pauza zatrzymuje', async ({ browser }) => {
    const ctx = await browser.newContext({ reducedMotion: 'no-preference', viewport: { width: 1440, height: 900 } });
    const page = await ctx.newPage();
    await page.clock.install();
    await page.goto(ADRES);
    await page.waitForLoadState('load');
    const img = page.locator('.hero img');
    await expect(img).toHaveCount(1);
    await expect(img).toHaveAttribute('src', /gala-wsrod-gosci/);
    await expect(page.locator('#heroLicznik')).toHaveText('01 / 06');
    const dalej = async () => { await page.clock.runFor(6000); await page.waitForTimeout(250); await page.clock.runFor(500); await page.waitForTimeout(100); };

    const wysokosc = () => page.locator('.hero').evaluate((e) => e.getBoundingClientRect().height);
    const h0 = await wysokosc();
    await dalej();
    await expect(img).toHaveAttribute('src', /eco-studio-wywiad/);
    expect(await wysokosc(), 'zmiana kadru nie zmienia wysokości hero').toBe(h0);
    await expect(page.locator('#heroLicznik')).toHaveText('02 / 06');
    await expect(page.locator('#heroOpis')).toHaveText('Finał Eco Studio ELECTRO-SYSTEM · Warszawa');
    expect(await unikalne(page)).toBe(true);
    for (let n = 3; n <= 6; n++) {
      await dalej();
      await expect(page.locator('#heroLicznik')).toHaveText(`0${n} / 06`);
      expect(await unikalne(page), `slajd ${n}`).toBe(true);
    }
    await dalej();
    await expect(page.locator('#heroLicznik')).toHaveText('01 / 06');

    // pauza: przycisk zatrzymuje, „Wznów” rusza dalej
    await page.locator('#heroPauza').click();
    await expect(page.locator('#heroPauza')).toHaveAttribute('aria-pressed', 'true');
    await expect(page.locator('#heroPauza')).toHaveText('Wznów');
    await page.mouse.move(5, 5);
    await page.evaluate(() => document.activeElement.blur());
    await page.clock.runFor(30000); await page.waitForTimeout(200);
    await expect(page.locator('#heroLicznik')).toHaveText('01 / 06');
    await page.locator('#heroPauza').click();
    await page.mouse.move(5, 5);
    await page.evaluate(() => document.activeElement.blur());
    await dalej();
    await expect(page.locator('#heroLicznik')).toHaveText('02 / 06');
    await ctx.close();
  });

  test('ograniczony ruch: nic nie zmienia się samo; najwyżej 3 zdjęcia na realizację', async ({ browser }) => {
    const ctx = await browser.newContext({ reducedMotion: 'reduce', viewport: { width: 1440, height: 900 } });
    const page = await ctx.newPage();
    await page.clock.install();
    await page.goto(ADRES);
    await page.waitForLoadState('load');
    await page.clock.runFor(30000);
    await expect(page.locator('#heroLicznik')).toHaveText('01 / 06');
    await expect(page.locator('#heroPauza')).toHaveText('Następne zdjęcie');

    // wszystkie zdjęcia, jakie strona pokazuje: stałe, slajdy hero i szuflady
    const pliki = new Set(await page.evaluate(() => [...document.images].map((i) => i.getAttribute('src'))));
    for (let n = 2; n <= 6; n++) {
      await page.locator('#heroPauza').click();
      await page.waitForTimeout(150); await page.clock.runFor(50); await page.waitForTimeout(50);
      await expect(page.locator('#heroLicznik')).toHaveText(`0${n} / 06`);
      pliki.add(await page.locator('.hero img').getAttribute('src'));
    }
    for (const klucz of await page.evaluate(() => [...new Set([...document.querySelectorAll('[data-cs]')].map((b) => b.dataset.cs))])) {
      await page.locator(`[data-cs="${klucz}"]`).first().click();
      for (const s of await page.locator('#szufladaZdjecia img').evaluateAll((im) => im.map((i) => i.getAttribute('src')))) pliki.add(s);
      expect(await unikalne(page), `szuflada ${klucz}`).toBe(true);
      await page.keyboard.press('Escape');
    }
    const naRealizacje = {};
    for (const p of pliki) if (/realizacja-/.test(p)) (naRealizacje[doRealizacji(p)] ??= new Set()).add(p);
    const ponadLimit = Object.entries(naRealizacje).filter(([, s]) => s.size > 3).map(([k, s]) => `${k}: ${[...s].join(', ')}`);
    expect(ponadLimit).toEqual([]);
    await ctx.close();
  });
});

test('treść: branding zamiast stroju, robot mówi w każdym języku', async ({ page }) => {
  await page.goto(ADRES);
  const tekst = await page.locator('body').textContent();
  expect(tekst).not.toMatch(/\bstr[óo]j(u|em|e)?\b|garderob/i);
  const lead = page.locator('.hero .lead');
  await expect(lead).toContainText('Mówi po polsku i w każdym innym języku');
  await expect(lead).toContainText('branding w cenie');
  await expect(page.locator('#wystep')).toContainText('na Litwie, w Niemczech, Czechach i Rumunii');
  await expect(page.locator('#faq-5')).toContainText('w każdym innym języku');
  const ld = await page.evaluate(() => [...document.querySelectorAll('script[type="application/ld+json"]')].map((s) => s.textContent).join(' '));
  expect(ld).not.toMatch(/\bstr[óo]j/i);
});

// ——— Pasy bez końca: realizacje i klienci ———
const przesuniecia = (page) => page.evaluate(() => [...document.querySelectorAll('.pas')].map((pas) => {
  const t = pas.querySelector('.pas__tor'); const a = pas.getBoundingClientRect(), r = t.getBoundingClientRect();
  return { x: new DOMMatrix(getComputedStyle(t).transform).m41, pokrywa: r.left <= a.left + 1 && r.right >= a.right - 1 };
}));

test.describe('pasy realizacji i klientów', () => {
  for (const vp of [{ width: 1440, height: 900 }, { width: 375, height: 812 }]) {
    test(`ruch bez końca, kopie poza dostępnością, pauza @${vp.width}`, async ({ browser }) => {
      const ctx = await browser.newContext({ reducedMotion: 'no-preference', viewport: vp });
      const page = await ctx.newPage();
      await page.goto(ADRES); await page.waitForLoadState('load');
      const zdjecia = page.locator('.pasy[data-grupa="zdjecia"]');
      await zdjecia.scrollIntoViewIfNeeded();
      await page.mouse.move(2, 2);

      // każdy rząd jedzie i przez cały czas pokrywa szerokość ekranu — nie widać końca
      const a = await przesuniecia(page);
      await page.waitForTimeout(1200);
      const b = await przesuniecia(page);
      for (const i of [0, 1, 2]) {
        expect(Math.abs(b[i].x - a[i].x), `rząd ${i + 1} stoi`).toBeGreaterThan(10);
        expect(a[i].pokrywa && b[i].pokrywa, `rząd ${i + 1} ma koniec`).toBe(true);
      }
      // kierunki na przemian
      expect(Math.sign(b[0].x - a[0].x)).not.toBe(Math.sign(b[1].x - a[1].x) || 0);

      // kopie: ukryte przed czytnikiem, poza kolejnością Tab; oryginały bez powtórzeń
      const kopie = await page.evaluate(() => {
        const k = [...document.querySelectorAll('.pas__tor > [data-kopia]')];
        return { ile: k.length, ukryte: k.every((li) => li.getAttribute('aria-hidden') === 'true'),
          tab: k.flatMap((li) => [...li.querySelectorAll('button, a')]).every((x) => x.tabIndex === -1) };
      });
      expect(kopie.ile).toBeGreaterThan(0);
      expect(kopie.ukryte && kopie.tab).toBe(true);
      expect(await unikalne(page)).toBe(true);

      // przycisk zatrzymuje całą grupę
      const pauza = page.locator('.pasy__pauza[data-pasy="zdjecia"]');
      await expect(pauza).toBeVisible();
      await pauza.click();
      await expect(pauza).toHaveAttribute('aria-pressed', 'true');
      await expect(pauza).toHaveText('Wznów ruch');
      await page.mouse.move(2, 2); await page.locator('body').evaluate(() => document.activeElement.blur());
      await page.waitForTimeout(1500);
      const c = await przesuniecia(page); await page.waitForTimeout(800); const d = await przesuniecia(page);
      for (const i of [0, 1, 2]) expect(d[i].x, `rząd ${i + 1} po pauzie`).toBe(c[i].x);
      await pauza.click();
      await expect(pauza).toHaveText('Zatrzymaj ruch');
      await ctx.close();
    });
  }

  test('najechanie wyhamowuje rząd, przeciąganie przesuwa bez otwierania szuflady, klik otwiera', async ({ browser }) => {
    const ctx = await browser.newContext({ reducedMotion: 'no-preference', viewport: { width: 1440, height: 900 } });
    const page = await ctx.newPage();
    await page.goto(ADRES); await page.waitForLoadState('load');
    const pas = page.locator('.pas').nth(1);
    await pas.scrollIntoViewIfNeeded();
    const box = await pas.boundingBox();
    await page.mouse.move(box.x + box.width / 2, box.y + 100);
    await page.waitForTimeout(1500);
    const e = await przesuniecia(page); await page.waitForTimeout(700); const f = await przesuniecia(page);
    expect(f[1].x, 'rząd pod kursorem stoi').toBe(e[1].x);
    expect(f[0].x, 'inne rzędy jadą dalej').not.toBe(e[0].x);

    await page.mouse.down();
    await page.mouse.move(box.x + box.width / 2 - 300, box.y + 100, { steps: 12 });
    await page.mouse.up();
    const g = await przesuniecia(page);
    expect(Math.abs(g[1].x - f[1].x)).toBeGreaterThan(200);
    await page.waitForTimeout(200);
    await expect(page.locator('#szuflada')).toBeHidden();

    await page.waitForTimeout(1500);
    await page.mouse.click(box.x + box.width / 2, box.y + 100);
    await expect(page.locator('#szuflada')).toBeVisible();
    await ctx.close();
  });

  test('układ: w rzędzie żadne dwa sąsiednie kadry (także na styku pętli) nie są z tej samej realizacji', async ({ page }) => {
    await page.goto(ADRES);
    const rzedy = await page.evaluate(() => [...document.querySelectorAll('.pasy[data-grupa="zdjecia"] .pas')]
      .map((pas) => [...pas.querySelectorAll('.pas__tor > li:not([data-kopia]) [data-cs]')].map((b) => b.dataset.cs)));
    expect(rzedy.length).toBeGreaterThanOrEqual(3);
    for (const r of rzedy) r.forEach((cs, i) => expect(cs, r.join(' ')).not.toBe(r[(i + 1) % r.length]));
    const nazwy = await page.locator('.pasy[data-grupa="nazwy"] .pas__tor > li:not([data-kopia])').allInnerTexts();
    expect(nazwy.length).toBe(39);
    expect(new Set(nazwy).size).toBe(39);
  });

  test('ograniczony ruch: nic nie jedzie, bez kopii, nazwy jako zwykła lista', async ({ browser }) => {
    const ctx = await browser.newContext({ reducedMotion: 'reduce', viewport: { width: 1440, height: 900 } });
    const page = await ctx.newPage();
    await page.goto(ADRES); await page.waitForLoadState('load');
    await page.locator('.pasy').first().scrollIntoViewIfNeeded();
    expect(await page.locator('[data-kopia]').count()).toBe(0);
    await expect(page.locator('.pasy__pauza').first()).toBeHidden();
    const a = await przesuniecia(page); await page.waitForTimeout(800); const b = await przesuniecia(page);
    expect(b.map((x) => x.x)).toEqual(a.map((x) => x.x));
    expect(await page.locator('.pasy--ruch').count()).toBe(0);
    await ctx.close();
  });
});
