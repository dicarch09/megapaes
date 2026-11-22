# Cálculos de las lecciones de fisica.html. Lo carga tools/verificar.py (comparte chk, idx_num, etc.).
# ruff: noqa: F821
import math
from fractions import Fraction

G = 10  # g usado en toda la app

# ===== Describir el movimiento
chk("fis-cin-b1")(lambda q: idx_num(q, math.hypot(3, 4)))
chk("fis-cin-b3")(lambda q: idx_num(q, 30 / 1.5))
chk("fis-cin-p1")(lambda q: idx_partes(q, (400 / 80, 0 / 80), r" y "))
chk("fis-cin-p2")(lambda q: idx_num(q, (30 - 10) / 4))
chk("fis-cin-p3")(lambda q: idx_num(q, (6 - (-4)) / 5))
chk("fis-cin-d1")(lambda q: idx_num(q, 120 / (60 / 60 + 60 / 30)))
chk("fis-cin-d3")(lambda q: idx_num(q, abs(-20 - 20) / 5))
CONCEPTUALES["fis-cin-b2"] = "magnitudes escalares y vectoriales"
CONCEPTUALES["fis-cin-d2"] = "lanzamiento vertical: desplazamiento y aceleración (cualitativa)"

# ===== MRU y MRUA
X = lambda x0, v0, a, t: x0 + v0 * t + a * t * t / 2  # noqa: E731
chk("fis-mru-b1")(lambda q: idx_num(q, X(5, 3, 0, 4)))
chk("fis-mru-b3")(lambda q: idx_num(q, 0 + 3 * 6))


@chk("fis-mru-p1")
def _(q):
    # x = 10 − 2t + t²  →  v0 = −2, ½a = 1
    v0, a = -2, 2 * 1
    def ok(t):
        m = re.match(r"v₀ = (\S+) m/s y a = (\S+) m/s²$", t)
        return bool(m) and cerca(valor(m.group(1)), v0) and cerca(valor(m.group(2)), a)
    return unico(q, ok, "v0 = −2, a = 2")


chk("fis-mru-p2")(lambda q: idx_num(q, 0.5 * 4 * 12 + 6 * 12))


@chk("fis-mru-p3")
def _(q):
    a = (0 - 20) / 4
    return idx_num(q, X(0, 20, a, 4))


chk("fis-mru-d1")(lambda q: idx_num(q, 70 * (300 / (70 + 80))))
chk("fis-mru-d2")(lambda q: idx_num(q, X(0, 4, 2, 3) - X(0, 4, 2, 2)))


@chk("fis-mru-d3")
def _(q):
    a = (-10 - 10) / 4
    pasos = [X(0, 10, a, i / 1000) for i in range(4001)]
    despl = pasos[-1]
    dist = sum(abs(pasos[i + 1] - pasos[i]) for i in range(4000))
    return idx_partes(q, (round(despl, 6), round(dist, 6)), r" y ")


CONCEPTUALES["fis-mru-b2"] = "lectura de gráfico x–t (cualitativa)"

# ===== Relatividad de Galileo
chk("fis-gal-b1")(lambda q: idx_num(q, 2 + 20))
chk("fis-gal-b2")(lambda q: idx_num(q, 90 - 70))


@chk("fis-gal-b3")
def _(q):
    v = 0 - 15
    return idx_texto(q, f"A {abs(v)} m/s hacia el {'oeste' if v < 0 else 'este'}")


chk("fis-gal-p1")(lambda q: idx_num(q, 60 + 40))
chk("fis-gal-p3")(lambda q: idx_partes(q, (5 + 3, 5 - 3), r" m/s río abajo y | m/s río arriba"))
chk("fis-gal-d1")(lambda q: idx_num(q, 100 / (25 - 20)))
chk("fis-gal-d3")(lambda q: idx_num(q, -30 + 30))
CONCEPTUALES["fis-gal-p2"] = "sistema inercial: caída de una moneda (cualitativa)"
CONCEPTUALES["fis-gal-d2"] = "invariantes de Galileo (cualitativa)"

