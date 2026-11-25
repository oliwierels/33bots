/* Wygenerowane przez tresci/landing/buduj.py ze skryptu w index.html. Zmiany wprowadzaj tam.
   Podstrony w układzie strony głównej: hero, pasy realizacji, szuflada, FAQ, baner cookie,
   formularz rezerwacji (Formspree) i pomiar — ten sam kod co na stronie głównej. */
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ——— Hero: rotacja zdjęć z realizacji ———
     Jeden element img: przygaszenie, podmiana źródła, rozjaśnienie. Co 3 s, od załadowania
     strony; pauza przyciskiem, najechaniem i fokusem (WCAG 2.2.2). Przy ograniczonym
     ruchu nic nie zmienia się samo — przycisk przełącza zdjęcia ręcznie. */
  const SLAJDY = (window.SLAJDY && window.SLAJDY.length) ? window.SLAJDY : [
    { src: 'realizacja-gala-wsrod-gosci.jpg', alt: 'Robot humanoidalny wśród gości gali', klient: 'Drezdeńska Noc Zamków', gdzie: 'Drezno' },
    { src: 'realizacja-eco-studio-wywiad.jpg', alt: 'Dziennikarka nagrywa wywiad z robotem humanoidalnym przy ściance sponsorów Eco Studio', klient: 'Finał Eco Studio ELECTRO-SYSTEM', gdzie: 'Warszawa' },
    { src: 'realizacja-przelewice-arkady.jpg', alt: 'Robot humanoidalny w podświetlonych arkadach podczas Nocy Bajek', klient: 'Ogród Dendrologiczny w Przelewicach', gdzie: 'Noc Bajek' },
    { src: 'realizacja-yeah-gym-koszulka.jpg', alt: 'Robot humanoidalny w koszulce klubu YEAH GYM macha na powitanie', klient: 'YEAH GYM', gdzie: 'Wrocław' },
    { src: 'realizacja-matys-silver-garden.jpg', alt: 'Robot humanoidalny przy ściance inwestycji Silver Garden na stoisku Matys Development', klient: 'Matys Development', gdzie: 'Szczecin' },
    { src: 'realizacja-szkola-kosmos-majaland.jpg', alt: 'Robot humanoidalny w fartuchu Szkoły Kosmos na rozpoczęciu roku', klient: 'Szkoła Kosmos', gdzie: 'Majaland' },
  ];
  const heroMedia = document.getElementById('heroMedia');
  // .pl: w hero jest robot 3D zamiast zdjęć — rotacja działa tylko tam, gdzie jest karta zdjęć.
  if (heroMedia) {
  const heroImg = heroMedia.querySelector('img');
  const heroLicznik = document.getElementById('heroLicznik');
  const heroOpis = document.getElementById('heroOpis');
  const heroPauza = document.getElementById('heroPauza');
  const nr = (n) => String(n).padStart(2, '0');
  let slajd = 0, zatrzymane = false, wstrzymane = false, zegar = null;

  const pokazSlajd = async (n) => {
    const s = SLAJDY[n];
    const wstepnie = new Image();
    wstepnie.src = s.src;
    try { await wstepnie.decode(); } catch (e) { /* pokaż mimo to */ }
    heroImg.classList.add('znika');
    await new Promise((r) => setTimeout(r, reduce ? 0 : 400));
    heroImg.removeAttribute('fetchpriority');
    heroImg.src = s.src; heroImg.alt = s.alt;
    heroImg.removeAttribute('width'); heroImg.removeAttribute('height');
    heroLicznik.textContent = `${nr(n + 1)} / ${nr(SLAJDY.length)}`;
    heroOpis.replaceChildren(Object.assign(document.createElement('b'), { textContent: s.klient }), ` · ${s.gdzie}`);
    heroImg.classList.remove('znika');
    slajd = n;
  };
  const nastepny = () => pokazSlajd((slajd + 1) % SLAJDY.length);
  const planuj = () => {
    clearTimeout(zegar);
    if (reduce || zatrzymane || wstrzymane || document.hidden) return;
    zegar = setTimeout(async () => { await nastepny(); planuj(); }, 3000);
  };
  heroPauza.hidden = false;
  if (reduce) {
    heroPauza.textContent = 'Następne zdjęcie';
    heroPauza.removeAttribute('aria-pressed');
    heroPauza.addEventListener('click', nastepny);
  } else {
    heroPauza.addEventListener('click', () => {
      zatrzymane = !zatrzymane;
      heroPauza.setAttribute('aria-pressed', String(zatrzymane));
      heroPauza.textContent = zatrzymane ? 'Wznów' : 'Pauza';
      planuj();
    });
    const wstrzymaj = (tak) => { wstrzymane = tak; planuj(); };
    heroMedia.addEventListener('mouseenter', () => wstrzymaj(true));
    heroMedia.addEventListener('mouseleave', () => wstrzymaj(false));
    heroMedia.addEventListener('focusin', () => wstrzymaj(true));
    heroMedia.addEventListener('focusout', () => wstrzymaj(false));
    document.addEventListener('visibilitychange', planuj);
    if (document.readyState === 'complete') planuj(); else addEventListener('load', planuj);
  }
  }

  /* ——— Hero: data wydarzenia przechodzi do formularza rezerwacji ———
     Pole w hero niczego nie wysyła. Przycisk to zwykły link do rezerwacji (działa też bez JS),
     a wybrana data trafia do pola „Data” w formularzu. Kalendarz zaczyna się od dziś. */
  const heroData = document.getElementById('heroData');
  const heroCta = document.querySelector('.hero [data-cta="hero"]');
  if (heroData && heroCta) {
    heroData.min = new Date(Date.now() - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 10);
    // Myszką kalendarz otwiera się po kliknięciu w całe pole, nie tylko w ikonę.
    if (matchMedia('(pointer: fine)').matches) {
      heroData.addEventListener('click', () => { try { heroData.showPicker(); } catch (e) { /* zwykłe pole */ } });
    }
    heroData.addEventListener('keydown', (e) => { if (e.key === 'Enter') { e.preventDefault(); heroCta.click(); } });
    // Po wyborze daty przycisk świeci mocniej (.termin--gotowe) — następny krok jest oczywisty.
    const gotowe = () => heroData.closest('.termin').classList.toggle('termin--gotowe', !!heroData.value);
    heroData.addEventListener('input', gotowe);
    heroData.addEventListener('change', gotowe);
    heroCta.addEventListener('click', () => {
      const pole = document.getElementById('pole-data');
      const nieustalona = document.getElementById('data-nieustalona');
      if (heroData.value && pole) {
        pole.value = heroData.value;
        if (nieustalona && nieustalona.checked) { nieustalona.checked = false; pole.disabled = false; }
      }
      // Po przewinięciu klawiatura zaczyna od pierwszego pytania formularza.
      const typ = document.querySelector('#formularz input[name=event_type]');
      if (typ) setTimeout(() => typ.focus({ preventScroll: true }), reduce ? 0 : 700);
    });
  }

  /* ——— Nawigacja: tło i linia włosowa po przewinięciu ——— */
  const nav = document.getElementById('nav');
  const tloNav = () => nav.classList.toggle('nav--tlo', scrollY > 8 || !panel.hidden);

  /* ——— Menu mobilne ——— */
  const przycisk = document.getElementById('navPrzycisk');
  const panel = document.getElementById('navPanel');
  const menu = (otworz) => {
    panel.hidden = !otworz;
    przycisk.setAttribute('aria-expanded', String(otworz));
    przycisk.textContent = otworz ? 'Zamknij' : 'Menu';
    tloNav();
  };
  przycisk.addEventListener('click', () => menu(panel.hidden));
  panel.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => menu(false)));
  addEventListener('keydown', (e) => { if (e.key === 'Escape' && !panel.hidden) { menu(false); przycisk.focus(); } });
  addEventListener('resize', () => { if (innerWidth >= 1024 && !panel.hidden) menu(false); });
  addEventListener('scroll', tloNav, { passive: true });
  tloNav();

  /* ——— Wejście sekcji: raz, 12 px, 700 ms ——— */
  const wejscia = document.querySelectorAll('.wejscie');
  if (reduce || !('IntersectionObserver' in window)) {
    wejscia.forEach((el) => el.classList.add('widoczne'));
  } else {
    const io = new IntersectionObserver((wpisy) => wpisy.forEach((w) => {
      if (w.isIntersecting) { w.target.classList.add('widoczne'); io.unobserve(w.target); }
    }), { rootMargin: '0px 0px -8% 0px' });
    wejscia.forEach((el) => io.observe(el));
  }

  /* ——— Pasek mobilny: po minięciu hero, ale nie przy rezerwacji ———
     Przy formularzu pasek prowadziłby tam, gdzie użytkownik już jest, i zasłaniał „Dalej”. */
  const pasek = document.getElementById('pasekMobilny');
  const hero = document.querySelector('.hero');
  const rezerwacja = document.getElementById('kontakt');
  if (pasek && hero) {
    const naEkranie = new Map();
    const obserwator = new IntersectionObserver((wpisy) => {
      wpisy.forEach((w) => naEkranie.set(w.target, w.isIntersecting));
      pasek.classList.toggle('pasek--widoczny', ![...naEkranie.values()].some(Boolean));
    }, { rootMargin: '-80px 0px 0px 0px' });
    obserwator.observe(hero);
    if (rezerwacja) obserwator.observe(rezerwacja);
  }

  /* ——— Formularz rezerwacji: niebieska poświata idzie za kursorem ———
     Tylko myszką i bez ograniczenia ruchu; poza tym poświata stoi w prawym górnym rogu karty. */
  const karta = document.querySelector('.rez .rez__form');
  if (karta && !reduce && matchMedia('(pointer: fine)').matches) {
    karta.addEventListener('pointermove', (e) => {
      const r = karta.getBoundingClientRect();
      karta.style.setProperty('--sx', `${Math.round(e.clientX - r.left)}px`);
      karta.style.setProperty('--sy', `${Math.round(e.clientY - r.top)}px`);
    });
    karta.addEventListener('pointerleave', () => { karta.style.removeProperty('--sx'); karta.style.removeProperty('--sy'); });
  }

  /* ——— Pomiar: kliknięcia w „Sprawdź termin” jako zdarzenie cta_click w GTM ——— */
  document.addEventListener('click', (e) => {
    const cta = e.target.closest('[data-cta]');
    if (!cta || !window.dataLayer) return;
    const zdarzenie = { event: 'cta_click', cta_place: cta.dataset.cta };
    if (cta === heroCta) zdarzenie.cta_date = heroData && heroData.value ? 'yes' : 'no';
    window.dataLayer.push(zdarzenie);
  });

  /* ——— Szuflada realizacji ———
     Dodatkowe zdjęcia wstawiane dopiero przy otwarciu i usuwane przy zamknięciu,
     więc każdy kadr jest w DOM najwyżej raz. */
  /* ——— Pasy bez końca: realizacje i klienci ———
     Przy ograniczonym ruchu pasy zostają zwykłymi rzędami przewijanymi ręcznie.
     W przeciwnym razie za oryginałem doklejane są kopie rzędu (aria-hidden,
     poza kolejnością Tab), a tor przesuwa się co klatkę i zawija o szerokość
     jednego kompletu — rząd nie ma końca. Najechanie i fokus wyhamowują rząd,
     przycisk zatrzymuje całą grupę (WCAG 2.2.2), rząd można też przeciągnąć
     myszą albo palcem. */
  const grupyPasow = [...document.querySelectorAll('.pasy[data-grupa]')];
  if (!reduce && grupyPasow.length) {
    const rzedy = [];
    const zawin = (r) => { if (r.fokus) { r.x = Math.min(r.x, r.margines); return; } r.x %= r.komplet; if (r.x > 0) r.x -= r.komplet; };
    const rysuj = (r) => { r.tor.style.transform = `translate3d(${r.x.toFixed(2)}px,0,0)`; };
    const zbuduj = (r) => {
      r.tor.querySelectorAll('[data-kopia]').forEach((k) => k.remove());
      const kopiuj = () => r.oryginaly.forEach((li) => {
        const k = li.cloneNode(true);
        k.dataset.kopia = ''; k.setAttribute('aria-hidden', 'true');
        k.querySelectorAll('button, a').forEach((b) => b.setAttribute('tabindex', '-1'));
        r.tor.append(k);
      });
      kopiuj();
      r.komplet = r.tor.children[r.oryginaly.length].offsetLeft - r.oryginaly[0].offsetLeft;
      const potrzeba = Math.ceil((r.pas.clientWidth + r.komplet) / r.komplet);
      for (let i = 2; i < potrzeba; i++) kopiuj();
      r.margines = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--margin')) || 20;
      zawin(r); rysuj(r);
    };

    grupyPasow.forEach((el) => {
      el.classList.add('pasy--ruch');
      const grupa = { zatrzymana: false, widoczna: true };
      const przycisk = document.querySelector(`.pasy__pauza[data-pasy="${el.dataset.grupa}"]`);
      if (przycisk) {
        przycisk.hidden = false;
        przycisk.addEventListener('click', () => {
          grupa.zatrzymana = !grupa.zatrzymana;
          przycisk.setAttribute('aria-pressed', String(grupa.zatrzymana));
          przycisk.textContent = grupa.zatrzymana ? 'Wznów ruch' : 'Zatrzymaj ruch';
        });
      }
      new IntersectionObserver(([w]) => { grupa.widoczna = w.isIntersecting; }, { rootMargin: '200px 0px' }).observe(el);

      el.querySelectorAll('.pas').forEach((pas) => {
        const tor = pas.querySelector('.pas__tor');
        const r = { pas, tor, grupa, oryginaly: [...tor.children], x: 0, v: 0, komplet: 1, margines: 20,
          predkosc: (parseFloat(pas.dataset.predkosc) || 24) * (pas.dataset.kierunek === '1' ? 1 : -1),
          najechany: false, fokus: false, ciag: null, blokujKlik: false };
        rzedy.push(r);
        zbuduj(r);

        pas.addEventListener('pointerenter', (e) => { if (e.pointerType === 'mouse') r.najechany = true; });
        pas.addEventListener('pointerleave', (e) => { if (e.pointerType === 'mouse') r.najechany = false; });
        pas.addEventListener('focusin', (e) => {
          r.fokus = true;
          const li = e.target.closest('li');
          if (!li) return;
          const a = pas.getBoundingClientRect(), b = li.getBoundingClientRect();
          if (b.left < a.left + r.margines) r.x += a.left + r.margines - b.left;
          else if (b.right > a.right - r.margines) r.x -= b.right - (a.right - r.margines);
          r.v = 0; zawin(r); rysuj(r);
        });
        pas.addEventListener('focusout', (e) => { if (!pas.contains(e.relatedTarget)) r.fokus = false; });

        // Przeciąganie: dopiero po 6 px, żeby zwykłe kliknięcie otwierało szufladę.
        pas.addEventListener('pointerdown', (e) => {
          if (e.button !== 0) return;
          r.ciag = { id: e.pointerId, x0: e.clientX, y0: e.clientY, start: r.x, aktywne: false, t: performance.now(), ostX: e.clientX, vx: 0 };
        });
        pas.addEventListener('pointermove', (e) => {
          const c = r.ciag;
          if (!c || c.id !== e.pointerId) return;
          const dx = e.clientX - c.x0, dy = e.clientY - c.y0;
          if (!c.aktywne) {
            if (Math.abs(dx) < 6) return;
            if (Math.abs(dy) > Math.abs(dx)) { r.ciag = null; return; }
            c.aktywne = true; pas.setPointerCapture(e.pointerId); pas.classList.add('pas--ciagniety');
          }
          const t = performance.now();
          c.vx = ((e.clientX - c.ostX) / Math.max(8, t - c.t)) * 1000; c.t = t; c.ostX = e.clientX;
          r.x = c.start + dx; zawin(r); c.start = r.x - dx; rysuj(r);
        });
        const puszczony = (e) => {
          const c = r.ciag;
          if (!c || c.id !== e.pointerId) return;
          if (c.aktywne) {
            r.v = Math.max(-1600, Math.min(1600, c.vx));
            r.blokujKlik = true; setTimeout(() => { r.blokujKlik = false; }, 0);
            pas.classList.remove('pas--ciagniety');
          }
          r.ciag = null;
        };
        pas.addEventListener('pointerup', puszczony);
        pas.addEventListener('pointercancel', puszczony);
        pas.addEventListener('click', (e) => { if (r.blokujKlik) { e.preventDefault(); e.stopPropagation(); } }, true);
      });
    });

    let ostatnia = 0;
    const klatka = (t) => {
      const dt = Math.min(0.05, ostatnia ? (t - ostatnia) / 1000 : 0);
      ostatnia = t;
      for (const r of rzedy) {
        if (!r.grupa.widoczna || r.ciag?.aktywne) continue;
        const cel = r.grupa.zatrzymana || r.najechany || r.fokus ? 0 : r.predkosc;
        r.v += (cel - r.v) * (1 - Math.exp(-dt * (cel === 0 ? 6 : 2.5)));
        if (cel === 0 && Math.abs(r.v) < 0.05) r.v = 0;
        if (r.v === 0) continue;
        r.x += r.v * dt; zawin(r); rysuj(r);
      }
      requestAnimationFrame(klatka);
    };
    requestAnimationFrame(klatka);

    let czekaj = 0;
    addEventListener('resize', () => { clearTimeout(czekaj); czekaj = setTimeout(() => rzedy.forEach(zbuduj), 150); });
    addEventListener('load', () => rzedy.forEach(zbuduj));
  }

  const REALIZACJE = {
    "eco-studio": {
      "klient": "ELECTRO-SYSTEM · Eco Studio",
      "podpis": "Finał 7. sezonu · Warszawa · 2026",
      "liczby": [
        [
          "15.09.2026",
          "finał 7. sezonu"
        ],
        [
          "Eko Partner 2026",
          "tytuł od organizatora"
        ],
        [
          "TVP2",
          "„Pytanie na śniadanie”"
        ]
      ],
      "opis": "Robot był jedną z atrakcji finału, obok koncertów i części oficjalnej. Pracował na scenie z prowadzącymi i finalistami oraz przy ściance sponsorów, gdzie nagrano z nim wywiad.",
      "link": "case-study-eco-studio-electro-system.html",
      "zdjecia": []
    },
    "women-in-tech": {
      "klient": "Women in Tech Summit",
      "podpis": "EXPO XXI · Warszawa · 2026",
      "liczby": [
        [
          "~14 000",
          "uczestniczek i uczestników"
        ],
        [
          "10–11.06.2026",
          "EXPO XXI, Warszawa"
        ]
      ],
      "opis": "Największa konferencja women-in-tech w Europie. Robot pracował na wybiegu i wśród uczestniczek.",
      "link": "case-study-women-in-tech.html",
      "zdjecia": []
    },
    "lexai": {
      "klient": "LEX AI",
      "podpis": "Długi Targ · Gdańsk",
      "liczby": [
        [
          "Teleexpress",
          "materiał w TVP"
        ],
        [
          "TVP Gdańsk",
          "reportaż o aplikacji LEX AI"
        ]
      ],
      "opis": "Robot stanął przy fontannie Neptuna w roli symbolu aplikacji — witał przechodniów, podawał rękę, pozował do zdjęć i odpowiadał na pytania.",
      "link": "case-study-lexai.html",
      "zdjecia": []
    },
    "grupa-rekord": {
      "klient": "Grupa Rekord",
      "podpis": "MSPO · Targi Kielce · 2026",
      "liczby": [
        [
          "8–9 września",
          "dwa dni targów"
        ],
        [
          "3Z-05",
          "stoisko w Hali RFS"
        ]
      ],
      "opis": "Robot przedstawiał po kolei wszystkie spółki grupy i zapraszał przechodzących korytarzem na stoiskowy pokaz medycyny pola walki.",
      "link": "case-study-grupa-rekord-mspo.html",
      "zdjecia": []
    },
    "kopernik": {
      "klient": "Centrum Nauki Kopernik",
      "podpis": "„O czym śnią roboty” · Warszawa",
      "liczby": [
        [
          "17 września",
          "wieczór tylko dla dorosłych"
        ],
        [
          "19:00–22:00",
          "trzy godziny pracy"
        ]
      ],
      "opis": "Robot stał przy Fontannie powietrznej, rozmawiał ze zwiedzającymi i pozował do zdjęć.",
      "link": "case-study-centrum-nauki-kopernik.html",
      "zdjecia": []
    },
    "przelewice": {
      "klient": "Ogród Dendrologiczny w Przelewicach",
      "podpis": "Noc Bajek Pokolenia",
      "liczby": [
        [
          "12 września",
          "Noc Bajek Pokolenia"
        ],
        [
          "Mauzoleum",
          "stanowisko po zmroku"
        ]
      ],
      "opis": "Robot pracował po zmroku przy Mauzoleum rodziny von Prillwitz, w świetle reflektorów ustawionych na arkadach.",
      "link": "case-study-ogrod-przelewice.html",
      "zdjecia": []
    },
    "drezno": {
      "klient": "Drezdeńska Noc Zamków",
      "podpis": "Drezno · Niemcy",
      "liczby": [],
      "opis": "Robot w cekinowym smokingu i koronie na balu w drezdeńskim pałacu — na czerwonym dywanie, w sali balowej i wśród gości.",
      "link": null,
      "zdjecia": []
    },
    "gonia-auto": {
      "klient": "Gonia Auto",
      "podpis": "salon samochodowy",
      "liczby": [],
      "opis": "Robot w firmowej czerwieni przed salonem Gonia Auto.",
      "link": null,
      "zdjecia": []
    },
    "loza": {
      "klient": "Loża Przedsiębiorców",
      "podpis": "Mikołajki",
      "liczby": [],
      "opis": "Robot w koszulce Loży Przedsiębiorców na spotkaniu w Mikołajkach.",
      "link": "robot-wynajem-mikolajki.html",
      "zdjecia": []
    },
    "dream-med": {
      "klient": "Dream-Med",
      "podpis": "Warsaw Medical Expo · 2026",
      "liczby": [],
      "opis": "Robot na stoisku Dream-Med podczas Warsaw Medical Expo 2026.",
      "link": null,
      "zdjecia": []
    },
    "matys": {
      "klient": "Matys Development",
      "podpis": "targi nieruchomości · Szczecin",
      "liczby": [],
      "opis": "Robot na stoisku Matys Development podczas targów nieruchomości w Szczecinie, z materiałami inwestycji Silver Garden.",
      "link": null,
      "zdjecia": []
    },
    "szkola-kosmos": {
      "klient": "Szkoła Kosmos",
      "podpis": "rozpoczęcie roku · Majaland",
      "liczby": [],
      "opis": "Robot w fartuchu Szkoły Kosmos na rozpoczęciu roku szkolnego w Majalandzie.",
      "link": null,
      "zdjecia": []
    },
    "yeah-gym": {
      "klient": "YEAH GYM",
      "podpis": "klub fitness · Wrocław",
      "liczby": [],
      "opis": "Robot w koszulce klubu YEAH GYM na sali treningowej we Wrocławiu.",
      "link": null,
      "zdjecia": []
    },
    "jednorozec": {
      "klient": "Gmina Jednorożec",
      "podpis": "Parada Jednorożców",
      "liczby": [],
      "opis": "Robot w koszulce gminy na Paradzie Jednorożców, w plenerze do zmroku.",
      "link": null,
      "zdjecia": []
    },
    "tet-trung-thu": {
      "klient": "Tết Trung Thu",
      "podpis": "Święto Środka Jesieni",
      "liczby": [],
      "opis": "Robot w galowej oprawie wśród gości Święta Środka Jesieni.",
      "link": null,
      "zdjecia": []
    },
    "wesele": {
      "klient": "Wesele",
      "podpis": "przyjęcie weselne",
      "liczby": [],
      "opis": "Robot na parkiecie podczas wieczornej części przyjęcia weselnego.",
      "link": null,
      "zdjecia": []
    }
  };
  const szuflada = document.getElementById('szuflada');
  const tlo = document.getElementById('szufladaTlo');
  const el = (id) => document.getElementById(id);
  const zamknij = el('szufladaZamknij');
  let powrot = null;

  const otworz = (klucz, zrodlo) => {
    const d = REALIZACJE[klucz];
    if (!d) return;
    powrot = zrodlo;
    el('szufladaPodpis').textContent = d.podpis;
    el('szufladaTytul').textContent = d.klient;
    el('szufladaOpis').textContent = d.opis;
    const liczby = el('szufladaLiczby');
    liczby.replaceChildren();
    liczby.hidden = !d.liczby.length;
    d.liczby.forEach(([a, b]) => {
      const w = document.createElement('div');
      const dt = document.createElement('dt'); dt.textContent = a;
      const dd = document.createElement('dd'); dd.textContent = b;
      w.append(dt, dd); liczby.append(w);
    });
    const zdjecia = el('szufladaZdjecia');
    zdjecia.replaceChildren();
    zdjecia.hidden = !d.zdjecia.length;
    d.zdjecia.forEach((z) => {
      const pic = document.createElement('picture');
      const src = document.createElement('source');
      src.type = 'image/webp'; src.srcset = `${z.plik}-400.webp 400w, ${z.plik}.webp ${z.w}w`; src.sizes = '(max-width: 767px) 100vw, 480px';
      const img = document.createElement('img');
      img.src = `${z.plik}.jpg`; img.alt = z.alt; img.width = z.w; img.height = z.h; img.decoding = 'async';
      pic.append(src, img); zdjecia.append(pic);
    });
    const link = el('szufladaLink');
    link.parentElement.hidden = !d.link;
    if (d.link) link.href = d.link;
    tlo.hidden = false; szuflada.hidden = false;
    document.body.style.overflow = 'hidden';
    zamknij.focus();
  };
  const zamknijSzuflade = () => {
    if (szuflada.hidden) return;
    szuflada.hidden = true; tlo.hidden = true;
    el('szufladaZdjecia').replaceChildren();
    document.body.style.overflow = '';
    if (powrot) powrot.focus();
  };
  document.addEventListener('click', (e) => {
    const b = e.target.closest('[data-cs]');
    if (b) otworz(b.dataset.cs, b);
  });
  zamknij.addEventListener('click', zamknijSzuflade);
  tlo.addEventListener('click', zamknijSzuflade);
  addEventListener('keydown', (e) => {
    if (szuflada.hidden) return;
    if (e.key === 'Escape') { zamknijSzuflade(); return; }
    if (e.key !== 'Tab') return;
    // Fokus zostaje w szufladzie, dopóki jest otwarta.
    const f = [...szuflada.querySelectorAll('a[href], button')].filter((x) => x.offsetParent !== null);
    if (!f.length) return;
    if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
    else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
  });

  /* ——— FAQ: akordeon ——— */
  document.querySelectorAll('.faq__q').forEach((q) => q.addEventListener('click', () => {
    const otwarte = q.getAttribute('aria-expanded') === 'true';
    q.setAttribute('aria-expanded', String(!otwarte));
    document.getElementById(q.getAttribute('aria-controls')).hidden = otwarte;
  }));

  /* ——— Baner cookie ———
     Zgody zbiera ConsentBoard (baner ładowany przez GTM). Nasz baner informacyjny znika,
     gdy tylko skrypt ConsentBoard pojawi się na stronie, i w tej przeglądarce nie pokazuje
     się więcej, dopóki ConsentBoard się ładuje. Bez ConsentBoard działa jak dawniej. */
  const ciasteczka = document.getElementById('cookies');
  const pokazBaner = () => { if (!localStorage.getItem('33bots-cookies')) ciasteczka.classList.add('show'); };
  const skryptCmp = (n) => n.nodeName === 'SCRIPT' && /^https:\/\/([^/]+\.)?consentboard\.[a-z]+\//i.test(n.src);
  const cmpJest = () => Array.from(document.scripts).some(skryptCmp);
  const cmpZastepuje = () => { localStorage.setItem('33bots-cmp', '1'); ciasteczka.remove(); };
  if (cmpJest()) cmpZastepuje();
  else {
    new MutationObserver((zmiany, obs) => {
      if (zmiany.some((z) => Array.from(z.addedNodes).some(skryptCmp))) { obs.disconnect(); cmpZastepuje(); }
    }).observe(document.documentElement, { childList: true, subtree: true });
    if (localStorage.getItem('33bots-cmp')) {
      // ConsentBoard był tu wcześniej, ale 8 s po wejściu wciąż go nie ma: wracamy do naszego banera.
      setTimeout(() => { if (!cmpJest()) { localStorage.removeItem('33bots-cmp'); pokazBaner(); } }, 8000);
    } else {
      setTimeout(pokazBaner, 1400);
    }
  }
  document.getElementById('cookiesOk').addEventListener('click', () => {
    localStorage.setItem('33bots-cookies', '1');
    ciasteczka.classList.remove('show');
  });

  /* ——— Formularz: krok 1 wydarzenie, krok 2 kontakt, wysyłka na Formspree ——— */
  const form = document.getElementById('formularz');
  const krok1 = el('krok1'), krok2 = el('krok2');
  const etykiety = form.querySelectorAll('[data-krok-etykieta]');
  const pokazKrok = (n) => {
    krok1.hidden = n !== 1; krok2.hidden = n !== 2;
    etykiety.forEach((e) => { if (e.dataset.krokEtykieta === String(n)) e.setAttribute('aria-current', 'step'); else e.removeAttribute('aria-current'); });
    (n === 2 ? el('pole-name') : form.querySelector('input[name=event_type]')).focus();
  };
  const dataPole = el('pole-data'), nieustalona = el('data-nieustalona');
  dataPole.min = new Date(Date.now() - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 10);
  nieustalona.addEventListener('change', () => { dataPole.disabled = nieustalona.checked; if (nieustalona.checked) dataPole.value = ''; });

  const poleTyp = el('pole-typ'), bladTyp = el('blad-typ');
  form.querySelectorAll('input[name=event_type]').forEach((r) => r.addEventListener('change', () => {
    bladTyp.hidden = true; poleTyp.removeAttribute('data-blad');
  }));
  el('dalej').addEventListener('click', () => {
    const typ = form.querySelector('input[name=event_type]:checked');
    bladTyp.hidden = !!typ;
    poleTyp.toggleAttribute('data-blad', !typ);
    if (!typ) { form.querySelector('input[name=event_type]').focus(); return; }
    pokazKrok(2);
  });
  el('wstecz').addEventListener('click', () => pokazKrok(1));

  const opis = el('pole-message'), licznik = el('licznik');
  opis.addEventListener('input', () => { licznik.textContent = opis.value.length; });

  const sprawdz = (pole, ok) => {
    const box = pole.closest('.pole');
    box.toggleAttribute('data-blad', !ok);
    box.querySelector('.pole__blad').hidden = ok;
    pole.setAttribute('aria-invalid', String(!ok));
    return ok;
  };
  const imie = el('pole-name'), mail = el('pole-email');
  imie.addEventListener('input', () => { if (imie.hasAttribute('aria-invalid')) sprawdz(imie, imie.value.trim().length > 1); });
  mail.addEventListener('input', () => { if (mail.hasAttribute('aria-invalid')) sprawdz(mail, /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(mail.value.trim())); });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const okImie = sprawdz(imie, imie.value.trim().length > 1);
    const okMail = sprawdz(mail, /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(mail.value.trim()));
    if (!okImie || !okMail) { (okImie ? mail : imie).focus(); return; }

    const d = new FormData(form);
    const payload = {
      name:       d.get('name').trim(),
      company:    d.get('company')    || '—',
      email:      d.get('email').trim(),
      phone:      d.get('phone')      || '—',
      date:       nieustalona.checked ? 'nieustalony' : (d.get('date') || '—'),
      location:   d.get('location')   || '—',
      message:    d.get('message')    || '—',
      event_type: d.get('event_type') || '—',
      guests:     d.get('guests')     || '—',
    };

    const btn = el('wyslij');
    const pierwotny = btn.innerHTML;
    btn.disabled = true; btn.textContent = 'Wysyłanie…';
    const blad = el('blad-wysylki');
    blad.hidden = true;
    try {
      const res = await fetch('https://formspree.io/f/mnjwvray', {
        method: 'POST',
        headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      // Pomiar: wysłane zgłoszenie jako zdarzenie generate_lead w GTM (tag konwersji dodaje się w GTM).
      if (window.dataLayer) window.dataLayer.push({ event: 'generate_lead', form_id: 'formularz', event_type: payload.event_type });
      // Google Ads: konwersja formularza (etykieta od agencji) — tylko .pl, tag AW jest w <head> tej strony.
      if (typeof gtag === 'function' && document.documentElement.lang === 'pl') {
        gtag('event', 'conversion', { send_to: 'AW-18167851767/BdKnCOr2uqQdEPfVjddD' });
      }
      const sukces = document.createElement('div');
      sukces.className = 'form-sukces';
      sukces.setAttribute('role', 'status');
      const t = document.createElement('p'); t.className = 'h3'; t.textContent = 'Mamy Twoje zgłoszenie.';
      const p = document.createElement('p'); p.className = 'body';
      p.append('Odezwiemy się na ', Object.assign(document.createElement('strong'), { textContent: payload.email }),
        '. Odpowiadamy zwykle w ciągu 30 minut. Wycenę od razu podamy przez telefon: +48 531 408 004.');
      sukces.append(t, p);
      form.replaceChildren(sukces);
    } catch (err) {
      blad.textContent = 'Nie udało się wysłać. Zadzwoń: +48 531 408 004 albo napisz na kontakt@33bots.pl.';
      blad.hidden = false;
      btn.disabled = false; btn.innerHTML = pierwotny;
    }
  });
})();
