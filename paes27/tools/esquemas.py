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
  svg(ln(30, 88, 120, 2, 'm', 1.5, '4 4'), curva(puntos(lambda x: 80 - 2 ** ((x - 40) / 14) * 10, 20, 80), 'a', 3), curva(puntos(lambda x: 80 - (14 * math.log2(max(x - 30, .5) / 10) + 40) + 30, 34, 180), 'b', 3), tx(60, 18, 'bˣ'), tx(170, 46, 'log<tspan baseline-shift="sub" font-size="75%">b</tspan> x', 'end')),
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


# =====================================================================
# M2 · lecciones de prioridad B y C
# =====================================================================
def txs(x, y, t, anchor='middle', tam=11, c=None):
    st = f'font-size:{tam}px' + (f';fill:var(--{c})' if c else '')
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="{st}">{t}</text>'


def rect(x, y, w, h, var='acc', op=.4):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" style="fill:var(--{var});fill-opacity:{op}"/>'


def arco(cx, cy, r, g1, g2, c='w', w=3):
    """Arco de circunferencia de g1 a g2 grados (antihorario, y hacia arriba)."""
    x1, y1 = cx + r * math.cos(math.radians(g1)), cy - r * math.sin(math.radians(g1))
    x2, y2 = cx + r * math.cos(math.radians(g2)), cy - r * math.sin(math.radians(g2))
    grande = 1 if (g2 - g1) % 360 > 180 else 0
    return f'<path class="{c}" d="M{x1:.1f} {y1:.1f}A{r} {r} 0 {grande} 0 {x2:.1f} {y2:.1f}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'


def en_circ(cx, cy, r, g):
    return (round(cx + r * math.cos(math.radians(g)), 1), round(cy - r * math.sin(math.radians(g)), 1))


def campana(x0, x1, mu, sig, base, alto):
    return [(x, base - alto * math.exp(-((x - mu) / sig) ** 2 / 2)) for x in [x0 + (x1 - x0) * i / 100 for i in range(101)]]


def cubo(x, y, l, c='a'):
    d = l * 0.45
    return (poly([(x, y), (x + l, y), (x + l, y - l), (x, y - l)], c, None) + poly([(x, y - l), (x + d, y - l - d), (x + l + d, y - l - d), (x + l, y - l)], c, None)
            + poly([(x + l, y), (x + l + d, y - d), (x + l + d, y - l - d), (x + l, y - l)], c, None))


def ejes_c(cx=100, cy=46, x0=10, x1=190, y0=6, y1=88):
    return fl(x0, cy, x1, cy, 'm', 1.6) + fl(cx, y1, cx, y0, 'm', 1.6)


def cruce(A, B, C, D):
    """Punto donde se cortan los segmentos AB y CD."""
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = A, B, C, D
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t_ = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    return round(x1 + t_ * (x2 - x1), 1), round(y1 + t_ * (y2 - y1), 1)

