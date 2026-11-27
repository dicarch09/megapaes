// == paes27-gen v1 ==
// Preguntas con números nuevos (practica.html). Se copia IDÉNTICO con tools/sync_core.py: edita tools/generadores.js.
// Cada familia arma el enunciado, calcula la correcta y arma las incorrectas desde un error real (su trampa).
// tools/verificar_gen.py recalcula por su cuenta miles de muestras de cada familia.
const GEN = (() => {
  'use strict';
  const OTRA = { otra: true }; // «estos números no sirven: sortea otros»
  const FAM = [];
  const fam = (id, tema, niveles, nombre, gen) => FAM.push({ id, tema, niveles, nombre, gen });

  // ---------------- azar con semilla (mulberry32): una semilla = una pregunta reproducible ----------------
  function rng(seed) {
    let a = seed >>> 0;
    return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  }
  function azar(r) {
    const ent = (a, b) => a + Math.floor(r() * (b - a + 1));
    const elige = (arr) => arr[Math.floor(r() * arr.length)];
    const nz = (a, b) => { for (let i = 0; i < 99; i++) { const v = ent(a, b); if (v !== 0) return v; } throw OTRA; };
    const baraja = (arr) => { const a = arr.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
    return { r, ent, elige, nz, baraja };
  }

  // ---------------- números exactos ----------------
  const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a || 1; };
  const lcm = (a, b) => Math.abs(a * b) / gcd(a, b);
  function F(p, q = 1) {
    if (typeof p === 'object') return p;
    if (!Number.isInteger(p) || !Number.isInteger(q)) throw new Error('fracción con no enteros: ' + p + '/' + q);
    if (q === 0) throw OTRA;
    if (q < 0) { p = -p; q = -q; }
    const g = gcd(p, q);
    return { p: p / g, q: q / g };
  }
  const fadd = (a, b) => { a = F(a); b = F(b); return F(a.p * b.q + b.p * a.q, a.q * b.q); };
  const fsub = (a, b) => { b = F(b); return fadd(a, F(-b.p, b.q)); };
  const fmul = (a, b) => { a = F(a); b = F(b); return F(a.p * b.p, a.q * b.q); };
  const fdiv = (a, b) => { a = F(a); b = F(b); if (b.p === 0) throw OTRA; return F(a.p * b.q, a.q * b.p); };
  const fneg = (a) => { a = F(a); return F(-a.p, a.q); };
  const finv = (a) => fdiv(1, a);
  const fval = (a) => { a = F(a); return a.p / a.q; };
  const fent = (a) => { a = F(a); return a.q === 1; };
  const fpow = (a, n) => { let r = F(1); for (let i = 0; i < Math.abs(n); i++) r = fmul(r, a); return n < 0 ? finv(r) : r; };
  const fact = (n) => { let r = 1; for (let i = 2; i <= n; i++) r *= i; return r; };
  const comb = (n, k) => (k < 0 || k > n ? 0 : Math.round(fact(n) / (fact(k) * fact(n - k))));
  const perm = (n, k) => Math.round(fact(n) / fact(n - k));

  // ---------------- formato (coma decimal, signo −, miles con punto) ----------------
  const MENOS = '−';
  function num(x, d = 6) {
    if (typeof x === 'object') return fq(x);
    if (!Number.isFinite(x) || Math.abs(x) > 1e12) throw OTRA;
    let r = Math.round(x * 10 ** d) / 10 ** d;
    if (Object.is(r, -0) || Math.abs(r) < 1e-12) r = 0;
    const neg = r < 0;
    let [e, dec] = String(Math.abs(r)).split('.');
    if (/e/.test(e)) throw OTRA;
    if (e.length > 4) e = e.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    return (neg ? MENOS : '') + e + (dec ? ',' + dec : '');
  }
  function fq(f) { f = F(f); return f.q === 1 ? num(f.p) : `${num(f.p)}/${f.q}`; }
  const par = (v) => (fval(F(v)) < 0 ? `(${fq(v)})` : fq(v));
  const pesos = (x) => { if (!Number.isInteger(Math.round(x * 1e6) / 1e6) || x < 0) throw OTRA; return '$' + String(Math.round(x)).replace(/\B(?=(\d{3})+(?!\d))/g, '.'); };
  const pct = (x) => `${num(x, 4)} %`;
  const sup = (s) => `<sup>${s}</sup>`;
  const sub = (s) => `<sub>${s}</sub>`;
  // c·√r simplificado: 2√3/3, −√2/2, 5√3
  function rad(c, r) {
    c = F(c);
    if (c.p === 0) return '0';
    let s = 1;
    for (let k = 2; k * k <= r; k++) while (r % (k * k) === 0) { r /= k * k; s *= k; }
    c = fmul(c, s);
    if (r === 1) return fq(c);
    const neg = c.p < 0, p = Math.abs(c.p);
    return (neg ? MENOS : '') + (p === 1 ? '' : num(p)) + '√' + r + (c.q !== 1 ? '/' + c.q : '');
  }
  // c·π: 36π, 32π/3, π/2
  function pit(c) {
    c = F(c);
    if (c.p === 0) return '0';
    const neg = c.p < 0, p = Math.abs(c.p);
    return (neg ? MENOS : '') + (p === 1 ? '' : num(p)) + 'π' + (c.q !== 1 ? '/' + c.q : '');
  }
  // a + b√r (a, b fracciones): 15 + 5√3
  function sumaRad(a, b, r) {
    a = F(a); b = F(b);
    if (b.p === 0) return fq(a);
    if (a.p === 0) return rad(b, r);
    return `${fq(a)} ${b.p < 0 ? MENOS : '+'} ${rad(F(Math.abs(b.p), b.q), r)}`;
  }
  // expresión lineal: [[coef, 'x'], [coef, 'y'], [coef, '']]
  function lin(terms) {
    let s = '';
    for (const [c0, v] of terms) {
      const c = F(c0);
      if (c.p === 0) continue;
      const neg = c.p < 0, a = F(Math.abs(c.p), c.q);
      let cuerpo;
      if (!v) cuerpo = fq(a);
      else if (a.p === 1 && a.q === 1) cuerpo = v;
      else if (a.q === 1) cuerpo = num(a.p) + v;
      else cuerpo = `(${fq(a)})${v}`;
      s += s ? (neg ? ' − ' : ' + ') + cuerpo : (neg ? MENOS : '') + cuerpo;
    }
    return s || '0';
  }
  const ec = (a, b, c, vx = 'x', vy = 'y') => `${lin([[a, vx], [b, vy]])} = ${fq(c)}`;
  const rhs = (m, n) => lin([[m, 'x'], [n, '']]);
  const recta = (m, n) => 'y = ' + rhs(m, n);
  const pt = (x, y) => `(${fq(x)}, ${fq(y)})`;
  const intervalo = (a, b) => `[${fq(a)}, ${fq(b)}]`;
  // n/d y, si se simplifica, «= n'/d'»
  const fracEq = (n, d) => { const r = fq(F(n, d)); return r === `${n}/${d}` ? r : `${n}/${d} = ${r}`; };
  // a·x + b·y con números: «2·3 − (−1)» (sin coeficientes 1)
  function sust(pares) {
    let s = '';
    pares.forEach(([a, v], i) => {
      const cuerpo = (Math.abs(a) === 1 ? '' : num(Math.abs(a)) + '·') + par(v);
      s += i === 0 ? (a < 0 ? MENOS : '') + cuerpo : (a < 0 ? ' − ' : ' + ') + cuerpo;
    });
    return s;
  }
  const suma = (xs) => (xs.length === 1 ? String(xs[0]) : `${xs.join(' + ')} = ${xs.reduce((a, b) => a + b, 0)}`);
  const igual = (a, b) => (a === b ? a : `${a} = ${b}`); // «a = b» sin repetir si son iguales
  const kpor = (k, expr) => (k === 1 ? expr : `${k}(${expr})`);

  // ---------------- figuras (SVG simple, a escala aproximada) ----------------
  const esc = (v) => Math.round(v * 10) / 10;
  // Triángulo rectángulo en C. AC horizontal (abajo), BC vertical (izquierda). et: {AC, BC, AB, ang: 'A'|'B', simb}
  function figTri(ac, bc, et) {
    let k = Math.min(170 / ac, 100 / bc);
    let w = ac * k, h = bc * k;
    w = Math.max(w, 70); h = Math.max(h, 45);
    const C = [34, 18 + h], A = [34 + w, 18 + h], B = [34, 18];
    const W = w + 74, H = h + 44;
    let s = `<svg class="gfig" viewBox="0 0 ${esc(W)} ${esc(H)}" width="${esc(W)}" height="${esc(H)}" role="img" aria-label="Triángulo ABC rectángulo en C">`;
    s += `<path d="M${C[0]} ${C[1]}L${esc(A[0])} ${esc(A[1])}L${B[0]} ${B[1]}Z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>`;
    s += `<path d="M${C[0]} ${esc(C[1] - 11)}h11v11" fill="none" stroke="currentColor" stroke-width="1.5"/>`;
    const V = et.ang === 'B' ? B : A;
    if (et.ang) {
      const u1 = et.ang === 'A' ? [-1, 0] : [0, 1];
      const d = et.ang === 'A' ? [B[0] - A[0], B[1] - A[1]] : [A[0] - B[0], A[1] - B[1]];
      const L = Math.hypot(d[0], d[1]); const u2 = [d[0] / L, d[1] / L];
      const R = 22;
      const p1 = et.ang === 'A' ? [V[0] + u1[0] * R, V[1] + u1[1] * R] : [V[0] + u2[0] * R, V[1] + u2[1] * R];
      const p2 = et.ang === 'A' ? [V[0] + u2[0] * R, V[1] + u2[1] * R] : [V[0] + u1[0] * R, V[1] + u1[1] * R];
      s += `<path d="M${esc(p1[0])} ${esc(p1[1])}A${R} ${R} 0 0 1 ${esc(p2[0])} ${esc(p2[1])}" fill="none" stroke="var(--warn,#e0a000)" stroke-width="2"/>`;
      const bi = [u1[0] + u2[0], u1[1] + u2[1]]; const lb = Math.hypot(bi[0], bi[1]);
      s += `<text x="${esc(V[0] + (bi[0] / lb) * 36)}" y="${esc(V[1] + (bi[1] / lb) * 36 + 5)}" text-anchor="middle" style="fill:var(--warn,#e0a000);font-size:14px">${et.simb || 'α'}</text>`;
    }
    const t = (x, y, txt, an = 'middle') => `<text x="${esc(x)}" y="${esc(y)}" text-anchor="${an}" style="font-size:14px;fill:currentColor">${txt}</text>`;
    s += t(C[0] - 12, C[1] + 6, 'C') + t(A[0] + 12, A[1] + 6, 'A') + t(B[0] - 12, B[1] + 4, 'B');
    if (et.AC) s += t((C[0] + A[0]) / 2, C[1] + 20, et.AC);
    if (et.BC) s += t(C[0] - 8, (C[1] + B[1]) / 2 + 5, et.BC, 'end');
    if (et.AB) s += t((A[0] + B[0]) / 2 + 10, (A[1] + B[1]) / 2 - 6, et.AB, 'start');
    return s + '</svg>';
  }
  // Circunferencia de centro O con A y B abajo (ángulo del centro c) y C arriba.
  function figCirc(c, conCentro = true) {
    const cx = 100, cy = 80, R = 62;
    const P = (g) => [cx + R * Math.cos((g * Math.PI) / 180), cy - R * Math.sin((g * Math.PI) / 180)];
    const A = P(-90 - c / 2), B = P(-90 + c / 2), C = P(90);
    const l = (p, q, w = 2, col = 'currentColor') => `<path d="M${esc(p[0])} ${esc(p[1])}L${esc(q[0])} ${esc(q[1])}" stroke="${col}" stroke-width="${w}"/>`;
    const t = (p, txt, dx, dy) => `<text x="${esc(p[0] + dx)}" y="${esc(p[1] + dy)}" text-anchor="middle" style="font-size:14px;fill:currentColor">${txt}</text>`;
    let s = `<svg class="gfig" viewBox="0 0 200 162" width="200" height="162" role="img" aria-label="Circunferencia con ángulo del centro e inscrito">`;
    s += `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="currentColor" stroke-width="2"/>`;
    s += l(C, A, 2, 'var(--warn,#e0a000)') + l(C, B, 2, 'var(--warn,#e0a000)');
    if (conCentro) s += l([cx, cy], A, 2, 'var(--acc,#0e8bd8)') + l([cx, cy], B, 2, 'var(--acc,#0e8bd8)') + `<circle cx="${cx}" cy="${cy}" r="3" fill="currentColor"/>` + `<text x="${cx + 13}" y="${cy + 5}" text-anchor="middle" style="font-size:14px;fill:currentColor;paint-order:stroke;stroke:var(--panel,#fff);stroke-width:4px">O</text>`;
    s += t(A, 'A', -10, 12) + t(B, 'B', 10, 12) + t(C, 'C', 0, -8);
    return s + '</svg>';
  }

  // =====================================================================
  // M2 · Rectas en el plano + sistemas 2×2
  // =====================================================================
  const T_REC = 'm2.alg.sistemas-rectas';
  fam('rec-pendiente', T_REC, ['basico'], 'Pendiente entre dos puntos', (t) => {
    const x1 = t.ent(-5, 6), x2 = t.ent(-5, 6), y1 = t.ent(-6, 8), y2 = t.ent(-6, 8);
    if (x1 === x2 || y1 === y2) throw OTRA;
    const dx = x2 - x1, dy = y2 - y1, m = F(dy, dx);
    const malas = [
      [fq(F(dx, dy)), 'Invertiste la fórmula: la pendiente es Δy/Δx (lo que sube dividido por lo que avanza), no Δx/Δy.'],
      [fq(F(dy, -dx)), 'Restaste en distinto orden arriba (y₂ − y₁) y abajo (x₁ − x₂). Usa el mismo orden en los dos.'],
      [num(dy), 'Te quedaste solo con lo que sube (Δy). Falta dividir por lo que avanza (Δx).'],
    ];
    if (x1 + x2 !== 0) malas.push([fq(F(y1 + y2, x1 + x2)), 'Sumaste las coordenadas. La pendiente usa diferencias: (y₂ − y₁)/(x₂ − x₁).']);
    return {
      enun: `¿Cuál es la pendiente de la recta que pasa por los puntos ${pt(x1, y1)} y ${pt(x2, y2)}?`,
      ok: fq(m), malas,
      exp: `m = (y₂ − y₁)/(x₂ − x₁) = (${num(y2)} − ${par(y1)})/(${num(x2)} − ${par(x1)}) = ${igual(`${num(dy)}/${num(dx)}`, fq(m))}.`,
      p: { x1, y1, x2, y2 },
    };
  });

  fam('rec-general', T_REC, ['basico', 'paes'], 'Pendiente y coeficiente de posición de ax + by = c', (t, nivel) => {
    const a = t.nz(-6, 6), b = t.nz(-5, 5), c = t.nz(-10, 10);
    if (Math.abs(b) === 1 && nivel === 'paes') throw OTRA;
    const pide = nivel === 'basico' ? 'pend' : t.elige(['pend', 'pos']);
    const m = F(-a, b), n = F(c, b);
    const desp = `${lin([[b, 'y']])} = ${lin([[-a, 'x'], [c, '']])} → y = ${rhs(m, n)}`;
    if (pide === 'pend') {
      return {
        enun: `¿Cuál es la pendiente de la recta ${ec(a, b, c)}?`, ok: fq(m),
        malas: [
          [fq(F(a, b)), 'Olvidaste cambiar el signo al pasar el término con x al otro lado.'],
          [fq(F(-b, a)), 'Dividiste al revés: la pendiente es −a/b (el coeficiente de x sobre el de y, con el signo cambiado).'],
          [fq(n), 'Ese es el coeficiente de posición (donde la recta corta al eje Y), no la pendiente.'],
          [num(a), 'Leíste el coeficiente de x sin despejar y. La pendiente se lee en la forma y = mx + n.'],
        ],
        exp: `Despeja y: ${desp}. La pendiente es ${fq(m)}.`, p: { a, b, c, pide },
      };
    }
    return {
      enun: `¿En qué valor corta al eje Y la recta ${ec(a, b, c)}? (su coeficiente de posición)`, ok: fq(n),
      malas: [
        [num(c), 'Leíste el término libre sin dividir por el coeficiente de y.'],
        [fq(F(-c, b)), 'Cambiaste el signo del término libre: al despejar y, ese número no cambia de lado.'],
        [fq(m), 'Esa es la pendiente, no el coeficiente de posición.'],
        [fq(F(c, a)), 'Dividiste por el coeficiente de x. Para despejar y se divide por el de y.'],
      ],
      exp: `Despeja y: ${desp}. Corta al eje Y en y = ${fq(n)}.`, p: { a, b, c, pide },
    };
  });

  fam('rec-sistema', T_REC, ['basico', 'paes'], 'Resolver un sistema 2×2', (t, nivel) => {
    const x = t.ent(-6, 7), y = t.ent(-6, 7);
    let a1, b1, a2, b2;
    if (nivel === 'basico') { a1 = 1; b1 = t.elige([1, 2, -1]); a2 = t.elige([1, 2, 3]); b2 = t.elige([-1, -2, 1, 3]); }
    else { a1 = t.nz(-5, 5); b1 = t.nz(-5, 5); a2 = t.nz(-5, 5); b2 = t.nz(-5, 5); }
    if (a1 * b2 - a2 * b1 === 0) throw OTRA;
    const c1 = a1 * x + b1 * y, c2 = a2 * x + b2 * y;
    const pide = nivel === 'basico' ? t.elige(['x', 'y']) : t.elige(['x + y', 'x − y', 'x·y', 'x', 'y']);
    const V = { x, y, 'x + y': x + y, 'x − y': x - y, 'x·y': x * y };
    const malas = [];
    const add = (v, tr) => malas.push([fq(v), tr]);
    if (pide === 'x') { add(y, 'Ese es el valor de y. Se pregunta por x.'); add(-x, 'Error de signo al despejar: revisa el signo cada vez que pasas un término al otro lado.'); add(F(c1, a1), 'Despejaste x de la primera ecuación como si y valiera 0.'); }
    if (pide === 'y') { add(x, 'Ese es el valor de x. Se pregunta por y.'); add(-y, 'Error de signo al despejar: revisa el signo cada vez que pasas un término al otro lado.'); add(F(c1, b1), 'Despejaste y de la primera ecuación como si x valiera 0.'); }
    if (pide === 'x + y') { add(x - y, 'Calculaste x − y en vez de x + y.'); add(x, 'Ese es solo el valor de x; falta sumarle y.'); add(y, 'Ese es solo el valor de y; falta sumarle x.'); add(-(x + y), 'Error de signo: revisa los signos de x e y.'); }
    if (pide === 'x − y') { add(x + y, 'Calculaste x + y en vez de x − y.'); add(y - x, 'Restaste al revés: calculaste y − x.'); add(x, 'Ese es solo el valor de x; falta restarle y.'); }
    if (pide === 'x·y') { add(x + y, 'Sumaste en vez de multiplicar.'); add(-x * y, 'Error de signo en una de las variables.'); add(x, 'Ese es solo el valor de x.'); add(y, 'Ese es solo el valor de y.'); }
    return {
      enun: `Si x e y cumplen el sistema<br>${ec(a1, b1, c1)}<br>${ec(a2, b2, c2)}<br>¿cuál es el valor de ${pide}?`,
      ok: fq(V[pide]), malas,
      exp: `Resolviendo (por reducción o por sustitución): x = ${num(x)} e y = ${num(y)}. Comprueba en la primera: ${sust([[a1, x], [b1, y]])} = ${num(c1)}. Entonces ${pide} = ${fq(V[pide])}.`,
      p: { a1, b1, c1, a2, b2, c2, pide },
    };
  });

  fam('rec-tipo', T_REC, ['basico', 'paes'], '¿Cuántas soluciones tiene? (rectas que se cortan, paralelas o iguales)', (t, nivel) => {
    const caso = t.elige(['una', 'ninguna', 'infinitas']);
    let a1, b1, c1;
    if (nivel === 'basico') { const m = t.nz(-4, 4), n = t.ent(-6, 6); a1 = -m; b1 = 1; c1 = n; }
    else { a1 = t.nz(-5, 5); b1 = t.nz(-5, 5); c1 = t.ent(-8, 8); }
    const k = t.elige([2, 3, -2, -1, -3]);
    let a2, b2, c2;
    if (caso === 'infinitas') { a2 = k * a1; b2 = k * b1; c2 = k * c1; }
    else if (caso === 'ninguna') { a2 = k * a1; b2 = k * b1; c2 = k * c1 + t.nz(-5, 5); }
    else { a2 = t.nz(-5, 5); b2 = t.nz(-5, 5); c2 = t.ent(-8, 8); if (a1 * b2 - a2 * b1 === 0) throw OTRA; }
    const m1 = F(-a1, b1), n1 = F(c1, b1), m2 = F(-a2, b2), n2 = F(c2, b2);
    const L1 = nivel === 'basico' ? recta(m1, n1) : ec(a1, b1, c1);
    const OP = { una: 'Exactamente una solución', ninguna: 'Ninguna solución', infinitas: 'Infinitas soluciones', dos: 'Exactamente dos soluciones' };
    const TR = {
      dos: 'Dos rectas distintas se cortan en un punto como máximo: nunca hay exactamente dos soluciones.',
      'una|ninguna': `Las dos rectas tienen pendiente ${fq(m1)} y distinto coeficiente de posición (${fq(n1)} y ${fq(n2)}): son paralelas y nunca se cortan.`,
      'una|infinitas': `Al despejar y, las dos quedan y = ${rhs(m1, n1)}: es la misma recta, y cada uno de sus puntos es solución.`,
      'ninguna|una': `Las pendientes son distintas (${fq(m1)} y ${fq(m2)}): las rectas se cortan en un punto.`,
      'ninguna|infinitas': `Tienen la misma pendiente y también el mismo coeficiente de posición (${fq(n1)}): no son paralelas distintas, son la misma recta.`,
      'infinitas|una': `Para infinitas soluciones las dos ecuaciones deben ser la misma recta; aquí ni siquiera las pendientes son iguales (${fq(m1)} y ${fq(m2)}).`,
      'infinitas|ninguna': `Tienen la misma pendiente (${fq(m1)}), pero distinto coeficiente de posición (${fq(n1)} y ${fq(n2)}): son paralelas, no la misma recta.`,
    };
    const malas = ['una', 'ninguna', 'infinitas', 'dos'].filter((c) => c !== caso).map((c) => [OP[c], c === 'dos' ? TR.dos : TR[`${c}|${caso}`]]);
    const fin = { una: `Pendientes distintas: las rectas se cortan en un solo punto.`, ninguna: `Misma pendiente y distinto coeficiente de posición: son paralelas, no hay solución.`, infinitas: `Misma pendiente y mismo coeficiente de posición: es la misma recta, hay infinitas soluciones.` }[caso];
    return {
      enun: `¿Cuántas soluciones tiene el sistema<br>${L1}<br>${ec(a2, b2, c2)}?`,
      ok: OP[caso], malas, todas: true,
      exp: `Despejando y en cada una: y = ${rhs(m1, n1)} e y = ${rhs(m2, n2)}. ${fin}`,
      p: { a1, b1, c1, a2, b2, c2, caso },
    };
  });

  const linK = (b, c) => `kx ${b < 0 ? MENOS : '+'} ${Math.abs(b) === 1 ? '' : Math.abs(b)}y = ${fq(c)}`;
  fam('rec-k', T_REC, ['dificil'], 'Valor de k para que no haya solución (o haya infinitas)', (t) => {
    const k0 = t.nz(-6, 6), b1 = t.nz(-4, 4), c1 = t.nz(-8, 8), lam = t.elige([2, 3, -2, -1, -3]);
    const a2 = lam * k0, b2 = lam * b1;
    if (t.r() < 0.5) {
      const c2 = lam * c1 + t.nz(-5, 5);
      return {
        enun: `¿Para qué valor de k el sistema<br>${linK(b1, c1)}<br>${ec(a2, b2, c2)}<br>no tiene solución?`,
        ok: num(k0),
        malas: [
          [fq(F(-b1 * b2, a2)), 'Con ese valor las rectas quedan perpendiculares (m₁·m₂ = −1). Sin solución significa paralelas: igual pendiente.'],
          [num(-k0), `Error de signo. Para que sean paralelas, k/${par(a2)} debe ser igual a ${num(b1)}/${par(b2)}.`],
          [fq(F(a2 * b2, b1)), `Cruzaste mal la proporción: es k/${par(a2)} = ${num(b1)}/${par(b2)}, o sea k = ${num(a2)}·${par(b1)}/${par(b2)}.`],
        ],
        exp: `Sin solución = rectas paralelas distintas: los coeficientes de x e y deben ser proporcionales. k/${par(a2)} = ${num(b1)}/${par(b2)} → k = ${num(k0)}. Con k = ${num(k0)}, la segunda ecuación tiene los coeficientes de la primera multiplicados por ${num(lam)}, pero no el término libre (${num(lam)}·${par(c1)} = ${num(lam * c1)} ≠ ${num(c2)}): son paralelas.`,
        p: { tipo: 'ninguna', b1, c1, a2, b2, c2 },
      };
    }
    const c2 = lam * c1;
    return {
      enun: `¿Para qué valor de k el sistema<br>${lin([[k0, 'x'], [b1, 'y']])} = k<br>${ec(a2, b2, c2)}<br>tiene infinitas soluciones?`,
      ok: num(c1),
      malas: [
        [num(c2), `Copiaste el término libre de la otra ecuación. La segunda es la primera multiplicada por ${num(lam)}: hay que dividir ${num(c2)} por ${num(lam)}.`],
        [num(c2 * lam), `Multiplicaste por ${num(lam)} en vez de dividir.`],
        [num(-c1), 'Error de signo al comparar las dos ecuaciones.'],
      ],
      exp: `Infinitas soluciones = la misma recta. La segunda ecuación es la primera multiplicada por ${num(lam)} (${num(a2)} = ${num(lam)}·${par(k0)} y ${num(b2)} = ${num(lam)}·${par(b1)}). Entonces ${num(c2)} = ${num(lam)}·k → k = ${num(c1)}.`,
      p: { tipo: 'infinitas', a1: k0, b1, a2, b2, c2 },
    };
  });

  const PENDS = [[2, 1], [-2, 1], [3, 1], [-3, 1], [1, 2], [-1, 2], [1, 3], [-1, 3], [2, 3], [-2, 3], [3, 2], [-3, 2]];
  fam('rec-perpendicular', T_REC, ['paes', 'dificil'], 'Rectas paralelas y perpendiculares', (t, nivel) => {
    const [mp, mq] = t.elige(PENDS);
    const m = F(mp, mq), mperp = F(-mq, mp), n = F(t.nz(-6, 6));
    const mT = m.q === 1 && m.p > 0 ? num(m.p) : `(${fq(m)})`;
    if (nivel === 'paes') {
      const tipo = t.elige(['perpendicular', 'paralela']);
      if (tipo === 'perpendicular') {
        return {
          enun: `¿Cuál es la pendiente de una recta perpendicular a ${recta(m, n)}?`, ok: fq(mperp),
          malas: [
            [fq(m), 'Esa es la pendiente de una paralela. Para perpendiculares: m₁·m₂ = −1.'],
            [fq(fneg(m)), 'Solo cambiaste el signo; también hay que invertir: m₂ = −1/m₁.'],
            [fq(finv(m)), 'Solo invertiste; también hay que cambiar el signo: m₂ = −1/m₁.'],
            [fq(n), 'Usaste el coeficiente de posición; la pendiente es el número que multiplica a x.'],
          ],
          exp: `La pendiente de la recta es ${fq(m)}. Perpendicular: m₂ = −1/m₁ = ${igual(`−1/${mT}`, fq(mperp))}. Comprueba: ${par(m)}·${par(mperp)} = −1.`,
          p: { m, tipo },
        };
      }
      return {
        enun: `¿Cuál es la pendiente de una recta paralela a ${recta(m, n)}?`, ok: fq(m),
        malas: [
          [fq(mperp), 'Esa es la pendiente de una perpendicular. Las paralelas tienen la misma pendiente.'],
          [fq(fneg(m)), 'Las paralelas tienen la misma pendiente, sin cambiar el signo.'],
          [fq(n), 'Ese es el coeficiente de posición; la pendiente es el número que multiplica a x.'],
        ],
        exp: `Las rectas paralelas tienen igual pendiente: ${fq(m)}.`, p: { m, tipo },
      };
    }
    const L = lcm(Math.abs(mp), mq);
    const p = L * t.nz(-Math.floor(6 / L), Math.floor(6 / L)), q = t.ent(-5, 6);
    const np = fsub(q, fmul(mperp, p));
    return {
      enun: `¿Cuál es la ecuación de la recta que pasa por ${pt(p, q)} y es perpendicular a ${recta(m, n)}?`,
      ok: recta(mperp, np),
      malas: [
        [recta(m, fsub(q, fmul(m, p))), 'Esa recta pasa por el punto, pero es paralela a la dada (misma pendiente). Perpendicular: m₂ = −1/m₁.'],
        [recta(finv(m), fsub(q, fmul(finv(m), p))), 'Invertiste la pendiente, pero sin cambiar el signo: m₂ = −1/m₁.'],
        [recta(mperp, n), 'La pendiente está bien, pero copiaste el coeficiente de posición de la recta dada. Hay que calcularlo con el punto.'],
        [recta(mperp, fadd(q, fmul(mperp, p))), `Error de signo al despejar n: de ${num(q)} = m·${par(p)} + n sale n = ${num(q)} − m·${par(p)}.`],
      ],
      exp: `Pendiente perpendicular: ${igual(`−1/${mT}`, fq(mperp))}. Con el punto: ${num(q)} = ${mperp.q === 1 ? num(mperp.p) : '(' + fq(mperp) + ')'}·${par(p)} + n → n = ${fq(np)}. La recta es ${recta(mperp, np)}.`,
      p: { m, n, p, q },
    };
  });

  fam('rec-corte', T_REC, ['paes', 'dificil'], 'Punto donde se cortan dos rectas', (t, nivel) => {
    const x = t.ent(-5, 6), y = t.ent(-5, 6), m1 = t.nz(-4, 4);
    let m2; do m2 = t.nz(-4, 4); while (m2 === m1);
    const n1 = y - m1 * x, n2 = y - m2 * x;
    let E1 = recta(m1, n1), E2 = recta(m2, n2);
    if (nivel === 'dificil') { const k1 = t.elige([1, 2, -1]), k2 = t.elige([1, -1, 2]); E1 = ec(k1 * m1, -k1, -k1 * n1); E2 = ec(k2 * m2, -k2, -k2 * n2); }
    return {
      enun: `¿En qué punto se cortan las rectas ${E1} y ${E2}?`, ok: pt(x, y),
      malas: [
        [pt(y, x), 'Invertiste las coordenadas: primero va x y después y.'],
        [pt(-x, -m1 * x + n1), 'Error de signo al despejar x: de m₁x + n₁ = m₂x + n₂ sale x = (n₂ − n₁)/(m₁ − m₂).'],
        [pt(0, n1), 'Ese es el punto donde la primera recta corta al eje Y, no donde se cortan las dos rectas.'],
        [pt(0, n2), 'Ese es el punto donde la segunda recta corta al eje Y, no donde se cortan las dos rectas.'],
      ],
      exp: `Despejando y: y = ${rhs(m1, n1)} e y = ${rhs(m2, n2)}. Igualando: ${rhs(m1, n1)} = ${rhs(m2, n2)} → x = ${num(x)}. Reemplazando: y = ${num(y)}. Se cortan en ${pt(x, y)}.`,
      p: { m1, n1, m2, n2 },
    };
  });

  // =====================================================================
  // M2 · Logaritmos + función exponencial y logarítmica
  // =====================================================================
  const T_LOG = 'm2.num.log-exp';
  const potTxt = (b, e) => (e >= 0 ? num(b ** e) : b === 10 ? num(10 ** e) : `1/${num(b ** -e)}`);
  const logDe = (b, arg) => (b === 10 ? `log ${arg}` : `log${sub(b)} ${arg}`);
  fam('log-valor', T_LOG, ['basico'], 'Valor de un logaritmo', (t) => {
    const b = t.elige([2, 3, 5, 10]);
    const k = t.ent(-3, { 2: 7, 3: 5, 5: 4, 10: 5 }[b]);
    if (k === 0) throw OTRA;
    const N = potTxt(b, k);
    const arg = k < 0 && b !== 10 ? `(${N})` : N;
    const malas = [
      [num(-k), k > 0 ? `Error de signo: ${b}${sup(num(-k))} = ${potTxt(b, -k)}, no ${N}.` : `Olvidaste el signo: ${N} = ${b}${sup(num(k))}. Un número entre 0 y 1 tiene logaritmo negativo.`],
      [num(k - 1), `${b}${sup(num(k - 1))} = ${potTxt(b, k - 1)}, no ${N}. Cuenta bien cuántas veces se multiplica ${b}.`],
      [num(k + 1), `${b}${sup(num(k + 1))} = ${potTxt(b, k + 1)}, no ${N}. Cuenta bien cuántas veces se multiplica ${b}.`],
    ];
    if (k >= 2) malas.push([num(b ** k / b), `Dividiste ${N} entre ${b}. El logaritmo es un exponente: ¿a qué hay que elevar ${b} para obtener ${N}?`]);
    return {
      enun: `¿Cuál es el valor de ${logDe(b, arg)}?${b === 10 ? ' (log = logaritmo en base 10)' : ''}`,
      ok: num(k), malas,
      exp: `${b}${sup(num(k))} = ${N}, así que ${logDe(b, arg)} = ${num(k)}.`,
      p: { b, k },
    };
  });

  // log N = ca·a + cb·b + c1, con a = log 2 y b = log 3
  const LOGN = [
    ['12', [2, 1, 0], '12 = 2²·3'], ['18', [1, 2, 0], '18 = 2·3²'], ['24', [3, 1, 0], '24 = 2³·3'], ['36', [2, 2, 0], '36 = 2²·3²'],
    ['54', [1, 3, 0], '54 = 2·3³'], ['72', [3, 2, 0], '72 = 2³·3²'], ['1,5', [-1, 1, 0], '1,5 = 3/2'], ['2/3', [1, -1, 0], '2/3'],
    ['8/3', [3, -1, 0], '8/3 = 2³/3'], ['5', [-1, 0, 1], '5 = 10/2'], ['15', [-1, 1, 1], '15 = 3·10/2'], ['20', [1, 0, 1], '20 = 2·10'],
    ['0,6', [1, 1, -1], '0,6 = 2·3/10'], ['50', [-1, 0, 2], '50 = 100/2'], ['0,2', [1, 0, -1], '0,2 = 2/10'], ['45', [-1, 2, 1], '45 = 3²·10/2'],
  ];
  function combo(ca, cb, c1) {
    const ts = [[ca, 'a'], [cb, 'b'], [c1, '']].filter((x) => x[0] !== 0);
    return lin([...ts.filter((x) => x[0] > 0), ...ts.filter((x) => x[0] < 0)]);
  }
  fam('log-propiedades', T_LOG, ['paes'], 'Propiedades: log de un producto, cociente y potencia', (t) => {
    const [N, [ca, cb, c1], desc] = t.elige(LOGN);
    const ok = combo(ca, cb, c1);
    const malas = [];
    if (ca !== cb) malas.push([combo(cb, ca, c1), 'Cambiaste a por b: a = log 2 y b = log 3.']);
    if (ca >= 2 || cb >= 2) {
      const pv = (c, v) => (c >= 2 ? v + sup(c) : c === 1 ? v : '');
      const partes = [pv(ca, 'a'), pv(cb, 'b')].filter(Boolean);
      const [cc, bb, vv] = ca >= 2 ? [ca, 2, 'a'] : [cb, 3, 'b'];
      if (ca >= 0 && cb >= 0 && c1 === 0) malas.push([partes.join(' + '), `log(${bb}${sup(cc)}) = ${cc}·log ${bb} = ${cc}${vv}. El exponente pasa multiplicando; no queda ${vv}${sup(cc)}.`]);
    }
    if (ca > 0 && cb > 0 && c1 === 0) malas.push([`${ca * cb === 1 ? '' : ca * cb}a·b`, 'log(x·y) = log x + log y. El logaritmo de un producto es una suma, no una multiplicación.']);
    const neg = [[ca, 'a'], [cb, 'b'], [c1, '']].filter((x) => x[0] < 0), pos = [[ca, 'a'], [cb, 'b'], [c1, '']].filter((x) => x[0] > 0);
    if (neg.length === 1 && pos.length >= 1) {
      const arriba = lin(pos), abajo = neg[0][1] ? lin([[-neg[0][0], neg[0][1]]]) : num(10 ** -neg[0][0]);
      malas.push([`${pos.length > 1 ? '(' + arriba + ')' : arriba}/${abajo}`, 'log(x/y) = log x − log y. El logaritmo de un cociente es una resta, no una división.']);
    }
    if (neg.length) malas.push([combo(Math.abs(ca), Math.abs(cb), Math.abs(c1)), `Sumaste un logaritmo que va restando: ${desc}, y en un cociente log(x/y) = log x − log y.`]);
    if (c1 !== 0 && (ca !== 0 || cb !== 0)) malas.push([combo(ca, cb, 0), `Olvidaste el log ${10 ** Math.abs(c1)} = ${Math.abs(c1)} de la descomposición (${desc}).`]);
    if (N === '36') malas.push(['(a + b)<sup>2</sup>', 'log 36 = log(6²) = 2·log 6 = 2(a + b). El exponente pasa multiplicando, no queda (log 6)².']);
    if (N === '20') malas.push(['2a + 1', 'Si escribes 20 = 2²·5, recuerda que log 5 = log(10/2) = 1 − a, no 1. Queda 2a + 1 − a = a + 1.']);
    const arg = N.includes('/') ? `(${N})` : N;
    const tl = [[ca, 'log 2'], [cb, 'log 3'], [Math.sign(c1), Math.abs(c1) === 2 ? 'log 100' : 'log 10']].filter((x) => x[0] !== 0);
    const logs = [...tl.filter((x) => x[0] > 0), ...tl.filter((x) => x[0] < 0)].map(([c, v], i) => (i === 0 ? (c < 0 ? MENOS : '') : c < 0 ? ' − ' : ' + ') + (Math.abs(c) === 1 ? v : Math.abs(c) + '·' + v)).join('');
    return {
      enun: `Si log 2 = a y log 3 = b, ¿cuál es el valor de log ${arg}? (log = logaritmo en base 10)`,
      ok, malas,
      exp: `Descompón: ${desc}. Entonces log ${arg} = ${logs} = ${ok}.`,
      p: { N },
    };
  });

  fam('log-ecuacion-exp', T_LOG, ['paes', 'dificil'], 'Ecuación exponencial (igualar bases)', (t, nivel) => {
    const c = t.elige([2, 3]);
    const exps = c === 2 ? [1, 2, 3, 4, 5] : [1, 2, 3];
    const al = t.elige(exps), be = t.elige(exps);
    if (al === be) throw OTRA;
    const A = c ** al, B = c ** be, x = t.ent(-4, 6), s = t.nz(-4, 4);
    const ex = (k) => lin([[1, 'x'], [k, '']]);
    if (nivel === 'paes') {
      const r = al * (x + s);
      if (r % be !== 0 || r === 0) throw OTRA;
      const tt = r / be;
      const malas = [
        [fq(F(tt - s)), `Igualaste los exponentes sin escribir las dos potencias en la misma base. Primero: ${A} = ${c}${sup(al)} y ${B} = ${c}${sup(be)}.`],
        [fq(F(be * tt - s, al)), `Multiplicaste por ${al} solo la x. Todo el exponente se multiplica: ${kpor(al, ex(s))}.`],
        [num(-x), 'Error de signo al despejar x.'],
        [fq(fsub(F(al * tt, be), s)), `Cambiaste los exponentes: ${A} = ${c}${sup(al)} y ${B} = ${c}${sup(be)}, no al revés.`],
      ];
      return {
        enun: `¿Cuál es el valor de x en la ecuación ${A}${sup(ex(s))} = ${B}${sup(num(tt))}?`, ok: num(x), malas,
        exp: `Misma base: ${c}${sup(kpor(al, ex(s)))} = ${c}${sup(be === 1 ? num(tt) : `${be}·${par(tt)}`)}. Igualando exponentes: ${kpor(al, ex(s))} = ${num(be * tt)}${al === 1 ? '' : ` → ${ex(s)} = ${num(be * tt / al)}`} → x = ${num(x)}.`,
        p: { A, B, s, t: tt, forma: 'pot' },
      };
    }
    const num2 = al * (x + s) - be * x;
    if (num2 % be !== 0) throw OTRA;
    const tt = num2 / be;
    if (tt === s) throw OTRA;
    const malas = [
      [fq(F(tt - s, al - be)), `Multiplicaste solo la x por los exponentes. Todo el exponente se multiplica: ${kpor(al, ex(s))} = ${kpor(be, ex(tt))}.`],
      [num(-x), 'Error de signo al despejar x.'],
      [fq(F(al * tt - be * s, be - al)), `Cambiaste los exponentes: ${A} = ${c}${sup(al)} y ${B} = ${c}${sup(be)}, no al revés.`],
      ['No tiene solución', `Si igualas los exponentes sin cambiar la base, ${ex(s)} = ${ex(tt)} parece imposible. Primero escribe ${A} = ${c}${sup(al)} y ${B} = ${c}${sup(be)}.`],
    ];
    return {
      enun: `¿Cuál es el valor de x en la ecuación ${A}${sup(ex(s))} = ${B}${sup(ex(tt))}?`, ok: num(x), malas,
      exp: `Misma base: ${c}${sup(kpor(al, ex(s)))} = ${c}${sup(kpor(be, ex(tt)))}. Igualando exponentes: ${kpor(al, ex(s))} = ${kpor(be, ex(tt))} → ${lin([[al, 'x'], [al * s, '']])} = ${lin([[be, 'x'], [be * tt, '']])} → x = ${num(x)}.`,
      p: { A, B, s, t: tt, forma: 'pot-x' },
    };
  });

  fam('log-crecimiento', T_LOG, ['basico', 'paes'], 'Crecimiento y decaimiento exponencial', (t, nivel) => {
    const tipo = t.elige(['duplica', 'duplica', 'triplica', 'mitad']);
    const f = { duplica: 2, triplica: 3, mitad: 0.5 }[tipo];
    const P0 = t.elige([100, 200, 250, 300, 400, 500, 800, 1000, 1500, 2000, 3200, 6400]);
    const h = t.elige([2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 30]);
    const k = t.ent(2, tipo === 'triplica' ? 4 : 5);
    const u = t.elige(['minutos', 'horas']);
    const T = k * h;
    if (tipo === 'mitad' && P0 % 2 ** (k + 1)) throw OTRA;
    const P = P0 * f ** k;
    const fs = tipo === 'mitad' ? '(1/2)' : String(f);
    const quien = tipo === 'mitad' ? 'mg' : 'bacterias';
    const intro = tipo === 'mitad'
      ? `Una muestra radiactiva tiene ${num(P0)} mg y su masa se reduce a la mitad cada ${h} ${u}.`
      : `Un cultivo tiene ${num(P0)} bacterias y la cantidad se ${tipo} cada ${h} ${u}.`;
    const enun = nivel === 'basico'
      ? `${intro} ${tipo === 'mitad' ? '¿Cuántos mg quedarán' : '¿Cuántas bacterias habrá'} después de ${T} ${u}?`
      : `${intro} La cantidad después de t ${u} es C(t) = ${num(P0)}·${fs}${sup('t/' + h)}. ¿Cuál es el valor de C(${T})?`;
    const malas = [
      [`${num(P0 * f ** (k - 1))} ${quien}`, `Contaste un período menos: en ${T} ${u} hay ${T}/${h} = ${k} períodos.`],
      [`${num(P0 * f ** (k + 1))} ${quien}`, `Contaste un período de más: en ${T} ${u} hay ${T}/${h} = ${k} períodos.`],
    ];
    if (tipo === 'mitad') malas.push([`${num(P0 / (2 * k))} ${quien}`, `Dividiste por 2·${k}. Se divide por 2 en cada período, o sea por 2${sup(k)} = ${2 ** k}.`]);
    else {
      malas.push([`${num(P0 * (1 + (f - 1) * k))} ${quien}`, `Sumaste ${num(P0 * (f - 1))} en cada período (crecimiento lineal). Al ${tipo === 'duplica' ? 'duplicarse' : 'triplicarse'}, se multiplica por ${f} cada vez: ${num(P0)}·${f}${sup(k)}.`]);
      malas.push([`${num(P0 * f * k)} ${quien}`, `Multiplicaste por ${f}·${k}. Hay que multiplicar ${k} veces por ${f}: ${f}${sup(k)} = ${f ** k}.`]);
    }
    return {
      enun, ok: `${num(P)} ${quien}`, malas,
      exp: `En ${T} ${u} hay ${T}/${h} = ${k} períodos. Cada período multiplica por ${fs}: ${num(P0)}·${fs}${sup(k)} = ${num(P)}.`,
      p: { P0, f, h, T },
    };
  });

  fam('log-tiempo', T_LOG, ['dificil'], '¿Cuánto tiempo tarda? (despejar el exponente)', (t) => {
    const f = t.elige([2, 2, 3]);
    const k = t.ent(2, f === 2 ? 6 : 4);
    const P0 = t.elige([50, 100, 200, 250, 300, 500, 1000]);
    const h = t.elige([2, 3, 4, 5, 6, 8, 10, 12, 15, 20]);
    const u = t.elige(['minutos', 'horas', 'días']);
    const ratio = f ** k, P = P0 * ratio;
    const nom = f === 2 ? 'duplicaciones' : 'triplicaciones';
    return {
      enun: `Una población de ${num(P0)} bacterias se ${f === 2 ? 'duplica' : 'triplica'} cada ${h} ${u}. ¿Cuánto tiempo tarda en llegar a ${num(P)} bacterias?`,
      ok: `${num(k * h)} ${u}`,
      malas: [
        [`${num(k)} ${u}`, `Ese es el número de ${nom} (${f}${sup(k)} = ${ratio}). Cada una dura ${h} ${u}: ${k}·${h} = ${k * h}.`],
        [`${num((h * (ratio - 1)) / (f - 1))} ${u}`, `Supusiste que en cada período se suman ${num(P0 * (f - 1))} bacterias (crecimiento lineal). El crecimiento es exponencial: se multiplica.`],
        [`${num(h * (k + 1))} ${u}`, `Contaste también el instante inicial como un período: hay ${k} períodos, no ${k + 1}.`],
        [`${num(h * k * f)} ${u}`, `Leíste ${f}${sup(k)} como ${f}·${k} = ${f * k} períodos. Son ${k} períodos, porque ${f}${sup(k)} = ${ratio}.`],
      ],
      exp: `${num(P)}/${num(P0)} = ${ratio} = ${f}${sup(k)}: hacen falta ${k} ${nom} de ${h} ${u}. Con logaritmos: t = ${h}·log${sub(f)} ${ratio} = ${h}·${k} = ${k * h} ${u}.`,
      p: { P0, P, f, h },
    };
  });

  fam('log-ecuacion', T_LOG, ['dificil'], 'Ecuación logarítmica (y comprobar la solución)', (t) => {
    const b = t.elige([2, 3]);
    const i = t.ent(1, b === 2 ? 4 : 3), j = t.ent(0, i - 1);
    const r = b ** i, bj = b ** j, d = r - bj, k = i + j, bk = b ** k;
    return {
      enun: `¿Cuál es la solución de la ecuación log${sub(b)} x + log${sub(b)} (x − ${d}) = ${k}?`,
      ok: num(r),
      malas: [
        [`${num(r)} y ${num(-bj)}`, `x = −${bj} no sirve: haría negativo el argumento del logaritmo, y el logaritmo de un número negativo no existe. Siempre comprueba.`],
        [num(-bj), `Elegiste la raíz que no sirve: con x = −${bj}, log${sub(b)} x no existe.`],
        [fq(F(bk + d, 2)), `Escribiste log x + log(x − ${d}) = log(2x − ${d}). La suma de logaritmos es el logaritmo del producto: log[x(x − ${d})].`],
      ],
      exp: `log${sub(b)} x + log${sub(b)} (x − ${d}) = log${sub(b)} [x(x − ${d})] = ${k} → x(x − ${d}) = ${b}${sup(k)} = ${bk} → ${lin([[1, 'x²'], [-d, 'x'], [-bk, '']])} = 0 → x = ${r} o x = −${bj}. Solo x = ${r} deja positivos los dos argumentos.`,
      p: { b, d, k },
    };
  });

  // =====================================================================
  // M2 · Probabilidad condicional
  // =====================================================================
  const T_CON = 'm2.pro.condicional';
  const CTX_TABLA = [
    { quien: 'estudiantes', uno: 'un estudiante', encF: 'Curso', encC: 'Deporte',
      filas: [{ t: '3.° A', sub: 'sea de 3.° A', pl: 'son de 3.° A', inf: 'ser de 3.° A', de: 'de 3.° A' }, { t: '3.° B', sub: 'sea de 3.° B', pl: 'son de 3.° B', inf: 'ser de 3.° B', de: 'de 3.° B' }],
      cols: [{ t: 'Fútbol', sub: 'prefiera fútbol', pl: 'prefieren fútbol', inf: 'preferir fútbol', no: 'no prefiere fútbol', noPl: 'no prefieren fútbol' }, { t: 'Vóleibol', sub: 'prefiera vóleibol', pl: 'prefieren vóleibol', inf: 'preferir vóleibol', no: 'no prefiere vóleibol', noPl: 'no prefieren vóleibol' }, { t: 'Básquetbol', sub: 'prefiera básquetbol', pl: 'prefieren básquetbol', inf: 'preferir básquetbol', no: 'no prefiere básquetbol', noPl: 'no prefieren básquetbol' }] },
    { quien: 'clientes', uno: 'un cliente', encF: 'Bebida', encC: 'Tamaño',
      filas: [{ t: 'Café', sub: 'haya pedido café', pl: 'pidieron café', inf: 'pedir café', de: 'que pidió café' }, { t: 'Té', sub: 'haya pedido té', pl: 'pidieron té', inf: 'pedir té', de: 'que pidió té' }],
      cols: [{ t: 'Chico', sub: 'haya pedido tamaño chico', pl: 'pidieron tamaño chico', inf: 'pedir tamaño chico', no: 'no pidió tamaño chico', noPl: 'no pidieron tamaño chico' }, { t: 'Mediano', sub: 'haya pedido tamaño mediano', pl: 'pidieron tamaño mediano', inf: 'pedir tamaño mediano', no: 'no pidió tamaño mediano', noPl: 'no pidieron tamaño mediano' }, { t: 'Grande', sub: 'haya pedido tamaño grande', pl: 'pidieron tamaño grande', inf: 'pedir tamaño grande', no: 'no pidió tamaño grande', noPl: 'no pidieron tamaño grande' }] },
    { quien: 'postulantes', uno: 'un postulante', encF: 'Jornada', encC: 'Resultado',
      filas: [{ t: 'Mañana', sub: 'sea de la jornada de la mañana', pl: 'son de la jornada de la mañana', inf: 'ser de la jornada de la mañana', de: 'de la jornada de la mañana' }, { t: 'Tarde', sub: 'sea de la jornada de la tarde', pl: 'son de la jornada de la tarde', inf: 'ser de la jornada de la tarde', de: 'de la jornada de la tarde' }],
      cols: [{ t: 'Aprobó', sub: 'haya aprobado', pl: 'aprobaron', inf: 'aprobar', no: 'no aprobó', noPl: 'no aprobaron' }, { t: 'Reprobó', sub: 'haya reprobado', pl: 'reprobaron', inf: 'reprobar', no: 'no reprobó', noPl: 'no reprobaron' }] },
  ];
  fam('cond-tabla', T_CON, ['basico', 'paes', 'dificil'], 'Tabla de doble entrada', (t, nivel) => {
    const C = t.elige(nivel === 'dificil' ? CTX_TABLA.slice(0, 2) : CTX_TABLA);
    const nc = C.cols.length;
    const tab = C.filas.map(() => C.cols.map(() => t.ent(3, 25)));
    const Rt = tab.map((f) => f.reduce((a, b) => a + b, 0));
    const Ct = C.cols.map((_, j) => tab.reduce((a, f) => a + f[j], 0));
    const N = Rt.reduce((a, b) => a + b, 0);
    const i = t.ent(0, 1), j = t.ent(0, nc - 1), F_ = C.filas[i], K = C.cols[j], n = tab[i][j];
    const tot = nivel === 'basico';
    // sumas a la vista (la tabla de PAES y Difícil no trae totales)
    const sR = tot ? String(Rt[i]) : suma(tab[i]);
    const sC = tot ? String(Ct[j]) : suma(tab.map((f) => f[j]));
    let h = `<table><tr><th>${C.encF} \\ ${C.encC}</th>${C.cols.map((c) => `<th>${c.t}</th>`).join('')}${tot ? '<th>Total</th>' : ''}</tr>`;
    C.filas.forEach((f, a) => { h += `<tr><th>${f.t}</th>${tab[a].map((v) => `<td>${v}</td>`).join('')}${tot ? `<td>${Rt[a]}</td>` : ''}</tr>`; });
    if (tot) h += `<tr><th>Total</th>${Ct.map((v) => `<td>${v}</td>`).join('')}<td>${N}</td></tr>`;
    h += '</table>';
    const pre = `La tabla muestra a ${N} ${C.quien}.${h}`;
    const tipo = nivel === 'basico' ? 'col|fila' : nivel === 'paes' ? t.elige(['fila|col', 'col|fila']) : 'fila|nocol';
    if (tipo === 'col|fila') {
      return {
        enun: `${pre}Se elige al azar ${C.uno} ${F_.de}. ¿Cuál es la probabilidad de que ${K.sub}?`, ok: fq(F(n, Rt[i])),
        malas: [
          [fq(F(n, Ct[j])), `Dividiste por todos los que ${K.pl} (${Ct[j]}). La condición es ${F_.inf}: el total se reduce a los ${Rt[i]} que ${F_.pl}.`],
          [fq(F(n, N)), `Esa es la probabilidad de ${F_.inf} y ${K.inf}, sobre todos. Como ya se sabe que es ${F_.de.replace(/^que /, 'alguien que ')}, se divide por ${Rt[i]}.`],
          [fq(F(Ct[j], N)), `Esa es la probabilidad de ${K.inf} entre todos: no usaste la condición.`],
          [fq(F(Rt[i], N)), `Esa es la probabilidad de ${F_.inf}, que ya se sabe.`],
        ],
        exp: `Solo cuentan los que ${F_.pl}: ${sR}. De ellos, ${n} ${K.pl}. P = ${fracEq(n, Rt[i])}.`,
        p: { tab, tipo, i, j },
      };
    }
    if (tipo === 'fila|col') {
      return {
        enun: `${pre}Se elige al azar ${C.uno} y resulta que ${K.no.replace(/^no /, '')}. ¿Cuál es la probabilidad de que ${F_.sub}?`, ok: fq(F(n, Ct[j])),
        malas: [
          [fq(F(n, Rt[i])), `Dividiste por el total de la fila (${Rt[i]}). La condición es ${K.inf}: el total se reduce a los ${Ct[j]} que ${K.pl}.`],
          [fq(F(n, N)), `Esa es la probabilidad de ${F_.inf} y ${K.inf}, sobre todos. Como ya se sabe lo segundo, se divide por ${Ct[j]}.`],
          [fq(F(Rt[i], N)), `Esa es la probabilidad de ${F_.inf} entre todos: no usaste la condición.`],
          [fq(F(Ct[j] - n, Ct[j])), 'Tomaste la otra fila: contaste a los que no cumplen lo pedido.'],
        ],
        exp: `Solo cuentan los que ${K.pl}: ${sC}. De ellos, ${n} ${F_.pl}. P = ${fracEq(n, Ct[j])}.`,
        p: { tab, tipo, i, j },
      };
    }
    const rest = Rt[i] - n, base = N - Ct[j];
    const restoFila = tab[i].filter((_, c) => c !== j), restoBase = tab.flatMap((f) => f.filter((_, c) => c !== j));
    return {
      enun: `${pre}Se elige al azar ${C.uno} que ${K.no}. ¿Cuál es la probabilidad de que ${F_.sub}?`, ok: fq(F(rest, base)),
      malas: [
        [fq(F(n, Ct[j])), `Usaste a los que sí ${K.pl}. La condición es que NO.`],
        [fq(F(rest, N)), `Dividiste por todos (${N}). La condición deja solo a los ${base} que ${K.noPl}.`],
        [fq(F(rest, Rt[i])), `Dividiste por el total de la fila. Abajo va el grupo de la condición: los ${base} que ${K.noPl}.`],
        [fq(F(Rt[i], N)), `No usaste la condición: esa es la probabilidad de ${F_.inf} entre todos.`],
      ],
      exp: `Los que ${K.noPl}: ${suma(restoBase)}. De ellos, ${F_.pl} ${suma(restoFila)}. P = ${fracEq(rest, base)}.`,
      p: { tab, tipo, i, j },
    };
  });
  fam('cond-arbol', T_CON, ['paes', 'dificil'], 'Árbol: probabilidad total y «al revés»', (t, nivel) => {
    const pA = t.elige([20, 25, 30, 40, 60, 70, 75, 80]), pB = 100 - pA;
    const D = [2, 3, 4, 5, 6, 8, 10, 12, 15, 20];
    const dA = t.elige(D); let dB; do dB = t.elige(D); while (dB === dA);
    const C = t.elige([
      { intro: `Una fábrica tiene dos máquinas. La máquina A hace el ${pA} % de las piezas y la B, el resto. Son defectuosas el ${dA} % de las piezas de A y el ${dB} % de las de B.`, obj: 'una pieza', ev: 'sea defectuosa', evInd: 'es defectuosa', a: 'venga de la máquina A', b: 'venga de la máquina B', A: 'máquina A', B: 'máquina B', E: 'defectuosa', rA: 'la rama de la máquina A', rB: 'la de la máquina B', aA: 'a la máquina A' },
      { intro: `En un colegio, el ${pA} % de los estudiantes llega en bus y el resto en metro. Llega atrasado el ${dA} % de los que vienen en bus y el ${dB} % de los que vienen en metro.`, obj: 'un estudiante', ev: 'llegue atrasado', evInd: 'llegó atrasado', a: 'haya venido en bus', b: 'haya venido en metro', A: 'bus', B: 'metro', E: 'atrasado', rA: 'la rama del bus', rB: 'la del metro', aA: 'al bus' },
    ]);
    const tot = pA * dA + pB * dB; // en «diezmilésimos»
    const d4 = (x) => num(x / 10000);
    if (nivel === 'paes') {
      return {
        enun: `${C.intro} Se elige ${C.obj} al azar. ¿Cuál es la probabilidad de que ${C.ev}?`, ok: pct(tot / 100),
        malas: [
          [pct(dA + dB), `Sumaste los porcentajes de las dos ramas sin ponderar por cuánto pesa cada una (${pA} % y ${pB} %).`],
          [pct((dA + dB) / 2), `Promediaste las dos ramas como si cada una pesara 50 %. Hay que ponderar: ${pA} % y ${pB} %.`],
          [pct((pA * dA) / 100), `Contaste solo ${C.rA}. Falta sumar ${C.rB}.`],
          [pct((pA * dB + pB * dA) / 100), `Cruzaste las ramas: ${C.aA} (${pA} %) le corresponde el ${dA} %, no el ${dB} %.`],
        ],
        exp: `Probabilidad total = suma de las dos ramas: ${num(pA / 100)}·${num(dA / 100)} + ${num(pB / 100)}·${num(dB / 100)} = ${d4(pA * dA)} + ${d4(pB * dB)} = ${d4(tot)} = ${pct(tot / 100)}.`,
        p: { pA, dA, dB, pide: 'total' },
      };
    }
    return {
      enun: `${C.intro} Se elige ${C.obj} al azar y ${C.evInd}. ¿Cuál es la probabilidad de que ${C.a}?`, ok: fq(F(pA * dA, tot)),
      malas: [
        [fq(F(pA * dA, 10000)), `Esa es P(${C.A} y ${C.E}) sobre todos. Como ya se sabe que ${C.evInd}, hay que dividirla por P(${C.E}) = ${d4(tot)}.`],
        [fq(F(dA, 100)), `Esa es P(${C.E} | ${C.A}) = ${dA} %. Aquí la condición va al revés: se sabe que ${C.evInd} y se pregunta por ${C.A}.`],
        [fq(F(pA, 100)), `Esa es P(${C.A}) sin usar la información de que ${C.evInd}.`],
        [fq(F(pB * dB, tot)), `Esa es la probabilidad de que ${C.b}: tomaste la otra rama.`],
      ],
      exp: `P(${C.A} y ${C.E}) = ${num(pA / 100)}·${num(dA / 100)} = ${d4(pA * dA)}. P(${C.E}) = ${d4(pA * dA)} + ${num(pB / 100)}·${num(dB / 100)} = ${d4(tot)}. P(${C.A} | ${C.E}) = ${d4(pA * dA)}/${d4(tot)} = ${fq(F(pA * dA, tot))}.`,
      p: { pA, dA, dB, pide: 'bayes' },
    };
  });
  fam('cond-urna', T_CON, ['basico', 'paes', 'dificil'], 'Extracciones sin reposición', (t, nivel) => {
    const r = t.ent(2, 8), a = t.ent(2, 8), n = r + a;
    const [cR, cA] = t.elige([['rojas', 'azules'], ['verdes', 'blancas'], ['negras', 'amarillas']]);
    const sing = (s) => s.slice(0, -1);
    const intro = `Una caja tiene ${r} fichas ${cR} y ${a} ${cA}. Se sacan dos fichas al azar, una tras otra y sin devolverlas.`;
    if (nivel === 'basico') {
      return {
        enun: `${intro} Si la primera fue ${sing(cR)}, ¿cuál es la probabilidad de que la segunda también sea ${sing(cR)}?`, ok: fq(F(r - 1, n - 1)),
        malas: [
          [fq(F(r, n)), `Esa sería con reposición. Al no devolverla, queda una ficha ${sing(cR)} menos y una ficha menos en total.`],
          [fq(F(r - 1, n)), 'Restaste la ficha arriba, pero no abajo: también hay una ficha menos en total.'],
          [fq(F(r, n - 1)), `Restaste una ficha del total, pero no de las ${cR}.`],
        ],
        exp: `Después de sacar una ${sing(cR)} quedan ${r - 1} ${cR} de ${n - 1} fichas: P = ${r - 1}/${n - 1}${fq(F(r - 1, n - 1)) !== `${r - 1}/${n - 1}` ? ' = ' + fq(F(r - 1, n - 1)) : ''}.`,
        p: { r, a, pide: 'segunda' },
      };
    }
    if (nivel === 'paes') {
      return {
        enun: `${intro} ¿Cuál es la probabilidad de que las dos sean ${cR}?`, ok: fq(F(r * (r - 1), n * (n - 1))),
        malas: [
          [fq(F(r * r, n * n)), `Esa sería con reposición. Sin devolver, la segunda es ${r - 1}/${n - 1}.`],
          [fq(F(r * (r - 1), n * n)), 'En la segunda extracción restaste una ficha arriba, pero no abajo.'],
          ...(fval(fadd(F(r, n), F(r - 1, n - 1))) < 1 ? [[fq(fadd(F(r, n), F(r - 1, n - 1))), 'Sumaste las probabilidades. Para «la primera y la segunda» se multiplican.']] : []),
        ],
        exp: `P = ${r}/${n} · ${r - 1}/${n - 1} = ${r * (r - 1)}/${n * (n - 1)} = ${fq(F(r * (r - 1), n * (n - 1)))}.`,
        p: { r, a, pide: 'ambas' },
      };
    }
    return {
      enun: `${intro} ¿Cuál es la probabilidad de sacar una ficha de cada color?`, ok: fq(F(2 * r * a, n * (n - 1))),
      malas: [
        [fq(F(r * a, n * (n - 1))), `Contaste solo «${sing(cR)} y después ${sing(cA)}». También sirve «${sing(cA)} y después ${sing(cR)}».`],
        [fq(F(2 * r * a, n * n)), `Esa sería con reposición. Sin devolver, la segunda se divide por ${n - 1}.`],
        [fq(fsub(1, F(r * (r - 1), n * (n - 1)))), `Restaste a 1 solo el caso «dos ${cR}». También hay que restar «dos ${cA}».`],
      ],
      exp: `Dos órdenes: ${r}/${n}·${a}/${n - 1} + ${a}/${n}·${r}/${n - 1} = ${2 * r * a}/${n * (n - 1)} = ${fq(F(2 * r * a, n * (n - 1)))}.`,
      p: { r, a, pide: 'distintas' },
    };
  });

  // =====================================================================
  // M2 · Permutaciones y combinatoria
  // =====================================================================
  const T_COMB = 'm2.pro.combinatoria';
  const NOMBRES = [['Ana', 'Benja'], ['Camila', 'Diego'], ['Elena', 'Fran'], ['Gabi', 'Hugo'], ['Isa', 'Joaquín']];
  fam('comb-fila', T_COMB, ['basico', 'paes', 'dificil'], 'Ordenar en fila (con y sin condición)', (t, nivel) => {
    const n = t.ent(nivel === 'basico' ? 4 : 5, 8);
    const [A, B] = t.elige(NOMBRES);
    const f = fact(n), f1 = fact(n - 1);
    if (nivel === 'basico') {
      const obj = t.elige(['libros distintos en un estante', 'personas en una fila', 'autos distintos en una fila de estacionamientos']);
      return {
        enun: `¿De cuántas formas se pueden ordenar ${n} ${obj}?`, ok: num(f),
        malas: [
          [num(n * n), `Multiplicaste ${n}·${n}. Para el primer lugar hay ${n} opciones, para el segundo ${n - 1}, y así hasta 1.`],
          [num(n * (n - 1)), 'Contaste solo los dos primeros lugares. Sigue hasta el último: n·(n − 1)·…·1.'],
          [num(f1), `Te faltó un factor: ${n}! = ${n}·${n - 1}·…·1, no ${n - 1}!.`],
          [num(n ** n), 'Permitiste repetir: cada uno ocupa un solo lugar, así que las opciones van bajando.'],
        ],
        exp: `${n} opciones para el primer lugar, ${n - 1} para el segundo… → ${n}! = ${num(f)}.`, p: { n, pide: 'todas' },
      };
    }
    if (nivel === 'paes') {
      return {
        enun: `${n} personas, entre ellas ${A} y ${B}, se ordenan en una fila. ¿De cuántas formas pueden ordenarse si ${A} y ${B} deben quedar juntos?`, ok: num(2 * f1),
        malas: [
          [num(f1), `Pegaste a ${A} y ${B} en un bloque, pero olvidaste que dentro del bloque pueden ir en 2 órdenes (${A}–${B} o ${B}–${A}).`],
          [num(f), 'No usaste la condición: ese es el total de filas.'],
          [num(f - 2 * f1), `Ese es el número de filas donde ${A} y ${B} NO quedan juntos.`],
        ],
        exp: `Junta a ${A} y ${B} en un bloque: quedan ${n - 1} «piezas» → ${n - 1}! = ${num(f1)} órdenes. Dentro del bloque, 2 órdenes. Total: 2·${num(f1)} = ${num(2 * f1)}.`,
        p: { n, pide: 'juntos' },
      };
    }
    return {
      enun: `${n} personas, entre ellas ${A} y ${B}, se ordenan en una fila. ¿De cuántas formas pueden ordenarse si ${A} y ${B} NO pueden quedar juntos?`, ok: num(f - 2 * f1),
      malas: [
        [num(2 * f1), `Ese es el número de filas donde ${A} y ${B} SÍ quedan juntos.`],
        [num(f - f1), `Restaste las filas con ellos juntos, pero olvidaste multiplicar por 2 (pueden ir ${A}–${B} o ${B}–${A}).`],
        [num(f), 'No usaste la condición: ese es el total de filas.'],
      ],
      exp: `Total: ${n}! = ${num(f)}. Juntos: 2·${n - 1}! = ${num(2 * f1)}. No juntos = total − juntos = ${num(f - 2 * f1)}.`,
      p: { n, pide: 'separados' },
    };
  });

  fam('comb-cargos', T_COMB, ['basico', 'paes'], 'Elegir con orden (cargos, podio)', (t) => {
    const k = t.elige([2, 3, 3]), n = t.ent(k + 2, 12);
    const C = t.elige([
      { enun: `En una carrera corren ${n} atletas. ¿De cuántas formas distintas pueden quedar ${k === 3 ? 'el 1.°, el 2.° y el 3.° lugar' : 'el 1.° y el 2.° lugar'}?`, quien: 'un atleta', u: 'lugar', us: 'lugares' },
      { enun: `Un curso de ${n} estudiantes debe elegir ${k === 3 ? 'presidencia, secretaría y tesorería' : 'presidencia y secretaría'}. Nadie puede tener dos cargos. ¿De cuántas formas se puede hacer?`, quien: 'una persona', u: 'cargo', us: 'cargos' },
    ]);
    const V = perm(n, k);
    return {
      enun: C.enun, ok: num(V),
      malas: [
        [num(comb(n, k)), `Contaste grupos sin orden. Aquí los ${C.us} son distintos: sí importa el orden.`],
        [num(n ** k), `Permitiste que ${C.quien} ocupe dos ${C.us} a la vez.`],
        [num(n * k), `Multiplicaste ${n}·${k}. Es un factor por ${C.u}, cada uno con una opción menos: ${n}·${n - 1}${k === 3 ? '·' + (n - 2) : ''}.`],
      ],
      exp: `Con orden y sin repetir: ${n}·${n - 1}${k === 3 ? '·' + (n - 2) : ''} = ${num(V)}.`, p: { n, k, pide: 'variacion' },
    };
  });

  fam('comb-comite', T_COMB, ['paes', 'dificil'], 'Elegir sin orden (comités)', (t, nivel) => {
    if (nivel === 'paes') {
      const n = t.ent(6, 12), k = t.ent(2, Math.min(5, n - 2));
      return {
        enun: `¿De cuántas formas se puede elegir un comité de ${k} personas entre ${n}?`, ok: num(comb(n, k)),
        malas: [
          [num(perm(n, k)), `Contaste con orden. En un comité no importa el orden: hay que dividir por ${k}! = ${fact(k)}.`],
          [num(n * k), `Multiplicaste ${n}·${k}. Se usa C(${n}, ${k}) = ${n}!/(${k}!·${n - k}!).`],
          [num(n ** k), 'Permitiste elegir a la misma persona más de una vez, y además con orden.'],
        ],
        exp: `C(${n}, ${k}) = ${n}!/(${k}!·${n - k}!) = ${num(comb(n, k))}.`, p: { n, k, pide: 'comb' },
      };
    }
    const m = t.ent(4, 9), q = t.ent(4, 9), a = t.ent(1, 3), b = t.ent(1, 3);
    const ok = comb(m, a) * comb(q, b);
    return {
      enun: `En 3.° medio hay ${m} estudiantes y en 4.° medio hay ${q}. ¿De cuántas formas se puede armar una comisión con ${a} ${a === 1 ? 'estudiante' : 'estudiantes'} de 3.° y ${b} de 4.°?`, ok: num(ok),
      malas: [
        [num(comb(m, a) + comb(q, b)), 'Sumaste las formas de cada curso. Se eligen los dos grupos a la vez: se multiplican.'],
        [num(comb(m + q, a + b)), `Juntaste a todos (${m + q}) y olvidaste la condición de cuántos de cada curso.`],
        [num(perm(m, a) * perm(q, b)), 'Usaste orden. En una comisión no importa el orden.'],
      ],
      exp: `C(${m}, ${a})·C(${q}, ${b}) = ${comb(m, a)}·${comb(q, b)} = ${num(ok)}.`, p: { m, a, q, b, pide: 'dos' },
    };
  });

  const PALABRAS = ['BANANA', 'PAPAYA', 'CARRERA', 'MANZANA', 'COCO', 'ACACIA', 'RECORRER', 'TOMATERO', 'PERRERA', 'ALBAHACA', 'CALCETA'];
  fam('comb-anagramas', T_COMB, ['paes', 'dificil'], 'Ordenar letras con repetición', (t, nivel) => {
    const w = t.elige(PALABRAS);
    const cuenta = {}; for (const ch of w) cuenta[ch] = (cuenta[ch] || 0) + 1;
    const rep = Object.entries(cuenta).filter(([, c]) => c > 1);
    if (rep.length < 2) throw OTRA;
    const n = w.length, den = rep.reduce((a, [, c]) => a * fact(c), 1), total = fact(n) / den;
    const descr = rep.map(([ch, c]) => `${ch} ${c} veces`).join(', ');
    if (nivel === 'paes') {
      const max = rep.reduce((a, b) => (b[1] > a[1] ? b : a));
      const sm = rep.reduce((a, [, c]) => a + c, 0);
      return {
        enun: `¿Cuántas «palabras» distintas (con o sin sentido) se pueden formar ordenando todas las letras de ${w}?`, ok: num(total),
        malas: [
          [num(fact(n)), 'No dividiste por las letras repetidas: intercambiar dos letras iguales da la misma palabra.'],
          [num(fact(n) / fact(max[1])), `Dividiste solo por la ${max[0]} repetida. Hay que dividir por cada letra que se repite (${descr}).`],
          [num(fact(n) / fact(sm)), `Dividiste por (${rep.map((x) => x[1]).join(' + ')})!; se divide por el producto ${rep.map((x) => x[1] + '!').join('·')}.`],
        ],
        exp: `${n} letras, con ${descr}: ${n}!/(${rep.map((x) => x[1] + '!').join('·')}) = ${num(fact(n))}/${den} = ${num(total)}.`,
        p: { w, pide: 'todas' },
      };
    }
    // difícil: deben empezar con una letra dada
    const X = t.elige(rep)[0], cx = cuenta[X];
    const c2 = { ...cuenta, [X]: cx - 1 };
    const den2 = Object.values(c2).reduce((a, c) => a * fact(c), 1);
    const ok = fact(n - 1) / den2;
    const malas = [
      [num(total), 'No usaste la condición: ese es el total de ordenamientos.'],
      [num(fact(n - 1) / den), `Fijaste la ${X} al comienzo, pero seguiste dividiendo por ${cx}!: entre las letras que quedan hay solo ${cx - 1} letra${cx - 1 === 1 ? '' : 's'} ${X}.`],
      [num(fact(n - 1)), `Fijaste la ${X}, pero no dividiste por las letras repetidas que quedan.`],
    ];
    if (Number.isInteger(total / n)) malas.push([num(total / n), `Dividiste el total por ${n}, como si cada letra tuviera la misma chance de ir primero. La ${X} aparece ${cx} veces: su parte es ${cx}/${n} del total.`]);
    return {
      enun: `Con todas las letras de ${w}, ¿cuántas «palabras» distintas (con o sin sentido) empiezan con ${X}?`, ok: num(ok), malas,
      exp: `Fija una ${X} al comienzo. Quedan ${n - 1} letras, con ${Object.entries(c2).filter(([, c]) => c > 1).map(([ch, c]) => `${ch} ${c} veces`).join(', ') || 'ninguna repetida'}: ${n - 1}!/(${Object.values(c2).filter((c) => c > 1).map((c) => c + '!').join('·') || '1'}) = ${num(fact(n - 1))}/${den2} = ${num(ok)}.`,
      p: { w, pide: 'empieza', X },
    };
  });
  fam('comb-numeros', T_COMB, ['paes', 'dificil'], 'Formar números con dígitos', (t, nivel) => {
    const d = t.ent(5, 9), k = t.elige([3, 3, 4]);
    if (nivel === 'paes') {
      if (t.r() < 0.5) {
        return {
          enun: `¿Cuántos números de ${k} cifras distintas se pueden formar con los dígitos del 1 al ${d}?`, ok: num(perm(d, k)),
          malas: [
            [num(d ** k), 'Permitiste repetir cifras; aquí deben ser distintas.'],
            [num(comb(d, k)), 'Contaste grupos de cifras sin orden; 123 y 321 son números distintos.'],
            [num(d * k), `Multiplicaste ${d}·${k}. Son ${d} opciones para la primera cifra, ${d - 1} para la segunda…`],
          ],
          exp: `${d}·${d - 1}·${d - 2}${k === 4 ? '·' + (d - 3) : ''} = ${num(perm(d, k))}.`, p: { d, k, pide: 'distintas' },
        };
      }
      return {
        enun: `¿Cuántos números de ${k} cifras se pueden formar con los dígitos del 1 al ${d}, si se pueden repetir?`, ok: num(d ** k),
        malas: [
          [num(perm(d, k)), 'Exigiste cifras distintas; aquí se pueden repetir.'],
          [num(k ** d), `Invertiste base y exponente: son ${d} opciones en cada una de las ${k} cifras → ${d}${sup(k)}.`],
          [num(d * k), `Sumaste ${k} veces ${d}. Las opciones de cada cifra se multiplican.`],
        ],
        exp: `${d} opciones para cada una de las ${k} cifras: ${d}${sup(k)} = ${num(d ** k)}.`, p: { d, k, pide: 'repite' },
      };
    }
    const e = Math.floor(d / 2), ok = e * perm(d - 1, k - 1);
    const malas = [
      [num(e * d ** (k - 1)), 'Permitiste repetir cifras; deben ser distintas.'],
      [num(e * perm(d, k - 1)), `Olvidaste que la última cifra ya se usó: para las otras quedan ${d - 1} dígitos, no ${d}.`],
      [num(perm(d - 1, k - 1)), `Olvidaste multiplicar por las ${e} opciones de la última cifra (${[2, 4, 6, 8].filter((x) => x <= d).join(', ')}).`],
    ];
    if (d % 2) malas.push([num(perm(d, k) / 2), `Dividiste por 2 como si la mitad de los dígitos fueran pares. Del 1 al ${d} hay ${e} pares y ${d - e} impares.`]);
    return {
      enun: `¿Cuántos números pares de ${k} cifras distintas se pueden formar con los dígitos del 1 al ${d}?`, ok: num(ok), malas,
      exp: `Empieza por la restricción: la última cifra debe ser par (${e} opciones). Las otras ${k - 1} cifras se eligen con orden entre los ${d - 1} dígitos que quedan: ${e}·${perm(d - 1, k - 1)} = ${num(ok)}.`,
      p: { d, k, pide: 'pares' },
    };
  });

  // =====================================================================
  // M2 · Razones trigonométricas
  // =====================================================================
  const T_TRIG = 'm2.geo.trig-razones';
  const TRIPLES = [[3, 4, 5], [5, 12, 13], [8, 15, 17], [7, 24, 25], [20, 21, 29], [6, 8, 10], [9, 12, 15]];
  fam('trig-razon', T_TRIG, ['basico', 'paes'], 'Seno, coseno y tangente en el triángulo rectángulo', (t, nivel) => {
    let [p, q, h] = t.elige(TRIPLES);
    const s = t.elige([1, 1, 2]); p *= s; q *= s; h *= s;
    if (t.r() < 0.5) [p, q] = [q, p];
    const BC = p, AC = q, AB = h; // α en A: opuesto BC, adyacente AC
    const ang = nivel === 'basico' ? 'A' : t.elige(['A', 'B']);
    const pide = t.elige(['sen', 'cos', 'tan']);
    const op = ang === 'A' ? BC : AC, ad = ang === 'A' ? AC : BC;
    const val = { sen: F(op, h), cos: F(ad, h), tan: F(op, ad) };
    let et = { AC: AC + '', BC: BC + '', AB: AB + '', ang, simb: ang === 'A' ? 'α' : 'β' };
    let falta = null;
    if (nivel === 'paes') {
      const OP = ang === 'A' ? 'BC' : 'AC', AD = ang === 'A' ? 'AC' : 'BC';
      falta = t.elige({ sen: [OP, 'AB'], cos: [AD, 'AB'], tan: [OP, AD] }[pide]); et[falta] = '';
    }
    const sim = ang === 'A' ? 'α' : 'β';
    const T = {
      sen: [[val.cos, `Usaste el cateto adyacente a ${sim}; el seno usa el opuesto.`], [val.tan, 'Dividiste por el otro cateto; el seno es opuesto/hipotenusa.'], [F(h, op), 'Invertiste la razón: el seno es opuesto/hipotenusa.']],
      cos: [[val.sen, `Usaste el cateto opuesto a ${sim}; el coseno usa el adyacente.`], [val.tan, 'Esa es la tangente (opuesto/adyacente).'], [F(h, ad), 'Invertiste la razón: el coseno es adyacente/hipotenusa.']],
      tan: [[F(ad, op), 'Invertiste la razón: la tangente es opuesto/adyacente.'], [val.sen, 'Ese es el seno: dividiste por la hipotenusa.'], [val.cos, 'Ese es el coseno: usaste el adyacente sobre la hipotenusa.']],
    };
    const malas = T[pide].map(([v, tr]) => [fq(v), tr]);
    if (falta === 'AB' && pide !== 'tan') malas.push([fq(F(pide === 'sen' ? op : ad, BC + AC)), `La hipotenusa no es la suma de los catetos: por Pitágoras, AB = √(${AC}² + ${BC}²) = ${AB}.`]);
    if (falta && falta !== 'AB') {
      const conocido = falta === 'AC' ? BC : AC, malo = AB - conocido;
      const esOp = falta === (ang === 'A' ? 'BC' : 'AC'); // el cateto que falta, ¿es el opuesto al ángulo?
      const o2 = esOp ? malo : op, a2 = esOp ? ad : malo;
      const v = pide === 'sen' ? (esOp ? F(o2, h) : null) : pide === 'cos' ? (esOp ? null : F(a2, h)) : F(o2, a2);
      if (v) malas.push([fq(v), `El cateto que falta no es ${AB} − ${conocido}: por Pitágoras, ${falta} = √(${AB}² − ${conocido}²) = ${falta === 'AC' ? AC : BC}.`]);
    }
    const nom = { sen: 'sen', cos: 'cos', tan: 'tan' }[pide];
    return {
      enun: `En el triángulo ABC, rectángulo en C, ${nivel === 'paes' ? 'se conocen dos lados (ver figura). ¿Cuál' : '¿cuál'} es el valor de ${nom} ${sim}?${figTri(AC, BC, et)}`,
      ok: fq(val[pide]), malas,
      exp: `${falta ? `Falta ${falta}; por Pitágoras, ${falta} = ${falta === 'AC' ? AC : falta === 'BC' ? BC : AB}. ` : ''}Para ${sim}: opuesto = ${op}, adyacente = ${ad}, hipotenusa = ${h}. ${nom} ${sim} = ${pide === 'sen' ? 'opuesto/hipotenusa' : pide === 'cos' ? 'adyacente/hipotenusa' : 'opuesto/adyacente'} = ${fq(val[pide])}.`,
      p: { AC, BC, AB, ang, pide },
    };
  });

  // valores exactos: [coeficiente, radicando]
  const TV = { 30: { sen: [F(1, 2), 1], cos: [F(1, 2), 3], tan: [F(1, 3), 3] }, 45: { sen: [F(1, 2), 2], cos: [F(1, 2), 2], tan: [F(1), 1] }, 60: { sen: [F(1, 2), 3], cos: [F(1, 2), 1], tan: [F(1), 3] } };
  const porTV = (L, [c, r]) => rad(fmul(L, c), r);
  const entreTV = (L, [c, r]) => rad(fdiv(L, fmul(c, r)), r); // L/(c√r) = L√r/(c·r)
  const LADO = { hip: 'la hipotenusa', op: 'el cateto opuesto', ad: 'el cateto adyacente' };
  fam('trig-lado', T_TRIG, ['paes'], 'Calcular un lado con 30°, 45° o 60°', (t) => {
    const th = t.elige([30, 45, 60]), L = t.elige([4, 6, 8, 10, 12, 14, 16, 18, 20]);
    const [con, bus] = t.elige([['hip', 'op'], ['hip', 'ad'], ['ad', 'op'], ['op', 'ad'], ['op', 'hip'], ['ad', 'hip']]);
    const REL = { 'hip|op': ['sen', '·'], 'hip|ad': ['cos', '·'], 'ad|op': ['tan', '·'], 'op|ad': ['tan', '/'], 'op|hip': ['sen', '/'], 'ad|hip': ['cos', '/'] };
    const [fn, opr] = REL[con + '|' + bus];
    const calc = (f, o) => (o === '·' ? porTV(L, TV[th][f]) : entreTV(L, TV[th][f]));
    const clave = { sen: 'sen θ = opuesto/hipotenusa', cos: 'cos θ = adyacente/hipotenusa', tan: 'tan θ = opuesto/adyacente' }[fn];
    const ok = calc(fn, opr);
    const malas = [];
    for (const f of ['sen', 'cos', 'tan']) for (const o of ['·', '/']) {
      if (f === fn && o === opr) continue;
      malas.push([calc(f, o) + ' cm', `Planteaste ${o === '·' ? `${L}·${f} ${th}°` : `${L}/${f} ${th}°`}. Conoces ${LADO[con]} y buscas ${LADO[bus]}: se usa ${clave}.`]);
    }
    const pos = { hip: 'AB', op: 'BC', ad: 'AC' };
    const et = { ang: 'A', simb: th + '°' };
    et[pos[con]] = `${L} cm`; et[pos[bus]] = 'x';
    return {
      enun: `En el triángulo ABC, rectángulo en C, el ángulo en A mide ${th}° y ${pos[con]} = ${L} cm. ¿Cuánto mide ${pos[bus]}?${figTri(th === 30 ? 1.73 : th === 45 ? 1 : 1, th === 60 ? 1.73 : 1, et)}`,
      ok: ok + ' cm', malas,
      exp: `Desde A: ${pos[con]} es ${LADO[con]} y ${pos[bus]} es ${LADO[bus]}. Con ${clave}: x = ${opr === '·' ? `${L}·${fn} ${th}°` : `${L}/${fn} ${th}°`} = ${ok} cm.`,
      p: { th, L, con, bus },
    };
  });

  fam('trig-altura', T_TRIG, ['paes', 'dificil'], 'Ángulo de elevación: alturas', (t, nivel) => {
    if (nivel === 'paes') {
      const th = t.elige([30, 45, 60]), d = t.elige([6, 8, 10, 12, 15, 18, 20, 24, 30, 40, 50]);
      const obj = t.elige(['un edificio', 'un árbol', 'una torre', 'un poste']);
      const ok = porTV(d, TV[th].tan);
      const malas = [['sen', '·'], ['cos', '·'], ['tan', '/']].map(([f, o]) => [(o === '·' ? porTV(d, TV[th][f]) : entreTV(d, TV[th][f])) + ' m', `Usaste ${o === '·' ? `${d}·${f} ${th}°` : `${d}/${f} ${th}°`}. La altura es el cateto opuesto al ángulo y la distancia al pie es el adyacente: tan ${th}° = altura/${d}.`]);
      return {
        enun: `Desde un punto del suelo, a ${d} m del pie de ${obj}, se ve su parte más alta con un ángulo de elevación de ${th}°. ¿Cuál es su altura?`,
        ok: ok + ' m', malas,
        exp: `tan ${th}° = altura/${d} → altura = ${d}·tan ${th}° = ${ok} m.`, p: { th, d },
      };
    }
    const [t1, t2] = t.elige([[30, 60], [45, 60]]);
    const s = t.elige([6, 10, 12, 18, 20, 24, 30]);
    // h = s/(cot t1 − cot t2) en la forma a + b√3
    const H = t1 === 30 ? [F(0), F(s, 2)] : [F(3 * s, 2), F(s, 2)];
    const X = t1 === 30 ? [F(s, 2), F(0)] : [F(s, 2), F(s, 2)]; // distancia del punto cercano al pie = h/tan t2
    const Hfar = t1 === 30 ? [F(0), F(s, 3)] : [F(s), F(0)];
    const ok = sumaRad(H[0], H[1], 3);
    return {
      enun: `Desde un punto A del suelo se ve la parte más alta de una torre con un ángulo de elevación de ${t1}°. Después de caminar ${s} m en línea recta hacia la torre, desde el punto B se ve con un ángulo de ${t2}°. ¿Cuál es la altura de la torre?`,
      ok: ok + ' m',
      malas: [
        [sumaRad(0, s, 3) + ' m', `Usaste ${s} m como si fuera la distancia de B al pie de la torre (h = ${s}·tan ${t2}°). Esa distancia no se conoce: es la incógnita x.`],
        [sumaRad(Hfar[0], Hfar[1], 3) + ' m', `Usaste ${s} m como distancia de A al pie de la torre (h = ${s}·tan ${t1}°). Desde A, la distancia es x + ${s}.`],
        [sumaRad(X[0], X[1], 3) + ' m', 'Esa es la distancia x desde B hasta el pie de la torre, no la altura.'],
      ],
      exp: `Sea x la distancia de B al pie. tan ${t2}° = h/x y tan ${t1}° = h/(x + ${s}). ${t1 === 30 ? `De la primera, x = h/√3; en la segunda, h√3 = x + ${s} = h/√3 + ${s} → h(√3 − 1/√3) = ${s} → h = ${s}√3/2` : `De la primera, x = h/√3; en la segunda, h = x + ${s} = h/√3 + ${s} → h(1 − 1/√3) = ${s} → h = ${s}√3/(√3 − 1) = ${s}(3 + √3)/2`} = ${ok} m.`,
      p: { t1, t2, s },
    };
  });

  fam('trig-dado-seno', T_TRIG, ['basico', 'paes'], 'De una razón a las otras', (t, nivel) => {
    let [a, b, c] = t.elige(nivel === 'basico' ? TRIPLES.slice(0, 5) : TRIPLES.slice(1, 5));
    if (t.r() < 0.5) [a, b] = [b, a];
    const dato = t.elige(nivel === 'basico' ? ['sen'] : ['sen', 'cos']);
    const pide = dato === 'sen' ? t.elige(['cos', 'tan']) : t.elige(['sen', 'tan']);
    const op = a, ad = b; // sen = a/c, cos = b/c
    const dTxt = dato === 'sen' ? `sen α = ${fq(F(op, c))}` : `cos α = ${fq(F(ad, c))}`;
    const conocido = dato === 'sen' ? op : ad, otro = dato === 'sen' ? ad : op;
    const val = { sen: F(op, c), cos: F(ad, c), tan: F(op, ad) };
    const malas = [];
    if (pide === 'tan') {
      malas.push([fq(F(ad, op)), 'Invertiste la razón: tangente = opuesto/adyacente.']);
      malas.push([fq(F(c, otro)), 'Dividiste la hipotenusa por un cateto; esa no es la tangente.']);
      malas.push([fq(dato === 'sen' ? F(op, c - op) : F(c - ad, ad)), `El otro cateto no es ${c} − ${conocido}: por Pitágoras, √(${c}² − ${conocido}²) = ${otro}.`]);
    } else {
      malas.push([fq(F(c - conocido, c)), `El otro cateto no es ${c} − ${conocido}: por Pitágoras, √(${c}² − ${conocido}²) = ${otro}.`]);
      malas.push([fq(val.tan), 'Esa es la tangente (opuesto/adyacente).']);
      malas.push([fq(F(c, otro)), 'Invertiste la razón: se divide por la hipotenusa.']);
      malas.push([fq(F(op === conocido ? ad : op, conocido)), `Dividiste por ${conocido}, que es un cateto; aquí se divide por la hipotenusa.`]);
    }
    return {
      enun: `En un triángulo rectángulo, α es un ángulo agudo y ${dTxt}. ¿Cuál es el valor de ${pide} α?`, ok: fq(val[pide]), malas,
      exp: `Arma un triángulo con ${dato === 'sen' ? `opuesto ${op}` : `adyacente ${ad}`} e hipotenusa ${c}. Por Pitágoras, el otro cateto es √(${c}² − ${conocido}²) = ${otro}. Entonces ${pide} α = ${fq(val[pide])}.`,
      p: { op, ad, c, pide },
    };
  });

  // =====================================================================
  // M2 · Gráficos de seno y coseno
  // =====================================================================
  const T_TRIF = 'm2.alg.trig-funciones';
  fam('trigf-parametros', T_TRIF, ['basico', 'paes', 'dificil'], 'Amplitud, período y recorrido de a·sen(bx) + d', (t, nivel) => {
    const A = F(t.elige([1, 2, 3, 4, -1, -2, -3])), B = t.elige([F(1, 2), F(1), F(2), F(3), F(4)]), D = t.ent(-3, 3);
    const fn = t.elige(['sen', 'cos']);
    const amp = Math.abs(A.p), per = fdiv(2, B);
    if (nivel === 'basico' && (fval(B) === amp || fval(B) === 1 || fval(B) === Math.abs(D) || fval(B) === amp / 2 || fval(B) === amp + Math.abs(D))) throw OTRA; // que cada alternativa tenga un solo origen
    const aT = A.p === 1 ? '' : A.p === -1 ? MENOS : num(A.p) + ' ';
    const bT = B.q === 2 ? 'x/2' : B.p === 1 ? 'x' : B.p + 'x';
    const f = `f(x) = ${aT}${fn}(${bT})${D ? (D > 0 ? ' + ' + D : ' ' + MENOS + ' ' + -D) : ''}`;
    const fin = `el ${num(D)} del final`;
    if (nivel === 'basico') {
      const malas = [[num(2 * amp), 'Esa es la distancia entre el máximo y el mínimo; la amplitud es la mitad.'], [fq(B), `Ese número (el que multiplica a x) cambia el período, no la amplitud.`]];
      if (A.p < 0) malas.push([num(A.p), `La amplitud es una distancia: se toma el valor absoluto de ${num(A.p)}.`]);
      if (D) malas.push([num(amp + Math.abs(D)), `Sumaste ${fin} a la amplitud: ese número solo sube o baja la curva.`]);
      if (amp / 2 !== Math.abs(D)) malas.push([fq(F(amp, 2)), 'Dividiste por 2: la amplitud ya es la distancia desde la línea media hasta el máximo.']);
      return { enun: `¿Cuál es la amplitud de la función ${f}?`, ok: num(amp), malas, exp: `La amplitud es el valor absoluto del número que multiplica a ${fn}: |${fq(A)}| = ${amp}.`, p: { A, B, D, fn, pide: 'amp' } };
    }
    if (nivel === 'paes') {
      const malas = [[pit(fmul(2, B)), `Multiplicaste por ${fq(B)}. El período es 2π dividido por el número que acompaña a x.`], [pit(fdiv(1, B)), `Usaste π. El período de ${fn} x es 2π.`]];
      if (!(B.p === 1 && B.q === 1)) malas.push(['2π', 'Ignoraste el número que multiplica a x: ese número cambia el período.']);
      if (amp !== 1) malas.push([pit(fmul(per, amp)), `El número que multiplica a ${fn} (${fq(A)}) cambia la amplitud, no el período.`]);
      const per1 = `2π/${B.q === 1 ? B.p : '(' + fq(B) + ')'}`;
      return { enun: `¿Cuál es el período de la función ${f}?`, ok: pit(per), malas, exp: `Período = 2π dividido por el número que acompaña a x: ${per1}${per1 !== pit(per) ? ' = ' + pit(per) : ''}.`, p: { A, B, D, fn, pide: 'per' } };
    }
    const malas = [];
    if (D) malas.push([intervalo(-amp, amp), `Olvidaste ${fin}: la curva se mueve ${D > 0 ? 'hacia arriba' : 'hacia abajo'} ${Math.abs(D)}.`]);
    if (amp !== 1 || D) malas.push([intervalo(-1, 1), `Ese es el recorrido de ${fn} x sin cambios; la amplitud y ${fin} lo modifican.`]);
    if (fval(B) !== amp) malas.push([intervalo(fsub(D, B), fadd(D, B)), `Usaste ${fq(B)} (el número que multiplica a x) como amplitud; la amplitud es ${amp}.`]);
    malas.push([intervalo(D - 2 * amp, D + 2 * amp), `Duplicaste la amplitud: el máximo está ${amp} sobre la línea media, no ${2 * amp}.`]);
    malas.push([intervalo(D, D + amp), 'La curva baja tanto como sube: el recorrido va de la línea media menos la amplitud a la línea media más la amplitud.']);
    return { enun: `¿Cuál es el recorrido de la función ${f}?`, ok: intervalo(D - amp, D + amp), malas, exp: `${fn} oscila entre −1 y 1.${amp !== 1 ? ` Multiplicado por ${fq(A)}, oscila entre −${amp} y ${amp}.` : ''}${D ? ` Con ${fin}, todo se mueve ${D > 0 ? 'arriba' : 'abajo'} ${Math.abs(D)}.` : ''} Recorrido: ${intervalo(D - amp, D + amp)}.`, p: { A, B, D, fn, pide: 'rec' } };
  });
  const SV = { 0: [F(0), 1], 30: [F(1, 2), 1], 45: [F(1, 2), 2], 60: [F(1, 2), 3], 90: [F(1), 1] };
  function exacto(fn, g) { // valor exacto de sen/cos en grados
    const m = ((g % 360) + 360) % 360;
    const r0 = m % 180, ref = r0 > 90 ? 180 - r0 : r0;
    const sgnS = m > 0 && m < 180 ? 1 : m > 180 ? -1 : 0;
    const sgnC = m < 90 || m > 270 ? 1 : m > 90 && m < 270 ? -1 : 0;
    const [c, r] = fn === 'sen' ? SV[ref] : SV[90 - ref];
    const sg = fn === 'sen' ? sgnS : sgnC;
    return [fmul(c, sg || 1), r, sg];
  }
  const exTxt = ([c, r, sg]) => (sg === 0 ? '0' : rad(c, r));
  fam('trigf-valor', T_TRIF, ['basico', 'paes'], 'Seno y coseno en la circunferencia unitaria', (t, nivel) => {
    const g = t.elige(nivel === 'basico' ? [30, 45, 60, 120, 135, 150, 210, 225, 240, 300, 315, 330] : [120, 135, 150, 210, 225, 240, 300, 315, 330]);
    const fn = t.elige(['sen', 'cos']), otra = fn === 'sen' ? 'cos' : 'sen';
    const v = exacto(fn, g), w = exacto(otra, g);
    const cuad = g < 90 ? 'primer' : g < 180 ? 'segundo' : g < 270 ? 'tercer' : 'cuarto';
    const pos = fval(v[0]) > 0;
    const malas = [
      [exTxt(w), `Ese es el ${otra === 'sen' ? 'seno' : 'coseno'} de ese ángulo. En la circunferencia unitaria, el coseno es la coordenada x y el seno es la coordenada y.`],
      [rad(fneg(v[0]), v[1]), `Error de signo: en el ${cuad} cuadrante el ${fn === 'sen' ? 'seno' : 'coseno'} es ${pos ? 'positivo' : 'negativo'}.`],
      [rad(fneg(w[0]), w[1]), `Ese es el ${otra === 'sen' ? 'seno' : 'coseno'} con el signo cambiado. Coseno = coordenada x, seno = coordenada y.`],
    ];
    if (v[1] === 2) { malas.push([rad(fmul(F(1, 2), pos ? 1 : -1), 3), 'Confundiste los valores: con ángulo de referencia 45°, seno y coseno valen √2/2 en valor absoluto.']); malas.push([fq(fmul(F(1, 2), pos ? 1 : -1)), 'Ese es un valor de 30° o 60°. El ángulo de referencia aquí es 45°: √2/2.']); }
    const gT = nivel === 'basico' ? `${g}°` : pit(F(g, 180));
    return {
      enun: `¿Cuál es el valor de ${fn}(${gT})?${nivel === 'paes' ? ' (el ángulo está en radianes)' : ''}`, ok: exTxt(v), malas,
      exp: `${nivel === 'paes' ? `${gT} = ${g}°. ` : ''}Está en el ${cuad} cuadrante, con ángulo de referencia ${((g % 180) > 90 ? 180 - (g % 180) : g % 180)}°. Allí el ${fn === 'sen' ? 'seno' : 'coseno'} es ${pos ? 'positivo' : 'negativo'}: ${fn}(${gT}) = ${exTxt(v)}.`,
      p: { g, fn },
    };
  });

  // =====================================================================
  // M2 · Medidas de dispersión
  // =====================================================================
  const T_DIS = 'm2.pro.dispersion';
  fam('disp-rango', T_DIS, ['basico'], 'Rango', (t) => {
    const n = t.ent(5, 7);
    const xs = []; while (xs.length < n) { const v = t.ent(2, 40); if (!xs.includes(v)) xs.push(v); }
    const mx = Math.max(...xs), mn = Math.min(...xs);
    const malas = [
      [num(Math.abs(xs[n - 1] - xs[0])), 'Restaste el último y el primero tal como aparecen (sin fijarte en el signo). Primero busca el mayor y el menor.'],
      [num(mx), 'Ese es el dato mayor. El rango es mayor − menor.'],
      [num(mx + mn), 'Sumaste el mayor y el menor; el rango es su diferencia.'],
    ];
    const s = xs.reduce((a, b) => a + b, 0);
    if (s % n === 0) malas.push([num(s / n), 'Ese es el promedio: dice dónde está el centro, no cuánto se dispersan los datos.']);
    return { enun: `¿Cuál es el rango del conjunto de datos ${xs.join(', ')}?`, ok: num(mx - mn), malas, exp: `Mayor: ${mx}. Menor: ${mn}. Rango = ${mx} − ${mn} = ${mx - mn}.`, p: { xs } };
  });

  const DESV = [[-3, -1, 1, 3], [-4, 0, 0, 4], [-5, -1, 1, 5], [-2, 0, 0, 2], [-2, -1, 0, 1, 2], [-4, -2, 0, 2, 4], [-6, -3, 0, 3, 6], [-5, -5, 0, 5, 5], [-5, -1, -1, 1, 1, 5], [-3, -3, 0, 0, 3, 3]];
  fam('disp-desviacion', T_DIS, ['paes'], 'Desviación estándar', (t) => {
    const d = t.elige(DESV), mu = t.ent(7, 20), n = d.length;
    const xs = t.baraja(d.map((x) => mu + x));
    const ss = d.reduce((a, x) => a + x * x, 0);
    if (ss % n) throw OTRA;
    const v = ss / n, mad = F(d.reduce((a, x) => a + Math.abs(x), 0), n);
    // √(ss/(n−1)) = √(ss·(n−1))/(n−1)
    return {
      enun: `¿Cuál es la desviación estándar del conjunto de datos ${xs.join(', ')}?`, ok: rad(1, v),
      malas: [
        [num(v), 'Esa es la varianza. La desviación estándar es su raíz cuadrada.'],
        [rad(F(1, n - 1), ss * (n - 1)), `Dividiste por n − 1 = ${n - 1}. En la PAES la varianza se calcula dividiendo por n = ${n}.`],
        [fq(mad), 'Ese es el promedio de las distancias a la media, sin elevarlas al cuadrado.'],
        [rad(1, ss), `Te faltó dividir por n = ${n} antes de sacar la raíz.`],
      ],
      exp: `Media = ${mu}. Distancias a la media: ${d.map(num).join(', ')}. Sus cuadrados suman ${ss}. Varianza = ${ss}/${n} = ${v}. Desviación estándar = √${v}${rad(1, v) !== '√' + v ? ' = ' + rad(1, v) : ''}.`,
      p: { xs },
    };
  });

  fam('disp-cambio', T_DIS, ['paes', 'dificil'], 'Qué pasa con la media y la dispersión al transformar los datos', (t, nivel) => {
    const mu = t.ent(4, 30), sg = t.ent(2, 6), a = t.elige([2, 3, -2, -3, 4]), b = t.nz(-10, 10);
    const tr = `${lin([[a, 'x'], [b, '']])}`;
    const intro = `Un conjunto de datos tiene media ${mu} y desviación estándar ${sg}. Cada dato x se reemplaza por ${tr}.`;
    const sb = b > 0 ? `Sumar ${b}` : `Restar ${-b}`;
    if (nivel === 'paes') {
      const pide = t.elige(['desv', 'media']);
      if (pide === 'desv') {
        const malas = [[num(Math.abs(a) * sg + b), `Aplicaste el ${b > 0 ? '+' : MENOS}${Math.abs(b)} a la desviación. ${sb} mueve todos los datos, pero no cambia su dispersión.`], [num(a * a * sg), `Multiplicaste por ${par(a)}² = ${a * a}: ese factor es para la varianza, no para la desviación estándar.`], [num(sg), `Multiplicar los datos sí cambia la dispersión: la desviación se multiplica por ${Math.abs(a)}.`]];
        if (a < 0) malas.push([num(a * sg), `Una desviación estándar nunca es negativa: se multiplica por ${Math.abs(a)}, no por ${num(a)}.`]);
        return { enun: `${intro} ¿Cuál es la nueva desviación estándar?`, ok: num(Math.abs(a) * sg), malas, exp: `${sb} no cambia la dispersión. Multiplicar por ${num(a)} la multiplica por |${num(a)}| = ${Math.abs(a)}: ${Math.abs(a)}·${sg} = ${Math.abs(a) * sg}.`, p: { mu, sg, a, b, pide } };
      }
      return {
        enun: `${intro} ¿Cuál es la nueva media?`, ok: num(a * mu + b),
        malas: [[num(a * mu), `Olvidaste ${b > 0 ? 'sumar' : 'restar'} ${Math.abs(b)}: la media también se desplaza.`], [num(mu + b), `Olvidaste multiplicar por ${num(a)}.`], [num(a * (mu + b)), `${b > 0 ? 'Sumaste' : 'Restaste'} antes de multiplicar: es ${num(a)}·${mu} ${b > 0 ? '+' : MENOS} ${Math.abs(b)}, no ${num(a)}·(${mu} ${b > 0 ? '+' : MENOS} ${Math.abs(b)}).`]],
        exp: `La media sigue la misma transformación: ${num(a)}·${mu} ${b > 0 ? '+' : MENOS} ${Math.abs(b)} = ${num(a * mu + b)}.`, p: { mu, sg, a, b, pide },
      };
    }
    return {
      enun: `${intro} ¿Cuál es la nueva varianza?`, ok: num(a * a * sg * sg),
      malas: [
        [num(Math.abs(a) * sg * sg), `La varianza se multiplica por ${par(a)}² = ${a * a}, no por ${Math.abs(a)}.`],
        [num(a * a * sg), `Te faltó elevar al cuadrado la desviación: la varianza original es ${sg}² = ${sg * sg}.`],
        [num(a * a * sg * sg + b), `Aplicaste el ${b > 0 ? '+' : MENOS}${Math.abs(b)} a la varianza. ${sb} no cambia la dispersión.`],
        [num(Math.abs(a) * sg + b), `Calculaste ${Math.abs(a)}·${sg} ${b > 0 ? '+' : MENOS} ${Math.abs(b)}: ${sb.toLowerCase()} no cambia la dispersión y falta elevar al cuadrado. La varianza es ${par(a)}²·${sg}².`],
      ],
      exp: `Varianza original = ${sg}² = ${sg * sg}. ${sb} no la cambia; multiplicar por ${num(a)} la multiplica por ${par(a)}² = ${a * a}: ${a * a}·${sg * sg} = ${a * a * sg * sg}.`,
      p: { mu, sg, a, b, pide: 'var' },
    };
  });
  // =====================================================================
  // M2 · Binomial y normal
  // =====================================================================
  const T_BIN = 'm2.pro.binomial-normal';
  const CTX_BIN = [
    { p: F(1, 2), txt: (n) => `Se lanza una moneda equilibrada ${n} veces.`, ex: (k) => `obtener exactamente ${k} ${k === 1 ? 'cara' : 'caras'}`, al: 'obtener al menos una cara', uno: 'una cara', ning: 'ninguna cara', todos: 'todas salen cara' },
    { p: F(1, 3), txt: (n) => `Se lanza un dado común ${n} veces.`, ex: (k) => `obtener exactamente ${k} ${k === 1 ? 'vez' : 'veces'} un número mayor que 4`, al: 'obtener al menos una vez un número mayor que 4', uno: 'una vez', ning: 'ninguna vez', todos: 'todas las veces sale mayor que 4' },
    { p: F(1, 4), txt: (n) => `Un estudiante responde al azar ${n} preguntas de 4 alternativas cada una.`, ex: (k) => `acertar exactamente ${k} ${k === 1 ? 'pregunta' : 'preguntas'}`, al: 'acertar al menos una pregunta', uno: 'una', ning: 'ninguna', todos: 'todas son correctas' },
    { p: F(3, 4), txt: (n) => `Una jugadora convierte el 75 % de sus penales. Patea ${n} penales.`, ex: (k) => `convertir exactamente ${k} ${k === 1 ? 'penal' : 'penales'}`, al: 'convertir al menos un penal', uno: 'uno', ning: 'ninguno', todos: 'convierte todos' },
    { p: F(2, 3), txt: (n) => `Cada semilla germina con probabilidad 2/3. Se siembran ${n} semillas.`, ex: (k) => `que germinen exactamente ${k} ${k === 1 ? 'semilla' : 'semillas'}`.replace('germinen exactamente 1 semilla', 'germine exactamente 1 semilla'), al: 'que germine al menos una semilla', uno: 'una', ning: 'ninguna', todos: 'todas germinan' },
  ];
  fam('bin-probabilidad', T_BIN, ['paes', 'dificil'], 'Probabilidad binomial', (t, nivel) => {
    const C = t.elige(CTX_BIN), n = t.ent(3, nivel === 'paes' ? 4 : 5);
    const p = C.p, q = fsub(1, p);
    if (nivel === 'paes') {
      const k = t.ent(1, n - 1);
      const ok = fmul(comb(n, k), fmul(fpow(p, k), fpow(q, n - k)));
      const malas = [
        [fq(fmul(fpow(p, k), fpow(q, n - k))), `Calculaste una sola secuencia. ${k === 1 ? 'El éxito puede ir' : `Los ${k} éxitos pueden ir`} en C(${n}, ${k}) = ${comb(n, k)} posiciones distintas.`],
        [fq(fmul(comb(n, k), fmul(fpow(p, n - k), fpow(q, k)))), 'Cambiaste éxito por fracaso en los exponentes.'],
        [fq(F(k, n)), 'Dividiste éxitos por intentos; eso no es la probabilidad binomial.'],
      ];
      const sinFr = fmul(comb(n, k), fpow(p, k));
      if (fval(sinFr) < 1) malas.push([fq(sinFr), `Olvidaste los fracasos: falta multiplicar por (${fq(q)})${sup(n - k)}.`]);
      return {
        enun: `${C.txt(n)} ¿Cuál es la probabilidad de ${C.ex(k)}?`, ok: fq(ok), malas,
        exp: `Binomial con n = ${n} y p = ${fq(p)}: P(X = ${k}) = C(${n}, ${k})·(${fq(p)})${sup(k)}·(${fq(q)})${sup(n - k)} = ${comb(n, k)}·${fq(fpow(p, k))}·${fq(fpow(q, n - k))} = ${fq(ok)}.`,
        p: { n, k, p, pide: 'exacto' },
      };
    }
    const ok = fsub(1, fpow(q, n));
    const malas = [
      [fq(fpow(q, n)), `Esa es la probabilidad de ${C.ning}. «Al menos ${C.uno}» es lo contrario: 1 − (${fq(q)})${sup(n)}.`],
      [fq(fmul(n, fmul(p, fpow(q, n - 1)))), `Esa es la probabilidad de exactamente ${C.uno}; «al menos ${C.uno}» también incluye ${['dos', 'tres', 'cuatro', 'cinco'].slice(0, n - 1).join(', ').replace(/, ([^,]*)$/, ' o $1')}.`],
      [fq(fsub(1, fpow(p, n))), `Restaste a 1 el caso en que ${C.todos}. Lo contrario de «al menos ${C.uno}» es «${C.ning}»: (${fq(q)})${sup(n)}.`],
    ];
    if (fval(fmul(n, p)) < 1) malas.push([fq(fmul(n, p)), `Sumaste ${fq(p)} por cada intento; las probabilidades de intentos distintos no se suman así.`]);
    return {
      enun: `${C.txt(n)} ¿Cuál es la probabilidad de ${C.al}?`, ok: fq(ok), malas,
      exp: `Lo contrario de «al menos ${C.uno}» es «${C.ning}»: P(X = 0) = (${fq(q)})${sup(n)} = ${fq(fpow(q, n))}. Entonces P(X ≥ 1) = 1 − ${fq(fpow(q, n))} = ${fq(ok)}.`,
      p: { n, p, pide: 'almenos' },
    };
  });
  fam('bin-esperanza', T_BIN, ['basico', 'paes'], 'Valor esperado y varianza de la binomial', (t, nivel) => {
    const n = t.elige([10, 20, 30, 40, 50, 60, 80, 100, 200]), pc = t.elige([10, 20, 25, 30, 40, 50, 60, 75, 80]);
    const p = pc / 100, E = (n * pc) / 100, V = (n * pc * (100 - pc)) / 10000;
    const pT = num(p);
    if (nivel === 'basico') {
      return {
        enun: `Si X sigue una distribución binomial con n = ${n} y p = ${pT}, ¿cuál es su valor esperado?`, ok: num(E),
        malas: [[pT, `Ese es p. El valor esperado es n·p.`], [num(n - E), 'Usaste la probabilidad de fracaso: n·(1 − p).'], [num(V), 'Esa es la varianza: n·p·(1 − p).']],
        exp: `E(X) = n·p = ${n}·${pT} = ${num(E)}.`, p: { n, p, pide: 'E' },
      };
    }
    return {
      enun: `Si X sigue una distribución binomial con n = ${n} y p = ${pT}, ¿cuál es su varianza?`, ok: num(V),
      malas: [[num(E), 'Ese es el valor esperado n·p. A la varianza le falta multiplicar por (1 − p).'], [num(n * p * p), 'Elevaste p al cuadrado; la varianza es n·p·(1 − p).'], [num(Math.sqrt(V), 4), 'Esa es la desviación estándar (la raíz de la varianza).']],
      exp: `Var(X) = n·p·(1 − p) = ${n}·${pT}·${num(1 - p)} = ${num(V)}.`, p: { n, p, pide: 'V' },
    };
  });

  const PHI = [[0.5, 0.691], [1, 0.841], [1.5, 0.933], [2, 0.977], [2.5, 0.994]];
  const CTX_NORMAL = [
    ['El puntaje de una prueba', 500, 100], ['El puntaje de una prueba', 600, 50], ['El puntaje de un ensayo', 60, 8], ['El puntaje de un ensayo', 70, 4],
    ['La estatura (en cm) de un grupo de adultos', 170, 10], ['La estatura (en cm) de un grupo de adultos', 165, 6],
    ['El peso (en g) de unos paquetes de arroz', 1000, 20], ['El peso (en g) de unos paquetes de café', 250, 10],
  ];
  fam('normal', T_BIN, ['basico', 'paes', 'dificil'], 'Distribución normal: estandarizar y usar la tabla', (t, nivel) => {
    const [ctx, mu, sg] = t.elige(CTX_NORMAL);
    const [z, ph] = t.elige(PHI);
    const intro = `${ctx} sigue una distribución normal con media ${num(mu)} y desviación estándar ${sg}.`;
    const x = mu + z * sg;
    if (nivel === 'basico') {
      return {
        enun: `${intro} ¿Cuál es el valor z (estandarizado) de x = ${num(x)}?`, ok: num(z),
        malas: [[num(x - mu), `Te faltó dividir por la desviación estándar ${sg}.`], [num(-z), 'Restaste al revés: z = (x − μ)/σ.'], [num(x / sg, 3), 'Olvidaste restar la media antes de dividir.']],
        exp: `z = (x − μ)/σ = (${num(x)} − ${num(mu)})/${sg} = ${num(z)}.`, p: { mu, sg, x, pide: 'z' },
      };
    }
    const tabla = `Usa que P(Z ≤ ${num(z)}) = ${num(ph)}.`;
    if (nivel === 'paes') {
      const lado = t.elige(['sobre', 'bajo']);
      const xv = lado === 'sobre' ? x : mu - z * sg;
      return {
        enun: `${intro} ${tabla} ¿Cuál es la probabilidad de que un valor elegido al azar sea ${lado === 'sobre' ? 'mayor' : 'menor'} que ${num(xv)}?`, ok: num(1 - ph, 3),
        malas: [
          [num(ph), lado === 'sobre' ? `Esa es la probabilidad de estar bajo ${num(xv)}; se pide sobre: 1 − ${num(ph)}.` : `Esa es la probabilidad de estar bajo μ + ${num(z)}σ. Por simetría, bajo μ − ${num(z)}σ queda 1 − ${num(ph)}.`],
          [num(ph - 0.5, 3), `Esa es la probabilidad de estar entre la media y ${num(lado === 'sobre' ? x : mu - z * sg)}.`],
          [num(2 * ph - 1, 3), `Esa es la probabilidad de estar entre μ − ${num(z)}σ y μ + ${num(z)}σ.`],
        ],
        exp: `z = ${lado === 'sobre' ? '' : MENOS}${num(z)}. ${lado === 'sobre' ? `P(Z &gt; ${num(z)}) = 1 − ${num(ph)}` : `Por simetría, P(Z &lt; −${num(z)}) = P(Z &gt; ${num(z)}) = 1 − ${num(ph)}`} = ${num(1 - ph, 3)}.`,
        p: { ph, pide: 'cola' },
      };
    }
    if (t.r() < 0.5) {
      return {
        enun: `${intro} ${tabla} ¿Cuál es la probabilidad de que un valor elegido al azar esté entre ${num(mu - z * sg)} y ${num(x)}?`, ok: num(2 * ph - 1, 3),
        malas: [[num(ph), `Esa es la probabilidad de estar bajo ${num(x)}: incluye toda la cola izquierda.`], [num(ph - 0.5, 3), 'Esa es solo la mitad del intervalo (de la media hacia un lado).'], [num(1 - ph, 3), `Esa es una cola: la probabilidad de estar sobre ${num(x)}.`], [num(2 * (1 - ph), 3), 'Esas son las dos colas: lo que queda fuera del intervalo.']],
        exp: `Es el intervalo μ ± ${num(z)}σ. P(−${num(z)} ≤ Z ≤ ${num(z)}) = ${num(ph)} − (1 − ${num(ph)}) = 2·${num(ph)} − 1 = ${num(2 * ph - 1, 3)}.`,
        p: { ph, pide: 'centro' },
      };
    }
    const des = z === 1 ? 'una desviación estándar' : `${num(z)} desviaciones estándar`;
    return {
      enun: `${intro} ${tabla} ¿Bajo qué valor queda el ${num(ph * 100, 1)} % de los datos?`, ok: num(x),
      malas: [[num(mu + z), `Sumaste ${num(z)} a la media; hay que sumar ${des}: ${num(z)}·${sg}.`], [num(mu - z * sg), `Restaste: bajo μ − ${num(z)}σ queda solo el ${num((1 - ph) * 100, 1)} %.`], [num(z * sg), `Eso es lo que se aleja de la media (${num(z)}·${sg}); falta sumarle la media.`]],
      exp: `El ${num(ph * 100, 1)} % queda bajo z = ${num(z)}. x = μ + z·σ = ${num(mu)} + ${num(z)}·${sg} = ${num(x)}.`,
      p: { mu, sg, z, pide: 'percentil' },
    };
  });
  // =====================================================================
  // M2 · Circunferencia
  // =====================================================================
  const T_CIR = 'm2.geo.circunferencia';
  fam('circ-inscrito', T_CIR, ['basico', 'paes'], 'Ángulo del centro, inscrito y cuadrilátero inscrito', (t, nivel) => {
    const v = nivel === 'basico' ? t.elige(['central', 'inscrito']) : t.elige(['central', 'inscrito', 'cuadri', 'arco']);
    if (v === 'central') {
      const c = 2 * t.ent(20, 80);
      return {
        enun: `En la circunferencia de centro O, el ángulo del centro AOB mide ${c}° y C está en el arco mayor AB. ¿Cuánto mide el ángulo ACB?${figCirc(c)}`, ok: `${c / 2}°`,
        malas: [[`${c}°`, 'El ángulo inscrito no es igual al del centro: mide la mitad.'], ...(2 * c < 180 ? [[`${2 * c}°`, 'Al revés: el del centro es el doble del inscrito, no el inscrito el doble del central.']] : []), [`${180 - c / 2}°`, `Ese valor sería si C estuviera en el arco menor. Aquí C está en el arco mayor.`], [`${180 - c}°`, 'Restaste de 180°. El inscrito es la mitad del ángulo del centro que abarca el mismo arco.']],
        exp: `El ángulo inscrito ACB y el ángulo del centro AOB abarcan el mismo arco AB: el inscrito mide la mitad, ${c}°/2 = ${c / 2}°.`, p: { v, c },
      };
    }
    if (v === 'inscrito') {
      const i = t.ent(15, 80);
      return {
        enun: `En la circunferencia de centro O, el ángulo inscrito ACB mide ${i}°. ¿Cuánto mide el ángulo del centro AOB que abarca el mismo arco?${figCirc(2 * i)}`, ok: `${2 * i}°`,
        malas: [[`${i}°`, 'El ángulo del centro no es igual al inscrito: es el doble.'], [`${i / 2}°`.replace('.', ','), 'Dividiste por 2: es el inscrito el que mide la mitad, no el del centro.'], [`${180 - i}°`, 'Restaste de 180°. El ángulo del centro es el doble del inscrito que abarca el mismo arco.']],
        exp: `El ángulo del centro mide el doble del inscrito que abarca el mismo arco: 2·${i}° = ${2 * i}°.`, p: { v, i },
      };
    }
    if (v === 'cuadri') {
      const a = t.ent(55, 125);
      if (a === 90) throw OTRA;
      return {
        enun: `El cuadrilátero ABCD está inscrito en una circunferencia. Si el ángulo en A mide ${a}°, ¿cuánto mide el ángulo en C (el opuesto a A)?`, ok: `${180 - a}°`,
        malas: [[`${a}°`, 'Los ángulos opuestos de un cuadrilátero inscrito no son iguales: suman 180°.'], [`${360 - a}°`, 'Suman 180°, no 360°. (360° es la suma de los cuatro ángulos.)'], ['90°', 'No tiene por qué ser recto: eso pasa solo si el ángulo abarca un diámetro.']],
        exp: `En un cuadrilátero inscrito, los ángulos opuestos suman 180°: 180° − ${a}° = ${180 - a}°.`, p: { v, a },
      };
    }
    const i = t.ent(20, 85);
    return {
      enun: `Un ángulo inscrito en una circunferencia mide ${i}°. ¿Cuánto mide el arco que abarca?`, ok: `${2 * i}°`,
      malas: [[`${i}°`, 'El arco no mide lo mismo que el inscrito: mide el doble (lo mismo que el ángulo del centro).'], [`${i / 2}°`.replace('.', ','), 'Dividiste por 2: el arco mide el doble del inscrito.'], [`${360 - 2 * i}°`, 'Ese es el otro arco, el que el ángulo no abarca.']],
      exp: `Un ángulo inscrito mide la mitad del arco que abarca: arco = 2·${i}° = ${2 * i}°.`, p: { v, i },
    };
  });

  fam('circ-angulos-arcos', T_CIR, ['paes', 'dificil'], 'Ángulos con vértice dentro o fuera de la circunferencia', (t, nivel) => {
    if (nivel === 'paes') {
      const a = t.ent(30, 160), b = t.ent(20, 140);
      if ((a + b) % 2 || a + b >= 340 || a === b) throw OTRA;
      return {
        enun: `Dos cuerdas AB y CD se cortan en un punto P dentro de la circunferencia. El ángulo APC abarca un arco AC de ${a}° y su opuesto por el vértice abarca un arco BD de ${b}°. ¿Cuánto mide el ángulo APC?`, ok: `${(a + b) / 2}°`,
        malas: [[`${a + b}°`, 'Te faltó dividir por 2: el ángulo interior es la semisuma de los arcos.'], [`${Math.abs(a - b) / 2}°`.replace('.', ','), 'Esa es la fórmula del ángulo con vértice fuera (semidiferencia). Con el vértice dentro, los arcos se suman.'], [`${a / 2}°`.replace('.', ','), 'Usaste solo uno de los arcos, como si fuera un ángulo inscrito.'], [`${180 - (a + b) / 2}°`, 'Ese es el ángulo adyacente (APD), no el pedido.']],
        exp: `Ángulo con vértice dentro = semisuma de los arcos que abarcan él y su opuesto: (${a}° + ${b}°)/2 = ${(a + b) / 2}°.`, p: { a, b, pide: 'interior' },
      };
    }
    const a = t.ent(80, 220), b = t.ent(20, 100);
    if ((a - b) % 2 || a <= b + 10 || a + b >= 350) throw OTRA;
    return {
      enun: `Desde un punto P fuera de una circunferencia se trazan dos secantes. El ángulo en P abarca un arco lejano de ${a}° y un arco cercano de ${b}°. ¿Cuánto mide el ángulo en P?`, ok: `${(a - b) / 2}°`,
      malas: [[`${(a + b) / 2}°`.replace('.', ','), 'Sumaste los arcos. Con el vértice fuera de la circunferencia, los arcos se restan.'], [`${a - b}°`, 'Te faltó dividir por 2: el ángulo exterior es la semidiferencia de los arcos.'], [`${a / 2}°`.replace('.', ','), 'Ese sería un ángulo inscrito que abarca el arco lejano. P está fuera, así que hay que restar el arco cercano.']],
      exp: `Ángulo con vértice fuera = semidiferencia de los arcos: (${a}° − ${b}°)/2 = ${(a - b) / 2}°.`, p: { a, b, pide: 'exterior' },
    };
  });

  fam('circ-segmentos', T_CIR, ['basico', 'paes', 'dificil'], 'Cuerdas, secantes y tangentes (producto de segmentos)', (t, nivel) => {
    if (nivel === 'basico') {
      const a = t.ent(2, 12), b = t.ent(2, 12), c = t.ent(2, 12);
      if ((a * b) % c || a * b / c === a || c === a) throw OTRA;
      const d = (a * b) / c;
      const malas = [[fq(F(b * c, a)), 'Planteaste una proporción (AP/PB = CP/PD). La relación es un producto: AP·PB = CP·PD.'], [fq(F(a * c, b)), 'Cruzaste los segmentos: se multiplican los dos trozos de una misma cuerda.']];
      if (a + b - c > 0) malas.push([num(a + b - c), 'Sumaste los trozos. Lo que se conserva es el producto: AP·PB = CP·PD.']);
      return {
        enun: `En una circunferencia, las cuerdas AB y CD se cortan en P. Si AP = ${a}, PB = ${b} y CP = ${c}, ¿cuánto mide PD?`, ok: fq(F(d)), malas,
        exp: `AP·PB = CP·PD → ${a}·${b} = ${c}·PD → PD = ${a * b}/${c} = ${fq(F(d))}.`, p: { a, b, c, pide: 'cuerdas' },
      };
    }
    if (nivel === 'paes') {
      const [a, b] = t.elige([[1, 4], [1, 9], [2, 8], [3, 12], [4, 9], [1, 16], [2, 18], [4, 16], [3, 27], [5, 20], [4, 25], [9, 16]]);
      const pt_ = Math.sqrt(a * b);
      return {
        enun: `Desde un punto P exterior se trazan una tangente PT y una secante que corta a la circunferencia en A y B (A entre P y B). Si PA = ${a} y PB = ${b}, ¿cuánto mide PT?`, ok: num(pt_),
        malas: [[fq(F(a + b, 2)), 'Promediaste. La tangente cumple PT² = PA·PB (media geométrica, no aritmética).'], [num(a * b), 'Olvidaste la raíz: PT² = PA·PB, así que PT = √(PA·PB).'], [rad(1, a * (b - a)), 'Usaste la cuerda AB en vez de la secante completa PB: PT² = PA·PB.']],
        exp: `PT² = PA·PB = ${a}·${b} = ${a * b} → PT = ${num(pt_)}.`, p: { a, b, pide: 'tangente' },
      };
    }
    const a = t.ent(2, 8), e1 = t.ent(2, 12), c = t.ent(2, 9);
    if (c === a) throw OTRA;
    const prod = a * (a + e1);
    if (prod % c) throw OTRA;
    const e2 = prod / c - c;
    if (e2 <= 0) throw OTRA;
    const malas = [[fq(F(a * e1, c)), 'Multiplicaste el trozo exterior por la cuerda interior. Se multiplica por la secante completa: PA·PB = PC·PD.'], [num(prod / c), 'Ese es PD, la secante completa. Se pide la cuerda CD = PD − PC.']];
    const pd2 = F(c * (a + e1), a);
    if (fval(pd2) > c) malas.push([fq(fsub(pd2, c)), 'Planteaste la igualdad al revés. Es PA·PB = PC·PD: cada trozo exterior por su secante completa.']);
    return {
      enun: `Desde un punto P exterior se trazan dos secantes. Una corta a la circunferencia en A y B (A entre P y B), con PA = ${a} y AB = ${e1}. La otra la corta en C y D, con PC = ${c} (C entre P y D). ¿Cuánto mide CD?`, ok: num(e2), malas,
      exp: `PA·PB = PC·PD, con PB = ${a} + ${e1} = ${a + e1}: ${a}·${a + e1} = ${c}·PD → PD = ${prod / c}. CD = PD − PC = ${prod / c} − ${c} = ${e2}.`,
      p: { a, e1, c, pide: 'secantes' },
    };
  });

  // =====================================================================
  // M2 · Homotecia
  // =====================================================================
  const T_HOM = 'm2.geo.homotecia';
  const RAZONES = [F(2), F(3), F(-1), F(-2), F(1, 2), F(-1, 2), F(3, 2), F(-3)];
  fam('hom-punto', T_HOM, ['basico', 'paes'], 'Imagen de un punto por homotecia', (t, nivel) => {
    const k = t.elige(RAZONES);
    const O = nivel === 'basico' ? [0, 0] : [t.ent(-4, 4), t.ent(-4, 4)];
    const den = k.q;
    const P = [O[0] + den * t.nz(-3, 3), O[1] + den * t.ent(-3, 3)];
    const img = (kk, base = O) => [fadd(base[0], fmul(kk, P[0] - O[0])), fadd(base[1], fmul(kk, P[1] - O[1]))];
    const Pi = img(k);
    const malas = [
      [pt(...img(finv(k))), `Dividiste por ${fq(k)} en vez de multiplicar.`],
      [pt(...img(fneg(k))), `Error de signo: con razón ${fval(k) > 0 ? 'positiva la imagen queda del mismo lado que P' : 'negativa la imagen queda al otro lado del centro'}.`],
      [pt(fadd(P[0], fmul(k, P[0] - O[0])), fadd(P[1], fmul(k, P[1] - O[1]))), 'Sumaste k·(P − O) a P; se suma al centro O: P\' = O + k·(P − O).'],
    ];
    if (nivel === 'basico') { malas.push([pt(fmul(k, P[0]), P[1]), 'Multiplicaste solo la coordenada x; se multiplican las dos.']); malas.push([pt(fadd(P[0], k), fadd(P[1], k)), 'Sumaste k a las coordenadas. La homotecia multiplica.']); }
    else malas.push([pt(fmul(k, P[0]), fmul(k, P[1])), 'Multiplicaste las coordenadas de P por k como si el centro fuera el origen. Se multiplica el vector OP: P\' = O + k·(P − O).']);
    return {
      enun: `¿Cuáles son las coordenadas de la imagen del punto P${pt(P[0], P[1])} por una homotecia de centro ${nivel === 'basico' ? 'en el origen' : 'O' + pt(O[0], O[1])} y razón ${fq(k)}?`, ok: pt(...Pi), malas,
      exp: `P' = O + k·(P − O)${nivel === 'basico' ? ' = k·P' : ''}. P − O = ${pt(P[0] - O[0], P[1] - O[1])}; por ${fq(k)}: ${pt(fmul(k, P[0] - O[0]), fmul(k, P[1] - O[1]))}; ${nivel === 'basico' ? '' : 'más O: '}P' = ${pt(...Pi)}.`,
      p: { O, P, k },
    };
  });

  fam('hom-medidas', T_HOM, ['basico', 'paes', 'dificil'], 'Homotecia: perímetros y áreas', (t, nivel) => {
    const k = t.elige([F(2), F(3), F(-2), F(-3), F(1, 2), F(3, 2), F(-1, 2), F(5, 2)]);
    const ak = F(Math.abs(k.p), k.q);
    if (nivel === 'dificil') {
      const A = 4 * t.ent(1, 12) * k.q * k.q, A2 = fmul(A, fmul(ak, ak));
      return {
        enun: `Una figura de área ${A} cm² se transforma por una homotecia y su imagen tiene área ${fq(A2)} cm². ¿Cuál es el valor absoluto de la razón de la homotecia?`, ok: fq(ak),
        malas: [[fq(fmul(ak, ak)), 'Esa es la razón entre las áreas. La razón de homotecia es su raíz cuadrada: las áreas cambian por k².'], [fq(finv(ak)), 'Invertiste la razón: es imagen/original, no original/imagen.'], [fq(fdiv(fsub(A2, A), A)), 'Calculaste cuánto creció el área (en proporción). La razón es √(área imagen/área original).']],
        exp: `Las áreas cambian por k²: k² = ${fq(A2)}/${A} = ${fq(fmul(ak, ak))} → |k| = ${fq(ak)}.`, p: { A, A2, pide: 'razon' },
      };
    }
    if (nivel === 'basico') {
      const P = t.ent(3, 15) * 2 * k.q;
      const malas = [[fq(fmul(P, fmul(ak, ak))), 'El perímetro es una longitud: se multiplica por |k|, no por k².'], [fq(fadd(P, ak)), 'Sumaste k. La homotecia multiplica las longitudes.'], [fq(fdiv(P, ak)), `Dividiste por ${fq(ak)}: hay que multiplicar.`]];
      if (k.p < 0) malas.push([fq(fmul(P, k)), 'Un perímetro no puede ser negativo: se multiplica por |k|.']);
      return { enun: `Un polígono tiene perímetro ${P} cm. ¿Cuál es el perímetro de su imagen por una homotecia de razón ${fq(k)}?`, ok: fq(fmul(P, ak)) + ' cm', malas: malas.map(([a, b]) => [a + ' cm', b]), exp: `Las longitudes se multiplican por |k| = ${fq(ak)}: ${P}·${fq(ak)} = ${fq(fmul(P, ak))} cm.`, p: { P, k, pide: 'per' } };
    }
    const A = t.ent(2, 12) * k.q * k.q;
    const malas = [[fq(fmul(A, ak)), 'El área se multiplica por k², no por k.'], [fq(fmul(A, fmul(ak, fmul(ak, ak)))), 'k³ es para volúmenes; las áreas usan k².'], [fq(fdiv(A, fmul(ak, ak))), 'Dividiste por k²: hay que multiplicar.']];
    if (k.p < 0) malas.push([fq(fmul(A, fmul(k, ak))), 'El signo de k solo invierte la figura; un área no puede ser negativa.']);
    return { enun: `Un triángulo tiene área ${A} cm². ¿Cuál es el área de su imagen por una homotecia de razón ${fq(k)}?`, ok: fq(fmul(A, fmul(k, k))) + ' cm²', malas: malas.map(([a, b]) => [a + ' cm²', b]), exp: `Las áreas se multiplican por k² = ${fq(fmul(k, k))}: ${A}·${fq(fmul(k, k))} = ${fq(fmul(A, fmul(k, k)))} cm².`, p: { A, k, pide: 'area' } };
  });

  fam('hom-razon', T_HOM, ['dificil'], 'Encontrar la razón de homotecia', (t) => {
    const k = t.elige(RAZONES), O = [t.ent(-3, 3), t.ent(-3, 3)];
    const P = [O[0] + k.q * t.nz(-3, 3), O[1] + k.q * t.nz(-3, 3)];
    const Pi = [fadd(O[0], fmul(k, P[0] - O[0])), fadd(O[1], fmul(k, P[1] - O[1]))];
    const malas = [[fq(finv(k)), "Invertiste: k = (P' − O)/(P − O), la imagen va arriba."], [fq(fneg(k)), fval(k) > 0 ? 'P y su imagen están del mismo lado del centro: la razón es positiva.' : 'P y su imagen están en lados opuestos del centro: la razón es negativa.']];
    if (P[0] !== 0) malas.push([fq(fdiv(Pi[0], P[0])), 'Dividiste las coordenadas sin restar el centro. Hay que comparar P − O con P\' − O.']);
    if (P[1] !== 0) malas.push([fq(fdiv(Pi[1], P[1])), 'Dividiste las coordenadas sin restar el centro. Hay que comparar P − O con P\' − O.']);
    malas.push([fq(fsub(k, 1)), "Calculaste (P' − P)/(P − O). La razón compara P' − O con P − O."]);
    return {
      enun: `Una homotecia de centro O${pt(O[0], O[1])} lleva el punto P${pt(P[0], P[1])} al punto P'${pt(Pi[0], Pi[1])}. ¿Cuál es la razón de la homotecia?`, ok: fq(k), malas,
      exp: `P − O = ${pt(P[0] - O[0], P[1] - O[1])} y P' − O = ${pt(fsub(Pi[0], O[0]), fsub(Pi[1], O[1]))}. P' − O = k·(P − O) → k = ${fq(k)}.`,
      p: { O, P, Pi },
    };
  });

  // =====================================================================
  // M2 · Matemática financiera
  // =====================================================================
  const T_FIN = 'm2.num.financiera';
  fam('fin-compuesto', T_FIN, ['basico', 'paes'], 'Interés compuesto', (t, nivel) => {
    const n = t.elige([2, 2, 3]), i = t.elige([1, 2, 3, 4, 5, 10, 20]);
    const C = n === 2 ? 10000 * t.elige([10, 20, 30, 50, 80, 100, 150, 200]) : 1000000 * t.ent(1, 5);
    const M = (C * (100 + i) ** n) / 100 ** n, I = M - C;
    const per = t.elige(['anual', 'mensual']), u = per === 'anual' ? 'años' : 'meses';
    const intro = `Se depositan ${pesos(C)} a un interés compuesto del ${i} % ${per} durante ${n} ${u}.`;
    if (nivel === 'basico') {
      return {
        enun: `${intro} ¿Cuánto dinero habrá al final?`, ok: pesos(M),
        malas: [[pesos(C * (1 + (n * i) / 100)), 'Calculaste interés simple. En el compuesto, el interés de cada período se suma al capital y también gana interés.'], [pesos(I), 'Ese es solo el interés ganado; el monto final incluye el capital.'], [pesos(C * (1 + i / 100) * n), `Multiplicaste por ${n} en vez de elevar a ${n}.`]],
        exp: `M = C·(1 + i)${sup('n')} = ${pesos(C)}·${num(1 + i / 100)}${sup(n)} = ${pesos(M)}.`, p: { C, i, n, pide: 'M' },
      };
    }
    return {
      enun: `${intro} ¿Cuánto interés se gana en total?`, ok: pesos(I),
      malas: [[pesos((C * i * n) / 100), 'Ese es el interés simple. En el compuesto, cada período gana interés sobre lo acumulado.'], [pesos(M), 'Ese es el monto final; el interés es lo ganado por sobre el capital.'], [pesos((C * i) / 100), 'Ese es el interés de un solo período.']],
      exp: `M = ${pesos(C)}·${num(1 + i / 100)}${sup(n)} = ${pesos(M)}. Interés = M − C = ${pesos(I)}.`, p: { C, i, n, pide: 'I' },
    };
  });

  fam('fin-simple', T_FIN, ['basico'], 'Interés simple', (t) => {
    const C = 10000 * t.elige([10, 20, 30, 40, 50, 60, 80, 100, 120]), i = t.ent(1, 5), m = t.ent(2, 11);
    const I = (C * i * m) / 100;
    const pide = t.elige(['I', 'M']);
    const comp = Math.round(C * (1 + i / 100) ** m);
    const malas = pide === 'I'
      ? [[pesos((C * i) / 100), 'Calculaste el interés de un solo mes.'], [pesos(C + I), 'Ese es el monto final (capital + interés); se pide solo el interés.'], [pesos(comp - C), 'Calculaste interés compuesto; aquí el interés es simple: cada mes se gana lo mismo.']]
      : [[pesos(C + (C * i) / 100), 'Sumaste el interés de un solo mes.'], [pesos(I), 'Ese es solo el interés; el monto final suma el capital.'], [pesos(comp), 'Calculaste interés compuesto; aquí el interés es simple: cada mes se gana lo mismo.']];
    return {
      enun: `Se invierten ${pesos(C)} a un interés simple del ${i} % mensual durante ${m} meses. ¿Cuánto ${pide === 'I' ? 'interés se gana' : 'dinero hay al final'}?`, ok: pesos(pide === 'I' ? I : C + I), malas,
      exp: `Interés simple: I = C·i·t = ${pesos(C)}·${num(i / 100)}·${m} = ${pesos(I)}.${pide === 'M' ? ` Monto = ${pesos(C)} + ${pesos(I)} = ${pesos(C + I)}.` : ''}`, p: { C, i, m, pide },
    };
  });

  fam('fin-credito', T_FIN, ['paes', 'dificil'], 'Costo de un crédito (con y sin pie)', (t, nivel) => {
    const n = t.elige([6, 10, 12, 18, 24, 36]);
    if (nivel === 'paes') {
      const M = 100000 * t.ent(5, 40), r = t.ent(5, 40);
      const q = Math.ceil((M * (1 + r / 100)) / n / 1000) * 1000;
      return {
        enun: `Un crédito de consumo de ${pesos(M)} se paga en ${n} cuotas iguales de ${pesos(q)}. ¿Cuál es el costo del crédito (lo que se paga por sobre lo pedido)?`, ok: pesos(n * q - M),
        malas: [[pesos(n * q), 'Ese es el total pagado. El costo es lo que se paga por sobre lo que se pidió.'], [pesos(q), 'Esa es una cuota.'], ...((n * q - M) % n ? [] : [[pesos((n * q - M) / n), 'Ese es el costo repartido por cuota; se pide el costo total.']])],
        exp: `Total pagado: ${n}·${pesos(q)} = ${pesos(n * q)}. Costo = ${pesos(n * q)} − ${pesos(M)} = ${pesos(n * q - M)}.`, p: { M, n, q, pie: 0 },
      };
    }
    const P = 100000 * t.ent(5, 30), pie = 10000 * Math.round((P * t.elige([10, 20, 25, 30])) / 100 / 10000), r = t.ent(8, 40);
    const q = Math.ceil(((P - pie) * (1 + r / 100)) / n / 1000) * 1000;
    return {
      enun: `Un producto cuesta ${pesos(P)} al contado. Se compra con un pie de ${pesos(pie)} y ${n} cuotas de ${pesos(q)}. ¿Cuánto más se paga que al contado?`, ok: pesos(pie + n * q - P),
      malas: [[pesos(n * q - P), 'Olvidaste sumar el pie: también es parte de lo que se paga.'], [pesos(pie + n * q), 'Ese es el total pagado; se pide la diferencia con el precio al contado.'], [pesos(n * q), 'Contaste solo las cuotas, sin el pie y sin compararlas con el precio.']],
      exp: `Total pagado: ${pesos(pie)} + ${n}·${pesos(q)} = ${pesos(pie + n * q)}. Diferencia con el contado: ${pesos(pie + n * q)} − ${pesos(P)} = ${pesos(pie + n * q - P)}.`, p: { M: P, n, q, pie },
    };
  });

  fam('fin-afp', T_FIN, ['basico', 'paes'], 'AFP y créditos en UF', (t, nivel) => {
    if (nivel === 'basico') {
      const s = 10000 * t.ent(50, 250), c = t.elige([0.5, 1, 1.2, 1.5, 2]);
      const D = (s * (10 + c)) / 100;
      return {
        enun: `De un sueldo imponible de ${pesos(s)} se descuenta para la AFP el 10 % obligatorio más una comisión del ${num(c)} % del sueldo. ¿Cuánto se descuenta en total?`, ok: pesos(D),
        malas: [[pesos(s / 10), 'Olvidaste la comisión de la AFP.'], [pesos((s * c) / 100), 'Esa es solo la comisión; falta el 10 % obligatorio.'], [pesos(s - D), 'Eso es lo que queda del sueldo, no el descuento.']],
        exp: `${num(10 + c)} % de ${pesos(s)} = ${num((10 + c) / 100)}·${pesos(s)} = ${pesos(D)}.`, p: { s, c, pide: 'afp' },
      };
    }
    const d = t.ent(8, 25), U = 1000 * t.ent(36, 40), m = t.elige([12, 6]);
    return {
      enun: `El dividendo mensual de un crédito hipotecario es de ${d} UF. Si la UF vale ${pesos(U)}, ¿cuánto se paga en pesos en ${m} meses?`, ok: pesos(d * U * m),
      malas: [[pesos(d * U), 'Ese es un solo dividendo.'], [`${d * m} UF`, 'Ese total está en UF: falta convertirlo a pesos.'], [pesos(U * m), `Olvidaste multiplicar por las ${d} UF del dividendo: calculaste como si fuera 1 UF al mes.`]],
      exp: `${d} UF·${pesos(U)} = ${pesos(d * U)} por mes. En ${m} meses: ${pesos(d * U * m)}.`, p: { d, U, m, pide: 'uf' },
    };
  });

  // =====================================================================
  // M2 · Esfera
  // =====================================================================
  const T_ESF = 'm2.geo.esfera';
  fam('esf-medidas', T_ESF, ['basico', 'paes'], 'Área y volumen de la esfera', (t, nivel) => {
    const r = t.ent(1, 9), conD = nivel === 'paes' && t.r() < 0.6, d = 2 * r;
    const dato = conD ? `diámetro ${d} cm` : `radio ${r} cm`;
    const pide = t.elige(['V', 'A']);
    if (pide === 'V') {
      const malas = [[pit(4 * r * r) + ' cm³', 'Esa fórmula es la del área (4πr²); el volumen es (4/3)πr³.'], [pit(4 * r ** 3) + ' cm³', 'Olvidaste dividir por 3: V = (4/3)πr³.'], [pit(F(4 * r * r, 3)) + ' cm³', 'Elevaste el radio al cuadrado; el volumen usa r³.']];
      if (conD) malas.push([pit(F(4 * d ** 3, 3)) + ' cm³', `Usaste el diámetro como radio: r = ${d}/2 = ${r}.`]);
      return { enun: `¿Cuál es el volumen de una esfera de ${dato}?`, ok: pit(F(4 * r ** 3, 3)) + ' cm³', malas, exp: `${conD ? `r = ${d}/2 = ${r} cm. ` : ''}V = (4/3)πr³ = (4/3)π·${r ** 3} = ${pit(F(4 * r ** 3, 3))} cm³.`, p: { r, pide } };
    }
    const malas = [[pit(r * r) + ' cm²', 'Esa es el área de un círculo máximo. La esfera tiene 4 veces eso: 4πr².'], [pit(F(4 * r ** 3, 3)) + ' cm²', 'Esa es la fórmula del volumen; el área es 4πr².'], [pit(2 * r * r) + ' cm²', 'Esa es el área de media esfera (sin la tapa).']];
    if (conD) malas.push([pit(4 * d * d) + ' cm²', `Usaste el diámetro como radio: r = ${d}/2 = ${r}.`]);
    return { enun: `¿Cuál es el área de una esfera de ${dato}?`, ok: pit(4 * r * r) + ' cm²', malas, exp: `${conD ? `r = ${d}/2 = ${r} cm. ` : ''}A = 4πr² = 4π·${r * r} = ${pit(4 * r * r)} cm².`, p: { r, pide } };
  });

  fam('esf-escala', T_ESF, ['paes'], 'Si el radio cambia, ¿cuánto cambian el área y el volumen?', (t) => {
    const k = t.elige([2, 3, 4]), pide = t.elige(['V', 'A']), q = pide === 'V' ? 'volumen' : 'área';
    const ok = pide === 'V' ? k ** 3 : k ** 2;
    return {
      enun: `Si el radio de una esfera se multiplica por ${k}, ¿por cuánto se multiplica su ${q}?`, ok: num(ok),
      malas: [[num(k), `El ${q} no crece igual que el radio: ${pide === 'V' ? 'el volumen depende de r³' : 'el área depende de r²'}.`], [num(pide === 'V' ? k ** 2 : k ** 3), pide === 'V' ? 'k² es para áreas; el volumen usa r³.' : 'k³ es para volúmenes; el área usa r².'], [num(pide === 'V' ? 3 * k : 2 * k), `Multiplicaste por el exponente; hay que elevar: ${k}${sup(pide === 'V' ? 3 : 2)}.`]],
      exp: `${pide === 'V' ? 'V = (4/3)πr³' : 'A = 4πr²'}: con r → ${k}r, queda multiplicado por ${k}${sup(pide === 'V' ? 3 : 2)} = ${ok}.`, p: { k, pide },
    };
  });

  fam('esf-fundir', T_ESF, ['dificil'], 'Esferas y cilindros: igualar volúmenes', (t) => {
    const r = t.ent(2, 9), R = t.ent(2, 9);
    if ((4 * r ** 3) % (3 * R * R)) throw OTRA;
    const h = (4 * r ** 3) / (3 * R * R);
    return {
      enun: `Una esfera de metal de radio ${r} cm se funde y con todo el metal se forma un cilindro de radio ${R} cm. ¿Cuál es la altura del cilindro?`, ok: `${num(h)} cm`,
      malas: [[`${fq(F(4 * r ** 3, R * R))} cm`, 'Olvidaste dividir por 3 el volumen de la esfera: (4/3)πr³.'], [`${fq(F(r ** 3, R * R))} cm`, 'Olvidaste el 4/3 del volumen de la esfera.'], [`${fq(F(4 * r ** 3, 3 * R))} cm`, 'Dividiste por R en vez de R²: el volumen del cilindro es πR²h.']],
      exp: `Volúmenes iguales: (4/3)π·${r}³ = π·${R}²·h → h = 4·${r ** 3}/(3·${R * R}) = ${num(h)} cm.`, p: { r, R },
    };
  });

  // =====================================================================
  // M2 · Función potencia
  // =====================================================================
  const T_POT = 'm2.alg.potencia';
  fam('pot-valor', T_POT, ['basico', 'paes'], 'Evaluar f(x) = a·xⁿ', (t, nivel) => {
    const a = t.nz(-3, 3), n = nivel === 'basico' ? t.ent(2, 5) : t.elige([-1, -2, -3, 3, 4]);
    const x = nivel === 'basico' ? t.elige([-3, -2, -1, 2, 3]) : t.elige([-2, -1, 2, 3, F(1, 2)]);
    const v = fmul(a, fpow(x, n));
    const f = `f(x) = ${a === 1 ? '' : a === -1 ? MENOS : num(a)}x${sup(num(n))}`;
    const malas = [[fq(fmul(a * n, x)), `Multiplicaste por ${num(n)} en vez de elevar.`], [fq(fpow(fmul(a, x), n)), `Elevaste también el ${num(a)}: solo se eleva x.`]];
    if (n % 2 === 0 && fval(x) < 0) malas.push([fq(fneg(v)), `(${fq(x)})${sup(num(n))} es positivo: el signo menos también se eleva (exponente par).`]);
    if (n < 0) { malas.push([fq(fmul(a, fneg(fpow(x, -n)))), 'El exponente negativo no hace negativo el resultado: invierte la base. x⁻ⁿ = 1/xⁿ.']); malas.push([fq(fmul(a, fpow(x, -n))), 'Olvidaste invertir: x⁻ⁿ = 1/xⁿ.']); }
    malas.push([fq(fneg(v)), 'Error de signo: revisa el signo de a y el de la potencia.']);
    return { enun: `Si ${f}, ¿cuál es el valor de f(${fq(x)})?`, ok: fq(v), malas, exp: `f(${fq(x)}) = ${num(a)}·(${fq(x)})${sup(num(n))} = ${num(a)}·${par(fpow(x, n))} = ${fq(v)}.`, p: { a, n, x } };
  });

  fam('pot-parametro', T_POT, ['paes', 'dificil'], 'Encontrar a o n en f(x) = a·xⁿ', (t, nivel) => {
    if (nivel === 'paes') {
      const a = t.nz(-4, 4), n = t.ent(2, 4), p = t.elige([-2, 2, 3]);
      const q = a * p ** n;
      return {
        enun: `El gráfico de f(x) = a·x${sup(n)} pasa por el punto ${pt(p, q)}. ¿Cuál es el valor de a?`, ok: num(a),
        malas: [[fq(F(q, p)), `Dividiste por ${num(p)}; hay que dividir por ${par(p)}${sup(n)} = ${num(p ** n)}.`], [num(q * p ** n), `Multiplicaste por ${num(p ** n)} en vez de dividir.`], [num(q - p ** n), 'Restaste; f(x) = a·xⁿ es un producto.']],
        exp: `${num(q)} = a·${par(p)}${sup(n)} = a·${par(p ** n)} → a = ${num(q)}/${par(p ** n)} = ${num(a)}.`, p: { n, p, q },
      };
    }
    const a = t.nz(-3, 3), n = t.ent(2, 5);
    return {
      enun: `La función f(x) = a·x${sup('n')} cumple f(1) = ${num(a)} y f(2) = ${num(a * 2 ** n)}. ¿Cuál es el valor de n?`, ok: num(n),
      malas: [[num(2 ** n), `Ese es f(2)/f(1). n es el exponente: 2${sup('n')} = ${2 ** n}.`], [num(-n), `Invertiste la razón: f(1)/f(2) = 1/${2 ** n} da n = −${n}. Es f(2)/f(1) = 2${sup('n')}.`], [num(a * 2 ** n - a), 'Restaste los valores; hay que dividirlos y buscar el exponente.']],
      exp: `f(1) = a = ${num(a)}. f(2) = ${num(a)}·2${sup('n')} = ${num(a * 2 ** n)} → 2${sup('n')} = ${2 ** n} → n = ${n}.`, p: { a, n },
    };
  });

  // =====================================================================
  // M2 · Operatoria en los reales
  // =====================================================================
  const T_REA = 'm2.num.reales';
  fam('real-raices', T_REA, ['basico', 'paes'], 'Sumar raíces y cuadrado de un binomio', (t, nivel) => {
    if (nivel === 'basico') {
      const b = t.elige([2, 3, 5, 6, 7]), a = t.ent(1, 5), c = t.ent(1, 5), d = t.ent(1, 4);
      if (a + c - d === 0 || a === c) throw OTRA;
      const rr = (k) => `√${k * k * b}`;
      const tot = a * a * b + c * c * b - d * d * b;
      if (tot <= 0) throw OTRA;
      return {
        enun: `¿Cuál es el valor de ${rr(a)} + ${rr(c)} − ${rr(d)}?`, ok: rad(a + c - d, b),
        malas: [[rad(1, tot), 'Operaste los números dentro de la raíz: √x + √y no es √(x + y).'], [rad(a + c + d, b), 'Sumaste el último término; va restando.'], [num(a + c - d), `Olvidaste el √${b} común.`]],
        exp: `${rr(a)} = ${rad(a, b)}, ${rr(c)} = ${rad(c, b)}, ${rr(d)} = ${rad(d, b)}. Suma: (${a} + ${c} − ${d})√${b} = ${rad(a + c - d, b)}.`, p: { a, c, d, b },
      };
    }
    const [p, q] = t.elige([[2, 3], [2, 5], [3, 5], [2, 7], [3, 7], [5, 7], [3, 2], [5, 3]]);
    const sg = t.elige([1, -1]);
    const ok = sumaRad(p + q, 2 * sg, p * q);
    return {
      enun: `¿Cuál es el valor de (√${p} ${sg > 0 ? '+' : MENOS} √${q})²?`, ok,
      malas: [[num(p + q), 'El cuadrado de un binomio tiene tres términos: falta el doble producto 2·√' + p + '·√' + q + '.'], [sumaRad(p + q, sg, p * q), 'Falta el 2 del doble producto: (a ± b)² = a² ± 2ab + b².'], [sumaRad(p + q, -2 * sg, p * q), 'Error de signo en el doble producto.']],
      exp: `(a ${sg > 0 ? '+' : MENOS} b)² = a² ${sg > 0 ? '+' : MENOS} 2ab + b² = ${p} ${sg > 0 ? '+' : MENOS} 2√${p * q} + ${q} = ${ok}.`, p: { p, q, sg },
    };
  });

  fam('real-racionalizar', T_REA, ['paes', 'dificil'], 'Racionalizar', (t, nivel) => {
    if (nivel === 'paes') {
      const b = t.elige([2, 3, 5, 6, 7]), a = t.ent(1, 12);
      if (a % b === 0 && a / b === 1) throw OTRA;
      return {
        enun: `¿Cuál es el resultado de racionalizar ${a}/√${b}?`, ok: rad(F(a, b), b),
        malas: [[rad(a, b), `Multiplicaste arriba por √${b}, pero olvidaste dividir por ${b} (√${b}·√${b} = ${b}).`], [fq(F(a, b)), 'Perdiste la raíz del numerador.'], [rad(F(1, a), b), 'Invertiste la fracción.']],
        exp: `${a}/√${b} · √${b}/√${b} = ${igual(`${a === 1 ? '' : a}√${b}/${b}`, rad(F(a, b), b))}.`, p: { a, b },
      };
    }
    const [m, n] = t.elige([[3, 2], [5, 2], [5, 3], [7, 3], [6, 2], [7, 5], [6, 5], [7, 2]]);
    const k = t.ent(1, 4), c = k * (m - n);
    const conj = (coef, s) => (coef === 1 ? `√${m} ${s > 0 ? '+' : MENOS} √${n}` : `${num(coef)}(√${m} ${s > 0 ? '+' : MENOS} √${n})`);
    const malas = [[conj(k, -1), 'Multiplicaste por el conjugado, pero mantuviste el signo menos arriba.'], [conj(c, 1), `Olvidaste dividir por ${m} − ${n} = ${m - n}.`]];
    const fr2 = F(c, m + n);
    malas.push([fr2.q === 1 ? conj(fr2.p, 1) : `${fr2.p === 1 ? '' : num(fr2.p)}(√${m} + √${n})/${fr2.q}`, `El denominador es (√${m} − √${n})(√${m} + √${n}) = ${m} − ${n}, no ${m} + ${n}.`]);
    return {
      enun: `¿Cuál es el resultado de racionalizar ${c}/(√${m} − √${n})?`, ok: conj(k, 1), malas,
      exp: `Multiplica por el conjugado √${m} + √${n}: abajo queda ${m} − ${n} = ${m - n}. ${c}(√${m} + √${n})/${m - n} = ${conj(k, 1)}.`, p: { c, m, n },
    };
  });

  fam('real-pot-fraccion', T_REA, ['basico'], 'Potencias de exponente fraccionario', (t) => {
    const r = t.elige([2, 3, 4, 5]), q = t.elige([2, 3]), p = t.ent(1, 3) * t.elige([1, 1, -1]);
    const B = r ** q;
    if (B > 200) throw OTRA;
    const v = fpow(r, p), ap = Math.abs(p);
    const malas = [[fq(fmul(B, F(p, q))), 'Multiplicaste la base por el exponente.'], [num(B), `Ignoraste el exponente: ${B}${sup(`${ap}/${q}`)} es la raíz ${q === 2 ? 'cuadrada' : 'cúbica'} de ${B}, elevada a ${ap}.`]];
    if (p < 0) { malas.push([fq(fneg(v)), 'El exponente negativo invierte, no cambia el signo.']); malas.push([fq(fpow(r, ap)), 'Olvidaste invertir: a⁻ⁿ = 1/aⁿ.']); }
    if (ap !== 1) { malas.push([fq(p < 0 ? F(1, r) : F(r)), `Sacaste la raíz ${q === 2 ? 'cuadrada' : 'cúbica'}, pero olvidaste elevar a ${ap}.`]); malas.push([fq(p < 0 ? F(1, r * ap) : F(r * ap)), `Multiplicaste la raíz por ${ap} en vez de elevarla a ${ap}.`]); }
    const otraRaiz = q === 3 ? Math.round(Math.sqrt(B)) : Math.round(Math.cbrt(B));
    if ((q === 3 ? otraRaiz ** 2 : otraRaiz ** 3) === B && otraRaiz !== r) malas.push([fq(fpow(otraRaiz, p)), `Sacaste raíz ${q === 3 ? 'cuadrada' : 'cúbica'}; el denominador ${q} indica raíz ${q === 3 ? 'cúbica' : 'cuadrada'}.`]);
    return {
      enun: `¿Cuál es el valor de ${B}${sup(`${p < 0 ? MENOS : ''}${Math.abs(p)}/${q}`)}?`, ok: fq(v), malas,
      exp: `${B}${sup(`${p < 0 ? MENOS : ''}${Math.abs(p)}/${q}`)} = (${q === 2 ? '√' : '∛'}${B})${sup(num(p))} = ${r}${sup(num(p))} = ${fq(v)}.`, p: { B, p, q },
    };
  });

  // =====================================================================
  // M2 · M1 en versión difícil
  // =====================================================================
  const T_M1D = 'm2.m1-dificil';
  fam('m1d-cuadratica', T_M1D, ['paes', 'dificil'], 'Función cuadrática: vértice, ceros y discriminante', (t, nivel) => {
    if (nivel === 'paes') {
      const a = t.elige([1, -1, 2, -2]), h = t.nz(-5, 5), k = t.ent(-6, 6);
      const b = -2 * a * h, c = a * h * h + k;
      return {
        enun: `¿Cuál es el vértice de la parábola f(x) = ${lin([[a, 'x²'], [b, 'x'], [c, '']])}?`, ok: pt(h, k),
        malas: [[pt(-h, 4 * a * h * h + k), `Error de signo en x = −b/(2a) = −${par(b)}/${par(2 * a)} = ${num(h)}.`], [pt(h, c), `${num(c)} es donde la parábola corta al eje Y, no la altura del vértice. Reemplaza x = ${num(h)} en f.`], [pt(k, h), 'Invertiste las coordenadas del vértice.']],
        exp: `x = −b/(2a) = −${par(b)}/${par(2 * a)} = ${num(h)}. f(${num(h)}) = ${num(k)}. Vértice: ${pt(h, k)}.`, p: { a, b, c },
      };
    }
    if (t.r() < 0.5) {
      const b = 2 * t.nz(-6, 6);
      return {
        enun: `¿Para qué valor de m la ecuación ${lin([[1, 'x²'], [b, 'x']])} + m = 0 tiene una única solución real?`, ok: num((b * b) / 4),
        malas: [[num(-b / 2), 'Ese es el x del vértice. Una única solución pide discriminante 0: b² − 4m = 0.'], [num(-(b * b) / 4), 'Error de signo: b² − 4m = 0 → m = b²/4.'], [num(b * b), 'Te faltó dividir por 4: b² − 4m = 0 → m = b²/4.']],
        exp: `Una única solución ⇔ discriminante = 0: ${par(b)}² − 4m = ${b * b} − 4m = 0 → m = ${(b * b) / 4}.`, p: { b, pide: 'disc' },
      };
    }
    const r1 = t.ent(-7, 7), r2 = t.ent(-7, 7);
    if (r1 === r2 || r1 === -r2 || r1 === 0 || r2 === 0) throw OTRA;
    const [u, v] = [Math.min(r1, r2), Math.max(r1, r2)];
    const S = (a, b) => `x = ${num(Math.min(a, b))} y x = ${num(Math.max(a, b))}`;
    const fac = (r) => (r < 0 ? `(x + ${-r})` : `(x − ${r})`);
    return {
      enun: `¿Cuáles son las soluciones de la ecuación ${lin([[1, 'x²'], [-(r1 + r2), 'x'], [r1 * r2, '']])} = 0?`, ok: S(u, v),
      malas: [[S(-u, -v), `Cambiaste los signos: si ${fac(u)}${fac(v)} = 0, las soluciones son los números que anulan cada factor, x = ${num(u)} y x = ${num(v)}.`], [S(1, r1 * r2), `Las soluciones deben multiplicar ${num(r1 * r2)}, pero también sumar ${num(r1 + r2)}.`], [S(-u, v), 'Error de signo en una de las soluciones: comprueba reemplazando en la ecuación.']],
      exp: `Factoriza: ${lin([[1, 'x²'], [-(r1 + r2), 'x'], [r1 * r2, '']])} = ${fac(u)}${fac(v)}. Cada factor se anula en x = ${num(u)} y x = ${num(v)}. (Las soluciones suman ${num(r1 + r2)} y multiplican ${num(r1 * r2)}.)`, p: { r1, r2, pide: 'raices' },
    };
  });

  fam('m1d-thales', T_M1D, ['paes', 'dificil'], 'Semejanza y Thales', (t, nivel) => {
    if (nivel === 'paes') {
      const a = t.ent(2, 9), b = t.ent(2, 9), d = t.ent(1, 3) * a + t.elige([0, a]);
      const BC = F(d * (a + b), a);
      return {
        enun: `En el triángulo ABC, D está en AB y E en AC, con DE paralelo a BC. Si AD = ${a} cm, DB = ${b} cm y DE = ${d} cm, ¿cuánto mide BC?`, ok: fq(BC) + ' cm',
        malas: [[fq(F(d * b, a)) + ' cm', `Usaste DB en vez de AB = AD + DB = ${a + b}.`], [num(d + b) + ' cm', `Sumaste DB a DE (${d} + ${b}). Hay que usar la proporción DE/BC = AD/AB.`], [fq(F(d * a, a + b)) + ' cm', 'Invertiste la razón: BC debe ser mayor que DE.']],
        exp: `Por Thales (triángulos ADE y ABC semejantes): DE/BC = AD/AB → ${d}/BC = ${a}/${a + b} → BC = ${d}·${a + b}/${a} = ${fq(BC)} cm.`, p: { a, b, d },
      };
    }
    const [m, n] = t.elige([[3, 2], [5, 2], [4, 3], [5, 3], [2, 1], [3, 1]]);
    const A = n * n * t.ent(2, 9);
    const A2 = fmul(A, F(m * m, n * n));
    return {
      enun: `Dos triángulos son semejantes y la razón entre sus lados es ${m}:${n}. Si el área del menor es ${A} cm², ¿cuál es el área del mayor?`, ok: fq(A2) + ' cm²',
      malas: [[fq(fmul(A, F(m, n))) + ' cm²', `Las áreas están en razón (${m}/${n})², no ${m}/${n}.`], [fq(fmul(A, F(m ** 3, n ** 3))) + ' cm²', 'La razón al cubo es para volúmenes; las áreas usan el cuadrado.'], [fq(fmul(A, F(n * n, m * m))) + ' cm²', 'Invertiste la razón: el triángulo mayor tiene más área.']],
      exp: n === 1 ? `Razón de áreas = (razón de lados)² = ${m}² = ${m * m}. Área mayor = ${A}·${m * m} = ${fq(A2)} cm².` : `Razón de áreas = (razón de lados)² = (${m}/${n})² = ${m * m}/${n * n}. Área mayor = ${A}·${m * m}/${n * n} = ${fq(A2)} cm².`, p: { m, n, A },
    };
  });

  fam('m1d-cilindro', T_M1D, ['basico', 'paes'], 'Cilindro: volumen y área', (t, nivel) => {
    const r = t.ent(1, 8), h = t.ent(2, 12), conD = nivel === 'paes' && t.r() < 0.6, d = 2 * r;
    const pide = nivel === 'basico' ? 'V' : t.elige(['V', 'A']);
    const dato = conD ? `diámetro basal ${d} cm` : `radio basal ${r} cm`;
    if (pide === 'V') {
      const malas = [[pit(2 * r * h) + ' cm³', 'Esa es el área lateral (2πrh), no el volumen.'], [pit(r * h) + ' cm³', 'Te faltó elevar el radio al cuadrado: V = πr²h.'], [pit(F(r * r * h, 3)) + ' cm³', 'Dividiste por 3: esa es la fórmula del cono.']];
      if (conD) malas.push([pit(d * d * h) + ' cm³', `Usaste el diámetro como radio: r = ${d}/2 = ${r}.`]);
      return { enun: `¿Cuál es el volumen de un cilindro de ${dato} y altura ${h} cm?`, ok: pit(r * r * h) + ' cm³', malas, exp: `${conD ? `r = ${r} cm. ` : ''}V = πr²h = π·${r * r}·${h} = ${pit(r * r * h)} cm³.`, p: { r, h, pide } };
    }
    const malas = [[pit(2 * r * h) + ' cm²', 'Esa es solo el área lateral; faltan las dos tapas (2πr²).'], [pit(2 * r * h + r * r) + ' cm²', 'Contaste una sola tapa; el cilindro tiene dos.'], [pit(r * r * h) + ' cm²', 'Esa es la fórmula del volumen.']];
    if (conD) malas.push([pit(2 * d * h + 2 * d * d) + ' cm²', `Usaste el diámetro como radio: r = ${d}/2 = ${r}.`]);
    return { enun: `¿Cuál es el área total de un cilindro de ${dato} y altura ${h} cm?`, ok: pit(2 * r * h + 2 * r * r) + ' cm²', malas, exp: `${conD ? `r = ${r} cm. ` : ''}Área total = 2πrh + 2πr² = ${pit(2 * r * h)} + ${pit(2 * r * r)} = ${pit(2 * r * h + 2 * r * r)} cm².`, p: { r, h, pide } };
  });

  // =====================================================================
  // M2 · Suficiencia de datos
  // =====================================================================
  const SD_OPS = ['(1) por sí sola', '(2) por sí sola', 'Ambas juntas, (1) y (2)', 'Cada una por sí sola, (1) ó (2)', 'Se requiere información adicional'];
  fam('sd-valor', 'm2.sd', ['basico', 'paes', 'dificil'], 'Suficiencia de datos: ¿se puede determinar x?', (t, nivel) => {
    const [vx, vy] = t.elige([['x', 'y'], ['a', 'b'], ['m', 'n'], ['p', 'q']]);
    const x0 = t.nz(-6, 7), y0 = t.nz(-6, 7);
    if (Math.abs(x0) === Math.abs(y0)) throw OTRA;
    const S = {
      X: () => { const a = t.nz(-4, 5), e = t.ent(-9, 9); return { tipo: 'X', a, e, f: a * x0 + e, txt: `${lin([[a, vx], [e, '']])} = ${num(a * x0 + e)}` }; },
      Y: () => { const b = t.nz(-4, 5), e = t.ent(-9, 9); return { tipo: 'Y', b, e, f: b * y0 + e, txt: `${lin([[b, vy], [e, '']])} = ${num(b * y0 + e)}` }; },
      XY: () => {
        const a = t.nz(-3, 4), b = t.nz(-3, 4);
        const c = a * x0 + b * y0;
        const v = t.r();
        let txt = `${lin([[a, vx], [b, vy]])} = ${num(c)}`;
        if (a === 1 && b === 1 && v < 0.4) txt = `La suma de ${vx} e ${vy} es ${num(c)}.`;
        if (a === 1 && b === -1 && c > 0 && v < 0.4) txt = `${vx} es ${c} ${c === 1 ? 'unidad' : 'unidades'} mayor que ${vy}.`;
        return { tipo: 'XY', a, b, c, txt };
      },
      SQ: () => ({ tipo: 'SQ', v2: x0 * x0, txt: `${vx}² = ${x0 * x0}` }),
      POS: () => ({ tipo: 'POS', s: x0 > 0 ? 1 : -1, txt: x0 > 0 ? `${vx} &gt; 0` : `${vx} &lt; 0` }),
    };
    const otraXY = (s1) => { for (let i = 0; i < 30; i++) { const s = S.XY(); if (s.a * s1.b - s.b * s1.a !== 0) return s; } throw OTRA; };
    const doble = (s1) => { const l = t.elige([2, 3, -2, -1]); return { tipo: 'XY', a: l * s1.a, b: l * s1.b, c: l * s1.c, lam: l, txt: `${lin([[l * s1.a, vx], [l * s1.b, vy]])} = ${num(l * s1.c)}` }; };
    const CASOS = {
      basico: [() => [S.X(), S.SQ()], () => [S.X(), S.Y()], () => [S.X(), S.X()], () => [S.X(), S.XY()], () => [S.X(), S.POS()]],
      paes: [() => { const a = S.XY(); return [a, otraXY(a)]; }, () => { const a = S.XY(); return [a, S.Y()]; }, () => [S.SQ(), S.POS()], () => [S.XY(), S.SQ()], () => [S.Y(), S.POS()]],
      dificil: [() => { const a = S.XY(); return [a, doble(a)]; }, () => [S.SQ(), S.XY()], () => [S.POS(), S.XY()], () => [S.SQ(), S.Y()]],
    };
    let [s1, s2] = t.elige(CASOS[nivel])();
    if (t.r() < 0.5) [s1, s2] = [s2, s1];
    if (s1.txt === s2.txt) throw OTRA;
    const solo = (s) => s.tipo === 'X';
    const tipos = [s1.tipo, s2.tipo].sort().join('+');
    const indep = s1.tipo === 'XY' && s2.tipo === 'XY' && s1.a * s2.b - s1.b * s2.a !== 0;
    const juntas = solo(s1) || solo(s2) || tipos === 'XY+Y' || indep || tipos === 'POS+SQ';
    const ok1 = solo(s1), ok2 = solo(s2);
    const correcta = ok1 && ok2 ? 3 : ok1 ? 0 : ok2 ? 1 : juntas ? 2 : 4;
    const porque = (s, i) => {
      if (s.tipo === 'X') return `(${i}) sola alcanza: ${s.txt} → ${vx} = ${num(x0)}.`;
      if (s.tipo === 'Y') return `(${i}) sola no alcanza: solo da ${vy} = ${num(y0)} y no dice nada de ${vx}.`;
      if (s.tipo === 'XY') return `(${i}) sola no alcanza: una ecuación con dos incógnitas tiene infinitas soluciones.`;
      if (s.tipo === 'SQ') return `(${i}) sola no alcanza: ${vx}² = ${x0 * x0} da ${vx} = ${Math.abs(x0)} o ${vx} = −${Math.abs(x0)}.`;
      return `(${i}) sola no alcanza: hay infinitos números ${s.s > 0 ? 'positivos' : 'negativos'}.`;
    };
    let jTxt;
    if (tipos === 'XY+Y') jTxt = `Juntas sí: con ${vy} = ${num(y0)} en la otra ecuación se despeja ${vx} = ${num(x0)}.`;
    else if (indep) jTxt = `Juntas sí: son dos ecuaciones independientes (un sistema con solución única: ${vx} = ${num(x0)}, ${vy} = ${num(y0)}).`;
    else if (tipos === 'POS+SQ') jTxt = `Juntas sí: de ${vx} = ±${Math.abs(x0)}, solo ${vx} = ${num(x0)} cumple la otra condición.`;
    else if (tipos === 'XY+XY') jTxt = `Juntas tampoco: una ecuación es la otra multiplicada por un número. Es la misma información, así que sigue habiendo infinitas soluciones.`;
    else if (tipos === 'SQ+XY') jTxt = `Juntas tampoco: ${vx} puede ser ${Math.abs(x0)} o −${Math.abs(x0)}, y para cada uno hay un ${vy} que cumple la ecuación.`;
    else if (tipos === 'POS+XY') jTxt = `Juntas tampoco: hay infinitos pares con ${vx} ${x0 > 0 ? 'positivo' : 'negativo'} que cumplen la ecuación.`;
    else if (tipos === 'SQ+Y' || tipos === 'POS+Y') jTxt = `Juntas tampoco: la que habla de ${vy} no ayuda a decidir el valor de ${vx}.`;
    else jTxt = 'Juntas sí (basta una de ellas).';
    const r1 = porque(s1, 1), r2 = porque(s2, 2);
    const tr = (L) => {
      if (L === 0) return ok1 ? `Ojo: ${r2.replace('sola alcanza', 'sola también alcanza')}` : r1;
      if (L === 1) return ok2 ? `Ojo: ${r1.replace('sola alcanza', 'sola también alcanza')}` : r2;
      if (L === 2) return ok1 ? `No hace falta juntarlas: ${r1}` : ok2 ? `No hace falta juntarlas: ${r2}` : jTxt;
      if (L === 3) return !ok1 ? r1 : r2;
      return ok1 ? r1 : ok2 ? r2 : jTxt;
    };
    const opciones = SD_OPS.map((txt, L) => ({ texto: txt, trampa: L === correcta ? '' : tr(L) }));
    return {
      enun: `Se puede determinar el valor de ${vx} si:<br>(1) ${s1.txt}<br>(2) ${s2.txt}`,
      fijas: opciones, correcta,
      exp: `${r1} ${r2} ${ok1 || ok2 ? '' : jTxt} Respuesta: ${SD_OPS[correcta]}.`.replace('  ', ' '),
      p: { x0, y0, st: [s1, s2].map((s) => ({ ...s, txt: undefined })) },
    };
  });

  // =====================================================================
  // armado de la pregunta
  // =====================================================================
  const limpio = (s) => String(s).replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
  const MALO = /NaN|undefined|Infinity|\[object|−0(?![,\d])|(^|[\s(=·,\[\/])-\d/;
  let ESTRICTO = false;
  function armar(o, t) {
    if (o.fijas) return { opciones: o.fijas, correcta: o.correcta };
    const okT = limpio(o.ok);
    const vistos = new Set([okT]);
    const malas = [];
    for (const [texto, trampa] of (o.todas ? o.malas : t.baraja(o.malas))) {
      const k = limpio(texto);
      if (!trampa || vistos.has(k)) continue;
      vistos.add(k); malas.push({ texto, trampa });
      if (malas.length === 3) break;
    }
    if (malas.length < 3) return null;
    const pos = t.ent(0, 3);
    const opciones = malas.slice();
    opciones.splice(pos, 0, { texto: o.ok, trampa: '' });
    return { opciones, correcta: pos };
  }
  const PRUEBA = (tema) => (tema.startsWith('m2.') ? 'M2' : tema.startsWith('m1.') ? 'M1' : 'CIE');
  function crear(f, nivel, seed) {
    if (typeof f === 'string') f = FAM.find((x) => x.id === f);
    for (let intento = 0; intento < 400; intento++) {
      const s = (seed + intento * 7919) >>> 0;
      const t = azar(rng(s));
      let o;
      try { o = f.gen(t, nivel); } catch (e) { if (e === OTRA) continue; throw e; }
      const q = armar(o, t);
      if (!q) continue;
      const todo = [o.enun, o.exp, ...q.opciones.map((x) => x.texto + ' ' + x.trampa)].join(' ');
      if (MALO.test(todo)) { if (ESTRICTO) throw new Error(`${f.id}: texto con valor inválido: ${todo.match(MALO)[0]} en ${todo.slice(0, 200)}`); continue; }
      return { id: `g.${f.id}.${nivel}.${s}`, prueba: PRUEBA(f.tema), tema: f.tema, nivel, enunciado: o.enun, opciones: q.opciones, correcta: q.correcta, explicacion: o.exp, fam: f.id, p: o.p };
    }
    throw new Error('no se pudo generar ' + f.id);
  }
  const familias = (tema, nivel) => FAM.filter((f) => f.tema === tema && (!nivel || f.niveles.includes(nivel)));
  const temas = () => [...new Set(FAM.map((f) => f.tema))];
  // Rota las familias del tema para que no se repita el mismo tipo seguido.
  const colas = {};
  const recientes = [];
  function nuevo(tema, nivel, semilla) {
    const fs = familias(tema, nivel);
    if (!fs.length) return null;
    const k = tema + '|' + nivel;
    if (!colas[k] || !colas[k].length) colas[k] = azar(Math.random).baraja(fs.map((f) => f.id));
    const id = colas[k].shift();
    if (semilla !== undefined) return crear(id, nivel, semilla);
    let q;
    for (let i = 0; i < 12; i++) { // evita repetir un enunciado de las últimas 40 preguntas
      q = crear(id, nivel, Math.floor(Math.random() * 2 ** 31));
      if (!recientes.includes(limpio(q.enunciado))) break;
    }
    recientes.push(limpio(q.enunciado)); if (recientes.length > 40) recientes.shift();
    return q;
  }
  return { FAM, familias, temas, crear, nuevo, estricto: (v) => { ESTRICTO = v; } };
})();
if (typeof module !== 'undefined') module.exports = GEN;
// == fin paes27-gen v1 ==
