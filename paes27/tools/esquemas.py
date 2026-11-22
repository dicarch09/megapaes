#!/usr/bin/env python3
"""Esquemas visuales (SVG) para las viñetas de «El porqué».

Cada lección tiene una lista de esquemas, uno por paso, en el mismo orden que su <ol>.
Inyecta al inicio de cada <li> y es idempotente: borra los esquemas anteriores antes de poner los nuevos.
Los colores salen de clases (.a .b .w .r .g .m y rellenos .fa .fb .fw .fr .fg .fm) que define core.css,
así siguen el tema claro/oscuro.

Uso: python3 tools/esquemas.py
"""
import math
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FILL = {'a': 'fa', 'b': 'fb', 'w': 'fw', 'r': 'fr', 'g': 'fg', 'm': 'fm'}


def ln(x1, y1, x2, y2, c='m', w=2.5, d=''):
    dash = f' stroke-dasharray="{d}"' if d else ''
    return f'<path class="{c}" d="M{x1} {y1}L{x2} {y2}" stroke-width="{w}" stroke-linecap="round"{dash}/>'


def fl(x1, y1, x2, y2, c='a', w=3):
    a = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - 8 * math.cos(a), y2 - 8 * math.sin(a)
    l = (bx + 4.5 * math.sin(a), by - 4.5 * math.cos(a))
    r = (bx - 4.5 * math.sin(a), by + 4.5 * math.cos(a))
    return ln(x1, y1, round(bx, 1), round(by, 1), c, w) + f'<path class="{FILL[c]}" d="M{x2} {y2}L{l[0]:.1f} {l[1]:.1f}L{r[0]:.1f} {r[1]:.1f}Z"/>'


def tx(x, y, t, anchor='middle'):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}">{t}</text>'


def caja(x, y, w, h, c='a'):
    return f'<rect class="{c}" x="{x}" y="{y}" width="{w}" height="{h}" rx="4" stroke-width="2.5"/>'


def circ(x, y, r, f='fw'):
    return f'<circle class="{f}" cx="{x}" cy="{y}" r="{r}"/>'


def aro(x, y, r, c='m', w=2.5):
    return f'<circle class="{c}" cx="{x}" cy="{y}" r="{r}" stroke-width="{w}"/>'


def poly(pts, c='a', fillc=None, op=.25):
    d = 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + 'Z'
    estilo = f' style="fill:var(--{fillc});fill-opacity:{op}"' if fillc else ''
    return f'<path class="{c}" d="{d}" stroke-width="2"{estilo}/>'


def curva(pts, c='a', w=3):
    return f'<path class="{c}" d="M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + f'" stroke-width="{w}" fill="none" stroke-linecap="round"/>'


def ejes(x0=20, y0=78, w=165, h=68, tx_='t', ty='x'):
    return fl(x0, y0, x0 + w, y0, 'm', 1.8) + fl(x0, y0, x0, y0 - h, 'm', 1.8) + tx(x0 + w - 4, y0 + 12, tx_, 'end') + tx(x0 + 8, y0 - h + 6, ty, 'start')


def svg(*partes):
    return '<svg class="esq" viewBox="0 0 200 92" aria-hidden="true">' + ''.join(partes) + '</svg>'


def puntos(f, x0, x1, n=60):
    return [(x0 + (x1 - x0) * i / n, f(x0 + (x1 - x0) * i / n)) for i in range(n + 1)]


def tachar(x, y, w, t, tachado):
    return tx(x, y, t, 'start') + (ln(x - 2, y - 4, x + w, y - 4, 'r', 2) if tachado else '')


