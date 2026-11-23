#!/usr/bin/env python3
"""Esquemas (SVG) para las tarjetas de las lecciones de Física escritas a mano en fisica.html.

Para cada lección hay una lista con un esquema por tarjeta, en el mismo orden (None = sin esquema).
El esquema va justo después del <h4> de la tarjeta. Es idempotente: borra los esquemas anteriores de esas tarjetas.
Los colores salen de clases de core.css (.a .b .w .r .g .m y rellenos .fa .fb .fw .fr .fg .fm), así siguen el tema.

Uso: python3 tools/tarjetas.py
"""
import math
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from esquemas import aro, caja, circ, curva, fl, ln, onda, poly, puntos, rayo_luz, svg, tx  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parent.parent


def p(*pts):
    return 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)


def trazo(d, c='m', w=2.5, extra=''):
    return f'<path class="{c}" d="{d}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"{extra}/>'


def punteado(x, y, r, c='m', w=1.6):
    return f'<circle class="{c}" cx="{x}" cy="{y}" r="{r}" stroke-width="{w}" stroke-dasharray="4 3"/>'


def fase(x, y, r, k, der=True):
    """Disco de un planeta con fracción iluminada k; luz desde la derecha (der) o la izquierda."""
    rx = abs(1 - 2 * k) * r
    s1 = 1 if der else 0                       # primer arco por el lado iluminado
    s2 = (1 if k > 0.5 else 0) if der else (0 if k > 0.5 else 1)
    luz = (f'<path class="fw" d="M{x} {y - r}A{r} {r} 0 0 {s1} {x} {y + r}A{rx:.2f} {r} 0 0 {s2} {x} {y - r}Z"/>')
    return f'<circle cx="{x}" cy="{y}" r="{r}" style="fill:var(--muted);fill-opacity:.35"/>' + luz


def sector(cx, cy, r, a1, a2, clase):
    x1, y1 = cx + r * math.cos(a1), cy - r * math.sin(a1)
    x2, y2 = cx + r * math.cos(a2), cy - r * math.sin(a2)
    grande = 1 if (a2 - a1) % (2 * math.pi) > math.pi else 0
    return f'<path class="{clase}" d="M{cx} {cy}L{x1:.1f} {y1:.1f}A{r} {r} 0 {grande} 0 {x2:.1f} {y2:.1f}Z"/>'


