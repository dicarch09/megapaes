#!/usr/bin/env python3
"""Fichas finales (index.html, pestaña «Fichas»): una por prueba, con fórmulas y trampas para la mañana del examen.

El contenido sigue lo que enseñan las lecciones («El porqué» de M2 y Física, tarjetas de M1 y de Lectora).
La ficha de M1 se arma con las tarjetas de tools/m1.py. Algunos dibujos se copian de «El porqué» de cada lección.
Escribe el HTML entre <!-- @@fichas@@ --> y <!-- @@/fichas@@ --> de index.html. Es idempotente.
Uso: python3 tools/fichas.py
"""
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / 'tools'))
import m1  # noqa: E402

PAGINAS = {p: (RAIZ / p).read_text(encoding='utf-8') for p in ('m2.html', 'fisica.html')}


def esq(pagina, leccion, i):
    """El dibujo del paso i (desde 0) de «El porqué» de una lección."""
    s = PAGINAS[pagina]
    sec = re.search(r'<section class="leccion" id="' + re.escape(leccion) + r'"(.*?)</section>', s, re.S).group(1)
    pq = re.search(r'<details class="acc">.*?<ol>(.*?)</ol>', sec, re.S).group(1)
    li = re.findall(r'<li>(.*?)</li>', pq, re.S)[i]
    return re.search(r'<svg class="esq".*?</svg>', li, re.S).group(0)


def fi(tema, titulo, lineas, trampa=None, dib='', prio=None):
    tr = f'<div class="fi-tr"><span class="no">{trampa[0]}</span><span class="si">{trampa[1]}</span></div>' if trampa else ''
    chip = f'<span class="chip {prio}">{prio}</span>' if prio else ''
    attr = f' data-tema="{tema}"' if tema else ''
    return (f'<div class="fi"{attr}><h4>{titulo} {chip}<span class="fi-dom"></span></h4>{dib}'
            f'<ul>{"".join(("<li class=\"t\">" if x.startswith("<table") else "<li>") + x + "</li>" for x in lineas)}</ul>{tr}</div>')


def eje(nombre, items):
    return f'<section class="fi-eje"><h3>{nombre}</h3>{"".join(items)}</section>'


def tabla(filas, cab=None):
    h = ''.join(f'<th>{c}</th>' for c in cab) if cab else ''
    return '<table class="fi-tab">' + (f'<tr>{h}</tr>' if h else '') + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in f) + '</tr>' for f in filas) + '</table>'


def ficha(pr, titulo, cuando, consejos, ejes):
    return (f'<article class="ficha" data-ficha="{pr}" hidden><header class="fi-cab fi-{pr}"><h2>{titulo}</h2><p>{cuando}</p></header>'
            f'<ul class="fi-consejos">{"".join(f"<li>{c}</li>" for c in consejos)}</ul><div class="fi-cols">{"".join(ejes)}</div></article>')


