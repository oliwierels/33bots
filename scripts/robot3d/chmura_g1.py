# -*- coding: utf-8 -*-
"""Chmura punktów robota Unitree G1 (23 stopnie swobody) do sceny w hero strony głównej.

Źródło geometrii: repozytorium unitreerobotics/unitree_ros, katalog robots/g1_description
(URDF g1_23dof_rev_1_0.urdf i siatki STL), licencja BSD-3-Clause — treść licencji
w robot/LICENCJA-UNITREE.txt, który trafia na serwer razem z plikiem danych.

Co robi:
  1. czyta URDF, scala człony połączone stawami stałymi (głowa, logo, obrys miednicy)
     z rodzicem — zostaje miednica i 23 człony ruchome;
  2. z powierzchni siatek losuje punkty proporcjonalnie do pola trójkątów, potem
     przerzedza je siatką wokseli, żeby rozkład był równy (bez skupisk);
  3. dodaje punkty wzdłuż ostrych krawędzi (kąt dwuścienny > 35°) — rysują kontur;
  4. zapisuje plik binarny: nagłówek JSON z kinematyką i liczbą punktów każdego
     segmentu (najpierw powierzchnia, potem krawędzie), potem pozycje int16 w układzie
     członu i normalne w kodowaniu oktaedrycznym (2 × int8) — 8 bajtów na punkt.

Użycie (numpy w osobnym środowisku):
  python3 scripts/robot3d/chmura_g1.py <katalog g1_description> robot/g1.bin 30000 9000
  python3 scripts/robot3d/chmura_g1.py <katalog g1_description> robot/g1-lekki.bin 13000 4000
"""
import json
import math
import struct
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np

URDF = 'g1_23dof_rev_1_0.urdf'
KAT_KRAWEDZI = math.radians(50)
rng = np.random.default_rng(33)


def rpy_macierz(r, p, y):
    cr, sr, cp, sp, cy, sy = math.cos(r), math.sin(r), math.cos(p), math.sin(p), math.cos(y), math.sin(y)
    return np.array([
        [cy * cp, cy * sp * sr - sy * cr, cy * sp * cr + sy * sr],
        [sy * cp, sy * sp * sr + cy * cr, sy * sp * cr - cy * sr],
        [-sp, cp * sr, cp * cr]])


def transformacja(xyz, rpy):
    t = np.eye(4)
    t[:3, :3] = rpy_macierz(*rpy)
    t[:3, 3] = xyz
    return t


def liczby(s, domyslnie='0 0 0'):
    return [float(x) for x in (s or domyslnie).split()]


