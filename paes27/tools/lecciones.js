// == paes27-lecciones v2 ==
// Utilidades de las páginas de lecciones. Se copia IDÉNTICO con tools/sync_core.py: edita tools/lecciones.js.
const { TEMAS, el } = P27;
const $ = (s) => document.querySelector(s);
// Las pizarras son siempre oscuras y tienen su propia paleta (core.css, regla .cv):
// los colores se leen desde un elemento .cv de muestra, no desde la raíz de la página.
const SONDA_CV = document.createElement('div'); SONDA_CV.className = 'cv'; SONDA_CV.hidden = true; document.body.appendChild(SONDA_CV);
const cssv = (v) => getComputedStyle(SONDA_CV).getPropertyValue(v).trim();
const COL = {};
for (const k of ['acc', 'acc2', 'ok', 'mal', 'warn', 'ink', 'muted', 'line']) COL[k] = cssv('--' + k);
COL.bg = cssv('--cv'); COL.panel = cssv('--cv-panel'); COL.panel2 = cssv('--cv-panel2');
const tono = (c, a) => { let h = (c || '#888888').replace('#', ''); if (h.length === 3) h = h.split('').map((x) => x + x).join(''); const n = parseInt(h, 16); return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${a})`; };
const REDUCIR = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

// ---------------- formato ----------------
function fmt(x, d = 2) {
  if (!Number.isFinite(x)) return '—';
  let r = Number(x.toFixed(d));
  if (Object.is(r, -0) || Math.abs(r) < 1e-12) r = 0;
  return String(r).replace('.', ',').replace('-', '−');
}
const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a || 1; };
function frac(n, d) { if (d === 0) return '—'; const g = gcd(n, d); n /= g; d /= g; if (d < 0) { n = -n; d = -d; } return d === 1 ? fmt(n) : `${fmt(n)}/${d}`; }
// "y = 2x − 3"
function recta(m, n) {
  let s = 'y = ';
  if (m === 0) return s + fmt(n);
  s += m === 1 ? 'x' : m === -1 ? '−x' : `${fmt(m)}x`;
  if (n > 0) s += ` + ${fmt(n)}`; else if (n < 0) s += ` − ${fmt(-n)}`;
  return s;
}
const par = (x) => (x < 0 ? `(${fmt(x)})` : fmt(x));

// ---------------- lienzo 2D ----------------
class Lienzo {
  constructor(canvas, o) {
    this.c = canvas; this.ctx = canvas.getContext('2d');
    this.o = { aspecto: 0.62, maxH: 420, ...o };
    this.dibujar = o.dibujar || (() => {});
    this.w = 0; this.h = 0;
    this.ajustar(true);
    new ResizeObserver(() => this.ajustar()).observe(canvas.parentElement);
  }
  ajustar(forzar) {
    const w = Math.max(220, this.c.parentElement.clientWidth);
    const h = Math.min(this.o.maxH, Math.round(w * this.o.aspecto));
    if (!forzar && w === this.w && h === this.h) return;
    const dpr = window.devicePixelRatio || 1;
    this.c.width = Math.round(w * dpr); this.c.height = Math.round(h * dpr);
    this.c.style.height = h + 'px';
    this.w = w; this.h = h;
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    this.fijarVista();
    this.redibujar();
  }
  fijarVista() {
    const v = this.o.vista;
    if (!v) return;
    this.x0 = v.x0; this.x1 = v.x1;
    if (v.igual) { // unidades iguales en x e y
      const alto = (v.x1 - v.x0) * (this.h / this.w);
      this.y0 = v.yc - alto / 2; this.y1 = v.yc + alto / 2;
    } else { this.y0 = v.y0; this.y1 = v.y1; }
  }
  redibujar() { if (this.w) this.dibujar(this); }
  X(x) { return ((x - this.x0) / (this.x1 - this.x0)) * this.w; }
  Y(y) { return this.h - ((y - this.y0) / (this.y1 - this.y0)) * this.h; }
  limpiar() { const c = this.ctx; c.clearRect(0, 0, this.w, this.h); c.fillStyle = COL.bg; c.fillRect(0, 0, this.w, this.h); }
  grilla(paso = 1, etiquetas = true, pasoEt = paso * 2) {
    const c = this.ctx;
    c.lineWidth = 1; c.strokeStyle = tono(COL.muted, .16);
    c.beginPath();
    for (let x = Math.ceil(this.x0 / paso) * paso; x <= this.x1; x += paso) { c.moveTo(this.X(x), 0); c.lineTo(this.X(x), this.h); }
    for (let y = Math.ceil(this.y0 / paso) * paso; y <= this.y1; y += paso) { c.moveTo(0, this.Y(y)); c.lineTo(this.w, this.Y(y)); }
    c.stroke();
    c.strokeStyle = tono(COL.muted, .6); c.lineWidth = 1.3;
    c.beginPath(); c.moveTo(0, this.Y(0)); c.lineTo(this.w, this.Y(0)); c.moveTo(this.X(0), 0); c.lineTo(this.X(0), this.h); c.stroke();
    if (!etiquetas) return;
    c.fillStyle = COL.muted; c.font = '11px system-ui'; c.textAlign = 'center'; c.textBaseline = 'top';
    for (let x = Math.ceil(this.x0 / pasoEt) * pasoEt; x <= this.x1; x += pasoEt) if (Math.abs(x) > 1e-9) c.fillText(fmt(x), this.X(x), this.Y(0) + 3);
    c.textAlign = 'right'; c.textBaseline = 'middle';
    for (let y = Math.ceil(this.y0 / pasoEt) * pasoEt; y <= this.y1; y += pasoEt) if (Math.abs(y) > 1e-9) c.fillText(fmt(y), this.X(0) - 4, this.Y(y));
  }
  fn(f, color, ancho = 2.5, xa = this.x0, xb = this.x1, dash) {
    const c = this.ctx; c.strokeStyle = color; c.lineWidth = ancho; c.setLineDash(dash || []);
    c.beginPath();
    let pen = false; let py = 0;
    const N = Math.max(200, this.w);
    for (let i = 0; i <= N; i++) {
      const x = xa + ((xb - xa) * i) / N; const y = f(x);
      const Y = this.Y(y);
      if (!Number.isFinite(y) || Y < -2000 || Y > this.h + 2000 || (pen && Math.abs(Y - py) > this.h * 2)) { pen = false; continue; }
      if (pen) c.lineTo(this.X(x), Y); else c.moveTo(this.X(x), Y);
      pen = true; py = Y;
    }
    c.stroke(); c.setLineDash([]);
  }
  seg(x1, y1, x2, y2, color, ancho = 2, dash) {
    const c = this.ctx; c.strokeStyle = color; c.lineWidth = ancho; c.setLineDash(dash || []);
    c.beginPath(); c.moveTo(this.X(x1), this.Y(y1)); c.lineTo(this.X(x2), this.Y(y2)); c.stroke(); c.setLineDash([]);
  }
  punto(x, y, color, r = 5) { const c = this.ctx; c.fillStyle = color; c.beginPath(); c.arc(this.X(x), this.Y(y), r, 0, 7); c.fill(); }
  texto(t, x, y, color, o = {}) {
    const c = this.ctx; c.fillStyle = color || COL.ink; c.font = `${o.peso || 600} ${o.tam || 13}px system-ui`;
    c.textAlign = o.align || 'left'; c.textBaseline = o.base || 'bottom';
    const px = o.px ? x : this.X(x) + (o.dx || 0); const py = o.px ? y : this.Y(y) + (o.dy || 0);
    if (o.fondo) {
      const m = c.measureText(t); const w = m.width + 8; const th = (o.tam || 13) + 6;
      const ax = o.align === 'center' ? px - w / 2 : o.align === 'right' ? px - w + 4 : px - 4;
      const ay = o.base === 'top' ? py - 2 : o.base === 'middle' ? py - th / 2 : py - th + 2;
      c.fillStyle = tono(COL.bg, .85); c.fillRect(ax, ay, w, th); c.fillStyle = color || COL.ink;
    }
    c.fillText(t, px, py);
  }
}

// ---------------- animaciones (solo corren si se ven) ----------------
const ANIMS = {};
function animar(id, lienzo, cuadro) {
  const a = { t: 0, corre: !REDUCIR, visible: false, lienzo, cuadro };
  lienzo.dibujar = () => cuadro(a.t);
  ANIMS[id] = a;
  new IntersectionObserver((es) => { a.visible = es[0].isIntersecting; }).observe(lienzo.c);
  lienzo.redibujar();
  return a;
}
let tPrev = null;
function bucle(ts) {
  const dt = tPrev === null ? 0 : Math.min(0.05, (ts - tPrev) / 1000);
  tPrev = ts;
  for (const a of Object.values(ANIMS)) if (a.corre && a.visible) { a.t += dt; a.lienzo.redibujar(); }
  requestAnimationFrame(bucle);
}
requestAnimationFrame(bucle);
document.addEventListener('click', (e) => {
  const b = e.target.closest('[data-pausa]'); if (!b) return;
  const a = ANIMS[b.dataset.pausa]; if (!a) return;
  a.corre = !a.corre; b.textContent = a.corre ? '⏸ Pausa' : '▶ Reproducir';
});
if (REDUCIR) document.querySelectorAll('[data-pausa]').forEach((b) => { b.textContent = '▶ Reproducir'; });

function sliders(ids, alCambiar, fmtV = {}) {
  const val = {};
  const leer = () => {
    for (const id of ids) {
      const inp = document.getElementById(id); val[id] = Number(inp.value);
      const o = document.getElementById(id + '-v'); if (o) o.textContent = fmtV[id] ? fmtV[id](val[id]) : fmt(val[id]);
    }
    alCambiar(val);
  };
  ids.forEach((id) => document.getElementById(id).addEventListener('input', leer));
  leer();
  return { val, leer };
}
const lerp = (a, b, t) => a + (b - a) * t;
const suave = (t) => t * t * (3 - 2 * t);

// =====================================================================
// utilidades Fase 2c: arrastre, arcos de ángulo, círculos, WebGL
// =====================================================================
function arrastrable(L, puntos, alMover) {
  let activo = null;
  const pos = (e) => { const r = L.c.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; };
  const mundo = ([px, py]) => [L.x0 + (px / L.w) * (L.x1 - L.x0), L.y0 + ((L.h - py) / L.h) * (L.y1 - L.y0)];
  L.c.addEventListener('pointerdown', (e) => {
    const [px, py] = pos(e); let mejor = null, d0 = 24;
    puntos().forEach((p, i) => { const d = Math.hypot(L.X(p.x) - px, L.Y(p.y) - py); if (d < d0) { d0 = d; mejor = i; } });
    if (mejor !== null) { activo = mejor; L.c.setPointerCapture(e.pointerId); L.c.style.cursor = 'grabbing'; e.preventDefault(); }
  });
  L.c.addEventListener('pointermove', (e) => { if (activo === null) return; const [x, y] = mundo(pos(e)); alMover(activo, Math.round(x * 2) / 2, Math.round(y * 2) / 2); });
  const fin = () => { activo = null; L.c.style.cursor = 'grab'; };
  L.c.addEventListener('pointerup', fin); L.c.addEventListener('pointercancel', fin);
}
function arcoAngulo(L, V, P1, P2, r, color) {
  const c = L.ctx, vx = L.X(V[0]), vy = L.Y(V[1]);
  const a1 = Math.atan2(L.Y(P1[1]) - vy, L.X(P1[0]) - vx), a2 = Math.atan2(L.Y(P2[1]) - vy, L.X(P2[0]) - vx);
  let d = a2 - a1; while (d <= -Math.PI) d += 2 * Math.PI; while (d > Math.PI) d -= 2 * Math.PI;
  c.strokeStyle = color; c.lineWidth = 2; c.beginPath(); c.arc(vx, vy, r, a1, a1 + d, d < 0); c.stroke();
}
const angulo = (V, P1, P2) => { const u = [P1[0] - V[0], P1[1] - V[1]], v = [P2[0] - V[0], P2[1] - V[1]]; return (Math.acos(Math.max(-1, Math.min(1, (u[0] * v[0] + u[1] * v[1]) / (Math.hypot(...u) * Math.hypot(...v))))) * 180) / Math.PI; };
const enCirc = (g, r = 1) => [r * Math.cos((g * Math.PI) / 180), r * Math.sin((g * Math.PI) / 180)];
function circulo(L, cx, cy, r, color, ancho = 2) { const c = L.ctx; c.strokeStyle = color; c.lineWidth = ancho; c.beginPath(); c.arc(L.X(cx), L.Y(cy), (r * L.w) / (L.x1 - L.x0), 0, 7); c.stroke(); }
function arcoCirc(L, g1, g2, color, ancho = 5) { // arco de la circunferencia unitaria desde g1 hasta g2 (grados, antihorario)
  const c = L.ctx; const R = L.w / (L.x1 - L.x0);
  c.strokeStyle = color; c.lineWidth = ancho; c.beginPath(); c.arc(L.X(0), L.Y(0), R, (-g1 * Math.PI) / 180, (-g2 * Math.PI) / 180, true); c.stroke();
}
const etiqueta = (L, t, P, color, dx = 8, dy = -6) => L.texto(t, P[0], P[1], color, { dx, dy, tam: 13 });
const hayWebGL = (() => { try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch (e) { return false; } })();
let promThree = null;
const cargarThree = () => (promThree = promThree || import('./lib/three.module.min.js'));

function montarEjemplos(EJEMPLOS) {
document.querySelectorAll('.ejemplo').forEach((box) => {
  const ej = EJEMPLOS[box.dataset.ej];
  box.innerHTML = `<div class="enun">${ej.enun}</div><ol></ol>`;
  const ol = box.querySelector('ol');
  const fila = el('div', 'fila'); fila.style.marginTop = '8px';
  const b = el('button', 'btn mini', 'Siguiente paso (1/' + ej.pasos.length + ')');
  const todo = el('button', 'btn sec mini', 'Ver todo');
  let i = 0;
  const mostrar = () => {
    ol.appendChild(el('li', '', ej.pasos[i++]));
    if (i < ej.pasos.length) b.textContent = `Siguiente paso (${i + 1}/${ej.pasos.length})`;
    else { b.hidden = true; todo.hidden = true; box.appendChild(el('div', 'trampa-ej', `<b>Trampa típica:</b> ${ej.trampa}`)); }
  };
  b.onclick = mostrar; todo.onclick = () => { while (i < ej.pasos.length) mostrar(); };
  fila.append(b, todo); box.appendChild(fila);
  box.appendChild(el('p', 'small muted', 'Antes de cada paso, intenta adivinar qué viene.'));
});
}

// =====================================================================
// PRÁCTICA en 3 niveles
// =====================================================================
const NIVELES = [['basico', 'Básico'], ['paes', 'PAES'], ['dificil', 'Difícil']];
function montarPracticas(BANCO) {
document.querySelectorAll('.practica').forEach((box) => {
  const temas = box.dataset.temas.split(',');
  const bar = el('div', 'niveles');
  const quiz = el('div', 'quiz');
  const dom = P27.dominio(temas[0]);
  quiz.innerHTML = `<p class="muted small">Elige un nivel. ${dom === null || dom < 40 ? 'Te conviene partir por <b>Básico</b>.' : dom < 70 ? 'Te conviene el nivel <b>PAES</b>.' : 'Prueba el nivel <b>Difícil</b>.'} Cada alternativa incorrecta te explica su trampa.</p>`;
  const botones = {};
  NIVELES.forEach(([n, nombre]) => {
    const b = el('button', 'btn sec mini', nombre);
    const cant = BANCO.filter((q) => temas.includes(q.tema) && q.nivel === n).length;
    b.title = cant ? `${cant} preguntas` : 'Sin preguntas en este nivel';
    b.disabled = !cant;
    b.onclick = () => empezar(n);
    botones[n] = b; bar.appendChild(b);
  });
  box.append(bar, quiz);
  function empezar(nivel) {
    Object.entries(botones).forEach(([n, b]) => b.classList.toggle('on', n === nivel));
    const qs = BANCO.filter((q) => temas.includes(q.tema) && q.nivel === nivel).sort(() => Math.random() - 0.5);
    let i = 0, aciertos = 0;
    const sig = () => {
      if (i >= qs.length) return resumen();
      const q = qs[i++];
      P27.pregunta(quiz, q, {
        registrar: true, mezclar: true,
        meta: `${NIVELES.find((x) => x[0] === nivel)[1]} · pregunta ${i} de ${qs.length} · ${TEMAS[q.tema].nombre}`,
        textoSiguiente: i < qs.length ? 'Siguiente' : 'Ver resultado',
        onRespuesta: ({ ok }) => { if (ok) aciertos++; },
        onSiguiente: sig,
      });
    };
    const resumen = () => {
      const idx = NIVELES.findIndex((x) => x[0] === nivel);
      const r = el('div', 'resumen-nivel');
      const bien = aciertos === qs.length, mal = aciertos <= qs.length / 3;
      r.innerHTML = `<h3>${aciertos}/${qs.length} en ${NIVELES[idx][1]}</h3><p>${bien ? (idx < 2 ? '¡Listo! Sube de nivel.' : '¡Dominado! Este tema queda para el repaso espaciado.') : mal ? 'Vuelve a «Manipular» y al ejemplo antes de repetir. Los temas fallados vuelven mañana y en 3 días.' : 'Casi. Revisa las trampas que te pillaron y repite.'}</p>`;
      const f = el('div', 'fila');
      const rep = el('button', 'btn sec mini', 'Repetir nivel'); rep.onclick = () => empezar(nivel); f.appendChild(rep);
      if (idx < 2) { const s2 = el('button', 'btn mini', `Nivel ${NIVELES[idx + 1][1]}`); s2.onclick = () => empezar(NIVELES[idx + 1][0]); f.appendChild(s2); }
      const dom2 = P27.dominio(temas[0]);
      f.appendChild(el('span', 'small muted', `Dominio ahora: ${dom2 === null ? '—' : dom2 + ' %'}`));
      r.appendChild(f);
      quiz.innerHTML = ''; quiz.appendChild(r);
    };
    sig();
  }
});
}

// =====================================================================
// ENSAYO CRONOMETRADO (sin feedback hasta el final). Estado en paes27:ensayos.
// =====================================================================
// cfg: { prueba, titulo, pool, modos: {clave: {n, seg, nombre}}, alFinal (tema que va al final), intro(nDisponibles) }
function montarEnsayo(pane, cfg) {
  const POOL = cfg.pool;
  const MODOS = cfg.modos;
  const fmtT = (s) => { s = Math.max(0, Math.round(s)); const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), x = s % 60; return (h ? h + ':' + String(m).padStart(2, '0') : m) + ':' + String(x).padStart(2, '0'); };
  const lista = () => P27.cargar('ensayos', []);
  const enCurso = () => lista().find((e) => e.estado === 'en-curso' && e.prueba === cfg.prueba);
  const guardarEns = (e) => { const l = lista().filter((x) => x.id !== e.id); l.push(e); P27.guardar('ensayos', l); };
  const POR_ID = Object.fromEntries(POOL.map((q) => [q.id, q]));
  let timer = null, st = null;

  function elegir(n) {
    const vistos = {};
    for (const e of lista()) for (const r of e.respuestas || []) vistos[r.id] = (vistos[r.id] || 0) + 1;
    let candidatos = POOL.filter((q) => q.nivel !== 'basico');
    if (candidatos.length < n) candidatos = POOL.slice();
    const porTema = {};
    for (const q of candidatos.sort(() => Math.random() - 0.5)) (porTema[q.tema] = porTema[q.tema] || []).push(q);
    for (const t in porTema) porTema[t].sort((a, b) => (vistos[a.id] || 0) - (vistos[b.id] || 0));
    const temas = Object.keys(porTema).sort((a, b) => (P27.PESO_PRIO[TEMAS[b].prio] - P27.PESO_PRIO[TEMAS[a].prio]) || Math.random() - 0.5);
    const out = [];
    while (out.length < n && temas.some((t) => porTema[t].length)) for (const t of temas) if (porTema[t].length && out.length < n) out.push(porTema[t].shift());
    const fin = out.filter((q) => q.tema === cfg.alFinal);
    return [...out.filter((q) => q.tema !== cfg.alFinal).sort(() => Math.random() - 0.5), ...fin]; // p. ej. suficiencia al final, como en la prueba
  }

  function empezar(modo) {
    const M = MODOS[modo];
    const qs = elegir(M.n);
    const orden = {};
    for (const q of qs) {
      const o = q.opciones.map((_, i) => i);
      if (q.tema !== 'm2.sd') o.sort(() => Math.random() - 0.5);
      orden[q.id] = o;
    }
    st = { id: 'ens-' + Date.now(), prueba: cfg.prueba, estado: 'en-curso', modo, inicio: Date.now(), limite: M.seg, ids: qs.map((q) => q.id), orden, resp: {}, marcadas: [], actual: 0 };
    guardarEns(st);
    correr();
  }

  const restante = () => st.limite - (Date.now() - st.inicio) / 1000;

  function correr() {
    clearInterval(timer);
    timer = setInterval(() => { const r = $('#ens-reloj'); if (!r) return; const s = restante(); r.textContent = fmtT(s); r.classList.toggle('txt-mal', s < 600); if (s <= 0) terminar(true); }, 1000);
    pintar();
  }

  function pintar() {
    if (restante() <= 0) return terminar(true);
    const q = POR_ID[st.ids[st.actual]];
    const n = st.ids.length;
    const resp = Object.keys(st.resp).length;
    pane.innerHTML = '';
    const top = el('div', 'ens-top');
    top.innerHTML = `<div><b>${cfg.titulo} · ${MODOS[st.modo].nombre}</b> · pregunta ${st.actual + 1} de ${n} · respondidas ${resp}/${n}</div><div class="ens-reloj">⏱ <span id="ens-reloj">${fmtT(restante())}</span></div>`;
    const bEnt = el('button', 'btn sec mini', 'Entregar');
    bEnt.onclick = () => { const f = n - resp; if (confirm(f ? `Te faltan ${f} preguntas. No hay descuento por error: conviene responderlas todas. ¿Entregar igual?` : '¿Entregar el ensayo?')) terminar(false); };
    top.appendChild(bEnt);
    pane.appendChild(top);
    const caja = el('div', 'q');
    caja.appendChild(el('div', 'q-meta', `Pregunta ${st.actual + 1}${st.marcadas.includes(q.id) ? ' · <span class="txt-warn">marcada para revisar</span>' : ''}`));
    caja.appendChild(el('div', 'q-enun', q.enunciado));
    const ops = el('div', 'q-ops');
    st.orden[q.id].forEach((oi, pos) => {
      const b = el('button', 'q-op' + (st.resp[q.id] === oi ? ' sel' : ''), `<span class="q-l">${'ABCDE'[pos]}</span><span class="q-t">${q.opciones[oi].texto}</span>`);
      b.type = 'button';
      b.onclick = () => elegirOp(pos);
      ops.appendChild(b);
    });
    caja.appendChild(ops);
    const acc = el('div', 'q-acc');
    const bAnt = el('button', 'btn sec mini', '← Anterior'); bAnt.disabled = st.actual === 0; bAnt.onclick = () => ir2(st.actual - 1);
    const bMar = el('button', 'btn sec mini', st.marcadas.includes(q.id) ? 'Desmarcar' : 'Marcar para revisar');
    bMar.onclick = () => { const i = st.marcadas.indexOf(q.id); if (i >= 0) st.marcadas.splice(i, 1); else st.marcadas.push(q.id); guardarEns(st); pintar(); };
    const bSig = el('button', 'btn mini', st.actual + 1 < n ? 'Siguiente <kbd>Enter</kbd>' : 'Ir a entregar'); bSig.onclick = () => (st.actual + 1 < n ? ir2(st.actual + 1) : bEnt.click());
    acc.append(bAnt, bMar, bSig);
    caja.appendChild(acc);
    pane.appendChild(caja);
    const grilla = el('div', 'ens-grilla');
    st.ids.forEach((id, i) => {
      const b = el('button', (st.resp[id] !== undefined ? 'r ' : '') + (st.marcadas.includes(id) ? 'm ' : '') + (i === st.actual ? 'a' : ''), String(i + 1));
      b.type = 'button'; b.onclick = () => ir2(i); grilla.appendChild(b);
    });
    pane.appendChild(el('div', 'small muted', 'Mapa: <span class="ens-ley r">respondida</span> <span class="ens-ley m">marcada</span>. Atajos: 1–5 para elegir, Enter para seguir. Puedes cambiar respuestas hasta entregar.'));
    pane.appendChild(grilla);
  }
  function elegirOp(pos) {
    const q = POR_ID[st.ids[st.actual]];
    const oi = st.orden[q.id][pos];
    if (oi === undefined) return;
    if (st.resp[q.id] === oi) delete st.resp[q.id]; else st.resp[q.id] = oi;
    guardarEns(st); pintar();
  }
  function ir2(i) { st.actual = Math.max(0, Math.min(st.ids.length - 1, i)); guardarEns(st); pintar(); window.scrollTo({ top: pane.offsetTop - 10 }); }

  document.addEventListener('keydown', (ev) => {
    if (!st || st.estado !== 'en-curso' || !pane.offsetParent) return;
    if (ev.ctrlKey || ev.metaKey || ev.altKey || (ev.target && /INPUT|TEXTAREA|SELECT/.test(ev.target.tagName))) return;
    if (ev.key >= '1' && ev.key <= '5') { elegirOp(Number(ev.key) - 1); ev.preventDefault(); }
    else if (ev.key === 'Enter') { ev.preventDefault(); if (st.actual + 1 < st.ids.length) ir2(st.actual + 1); }
  });

  function terminar(porTiempo) {
    clearInterval(timer);
    const respuestas = st.ids.map((id) => { const q = POR_ID[id]; const e = st.resp[id]; return { id, tema: q.tema, nivel: q.nivel, elegida: e === undefined ? -1 : e, ok: e === q.correcta }; });
    for (const r of respuestas) P27.registrar(r.tema, r.nivel, r.ok);
    const fin = { id: st.id, prueba: cfg.prueba, estado: 'hecho', modo: st.modo, fecha: P27.hoy(), correctas: respuestas.filter((r) => r.ok).length, total: respuestas.length,
      omitidas: respuestas.filter((r) => r.elegida === -1).length, segundos: Math.round(Math.min(st.limite, (Date.now() - st.inicio) / 1000)), porTiempo, respuestas };
    guardarEns(fin);
    st = null;
    resultado(fin);
  }

  function resultado(e) {
    pane.innerHTML = '';
    const volver = el('button', 'btn sec mini', '← Volver al inicio del ensayo'); volver.onclick = () => inicio();
    pane.appendChild(volver);
    const pct = Math.round((e.correctas / e.total) * 100);
    const temas = {};
    for (const r of e.respuestas) { temas[r.tema] = temas[r.tema] || [0, 0]; temas[r.tema][1]++; if (r.ok) temas[r.tema][0]++; }
    const c = el('div', 'card', `<h2>${e.correctas}/${e.total} correctas (${pct} %)</h2><p class="muted">${MODOS[e.modo].nombre} · ${fmtT(e.segundos)} usados${e.porTiempo ? ' · se acabó el tiempo' : ''} · ${e.omitidas} sin responder.</p><p class="small muted">Esto no es un puntaje PAES: es el % de acierto en preguntas de la app. Los temas fallados vuelven en tu repaso de mañana y en 3 días.</p>`);
    const tb = el('table', 'res');
    tb.innerHTML = '<tr><th>Tema</th><th>Correctas</th><th></th></tr>' + Object.entries(temas).sort((a, b) => a[1][0] / a[1][1] - b[1][0] / b[1][1]).map(([t, [a, b]]) => {
      const T = TEMAS[t];
      return `<tr><td>${T.nombre}</td><td class="${a / b >= 0.7 ? 'txt-ok' : a / b >= 0.4 ? 'txt-warn' : 'txt-mal'}">${a}/${b}</td><td>${T.leccion ? `<a href="${T.leccion}">lección</a>` : ''}</td></tr>`;
    }).join('');
    c.appendChild(tb);
    pane.appendChild(c);
    const malas = e.respuestas.filter((r) => !r.ok);
    if (malas.length) {
      const c2 = el('div', 'card', `<h3>Revisa tus ${malas.length} errores</h3><p class="small muted">Para cada uno: ¿fue concepto, cálculo o trampa?</p>`);
      malas.forEach((r, i) => {
        const q = POR_ID[r.id]; if (!q) return;
        const d = el('details', 'acc');
        d.innerHTML = `<summary>${i + 1}. ${TEMAS[q.tema].nombre}</summary><div class="in"><div>${q.enunciado}</div>${r.elegida >= 0 ? `<p class="q-trampa"><b>Marcaste:</b> ${q.opciones[r.elegida].texto}. <b>La trampa:</b> ${q.opciones[r.elegida].trampa}</p>` : '<p class="muted">Sin responder.</p>'}<p><b>Correcta:</b> ${q.opciones[q.correcta].texto}. ${q.explicacion}</p></div>`;
        c2.appendChild(d);
      });
      pane.appendChild(c2);
    }
  }

  function inicio() {
    clearInterval(timer);
    const cur = enCurso();
    if (cur) { st = cur; if (restante() <= 0) return terminar(true); return correr(); }
    pane.innerHTML = '';
    const nAvanz = POOL.filter((q) => q.nivel !== 'basico').length;
    const c = el('div', 'card', cfg.intro(nAvanz));
    const f = el('div', 'fila');
    for (const [k, M] of Object.entries(MODOS)) {
      const b = el('button', k === 'completo' ? 'btn' : 'btn sec', `${M.nombre}: ${M.n} preguntas · ${fmtT(M.seg)}`);
      b.onclick = () => { if (confirm(`Empieza el ensayo ${M.nombre.toLowerCase()}: ${M.n} preguntas en ${fmtT(M.seg)}. El reloj no se detiene. ¿Listo?`)) empezar(k); };
      f.appendChild(b);
    }
    c.appendChild(f);
    pane.appendChild(c);
    const hechos = lista().filter((e) => e.estado === 'hecho' && e.prueba === cfg.prueba).reverse();
    if (hechos.length) {
      const h = el('div', 'card', `<h3>Historial · ${cfg.titulo}</h3>`);
      hechos.forEach((e) => {
        const fila = el('div', 'fila');
        fila.innerHTML = `<span>${P27.fechaCorta(e.fecha)} · ${MODOS[e.modo].nombre} · <b>${e.correctas}/${e.total}</b> (${Math.round((e.correctas / e.total) * 100)} %) · ${fmtT(e.segundos)}</span>`;
        const b = el('button', 'btn sec mini', 'Ver errores'); b.onclick = () => resultado(e); fila.appendChild(b);
        h.appendChild(fila);
      });
      pane.appendChild(h);
    }
  }
  return { inicio };
}

// ---------------- dominio en vivo ----------------
function montarDominio() {
function pintarDominio() {
  document.querySelectorAll('.dom[data-tema]').forEach((s) => {
    const v = P27.dominio(s.dataset.tema);
    s.style.color = P27.colorDominio(v);
    s.textContent = `${s.dataset.tema.includes('trig-funciones') ? 'Funciones' : 'Dominio'} ${v === null ? '—' : v + ' %'}`;
    s.title = v === null ? 'Aún sin datos: practica para medirlo' : 'Tu dominio de este tema (0–100 %)';
  });
}
window.addEventListener('p27:cambio', pintarDominio);
window.addEventListener('storage', pintarDominio);
pintarDominio();
}

// ---------------- acordeón de lecciones ----------------
function montarAcordeon() {
document.querySelectorAll('.leccion').forEach((l) => {
  l.classList.add('cerrada');
  l.querySelector('.lec-head').addEventListener('click', (e) => { if (e.target.closest('a,button,select,input')) return; l.classList.toggle('cerrada'); });
  const prio = l.querySelector('.lec-head .chip.A,.lec-head .chip.B,.lec-head .chip.C');
  if (prio && prio.textContent.length === 1) prio.textContent = 'Prioridad ' + prio.textContent;
});
montarPasos();
}

// Los 5 pasos de cada lección como pestañas (pills): se ve un paso a la vez.
// Lo que va antes del primer paso (la idea, tarjetas, avisos) queda siempre visible.
const NOMBRE_PASO = [[/^ver\b/i, 'Ver'], [/manipular/i, 'Manipular'], [/porqu/i, 'El porqué'], [/ejemplo/i, 'Ejemplo'], [/pr[aá]ctica/i, 'Práctica']];
function montarPasos() {
document.querySelectorAll('.leccion > .lec-body').forEach((body) => {
  const esPaso = (n) => n.matches('.paso, details.acc');
  // «2b», «2c»…: continúan el paso anterior (misma pestaña, con su subtítulo visible)
  const esSub = (n) => n.matches('.paso') && /^\d+[a-z]$/i.test(((n.querySelector('h3 .n') || {}).textContent || '').trim());
  const hijos = [...body.children];
  const k0 = hijos.findIndex(esPaso);
  if (k0 < 0) return;
  const grupos = [];
  for (const n of hijos.slice(k0)) { if ((esPaso(n) && !esSub(n)) || !grupos.length) grupos.push([n]); else grupos[grupos.length - 1].push(n); }
  if (grupos.length < 2) return;
  body.classList.add('con-pasos');
  const barra = el('div', 'pasos'); barra.setAttribute('role', 'tablist');
  const pasos = grupos.map((g, i) => {
    const cab = g[0].matches('details') ? g[0].querySelector('summary') : g[0].querySelector('h3');
    const txt = (cab ? cab.textContent : '').replace(/^\s*\d+\s*/, '').trim();
    const nombre = (NOMBRE_PASO.find(([re]) => re.test(txt)) || [0, txt.split(/[·(:]/)[0].trim()])[1];
    if (g[0].matches('details')) { g[0].open = true; g[0].classList.add('porque'); }
    const pane = el('div', 'paso-pane' + (g.some(esSub) ? ' multi' : '')); pane.setAttribute('role', 'tabpanel');
    g[0].before(pane); g.forEach((n) => pane.appendChild(n));
    const b = el('button', '', `${i + 1} ${nombre}`); b.type = 'button'; b.setAttribute('role', 'tab');
    b.addEventListener('click', () => mostrar(i));
    barra.appendChild(b);
    return { pane, b, nombre };
  });
  pasos.forEach((p, i) => {
    if (i === pasos.length - 1) return;
    const s = el('button', 'btn sec mini', `Sigue: ${i + 2} ${pasos[i + 1].nombre} →`); s.type = 'button';
    s.addEventListener('click', () => { mostrar(i + 1); const r = barra.getBoundingClientRect(); if (r.top < 0) barra.scrollIntoView({ block: 'start', behavior: REDUCIR ? 'auto' : 'smooth' }); });
    const w = el('div', 'paso-sig'); w.appendChild(s); p.pane.appendChild(w);
  });
  body.insertBefore(barra, body.firstChild);
  function mostrar(i) {
    pasos.forEach((p, k) => { p.pane.classList.toggle('on', k === i); p.b.classList.toggle('on', k === i); p.b.setAttribute('aria-selected', String(k === i)); });
  }
  mostrar(0);
});
}

// Escena Three.js con luces y cámara; devuelve null si no hay WebGL (la página cae a Canvas 2D).
async function escena3D(cont, armar) {
  if (!hayWebGL) return null;
  let T;
  try { T = await cargarThree(); } catch (e) { return null; }
  const renderer = new T.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));
  renderer.setClearColor(COL.bg);
  cont.appendChild(renderer.domElement);
  const escena = new T.Scene();
  const camara = new T.PerspectiveCamera(38, 1.6, 0.1, 200);
  escena.add(new T.AmbientLight(0xffffff, 0.55));
  const luz = new T.DirectionalLight(0xffffff, 1.6); luz.position.set(3, 5, 6); escena.add(luz);
  const api = armar(T, escena, camara);
  const medir = () => { const w = cont.clientWidth || 300, h = cont.clientHeight || 300; renderer.setSize(w, h); camara.aspect = w / h; camara.updateProjectionMatrix(); render(); };
  const render = () => renderer.render(escena, camara);
  new ResizeObserver(medir).observe(cont);
  medir();
  return { c: renderer.domElement, dibujar: null, redibujar() { if (this.dibujar) this.dibujar(); else render(); }, render, api, T };
}
function aro(T, r, y, color) {
  const pts = []; for (let i = 0; i <= 64; i++) { const a = (i / 64) * Math.PI * 2; pts.push(new T.Vector3(r * Math.cos(a), y, r * Math.sin(a))); }
  return new T.Line(new T.BufferGeometry().setFromPoints(pts), new T.LineBasicMaterial({ color }));
}
function respaldo2D(cont, dibujar) {
  cont.style.height = 'auto';
  const cv = document.createElement('canvas'); cont.appendChild(cv);
  return new Lienzo(cv, { aspecto: 0.55, maxH: 340, dibujar });
}
// == fin paes27-lecciones v2 ==