# =====================================================================================
# M2
# =====================================================================================
M2 = ficha('M2', 'Ficha final · Matemática 2', 'Lunes 30 de noviembre, 15:00 · 55 preguntas (50 cuentan) en 2 h 20 min · unos 2½ min por pregunta', [
    'M2 también evalúa todo M1: si una pregunta parece de M1, no es una trampa, es parte de la prueba.',
    'Las de suficiencia de datos vienen al final: guarda tiempo para ellas y no calcules de más.',
    'No hay descuento por error: no dejes ninguna en blanco.',
], [
    eje('Álgebra y funciones', [
        fi('m2.alg.sistemas-rectas', 'Rectas y sistemas 2×2', [
            'Pendiente m = (y₂ − y₁)/(x₂ − x₁). Recta: y = mx + n (n = corte con el eje Y).',
            'En ax + by = c (b ≠ 0): m = −a/b. Sin despejar: a₁/a₂ = b₁/b₂ ≠ c₁/c₂ → paralelas (0 soluciones); a₁/a₂ = b₁/b₂ = c₁/c₂ → misma recta (infinitas).',
            'Se cortan (m₁ ≠ m₂): <b>1 solución</b>. Paralelas (m igual, n distinto): <b>0</b>. Misma recta: <b>infinitas</b>.',
            'Perpendiculares: m₁ · m₂ = −1.',
        ], ('En 2x + 3y = 6 la pendiente es 2.', 'Despejo: y = −(2/3)x + 2, así que m = −2/3.'), esq('m2.html', 'm2.alg.sistemas-rectas', 4), 'A'),
        fi('m2.alg.trig-funciones', 'Gráficos de seno y coseno', [
            'f(x) = A·sen(Bx) + C: amplitud |A|, período 2π/|B| (en grados, 360°/|B|), máximo C + |A|, mínimo C − |A|.',
            'sen y cos van de −1 a 1 y se repiten cada 360° = 2π. sen(0) = 0; cos(0) = 1.',
        ], ('El período de sen(2x) es 2.', 'Período = 2π/B = 2π/2 = π.'), prio='B'),
        fi('m2.alg.potencia', 'Función potencia a·xⁿ', [
            'n par: simétrica respecto del eje Y (función par). n impar: simétrica respecto del origen.',
            'Con a = 1 y n ≥ 1, todas pasan por (0, 0) y (1, 1). Con n negativo (xⁿ = 1/x<sup>|n|</sup>) no existe en x = 0, pero igual pasa por (1, 1). a &lt; 0 la refleja en el eje X.',
            'Entre 0 y 1, más exponente da un número más chico: 0,5³ = 0,125 &lt; 0,5² = 0,25.',
        ], ('Para x entre 0 y 1, x³ &gt; x².', 'Es al revés: x³ &lt; x² (y para x &gt; 1, x³ &gt; x²).'), prio='C'),
        fi('m2.m1-dificil', 'Cuadrática, semejanza y cilindro', [
            'Vértice: x = −b/(2a). Δ = b² − 4ac: Δ &gt; 0 dos soluciones; Δ = 0 una; Δ &lt; 0 ninguna real.',
            'a &gt; 0 abre hacia arriba (mínimo); a &lt; 0 hacia abajo (máximo).',
            'Razón de semejanza k: longitudes ×k, áreas ×k², volúmenes ×k³.',
            'Cilindro: V = πr²h; área total = 2πr² + 2πrh.',
        ], ('Si el radio del cilindro se duplica, el volumen se duplica.', 'Se multiplica por 4, porque el radio está al cuadrado (πr²h).'), prio='C'),
    ]),
    eje('Números', [
        fi('m2.num.log-exp', 'Logaritmos, exponencial y logarítmica', [
            'log<sub>b</sub> N = k ⇔ bᵏ = N, con b &gt; 0, b ≠ 1 y N &gt; 0. log<sub>b</sub> 1 = 0; log<sub>b</sub> b = 1.',
            'log(M·N) = log M + log N; log(M/N) = log M − log N; log(Mᵏ) = k·log M.',
            'Cambio de base: log<sub>b</sub> N = log N / log b.',
            'y = bˣ pasa por (0, 1); y = log<sub>b</sub> x pasa por (1, 0) y solo existe para x &gt; 0. Son reflejo una de otra en y = x. Crecen si b &gt; 1.',
        ], ('log(M + N) = log M + log N.', 'No hay regla para la suma. Y ojo: (log M)² ≠ 2·log M.'), esq('m2.html', 'm2.num.log-exp', 4), 'A'),
        fi('m2.num.reales', 'Operatoria en los reales', [
            'ⁿ√(aᵐ) = a<sup>m/n</sup>; √a · √b = √(ab).',
            'Simplificar: √48 = √(16·3) = 4√3. Solo se suman raíces iguales: 2√3 + 3√3 = 5√3.',
            '(√a + √b)(√a − √b) = a − b: sirve para racionalizar.',
        ], ('√(9 + 16) = √9 + √16 = 7.', '√(9 + 16) = √25 = 5.'), prio='C'),
        fi('m2.num.financiera', 'Matemática financiera', [
            'Monto final con interés simple: C·(1 + i·n) (el interés ganado es C·i·n). Compuesto: C·(1 + i)ⁿ (interés = monto − C).',
            'i en decimal (5 % = 0,05) y en la misma unidad que n: tasa mensual con meses, tasa anual con años.',
            'Crédito: cuotas pagadas = cuota × n.º de cuotas. Costo del crédito = cuotas pagadas − monto prestado. Con pie: (pie + cuotas) − precio al contado.',
            'AFP: cada mes se descuenta el 10 % del sueldo imponible para tu cuenta, más la comisión de la AFP.',
        ], ('Subir 5 % y luego bajar 5 % deja el precio igual.', '1,05 · 0,95 = 0,9975: queda 0,25 % más bajo.'), prio='B'),
    ]),
    eje('Geometría', [
        fi('m2.geo.trig-razones', 'Razones trigonométricas', [
            'sen α = opuesto/hipotenusa; cos α = adyacente/hipotenusa; tan α = opuesto/adyacente = sen α/cos α.',
            'sen²α + cos²α = 1. En la circunferencia de radio 1, el punto del ángulo θ es (cos θ, sen θ).',
            tabla([['sen', '1/2', '√2/2', '√3/2'], ['cos', '√3/2', '√2/2', '1/2'], ['tan', '√3/3', '1', '√3']], ['', '30°', '45°', '60°']),
        ], ('Tomar el cateto que toca el ángulo como el opuesto.', 'El opuesto es el que NO toca el ángulo; el adyacente sí lo toca (y no es la hipotenusa).'), prio='A'),
        fi('m2.geo.circunferencia', 'Ángulos, arcos, cuerdas y secantes', [
            'Ángulo del centro = arco. Ángulo inscrito = la mitad del arco que abarca.',
            'Inscrito en una semicircunferencia = 90°. Cuadrilátero inscrito: ángulos opuestos suman 180°.',
            'Cuerdas que se cortan en P: PA·PB = PC·PD (los dos trozos de cada cuerda). Dos secantes desde P exterior: PA·PB = PC·PD, con PA = tramo exterior y PB = secante completa (no la cuerda).',
            'Largo de un arco de α°: 2πr·α/360.',
        ], ('El ángulo inscrito mide lo mismo que su arco.', 'Mide la mitad: un arco de 100° da un inscrito de 50°.'), esq('m2.html', 'm2.geo.circunferencia', 2), 'B'),
        fi('m2.geo.homotecia', 'Homotecia', [
            'Con centro O y razón k: P\' = O + k·(P − O). Con centro en el origen: P\' = k·P.',
            'Lados ×|k|, áreas ×k², volúmenes ×|k|³. k &lt; 0: la imagen queda al otro lado de O (rotada en 180°).',
            '|k| &gt; 1 amplía; 0 &lt; |k| &lt; 1 reduce; k = −1 es una simetría central.',
        ], ('Con k = −2 el área se multiplica por −2.', 'Se multiplica por k² = 4.'), prio='B'),
        fi('m2.geo.esfera', 'Esfera', [
            'Área = 4πr². Volumen = (4/3)πr³.',
            'Semiesfera: volumen (2/3)πr³; área curva 2πr² (+ πr² de la base si es sólida = 3πr²).',
            'Radio ×k → área ×k², volumen ×k³.',
        ], ('Usar el diámetro en la fórmula.', 'Si te dan el diámetro d, usa r = d/2 antes de elevar.'), prio='B'),
    ]),
    eje('Probabilidad y estadística', [
        fi('m2.pro.condicional', 'Probabilidad condicional', [
            'P(A | B) = P(A ∩ B)/P(B). En una tabla: la fila o columna de B es el nuevo total.',
            'Árbol: multiplica a lo largo de cada camino y suma los caminos que llegan al mismo resultado (probabilidad total).',
            'A y B independientes ⇔ P(A | B) = P(A) ⇔ P(A ∩ B) = P(A)·P(B).',
        ], ('P(A | B) = P(B | A).', 'Mismo numerador, distinto denominador: n(A ∩ B)/n(B) vs n(A ∩ B)/n(A).'), prio='A'),
        fi('m2.pro.combinatoria', 'Permutaciones y combinatoria', [
            'Ordenar n cosas: n!. Elegir k con orden y sin repetir: n!/(n − k)!. Con repetición: nᵏ.',
            'Sin orden: C(n, k) = n!/(k!·(n − k)!). C(n, k) = C(n, n − k).',
            'Lo que ocurre a la vez («y») se multiplica: «2 de 5 y 2 de 4» = C(5, 2)·C(4, 2) = 60. Casos que se excluyen («o») se suman.',
        ], ('Elegir presidente y tesorero con C(n, 2).', 'Los cargos son distintos: el orden importa → n·(n − 1).'), prio='A'),
        fi('m2.pro.dispersion', 'Medidas de dispersión', [
            'Rango = máximo − mínimo. Varianza = Σ(xᵢ − x̄)²/n. Desviación estándar σ = √varianza.',
            'Sumar c a todos: la media sube c y σ no cambia. Multiplicar por k: σ ×|k| y varianza ×k².',
        ], ('Si a todos les sumo 5 puntos, σ sube 5.', 'σ no cambia: todos se mueven igual. Solo la media sube 5.'), prio='A'),
        fi('m2.pro.binomial-normal', 'Binomial y normal', [
            'Binomial: P(X = k) = C(n, k)·pᵏ·(1 − p)ⁿ⁻ᵏ. μ = n·p; σ = √(n·p·(1 − p)).',
            'Normal: z = (x − μ)/σ. Entre μ ± σ ≈ 68 %; μ ± 2σ ≈ 95 %; μ ± 3σ ≈ 99,7 %.',
            'Simetría: P(Z ≤ 0) = 0,5; P(Z ≤ −a) = 1 − P(Z ≤ a).',
        ], ('Fuera de μ ± σ queda 32 % en cada cola.', 'Queda ≈ 32 % entre las dos colas: ≈ 16 % en cada una.'), esq('m2.html', 'm2.pro.binomial-normal', 4), 'B'),
    ]),
    eje('Suficiencia de datos (al final)', [
        fi('m2.sd', 'Método de descarte', [
            '<b>1.</b> Tapa la (2): ¿la (1) sola permite responder con un único resultado? Sí → quedan A o D. No → quedan B, C o E.',
            '<b>2.</b> Tapa la (1) y mira la (2) sola. Con eso decides.',
            '<b>3.</b> Solo si ninguna sirve sola, júntalas: alcanzan → C; no alcanzan → E.',
            tabla([['A', '(1) por sí sola'], ['B', '(2) por sí sola'], ['C', 'Ambas juntas, (1) y (2)'], ['D', 'Cada una por sí sola, (1) ó (2)'], ['E', 'Se requiere información adicional']]),
        ], ('Calcular el valor completo antes de decidir.', 'Basta saber si lo que PREGUNTAN queda con un solo valor. Ojo: x² = 9 deja x = 3 o −3 (no alcanza para x, pero sí para x²).'), prio='A'),
    ]),
])

