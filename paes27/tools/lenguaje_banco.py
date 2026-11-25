#!/usr/bin/env python3
"""Banco de Competencia Lectora: 6 textos originales + sus preguntas -> tools/banco_len.json.

Con el texto del diagnóstico (banco_diag.json, LEN) suman 7 textos, como la prueba real.
Cada pregunta lleva además del contrato:
  texto      id del texto ('t1'…'t6'; las del diagnóstico usan el texto del diagnóstico)
  tarea      letra de la tarea lectora del temario DEMRE 2027 (a–n)
  evidencia  fragmentos EXACTOS del texto que se resaltan al responder
  opciones[].tipo  tipo de trampa de cada alternativa incorrecta (ver TIPOS)
Uso: python3 tools/lenguaje_banco.py   (escribe banco_len.json y completa los campos del diagnóstico)
"""
import json
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parent.parent
T = RAIZ / 'tools'

# Tipos de trampa (los mismos nombres usa lenguaje.html)
TIPOS = {
    'otro-dato': 'Otro dato del texto',
    'fuera': 'Fuera del texto',
    'contrario': 'Al revés',
    'exagera': 'Exagera',
    'parcial': 'Se queda corta',
    'amplia': 'Se pasa de amplia',
    'literal': 'Al pie de la letra',
    'voz': 'Voz equivocada',
    'opinion': 'Opinión como hecho',
}
# Tareas lectoras del temario (a–b localizar, c–h interpretar, i–n evaluar)
TAREAS = {
    'len.localizar': 'ab',
    'len.interpretar': 'cdefgh',
    'len.evaluar': 'ijklmn',
}


def pars(*ps):
    return ''.join(f'<p><b>{i}</b> {p}</p>' for i, p in enumerate(ps, 1))


TEXTOS = []
PREGUNTAS = []


def texto(id_, titulo, tipo, literario, html, nota='Texto original, escrito para esta app.'):
    TEXTOS.append({'id': id_, 'titulo': titulo, 'tipo': tipo, 'literario': literario, 'html': html, 'nota': nota})


def q(tid, n, tema, nivel, tarea, enunciado, ops, explicacion, evidencia):
    """ops: lista de (texto, tipo, trampa); la correcta lleva tipo None y trampa ''."""
    correcta = [i for i, o in enumerate(ops) if o[1] is None]
    assert len(correcta) == 1, (tid, n)
    PREGUNTAS.append({
        'id': f'len-{tid}-{n:02d}', 'prueba': 'LEN', 'eje': 'Habilidades', 'tema': 'len.' + tema, 'nivel': nivel,
        'texto': tid, 'tarea': tarea, 'enunciado': enunciado,
        'opciones': [({'texto': t, 'trampa': tr, 'tipo': ti} if ti else {'texto': t, 'trampa': ''}) for t, ti, tr in ops],
        'correcta': correcta[0], 'explicacion': explicacion, 'evidencia': evidencia,
    })


OK = (None, '')

# =====================================================================================
# T1 · Artículo de divulgación científica
# =====================================================================================
texto('t1', 'El mapa que se baila', 'Artículo de divulgación científica', False, pars(
    'Cuando una abeja obrera encuentra flores con buen néctar, no se guarda el secreto. Vuelve a la colmena y, sobre la superficie vertical del panal, en plena oscuridad, empieza a moverse de una forma muy particular. Sus compañeras la rodean, la tocan con las antenas y, al poco rato, varias de ellas salen volando directo hacia las mismas flores. Durante siglos, los apicultores observaron estos movimientos sin entender qué significaban.',
    'Quien descifró el misterio fue el zoólogo austríaco Karl von Frisch, a mediados del siglo XX. Después de años observando colmenas con paredes de vidrio, describió dos tipos de danza. Cuando el alimento está cerca de la colmena, la abeja traza pequeños círculos, primero hacia un lado y luego hacia el otro: es la «danza en redondo», que solo anuncia que hay comida en los alrededores. Cuando el alimento está lejos, la abeja recorre una línea recta mientras sacude el abdomen, vuelve en semicírculo al punto de partida y repite el recorrido: es la «danza del meneo».',
    'Lo asombroso es que la danza del meneo funciona como un mapa. El ángulo de la línea recta respecto de la vertical del panal indica el ángulo entre el sol y las flores: si la abeja avanza hacia arriba, las flores están en dirección al sol; si avanza hacia abajo, en dirección contraria. Y la duración del meneo informa la distancia: mientras más se prolonga, más lejos está el alimento. Así, un insecto con un cerebro más pequeño que una semilla de sésamo comunica dirección y distancia con un código que los seres humanos tardamos siglos en leer.',
    'No todos aceptaron la explicación. En la década de 1960, algunos investigadores sostuvieron que las abejas encontraban las flores guiándose por el olor que la bailarina traía en el cuerpo, y que la danza no transmitía información útil. La discusión se prolongó durante décadas, porque en una colmena real era muy difícil separar un factor del otro.',
    'Los experimentos posteriores inclinaron la balanza. En uno de ellos, un equipo construyó una pequeña abeja robot que imitaba la danza, y algunas abejas volaron en la dirección que el robot indicaba, aunque el robot nunca había visitado ninguna flor. Años después, otros científicos siguieron con radar el vuelo de abejas que acababan de observar una danza: volaron en la dirección indicada y recorrieron aproximadamente la distancia anunciada. Hoy se acepta que la danza transmite información, aunque el olor también ayuda a las abejas a reconocer el lugar exacto cuando ya están cerca.',
    'En 1973, von Frisch recibió el Premio Nobel de Fisiología o Medicina. Su trabajo demostró algo que en su época parecía increíble: que comunicar algo que no está presente, mediante un código de movimientos, no es exclusivo de los seres humanos.',
), nota='Texto original de divulgación, escrito para esta app a partir de hechos conocidos sobre la danza de las abejas.')

q('t1', 1, 'localizar', 'basico', 'a', 'Según el texto, ¿qué informa la duración del meneo?', [
    ('La distancia entre la colmena y el alimento.', *OK),
    ('La dirección de las flores respecto del sol.', 'otro-dato', 'Eso lo indica el ángulo de la línea recta, no la duración (párrafo 3).'),
    ('La cantidad de néctar que hay en las flores.', 'fuera', 'El texto nunca dice que la danza informe cuánto néctar hay.'),
    ('Que hay comida en los alrededores de la colmena.', 'otro-dato', 'Eso lo anuncia la danza en redondo (párrafo 2), no la duración del meneo.'),
], 'Párrafo 3: «la duración del meneo informa la distancia: mientras más se prolonga, más lejos está el alimento».',
  ['la duración del meneo informa la distancia: mientras más se prolonga, más lejos está el alimento'])

q('t1', 2, 'localizar', 'paes', 'b', 'De acuerdo con el párrafo 2, ¿en qué caso una abeja realiza la «danza en redondo»?', [
    ('Cuando quiere indicar la dirección exacta de las flores.', 'contrario', 'La danza en redondo «solo anuncia que hay comida en los alrededores»: no da la dirección.'),
    ('Cuando la comida se encuentra a poca distancia de la colmena.', *OK),
    ('Cuando vuelve en semicírculo al punto de partida.', 'otro-dato', 'Volver en semicírculo es parte de la danza del meneo, no de la danza en redondo.'),
    ('Cuando sus compañeras la tocan con las antenas.', 'otro-dato', 'Aparece en el párrafo 1 y no indica cuándo se hace la danza en redondo.'),
], '«A poca distancia» es una paráfrasis de «Cuando el alimento está cerca de la colmena».',
  ['Cuando el alimento está cerca de la colmena, la abeja traza pequeños círculos'])

q('t1', 3, 'interpretar', 'paes', 'c', '¿Qué relación hay entre el párrafo 4 y el párrafo 5?', [
    ('El 4 plantea una objeción y el 5 presenta las pruebas que la resolvieron.', *OK),
    ('El 4 explica el método de von Frisch y el 5, sus resultados.', 'voz', 'El párrafo 4 no habla del método de von Frisch: presenta lo que pensaban otros investigadores que dudaban de él.'),
    ('El 4 presenta una objeción y el 5 muestra que esa objeción era correcta.', 'contrario', 'Al revés: los experimentos del 5 mostraron que la danza SÍ transmite información.'),
    ('El 4 y el 5 explican por qué las abejas prefieren guiarse por el olor antes que por la danza.', 'fuera', 'El texto no dice que las abejas prefieran nada; solo que el olor ayuda al final, cuando ya están cerca.'),
], 'El 4 abre la duda (¿la danza o el olor?) y el 5 la resuelve con experimentos: es una relación problema/solución entre partes.',
  ['No todos aceptaron la explicación', 'Los experimentos posteriores inclinaron la balanza'])

q('t1', 4, 'interpretar', 'basico', 'h', 'En el párrafo 3, ¿para qué se menciona que el cerebro de la abeja es «más pequeño que una semilla de sésamo»?', [
    ('Para informar el tamaño exacto del cerebro de las abejas obreras.', 'literal', 'Es una comparación para impresionar, no una medida exacta.'),
    ('Para mostrar que las abejas tienen poca capacidad de aprender.', 'contrario', 'Al revés: el contraste resalta lo mucho que logra un cerebro tan pequeño.'),
    ('Para destacar cuánto logra comunicar un cerebro tan pequeño.', *OK),
    ('Para explicar por qué las abejas bailan en la oscuridad.', 'fuera', 'El texto no relaciona el tamaño del cerebro con la oscuridad.'),
], 'La frase completa contrasta el cerebro diminuto con «un código que los seres humanos tardamos siglos en leer»: busca asombro.',
  ['un insecto con un cerebro más pequeño que una semilla de sésamo comunica dirección y distancia con un código que los seres humanos tardamos siglos en leer'])

