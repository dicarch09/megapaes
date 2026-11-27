# Práctica infinita (practica.html): recalcula por su cuenta muestras de cada generador de tools/generadores.js.
# Lo carga tools/verificar.py (comparte idx_num, idx_texto, idx_func, unico, valor, cerca, idx_sd, POST…).
# Cada familia tiene aquí su propio cálculo, hecho desde los parámetros (p) de la muestra, y se exige
# que exactamente una alternativa coincida y que sea `correcta`.
# ruff: noqa: F821
import itertools as _it
import json as _json
import subprocess as _sp
from functools import lru_cache as _cache

GEN_MUESTRAS = 120  # por familia y nivel
GCHK = {}


def gchk(*ids):
    def deco(fn):
        for i in ids:
            GCHK[i] = fn
        return fn
    return deco


def _fr(v):
    return Fraction(v["p"], v["q"]) if isinstance(v, dict) else Fraction(v)


L2, L3 = math.log10(2), math.log10(3)


# ---------------- rectas y sistemas
@gchk("rec-pendiente")
def _(q, p):
    return idx_num(q, Fraction(p["y2"] - p["y1"], p["x2"] - p["x1"]))


@gchk("rec-general")
def _(q, p):
    return idx_num(q, Fraction(-p["a"], p["b"]) if p["pide"] == "pend" else Fraction(p["c"], p["b"]))


@gchk("rec-sistema")
def _(q, p):
    a1, b1, c1, a2, b2, c2 = (p[k] for k in ("a1", "b1", "c1", "a2", "b2", "c2"))
    det = a1 * b2 - a2 * b1
    x, y = Fraction(c1 * b2 - c2 * b1, det), Fraction(a1 * c2 - a2 * c1, det)
    return idx_num(q, {"x": x, "y": y, "x + y": x + y, "x − y": x - y, "x·y": x * y}[p["pide"]])


@gchk("rec-tipo")
def _(q, p):
    a1, b1, c1, a2, b2, c2 = (p[k] for k in ("a1", "b1", "c1", "a2", "b2", "c2"))
    if a1 * b2 - a2 * b1 != 0:
        esp = "Exactamente una solución"
    elif a1 * c2 - a2 * c1 == 0 and b1 * c2 - b2 * c1 == 0:
        esp = "Infinitas soluciones"
    else:
        esp = "Ninguna solución"
    return idx_texto(q, esp)


@gchk("rec-k")
def _(q, p):
    if p["tipo"] == "ninguna":
        k = Fraction(p["a2"] * p["b1"], p["b2"])          # k·b2 = a2·b1
        if p["c1"] * p["b2"] == p["c2"] * p["b1"]:
            raise Falla("con ese k las rectas coinciden")
        return idx_num(q, k)
    if p["b1"] * p["a2"] != p["b2"] * p["a1"]:
        raise Falla("las rectas no son paralelas")
    return idx_num(q, Fraction(p["c2"] * p["a1"], p["a2"]))   # (a1, b1, k) proporcional a (a2, b2, c2)


@gchk("rec-perpendicular")
def _(q, p):
    m = _fr(p["m"])
    if "tipo" in p:
        return idx_num(q, -1 / m if p["tipo"] == "perpendicular" else m)
    mp = -1 / m
    n = Fraction(p["q"]) - mp * p["p"]
    return idx_func(q, lambda x: float(mp) * x + float(n))


@gchk("rec-corte")
def _(q, p):
    x = Fraction(p["n2"] - p["n1"], p["m1"] - p["m2"])
    return idx_num(q, (x, p["m1"] * x + p["n1"]))


# ---------------- logaritmos
@gchk("log-valor")
def _(q, p):
    # se lee el argumento desde el enunciado que ve el estudiante
    m = re.search(r"¿Cuál es el valor de log(?:<sub>(\d+)</sub>)? (.+?)\?", q["enunciado"])
    base = int(m.group(1) or 10)
    arg = valor(m.group(2).strip("()"))
    if base != p["b"]:
        raise Falla("la base del enunciado no calza")
    return idx_num(q, math.log(arg, base))


@gchk("log-propiedades")
def _(q, p):
    N = Fraction(p["N"].replace(",", "."))
    return idx_num(q, math.log10(N), env={"a": L2, "b": L3})


