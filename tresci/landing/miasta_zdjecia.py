# -*- coding: utf-8 -*-
"""Jednorazowo: zdjęcia hero i realizacji lokalnej w źródłach stron miast.
Tylko prawdziwe kadry; podpis mówi, gdzie zrobiono zdjęcie (miasta bez własnych zdjęć
pokazują realizacje z innych miejsc, podpisane zgodnie z prawdą)."""
import json, re
from pathlib import Path
TU = Path(__file__).resolve().parent / 'strony'
S = lambda src, alt, klient, gdzie: {'src': src, 'alt': alt, 'klient': klient, 'gdzie': gdzie}
OGOLNE = [
    S('realizacja-women-in-tech-wybieg.jpg', 'Robot humanoidalny na różowym wybiegu Women in Tech Summit', 'Women in Tech Summit', 'EXPO XXI, Warszawa'),
    S('realizacja-gala-wsrod-gosci.jpg', 'Robot humanoidalny wśród gości gali', 'Drezdeńska Noc Zamków', 'Drezno'),
    S('realizacja-eco-studio-wywiad.jpg', 'Dziennikarka przeprowadza wywiad z robotem humanoidalnym przy ściance sponsorów Eco Studio', 'Finał Eco Studio ELECTRO-SYSTEM', 'Warszawa'),
    S('realizacja-przelewice-arkady.jpg', 'Robot humanoidalny w Ogrodzie Dendrologicznym w Przelewicach po zmroku', 'Ogród Dendrologiczny w Przelewicach', 'Noc Bajek'),
]
WLASNE = {
    'gdansk': [S('realizacja-lexai-starowka.jpg', 'Robot humanoidalny w koszulce LEX AI na starówce, przechodnie robią zdjęcia', 'LEX AI', 'Długi Targ, Gdańsk'),
               S('realizacja-lexai-ulica.jpg', 'Robot humanoidalny LEX AI idący ulicą starówki z teczką w dłoni', 'LEX AI', 'Główne Miasto, Gdańsk')],
    'wroclaw': [S('realizacja-yeah-gym-koszulka.jpg', 'Robot humanoidalny w koszulce klubu YEAH GYM macha na powitanie', 'YEAH GYM', 'Wrocław'),
                S('realizacja-yeah-gym-silownia.jpg', 'Robot humanoidalny w strefie treningowej klubu YEAH GYM', 'YEAH GYM', 'Wrocław'),
                S('realizacja-yeah-gym-trening.jpg', 'Robot humanoidalny obok trenerki w klubie fitness', 'YEAH GYM', 'Wrocław')],
    'szczecin': [S('realizacja-matys-silver-garden.jpg', 'Robot humanoidalny przy ściance inwestycji Silver Garden na stoisku Matys Development', 'Matys Development', 'targi nieruchomości, Szczecin'),
                 S('realizacja-matys-stoisko.jpg', 'Robot humanoidalny w koszulce Matys przy stoisku dewelopera', 'Matys Development', 'targi nieruchomości, Szczecin')],
}
FOTO_CASE = {'gdansk': ('realizacja-lexai-ulica.jpg', 'Robot humanoidalny LEX AI idący ulicą starówki z teczką w dłoni', 900, 1186)}
for f in sorted(TU.glob('robot-wynajem-*.html')):
    miasto = f.stem.replace('robot-wynajem-', '')
    if miasto == 'warszawa':
        continue
    t = f.read_text(encoding='utf-8')
    m = re.match(r'<!-- landing (\{.*?\}) -->', t, re.S)
    d = json.loads(m.group(1))
    slajdy = (WLASNE.get(miasto, []) + OGOLNE)[:6]
    d['slajdy'] = slajdy
    t = t.replace(m.group(0), '<!-- landing ' + json.dumps(d, ensure_ascii=False) + ' -->', 1)
    s = slajdy[0]
    t = t.replace('<img src="HERO.jpg" alt="HERO_ALT"', f'<img src="{s["src"]}" alt="{s["alt"]}"').replace('HERO_OPIS', f'<b>{s["klient"]}</b> · {s["gdzie"]}')
    t = t.replace('id="heroLicznik">01 / 06<', f'id="heroLicznik">01 / {len(slajdy):02d}<')
    if 'ZDJECIE.jpg' in t:
        src, alt, w, h = FOTO_CASE[miasto]
        t = t.replace('<img src="ZDJECIE.jpg" alt="ALT" loading="lazy" width="1200" height="900" />', f'<img src="{src}" alt="{alt}" loading="lazy" width="{w}" height="{h}" />')
    assert 'HERO' not in t and 'ZDJECIE' not in t, miasto
    f.write_text(t, encoding='utf-8')
    print('  ✓', miasto, len(slajdy))