# ===== Newton
chk("fis-new-b1")(lambda q: idx_num(q, 20 / 4))
chk("fis-new-p1")(lambda q: idx_num(q, (30 - 10) / 5))
chk("fis-new-p2")(lambda q: idx_num(q, 500 * G))
chk("fis-new-p3")(lambda q: idx_num(q, 2 * (20 / (2 + 3))))
chk("fis-new-d1")(lambda q: idx_num(q, 1000 * (20 / 10)))
chk("fis-new-d2")(lambda q: idx_num(q, 60 * (G + 2)))
chk("fis-new-d3")(lambda q: idx_num(q, math.hypot(6, 8) / 2))
CONCEPTUALES["fis-new-b2"] = "tercera ley (cualitativa)"
CONCEPTUALES["fis-new-b3"] = "primera ley (cualitativa)"

# ===== Fuerzas
chk("fis-fue-b1")(lambda q: idx_num(q, 70 * G))
chk("fis-fue-b2")(lambda q: idx_num(q, 400 * 0.1))
chk("fis-fue-p1")(lambda q: idx_num(q, 5 * Fraction(5, 2)))


@chk("fis-fue-p2")
def _(q):
    N = 20 * G
    max_e, F = 0.4 * N, 60
    mueve = F > max_e
    roce = 0.3 * N if mueve else F
    return idx_texto(q, f"{'Se mueve' if mueve else 'No se mueve'} y el roce vale {roce:g} N")


chk("fis-fue-p3")(lambda q: idx_num(q, (50 - 0.2 * 10 * G) / 10))
chk("fis-fue-d1")(lambda q: idx_partes(q, (0.5 * 50 * G, 0.4 * 50 * G), r" y "))
chk("fis-fue-d3")(lambda q: idx_num(q, 3 * G / ((26 - 20) / 100)))
CONCEPTUALES["fis-fue-b3"] = "normal y peso (cualitativa)"
CONCEPTUALES["fis-fue-d2"] = "velocidad terminal (cualitativa)"


def _ejemplos_fis_mec():
    assert (12 + 4) / 4 == 4 and (12 - 4) / 4 == 2
    t = 20 / 4
    assert t == 5 and X(0, 20, -4, t) == 50
    assert 50 / (60 + 40) == 0.5
    assert (30 - 10) / 5 == 4 and 0 + 4 * 3 == 12
    N = 10 * G
    assert 0.5 * N == 50 and 40 < 50 and 60 > 50 and (60 - 0.3 * N) / 10 == 3


_ejemplos_fis_mec()


# ===== Ondas
C_LUZ = 3e8
chk("fis-ond-b1")(lambda q: idx_num(q, 1 / 5))
chk("fis-ond-b3")(lambda q: idx_num(q, 2 * 3))
chk("fis-ond-p1")(lambda q: idx_num(q, C_LUZ / 1.5e6))
chk("fis-ond-d1")(lambda q: idx_num(q, C_LUZ * 2e-15))
chk("fis-ond-d3")(lambda q: idx_num(q, round(C_LUZ / 2.45e9 * 100), tol=1e-9))   # λ en cm, redondeado


@chk("fis-ond-p3")
def _(q):
    f = 5e14
    r = (C_LUZ / (2 * f)) / (C_LUZ / f)
    return idx_texto(q, {0.5: "Se reduce a la mitad", 2: "Se duplica", 1: "No cambia"}[r])


@chk("fis-ond-d2")
def _(q):
    fa, fb = C_LUZ / 400e-9, C_LUZ / 800e-9
    assert abs(fa / fb - 2) < 1e-12
    return idx_texto(q, "A tiene el doble de frecuencia que B, y ambas viajan a la misma rapidez.")


CONCEPTUALES["fis-ond-b2"] = "definición de longitud de onda"
CONCEPTUALES["fis-ond-p2"] = "la frecuencia se conserva al cambiar de medio"


def imagen(tipo, d, f):
    """Clasifica la imagen con 1/f = 1/do + 1/di (f < 0 divergentes y convexos)."""
    if tipo == 'plano':
        di = -d
    else:
        fs = {'conv': f, 'conc': f, 'div': -f, 'convx': -f}[tipo]
        di = 1 / (1 / fs - 1 / d)
    m = -di / d
    tam = "del mismo tamaño" if abs(abs(m) - 1) < 1e-9 else ("de mayor tamaño" if abs(m) > 1 else "de menor tamaño")
    return ("Real" if di > 0 else "Virtual"), ("invertida" if m < 0 else "derecha"), tam, di, m


