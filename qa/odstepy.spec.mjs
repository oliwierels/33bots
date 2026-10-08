// Tekst nie dotyka ramek ani krawędzi tła — na każdej zmienionej podstronie.
// Przy każdej kolejnej zmianie dopisz tu podstronę, którą ruszasz.
import { test, expect } from '@playwright/test';
import { naruszeniaOdstepow, przewinCala, fontyZRepo } from './odstepy.mjs';

const STRONY = [
  '/',
  '/case-study-eco-studio-electro-system.html',
  '/case-study-lexai.html',
  '/oferta-konferencje.html',
  '/oferta-targi.html',
  '/sklep.html',
  '/wdrozenia.html',
  // artykuły poradnika (nowy szablon)
  '/blog-atrakcje-eventowe.html',
  '/blog-ile-kosztuje-wynajem-robota.html',
  '/blog-lekcje-z-eventow-z-robotem.html',
  '/blog-robot-na-event-korporacyjny-przewodnik.html',
  '/blog-robot-na-event-miedzynarodowy.html',
  '/blog-robot-na-festyn-i-dni-gminy.html',
  // stare podstrony z dopisaną kartą poradnika
  '/blog.html',
  '/blog-atrakcja-na-event-firmowy.html',
  '/blog-robot-z-ai-rozmawiajacy-po-polsku.html',
  '/robot-na-dni-miasta.html',
  '/robot-na-festiwal.html',
  '/robot-na-piknik-firmowy.html',
  '/robot-na-dzien-dziecka.html',
  '/robot-na-event-outdoor.html',
  '/robot-na-event-miejski.html',
  '/robot-dla-dzieci.html',
  '/robot-na-event-korporacyjny.html',
  '/robot-na-impreze-firmowa.html',
  '/roboty-na-eventy-firmowe.html',
  '/robot-na-integracje-firmowa.html',
  '/robot-na-rocznice-firmy.html',
  '/robot-na-targi.html',
  '/robot-na-expo.html',
  '/robot-employer-branding.html',
  '/wynajem-robota-do-firmy.html',
  '/robot-na-konferencje.html',
  '/robot-na-konferencje-technologiczna.html',
  '/robot-ai-na-wydarzenie.html',
  '/robot-konferansjer.html',
  '/robot-na-event-vip.html',
  '/atrakcje-na-event.html',
  '/nowoczesne-atrakcje-eventowe.html',
  '/robot-na-impreze.html',
  '/robot-na-event.html',
  '/show-robotow.html',
  '/robot-na-gale.html',
  '/robot-na-bankiet.html',
  '/wypozyczenie-robota.html',
  '/wynajem-robotow.html',
  '/robot-humanoidalny-na-event.html',
];
const EKRANY = [
  { width: 375, height: 812, minimum: 24 },
  { width: 1440, height: 900, minimum: 32 },
];

test.use({ contextOptions: { reducedMotion: 'reduce' } });

for (const adres of STRONY) {
  for (const ekran of EKRANY) {
    test(`odstępy ${adres} @${ekran.width}`, async ({ page }) => {
      await page.setViewportSize({ width: ekran.width, height: ekran.height });
      await fontyZRepo(page);
      await page.goto('http://localhost:8080' + adres);
      await page.evaluate(() => document.fonts.ready);
      await przewinCala(page);
      const naruszenia = await naruszeniaOdstepow(page, ekran.minimum);
      expect(naruszenia, JSON.stringify(naruszenia, null, 1)).toEqual([]);
    });
  }
}
