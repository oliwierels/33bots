/* Barrierefreiheit-Panel (BFSG).
   Einstellungen werden ausschliesslich lokal im Browser gespeichert
   (localStorage) und nicht an den Server uebertragen. */
(function () {
  'use strict';
  var KEY = 'a11y-prefs';
  var DEFAULTS = { font: 'normal', theme: 'dark', contrast: 'normal', motion: 'on' };
  var root = document.documentElement;

  function load() {
    try { return Object.assign({}, DEFAULTS, JSON.parse(localStorage.getItem(KEY) || '{}')); }
    catch (e) { return Object.assign({}, DEFAULTS); }
  }
  function save(p) {
    try { localStorage.setItem(KEY, JSON.stringify(p)); } catch (e) { /* Speicher gesperrt */ }
  }
  function apply(p) {
    root.setAttribute('data-a11y-font', p.font);
    root.setAttribute('data-a11y-theme', p.theme);
    root.setAttribute('data-a11y-contrast', p.contrast);
    root.setAttribute('data-a11y-motion', p.motion);
    document.querySelectorAll('.a11y-opt').forEach(function (b) {
      b.setAttribute('aria-pressed', String(p[b.dataset.a11y] === b.dataset.value));
    });
  }

  var prefs = load();
  apply(prefs);

  var toggle = document.getElementById('a11yToggle');
  var panel = document.getElementById('a11yPanel');
  if (!toggle || !panel) return;

  function open(state) {
    panel.hidden = !state;
    toggle.setAttribute('aria-expanded', String(state));
    toggle.setAttribute('aria-label', state
      ? 'Barrierefreiheit-Einstellungen schliessen'
      : 'Barrierefreiheit-Einstellungen oeffnen');
    if (state) { var f = panel.querySelector('.a11y-opt'); if (f) f.focus(); }
  }

  toggle.addEventListener('click', function () { open(panel.hidden); });

  panel.addEventListener('click', function (e) {
    var btn = e.target.closest('.a11y-opt');
    if (!btn) return;
    prefs[btn.dataset.a11y] = btn.dataset.value;
    save(prefs);
    apply(prefs);
  });

  var reset = document.getElementById('a11yReset');
  if (reset) reset.addEventListener('click', function () {
    prefs = Object.assign({}, DEFAULTS);
    save(prefs);
    apply(prefs);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !panel.hidden) { open(false); toggle.focus(); }
  });
  document.addEventListener('click', function (e) {
    if (!panel.hidden && !panel.contains(e.target) && !toggle.contains(e.target)) open(false);
  });
})();
