"""Dibujos (SVG) para las tarjetas de bioquim.html, además del esquema principal de cada tema. Los usa tools/bioquim.py.

DIBUJOS[(id del tema, título de la tarjeta)] = svg  → va dentro de esa tarjeta, después del título.
"""
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from esquemas import aro, caja, circ, curva, fl, ln, poly, puntos, svg  # noqa: E402
from m1_dibujos import marco, rel, t  # noqa: E402


def elipse(cx, cy, rx, ry, c='m', w=2, relleno=None, op=.25):
    st = f' style="fill:var(--{relleno});fill-opacity:{op}"' if relleno else ''
    return f'<ellipse class="{c}" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" stroke-width="{w}"{st}/>'


def redondo(x, y, w, h, r, c='m', w_=2, relleno=None, op=.2):
    st = f' style="fill:var(--{relleno});fill-opacity:{op}"' if relleno else ''
    return f'<rect class="{c}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" stroke-width="{w_}"{st}/>'


def trazo(d, c='m', w=2.5):
    return f'<path class="{c}" d="{d}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'


def vaso(x, y, w, h, nivel, var='acc2', op=.3):
    """Vaso de precipitado: borde abierto arriba y líquido hasta «nivel» (0–1)."""
    liq = rect_(x + 1, y + h - h * nivel, w - 2, h * nivel - 1, var, op)
    return liq + trazo(f'M{x} {y}L{x} {y + h}L{x + w} {y + h}L{x + w} {y}', 'm', 2.2)


def rect_(x, y, w, h, var, op):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" style="fill:var(--{var});fill-opacity:{op}"/>'


def molecula(x, y, partes):
    """partes: [(dx, dy, r, relleno)]"""
    return ''.join(circ(round(x + dx, 1), round(y + dy, 1), r, f) for dx, dy, r, f in partes)


H2O = [(0, 0, 5, 'fr'), (-6, -5, 3.2, 'fm'), (6, -5, 3.2, 'fm')]
O2 = [(-3.5, 0, 4.5, 'fr'), (3.5, 0, 4.5, 'fr')]
H2 = [(-2.6, 0, 3.2, 'fm'), (2.6, 0, 3.2, 'fm')]


# =====================================================================
# Biología
# =====================================================================
def pro_eu():
    bact = redondo(6, 30, 64, 32, 16, 'b', 2.5, 'acc2', .15) + trazo('M70 46Q76 40 82 46T94 46', 'b', 2) + trazo('M22 44Q32 36 42 46T60 44', 'w', 2)
    euc = elipse(158, 46, 36, 30, 'a', 2.5, 'acc', .12) + circ(158, 46, 10, 'fa') + elipse(136, 34, 7, 4, 'g', 1.6) + elipse(178, 60, 7, 4, 'g', 1.6) + elipse(142, 64, 6, 3.5, 'w', 1.6)
    return svg(bact, euc, t(38, 82, 'sin núcleo', tam=10.5), t(38, 22, 'procarionte', c='b', tam=10.5), t(158, 10, 'eucarionte', c='a', tam=10.5), t(158, 90, 'núcleo + organelos', tam=10.5))


def animal_vegetal():
    veg = redondo(6, 10, 84, 70, 4, 'g', 3) + redondo(12, 16, 72, 58, 2, 'g', 1.4) + redondo(30, 26, 40, 38, 8, 'b', 1.6, 'acc2', .25)
    veg += ''.join(elipse(x, y, 6, 3.5, 'g', 1.6, 'ok', .5) for x, y in ((20, 24), (76, 30), (20, 66), (78, 66))) + circ(78, 46, 5, 'fa')
    ani = elipse(150, 44, 40, 34, 'a', 2.5, 'acc', .1) + circ(150, 44, 10, 'fa') + ln(124, 58, 132, 58, 'w', 3) + ln(128, 54, 128, 62, 'w', 3)
    return svg(veg, t(48, 92, 'vegetal', c='g', tam=10.5), ani, t(150, 92, 'animal', c='a', tam=10.5), t(134, 76, 'centriolo', c='w', tam=8.5))


def ruta_proteinas():
    nuc = circ(20, 46, 12, 'fa')
    rer = ''.join(trazo(f'M{40 + 0} {30 + 8 * k}Q{52} {24 + 8 * k} {64} {30 + 8 * k}', 'b', 2) for k in range(4)) + ''.join(circ(44 + 6 * k, 29, 1.6, 'fm') for k in range(4))
    golgi = ''.join(trazo(f'M{112} {28 + 8 * k}Q{126} {20 + 8 * k + (k * 1.5)} {140} {28 + 8 * k}', 'w', 2.5) for k in range(4))
    return svg(nuc, rer, golgi, fl(66, 46, 98, 46, 'm', 1.8), circ(84, 46, 3.5, 'fg'), fl(142, 46, 172, 46, 'm', 1.8), circ(158, 46, 3.5, 'fg'),
               ln(186, 14, 186, 78, 'm', 3), t(20, 76, 'núcleo', tam=10), t(52, 76, 'RER', c='b', tam=10.5), t(126, 76, 'Golgi', c='w', tam=10.5),
               t(186, 90, 'sale', 'end', tam=10), t(84, 36, 'vesícula', tam=9))


