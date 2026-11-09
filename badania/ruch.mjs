// Czy robot na żywej stronie sam się rusza: kąty stawów co sekundę przez 15 s na przyklejonej scenie.
import { chromium } from 'playwright';
import fs from 'node:fs';
const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
const bledy = []; p.on('pageerror', (e) => bledy.push(e.message));
await p.goto('https://33bots.pl/?robot-debug&k=' + Date.now(), { waitUntil: 'load' });
await p.evaluate(() => { const r = document.getElementById('robot'); scrollTo({ top: scrollY + r.getBoundingClientRect().top + 10, behavior: 'instant' }); });
await p.waitForFunction(() => document.documentElement.dataset.robot === 'gotowy', null, { timeout: 40000 });
const probki = [];
for (let i = 0; i < 15; i++) {
  await p.waitForTimeout(1000);
  probki.push(await p.evaluate(() => { const q = window.__robot.q(), I = window.__robot.IDX(); return { prawyBark: +q[I.right_shoulder_pitch_joint].toFixed(2), lewyBark: +q[I.left_shoulder_pitch_joint].toFixed(2), pas: +q[I.waist_yaw_joint].toFixed(2), dymek: document.getElementById('robotDymek').textContent.slice(0, 20) }; }));
  if (i === 6) await p.screenshot({ path: 'badania/wyniki/zywo/ruch.png' });
}
const wynik = { bledy, probki, zakres: ['prawyBark', 'lewyBark', 'pas'].map((k) => Math.max(...probki.map((x) => x[k])) - Math.min(...probki.map((x) => x[k]))) };
fs.writeFileSync('badania/wyniki/zywo/ruch.json', JSON.stringify(wynik, null, 1));
console.log(JSON.stringify(wynik));
await b.close();
