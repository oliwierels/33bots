/* Strona główna .pl: liczniki w pasku skali, aktywny krok występu (poza robota),
   kalkulator ceny. Robot 3D jest w js/robot3d.js, reszta strony w skrypcie w index.html. */
(() => {
  'use strict';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  // 5500 → „5 500” (twarda spacja; pl-PL w toLocaleString nie grupuje czterech cyfr)
  const kwota = (n) => String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
  const rzadko = (f) => { let czeka = false; return () => { if (czeka) return; czeka = true; requestAnimationFrame(() => { czeka = false; f(); }); }; };

  /* ——— Liczniki: liczą od zera, kiedy wchodzą na ekran (te widoczne od razu stoją) ——— */
  const liczniki = [...document.querySelectorAll('[data-licz]')].filter((el) => +el.dataset.licz > 0);
  if (!reduce && 'IntersectionObserver' in window) {
    const liczDo = (el) => {
      const cel = +el.dataset.licz, t0 = performance.now(), czas = 1500;
      const krok = (t) => {
        const p = Math.min(1, (t - t0) / czas), e = 1 - Math.pow(2, -10 * p);
        el.textContent = kwota(cel * (p < 1 ? e : 1));
        if (p < 1) requestAnimationFrame(krok);
      };
      requestAnimationFrame(krok);
    };
    const io = new IntersectionObserver((wpisy) => wpisy.forEach((w) => {
      if (w.isIntersecting) { io.unobserve(w.target); liczDo(w.target); }
    }), { threshold: 0.8 });
    liczniki.forEach((el) => { if (el.getBoundingClientRect().top > innerHeight) { el.textContent = '0'; io.observe(el); } });
  }

  /* ——— Występ: krok najbliżej linii czytania ustawia pozę robota ———
     Desktop: linia w połowie ekranu. Telefon: tuż pod przyklejoną sceną. */
  const sekcja = document.getElementById('wystep');
  if (sekcja) {
    const kroki = [...sekcja.querySelectorAll('.wiersz[data-poza]')];
    const scena = sekcja.querySelector('.wystep__scena');
    const nr = document.getElementById('wystepNr'), nazwa = document.getElementById('wystepNazwa');
    const jezyk = document.getElementById('wystepJezyk'), czas = document.getElementById('wystepCzas');
    const kropka = sekcja.querySelector('.wystep__kropka');
    let aktywny = -1;
    const aktualizuj = () => {
      const sr = scena.getBoundingClientRect();
      const linia = innerWidth < 1024 ? sr.bottom + (innerHeight - sr.bottom) * 0.3 : innerHeight * 0.5;
      let naj = 0, odl = Infinity;
      kroki.forEach((k, i) => {
        const r = k.getBoundingClientRect();
        const d = r.top <= linia && r.bottom >= linia ? 0 : Math.min(Math.abs(r.top - linia), Math.abs(r.bottom - linia));
        if (d < odl) { odl = d; naj = i; }
      });
      if (naj === aktywny) return;
      aktywny = naj;
      kroki.forEach((k, i) => k.classList.toggle('wiersz--aktywny', i === naj));
      sekcja.dataset.poza = kroki[naj].dataset.poza;
      nr.textContent = String(naj + 1).padStart(2, '0');
      nazwa.textContent = kroki[naj].querySelector('.h3').textContent;
    };
    addEventListener('scroll', rzadko(aktualizuj), { passive: true });
    addEventListener('resize', rzadko(aktualizuj));
    aktualizuj();

    // „Głos”: powitania w językach krajów, w których pracowaliśmy, i kilku innych.
    // „Zdjęcia”: licznik nagrania. Tylko gdy sekcja jest na ekranie i ruch jest dozwolony.
    const POWITANIA = ['Dzień dobry', 'Hello', 'Guten Tag', 'Laba diena', 'Dobrý den', 'Bună ziua', 'Bonjour', 'Hola', 'Ciao', 'こんにちは'];
    let widac = false, i = 0, sek = 0, zegar = 0;
    const tik = () => {
      if (!widac) return;
      const poza = sekcja.dataset.poza;
      if (poza === 'mowi') { i = (i + 1) % POWITANIA.length; jezyk.textContent = POWITANIA[i]; }
      if (poza === 'zdjecie') {
        sek += 0.5;
        const s = Math.floor(sek);
        czas.textContent = ['00', String(Math.floor(s / 60)).padStart(2, '0'), String(s % 60).padStart(2, '0')].join(':');
        kropka.classList.toggle('zgasla', sek % 1 !== 0);
      } else sek = 0;
    };
    if (!reduce && 'IntersectionObserver' in window) {
      new IntersectionObserver(([w]) => {
        widac = w.isIntersecting;
        clearInterval(zegar);
        if (widac) zegar = setInterval(tik, 500);
      }).observe(sekcja);
    }
  }

  /* ——— Kalkulator ceny ———
     Pełny dzień od 5 500 zł netto; dwa dni i więcej: 15% taniej za każdy dzień;
     wejście (kilka godzin) wyceniamy indywidualnie, zawsze taniej niż pełny dzień. */
  const kalk = document.getElementById('kalkulator');
  if (kalk) {
    const DZIEN = 5500, RABAT = 0.85;
    const el = (id) => document.getElementById(id);
    const pole = { dni: el('kalkDni'), ile: el('kalkIle'), etykieta: el('kalkEtykieta'), od: el('kalkOd'), kwota: el('kalkKwota'), zl: el('kalkZl'), opis: el('kalkOpis') };
    const minus = kalk.querySelector('[data-dni="-1"]'), plus = kalk.querySelector('[data-dni="1"]');
    let dni = 2, pokazana = DZIEN, ruszony = false, anim = 0;

    const pokazKwote = (cel) => {
      cancelAnimationFrame(anim);
      if (reduce) { pole.kwota.textContent = kwota(cel); pokazana = cel; return; }
      const z = pokazana, t0 = performance.now();
      const krok = (t) => {
        const p = Math.min(1, (t - t0) / 420), e = 1 - Math.pow(1 - p, 3);
        pokazana = z + (cel - z) * e;
        pole.kwota.textContent = kwota(Math.round(pokazana / 5) * 5);
        if (p < 1) anim = requestAnimationFrame(krok); else { pokazana = cel; pole.kwota.textContent = kwota(cel); }
      };
      anim = requestAnimationFrame(krok);
    };
    const wybor = () => (kalk.querySelector('input[name=kalk_format]:checked') || {}).value || 'dzien';
    const licz = () => {
      const f = wybor();
      pole.dni.hidden = f !== 'dni';
      if (f === 'wejscie') {
        pole.etykieta.textContent = 'Wejście · kilka godzin · cena netto';
        pole.od.textContent = 'poniżej';
        pokazKwote(DZIEN);
        pole.opis.textContent = 'Kwotę podajemy po krótkiej rozmowie o programie — zawsze taniej niż pełny dzień.';
      } else if (f === 'dni') {
        const suma = dni * DZIEN * RABAT;
        pole.ile.textContent = String(dni);
        minus.disabled = dni <= 2; plus.disabled = dni >= 7;
        pole.etykieta.textContent = `${dni} dni · cena netto`;
        pole.od.textContent = 'od';
        pokazKwote(suma);
        pole.opis.textContent = `${dni} × ${kwota(DZIEN * RABAT)} zł zamiast ${dni} × ${kwota(DZIEN)} zł — oszczędzasz ${kwota(dni * DZIEN * (1 - RABAT))} zł.`;
      } else {
        pole.etykieta.textContent = 'Pełny dzień · cena netto';
        pole.od.textContent = 'od';
        pokazKwote(DZIEN);
        pole.opis.textContent = 'Ostateczna kwota zależy od lokalizacji i długości trwania.';
      }
    };
    kalk.addEventListener('change', () => { ruszony = true; licz(); });
    kalk.querySelectorAll('[data-dni]').forEach((b) => b.addEventListener('click', () => {
      ruszony = true;
      dni = Math.max(2, Math.min(7, dni + +b.dataset.dni));
      licz();
    }));
    licz();

    // Przycisk pod kalkulatorem: wybrany format trafia do opisu wydarzenia w formularzu,
    // jeśli użytkownik coś wybrał, a pole jest jeszcze puste.
    const cta = document.querySelector('#formaty [data-cta="formaty"]');
    const opis = document.getElementById('pole-message'), licznik = document.getElementById('licznik');
    if (cta && opis) cta.addEventListener('click', () => {
      if (!ruszony || opis.value.trim()) return;
      const f = wybor();
      const zl = (n) => kwota(n).replace(/\u00a0/g, ' '); // w polu tekstowym zwykła spacja
      opis.value = f === 'wejscie' ? 'Interesuje mnie krótsze wejście (kilka godzin).'
        : f === 'dni' ? `Interesuje mnie ${dni} dni (od ${zl(dni * DZIEN * RABAT)} zł netto).`
          : `Interesuje mnie pełny dzień (od ${zl(DZIEN)} zł netto).`;
      if (licznik) licznik.textContent = opis.value.length;
    });
  }
})();
