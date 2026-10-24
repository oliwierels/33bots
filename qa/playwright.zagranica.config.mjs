// Testy stron 33bots.de, 33bots.at i 33bots.lt, generowanych z układu strony PL
// (tresci/zagranica/buduj_glowna.py). Repozytoria rynków leżą obok tego:
//   ../33bots-de        (gałąź z 33bots.de)
//   ../strona-austria   (repozytorium 33bots.at)
//   ../litwa-strona     (repozytorium 33bots.lt)
// Inne położenie: zmienne RYNEK_DE, RYNEK_AT i RYNEK_LT.
//
// Uruchomienie z katalogu głównego repozytorium PL:
//   qa/node_modules/.bin/playwright test --config qa/playwright.zagranica.config.mjs
import { defineConfig } from '@playwright/test';
import { fileURLToPath } from 'node:url';

const obok = (nazwa) => fileURLToPath(new URL(`../../${nazwa}`, import.meta.url));
const DE = process.env.RYNEK_DE || obok('33bots-de');
const AT = process.env.RYNEK_AT || obok('strona-austria');
const LT = process.env.RYNEK_LT || obok('litwa-strona');
const serwer = (port, katalog) => ({
  command: `python3 -m http.server ${port} --bind 127.0.0.1 --directory "${katalog}"`,
  url: `http://127.0.0.1:${port}/`,
  reuseExistingServer: true,
  timeout: 20_000,
  stdout: 'ignore',
  stderr: 'pipe',
});

export default defineConfig({
  testDir: '.',
  testMatch: /zagranica\.spec\.mjs$/,
  timeout: 90_000,
  workers: 2,
  reporter: [['list']],
  use: { browserName: 'chromium' },
  webServer: [serwer(8081, DE), serwer(8082, AT), serwer(8083, LT)],
});
