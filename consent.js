/* Cookie-Einwilligung nach § 25 TDDDG und Art. 6 DSGVO.
   Analyse-Dienste (Google Tag Manager, Albacross) werden erst nach
   ausdruecklicher Einwilligung geladen. Ohne Einwilligung laeuft die
   Website vollstaendig ohne diese Dienste. */
(function () {
  'use strict';
  var KEY = 'consent-v1';
  var loaded = false;

  function read() {
    try { return JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) { return null; }
  }
  function write(v) {
    try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) { /* Speicher gesperrt */ }
  }

  function loadAnalytics() {
    if (loaded) return;
    loaded = true;
    var id = window.__gtmId;
    if (id) {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });
      var g = document.createElement('script');
      g.async = true;
      g.src = 'https://www.googletagmanager.com/gtm.js?id=' + id;
      document.head.appendChild(g);
    }
    if (window.__albacrossId) {
      window._nQc = window.__albacrossId;
      var a = document.createElement('script');
      a.async = true;
      a.src = 'https://serve.albacross.com/track.js';
      document.head.appendChild(a);
    }
  }

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  var stored = read();
  if (stored && stored.analytics) loadAnalytics();

  ready(function () {
    var banner = document.getElementById('consentBanner');
    if (!banner) return;
    var options = document.getElementById('consentOptions');
    var analytics = document.getElementById('consentAnalytics');
    var btnAll = document.getElementById('consentAcceptAll');
    var btnNone = document.getElementById('consentRejectAll');
    var btnSettings = document.getElementById('consentSettings');
    var btnSave = document.getElementById('consentSave');
    var reopen = document.getElementById('consentReopen');

    function show() {
      banner.hidden = false;
      var s = read();
      if (analytics) analytics.checked = !!(s && s.analytics);
    }
    function decide(useAnalytics) {
      write({ analytics: !!useAnalytics, ts: Date.now() });
      if (useAnalytics) loadAnalytics();
      banner.hidden = true;
    }

    if (!stored) show();

    if (btnAll) btnAll.addEventListener('click', function () { decide(true); });
    if (btnNone) btnNone.addEventListener('click', function () { decide(false); });
    if (btnSettings) btnSettings.addEventListener('click', function () {
      if (options) options.hidden = false;
      btnSettings.hidden = true;
      if (btnSave) btnSave.hidden = false;
    });
    if (btnSave) btnSave.addEventListener('click', function () {
      decide(analytics && analytics.checked);
    });
    if (reopen) reopen.addEventListener('click', function (e) {
      e.preventDefault();
      if (options) options.hidden = false;
      if (btnSettings) btnSettings.hidden = true;
      if (btnSave) btnSave.hidden = false;
      show();
      banner.scrollIntoView({ block: 'nearest' });
    });
  });
})();
