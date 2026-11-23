# Cálculos del rescate de Biología y Química (bioquim.html). Lo carga tools/verificar.py (comparte chk, idx_num, etc.).
# ruff: noqa: F821
from fractions import Fraction

MASA = {"H": 1, "C": 12, "N": 14, "O": 16}
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def formula(**n):
    """formula(C=6, H=12, O=6) -> 'C₆H₁₂O₆' (el 1 no se escribe)."""
    return "".join(el + ("" if k == 1 else str(k).translate(SUB)) for el, k in n.items())


def masa_molar(**n):
    return sum(MASA[el] * k for el, k in n.items())


# ===== Biología: todo conceptual (revisión ciega sin cálculos)
for _id, _m in {
    "bq-bcel-b": "la mitocondria produce el ATP", "bq-bcel-p": "células secretoras: RER + Golgi", "bq-bcel-d": "rasgos de una procarionte",
    "bq-bner-b": "orden del arco reflejo", "bq-bner-p": "despolarización: entra Na⁺", "bq-bner-d": "bloqueo de receptores postsinápticos",
    "bq-brep-b": "fecundación en la trompa", "bq-brep-p": "pico de LH y ovulación", "bq-brep-d": "caída de progesterona y menstruación",
    "bq-bant-b": "solo el condón previene ITS", "bq-bant-p": "ITS virales: VIH y herpes", "bq-bant-d": "por qué falla el calendario",
    "bq-bdiv-b": "fase S: replicación del ADN", "bq-bdiv-d": "punto de control G1–S y cáncer",
    "bq-bman-b": "insulina recombinante", "bq-bman-p": "código genético universal", "bq-bman-d": "productos sin manipulación genética",
    "bq-bevo-b": "estructuras homólogas", "bq-bevo-p": "explicación de Lamarck", "bq-bevo-d": "resistencia a antibióticos por selección",
    "bq-bfot-b": "el O₂ viene del agua", "bq-bfot-p": "fase oscura en el estroma", "bq-bfot-d": "factor limitante",
    "qui": None,
}.items():
    if _m:
        CONCEPTUALES[_id] = _m + " (cualitativa)"


@chk("bq-bdiv-p")
def _(q):
    n_cel, cromos = 2 ** 2, 46 // 2    # dos divisiones; mitad de cromosomas
    return idx_texto(q, f"{n_cel} células con {cromos} cromosomas cada una")


# ===== Materia
CONCEPTUALES["bq-qmat-b"] = "mezcla homogénea (cualitativa)"
CONCEPTUALES["bq-qmat-p"] = "destilación por distinto punto de ebullición (cualitativa)"
chk("bq-qmat-d")(lambda q: idx_num(q, 54 / (40 - 20)))

# ===== Modelos atómicos
CONCEPTUALES["bq-qmod-b"] = "modelo de Rutherford (cualitativa)"
CONCEPTUALES["bq-qmod-d"] = "conclusión de la lámina de oro (cualitativa)"


@chk("bq-qmod-p")
def _(q):
    Z, A = 26, 56
    return idx_texto(q, f"{Z} protones, {A - Z} neutrones y {Z} electrones")


# ===== Carbono
CONCEPTUALES["bq-qcar-b"] = "hibridación sp del etino (cualitativa)"
chk("bq-qcar-p")(lambda q: idx_num(q, 360 / 3))


@chk("bq-qcar-d")
def _(q):
    L = {"C≡C": 120, "C=C": 134, "C–C": 154}   # pm
    orden = " < ".join(sorted(L, key=L.get))
    import html
    return unico(q, lambda t: html.unescape(t).strip() == orden, repr(orden))


# ===== Orgánica
CONCEPTUALES["bq-qorg-b"] = "grupo alcohol del etanol (cualitativa)"
CONCEPTUALES["bq-qorg-d"] = "cetona vs aldehído (cualitativa)"
chk("bq-qorg-p")(lambda q: idx_texto(q, formula(C=5, H=2 * 5 + 2)))

# ===== Estequiometría
chk("bq-qest-b")(lambda q: idx_num(q, 36 / masa_molar(H=2, O=1)))
chk("bq-qest-p")(lambda q: idx_num(q, 6 * Fraction(2, 3)))


@chk("bq-qest-d")
def _(q):
    h2, o2 = 4, 3
    lim = "H₂" if h2 / 2 < o2 / 1 else "O₂"
    agua = h2 if lim == "H₂" else 2 * o2
    return idx_texto(q, f"El {lim}; se forman {agua:g} mol de H₂O")


# ===== Composición
chk("bq-qcom-b")(lambda q: idx_num(q, 12 / masa_molar(C=1, O=2) * 100, tol=2e-3))


@chk("bq-qcom-p")
def _(q):
    n = 180 // masa_molar(C=1, H=2, O=1)
    return idx_texto(q, formula(C=n, H=2 * n, O=n))


@chk("bq-qcom-d")
def _(q):
    moles = {"C": 40 / 12, "H": 6.7 / 1, "O": 53.3 / 16}
    menor = min(moles.values())
    razon = {el: round(v / menor) for el, v in moles.items()}
    assert all(abs(v / menor - razon[el]) < 0.03 for el, v in moles.items())
    return idx_texto(q, formula(**razon))


# ===== Soluciones
chk("bq-qsol-b")(lambda q: idx_num(q, 20 / (20 + 180) * 100))
chk("bq-qsol-p")(lambda q: idx_num(q, 0.5 / (250 / 1000)))
chk("bq-qsol-d")(lambda q: idx_num(q, 2 * 100 / 0.5 - 100))
