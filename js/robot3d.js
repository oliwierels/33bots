/* Robot w hero: chmura punktów prawdziwego Unitree G1 (23 stopnie swobody).
   Geometria z unitreerobotics/unitree_ros (URDF i siatki STL, BSD-3-Clause) — licencja
   w robot/LICENCJA-UNITREE.txt. Dane przygotowuje scripts/robot3d/chmura_g1.py.

   Jedno płótno WebGL na cały ekran, nad treścią, bez zdarzeń wskaźnika. Robot zajmuje
   pole wskazane w HTML przez [data-scena]: hero (stoi i patrzy za kursorem), liczba
   (punkty układają się w „100+”), wystep (pozy kolejnych kroków występu). Układ strony
   decyduje, gdzie robot stoi — skrypt tylko wypełnia te pola.

   Bez WebGL: klasa bez-3d na <html>, hero wraca do zdjęcia. Ograniczony ruch: robot stoi,
   bez przelotów i gestów; pauza w hero zatrzymuje też robota (WCAG 2.2.2). */
(() => {
  'use strict';
  const html = document.documentElement;
  const scenaHero = document.querySelector('[data-scena="hero"]');
  if (!scenaHero) return;
  const scenaLiczba = document.querySelector('[data-scena="liczba"]');
  const scenaWystep = document.querySelector('[data-scena="wystep"]');
  const wystep = document.getElementById('wystep');
  const ruchMq = matchMedia('(prefers-reduced-motion: reduce)');
  let reduce = ruchMq.matches;
  const lekki = innerWidth < 768 || (navigator.hardwareConcurrency || 8) <= 4 || !!(navigator.connection && navigator.connection.saveData);

  const canvas = document.createElement('canvas');
  canvas.className = 'robot3d';
  canvas.setAttribute('aria-hidden', 'true');
  let gl = null;
  try {
    gl = canvas.getContext('webgl', { alpha: true, antialias: false, depth: true, stencil: false,
      premultipliedAlpha: true, powerPreference: lekki ? 'low-power' : 'high-performance' });
  } catch (e) { gl = null; }
  const bez3d = () => { html.classList.add('bez-3d'); html.dataset.robot = 'brak'; canvas.remove(); };
  if (!gl) { bez3d(); return; }

  /* ——— Matematyka: macierze 3×3 wierszowe (kinematyka), 4×4 kolumnowe (GL) ——— */
  const mnoz3 = (a, b) => {
    const r = new Array(9);
    for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) r[i * 3 + j] = a[i * 3] * b[j] + a[i * 3 + 1] * b[3 + j] + a[i * 3 + 2] * b[6 + j];
    return r;
  };
  const razy3 = (m, v) => [m[0] * v[0] + m[1] * v[1] + m[2] * v[2], m[3] * v[0] + m[4] * v[1] + m[5] * v[2], m[6] * v[0] + m[7] * v[1] + m[8] * v[2]];
  const obrotOs = (o, k) => {
    const c = Math.cos(k), s = Math.sin(k), t = 1 - c, [x, y, z] = o;
    return [t * x * x + c, t * x * y - s * z, t * x * z + s * y, t * x * y + s * z, t * y * y + c, t * y * z - s * x, t * x * z - s * y, t * y * z + s * x, t * z * z + c];
  };
  const kwaternion = (m, q, o) => {
    const tr = m[0] + m[4] + m[8];
    let x, y, z, w;
    if (tr > 0) { const s = Math.sqrt(tr + 1) * 2; w = s / 4; x = (m[7] - m[5]) / s; y = (m[2] - m[6]) / s; z = (m[3] - m[1]) / s; }
    else if (m[0] > m[4] && m[0] > m[8]) { const s = Math.sqrt(1 + m[0] - m[4] - m[8]) * 2; w = (m[7] - m[5]) / s; x = s / 4; y = (m[1] + m[3]) / s; z = (m[2] + m[6]) / s; }
    else if (m[4] > m[8]) { const s = Math.sqrt(1 + m[4] - m[0] - m[8]) * 2; w = (m[2] - m[6]) / s; x = (m[1] + m[3]) / s; y = s / 4; z = (m[5] + m[7]) / s; }
    else { const s = Math.sqrt(1 + m[8] - m[0] - m[4]) * 2; w = (m[3] - m[1]) / s; x = (m[2] + m[6]) / s; y = (m[5] + m[7]) / s; z = s / 4; }
    q[o] = x; q[o + 1] = y; q[o + 2] = z; q[o + 3] = w;
  };
  const m4 = () => new Float32Array(16);
  const m4mnoz = (a, b) => {
    const r = m4();
    for (let c = 0; c < 4; c++) for (let w = 0; w < 4; w++) r[c * 4 + w] = a[w] * b[c * 4] + a[4 + w] * b[c * 4 + 1] + a[8 + w] * b[c * 4 + 2] + a[12 + w] * b[c * 4 + 3];
    return r;
  };
  const m4persp = (fov, near, far) => {
    const f = 1 / Math.tan(fov / 2), r = m4();
    r[0] = f; r[5] = f; r[10] = (far + near) / (near - far); r[11] = -1; r[14] = 2 * far * near / (near - far);
    return r;
  };
  const m4widok = (oko, cel) => { // kamera na osi Z (GL), patrzy w cel, góra = +Y
    const z = [oko[0] - cel[0], oko[1] - cel[1], oko[2] - cel[2]];
    const dz = Math.hypot(...z); z[0] /= dz; z[1] /= dz; z[2] /= dz;
    const x = [z[2], 0, -z[0]]; const dx = Math.hypot(...x); x[0] /= dx; x[2] /= dx;
    const y = [z[1] * x[2] - z[2] * x[1], z[2] * x[0] - z[0] * x[2], z[0] * x[1] - z[1] * x[0]];
    const r = m4();
    r[0] = x[0]; r[4] = x[1]; r[8] = x[2]; r[1] = y[0]; r[5] = y[1]; r[9] = y[2]; r[2] = z[0]; r[6] = z[1]; r[10] = z[2];
    r[12] = -(x[0] * oko[0] + x[1] * oko[1] + x[2] * oko[2]);
    r[13] = -(y[0] * oko[0] + y[1] * oko[1] + y[2] * oko[2]);
    r[14] = -(z[0] * oko[0] + z[1] * oko[1] + z[2] * oko[2]);
    r[15] = 1;
    return r;
  };
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const gladko = (a, b, v) => { const t = clamp((v - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };
  const hash = (i) => { const s = Math.sin(i * 12.9898 + 78.233) * 43758.5453; return s - Math.floor(s); };

  /* ——— Shadery ——— */
  const VS = `
attribute vec3 aPos; attribute vec2 aNrm; attribute float aSeg; attribute vec2 aTxt; attribute float aLos;
uniform vec4 uQ[26]; uniform vec4 uT[26];
uniform float uSkala, uMorf, uCel, uCzas, uPx, uSkan, uRozb, uWiatr;
uniform mat4 uM, uVP; uniform vec4 uTxt; uniform vec3 uKam; uniform vec4 uBlask; uniform float uZaslona;
varying float vJ;
vec3 obr(vec4 q, vec3 v) { return v + 2.0 * cross(q.xyz, cross(q.xyz, v) + q.w * v); }
vec3 okt(vec2 e) {
  vec3 v = vec3(e, 1.0 - abs(e.x) - abs(e.y));
  if (v.z < 0.0) v.xy = (1.0 - abs(v.yx)) * vec2(v.x >= 0.0 ? 1.0 : -1.0, v.y >= 0.0 ? 1.0 : -1.0);
  return normalize(v);
}
void main() {
  float kraw = step(127.5, aSeg);
  float s = aSeg - 128.0 * kraw;
  int i = int(s + 0.5);
  vec3 lp = aPos * uSkala;
  vec3 wp = obr(uQ[i], lp) + uT[i].xyz;
  vec3 wn = obr(uQ[i], okt(aNrm));
  vec4 sw = uM * vec4(wp, 1.0);
  vec3 n = normalize(mat3(uM) * wn);
  vec4 c = uVP * sw;
  vec3 ndcR = c.xyz / c.w;
  vec2 tekst = vec2(uTxt.x + aTxt.x, uTxt.y + aTxt.y) * uTxt.zw;
  tekst = vec2(tekst.x - 1.0, 1.0 - tekst.y);
  float a1 = aLos * 6.2832, a2 = fract(aLos * 7.31) * 6.2832;
  vec2 chmura = vec2(cos(a1), sin(a1)) * (0.35 + 0.9 * fract(aLos * 3.7)) * vec2(1.3, 1.0) + vec2(0.0, 0.25);
  vec2 cel = mix(tekst, chmura, uCel);
  float t = clamp(uMorf * 1.7 - aLos * 0.7, 0.0, 1.0);
  t = t * t * (3.0 - 2.0 * t);
  vec2 p = mix(ndcR.xy, cel, t);
  float lot = sin(3.14159 * t);
  p += lot * uRozb * vec2(cos(a2 + uCzas * 0.7), sin(a2 * 1.3 + uCzas * 0.5)) * (0.08 + 0.22 * fract(aLos * 5.3));
  p.x += uWiatr * (fract(aLos * 9.1) - 0.5) * 0.04 * (1.0 - t);
  float z = mix(clamp(ndcR.z, -1.0, 1.0), 0.0, t) + uZaslona * 0.004;
  gl_Position = vec4(p, z, 1.0);
  vec3 V = normalize(uKam - sw.xyz);
  float nv = dot(n, V);
  float swiatlo = max(dot(n, normalize(vec3(-0.45, 0.75, 0.55))), 0.0);
  float kontur = pow(1.0 - abs(nv), 2.2);
  float przod = mix(0.55, 1.0, smoothstep(-0.2, 0.4, nv));
  float skan = exp(-pow((wp.z - uSkan) / 0.012, 2.0)) * 0.6;
  float blask = uBlask.w * (1.0 - smoothstep(0.0, 0.11, distance(wp, uBlask.xyz)));
  float j = (0.16 + 0.6 * swiatlo + 0.55 * kontur + 0.55 * kraw) * przod + 0.85 * skan + 0.9 * blask;
  if (i == 25) j = 0.22 * (1.0 - smoothstep(0.35, 0.62, length(wp.xy)));
  vJ = mix(j, 0.95, t);
  float rozm = uPx * mix(1.0, 0.85, kraw) * (1.0 + 0.8 * skan + 0.6 * blask) * (3.3 / c.w) * (1.0 + uZaslona * 1.6);
  gl_PointSize = mix(rozm, uPx * 1.15, t);
}`;
  const FS = `
precision mediump float;
varying float vJ; uniform float uAlfa;
void main() {
  vec2 d = gl_PointCoord - 0.5;
  float r = dot(d, d);
  if (r > 0.25) discard;
  float a = (1.0 - r * 4.0) * uAlfa * 0.75;
  gl_FragColor = vec4(vec3(min(vJ, 1.4)) * a, a);
}`;
  const shader = (typ, zrodlo) => {
    const s = gl.createShader(typ); gl.shaderSource(s, zrodlo); gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
    return s;
  };
  let prog;
  try {
    prog = gl.createProgram();
    gl.attachShader(prog, shader(gl.VERTEX_SHADER, VS));
    gl.attachShader(prog, shader(gl.FRAGMENT_SHADER, FS));
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(prog));
  } catch (e) { bez3d(); return; }
  const U = {};
  for (const n of ['uQ', 'uT', 'uSkala', 'uMorf', 'uCel', 'uCzas', 'uPx', 'uSkan', 'uRozb', 'uWiatr', 'uM', 'uVP', 'uTxt', 'uKam', 'uBlask', 'uAlfa', 'uZaslona']) U[n] = gl.getUniformLocation(prog, n);
  const A = {};
  for (const n of ['aPos', 'aNrm', 'aSeg', 'aTxt', 'aLos']) A[n] = gl.getAttribLocation(prog, n);

  /* ——— Stan robota ——— */
  let S = null;           // segmenty z pliku
  let q = null, qCel = null;
  const IDX = {};
  let N = 0, bufTxt = null, txt = null, podeszwa = null;
  const kw = new Float32Array(26 * 4), tr = new Float32Array(26 * 4);
  const swiat = [];       // [R, t] segmentów po kinematyce, układ URDF (z w górę, x do przodu)

  const kinematyka = () => {
    for (let i = 0; i < S.length; i++) {
      const s = S[i];
      if (s.rodzic < 0) { swiat[i] = [[1, 0, 0, 0, 1, 0, 0, 0, 1], [0, 0, 0]]; continue; }
      const [Rp, tp] = swiat[s.rodzic];
      const R = mnoz3(mnoz3(Rp, s.R), obrotOs(s.os, q[i]));
      const t0 = razy3(Rp, s.t);
      swiat[i] = [R, [t0[0] + tp[0], t0[1] + tp[1], t0[2] + tp[2]]];
    }
    // Stopy na podłodze: miednica przesuwa się tak, żeby podeszwy stały w (0, 0, 0).
    const st = [IDX.left_ankle_roll_joint, IDX.right_ankle_roll_joint].map((i) => {
      const [R, t] = swiat[i]; const p = razy3(R, podeszwa[i]);
      return [p[0] + t[0], p[1] + t[1], p[2] + t[2]];
    });
    const dx = -(st[0][0] + st[1][0]) / 2, dy = -(st[0][1] + st[1][1]) / 2, dz = -Math.min(st[0][2], st[1][2]);
    for (let i = 0; i < S.length; i++) {
      const [R, t] = swiat[i];
      t[0] += dx; t[1] += dy; t[2] += dz;
      kwaternion(R, kw, i * 4);
      tr[i * 4] = t[0]; tr[i * 4 + 1] = t[1]; tr[i * 4 + 2] = t[2];
    }
    kw[25 * 4 + 3] = 1; // podłoga: bez obrotu, w początku układu
  };
  const punktSwiata = (i, lokalny) => { const [R, t] = swiat[i]; const p = razy3(R, lokalny); return [p[0] + t[0], p[1] + t[1], p[2] + t[2]]; };

  /* ——— Pozy: kąty w radianach, nazwy stawów z URDF ———
     Ramię: pitch ujemny = do przodu/w górę, roll lewego dodatni = w bok (prawego ujemny),
     łokieć 0 = przedramię poziomo do przodu, ok. 1,5 = wyprostowane w dół. */
  const P = (o) => o;
  const BAZA = P({
    left_hip_pitch_joint: -0.14, right_hip_pitch_joint: -0.14, left_knee_joint: 0.32, right_knee_joint: 0.32,
    left_ankle_pitch_joint: -0.18, right_ankle_pitch_joint: -0.18,
    left_hip_roll_joint: 0.02, right_hip_roll_joint: -0.02, left_ankle_roll_joint: -0.02, right_ankle_roll_joint: 0.02,
    left_shoulder_pitch_joint: 0.18, right_shoulder_pitch_joint: 0.18, left_shoulder_roll_joint: 0.16, right_shoulder_roll_joint: -0.16,
    left_shoulder_yaw_joint: 0.05, right_shoulder_yaw_joint: -0.05, left_elbow_joint: 1.15, right_elbow_joint: 1.15,
    left_wrist_roll_joint: 0, right_wrist_roll_joint: 0, waist_yaw_joint: 0,
  });
  const POZY = {
    stoi: (t) => ({ left_elbow_joint: 1.15 + 0.03 * Math.sin(t * 1.3), right_elbow_joint: 1.15 + 0.03 * Math.sin(t * 1.3 + 1) }),
    // ramię w bok i w górę, przedramię pionowo; machanie = obrót wokół osi ramienia
    macha: (t) => ({ right_shoulder_pitch_joint: -1.0, right_shoulder_roll_joint: -0.7, right_shoulder_yaw_joint: -0.05 + 0.34 * Math.sin(t * 6.5),
      right_elbow_joint: 0.1, waist_yaw_joint: -0.1 }),
    // wyprostowana ręka w stronę przycisku „Sprawdź termin” (po lewej od robota, niżej)
    wskazuje: () => ({ right_shoulder_pitch_joint: -0.85, right_shoulder_roll_joint: -0.85, right_shoulder_yaw_joint: 0,
      right_elbow_joint: 1.45, waist_yaw_joint: -0.32 }),
    wita: (t) => ({ left_shoulder_pitch_joint: -0.45, right_shoulder_pitch_joint: -0.45, left_shoulder_roll_joint: 0.72 + 0.05 * Math.sin(t * 1.6),
      right_shoulder_roll_joint: -0.72 - 0.05 * Math.sin(t * 1.6), left_shoulder_yaw_joint: 0.3, right_shoulder_yaw_joint: -0.3,
      left_elbow_joint: 0.95, right_elbow_joint: 0.95 }),
    mowi: (t) => ({ left_shoulder_pitch_joint: -0.2 + 0.1 * Math.sin(t * 2.6), right_shoulder_pitch_joint: -0.22 + 0.12 * Math.sin(t * 2.1 + 1.4),
      left_shoulder_roll_joint: 0.25, right_shoulder_roll_joint: -0.25,
      left_elbow_joint: 0.3 + 0.15 * Math.sin(t * 2.6 + 0.5), right_elbow_joint: 0.3 + 0.18 * Math.sin(t * 2.1 + 2),
      left_wrist_roll_joint: -0.5 + 0.3 * Math.sin(t * 3), right_wrist_roll_joint: 0.5 + 0.3 * Math.sin(t * 2.7),
      waist_yaw_joint: 0.12 * Math.sin(t * 0.9) }),
    // zapowiedź prelegenta: ręka w bok, otwarta dłoń
    przedstawia: (t) => ({ right_shoulder_pitch_joint: -1.25, right_shoulder_roll_joint: -0.6, right_elbow_joint: 1.45,
      right_wrist_roll_joint: 0.6, waist_yaw_joint: -0.25 + 0.04 * Math.sin(t * 1.2), left_elbow_joint: 1.0 }),
    tanczy: (t) => {
      const b = t * 4.2, s = Math.sin(b), k = Math.abs(Math.sin(b / 2));
      return { left_shoulder_pitch_joint: -0.9 - 0.5 * s, right_shoulder_pitch_joint: -0.9 + 0.5 * s,
        left_shoulder_roll_joint: 0.5 + 0.25 * s, right_shoulder_roll_joint: -0.5 + 0.25 * s,
        left_elbow_joint: 0.2 + 0.3 * k, right_elbow_joint: 0.2 + 0.3 * (1 - k), waist_yaw_joint: 0.35 * s,
        left_knee_joint: 0.32 + 0.22 * k, right_knee_joint: 0.32 + 0.22 * k,
        left_hip_pitch_joint: -0.14 - 0.11 * k, right_hip_pitch_joint: -0.14 - 0.11 * k,
        left_ankle_pitch_joint: -0.18 - 0.11 * k, right_ankle_pitch_joint: -0.18 - 0.11 * k };
    },
    branding: (t) => ({ left_shoulder_pitch_joint: 0.3, right_shoulder_pitch_joint: 0.3, left_shoulder_roll_joint: 0.35,
      right_shoulder_roll_joint: -0.35, left_elbow_joint: 1.35, right_elbow_joint: 1.35, waist_yaw_joint: 0.05 * Math.sin(t) }),
    // do zdjęcia: obie ręce w górę
    zdjecie: (t) => ({ left_shoulder_pitch_joint: -2.6, right_shoulder_pitch_joint: -2.6, left_shoulder_roll_joint: 0.5 + 0.06 * Math.sin(t * 3),
      right_shoulder_roll_joint: -0.5 - 0.06 * Math.sin(t * 3), left_elbow_joint: 1.4, right_elbow_joint: 1.4 }),
  };

  /* ——— Ładowanie danych ——— */
  const WERSJA_DANYCH = 'c5fc3eba'; // ustawia buduj.sh (suma plików robot/*.bin)
  const dpr = Math.min(devicePixelRatio || 1, lekki ? 1.5 : 2);
  const wczytaj = async () => {
    const r = await fetch((lekki ? 'robot/g1-lekki.bin' : 'robot/g1.bin') + '?v=' + WERSJA_DANYCH, { priority: 'low' });
    if (!r.ok) throw new Error('robot: ' + r.status);
    const dane = await r.arrayBuffer();
    const dv = new DataView(dane);
    const dl = dv.getUint32(0, true);
    const nag = JSON.parse(new TextDecoder().decode(new Uint8Array(dane, 4, dl)));
    const n = nag.n, o = 4 + dl;
    const pos = new Int16Array(dane, o, n * 3);
    const nrm = new Int8Array(dane, o + n * 6, n * 2);
    // Punkty leżą blokami: segment po segmencie, najpierw powierzchnia, potem krawędzie (bit 128).
    const seg = new Uint8Array(n);
    let k0 = 0;
    for (const [si, ilePow, ileKraw] of nag.bloki) { seg.fill(si, k0, k0 + ilePow); seg.fill(si | 128, k0 + ilePow, k0 + ilePow + ileKraw); k0 += ilePow + ileKraw; }
    S = nag.segmenty.map((s) => {
      const m = s.macierz || [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]];
      return { nazwa: s.nazwa, rodzic: s.rodzic, staw: s.staw, os: s.os || [0, 0, 1], min: s.min ?? -9, max: s.max ?? 9,
        R: [m[0][0], m[0][1], m[0][2], m[1][0], m[1][1], m[1][2], m[2][0], m[2][1], m[2][2]], t: [m[0][3], m[1][3], m[2][3]] };
    });
    S.forEach((s, i) => { if (s.staw) IDX[s.staw] = i; });
    q = new Float32Array(S.length); qCel = new Float32Array(S.length);
    for (const [k, v] of Object.entries(BAZA)) q[IDX[k]] = v;

    // Podeszwy: środek najniższych punktów stopy w układzie członu kostki.
    podeszwa = {};
    for (const nazwa of ['left_ankle_roll_joint', 'right_ankle_roll_joint']) {
      const si = IDX[nazwa]; let zmin = 9, sx = 0, sy = 0, ile = 0;
      for (let i = 0; i < n; i++) if ((seg[i] & 127) === si) zmin = Math.min(zmin, pos[i * 3 + 2]);
      for (let i = 0; i < n; i++) if ((seg[i] & 127) === si && pos[i * 3 + 2] < zmin + 600) { sx += pos[i * 3]; sy += pos[i * 3 + 1]; ile++; }
      podeszwa[si] = [sx / ile / 32767 * nag.skala, sy / ile / 32767 * nag.skala, zmin / 32767 * nag.skala];
    }

    // Podłoga: koncentryczne okręgi punktów wokół stóp (segment 25, bez ruchu).
    const kola = [];
    for (const [r, ile] of [[0.26, 150], [0.36, 220], [0.46, 300], [0.56, 360]]) {
      for (let i = 0; i < ile; i++) { const a = (i / ile) * Math.PI * 2; kola.push(Math.cos(a) * r, Math.sin(a) * r * 0.999, 0); }
    }
    for (let i = 0; i < 72; i++) { const a = (i / 72) * Math.PI * 2; for (let k = 0; k < 6; k++) { const r = 0.58 + k * 0.012; kola.push(Math.cos(a) * r, Math.sin(a) * r, 0); } }
    const nP = kola.length / 3;
    N = n + nP;
    const P16 = new Int16Array(N * 3); P16.set(pos);
    for (let i = 0; i < kola.length; i++) P16[n * 3 + i] = Math.round(kola[i] / nag.skala * 32767);
    const N8 = new Int8Array(N * 2); N8.set(nrm); // podłoga: normalna (0, 0, 1) = (0, 0) w kodowaniu oktaedrycznym
    const S8 = new Uint8Array(N); S8.set(seg); S8.fill(25, n);
    const los = new Float32Array(N);
    for (let i = 0; i < N; i++) los[i] = hash(i + 0.5);
    txt = new Float32Array(N * 2);

    const bufor = (dane, atr, rozm, typ, norm) => {
      const b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, dane, gl.STATIC_DRAW);
      gl.enableVertexAttribArray(atr); gl.vertexAttribPointer(atr, rozm, typ, norm, 0, 0);
      return b;
    };
    gl.useProgram(prog);
    bufor(P16, A.aPos, 3, gl.SHORT, true);
    bufor(N8, A.aNrm, 2, gl.BYTE, true);
    bufor(S8, A.aSeg, 1, gl.UNSIGNED_BYTE, false);
    bufor(los, A.aLos, 1, gl.FLOAT, false);
    bufTxt = bufor(txt, A.aTxt, 2, gl.FLOAT, false);
    gl.uniform1f(U.uSkala, nag.skala);
  };

  /* ——— Cel „100+”: punkty z pikseli napisu, w pikselach CSS względem pola liczby ——— */
  let txtGotowy = false, txtKlucz = '';
  const zbudujTekst = async () => {
    const el = scenaLiczba && scenaLiczba.querySelector('[data-tekst]');
    if (!el || !N) return;
    const st = getComputedStyle(el);
    const klucz = [el.textContent, st.fontSize, st.fontWeight, st.letterSpacing, el.clientWidth].join('|');
    if (klucz === txtKlucz) return;
    txtKlucz = klucz;
    try { await document.fonts.load(`${st.fontWeight} ${st.fontSize} ${st.fontFamily}`); } catch (e) { /* font systemowy */ }
    const fs = parseFloat(st.fontSize), lh = parseFloat(st.lineHeight) || fs;
    const r = el.getBoundingClientRect();
    const w = Math.ceil(r.width + fs), h = Math.ceil(lh + fs * 0.5);
    const k = Math.min(1, 900 / w);
    const c = document.createElement('canvas'); c.width = Math.ceil(w * k); c.height = Math.ceil(h * k);
    const x = c.getContext('2d', { willReadFrequently: true });
    x.scale(k, k);
    x.font = `${st.fontWeight} ${fs}px ${st.fontFamily}`;
    if ('letterSpacing' in x) x.letterSpacing = st.letterSpacing === 'normal' ? '0px' : st.letterSpacing;
    x.textBaseline = 'alphabetic';
    const m = x.measureText(el.textContent);
    const asc = m.fontBoundingBoxAscent ?? fs * 0.8, desc = m.fontBoundingBoxDescent ?? fs * 0.2;
    const linia = (lh - (asc + desc)) / 2 + asc;
    const lewo = st.textAlign === 'right' || st.textAlign === 'end' ? r.width - m.width : 0;
    x.fillStyle = '#fff';
    x.fillText(el.textContent, lewo, linia);
    const d = x.getImageData(0, 0, c.width, c.height).data;
    const pel = [];
    for (let i = 3; i < d.length; i += 4) if (d[i] > 140) pel.push((i - 3) / 4);
    if (!pel.length) return;
    // Pozycja napisu względem pola sceny (nie samego elementu tekstu).
    const rs = scenaLiczba.getBoundingClientRect();
    const ox = r.left - rs.left, oy = r.top - rs.top;
    for (let i = 0; i < N; i++) {
      const p = pel[Math.floor(hash(i * 1.7 + 3.1) * pel.length)];
      const px = (p % c.width + hash(i + 9.3)) / k, py = (Math.floor(p / c.width) + hash(i + 4.4)) / k;
      txt[i * 2] = ox + px; txt[i * 2 + 1] = oy + py;
    }
    gl.bindBuffer(gl.ARRAY_BUFFER, bufTxt);
    gl.bufferData(gl.ARRAY_BUFFER, txt, gl.STATIC_DRAW);
    txtGotowy = true;
  };

  /* ——— Wejście użytkownika ——— */
  const mysz = { x: 0.5, y: 0.4, jest: false };
  let orbita = 0, orbitaV = 0, ciagnie = null, puszczono = -9;
  addEventListener('pointermove', (e) => { if (e.pointerType === 'mouse') { mysz.x = e.clientX / innerWidth; mysz.y = e.clientY / innerHeight; mysz.jest = true; } }, { passive: true });
  document.addEventListener('mouseleave', () => { mysz.jest = false; });
  scenaHero.addEventListener('pointerdown', (e) => {
    if (reduce || e.button !== 0) return;
    ciagnie = { id: e.pointerId, x: e.clientX, t: performance.now(), dx: 0 };
    scenaHero.setPointerCapture(e.pointerId);
  });
  scenaHero.addEventListener('pointermove', (e) => {
    if (!ciagnie || ciagnie.id !== e.pointerId) return;
    const dx = e.clientX - ciagnie.x, t = performance.now();
    orbita += dx * 0.011; orbitaV = dx * 0.011 / Math.max(0.008, (t - ciagnie.t) / 1000);
    ciagnie.x = e.clientX; ciagnie.t = t; ciagnie.dx += Math.abs(dx);
  });
  const pusc = (e) => {
    if (!ciagnie || ciagnie.id !== e.pointerId) return;
    if (ciagnie.dx < 6) gest('macha', 2.4);
    ciagnie = null; puszczono = performance.now() / 1000;
  };
  scenaHero.addEventListener('pointerup', pusc);
  scenaHero.addEventListener('pointercancel', pusc);

  // Kursor nad „Sprawdź termin” w hero: robot wskazuje przycisk.
  let wskazuje = false;
  const ctaHero = document.querySelector('.hero [data-cta="hero"]');
  if (ctaHero) {
    ctaHero.addEventListener('pointerenter', () => { wskazuje = true; });
    ctaHero.addEventListener('pointerleave', () => { wskazuje = false; });
    ctaHero.addEventListener('focus', () => { wskazuje = true; });
    ctaHero.addEventListener('blur', () => { wskazuje = false; });
  }
  // Pauza w hero (przycisk rotacji zdjęć) zatrzymuje też robota.
  const pauza = document.getElementById('heroPauza');
  const zatrzymany = () => reduce || (pauza && pauza.getAttribute('aria-pressed') === 'true');

  let gestNazwa = null, gestDo = 0, dbgKaty = null, dbgOrbita = null;
  const gest = (nazwa, czas) => { if (zatrzymany()) return; gestNazwa = nazwa; gestDo = zegar + czas; };

  /* ——— Reżyser: gdzie robot stoi, w co się zmienia, jak bardzo go widać ——— */
  let zegar = 0, wejscie = 0, gotowy = false;
  const rezyser = () => {
    const vh = innerHeight;
    const rH = scenaHero.getBoundingClientRect();
    const widacH = clamp(Math.min(rH.bottom, vh) - Math.max(rH.top, 0), 0, rH.height) / Math.max(1, Math.min(rH.height, vh));
    const st = { rect: rH, morf: 0, cel: 0, alfa: gladko(0.05, 0.6, widacH), poza: null, strefa: 'hero' };
    if (scenaWystep && scenaWystep.offsetParent !== null) {
      const rW = scenaWystep.getBoundingClientRect(), rs = wystep.getBoundingClientRect();
      if (rs.top < vh && rs.bottom > 0) {
        const wej = clamp((vh - rs.top) / (vh * 0.55), 0, 1), wyj = clamp(rs.bottom / (vh * 0.6), 0, 1);
        const m = 1 - Math.min(wej, wyj);
        return { rect: rW, morf: reduce ? (m < 1 ? 0 : 1) : m, cel: 1, alfa: reduce ? (m < 1 ? 1 : 0) : 1 - gladko(0.55, 1, m), poza: wystep.dataset.poza || 'wita', strefa: 'wystep' };
      }
    }
    if (scenaLiczba && txtGotowy && !reduce) {
      const rL = scenaLiczba.getBoundingClientRect();
      const srodek = rL.top + rL.height / 2;
      const m = gladko(vh * 0.95, vh * 0.5, srodek);
      if (m > 0) {
        st.morf = m; st.cel = 0; st.strefa = 'liczba';
        const zostaje = clamp((rL.bottom - 40) / (rL.height * 0.7), 0, 1);
        st.alfa = Math.max(st.alfa * (1 - m), m * zostaje);
        st.rectL = rL;
      }
    }
    return st;
  };

  /* ——— Rysowanie ——— */
  let W = 0, H = 0;
  const rozmiar = () => {
    const w = Math.round(canvas.clientWidth * dpr), h = Math.round(canvas.clientHeight * dpr);
    if (w !== W || h !== H) { W = canvas.width = w; H = canvas.height = h; }
  };
  const FOV = 24 * Math.PI / 180, ODL = 1.42 / (2 * Math.tan(FOV / 2));
  const OKO = [0, 0.7, ODL], CEL = [0, 0.66, 0];
  const PROJ = m4persp(FOV, 0.1, 20), WIDOK = m4widok(OKO, CEL);
  // Podpisy przy robocie: każdy należy do swojej sceny, data-hud-poza zawęża go do wybranych póz.
  const hud = [...document.querySelectorAll('[data-hud]')].map((el) => ({ el, scena: el.closest('[data-scena]'),
    pozy: (el.dataset.hudPoza || '').split(' ').filter(Boolean) }));
  const HUD_PKT = { // punkt w układzie członu (URDF): głowa i pierś po lewej stronie robota = prawa strona ekranu
    glowa: ['waist_yaw_joint', [0.03, 0.1, 0.42]], piers: ['waist_yaw_joint', [0.1, 0.11, 0.2]],
    dlon: ['right_wrist_roll_joint', [0.1, -0.02, 0]], podloga: [null, [0, 0.5, 0.02]],
  };
  let ost = 0, wyglad = { morf: 0, alfa: 0 }, klatkaId = 0, dziala = false, lookX = 0;

  const klatka = (tms) => {
    klatkaId = 0;
    const t = tms / 1000, dt = Math.min(0.05, ost ? t - ost : 0.016); ost = t;
    const stoj = zatrzymany();
    if (!stoj) zegar += dt;
    const st = rezyser();
    rozmiar();
    const cr = canvas.getBoundingClientRect();

    // wejście: punkty zlatują się w robota po załadowaniu
    wejscie = reduce ? 1 : Math.min(1, wejscie + dt / 2.2);
    let morf = st.morf, cel = st.cel;
    if (wejscie < 1 && st.strefa === 'hero') { morf = 1 - gladko(0, 1, wejscie); cel = 1; }
    wyglad.alfa += (st.alfa - wyglad.alfa) * (reduce ? 1 : 1 - Math.exp(-dt * 8));

    // pozy
    let poza = st.poza || 'stoi';
    if (st.strefa === 'hero') {
      if (wskazuje) poza = 'wskazuje';
      else if (gestNazwa && zegar < gestDo) poza = gestNazwa;
      else { gestNazwa = null; if (wejscie >= 1 && !stoj && zegar > 3 && Math.floor(zegar) % 14 === 0 && Math.random() < dt * 1.5) gest('macha', 2.4); }
    }
    for (let i = 0; i < S.length; i++) qCel[i] = q[i];
    for (const [k, v] of Object.entries(BAZA)) qCel[IDX[k]] = v;
    const czas = stoj ? 0 : zegar;
    const nad = (POZY[poza] || POZY.stoi)(czas);
    for (const [k, v] of Object.entries(nad)) qCel[IDX[k]] = v;
    if (dbgKaty) for (const [k, v] of Object.entries(dbgKaty)) qCel[IDX[k]] = v;
    if (!stoj) { // oddech: lekkie ugięcie kolan
      const o = 0.025 * Math.sin(czas * 1.4);
      for (const s of ['left', 'right']) { qCel[IDX[s + '_knee_joint']] += o * 2; qCel[IDX[s + '_hip_pitch_joint']] -= o; qCel[IDX[s + '_ankle_pitch_joint']] -= o; }
    }
    // spojrzenie za kursorem: obrót tułowia w pasie (G1 nie ma szyi)
    const rr = st.rect;
    const sx = (rr.left + rr.width / 2) / innerWidth;
    const celLook = mysz.jest && !stoj && st.strefa === 'hero' && !wskazuje ? clamp((mysz.x - sx) * 1.6, -0.75, 0.75) : 0;
    lookX += (celLook - lookX) * (1 - Math.exp(-dt * 4));
    qCel[IDX.waist_yaw_joint] += lookX * 0.8;
    const k = reduce ? 1 : 1 - Math.exp(-dt * (poza === 'tanczy' || poza === 'macha' || poza === 'mowi' ? 14 : 6));
    for (let i = 0; i < S.length; i++) {
      const s = S[i]; if (!s.staw) continue;
      q[i] += (clamp(qCel[i], s.min, s.max) - q[i]) * k;
    }
    kinematyka();

    // orbita: przeciąganie, potem powolny powrót przodem do widza
    if (!ciagnie) {
      orbita += orbitaV * dt; orbitaV *= Math.exp(-dt * 3);
      if (t - puszczono > 1.2) { const cel0 = Math.round(orbita / (Math.PI * 2)) * Math.PI * 2; orbita += (cel0 - orbita) * (1 - Math.exp(-dt * 1.6)); }
    }
    const yaw = dbgOrbita ?? orbita + lookX * 0.35;

    // macierz modelu: URDF (x przód, y lewo, z góra) → GL (x prawo, y góra, z do widza)
    const c = Math.cos(yaw), s = Math.sin(yaw);
    const M = m4();
    M[0] = s; M[1] = 0; M[2] = c;          // kolumna x_urdf
    M[4] = c; M[5] = 0; M[6] = -s;         // kolumna y_urdf
    M[8] = 0; M[9] = 1; M[10] = 0;         // kolumna z_urdf
    M[15] = 1;
    // przesunięcie obiektywu: robot wypełnia pole sceny w płótnie
    const cx = ((rr.left - cr.left + rr.width / 2) / cr.width) * 2 - 1;
    const cy = 1 - ((rr.top - cr.top + rr.height / 2) / cr.height) * 2;
    const sy = rr.height / cr.height, sxk = rr.height / cr.width;
    const SH = m4(); SH[0] = sxk; SH[5] = sy; SH[10] = 1; SH[15] = 1; SH[8] = 0; SH[12] = 0;
    const VP = m4mnoz(PROJ, WIDOK);
    // clip' = SH·clip + przesunięcie·w
    const PRZ = m4(); PRZ[0] = 1; PRZ[5] = 1; PRZ[10] = 1; PRZ[15] = 1; PRZ[8] = 0; PRZ[9] = 0;
    const VP2 = m4mnoz(SH, VP);
    for (let i = 0; i < 4; i++) { VP2[i * 4] += cx * VP[i * 4 + 3]; VP2[i * 4 + 1] += cy * VP[i * 4 + 3]; }

    gl.viewport(0, 0, W, H);
    gl.clearColor(0, 0, 0, 0);
    gl.clear(gl.COLOR_BUFFER_BIT);
    if (wyglad.alfa > 0.004) {
      gl.enable(gl.BLEND); gl.blendFunc(gl.ONE, gl.ONE);
      gl.useProgram(prog);
      gl.uniform4fv(U.uQ, kw); gl.uniform4fv(U.uT, tr);
      gl.uniformMatrix4fv(U.uM, false, M);
      gl.uniformMatrix4fv(U.uVP, false, VP2);
      gl.uniform3f(U.uKam, OKO[0], OKO[1], OKO[2]);
      const rl = st.rectL || (scenaLiczba && scenaLiczba.getBoundingClientRect()) || { left: 0, top: 0 };
      gl.uniform4f(U.uTxt, rl.left - cr.left, rl.top - cr.top, 2 / cr.width, 2 / cr.height);
      gl.uniform1f(U.uMorf, morf);
      gl.uniform1f(U.uCel, cel);
      gl.uniform1f(U.uCzas, czas);
      gl.uniform1f(U.uRozb, reduce ? 0 : 1);
      gl.uniform1f(U.uWiatr, 0);
      gl.uniform1f(U.uSkan, stoj ? -1 : ((czas % 7) / 5.2) * 1.5 - 0.1);
      const blask = poza === 'branding' ? 0.55 + 0.25 * Math.sin(czas * 3) : 0;
      const pk = punktSwiata(IDX.waist_yaw_joint, [0.1, 0, 0.22]);
      gl.uniform4f(U.uBlask, pk[0], pk[1], pk[2], blask);
      gl.uniform1f(U.uPx, clamp(rr.height / 820, 0.55, 1.3) * (lekki ? 2.5 : 2.4) * Math.pow(dpr, 0.85));
      gl.uniform1f(U.uAlfa, wyglad.alfa);
      // 1. przebieg: większe punkty tylko do bufora głębi — przód robota zasłania tył.
      gl.clear(gl.DEPTH_BUFFER_BIT);
      gl.enable(gl.DEPTH_TEST); gl.depthFunc(gl.LEQUAL);
      gl.colorMask(false, false, false, false);
      gl.uniform1f(U.uZaslona, 1);
      gl.drawArrays(gl.POINTS, 0, N);
      // 2. przebieg: właściwe punkty, bez zapisu głębi.
      gl.colorMask(true, true, true, true);
      gl.depthMask(false);
      gl.uniform1f(U.uZaslona, 0);
      gl.drawArrays(gl.POINTS, 0, N);
      gl.depthMask(true);
    }

    // podpisy przy robocie: rzut punktów ciała na ekran
    const scenaTeraz = st.strefa === 'wystep' ? scenaWystep : scenaHero;
    for (const h of hud) {
      const el = h.el;
      const [staw, lok] = HUD_PKT[el.dataset.hud] || [];
      const pokazHud = !!lok && h.scena === scenaTeraz && st.strefa !== 'liczba' && morf < 0.05 && wejscie >= 1 && wyglad.alfa > 0.5
        && (!h.pozy.length || h.pozy.includes(poza));
      el.classList.toggle('hud--widoczny', pokazHud);
      if (!pokazHud) continue;
      const p = staw ? punktSwiata(IDX[staw], lok) : lok;
      const v = [M[0] * p[0] + M[4] * p[1] + M[8] * p[2], M[1] * p[0] + M[5] * p[1] + M[9] * p[2], M[2] * p[0] + M[6] * p[1] + M[10] * p[2], 1];
      const cl = [0, 1, 2, 3].map((r) => VP2[r] * v[0] + VP2[4 + r] * v[1] + VP2[8 + r] * v[2] + VP2[12 + r]);
      const X = (cl[0] / cl[3] + 1) / 2 * cr.width + cr.left - rr.left, Y = (1 - cl[1] / cl[3]) / 2 * cr.height + cr.top - rr.top;
      el.style.setProperty('--x', X.toFixed(1) + 'px');
      el.style.setProperty('--y', Y.toFixed(1) + 'px');
    }

    const dalej = wyglad.alfa > 0.004 || st.alfa > 0.004;
    if (dalej && !document.hidden) planuj();
    else { dziala = false; canvas.style.visibility = 'hidden'; }
  };
  const planuj = () => { if (!klatkaId) klatkaId = requestAnimationFrame(klatka); };
  const obudz = () => {
    if (!gotowy) return;
    if (!dziala) { dziala = true; canvas.style.visibility = ''; ost = 0; }
    planuj();
  };
  addEventListener('scroll', obudz, { passive: true });
  addEventListener('resize', () => { obudz(); clearTimeout(zbudujTekst.t); zbudujTekst.t = setTimeout(zbudujTekst, 200); });
  document.addEventListener('visibilitychange', obudz);
  addEventListener('pointermove', obudz, { passive: true });
  if (pauza) new MutationObserver(obudz).observe(pauza, { attributes: true, attributeFilter: ['aria-pressed'] });
  if (wystep) new MutationObserver(obudz).observe(wystep, { attributes: true, attributeFilter: ['data-poza'] });
  ruchMq.addEventListener?.('change', (e) => { reduce = e.matches; obudz(); });

  const dane = wczytaj(); // od razu: plik idzie równolegle z resztą strony, rysowanie rusza po załadowaniu
  dane.catch(() => {});
  const start = async () => {
    try {
      await dane;
    } catch (e) { bez3d(); return; }
    document.body.append(canvas);
    html.classList.add('z-3d');
    gotowy = true; dziala = true;
    html.dataset.robot = 'gotowy';
    planuj();
    zbudujTekst();
    if (!reduce) setTimeout(() => gest('macha', 2.6), 2300);
  };
  start();

  // Podgląd do strojenia (tylko z ?robot-debug).
  if (/[?&]robot-debug/.test(location.search)) {
    window.__robot = { POZY, BAZA, IDX: () => IDX, ustaw: (n) => { gestNazwa = n; gestDo = 1e9; obudz(); }, q: () => q,
      orbita: (v) => { dbgOrbita = v; obudz(); }, katy: (o) => { dbgKaty = o; obudz(); } };
  }
})();
