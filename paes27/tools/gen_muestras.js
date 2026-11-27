// Genera muestras de todas las familias de tools/generadores.js para que tools/verificar_gen.py las recalcule.
// Uso: node tools/gen_muestras.js [n_por_familia_y_nivel]   → JSON por stdout
const fs = require('fs');
const path = require('path');
const GEN = require('./generadores.js');

const N = Number(process.argv[2] || 200);
const core = fs.readFileSync(path.join(__dirname, 'core.js'), 'utf-8');
const EJE = {};
for (const m of core.matchAll(/\['([a-z0-9.\-]+)', '(M2|M1|CIE|LEN)', '([^']+)'/g)) EJE[m[1]] = m[3];

GEN.estricto(true);
const out = { familias: [], muestras: [], errores: [] };
for (const f of GEN.FAM) {
  out.familias.push({ id: f.id, tema: f.tema, niveles: f.niveles, nombre: f.nombre });
  for (const nivel of f.niveles) {
    for (let s = 1; s <= N; s++) {
      try {
        const q = GEN.crear(f, nivel, s * 104729 + nivel.length);
        q.eje = EJE[q.tema] || '';
        out.muestras.push(q);
      } catch (e) {
        out.errores.push(`${f.id}/${nivel}/${s}: ${e.message}`);
        break;
      }
    }
  }
}
process.stdout.write(JSON.stringify(out));