@gchk("log-ecuacion-exp")
def _(q, p):
    A, B, s, t = p["A"], p["B"], p["s"], p["t"]

    def cumple(txt):
        v = valor(txt)
        if v is None or isinstance(v, (tuple, list)):
            return False
        izq = math.log(A) * (v + s)
        der = math.log(B) * (t if p["forma"] == "pot" else (v + t))
        return cerca(izq, der, 1e-9)
    return unico(q, cumple, "la solución de la ecuación")


@gchk("log-crecimiento")
def _(q, p):
    return idx_num(q, p["P0"] * p["f"] ** (p["T"] / p["h"]))


@gchk("log-tiempo")
def _(q, p):
    return idx_num(q, p["h"] * math.log(p["P"] / p["P0"], p["f"]))


@gchk("log-ecuacion")
def _(q, p):
    b, d, k = p["b"], p["d"], p["k"]
    disc = d * d + 4 * b ** k
    r = math.isqrt(disc)
    if r * r != disc:
        raise Falla("discriminante no es cuadrado")
    sols = [x for x in (Fraction(d + r, 2), Fraction(d - r, 2)) if x > 0 and x - d > 0]
    if len(sols) != 1:
        raise Falla(f"soluciones válidas: {sols}")
    return idx_num(q, sols[0])


# ---------------- probabilidad condicional
@gchk("cond-tabla")
def _(q, p):
    tab, i, j = p["tab"], p["i"], p["j"]
    R = sum(tab[i])
    C = sum(f[j] for f in tab)
    N = sum(map(sum, tab))
    n = tab[i][j]
    esp = {"col|fila": Fraction(n, R), "fila|col": Fraction(n, C), "fila|nocol": Fraction(R - n, N - C)}[p["tipo"]]
    return idx_num(q, esp)


@gchk("cond-arbol")
def _(q, p):
    pA, dA, dB = p["pA"], p["dA"], p["dB"]
    PA, DA, DB = Fraction(pA, 100), Fraction(dA, 100), Fraction(dB, 100)
    total = PA * DA + (1 - PA) * DB
    return idx_num(q, total * 100) if p["pide"] == "total" else idx_num(q, PA * DA / total)


@gchk("cond-urna")
def _(q, p):
    bolas = ["R"] * p["r"] + ["A"] * p["a"]
    pares = list(_it.permutations(range(len(bolas)), 2))
    col = [(bolas[i], bolas[j]) for i, j in pares]
    if p["pide"] == "segunda":
        prim = [c for c in col if c[0] == "R"]
        esp = Fraction(sum(c[1] == "R" for c in prim), len(prim))
    elif p["pide"] == "ambas":
        esp = Fraction(sum(c == ("R", "R") for c in col), len(col))
    else:
        esp = Fraction(sum(c[0] != c[1] for c in col), len(col))
    return idx_num(q, esp)


# ---------------- combinatoria (conteo por fuerza bruta, con caché)
@_cache(None)
def _filas(n):
    tot = jun = 0
    for pm in _it.permutations(range(n)):
        tot += 1
        jun += abs(pm.index(0) - pm.index(1)) == 1
    return tot, jun


@gchk("comb-fila")
def _(q, p):
    tot, jun = _filas(p["n"])
    return idx_num(q, {"todas": tot, "juntos": jun, "separados": tot - jun}[p["pide"]])


@gchk("comb-cargos")
def _(q, p):
    return idx_num(q, sum(1 for _ in _it.permutations(range(p["n"]), p["k"])))


@gchk("comb-comite")
def _(q, p):
    if p["pide"] == "comb":
        return idx_num(q, sum(1 for _ in _it.combinations(range(p["n"]), p["k"])))
    return idx_num(q, math.comb(p["m"], p["a"]) * math.comb(p["q"], p["b"]))


@_cache(None)
def _anagramas(w, X=None):
    pal = set(_it.permutations(w))
    return len(pal) if X is None else sum(1 for x in pal if x[0] == X)


@gchk("comb-anagramas")
def _(q, p):
    return idx_num(q, _anagramas(p["w"], p.get("X")))


@_cache(None)
def _numeros(d, k, pide):
    dig = range(1, d + 1)
    if pide == "repite":
        return d ** k
    todos = list(_it.permutations(dig, k))
    return len(todos) if pide == "distintas" else sum(1 for t in todos if t[-1] % 2 == 0)


@gchk("comb-numeros")
def _(q, p):
    return idx_num(q, _numeros(p["d"], p["k"], p["pide"]))