q('t1', 5, 'interpretar', 'dificil', 'd', 'A partir de los párrafos 4 y 5, ¿por qué fue importante que el robot «nunca había visitado ninguna flor»?', [
    ('Porque así el robot no podía contagiar enfermedades a la colmena.', 'fuera', 'El texto no habla de enfermedades.'),
    ('Porque permitía separar el efecto de la danza del efecto del olor de las flores.', *OK),
    ('Porque demostró que las abejas no usan el olor para nada.', 'exagera', 'El párrafo 5 dice que el olor también ayuda cuando ya están cerca.'),
    ('Porque así todas las abejas de la colmena volaron hacia donde indicaba el robot.', 'exagera', 'El texto dice «algunas abejas», no todas.'),
], 'El problema era que en una colmena real no se podía separar la danza del olor (párrafo 4). Un robot que no venía de ninguna flor sí lo separa: si las abejas igual van, es por la danza.',
  ['era muy difícil separar un factor del otro', 'aunque el robot nunca había visitado ninguna flor'])

q('t1', 6, 'evaluar', 'paes', 'k', '¿Cuál es el propósito principal del texto?', [
    ('Convencer al lector de que hay que proteger a las abejas y sus colmenas.', 'fuera', 'El texto no habla de protección ni busca convencer de eso.'),
    ('Narrar la vida y los descubrimientos del zoólogo Karl von Frisch.', 'parcial', 'Von Frisch aparece, pero el texto se centra en la danza, no en su biografía.'),
    ('Describir la danza en redondo de las abejas.', 'parcial', 'Es solo una parte del párrafo 2.'),
    ('Explicar cómo se comunican las abejas y cómo se comprobó.', *OK),
], 'Reúne todo el texto: qué hacen las abejas (1–3), la duda (4), las pruebas (5) y su importancia (6).',
  ['la danza del meneo funciona como un mapa', 'Hoy se acepta que la danza transmite información'])

q('t1', 7, 'evaluar', 'dificil', 'n', 'Un apicultor ve que una abeja, en el panal, recorre su línea recta hacia abajo y menea el abdomen durante mucho rato. Según el texto, ¿qué puede concluir?', [
    ('Que hay alimento cerca, en dirección al sol.', 'contrario', 'Invierte las dos cosas: hacia abajo es en dirección contraria al sol, y un meneo largo indica que está lejos.'),
    ('Que hay alimento lejos, en dirección al sol.', 'contrario', 'Hacia abajo indica la dirección contraria al sol (párrafo 3).'),
    ('Que hay alimento lejos, en dirección contraria al sol.', *OK),
    ('Que la abeja está avisando de un peligro.', 'fuera', 'El texto solo habla de danzas para comunicar alimento.'),
], 'Párrafo 3: hacia abajo = dirección contraria al sol; meneo más largo = más lejos.',
  ['si avanza hacia abajo, en dirección contraria', 'mientras más se prolonga, más lejos está el alimento'])

q('t1', 8, 'evaluar', 'paes', 'j', 'Si un lector quisiera calcular a cuántos metros están las flores a partir de una danza, ¿qué información le falta al texto?', [
    ('Hacia dónde apunta la línea recta de la danza.', 'otro-dato', 'Eso sirve para la dirección, no para la distancia, y el texto ya lo explica.'),
    ('A cuántos metros equivale cada segundo de meneo.', *OK),
    ('Si la danza transmite información o no.', 'contrario', 'El texto sí lo responde: el párrafo 5 dice que hoy se acepta que la transmite.'),
    ('Qué significa que la línea recta apunte hacia arriba.', 'otro-dato', 'El texto lo explica (en dirección al sol) y sirve para la dirección, no para la distancia.'),
], 'El texto dice que «más largo = más lejos», pero no da la equivalencia entre tiempo y metros: la información es insuficiente para calcular.',
  ['mientras más se prolonga, más lejos está el alimento'])

q('t1', 9, 'localizar', 'dificil', 'b', 'Según el párrafo 5, ¿qué hicieron las abejas que fueron seguidas con radar después de observar una danza?', [
    ('Siguieron el olor que la bailarina traía en el cuerpo.', 'voz', 'Eso es lo que sostenían quienes dudaban de von Frisch (párrafo 4), no lo que mostró el radar.'),
    ('Volaron en la dirección indicada, pero mucho menos lejos de lo anunciado.', 'contrario', 'El texto dice que recorrieron «aproximadamente la distancia anunciada».'),
    ('Se orientaron por la danza y llegaron más o menos a la distancia que esta señalaba.', *OK),
    ('Esperaron en la colmena hasta que la abeja robot les indicó el camino.', 'otro-dato', 'La abeja robot es otro experimento del mismo párrafo.'),
], 'Párrafo 5: «volaron en la dirección indicada y recorrieron aproximadamente la distancia anunciada». La correcta lo dice con otras palabras.',
  ['volaron en la dirección indicada y recorrieron aproximadamente la distancia anunciada'])

# =====================================================================================
# T2 · Columna de opinión
# =====================================================================================
texto('t2', 'El uniforme no nos iguala', 'Columna de opinión', False, pars(
    'Cada marzo se repite la misma escena: familias haciendo fila en las tiendas para comprar jumpers, pantalones grises y camisas blancas que, en pocos meses, quedarán cortos. Y cada marzo se repite también el mismo argumento a favor del uniforme escolar obligatorio: que iguala a los estudiantes, que evita que se note quién tiene más y quién tiene menos. Es un argumento noble. Pero, después de quince años haciendo clases, creo que es falso.',
    'Basta mirar un patio cualquiera. Con uniforme o sin él, los estudiantes saben perfectamente quién tiene zapatillas de marca, quién lleva el último modelo de celular y quién volvió de vacaciones bronceado por la playa. La desigualdad no está en la ropa: está en la casa, en el barrio, en las oportunidades. Pretender borrarla con una camisa blanca es como querer bajar la fiebre rompiendo el termómetro.',
    'Además, el uniforme cuesta. Una familia con tres hijos debe comprar al menos tres juegos completos cada año, además de la ropa que los niños usan los fines de semana. Para muchas familias, esa compra obligatoria pesa más que cualquier diferencia de marcas.',
    'Se dirá que el uniforme crea identidad y sentido de pertenencia. Es cierto que muchos exalumnos recuerdan con cariño su insignia. Pero la pertenencia no se cose en la ropa: nace de un proyecto compartido, de profesores que conocen a sus estudiantes por su nombre, de espacios donde todos tienen algo que aportar. Si un colegio necesita una corbata para que sus alumnos se sientan parte de él, el problema no es la ropa.',
    'Quienes defienden el uniforme, en el fondo, solo extrañan el colegio de su infancia. Yo propongo algo más modesto que una prohibición: que el uniforme sea voluntario y que cada familia pueda elegir. ¿Qué perdemos con probar? Si de verdad iguala, los estudiantes lo elegirán solos.',
), nota='Columna ficticia, escrita para esta app.')

q('t2', 1, 'localizar', 'basico', 'a', 'Según el emisor, ¿dónde está realmente la desigualdad entre los estudiantes?', [
    ('En la casa, el barrio y las oportunidades de cada uno.', *OK),
    ('En la ropa que usan los fines de semana.', 'otro-dato', 'Esa ropa aparece en el párrafo 3, como parte del costo para las familias.'),
    ('En las zapatillas de marca y los celulares de último modelo.', 'parcial', 'Son solo señales que los estudiantes notan; el emisor dice que la desigualdad de fondo está en la casa, el barrio y las oportunidades.'),
    ('En el costo de comprar uniformes cada año.', 'otro-dato', 'El costo es otro argumento (párrafo 3), no dónde está la desigualdad.'),
], 'Párrafo 2: «La desigualdad no está en la ropa: está en la casa, en el barrio, en las oportunidades».',
  ['La desigualdad no está en la ropa: está en la casa, en el barrio, en las oportunidades.'])

q('t2', 2, 'localizar', 'paes', 'b', '¿Qué propone el emisor en el último párrafo?', [
    ('Prohibir el uniforme en todos los colegios.', 'contrario', 'Dice explícitamente que propone «algo más modesto que una prohibición».'),
    ('Que los colegios regalen el uniforme a las familias con más hijos.', 'fuera', 'Nunca propone regalar uniformes.'),
    ('Que cada familia decida si su hijo usa o no el uniforme.', *OK),
    ('Mantener el uniforme solo en las ceremonias del colegio.', 'fuera', 'El texto no menciona ceremonias.'),
], 'Es una paráfrasis de «que el uniforme sea voluntario y que cada familia pueda elegir».',
  ['que el uniforme sea voluntario y que cada familia pueda elegir'])

q('t2', 3, 'interpretar', 'paes', 'e', 'En el párrafo 2, ¿qué quiere decir el emisor al comparar el uniforme con «bajar la fiebre rompiendo el termómetro»?', [
    ('Que el uniforme enferma a los estudiantes.', 'literal', 'Lee la comparación al pie de la letra: nadie habla de enfermedades reales.'),
    ('Que el uniforme oculta una señal del problema sin resolver su causa.', *OK),
    ('Que la desigualdad es un problema de salud pública.', 'literal', 'Toma la fiebre de forma literal. La comparación es sobre esconder la señal, no sobre salud.'),
    ('Que el uniforme empeora la desigualdad entre los estudiantes.', 'exagera', 'El emisor dice que el uniforme no la resuelve, no que la empeore.'),
], 'Romper el termómetro no baja la fiebre: solo impide verla. Igual, el uniforme tapa una señal de la desigualdad, pero la desigualdad sigue.',
  ['Pretender borrarla con una camisa blanca es como querer bajar la fiebre rompiendo el termómetro.'])