# =====================================================================
# Física · Mecánica
# =====================================================================
ESQ = {
 ('fisica.html', 'fis.mec.cinematica'): [
  svg(fl(15, 60, 190, 60, 'm', 2), tx(30, 80, 'O'), ln(30, 54, 30, 66, 'm', 2.5), circ(120, 60, 7), tx(120, 44, 'x = 3 m'), tx(182, 80, '+', 'end')),
  svg(fl(25, 34, 165, 34, 'b', 3), fl(165, 46, 95, 46, 'b', 3), tx(95, 24, 'distancia = 7 + 4 = 11'), fl(25, 72, 95, 72, 'r', 3.5), tx(60, 88, 'Δx = 3')),
  svg(curva([(40 + 60 * math.cos(t / 10), 46 + 26 * math.sin(t / 10)) for t in range(0, 63)], 'b', 3), circ(100, 46, 6, 'fa'), tx(100, 30, 'vuelve al inicio'), tx(100, 86, 'Δx = 0 → v media = 0')),
  svg(ejes(), curva([(20 + i * 1.6, 78 - 0.006 * (i * 1.6) ** 2 - 4) for i in range(0, 100)], 'a', 3), ln(95, 72, 175, 18, 'w', 2.5), circ(135, 45, 4.5), tx(150, 60, 'pendiente = v', 'start')),
  svg(fl(30, 32, 100, 32, 'g', 4), tx(65, 22, '+20 m/s'), fl(170, 62, 100, 62, 'r', 4), tx(135, 82, '−20 m/s'), tx(40, 70, 'Δv = −40', 'start')),
 ],
 ('fisica.html', 'fis.mec.mru-mrua'): [
  svg(ejes(), ln(20, 66, 175, 22, 'a', 3.5), tx(130, 30, 'recta', 'start')),
  svg(ejes(ty='v'), ln(20, 70, 175, 20, 'b', 3.5), ln(80, 51, 130, 51, 'w', 2, '4 3'), ln(130, 51, 130, 35, 'w', 2, '4 3'), tx(150, 50, 'a', 'start')),
  svg(ejes(ty='v'), poly([(20, 78), (20, 60), (150, 26), (150, 78)], 'b', 'acc2', .3), tx(85, 66, 'área = Δx')),
  svg(ejes(ty='v'), poly([(20, 78), (20, 56), (150, 56), (150, 78)], 'a', 'acc', .25), poly([(20, 56), (150, 22), (150, 56)], 'w', 'warn', .3), tx(85, 70, 'v₀·t'), tx(125, 50, '½at²')),
  svg(ejes(ty='v'), ln(20, 22, 140, 78, 'r', 3.5), circ(140, 78, 5, 'fr'), tx(140, 66, 't = −v₀/a', 'start')),
 ],
 ('fisica.html', 'fis.mec.galileo'): [
  svg(ln(10, 74, 190, 74, 'm', 2.5), caja(55, 40, 90, 30, 'b'), fl(150, 55, 185, 55, 'b', 3), tx(170, 46, 'V'), tx(100, 88, 'andén (S) · tren (S′)')),
  svg(fl(10, 70, 190, 70, 'm', 1.8), fl(60, 40, 190, 40, 'b', 1.8), tx(14, 62, 'S', 'start'), tx(64, 32, 'S′', 'start'), fl(10, 82, 60, 82, 'w', 2.5), tx(35, 92, 'V·t'), circ(140, 40, 5, 'fa'), tx(140, 26, 'x = x′ + V·t')),
  svg(fl(20, 30, 70, 30, 'a', 4), tx(45, 20, 'v′'), tx(80, 34, '+'), fl(92, 30, 172, 30, 'b', 4), tx(132, 20, 'V'), fl(20, 66, 172, 66, 'w', 4.5), tx(96, 86, 'v = v′ + V')),
  svg(aro(55, 42, 22), aro(145, 42, 22), ln(55, 42, 55, 26, 'w', 3), ln(145, 42, 145, 26, 'w', 3), tx(100, 86, 't = t′ y a = a′')),
  svg(caja(40, 14, 120, 66, 'b'), circ(100, 34, 6), fl(100, 42, 100, 74, 'w', 3), tx(100, 90, 'cae recto a tus pies'), fl(165, 47, 192, 47, 'b', 2.5)),
 ],
 ('fisica.html', 'fis.mec.newton'): [
  svg(caja(78, 34, 44, 30), fl(122, 49, 168, 49, 'w', 3.5), fl(78, 49, 32, 49, 'r', 3.5), tx(100, 86, 'ΣF = 0 → v constante')),
  svg(caja(70, 34, 44, 30), fl(114, 49, 175, 49, 'w', 4), tx(150, 40, 'F'), fl(80, 80, 120, 80, 'g', 2.5), tx(100, 26, 'a = F/m')),
  svg(caja(40, 34, 50, 30, 'a'), caja(110, 34, 50, 30, 'b'), fl(90, 44, 128, 44, 'w', 3), fl(110, 56, 72, 56, 'r', 3), tx(100, 86, 'en cuerpos distintos')),
  svg(caja(78, 30, 44, 30), fl(122, 45, 165, 45, 'w', 3), fl(78, 52, 40, 52, 'r', 3), fl(100, 30, 100, 6, 'g', 3), fl(100, 60, 100, 86, 'b', 3), tx(170, 40, 'F', 'start'), tx(32, 48, 'f', 'end'), tx(108, 14, 'N', 'start'), tx(108, 86, 'P', 'start')),
  svg(fl(30, 74, 130, 74, 'a', 3.5), tx(80, 88, '6 N'), fl(30, 74, 30, 14, 'b', 3.5), tx(22, 44, '8 N', 'end'), fl(30, 74, 130, 14, 'w', 4), tx(140, 30, '10 N', 'start')),
 ],
 ('fisica.html', 'fis.mec.fuerzas'): [
  svg(circ(100, 26, 13, 'fa'), fl(100, 40, 100, 84, 'b', 3.5), tx(112, 70, 'P = m·g', 'start')),
  svg(ln(30, 62, 170, 62, 'm', 3), caja(80, 38, 40, 24), fl(100, 38, 100, 6, 'g', 3), fl(100, 62, 100, 88, 'b', 3), tx(110, 16, 'N', 'start'), tx(110, 84, 'P', 'start')),
  svg(ln(20, 10, 60, 10, 'm', 3), curva([(40 + (8 if i % 2 else -8), 14 + i * 4.5) for i in range(12)], 'b', 2.5), caja(28, 66, 24, 18, 'w'), fl(70, 30, 70, 66, 'r', 2.5), tx(76, 52, 'x', 'start'), tx(140, 50, 'F = k·x')),
  svg(ln(20, 70, 180, 70, 'm', 3), caja(80, 44, 40, 26), fl(120, 57, 165, 57, 'w', 3), fl(80, 64, 40, 64, 'r', 3), tx(100, 26, 'f = F (hasta μₑ·N)')),
  svg(ejes(ty='f', tx_='F'), ln(20, 78, 95, 24, 'r', 3), ln(95, 24, 95, 44, 'r', 3), ln(95, 44, 180, 44, 'r', 3), tx(100, 18, 'μₑN', 'start'), '<text x="150" y="38" text-anchor="middle">μ<tspan baseline-shift="sub" font-size="70%">c</tspan>N</text>'),
 ],
}

