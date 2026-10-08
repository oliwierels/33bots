// Testy stron głównych 33bots.de i 33bots.at, generowanych z układu strony PL
// (tresci/zagranica/buduj_glowna.py). Repozytoria rynków leżą obok tego:
//   ../33bots-de        (gałąź z 33bots.de)
//   ../strona-austria   (repozytorium 33bots.at)
// Inne położenie: zmienne RYNEK_DE i RYNEK_AT.
//
// Uruchomienie z katalogu głównego repozytorium PL:
//   qa/node_modules/.bin/playwright test --config qa/playwright.zagranica.config.mjs
import { defineConfig } from '@playwright/test';
import { fileURLToPath } from 'node:url';

const obok = (nazwa) => fileURLToPath(new URL(`../../${nazwa}`, import.meta.url));
const DE = process.env.RYNEK_DE || obok('33bots-de');
const AT = process.env.RYNEK_AT || obok('strona-austria');
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
  webServer: [serwer(8081, DE), serwer(8082, AT)],
});
