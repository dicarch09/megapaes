#!/usr/bin/env python3
"""Copia tools/core.js y tools/core.css dentro de cada HTML, entre sus marcadores.

Uso: python3 tools/sync_core.py          (sincroniza)
     python3 tools/sync_core.py --check  (falla si algún HTML está desactualizado)
"""
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
BLOQUES = [
    (RAIZ / "tools" / "core.js", r"// == paes27-core v\d+ ==", r"// == fin paes27-core v\d+ =="),
    (RAIZ / "tools" / "core.css", r"/\* == paes27-css v\d+ == \*/", r"/\* == fin paes27-css v\d+ == \*/"),
]
# Bloques opcionales: solo se sincronizan en las páginas que tienen sus marcadores.
OPCIONALES = [
    (RAIZ / "tools" / "lecciones.js", r"// == paes27-lecciones v\d+ ==", r"// == fin paes27-lecciones v\d+ =="),
]


def main() -> int:
    check = "--check" in sys.argv
    malos = []
    for html in sorted(RAIZ.glob("*.html")):
        txt = html.read_text(encoding="utf-8")
        nuevo = txt
        for fuente, ini, fin in BLOQUES:
            bloque = fuente.read_text(encoding="utf-8").strip()
            pat = re.compile(ini + r".*?" + fin, re.S)
            if not pat.search(nuevo):
                malos.append(f"{html.name}: falta el bloque {fuente.name}")
                continue
            nuevo = pat.sub(lambda _m: bloque, nuevo, count=1)
        for fuente, ini, fin in OPCIONALES:
            pat = re.compile(ini + r".*?" + fin, re.S)
            if pat.search(nuevo):
                bloque = fuente.read_text(encoding="utf-8").strip()
                nuevo = pat.sub(lambda _m: bloque, nuevo, count=1)
        # bancos JSON: <script type="application/json" id="banco-X"> <- tools/banco_X.json
        def _banco(m):
            fuente = RAIZ / "tools" / ("banco_" + m.group(2) + ".json")
            if not fuente.exists():
                return m.group(0)
            return m.group(1) + "\n" + fuente.read_text(encoding="utf-8").strip() + "\n" + m.group(3)
        nuevo = re.sub(r'(<script type="application/json" id="banco-([a-z0-9]+)">)(?:.*?)(</script>)', _banco, nuevo, flags=re.S)
        if nuevo != txt:
            if check:
                malos.append(f"{html.name}: bloque compartido desactualizado")
            else:
                html.write_text(nuevo, encoding="utf-8")
                print(f"sincronizado {html.name}")
    for m in malos:
        print("ERROR", m)
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main())
