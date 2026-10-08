# -*- coding: utf-8 -*-
"""Podstrony rynków zagranicznych: te same porządki wizualne co na podstronach .pl.

Strona główna każdego rynku powstaje z buduj_glowna.py. Tutaj podstrony
dostają to, co podstrony .pl dostały przy przebudowie:

33bots.de (podstrony na style.css, jak większość podstron .pl):
  • style.css z repozytorium PL — kroje Space Grotesk i Plus Jakarta Sans
    lokalnie, bez ziarna, poświaty, skanowania i pływania robota,
  • main.js z repozytorium PL (bez efektów kursora i paska postępu, odporny
    na strony bez menu, FAQ czy formularza) z niemieckimi tekstami,
  • usunięte warstwy efektów (#cursorGlow, #scrollProgress) i zbędny krój Inter,
  • numery wersji arkuszy i skryptów z sumy kontrolnej — przeglądarka nie poda
    starego main.js, który bez tych warstw przerywałby się na błędzie,
  • robot mówi po niemiecku i w każdym innym języku (zdania o samej mowie).

33bots.at (podstrony na Tailwindzie, jak sklep i wdrożenia na .pl):
  • konfiguracja Tailwinda jak na .pl: krój Plus Jakarta Sans, bez animacji
    zorzy, pływania, migotania i pulsowania,
  • kroje pisma lokalnie zamiast z Google Fonts,
  • przebudowany assets-redesign.css i jego numer wersji.

Skrypt można uruchamiać wielokrotnie — każda zmiana jest idempotentna.

Użycie (z katalogu głównego repozytorium 33bots.pl):
  python3 tresci/zagranica/podstrony.py de ../33bots-de
  python3 tresci/zagranica/podstrony.py at ../strona-austria
"""
import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

PL = Path(__file__).resolve().parent.parent.parent


def md5(plik):
    return hashlib.md5(Path(plik).read_bytes()).hexdigest()[:8]


def zamien(tekst, stare, nowe, nazwa):
    n = tekst.count(stare)
    assert n == 1, f'{nazwa}: „{stare[:60]}” występuje {n}×, oczekiwano 1'
    return tekst.replace(stare, nowe)


# ——— 33bots.de ———

def main_js_de():
    """main.js z .pl z niemieckimi tekstami; 33bots.de nie ma banera cookie."""
    s = (PL / 'main.js').read_text(encoding='utf-8')
    for stare, nowe in [
        ("hamburger.setAttribute('aria-label', open ? 'Zamknij menu' : 'Menu');",
         "hamburger.setAttribute('aria-label', open ? 'Menü schließen' : 'Menü öffnen');"),
        ("const errorMsg = { valueMissing: 'To pole jest wymagane', typeMismatch: 'Nieprawidłowy format' };",
         "const errorMsg = { valueMissing: 'Dieses Feld ist erforderlich', typeMismatch: 'Ungültiges Format' };"),
        (": 'Sprawdź to pole';", ": 'Bitte prüfen Sie dieses Feld';"),
        ("btn.textContent = 'Wysyłanie...';", "btn.textContent = 'Wird gesendet …';"),
        ("event_label: 'Formularz kontaktowy',", "event_label: 'Kontaktformular',"),
        ("""        <h3>Wiadomość wysłana</h3>
        <p>Odezwiemy się na <strong>${payload.email}</strong><br>w ciągu 24 godzin roboczych.</p>""",
         """        <h3>Nachricht gesendet</h3>
        <p>Wir melden uns an <strong>${payload.email}</strong><br>innerhalb von 24 Werkstunden.</p>"""),
        ("btn.textContent = 'Spróbuj ponownie';", "btn.textContent = 'Erneut versuchen';"),
        ("errEl.textContent = 'Coś poszło nie tak. Napisz bezpośrednio na kontakt@33bots.pl';",
         "errEl.textContent = 'Etwas ist schiefgelaufen. Schreiben Sie uns direkt an kontakt@33bots.de';"),
    ]:
        s = zamien(s, stare, nowe, 'main.js')
    baner = re.search(r'// ── COOKIE BANNER ─+\n.*?\n}\n', s, re.S)
    assert baner, 'main.js: nie znaleziono banera cookie'
    s = s.replace(baner.group(0), """// ── COOKIE-HINWEIS ────────────────────────────────────────────
// 33bots.de bindet keine Analyse-Dienste ein, daher gibt es keinen
// Cookie-Banner (§ 25 TDDDG): Es werden nur technisch notwendige Daten genutzt.
""")
    polskie = re.findall(r"'[^'\n]*[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ][^'\n]*'", re.sub(r'//[^\n]*', '', s))
    assert not polskie, f'main.js: zostały polskie teksty: {polskie}'
    return s


