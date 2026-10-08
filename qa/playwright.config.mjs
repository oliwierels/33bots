// Testy akceptacyjne 33bots.pl.
// Uruchomienie z katalogu głównego repozytorium:
//   qa/node_modules/.bin/playwright test --config qa/playwright.config.mjs
// Serwer statyczny startuje sam (python3 -m http.server na porcie 8080).
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  testMatch: /.*\.spec\.mjs$/,
  // Strony DE i AT mają własną konfigurację (playwright.zagranica.config.mjs).
  testIgnore: /zagranica\.spec\.mjs$/,
  timeout: 90_000,
  workers: 2,
  reporter: [['list']],
  use: { browserName: 'chromium' },
  webServer: {
    command: 'python3 -m http.server 8080 --bind 127.0.0.1 --directory ..',
    url: 'http://127.0.0.1:8080/',
    reuseExistingServer: true,
    timeout: 20_000,
    stdout: 'ignore',
    stderr: 'pipe',
  },
});