q('t2', 4, 'interpretar', 'paes', 'f', '¿Cuál es la tesis del emisor?', [
    ('El uniforme es demasiado caro para las familias que tienen varios hijos.', 'parcial', 'Es uno de sus argumentos (párrafo 3), no la tesis.'),
    ('Los colegios no pueden hacer nada contra la desigualdad del país, tengan o no uniforme obligatorio.', 'amplia', 'Va mucho más allá: el texto trata del uniforme, no de todo lo que pueden o no hacer los colegios.'),
    ('Muchos exalumnos recuerdan con cariño la insignia de su colegio.', 'parcial', 'Es una concesión que hace el emisor en el párrafo 4, no su tesis.'),
    ('El uniforme obligatorio no iguala a los estudiantes, por lo que debería ser voluntario.', *OK),
], 'La tesis aparece al final del párrafo 1 («creo que es falso» que iguale) y se completa con la propuesta del párrafo 5.',
  ['Es un argumento noble. Pero, después de quince años haciendo clases, creo que es falso.', 'que el uniforme sea voluntario y que cada familia pueda elegir'])

q('t2', 5, 'interpretar', 'dificil', 'h', '¿Qué función cumple el párrafo 4 en la argumentación?', [
    ('Agrega una razón propia del emisor para mantener el uniforme.', 'contrario', 'El emisor no defiende el uniforme: presenta esa razón de otros para rebatirla.'),
    ('Da un ejemplo del costo del uniforme para las familias.', 'otro-dato', 'El costo es el tema del párrafo 3.'),
    ('Reconoce un argumento contrario y luego lo rebate.', *OK),
    ('Demuestra con datos que el uniforme no crea identidad.', 'exagera', 'No entrega datos: da razones. «Demuestra con datos» exagera lo que hace el párrafo.'),
], '«Se dirá que…» introduce la objeción; «Es cierto que…» la concede; «Pero…» la refuta. Es un contraargumento con su refutación.',
  ['Se dirá que el uniforme crea identidad y sentido de pertenencia', 'Pero la pertenencia no se cose en la ropa'])

q('t2', 6, 'evaluar', 'paes', 'l', '¿Qué actitud muestra el emisor frente al argumento de que el uniforme iguala a los estudiantes?', [
    ('Lo desprecia por considerarlo malintencionado.', 'exagera', 'Al contrario de despreciarlo, lo llama «noble». El tono es de desacuerdo, no de desprecio.'),
    ('Lo considera bien intencionado, pero equivocado.', *OK),
    ('Lo acepta, aunque con algunas dudas.', 'contrario', 'No lo acepta: dice que «es falso».'),
    ('Se mantiene neutral, sin tomar posición.', 'contrario', 'Toma posición clara: «creo que es falso».'),
], '«Es un argumento noble» (bien intencionado) + «creo que es falso» (equivocado).',
  ['Es un argumento noble. Pero, después de quince años haciendo clases, creo que es falso.'])

q('t2', 7, 'evaluar', 'dificil', 'j', '¿Qué debilidad tiene la afirmación «Quienes defienden el uniforme, en el fondo, solo extrañan el colegio de su infancia»?', [
    ('Contradice la propuesta del mismo emisor de hacer voluntario el uniforme.', 'fuera', 'No hay contradicción entre las dos ideas: el problema es otro.'),
    ('Usa datos falsos sobre los exalumnos.', 'fuera', 'No usa ningún dato: es una afirmación sin pruebas.'),
    ('Es una pregunta retórica que no espera respuesta.', 'otro-dato', 'La pregunta retórica del texto es otra: «¿Qué perdemos con probar?».'),
    ('Generaliza y atribuye a todos sus opositores un motivo que no demuestra.', *OK),
], 'Es una falla argumentativa: una generalización («quienes defienden», «solo») que descalifica el motivo del otro en vez de responder sus razones.',
  ['Quienes defienden el uniforme, en el fondo, solo extrañan el colegio de su infancia.'])

q('t2', 8, 'evaluar', 'basico', 'k', '¿Para qué incluye el emisor la frase «después de quince años haciendo clases»?', [
    ('Para dar respaldo a su opinión con su experiencia.', *OK),
    ('Para informar su edad a los lectores.', 'fuera', 'No habla de su edad, sino de su experiencia como profesor.'),
    ('Para mostrar que está cansado de hacer clases.', 'fuera', 'Nada en el texto sugiere cansancio.'),
    ('Para probar con estadísticas que el uniforme no iguala.', 'exagera', 'La experiencia personal no es una estadística.'),
], 'Es un recurso de autoridad: la opinión pesa más si viene de alguien que ha visto muchos patios de colegio.',
  ['después de quince años haciendo clases'])

# =====================================================================================
# T3 · Cuento
# =====================================================================================
texto('t3', 'La balanza', 'Cuento', True, pars(
    'Mi papá pesaba las paltas como quien pesa una promesa. Las dejaba en un platillo de la balanza de hierro, ponía las pesas en el otro, esperaba que la aguja dejara de temblar y recién entonces decía el precio, mirando al cliente a los ojos. «Un kilo es un kilo», repetía. Yo tenía doce años y lo ayudaba los sábados en la feria; mi trabajo era dar el vuelto y sonreír.',
    'En el puesto de al lado, don Ramiro tenía una balanza digital, roja y brillante, que mostraba los números con luces. Las señoras se detenían frente a ella como frente a una vitrina. Una mañana le pregunté a mi papá por qué no compraba una igual. Se quedó callado mientras amarraba una bolsa y después dijo: «Esa balanza la arregla un técnico. Esta la arreglo yo».',
    'Seis años después, la balanza de hierro seguía en el mismo lugar y yo ya no daba vueltos: llevaba las cuentas del puesto en un cuaderno. Ese invierno llegó la carta de la universidad. Me habían aceptado en Santiago, lejos del puesto, de las paltas y de los sábados. La leí tres veces encerrada en el baño y la guardé debajo del colchón. No sabía cómo decírselo: en mi casa, irse era casi lo mismo que abandonar.',
    'Pasé semanas sin tocar el tema. Mi papá, en cambio, empezó a hacer cosas raras: me pedía que yo pesara la mercadería, que yo atendiera a los clientes difíciles, que yo negociara con los camioneros de la madrugada. Una vez lo sorprendí mirándome desde el fondo del puesto, con los brazos cruzados, como quien revisa que una máquina funcione bien.',
    'El último sábado de febrero, antes de abrir, me pasó un paquete envuelto en papel de diario. Adentro estaba la pesa más chica de la balanza, la de cien gramos, gastada en los bordes por los años. «Para que no se te olvide», me dijo. «Un kilo es un kilo, allá también». Entonces entendí que la carta nunca había estado tan escondida como yo creía.',
    'Hoy trabajo en un laboratorio donde las balanzas miden millonésimas de gramo y no tienen aguja. Pero la pesa de cien gramos está sobre mi escritorio, y cada vez que alguien me pide redondear un resultado para que se vea mejor, la miro y digo que no.',
), nota='Cuento original, escrito para esta app.')

q('t3', 1, 'localizar', 'basico', 'a', '¿Qué le regaló el padre a la narradora el último sábado de febrero?', [
    ('La balanza de hierro completa.', 'exagera', 'Le regaló solo una pesa, no la balanza entera.'),
    ('Una balanza digital como la de don Ramiro.', 'otro-dato', 'La balanza digital es la del puesto vecino (párrafo 2).'),
    ('La pesa más chica de la balanza, la de cien gramos.', *OK),
    ('La carta de la universidad envuelta en papel de diario.', 'otro-dato', 'Mezcla dos elementos: la carta la guardó ella; el papel de diario envolvía la pesa.'),
], 'Párrafo 5: «Adentro estaba la pesa más chica de la balanza, la de cien gramos».',
  ['Adentro estaba la pesa más chica de la balanza, la de cien gramos'])

q('t3', 2, 'localizar', 'paes', 'b', 'Según el párrafo 4, ¿qué cambió en la conducta del padre después de que llegó la carta?', [
    ('Dejó de hablar con su hija durante semanas.', 'voz', 'Es la narradora la que «pasó semanas sin tocar el tema», no el padre.'),
    ('Empezó a encargarle a su hija tareas importantes del puesto.', *OK),
    ('Decidió comprar una balanza digital para el puesto.', 'fuera', 'El texto nunca dice que la comprara.'),
    ('Le prohibió irse a estudiar a Santiago.', 'contrario', 'Hace lo contrario: la prepara para irse.'),
], 'Es una paráfrasis de «me pedía que yo pesara la mercadería, que yo atendiera a los clientes difíciles, que yo negociara con los camioneros».',
  ['me pedía que yo pesara la mercadería, que yo atendiera a los clientes difíciles, que yo negociara con los camioneros de la madrugada'])