def snc_snp():
    cuerpo = circ(60, 16, 11, 'fa') + ln(60, 27, 60, 70, 'a', 4)
    nervios = (ln(60, 36, 30, 58, 'b', 2) + ln(60, 36, 90, 58, 'b', 2) + ln(60, 70, 44, 90, 'b', 2) + ln(60, 70, 76, 90, 'b', 2)
               + ln(60, 50, 36, 72, 'b', 1.5) + ln(60, 50, 84, 72, 'b', 1.5))
    return svg(nervios, cuerpo, t(150, 30, 'SNC: encéfalo', c='a', tam=11), t(150, 44, 'y médula', c='a', tam=11), t(150, 68, 'SNP: nervios', c='b', tam=11))


def potencial_accion():
    Y = lambda mv: 70 - (mv + 80) * 0.55
    pts = [(10, Y(-70)), (50, Y(-70)), (60, Y(-55))]
    pts += [(60 + u, Y(-55 + 85 * (u / 12))) for u in range(1, 13)]
    pts += [(72 + u, Y(30 - 110 * (u / 18))) for u in range(1, 19)]
    pts += [(90 + u, Y(-80 + 10 * (u / 30))) for u in range(1, 31)] + [(190, Y(-70))]
    return svg(ln(10, Y(-55), 190, Y(-55), 'w', 1.4, '4 3'), curva(pts, 'a', 3), t(196, Y(-55) - 3, 'umbral', 'end', c='w', tam=9.5),
               t(44, 22, 'entra Na⁺', 'middle', c='g', tam=10), t(118, 22, 'sale K⁺', 'middle', c='r', tam=10), t(26, 84, '−70 mV', 'middle', tam=10),
               t(72, 8, '+30', 'middle', tam=9.5))


def sinapsis():
    term = trazo('M6 20Q70 20 76 46Q70 72 6 72', 'a', 3) + ''.join(aro(x, y, 5, 'a', 1.6) for x, y in ((36, 36), (50, 52), (32, 58)))
    nt = ''.join(circ(x, y, 2.2, 'fw') for x, y in ((84, 38), (90, 50), (86, 58), (94, 42)))
    post = trazo('M110 14Q104 46 110 78', 'b', 3) + ''.join(caja(106, y, 8, 6, 'b') for y in (32, 44, 56))
    return svg(term, nt, post, fl(124, 46, 158, 46, 'g', 2.5), t(40, 88, 'vesículas', tam=10), t(92, 10, 'neurotransmisor', tam=10), t(176, 40, 'señal', tam=10.5), t(176, 54, 'nueva', tam=10.5))


def arco_reflejo():
    return svg(circ(14, 66, 6, 'fw'), t(14, 86, 'receptor', tam=9.5), trazo('M20 62Q60 20 96 34', 'b', 2.5), redondo(96, 22, 22, 30, 6, 'a', 2.5, 'acc', .2), t(107, 16, 'médula', tam=10),
               trazo('M118 44Q150 70 172 66', 'r', 2.5), redondo(172, 56, 22, 18, 6, 'r', 2), t(183, 86, 'músculo', tam=9.5),
               t(56, 22, 'sensitiva', c='b', tam=10), t(146, 76, 'motora', c='r', tam=10))


def gametos():
    esp = elipse(24, 46, 9, 6, 'a', 2, 'acc', .3) + elipse(19, 46, 3, 5, 'w', 1.6) + ln(33, 46, 42, 46, 'w', 3.5) + trazo('M42 46Q50 38 58 46T74 46T90 46', 'a', 2)
    ovo = circ(150, 46, 34, 'fw') + aro(150, 46, 38, 'm', 2) + circ(150, 46, 9, 'fa')
    return svg(esp, ovo, t(48, 74, 'espermatozoide', tam=10), t(48, 86, 'chico, con flagelo', tam=9.5), t(150, 90, 'ovocito: grande, inmóvil', tam=9.5), t(20, 30, 'acrosoma', tam=9))


def fecundacion():
    utero = trazo('M80 30L120 30L112 70L88 70Z', 'm', 2.5)
    trompa = trazo('M80 32Q50 14 26 30', 'a', 3) + trazo('M120 32Q150 14 174 30', 'a', 3)
    return svg(utero, trompa, circ(20, 38, 7, 'fw'), circ(180, 38, 7, 'fw'), circ(46, 22, 4, 'fr'), trazo('M60 64Q54 48 48 30', 'b', 1.6), fl(60, 66, 52, 38, 'b', 1.6),
               t(46, 12, 'aquí: trompa', c='r', tam=10), t(20, 56, 'ovario', tam=9.5), t(100, 54, 'útero', tam=10), t(100, 88, 'cigoto → útero (implantación)', tam=9.5))


def ciclo_ovarico():
    ln_ = ln(10, 70, 190, 70, 'm', 1.6) + ln(100, 14, 100, 70, 'r', 1.4, '3 3')
    foli = ''.join(aro(18 + 18 * k, 56, 3 + 2.2 * k, 'a', 1.8) for k in range(5))
    lut = circ(140, 52, 12, 'fw') + circ(170, 54, 8, 'fw')
    return svg(ln_, foli, circ(100, 44, 4, 'fr'), fl(104, 40, 118, 28, 'r', 1.8), lut, t(54, 86, 'folicular (FSH)', tam=10), t(100, 10, 'ovulación (LH)', c='r', tam=10),
               t(155, 86, 'lútea', tam=10), t(155, 34, 'cuerpo lúteo', c='w', tam=9.5))


