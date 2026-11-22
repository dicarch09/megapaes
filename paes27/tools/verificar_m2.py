# Cálculos de las lecciones de m2.html. Lo carga tools/verificar.py (comparte chk, idx_num, etc.).
# ruff: noqa: F821
import math
from fractions import Fraction

# ===== Lección 1 · rectas + sistemas
chk("m2-rec-b1")(lambda q: idx_num(q, Fraction(-4, 2)))                        # 2y = -4x + 6
chk("m2-rec-b2")(lambda q: idx_num(q, Fraction(7 - 1, 4 - 2)))
chk("m2-rec-b3")(lambda q: idx_num(q, ((10 + 4) / 2, (10 - 4) / 2)))
chk("m2-rec-p1")(lambda q: idx_func(q, lambda x: (-1 / 3) * x - 2))           # m = -1/3 (perpendicular a 3), n = -2
chk("m2-rec-p2")(lambda q: idx_num(q, Fraction(-2, -4)))                       # 2x - 4y = 8 -> y = x/2 - 2


@chk("m2-rec-p3")
def _(q):
    # 2c + 3l = 3400 ; c + 2l = 2000  (Cramer)
    det = 2 * 2 - 3 * 1
    c = (3400 * 2 - 3 * 2000) / det
    l = (2 * 2000 - 1 * 3400) / det
    assert 2 * c + 3 * l == 3400 and c + 2 * l == 2000
    return idx_num(q, c)


@chk("m2-rec-d1")
def _(q):
    k = Fraction(2, 4) * 6                       # 2/4 = k/6
    assert Fraction(5, 7) != Fraction(2, 4)      # no coinciden: sin solución
    return idx_num(q, k)


@chk("m2-rec-d2")
def _(q):
    x = (5 + 1) / (2 + 1)                        # 2x - 1 = -x + 5
    base = 5 - (-1)
    return idx_num(q, base * x / 2)


@chk("m2-rec-d3")
def _(q):
    m = (-4 - 4) / (3 - (-1))
    n = 4 - m * (-1)
    return idx_num(q, (-n / m, 0))


# ===== Lección 2 · logaritmos
chk("m2-log-b1")(lambda q: idx_num(q, math.log(125, 5)))
chk("m2-log-b2")(lambda q: idx_num(q, math.log10(1000) + math.log10(0.1)))


@chk("m2-log-b3")
def _(q):
    # log2(x - 3) existe si x - 3 > 0: frontera 3 excluida
    assert all((x - 3 > 0) == (x > 3) for x in (2.9, 3, 3.1))
    return idx_texto(q, "x > 3")


chk("m2-log-p1")(lambda q: idx_num(q, math.log10(18), env={"a": math.log10(2), "b": math.log10(3)}))
chk("m2-log-p2")(lambda q: idx_num(q, (math.log(27, 3) + 1) / 2))


@chk("m2-log-p3")
def _(q):
    f = lambda x: 0.5 ** x  # noqa: E731
    decreciente = f(2) < f(1)
    corte = f(0)
    esperado = f"Es {'decreciente' if decreciente else 'creciente'} y corta al eje Y en (0, {corte:g})."
    return idx_texto(q, esperado)


chk("m2-log-d1")(lambda q: idx_num(q, 3 * 0.4 - 2 * 0.4))                    # log_a 8 = 3·0,4 ; log_a 4 = 2·0,4


@chk("m2-log-d2")
def _(q):
    # x(x - 8) = 9 -> x² - 8x - 9 = 0 ; dominio x > 8
    disc = 64 + 36
    raices = [(8 + math.sqrt(disc)) / 2, (8 - math.sqrt(disc)) / 2]
    validas = [r for r in raices if r > 8]
    assert len(validas) == 1
    return idx_num(q, validas[0])


chk("m2-log-d3")(lambda q: idx_num(q, 0.30 / 0.04))

# ===== Lección 3 · probabilidad condicional
chk("m2-con-b1")(lambda q: idx_num(q, Fraction(6, 8 + 6)))
chk("m2-con-b2")(lambda q: idx_num(q, 0.2 / 0.4))
chk("m2-con-b3")(lambda q: idx_num(q, Fraction(4, 10) * Fraction(3, 9)))
chk("m2-con-p1")(lambda q: idx_num(q, Fraction(25, 40)))
chk("m2-con-p2")(lambda q: idx_num(q, (0.7 * 0.02 + 0.3 * 0.05) * 100))       # en %


@chk("m2-con-p3")
def _(q):
    casos = [a + b for a in "CS" for b in "CS"]
    cond = [c for c in casos if "C" in c]
    return idx_num(q, Fraction(sum(c == "CC" for c in cond), len(cond)))


@chk("m2-con-d1")
def _(q):
    pos = 0.1 * 0.9 + 0.9 * 0.2
    return idx_num(q, 0.1 * 0.9 / pos)


chk("m2-con-d2")(lambda q: idx_num(q, 0.3 + 0.5 - 0.3 * 0.5))


@chk("m2-con-d3")
def _(q):
    M, H = Fraction(3, 5), Fraction(2, 5)
    pl = M * Fraction(1, 2) + H * Fraction(1, 4)
    return idx_num(q, H * Fraction(1, 4) / pl)


# ===== Lección 4 · trigonometría
chk("m2-tri-b1")(lambda q: idx_num(q, Fraction(math.isqrt(13 ** 2 - 5 ** 2), 13)))
chk("m2-tri-b2")(lambda q: idx_num(q, math.sin(math.radians(30)) + math.cos(math.radians(60))))
chk("m2-tri-b3")(lambda q: idx_num(q, abs(-4)))
chk("m2-tri-p1")(lambda q: idx_num(q, 20 * math.tan(math.radians(30))))
chk("m2-tri-p2")(lambda q: idx_num(q, 2 * math.pi / 3))
chk("m2-tri-p3")(lambda q: idx_num(q, math.sin(math.atan(1)) * math.cos(math.atan(1))))


@chk("m2-tri-d1")
def _(q):
    h, x = 2 * math.sin(math.radians(30)), 2 * math.cos(math.radians(30))
    return idx_partes(q, (h, x), r" km de altura y | km en horizontal")


@chk("m2-tri-d2")
def _(q):
    mx, mn, per = 5, 1, math.pi
    A, C, B = (mx - mn) / 2, (mx + mn) / 2, 2 * math.pi / per
    return idx_func(q, lambda x: A * math.sin(B * x) + C)


@chk("m2-tri-d3")
def _(q):
    bc = 10 * 0.6
    ac = math.sqrt(10 ** 2 - bc ** 2)
    return idx_num(q, bc * ac / 2)


# ===== Ejemplos resueltos (números escritos a mano en m2.html)
def _ejemplos():
    m = (7 - 3) / (3 - 1); n = 3 - m * 1
    x = (7 - n) / (m + 1); y = m * x + n
    assert (m, n, x, y) == (2, 1, 2, 5) and -x + 7 == y
    t = math.log2(16000 / 500)
    assert t == 5 and 500 * 2 ** 5 == 16000
    p = 0.6 * 0.3 / (0.6 * 0.3 + 0.4 * 0.1)
    assert abs(p - 9 / 11) < 1e-12 and round(p, 2) == 0.82
    h = 6 * math.sin(math.radians(60))
    assert abs(h - 3 * math.sqrt(3)) < 1e-12 and round(h, 1) == 5.2 and 3 < h < 6


_ejemplos()