# ---------------- trigonometría
@gchk("trig-razon")
def _(q, p):
    AC, BC, AB = p["AC"], p["BC"], p["AB"]
    if AC * AC + BC * BC != AB * AB:
        raise Falla("no es triángulo rectángulo")
    op, ad = (BC, AC) if p["ang"] == "A" else (AC, BC)
    return idx_num(q, {"sen": Fraction(op, AB), "cos": Fraction(ad, AB), "tan": Fraction(op, ad)}[p["pide"]])


@gchk("trig-lado")
def _(q, p):
    th, L = math.radians(p["th"]), p["L"]
    if p["con"] == "hip":
        lados = {"hip": L, "op": L * math.sin(th), "ad": L * math.cos(th)}
    elif p["con"] == "op":
        lados = {"op": L, "hip": L / math.sin(th), "ad": L / math.tan(th)}
    else:
        lados = {"ad": L, "hip": L / math.cos(th), "op": L * math.tan(th)}
    return idx_num(q, lados[p["bus"]])


@gchk("trig-altura")
def _(q, p):
    if "d" in p:
        return idx_num(q, p["d"] * math.tan(math.radians(p["th"])))
    t1, t2 = math.radians(p["t1"]), math.radians(p["t2"])
    return idx_num(q, p["s"] / (1 / math.tan(t1) - 1 / math.tan(t2)))


@gchk("trig-dado-seno")
def _(q, p):
    op, ad, c = p["op"], p["ad"], p["c"]
    if op * op + ad * ad != c * c:
        raise Falla("no es trío pitagórico")
    return idx_num(q, {"sen": Fraction(op, c), "cos": Fraction(ad, c), "tan": Fraction(op, ad)}[p["pide"]])


@gchk("trigf-parametros")
def _(q, p):
    A, B, D = _fr(p["A"]), _fr(p["B"]), p["D"]
    if p["pide"] == "amp":
        return idx_num(q, abs(A))
    if p["pide"] == "per":
        return idx_num(q, 2 * math.pi / float(B))
    return idx_num(q, [D - abs(A), D + abs(A)])


@gchk("trigf-valor")
def _(q, p):
    f = math.sin if p["fn"] == "sen" else math.cos
    return idx_num(q, f(math.radians(p["g"])), tol=1e-9)


# ---------------- dispersión
@gchk("disp-rango")
def _(q, p):
    return idx_num(q, max(p["xs"]) - min(p["xs"]))


@gchk("disp-desviacion")
def _(q, p):
    return idx_num(q, statistics.pstdev(p["xs"]))


@gchk("disp-cambio")
def _(q, p):
    mu, sg, a, b = p["mu"], p["sg"], p["a"], p["b"]
    return idx_num(q, {"desv": abs(a) * sg, "media": a * mu + b, "var": (a * sg) ** 2}[p["pide"]])


# ---------------- binomial y normal
@gchk("bin-probabilidad")
def _(q, p):
    n, pr = p["n"], _fr(p["p"])
    pmf = [math.comb(n, k) * pr ** k * (1 - pr) ** (n - k) for k in range(n + 1)]
    return idx_num(q, pmf[p["k"]] if p["pide"] == "exacto" else sum(pmf[1:]))


@gchk("bin-esperanza")
def _(q, p):
    n, pr = p["n"], p["p"]
    return idx_num(q, n * pr if p["pide"] == "E" else n * pr * (1 - pr))


@gchk("normal")
def _(q, p):
    if p["pide"] == "z":
        return idx_num(q, (p["x"] - p["mu"]) / p["sg"])
    if p["pide"] == "cola":
        return idx_num(q, 1 - p["ph"])
    if p["pide"] == "centro":
        return idx_num(q, 2 * p["ph"] - 1)
    return idx_num(q, p["mu"] + p["z"] * p["sg"])


# ---------------- circunferencia
@gchk("circ-inscrito")
def _(q, p):
    v = p["v"]
    return idx_num(q, {"central": Fraction(p.get("c", 0), 2), "inscrito": 2 * p.get("i", 0),
                       "cuadri": 180 - p.get("a", 0), "arco": 2 * p.get("i", 0)}[v])


@gchk("circ-angulos-arcos")
def _(q, p):
    return idx_num(q, Fraction(p["a"] + p["b"], 2) if p["pide"] == "interior" else Fraction(p["a"] - p["b"], 2))


@gchk("circ-segmentos")
def _(q, p):
    if p["pide"] == "cuerdas":
        return idx_num(q, Fraction(p["a"] * p["b"], p["c"]))
    if p["pide"] == "tangente":
        return idx_num(q, math.sqrt(p["a"] * p["b"]))
    pd = Fraction(p["a"] * (p["a"] + p["e1"]), p["c"])
    return idx_num(q, pd - p["c"])