@chk("fis-len-b1")
def _(q):
    t, o, tam, *_ = imagen('plano', 20, None)
    return idx_texto(q, f"{t}, {o} y {tam}")


@chk("fis-len-b3")
def _(q):
    t, o, tam, *_ = imagen('convx', 30, 10)
    return idx_texto(q, f"{t}, {o} y {tam.replace('de menor tamaño', 'más pequeña')}")


@chk("fis-len-p1")
def _(q):
    t, o, tam, *_ = imagen('conv', 20, 10)
    return idx_texto(q, f"{t}, {o} y {tam}")


@chk("fis-len-p2")
def _(q):
    t, o, tam, *_ = imagen('conv', 6, 10)
    return idx_texto(q, f"{t}, {o} y {tam}")


chk("fis-len-d1")(lambda q: idx_num(q, 1 / (1 / 10 - 1 / 15)))


@chk("fis-len-d2")
def _(q):
    t, o, tam, di, m = imagen('conc', 30, 10)
    assert t == "Real" and o == "invertida" and abs(di - 15) < 1e-9
    return idx_texto(q, f"Real, invertida y menor, a {di:g} cm del espejo")


@chk("fis-len-d3")
def _(q):
    ds = [100, 50, 30, 20, 15, 12, 11]
    datos = [imagen('conv', d, 10) for d in ds]
    assert all(x[0] == "Real" for x in datos)
    assert all(datos[i + 1][3] > datos[i][3] and abs(datos[i + 1][4]) > abs(datos[i][4]) for i in range(len(ds) - 1))
    return idx_texto(q, "Se aleja de la lente y se agranda")


CONCEPTUALES["fis-len-b2"] = "lupa: lente convergente con objeto dentro de F"
CONCEPTUALES["fis-len-p3"] = "imagen proyectada: real e invertida"
chk("fis-ref-b1")(lambda q: idx_num(q, 30))
chk("fis-ref-p1")(lambda q: idx_num(q, C_LUZ / 1.33, tol=2e-3))


@chk("fis-ref-p2")
def _(q):
    assert 450 * 1.5 == 675
    return idx_texto(q, f"La frecuencia no cambia y λ = {450 / 1.5:g} nm")


@chk("fis-ref-d1")
def _(q):
    th1 = math.radians(30)
    th2 = math.asin(1.33 * math.sin(th1))   # del agua (1,33) al aire (1)
    assert th2 > th1 and C_LUZ / 1 > C_LUZ / 1.33
    return idx_texto(q, "Aumenta su rapidez y se aleja de la normal")


CONCEPTUALES["fis-ref-b2"] = "propagación rectilínea (cualitativa)"
CONCEPTUALES["fis-ref-d2"] = "absorción (cualitativa)"
CONCEPTUALES["fis-cos-p3"] = "Big Crunch vs expansión acelerada (cualitativa)"
ORDEN_EM = ["Ondas de radio", "Microondas", "Infrarrojo", "Luz visible", "Ultravioleta", "Rayos X", "Rayos gamma"]


@chk("fis-esp-b1")
def _(q):
    presentes = [o["texto"] for o in q["opciones"]]
    return idx_texto(q, min(presentes, key=ORDEN_EM.index))


@chk("fis-esp-d1")
def _(q):
    f = C_LUZ / 0.03
    banda = "microondas" if 3e8 <= f < 3e11 else "?"
    def ok(t):
        m = re.match(r"(\S+) Hz, (.+)$", t)
        return bool(m) and cerca(valor(m.group(1)), f) and m.group(2) == banda
    return unico(q, ok, f"{f:g} Hz, {banda}")


