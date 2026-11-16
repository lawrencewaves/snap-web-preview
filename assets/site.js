// SNAP SURF TRIPS · formularios → api/enquiry.php · popup · UTM sin cookies · consentimiento de analítica (solo si hay GA)
(function () {
  var B = document.body.dataset, dlg = document.getElementById('ok'), t0 = Date.now();
  var DEMO = location.protocol === 'file:' || /github\.io$/.test(location.hostname); // vista previa en local: enseña el popup sin enviar nada

  // UTM: sin cookies ni almacenamiento. Se leen de la URL y se propagan en los enlaces internos.
  var utm = {}, qs = [];
  new URLSearchParams(location.search).forEach(function (v, k) { if (/^utm_[a-z]{2,10}$/.test(k)) { utm[k] = v.slice(0, 120); qs.push(k + '=' + encodeURIComponent(utm[k])); } });
  if (qs.length) document.querySelectorAll('a[href]').forEach(function (a) {
    var h = a.getAttribute('href');
    if (/^(https?:|mailto:|tel:|#)/.test(h)) return;
    var p = h.split('#');
    a.setAttribute('href', p[0] + (p[0].indexOf('?') < 0 ? '?' : '&') + qs.join('&') + (p[1] ? '#' + p[1] : ''));
  });

  var mb = document.querySelector('.menu-btn'), mn = document.getElementById('mainnav');
  if (mb) mb.addEventListener('click', function () { var o = mn.classList.toggle('open'); mb.setAttribute('aria-expanded', o); });

  document.querySelectorAll('[data-pack]').forEach(function (a) {
    a.addEventListener('click', function () {
      var h = document.querySelector('input[name=packageId]'), n = document.querySelector('select[name=nights]');
      if (h) h.value = a.dataset.pack;
      if (n) n.value = a.dataset.pack.charAt(0);
    });
  });

  function showOk(id) {
    document.getElementById('ok-ref').textContent = id ? B.ref + ': ' + id : '';
    if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', '');
  }
  document.getElementById('ok-x').addEventListener('click', function () { dlg.close ? dlg.close() : dlg.removeAttribute('open'); });

  document.querySelectorAll('form.enq').forEach(function (f) {
    f.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var err = f.querySelector('.err'), btn = f.querySelector('button[type=submit]'), bad = null;
      err.hidden = true;
      f.querySelectorAll('[required]').forEach(function (el) {
        var ok = el.type === 'checkbox' ? el.checked : el.value.trim() !== '' && el.checkValidity();
        el.setAttribute('aria-invalid', ok ? 'false' : 'true');
        if (!ok && !bad) bad = el;
      });
      if (bad) { err.textContent = B.req; err.hidden = false; bad.focus(); return; }

      var d = { type: f.dataset.type, page: location.pathname, lang: document.documentElement.lang, utm: utm, elapsed: Math.round((Date.now() - t0) / 1000) };
      new FormData(f).forEach(function (v, k) { d[k] = typeof v === 'string' ? v.trim() : v; });
      d.consent = !!f.querySelector('[name=consent]').checked;
      d.marketing = !!f.querySelector('[name=marketing]').checked;
      d.flexible = !!(f.querySelector('[name=flexible]') || {}).checked;

      if (DEMO) { showOk('DEMO'); return; }
      btn.disabled = true;
      fetch(B.api, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(d) })
        .then(function (r) { return r.json().then(function (j) { return { s: r.status, j: j }; }); })
        .then(function (x) {
          if (x.s === 200 && x.j.ok) {
            f.reset(); showOk(x.j.id);
            if (window.gtag) window.gtag('event', 'enquiry_submitted', { enquiry_type: d.type });
          } else { throw new Error(x.j.error || 'error'); }
        })
        .catch(function () { err.textContent = B.fail; err.hidden = false; }) // nunca «recibida» sin confirmación del servidor
        .then(function () { btn.disabled = false; });
    });
  });

  // Analítica: solo existe si se configura GA_ID en build.py. Nada se carga antes de «Aceptar».
  if (B.ga) {
    var ck = document.getElementById('ck'), KEY = 'snap_consent', c = null;
    try { c = JSON.parse(localStorage.getItem(KEY)); } catch (e) {}
    if (c && Date.now() - c.t > 31536e6) c = null; // se vuelve a preguntar a los 12 meses
    function loadGA() {
      var s = document.createElement('script'); s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + B.ga; document.head.appendChild(s);
      window.dataLayer = window.dataLayer || []; window.gtag = function () { window.dataLayer.push(arguments); };
      window.gtag('js', new Date()); window.gtag('config', B.ga, { anonymize_ip: true });
    }
    if (!c) ck.hidden = false; else if (c.v === 1) loadGA();
    ck.querySelectorAll('[data-ck]').forEach(function (b) {
      b.addEventListener('click', function () {
        var v = +b.dataset.ck, was = c && c.v;
        try { localStorage.setItem(KEY, JSON.stringify({ v: v, t: Date.now() })); } catch (e) {}
        ck.hidden = true;
        if (v === 1 && !window.gtag) loadGA();
        if (v === 0 && was === 1) location.reload(); // retirar el consentimiento deja de cargar la analítica
      });
    });
    var o = document.getElementById('ck-open');
    if (o) o.addEventListener('click', function (e) { e.preventDefault(); ck.hidden = false; });
  }
})();