def ciclo_uterino():
    X = lambda d: 10 + d * 6.4
    pts = [(X(d), 60 + 18 * (d - 0) / 5) for d in (0, 5)] + [(X(d), 78 - 40 * ((d - 5) / 9)) for d in range(6, 15)] + [(X(d), 38 - 20 * ((d - 14) / 10)) for d in range(15, 25)] + [(X(26), 30), (X(28), 62)]
    return svg(ln(10, 80, 190, 80, 'm', 1.6), curva(pts, 'r', 3), *[ln(X(d), 14, X(d), 80, 'm', 1, '3 3') for d in (5, 14)],
               t(X(2.5), 12, 'regla', tam=9.5), t(X(9.5), 12, 'prolifera', tam=9.5), t(X(21), 12, 'secretora', tam=9.5), t(100, 92, 'grosor del endometrio · días 1 a 28', tam=9.5))


def temp_basal():
    pts = [(10 + 6.4 * d, 66 + (2 if d % 3 else -2) - (22 if d > 14 else 0)) for d in range(0, 29)]
    return svg(ln(10, 80, 190, 80, 'm', 1.6), curva(pts, 'w', 2.5), ln(100, 14, 100, 80, 'r', 1.4, '3 3'), t(100, 10, 'ovulación', c='r', tam=10),
               t(150, 30, 'sube ~0,3 °C', tam=10), t(50, 54, 'temperatura', tam=10), t(100, 92, 'días del ciclo', tam=9.5))


def barrera():
    return svg(trazo('M150 20Q186 46 150 72', 'w', 3), circ(176, 46, 10, 'fw'), ln(120, 14, 120, 78, 'r', 4),
               *[trazo(f'M{20 + 18 * k} {30 + 12 * (k % 3)}q6 -6 12 0', 'a', 2) + circ(34 + 18 * k, 30 + 12 * (k % 3), 3.5, 'fa') for k in range(5)],
               t(120, 90, 'barrera', c='r', tam=10), t(176, 90, 'ovocito', tam=10))


def hormonal():
    return svg(elipse(50, 46, 32, 22, 'w', 2.5, 'warn', .15), *[aro(x, 46, 6, 'w', 1.6) for x in (36, 52, 66)], fl(84, 46, 124, 46, 'm', 2),
               circ(146, 46, 10, 'fw'), ln(134, 34, 158, 58, 'r', 3), ln(158, 34, 134, 58, 'r', 3), t(50, 84, 'ovario', tam=10), t(146, 84, 'no hay ovulación', c='r', tam=10))


def quirurgico():
    return svg(trazo('M10 46L80 46', 'a', 4), trazo('M110 46L190 46', 'a', 4), ln(84, 34, 84, 58, 'r', 2.5), ln(106, 34, 106, 58, 'r', 2.5),
               t(95, 24, 'cortado y atado', c='r', tam=10), t(100, 76, 'conducto deferente o trompa', tam=10), t(100, 90, 'no pasan los gametos', tam=10))


def cromatina():
    adn = trazo('M6 46' + ''.join(f'Q{10 + 16 * k} {34 if k % 2 else 58} {14 + 16 * k} 46' for k in range(5)), 'b', 2) + ''.join(circ(14 + 16 * k, 46, 5, 'fa') for k in range(5))
    crom = trazo('M140 16Q146 46 140 76', 'w', 7) + trazo('M160 16Q154 46 160 76', 'w', 7) + circ(150, 46, 5, 'fr')
    return svg(adn, t(44, 76, 'ADN + histonas', tam=10), fl(92, 46, 120, 46, 'm', 2), crom, t(186, 10, 'cromátidas', 'end', tam=9.5), t(150, 90, 'centrómero', c='r', tam=9.5))


def ciclo_celular():
    cx, cy, r = 56, 46, 34
    def sec(g1, g2, var):
        a1, a2 = math.radians(g1), math.radians(g2)
        x1, y1 = cx + r * math.cos(a1), cy - r * math.sin(a1)
        x2, y2 = cx + r * math.cos(a2), cy - r * math.sin(a2)
        grande = 1 if g2 - g1 > 180 else 0
        return f'<path d="M{cx} {cy}L{x1:.1f} {y1:.1f}A{r} {r} 0 {grande} 0 {x2:.1f} {y2:.1f}Z" style="fill:var(--{var});fill-opacity:.55"/>'
    return svg(sec(90, 250, 'acc'), sec(250, 340, 'acc2'), sec(340, 410, 'warn'), sec(410, 450, 'mal'), aro(cx, cy, r, 'm', 1.5),
               t(38, 38, 'G1', tam=11), t(64, 76, 'S', tam=11), t(84, 46, 'G2', tam=10), t(70, 18, 'M', tam=10),
               t(150, 30, 'interfase:', tam=10.5), t(150, 44, 'G1 → S → G2', tam=10.5), t(150, 66, 'M: división', c='r', tam=10.5))


