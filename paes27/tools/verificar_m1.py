# Cálculos de m1.html (repaso rápido + trampas de M1). Lo carga tools/verificar.py (comparte chk, idx_num, etc.).
# ruff: noqa: F821
import html
import math
import re
from fractions import Fraction as F


def idx_desig(q, op, lim):
    """Alternativas tipo 'x < −3': una sola coincide con el operador y el límite."""
    def ok(t):
        m = re.match(r"^\s*x\s*([<>]=?)\s*(.+)$", html.unescape(re.sub(r"<[^>]+>", "", t)))
        return bool(m) and m.group(1) == op and cerca(valor(m.group(2)), lim)
    return unico(q, ok, f"x {op} {lim}")


# ===== Enteros y racionales
chk("m1-ent-b1")(lambda q: idx_num(q, -3 + 5 * (-2)))
chk("m1-ent-p1")(lambda q: idx_num(q, max(F(2, 3), F(66, 100), F(5, 8), F(6, 10))))
chk("m1-ent-p2")(lambda q: idx_num(q, F(3, 4) * (1 - F(1, 3))))
chk("m1-ent-d1")(lambda q: idx_num(q, (F(-2, 3) - F(1, 2)) / (F(-2, 3) * F(1, 2))))


@chk("m1-ent-d2")
def _(q):
    fuera = [i for i, o in enumerate(q["opciones"]) if not (F(1, 3) < F(valor(o["texto"])).limit_denominator(1000) < F(1, 2))]
    if len(fuera) != 1:
        raise Falla(f"{len(fuera)} alternativas fuera de (1/3, 1/2)")
    return fuera[0]


# ===== Porcentaje
chk("m1-por-b1")(lambda q: idx_num(q, 15 / 100 * 240))
chk("m1-por-p1")(lambda q: idx_num(q, 20000 * 1.1 * 0.9))
chk("m1-por-p2")(lambda q: idx_num(q, (40 - 12) / 40 * 100))
chk("m1-por-d1")(lambda q: idx_num(q, 12000 / 0.8))
chk("m1-por-d2")(lambda q: idx_num(q, 400 * 1.5 ** 2))

# ===== Potencias y raíces
chk("m1-pot-b1")(lambda q: idx_num(q, 2 ** -3))
chk("m1-pot-p1")(lambda q: idx_num(q, 1.7 ** 3 * 1.7 ** 5 / 1.7 ** 2, env={"a": 1.7}))
chk("m1-pot-p2")(lambda q: idx_num(q, math.sqrt(50) + math.sqrt(18)))
chk("m1-pot-d1")(lambda q: idx_num(q, 27 ** (2 / 3)))
chk("m1-pot-d2")(lambda q: idx_num(q, 2 ** (math.log2(32) - 2)))

# ===== Expresiones algebraicas
chk("m1-exp-b1")(lambda q: idx_func(q, lambda x: (x + 3) ** 2))
chk("m1-exp-p1")(lambda q: idx_func(q, lambda x: x ** 2 - 5 * x + 6))
chk("m1-exp-p2")(lambda q: idx_func(q, lambda x: (2 * x - 1) * (2 * x + 1)))


@chk("m1-exp-d1")
def _(q):
    a = (7 + math.sqrt(49 - 40)) / 2          # a + b = 7, ab = 10 → a = 5, b = 2
    b = 7 - a
    return idx_num(q, a ** 2 + b ** 2)


chk("m1-exp-d2")(lambda q: idx_func(q, lambda x: (x ** 2 - 9) / (x ** 2 + 3 * x)))

# ===== Ecuaciones, inecuaciones y sistemas
chk("m1-ecu-b1")(lambda q: idx_num(q, F(5 + 6, 3 - 2)))
chk("m1-ecu-p1")(lambda q: idx_desig(q, "<", (9 - 3) / -2))     # dividir por −2 invierte '>'


@chk("m1-ecu-p2")
def _(q):
    x = (10 + 4) / 2
    return idx_num(q, x * (10 - x))


@chk("m1-ecu-d1")
def _(q):
    n = (5 * 8 - 34) / (5 - 3)      # 5(8 − n) + 3n = 34
    assert n == int(n) and 0 <= n <= 8
    return idx_num(q, n)


