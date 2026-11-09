// Strona główna po przebudowie: robot 3D z punktów, kalkulator ceny, kroki występu.
// Robot zależy od WebGL w przeglądarce testowej: bez niego strona musi wrócić do zdjęcia (bez-3d).
import { test, expect } from '@playwright/test';

const ADRES = 'http://localhost:8080/';

test.describe('robot 3D', () => {
  test('dane robota: nagłówek, 24 segmenty, liczba punktów zgodna z rozmiarem pliku', async ({ request }) => {
    for (const plik of ['robot/g1.bin', 'robot/g1-lekki.bin']) {
      const odp = await request.get(ADRES + plik);
      expect(odp.ok(), plik).toBe(true);
      const b = await odp.body();
      const dl = b.readUInt32LE(0);
      const nag = JSON.parse(b.subarray(4, 4 + dl).toString('utf8'));
      expect(nag.segmenty.length).toBe(24);
      expect(nag.bloki.reduce((s, [, a, k]) => s + a + k, 0)).toBe(nag.n);
      expect(b.length).toBe(4 + dl + nag.n * 8);
    }
    expect((await request.get(ADRES + 'robot/LICENCJA-UNITREE.txt')).ok()).toBe(true);
  });

  test('ładuje się albo wraca do zdjęcia; płótno nie łapie kliknięć i nie zasłania przycisku', async ({ page }) => {
    const bledy = [];
    page.on('pageerror', (e) => bledy.push(e.message));
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(ADRES);
    // dane robota ładują się dopiero po załadowaniu strony, przy zbliżaniu się do jego sceny
    await page.locator('#robot').scrollIntoViewIfNeeded();
    await expect.poll(() => page.evaluate(() => document.documentElement.dataset.robot || ''), { timeout: 20000 }).toMatch(/gotowy|brak/);
    const stan = await page.evaluate(() => document.documentElement.dataset.robot);
    if (stan === 'gotowy') {
      const c = page.locator('canvas.robot3d');
      await expect(c).toHaveCount(1);
      await expect(c).toHaveCSS('pointer-events', 'none');
      await expect(c).toHaveAttribute('aria-hidden', 'true');
      // przycisk w hero da się kliknąć mimo płótna nad treścią
      await page.locator('.hero [data-cta="hero"]').click({ trial: true });
    } else {
      await expect(page.locator('html')).toHaveClass(/bez-3d/);
      await expect(page.locator('#robot')).toBeHidden();
    }
    expect(bledy).toEqual([]);
  });
});

test.describe('polecenia i ruch', () => {
  test('przyciski poleceń: gest w dataLayer, dymek; „Zatrzymaj ruch” zatrzymuje robota i animacje kart', async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(ADRES);
    await page.evaluate(() => { const r = document.getElementById('robot'); scrollTo({ top: scrollY + r.getBoundingClientRect().top + 10, behavior: 'instant' }); });
    await expect.poll(() => page.evaluate(() => document.documentElement.dataset.robot || ''), { timeout: 20000 }).toMatch(/gotowy|brak/);
    if (await page.evaluate(() => document.documentElement.dataset.robot) === 'gotowy') {
      await page.locator('[data-robot-gest="tanczy"]').click();
      expect(await page.evaluate(() => window.dataLayer.filter((z) => z.event === 'robot_gest').map((z) => z.robot_gest))).toContain('tanczy');
      await page.locator('[data-robot-gest="mowi"]').click();
      await expect(page.locator('#robotDymek')).not.toBeEmpty();
    }
    const pauza = page.locator('#robotPauza');
    await pauza.click();
    await expect(pauza).toHaveAttribute('aria-pressed', 'true');
    await expect(pauza).toHaveText('Wznów ruch');
    await expect(page.locator('.zasady__pauza')).toHaveText('Wznów ruch');
    expect(await page.locator('#zasady .a-wiazka').evaluate((e) => getComputedStyle(e).animationPlayState)).toBe('paused');
    await page.locator('.zasady__pauza').click();
    await expect(pauza).toHaveAttribute('aria-pressed', 'false');
  });
});

