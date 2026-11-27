// SNAP SURF TRIPS · formularios → api/enquiry.php · popup · UTM sin cookies · consentimiento de analítica (solo si hay GA)
(function () {
  var B = document.body.dataset, dlg = document.getElementById('ok');
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

  // contador propio sin cookies (solo en el servidor real)
  if (!DEMO && navigator.sendBeacon) try { navigator.sendBeacon(B.api.replace('enquiry.php', 'hit.php'), JSON.stringify({ p: location.pathname, s: utm.utm_source || '', r: document.referrer })); } catch (e) {}

  function bindCopy(b) {
    b.addEventListener('click', function () { var t = b.textContent; (navigator.clipboard ? navigator.clipboard.writeText(b.dataset.copy) : Promise.reject()).then(function () { b.textContent = '✓'; setTimeout(function () { b.textContent = t; }, 1600); }).catch(function () { prompt('', b.dataset.copy); }); });
  }
  document.querySelectorAll('[data-copy]').forEach(bindCopy);

  // Buscador de surf trip: puntuación transparente con los datos de cada destino (mdata)
  var mf = document.getElementById('matcher'), mr = document.getElementById('mres');
  if (mf) {
    var M = JSON.parse(document.getElementById('mdata').textContent), T = M.t;
    var score = function (k, a) {
      var D = M.d[k], s = 50, why = [], no = [], size = +a.size, mo = +a.month;
      if (size > D.max) no.push('big');
      if (a.who === 'school' && !D.minors) no.push('noMinors');
      if (mo && (D.months.indexOf(mo) < 0 || (size >= 20 && D.groupClosed.indexOf(mo) >= 0))) no.push('closed');
      if (no.length) return { k: k, s: 0, why: no };
      why.push('size'); if (mo) { why.push('month'); s += 10; }
      if (a.who === 'school') { why.push('minors'); s += 10; }
      s += D.vibe[a.vibe] || 0;
      if ((a.level === 'never' || a.level === 'beginner' || a.vibe === 'learn') && D.lessons) { why.push('lessons'); s += 10; }
      if ((a.vibe === 'work' || a.who === 'company') && D.vibe.work >= 10) why.push('work');
      if ((D.vibe[a.vibe] || 0) >= 20) why.push('vibe');
      return { k: k, s: Math.min(99, s), why: why };
    };
    var esc = function (t) { var d = document.createElement('div'); d.textContent = t; return d.innerHTML; };
    var show = function (a, shared) {
      var res = Object.keys(M.d).map(function (k) { return score(k, a); }).sort(function (x, y) { return y.s - x.s; });
      var best = res[0], html = '';
      if (!best.s) { html = '<p class="lead">' + esc(T.none) + '</p><a class="btn btn-ink" href="' + M.u.contact + '">' + (M.lang === "es" ? "Contactar" : "Contact us") + '</a>'; }
      else {
        var link = location.origin + location.pathname + '?r=' + best.k;
        html = '<article class="mcard"><p class="kicker">' + (shared ? '★ ' : '') + Math.round(best.s) + '% match</p><h2 class="mega">' + esc(T[best.k]) + '</h2><p class="kicker">' + esc(T.why) + '</p><ul>' +
          best.why.map(function (w) { return '<li>✓ ' + esc(T.r[w]) + '</li>'; }).join('') + '</ul><div class="row">' +
          '<a class="btn btn-accent" href="#enquire" id="mgo">' + (M.lang === 'es' ? 'Pedir mi propuesta' : 'Request my proposal') + '</a>' +
          '<a class="btn" href="' + M.u[best.k] + '">' + (M.lang === 'es' ? 'Ver el destino' : 'See the destination') + '</a></div>' +
          '<div class="row"><a class="btn sm" rel="noopener" href="https://wa.me/?text=' + encodeURIComponent((M.lang === 'es' ? 'Mi surf trip ideal: ' : 'My surf trip match: ') + T[best.k] + ' ' + link) + '">WhatsApp</a>' +
          '<button class="btn sm" type="button" data-copy="' + link + '">' + (M.lang === 'es' ? 'Copiar enlace' : 'Copy link') + '</button></div></article>';
        var alt = res[1];
        if (alt && alt.s) html += '<p class="kicker">' + esc(T.alt) + ': <a href="' + M.u[alt.k] + '">' + esc(T[alt.k]) + '</a> · ' + Math.round(alt.s) + '%</p>';
        var f = document.querySelector('#enquire form'), set = function (n, v) { var i = f.querySelector('[name=' + n + ']'); if (i) i.value = v; };
        set('listingId', M.d[best.k].listing); set('people', a.size); set('dates', a.month === '0' ? 'flexible' : a.month); set('level', a.level || ''); set('groupType', a.who || '');
        f.dataset.type = +a.size >= 20 ? 'group' : 'individual'; window.__match = a; document.getElementById('enquire').hidden = false;
      }
      mr.innerHTML = html; mr.hidden = false;
      mr.querySelectorAll('[data-copy]').forEach(bindCopy);
      mr.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
      if (window.gtag) window.gtag('event', 'matcher_result', { destination: best.k });
    };
    mf.addEventListener('submit', function (ev) {
      ev.preventDefault(); var a = {}, miss = null;
      ['who', 'size', 'month', 'level', 'vibe'].forEach(function (n) { var c = mf.querySelector('[name=' + n + ']:checked'); if (c) a[n] = c.value; else if (!miss) miss = mf.querySelector('[name=' + n + ']'); });
      if (miss) { miss.closest('fieldset').scrollIntoView({ block: 'center' }); miss.focus(); return; }
      show(a, false);
    });
    var r = new URLSearchParams(location.search).get('r');
    if (r && M.d[r]) { mr.innerHTML = '<article class="mcard"><p class="kicker">★ ' + (M.lang === 'es' ? 'Te han compartido este destino' : 'A friend shared this match') + '</p><h2 class="mega">' + esc(T[r]) + '</h2><div class="row"><a class="btn btn-accent" href="#matcher">' + (M.lang === 'es' ? 'Haz tu test' : 'Take the test') + '</a><a class="btn" href="' + M.u[r] + '">' + (M.lang === 'es' ? 'Ver el destino' : 'See the destination') + '</a></div></article>'; mr.hidden = false; }
  }

  var mb = document.querySelector('.menu-btn'), mn = document.getElementById('mainnav');
  if (mb) mb.addEventListener('click', function () { var o = mn.classList.toggle('open'); mb.setAttribute('aria-expanded', o); });

  // aparición suave al hacer scroll (sin efecto si el usuario pide menos movimiento)
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('main > section:not(.hero):not(.ticker), .three > *, .packs article, .gallery .ph').forEach(function (el) { el.classList.add('rv'); io.observe(el); });
  }

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

  var newKey = function () { try { return crypto.randomUUID(); } catch (e) { return Date.now().toString(36) + Math.random().toString(36).slice(2, 12); } };

  // Selector de destino de grupos: rellena listingId y respeta ?d=sagres|bali
  document.querySelectorAll('select[data-dest]').forEach(function (s) {
    var h = s.form && s.form.querySelector('[name=listingId]');
    var apply = function () { var o = s.options[s.selectedIndex]; if (h) h.value = (o && o.getAttribute('data-listing')) || ''; };
    var q = new URLSearchParams(location.search).get('d');
    if (q) for (var i = 0; i < s.options.length; i++) if (s.options[i].getAttribute('data-key') === q) { s.selectedIndex = i; break; }
    s.addEventListener('change', apply);
    if (s.form) s.form.addEventListener('reset', function () { setTimeout(apply, 0); });
    apply();
  });

  // Token antispam: se pide al empezar a rellenar el formulario (los robots que solo envían la petición no lo tienen)
  var tok = null, tokP = null, tokAt = 0;
  var getTok = function () {
    if (tokP) return tokP;
    tokP = fetch(B.api.replace('enquiry.php', 'token.php'), { cache: 'no-store' }).then(function (r) { return r.json(); })
      .then(function (j) { tok = j.t; tokAt = Date.now(); return tok; }).catch(function () { tokP = null; tok = ''; tokAt = Date.now(); return ''; });
    return tokP;
  };

  document.querySelectorAll('form.enq').forEach(function (f) {
    var key = newKey();   // misma clave en los reintentos del mismo envío; nueva tras un envío correcto
    if (!DEMO) ['focusin', 'pointerdown', 'keydown'].forEach(function (n) { f.addEventListener(n, function () { getTok(); }, { once: true }); });
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

      var d = { type: f.dataset.type, page: location.pathname, lang: document.documentElement.lang, utm: utm, idemKey: key };
      new FormData(f).forEach(function (v, k) { d[k] = typeof v === 'string' ? v.trim() : v; });
      d.consent = !!f.querySelector('[name=consent]').checked;
      d.marketing = !!f.querySelector('[name=marketing]').checked;
      d.flexible = !!(f.querySelector('[name=flexible]') || {}).checked;
      if (window.__match && f.closest('#enquire') && document.getElementById('matcher')) d.matcher = window.__match;

      if (DEMO) { showOk('DEMO'); return; }
      btn.disabled = true;
      var send = function (retry) {
        // el servidor exige un token firmado con al menos 4 s de antigüedad: se espera lo que falte (casi nunca hace falta)
        return getTok().then(function () { return new Promise(function (r) { setTimeout(r, Math.max(0, 4300 - (Date.now() - tokAt))); }); })
          .then(function () { d.tok = tok; return fetch(B.api, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(d) }); })
          .then(function (r) { return r.json().then(function (j) { return { s: r.status, j: j }; }); })
          .then(function (x) {
            tok = null; tokP = null;   // un token solo vale una vez
            if (x.s === 409 && x.j.error === 'token' && !retry) return send(true);   // token caducado o ya usado: pide otro y reintenta una vez
            if (x.s === 200 && x.j.ok) {
              f.reset(); key = newKey(); showOk(x.j.id);
              if (window.gtag) window.gtag('event', 'enquiry_submitted', { enquiry_type: d.type });
            } else { throw new Error(x.j.error || 'error'); }
          });
      };
      send(false)
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