q('t3', 3, 'interpretar', 'paes', 'd', '¿Qué se puede inferir de la frase «la carta nunca había estado tan escondida como yo creía»?', [
    ('Que el padre ya sabía que la hija se iría y la había estado preparando.', *OK),
    ('Que el padre encontró la carta debajo del colchón y la leyó a escondidas.', 'fuera', 'Sabemos que el padre lo sabía, pero el texto no dice cómo se enteró.'),
    ('Que la narradora perdió la carta debajo del colchón.', 'literal', 'Lee «escondida» como un objeto perdido; la frase habla de un secreto que no era tal.'),
    ('Que el padre quería que su hija se quedara en la feria.', 'contrario', 'La pesa y el «allá también» muestran que acepta que se vaya.'),
], 'Las «cosas raras» del párrafo 4 cobran sentido: el padre sabía y la estaba preparando para irse.',
  ['Entonces entendí que la carta nunca había estado tan escondida como yo creía.', 'Mi papá, en cambio, empezó a hacer cosas raras'])

q('t3', 4, 'interpretar', 'paes', 'e', '¿Qué representa la pesa de cien gramos en el último párrafo?', [
    ('El fracaso del negocio familiar.', 'fuera', 'Nada indica que el negocio fracasara.'),
    ('La honestidad que la narradora aprendió de su padre.', *OK),
    ('La nostalgia por la balanza digital de don Ramiro.', 'otro-dato', 'La pesa es de la balanza de hierro del padre, no de la digital.'),
    ('La precisión de los instrumentos del laboratorio.', 'literal', 'Las balanzas del laboratorio son mucho más precisas: la pesa no vale por su precisión, sino por lo que significa.'),
], 'La pesa es un símbolo: cuando le piden «redondear un resultado para que se vea mejor», la mira y se niega. Es el «un kilo es un kilo» del padre.',
  ['cada vez que alguien me pide redondear un resultado para que se vea mejor, la miro y digo que no'])

q('t3', 5, 'interpretar', 'dificil', 'h', '¿Qué función cumple en el relato la respuesta del padre: «Esa balanza la arregla un técnico. Esta la arreglo yo»?', [
    ('Mostrar que el padre no tiene dinero suficiente para comprar una balanza nueva.', 'fuera', 'El texto no habla de su situación económica.'),
    ('Explicar por qué las señoras preferían el puesto de don Ramiro.', 'otro-dato', 'La respuesta es sobre el padre y su balanza, no sobre las clientas.'),
    ('Mostrar que el padre confía en lo que conoce y puede cuidar él mismo.', *OK),
    ('Anticipar que la balanza de hierro se va a romper.', 'fuera', 'La balanza no se rompe: seis años después «seguía en el mismo lugar».'),
], 'La frase caracteriza al padre: confía en lo que entiende y puede cuidar él mismo, como confía en su «un kilo es un kilo», que es lo que después le hereda a su hija.',
  ['Esa balanza la arregla un técnico. Esta la arreglo yo'])

q('t3', 6, 'evaluar', 'paes', 'k', '¿Desde qué perspectiva se cuenta la historia?', [
    ('Una niña de doce años que cuenta lo que le pasa mientras ocurre.', 'parcial', 'Tenía doce al comienzo, pero el último párrafo («Hoy trabajo en un laboratorio») muestra que narra desde la adultez.'),
    ('Un narrador que observa desde afuera y sabe lo que piensan todos.', 'contrario', 'Narra en primera persona («Mi papá», «Yo tenía») y no sabe lo que piensa el padre: lo descubre.'),
    ('El padre, que recuerda cómo se fue su hija.', 'voz', 'Quien narra es la hija («Mi papá pesaba…»).'),
    ('Una narradora adulta que recuerda su adolescencia en primera persona.', *OK),
], 'Primera persona y mirada retrospectiva: «Yo tenía doce años…», «Seis años después…», «Hoy trabajo…».',
  ['Yo tenía doce años', 'Hoy trabajo en un laboratorio'])

q('t3', 7, 'interpretar', 'dificil', 'f', '¿Cuál de las siguientes afirmaciones expresa mejor el tema del relato?', [
    ('Lo que se aprende en casa acompaña a una persona aunque se vaya lejos.', *OK),
    ('La tecnología moderna está acabando con los oficios tradicionales.', 'fuera', 'La balanza digital aparece, pero el relato no trata de la desaparición de los oficios.'),
    ('Los hijos deben quedarse a ayudar en el negocio familiar.', 'contrario', 'El padre acepta que la hija se vaya y le regala la pesa para el camino.'),
    ('El trabajo en la feria es muy duro.', 'parcial', 'Es parte del ambiente del relato, no su tema.'),
], 'La hija se va, pero se lleva el «un kilo es un kilo»: la honestidad aprendida en el puesto sigue guiándola en el laboratorio.',
  ['«Un kilo es un kilo, allá también»', 'la miro y digo que no'])

q('t3', 8, 'interpretar', 'basico', 'c', '¿Por qué la narradora esconde la carta de la universidad debajo del colchón?', [
    ('Porque la carta traía malas noticias.', 'contrario', 'Al revés: la habían aceptado en la universidad.'),
    ('Porque su padre le había prohibido postular a la universidad en Santiago.', 'fuera', 'El texto nunca dice que el padre se lo prohibiera.'),
    ('Porque temía que su familia viera su partida como un abandono.', *OK),
    ('Porque no quería estudiar en Santiago.', 'fuera', 'Nada indica que no quisiera ir: el problema era cómo decirlo.'),
], 'La causa está en la oración siguiente: «No sabía cómo decírselo: en mi casa, irse era casi lo mismo que abandonar».',
  ['No sabía cómo decírselo: en mi casa, irse era casi lo mismo que abandonar.'])

# =====================================================================================
# T4 · Instructivo (texto discontinuo, documento público ficticio)
# =====================================================================================
T4_HTML = (
    '<p class="doc-entidad">Municipalidad de Puerto Alto · Oficina de Educación</p>'
    '<p>La Municipalidad de Puerto Alto entrega un aporte mensual para el transporte de estudiantes de enseñanza media que viven lejos de su liceo. Lee este instructivo completo antes de postular.</p>'
    '<h4>¿En qué consiste?</h4>'
    '<p>Un abono de <b>$15.000 mensuales</b> en la tarjeta de transporte del estudiante, de abril a diciembre (ambos meses incluidos).</p>'
    '<h4>Requisitos (debes cumplirlos todos)</h4>'
    '<table class="doc-tabla"><tr><th>Requisito</th><th>Cómo se acredita</th></tr>'
    '<tr><td>Ser estudiante regular de enseñanza media en un liceo de Puerto Alto</td><td>Certificado de alumno regular 2027</td></tr>'
    '<tr><td>Vivir a más de 2 km del liceo</td><td>Boleta de luz, agua o gas de los últimos tres meses, con la dirección del hogar</td></tr>'
    '<tr><td>Pertenecer al 40 % de hogares más vulnerables según el Registro Social de Hogares</td><td>No necesitas presentar nada: la Municipalidad lo revisa</td></tr>'
    '<tr><td>Haber tenido al menos 85 % de asistencia el año anterior</td><td>Informe de notas y asistencia del año anterior</td></tr></table>'
    '<p class="doc-nota">Si tienes una discapacidad acreditada, no necesitas cumplir el requisito de distancia. Si estás en 1.º medio, se considera tu asistencia de 8.º básico.</p>'
    '<h4>Fechas</h4>'
    '<table class="doc-tabla"><tr><th>Etapa</th><th>Fecha</th></tr>'
    '<tr><td>Postulación</td><td>Del 2 al 20 de marzo</td></tr>'
    '<tr><td>Publicación de resultados</td><td>31 de marzo</td></tr>'
    '<tr><td>Primer abono</td><td>10 de abril</td></tr>'
    '<tr><td>Último abono</td><td>10 de diciembre</td></tr></table>'
    '<h4>¿Cómo postulo?</h4>'
    '<ol><li>Reúne los documentos de la tabla de requisitos.</li><li>Llena el formulario en la Oficina de Educación (lunes a viernes, de 9:00 a 14:00) o en el sitio web de la Municipalidad.</li><li>Guarda el comprobante con tu número de folio: lo necesitarás para consultar el resultado.</li></ol>'
    '<p class="doc-aviso"><b>Las postulaciones incompletas no serán evaluadas.</b></p>'
)
texto('t4', 'Subsidio de Transporte Escolar 2027: cómo postular', 'Instructivo (texto discontinuo)', False, T4_HTML,
      nota='Documento ficticio: Puerto Alto y este subsidio no existen. Escrito para esta app.')

q('t4', 1, 'localizar', 'basico', 'a', '¿Hasta qué fecha se puede postular al subsidio?', [
    ('Hasta el 2 de marzo.', 'otro-dato', 'El 2 de marzo es el primer día de postulación, no el último.'),
    ('Hasta el 20 de marzo.', *OK),
    ('Hasta el 31 de marzo.', 'otro-dato', 'Esa es la fecha de publicación de resultados.'),
    ('Hasta el 10 de abril.', 'otro-dato', 'Esa es la fecha del primer abono.'),
], 'Tabla de fechas: «Postulación · Del 2 al 20 de marzo».', ['Del 2 al 20 de marzo'])