CONCEPTUALES["fis-esp-b2"] = "usos del espectro"
CONCEPTUALES["fis-esp-p1"] = "color por reflexión selectiva"
CONCEPTUALES["fis-esp-p2"] = "dispersión en el prisma"
CONCEPTUALES["fis-esp-d2"] = "energía y frecuencia (cualitativa)"
chk("fis-dop-d1")(lambda q: idx_num(q, 1 + (-1)))   # amplitud A con A = 1
for _id, _m in [("fis-dop-b1", "Doppler"), ("fis-dop-b2", "interferencia"), ("fis-dop-p1", "corrimiento al rojo"), ("fis-dop-p2", "difracción"),
                ("fis-dop-d2", "radar Doppler"), ("fis-dis-b1", "radar"), ("fis-dis-p1", "telescopios"), ("fis-dis-d1", "fibra óptica")]:
    CONCEPTUALES[_id] = _m + " (cualitativa)"


def _ejemplos_fis_ond():
    assert C_LUZ / 1e8 == 3
    assert imagen('conv', 15, 10)[:3] == ("Real", "invertida", "de mayor tamaño") and abs(imagen('conv', 15, 10)[3] - 30) < 1e-9
    assert C_LUZ / 1.5 == 2e8 and 600 / 1.5 == 400


_ejemplos_fis_ond()


# ===== Electricidad
par_ = lambda *r: 1 / sum(1 / x for x in r)  # noqa: E731
chk("fis-ohm-b1")(lambda q: idx_num(q, 12 / 4))
chk("fis-ohm-b2")(lambda q: idx_num(q, 3 + 6))
chk("fis-ohm-b3")(lambda q: idx_num(q, par_(6, 6)))
chk("fis-ohm-p1")(lambda q: idx_num(q, 12 / (2 + 2 + 2)))
chk("fis-ohm-p2")(lambda q: idx_num(q, 12 / 4 + 12 / 12))
chk("fis-ohm-d1")(lambda q: idx_num(q, 8 / (2 + par_(6, 3))))
chk("fis-ohm-d2")(lambda q: idx_num(q, 12 / (2 + 4) * 4))


@chk("fis-ohm-d3")
def _(q):
    V, R = 12, 6
    assert V / par_(R, 4) > V / R
    return idx_texto(q, "Aumenta")


CONCEPTUALES["fis-ohm-p3"] = "circuito en serie abierto (cualitativa)"
chk("fis-pot-b1")(lambda q: idx_num(q, 220 * 5))
chk("fis-pot-b2")(lambda q: idx_num(q, 1000 / 1000 * 2))
chk("fis-pot-p1")(lambda q: idx_num(q, 60 / 1000 * 5 * 30 * 150))
chk("fis-pot-p2")(lambda q: idx_num(q, 20 ** 2 / 10))
chk("fis-pot-p3")(lambda q: idx_num(q, 10 / 100 * 100))
chk("fis-pot-d1")(lambda q: idx_num(q, 110 ** 2 / (220 ** 2 / 2200)))
chk("fis-pot-d3")(lambda q: idx_num(q, (60 - 10) / 1000 * 1000))


@chk("fis-pot-d2")
def _(q):
    r60, r100 = 220 ** 2 / 60, 220 ** 2 / 100
    return idx_texto(q, "La de 60 W" if r60 > r100 else "La de 100 W")


CONCEPTUALES["fis-pot-b3"] = "el kWh es unidad de energía"


@chk("fis-dom-d1")
def _(q):
    I = (1760 + 880) / 220
    assert 1760 / 220 == 8 and 880 / 220 == 4
    return idx_texto(q, f"El automático corta, porque circulan {I:g} A en total" if I > 10 else "?")


CONCEPTUALES["fis-dom-b1"] = "conexión en paralelo de la casa"
CONCEPTUALES["fis-dom-p1"] = "función del disyuntor"
for _id in ["fis-tec-b1", "fis-tec-b2", "fis-tec-p1", "fis-tec-p2", "fis-tec-d1", "fis-tec-d2", "fis-cos-b1", "fis-cos-p1", "fis-cos-p2", "fis-cos-d1"]:
    CONCEPTUALES[_id] = "Tierra y Universo (cualitativa)"


def _ejemplos_fis_ele():
    assert par_(6, 3) == 2 and 12 / (4 + 2) == 2 and 2 * 4 == 8 and abs(4 / 6 - 0.667) < 1e-3
    assert 0.12 * 150 == 18 and round(18 * 180) == 3240


_ejemplos_fis_ele()