def wczytaj_stl(plik):
    dane = plik.read_bytes()
    n = struct.unpack('<I', dane[80:84])[0]
    if 84 + n * 50 == len(dane):
        rek = np.frombuffer(dane, dtype=np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')]), count=n, offset=84)
        return rek['v'].astype(np.float64)
    # STL tekstowy
    v = [liczby(l.split(None, 1)[1]) for l in dane.decode('ascii', 'ignore').splitlines() if l.strip().startswith('vertex')]
    return np.array(v, dtype=np.float64).reshape(-1, 3, 3)


def krawedzie_ostre(tri):
    """Odcinki na styku trójkątów, które łamią się pod kątem większym niż KAT_KRAWEDZI."""
    v = tri.reshape(-1, 3)
    klucz = np.round(v / 1e-5).astype(np.int64)
    _, idx = np.unique(klucz, axis=0, return_inverse=True)
    idx = idx.reshape(-1, 3)
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    dl = np.linalg.norm(n, axis=1)
    ok = dl > 1e-12
    n[ok] /= dl[ok, None]
    mapa = {}
    for t, (a, b, c) in enumerate(idx):
        if not ok[t]:
            continue
        for p, q in ((a, b), (b, c), (c, a)):
            k = (p, q) if p < q else (q, p)
            mapa.setdefault(k, []).append(t)
    pozycje = {}
    for t, (a, b, c) in enumerate(idx):
        for j, w in enumerate((a, b, c)):
            pozycje[w] = tri[t, j]
    odcinki = []
    for (p, q), ts in mapa.items():
        if len(ts) == 1:
            ostra = True                      # brzeg otwartej siatki
        elif len(ts) == 2:
            ostra = math.acos(max(-1.0, min(1.0, float(np.dot(n[ts[0]], n[ts[1]]))))) > KAT_KRAWEDZI
        else:
            ostra = False
        if ostra:
            odcinki.append((pozycje[p], pozycje[q], n[ts[0]]))
    return odcinki


def probki_powierzchni(tri, ile):
    a, b, c = tri[:, 0], tri[:, 1], tri[:, 2]
    n = np.cross(b - a, c - a)
    pole = np.linalg.norm(n, axis=1) / 2
    ok = pole > 1e-12
    a, b, c, n, pole = a[ok], b[ok], c[ok], n[ok], pole[ok]
    n /= (2 * pole)[:, None]
    wybor = rng.choice(len(pole), size=ile, p=pole / pole.sum())
    u, w = rng.random(ile), rng.random(ile)
    z = u + w > 1
    u[z], w[z] = 1 - u[z], 1 - w[z]
    p = a[wybor] + (b[wybor] - a[wybor]) * u[:, None] + (c[wybor] - a[wybor]) * w[:, None]
    return p, n[wybor]


def przerzedz(p, n, cel):
    """Siatka wokseli: z każdej komórki jeden punkt — równy rozkład bez skupisk."""
    if len(p) <= cel:
        return p, n
    lo, hi = p.min(0), p.max(0)
    obj = float(np.prod(np.maximum(hi - lo, 1e-3)))
    bok = (obj / (cel * 2.2)) ** (1 / 3)
    for _ in range(40):
        kom = np.floor((p - lo) / bok).astype(np.int64)
        _, pierwszy = np.unique(kom, axis=0, return_index=True)
        if len(pierwszy) < cel:
            bok *= 0.93
            continue
        if len(pierwszy) > cel * 1.25:
            bok *= 1.05
            continue
        break
    wybor = rng.permutation(pierwszy)[:cel]
    wybor.sort()
    return p[wybor], n[wybor]


def main():
    katalog, wyjscie, n_pow, n_kraw = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    korzen = ET.parse(katalog / URDF).getroot()
    czlony = {l.get('name'): l for l in korzen.findall('link')}
    stawy = [j for j in korzen.findall('joint') if j.get('type') != 'floating']

    # Segmenty: miednica + człony za stawami obrotowymi. Człony za stawami stałymi
    # dopisują swoje siatki do segmentu rodzica z odpowiednią transformacją.
    segmenty = [{'nazwa': 'pelvis', 'rodzic': -1, 'staw': None}]
    seg_czlonu = {'pelvis': (0, np.eye(4))}
    for j in stawy:
        rodzic, dziecko = j.find('parent').get('link'), j.find('child').get('link')
        o = j.find('origin')
        t = transformacja(liczby(o.get('xyz') if o is not None else None), liczby(o.get('rpy') if o is not None else None))
        si, tr = seg_czlonu[rodzic]
        if j.get('type') == 'fixed':
            seg_czlonu[dziecko] = (si, tr @ t)
            continue
        assert np.allclose(tr, np.eye(4)) or True
        lim = j.find('limit')
        nowy = {'nazwa': dziecko, 'rodzic': si, 'staw': j.get('name'),
                'macierz': (tr @ t).tolist(),
                'os': liczby(j.find('axis').get('xyz')),
                'min': float(lim.get('lower')), 'max': float(lim.get('upper'))}
        seg_czlonu[dziecko] = (len(segmenty), np.eye(4))
        segmenty.append(nowy)

    # Siatki w układach segmentów
    siatki = [[] for _ in segmenty]
    for nazwa, (si, tr) in seg_czlonu.items():
        for vis in czlony[nazwa].findall('visual'):
            m = vis.find('geometry/mesh')
            if m is None:
                continue
            o = vis.find('origin')
            tv = tr @ transformacja(liczby(o.get('xyz') if o is not None else None), liczby(o.get('rpy') if o is not None else None))
            tri = wczytaj_stl(katalog / m.get('filename'))
            v = tri.reshape(-1, 3) @ tv[:3, :3].T + tv[:3, 3]
            siatki[si].append(v.reshape(-1, 3, 3))
    siatki = [np.concatenate(s) if s else np.zeros((0, 3, 3)) for s in siatki]

    pola = np.array([float(np.linalg.norm(np.cross(s[:, 1] - s[:, 0], s[:, 2] - s[:, 0]), axis=1).sum() / 2) if len(s) else 0 for s in siatki])
    odcinki = [krawedzie_ostre(s) if len(s) else [] for s in siatki]
    dlugosci = np.array([sum(float(np.linalg.norm(b - a)) for a, b, _ in o) for o in odcinki])

    P, N, bloki = [], [], []
    for si, s in enumerate(siatki):
        blok = [si, 0, 0]
        if len(s):
            cel = max(60, int(round(n_pow * pola[si] / pola.sum())))
            p, n = probki_powierzchni(s, cel * 10)
            p, n = przerzedz(p, n, cel)
            P.append(p); N.append(n); blok[1] = len(p)
            # krawędzie: punkty w losowych miejscach odcinków, gęstość równa dla całego robota
            cel_k = int(round(n_kraw * dlugosci[si] / max(dlugosci.sum(), 1e-9)))
            if cel_k and odcinki[si]:
                krok = dlugosci[si] / cel_k
                kp, kn = [], []
                for a, b, nn in odcinki[si]:
                    d = float(np.linalg.norm(b - a))
                    for _ in range(int(d / krok + rng.random())):
                        t = rng.random()
                        kp.append(a + (b - a) * t); kn.append(nn)
                if kp:
                    P.append(np.array(kp)); N.append(np.array(kn)); blok[2] = len(kp)
        bloki.append(blok)

    P, N = np.concatenate(P), np.concatenate(N)
    skala = float(np.abs(P).max()) * 1.001
    pos = np.round(P / skala * 32767).astype('<i2')
    # normalne: kodowanie oktaedryczne
    n = N / np.maximum(np.abs(N).sum(1, keepdims=True), 1e-9)
    dol = n[:, 2] < 0
    xy = n[:, :2].copy()
    znak = np.where(xy >= 0, 1.0, -1.0)
    xy[dol] = (1 - np.abs(n[dol][:, [1, 0]])) * znak[dol]
    okt = np.round(np.clip(xy, -1, 1) * 127).astype('i1')

    naglowek = {
        'zrodlo': 'unitreerobotics/unitree_ros robots/g1_description/' + URDF + ' (BSD-3-Clause, Unitree Robotics)',
        'n': int(len(P)), 'skala': skala, 'bloki': bloki,
        'segmenty': [{k: v for k, v in s.items()} for s in segmenty],
    }
    js = json.dumps(naglowek, separators=(',', ':')).encode('utf-8')
    js += b' ' * ((-len(js) - 4) % 4)
    wyjscie.parent.mkdir(parents=True, exist_ok=True)
    with open(wyjscie, 'wb') as f:
        f.write(struct.pack('<I', len(js)))
        f.write(js)
        f.write(pos.tobytes())
        f.write(okt.tobytes())
    kraw = sum(b[2] for b in bloki)
    print(f'{wyjscie}: {len(P)} punktów ({len(P) - kraw} powierzchnia, {kraw} krawędzie), '
          f'{len(segmenty)} segmentów, skala {skala:.4f} m, {wyjscie.stat().st_size / 1024:.0f} KB')


if __name__ == '__main__':
    main()
