#!/usr/bin/env python3
"""Lecciones de m1.html: repaso rápido + trampas típicas, en tarjetas, y 5 preguntas por tema (tools/banco_m1.json).

Ricardo tiene M1 firme: no hay simulaciones, solo lo que hay que recordar y los errores que cuestan puntos.
Escribe las lecciones entre <!-- @@num@@ --> … <!-- @@/num@@ --> (y alg, geo, pro). Es idempotente.
Uso: python3 tools/m1.py
"""
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent


def trampa(no, si):
    return f'<span class="no">{no}</span><span class="si">{si}</span>'


# (id, pestaña, prioridad, título, idea, [(tipo, título, html)])   tipo: 'repaso' o 'trampa'
TEMAS = [
    ('m1.num.enteros-racionales', 'num', 'B', 'Enteros y racionales',
     'Casi todos los errores aquí son de <b>orden de operaciones</b> y de <b>signos</b>. Antes de marcar, revisa los dos.',
     [('repaso', 'Orden de operaciones', 'Paréntesis → potencias → multiplicación y división (de izquierda a derecha) → suma y resta.'),
      ('repaso', 'Signos', '(−) · (−) = + y (−) · (+) = −. Restar un negativo es sumar: 5 − (−3) = 8.'),
      ('repaso', 'Fracciones', 'Sumar: iguala denominadores. Multiplicar: arriba por arriba y abajo por abajo. Dividir: multiplica por el inverso. Comparar: pasa a decimal.'),
      ('trampa', 'Sumar antes de multiplicar', trampa('−3 + 5 · (−2) = 2 · (−2) = −4', '−3 + 5 · (−2) = −3 − 10 = −13')),
      ('trampa', 'Sumar fracciones «de a pares»', trampa('1/2 + 1/3 = 2/5', '1/2 + 1/3 = 3/6 + 2/6 = 5/6')),
      ('trampa', 'Fracción de lo que queda', trampa('Tiene 3/4 y usa 1/3 de eso: 3/4 − 1/3', 'Queda 3/4 · (1 − 1/3) = 1/2'))]),
    ('m1.num.porcentaje', 'num', 'B', 'Porcentaje',
     'Piensa el porcentaje como un <b>factor</b>: subir 20 % es multiplicar por 1,2 y bajar 20 % es multiplicar por 0,8.',
     [('repaso', 'Lo básico', 'a % de b = a/100 · b. Subir p %: × (1 + p/100). Bajar p %: × (1 − p/100).'),
      ('repaso', 'Cambios seguidos', 'Se multiplican los factores: +10 % y luego −10 % = 1,1 · 0,9 = 0,99 (baja 1 %).'),
      ('trampa', 'Subir y bajar lo mismo', trampa('+10 % y −10 %: queda igual', '1,1 · 0,9 = 0,99: queda 1 % más bajo')),
      ('trampa', 'Volver al precio original', trampa('Con 20 % de descuento cuesta $12.000 → original = 12.000 · 1,2', 'original = 12.000 / 0,8 = $15.000')),
      ('trampa', '¿Porcentaje de qué?', trampa('Subió de 50 a 60: subió 10 %', 'Subió 10 sobre 50: 10/50 = 20 %'))]),
    ('m1.num.potencias-raices', 'num', 'B', 'Potencias y raíces',
     'Las propiedades de potencias piden <b>igual base</b> (o igual exponente: aⁿ · bⁿ = (a · b)ⁿ). Las de raíces piden <b>multiplicación o división</b>. Con sumas no funcionan.',
     [('repaso', 'Potencias', 'aᵐ · aⁿ = aᵐ⁺ⁿ<br>aᵐ / aⁿ = aᵐ⁻ⁿ<br>(aᵐ)ⁿ = aᵐⁿ<br>a⁰ = 1 (a ≠ 0)<br>a⁻ⁿ = 1/aⁿ'),
      ('repaso', 'Raíces', 'ⁿ√a = a<sup>1/n</sup><br>a<sup>m/n</sup> = (ⁿ√a)ᵐ<br>√(a · b) = √a · √b<br>Ejemplo: √50 = √(25 · 2) = 5√2'),
      ('trampa', 'Exponente negativo', trampa('2⁻³ = −8', '2⁻³ = 1/2³ = 1/8')),
      ('trampa', 'Raíz de una suma', trampa('√9 + √16 = √25 = 5', '√9 + √16 = 3 + 4 = 7')),
      ('trampa', 'Paréntesis y signo', trampa('(−2)⁴ = −16', '(−2)⁴ = 16, pero −2⁴ = −16')),
      ('trampa', 'Multiplicar potencias', trampa('a³ · a⁵ = a¹⁵', 'a³ · a⁵ = a⁸ (los exponentes se suman)'))]),
    ('m1.alg.expresiones', 'alg', 'B', 'Expresiones algebraicas',
     'Tres productos notables resuelven la mayoría de las preguntas. Y una regla de oro: <b>no se simplifica lo que está sumando</b>.',
     [('repaso', 'Productos notables', '(a ± b)² = a² ± 2ab + b²<br>(a + b)(a − b) = a² − b²<br>(x + a)(x + b) = x² + (a + b)x + ab'),
      ('repaso', 'Factorizar', 'Factor común: 6x² + 9x = 3x(2x + 3). Trinomio x² + bx + c: dos números que sumen b y multipliquen c.'),
      ('repaso', 'Truco útil', 'a² + b² = (a + b)² − 2ab. Sirve cuando te dan la suma y el producto.'),
      ('trampa', 'El cuadrado de una suma', trampa('(x + 3)² = x² + 9', '(x + 3)² = x² + 6x + 9')),
      ('trampa', 'Simplificar una suma', trampa('(x + 3)/3 = x', '(x + 3)/3 = x/3 + 1')),
      ('trampa', 'Menos delante del paréntesis', trampa('−(x − 4) = −x − 4', '−(x − 4) = −x + 4'))]),
    ('m1.alg.ecuaciones', 'alg', 'A', 'Ecuaciones, inecuaciones y sistemas',
     'Despeja con calma y <b>verifica reemplazando</b>. En las inecuaciones hay un solo cuidado extra: el signo negativo.',
     [('repaso', 'Ecuación lineal', 'Lo que suma pasa restando; lo que multiplica pasa dividiendo. Verifica reemplazando el valor.'),
      ('repaso', 'Inecuación', 'Igual que una ecuación, pero si multiplicas o divides por un número negativo, la desigualdad se invierte.'),
      ('repaso', 'Sistemas 2×2', 'Reducción: suma o resta las ecuaciones para eliminar una incógnita. Sustitución: despeja una y reemplázala en la otra.'),
      ('trampa', 'Dividir por un negativo', trampa('−2x &gt; 6 → x &gt; −3', '−2x &gt; 6 → x &lt; −3')),
      ('trampa', 'Distribuir', trampa('3(x − 2) = 3x − 2', '3(x − 2) = 3x − 6')),
      ('trampa', 'Contestar lo que preguntan', trampa('Resuelves x = 7, y = 3 y marcas 7', 'Si piden x · y, la respuesta es 21'))]),
    ('m1.alg.funciones', 'alg', 'A', 'Función lineal, afín y cuadrática',
     'En la recta mira la <b>pendiente</b> y el <b>corte con Y</b>. En la parábola, el <b>vértice</b>, los <b>ceros</b> y hacia dónde abre.',
     [('repaso', 'Afín y lineal', 'y = mx + n. m = Δy/Δx (pendiente); n = corte con el eje Y. Lineal: n = 0 (pasa por el origen).'),
      ('repaso', 'Cuadrática', 'y = ax² + bx + c. a &gt; 0 abre hacia arriba. Vértice: x = −b/(2a). Corte con Y: (0, c). Ceros: ax² + bx + c = 0. Discriminante b² − 4ac: &gt; 0 dos ceros reales (corta el eje X dos veces); = 0 uno (toca el eje X en el vértice); &lt; 0 ninguno (no corta el eje X).'),
      ('trampa', 'Pendiente al revés', trampa('m = Δx / Δy', 'm = Δy / Δx')),
      ('trampa', 'Signo del vértice', trampa('y = x² − 6x + 5: vértice en x = −3', 'x = −b/(2a) = −(−6)/2 = 3')),
      ('trampa', 'Reemplazar un negativo', trampa('f(x) = x², f(−4) = −4² = −16', 'f(−4) = (−4)² = 16: usa paréntesis'))]),
    ('m1.alg.proporcionalidad', 'alg', 'C', 'Proporcionalidad',
     'Pregúntate: si una cantidad aumenta, ¿la otra aumenta en la misma proporción (<b>directa</b>) o disminuye (<b>inversa</b>)?',
     [('repaso', 'Directa', 'y / x es constante. Si x se duplica, y se duplica. Su gráfico es una recta que pasa por el origen.'),
      ('repaso', 'Inversa', 'x · y es constante. Si x se duplica, y se reduce a la mitad. Su gráfico es una hipérbola.'),
      ('trampa', 'Trabajadores y días', trampa('6 trabajadores tardan 10 días; 4 tardan 10 · 4/6', 'Menos trabajadores, más días: 6 · 10 = 4 · d → d = 15')),
      ('trampa', 'Crecer no basta', trampa('y crece cuando x crece: es directa', 'Directa exige y/x constante (y = 2x + 1 crece, pero no es proporcional)'))]),
    ('m1.geo.areas-volumenes', 'geo', 'A', 'Áreas y volúmenes (incluye cilindro)',
     'Anota la fórmula antes de reemplazar y revisa dos cosas: <b>radio o diámetro</b> y <b>unidades</b>.',
     [('repaso', 'Áreas', 'Triángulo: b · h / 2<br>Paralelogramo: b · h<br>Trapecio: (B + b) · h / 2<br>Círculo: πr²; su perímetro: 2πr'),
      ('repaso', 'Cuerpos', 'Cubo: área 6a², volumen a³. Paralelepípedo: área 2(ab + bc + ac), volumen abc. Cilindro: área 2πr² + 2πrh, volumen πr²h.'),
      ('repaso', 'Unidades', '1 m³ = 1.000 L<br>1 L = 1.000 cm³<br>1 m² = 10.000 cm²'),
      ('trampa', 'Radio o diámetro', trampa('Diámetro 10 → A = π · 10²', 'r = 10/2 = 5 → A = 25π')),
      ('trampa', 'El trapecio', trampa('A = (B + b) · h', 'A = (B + b) · h / 2')),
      ('trampa', 'Pasar m² a cm²', trampa('1 m² = 100 cm²', '1 m² = 100 · 100 = 10.000 cm²'))]),
    ('m1.geo.semejanza-pitagoras', 'geo', 'A', 'Semejanza y Pitágoras',
     'Pitágoras solo en triángulos <b>rectángulos</b>. En semejanza, todo depende de la <b>razón k</b> entre lados correspondientes.',
     [('repaso', 'Pitágoras', 'a² + b² = c² (c es la hipotenusa, frente al ángulo recto). Tríos: 3-4-5, 5-12-13, 6-8-10, 8-15-17.'),
      ('repaso', 'Semejanza', 'Mismos ángulos y lados proporcionales (razón k). Perímetros × k, áreas × k², volúmenes × k³.'),
      ('repaso', 'Escalas', '1 : 50.000 significa que 1 cm del mapa son 50.000 cm reales (500 m).'),
      ('trampa', 'Buscar un cateto', trampa('Hipotenusa 5 y cateto 3: √(25 + 9)', 'Para un cateto se resta: √(25 − 9) = 4')),
      ('trampa', 'Áreas semejantes', trampa('Razón 1 : 3 → el área se triplica', 'El área se multiplica por 3² = 9')),
      ('trampa', 'Unidades de la escala', trampa('400.000 cm = 40 km', '400.000 cm = 4.000 m = 4 km'))]),
    ('m1.geo.transformaciones', 'geo', 'C', 'Transformaciones isométricas',
     'Las isometrías mueven figuras <b>sin cambiar su forma ni su tamaño</b>. Basta con saber qué le pasa a un punto (x, y).',
     [('repaso', 'Reglas', 'Traslación por (a, b): (x + a, y + b). Reflexión en el eje X: (x, −y). En el eje Y: (−x, y). Rotación 90° antihoraria con centro en el origen: (−y, x). Rotación 180° con centro en el origen: (−x, −y).'),
      ('trampa', 'Eje X o eje Y', trampa('Reflejar (3, 5) en el eje Y → (3, −5)', '(−3, 5): reflejar en el eje Y cambia la x')),
      ('trampa', 'Sentido de giro', trampa('90° antihorario: (x, y) → (y, −x)', '(x, y) → (−y, x); (y, −x) es el horario'))]),
    ('m1.pro.datos', 'pro', 'B', 'Datos y medidas de posición',
     'Primero <b>ordena</b> los datos. Después ubica la mediana y los cuartiles: dividen los datos en cuatro partes iguales.',
     [('repaso', 'Tablas y promedio', 'Frecuencia relativa = absoluta / total (× 100 para %). Promedio = suma de los datos / cantidad de datos.'),
      ('repaso', 'Cuartiles y cajón', 'Q₂ = mediana. Q₁ deja el 25 % de los datos abajo; Q₃, el 75 %. El percentil k deja el k % abajo. Cómo hallar Q₁: ordena, toma la mitad de abajo (sin la mediana si n es impar) y busca su mediana; Q₃ igual con la mitad de arriba. Diagrama de cajón: mínimo, Q₁, mediana, Q₃ y máximo; la caja tiene el 50 % central.'),
      ('trampa', 'Mediana sin ordenar', trampa('Mediana de 9, 2, 7: el dato del medio es 2', 'Ordena: 2, 7, 9 → la mediana es 7')),
      ('trampa', 'Leer el cajón', trampa('La línea de la caja es el promedio', 'Es la mediana')),
      ('trampa', 'La nota que falta', trampa('Promedio 5,5 en 4 notas; para 5,8: (5,5 + x)/2 = 5,8', '(4 · 5,5 + x)/5 = 5,8 → x = 7,0'))]),
    ('m1.pro.probabilidad', 'pro', 'B', 'Probabilidad (Laplace y reglas)',
     'Antes de contar, escribe <b>todos los casos posibles</b> y revisa si son igual de probables. «O» suma (restando lo que se repite); «y» multiplica.',
     [('repaso', 'Laplace', 'P = casos favorables / casos posibles (si todos son igual de probables). 0 ≤ P ≤ 1. P(no A) = 1 − P(A).'),
      ('repaso', 'Reglas', '«O»: P(A ∪ B) = P(A) + P(B) − P(A ∩ B). «Y» (independientes): P(A) · P(B). Sin reposición la segunda cambia: 5/10 · 4/9.'),
      ('trampa', 'Casos que no son igual de probables', trampa('Dos monedas: 0, 1 o 2 caras → P(una cara) = 1/3', 'Casos: CC, CS, SC, SS → P = 2/4 = 1/2')),
      ('trampa', 'Contar dos veces', trampa('P(fútbol o básquetbol) = 18/30 + 12/30', 'Resta a los que juegan ambos: (18 + 12 − 5)/30')),
      ('trampa', 'Sin reposición', trampa('Dos rojas sin devolver: 5/10 · 5/10', '5/10 · 4/9: queda una roja menos'))]),
]