# =====================================================================================
# Física (Ciencias)
# =====================================================================================
CIE = ficha('CIE', 'Ficha final · Ciencias Física', 'Martes 1 de diciembre, 15:00 · 80 preguntas (75 cuentan) en 2 h 40 min: 54 del módulo común (Biología, Química y Física) y 26 de Física', [
    'Unos 2 minutos por pregunta. Las de Biología y Química suelen ser más cortas: no te quedes pegado en una.',
    'Lee las unidades: km/h → m/s: ÷ 3,6 (m/s → km/h: × 3,6); minutos → segundos: × 60; W → kW: ÷ 1000.',
    'Si la pregunta da g, usa ese valor (a menudo 10 m/s²).',
], [
    eje('Mecánica', [
        fi('fis.mec.cinematica', 'Posición, velocidad y aceleración', [
            'Desplazamiento Δx = x<sub>final</sub> − x<sub>inicial</sub> (con signo). Distancia recorrida: todos los tramos sin signo; nunca menor que |Δx|.',
            'Rapidez media = distancia/Δt. Velocidad media = Δx/Δt. Aceleración media = Δv/Δt.',
            'Hay aceleración si cambia la rapidez, la dirección o el sentido.',
        ], ('Si vuelve al punto de partida, su velocidad media es igual a su rapidez media.', 'Su velocidad media es 0 (Δx = 0), aunque la rapidez media no.'), prio='A'),
        fi('fis.mec.mru-mrua', 'MRU y MRUA', [
            'MRU: x = x₀ + v·t. En x–t es una recta; su pendiente es v.',
            'MRUA: v = v₀ + a·t; x = x₀ + v₀·t + ½·a·t².',
            'En v–t: la pendiente es a y el área bajo la curva (con signo: bajo el eje cuenta negativa) es el desplazamiento.',
            'Frena si a y v tienen signos opuestos. Se detiene en t = −v₀/a.',
        ], ('En un gráfico x–t, la velocidad es la altura de la curva.', 'En x–t la velocidad es la pendiente. La altura es la posición.'), esq('fisica.html', 'fis.mec.mru-mrua', 2), 'A'),
        fi('fis.mec.galileo', 'Relatividad de Galileo', [
            'Tren con velocidad V respecto del andén; x\' y v\' se miden en el tren. Desde el andén: x = x\' + V·t y v = v\' + V (con signo). Velocidad de A respecto de B = v<sub>A</sub> − v<sub>B</sub>.',
            'El tiempo y la aceleración son iguales en ambos sistemas.',
            'Dentro de un sistema a velocidad constante, todo pasa igual que en reposo.',
        ], ('En un bus a velocidad constante, una moneda que cae se va hacia atrás.', 'Cae a tus pies: lleva la misma velocidad que el bus.'), prio='B'),
        fi('fis.mec.newton', 'Leyes de Newton', [
            '1.ª: si ΣF = 0, la velocidad no cambia (reposo o línea recta a velocidad constante).',
            '2.ª: ΣF = m·a (a en la dirección de ΣF).',
            '3.ª: acción y reacción son iguales, opuestas y actúan sobre cuerpos distintos.',
            'Diagrama de cuerpo libre: solo las fuerzas que actúan SOBRE el cuerpo.',
        ], ('Acción y reacción se anulan.', 'No se anulan: actúan sobre cuerpos distintos.'), prio='A'),
        fi('fis.mec.fuerzas', 'Peso, normal, tensión, Hooke y roce', [
            'Peso P = m·g (N): la masa (kg) es la misma en todo lugar; el peso cambia con g.',
            'Normal: perpendicular a la superficie. N = P solo en superficie horizontal, sin otras fuerzas verticales y sin aceleración vertical (en un ascensor que acelera hacia arriba, N &gt; P).',
            'Hooke: F = k·x, con x = cuánto se estira o comprime (largo final − largo natural), en metros; no el largo total. Tensión: igual en toda la cuerda ideal.',
            'Roce estático ≤ μ<sub>e</sub>·N (vale lo justo para que no se mueva). Roce cinético = μ<sub>c</sub>·N, con μ<sub>c</sub> &lt; μ<sub>e</sub>.',
        ], ('La normal es la reacción del peso.', 'La reacción del peso es la fuerza con que el cuerpo atrae a la Tierra: actúa sobre la Tierra.'), prio='A'),
    ]),
    eje('Ondas', [
        fi('fis.ond.elementos', 'Elementos de una onda', [
            'v = λ·f = λ/T; f = 1/T. Una onda transporta energía, no materia.',
            'Al cambiar de medio cambian v y λ; la frecuencia NO cambia. Luz en el vacío: c = 3·10⁸ m/s.',
        ], ('Al pasar del aire al agua, la luz cambia su frecuencia.', 'Cambian v y λ; f la fija la fuente.'), esq('fisica.html', 'fis.ond.elementos', 1), 'A'),
        fi('fis.ond.reflexion-refraccion', 'Reflexión y refracción', [
            'Reflexión: ángulo de incidencia = ángulo de reflexión, medidos desde la normal.',
            'n = c/v. Al pasar a un medio más lento (n mayor), el rayo se acerca a la normal; si entra perpendicular, no se desvía.',
        ], ('Medir los ángulos desde la superficie.', 'Se miden desde la normal (la perpendicular a la superficie).'), prio='B'),
        fi('fis.ond.espejos-lentes', 'Espejos y lentes', [
            'Real = invertida = se proyecta en una pantalla. Virtual = derecha = no se proyecta.',
            tabla([['d &gt; 2f', 'real, invertida, menor'], ['d = 2f', 'real, invertida, igual'], ['f &lt; d &lt; 2f', 'real, invertida, mayor'], ['d = f', 'no se forma imagen (los rayos salen paralelos)'], ['d &lt; f', 'virtual, derecha, mayor (lupa)']], ['Lente convergente / espejo cóncavo', 'Imagen']),
            'En el espejo cóncavo, 2f es el centro de curvatura. Lente divergente y espejo convexo: virtual, derecha y menor.',
            'Espejo plano: virtual, derecha, igual y a la misma distancia detrás del espejo (izquierda y derecha se ven intercambiadas).',
        ], ('La imagen en un espejo plano es real.', 'Es virtual: no se puede proyectar en una pantalla.'), prio='A'),
        fi('fis.ond.espectro-color', 'Espectro electromagnético y color', [
            'De menor a mayor frecuencia: radio → microondas → infrarrojo → visible (rojo → violeta) → UV → rayos X → gamma.',
            'Todas van a c en el vacío. Más frecuencia = menos λ y más energía.',
            'Un objeto se ve del color que refleja. En el prisma, el violeta se desvía más.',
        ], ('Las ondas de radio viajan más rápido que la luz.', 'Todas las ondas EM van a c en el vacío.'), prio='B'),
        fi('fis.ond.doppler-interferencia', 'Doppler, interferencia y difracción', [
            'Si fuente y observador se acercan: f percibida mayor (λ menor). Si se alejan: f menor. Galaxias corridas al rojo: se alejan.',
            'Interferencia: cresta + cresta = constructiva; cresta + valle = destructiva.',
            'Difracción: se nota cuando la abertura u obstáculo tiene un tamaño parecido a λ.',
        ], ('Con Doppler cambia la rapidez de la onda.', 'Cambia la frecuencia que se percibe, no la rapidez.'), prio='B'),
        fi('fis.ond.dispositivos', 'Dispositivos', [
            'Radar: microondas que rebotan (distancia por el tiempo, velocidad por Doppler). Láser: luz de una sola frecuencia, en fase.',
            'Fibra óptica: la luz rebota por dentro (reflexión total interna). Telescopio refractor: lentes; reflector: espejo cóncavo; radiotelescopio: antena parabólica.',
        ], prio='C'),
    ]),
    eje('Electricidad', [
        fi('fis.ele.ohm', 'Ley de Ohm y circuitos', [
            'V = I·R. Corriente I = q/t (1 A = 1 C/s).',
            'Serie: misma corriente; R = R₁ + R₂. Paralelo: mismo voltaje; 1/R = 1/R₁ + 1/R₂ (dos iguales: R/2).',
            'En paralelo, la R total es menor que la menor. Mixto: reduce por partes, desde adentro hacia afuera: junta lo que está claramente en serie o en paralelo dentro de cada rama, y repite.',
        ], ('En paralelo se suman las resistencias.', 'En paralelo se suman las corrientes y la resistencia total baja.'), esq('fisica.html', 'fis.ele.ohm', 3), 'A'),
        fi('fis.ele.potencia', 'Potencia y energía eléctrica', [
            'P = V·I = I²·R = V²/R (W). E = P·t.',
            'Con P en kW y t en horas: E en kWh. Costo = kWh × precio del kWh. Ej.: 2000 W durante 30 min = 2 kW · 0,5 h = 1 kWh.',
            'Eficiencia = energía útil/energía consumida.',
        ], ('El kWh es una unidad de potencia.', 'El kWh es energía (potencia × tiempo).'), prio='A'),
        fi('fis.ele.domiciliaria', 'Instalación de la casa', [
            'Enchufes en paralelo, todos a 220 V. Interruptor en serie con su ampolleta.',
            'Disyuntor: corta por sobrecarga o cortocircuito (protege la instalación). Diferencial: corta si hay fuga de corriente (protege a las personas). Tierra: desvía la fuga de la carcasa.',
        ], ('El diferencial protege los cables de recalentarse.', 'Eso lo hace el disyuntor; el diferencial protege a las personas.'), prio='C'),
    ]),
    eje('Tierra y Universo', [
        fi('fis.tie.tectonica', 'Tectónica de placas y sismos', [
            'Wegener: deriva continental (encaje, fósiles y rocas iguales, huellas de glaciares; Pangea).',
            'Placas de litosfera sobre la astenosfera. Límites: convergente (subducción, como en Chile), divergente (dorsales), transformante.',
            'Hipocentro: donde se origina, en profundidad. Epicentro: el punto de la superficie justo encima.',
            'Modelo físico: litosfera, astenosfera, mesosfera, núcleo externo (líquido), núcleo interno (sólido). Químico: corteza, manto, núcleo.',
        ], ('El epicentro es el punto donde se origina el sismo.', 'Ese es el hipocentro; el epicentro está en la superficie, encima.'), prio='B'),
        fi('fis.mec.cosmos', 'Sistema solar y origen del universo', [
            'Geocéntrico: Aristóteles y Ptolomeo (epiciclos). Heliocéntrico: Copérnico.',
            'Galileo (telescopio): fases completas de Venus, lunas de Júpiter. Kepler: órbitas elípticas con el Sol en un foco; más rápido cerca del Sol; más lejos del Sol, más tarda en dar la vuelta (T² ∝ a³).',
            'Big Bang (hace ~13 800 millones de años). Evidencias: corrimiento al rojo de las galaxias, radiación de fondo de microondas, abundancia de H y He.',
            'Big Crunch: hipótesis de que la expansión se frenaría y el universo volvería a contraerse; hoy se ve poco probable porque la expansión se acelera.',
        ], ('Copérnico confirmó el heliocentrismo con el telescopio.', 'Las observaciones con telescopio fueron de Galileo.'), prio='C'),
    ]),
    eje('Biología y Química en 1 minuto (módulo común)', [
        fi(None, 'Biología', [
            'Mitocondria: respiración celular (ATP). Cloroplasto: fotosíntesis. Ribosomas → RER → Golgi: proteínas para exportar.',
            'Impulso nervioso: al despolarizarse entra Na⁺; luego sale K⁺. Sinapsis: neurotransmisores.',
            'Fecundación: en la trompa (tuba uterina). Pico de LH → ovulación.',
            'Mitosis: 2 células iguales a la madre. Meiosis: 4 células con la mitad de los cromosomas y distintas entre sí (variabilidad).',
            'Fotosíntesis: 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂ (el O₂ viene del agua). Selección natural: sobreviven y se reproducen más los mejor adaptados.',
        ]),
        fi(None, 'Química', [
            'Z = protones; A = protones + neutrones. Neutro: electrones = Z.',
            'Carbono: simple sp³, doble sp², triple sp.',
            'n = masa/M (mol). Molaridad = mol de soluto/L de solución. %m/m = masa de soluto/masa de solución × 100.',
            'Dilución: C₁·V₁ = C₂·V₂. Reactivo limitante: el que se acaba primero.',
        ]),
    ]),
])