def fases_mitosis():
    def celula(x, cont, et):
        return aro(x, 40, 20, 'm', 2) + cont + t(x, 82, et, tam=9)
    X = lambda x, y: trazo(f'M{x - 3} {y - 5}L{x + 3} {y + 5}M{x + 3} {y - 5}L{x - 3} {y + 5}', 'w', 2.2)
    pro = ''.join(X(x, y) for x, y in ((18, 34), (30, 46), (22, 50)))
    met = ln(74, 22, 74, 58, 'm', 1, '2 2') + ''.join(X(74, y) for y in (30, 40, 50))
    ana = ''.join(trazo(f'M{x} {y - 4}L{x} {y + 4}', 'w', 2.2) for x in (116, 136) for y in (30, 40, 50))
    telo = circ(166, 40, 6, 'fa') + circ(186, 40, 6, 'fa') + ln(176, 20, 176, 60, 'm', 1.6, '3 3')
    return svg(celula(24, pro, 'profase'), celula(74, met, 'metafase'), celula(126, ana, 'anafase'), aro(176, 40, 20, 'm', 2), telo, t(176, 82, 'telofase', tam=9))


def entrecruzamiento():
    return svg(trazo('M20 20L20 72', 'a', 7), trazo('M36 20L36 72', 'r', 7), fl(52, 46, 80, 46, 'm', 2),
               trazo('M100 20L100 44', 'a', 7), trazo('M100 44L100 72', 'r', 7), trazo('M116 20L116 44', 'r', 7), trazo('M116 44L116 72', 'a', 7),
               t(28, 88, 'homólogos', tam=9.5), t(108, 88, 'intercambian', tam=9.5), t(162, 40, 'gametos', tam=10.5), t(162, 54, 'únicos', tam=10.5))


