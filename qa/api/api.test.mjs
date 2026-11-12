// Testy publicznego API i serwera MCP (api/index.php) — lokalnie, z atrapą odbiorcy formularza.
// Żadne zgłoszenie nie wychodzi poza ten komputer: zmienna API_33BOTS_ODBIORCA kieruje je do atrapy.
//   node --test qa/api/api.test.mjs
import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { mkdtempSync, readFileSync, existsSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const TU = dirname(fileURLToPath(import.meta.url));
const KORZEN = join(TU, '..', '..');
const procesy = [];
const dziennik = join(mkdtempSync(join(tmpdir(), 'api33-')), 'zgloszenia.jsonl');
writeFileSync(dziennik, '');

function php(port, odbiorca) {
  const p = spawn('php', ['-S', `127.0.0.1:${port}`, join(TU, 'router.php')], {
    cwd: KORZEN, stdio: 'ignore',
    env: { ...process.env, API_33BOTS_ODBIORCA: odbiorca, TMPDIR: mkdtempSync(join(tmpdir(), 'api33-limit-')) },
  });
  procesy.push(p);
  return `http://127.0.0.1:${port}`;
}
async function czekaj(adres) {
  for (let i = 0; i < 80; i++) {
    try { await fetch(adres); return; } catch { await new Promise((r) => setTimeout(r, 100)); }
  }
  throw new Error(`serwer nie wstał: ${adres}`);
}
const przekazane = () => readFileSync(dziennik, 'utf8').split('\n').filter(Boolean).map((l) => JSON.parse(l));
const post = (adres, cialo, naglowki = {}) => fetch(adres, {
  method: 'POST', headers: { 'Content-Type': 'application/json', ...naglowki },
  body: typeof cialo === 'string' ? cialo : JSON.stringify(cialo),
});
const jutro = new Date(Date.now() + 14 * 86400e3).toISOString().slice(0, 10);
const DOBRE = { imie: 'Anna Testowa', email: 'anna@example.com', telefon: '+48 600 000 000', firma: 'Przykład sp. z o.o.',
  data: jutro, miejsce: 'Warszawa, EXPO XXI', rodzaj: 'targi', goscie: '500', opis: 'Dwa dni targów, robot przy stoisku.', zgoda: true };

let A, B, C;
before(async () => {
  procesy.push(spawn('python3', [join(TU, 'odbiorca.py'), '8191', dziennik], { stdio: 'ignore' }));
  A = php(8190, 'http://127.0.0.1:8191/f/test');
  B = php(8192, 'http://127.0.0.1:8191/f/test');
  C = php(8193, 'http://127.0.0.1:8199/f/nikogo');   // nikt nie słucha → błąd przekazania
  await Promise.all([czekaj(`${A}/api/`), czekaj(`${B}/api/`), czekaj(`${C}/api/`)]);
  for (let i = 0; i < 80 && !existsSync(dziennik); i++) await new Promise((r) => setTimeout(r, 50));
  await new Promise((r) => setTimeout(r, 400));
});
after(() => procesy.forEach((p) => p.kill()));

test('opis API: zasoby, wersja, informacje o ofercie', async () => {
  const r = await fetch(`${A}/api/`);
  assert.equal(r.status, 200);
  assert.match(r.headers.get('content-type'), /application\/json/);
  assert.equal(r.headers.get('x-robots-tag'), 'noindex');
  const d = await r.json();
  assert.ok(d.zasoby['POST /api/zapytania'] && d.zasoby['GET /api/wycena'] && d.zasoby['POST /mcp']);
  assert.equal(d.informacje.ceny.pl.pelny_dzien_od, 5500);
  assert.equal(d.informacje.kontakt.telefon, '+48 531 408 004');
});

test('wycena: ceny jak na stronach, rabat 15% od dwóch dni, krótki pokaz bez kwoty', async () => {
  const w = async (q) => (await fetch(`${A}/api/wycena${q}`)).json();
  assert.deepEqual([(await w('')).kwota_od, (await w('')).waluta, (await w('')).podatek], [5500, 'PLN', 'netto']);
  assert.equal((await w('?dni=2')).kwota_od, 9350);
  assert.equal((await w('?dni=2')).rabat_procent, 15);
  assert.equal((await w('?rynek=de&dni=3')).kwota_od, 6375);
  assert.deepEqual([(await w('?rynek=at')).kwota_od, (await w('?rynek=at')).podatek], [2300, 'netto']);
  assert.equal((await w('?rynek=lt')).kwota_od, 2100);
  const k = await w('?krotki=1');
  assert.equal(k.kwota_od, null);
  assert.match(k.opis, /indywidualnie/);
  assert.equal((await fetch(`${A}/api/wycena?rynek=fr`)).status, 422);
  assert.equal((await fetch(`${A}/api/wycena?dni=0`)).status, 422);
  assert.equal((await fetch(`${A}/api/wycena?dni=abc`)).status, 422);
});

test('zapytanie: poprawne trafia do odbiorcy z tymi samymi nazwami pól co formularz na stronie', async () => {
  const przed = przekazane().length;
  const r = await post(`${A}/api/zapytania`, DOBRE);
  assert.equal(r.status, 201);
  assert.equal((await r.json()).status, 'przyjete');
  const z = przekazane();
  assert.equal(z.length, przed + 1);
  const { pola, origin } = z.at(-1);
  assert.deepEqual(Object.keys(pola).sort(), ['company', 'date', 'email', 'event_type', 'guests', 'location', 'message', 'name', 'phone']);
  assert.equal(pola.name, 'Anna Testowa');
  assert.equal(pola.email, 'anna@example.com');
  assert.equal(pola.date, jutro);
  assert.match(pola.message, /^\[Zgłoszenie przez API · rynek: Polska\]\nDwa dni targów/);
  assert.equal(origin, 'https://33bots.pl');
});

test('zapytanie: błędne dane dają 422 i nic nie wychodzi', async () => {
  const przed = przekazane().length;
  const zle = [
    [{ ...DOBRE, zgoda: undefined }, 'zgoda'], [{ ...DOBRE, zgoda: 'tak' }, 'zgoda'],
    [{ ...DOBRE, email: 'nie-mail' }, 'email'], [{ ...DOBRE, imie: 'A' }, 'imie'],
    [{ ...DOBRE, data: '2020-01-01' }, 'data'], [{ ...DOBRE, data: '31.12.2030' }, 'data'],
    [{ ...DOBRE, telefon: 'zadzwoń' }, 'telefon'], [{ ...DOBRE, rynek: 'us' }, 'rynek'],
    [{ ...DOBRE, opis: 'http://a http://b http://c http://d' }, 'opis'],
  ];
  for (const [cialo, pole] of zle) {
    const r = await post(`${A}/api/zapytania`, cialo);
    assert.equal(r.status, 422, pole);
    assert.ok((await r.json()).pola[pole], pole);
  }
  assert.equal(przekazane().length, przed);
});

test('zapytanie: pole-pułapka, zły JSON, za duże żądanie, zła metoda', async () => {
  const przed = przekazane().length;
  const pulapka = await post(`${A}/api/zapytania`, { ...DOBRE, website: 'http://spam.example' });
  assert.equal(pulapka.status, 201);
  assert.equal((await post(`${A}/api/zapytania`, '{nie json')).status, 400);
  assert.equal((await post(`${A}/api/zapytania`, { ...DOBRE, opis: 'x'.repeat(20000) })).status, 413);
  const get = await fetch(`${A}/api/zapytania`);
  assert.equal(get.status, 405);
  assert.match(get.headers.get('allow'), /POST/);
  assert.equal((await fetch(`${A}/api/nic`)).status, 404);
  assert.equal(przekazane().length, przed);
});

test('zapytanie: data „nieustalony” i same pola wymagane przechodzą; puste pola idą jako „—”', async () => {
  const r = await post(`${A}/api/zapytania`, { imie: 'Jan Minimalny', email: 'jan@example.com', data: 'nieustalony', zgoda: true, rynek: 'de' });
  assert.equal(r.status, 201);
  const { pola } = przekazane().at(-1);
  assert.equal(pola.date, 'nieustalony');
  assert.deepEqual([pola.company, pola.phone, pola.location, pola.event_type, pola.guests], ['—', '—', '—', '—', '—']);
  assert.match(pola.message, /rynek: Deutschland/);
});

test('ograniczenie: szóste zapytanie w godzinie z jednego adresu dostaje 429 i nie wychodzi', async () => {
  const przed = przekazane().length;
  for (let i = 0; i < 5; i++) assert.equal((await post(`${B}/api/zapytania`, DOBRE)).status, 201, `zapytanie ${i + 1}`);
  const r = await post(`${B}/api/zapytania`, DOBRE);
  assert.equal(r.status, 429);
  assert.match((await r.json()).opis, /\+48 531 408 004/);
  assert.equal(przekazane().length, przed + 5);
});

test('odbiorca nie odpowiada: 502 z telefonem i adresem e-mail zamiast cichej utraty', async () => {
  const r = await post(`${C}/api/zapytania`, DOBRE);
  assert.equal(r.status, 502);
  const d = await r.json();
  assert.equal(d.blad, 'nie_przekazano');
  assert.match(d.opis, /\+48 531 408 004.*kontakt@33bots\.pl/);
});

const rpc = (adres, id, method, params) => post(`${adres}/mcp`, { jsonrpc: '2.0', id, method, params });

test('MCP: initialize, wersje protokołu, powiadomienia, ping, nieznana metoda', async () => {
  const i = await (await rpc(A, 1, 'initialize', { protocolVersion: '2025-03-26', capabilities: {}, clientInfo: { name: 'test', version: '1' } })).json();
  assert.equal(i.result.protocolVersion, '2025-03-26');
  assert.equal(i.result.serverInfo.name, '33bots');
  assert.ok(i.result.capabilities.tools);
  const nowa = await (await rpc(A, 2, 'initialize', { protocolVersion: '2099-01-01' })).json();
  assert.equal(nowa.result.protocolVersion, '2025-06-18');
  const pow = await post(`${A}/mcp`, { jsonrpc: '2.0', method: 'notifications/initialized' });
  assert.equal(pow.status, 202);
  assert.equal(await pow.text(), '');
  assert.deepEqual((await (await rpc(A, 3, 'ping')).json()).result, {});
  assert.equal((await (await rpc(A, 4, 'resources/list')).json()).error.code, -32601);
  assert.equal((await (await post(`${A}/mcp`, { id: 5, method: 'ping' })).json()).error.code, -32600);
  const get = await fetch(`${A}/mcp`);
  assert.equal(get.status, 405);
  const opt = await fetch(`${A}/mcp`, { method: 'OPTIONS' });
  assert.equal(opt.status, 204);
  assert.equal(opt.headers.get('access-control-allow-origin'), '*');
});

test('MCP: lista narzędzi ze schematami; get_quote i get_offer_info tylko czytają', async () => {
  const l = await (await rpc(A, 1, 'tools/list')).json();
  const nazwy = l.result.tools.map((t) => t.name);
  assert.deepEqual(nazwy, ['get_offer_info', 'get_quote', 'request_quote']);
  for (const t of l.result.tools) assert.equal(t.inputSchema.type, 'object');
  const rq = l.result.tools[2];
  assert.deepEqual(rq.inputSchema.required, ['imie', 'email', 'zgoda']);
  assert.equal(rq.annotations.readOnlyHint, false);
  assert.equal(l.result.tools[1].annotations.readOnlyHint, true);
  assert.deepEqual(JSON.parse(JSON.stringify(l.result.tools[0].inputSchema.properties)), {});

  const q = await (await rpc(A, 2, 'tools/call', { name: 'get_quote', arguments: { rynek: 'pl', dni: 2 } })).json();
  assert.equal(q.result.isError, false);
  assert.equal(q.result.structuredContent.kwota_od, 9350);
  assert.match(q.result.content[0].text, /9 350 PLN netto/);
  const zly = await (await rpc(A, 3, 'tools/call', { name: 'get_quote', arguments: { dni: 99 } })).json();
  assert.equal(zly.result.isError, true);
  const info = await (await rpc(A, 4, 'tools/call', { name: 'get_offer_info', arguments: {} })).json();
  assert.equal(info.result.structuredContent.ceny.de.pelny_dzien_od, 2500);
  const nie = await (await rpc(A, 5, 'tools/call', { name: 'usun_wszystko', arguments: {} })).json();
  assert.equal(nie.result.isError, true);
  assert.equal((await (await rpc(A, 6, 'tools/call', {})).json()).error.code, -32602);
});

test('MCP: request_quote bez zgody nic nie wysyła; ze zgodą przekazuje zapytanie z dopiskiem o asystencie', async () => {
  const przed = przekazane().length;
  const bez = await (await rpc(A, 1, 'tools/call', { name: 'request_quote', arguments: { imie: 'Ewa Nowak', email: 'ewa@example.com' } })).json();
  assert.equal(bez.result.isError, true);
  assert.match(bez.result.content[0].text, /zgoda/);
  assert.equal(przekazane().length, przed);
  const ok = await (await rpc(A, 2, 'tools/call', { name: 'request_quote', arguments: { imie: 'Ewa Nowak', email: 'ewa@example.com', miejsce: 'Wien', rynek: 'at', zgoda: true } })).json();
  assert.equal(ok.result.isError, false);
  assert.equal(ok.result.structuredContent.status, 'przyjete');
  assert.equal(ok.result.structuredContent.kontakt.email, 'kontakt@33bots.at');
  const { pola } = przekazane().at(-1);
  assert.match(pola.message, /^\[Zgłoszenie przez asystenta AI \(MCP\) · rynek: Österreich\]/);
  assert.equal(pola.location, 'Wien');
});

test('MCP: paczka wiadomości wraca jako lista odpowiedzi bez powiadomień', async () => {
  const r = await post(`${A}/mcp`, [
    { jsonrpc: '2.0', id: 'a', method: 'ping' },
    { jsonrpc: '2.0', method: 'notifications/initialized' },
    { jsonrpc: '2.0', id: 'b', method: 'tools/list' },
  ]);
  const d = await r.json();
  assert.deepEqual(d.map((o) => o.id), ['a', 'b']);
});