# ---------------- homotecia
@gchk("hom-punto")
def _(q, p):
    k, (ox, oy), (px, py) = _fr(p["k"]), p["O"], p["P"]
    return idx_num(q, (ox + k * (px - ox), oy + k * (py - oy)))


@gchk("hom-medidas")
def _(q, p):
    if p["pide"] == "razon":
        return idx_num(q, math.sqrt(float(_fr(p["A2"]) / p["A"])))
    k = _fr(p["k"])
    return idx_num(q, abs(k) * p["P"] if p["pide"] == "per" else k * k * p["A"])


@gchk("hom-razon")
def _(q, p):
    (ox, oy), (px, py) = p["O"], p["P"]
    pix, piy = _fr(p["Pi"][0]), _fr(p["Pi"][1])
    kx, ky = (pix - ox) / (px - ox), (piy - oy) / (py - oy)
    if kx != ky:
        raise Falla("P' no está en la recta OP")
    return idx_num(q, kx)


# ---------------- matemática financiera
@gchk("fin-compuesto")
def _(q, p):
    C, i, n = p["C"], p["i"], p["n"]
    M = C * Fraction(100 + i, 100) ** n
    return idx_num(q, M if p["pide"] == "M" else M - C)


@gchk("fin-simple")
def _(q, p):
    I = Fraction(p["C"] * p["i"] * p["m"], 100)
    return idx_num(q, I if p["pide"] == "I" else p["C"] + I)


@gchk("fin-credito")
def _(q, p):
    return idx_num(q, p["pie"] + p["n"] * p["q"] - p["M"])


@gchk("fin-afp")
def _(q, p):
    if p["pide"] == "afp":
        return idx_num(q, p["s"] * (10 + p["c"]) / 100)
    return idx_num(q, p["d"] * p["U"] * p["m"])


# ---------------- esfera
@gchk("esf-medidas")
def _(q, p):
    r = p["r"]
    return idx_num(q, 4 / 3 * math.pi * r ** 3 if p["pide"] == "V" else 4 * math.pi * r * r)


@gchk("esf-escala")
def _(q, p):
    return idx_num(q, p["k"] ** (3 if p["pide"] == "V" else 2))


@gchk("esf-fundir")
def _(q, p):
    return idx_num(q, (4 / 3 * math.pi * p["r"] ** 3) / (math.pi * p["R"] ** 2))


# ---------------- función potencia y reales
@gchk("pot-valor")
def _(q, p):
    return idx_num(q, p["a"] * _fr(p["x"]) ** p["n"])


@gchk("pot-parametro")
def _(q, p):
    if "q" in p:
        return idx_num(q, Fraction(p["q"], p["p"] ** p["n"]))
    f1, f2 = p["a"], p["a"] * 2 ** p["n"]
    return idx_num(q, math.log2(f2 / f1))


@gchk("real-raices")
def _(q, p):
    if "b" in p:
        a, c, d, b = p["a"], p["c"], p["d"], p["b"]
        return idx_num(q, math.sqrt(a * a * b) + math.sqrt(c * c * b) - math.sqrt(d * d * b))
    return idx_num(q, (math.sqrt(p["p"]) + p["sg"] * math.sqrt(p["q"])) ** 2)


@gchk("real-racionalizar")
def _(q, p):
    if "a" in p:
        return idx_num(q, p["a"] / math.sqrt(p["b"]))
    return idx_num(q, p["c"] / (math.sqrt(p["m"]) - math.sqrt(p["n"])))


@gchk("real-pot-fraccion")
def _(q, p):
    return idx_num(q, p["B"] ** (p["p"] / p["q"]))


# ---------------- M1 en versión difícil
@gchk("m1d-cuadratica")
def _(q, p):
    if "a" in p:
        a, b, c = p["a"], p["b"], p["c"]
        h = Fraction(-b, 2 * a)
        return idx_num(q, (h, a * h * h + b * h + c))
    if p["pide"] == "disc":
        return idx_num(q, Fraction(p["b"] ** 2, 4))
    s, pr = p["r1"] + p["r2"], p["r1"] * p["r2"]
    disc = s * s - 4 * pr
    esp = {Fraction(s - math.isqrt(disc), 2), Fraction(s + math.isqrt(disc), 2)}

    def es(t):
        partes = re.findall(r"x = (\S+)", re.sub(r"<[^>]+>", "", t))
        return {Fraction(valor(x)) for x in partes} == esp if partes else False
    return unico(q, es, f"las raíces {esp}")


