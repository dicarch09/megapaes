// == paes27-core v3 ==
// Bloque compartido. Se copia IDÉNTICO en cada página con tools/sync_core.py.
// No lo edites dentro de un HTML: edita tools/core.js y vuelve a sincronizar.
const P27 = (() => {
  'use strict';
  const VERSION = 3;
  const K = { diag: 'paes27:diag', dominio: 'paes27:dominio', repaso: 'paes27:repaso', ruta: 'paes27:ruta', ensayos: 'paes27:ensayos' };

  const PRUEBAS = {
    M2:  { id: 'M2',  corto: 'M2',      nombre: 'Matemática 2 (M2)',     fecha: '2026-11-30', hora: '15:00', prior: 30, peso: 1.2 },
    LEN: { id: 'LEN', corto: 'Lectora', nombre: 'Competencia Lectora',   fecha: '2026-12-01', hora: '09:00', prior: 50, peso: 0.6 },
    CIE: { id: 'CIE', corto: 'Física',  nombre: 'Ciencias Física',       fecha: '2026-12-01', hora: '15:00', prior: 30, peso: 1.0 },
    M1:  { id: 'M1',  corto: 'M1',      nombre: 'Matemática 1 (M1)',     fecha: '2026-12-02', hora: '09:00', prior: 60, peso: 0.7 },
  };

  // [id, prueba, eje, prio, nombre, lección (página#ancla) o null]
  const LISTA = [
    ['m2.alg.sistemas-rectas', 'M2', 'Álgebra y funciones', 'A', 'Rectas en el plano + sistemas 2×2', 'm2.html#m2.alg.sistemas-rectas'],
    ['m2.num.log-exp', 'M2', 'Números', 'A', 'Logaritmos + función exponencial y logarítmica', 'm2.html#m2.num.log-exp'],
    ['m2.pro.condicional', 'M2', 'Probabilidad y estadística', 'A', 'Probabilidad condicional', 'm2.html#m2.pro.condicional'],
    ['m2.pro.combinatoria', 'M2', 'Probabilidad y estadística', 'A', 'Permutaciones y combinatoria', 'm2.html#m2.pro.combinatoria'],
    ['m2.geo.trig-razones', 'M2', 'Geometría', 'A', 'Razones trigonométricas', 'm2.html#m2.geo.trig-razones'],
    ['m2.pro.dispersion', 'M2', 'Probabilidad y estadística', 'A', 'Medidas de dispersión', 'm2.html#m2.pro.dispersion'],
    ['m2.sd', 'M2', 'Transversal', 'A', 'Suficiencia de datos', 'm2.html#m2.sd'],
    ['m2.alg.trig-funciones', 'M2', 'Álgebra y funciones', 'B', 'Gráficos de seno y coseno', 'm2.html#m2.geo.trig-razones'],
    ['m2.pro.binomial-normal', 'M2', 'Probabilidad y estadística', 'B', 'Binomial y normal', 'm2.html#m2.pro.binomial-normal'],
    ['m2.geo.circunferencia', 'M2', 'Geometría', 'B', 'Circunferencia: ángulos, arcos, cuerdas', 'm2.html#m2.geo.circunferencia'],
    ['m2.geo.homotecia', 'M2', 'Geometría', 'B', 'Homotecia', 'm2.html#m2.geo.homotecia'],
    ['m2.num.financiera', 'M2', 'Números', 'B', 'Matemática financiera', 'm2.html#m2.num.financiera'],
    ['m2.geo.esfera', 'M2', 'Geometría', 'B', 'Esfera: área y volumen', 'm2.html#m2.geo.esfera'],
    ['m2.alg.potencia', 'M2', 'Álgebra y funciones', 'C', 'Función potencia', 'm2.html#m2.alg.potencia'],
    ['m2.num.reales', 'M2', 'Números', 'C', 'Operatoria en los reales', 'm2.html#m2.num.reales'],
    ['m2.m1-dificil', 'M2', 'Transversal', 'C', 'M1 versión difícil', 'm2.html#m2.m1-dificil'],

    ['fis.mec.cinematica', 'CIE', 'Mecánica', 'A', 'Posición, desplazamiento, velocidad, aceleración', null],
    ['fis.mec.mru-mrua', 'CIE', 'Mecánica', 'A', 'MRU y MRUA: itinerario y gráficos', null],
    ['fis.mec.newton', 'CIE', 'Mecánica', 'A', 'Leyes de Newton + diagrama de cuerpo libre', null],
    ['fis.mec.fuerzas', 'CIE', 'Mecánica', 'A', 'Peso, normal, tensión, Hooke, roce', null],
    ['fis.ond.elementos', 'CIE', 'Ondas', 'A', 'Ondas: v = λ·f, período, amplitud', null],
    ['fis.ond.espejos-lentes', 'CIE', 'Ondas', 'A', 'Espejos y lentes', null],
    ['fis.ele.ohm', 'CIE', 'Electricidad', 'A', 'Ley de Ohm: serie, paralelo, mixto', null],
    ['fis.ele.potencia', 'CIE', 'Electricidad', 'A', 'Potencia y energía eléctrica (kWh)', null],
    ['fis.ond.reflexion-refraccion', 'CIE', 'Ondas', 'B', 'Reflexión, refracción, absorción', null],
    ['fis.ond.espectro-color', 'CIE', 'Ondas', 'B', 'Espectro EM, color y dispersión', null],
    ['fis.ond.doppler-interferencia', 'CIE', 'Ondas', 'B', 'Doppler, interferencia, difracción', null],
    ['fis.mec.galileo', 'CIE', 'Mecánica', 'B', 'Relatividad de Galileo', null],
    ['fis.tie.tectonica', 'CIE', 'Tierra y Universo', 'B', 'Tectónica de placas, sismos, interior', null],
    ['fis.mec.cosmos', 'CIE', 'Tierra y Universo', 'C', 'Sistema solar + origen del universo', null],
    ['fis.ond.dispositivos', 'CIE', 'Ondas', 'C', 'Radar, láser, telescopios, fibra óptica', null],
    ['fis.ele.domiciliaria', 'CIE', 'Electricidad', 'C', 'Instalación eléctrica domiciliaria', null],

    ['bio.celular', 'CIE', 'Biología', 'R', 'Organización y actividad celular', null],
    ['bio.procesos', 'CIE', 'Biología', 'R', 'Procesos y funciones (incl. sistema nervioso)', null],
    ['bio.herencia', 'CIE', 'Biología', 'R', 'Herencia y evolución', null],
    ['bio.ambiente', 'CIE', 'Biología', 'R', 'Organismo y ambiente', null],
    ['qui.atomica', 'CIE', 'Química', 'R', 'Estructura atómica', null],
    ['qui.organica', 'CIE', 'Química', 'R', 'Química orgánica', null],
    ['qui.estequiometria', 'CIE', 'Química', 'R', 'Reacciones y estequiometría', null],

    ['m1.num.enteros-racionales', 'M1', 'Números', 'B', 'Enteros y racionales', null],
    ['m1.num.porcentaje', 'M1', 'Números', 'B', 'Porcentaje', null],
    ['m1.num.potencias-raices', 'M1', 'Números', 'B', 'Potencias y raíces', null],
    ['m1.alg.expresiones', 'M1', 'Álgebra y funciones', 'B', 'Expresiones algebraicas', null],
    ['m1.alg.ecuaciones', 'M1', 'Álgebra y funciones', 'A', 'Ecuaciones, inecuaciones y sistemas', null],
    ['m1.alg.funciones', 'M1', 'Álgebra y funciones', 'A', 'Función lineal, afín y cuadrática', null],
    ['m1.alg.proporcionalidad', 'M1', 'Álgebra y funciones', 'C', 'Proporcionalidad', null],
    ['m1.geo.areas-volumenes', 'M1', 'Geometría', 'A', 'Áreas y volúmenes (incl. cilindro)', null],
    ['m1.geo.semejanza-pitagoras', 'M1', 'Geometría', 'A', 'Semejanza y Pitágoras', null],
    ['m1.geo.transformaciones', 'M1', 'Geometría', 'C', 'Transformaciones isométricas', null],
    ['m1.pro.datos', 'M1', 'Probabilidad y estadística', 'B', 'Datos y medidas de posición', null],
    ['m1.pro.probabilidad', 'M1', 'Probabilidad y estadística', 'B', 'Probabilidad (Laplace)', null],

    ['len.localizar', 'LEN', 'Habilidades', 'B', 'Localizar información', null],
    ['len.interpretar', 'LEN', 'Habilidades', 'A', 'Interpretar (idea principal, función)', null],
    ['len.evaluar', 'LEN', 'Habilidades', 'A', 'Evaluar (propósito, postura)', null],
  ];
  const TEMAS = {};
  for (const [id, prueba, eje, prio, nombre, leccion] of LISTA) TEMAS[id] = { id, prueba, eje, prio, nombre, leccion };
  const PESO_PRIO = { A: 3, B: 2, C: 1, R: 1.5 };

  // ---------- almacenamiento ----------
  function cargar(k, def) {
    try { const s = localStorage.getItem(K[k]); return s ? JSON.parse(s) : def; } catch (e) { return def; }
  }
  function guardar(k, v) {
    try { localStorage.setItem(K[k], JSON.stringify(v)); } catch (e) { console.warn('No se pudo guardar', k); }
    window.dispatchEvent(new CustomEvent('p27:cambio', { detail: k }));
  }

  // ---------- fechas (locales) ----------
  const pad = (n) => String(n).padStart(2, '0');
  const iso = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
  const hoy = () => iso(new Date());
  function aFecha(s) { const [y, m, d] = s.split('-').map(Number); return new Date(y, m - 1, d); }
  const sumarDias = (s, n) => { const d = aFecha(s); d.setDate(d.getDate() + n); return iso(d); };
  const difDias = (a, b) => Math.round((aFecha(b) - aFecha(a)) / 86400000);
  const DIAS = ['dom', 'lun', 'mar', 'mié', 'jue', 'vie', 'sáb'];
  const MESES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];
  const fechaCorta = (s) => { const d = aFecha(s); return `${DIAS[d.getDay()]} ${d.getDate()} ${MESES[d.getMonth()]}`; };

  // ---------- dominio ----------
  function prior(tema) { const t = TEMAS[tema]; return t ? PRUEBAS[t.prueba].prior : 30; }
  function dominio(tema) { const d = cargar('dominio', {}); return tema in d ? d[tema] : null; }
  function dominioEf(tema) { const v = dominio(tema); return v === null ? prior(tema) : v; }
  // Correcta en difícil sube más; incorrecta en básico baja más.
  const PESO_NIVEL = { basico: [0.7, 1.4], paes: [1, 1], dificil: [1.4, 0.7] };
  function registrar(tema, nivel, ok, opts = {}) {
    const d = cargar('dominio', {});
    let v = tema in d ? d[tema] : prior(tema);
    const base = opts.diag ? 0.35 : 0.15;
    const [sube, baja] = PESO_NIVEL[nivel] || PESO_NIVEL.paes;
    v = ok ? v + (100 - v) * base * sube : v - v * base * baja;
    d[tema] = Math.max(0, Math.min(100, Math.round(v)));
    guardar('dominio', d);
    if (!ok) programarRepaso(tema); else cumplirRepaso(tema);
    return d[tema];
  }

  // ---------- repaso espaciado: un fallo vuelve en +1 y +3 días ----------
  function programarRepaso(tema) {
    const r = cargar('repaso', []);
    const h = hoy();
    for (const n of [1, 3]) {
      const due = sumarDias(h, n);
      if (!r.some((x) => x.tema === tema && x.due === due && !x.hecho)) r.push({ tema, due, hecho: false, creado: h });
    }
    guardar('repaso', r);
  }
  function cumplirRepaso(tema) {
    const r = cargar('repaso', []);
    const h = hoy();
    let cambio = false;
    for (const x of r) if (x.tema === tema && !x.hecho && x.due <= h) { x.hecho = true; x.cumplido = h; cambio = true; }
    if (cambio) guardar('repaso', r);
  }
  function repasoPendiente(fecha = hoy()) {
    const r = cargar('repaso', []);
    return [...new Set(r.filter((x) => !x.hecho && x.due <= fecha).map((x) => x.tema))];
  }

  // ---------- exportar / importar ----------
  function exportar() {
    const datos = {};
    for (const k of Object.keys(K)) datos[k] = cargar(k, null);
    return { app: 'paes27', version: VERSION, exportado: new Date().toISOString(), datos };
  }
  function importar(obj) {
    if (!obj || obj.app !== 'paes27' || typeof obj.datos !== 'object') throw new Error('No es un respaldo de esta app.');
    for (const k of Object.keys(K)) if (obj.datos[k] !== null && obj.datos[k] !== undefined) guardar(k, obj.datos[k]);
  }

  // ---------- widget de pregunta (atajos 1–5, N = no sé, Enter = seguir) ----------
  const LETRAS = 'ABCDE';
  let activa = null;
  const NIVEL_TXT = { basico: 'Básico', paes: 'PAES', dificil: 'Difícil' };
  function el(tag, cls, html) { const e = document.createElement(tag); if (cls) e.className = cls; if (html !== undefined) e.innerHTML = html; return e; }

  // opts: { onRespuesta({ok, elegida}), onSiguiente(), noSe: bool, mezclar: bool, registrar: bool, meta: string, textoSiguiente }
  function pregunta(cont, q, opts = {}) {
    cont.innerHTML = '';
    const caja = el('div', 'q');
    const meta = opts.meta !== undefined ? opts.meta : `${NIVEL_TXT[q.nivel] || ''} · ${(TEMAS[q.tema] || {}).nombre || q.tema}`;
    if (meta) caja.appendChild(el('div', 'q-meta', meta));
    caja.appendChild(el('div', 'q-enun', q.enunciado));
    const orden = q.opciones.map((_, i) => i);
    if (opts.mezclar && q.tema !== 'm2.sd') for (let i = orden.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [orden[i], orden[j]] = [orden[j], orden[i]]; }
    const lista = el('div', 'q-ops');
    const botones = [];
    orden.forEach((oi, pos) => {
      const b = el('button', 'q-op', `<span class="q-l">${LETRAS[pos]}</span><span class="q-t">${q.opciones[oi].texto}</span>`);
      b.type = 'button'; b.dataset.oi = oi;
      b.addEventListener('click', () => responder(oi));
      botones.push(b); lista.appendChild(b);
    });
    caja.appendChild(lista);
    const fb = el('div', 'q-fb'); fb.hidden = true; caja.appendChild(fb);
    const acc = el('div', 'q-acc');
    let bNoSe = null;
    if (opts.noSe) { bNoSe = el('button', 'btn sec', 'No sé <kbd>N</kbd>'); bNoSe.type = 'button'; bNoSe.addEventListener('click', () => responder(-1)); acc.appendChild(bNoSe); }
    const bSig = el('button', 'btn', `${opts.textoSiguiente || 'Siguiente'} <kbd>Enter</kbd>`); bSig.type = 'button'; bSig.hidden = true;
    bSig.addEventListener('click', () => { if (opts.onSiguiente) opts.onSiguiente(); });
    acc.appendChild(bSig); caja.appendChild(acc);
    cont.appendChild(caja);

    let respondida = false;
    function responder(oi) {
      if (respondida) return;
      respondida = true;
      const ok = oi === q.correcta;
      botones.forEach((b) => {
        b.disabled = true;
        const i = Number(b.dataset.oi);
        if (i === q.correcta) b.classList.add('ok');
        else if (i === oi) b.classList.add('mal');
      });
      let h = ok ? '<b class="txt-ok">¡Correcta!</b> ' : (oi === -1 ? '<b class="txt-mal">Sin responder.</b> ' : '<b class="txt-mal">Incorrecta.</b> ');
      if (!ok && oi >= 0 && q.opciones[oi].trampa) h += `<div class="q-trampa"><b>La trampa:</b> ${q.opciones[oi].trampa}</div>`;
      h += `<div class="q-exp"><b>Correcta: ${LETRAS[orden.indexOf(q.correcta)]}.</b> ${q.explicacion}</div>`;
      fb.innerHTML = h; fb.hidden = false;
      if (bNoSe) bNoSe.hidden = true;
      bSig.hidden = !opts.onSiguiente;
      if (opts.registrar) registrar(q.tema, q.nivel, ok);
      if (opts.onRespuesta) opts.onRespuesta({ ok, elegida: oi });
      if (!bSig.hidden) bSig.focus({ preventScroll: true });
    }
    const api = { caja, responder: (pos) => { if (pos < botones.length) responder(Number(botones[pos].dataset.oi)); }, noSe: () => { if (opts.noSe) responder(-1); }, siguiente: () => { if (respondida && !bSig.hidden) bSig.click(); }, get respondida() { return respondida; } };
    caja.addEventListener('pointerdown', () => { activa = api; });
    activa = api;
    return api;
  }
  document.addEventListener('keydown', (ev) => {
    if (!activa || !document.body.contains(activa.caja) || !activa.caja.offsetParent) return; // solo la pregunta visible
    const t = ev.target;
    if (t && (t.tagName === 'TEXTAREA' || (t.tagName === 'INPUT' && t.type !== 'range' && t.type !== 'checkbox') || t.isContentEditable)) return;
    if (ev.ctrlKey || ev.metaKey || ev.altKey) return;
    if (ev.key >= '1' && ev.key <= '5' && !activa.respondida) { activa.responder(Number(ev.key) - 1); ev.preventDefault(); }
    else if ((ev.key === 'n' || ev.key === 'N') && !activa.respondida) { activa.noSe(); }
    else if (ev.key === 'Enter' && activa.respondida) { ev.preventDefault(); activa.siguiente(); }
  });

  // ---------- acordeones y pestañas ----------
  function colorDominio(v) { return v === null ? 'var(--muted)' : v < 40 ? 'var(--mal)' : v < 70 ? 'var(--warn)' : 'var(--ok)'; }

  // ---------- tema (claro/oscuro), logo y firma dicarch ----------
  const TEMA_K = 'paes27:tema';
  const tema = () => document.documentElement.dataset.theme || (window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  // Las pizarras leen los colores al cargar: al cambiar de tema se recarga (el progreso está guardado).
  function alternarTema() { try { localStorage.setItem(TEMA_K, tema() === 'dark' ? 'light' : 'dark'); } catch (e) { /* sin almacenamiento: solo esta vez */ } location.reload(); }
  const LOGO = '<svg viewBox="0 0 64 64" role="img" aria-label="PAES·27"><defs>'
    + '<linearGradient id="p27t" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#14C1CF"/><stop offset="1" stop-color="#0E9FD8"/></linearGradient>'
    + '<linearGradient id="p27v" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1FE39A"/><stop offset="1" stop-color="#0BC46E"/></linearGradient>'
    + '<linearGradient id="p27m" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D9127A"/><stop offset="1" stop-color="#F2295F"/></linearGradient>'
    + '<linearGradient id="p27o" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FF8A1F"/><stop offset="1" stop-color="#FFC53A"/></linearGradient></defs>'
    + '<rect x="32" y="4" width="28" height="28" rx="6" fill="url(#p27v)"/><rect x="4" y="4" width="30" height="30" rx="6" fill="url(#p27t)"/>'
    + '<rect x="31" y="31" width="29" height="29" rx="6" fill="url(#p27o)"/><rect x="4" y="32" width="29" height="28" rx="6" fill="url(#p27m)"/>'
    + '<g stroke="#fff" stroke-width="4" stroke-linecap="round" fill="none"><path d="M19 12v14M12 19h14"/><path d="M41 13l10 10M51 13L41 23"/><path d="M12 46h14"/><path d="M38 42h15M38 50h15"/></g>'
    + '<g fill="#fff"><circle cx="19" cy="40" r="2.4"/><circle cx="19" cy="52" r="2.4"/></g></svg>';
  const ICONO_TEMA = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><circle cx="12" cy="12" r="8"/><path d="M12 4a8 8 0 0 0 0 16z" fill="currentColor"/></svg>';
  function montarMarca() {
    document.querySelectorAll('[data-logo]').forEach((e) => { e.innerHTML = LOGO; });
    document.querySelectorAll('[data-tema-btn]').forEach((b) => {
      b.innerHTML = ICONO_TEMA; b.type = 'button';
      b.title = tema() === 'dark' ? 'Cambiar a tema claro' : 'Cambiar a tema oscuro'; b.setAttribute('aria-label', b.title);
      b.addEventListener('click', alternarTema);
    });
    document.querySelectorAll('[data-firma]').forEach((e) => { e.innerHTML = '<img src="lib/dicarch.webp" alt="" width="30" height="30"><span>PAES·27 · hecho por <b>dicarch</b></span>'; });
  }
  montarMarca();

  return { VERSION, K, PRUEBAS, tema, alternarTema, TEMAS, PESO_PRIO, cargar, guardar, hoy, sumarDias, difDias, fechaCorta, aFecha, prior, dominio, dominioEf, registrar, programarRepaso, cumplirRepaso, repasoPendiente, exportar, importar, pregunta, colorDominio, el };
})();
// == fin paes27-core v3 ==