JEZYK_DE = [
    ('spricht dank KI-Integration Deutsch.', 'spricht dank KI-Integration Deutsch und jede andere Sprache.'),
    ('der läuft, tanzt, gestikuliert und dank KI Deutsch spricht.', 'der läuft, tanzt, gestikuliert und dank KI Deutsch und jede andere Sprache spricht.'),
    ('<h3 class="tile__title">Er spricht Deutsch</h3>', '<h3 class="tile__title">Er spricht Deutsch und jede andere Sprache</h3>'),
]

# Odstępy tekstu od ramek (reguła 24/32 px), jak poprawki na podstronach .pl:
# przycisk w ramce poradnika łamie się na telefonie — wtedy ma 24 px z góry i z dołu
# (to samo rozwiązanie co na blog-robot-z-ai-rozmawiajacy-po-polsku.html),
# a najdłuższy link w ramce „Suchen Sie etwas anderes?” może przejść do nowej linii.
ODSTEPY_DE = [
    ('class="btn-cta" style="display:inline-flex;">Kostenloses Angebot anfordern →',
     'class="btn-cta" style="display:inline-flex; padding:clamp(16px, calc(40px - 2vw), 24px) var(--s4); line-height:1.4;">Kostenloses Angebot anfordern →'),
    ('white-space:nowrap;">Roboter für den Junggesellinnenabschied →', '">Roboter für den Junggesellinnenabschied →'),
]

KOMENTARZ_INTER = """  <!-- Keine Verbindungen zu Dritten vor der Einwilligung: Analyse-Tags sind
       consent-gated, die Schrift Inter wird lokal ausgeliefert. -->
  <link rel="stylesheet" href="fonts/inter.css" />
"""
KOMENTARZ_FONTY = """  <!-- Schriften (Space Grotesk, Plus Jakarta Sans) lokal über style.css —
       keine Verbindungen zu Dritten. -->
"""
EFEKTY = ['  <div class="cursor-glow" id="cursorGlow" aria-hidden="true"></div>\n',
          '  <div class="scroll-progress" id="scrollProgress" aria-hidden="true"></div>\n']


def podstrony_de(cel):
    shutil.copy2(PL / 'style.css', cel / 'style.css')
    (cel / 'main.js').write_text(main_js_de(), encoding='utf-8')
    wersje = {p: md5(cel / p) for p in ('style.css', 'main.js', 'a11y.css', 'a11y.js', 'gallery.css')}
    zmienione = 0
    for strona in sorted(cel.glob('*.html')):
        if strona.name == 'index.html':
            continue      # strona główna z buduj_glowna.py
        s = stary = strona.read_text(encoding='utf-8')
        for efekt in EFEKTY:
            s = s.replace(efekt, '')
        s = s.replace(KOMENTARZ_INTER, KOMENTARZ_FONTY)
        for stare, nowe in JEZYK_DE + ODSTEPY_DE:
            s = s.replace(stare, nowe)
        s = re.sub(r'(href|src)="(style\.css|main\.js|a11y\.css|a11y\.js|gallery\.css)(\?v=[^"]*)?"',
                   lambda m: f'{m.group(1)}="{m.group(2)}?v={wersje[m.group(2)]}"', s)
        assert 'cursorGlow' not in s and 'fonts/inter.css' not in s, f'{strona.name}: zostały efekty albo Inter'
        if s != stary:
            strona.write_text(s, encoding='utf-8')
            zmienione += 1
    return zmienione


# ——— 33bots.at ———

def klasy_at(tekst):
    """Odstępy jak na podstronach Tailwinda na .pl: tekst co najmniej 24 px od ramki
    lub krawędzi tła na telefonie i 32 px od 768 px; przyciski w jednej linii."""
    def popraw(m):
        k = m.group(1).split()
        z = set(k)

        def podmien(stare, nowe):
            return [nowe if t == stare else t for t in k]

        if {'cta-shine', 'px-9', 'py-5', 'text-base', 'tracking-wider'} <= z:        # przycisk główny
            for a, b in (('px-9', 'px-5'), ('py-5', 'py-4'), ('text-base', 'text-sm'), ('tracking-wider', 'tracking-normal')):
                k = podmien(a, b)
            k += ['sm:px-9', 'sm:text-base', 'sm:tracking-wider']
        elif {'border-line-hi', 'rounded-2xl'} <= z and z & {'py-4.5', 'py-5'}:     # przycisk z ramką
            k = podmien('py-4.5', 'py-4')
            k = podmien('py-5', 'py-4')
        elif {'rounded-[28px]', 'p-7'} <= z:                                         # karty
            i = k.index('p-7')
            k = k[:i] + ['p-6', 'md:p-8'] + k[i + 1:]
        elif {'absolute', 'bottom-0', 'px-4', 'pb-3', 'pt-8'} <= z:                  # podpis na zdjęciu
            k = [t for t in k if t not in ('px-4', 'pb-3', 'pt-8')] + ['px-6', 'pb-6', 'pt-10', 'md:px-8', 'md:pb-8']
        elif {'faq-btn', 'py-5'} <= z:                                                # pytanie FAQ
            i = k.index('py-5')
            k = k[:i] + ['py-6', 'md:py-8'] + k[i + 1:]
        elif {'pb-5', 'text-[14px]', 'leading-relaxed'} <= z:                         # odpowiedź FAQ
            i = k.index('pb-5')
            k = k[:i] + ['pb-6', 'md:pb-8'] + k[i + 1:]
        elif {'reveal', 'mb-6', 'inline-flex', 'rounded-full', 'backdrop-blur'} <= z:  # nadtytuł bez pigułki
            k = [t for t in k if t not in ('rounded-full', 'border', 'border-line-mid', 'bg-white/[.03]', 'px-4', 'py-2', 'backdrop-blur')]
        return f'class="{" ".join(k)}"'
    return re.sub(r'class="([^"]*)"', popraw, tekst)


