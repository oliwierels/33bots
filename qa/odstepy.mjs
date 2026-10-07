// Sprawdza, czy tekst nigdzie nie dotyka ramki ani krawędzi tła kontenera.
//
// Zasada: każdy kontener z obramowaniem lub tłem trzyma tekst co najmniej
// 24 px od krawędzi na telefonie i 32 px na desktopie.
//   • kontener z tłem albo z ramką dookoła — sprawdzane wszystkie cztery strony,
//   • kontener z linią tylko z jednej strony (linia włosowa) — tylko ta strona,
//   • kontener na całą szerokość ekranu (pas sekcji) — tylko góra i dół;
//     boki wyznacza margines strony, nie ten kontener.
//
// Pomijane, bo to nie są kontenery na treść:
//   • kontrolki: button, input, select, textarea oraz linki, etykiety
//     i elementy wewnątrz linku lub przycisku nie wyższe niż 64 px
//     (przyciski, przyciski-atrapy w klikalnych pasach),
//   • plakietki: jedna linia drobnego tekstu do 48 px wysokości (tagi,
//     pigułki, numery) i elementy nie większe niż 64 × 64 px,
//   • nagłówek strony (<header> przy samej górze dokumentu) — jego wysokość (72 px) wynika
//     ze specyfikacji nawigacji; przy tekście 15 px nie zmieści 32 px nad
//     i pod nim, więc to osobna decyzja, nie automatyczna poprawka,
//   • elementy niewidoczne (display: none, visibility: hidden, opacity: 0,
//     zawartość zwiniętego <details>),
//   • tekst schowany poza obszarem przewijanego potomka.

export async function naruszeniaOdstepow(page, minimum) {
  return page.evaluate((MIN) => {
    const POMIN = new Set(['BUTTON', 'INPUT', 'SELECT', 'TEXTAREA', 'OPTION', 'IMG', 'VIDEO',
      'IFRAME', 'SVG', 'PICTURE', 'SOURCE', 'SCRIPT', 'STYLE', 'NOSCRIPT', 'BR']);
    const vw = document.documentElement.clientWidth;

    const alfa = (kolor) => {
      const m = kolor.match(/rgba?\(([^)]+)\)/);
      if (!m) return 0;
      const p = m[1].split(/[\s,/]+/).filter(Boolean);
      return p.length >= 4 ? parseFloat(p[3]) : 1;
    };
    const widoczny = (el) => {
      // checkVisibility rozpoznaje też zawartość zwiniętego <details>
      // (content-visibility), której współrzędne Chrome i tak zwraca.
      if (el.checkVisibility && !el.checkVisibility({ opacityProperty: true, visibilityProperty: true, contentVisibilityAuto: true })) return false;
      for (let e = el; e && e !== document.documentElement; e = e.parentElement) {
        const s = getComputedStyle(e);
        if (s.display === 'none' || s.visibility === 'hidden' || parseFloat(s.opacity) === 0) return false;
      }
      return true;
    };
    const opis = (el) => {
      let s = el.tagName.toLowerCase();
      if (el.id) s += '#' + el.id;
      const klasy = (el.getAttribute('class') || '').trim().split(/\s+/).filter(Boolean).slice(0, 3);
      if (klasy.length) s += '.' + klasy.join('.');
      return s;
    };
    const przyciety = (t, odEl, doEl) => {
      for (let e = odEl; e && e !== doEl; e = e.parentElement) {
        const s = getComputedStyle(e);
        if (s.overflowX === 'visible' && s.overflowY === 'visible') continue;
        const r = e.getBoundingClientRect();
        if (t.right <= r.left || t.left >= r.right || t.bottom <= r.top || t.top >= r.bottom) return true;
      }
      return false;
    };

    const wyniki = [];
    for (const el of document.querySelectorAll('body *')) {
      if (POMIN.has(el.tagName)) continue;
      const s = getComputedStyle(el);
      if (s.display === 'inline' || s.display === 'contents') continue;
      const r = el.getBoundingClientRect();
      if (r.width < 1 || r.height < 1) continue;
      const kontrolka = (el.tagName === 'A' || el.tagName === 'LABEL' || el.getAttribute('role') === 'button'
        || el.parentElement?.closest('a, button')) && r.height <= 64;
      const plakietka = r.height <= 48 || (r.width <= 64 && r.height <= 64);
      const naglowekStrony = el.tagName === 'HEADER' && r.top <= 1
        && (['fixed', 'sticky'].includes(s.position) || r.top + scrollY <= 1);
      if (kontrolka || plakietka || naglowekStrony) continue;

      const tlo = alfa(s.backgroundColor) > 0.02 || s.backgroundImage !== 'none';
      const ramka = {};
      for (const [st, St] of [['top', 'Top'], ['right', 'Right'], ['bottom', 'Bottom'], ['left', 'Left']]) {
        ramka[st] = parseFloat(s[`border${St}Width`]) >= 1 && s[`border${St}Style`] !== 'none'
          && alfa(s[`border${St}Color`]) > 0.02;
      }
      if (!tlo && !Object.values(ramka).some(Boolean)) continue;
      if (!widoczny(el)) continue;

      const pelnaSzerokosc = r.width >= vw - 2;
      const wnetrze = {
        top: r.top + parseFloat(s.borderTopWidth),
        bottom: r.bottom - parseFloat(s.borderBottomWidth),
        left: r.left + parseFloat(s.borderLeftWidth),
        right: r.right - parseFloat(s.borderRightWidth),
      };
      const najblizej = { top: Infinity, right: Infinity, bottom: Infinity, left: Infinity };
      const probka = {};
      const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, {
        acceptNode: (n) => (n.nodeValue.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT),
      });
      for (let n = walker.nextNode(); n; n = walker.nextNode()) {
        const rodzic = n.parentElement;
        if (!rodzic || !widoczny(rodzic)) continue;
        const zakres = document.createRange();
        zakres.selectNodeContents(n);
        for (const t of zakres.getClientRects()) {
          if (t.width < 1 || t.height < 1) continue;
          if (przyciety(t, rodzic, el)) continue;
          const d = {
            top: t.top - wnetrze.top, bottom: wnetrze.bottom - t.bottom,
            left: t.left - wnetrze.left, right: wnetrze.right - t.right,
          };
          for (const st of Object.keys(d)) {
            if (d[st] < najblizej[st]) { najblizej[st] = d[st]; probka[st] = n.nodeValue.trim().slice(0, 40); }
          }
        }
      }
      for (const st of ['top', 'right', 'bottom', 'left']) {
        const wymagana = (tlo || ramka[st]) && !(pelnaSzerokosc && (st === 'left' || st === 'right'));
        if (wymagana && najblizej[st] < MIN - 0.5) {
          wyniki.push({ element: opis(el), strona: st, odstep: Math.round(najblizej[st]), wymagane: MIN, tekst: probka[st] });
        }
      }
    }
    return wyniki;
  }, minimum);
}

// Przewija stronę do końca, żeby odpaliły wszystkie animacje wejścia,
// i wraca na górę. Wywołuj przed pomiarem.
export async function przewinCala(page) {
  await page.evaluate(async () => {
    for (let y = 0; y < document.body.scrollHeight; y += Math.round(innerHeight * 0.6)) {
      scrollTo({ top: y, behavior: 'instant' });
      await new Promise((r) => setTimeout(r, 60));
    }
    scrollTo({ top: 0, behavior: 'instant' });
    await new Promise((r) => setTimeout(r, 400));
  });
}