test.describe('kalkulator ceny', () => {
  test.use({ contextOptions: { reducedMotion: 'reduce' } });
  test('formaty, dni, kwoty i wycena w opisie zgłoszenia', async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(ADRES);
    const kwota = page.locator('#kalkKwota');
    await expect(kwota).toHaveText('5 500');
    await expect(page.locator('#kalkDni')).toBeHidden();
    await page.locator('label.format:has-text("Targi")').click();
    await expect(page.locator('#kalkDni')).toBeVisible();
    await expect(kwota).toHaveText('9 350');
    await expect(page.locator('#kalkOpis')).toContainText('oszczędzasz 1 650 zł');
    await expect(page.locator('[data-dni="-1"]')).toBeDisabled(); // najmniej dwa dni
    for (let i = 0; i < 8; i++) await page.locator('[data-dni="1"]').click({ force: true });
    await expect(page.locator('#kalkIle')).toHaveText('7');
    await expect(kwota).toHaveText('32 725');
    await page.locator('[data-dni="-1"]').click();
    await page.locator('[data-dni="-1"]').click();
    await page.locator('[data-dni="-1"]').click();
    await page.locator('[data-dni="-1"]').click();
    await expect(kwota).toHaveText('14 025');
    await page.locator('label.format:has-text("Wejście")').click();
    await expect(page.locator('#kalkOd')).toHaveText('poniżej');
    await page.locator('label.format:has-text("Targi")').click();
    await page.locator('#formaty [data-cta="formaty"]').click();
    await expect(page.locator('#pole-message')).toHaveValue('Interesuje mnie 3 dni (od 14 025 zł netto).');
    await expect(page.locator('#licznik')).toHaveText('43');
    // pola kalkulatora nie trafiają do zgłoszenia (są poza formularzem)
    expect(await page.evaluate(() => [...new FormData(document.getElementById('formularz')).keys()].includes('kalk_format'))).toBe(false);
  });
});

test.describe('robot z bliska', () => {
  test('przewijanie sceny podświetla kolejne części ciała', async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(ADRES);
    const sekcja = page.locator('#robot');
    for (const [p, czesc] of [[0, 'glowa'], [0.25, 'twarz'], [0.42, 'piers'], [0.58, 'rece'], [0.75, 'nogi'], [0.97, 'stopy']]) {
      await page.evaluate((p) => { const r = document.getElementById('robot'); const top = scrollY + r.getBoundingClientRect().top;
        scrollTo({ top: top + (r.offsetHeight - innerHeight) * p, behavior: 'instant' }); }, p);
      await expect(sekcja).toHaveAttribute('data-czesc', czesc);
    }
  });
});

test.describe('robot sam z siebie', () => {
  test('na przyklejonej scenie robot sam wykonuje ruchy (stawy się zmieniają)', async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(ADRES + '?robot-debug');
    await page.evaluate(() => { const r = document.getElementById('robot'); scrollTo({ top: scrollY + r.getBoundingClientRect().top + 10, behavior: 'instant' }); });
    await expect.poll(() => page.evaluate(() => document.documentElement.dataset.robot || ''), { timeout: 20000 }).toMatch(/gotowy|brak/);
    test.skip(await page.evaluate(() => document.documentElement.dataset.robot) !== 'gotowy', 'bez WebGL w przeglądarce testowej');
    const katy = () => page.evaluate(() => { const q = window.__robot.q(), I = window.__robot.IDX(); return [q[I.right_shoulder_pitch_joint], q[I.left_shoulder_pitch_joint], q[I.waist_yaw_joint]]; });
    const start = await katy();
    await expect.poll(async () => { const k = await katy(); return Math.max(...k.map((v, i) => Math.abs(v - start[i]))); }, { timeout: 15000 }).toBeGreaterThan(0.3);
  });
});

test.describe('kroki występu', () => {
  for (const vp of [{ width: 1440, height: 900 }, { width: 375, height: 812 }]) {
    test(`aktywny krok ustawia pozę robota @${vp.width}`, async ({ page }) => {
      await page.setViewportSize(vp);
      await page.goto(ADRES);
      const sekcja = page.locator('#wystep');
      await expect(sekcja).toHaveAttribute('data-poza', 'wita');
      for (const [poza, nazwa] of [['mowi', 'Głos i wiedza'], ['zdjecie', 'Zdjęcia i nagrania']]) {
        await page.locator(`.wiersz[data-poza="${poza}"]`).evaluate((e) => {
          const r = e.getBoundingClientRect();
          const scena = document.querySelector('.wystep__scena').getBoundingClientRect();
          const linia = innerWidth < 1024 ? 72 + scena.height + (innerHeight - 72 - scena.height) * 0.3 : innerHeight / 2;
          scrollTo({ top: scrollY + r.top - linia + 40, behavior: 'instant' });
        });
        await expect(sekcja).toHaveAttribute('data-poza', poza);
        await expect(page.locator('#wystepNazwa')).toHaveText(nazwa);
        await expect(page.locator(`.wiersz[data-poza="${poza}"]`)).toHaveClass(/wiersz--aktywny/);
      }
    });
  }
});