chk("m1-ecu-d2")(lambda q: idx_num(q, (15000 - 8000) // 50))

# ===== Funciones
chk("m1-fun-b1")(lambda q: idx_num(q, 3 * -4 - 2))
chk("m1-fun-p1")(lambda q: idx_num(q, F(9 - 3, 4 - 1)))


@chk("m1-fun-p2")
def _(q):
    d = math.sqrt(1 + 48)
    return idx_partes(q, ((1 + d) / 2, (1 - d) / 2), r" y ")


chk("m1-fun-d1")(lambda q: idx_num(q, (3, 3 ** 2 - 6 * 3 + 5)))
chk("m1-fun-d2")(lambda q: idx_num(q, -5 * (20 / 10) ** 2 + 20 * (20 / 10)))

# ===== Proporcionalidad
chk("m1-pro-b1")(lambda q: idx_num(q, 6000 / 4 * 10))
chk("m1-pro-p1")(lambda q: idx_num(q, 6 * 10 / 4))
chk("m1-pro-p2")(lambda q: idx_num(q, 3 * 12 / 9))
chk("m1-pro-d1")(lambda q: idx_num(q, 2 + (3 * 8 - 3 * 2) / 4))


@chk("m1-pro-d2")
def _(q):
    pares = [(2, 10), (4, 5), (5, 4)]
    k = {x * y for x, y in pares}
    assert len(k) == 1 and len({F(y, x) for x, y in pares}) > 1
    return idx_texto(q, f"Inversa, con x · y = {k.pop()}")


# ===== Áreas y volúmenes
chk("m1-are-b1")(lambda q: idx_num(q, (8 + 4) * 5 / 2))
chk("m1-are-p1")(lambda q: idx_num(q, math.pi * 3 ** 2 * 10))
chk("m1-are-p2")(lambda q: idx_num(q, 6 * 4 ** 2))
chk("m1-are-d1")(lambda q: idx_num(q, math.pi * (10 / 2) ** 2))
chk("m1-are-d2")(lambda q: idx_num(q, 3.14 * (2 / 2) ** 2 * 1.5 * 1000))

# ===== Semejanza y Pitágoras
chk("m1-sem-b1")(lambda q: idx_num(q, math.hypot(6, 8)))
chk("m1-sem-p1")(lambda q: idx_num(q, math.sqrt(5 ** 2 - 3 ** 2)))
chk("m1-sem-p2")(lambda q: idx_num(q, 8 * 50000 / 100 / 1000))      # cm → m → km
chk("m1-sem-d1")(lambda q: idx_num(q, 18 * 3 / 2))
chk("m1-sem-d2")(lambda q: idx_num(q, 5 * 3 ** 2))

# ===== Transformaciones
chk("m1-tra-b1")(lambda q: idx_num(q, (2 - 3, -1 + 4)))
chk("m1-tra-p1")(lambda q: idx_num(q, (-3, 5)))
chk("m1-tra-p2")(lambda q: idx_num(q, (-1, 4)))                      # (x, y) → (−y, x)


@chk("m1-tra-d1")
def _(q):
    v = (-2 - 1, 5 - 1)
    return idx_num(q, (1 + v[0], 3 + v[1]))


@chk("m1-tra-d2")
def _(q):
    orig, img = [(1, 2), (3, 2), (1, 5)], [(-1, -2), (-3, -2), (-1, -5)]
    assert all((-x, -y) == p for (x, y), p in zip(orig, img))
    return idx_texto(q, "Una rotación de 180° con centro en el origen")


# ===== Datos y medidas de posición
chk("m1-dat-b1")(lambda q: idx_num(q, sum([5, 6, 6, 10, 13]) / 5))
chk("m1-dat-p1")(lambda q: idx_num(q, 9 / 36 * 100))


@chk("m1-dat-p2")
def _(q):
    d = sorted([2, 4, 4, 4, 7, 8, 9, 11, 12])
    n = len(d)
    # tres convenciones habituales dan lo mismo con estos datos
    excl = d[:n // 2]; incl = d[:n // 2 + 1]
    med = lambda v: (v[(len(v) - 1) // 2] + v[len(v) // 2]) / 2
    pos = (n + 1) / 4; interp = d[int(pos) - 1] + (pos - int(pos)) * (d[int(pos)] - d[int(pos) - 1])
    assert med(excl) == med(incl) == interp
    return idx_num(q, med(excl))


CONCEPTUALES["m1-dat-d1"] = "lectura de diagrama de cajón (cualitativa)"
chk("m1-dat-d2")(lambda q: idx_num(q, 5 * 5.8 - 4 * 5.5))

# ===== Probabilidad
chk("m1-prb-b1")(lambda q: idx_num(q, F(len([x for x in range(1, 7) if x > 4]), 6)))


@chk("m1-prb-p1")
def _(q):
    casos = [a + b for a in "CS" for b in "CS"]
    return idx_num(q, F(sum(c.count("C") == 1 for c in casos), len(casos)))


chk("m1-prb-p2")(lambda q: idx_num(q, F(5 + 2, 10)))
chk("m1-prb-d1")(lambda q: idx_num(q, F(5, 10) * F(4, 9)))
chk("m1-prb-d2")(lambda q: idx_num(q, F(18 + 12 - 5, 30)))
