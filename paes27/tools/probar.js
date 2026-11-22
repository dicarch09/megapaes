// Prueba de humo con Playwright: cero errores de consola, nada sale a internet,
// y los flujos principales funcionan. Uso (desde paes27/):
//   python3 -m http.server 8000 &   node tools/probar.js
const { chromium } = require('playwright');
const BASE = process.env.BASE || 'http://localhost:8000';
const SHOTS = process.env.SHOTS || '';

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1200, height: 900 } });
  const page = await ctx.newPage();
  const errores = [];
  const externos = [];
  page.on('console', (m) => { if (m.type() === 'error' || m.type() === 'warning') errores.push(`[${m.type()}] ${m.text()}`); });
  page.on('pageerror', (e) => errores.push(`[pageerror] ${e.message}`));
  page.on('request', (r) => { if (!r.url().startsWith(BASE) && !r.url().startsWith('blob:') && !r.url().startsWith('data:')) externos.push(r.url()); });
  page.on('dialog', (d) => d.accept());
  const tab = async (t) => { await page.click(`#tabs button[data-tab=${t}]`); await page.waitForSelector(`#p-${t}.on`); await page.waitForTimeout(50); };
  const ok = (c, msg) => { if (!c) { errores.push('[assert] ' + msg); console.log('  ✘', msg); } else console.log('  ✔', msg); };

  // ---------- HUB ----------
  console.log('index.html');
  await page.goto(BASE + '/index.html');
  await page.evaluate(() => localStorage.clear());
  await page.goto(BASE + '/index.html#hoy');
  ok(await page.locator('#p-hoy.on').isVisible(), 'pestaña Hoy visible');
  ok((await page.locator('.cuenta .ex').count()) === 4, 'cuenta regresiva de 4 pruebas');
  if (SHOTS) await page.screenshot({ path: SHOTS + '/hub-hoy.png', fullPage: true });

  // diagnóstico M2 completo con teclado: alterna correcta/incorrecta/no sé
  await tab('diag');
  await page.locator('.diag-card').first().locator('button', { hasText: 'Empezar' }).click();
  for (let i = 0; i < 15; i++) {
    await page.waitForSelector('.q-op');
    if (i % 3 === 2) await page.keyboard.press('n');
    else await page.keyboard.press(i % 3 === 0 ? '1' : '3');
    await page.waitForSelector('.q-fb:not([hidden])');
    if (i === 1 && SHOTS) await page.screenshot({ path: SHOTS + '/hub-diag.png' });
    await page.keyboard.press('Enter');
  }
  await page.waitForSelector('text=Pregunta por pregunta');
  const diag = await page.evaluate(() => JSON.parse(localStorage.getItem('paes27:diag')));
  ok(diag && diag.M2 && diag.M2.total === 15, 'diagnóstico M2 guardado con 15 respuestas');
  ok(!diag.enCurso, 'sin diagnóstico en curso al terminar');
  const dom = await page.evaluate(() => JSON.parse(localStorage.getItem('paes27:dominio')));
  ok(dom && Object.keys(dom).length >= 10, 'dominio actualizado: ' + Object.keys(dom || {}).length + ' temas');
  const rep = await page.evaluate(() => JSON.parse(localStorage.getItem('paes27:repaso')));
  ok(rep && rep.length > 0, 'repaso programado: ' + (rep || []).length + ' ítems');
  if (SHOTS) await page.screenshot({ path: SHOTS + '/hub-resultado.png', fullPage: true });

  // diagnóstico de Lectora: pausar a la mitad y continuar
  await page.click('text=← Volver a diagnósticos');
  await page.locator('.diag-card').nth(3).locator('button', { hasText: 'Empezar' }).click();
  await page.waitForSelector('.len-texto');
  await page.keyboard.press('1'); await page.keyboard.press('Enter');
  await page.keyboard.press('2'); await page.keyboard.press('Enter');
  await page.click('text=Pausar y salir');
  await page.reload();
  await tab('diag');
  ok(await page.locator('text=En curso: vas en la 3/6').isVisible(), 'Lectora reanudable en la 3/6');
  await page.locator('.diag-card').nth(3).locator('button', { hasText: 'Continuar' }).click();
  for (let i = 2; i < 6; i++) { await page.waitForSelector('.q-op:not([disabled])'); await page.keyboard.press('1'); await page.keyboard.press('Enter'); }
  await page.waitForSelector('text=Pregunta por pregunta');
  const d2 = await page.evaluate(() => JSON.parse(localStorage.getItem('paes27:diag')));
  ok(d2.LEN && d2.LEN.total === 6, 'Lectora guardada con 6 respuestas');

  // ruta
  await tab('ruta');
  const nDias = await page.locator('#p-ruta .dia').count();
  ok(nDias === 11, `ruta con 8 días + 3 días de prueba (${nDias})`);
  const ruta = await page.evaluate(() => JSON.parse(localStorage.getItem('paes27:ruta')));
  const resumen = Object.entries(ruta.dias).map(([f, bs]) => f.slice(8) + ':' + bs.map((b) => (b.prueba || '') + (b.tipo === 'flex' ? '' : '/' + b.tipo)).join(','));
  console.log('   ', resumen.join('\n    '));
  await page.selectOption('#selN', '8');
  const ruta8 = await page.evaluate(() => JSON.parse(localStorage.getItem('paes27:ruta')));
  ok(ruta8.N === 8, 'cambiar a 8 bloques recalcula');
  const chk = page.locator('#p-ruta .dia.hoy .bloque input:not([disabled])').first();
  if (await chk.count()) { await chk.check(); const r2 = await page.evaluate(() => JSON.parse(localStorage.getItem('paes27:ruta'))); ok(Object.values(r2.dias).flat().some((b) => b.hecho), 'marcar bloque como hecho'); }
  if (SHOTS) await page.screenshot({ path: SHOTS + '/hub-ruta.png', fullPage: true });

  // dominio y repaso
  await tab('dominio');
  ok((await page.locator('#p-dominio .dom-row').count()) > 40, 'panel de dominio con todos los temas');
  // forzar un repaso vencido para hoy y repasar
  await page.evaluate(() => { const r = JSON.parse(localStorage.getItem('paes27:repaso')); r.forEach((x) => { x.due = '2026-01-01'; }); localStorage.setItem('paes27:repaso', JSON.stringify(r)); });
  await tab('repaso');
  const btnRe = page.locator('#p-repaso button', { hasText: 'Rehacer' }).first();
  ok(await btnRe.count() > 0, 'repaso con preguntas del diagnóstico');
  await btnRe.click();
  await page.waitForSelector('.q-op');
  await page.keyboard.press('1');
  await page.waitForSelector('.q-fb:not([hidden])');
  await page.click('#p-repaso >> text=← Volver');

  // exportar / importar
  await tab('progreso');
  const [dl] = await Promise.all([page.waitForEvent('download'), page.click('button:has-text("Descargar respaldo")')]);
  const ruta_dl = await dl.path();
  const json = JSON.parse(require('fs').readFileSync(ruta_dl, 'utf8'));
  ok(json.app === 'paes27' && json.datos.diag.M2, 'respaldo exportado');
  await page.click('button:has-text("Borrar todo mi progreso")');
  ok((await page.evaluate(() => localStorage.getItem('paes27:diag'))) === null, 'borrar todo');
  await tab('progreso');
  await page.fill('#p-progreso textarea', JSON.stringify(json));
  await page.click('button:has-text("Importar texto")');
  const d3 = await page.evaluate(() => JSON.parse(localStorage.getItem('paes27:diag')));
  ok(d3 && d3.M2 && d3.M2.total === 15, 'respaldo importado');
  for (const t of ['hoy', 'ensayos', 'fichas']) { await tab(t); }

  // móvil: sin scroll horizontal
  await page.setViewportSize({ width: 380, height: 800 });
  for (const t of ['hoy', 'ruta', 'dominio', 'diag']) {
    await tab(t);
    const sw = await page.evaluate(() => document.documentElement.scrollWidth);
    ok(sw <= 380, `sin scroll horizontal en ${t} (${sw}px)`);
  }

  // ---------- M2 (si existe) ----------
  const r = await page.request.get(BASE + '/m2.html');
  if (r.ok()) {
    console.log('m2.html');
    await page.setViewportSize({ width: 1200, height: 900 });
    await page.goto(BASE + '/m2.html');
    await page.waitForTimeout(600);
    const lecciones = await page.locator('section.leccion').count();
    ok(lecciones >= 7, `lecciones en m2.html: ${lecciones}`);
    // cada lección: abrir, mover sliders, practicar los 3 niveles
    const ids = await page.locator('section.leccion').evaluateAll((ls) => ls.map((l) => l.id));
    for (const id of ids) {
      await page.goto(BASE + '/m2.html#' + id);
      await page.waitForTimeout(400);
      const sec = page.locator(`section.leccion[id="${id}"]`);
      ok(await sec.isVisible(), `lección ${id} visible por enlace directo`);
      const sliders = sec.locator('input[type=range]');
      const selects = await sec.locator('select').count();
      const n = await sliders.count();
      for (let i = 0; i < n; i++) {
        const s = sliders.nth(i);
        if (!(await s.isVisible())) continue;
        await s.focus(); await page.keyboard.press('ArrowRight'); await page.keyboard.press('ArrowRight'); await page.keyboard.press('End'); await page.keyboard.press('Home');
      }
      ok(n + selects >= 2, `${id}: ${n} sliders, ${selects} selectores`);
      const pasos = sec.locator('button', { hasText: 'Siguiente paso' });
      while (await pasos.isVisible()) await pasos.click();
      for (const nivel of ['Básico', 'PAES', 'Difícil']) {
        await sec.locator('.niveles button', { hasText: nivel }).click();
        let vueltas = 0;
        while (vueltas++ < 10) {
          const op = sec.locator('.q-op:not([disabled])').first();
          if (!(await op.count())) break;
          await op.click();
          const sig = sec.locator('.q-acc .btn:not([hidden])').last();
          if (await sig.isVisible()) await sig.click(); else break;
        }
        ok(await sec.locator('.resumen-nivel').isVisible(), `${id}: nivel ${nivel} completo`);
      }
      if (SHOTS) await page.screenshot({ path: `${SHOTS}/m2-${id}.png`, fullPage: false });
    }
    // ensayo corto: responder con teclado, recargar a la mitad, entregar
    await page.goto(BASE + '/m2.html#ensayo');
    await page.click('#p-ensayo button:has-text("Corto")');
    await page.waitForSelector('#ens-reloj');
    for (let i = 0; i < 5; i++) { await page.keyboard.press(String((i % 4) + 1)); await page.keyboard.press('Enter'); }
    await page.reload(); await page.waitForSelector('#ens-reloj');
    const enCurso = await page.evaluate(() => JSON.parse(localStorage.getItem('paes27:ensayos')).find((e) => e.estado === 'en-curso'));
    ok(enCurso && Object.keys(enCurso.resp).length === 5 && enCurso.ids.length === 20, `ensayo sigue en curso tras recargar (${enCurso && Object.keys(enCurso.resp).length} respondidas)`);
    ok(new Set(enCurso.ids).size === 20, 'ensayo sin preguntas repetidas');
    await page.click('#p-ensayo button:has-text("Entregar")');
    await page.waitForSelector('text=correctas (');
    const ens = await page.evaluate(() => JSON.parse(localStorage.getItem('paes27:ensayos')));
    ok(ens.length === 1 && ens[0].estado === 'hecho' && ens[0].total === 20 && ens[0].omitidas === 15, 'ensayo entregado y guardado');
    if (SHOTS) await page.screenshot({ path: SHOTS + '/m2-ensayo-resultado.png' });
    await page.goto(BASE + '/index.html#ensayos'); await page.waitForTimeout(300);
    ok(await page.locator('#p-ensayos >> text=Historial').isVisible(), 'el hub muestra el historial de ensayos');
    await page.goto(BASE + '/m2.html');
    const dom2 = await page.evaluate(() => JSON.parse(localStorage.getItem('paes27:dominio')));
    ok(dom2 && dom2['m2.num.log-exp'] !== undefined, 'práctica de M2 actualiza el dominio compartido');
    await page.setViewportSize({ width: 380, height: 800 });
    const sw = await page.evaluate(() => document.documentElement.scrollWidth);
    ok(sw <= 380, `m2 sin scroll horizontal en móvil (${sw}px)`);
  }

  console.log('\nErrores/avisos de consola:', errores.length ? '\n' + errores.join('\n') : 0);
  console.log('Pedidos fuera de localhost:', externos.length ? '\n' + externos.join('\n') : 0);
  await browser.close();
  process.exit(errores.length || externos.length ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });
