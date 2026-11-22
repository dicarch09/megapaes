#!/usr/bin/env python3
"""Verifica los bancos de preguntas incrustados en los HTML.

1. Estructura: campos del contrato, tema válido, cantidad de alternativas por prueba,
   trampa en cada incorrecta, ids únicos.
2. Cálculo: cada pregunta numérica tiene aquí su propio cálculo independiente; el script
   evalúa TODAS las alternativas y exige que exactamente una coincida y que sea `correcta`.
3. Cada pregunta debe estar en CHECKS (calculada) o en CONCEPTUALES (con motivo).
   Si falta en ambos, falla: así ninguna pregunta nueva se cuela sin verificar.

Uso: python3 tools/verificar.py    (sale con código 1 si algo falla)
"""
import json
import math
import pathlib
import re
import statistics
import sys
from fractions import Fraction
from itertools import product

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SD_OPCIONES = ["(1) por sí sola", "(2) por sí sola", "Ambas juntas, (1) y (2)",
               "Cada una por sí sola, (1) ó (2)", "Se requiere información adicional"]


class Falla(Exception):
    pass


# ---------------------------------------------------------------- lectura
def temas_validos():
    core = (RAIZ / "tools" / "core.js").read_text(encoding="utf-8")
    return set(re.findall(r"^\s*\['([a-z0-9.\-]+)', '(?:M2|M1|CIE|LEN)'", core, re.M))


def preguntas():
    out = []
    bancos_vistos = set()  # un mismo banco puede ir incrustado en varias páginas
    for html in sorted(RAIZ.glob("*.html")):
        txt = html.read_text(encoding="utf-8")
        for m in re.finditer(r'<script type="application/json" id="(banco-[a-z0-9]+)">(.*?)</script>', txt, re.S):
            if m.group(1) in bancos_vistos:
                continue
            bancos_vistos.add(m.group(1))
            datos = json.loads(m.group(2))

            def walk(x):
                if isinstance(x, dict):
                    if "id" in x and "opciones" in x:
                        out.append((html.name, x))
                    else:
                        for v in x.values():
                            walk(v)
                elif isinstance(x, list):
                    for v in x:
                        walk(v)
            walk(datos)
    return out


# ---------------------------------------------------------------- evaluación de alternativas
SUPER = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")
UNIDADES = r"(cm²|cm³|cm|m/s²|m/s|km/h|km|N/m|kWh|kg|Hz|UF|mA|m|N|A|Ω|V|W|J|s|años|horas|%|°)"


