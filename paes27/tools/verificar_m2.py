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


# ===== Fase 2c · esfera
VE = lambda r: Fraction(4, 3) * r ** 3  # volumen / π  # noqa: E731
AE = lambda r: 4 * r ** 2               # área / π     # noqa: E731
chk("m2-esf-b1")(lambda q: idx_num(q, float(VE(3)) * math.pi))
chk("m2-esf-b2")(lambda q: idx_num(q, AE(10 / 2) * math.pi))
chk("m2-esf-b3")(lambda q: idx_texto(q, f"Se multiplica por {float(VE(2) / VE(1)):g}"))
chk("m2-esf-p1")(lambda q: idx_num(q, float(VE(math.isqrt(64 // 4))) * math.pi))
chk("m2-esf-p2")(lambda q: idx_num(q, (2 * 6) ** 3 - float(VE(6)) * math.pi))
chk("m2-esf-p3")(lambda q: idx_num(q, VE(3) / VE(1)))
chk("m2-esf-d1")(lambda q: idx_num(q, (AE(3) / 2 + 3 ** 2) * math.pi))
chk("m2-esf-d2")(lambda q: idx_num(q, (4 / 3 * math.pi) / (math.pi * 2)))   # r = 1
chk("m2-esf-d3")(lambda q: idx_num(q, 3 * 4 / 4))                           # (4/3)πr³ = 4πr² → r = 3·4π/(4π)

# ===== Fase 2c · homotecia
homo_pt = lambda O, k, P: (O[0] + k * (P[0] - O[0]), O[1] + k * (P[1] - O[1]))  # noqa: E731
chk("m2-hom-b1")(lambda q: idx_num(q, abs(3) * 4))
chk("m2-hom-b2")(lambda q: idx_num(q, homo_pt((0, 0), 0.5, (6, -4))))
chk("m2-hom-p1")(lambda q: idx_num(q, (-3) ** 2 * 10))
chk("m2-hom-p2")(lambda q: idx_num(q, homo_pt((1, 2), 2, (4, 3))))
chk("m2-hom-p3")(lambda q: idx_num(q, -Fraction(15, 6)))
chk("m2-hom-d1")(lambda q: idx_num(q, Fraction(4 + 10, 4)))


@chk("m2-hom-d2")
def _(q):
    k = math.sqrt(Fraction(18, 2 ** 2))           # k² = área nueva / área original
    def ok(t):
        vals = [valor(x) for x in re.findall(r"k = ([^ ]+)", t)]
        return len(vals) == 2 and None not in vals and cerca(tuple(sorted(vals)), (-k, k))
    return unico(q, ok, "k = ±3√2/2")


@chk("m2-hom-d3")
def _(q):
    assert 2 * Fraction(-1, 2) == -1
    return idx_texto(q, "Congruente, girada en 180° respecto del centro.")


# ===== Fase 2c · circunferencia
chk("m2-cir-b1")(lambda q: idx_num(q, 80 / 2))
chk("m2-cir-b2")(lambda q: idx_num(q, 180 / 2))
chk("m2-cir-b3")(lambda q: idx_num(q, 4 * 6 / 3))
chk("m2-cir-p1")(lambda q: idx_num(q, 4 * 9 / 3))
chk("m2-cir-p2")(lambda q: idx_num(q, 180 - 70))
chk("m2-cir-p3")(lambda q: idx_num(q, 2 * math.pi * 6 * 60 / 360))
chk("m2-cir-d1")(lambda q: idx_num(q, 2 * (180 - 35 - 65)))
chk("m2-cir-d2")(lambda q: idx_num(q, math.hypot(6, 8) / 2))


@chk("m2-cir-d3")
def _(q):
    raices = [(-5 + s * math.sqrt(25 + 4 * 36)) / 2 for s in (1, -1)]
    validas = [r for r in raices if r > 0]
    assert len(validas) == 1
    return idx_num(q, validas[0])


# ===== Fase 2c · binomial y normal
def Phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


bpmf = lambda n, k, p: math.comb(n, k) * p ** k * (1 - p) ** (n - k)  # noqa: E731
chk("m2-bin-b1")(lambda q: idx_num(q, bpmf(3, 2, Fraction(1, 2))))
chk("m2-bin-b2")(lambda q: idx_num(q, 20 * 0.3))
chk("m2-bin-b3")(lambda q: idx_num(q, round(100 * (Phi(1) - Phi(-1)))))
chk("m2-bin-p1")(lambda q: idx_num(q, 1 - bpmf(5, 0, Fraction(1, 2))))
chk("m2-bin-p2")(lambda q: idx_num(q, (182 - 170) / 8))
chk("m2-bin-p3")(lambda q: idx_num(q, (100 - 95) / 2))   # regla 68–95–99,7: 70 = μ + 2σ
chk("m2-bin-d1")(lambda q: idx_num(q, bpmf(4, 2, Fraction(1, 3))))


@chk("m2-bin-d2")
def _(q):
    za, zb = (6.2 - 5.0) / 0.8, (72 - 60) / 10
    assert za > zb
    return idx_texto(q, "Ana, porque su valor z es mayor.")


@chk("m2-bin-d3")
def _(q):
    p = 1 - 4.8 / 8
    n = 8 / p
    def ok(t):
        m = re.match(r"n = (\S+), p = (\S+)$", t)
        return bool(m) and cerca(valor(m.group(1)), n) and cerca(valor(m.group(2)), p)
    return unico(q, ok, f"n = {n:g}, p = {p:g}")


# ===== Fase 2c · matemática financiera
chk("m2-fin-b1")(lambda q: idx_num(q, 500_000 * 0.03 * 4))
chk("m2-fin-b2")(lambda q: idx_num(q, 900_000 * (0.10 + 0.015)))
chk("m2-fin-b3")(lambda q: idx_num(q, 12 * 95_000 - 1_000_000))
chk("m2-fin-p1")(lambda q: idx_num(q, 2_000_000 * 1.005 ** 12))
chk("m2-fin-p2")(lambda q: idx_num(q, 10_000_000 * 1.05 * 0.95))
chk("m2-fin-p3")(lambda q: idx_num(q, 15 * 12 * 20))
chk("m2-fin-d1")(lambda q: idx_num(q, 0.301 / 0.0334, tol=0.01))
chk("m2-fin-d2")(lambda q: idx_num(q, 1_000_000 * (1.01 ** 12 - 1.12), tol=1e-3))
chk("m2-fin-d3")(lambda q: idx_num(q, 0.2 * 8_000_000 + 36 * 230_000 - 8_000_000))
CONCEPTUALES["m2-hom-b3"] = "homotecia k = −1: descripción cualitativa"


def _ejemplos_2c():
    assert 28 + 90 + 62 == 180
    assert homo_pt((1, 1), -2, (3, 4)) == (-3, -5) and 5 * (-2) ** 2 == 20
    assert VE(6) == 288 and Fraction(288, 36) == 8
    assert abs(bpmf(3, 2, 0.7) - 0.441) < 1e-12 and abs(0.7 ** 3 - 0.343) < 1e-12
    assert round(1_000_000 * 1.02 ** 3) == 1_061_208 and 1_000_000 * (1 + 0.02 * 3) == 1_060_000


_ejemplos_2c()


# ===== Fase 2d · función potencia, reales, M1 difícil
chk("m2-pof-b1")(lambda q: idx_num(q, 3 * (-2) ** 3))


@chk("m2-pof-b2")
def _(q):
    def par(t):
        f = lambda x: valor(re.sub(r"^f\(x\) = ", "", t), {"x": x})  # noqa: E731
        return all(cerca(f(-x), f(x)) for x in (0.7, 1.3, 2.1)) and not all(cerca(f(-x), -f(x)) for x in (0.7, 1.3))
    return unico(q, par, "función par")


chk("m2-pof-p1")(lambda q: idx_num(q, Fraction(-4, 2 ** 3)))


@chk("m2-pof-p2")
def _(q):
    xs = [0.1, 0.37, 0.5, 0.83, 0.99]
    assert all(x ** 2 > x ** 3 > x ** 4 for x in xs)
    return idx_texto(q, "x²")


@chk("m2-pof-d1")
def _(q):
    f = lambda x: -3 * x ** 6 + 5  # noqa: E731
    xs = [i / 100 for i in range(-300, 301)]
    assert max(f(x) for x in xs) == 5 and min(f(x) for x in xs) < -100
    return idx_texto(q, "y ≤ 5")


@chk("m2-pof-d2")
def _(q):
    xs = [i / 20 for i in range(-60, 61) if i % 20]
    verdad = {x for x in xs if x ** 5 > x ** 3}
    conj = {"−1 < x < 0 o x > 1": lambda x: -1 < x < 0 or x > 1, "x > 1": lambda x: x > 1, "x > 0": lambda x: x > 0,
            "x < −1 o 0 < x < 1": lambda x: x < -1 or 0 < x < 1}
    return unico(q, lambda t: {x for x in xs if conj[t](x)} == verdad, "conjunto solución")


@chk("m2-rea-b1")
def _(q):
    vals = {"√8": math.sqrt(8), "√(16/9)": Fraction(4, 3), "0,25": Fraction(1, 4), "∛27": 3}
    assert math.isqrt(8) ** 2 != 8 and Fraction(4, 3) ** 2 == Fraction(16, 9) and 3 ** 3 == 27
    return idx_texto(q, next(k for k, v in vals.items() if isinstance(v, float)))


chk("m2-rea-b2")(lambda q: idx_num(q, round(8 ** (2 / 3), 9)))
chk("m2-rea-p1")(lambda q: idx_num(q, math.sqrt(12) + math.sqrt(27) - math.sqrt(75)))
chk("m2-rea-p2")(lambda q: idx_num(q, (math.sqrt(5) + math.sqrt(2)) * (math.sqrt(5) - math.sqrt(2))))


@chk("m2-rea-d1")
def _(q):
    v = {"a": math.sqrt(10), "b": 3.2, "c": 30 ** (1 / 3)}
    return idx_texto(q, " < ".join(sorted(v, key=v.get)))


chk("m2-rea-d2")(lambda q: idx_num(q, (2 ** 0.5 * 2 ** (1 / 3)) ** 6))
chk("m2-mdi-b1")(lambda q: idx_num(q, (2 * 2 ** 2 + 2 * 2 * 5) * math.pi))
chk("m2-mdi-b2")(lambda q: idx_num(q, 8 * Fraction(3, 2) ** 2))


@chk("m2-mdi-p1")
def _(q):
    sin_sol = lambda m: 36 - 4 * m < 0  # noqa: E731
    assert sin_sol(9.01) and not sin_sol(9) and not sin_sol(8.99)
    return idx_texto(q, "m > 9")


chk("m2-mdi-p2")(lambda q: idx_num(q, max(x / 100 * (10 - x / 100) for x in range(0, 1001))))
chk("m2-mdi-d1")(lambda q: idx_num(q, 50 * 2 ** 2 * 2))   # π(2r)²(2h) = 8πr²h
chk("m2-mdi-d2")(lambda q: idx_num(q, -(2 ** 2 - 4 * 2)))   # y_v = 4 − 8 + c = 0


def _ejemplos_2d():
    assert max(-2 * (i / 10) ** 4 + 3 for i in range(-30, 31)) == 3
    assert abs(math.sqrt(12) + math.sqrt(27) - math.sqrt(48) - math.sqrt(3)) < 1e-12
    assert [k for k in range(-10, 11) if k * k - 36 == 0] == [-6, 6]


_ejemplos_2d()
