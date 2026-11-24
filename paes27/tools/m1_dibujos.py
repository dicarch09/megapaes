"""Dibujos (SVG) para las tarjetas de m1.html. Los usa tools/m1.py.

DIBUJOS[(id del tema, título de la tarjeta)] = svg  → va dentro de esa tarjeta, después del título.
NUEVAS[id del tema] = [(tipo, título, html, svg)]     → tarjetas extra «en un dibujo», al inicio del tema.
Colores por clase (.a .b .w .r .g .m; rellenos .fa .fb .fw .fr .fg .fm) o por variable (--acc, --acc2, --warn, --mal, --ok).
"""
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from esquemas import aro, caja, circ, curva, ejes, fl, ln, poly, puntos, svg, tx  # noqa: E402

VAR = {'a': 'acc', 'b': 'acc2', 'w': 'warn', 'r': 'mal', 'g': 'ok', 'm': 'muted'}


def t(x, y, s, anchor='middle', c=None, tam=None):
    estilo = []
    if c:
        estilo.append(f'fill:var(--{VAR[c]})')
    if tam:
        estilo.append(f'font-size:{tam}px')
    st = f' style="{";".join(estilo)}"' if estilo else ''
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}"{st}>{s}</text>'


def rel(x, y, w, h, c='a', op=.45):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" style="fill:var(--{VAR[c]});fill-opacity:{op}"/>'