q('t4', 2, 'localizar', 'paes', 'b', 'Según el instructivo, ¿qué documento sirve para acreditar dónde vive el estudiante?', [
    ('El certificado de alumno regular.', 'otro-dato', 'Ese acredita que es estudiante regular, no su domicilio.'),
    ('La cartola del Registro Social de Hogares.', 'otro-dato', 'El Registro Social de Hogares es de otro requisito, y para ese no hay que presentar nada.'),
    ('Una boleta reciente de un servicio básico con la dirección del hogar.', *OK),
    ('Una declaración firmada por el director del liceo con la dirección del estudiante.', 'fuera', 'El instructivo no pide ninguna declaración del director.'),
], 'La fila «Vivir a más de 2 km» pide una boleta de luz, agua o gas con la dirección: «servicio básico» es una paráfrasis.',
  ['Boleta de luz, agua o gas de los últimos tres meses, con la dirección del hogar'])

q('t4', 3, 'interpretar', 'paes', 'c', 'Si un estudiante obtiene el subsidio, ¿cuánto dinero recibirá en total durante el año?', [
    ('$15.000', 'parcial', 'Ese es el abono de un solo mes.'),
    ('$135.000', *OK),
    ('$150.000', 'otro-dato', 'Contaste desde marzo, pero marzo es el mes de postulación: el primer abono es en abril (9 meses).'),
    ('$180.000', 'fuera', 'Contaste los 12 meses del año; el abono es solo de abril a diciembre.'),
], 'De abril a diciembre, ambos incluidos, son 9 abonos: 9 · $15.000 = $135.000. Hay que cruzar el párrafo «¿En qué consiste?» con la tabla de fechas.',
  ['de abril a diciembre (ambos meses incluidos)', '$15.000 mensuales'])

q('t4', 4, 'localizar', 'paes', 'a', 'Si un estudiante está en 1.º medio, ¿qué asistencia se considera?', [
    ('La del primer semestre de 1.º medio.', 'fuera', 'El instructivo no menciona el semestre en curso.'),
    ('La de 8.º básico.', *OK),
    ('No se considera la asistencia.', 'contrario', 'Sí se considera: la de 8.º básico.'),
    ('La de 7.º y 8.º básico.', 'exagera', 'Solo se considera 8.º básico.'),
], 'Nota bajo la tabla de requisitos: «Si estás en 1.º medio, se considera tu asistencia de 8.º básico».',
  ['Si estás en 1.º medio, se considera tu asistencia de 8.º básico.'])

q('t4', 5, 'evaluar', 'paes', 'n', 'Tomás está en 3.º medio en un liceo de Puerto Alto, vive a 3 km del liceo, su hogar está en el 40 % más vulnerable y el año pasado tuvo 80 % de asistencia. ¿Puede obtener el subsidio?', [
    ('Sí, porque cumple la distancia y el tramo del Registro Social de Hogares.', 'parcial', 'Cumple varios requisitos, pero el instructivo dice que hay que cumplirlos TODOS.'),
    ('No, porque vive demasiado lejos del liceo.', 'contrario', 'Vivir lejos (más de 2 km) es justamente un requisito.'),
    ('No, porque no cumple la asistencia mínima.', *OK),
    ('Sí, si presenta un certificado de discapacidad.', 'otro-dato', 'La excepción por discapacidad es solo para el requisito de distancia, no para la asistencia.'),
], 'Se pide al menos 85 % de asistencia y Tomás tuvo 80 %. Como los requisitos se deben cumplir todos, no puede.',
  ['Requisitos (debes cumplirlos todos)', 'Haber tenido al menos 85 % de asistencia el año anterior'])

q('t4', 6, 'evaluar', 'basico', 'm', '¿Para qué se destaca en negrita «Las postulaciones incompletas no serán evaluadas»?', [
    ('Para indicar que es el título de una sección.', 'fuera', 'Los títulos son otros («Fechas», «¿Cómo postulo?»); esta frase es una advertencia.'),
    ('Para advertir sobre un error que deja fuera al postulante.', *OK),
    ('Para resumir de qué trata el subsidio.', 'parcial', 'No resume el subsidio: advierte sobre un error que deja fuera.'),
    ('Para señalar que es la información menos importante del instructivo.', 'contrario', 'La negrita hace lo contrario: llama la atención sobre algo importante.'),
], 'Es un recurso tipográfico: la negrita destaca una advertencia con consecuencias.',
  ['Las postulaciones incompletas no serán evaluadas.'])

q('t4', 7, 'evaluar', 'paes', 'i', '¿A quién se dirige principalmente el instructivo y con qué intención?', [
    ('A estudiantes y sus familias, para que sepan si pueden postular y cómo hacerlo.', *OK),
    ('A los directores de liceos, para que controlen la asistencia.', 'fuera', 'El texto habla directamente al estudiante («Si estás en 1.º medio…»), no a los directores.'),
    ('A todos los habitantes de la comuna, para informar todos los beneficios municipales.', 'amplia', 'Solo informa un subsidio y para un grupo específico.'),
    ('A los conductores del transporte público, para informar una nueva tarifa.', 'fuera', 'No habla de tarifas ni a conductores.'),
], 'Usa la segunda persona («Lee», «debes cumplirlos», «Si estás en…») y explica requisitos y pasos: busca que el estudiante postule bien.',
  ['Lee este instructivo completo antes de postular.'])

q('t4', 8, 'evaluar', 'dificil', 'j', 'Una apoderada lee el instructivo y no sabe qué pasa si su hija obtiene el subsidio y se cambia de liceo a mitad de año. ¿Qué se puede afirmar?', [
    ('Debe volver a postular en marzo del año siguiente.', 'fuera', 'El instructivo no dice nada sobre cambios de liceo.'),
    ('Pierde el subsidio, porque las postulaciones incompletas no se evalúan.', 'otro-dato', 'Esa regla es sobre postulaciones incompletas, no sobre cambios de liceo.'),
    ('Mantiene el subsidio, porque la excepción por discapacidad la protege.', 'otro-dato', 'Esa excepción es solo para el requisito de distancia.'),
    ('El instructivo no entrega información sobre esa situación.', *OK),
], 'Evaluar la suficiencia de un texto incluye reconocer cuándo NO responde algo. Las otras alternativas aplican reglas del texto a una situación que el texto no trata.',
  ['Requisitos (debes cumplirlos todos)'])

q('t4', 9, 'localizar', 'dificil', 'a', 'Según el instructivo, ¿para cuál de estos requisitos NO hay que presentar ningún documento?', [
    ('Vivir a más de 2 km del liceo.', 'otro-dato', 'Para ese se pide una boleta de luz, agua o gas con la dirección.'),
    ('Haber tenido al menos 85 % de asistencia el año anterior.', 'otro-dato', 'Para ese se pide el informe de notas y asistencia.'),
    ('Pertenecer al 40 % de hogares más vulnerables.', *OK),
    ('Ser estudiante regular de enseñanza media en Puerto Alto.', 'otro-dato', 'Para ese se pide el certificado de alumno regular.'),
], 'Tabla de requisitos, fila del Registro Social de Hogares: «No necesitas presentar nada: la Municipalidad lo revisa». Ojo con el NO de la pregunta.',
  ['No necesitas presentar nada: la Municipalidad lo revisa'])

# =====================================================================================
# T5 · Reseña cinematográfica
# =====================================================================================
texto('t5', 'Marea baja: lo que el mar no explica', 'Reseña de cine', False, pars(
    '«Marea baja», el primer largometraje de su directora, se estrenó el jueves en salas de todo el país. Dura 104 minutos y está filmada casi entera en una caleta del norte, con actores profesionales y pescadores de la zona. Cuenta la historia de Elías, un buzo mariscador que, tras la muerte de su hermano, debe decidir si vende su bote a una empresa que quiere instalarse en la caleta.',
    'Lo mejor de la película está en sus primeros cuarenta minutos. La cámara se queda quieta y deja que las cosas pasen: el agua golpeando el muelle, unas manos que reparan una red, un almuerzo en silencio. No hay música que nos diga qué sentir. En esos momentos, «Marea baja» confía en el espectador, y el espectador se lo agradece.',
    'Ayuda mucho la actuación del protagonista. Con muy pocas palabras, logra que entendamos el peso de una decisión que no es solo económica: vender el bote es también vender la memoria de su hermano. Los pescadores que actúan junto a él, que nunca antes habían estado frente a una cámara, aportan una naturalidad imposible de ensayar.',
    'El problema llega en la última media hora. Como si la directora hubiera desconfiado de todo lo construido, la película se llena de discursos. Los personajes explican lo que sienten, la música sube en cada escena importante y el conflicto se resuelve en una asamblea donde todos dicen exactamente lo que el guion necesita. Lo que antes se mostraba, ahora se subraya con plumón.',
    'Aun así, «Marea baja» merece verse. Sus defectos son los de una directora que todavía no se atreve a confiar del todo en sus imágenes; sus virtudes, las de alguien que sabe mirar. Quien vaya al cine buscando una historia contada sin apuro no saldrá decepcionado, siempre que esté dispuesto a perdonarle el final.',
), nota='Película y reseña ficticias, escritas para esta app.')

q('t5', 1, 'localizar', 'basico', 'a', '¿Qué decisión debe tomar Elías?', [
    ('Si vende su bote a una empresa.', *OK),
    ('Si se va a trabajar como buzo a otra caleta.', 'fuera', 'El texto no menciona otra caleta.'),
    ('Si convoca a una asamblea de pescadores.', 'otro-dato', 'La asamblea aparece en el párrafo 4 como la forma en que se resuelve el conflicto, no como la decisión de Elías.'),
    ('Si actúa en la película junto a los pescadores.', 'voz', 'Confunde al personaje (Elías) con el actor que lo interpreta.'),
], 'Párrafo 1: «debe decidir si vende su bote a una empresa que quiere instalarse en la caleta».',
  ['debe decidir si vende su bote a una empresa que quiere instalarse en la caleta'])