def leccion(tid, tab, prio, titulo, idea, tarjetas):
    cards = '\n'.join(f'      <div class="tarjeta {tipo}"><span class="onda">{"repaso rápido" if tipo == "repaso" else "trampa"}</span><h4>{tit}</h4><p>{html}</p></div>'
                      for tipo, tit, html in tarjetas)
    return (f'  <section class="leccion" id="{tid}" data-tab="{tab}">\n'
            f'    <div class="lec-head"><h2>{titulo}</h2><span class="chip {prio}">{prio}</span><span class="dom" data-tema="{tid}"></span></div>\n'
            f'    <div class="lec-body">\n    <p class="idea">{idea}</p>\n    <div class="tarjetas">\n{cards}\n    </div>\n'
            f'    <div class="paso"><h3><span class="n">✓</span> Práctica: 5 preguntas</h3><div class="practica" data-temas="{tid}"></div></div>\n'
            '    </div>\n  </section>')


def aplicar():
    p = RAIZ / 'm1.html'
    s = p.read_text(encoding='utf-8')
    for tab in ('num', 'alg', 'geo', 'pro'):
        html = '\n'.join(leccion(*t) for t in TEMAS if t[1] == tab)
        s, n = re.subn(rf'(<!-- @@{tab}@@ -->).*?(<!-- @@/{tab}@@ -->)', lambda m: f'{m.group(1)}\n{html}\n  {m.group(2)}', s, flags=re.S)
        assert n == 1, tab
    p.write_text(s, encoding='utf-8')
    print(f'm1.html: {len(TEMAS)} temas, {sum(len(t[5]) for t in TEMAS)} tarjetas')


if __name__ == '__main__':
    aplicar()