# =====================================================================
# M2 · lecciones de prioridad A
# =====================================================================
ESQ.update({
 ('m2.html', 'm2.alg.sistemas-rectas'): [
  svg(ejes(ty='y', tx_='x'), ln(30, 74, 170, 18, 'a', 3), ln(70, 58, 130, 58, 'w', 2, '4 3'), ln(130, 58, 130, 34, 'w', 2, '4 3'), tx(100, 70, 'Δx'), tx(136, 50, 'Δy', 'start'), tx(150, 88, 'm = Δy/Δx')),
  svg(ejes(ty='y', tx_='x'), ln(20, 60, 180, 20, 'a', 3), circ(20, 60, 5, 'fw'), tx(28, 72, 'n (corte con Y)', 'start'), tx(150, 34, 'y = mx + n')),
  svg(ln(20, 80, 180, 15, 'a', 3), ln(20, 18, 180, 78, 'b', 3), circ(100, 47.5, 6), tx(110, 40, '(x, y) en ambas', 'start')),
  svg(tx(100, 30, 'm₁x + n₁ = m₂x + n₂'), fl(100, 38, 100, 58, 'm', 2.5), tx(100, 76, 'x = (n₂ − n₁)/(m₁ − m₂)')),
  svg(ln(10, 70, 70, 20, 'a', 3), ln(30, 80, 90, 30, 'b', 3), tx(50, 92, 'paralelas: 0'), ln(115, 75, 185, 20, 'a', 6), ln(115, 75, 185, 20, 'b', 2.5, '6 5'), tx(150, 92, 'coinciden: ∞')),
 ],
 ('m2.html', 'm2.num.log-exp'): [
  svg(tx(55, 40, '2⁵ = 32'), tx(100, 42, '⇔'), tx(150, 40, 'log₂ 32 = 5'), fl(150, 52, 150, 70, 'w', 2.5), tx(150, 86, 'el log es el exponente')),
  svg(tx(100, 26, 'M = bᵖ    N = b^q'), fl(100, 34, 100, 50, 'm', 2.5), tx(100, 66, 'M·N = b^(p+q)'), tx(100, 86, 'log(M·N) = p + q')),
  svg(tx(100, 30, 'M/N = b^(p−q)'), fl(100, 38, 100, 54, 'm', 2.5), tx(100, 72, 'log(M/N) = log M − log N')),
  svg(tx(100, 30, 'Mᵏ = b^(p·k)'), fl(100, 38, 100, 54, 'm', 2.5), tx(100, 72, 'log(Mᵏ) = k·log M'), tx(100, 90, '≠ (log M)ᵏ')),
  svg(ln(30, 88, 120, 2, 'm', 1.5, '4 4'), curva(puntos(lambda x: 80 - 2 ** ((x - 40) / 14) * 10, 20, 105), 'a', 3), curva(puntos(lambda x: 80 - (14 * math.log2(max(x - 30, .5) / 10) + 40) + 30, 34, 180), 'b', 3), tx(60, 18, 'bˣ'), tx(170, 46, 'log_b x', 'end')),
 ],
 ('m2.html', 'm2.pro.condicional'): [
  svg(caja(10, 10, 180, 72, 'm'), f'<rect class="b" x="20" y="18" width="80" height="56" rx="8" stroke-width="3" style="fill:var(--acc2);fill-opacity:.18"/>', tx(60, 50, 'B'), tx(150, 50, 'fuera de B'), ln(115, 30, 185, 70, 'r', 2), ln(185, 30, 115, 70, 'r', 2)),
  svg(f'<circle class="b" cx="80" cy="46" r="34" stroke-width="3"/><circle class="a" cx="120" cy="46" r="34" stroke-width="3"/>', poly([(100, 18), (112, 30), (114, 46), (112, 62), (100, 74), (88, 62), (86, 46), (88, 30)], 'w', 'warn', .45), tx(60, 50, 'B'), tx(144, 50, 'A'), tx(100, 90, 'A ∩ B')),
  svg(tx(100, 34, 'P(A | B) ='), ln(50, 52, 150, 52, 'm', 2.5), tx(100, 46, 'n(A ∩ B)'), tx(100, 72, 'n(B)')),
  svg(tx(100, 24, 'n(A∩B)/n(B)'), fl(100, 30, 100, 44, 'm', 2), tx(100, 62, '÷ total arriba y abajo'), tx(100, 84, '= P(A∩B)/P(B)')),
  svg(circ(20, 46, 4, 'fm'), ln(20, 46, 90, 20, 'w', 3), ln(20, 46, 90, 72, 'm', 2), tx(52, 22, 'P(B)'), ln(90, 20, 165, 8, 'w', 3), ln(90, 20, 165, 34, 'm', 2), tx(128, 6, 'P(A|B)'), tx(150, 60, 'multiplico la rama', 'middle'), tx(176, 12, 'A', 'start')),
 ],
 ('m2.html', 'm2.geo.trig-razones'): [
  svg(poly([(15, 80), (75, 80), (75, 40)], 'a'), poly([(95, 80), (185, 80), (185, 20)], 'b'), tx(100, 92, 'mismo ángulo → semejantes')),
  svg(poly([(30, 80), (160, 80), (160, 18)], 'a'), tx(95, 92, 'adyacente'), tx(168, 52, 'opuesto', 'start'), tx(82, 42, 'hipotenusa', 'end'), tx(50, 76, 'α')),
  svg(aro(70, 50, 36), ln(70, 50, 95.5, 24.5, 'w', 3), ln(95.5, 24.5, 95.5, 50, 'g', 3), ln(70, 50, 95.5, 50, 'b', 3), tx(140, 30, 'x = cos θ', 'start'), tx(140, 52, 'y = sen θ', 'start')),
  svg(poly([(30, 80), (110, 80), (110, 30)], 'a'), tx(70, 92, 'cos'), tx(118, 58, 'sen', 'start'), tx(150, 30, 'sen²+cos²', 'middle'), tx(150, 48, '= 1')),
  svg(ln(10, 46, 190, 46, 'm', 1.5), curva(puntos(lambda x: 46 - 30 * math.sin((x - 10) / 180 * 4 * math.pi), 10, 190, 120), 'a', 3), fl(55, 46, 55, 16, 'w', 2.5), tx(62, 22, 'A', 'start'), ln(10, 84, 100, 84, 'g', 3), tx(55, 80, 'período 2π/B')),
 ],
 ('m2.html', 'm2.sd'): [
  svg(tx(100, 30, '¿un solo valor?'), tx(55, 66, 'x = 3 ✔'), tx(145, 66, 'x = ±3 ✘')),
  svg(tx(40, 22, '(1) sola'), tx(40, 40, '✔ → A o D'), tx(40, 66, '✘ → B, C o E'), caja(100, 8, 90, 76, 'm'), tachar(110, 30, 70, 'B C E', True), tachar(110, 62, 50, 'A D', False)),
  svg(tx(40, 22, '(2) sola'), tx(100, 50, 'decide entre A/D o B vs C/E'), tx(100, 78, 'tapa la (1)')),
  svg(tx(100, 26, 'ninguna sola → juntas'), fl(70, 36, 50, 58, 'g', 2.5), fl(130, 36, 150, 58, 'r', 2.5), tx(50, 76, 'alcanzan: C'), tx(150, 76, 'no: E')),
  svg(tx(100, 24, 'x² = 9 → dos valores'), tx(100, 50, 'x + y = 10 ≡ 2x + 2y = 20'), tx(100, 78, 'no calcules de más')),
 ],
 ('m2.html', 'm2.pro.combinatoria'): [
  svg(circ(20, 46, 4, 'fm'), *[ln(20, 46, 80, 16 + 30 * i, 'a', 2.5) for i in range(3)], *[ln(80, 16 + 30 * i, 150, 8 + 30 * i + 8 * j, 'b', 2) for i in range(3) for j in range(2)], tx(178, 50, '3·2 = 6', 'middle')),
  svg(*[caja(15 + 36 * i, 30, 30, 30, 'a') for i in range(5)], *[tx(30 + 36 * i, 50, str(5 - i)) for i in range(5)], tx(100, 82, '5·4·3·2·1 = 5!')),
  svg(*[caja(25 + 52 * i, 24, 44, 30, 'b') for i in range(3)], tx(47, 44, 'n'), tx(99, 44, 'n−1'), tx(151, 44, 'n−2'), tx(100, 80, 'con orden: n!/(n−k)!')),
  svg(tx(50, 30, 'AB  BA'), fl(90, 26, 120, 26, 'm', 2.5), tx(155, 30, '{A, B}'), tx(100, 66, 'cada grupo se contó k! veces'), tx(100, 86, 'C(n,k) = V/k!')),
  svg(*[circ(20 + 22 * i, 30, 8, 'fa' if i < 2 else 'fm') for i in range(5)], tx(130, 34, 'elijo 2', 'start'), *[circ(20 + 22 * i, 64, 8, 'fm' if i < 2 else 'fw') for i in range(5)], tx(130, 68, 'dejo 3', 'start'), tx(100, 90, 'C(5,2) = C(5,3)')),
 ],
 ('m2.html', 'm2.pro.dispersion'): [
  svg(ln(10, 60, 190, 60, 'm', 2), ln(100, 20, 100, 70, 'a', 2.5, '4 3'), tx(100, 16, 'x̄'), circ(40, 60, 6), circ(160, 60, 6), fl(100, 44, 46, 44, 'r', 2.5), fl(100, 44, 154, 44, 'g', 2.5)),
  svg(tx(100, 34, '−3  −1  0  +1  +3'), fl(100, 44, 100, 60, 'm', 2.5), tx(100, 80, 'suman 0')),
  svg(*[f'<rect class="w" x="{20 + 36 * i}" y="{78 - s * 6}" width="{s * 6}" height="{s * 6}" stroke-width="2" style="fill:var(--warn);fill-opacity:.25"/>' for i, s in enumerate([3, 1, 0.3, 1, 3])], tx(100, 14, 'cuadrados → promedio = varianza')),
  svg(tx(100, 34, 'varianza (notas²)'), fl(100, 42, 100, 58, 'm', 2.5), tx(100, 78, 'σ = √varianza (notas)')),
  svg(*[circ(30 + 14 * i, 30, 5) for i in range(4)], fl(90, 30, 110, 30, 'm', 2), *[circ(120 + 14 * i, 30, 5, 'fb') for i in range(4)], tx(100, 50, '+c: σ igual'), *[circ(40 + 8 * i, 76, 4) for i in range(4)], fl(80, 76, 100, 76, 'm', 2), *[circ(110 + 16 * i, 76, 4, 'fb') for i in range(4)], tx(176, 80, '×k: σ·|k|', 'end')),
 ],
})