q('t5', 2, 'localizar', 'dificil', 'b', 'Según la reseña, ¿qué aportan a la película los pescadores que actúan en ella?', [
    ('Conocimientos técnicos sobre el buceo.', 'fuera', 'Suena lógico, pero el texto no lo dice.'),
    ('Una espontaneidad que no se consigue con ensayos.', *OK),
    ('Discursos que explican lo que sienten los personajes.', 'otro-dato', 'Los discursos son el defecto de la última media hora (párrafo 4), no lo que aportan los pescadores.'),
    ('Una actuación que transmite el peso de la decisión con pocas palabras.', 'voz', 'Eso lo dice del protagonista, no de los pescadores.'),
], '«Espontaneidad que no se consigue con ensayos» parafrasea «una naturalidad imposible de ensayar».',
  ['aportan una naturalidad imposible de ensayar'])

q('t5', 3, 'interpretar', 'paes', 'e', 'En el párrafo 4, ¿qué significa que lo que antes se mostraba, «ahora se subraya con plumón»?', [
    ('Que la película pone textos escritos en pantalla.', 'literal', 'Lee la expresión al pie de la letra: no hay textos en pantalla.'),
    ('Que la película explica en exceso lo que antes dejaba ver con sutileza.', *OK),
    ('Que la última media hora es la parte más importante de la película.', 'literal', 'Aquí «subrayar» no es destacar lo importante: es remarcar lo obvio, y el emisor lo critica.'),
    ('Que la directora corrigió el guion durante el rodaje.', 'fuera', 'El texto no habla del rodaje.'),
], 'La frase resume el defecto: discursos, música que sube y personajes que explican lo que sienten. Todo se remarca, como con un plumón grueso.',
  ['Lo que antes se mostraba, ahora se subraya con plumón.', 'Los personajes explican lo que sienten'])

q('t5', 4, 'evaluar', 'paes', 'k', '¿Cómo se organiza la reseña?', [
    ('Presenta la película, destaca virtudes, señala un defecto y recomienda.', *OK),
    ('Resume la historia completa, incluido el final, y luego da su opinión sobre ella.', 'fuera', 'No cuenta el final: nunca dice qué decide Elías.'),
    ('Compara la película con otras del mismo género.', 'fuera', 'No menciona ninguna otra película.'),
    ('Critica la película y termina recomendando no verla.', 'contrario', 'Termina diciendo que «merece verse».'),
], 'Párrafo 1: presentación. 2 y 3: virtudes. 4: defecto. 5: balance y recomendación.',
  ['Lo mejor de la película', 'El problema llega en la última media hora', 'Aun así, «Marea baja» merece verse.'])

q('t5', 5, 'interpretar', 'dificil', 'd', '¿Qué se puede inferir sobre lo que el emisor valora en una película?', [
    ('Que prefiere a los actores profesionales por sobre los pescadores que actúan por primera vez.', 'contrario', 'Elogia justamente a los pescadores que nunca habían actuado.'),
    ('Que la música es siempre un defecto en el cine.', 'exagera', 'Critica que la música suba en cada escena importante, pero «siempre» va más allá de lo que dice.'),
    ('Que prefiere que una película muestre en vez de explicarlo todo.', *OK),
    ('Que las películas deberían durar menos de una hora.', 'fuera', 'Nunca critica la duración.'),
], 'Elogia que la película «confía en el espectador» y critica cuando «se llena de discursos»: valora mostrar sin explicar.',
  ['«Marea baja» confía en el espectador', 'la película se llena de discursos'])

q('t5', 6, 'evaluar', 'basico', 'l', '¿Cuál es la postura del emisor frente a «Marea baja»?', [
    ('La rechaza por completo por su final.', 'contrario', 'Critica el final, pero dice que la película «merece verse».'),
    ('La considera una obra perfecta.', 'exagera', 'Le señala un defecto claro: la última media hora.'),
    ('La recomienda, aunque considera que su final es débil.', *OK),
    ('No toma postura y solo describe la película.', 'contrario', 'Valora todo el tiempo: «lo mejor», «el problema», «merece verse».'),
], 'Párrafo 5: «merece verse… siempre que esté dispuesto a perdonarle el final».',
  ['Aun así, «Marea baja» merece verse.', 'siempre que esté dispuesto a perdonarle el final'])

q('t5', 7, 'evaluar', 'dificil', 'j', '¿Cuál de los siguientes enunciados de la reseña es un HECHO y no una opinión?', [
    ('«Lo mejor de la película está en sus primeros cuarenta minutos».', 'opinion', '«Lo mejor» es una valoración del emisor: otro espectador podría pensar distinto.'),
    ('«Dura 104 minutos y está filmada casi entera en una caleta del norte».', *OK),
    ('«“Marea baja” merece verse».', 'opinion', 'Es una recomendación: una opinión, no un dato que se pueda comprobar.'),
    ('«El espectador se lo agradece».', 'opinion', 'Atribuye a todos los espectadores un sentimiento: es una apreciación del emisor.'),
], 'Un hecho se puede comprobar (la duración, el lugar de filmación). Una opinión es una valoración.',
  ['Dura 104 minutos y está filmada casi entera en una caleta del norte'])

# =====================================================================================
# T6 · Crónica
# =====================================================================================
texto('t6', 'El hombre que le da vuelta a la música', 'Crónica', False, pars(
    'A las once de la mañana, cuando la plaza todavía huele a pan y a pasto mojado, don Aurelio estaciona su organillo junto a la pileta, le quita una manta de lana como quien destapa a un niño dormido y empieza a girar la manivela. Suena un vals. Dos palomas se espantan; una niña, en cambio, se acerca.',
    'El organillo tiene más de cien años y pesa casi lo mismo que su dueño. Por dentro, un cilindro de madera cubierto de pequeñas púas metálicas abre y cierra el paso del aire hacia los tubos: cada vuelta de manivela es, literalmente, una canción que se desenrolla. Don Aurelio lo heredó de su padre, que a su vez lo había heredado del suyo. «Yo no toco el organillo», aclara. «Yo le doy vuelta. La música ya viene adentro».',
    'Junto a él trabaja su nieto Kevin, de diecisiete años, que es chinchinero: lleva un bombo a la espalda, hace sonar unos platillos con una cuerda amarrada al pie y baila dando vueltas rapidísimas mientras golpea el bombo con dos baquetas largas. Cuando Kevin gira, los niños gritan, y cuando un niño grita, los adultos sacan la billetera. Así funciona la economía de la plaza.',
    'Pero no siempre funciona. Don Aurelio calcula que hoy gana la mitad que hace veinte años. Según él, los celulares compiten con ventaja: «La gente ya trae la música en el bolsillo. Antes, la música había que salir a buscarla». A eso se suma otro problema: cada vez quedan menos personas que sepan reparar y afinar un organillo.',
    'Le pregunto si Kevin seguirá con el oficio. Don Aurelio no responde de inmediato. Mira a su nieto, que en ese momento termina un giro y saluda con una reverencia exagerada, y se encoge de hombros. «Él dice que sí. Yo, a su edad, decía que no», responde, y vuelve a la manivela.',
    'Cuando me voy, el vals sigue sonando a mi espalda, cada vez más bajo, hasta que lo tapa el ruido de una micro. Me queda la sensación de haber escuchado algo que no se puede descargar.',
), nota='Crónica ficticia, escrita para esta app.')

q('t6', 1, 'localizar', 'basico', 'a', 'Según el párrafo 2, ¿qué mecanismo hace sonar la música dentro del organillo?', [
    ('Un cilindro con púas que abre y cierra el paso del aire hacia los tubos.', *OK),
    ('Unos parlantes que don Aurelio lleva escondidos dentro de la caja de madera.', 'fuera', 'El texto no menciona parlantes en el organillo.'),
    ('El bombo y los platillos del chinchinero.', 'otro-dato', 'Esos son los instrumentos de Kevin (párrafo 3), no el mecanismo del organillo.'),
    ('Las teclas que don Aurelio toca con los dedos mientras gira la manivela.', 'contrario', 'Él mismo dice: «Yo no toco el organillo. Yo le doy vuelta».'),
], 'Párrafo 2: «un cilindro de madera cubierto de pequeñas púas metálicas abre y cierra el paso del aire hacia los tubos».',
  ['un cilindro de madera cubierto de pequeñas púas metálicas abre y cierra el paso del aire hacia los tubos'])

q('t6', 2, 'localizar', 'paes', 'b', 'Según don Aurelio, ¿por qué hoy gana menos que antes?', [
    ('Porque cada vez es más difícil reparar el organillo.', 'otro-dato', 'Es otro problema del oficio, pero el texto no lo da como la razón de que gane menos.'),
    ('Porque la gente ya lleva música en su celular.', *OK),
    ('Porque los niños ya no se interesan por el organillo.', 'contrario', 'Los niños se acercan y gritan cuando Kevin baila.'),
    ('Porque su nieto todavía no sabe tocar el organillo.', 'fuera', 'El texto no dice eso.'),
], 'Es una paráfrasis de «los celulares compiten con ventaja: “La gente ya trae la música en el bolsillo”».',
  ['Según él, los celulares compiten con ventaja: «La gente ya trae la música en el bolsillo.'])