BANER_STARE = 'max-width: 640px; margin: 0 auto; padding: 1rem 1.25rem;'
BANER_NOWE = 'max-width: 640px; margin: 0 auto; padding: 24px;'
BANER_DESKTOP = '  @media (min-width: 768px) { .cookies { padding: 32px; } }\n'


def podstrony_at(cel):
    # Konfiguracja Tailwinda jak na .pl; zakres treści zostaje własny (wszystkie strony).
    konf = (PL / 'tailwind.config.js').read_text(encoding='utf-8')
    konf = re.sub(r"content: \[[^\]]*\]", "content: ['./*.html']", konf, count=1)
    (cel / 'tailwind.config.js').write_text(konf, encoding='utf-8')
    shutil.copy2(PL / 'tw-input.css', cel / 'tw-input.css')
    # Najpierw klasy na stronach, potem arkusz — Tailwind bierze klasy ze stron.
    for strona in sorted(cel.glob('*.html')):
        if strona.name == 'index.html':
            continue
        t = stary = strona.read_text(encoding='utf-8')
        t = klasy_at(t).replace(BANER_STARE, BANER_NOWE)
        # Cena w ramce: przy line-height 36 px glif 30 px wystaje 2 px ponad wiersz (jak „od 100 000 zł” na .pl).
        t = t.replace('<p class="font-display text-3xl font-700 text-white">', '<p class="font-display text-3xl font-700 leading-normal text-white">')
        if '.cookies { padding: 32px; }' not in t and '  .cookies.show { transform: none; }\n' in t:
            t = t.replace('  .cookies.show { transform: none; }\n', '  .cookies.show { transform: none; }\n' + BANER_DESKTOP, 1)
        if t != stary:
            strona.write_text(t, encoding='utf-8')
    subprocess.run(['npx', '--yes', 'tailwindcss@3.4.17', '-c', 'tailwind.config.js', '-i', 'tw-input.css',
                    '-o', 'assets-redesign.css', '--minify'], cwd=cel, check=True, capture_output=True)
    # Kroje pisma lokalnie (te same pliki co strona główna, w css/site.css).
    fonty = (PL / 'style.css').read_text(encoding='utf-8')
    fonty = fonty[:fonty.index('/* ===== TOKENS ===== */')].strip() + '\n'
    (cel / 'css').mkdir(exist_ok=True)
    (cel / 'css' / 'fonty.css').write_text(fonty.replace('url("fonts/', 'url("../fonts/'), encoding='utf-8')
    wersje = {'assets-redesign.css': md5(cel / 'assets-redesign.css'), 'css/fonty.css': md5(cel / 'css' / 'fonty.css')}
    google = re.compile(r'<link rel="preconnect" href="https://fonts\.googleapis\.com" />\n'
                        r'<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin />\n'
                        r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?[^"]*" />\n')
    zmienione = 0
    for strona in sorted(cel.glob('*.html')):
        if strona.name == 'index.html':
            continue
        s = stary = strona.read_text(encoding='utf-8')
        s = google.sub(f'<link rel="stylesheet" href="css/fonty.css?v={wersje["css/fonty.css"]}" />\n', s)
        s = re.sub(r'href="css/fonty\.css(\?v=[^"]*)?"', f'href="css/fonty.css?v={wersje["css/fonty.css"]}"', s)
        s = re.sub(r'href="assets-redesign\.css(\?v=[^"]*)?"', f'href="assets-redesign.css?v={wersje["assets-redesign.css"]}"', s)
        assert 'fonts.googleapis.com/css2' not in s, f'{strona.name}: został Google Fonts'
        if s != stary:
            strona.write_text(s, encoding='utf-8')
            zmienione += 1
    return zmienione


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ('de', 'at'):
        raise SystemExit(f'Użycie: python3 {sys.argv[0]} de|at <katalog repozytorium rynku>')
    cel = Path(sys.argv[2]).resolve()
    n = podstrony_de(cel) if sys.argv[1] == 'de' else podstrony_at(cel)
    print(f'{cel}: zmienione podstrony: {n}')


if __name__ == '__main__':
    main()
