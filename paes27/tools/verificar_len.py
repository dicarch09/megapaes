# Competencia Lectora (lenguaje.html). Lo carga tools/verificar.py (comparte chk, idx_num, CONCEPTUALES, POST…).
# ruff: noqa: F821
import importlib.util as _ilu
import json as _json

_spec = _ilu.spec_from_file_location("lenguaje_banco", RAIZ / "tools" / "lenguaje_banco.py")
_lb = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_lb)

# El subsidio se abona de abril a diciembre (ambos incluidos): 9 abonos de $15.000
chk("len-t4-03")(lambda q: idx_num(q, 15000 * len(range(4, 12 + 1))))

for _q in _lb.PREGUNTAS:
    if _q["id"] not in CHECKS:
        CONCEPTUALES[_q["id"]] = "comprensión lectora (evidencia marcada en el texto)"


def _len_forma():
    """Evidencia exacta en el texto, tarea del temario coherente con la habilidad y tipo de trampa válido."""
    banco = _json.loads((RAIZ / "tools" / "banco_len.json").read_text(encoding="utf-8"))
    diag = _json.loads((RAIZ / "tools" / "banco_diag.json").read_text(encoding="utf-8"))["LEN"]
    textos = banco["textos"] + [{"id": "diag", "titulo": diag["titulo"], "html": diag["texto"]}]
    errs = _lb.revisar(banco["preguntas"] + diag["preguntas"], textos)
    if [p["id"] for p in banco["preguntas"]] != [p["id"] for p in _lb.PREGUNTAS]:
        errs.append("banco_len.json desactualizado: corre python3 tools/lenguaje_banco.py")
    return errs


POST.append(_len_forma)
