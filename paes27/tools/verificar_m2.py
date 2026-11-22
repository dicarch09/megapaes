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


# ===== Fase 2a · suficiencia de datos (decide la alternativa con soluciones de muestra)
import itertools  # noqa: E402
import statistics  # noqa: E402

R1 = [Fraction(n, 2) for n in range(-40, 41)]
POS = [Fraction(n, 2) for n in range(1, 41)]


def sd_idx(sol1, sol2, solj, f):
    return idx_sd(None, determina(sol1, f), determina(sol2, f), determina(solj, f))


def chk_sd(qid, sol1, sol2, solj, f):
    @chk(qid)
    def _(q):
        return sd_idx(sol1, sol2, solj, f)


uno = lambda cond, dom=R1: [(x,) for x in dom if cond(x)]  # noqa: E731
chk_sd("m2-sd-b1", uno(lambda x: 3 * x - 2 == 10), uno(lambda x: x * x == 16), uno(lambda x: 3 * x - 2 == 10 and x * x == 16), lambda x: x)
chk_sd("m2-sd-b2", rejilla(lambda a, b: a - b == 5), rejilla(lambda a, b: a + b == 31), rejilla(lambda a, b: a - b == 5 and a + b == 31), lambda a, b: a)
pos2 = lambda cond: rejilla(lambda a, b: a > 0 and b > 0 and cond(a, b))  # noqa: E731
chk_sd("m2-sd-b3", pos2(lambda ac, bc: ac == 6), pos2(lambda ac, bc: bc == 8), pos2(lambda ac, bc: ac == 6 and bc == 8), lambda ac, bc: math.hypot(ac, bc))
nz = lambda cond: rejilla(lambda a, b: b != 0 and cond(a, b))  # noqa: E731
chk_sd("m2-sd-p1", nz(lambda a, b: 3 * a == 2 * b), nz(lambda a, b: a + b == 10), nz(lambda a, b: 3 * a == 2 * b and a + b == 10), lambda a, b: a / b)
ENT = range(-50, 51)
chk_sd("m2-sd-p2", uno(lambda n: 3 < n < 6, ENT), uno(lambda n: n % 2 == 0, ENT), uno(lambda n: 3 < n < 6 and n % 2 == 0, ENT), lambda n: n)
urna = lambda cond: [(r, a) for r in range(1, 40) for a in range(1, 40) if cond(r, a)]  # noqa: E731
chk_sd("m2-sd-p3", urna(lambda r, a: r + a == 12), urna(lambda r, a: a == 2 * r), urna(lambda r, a: r + a == 12 and a == 2 * r), lambda r, a: Fraction(r, r + a))
chk_sd("m2-sd-d1", rejilla(lambda x, y: x == 2 * y), rejilla(lambda x, y: y * y == 9), rejilla(lambda x, y: x == 2 * y and y * y == 9), lambda x, y: x * y)
# rectángulo: soluciones continuas parametrizadas
s_per = [(a, 10 - a) for a in (1, 2.5, 5, 7)]
s_diag = [(a, math.sqrt(52 - a * a)) for a in (2, 4, math.sqrt(26), 6.5)]
s_amb = [(a, 10 - a) for a in (4, 6) if abs(a * a + (10 - a) ** 2 - 52) < 1e-9]
assert len(s_amb) == 2
chk_sd("m2-sd-d2", s_per, s_diag, s_amb, lambda a, b: a * b)
ALU = range(1, 101)
chk_sd("m2-sd-d3", uno(lambda n: n % 4 == 0, ALU), uno(lambda n: 30 <= n <= 34, ALU), uno(lambda n: n % 4 == 0 and 30 <= n <= 34, ALU), lambda n: n)

# ===== Fase 2a · combinatoria
chk("m2-com-b1")(lambda q: idx_num(q, math.factorial(5)))
chk("m2-com-b2")(lambda q: idx_num(q, 3 * 4 * 2))
chk("m2-com-b3")(lambda q: idx_num(q, math.comb(6, 2)))
chk("m2-com-p1")(lambda q: idx_num(q, sum(1 for _ in itertools.product(range(10), repeat=4))))
chk("m2-com-p2")(lambda q: idx_num(q, sum(1 for _ in itertools.combinations(range(8), 3))))
chk("m2-com-p3")(lambda q: idx_num(q, sum(1 for _ in itertools.permutations(range(7), 3))))
chk("m2-com-d1")(lambda q: idx_num(q, sum(1 for p in itertools.permutations(range(5), 3) if p[0] != 0)))
chk("m2-com-d2")(lambda q: idx_num(q, sum(1 for h in itertools.combinations(range(5), 2) for m in itertools.combinations(range(4), 2))))
chk("m2-com-d3")(lambda q: idx_num(q, sum(1 for p in itertools.permutations(range(5)) if abs(p.index(0) - p.index(1)) == 1)))

# ===== Fase 2a · dispersión
chk("m2-dis-b1")(lambda q: idx_num(q, max([12, 7, 15, 9, 4]) - min([12, 7, 15, 9, 4])))


@chk("m2-dis-b3")
def _(q):
    d = [1, 4, 6, 9]
    antes, despues = statistics.pstdev(d), statistics.pstdev([x + 5 for x in d])
    return idx_texto(q, "No cambia" if abs(antes - despues) < 1e-12 else "?")


chk("m2-dis-p1")(lambda q: idx_num(q, math.sqrt(statistics.pvariance([2, 3, 5, 6, 9]))))


@chk("m2-dis-p2")
def _(q):
    d = [1, 4, 6, 9]
    k = statistics.pvariance([3 * x for x in d]) / statistics.pvariance(d)
    return idx_texto(q, f"Se multiplica por {k:g}")


@chk("m2-dis-p3")
def _(q):
    ana, beto = [5, 5, 5, 5], [3, 4, 6, 7]
    assert statistics.mean(ana) == statistics.mean(beto) and statistics.pstdev(beto) > statistics.pstdev(ana)
    return idx_texto(q, "Tienen la misma media, pero las notas de Beto tienen mayor desviación estándar.")


@chk("m2-dis-d1")
def _(q):
    d = [3, 5, 6, 7, 9]
    assert statistics.mean(d) == 6 and statistics.pvariance(d) == 4
    return idx_num(q, statistics.pvariance([Fraction(x) for x in d + [6]]))


chk("m2-dis-d2")(lambda q: idx_num(q, 100_000 * 1.1))
chk("m2-dis-d3")(lambda q: idx_num(q, statistics.pvariance([Fraction(x) for x in [2, 4, 3 * 4 - 2 - 4]])))
CONCEPTUALES["m2-dis-b2"] = "dispersión: comparación cualitativa de σ"


def _ejemplos_2a():
    c, l = 1040, 440
    assert 3 * c + 2 * l == 4000 and c == l + 600
    assert 10 * 9 * 8 == 720 and math.comb(10, 3) == 720 // math.factorial(3) == 120
    d = [2, 4, 4, 4, 5, 5, 7, 9]
    assert statistics.mean(d) == 5 and statistics.pvariance(d) == 4 and statistics.pstdev(d) == 2
    assert sum((x - 5) ** 2 for x in d) == 32


_ejemplos_2a()