@gchk("m1d-thales")
def _(q, p):
    if "d" in p:
        return idx_num(q, Fraction(p["d"] * (p["a"] + p["b"]), p["a"]))
    return idx_num(q, p["A"] * Fraction(p["m"], p["n"]) ** 2)


@gchk("m1d-cilindro")
def _(q, p):
    r, h = p["r"], p["h"]
    return idx_num(q, math.pi * r * r * h if p["pide"] == "V" else 2 * math.pi * r * h + 2 * math.pi * r * r)


# ---------------- suficiencia de datos: álgebra lineal exacta, independiente de las reglas del generador
def _rango(filas):
    m = [list(map(Fraction, f)) for f in filas]
    r = 0
    for c in range(2):
        piv = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c] / m[r][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return r


def _x_determinado(sts, x0):
    filas, sq, pos = [], None, None
    for s in sts:
        t = s["tipo"]
        if t == "X":
            filas.append((s["a"], 0, s["f"] - s["e"]))
        elif t == "Y":
            filas.append((0, s["b"], s["f"] - s["e"]))
        elif t == "XY":
            filas.append((s["a"], s["b"], s["c"]))
        elif t == "SQ":
            sq = s["v2"]
        elif t == "POS":
            pos = s["s"]
    A = [f[:2] for f in filas]
    if A and _rango(A + [(1, 0)]) == _rango(A):
        return True                              # e_x está en el espacio fila: x queda fijo
    if sq is None:
        return False                             # x libre en una recta o en todo el plano
    r = math.isqrt(sq)
    cands = {r, -r}
    if pos is not None:
        cands = {c for c in cands if c * pos > 0}

    def consistente(xv):
        ys = set()
        for a, b, c in filas:
            if b == 0:
                if a * xv != c:
                    return False
            else:
                ys.add(Fraction(c - a * xv, b))
        return len(ys) <= 1
    return len([c for c in cands if consistente(c)]) == 1


@gchk("sd-valor")
def _(q, p):
    s1, s2 = p["st"]
    return idx_sd(q, _x_determinado([s1], p["x0"]), _x_determinado([s2], p["x0"]), _x_determinado([s1, s2], p["x0"]))


# ---------------- revisión de todas las muestras
def _gen_revisar():
    errs = []
    try:
        out = _sp.run(["node", str(RAIZ / "tools" / "gen_muestras.js"), str(GEN_MUESTRAS)], capture_output=True, text=True, timeout=600, check=True).stdout
    except (OSError, _sp.SubprocessError) as e:
        return [f"no se pudo correr node tools/gen_muestras.js: {e}"]
    datos = _json.loads(out)
    errs += datos["errores"]
    temas = temas_validos()
    por_fam = {}
    for q in datos["muestras"]:
        f = q["fam"]
        e = revisar_estructura("practica", q, temas)
        if f not in GCHK:
            e.append("familia sin cálculo en verificar_gen.py")
        else:
            try:
                k = GCHK[f](q, q["p"])
                if k != q["correcta"]:
                    e.append(f"el cálculo da la alternativa {k} ({q['opciones'][k]['texto']!r}) pero correcta = {q['correcta']}")
            except Falla as x:
                e.append(f"cálculo: {x}")
        if e:
            por_fam.setdefault(f, []).append(f"{q['id']}: {'; '.join(e)} | {re.sub(r'<svg.*?</svg>', '[fig]', q['enunciado'])[:160]}")
    for f, lista in por_fam.items():
        errs += [f"{len(lista)} muestras con fallas en {f}"] + lista[:3]
    sin = {f["id"] for f in datos["familias"]} - set(GCHK)
    errs += [f"familia sin cálculo: {f}" for f in sorted(sin)]
    # los enlaces «Práctica infinita» de las lecciones deben apuntar justo a los temas con generador
    lec = (RAIZ / "tools" / "lecciones.js").read_text(encoding="utf-8")
    m = re.search(r"const CON_NUMEROS = new Set\(\[(.*?)\]\)", lec, re.S)
    gen_temas = {f["tema"] for f in datos["familias"]}
    if not m or set(re.findall(r"'([a-z0-9.\-]+)'", m.group(1))) != gen_temas:
        errs.append("CON_NUMEROS en lecciones.js no coincide con los temas de generadores.js")
    print(f"práctica infinita: {len(datos['familias'])} familias · {len(datos['muestras'])} muestras recalculadas")
    return errs


POST.append(_gen_revisar)