def a_python(t):
    t = re.sub(r"<sup>(.*?)</sup>", lambda m: "^(" + m.group(1) + ")", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = t.replace("−", "-").replace("·", "*").replace("×", "*").replace("$", "").strip()
    t = re.sub(r"\s*" + UNIDADES + r"\s*$", "", t)
    t = re.sub(r"[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+", lambda m: "^(" + m.group(0).translate(SUPER) + ")", t)
    t = re.sub(r"(?<=\d)\.(?=\d{3}\b)", "", t)          # 1.040.400 -> 1040400
    t = re.sub(r"(?<=\d),(?=\d)", ".", t)               # 1,08 -> 1.08
    t = t.replace("√(", "sqrt(")
    t = re.sub(r"√(\d+(?:\.\d+)?)", r"sqrt(\1)", t)
    t = t.replace("π", "pi").replace("sen", "sin")
    t = re.sub(r"(\d|\))\s*(?=(sqrt|pi|sin|cos|tan|log|[a-z(]))", r"\1*", t)
    return t.replace("^", "**")


ENTORNO = {"sqrt": math.sqrt, "pi": math.pi, "sin": math.sin, "cos": math.cos, "tan": math.tan,
           "log": math.log10, "abs": abs}


def valor(texto, env=None):
    try:
        return eval(a_python(texto), {"__builtins__": {}}, {**ENTORNO, **(env or {})})  # noqa: S307 (texto propio)
    except Exception:
        return None


def cerca(a, b, tol=1e-6):
    if a is None:
        return False
    if isinstance(b, (tuple, list)):
        return isinstance(a, (tuple, list)) and len(a) == len(b) and all(cerca(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, (tuple, list)):
        return False
    try:
        a, b = float(a), float(b)
        if abs(b) < 1e-12:
            return abs(a) < 1e-9
        return abs(a - b) <= tol * max(abs(a), abs(b))  # tolerancia relativa (sirve para 10⁻⁷ y para 10⁸)
    except (TypeError, ValueError):
        return False


def unico(q, pred, que):
    hits = [i for i, o in enumerate(q["opciones"]) if pred(o["texto"])]
    if len(hits) != 1:
        raise Falla(f"{len(hits)} alternativas coinciden con {que}")
    return hits[0]


def idx_num(q, objetivo, env=None, tol=1e-6):
    return unico(q, lambda t: cerca(valor(t, env), objetivo, tol), repr(objetivo))


def idx_func(q, f, prefijo=r"^\s*(y|f\(x\))\s*=\s*", puntos=(-1.3, 0.4, 1.7, 2.9)):
    def igual(t):
        t2 = re.sub(prefijo, "", re.sub(r"<[^>]+>", "", t))
        return all(cerca(valor(t2, {"x": x}), f(x), 1e-9) for x in puntos)
    return unico(q, igual, "la función esperada")


def idx_texto(q, esperado):
    return unico(q, lambda t: re.sub(r"<[^>]+>", "", t).strip() == esperado, repr(esperado))


def idx_partes(q, objetivo, sep):
    """Alternativas con varias magnitudes separadas por `sep` (p. ej. '1,4 m/s y 0,2 m/s')."""
    def ok(t):
        partes = [p for p in re.split(sep, re.sub(r"<[^>]+>", "", t)) if p.strip()]
        return cerca(tuple(valor(p) for p in partes), objetivo)
    return unico(q, ok, repr(objetivo))


def idx_sd(q, s1, s2, juntas):
    """Suficiencia de datos: s1, s2 = cada afirmación sola basta; juntas = ambas juntas bastan."""
    if s1 and s2:
        k = 3
    elif s1:
        k = 0
    elif s2:
        k = 1
    elif juntas:
        k = 2
    else:
        k = 4
    return k


def determina(soluciones, f):
    """¿Todas las soluciones dan el mismo valor de f? (soluciones = lista de tuplas que cumplen las condiciones)."""
    vals = {round(f(*s), 9) for s in soluciones}
    if not vals:
        raise Falla("sin soluciones de muestra")
    return len(vals) == 1


def rejilla(cond, rango=None):
    rango = rango or [Fraction(n, 2) for n in range(-40, 41)]
    return [(x, y) for x, y in product(rango, rango) if cond(x, y)]


# ---------------------------------------------------------------- cálculos por pregunta
CHECKS = {}


def chk(*ids):
    def deco(fn):
        for i in ids:
            CHECKS[i] = fn
        return fn
    return deco


# ===== Diagnóstico M2
chk("d-m2-01")(lambda q: idx_num(q, 2))                                  # ax - y = 5 -> y = ax - 5, paralela a pendiente 2
chk("d-m2-02")(lambda q: idx_num(q, Fraction(3 * 2, 6)))                 # k/3 = 2/6 = 4/12
chk("d-m2-03")(lambda q: idx_num(q, math.log2(32) - math.log(1 / 9, 3)))
chk("d-m2-04")(lambda q: idx_num(q, 2 * 0.3 + 0.48))
chk("d-m2-05")(lambda q: idx_num(q, Fraction(12, 22)))
chk("d-m2-06")(lambda q: idx_num(q, Fraction(math.comb(4, 2), 2 ** 4)))
chk("d-m2-07")(lambda q: idx_num(q, math.perm(6, 3)))
chk("d-m2-08")(lambda q: idx_num(q, Fraction(6, int(math.isqrt(10 ** 2 - 6 ** 2)))))


@chk("d-m2-09")
def _(q):
    A, B = 3, 2
    return unico(q, lambda t: (m := re.match(r"Amplitud (\S+), período (\S+)", t)) is not None
                 and cerca(valor(m.group(1)), abs(A)) and cerca(valor(m.group(2)), 2 * math.pi / B), "amp 3, período π")


chk("d-m2-10")(lambda q: idx_num(q, statistics.pvariance([2, 4, 6, 8, 10])))


@chk("d-m2-11")
def _(q):
    sol1 = rejilla(lambda x, y: x - y == 4)
    sol2 = rejilla(lambda x, y: 2 * x + 2 * y == 18)
    ambas = rejilla(lambda x, y: x - y == 4 and 2 * x + 2 * y == 18)
    s = lambda x, y: x + y  # noqa: E731
    return idx_sd(q, determina(sol1, s), determina(sol2, s), determina(ambas, s))


chk("d-m2-12")(lambda q: idx_num(q, 110 / 2))
chk("d-m2-13")(lambda q: idx_num(q, (-2 * 3, -2 * -1)))
chk("d-m2-14")(lambda q: idx_num(q, 1_000_000 * 1.02 ** 2))


@chk("d-m2-15")
def _(q):
    r = (36 * 3 / 4) ** (1 / 3)
    return idx_num(q, 4 * math.pi * r ** 2)


# ===== Diagnóstico Ciencias
chk("d-cie-01")(lambda q: idx_partes(q, ((30 + 40) / 50, abs(30 - 40) / 50), r" y "))
chk("d-cie-02")(lambda q: idx_num(q, 0.5 * 2 * 5 ** 2))
chk("d-cie-03")(lambda q: idx_num(q, (20 - 8) / 4))
chk("d-cie-04")(lambda q: idx_num(q, 200 * 0.05))
chk("d-cie-05")(lambda q: idx_num(q, 3e8 / 6e14))


@chk("d-cie-06")
def _(q):
    f, do = 10, 30
    di = 1 / (1 / f - 1 / do)
    m = -di / do
    tipo = "Real" if di > 0 else "Virtual"
    orient = "invertida" if m < 0 else "derecha"
    tam = "de menor tamaño" if abs(m) < 1 - 1e-9 else "de mayor tamaño" if abs(m) > 1 + 1e-9 else "del mismo tamaño"
    return idx_texto(q, f"{tipo}, {orient} y {tam}")


chk("d-cie-07")(lambda q: idx_num(q, 12 / (1 / (1 / 6 + 1 / 3))))
chk("d-cie-08")(lambda q: idx_num(q, 2 * (15 / 60) * 30 * 200))


@chk("d-cie-10")
def _(q):
    espectro = ["Ondas de radio", "Microondas", "Infrarrojo", "Luz roja", "Luz verde", "Luz violeta",
                "Ultravioleta", "Rayos X", "Rayos gamma"]
    presentes = [o["texto"] for o in q["opciones"]]
    for t in presentes:
        if t not in espectro:
            raise Falla(f"onda desconocida {t}")
    return idx_texto(q, max(presentes, key=espectro.index))




chk("d-cie-14")(lambda q: idx_num(q, 35 - 17))
chk("d-cie-15")(lambda q: idx_num(q, 3 * 2 / 1))

# ===== Diagnóstico M1
chk("d-m1-01")(lambda q: idx_num(q, (-3) ** 2 - 2 * (-4) + 6 / (-2)))


@chk("d-m1-02")
def _(q):
    cambio = round((1.2 * 0.8 - 1) * 100, 9)
    esperado = "Es igual" if cambio == 0 else f"Es {abs(cambio):g} % {'menor' if cambio < 0 else 'mayor'}"
    return idx_texto(q, esperado)


chk("d-m1-03")(lambda q: idx_num(q, math.sqrt(50) - math.sqrt(18)))
chk("d-m1-04")(lambda q: idx_func(q, lambda x: (2 * x - 3) ** 2, prefijo=r"^$"))
chk("d-m1-05")(lambda q: idx_num(q, (4 + 6) / (3 - 1)))
chk("d-m1-06")(lambda q: idx_num(q, (3, 3 ** 2 - 6 * 3 + 5)))
chk("d-m1-07")(lambda q: idx_num(q, math.pi * 3 ** 2 * 10))
chk("d-m1-08")(lambda q: idx_num(q, 15 * 4 / 3))
chk("d-m1-09")(lambda q: idx_num(q, statistics.median([5.0, 6.0, 4.0, 6.0, 7.0])))
chk("d-m1-10")(lambda q: idx_num(q, Fraction(sum(a + b == 7 for a in range(1, 7) for b in range(1, 7)), 36)))

CONCEPTUALES = {
    "d-cie-09": "refracción: cualitativa",
    "d-cie-11": "tectónica: cualitativa",
    "d-cie-12": "sinapsis: cualitativa",
    "d-cie-13": "mitosis: etapas (cualitativa)",
    **{f"d-len-0{i}": "comprensión lectora" for i in range(1, 7)},
}

# Las lecciones (m2.html) registran sus cálculos en este archivo aparte, para no mezclar.
for EXTRA in sorted((RAIZ / "tools").glob("verificar_*.py")):
    exec(compile(EXTRA.read_text(encoding="utf-8"), str(EXTRA), "exec"))  # noqa: S102 (archivo propio)


# ---------------------------------------------------------------- estructura
def revisar_estructura(archivo, q, temas):
    errores = []
    req = ["id", "prueba", "eje", "tema", "nivel", "enunciado", "opciones", "correcta", "explicacion"]
    for k in req:
        if k not in q:
            errores.append(f"falta '{k}'")
    if errores:
        return errores
    if q["tema"] not in temas:
        errores.append(f"tema desconocido {q['tema']}")
    if q["nivel"] not in ("basico", "paes", "dificil"):
        errores.append(f"nivel inválido {q['nivel']}")
    n = len(q["opciones"])
    if q["tema"] == "m2.sd":
        if [o["texto"] for o in q["opciones"]] != SD_OPCIONES:
            errores.append("suficiencia de datos: las 5 alternativas deben ser las fijas, en orden")
    elif q["prueba"] in ("M1", "M2", "LEN") and n != 4:
        errores.append(f"{q['prueba']} debe tener 4 alternativas (tiene {n})")
    elif q["prueba"] == "CIE" and n not in (4, 5):
        errores.append(f"Ciencias debe tener 4 o 5 alternativas (tiene {n})")
    if not (0 <= q["correcta"] < n):
        errores.append("correcta fuera de rango")
    textos = [o["texto"] for o in q["opciones"]]
    if len(set(textos)) != len(textos):
        errores.append("alternativas repetidas")
    for i, o in enumerate(q["opciones"]):
        if i == q["correcta"] and o.get("trampa"):
            errores.append("la correcta no debe tener trampa")
        if i != q["correcta"] and not o.get("trampa", "").strip():
            errores.append(f"alternativa {i} sin trampa")
    if not q["explicacion"].strip():
        errores.append("sin explicación")
    return errores


def main():
    temas = temas_validos()
    qs = preguntas()
    fallas = 0
    vistos = set()
    calculadas = conceptuales = 0
    for archivo, q in qs:
        qid = q.get("id", "?")
        errs = revisar_estructura(archivo, q, temas)
        if qid in vistos:
            errs.append("id repetido")
        vistos.add(qid)
        if qid in CHECKS:
            try:
                esperado = CHECKS[qid](q)
                if esperado != q["correcta"]:
                    errs.append(f"el cálculo da la alternativa {esperado} ({q['opciones'][esperado]['texto']!r}) "
                                f"pero correcta = {q['correcta']}")
                calculadas += 1
            except Falla as e:
                errs.append(f"cálculo: {e}")
        elif qid in CONCEPTUALES:
            conceptuales += 1
        else:
            errs.append("sin cálculo ni motivo en CONCEPTUALES")
        for e in errs:
            print(f"FALLA {archivo} {qid}: {e}")
        fallas += bool(errs)
    sobrantes = (set(CHECKS) | set(CONCEPTUALES)) - vistos
    for s in sorted(sobrantes):
        print(f"AVISO cálculo registrado para una pregunta que no existe: {s}")
    print(f"{len(qs)} preguntas · {calculadas} recalculadas · {conceptuales} conceptuales · {fallas} con fallas")
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main())