q('t6', 3, 'interpretar', 'paes', 'e', '¿Qué quiere decir don Aurelio con «Yo no toco el organillo. Yo le doy vuelta. La música ya viene adentro»?', [
    ('Que no sabe música y por eso el organillo suena mal.', 'fuera', 'Nada indica que suene mal.'),
    ('Que su trabajo no tiene ningún mérito, porque cualquiera podría hacerlo.', 'exagera', 'Explica cómo funciona el instrumento; no dice que su trabajo no valga.'),
    ('Que la música está guardada en el instrumento y él solo la hace sonar.', *OK),
    ('Que su nieto es el verdadero músico de la familia.', 'otro-dato', 'Kevin es chinchinero, pero la frase habla del organillo.'),
], 'Se relaciona con la explicación del cilindro con púas: la canción ya está «escrita» en el cilindro y la manivela la hace sonar.',
  ['cada vuelta de manivela es, literalmente, una canción que se desenrolla', 'Yo le doy vuelta. La música ya viene adentro'])

q('t6', 4, 'interpretar', 'basico', 'h', '¿Qué función cumple la frase «Así funciona la economía de la plaza» en el párrafo 3?', [
    ('Explicar con datos concretos cuánto dinero gana un organillero en la plaza.', 'exagera', 'No hay ningún dato: es un cierre con humor.'),
    ('Criticar a los adultos por gastar dinero en la plaza.', 'fuera', 'No hay crítica a los adultos.'),
    ('Introducir el tema de la pobreza en Chile.', 'amplia', 'Va mucho más allá de lo que trata el párrafo.'),
    ('Resumir con humor cómo el baile termina en dinero para ellos.', *OK),
], 'Kevin gira → los niños gritan → los adultos pagan. La frase resume esa cadena con ironía amable.',
  ['Cuando Kevin gira, los niños gritan, y cuando un niño grita, los adultos sacan la billetera. Así funciona la economía de la plaza.'])

q('t6', 5, 'interpretar', 'dificil', 'd', '¿Qué sugiere la respuesta de don Aurelio: «Él dice que sí. Yo, a su edad, decía que no»?', [
    ('Que no es seguro lo que hará Kevin: a esa edad uno cambia de idea.', *OK),
    ('Que Kevin miente cuando dice que quiere seguir con el oficio de su abuelo.', 'exagera', 'No lo acusa de mentir: solo duda de que lo dicho a esa edad sea definitivo.'),
    ('Que don Aurelio no quiere que su nieto siga con el organillo.', 'fuera', 'El texto no muestra lo que él quiere.'),
    ('Que don Aurelio nunca fue organillero.', 'contrario', 'Sí lo fue: heredó el organillo y sigue tocándolo.'),
], 'Él decía que no y terminó siendo organillero; su nieto dice que sí… y quizás cambie. Por eso se encoge de hombros.',
  ['se encoge de hombros', '«Él dice que sí. Yo, a su edad, decía que no»'])

q('t6', 6, 'evaluar', 'paes', 'k', '¿Cuál es el propósito principal de esta crónica?', [
    ('Explicar el funcionamiento técnico de un organillo.', 'parcial', 'Lo explica en el párrafo 2, pero es solo una parte.'),
    ('Retratar el oficio de un organillero y las dificultades que enfrenta hoy.', *OK),
    ('Convencer a los lectores de dar dinero a los artistas callejeros.', 'fuera', 'No hay ningún llamado a dar dinero.'),
    ('Denunciar la falta de técnicos que reparen instrumentos.', 'parcial', 'Es un detalle del párrafo 4, no el propósito del texto.'),
], 'La crónica muestra a don Aurelio trabajando, su historia, sus problemas y el futuro incierto del oficio.',
  ['Pero no siempre funciona', 'Le pregunto si Kevin seguirá con el oficio'])

q('t6', 7, 'evaluar', 'dificil', 'l', '¿Qué actitud del cronista se percibe en el último párrafo?', [
    ('Molestia por el ruido de la ciudad.', 'literal', 'La micro aparece, pero no es una queja: marca cómo lo moderno tapa lo antiguo.'),
    ('Indiferencia, porque se va de la plaza antes de que termine el vals.', 'contrario', 'La frase final muestra que la experiencia le dejó huella.'),
    ('Aprecio y algo de nostalgia por una experiencia que siente única.', *OK),
    ('Alegría porque podrá descargar el vals más tarde.', 'contrario', 'Dice lo contrario: es algo «que no se puede descargar».'),
], '«Algo que no se puede descargar» valora lo que solo se vive en persona, y el vals que se apaga tiene un tono nostálgico.',
  ['Me queda la sensación de haber escuchado algo que no se puede descargar.'])

# =====================================================================================
# T7 · Cuento (narrador en tercera persona, salto temporal)
# =====================================================================================
texto('t7', 'La casa de los relojes', 'Cuento', True, pars(
    'En la casa de doña Elcira había once relojes y todos marcaban las seis y diez. Los de pared, el de la cocina, el despertador del velador y hasta el reloj de bolsillo que dormía en un cajón con naftalina. Al principio, las visitas intentaban corregirlos. Después aprendieron a mirar sus propios teléfonos sin decir nada.',
    'Las seis y diez era la hora en que, treinta años atrás, don Hernán había salido a comprar pan y no había vuelto. Un camión, una esquina, una lluvia que nadie esperaba en octubre. Esa misma noche, doña Elcira detuvo el reloj del comedor. Al día siguiente detuvo los demás, uno por uno, con la paciencia de quien cierra las ventanas antes de una tormenta.',
    'Matilde, la nieta, llegó a vivir con ella el verano en que cumplió quince años. Traía una mochila, un celular con la pantalla trizada y la costumbre de preguntarlo todo. «¿Por qué los relojes están parados?», preguntó la primera noche. «Porque así me gustan», respondió la abuela, y le sirvió más sopa.',
    'Durante semanas, Matilde no volvió a preguntar. Pero se fijó en que la abuela pasaba el plumero por los relojes con más cuidado que por los retratos, y en que a veces se quedaba mirando el del comedor como quien espera que alguien entre por la puerta.',
    'Una tarde de marzo, mientras la abuela dormía siesta, Matilde descolgó el reloj de la cocina, le dio cuerda con una llave diminuta que encontró en el cajón del reloj de bolsillo y lo volvió a colgar. El tictac llenó la cocina como un pájaro que nadie había invitado.',
    'Doña Elcira lo escuchó al despertar. Se quedó quieta en el pasillo un largo rato, con una mano apoyada en la pared. Matilde esperó el reto desde la mesa. Pero la abuela solo se acercó al reloj, lo miró y dijo: «Va dos minutos atrasado». Y lo adelantó con la punta del dedo.',
), nota='Cuento original, escrito para esta app.')

q('t7', 1, 'localizar', 'basico', 'a', '¿Cuántos relojes había en la casa de doña Elcira?', [
    ('Seis.', 'otro-dato', 'Confundes la hora que marcaban (las seis y diez) con la cantidad de relojes.'),
    ('Once.', *OK),
    ('Treinta.', 'otro-dato', 'Treinta son los años que pasaron desde que don Hernán no volvió.'),
    ('Quince.', 'otro-dato', 'Quince es la edad de Matilde.'),
], 'Párrafo 1: «había once relojes y todos marcaban las seis y diez».',
  ['había once relojes y todos marcaban las seis y diez'])

q('t7', 2, 'localizar', 'paes', 'b', '¿Qué ocurrió a las seis y diez, treinta años antes?', [
    ('Doña Elcira detuvo todos los relojes de la casa.', 'otro-dato', 'Los detuvo después: uno esa noche y los demás al día siguiente.'),
    ('Matilde llegó a vivir con su abuela.', 'otro-dato', 'Matilde llega mucho después, a los quince años.'),
    ('Don Hernán salió de la casa y no regresó.', *OK),
    ('Se cortó la luz por una tormenta.', 'literal', 'La tormenta aparece solo en una comparación, y el texto no menciona ningún corte de luz.'),
], 'Es una paráfrasis de «don Hernán había salido a comprar pan y no había vuelto».',
  ['Las seis y diez era la hora en que, treinta años atrás, don Hernán había salido a comprar pan y no había vuelto.'])

q('t7', 3, 'interpretar', 'paes', 'e', '¿Qué representan los relojes detenidos?', [
    ('La falta de dinero de la familia para mandar a arreglarlos.', 'fuera', 'El texto nunca habla de dinero.'),
    ('El gusto de la abuela por coleccionar relojes antiguos.', 'literal', 'Toma al pie de la letra su respuesta evasiva: «Porque así me gustan».'),
    ('La incapacidad de la abuela para darles cuerda ella misma.', 'fuera', 'Nada lo indica: los detuvo ella misma, a propósito.'),
    ('El duelo de la abuela, detenida en el día de su pérdida.', *OK),
], 'Todos marcan la hora en que su esposo salió y no volvió, y ella los cuida «como quien espera que alguien entre por la puerta»: el tiempo se detuvo para ella.',
  ['Esa misma noche, doña Elcira detuvo el reloj del comedor.', 'como quien espera que alguien entre por la puerta'])

q('t7', 4, 'interpretar', 'paes', 'e', 'En el párrafo 2, ¿qué sugiere la comparación «con la paciencia de quien cierra las ventanas antes de una tormenta»?', [
    ('Que esa noche hubo una tormenta y la abuela cerró todas las ventanas.', 'literal', 'Es una comparación: no dice que haya cerrado ventanas.'),
    ('Que los detuvo con calma, como quien se protege del dolor.', *OK),
    ('Que detuvo los relojes con rabia y apuro.', 'contrario', 'El texto habla de «paciencia» y de hacerlo «uno por uno».'),
    ('Que detener los relojes le daba lo mismo.', 'contrario', 'Cerrar las ventanas antes de una tormenta es protegerse: no es indiferencia.'),
], 'Cerrar ventanas antes de una tormenta es prepararse y protegerse. Detener los relojes fue su forma de protegerse del dolor.',
  ['con la paciencia de quien cierra las ventanas antes de una tormenta'])