def recombinante():
    pl = lambda x, gap, ins: (f'<path class="a" d="M{x + 14 * math.cos(math.radians(110)):.1f} {40 - 14 * math.sin(math.radians(110)):.1f}A14 14 0 1 0 {x + 14 * math.cos(math.radians(70)):.1f} {40 - 14 * math.sin(math.radians(70)):.1f}" stroke-width="2.5" fill="none"/>'
                              + (trazo(f'M{x - 4.8:.1f} {40 - 13.2:.1f}Q{x} {40 - 16} {x + 4.8:.1f} {40 - 13.2:.1f}', 'w', 3.5) if ins else ''))
    bacterias = ''.join(redondo(140 + 22 * (k % 2), 22 + 22 * (k // 2), 18, 12, 6, 'b', 1.8) for k in range(4))
    return svg(pl(18, True, False), t(18, 70, '1 corta', tam=9.5), pl(60, False, True), t(60, 70, '2 pega', tam=9.5),
               redondo(84, 28, 36, 24, 12, 'b', 2), aro(102, 40, 6, 'a', 1.6), t(102, 70, '3 entra', tam=9.5), bacterias, t(162, 70, '4 multiplica', tam=9.5),
               t(100, 88, 'enzima de restricción → ligasa', tam=9.5))


def jirafas():
    def jirafa(x, cuello, c):
        return ln(x, 70, x, 70 - cuello, c, 4) + circ(x + 3, 70 - cuello, 4, 'f' + c) + redondo(x - 10, 66, 22, 10, 4, c, 2)
    return svg(jirafa(20, 18, 'm'), fl(36, 56, 52, 50, 'm', 1.6), jirafa(64, 34, 'm'), fl(80, 44, 96, 38, 'r', 1.6), jirafa(108, 34, 'r'),
               t(64, 90, 'Lamarck: lo estirado se hereda', tam=9.5), ln(84, 28, 96, 40, 'r', 2.5), ln(96, 28, 84, 40, 'r', 2.5), t(156, 40, 'falso: lo', c='r', tam=10), t(156, 54, 'adquirido', c='r', tam=10), t(156, 68, 'no se hereda', c='r', tam=10))


def homologas():
    def extremidad(x, sup, ant, dedo, abre, et):
        y1 = 6 + sup
        y2 = y1 + 2 + ant
        s = ln(x, 6, x, y1, 'a', 5) + ln(x - 3, y1 + 2, x - 3, y2, 'b', 3) + ln(x + 3, y1 + 2, x + 3, y2, 'b', 3)
        for k in range(5):
            g = math.radians(-abre / 2 + abre * k / 4)
            s += ln(x, y2 + 2, round(x + dedo * math.sin(g), 1), round(y2 + 2 + dedo * math.cos(g), 1), 'w', 2)
        return s + t(x, 80, et, tam=9.5)
    return svg(extremidad(30, 20, 18, 14, 40, 'brazo'), extremidad(100, 14, 16, 30, 90, 'ala murciélago'), extremidad(170, 8, 10, 22, 30, 'aleta ballena'),
               t(100, 91, 'mismos huesos, distinta función', tam=9.5))


def ciclo_c_o():
    return svg(caja(6, 30, 74, 30, 'g'), t(43, 49, 'fotosíntesis', tam=10), caja(120, 30, 74, 30, 'w'), t(157, 49, 'respiración', tam=10),
               trazo('M80 36Q100 18 120 36', 'g', 2.5), '<path class="fg" d="M120 36L111 33L116 27Z"/>', t(100, 16, 'glucosa + O₂', tam=10),
               trazo('M120 56Q100 74 80 56', 'w', 2.5), '<path class="fw" d="M80 56L89 59L84 65Z"/>', t(100, 84, 'CO₂ + H₂O', tam=10))


def cloroplasto():
    cl = elipse(70, 46, 62, 34, 'g', 2.5, 'ok', .12)
    grana = ''.join(redondo(x, y + 6 * k, 18, 5, 2.5, 'g', 1.4, 'ok', .5) for x, y in ((30, 34), (60, 46), (92, 34)) for k in range(3))
    return svg(cl, grana, t(160, 30, 'tilacoides:', 'middle', c='g', tam=10), t(160, 44, 'luz, H₂O → O₂', tam=9.5), t(160, 62, 'estroma:', c='a', tam=10), t(160, 76, 'CO₂ → glucosa', tam=9.5),
               circ(76, 70, 2, 'fa'), circ(50, 66, 2, 'fa'))


def limitante_luz():
    return svg(fl(14, 80, 190, 80, 'm', 1.6), fl(14, 80, 14, 6, 'm', 1.6), curva(puntos(lambda x: 80 - 56 * (1 - math.exp(-(x - 14) / 40)), 14, 186, 60), 'g', 3),
               ln(110, 24, 186, 24, 'w', 1.4, '4 3'), t(150, 18, 'otro factor limita', c='w', tam=9.5), t(100, 92, 'luz →', tam=10), t(22, 12, 'rapidez', 'start', tam=9.5))


def flujo_energia():
    return svg(circ(16, 30, 9, 'fw'), fl(28, 30, 50, 30, 'w', 2), caja(52, 20, 38, 20, 'g'), t(71, 34, 'planta', tam=9.5), fl(92, 30, 112, 30, 'm', 2),
               caja(114, 20, 34, 20, 'a'), t(131, 34, 'herb.', tam=9.5), fl(150, 30, 168, 30, 'm', 2), caja(170, 20, 26, 20, 'r'), t(183, 34, 'carn.', tam=9),
               *[fl(x, 42, x, 60, 'r', 1.6) for x in (71, 131, 183)], t(128, 74, 'calor (se pierde)', c='r', tam=9.5), t(100, 90, 'energía: un solo sentido', tam=9.5))


# =====================================================================
# Química
# =====================================================================
def particulas():
    def caja_p(x, cont, et):
        return marco(x, 10, 56, 56, 'm', 1.8) + cont + t(x + 28, 82, et, tam=10)
    el = ''.join(molecula(x, y, O2) for x, y in ((16, 24), (40, 30), (22, 50), (46, 54)))
    co = ''.join(molecula(x, y, H2O) for x, y in ((84, 28), (106, 32), (86, 54), (108, 56)))
    mz = ''.join(molecula(x, y, O2) for x, y in ((148, 24), (170, 52))) + ''.join(molecula(x, y, H2O) for x, y in ((172, 28), (148, 54)))
    return svg(caja_p(4, el, 'elemento'), caja_p(72, co, 'compuesto'), caja_p(140, mz, 'mezcla'))


def homo_hetero():
    homo = vaso(20, 14, 56, 60, .7, 'acc2', .35)
    hetero = vaso(122, 14, 56, 60, .4, 'acc2', .35) + rect_(123, 32, 54, 18, 'warn', .5)
    return svg(homo, t(48, 88, 'homogénea', tam=10), hetero, t(150, 88, 'heterogénea', tam=10), t(150, 44, 'aceite', tam=9), t(150, 66, 'agua', tam=9))


def separacion():
    filtro = poly([(8, 14), (40, 14), (24, 36)], 'm', None) + ln(24, 36, 24, 48, 'm', 2) + vaso(12, 50, 24, 22, .4) + t(24, 86, 'filtrar', tam=9)
    deca = trazo('M58 12L58 40L68 54L78 40L78 12', 'm', 2) + rect_(59, 16, 18, 12, 'warn', .5) + rect_(59, 28, 18, 12, 'acc2', .4) + ln(68, 54, 68, 66, 'm', 2) + t(68, 86, 'decantar', tam=9)
    dest = circ(112, 54, 12, 'fm') + ln(112, 42, 112, 30, 'm', 2) + ln(112, 30, 150, 50, 'b', 3) + vaso(142, 52, 16, 18, .4) + fl(112, 74, 112, 68, 'r', 1.6) + t(130, 86, 'destilar', tam=9)
    tamiz = ln(166, 40, 196, 40, 'm', 2) + ''.join(ln(170 + 6 * k, 36, 170 + 6 * k, 44, 'm', 1) for k in range(5)) + circ(176, 32, 4, 'fm') + circ(188, 31, 5, 'fm') + circ(180, 54, 1.8, 'fm') + circ(186, 58, 1.8, 'fm') + t(181, 86, 'tamizar', tam=9)
    return svg(filtro, deca, dest, tamiz)


def densidad():
    return svg(vaso(60, 8, 60, 72, .95, 'warn', .15), rect_(61, 15, 58, 20, 'warn', .45), rect_(61, 35, 58, 22, 'acc2', .35), rect_(61, 57, 58, 22, 'acc', .45),
               t(140, 28, 'aceite', 'start', tam=10), t(140, 49, 'agua', 'start', tam=10), t(140, 71, 'miel', 'start', tam=10), t(30, 26, 'menos', tam=10), t(30, 40, 'denso', tam=10),
               fl(30, 70, 30, 48, 'm', 2), t(30, 84, 'flota', tam=10))


def lamina_oro():
    rayos = ''.join(fl(6, y, 196, y, 'a', 1.6) for y in (14, 28, 64, 78)) + ln(6, 46, 92, 46, 'r', 1.8) + fl(92, 46, 30, 58, 'r', 1.8) + ln(6, 38, 92, 38, 'w', 1.8) + fl(92, 38, 180, 8, 'w', 1.8)
    return svg(ln(94, 6, 94, 86, 'w', 4), rayos, t(150, 50, 'casi todas', tam=10), t(150, 60, 'pasan', tam=10), t(30, 72, 'pocas rebotan', c='r', tam=9.5))


def salto_bohr():
    return svg(circ(50, 46, 4, 'fr'), aro(50, 46, 16, 'm', 1.6), aro(50, 46, 30, 'm', 1.6), aro(50, 46, 42, 'm', 1.6),
               circ(92, 46, 4, 'fa'), fl(80, 46, 68, 46, 'a', 2), circ(66, 46, 3, 'fm'),
               trazo('M100 40' + ''.join(f'q4 -6 8 0' for _ in range(6)), 'w', 2), '<path class="fw" d="M152 40L144 35L144 45Z"/>',
               t(150, 22, 'baja de nivel:', tam=10), t(150, 66, 'emite luz', c='w', tam=10.5))


def notacion_za():
    nucleo = ''.join(circ(40 + 7 * (k % 4), 36 + 7 * (k // 4), 3.4, 'fr' if k % 2 == 0 else 'fm') for k in range(12))
    return svg(nucleo, aro(50, 42, 28, 'a', 1.4), circ(78, 42, 3, 'fa'), circ(26, 30, 3, 'fa'),
               t(136, 26, 'A = 23 (p + n)', tam=10.5), t(136, 44, 'Z = 11 (protones)', c='r', tam=10.5), t(136, 62, 'n = 23 − 11 = 12', tam=10.5), t(136, 80, '²³₁₁Na', c='w', tam=13))


def cadenas():
    zig = curva([(10, 40), (24, 28), (38, 40), (52, 28), (66, 40)], 'a', 2.5)
    ram = curva([(84, 40), (98, 28), (112, 40), (126, 28)], 'b', 2.5) + ln(98, 28, 98, 14, 'b', 2.5)
    hexa = poly([(166 + 16 * math.cos(math.radians(30 + 60 * k)), 34 - 16 * math.sin(math.radians(30 + 60 * k))) for k in range(6)], 'w', None)
    return svg(zig, ram, hexa, t(38, 66, 'cadena', tam=10), t(106, 66, 'ramificada', tam=10), t(166, 66, 'anillo', tam=10), t(100, 88, 'C con 4 enlaces', tam=10))


def hibridacion_moleculas():
    met = t(30, 34, 'H', tam=10) + ln(30, 38, 30, 44, 'm', 1.6) + t(30, 52, 'H–C–H', tam=10) + ln(30, 56, 30, 62, 'm', 1.6) + t(30, 72, 'H', tam=10)
    ete = t(98, 52, 'H₂C=CH₂', tam=10.5)
    eti = t(166, 52, 'H–C≡C–H', tam=10.5)
    return svg(met, ete, eti, t(30, 16, 'sp³', c='a', tam=11), t(98, 16, 'sp²', c='b', tam=11), t(166, 16, 'sp', c='w', tam=11),
               t(30, 90, 'metano', tam=9.5), t(98, 90, 'eteno', tam=9.5), t(166, 90, 'etino', tam=9.5))


def largos_enlace():
    filas = [('C–C', 154, 'a'), ('C=C', 134, 'b'), ('C≡C', 120, 'w')]
    s = ''.join(rect_(40, 10 + 24 * i, 0.8 * l, 16, {'a': 'acc', 'b': 'acc2', 'w': 'warn'}[c], .55) + t(34, 23 + 24 * i, n, 'end', tam=10.5) + t(44 + 0.8 * l, 23 + 24 * i, f'{l} pm', 'start', tam=9.5)
                for i, (n, l, c) in enumerate(filas))
    return svg(s, t(100, 90, 'más enlaces: más corto y más fuerte', tam=9.5))


def alc_alq():
    alcano = curva([(10, 40), (24, 28), (38, 40)], 'a', 2.5)
    alqueno = curva([(70, 40), (84, 28), (98, 40)], 'b', 2.5) + ln(74.7, 41.2, 84.5, 32.8, 'b', 2)
    alquino = ln(130, 34, 190, 34, 'w', 2.5) + ln(146, 30, 174, 30, 'w', 2) + ln(146, 38, 174, 38, 'w', 2)
    return svg(alcano, alqueno, alquino, t(24, 62, 'propano', tam=9.5), t(24, 76, 'simples', c='a', tam=9.5), t(84, 62, 'propeno', tam=9.5), t(84, 76, 'un doble', c='b', tam=9.5),
               t(160, 62, 'propino', tam=9.5), t(160, 76, 'un triple', c='w', tam=9.5))


def grupos_o():
    def grupo(x, base, extra, et):
        return base + extra + t(x, 88, et, tam=9)
    alc = grupo(26, curva([(8, 50), (20, 40), (32, 50)], 'a', 2.2), ln(32, 50, 42, 42, 'r', 2) + t(46, 40, 'OH', 'start', c='r', tam=9), 'alcohol')
    ald = grupo(80, curva([(62, 50), (74, 40), (86, 50)], 'a', 2.2), ln(86, 50, 86, 34, 'r', 2) + ln(89, 50, 89, 34, 'r', 2) + t(88, 28, 'O', c='r', tam=9) + t(98, 54, 'H', tam=9), 'aldehído')
    cet = grupo(132, curva([(114, 50), (126, 40), (138, 50), (150, 40)], 'a', 2.2), ln(125, 40, 125, 24, 'r', 2) + ln(128, 40, 128, 24, 'r', 2) + t(127, 18, 'O', c='r', tam=9), 'cetona')
    aci = grupo(182, curva([(164, 50), (176, 40), (188, 50)], 'a', 2.2), ln(176, 40, 176, 24, 'r', 2) + ln(179, 40, 179, 24, 'r', 2) + t(177, 18, 'O', c='r', tam=9) + t(196, 60, 'OH', 'end', c='r', tam=9), 'ácido')
    return svg(alc, ald, cet, aci)


def conservacion():
    return svg(ln(20, 40, 180, 40, 'm', 3), poly([(100, 42), (90, 60), (110, 60)], 'm', 'muted', .5), caja(24, 16, 64, 22, 'a'), t(56, 31, 'reactantes', tam=10),
               caja(112, 16, 64, 22, 'g'), t(144, 31, 'productos', tam=10), t(100, 78, 'misma masa a cada lado', tam=10.5), t(100, 91, '(Lavoisier)', tam=9.5))


def pasos_esteq():
    cajas = [('g de A', 'a'), ('mol A', 'b'), ('mol B', 'b'), ('g de B', 'g')]
    s = ''.join(caja(4 + 50 * i, 30, 42, 24, c) + t(25 + 50 * i, 46, e, tam=9.5) for i, (e, c) in enumerate(cajas))
    s += ''.join(fl(46 + 50 * i, 42, 54 + 50 * i, 42, 'm', 1.6) for i in range(3))
    return svg(s, t(50, 22, '÷ M', tam=9.5), t(100, 70, '× coeficientes', tam=9.5), t(150, 22, '× M', tam=9.5), t(100, 90, 'siempre pasa por los moles', tam=9.5))


def limitante():
    izq = ''.join(molecula(14 + 14 * (k % 2), 22 + 16 * (k // 2), H2) for k in range(4)) + ''.join(molecula(52, 22 + 16 * k, O2) for k in range(3))
    der = ''.join(molecula(124 + 22 * (k % 2), 28 + 22 * (k // 2), H2O) for k in range(4)) + molecula(182, 46, O2) + aro(182, 46, 12, 'w', 1.8)
    return svg(izq, fl(72, 46, 104, 46, 'm', 2), der, t(36, 84, '4 H₂ + 3 O₂', tam=10), t(140, 84, '4 H₂O', tam=10), t(182, 70, 'sobra', c='w', tam=9.5))


def empirica_molecular():
    s = ''.join(caja(6 + 32 * k, 26, 28, 22, 'a') + t(20 + 32 * k, 41, 'CH₂O', tam=8.5) for k in range(6))
    return svg(s, t(100, 16, '6 × CH₂O', tam=10.5), t(100, 70, '= C₆H₁₂O₆ (glucosa)', c='g', tam=10.5), t(100, 88, 'n = 180 ÷ 30 = 6', tam=10))


def receta():
    filas = [('C 40 %', '40/12 = 3,33', '1'), ('H 6,7 %', '6,7/1 = 6,7', '2'), ('O 53,3 %', '53,3/16 = 3,33', '1')]
    s = ''.join(t(30, 24 + 18 * i, a, tam=9.5) + t(104, 24 + 18 * i, b, tam=9.5) + t(176, 24 + 18 * i, c, c='g', tam=10) for i, (a, b, c) in enumerate(filas))
    return svg(t(30, 10, '100 g', tam=9), t(104, 10, 'mol', tam=9), t(176, 10, '÷ menor', tam=9), s, t(100, 86, '→ CH₂O', c='g', tam=11))


def soluto_solvente():
    return svg(vaso(40, 12, 70, 66, .8, 'acc2', .3), *[circ(x, y, 3, 'fr') for x, y in ((54, 36), (72, 50), (92, 34), (60, 64), (86, 66), (98, 52))],
               t(150, 36, 'soluto (sal)', c='r', tam=10), t(150, 56, 'solvente (agua)', c='b', tam=10), t(75, 92, 'una sola fase', tam=9.5))


def mm():
    return svg(caja(6, 30, 50, 24, 'r'), t(31, 46, '10 g sal', tam=9.5), t(64, 46, '+', tam=12), caja(72, 30, 50, 24, 'b'), t(97, 46, '90 g agua', tam=9.5),
               t(130, 46, '=', tam=12), caja(138, 30, 58, 24, 'g'), t(167, 46, '100 g sol.', tam=9.5), t(100, 80, '10 % m/m (sobre la solución)', c='g', tam=10))


def molaridad():
    return svg(trazo('M40 8L40 30L20 80L100 80L80 30L80 8', 'm', 2.2), rect_(24, 56, 72, 23, 'acc2', .35), ln(38, 52, 82, 52, 'w', 1.6), t(60, 48, '1 L', c='w', tam=10),
               *[circ(x, 70, 3, 'fr') for x in (40, 60, 80)], t(150, 36, '2 mol en 1 L', tam=10.5), t(150, 56, '= 2 M', c='g', tam=12))


def mezclar():
    return svg(vaso(6, 26, 36, 40, .6), t(24, 82, '100 mL · 1 M', tam=8.5), t(52, 50, '+', tam=12), vaso(62, 26, 36, 40, .6, 'acc', .45), t(80, 82, '100 mL · 3 M', tam=8.5),
               fl(106, 46, 124, 46, 'm', 2), vaso(132, 14, 50, 52, .75, 'acc', .3), t(157, 82, '200 mL · 2 M', c='g', tam=9))


def solubilidad():
    return svg(fl(16, 80, 190, 80, 'm', 1.6), fl(16, 80, 16, 6, 'm', 1.6), curva(puntos(lambda x: 74 - 0.0025 * (x - 16) ** 2, 16, 180), 'r', 3),
               curva(puntos(lambda x: 24 + 0.28 * (x - 16), 16, 180), 'b', 3), t(160, 16, 'sólido', c='r', tam=10), t(176, 60, 'gas', c='b', tam=10),
               t(100, 92, 'temperatura →', tam=9.5), t(24, 12, 'solubilidad', 'start', tam=9.5))


DIBUJOS = {
    ('bio.celula', 'Procarionte y eucarionte'): pro_eu(),
    ('bio.celula', 'Lo que cambia'): animal_vegetal(),
    ('bio.celula', 'Ribosomas → RER → Golgi'): ruta_proteinas(),
    ('bio.nervioso', 'Central y periférico'): snc_snp(),
    ('bio.nervioso', 'De reposo a impulso'): potencial_accion(),
    ('bio.nervioso', 'De una neurona a otra'): sinapsis(),
    ('bio.nervioso', 'Responder sin pensar'): arco_reflejo(),
    ('bio.reproduccion', 'Espermatozoide y ovocito'): gametos(),
    ('bio.reproduccion', 'Dónde y cómo'): fecundacion(),
    ('bio.reproduccion', 'Folicular → ovulación → lútea'): ciclo_ovarico(),
    ('bio.reproduccion', 'Menstrual → proliferativa → secretora'): ciclo_uterino(),
    ('bio.anticoncepcion-its', 'Calendario, temperatura basal, Billings'): temp_basal(),
    ('bio.anticoncepcion-its', 'Condón y diafragma'): barrera(),
    ('bio.anticoncepcion-its', 'Píldora, inyección, implante'): hormonal(),
    ('bio.anticoncepcion-its', 'Vasectomía y ligadura'): quirurgico(),
    ('bio.division', 'Del hilo al cromosoma'): cromatina(),
    ('bio.division', 'G1 → S → G2'): ciclo_celular(),
    ('bio.division', 'Profase, metafase, anafase, telofase'): fases_mitosis(),
    ('bio.division', 'Por qué los hermanos no son iguales'): entrecruzamiento(),
    ('bio.manipulacion', 'Cómo se hace'): recombinante(),
    ('bio.evolucion', 'Uso, desuso y herencia de lo adquirido'): jirafas(),
    ('bio.evolucion', 'Cómo se sabe'): homologas(),
    ('bio.fotosintesis', 'Una es el reverso de la otra'): ciclo_c_o(),
    ('bio.fotosintesis', 'En los tilacoides'): cloroplasto(),
    ('bio.fotosintesis', 'Qué la acelera'): limitante_luz(),
    ('bio.fotosintesis', 'Energía fluye, materia circula'): flujo_energia(),
    ('qui.materia', 'Elemento y compuesto'): particulas(),
    ('qui.materia', 'Homogénea y heterogénea'): homo_hetero(),
    ('qui.materia', 'Cuatro métodos'): separacion(),
    ('qui.materia', 'Densidad y puntos de cambio'): densidad(),
    ('qui.modelos', 'Núcleo'): lamina_oro(),
    ('qui.modelos', 'Niveles de energía'): salto_bohr(),
    ('qui.modelos', 'Z y A'): notacion_za(),
    ('qui.carbono', 'Cuatro enlaces'): cadenas(),
    ('qui.carbono', 'Cuenta los enlaces del C'): hibridacion_moleculas(),
    ('qui.carbono', 'Simple, doble, triple'): largos_enlace(),
    ('qui.organica', 'Alcanos, alquenos, alquinos'): alc_alq(),
    ('qui.organica', 'Los más preguntados'): grupos_o(),
    ('qui.estequiometria', 'Lavoisier, Proust, Dalton'): conservacion(),
    ('qui.estequiometria', 'Cuatro pasos'): pasos_esteq(),
    ('qui.estequiometria', 'El que se acaba primero'): limitante(),
    ('qui.composicion', 'Proporción y fórmula real'): empirica_molecular(),
    ('qui.composicion', 'De porcentajes a fórmula'): receta(),
    ('qui.soluciones', 'Soluto y solvente'): soluto_solvente(),
    ('qui.soluciones', '%m/m, %m/v, %v/v, ppm'): mm(),
    ('qui.soluciones', 'Molaridad, molalidad, fracción molar'): molaridad(),
    ('qui.soluciones', 'Dos soluciones del mismo soluto'): mezclar(),
    ('qui.soluciones', 'Cuánto se puede disolver'): solubilidad(),
}