ESQ.update({
 ('m2.html', 'm2.alg.potencia'): [
  svg(fl(10, 80, 190, 80, 'm', 1.6), fl(100, 88, 100, 4, 'm', 1.6), curva(puntos(lambda x: 80 - 0.03 * (x - 100) ** 2, 56, 144), 'a', 3),
      ln(70, 53, 130, 53, 'w', 1.6, '4 3'), circ(70, 53, 4, 'fw'), circ(130, 53, 4, 'fw'), txs(70, 68, '−x'), txs(130, 68, 'x'), txs(172, 40, 'espejo en', tam=10), txs(172, 53, 'el eje Y', tam=10)),
  svg(ejes_c(), curva(puntos(lambda x: 46 - 1.85e-4 * (x - 100) ** 3, 37, 163), 'b', 3), ln(60, 57.8, 140, 34.2, 'w', 1.6, '4 3'),
      circ(60, 57.8, 4, 'fw'), circ(140, 34.2, 4, 'fw'), circ(100, 46, 3, 'fm'), txs(50, 16, 'simétrica', tam=10), txs(50, 29, 'respecto al origen', tam=10)),
  svg(fl(14, 84, 194, 84, 'm', 1.6), fl(20, 90, 20, 4, 'm', 1.6),
      curva([(20 + x * 110, 84 - x ** 2 * 62) for x in [i / 60 * 1.14 for i in range(61)]], 'a', 2.5),
      curva([(20 + x * 110, 84 - x ** 3 * 62) for x in [i / 60 * 1.09 for i in range(61)]], 'b', 2.5),
      curva([(20 + x * 110, 84 - x ** 4 * 62) for x in [i / 60 * 1.066 for i in range(61)]], 'w', 2.5),
      circ(130, 22, 4, 'fr'), circ(20, 84, 4, 'fr'), txs(136, 18, '(1, 1)', 'start'), txs(76, 54, 'x²', c='acc'), txs(92, 66, 'x³', c='acc2'), txs(104, 78, 'x⁴', c='warn')),
  svg(ejes_c(cy=50), curva(puntos(lambda x: 50 - 0.016 * (x - 100) ** 2, 60, 140), 'a', 2.5), curva(puntos(lambda x: 50 - 0.004 * (x - 100) ** 2, 20, 180), 'b', 2.5),
      curva(puntos(lambda x: 50 + 0.008 * (x - 100) ** 2, 40, 160), 'r', 2.5), txs(140, 12, '2x²', 'start', c='acc'), txs(186, 20, 'x²/2', 'end', c='acc2'), txs(164, 84, '−x²', 'start', c='mal')),
  svg(ejes_c(), curva(puntos(lambda x: 46 - 300 / (x - 100), 107.2, 190), 'a', 3), curva(puntos(lambda x: 46 - 300 / (x - 100), 10, 92.8), 'a', 3),
      txs(150, 20, 'x⁻¹ = 1/x'), txs(56, 84, 'no toca los ejes')),
 ],
 ('m2.html', 'm2.num.financiera'): [
  svg(caja(6, 32, 40, 26, 'm'), txs(26, 50, 'C', tam=13), fl(48, 38, 104, 24, 'g', 2.5), txs(76, 20, '× (1 + i)', c='ok'), caja(108, 10, 86, 24, 'g'), txs(151, 27, 'C(1 + i)'),
      fl(48, 52, 104, 66, 'r', 2.5), txs(76, 80, '× (1 − i)', c='mal'), caja(108, 56, 86, 24, 'r'), txs(151, 73, 'C(1 − i)')),
  svg(fl(10, 84, 194, 84, 'm', 1.6), *[rect(20 + 34 * k, 84 - (24 + 7 * k), 22, 24 + 7 * k, 'acc2', .5) for k in range(5)],
      *[txs(31 + 34 * k, 79 - (24 + 7 * k), '+C·i', tam=9) for k in range(1, 5)], txs(6, 12, 'simple: suma lo mismo', 'start', tam=10.5)),
  svg(fl(10, 84, 194, 84, 'm', 1.6), *[rect(20 + 34 * k, 84 - 26 * 1.25 ** k, 22, 26 * 1.25 ** k, 'acc', .5) for k in range(5)],
      ln(31, 84 - 26, 167, 84 - 26 - 4 * 26 * 0.25, 'm', 1.6, '4 3'), *[txs(48 + 34 * k, 90, '×(1+i)', tam=8.5) for k in range(4)], txs(70, 14, 'compuesto: multiplica')),
  svg(caja(6, 12, 188, 22, 'm'), rect(6, 12, 18.8, 22, 'ok', .7), rect(24.8, 12, 3, 22, 'mal', .9), txs(100, 28, 'sueldo imponible'),
      fl(15, 36, 15, 56, 'g', 2), txs(8, 68, '10 % → tu fondo', 'start', c='ok'), fl(26, 36, 60, 46, 'r', 1.8), txs(64, 50, 'comisión de la AFP', 'start', c='mal'),
      curva(puntos(lambda x: 84 - 10 * 1.018 ** (x - 110), 110, 194, 30), 'g', 2.5), txs(150, 90, 'el fondo rinde', tam=10)),
  svg(rect(6, 14, 120, 20, 'acc2', .5), txs(66, 28, 'monto recibido'), *[caja(6 + 30 * k, 46, 28, 20, 'a') for k in range(6)], txs(96, 80, 'cuota × n = total pagado'),
      rect(126, 14, 60, 20, 'mal', .5), txs(156, 10, 'costo', c='mal'), ln(126, 14, 126, 66, 'r', 1.6, '3 3')),
 ],
 ('m2.html', 'm2.num.reales'): [
  svg(cubo(30, 80, 46, 'b'), txs(53, 62, 'V = 8'), txs(53, 92, 'arista 2'), txs(150, 34, '∛8 = 2'), txs(150, 56, '8^(1/3) = 2', c='ok'), txs(150, 78, 'misma cosa')),
  svg(txs(100, 26, '√4 · √9 = 2 · 3 = 6', tam=13), txs(100, 52, '√(4 · 9) = √36 = 6', tam=13), txs(100, 82, 'iguales: se pueden juntar', c='ok')),
  svg(caja(6, 30, 44, 26, 'm'), txs(28, 48, '√48', tam=13), fl(52, 43, 70, 43, 'm', 2), caja(72, 30, 66, 26, 'w'), txs(105, 48, '√(16 · 3)', tam=12),
      fl(140, 43, 156, 43, 'm', 2), caja(158, 30, 38, 26, 'g'), txs(177, 48, '4√3', tam=13), txs(96, 74, '16 = 4²: cuadrado perfecto', c='warn')),
  svg(*[caja(6 + 30 * k, 14, 27, 22, 'a' if k < 2 else 'b') + txs(19.5 + 30 * k, 30, '√3', tam=10) for k in range(5)], txs(166, 30, '= 5√3', 'start', c='ok'),
      txs(100, 62, '√2 + √3 ≠ √5', c='mal'), txs(100, 82, 'solo se suman raíces iguales', tam=10.5)),
  svg(fl(6, 70, 194, 70, 'm', 1.8), *[ln(20 + 40 * k, 66, 20 + 40 * k, 74, 'm', 1.5) + txs(20 + 40 * k, 86, str(k), tam=10) for k in range(5)],
      poly([(20, 70), (60, 70), (60, 30), (20, 30)], 'b', None), ln(20, 70, 60, 30, 'w', 2), arco(20, 70, 56.6, 0, 45, 'w', 1.6),
      circ(76.6, 70, 4, 'fw'), txs(82, 60, '√2', 'start', c='warn'), circ(40, 70, 3.5, 'fa'), txs(40, 86, '1/2', c='acc', tam=10), circ(145.7, 70, 4, 'fr'), txs(145.7, 60, 'π', c='mal'),
      txs(140, 24, 'irracionales: decimales', tam=10), txs(140, 36, 'infinitos sin período', tam=10)),
 ],
 ('m2.html', 'm2.geo.circunferencia'): [
  svg(aro(70, 46, 36, 'm', 2), arco(70, 46, 36, 40, 140, 'w', 4), ln(70, 46, *en_circ(70, 46, 36, 40), 'a', 2.5), ln(70, 46, *en_circ(70, 46, 36, 140), 'a', 2.5),
      arco(70, 46, 10, 40, 140, 'a', 2), circ(70, 46, 3, 'fm'), txs(70, 64, 'O'), txs(70, 32, '100°', c='acc'), txs(150, 40, 'arco = 100°', c='warn'), txs(150, 58, 'ángulo del centro', tam=10)),
  svg(aro(70, 46, 36, 'm', 2), poly([en_circ(70, 46, 36, 270), (70, 46), en_circ(70, 46, 36, 140)], 'a', 'acc', .25), poly([en_circ(70, 46, 36, 270), (70, 46), en_circ(70, 46, 36, 40)], 'b', 'acc2', .25),
      ln(70, 82, 70, 10, 'w', 1.6, '4 3'), circ(70, 82, 3.5, 'fw'), txs(70, 92, 'C', tam=10), txs(150, 36, 'dos triángulos', tam=11), txs(150, 52, 'isósceles', tam=11), txs(150, 68, '(lados = radios)', tam=10)),
  svg(aro(70, 46, 36, 'm', 2), ln(*en_circ(70, 46, 36, 270), *en_circ(70, 46, 36, 140), 'b', 2.5), ln(*en_circ(70, 46, 36, 270), *en_circ(70, 46, 36, 40), 'b', 2.5),
      ln(70, 46, *en_circ(70, 46, 36, 140), 'a', 2.5), ln(70, 46, *en_circ(70, 46, 36, 40), 'a', 2.5), arco(70, 82, 12, 63, 117, 'b', 2), arco(70, 46, 9, 40, 140, 'a', 2),
      txs(70, 64, 'α', c='acc2'), txs(70, 33, '2α', c='acc'), txs(152, 30, 'del centro', tam=10.5), txs(152, 44, '= 2 × inscrito', tam=10.5), txs(152, 66, 'en el diámetro: 90°', tam=9.5)),
  svg(aro(70, 46, 36, 'm', 2), poly([en_circ(70, 46, 36, g) for g in (100, 200, 290, 20)], 'a', 'acc', .2),
      txs(*[v + d for v, d in zip(en_circ(70, 46, 36, 100), (0, -5))], 'α', c='acc'), txs(*[v + d for v, d in zip(en_circ(70, 46, 36, 290), (4, 14))], '180° − α', c='warn'),
      txs(150, 40, 'opuestos', tam=11), txs(150, 56, 'suman 180°', tam=11)),
  svg(aro(70, 46, 36, 'm', 2), ln(*en_circ(70, 46, 36, 150), *en_circ(70, 46, 36, 350), 'a', 2.5), ln(*en_circ(70, 46, 36, 75), *en_circ(70, 46, 36, 235), 'b', 2.5),
      circ(*cruce(en_circ(70, 46, 36, 150), en_circ(70, 46, 36, 350), en_circ(70, 46, 36, 75), en_circ(70, 46, 36, 235)), 4, 'fw'),
      txs(*en_circ(70, 50, 44, 150), 'A', tam=10), txs(*en_circ(70, 50, 44, 350), 'B', tam=10), txs(*en_circ(70, 50, 44, 75), 'C', tam=10), txs(*en_circ(70, 50, 44, 235), 'D', tam=10),
      txs(150, 40, 'PA · PB', tam=12), txs(150, 58, '= PC · PD', tam=12)),
 ],
 ('m2.html', 'm2.geo.homotecia'): [
  svg(ln(24, 70, 136, 6, 'm', 1.4, '4 3'), circ(60, 46, 4, 'fm'), txs(54, 40, 'O', 'end'), circ(90, 29, 4, 'fa'), txs(96, 32, 'P', 'start', c='acc'),
      circ(120, 12, 4, 'fg'), txs(126, 16, 'P′ (k = 2)', 'start', c='ok'), circ(30, 63, 4, 'fr'), txs(36, 74, 'k = −1', 'start', c='mal')),
  svg(ejes(ty='y', tx_='x'), fl(20, 78, 60, 62, 'a', 2.5), fl(20, 78, 100, 46, 'g', 2.5), circ(60, 62, 4, 'fa'), circ(100, 46, 4, 'fg'),
      txs(56, 56, 'P(2, 1)', 'end', c='acc'), txs(106, 44, 'P′(4, 2)', 'start', c='ok'), txs(150, 22, 'P′ = k · P', c='ok')),
  svg(poly([(20, 82), (65, 72), (45, 50)], 'a', 'acc', .3), poly([(20, 82), (110, 62), (70, 18)], 'b', None), circ(20, 82, 3.5, 'fm'), txs(14, 80, 'O', 'end'),
      txs(70, 84, 'A', tam=10), txs(40, 48, 'B', tam=10), txs(116, 66, 'A′', 'start', tam=10), txs(64, 16, 'B′', 'end', tam=10),
      txs(150, 30, 'A′B′ = 2 · AB', tam=11), txs(150, 48, 'y paralelos', tam=11)),
  svg(caja(20, 52, 24, 24, 'a'), txs(32, 90, 'k = 1', tam=10), caja(70, 28, 48, 48, 'b'), ln(94, 28, 94, 76, 'b', 1.5), ln(70, 52, 118, 52, 'b', 1.5), txs(94, 90, 'k = 2', tam=10),
      txs(162, 40, 'lados ×2', tam=11), txs(162, 58, 'área ×4', c='ok', tam=11)),
  svg(fl(6, 46, 194, 46, 'm', 1.8), *[ln(x, 40, x, 52, 'm', 1.6) + txs(x, 64, e, tam=10) for x, e in ((40, '−1'), (80, '0'), (120, '1'))],
      rect(80, 30, 40, 10, 'acc2', .5), rect(120, 30, 70, 10, 'ok', .5), rect(6, 30, 74, 10, 'mal', .35),
      txs(100, 24, 'reduce', tam=10), txs(155, 24, 'amplía', tam=10), txs(43, 24, 'k &lt; 0: invierte', tam=10), txs(40, 82, 'simetría central', tam=10), txs(120, 82, 'igual', tam=10)),
 ],
 ('m2.html', 'm2.geo.esfera'): [
  svg(caja(40, 16, 60, 60, 'm'), '<ellipse class="m" cx="70" cy="16" rx="30" ry="6" stroke-width="2" fill="none"/>', '<ellipse class="m" cx="70" cy="76" rx="30" ry="6" stroke-width="2" fill="none"/>',
      aro(70, 46, 30, 'b', 2.5), ln(70, 46, 100, 46, 'w', 2), txs(85, 42, 'r', c='warn'), ln(110, 16, 110, 76, 'w', 1.6), txs(116, 50, '2r', 'start', c='warn')),
  svg(caja(40, 16, 60, 60, 'm'), aro(70, 46, 30, 'b', 2.5), rect(40, 28, 60, 8, 'warn', .45), txs(150, 30, 'misma altura', tam=11), txs(150, 48, '→ misma área', c='ok', tam=11)),
  svg(rect(10, 22, 100, 46, 'acc2', .3), caja(10, 22, 100, 46, 'b'), txs(60, 82, '2πr', tam=11), txs(116, 50, '2r', 'start', tam=11),
      txs(162, 30, '4πr²', c='ok', tam=13), *[aro(140 + 15 * k, 58, 6, 'b', 2) for k in range(4)], txs(162, 82, '4 círculos', tam=10)),
  svg(rect(20, 20, 150, 18, 'acc', .5), txs(95, 33, 'cilindro: 2πr³', tam=11), rect(20, 52, 100, 18, 'acc2', .6), txs(70, 65, 'esfera', tam=11), txs(128, 65, '= 2/3', 'start', c='ok', tam=11),
      txs(100, 88, 'V = (4/3)πr³', c='ok')),
  svg(aro(30, 56, 14, 'a', 2.5), txs(30, 86, 'r', tam=11), aro(90, 46, 28, 'b', 2.5), txs(90, 86, '2r', tam=11), txs(162, 34, 'área ×4', tam=11), txs(162, 54, 'volumen ×8', c='ok', tam=11)),
 ],
 ('m2.html', 'm2.pro.binomial-normal'): [
  svg(circ(14, 46, 4, 'fm'), ln(14, 46, 56, 30, 'g', 2.5), ln(56, 30, 100, 46, 'g', 2.5), ln(100, 46, 144, 62, 'r', 2.5), circ(56, 30, 4, 'fg'), circ(100, 46, 4, 'fg'), circ(144, 62, 4, 'fr'),
      txs(32, 30, 'p', c='ok'), txs(80, 30, 'p', c='ok'), txs(124, 46, '1 − p', 'start', c='mal'), txs(100, 86, 'É É F: p · p · (1 − p)')),
  svg(*[txs(40 + 60 * k, 30, s_, tam=13) for k, s_ in enumerate(('ÉÉF', 'ÉFÉ', 'FÉÉ'))], txs(100, 60, '3 maneras = C(3, 2)', c='ok'), txs(100, 82, 'cada una vale p²(1 − p)', tam=10)),
  svg(fl(6, 80, 194, 80, 'm', 1.6), *[rect(14 + 16 * k, 80 - 230 * math.comb(10, k) / 1024, 12, 230 * math.comb(10, k) / 1024, 'acc', .6) for k in range(11)],
      ln(100, 80, 100, 14, 'w', 2, '4 3'), txs(100, 10, 'μ = n·p = 5', c='warn'), ln(75, 20, 125, 20, 'r', 1.6), txs(158, 24, '±σ', c='mal')),
  svg(curva(campana(10, 190, 90, 26, 80, 64), 'a', 3), ln(10, 80, 190, 80, 'm', 1.6), ln(90, 80, 90, 16, 'm', 1.4, '4 3'), ln(129, 80, 129, 34, 'w', 2),
      txs(90, 90, 'μ', tam=11), txs(129, 90, 'x', c='warn', tam=11), fl(92, 60, 127, 60, 'w', 1.8), txs(166, 30, 'z = 1,5', c='warn', tam=11), txs(166, 46, '1,5σ sobre μ', tam=10)),
  svg(poly([(100 - 50, 80)] + [p_ for p_ in campana(50, 150, 100, 25, 80, 66)] + [(150, 80)], 'b', 'acc2', .2), poly([(75, 80)] + [p_ for p_ in campana(75, 125, 100, 25, 80, 66)] + [(125, 80)], 'a', 'acc', .35),
      curva(campana(10, 190, 100, 25, 80, 66), 'a', 3), ln(10, 80, 190, 80, 'm', 1.6), txs(100, 60, '68 %'), txs(100, 90, '±2σ: 95 %', tam=10), txs(176, 30, '±3σ:', tam=10), txs(176, 42, '99,7 %', tam=10)),
 ],
 ('m2.html', 'm2.m1-dificil'): [
  svg(ejes(ty='y', tx_='x'), curva(puntos(lambda x: 26 + 0.012 * (x - 110) ** 2, 50, 170), 'a', 3), ln(110, 10, 110, 78, 'w', 1.6, '4 3'), circ(110, 26, 4.5, 'fr'), txs(116, 22, '(xᵥ, yᵥ)', 'start', c='mal'), txs(110, 90, 'xᵥ = −b/(2a)', c='warn')),
  svg(*[ln(x0, 54, x0 + 56, 54, 'm', 1.6) + curva([(x0 + 28 + u, 54 + d - 0.05 * u * u) for u in range(-25, 26)], c, 2.5) + txs(x0 + 28, 88, e, c=v, tam=10)
        for x0, d, c, v, e in ((4, 14, 'g', 'ok', 'Δ &gt; 0: dos'), (72, 0, 'w', 'warn', 'Δ = 0: una'), (140, -16, 'r', 'mal', 'Δ &lt; 0: ninguna'))]),
  svg(ejes(ty='A', tx_='x'), curva(puntos(lambda x: 78 - 0.0105 * (x - 20) * (180 - x), 20, 180), 'a', 3), circ(100, 78 - 0.0105 * 80 * 80, 5, 'fg'),
      txs(100, 0 + 78 - 0.0105 * 6400 - 8, 'máximo', c='ok'), txs(100, 90, 'a &lt; 0: el vértice es el máximo', tam=10)),
  svg(ln(10, 30, 40, 30, 'a', 3), ln(60, 30, 120, 30, 'b', 3), txs(150, 34, 'largo ×k', 'start', tam=10),
      caja(10, 46, 18, 18, 'a'), caja(60, 46, 36, 36, 'b'), ln(78, 46, 78, 82, 'b', 1.2), ln(60, 64, 96, 64, 'b', 1.2), txs(150, 66, 'área ×k²', 'start', tam=10),
      txs(100, 12, 'k = 2', c='warn')),
  svg(caja(14, 30, 88, 32, 'a'), aro(58, 16, 14, 'b', 2.5), aro(58, 76, 14, 'b', 2.5), txs(58, 51, '2πr', c='acc'), txs(106, 50, 'h', 'start'),
      txs(156, 34, '2 bases: 2πr²', tam=10.5), txs(156, 52, 'manto: 2πrh', tam=10.5), txs(156, 76, 'V = πr²h', c='ok', tam=11)),
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