q('t7', 5, 'interpretar', 'dificil', 'c', '¿Qué cambio muestra doña Elcira en el último párrafo?', [
    ('Acepta que el tiempo vuelva a correr en su casa.', *OK),
    ('Se enoja con su nieta por tocar el reloj.', 'contrario', 'Matilde espera el reto, pero no llega.'),
    ('Decide volver a detener todos los relojes.', 'contrario', 'Hace lo contrario: corrige la hora del reloj para que funcione bien.'),
    ('Olvida por completo a don Hernán.', 'exagera', 'Aceptar que el tiempo avance no es olvidar.'),
], 'En vez de detenerlo, adelanta el reloj para que marque la hora correcta: acepta que el tiempo siga.',
  ['«Va dos minutos atrasado». Y lo adelantó con la punta del dedo.'])

q('t7', 6, 'evaluar', 'paes', 'k', '¿Qué tipo de narrador tiene el relato?', [
    ('Matilde, que cuenta lo que vivió con su abuela.', 'voz', 'Matilde es un personaje: el relato habla de ella en tercera persona («Matilde descolgó…»).'),
    ('Doña Elcira, que recuerda a su esposo.', 'voz', 'El relato habla de doña Elcira en tercera persona.'),
    ('Un narrador en tercera persona, que no es personaje de la historia.', *OK),
    ('Un narrador en primera persona que participa como testigo.', 'contrario', 'No hay «yo» en el relato.'),
], 'Todo se cuenta en tercera persona («doña Elcira detuvo», «Matilde se fijó»), por alguien que no participa.',
  ['Matilde descolgó el reloj de la cocina', 'Doña Elcira lo escuchó al despertar.'])

q('t7', 7, 'interpretar', 'dificil', 'e', '¿Cuál es el conflicto central del relato?', [
    ('La pelea entre una abuela y su nieta adolescente.', 'exagera', 'No hay pelea: ni siquiera hay reto.'),
    ('La dificultad de reparar relojes antiguos.', 'literal', 'Los relojes no están rotos: están detenidos a propósito.'),
    ('El duelo de una mujer que no deja avanzar el tiempo.', *OK),
    ('La adaptación de una adolescente a vivir en una casa que no es la suya.', 'parcial', 'Matilde llega a vivir ahí, pero el conflicto es el de la abuela.'),
], 'El problema humano del relato es el duelo de doña Elcira; la nieta es quien lo destraba.',
  ['no había vuelto', 'como quien espera que alguien entre por la puerta'])

q('t7', 8, 'interpretar', 'basico', 'h', '¿Qué función cumple el párrafo 2 en el relato?', [
    ('Presentar a Matilde, la nieta, y contar cómo llegó a vivir a la casa.', 'otro-dato', 'Eso lo hace el párrafo 3.'),
    ('Explicar con un salto al pasado por qué los relojes están parados.', *OK),
    ('Contar cómo termina la historia.', 'otro-dato', 'El final está en el párrafo 6.'),
    ('Describir cómo era la casa por dentro.', 'fuera', 'Ningún párrafo se dedica a describir la casa.'),
], 'El párrafo 2 vuelve treinta años atrás (un salto temporal) para explicar el misterio del párrafo 1.',
  ['treinta años atrás'])

# =====================================================================================
# Diagnóstico (index.html): se completan tarea, tipo de trampa y evidencia
# =====================================================================================
DIAG = {
    'd-len-01': ('a', ['otro-dato', 'otro-dato', None, 'fuera'],
                 ['un grupo de personas pasó quince minutos copiando números de una lista antes de inventar usos para un vaso plástico']),
    'd-len-02': ('a', [None, 'otro-dato', 'otro-dato', 'otro-dato'],
                 ['Cuando se vuelve crónico, se relaciona con el desánimo y con conductas de riesgo']),
    'd-len-03': ('h', ['literal', 'exagera', None, 'otro-dato'],
                 ['el aburrimiento funciona de un modo parecido al hambre', 'el aburrimiento avisaría que lo que estamos haciendo ya no nos aporta nada y que conviene buscar otra cosa']),
    'd-len-04': ('f', ['exagera', None, 'contrario', 'parcial'],
                 ['no como una falla, sino como una señal', 'hoy casi nunca dejamos que esa señal haga su trabajo', 'La clave, dicen, no está en buscarlo ni en huir de él, sino en escucharlo']),
    'd-len-05': ('h', ['fuera', 'contrario', 'fuera', None],
                 ['Ese grupo propuso más ideas, y más variadas, que otro grupo que pasó directo a la tarea creativa']),
    'd-len-06': ('l', ['contrario', None, 'contrario', 'fuera'],
                 ['preguntarse qué nos está pidiendo antes de taparlo con lo primero que tengamos a mano']),
}


# Ajustes del diagnóstico tras la revisión ciega (mismo id y mismo orden de alternativas: los resultados guardados siguen valiendo)
DIAG_AJUSTES = {
    'd-len-03': {'opciones': {3: 'Criticar la idea antigua de que el aburrimiento es pereza o un defecto del carácter.'}},
    'd-len-04': {'opciones': {2: 'El teléfono celular es la causa principal del aburrimiento en la vida moderna.'}},
    'd-len-05': {'tema': 'len.interpretar', 'opciones': {1: 'Contradecir la idea de que el aburrimiento es una señal útil para cambiar de actividad.'}},
    'd-len-06': {'enunciado': '¿Con cuál de las siguientes afirmaciones estarían de acuerdo los especialistas que cita el texto?'},
}


def plano(html):
    return re.sub(r'<[^>]+>', '', html)


def revisar(preguntas, textos):
    """Errores de forma propios de Lectora (los usa también tools/verificar_len.py)."""
    errs = []
    por_id = {t['id']: t for t in textos}
    for p in preguntas:
        pid = p['id']
        t = por_id.get(p.get('texto'))
        if not t:
            errs.append(f'{pid}: texto desconocido {p.get("texto")!r}')
            continue
        if p.get('tarea') not in TAREAS.get(p['tema'], ''):
            errs.append(f'{pid}: tarea {p.get("tarea")!r} no corresponde a {p["tema"]}')
        ev = p.get('evidencia') or []
        if not ev:
            errs.append(f'{pid}: sin evidencia')
        for f in ev:
            if '<' in f or '>' in f:
                errs.append(f'{pid}: la evidencia no puede tener etiquetas: {f!r}')
            n = t['html'].count(f)
            if n != 1:
                errs.append(f'{pid}: la evidencia aparece {n} veces en el texto (debe ser 1): {f!r}')
        pos = sorted((t['html'].find(f), t['html'].find(f) + len(f)) for f in ev if f in t['html'])
        if any(pos[k][1] > pos[k + 1][0] for k in range(len(pos) - 1)):
            errs.append(f'{pid}: dos fragmentos de evidencia se superponen')
        for i, o in enumerate(p['opciones']):
            if i == p['correcta']:
                if o.get('tipo'):
                    errs.append(f'{pid}: la correcta no lleva tipo de trampa')
            elif o.get('tipo') not in TIPOS:
                errs.append(f'{pid}: alternativa {i} con tipo de trampa inválido {o.get("tipo")!r}')
    return errs


def main():
    diag_p = T / 'banco_diag.json'
    diag = json.loads(diag_p.read_text(encoding='utf-8'))
    for p in diag['LEN']['preguntas']:
        tarea, tipos, ev = DIAG[p['id']]
        aj = DIAG_AJUSTES.get(p['id'], {})
        for k in ('tema', 'enunciado'):
            if k in aj:
                p[k] = aj[k]
        for i, t in aj.get('opciones', {}).items():
            p['opciones'][i]['texto'] = t
        p['texto'] = 'diag'
        p['tarea'] = tarea
        p['evidencia'] = ev
        for o, ti in zip(p['opciones'], tipos):
            if ti:
                o['tipo'] = ti
            else:
                o.pop('tipo', None)
    diag_p.write_text(json.dumps(diag, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    texto_diag = {'id': 'diag', 'titulo': diag['LEN']['titulo'], 'html': diag['LEN']['texto']}
    errs = revisar(PREGUNTAS + diag['LEN']['preguntas'], TEXTOS + [texto_diag])
    for e in errs:
        print('ERROR', e)
    banco = {'textos': TEXTOS, 'preguntas': PREGUNTAS}
    (T / 'banco_len.json').write_text(json.dumps(banco, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    from collections import Counter
    c = Counter((p['tema'], p['nivel']) for p in PREGUNTAS + diag['LEN']['preguntas'])
    print(f'banco_len.json: {len(TEXTOS)} textos, {len(PREGUNTAS)} preguntas (+{len(diag["LEN"]["preguntas"])} del diagnóstico)')
    for tema in TAREAS:
        print(' ', tema, {n: c[(tema, n)] for n in ('basico', 'paes', 'dificil')})
    palabras = {t['id']: len(plano(t['html']).split()) for t in TEXTOS}
    print('  palabras por texto:', palabras)
    return 1 if errs else 0


if __name__ == '__main__':
    raise SystemExit(main())