def marco(x, y, w, h, c='m', ancho=2, dash=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<rect class="{c}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" stroke-width="{ancho}"{d}/>'


def barra(x, y, w, h, n, k, c='a', inicio=0):
    """Barra dividida en n partes con k pintadas (desde la parte «inicio»)."""
    partes = [rel(x + w * (inicio + i) / n, y, w / n, h, c) for i in range(k)]
    div = [ln(round(x + w * i / n, 1), y, round(x + w * i / n, 1), y + h, 'm', 1.5) for i in range(1, n)]
    return ''.join(partes) + marco(x, y, w, h) + ''.join(div)


def equis(x, y, r=6, c='r'):
    return ln(x - r, y - r, x + r, y + r, c, 2.5) + ln(x - r, y + r, x + r, y - r, c, 2.5)


def recta_num(x0, x1, y, v0, v1, marcas, tam=10):
    X = lambda v: x0 + (v - v0) * (x1 - x0) / (v1 - v0)
    s = fl(x0 - 6, y, x1 + 8, y, 'm', 1.8)
    for v in marcas:
        s += ln(round(X(v), 1), y - 4, round(X(v), 1), y + 4, 'm', 1.5) + t(round(X(v), 1), y + 15, str(v).replace('-', '−'), tam=tam)
    return s, X


def arco_flecha(x1, y, x2, alto, c='g'):
    xm = (x1 + x2) / 2
    a = math.atan2(alto, (x2 - x1) / 2)
    return (f'<path class="{c}" d="M{x1} {y}Q{xm} {y - 2 * alto} {x2} {y}" stroke-width="2" fill="none"/>'
            + f'<path class="f{c}" d="M{x2} {y}L{x2 - 7 * math.cos(a) - 3 * math.sin(a):.1f} {y - 7 * math.sin(a) + 3 * math.cos(a) - 6:.1f}L{x2 - 1:.1f} {y - 8:.1f}Z"/>')


# =====================================================================
# Números
# =====================================================================
def signos():
    s, X = recta_num(14, 184, 54, -4, 9, [-4, 0, 5, 8])
    return svg(s, fl(round(X(0), 1), 38, round(X(5), 1), 38, 'a', 3), t(round((X(0) + X(5)) / 2, 1), 30, '+5', c='a'),
               fl(round(X(5), 1), 38, round(X(8), 1), 38, 'g', 3), t(round((X(5) + X(8)) / 2, 1), 30, '−(−3)', c='g'),
               circ(round(X(8), 1), 54, 5, 'fg'), t(100, 90, 'restar un negativo = avanzar'))


def fracciones():
    return svg(barra(4, 14, 52, 18, 2, 1, 'a'), *[ln(round(4 + 52 * i / 6, 1), 14, round(4 + 52 * i / 6, 1), 32, 'm', .8, '2 2') for i in (1, 2, 4, 5)],
               t(64, 28, '+'), barra(72, 14, 52, 18, 3, 1, 'b'), *[ln(round(72 + 52 * i / 6, 1), 14, round(72 + 52 * i / 6, 1), 32, 'm', .8, '2 2') for i in (1, 3, 5)],
               t(133, 28, '='), barra(142, 14, 52, 18, 6, 3, 'a') + rel(142 + 52 * 3 / 6, 14, 52 * 2 / 6, 18, 'b'),
               t(30, 50, '3/6'), t(98, 50, '2/6'), t(168, 50, '5/6', c='g'),
               t(100, 76, 'mismo denominador primero'), t(100, 90, '2/5 sería menor que 1/2', c='r', tam=11))


def fraccion_resto():
    return svg(barra(20, 22, 160, 24, 4, 3, 'a'), equis(40, 34), t(100, 14, 'tiene 3/4'), t(40, 62, 'usa 1 de 3', c='r', tam=11),
               t(110, 62, 'quedan 2 de 4', c='g', tam=11), t(100, 86, 'queda 2/4 = 1/2'))


def cambios_seguidos():
    filas = [(100, 'a', '100'), (110, 'g', '× 1,1 = 110'), (99, 'r', '× 0,9 = 99')]
    s = ''.join(rel(6, 8 + 28 * i, w, 16, c, .6) + t(116, 21 + 28 * i, et, 'start') for i, (w, c, et) in enumerate(filas))
    return svg(s, ln(106, 4, 106, 84, 'm', 1.5, '3 3'), t(106, 92, '100', tam=10))


def precio_original():
    s = ''.join(rel(10 + 36 * i, 22, 36, 22, 'a', .55) for i in range(4)) + marco(10, 22, 180, 22) + ''.join(ln(10 + 36 * i, 22, 10 + 36 * i, 44, 'm', 1.5) for i in range(1, 5))
    s += ''.join(t(28 + 36 * i, 58, '3.000', tam=10) for i in range(5))
    return svg(s, t(82, 15, '80 % = $12.000', c='a'), t(172, 37, '20 %', tam=10), t(100, 84, '100 % = 5 · 3.000 = $15.000'))


def porcentaje_de_que():
    s = ''.join(rel(8 + 30 * i, 20, 30, 20, 'a', .5) for i in range(5)) + rel(158, 20, 30, 20, 'g', .7)
    s += marco(8, 20, 180, 20) + ''.join(ln(8 + 30 * i, 20, 8 + 30 * i, 40, 'm', 1.5) for i in range(1, 6))
    return svg(s, t(83, 14, '50 = 5 bloques de 10'), t(173, 14, '+10', c='g'), t(100, 62, '10 es 1 de los 5 bloques de 50'), t(100, 82, '10/50 = 20 %', c='g'))


def exponente_negativo():
    pot = ['2³', '2²', '2¹', '2⁰', '2⁻¹', '2⁻²', '2⁻³']
    val = ['8', '4', '2', '1', '1/2', '1/4', '1/8']
    s = ''.join(t(16 + 28 * i, 22, p_) + t(16 + 28 * i, 48, v, c='g' if i == 6 else None) for i, (p_, v) in enumerate(zip(pot, val)))
    s += ''.join(t(30 + 28 * i, 66, '÷2', tam=10, c='m') for i in range(6))
    return svg(s, marco(169, 32, 30, 22, 'g', 2), t(100, 88, 'cada paso a la derecha: ÷ 2'))


def raiz_suma():
    A, B, C = (40, 80), (120, 80), (40, 20)
    return svg(poly([A, B, C], 'a', 'acc', .15), ln(40, 70, 50, 70, 'm', 1.5) + ln(50, 70, 50, 80, 'm', 1.5),
               t(80, 92, '√16 = 4', tam=11), t(36, 54, '√9 = 3', 'end', tam=11), t(84, 44, '√25 = 5', 'start', c='w', tam=11),
               t(164, 34, '3 + 4 = 7', tam=11), t(164, 56, 'el atajo', tam=11), t(164, 70, 'mide 5', c='w', tam=11))


def multiplicar_potencias():
    s = ''.join(caja(10 + 20 * i, 26, 17, 20, 'a') + t(18.5 + 20 * i, 41, 'a') for i in range(3))
    s += ''.join(caja(82 + 20 * i, 26, 17, 20, 'b') + t(90.5 + 20 * i, 41, 'a') for i in range(5))
    return svg(s, t(38, 18, 'a³', c='a'), t(130, 18, 'a⁵', c='b'), t(74, 41, '·'), t(100, 70, '3 + 5 = 8 factores'), t(100, 88, 'a⁸ (no a¹⁵)', c='g'))


# =====================================================================
# Álgebra
# =====================================================================
def cuadrado_suma(a_, b_, ea, eb, eab, txt):
    x, y, A, B = 16, 4, 52, 30
    s = rel(x, y, A, A, 'a', .45) + rel(x + A, y, B, A, 'w', .45) + rel(x, y + A, A, B, 'w', .45) + rel(x + A, y + A, B, B, 'b', .5)
    s += marco(x, y, A + B, A + B, 'm', 2) + ln(x + A, y, x + A, y + A + B, 'm', 1.5) + ln(x, y + A, x + A + B, y + A, 'm', 1.5)
    s += t(x + A / 2, y + A / 2 + 5, ea) + t(x + A + B / 2, y + A / 2 + 5, eab, tam=11) + t(x + A / 2, y + A + B / 2 + 5, eab, tam=11) + t(x + A + B / 2, y + A + B / 2 + 5, eb, tam=11)
    return s, txt


def producto_notable():
    s, _ = cuadrado_suma('a', 'b', 'a²', 'b²', 'ab', '')
    return svg(s, t(150, 34, '(a + b)² ='), t(150, 54, 'a² + 2ab + b²', c='g'), t(150, 72, 'dos rectángulos', tam=11), t(150, 86, 'iguales: 2ab', tam=11))


def cuadrado_trampa():
    s, _ = cuadrado_suma('x', '3', 'x²', '9', '3x', '')
    return svg(s, marco(68, 4, 30, 52, 'r', 2.5) + marco(16, 56, 52, 30, 'r', 2.5), t(150, 30, 'x² + 9 olvida', c='r', tam=11),
               t(150, 44, 'los rectángulos', c='r', tam=11), t(150, 68, 'x² + 6x + 9', c='g'))


def balanza():
    return svg(ln(20, 40, 180, 40, 'm', 3), poly([(100, 42), (90, 60), (110, 60)], 'm', 'muted', .5),
               caja(20, 18, 64, 20, 'a'), t(52, 33, '2x + 3'), caja(124, 18, 48, 20, 'b'), t(148, 33, '11'),
               t(100, 76, 'lo mismo a ambos lados:'), t(100, 90, '−3 → 2x = 8 → ÷2 → x = 4', c='g', tam=11))


def inecuacion():
    s, X = recta_num(14, 186, 50, -7, 1, [-6, -3, 0])
    return svg(s, ln(14, 50, round(X(-3), 1) - 5, 50, 'g', 5), fl(40, 50, 14, 50, 'g', 5),
               f'<circle class="g" cx="{X(-3):.1f}" cy="50" r="5" stroke-width="2.5" style="fill:var(--panel2)"/>',
               t(56, 26, 'x &lt; −3', c='g'), t(150, 26, '−2x &gt; 6', tam=11), t(100, 88, '÷(−2) da vuelta el signo'))


def sistema():
    return svg(ln(20, 64, 180, 8, 'a', 3), ln(20, 10, 180, 62, 'b', 3), circ(100, 36, 5, 'fw'),
               t(100, 78, 'el cruce (x, y) es la solución', tam=11))


def afin():
    X = lambda x: 30 + x * 30
    Y = lambda y: 78 - y * 12
    s = fl(10, 78, 194, 78, 'm', 1.8) + fl(30, 88, 30, 4, 'm', 1.8)
    s += ln(X(-0.3), Y(1.4), X(5), Y(5.375), 'a', 3) + ln(X(0), Y(0), X(5), Y(3.75), 'b', 2, '5 4')
    s += ln(X(1), Y(2.5), X(3), Y(2.5), 'w', 2, '3 3') + ln(X(3), Y(2.5), X(3), Y(4), 'w', 2, '3 3')
    return svg(s, circ(X(0), Y(2), 4.5, 'fw'), t(36, Y(2) - 6, 'n', 'start', c='w'), t(X(2), Y(2.5) + 13, 'Δx', tam=11), t(X(3) + 4, Y(3.25) + 4, 'Δy', 'start', tam=11),
               t(194, 14, 'y = mx + n', 'end', c='a'), t(194, 68, 'lineal: n = 0', 'end', c='b', tam=11))


def cuadratica():
    X = lambda x: 46 + x * 30
    Y = lambda y: 60 - y * 12
    f = lambda x: x * x - 4 * x + 3
    s = fl(8, 60, 196, 60, 'm', 1.8) + fl(46, 88, 46, 4, 'm', 1.8)
    s += curva([(X(x), Y(f(x))) for x in [-0.2 + 4.4 * i / 60 for i in range(61)]], 'a', 3)
    s += circ(X(1), 60, 4.5, 'fg') + circ(X(3), 60, 4.5, 'fg') + circ(X(2), Y(-1), 4.5, 'fr') + circ(46, Y(3), 4.5, 'fw')
    return svg(s, t(X(2), 84, 'vértice', c='r', tam=11), t(X(2), 54, 'ceros', c='g', tam=11), t(40, Y(3) + 4, 'c', 'end', c='w'),
               t(196, 14, 'a &gt; 0: abre ∪', 'end', tam=11))


def vertice_trampa():
    X = lambda x: 30 + x * 22
    Y = lambda y: 48 - y * 7.5
    f = lambda x: x * x - 6 * x + 5
    s = fl(8, 48, 196, 48, 'm', 1.8) + fl(30, 90, 30, 4, 'm', 1.8)
    s += curva([(X(x), Y(f(x))) for x in [-0.05 + 6.1 * i / 80 for i in range(81)]], 'a', 3)
    s += ln(X(3), 4, X(3), 88, 'w', 1.8, '4 3') + circ(X(3), Y(-4), 4.5, 'fr') + circ(X(1), 48, 4, 'fg') + circ(X(5), 48, 4, 'fg')
    return svg(s, t(X(3) + 6, 16, 'x = 3', 'start', c='w'), t(X(1), 42, '1', tam=11), t(X(5), 42, '5', tam=11),
               t(194, 72, 'a mitad de', 'end', tam=11), t(194, 86, 'los ceros', 'end', tam=11))


def discriminante():
    def mini(x0, desplaz, c, et1, et2):
        s = ln(x0, 56, x0 + 58, 56, 'm', 1.8)
        s += curva([(x0 + 29 + u, 56 + desplaz - 0.05 * u * u) for u in range(-26, 27)], c, 2.5)  # ∪ con vértice bajo, en o sobre el eje
        return s + t(x0 + 29, 88, et1 + ' ' + et2, c=c, tam=10)
    return svg(mini(4, 14, 'g', '&gt; 0:', '2 cortes'), mini(71, 0, 'w', '= 0:', '1 toque'), mini(138, -16, 'r', '&lt; 0:', 'no corta'),
               t(100, 12, 'b² − 4ac', tam=11))


def directa():
    X = lambda x: 24 + x * 36
    Y = lambda y: 80 - y * 10
    s = ejes(x0=24, y0=80, w=160, h=74, tx_='x', ty='y') + ln(24, 80, X(3.9), Y(7.8), 'a', 3)
    s += ''.join(circ(X(x), Y(2 * x), 4, 'fw') for x in (1, 2, 3))
    return svg(s, t(150, 70, 'y/x = 2 siempre', tam=11), t(150, 56, 'pasa por (0, 0)', tam=11))


def inversa():
    X = lambda x: 20 + x * 20
    Y = lambda y: 82 - y * 9.5
    s = ejes(x0=20, y0=82, w=170, h=80, tx_='x', ty='y')
    s += rel(20, Y(6), 40, 82 - Y(6), 'a', .3) + rel(20, Y(2), 120, 82 - Y(2), 'b', .3)
    s += curva([(X(x), Y(12 / x)) for x in [1.6 + 6.4 * i / 60 for i in range(61)]], 'w', 3)
    return svg(s, circ(X(2), Y(6), 4, 'fa'), circ(X(6), Y(2), 4, 'fb'), t(120, 24, 'x · y = 12', 'start'), t(120, 38, 'misma área', 'start', tam=11))


def crecer_no_basta():
    X = lambda x: 26 + x * 40
    Y = lambda y: 82 - y * 9
    s = ejes(x0=26, y0=82, w=160, h=78, tx_='x', ty='y')
    s += ln(26, 82, X(3.6), Y(7.2), 'g', 3) + ln(26, Y(1), X(3.4), Y(7.8), 'r', 3) + circ(26, 82, 4, 'fg') + circ(26, Y(1), 4, 'fr')
    return svg(s, t(186, 58, 'y = 2x', 'end', c='g', tam=11), t(186, 72, 'y = 2x + 1', 'end', c='r', tam=11))


# =====================================================================
# Geometría
# =====================================================================
def areas():
    return svg(marco(10, 20, 80, 56, 'm', 1.6, '4 3'), poly([(10, 76), (90, 76), (62, 20)], 'a', 'acc', .35),
               ln(62, 20, 62, 76, 'w', 1.6, '3 3'), t(66, 52, 'h', 'start', c='w'), t(50, 90, 'b', c='a'),
               t(50, 12, 'b · h / 2', tam=11),
               aro(150, 46, 28, 'b', 2.5), ln(150, 46, 178, 46, 'w', 2.5), circ(150, 46, 3, 'fw'), t(164, 40, 'r', c='w'), t(150, 90, 'A = πr²'))


def cilindro():
    return svg(caja(14, 30, 88, 32, 'a'), aro(58, 16, 14, 'b', 2.5), aro(58, 76, 14, 'b', 2.5),
               t(58, 51, '2πr', c='a'), t(105, 50, 'h', 'start'), t(157, 34, 'tapas: 2πr²', c='b', tam=11), t(157, 52, 'manto: 2πr·h', c='a', tam=11),
               t(157, 76, 'V = πr²·h', tam=11))


def radio_diametro():
    return svg(aro(60, 46, 34, 'a', 2.5), ln(26, 46, 94, 46, 'r', 2.5), t(60, 62, 'd = 10', c='r', tam=11),
               ln(60, 46, 60, 12, 'g', 2.5), t(64, 28, 'r = 5', 'start', c='g', tam=11),
               t(150, 40, 'A = π · 5²'), t(150, 60, '= 25π', c='g'))


def trapecio():
    A, B, C, D = (10, 70), (70, 70), (55, 30), (25, 30)
    A2, D2 = (115, 30), (100, 70)
    return svg(poly([A, B, C, D], 'a', 'acc', .4), poly([B, D2, A2, C], 'b', 'acc2', .3), t(55, 86, 'B + b', tam=11),
               ln(122, 30, 122, 70, 'w', 1.6, '3 3'), t(126, 54, 'h', 'start', c='w'),
               t(100, 14, '2 trapecios iguales = paralelogramo', tam=10.5), t(170, 58, '÷ 2', c='g'))


def m2_cm2():
    s = marco(14, 8, 76, 76, 'a', 2.5) + ''.join(ln(round(14 + 7.6 * i, 1), 8, round(14 + 7.6 * i, 1), 84, 'm', .6) + ln(14, round(8 + 7.6 * i, 1), 90, round(8 + 7.6 * i, 1), 'm', .6) for i in range(1, 10))
    return svg(s, t(150, 30, '1 m = 100 cm'), t(150, 52, '100 · 100'), t(150, 72, '= 10.000 cm²', c='g'))


def pitagoras():
    C, A, B = (60, 58), (60, 34), (92, 58)
    return svg(poly([A, B, C], 'm', 'muted', .2), poly([(36, 34), (60, 34), (60, 58), (36, 58)], 'a', 'acc', .4),
               poly([(60, 58), (92, 58), (92, 90), (60, 90)], 'b', 'acc2', .4), poly([A, B, (116, 26), (84, 2)], 'w', 'warn', .4),
               t(48, 50, '9', tam=11), t(76, 78, '16', tam=11), t(88, 32, '25', tam=11),
               t(156, 40, '9 + 16 = 25'), t(156, 62, 'a² + b² = c²', c='g', tam=11))


def semejanza():
    big = poly([(70, 82), (130, 82), (100, 30)], 'b', 'acc2', .3) + poly([(100, 82), (85, 56), (115, 56)], 'b', None)
    return svg(poly([(10, 82), (40, 82), (25, 56)], 'a', 'acc', .45), t(25, 50, 'k = 1', tam=11), big, t(100, 22, 'k = 2', tam=11),
               t(166, 34, 'lados ×2', tam=11), t(166, 52, 'área ×4', c='g', tam=11), t(166, 70, 'volumen ×8', tam=11))


def cateto():
    A, B, C = (30, 82), (110, 82), (30, 22)
    return svg(poly([A, B, C], 'a', 'acc', .15), ln(30, 72, 40, 72, 'm', 1.5) + ln(40, 72, 40, 82, 'm', 1.5),
               t(26, 56, '3', 'end'), t(70, 46, '5', 'start', c='w'), t(70, 76, '?', c='r'),
               t(158, 34, 'hipotenusa: 5', tam=11), t(158, 54, '? = √(25 − 9)', tam=11), t(158, 74, '= 4', c='g'))


def escala():
    return svg(caja(8, 10, 70, 52, 'm'), curva([(14, 50), (30, 30), (48, 40), (70, 18)], 'a', 2.5), circ(14, 50, 3, 'fr'), circ(70, 18, 3, 'fr'),
               ln(100, 40, 180, 40, 'w', 3), *[ln(x, 34, x, 46, 'w', 2) for x in (100, 140, 180)],
               t(100, 30, '0', tam=10), t(140, 30, '1 cm', tam=10), t(180, 30, '2 cm', tam=10),
               t(140, 60, '500 m', tam=10), t(180, 60, '1 km', tam=10), t(100, 86, '1 : 50.000 → 1 cm = 500 m'))


def unidades_escala():
    return svg(caja(4, 8, 74, 22, 'a'), t(41, 23, '400.000 cm', tam=11), fl(80, 19, 104, 19, 'm', 2), t(92, 12, '÷100', tam=10),
               caja(106, 8, 64, 22, 'b'), t(138, 23, '4.000 m', tam=11), fl(138, 32, 138, 52, 'm', 2), t(158, 46, '÷1.000', 'start', tam=10),
               caja(110, 54, 56, 22, 'g'), t(138, 69, '4 km', tam=11), t(52, 70, 'no 40 km', c='r'))


def transformaciones():
    X = lambda x: 58 + 9 * x
    Y = lambda y: 46 - 9 * y
    g = ''.join(ln(X(i), 4, X(i), 88, 'm', .5) for i in range(-5, 6)) + ''.join(ln(10, Y(j), 106, Y(j), 'm', .5) for j in range(-4, 5))
    g += ln(10, 46, 106, 46, 'm', 1.6) + ln(58, 4, 58, 88, 'm', 1.6)
    pts = [((4, 2), 'fa', 'a', 'P'), ((4, -2), 'fb', 'b', 'X'), ((-4, 2), 'fw', 'w', 'Y'), ((-2, 4), 'fg', 'g', '90°'), ((-4, -2), 'fr', 'r', '180°')]
    s = g + ''.join(circ(X(x), Y(y), 3.8, f) + t(X(x) + 5, Y(y) - 4, et, 'start', c=c, tam=10) for (x, y), f, c, et in pts)
    reglas = [('a', 'P (x, y)'), ('b', 'eje X: (x, −y)'), ('w', 'eje Y: (−x, y)'), ('g', '90°: (−y, x)'), ('r', '180°: (−x, −y)')]
    s += ''.join(t(114, 16 + 17 * i, r, 'start', c=c, tam=11) for i, (c, r) in enumerate(reglas))
    return svg(s)


def reflejo_y():
    X = lambda x: 70 + 10 * x
    Y = lambda y: 84 - 12 * y
    s = ln(20, 84, 120, 84, 'm', 1.6) + ln(70, 6, 70, 90, 'w', 2.5) + ln(X(-3), Y(5), X(3), Y(5), 'm', 1.5, '3 3')
    return svg(s, circ(X(3), Y(5), 4.5, 'fa'), circ(X(-3), Y(5), 4.5, 'fg'), t(X(3) + 4, Y(5) + 18, '(3, 5)', tam=11), t(X(-3) - 4, Y(5) + 18, '(−3, 5)', c='g', tam=11),
               t(74, 76, 'eje Y', 'start', c='w', tam=10), t(160, 40, 'cambia la x', tam=11), t(160, 56, '(la que mide', tam=11), t(160, 70, 'al eje Y)', tam=11))


def giro():
    X = lambda x: 60 + 12 * x
    Y = lambda y: 64 - 12 * y
    s = ln(6, 64, 120, 64, 'm', 1.6) + ln(60, 4, 60, 90, 'm', 1.6)
    s += ln(60, 64, X(4), Y(1), 'a', 2) + ln(60, 64, X(-1), Y(4), 'g', 2)
    s += '<path class="w" d="M96 48A40 40 0 0 0 64 26" stroke-width="2.5" fill="none"/>' + '<path class="fw" d="M58 25L66 21L66 30Z"/>'
    return svg(s, circ(X(4), Y(1), 4.5, 'fa'), circ(X(-1), Y(4), 4.5, 'fg'), t(X(4) + 4, Y(1) + 16, '(4, 1)', tam=11), t(X(-1) - 4, Y(4) - 2, '(−1, 4)', 'end', c='g', tam=11),
               t(160, 34, 'antihorario', c='w', tam=11), t(160, 52, '(x, y) → (−y, x)', tam=11))


# =====================================================================
# Probabilidad y estadística
# =====================================================================
def cajon():
    s = ln(20, 48, 60, 48, 'm', 2.5) + ln(130, 48, 180, 48, 'm', 2.5) + ln(20, 38, 20, 58, 'm', 2.5) + ln(180, 38, 180, 58, 'm', 2.5)
    s += f'<rect class="a" x="60" y="34" width="70" height="28" stroke-width="2.5" style="fill:var(--acc);fill-opacity:.25"/>' + ln(88, 34, 88, 62, 'w', 3)
    s += ''.join(t(x, 24, e, tam=10.5) for x, e in ((20, 'mín'), (60, 'Q₁'), (88, 'Q₂'), (130, 'Q₃'), (180, 'máx')))
    s += ''.join(t(x, 78, '25 %', tam=10) for x in (40, 74, 109, 155))
    return svg(s, t(100, 92, 'la línea de la caja es la mediana', c='w', tam=10.5))


def mediana_orden():
    return svg(t(20, 30, '9', tam=16), t(46, 30, '2', tam=16), t(72, 30, '7', tam=16), ln(10, 24, 82, 24, 'r', 2),
               fl(96, 24, 116, 24, 'm', 2), t(106, 16, 'ordena', tam=10),
               t(132, 30, '2', tam=16), t(158, 30, '7', c='g', tam=16), t(184, 30, '9', tam=16), aro(158, 24, 12, 'g', 2),
               t(100, 66, 'la mediana es el dato del medio'), t(100, 84, 'de los datos ordenados', tam=11))


def promedio():
    s, X = recta_num(14, 186, 56, 0, 10, [0, 2, 4, 9, 10])
    return svg(s, circ(round(X(2), 1), 44, 6, 'fa'), circ(round(X(4), 1), 44, 6, 'fa'), circ(round(X(9), 1), 44, 6, 'fa'),
               poly([(X(5), 57), (X(5) - 8, 71), (X(5) + 8, 71)], 'w', 'warn', .8),
               t(100, 20, 'promedio = punto de equilibrio', tam=11), t(100, 90, '(2 + 4 + 9)/3 = 5', c='w', tam=11))


def arbol_monedas():
    s = circ(12, 46, 4, 'fm') + ln(12, 46, 56, 24, 'm', 2) + ln(12, 46, 56, 68, 'm', 2)
    s += t(62, 28, 'C', tam=11) + t(62, 72, 'S', tam=11)
    hojas = [(12, 'CC', None), (34, 'CS', 'g'), (58, 'SC', 'g'), (80, 'SS', None)]
    for y, e, c in hojas:
        s += ln(70, 24 if e[0] == 'C' else 68, 108, y, 'g' if c else 'm', 2) + t(114, y + 4, e, 'start', c=c, tam=11)
    return svg(s, t(170, 40, '2 de 4', c='g'), t(170, 60, '= 1/2', c='g'))


def arbol_y():
    s = circ(12, 46, 4, 'fm') + ln(12, 46, 70, 24, 'r', 3) + ln(12, 46, 70, 68, 'm', 1.5)
    s += ln(78, 24, 136, 10, 'r', 3) + ln(78, 24, 136, 38, 'm', 1.5)
    return svg(s, t(36, 26, '5/10', c='r', tam=11), t(108, 10, '4/9', c='r', tam=11), circ(74, 24, 4, 'fr'), circ(140, 10, 4, 'fr'),
               t(176, 14, 'roja y roja', tam=10), t(100, 80, '«y»: multiplica en la rama'), t(100, 92, '5/10 · 4/9', c='r', tam=11))


def urna():
    def frasco(x, rojas, azules):
        s = caja(x, 16, 64, 48, 'm')
        bolas = ['r'] * rojas + ['b'] * azules
        for i, c in enumerate(bolas):
            s += circ(x + 9 + 11.5 * (i % 5), 28 + 13 * (i // 5), 4.5, 'f' + c)
        return s
    return svg(frasco(6, 5, 5), t(38, 80, 'roja: 5/10', c='r', tam=11), fl(76, 40, 120, 40, 'm', 2), t(98, 32, 'saco 1', tam=10),
               frasco(128, 4, 5), t(160, 80, 'roja: 4/9', c='r', tam=11))


def venn_numeros():
    return svg('<circle class="a" cx="72" cy="44" r="34" stroke-width="2.5" style="fill:var(--acc);fill-opacity:.2"/>',
               '<circle class="b" cx="122" cy="44" r="34" stroke-width="2.5" style="fill:var(--acc2);fill-opacity:.2"/>',
               t(60, 49, '13'), t(97, 49, '5', c='w'), t(136, 49, '7'), t(60, 90, 'fútbol 18', c='a', tam=10.5), t(140, 90, 'básquet 12', c='b', tam=10.5),
               t(97, 8, 'ambos: se cuentan 1 vez', c='w', tam=10))


def venn():
    return svg('<circle class="a" cx="60" cy="46" r="30" stroke-width="2.5" style="fill:var(--acc);fill-opacity:.2"/>',
               '<circle class="b" cx="100" cy="46" r="30" stroke-width="2.5" style="fill:var(--acc2);fill-opacity:.2"/>',
               t(46, 51, 'A'), t(114, 51, 'B'), t(80, 51, '∩', c='w'),
               t(166, 34, '«o»: suma', tam=11), t(166, 52, 'y resta', tam=11), t(166, 70, 'lo común', c='w', tam=11))


# =====================================================================
DIBUJOS = {
    ('m1.num.enteros-racionales', 'Signos'): signos(),
    ('m1.num.enteros-racionales', 'Sumar fracciones «de a pares»'): fracciones(),
    ('m1.num.enteros-racionales', 'Fracción de lo que queda'): fraccion_resto(),
    ('m1.num.porcentaje', 'Cambios seguidos'): cambios_seguidos(),
    ('m1.num.porcentaje', 'Volver al precio original'): precio_original(),
    ('m1.num.porcentaje', '¿Porcentaje de qué?'): porcentaje_de_que(),
    ('m1.num.potencias-raices', 'Exponente negativo'): exponente_negativo(),
    ('m1.num.potencias-raices', 'Raíz de una suma'): raiz_suma(),
    ('m1.num.potencias-raices', 'Multiplicar potencias'): multiplicar_potencias(),
    ('m1.alg.expresiones', 'Productos notables'): producto_notable(),
    ('m1.alg.expresiones', 'El cuadrado de una suma'): cuadrado_trampa(),
    ('m1.alg.ecuaciones', 'Ecuación lineal'): balanza(),
    ('m1.alg.ecuaciones', 'Dividir por un negativo'): inecuacion(),
    ('m1.alg.ecuaciones', 'Sistemas 2×2'): sistema(),
    ('m1.alg.funciones', 'Afín y lineal'): afin(),
    ('m1.alg.funciones', 'Cuadrática'): cuadratica(),
    ('m1.alg.funciones', 'Signo del vértice'): vertice_trampa(),
    ('m1.alg.proporcionalidad', 'Directa'): directa(),
    ('m1.alg.proporcionalidad', 'Inversa'): inversa(),
    ('m1.alg.proporcionalidad', 'Crecer no basta'): crecer_no_basta(),
    ('m1.geo.areas-volumenes', 'Áreas'): areas(),
    ('m1.geo.areas-volumenes', 'Cuerpos'): cilindro(),
    ('m1.geo.areas-volumenes', 'Radio o diámetro'): radio_diametro(),
    ('m1.geo.areas-volumenes', 'El trapecio'): trapecio(),
    ('m1.geo.areas-volumenes', 'Pasar m² a cm²'): m2_cm2(),
    ('m1.geo.semejanza-pitagoras', 'Pitágoras'): pitagoras(),
    ('m1.geo.semejanza-pitagoras', 'Semejanza'): semejanza(),
    ('m1.geo.semejanza-pitagoras', 'Escalas'): escala(),
    ('m1.geo.semejanza-pitagoras', 'Buscar un cateto'): cateto(),
    ('m1.geo.semejanza-pitagoras', 'Unidades de la escala'): unidades_escala(),
    ('m1.geo.transformaciones', 'Reglas'): transformaciones(),
    ('m1.geo.transformaciones', 'Eje X o eje Y'): reflejo_y(),
    ('m1.geo.transformaciones', 'Sentido de giro'): giro(),
    ('m1.pro.datos', 'Tablas y promedio'): promedio(),
    ('m1.pro.datos', 'Cuartiles y cajón'): cajon(),
    ('m1.pro.datos', 'Mediana sin ordenar'): mediana_orden(),
    ('m1.pro.probabilidad', 'Reglas'): arbol_y(),
    ('m1.pro.probabilidad', 'Casos que no son igual de probables'): arbol_monedas(),
    ('m1.pro.probabilidad', 'Contar dos veces'): venn_numeros(),
    ('m1.pro.probabilidad', 'Sin reposición'): urna(),
}

NUEVAS = {
    'm1.alg.funciones': [('dibujo', 'El discriminante en el gráfico',
                          'Cuántas veces la parábola corta el eje X lo dice el signo de b² − 4ac.', discriminante())],
    'm1.pro.probabilidad': [('dibujo', '«O» en un diagrama',
                             'P(A ∪ B) = P(A) + P(B) − P(A ∩ B): si no restas la parte común, la cuentas dos veces.', venn())],
}


# =====================================================================
# Segunda pasada: tarjetas que quedaron sin dibujo
# =====================================================================
def orden_operaciones():
    pasos = [('( )', 'a'), ('xⁿ', 'b'), ('× ÷', 'w'), ('+ −', 'g')]
    s = ''.join(caja(6 + 48 * i, 52 - 14 * i, 42, 24, c) + t(27 + 48 * i, 68 - 14 * i, e, tam=12) + t(27 + 48 * i, 88 - 14 * i, f'{i + 1}.º', tam=10) for i, (e, c) in enumerate(pasos))
    return svg(s, t(6, 12, 'empate: de izquierda a derecha', 'start', tam=8.5))


def arbol_operacion():
    return svg(circ(100, 14, 9, 'fg'), t(100, 18, '+', tam=12), ln(94, 20, 60, 44, 'm', 2), ln(106, 20, 140, 44, 'm', 2),
               t(56, 54, '−3', tam=12), circ(140, 50, 9, 'fw'), t(140, 54, '×', tam=12), ln(134, 56, 112, 76, 'm', 2), ln(146, 56, 168, 76, 'm', 2),
               t(110, 88, '5', tam=12), t(170, 88, '(−2)', tam=12), t(178, 46, '1.º', 'start', c='w', tam=10), t(116, 10, '2.º', 'start', c='g', tam=10))


def multiplicar_fracciones():
    X0, Y0, W, H = 20, 10, 96, 72
    s = rel(X0, Y0, W * 3 / 4, H, 'a', .3) + rel(X0, Y0 + H / 3, W, H * 2 / 3, 'b', .3)
    s += marco(X0, Y0, W, H, 'm', 2) + ''.join(ln(round(X0 + W * i / 4, 1), Y0, round(X0 + W * i / 4, 1), Y0 + H, 'm', 1) for i in range(1, 4))
    s += ''.join(ln(X0, round(Y0 + H * j / 3, 1), X0 + W, round(Y0 + H * j / 3, 1), 'm', 1) for j in (1, 2))
    return svg(s, t(158, 30, '2/3 · 3/4', tam=11), t(158, 50, '= 6/12', c='g', tam=11), t(158, 70, '= 1/2', c='g', tam=11), t(68, 92, 'las dos sombras juntas: 6 de 12', tam=9))


def cien_cuadros():
    s = ''.join(rel(14 + 7.2 * (k % 10), 12 + 7.2 * (k // 10), 6.4, 6.4, 'a' if k < 20 else 'm', .7 if k < 20 else .18) for k in range(100))
    return svg(s, t(150, 34, '20 % =', tam=12), t(150, 52, '20 de cada 100', c='a', tam=11), t(150, 72, '× 0,20', tam=11))


def factorizar():
    return svg(rel(20, 26, 64, 36, 'a', .4), rel(84, 26, 40, 36, 'b', .45), marco(20, 26, 104, 36, 'm', 2), ln(84, 26, 84, 62, 'm', 1.6),
               t(52, 48, '6x²', tam=11), t(104, 48, '9x', tam=11), t(52, 20, '2x', tam=10), t(104, 20, '3', tam=10), t(14, 48, '3x', 'end', tam=10),
               t(160, 40, '3x(2x + 3)', c='g', tam=11), t(160, 58, 'factor común', tam=9.5), t(72, 82, 'el área no cambia', tam=9.5))


def simplificar_suma():
    return svg(t(40, 32, 'x + 3', tam=14), ln(14, 40, 66, 40, 'm', 2), t(40, 58, '3', tam=14), fl(76, 42, 98, 42, 'm', 2),
               t(120, 32, 'x', tam=14), ln(108, 40, 132, 40, 'm', 2), t(120, 58, '3', tam=14), t(144, 46, '+', tam=14),
               t(166, 32, '3', tam=14), ln(154, 40, 178, 40, 'm', 2), t(166, 58, '3', tam=14), t(100, 86, 'el 3 divide a todo el numerador', tam=9.5))


def menos_parentesis():
    return svg(t(24, 50, '−', c='r', tam=16), t(42, 50, '(', tam=16), t(60, 50, 'x', tam=14), t(80, 50, '−', tam=14), t(98, 50, '4', tam=14), t(114, 50, ')', tam=16),
               '<path class="r" d="M26 34Q42 14 58 34" stroke-width="2" fill="none"/>', '<path class="r" d="M26 34Q58 0 92 34" stroke-width="2" fill="none"/>',
               fl(124, 46, 140, 46, 'm', 2), t(170, 50, '−x + 4', c='g', tam=13), t(100, 82, 'el menos cambia el signo de cada término', tam=9))


def distribuir():
    return svg(t(30, 54, '3', c='a', tam=16), t(46, 54, '(', tam=16), t(64, 54, 'x', tam=14), t(84, 54, '−', tam=14), t(102, 54, '2', tam=14), t(118, 54, ')', tam=16),
               '<path class="a" d="M32 36Q48 14 62 36" stroke-width="2" fill="none"/>', '<path class="a" d="M32 36Q68 2 100 36" stroke-width="2" fill="none"/>',
               fl(128, 50, 144, 50, 'm', 2), t(172, 54, '3x − 6', c='g', tam=13), t(100, 84, 'multiplica a los dos términos', tam=9.5))


def pendiente():
    return svg(ln(30, 76, 170, 16, 'a', 3), ln(60, 63.1, 140, 63.1, 'w', 2, '4 3'), ln(140, 63.1, 140, 28.9, 'g', 2.5),
               t(100, 78, 'Δx (avanza)', c='w', tam=10.5), t(146, 50, 'Δy (sube)', 'start', c='g', tam=10.5), t(44, 24, 'm = Δy / Δx', 'start', tam=12))


def trabajadores():
    a = ''.join(rel(10 + 6 * i, 14 + 6.4 * j, 5.2, 5.6, 'a', .55) for i in range(10) for j in range(6))
    b = ''.join(rel(104 + 6 * i, 14 + 6.4 * j, 5.2, 5.6, 'b', .55) for i in range(15) for j in range(4))
    return svg(a, b, t(40, 64, '6 · 10 = 60', tam=10.5), t(149, 50, '4 · 15 = 60', tam=10.5), t(40, 80, '6 trabajadores', tam=9), t(149, 66, '4 trabajadores', tam=9),
               t(100, 92, 'el trabajo total no cambia', tam=9.5))


def litro():
    l = 44
    d = l * 0.45
    cubo_ = (poly([(30, 80), (30 + l, 80), (30 + l, 80 - l), (30, 80 - l)], 'b', 'acc2', .25) + poly([(30, 80 - l), (30 + d, 80 - l - d), (30 + l + d, 80 - l - d), (30 + l, 80 - l)], 'b', 'acc2', .15)
             + poly([(30 + l, 80), (30 + l + d, 80 - d), (30 + l + d, 80 - l - d), (30 + l, 80 - l)], 'b', 'acc2', .1))
    return svg(cubo_, t(52, 92, '10 cm', tam=10), t(52, 64, '1 L', c='b', tam=12), t(150, 34, '10·10·10', tam=11), t(150, 50, '= 1.000 cm³ = 1 L', tam=10.5), t(150, 72, '1 m³ = 1.000 L', c='g', tam=10.5))


def areas_semejantes():
    return svg(marco(16, 56, 22, 22, 'a', 2.5), t(27, 90, 'lado 1', tam=9.5), marco(70, 12, 66, 66, 'b', 2.5),
               *[ln(70 + 22 * i, 12, 70 + 22 * i, 78, 'b', 1.2) + ln(70, 12 + 22 * i, 136, 12 + 22 * i, 'b', 1.2) for i in (1, 2)],
               t(103, 90, 'lado 3', tam=9.5), t(170, 38, 'caben 9', c='g', tam=11), t(170, 56, 'área × 3²', tam=11))


def nota_falta():
    Y = lambda v: 84 - v * 8
    s = ''.join(rel(14 + 28 * i, Y(5.5), 22, 84 - Y(5.5), 'a', .5) for i in range(4)) + rel(128, Y(7), 22, 84 - Y(7), 'g', .6)
    return svg(ln(8, 84, 196, 84, 'm', 1.6), s, ln(8, Y(5.8), 196, Y(5.8), 'w', 1.8, '4 3'), t(196, Y(5.8) - 4, 'meta 5,8', 'end', c='w', tam=9.5),
               t(56, Y(5.5) + 14, '4 notas de 5,5 = 22', tam=9), t(139, Y(7) - 4, '7,0', c='g', tam=11), t(100, 12, '5 · 5,8 = 29 → 29 − 22 = 7', tam=9.5))


def laplace():
    def cara(x, n, fav):
        pos = {1: [(0, 0)], 2: [(-5, -5), (5, 5)], 3: [(-5, -5), (0, 0), (5, 5)], 4: [(-5, -5), (5, -5), (-5, 5), (5, 5)],
               5: [(-5, -5), (5, -5), (0, 0), (-5, 5), (5, 5)], 6: [(-5, -6), (5, -6), (-5, 0), (5, 0), (-5, 6), (5, 6)]}[n]
        return (f'<rect x="{x - 12}" y="20" width="24" height="24" rx="5" class="{"g" if fav else "m"}" stroke-width="2.2" style="fill:var(--{"ok" if fav else "muted"});fill-opacity:{.25 if fav else .08}"/>'
                + ''.join(circ(x + dx, 32 + dy, 2.2, 'fg' if fav else 'fm') for dx, dy in pos))
    return svg(*[cara(20 + 32 * (n - 1), n, n % 2 == 0) for n in range(1, 7)], t(100, 66, 'P(par) = 3 / 6 = 1/2', c='g', tam=11), t(100, 84, 'favorables / posibles', tam=10))


DIBUJOS.update({
    ('m1.num.enteros-racionales', 'Orden de operaciones'): orden_operaciones(),
    ('m1.num.enteros-racionales', 'Sumar antes de multiplicar'): arbol_operacion(),
    ('m1.num.enteros-racionales', 'Fracciones'): multiplicar_fracciones(),
    ('m1.num.porcentaje', 'Lo básico'): cien_cuadros(),
    ('m1.alg.expresiones', 'Factorizar'): factorizar(),
    ('m1.alg.expresiones', 'Simplificar una suma'): simplificar_suma(),
    ('m1.alg.expresiones', 'Menos delante del paréntesis'): menos_parentesis(),
    ('m1.alg.ecuaciones', 'Distribuir'): distribuir(),
    ('m1.alg.funciones', 'Pendiente al revés'): pendiente(),
    ('m1.alg.proporcionalidad', 'Trabajadores y días'): trabajadores(),
    ('m1.geo.areas-volumenes', 'Unidades'): litro(),
    ('m1.geo.semejanza-pitagoras', 'Áreas semejantes'): areas_semejantes(),
    ('m1.pro.datos', 'La nota que falta'): nota_falta(),
    ('m1.pro.probabilidad', 'Laplace'): laplace(),
})