# =====================================================================================
# M1 (desde las tarjetas de tools/m1.py)
# =====================================================================================
def m1_items(tab):
    out = []
    for tid, t, prio, titulo, idea, tarjetas in m1.TEMAS:
        if t != tab:
            continue
        rep = [f'<b>{tit}:</b> {html}' for tipo, tit, html in tarjetas if tipo == 'repaso']
        trs = [f'<b>{tit}:</b> {html}' for tipo, tit, html in tarjetas if tipo == 'trampa']
        out.append(f'<div class="fi" data-tema="{tid}"><h4>{titulo} <span class="chip {prio}">{prio}</span><span class="fi-dom"></span></h4>'
                   f'<ul>{"".join(f"<li>{x}</li>" for x in rep)}</ul>' + ''.join('<div class="fi-tr">' + x + '</div>' for x in trs) + '</div>')
    return out


M1 = ficha('M1', 'Ficha final · Matemática 1', 'Miércoles 2 de diciembre, 09:00 · 65 preguntas (60 cuentan) en 2 h 20 min · poco más de 2 min por pregunta', [
    'M1 ya lo dominas: aquí pierdes puntos por apuro, no por no saber. Lee el enunciado entero y lo que pregunta al final.',
    'Antes de marcar, revisa signos y unidades.',
    'No hay descuento por error: no dejes ninguna en blanco.',
], [eje(n, m1_items(t)) for t, n in (('num', 'Números'), ('alg', 'Álgebra y funciones'), ('geo', 'Geometría'), ('pro', 'Probabilidad y estadística'))])