# =====================================================================
# Física · Ondas, Electricidad y Tierra
# =====================================================================
def onda(x0, x1, yc, amp, lam, c='a', w=3, fase=0):
    return curva(puntos(lambda x: yc - amp * math.sin(2 * math.pi * (x - x0) / lam + fase), x0, x1, 120), c, w)


def rayo_luz(x, y, n, largo, c='w'):
    return ''.join(ln(x, y, round(x + largo * math.cos(2 * math.pi * k / n), 1), round(y + largo * math.sin(2 * math.pi * k / n), 1), c, 2) for k in range(n))


ESQ.update({
 ('fisica.html', 'fis.ond.elementos'): [
  svg(onda(10, 190, 46, 18, 60), fl(30, 80, 170, 80, 'w', 3), tx(100, 92, 'viaja la energía'), circ(70, 46, 5, 'fr')),
  svg(ln(10, 46, 190, 46, 'm', 1.2), onda(10, 190, 46, 22, 80), ln(30, 16, 110, 16, 'w', 2.5), tx(70, 12, 'λ'), fl(150, 46, 150, 26, 'g', 2.5), tx(158, 40, 'A', 'start')),
  svg(ejes(ty='y'), onda(20, 185, 46, 20, 70, 'b'), ln(38, 84, 108, 84, 'w', 2.5), tx(73, 92, 'T'), tx(150, 20, 'f = 1/T')),
  svg(onda(10, 190, 24, 11, 70, 'm', 2), onda(10, 190, 62, 11, 70, 'a', 3, -math.pi / 2), fl(28, 43, 98, 43, 'w', 2.5), tx(100, 88, 'en un período T avanza λ')),
  svg(ln(100, 6, 100, 86, 'm', 2), onda(10, 100, 46, 16, 45, 'a'), onda(100, 190, 46, 16, 28, 'b'), tx(55, 86, 'aire'), tx(145, 86, 'vidrio: λ menor')),
 ],
 ('fisica.html', 'fis.ond.espejos-lentes'): [
  svg(circ(100, 46, 5), rayo_luz(100, 46, 12, 38, 'w')),
  svg(ln(100, 6, 100, 86, 'b', 3.5), *[ln(10, 24 + 14 * i, 100, 24 + 14 * i, 'w', 2) + ln(100, 24 + 14 * i, 160, 46, 'w', 2) for i in range(4)], circ(160, 46, 4, 'fr'), tx(160, 62, 'F')),
  svg(ln(10, 60, 190, 60, 'm', 1.5), ln(100, 10, 100, 84, 'b', 3), fl(40, 60, 40, 34, 'a', 3), ln(40, 34, 100, 34, 'w', 2), ln(100, 34, 170, 79, 'w', 2), ln(40, 34, 170, 81, 'g', 2), fl(160, 60, 160, 76, 'r', 3)),
  svg(ln(20, 14, 20, 74, 'b', 3), ln(20, 26, 70, 46, 'w', 2), ln(20, 66, 70, 46, 'g', 2), ln(70, 46, 88, 38.8, 'w', 2), ln(70, 46, 88, 53.2, 'g', 2), circ(70, 46, 4, 'fr'), tx(46, 88, 'cruce real'), ln(150, 14, 150, 74, 'b', 3), ln(150, 34, 190, 18, 'w', 2), ln(150, 58, 190, 74, 'g', 2), ln(150, 34, 120, 46, 'm', 1.5, '4 3'), ln(150, 58, 120, 46, 'm', 1.5, '4 3'), circ(120, 46, 4, 'fr'), tx(154, 88, 'cruce virtual')),
  svg(ln(8, 50, 192, 50, 'm', 2), ln(190, 30, 190, 70, 'b', 3), *[ln(x, 46, x, 54, 'm', 2) for x in (130, 70)], tx(130, 66, 'F'), tx(70, 66, '2F'), tx(35, 36, 'menor'), tx(100, 36, 'mayor'), tx(160, 36, 'lupa')),
 ],
 ('fisica.html', 'fis.ond.reflexion-refraccion'): [
  svg(circ(20, 30, 8), rayo_luz(20, 30, 8, 14, 'w'), caja(80, 30, 14, 30, 'm'), poly([(94, 30), (190, 18), (190, 80), (94, 60)], 'm', 'muted', .2), tx(150, 90, 'sombra definida')),
  svg(ln(20, 70, 180, 70, 'm', 3), ln(100, 10, 100, 70, 'm', 1.5, '4 3'), fl(40, 20, 100, 70, 'w', 3), fl(100, 70, 160, 20, 'w', 3), tx(82, 40, 'θ'), tx(118, 40, 'θ')),
  svg(fl(20, 30, 180, 30, 'a', 3), tx(100, 16, 'aire: v ≈ c'), fl(20, 66, 120, 66, 'b', 3), tx(100, 86, 'agua: v = c/1,33')),
  svg(f'<rect x="0" y="46" width="200" height="46" style="fill:var(--acc2);fill-opacity:.15"/>', ln(0, 46, 200, 46, 'm', 2), ln(100, 4, 100, 90, 'm', 1.5, '4 3'), fl(40, 6, 100, 46, 'w', 3), fl(100, 46, 124, 88, 'w', 3), tx(160, 62, 'se acerca'), tx(160, 74, 'a la normal')),
  svg(ln(100, 6, 100, 70, 'm', 2), onda(10, 100, 40, 16, 44, 'w'), onda(100, 190, 40, 16, 30, 'w'), tx(100, 86, 'f igual · λ cambia')),
 ],
 ('fisica.html', 'fis.ond.espectro-color'): [
  svg(fl(20, 20, 150, 20, 'a', 3), tx(158, 24, 'radio', 'start'), fl(20, 46, 150, 46, 'w', 3), tx(158, 50, 'luz', 'start'), fl(20, 72, 150, 72, 'r', 3), tx(158, 76, 'rayos X', 'start'), tx(14, 90, 'todas a c', 'start')),
  svg(*[f'<rect x="{10 + 26 * i}" y="30" width="26" height="24" class="m" stroke-width="1.5"/>' for i in range(7)], tx(100, 22, 'radio · micro · IR · luz · UV · X · γ'), fl(20, 74, 180, 74, 'w', 3), tx(100, 90, 'más frecuencia, menos λ')),
  svg(onda(10, 95, 46, 14, 60, 'b', 2.5), onda(105, 190, 46, 14, 12, 'r', 2.5), tx(52, 86, 'radio: poca energía'), tx(148, 86, 'UV: mucha')),
  svg(poly([(70, 80), (100, 20), (130, 80)], 'b', 'acc2', .15), ln(10, 56, 85, 50, 'm', 3), *[ln(118, 50, 190, 40 + 7 * i, ['r', 'w', 'g', 'a', 'b'][i], 2.5) for i in range(5)], tx(30, 46, 'blanca')),
  svg(circ(100, 50, 18, 'fr'), fl(30, 20, 84, 40, 'a', 3), tx(30, 14, 'luz azul'), tx(100, 88, 'no hay rojo que reflejar → negra')),
 ],
 ('fisica.html', 'fis.ond.doppler-interferencia'): [
  svg(*[aro(100, 46, r, 'a', 2) for r in (10, 22, 34)], circ(100, 46, 4)),
  svg(*[aro(100 - 8 * k, 46, 10 + 12 * k, 'a', 2) for k in range(3)], circ(106, 46, 4, 'fr'), fl(112, 46, 136, 46, 'w', 2.5), tx(165, 24, 'adelante:'), tx(165, 36, 'f mayor'), tx(28, 72, 'atrás:'), tx(28, 84, 'f menor')),
  svg(f'<rect x="20" y="30" width="160" height="22" rx="4" class="m" stroke-width="1.5"/>', *[ln(x, 30, x, 52, 'r', 3) for x in (90, 120, 150)], fl(70, 66, 120, 66, 'r', 2.5), tx(100, 86, 'corrimiento al rojo: se aleja')),
  svg(onda(10, 90, 20, 8, 40, 'a', 2), onda(10, 90, 56, 16, 40, 'w', 3), tx(50, 90, 'constructiva'), onda(110, 190, 14, 6, 40, 'a', 2), onda(110, 190, 30, 6, 40, 'b', 2, math.pi), ln(110, 56, 190, 56, 'w', 3), tx(150, 90, 'destructiva')),
  svg(ln(80, 6, 80, 38, 'm', 4), ln(80, 54, 80, 86, 'm', 4), *[ln(20 + 12 * i, 20, 20 + 12 * i, 72, 'a', 2) for i in range(4)], *[f'<path class="a" d="M{80 + 14 * k} {46 - 12 * k} A {14 * k} {14 * k} 0 0 1 {80 + 14 * k} {46 + 12 * k}" stroke-width="2" fill="none"/>' for k in (1, 2, 3, 4)]),
 ],
 ('fisica.html', 'fis.ele.ohm'): [
  svg(ln(10, 46, 190, 46, 'm', 6), *[circ(25 + 30 * i, 46, 4, 'fb') for i in range(6)], fl(60, 26, 140, 26, 'w', 2.5), tx(100, 84, 'I = q/t')),
  svg(poly([(100, 10), (40, 80), (160, 80)], 'a'), ln(60, 56, 140, 56, 'a', 2), tx(100, 46, 'V'), tx(80, 74, 'I'), tx(120, 74, 'R'), tx(100, 92, 'V = I·R')),
  svg(ln(10, 46, 190, 46, 'm', 2.5), caja(40, 34, 40, 24, 'w'), caja(120, 34, 40, 24, 'b'), tx(60, 50, 'R₁'), tx(140, 50, 'R₂'), fl(20, 24, 50, 24, 'g', 2), fl(100, 24, 130, 24, 'g', 2), tx(100, 86, 'misma I · R = R₁ + R₂')),
  svg(ln(8, 46, 40, 46, 'm', 2.5), ln(160, 46, 192, 46, 'm', 2.5), ln(40, 20, 40, 72, 'm', 2.5), ln(160, 20, 160, 72, 'm', 2.5), ln(40, 20, 160, 20, 'm', 2.5), ln(40, 72, 160, 72, 'm', 2.5), circ(40, 46, 4, 'fr'), circ(160, 46, 4, 'fr'), caja(80, 11, 40, 18, 'w'), caja(80, 63, 40, 18, 'b'), tx(100, 24, 'R₁'), tx(100, 76, 'R₂'), tx(100, 50, 'mismo V')),
  svg(caja(10, 34, 34, 24, 'w'), tx(27, 50, 'R₁'), tx(55, 50, '+'), caja(64, 22, 34, 18, 'b'), caja(64, 52, 34, 18, 'b'), fl(110, 46, 132, 46, 'm', 2.5), caja(140, 34, 50, 24, 'g'), tx(165, 50, 'R'), tx(100, 90, 'primero el paralelo')),
 ],
 ('fisica.html', 'fis.ele.potencia'): [
  svg(circ(100, 40, 16, 'fw'), rayo_luz(100, 40, 10, 30, 'w'), tx(100, 88, '1 W = 1 J cada segundo')),
  svg(caja(6, 26, 54, 30, 'a'), tx(33, 45, '220 V'), tx(70, 46, '×'), caja(80, 26, 44, 30, 'b'), tx(102, 45, '5 A'), tx(134, 46, '='), caja(144, 26, 52, 30, 'g'), tx(170, 45, '1100 W'), tx(33, 76, 'V'), tx(102, 76, 'I'), tx(170, 76, 'P')),
  svg(ejes(ty='P', tx_='t'), poly([(20, 78), (20, 36), (150, 36), (150, 78)], 'w', 'warn', .25), tx(85, 62, 'E = P·t')),
  svg(caja(6, 26, 56, 30, 'w'), tx(34, 45, '18 kWh'), tx(72, 46, '×'), caja(82, 26, 44, 30, 'b'), tx(104, 45, '$180'), tx(136, 46, '='), caja(146, 26, 50, 30, 'g'), tx(171, 45, '$3.240'), tx(34, 76, 'energía'), tx(104, 76, 'precio'), tx(171, 76, 'cuenta')),
  svg(fl(10, 46, 100, 46, 'a', 10), fl(100, 46, 180, 20, 'g', 3), fl(100, 46, 180, 74, 'r', 8), tx(150, 14, 'luz 10 %'), tx(150, 90, 'calor 90 %')),
 ],
 ('fisica.html', 'fis.tie.tectonica'): [
  svg(poly([(20, 20), (80, 14), (90, 50), (70, 80), (30, 70)], 'a', 'acc', .2), poly([(110, 20), (175, 22), (180, 70), (120, 80), (100, 50)], 'b', 'acc2', .2), circ(84, 40, 4, 'fw'), circ(106, 42, 4, 'fw'), tx(100, 92, 'fósiles iguales a ambos lados')),
  svg(caja(10, 20, 85, 20, 'a'), caja(105, 20, 85, 20, 'b'), f'<rect x="10" y="44" width="180" height="36" rx="4" style="fill:var(--warn);fill-opacity:.2"/>', fl(50, 30, 20, 30, 'w', 2.5), fl(150, 30, 180, 30, 'w', 2.5), tx(100, 66, 'astenosfera (plástica)')),
  svg(fl(6, 34, 30, 34, 'a', 3), fl(60, 34, 36, 34, 'a', 3), tx(38, 66, 'convergente'), fl(94, 34, 72, 34, 'b', 3), fl(106, 34, 128, 34, 'b', 3), tx(100, 86, 'divergente'), fl(160, 50, 160, 18, 'g', 3), fl(174, 18, 174, 50, 'g', 3), tx(197, 66, 'transformante', 'end')),
  svg(ln(10, 30, 190, 30, 'm', 3), circ(100, 30, 6, 'fw'), tx(100, 20, 'epicentro'), f'<path class="fr" d="M100 66l4 8 9 1-7 6 2 9-8-5-8 5 2-9-7-6 9-1z"/>', tx(130, 78, 'hipocentro', 'start'), ln(100, 36, 100, 62, 'm', 1.5, '3 3')),
  svg('<rect x="6" y="4" width="188" height="10" style="fill:var(--muted);fill-opacity:.32"/>', tx(100, 12.5, 'litosfera · rígida'), '<rect x="6" y="14" width="188" height="18" style="fill:var(--warn);fill-opacity:.32"/>', tx(100, 26.5, 'astenosfera · plástica'), '<rect x="6" y="32" width="188" height="18" style="fill:var(--mal);fill-opacity:.32"/>', tx(100, 44.5, 'mesosfera'), '<rect x="6" y="50" width="188" height="20" style="fill:var(--acc2);fill-opacity:.32"/>', tx(100, 63.5, 'núcleo externo · líquido'), '<rect x="6" y="70" width="188" height="20" style="fill:var(--acc);fill-opacity:.32"/>', tx(100, 83.5, 'núcleo interno · sólido')),
 ],
})


def aplicar():
    por_pagina = {}
    for (pagina, lid), svgs in ESQ.items():
        por_pagina.setdefault(pagina, []).append((lid, svgs))
    for pagina, lecciones in por_pagina.items():
        p = RAIZ / pagina
        s = p.read_text(encoding='utf-8')
        for lid, svgs in lecciones:
            i = s.index(f'<section class="leccion" id="{lid}"')
            j = s.index('</section>', i)
            sec = s[i:j]
            a = sec.index('<details class="acc">')
            b = sec.index('</details>', a)
            det = re.sub(r'<svg class="esq".*?</svg>', '', sec[a:b], flags=re.S)
            trozos = det.split('<li>')
            if len(trozos) - 1 != len(svgs):
                raise SystemExit(f'{pagina} {lid}: {len(trozos) - 1} pasos y {len(svgs)} esquemas')
            det = trozos[0] + ''.join('<li>' + svgs[k] + trozos[k + 1] for k in range(len(svgs)))
            s = s[:i] + sec[:a] + det + sec[b:] + s[j:]
        p.write_text(s, encoding='utf-8')
        print(f'{pagina}: esquemas en {len(lecciones)} lecciones')


if __name__ == '__main__':
    aplicar()