def kepler(M, e):
    E = M
    for _ in range(40):
        E -= (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
    return E


# ---------------------------------------------------------------- sistema solar
def ptolomeo():
    cx, cy, R = 52, 48, 30
    ang = math.radians(35)
    ex, ey = cx + R * math.cos(ang), cy - R * math.sin(ang)
    px, py = ex + 12 * math.cos(math.radians(-20)), ey - 12 * math.sin(math.radians(-20))
    rizo = [(150 + 26 * math.cos(t) + 12 * math.cos(4 * t), 46 - 26 * math.sin(t) - 12 * math.sin(4 * t))
            for t in [i * 2 * math.pi / 160 for i in range(161)]]
    return svg(punteado(cx, cy, R), aro(round(ex, 1), round(ey, 1), 12, 'r', 2), circ(round(px, 1), round(py, 1), 4, 'fr'),
               circ(cx, cy, 7, 'fb'), tx(cx, 90, 'Tierra al centro'), tx(round(ex, 1) + 2, round(ey, 1) - 16, 'epiciclo'),
               curva(rizo, 'r', 2), tx(150, 90, 'camino: rizos'))


def copernico():
    cx, cy = 58, 46
    planetas = [(14, 'm', 'fm', 40), (26, 'b', 'fb', 200), (39, 'r', 'fr', 300)]
    partes = [circ(cx, cy, 8, 'fw')]
    for r, c, f, g in planetas:
        partes.append(punteado(cx, cy, r, c))
        partes.append(circ(round(cx + r * math.cos(math.radians(g)), 1), round(cy - r * math.sin(math.radians(g)), 1), 4, f))
    return svg(*partes, tx(150, 34, 'Sol al centro'), tx(150, 54, 'la Tierra (azul)'), tx(150, 70, 'es un planeta más'))


def galileo():
    lunas = ''.join(circ(x, 34, 2.6, 'fm') for x in (10, 22, 66, 80))
    venus = fase(112, 40, 15, 0.12) + fase(142, 40, 11, 0.4) + fase(166, 40, 8, 0.75) + fase(186, 40, 5.5, 0.97)
    return svg(circ(44, 34, 11, 'fw'), lunas, tx(44, 66, 'lunas de'), tx(44, 80, 'Júpiter'),
               venus, tx(148, 72, 'Venus: todas las fases'), tx(148, 87, 'llena = pequeña'))


def kepler_esq():
    cx, cy, a, b = 96, 46, 66, 36
    e = math.sqrt(1 - (b / a) ** 2)
    sx = cx + a * e
    P = lambda E: (cx + a * math.cos(E), cy - b * math.sin(E))
    def sec(m1, m2, clase, op):
        E1, E2 = kepler(m1, e), kepler(m2, e)
        pts = [(sx, cy)] + [P(E1 + (E2 - E1) * i / 30) for i in range(31)]
        return poly(pts, clase, clase == 'g' and 'ok' or 'acc2', op)
    elipse = f'<ellipse class="a" cx="{cx}" cy="{cy}" rx="{a}" ry="{b}" stroke-width="2.5" fill="none"/>'
    return svg(sec(-0.35, 0.35, 'g', .35), sec(math.pi - 0.35, math.pi + 0.35, 'b', .35), elipse, circ(round(sx, 1), cy, 7, 'fw'),
               tx(round(sx, 1) - 4, cy + 22, 'Sol'), tx(184, 22, 'rápido', 'middle'), tx(22, 22, 'lento'), tx(100, 90, 'mismo tiempo = misma área'))


def big_bang():
    sup = puntos(lambda x: 46 - 36 * ((x - 14) / 176) ** 0.55, 14, 190, 60)
    inf = [(x, 92 - y) for x, y in sup]
    puntos_g = []
    for k, x in enumerate([40, 64, 92, 124, 160]):
        alto = 36 * ((x - 14) / 176) ** 0.55
        for j in (-0.6, 0, 0.6):
            puntos_g.append(circ(x, round(46 + j * alto, 1), 2.2 + 0.4 * k, 'fa' if k > 1 else 'fw'))
    return svg(curva(sup, 'm', 2), curva(inf, 'm', 2), circ(14, 46, 5, 'fw'), *puntos_g,
               tx(14, 88, 'Big Bang', 'start'), tx(196, 88, 'hoy', 'end'), tx(196, 12, 'se expande y se enfría', 'end'))


def evidencias():
    lab = caja(4, 14, 64, 14, 'm') + ''.join(ln(x, 14, x, 28, 'a', 2.5) for x in (16, 30, 44))
    gal = caja(4, 40, 64, 14, 'm') + ''.join(ln(x, 40, x, 54, 'r', 2.5) for x in (26, 40, 54))
    pastel = (sector(170, 38, 20, math.pi / 2, math.pi / 2 + 1.5 * math.pi, 'fb') + sector(170, 38, 20, math.pi / 2 - 0.5 * math.pi, math.pi / 2, 'fw'))
    return svg(lab, gal, fl(18, 62, 52, 62, 'r', 2), tx(36, 78, 'al rojo'),
               onda(80, 140, 36, 9, 20, 'b', 2.5), tx(110, 66, 'fondo de'), tx(110, 80, 'microondas'),
               pastel, tx(170, 78, 'H y He'))


def big_crunch():
    ejes = fl(14, 80, 194, 80, 'm', 1.8) + fl(14, 80, 14, 8, 'm', 1.8)
    exp = puntos(lambda x: 80 - 52 * ((x - 14) / 90) ** 0.66, 14, 104, 30) + puntos(lambda x: 28 - 0.0035 * (x - 104) ** 2 - 0.12 * (x - 104), 104, 190, 30)
    crunch = puntos(lambda x: 80 - 52 * ((x - 14) / 90) ** 0.66, 14, 104, 30) + puntos(lambda x: 28 + 52 * ((x - 104) / 86) ** 2, 104, 190, 30)
    return svg(ejes, curva(exp, 'g', 2.5), curva(crunch, 'r', 2.5), tx(150, 16, 'se acelera'), tx(122, 68, 'Big Crunch'),
               tx(22, 14, 'tamaño', 'start'), tx(192, 92, 'tiempo', 'end'))


# ---------------------------------------------------------------- dispositivos
def radar():
    antena = trazo('M10 70Q22 46 40 40', 'a', 3) + ln(24, 58, 24, 84, 'm', 2.5) + ln(14, 84, 34, 84, 'm', 2.5)
    avion = poly([(150, 26), (186, 22), (190, 26), (186, 30)], 'w', 'warn', .5) + poly([(166, 25), (158, 12), (164, 12), (176, 25)], 'w', 'warn', .5)
    return svg(antena, fl(40, 44, 146, 28, 'w', 2.5), fl(146, 36, 44, 52, 'b', 2.5), avion,
               tx(96, 26, 'va'), tx(96, 62, 'vuelve'), tx(112, 88, 'tiempo → distancia'))


def laser():
    bulbo = circ(36, 38, 10, 'fw') + rayo_luz(36, 38, 10, 24, 'w')
    haz = caja(96, 30, 30, 16, 'r') + ''.join(ln(126, y, 196, y, 'r', 1.5) for y in (35, 38, 41)) + onda(130, 196, 38, 5, 16, 'r', 2)
    return svg(bulbo, tx(36, 80, 'ampolleta:'), tx(36, 92, 'todas direcciones'), haz, tx(150, 66, 'láser: un color,'), tx(150, 80, 'en fase, haz delgado'))


def fibra():
    sup = puntos(lambda x: 26 + 14 * math.sin((x - 10) / 180 * math.pi), 10, 190, 60)
    inf = [(x, y + 26) for x, y in sup]
    zig = [(10, 39 + 14 * math.sin(0))]
    for k, x in enumerate(range(28, 191, 18)):
        base = 26 + 14 * math.sin((x - 10) / 180 * math.pi)
        zig.append((x, base + (3 if k % 2 == 0 else 23)))
    return svg(curva(sup, 'b', 2.5), curva(inf, 'b', 2.5), curva(zig, 'w', 2), tx(100, 90, 'la luz rebota por dentro'))


def refractor():
    return svg(ln(4, 46, 196, 46, 'm', 1, '3 3'),
               '<ellipse class="b" cx="56" cy="46" rx="5" ry="30" stroke-width="2.5" style="fill:var(--acc2);fill-opacity:.2"/>',
               '<ellipse class="b" cx="168" cy="46" rx="4" ry="14" stroke-width="2.5" style="fill:var(--acc2);fill-opacity:.2"/>',
               *[ln(6, y, 56, y, 'w', 2) + ln(56, y, 140, 46, 'w', 2) for y in (24, 68)],
               ln(140, 46, 168, 46 + (46 - 24) * 28 / 84, 'w', 2), ln(140, 46, 168, 46 - (46 - 24) * 28 / 84, 'w', 2),
               ln(168, 53.3, 196, 53.3, 'w', 2), ln(168, 38.7, 196, 38.7, 'w', 2),
               tx(56, 90, 'objetivo'), tx(168, 90, 'ocular'), tx(140, 30, 'foco'))


def reflector():
    espejo = trazo('M176 8Q150 46 176 84', 'b', 4)
    rayos = ''.join(ln(6, y, 160 + 0.0 * y + abs(y - 46) * 0.55, y, 'w', 2) + ln(160 + abs(y - 46) * 0.55, y, 96, 46, 'w', 2) for y in (22, 70))
    return svg(espejo, rayos, ln(6, 46, 163, 46, 'w', 2), circ(96, 46, 4, 'fr'), tx(96, 66, 'foco'), tx(176, 92, 'espejo cóncavo', 'end'))


def radiotelescopio():
    plato = trazo('M60 30Q96 76 132 30', 'b', 4) + ln(96, 53, 96, 84, 'm', 3) + ln(80, 84, 112, 84, 'm', 3)
    receptor = ln(66, 34, 96, 14, 'm', 1.5) + ln(126, 34, 96, 14, 'm', 1.5) + circ(96, 14, 4, 'fr')
    ondas = ''.join(onda(150, 196, y, 3, 10, 'a', 2) for y in (20, 32))
    return svg(plato, receptor, ondas, tx(172, 54, 'ondas'), tx(172, 66, 'de radio'), tx(30, 60, 'ALMA'))


def prismaticos():
    prisma = poly([(50, 78), (150, 78), (100, 28)], 'b', 'acc2', .15)
    rayo = fl(76, 92, 76, 56, 'w', 2.5) + ln(76, 54, 124, 54, 'w', 2.5) + fl(124, 54, 124, 92, 'w', 2.5)
    return svg(prisma, rayo, tx(166, 30, 'el prisma', 'middle'), tx(166, 44, 'refleja', 'middle'), tx(166, 58, '2 veces', 'middle'), tx(30, 40, 'prisma'))


def antena_celular():
    torre = ln(30, 84, 40, 30, 'm', 2.5) + ln(50, 84, 40, 30, 'm', 2.5) + ln(34, 64, 46, 64, 'm', 2)
    arcos = ''.join(f'<path class="a" d="M{40 + r * 0.6:.1f} {30 - r * 0.8:.1f}A{r} {r} 0 0 1 {40 + r * 0.6:.1f} {30 + r * 0.8:.1f}" stroke-width="2" fill="none"/>' for r in (12, 22, 32))
    fono = caja(150, 30, 24, 42, 'b') + ln(158, 66, 166, 66, 'b', 2)
    return svg(torre, circ(40, 30, 4, 'fr'), arcos, fono, fl(90, 46, 144, 46, 'a', 2), tx(100, 90, 'ondas de radio a la rapidez c'))


# ---------------------------------------------------------------- instalación de la casa
def medidor():
    return svg(ln(6, 46, 66, 46, 'm', 3), caja(66, 24, 68, 44, 'w'), tx(100, 44, '0 1 2 3 4'), tx(100, 60, 'kWh'),
               ln(134, 46, 194, 46, 'm', 3), tx(30, 36, 'red'), tx(170, 36, 'casa'), tx(100, 88, 'cuenta = kWh × precio'))


def disyuntor():
    return svg(ln(6, 46, 76, 46, 'm', 3), circ(76, 46, 3.5, 'fm'), ln(76, 46, 118, 22, 'r', 3.5), circ(124, 46, 3.5, 'fm'),
               ln(124, 46, 194, 46, 'm', 3), tx(100, 70, 'I mayor que la permitida'), tx(100, 86, '→ se abre y corta'))


def diferencial():
    return svg(fl(6, 32, 130, 32, 'a', 2.5), fl(130, 50, 6, 50, 'b', 2.5), '<ellipse class="w" cx="96" cy="41" rx="9" ry="20" stroke-width="3" fill="none"/>',
               tx(6, 22, 'entra 10 A', 'start'), tx(6, 68, 'vuelve 9,97 A', 'start'), ln(130, 50, 160, 50, 'b', 2.5), fl(160, 50, 160, 72, 'r', 2.5),
               tx(184, 44, 'fuga', 'middle'), ln(150, 76, 170, 76, 'm', 2.5), ln(154, 80, 166, 80, 'm', 2), ln(158, 84, 162, 84, 'm', 1.5),
               tx(96, 88, 'distintas → corta'))


def tierra():
    return svg(caja(20, 16, 70, 46, 'm'), tx(55, 44, 'carcasa'), ln(90, 50, 140, 50, 'g', 2.5), ln(140, 50, 140, 72, 'g', 2.5),
               ln(126, 72, 154, 72, 'g', 2.5), ln(131, 78, 149, 78, 'g', 2), ln(136, 84, 144, 84, 'g', 1.5),
               fl(150, 54, 150, 68, 'w', 2), tx(166, 22, 'la fuga', 'middle'), tx(166, 36, 'va a tierra', 'middle'), tx(55, 82, 'no pasa por ti'))


def enchufes():
    rieles = ln(10, 20, 190, 20, 'r', 2.5) + ln(10, 72, 190, 72, 'b', 2.5)
    cargas = ''.join(ln(x, 20, x, 34, 'm', 2) + caja(x - 12, 34, 24, 24, 'w') + ln(x, 58, x, 72, 'm', 2) for x in (60, 110, 160))
    return svg(rieles, cargas, tx(24, 50, '220 V'), tx(100, 90, 'cada uno recibe 220 V'))


def interruptor():
    lazo = ln(20, 20, 70, 20, 'm', 2.5) + circ(70, 20, 3, 'fm') + ln(70, 20, 100, 6, 'r', 3) + circ(104, 20, 3, 'fm') + ln(104, 20, 180, 20, 'm', 2.5)
    lazo += ln(180, 20, 180, 72, 'm', 2.5) + ln(20, 72, 180, 72, 'm', 2.5) + ln(20, 20, 20, 72, 'm', 2.5)
    ampolleta = circ(130, 72, 10, 'fm') + ln(124, 66, 136, 78, 'm', 1.5) + ln(136, 66, 124, 78, 'm', 1.5)
    return svg(lazo, ampolleta, f'<circle cx="20" cy="46" r="10" class="b" stroke-width="2.5" style="fill:var(--panel2)"/>', tx(20, 50, '~'), tx(87, 40, 'abierto'), tx(130, 92, 'apagada'), tx(60, 64, 'en serie'))


TARJETAS = {
    'fis.mec.cosmos': [ptolomeo(), copernico(), galileo(), kepler_esq(), big_bang(), evidencias(), big_crunch()],
    'fis.ond.dispositivos': [radar(), laser(), fibra(), refractor(), reflector(), radiotelescopio(), prismaticos(), antena_celular()],
    'fis.ele.domiciliaria': [medidor(), disyuntor(), diferencial(), tierra(), enchufes(), interruptor()],
}


def aplicar():
    ruta = RAIZ / 'fisica.html'
    s = ruta.read_text(encoding='utf-8')
    for lid, esqs in TARJETAS.items():
        i = s.index(f'<section class="leccion" id="{lid}"')
        j = s.index('</section>', i)
        sec = s[i:j]
        partes = sec.split('<div class="tarjeta">')
        if len(partes) - 1 != len(esqs):
            raise SystemExit(f'{lid}: {len(partes) - 1} tarjetas y {len(esqs)} esquemas')
        for k, e in enumerate(esqs, start=1):
            t = re.sub(r'<svg class="esq".*?</svg>', '', partes[k], flags=re.S)
            if e:
                t = t.replace('</h4>', '</h4>' + e, 1)
            partes[k] = t
        s = s[:i] + '<div class="tarjeta">'.join(partes) + s[j:]
    ruta.write_text(s, encoding='utf-8')
    print(f'fisica.html: esquemas en {sum(len(v) for v in TARJETAS.values())} tarjetas de {len(TARJETAS)} lecciones')


if __name__ == '__main__':
    aplicar()