# =====================================================================================
# Competencia Lectora
# =====================================================================================
LEN = ficha('LEN', 'Ficha final · Competencia Lectora', 'Martes 1 de diciembre, 09:00 · 7 textos y 65 preguntas (60 cuentan) en 2 h 30 min · unos 20 min por texto', [
    'Lee cada texto entero una vez y anota al margen, en 2 o 3 palabras, de qué trata cada párrafo.',
    'Vuelve siempre al texto: la respuesta correcta es la que el texto respalda, no la que suena mejor.',
    'Si una pregunta te traba, márcala y sigue (no más de unos 20 min por texto). Deja 10 minutos para revisar las marcadas.',
], [
    eje('Las 3 habilidades', [
        fi('len.localizar', 'Localizar', [
            'Pide un dato escrito: «Según el texto…», «De acuerdo con el párrafo…».',
            'Palabra clave específica (nombre, cifra, fecha) → rastrea → lee la oración completa.',
            'La correcta suele estar dicha con <b>otras palabras</b> (paráfrasis).',
        ], ('Elegir la alternativa que copia palabras del texto.', 'Puede ser otro dato del texto: comprueba que responda ESTA pregunta.'), prio='B'),
        fi('len.interpretar', 'Interpretar', [
            'Idea principal, causa, función de un párrafo, significado de una expresión, inferencia.',
            'Usa los conectores: causa (porque, se debe a), consecuencia (por eso), contraste (sin embargo, pero), ejemplo (por ejemplo).',
            'La idea principal cubre TODO el texto: ni un detalle, ni el tema en general.',
        ], ('Leer al pie de la letra una comparación o frase hecha.', 'Pregúntate qué idea ilustra.'), prio='A'),
        fi('len.evaluar', 'Evaluar', [
            'Propósito (informar, convencer, instruir), postura y tono, recursos (negritas, tablas, citas), suficiencia de la información, casos nuevos.',
            'Hecho = se puede comprobar. Opinión = valora: creo, debería, lamentablemente, sin duda, lo mejor.',
            'Tono con la intensidad justa: crítico ≠ indignado.',
            'Caso nuevo: aplica paso a paso el criterio del texto al caso. Suficiencia: si preguntan qué información falta, la correcta es lo que el texto de verdad no responde (no lo rellenes con lo que sabes).',
        ], ('Tomar una ironía como un elogio.', 'Si un elogio choca con un hecho negativo, es crítica.'), prio='A'),
    ]),
    eje('Las 9 trampas', [
        fi(None, 'Cómo descartar', [
            '<b>Otro dato del texto:</b> está en el texto, pero responde otra pregunta.',
            '<b>Fuera del texto:</b> suena razonable, pero el texto no lo dice ni lo permite deducir.',
            '<b>Al revés:</b> dice lo contrario o invierte causa y consecuencia.',
            '<b>Exagera:</b> siempre, nunca, todos, solo; tonos extremos.',
            '<b>Se queda corta:</b> un detalle como si fuera la idea principal.',
            '<b>Se pasa de amplia:</b> serviría para cualquier texto del tema.',
            '<b>Al pie de la letra:</b> lee literal una figura o una ironía.',
            '<b>Voz equivocada:</b> confunde quién dice, piensa o hace algo (el emisor, un personaje, una fuente, los que se oponen).',
            '<b>Opinión como hecho:</b> confunde una valoración con un dato comprobable.',
        ]),
        fi(None, 'Textos literarios (cuentos)', [
            'Narrador: ¿primera persona (yo) o tercera? ¿Cuenta desde el presente lo que pasó antes?',
            'Busca el conflicto, cómo cambia el personaje y qué representan los objetos que se repiten (símbolos).',
            'Saltos temporales: «Seis años después», «treinta años atrás», «Hoy…».',
        ]),
    ]),
])


def aplicar():
    selector = ('<div class="card fichas-top no-print"><h2>Fichas finales</h2>'
                '<p>Una página por prueba con fórmulas y trampas, para leer la mañana del examen. <b>Nada nuevo:</b> solo repasar lo que ya practicaste.</p>'
                '<div class="fila" id="fichas-sel">'
                '<button class="btn sec" data-ficha="M2">M2 · lun 30</button>'
                '<button class="btn sec" data-ficha="LEN">Lectora · mar 1, 09:00</button>'
                '<button class="btn sec" data-ficha="CIE">Física · mar 1, 15:00</button>'
                '<button class="btn sec" data-ficha="M1">M1 · mié 2</button>'
                '<button class="btn mini" type="button" id="ficha-imprimir">Imprimir esta ficha</button></div>'
                '<p class="small muted">Los temas con <span class="fi-ojo">repásalo</span> tienen tu dominio bajo 50 %: léelos primero. Al lado de cada tema ves tu dominio actual.</p></div>')
    html = '\n'.join([selector, M2, LEN, CIE, M1])
    p = RAIZ / 'index.html'
    s = p.read_text(encoding='utf-8')
    s, n = re.subn(r'(<!-- @@fichas@@ -->).*?(<!-- @@/fichas@@ -->)', lambda m: f'{m.group(1)}\n{html}\n{m.group(2)}', s, flags=re.S)
    assert n == 1, 'faltan los marcadores de fichas en index.html'
    p.write_text(s, encoding='utf-8')
    temas = re.findall(r'class="fi" data-tema="([^"]+)"', html)
    print(f'fichas: 4 pruebas, {len(temas)} temas con dominio, {html.count("<svg")} dibujos, {len(html) // 1024} KB')


if __name__ == '__main__':
    aplicar()
