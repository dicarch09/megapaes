#!/usr/bin/env python3
"""Lecciones del rescate de Biología y Química (bioquim.html), en formato tarjeta.

Cada tema: una idea, tarjetas cortas (una con un esquema SVG) y su práctica (3 preguntas en tools/banco_bq.json).
Escribe las lecciones entre los marcadores <!-- @@bio@@ --> … <!-- @@/bio@@ --> y <!-- @@qui@@ --> … <!-- @@/qui@@ -->.
Es idempotente. Temas aprobados por Ricardo (ver CLAUDE.md). Uso: python3 tools/bioquim.py
"""
import math
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from esquemas import aro, caja, circ, curva, fl, ln, poly, puntos, svg, tx  # noqa: E402
from bioquim_dibujos import DIBUJOS  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parent.parent


def neurona():
    d = ''.join(ln(30, 46, x, y, 'a', 2) for x, y in ((8, 22), (6, 46), (10, 70), (18, 14), (16, 80)))
    mielina = ''.join(caja(60 + 24 * i, 39, 18, 14, 'b') for i in range(4))
    term = ''.join(ln(160, 46, 182, y, 'a', 2) + circ(184, y, 3, 'fa') for y in (30, 46, 62))
    return svg(d, circ(32, 46, 12, 'fa'), ln(44, 46, 160, 46, 'a', 3), mielina, term,
               tx(2, 90, 'dendritas', 'start'), tx(40, 26, 'soma'), tx(108, 30, 'axón con mielina'), tx(198, 16, 'terminal', 'end'),
               fl(70, 70, 150, 70, 'w', 2.5), tx(110, 86, 'sentido del impulso'))


def ciclo_hormonas():
    est = curva(puntos(lambda x: 76 - 46 * math.exp(-((x - 88) / 22) ** 2) - 14 * math.exp(-((x - 150) / 18) ** 2), 14, 194, 90), 'a', 2.5)
    lh = curva(puntos(lambda x: 76 - 56 * math.exp(-((x - 104) / 5) ** 2), 14, 194, 120), 'r', 2.5)
    pro = curva(puntos(lambda x: 76 - 38 * math.exp(-((x - 150) / 20) ** 2), 14, 194, 90), 'g', 2.5)
    return svg(ln(14, 78, 194, 78, 'm', 1.5), ln(104, 8, 104, 78, 'm', 1.2, '3 3'), est, lh, pro,
               tx(104, 90, 'ovulación ~día 14'), tx(60, 22, 'estrógenos', 'middle'), tx(118, 14, 'LH', 'start'), tx(170, 30, 'progesterona'),
               tx(14, 90, 'día 1', 'start'), tx(194, 90, '28', 'end'))


def mitosis_meiosis():
    def cel(x, y, r, c, t):
        return aro(x, y, r, c, 2.5) + tx(x, y + 4, t)
    izq = cel(30, 46, 14, 'a', '2n') + fl(46, 40, 66, 26, 'm', 2) + fl(46, 52, 66, 66, 'm', 2) + cel(80, 22, 12, 'a', '2n') + cel(80, 70, 12, 'a', '2n')
    der = (cel(116, 46, 14, 'b', '2n') + fl(132, 40, 146, 28, 'm', 2) + fl(132, 52, 146, 64, 'm', 2) + cel(156, 24, 10, 'b', 'n') + cel(156, 68, 10, 'b', 'n')
           + ''.join(fl(167, y, 178, y + d, 'm', 1.6) for y, d in ((20, -8), (28, 8), (64, -8), (72, 8))) + ''.join(cel(188, y, 7, 'w', 'n') for y in (10, 36, 56, 82)))
    return svg(izq, der, tx(55, 90, 'mitosis'), tx(150, 90, 'meiosis'))


def fotosintesis():
    return svg(caja(8, 30, 70, 32, 'g'), tx(43, 50, 'cloroplasto'), caja(122, 30, 70, 32, 'w'), tx(157, 50, 'mitocondria'),
               fl(78, 36, 122, 36, 'g', 2.5), tx(100, 28, 'glucosa + O₂'), fl(122, 56, 78, 56, 'w', 2.5), tx(100, 72, 'CO₂ + H₂O'),
               fl(20, 4, 20, 28, 'w', 2.5), tx(28, 12, 'luz', 'start'), fl(157, 64, 157, 86, 'r', 2.5), tx(170, 84, 'ATP', 'start'))


ESQUEMAS = {
    'bio.celula': svg(
        caja(6, 34, 80, 44, 'a'), ''.join(ln(10 + 8 * i, 34, 14 + 8 * i, 20, 'a', 2) + ln(14 + 8 * i, 20, 18 + 8 * i, 34, 'a', 2) for i in range(9)),
        tx(46, 60, 'enterocito'), tx(46, 92, '+ superficie'),
        caja(108, 30, 86, 48, 'w'), ''.join(f'<ellipse class="fw" cx="{120 + 16 * (i % 5)}" cy="{42 + 18 * (i // 5)}" rx="6" ry="3.5"/>' for i in range(10)),
        tx(151, 22, 'fibra muscular'), tx(151, 92, 'muchas mitocondrias')),
    'bio.nervioso': neurona(),
    'bio.reproduccion': ciclo_hormonas(),
    'bio.anticoncepcion-its': svg(
        caja(6, 8, 88, 76, 'r'), tx(50, 26, 'VIRUS'), tx(50, 46, 'VIH · herpes'), tx(50, 66, 'sin cura'),
        caja(106, 8, 88, 76, 'g'), tx(150, 26, 'BACTERIAS'), tx(150, 46, 'gonorrea'), tx(150, 60, 'clamidia'), tx(150, 76, 'antibióticos')),
    'bio.division': mitosis_meiosis(),
    'bio.manipulacion': svg(
        aro(40, 44, 22, 'a', 3), caja(34, 18, 14, 10, 'w'), tx(40, 84, 'plásmido + gen'), fl(66, 44, 98, 44, 'm', 2.5),
        f'<rect x="104" y="28" width="56" height="32" rx="16" class="b" stroke-width="2.5"/>', aro(124, 44, 7, 'a', 2), tx(132, 84, 'bacteria'),
        fl(162, 44, 184, 44, 'g', 2.5), circ(190, 44, 5, 'fg'), tx(186, 66, 'insulina')),
    'bio.evolucion': svg(
        ''.join(circ(14 + 12 * (i % 5), 24 + 14 * (i // 5), 4.5, 'fr' if i in (3, 11) else 'fm') for i in range(15)), tx(38, 86, 'generación 1'),
        fl(78, 44, 116, 44, 'w', 2.5), tx(97, 60, 'selección'),
        ''.join(circ(128 + 12 * (i % 5), 24 + 14 * (i // 5), 4.5, 'fm' if i in (2, 9) else 'fr') for i in range(15)), tx(152, 86, 'generación 20')),
    'bio.fotosintesis': fotosintesis(),
    'qui.materia': svg(
        caja(70, 2, 60, 18, 'm'), tx(100, 15, 'materia'), ln(100, 20, 50, 32, 'm', 2), ln(100, 20, 150, 32, 'm', 2),
        caja(4, 32, 92, 18, 'a'), tx(50, 45, 'sustancia pura'), caja(112, 32, 76, 18, 'b'), tx(150, 45, 'mezcla'),
        ln(50, 50, 26, 66, 'a', 2), ln(50, 50, 72, 78, 'a', 2), ln(150, 50, 126, 66, 'b', 2), ln(150, 50, 160, 78, 'b', 2),
        tx(32, 76, 'elemento'), tx(72, 90, 'compuesto'), tx(126, 76, 'homogénea'), tx(160, 90, 'heterogénea')),
    'qui.modelos': svg(
        circ(20, 40, 15, 'fm'), tx(20, 84, 'Dalton'),
        aro(66, 40, 16, 'r', 2.5), ''.join(circ(66 + dx, 40 + dy, 2.5, 'fa') for dx, dy in ((-7, -6), (6, -8), (0, 2), (-6, 9), (8, 7))), tx(66, 72, 'Thomson'),
        circ(128, 40, 3.5, 'fr'), '<ellipse class="a" cx="128" cy="40" rx="20" ry="8" stroke-width="1.8"/>', '<ellipse class="a" cx="128" cy="40" rx="8" ry="20" stroke-width="1.8"/>', tx(128, 84, 'Rutherford'),
        circ(180, 40, 3.5, 'fr'), aro(180, 40, 10, 'a', 1.8), aro(180, 40, 18, 'a', 1.8), circ(190, 40, 2.5, 'fa'), circ(180, 22, 2.5, 'fa'), tx(180, 72, 'Bohr')),
    'qui.carbono': svg(
        ''.join(ln(30, 44, 30 + 18 * math.cos(math.radians(a)), 44 + 18 * math.sin(math.radians(a)), 'a', 3) for a in (-90, 30, 150)), ln(30, 44, 36, 52, 'a', 3, '3 3'), circ(30, 44, 5, 'fm'),
        tx(30, 80, 'sp³ · 109,5°'),
        ''.join(ln(100, 44, 100 + 20 * math.cos(math.radians(a)), 44 + 20 * math.sin(math.radians(a)), 'b', 3) for a in (-90, 30, 150)), circ(100, 44, 5, 'fm'), tx(100, 80, 'sp² · 120°'),
        ln(146, 44, 194, 44, 'w', 3), circ(170, 44, 5, 'fm'), tx(170, 80, 'sp · 180°')),
    'qui.organica': svg(
        curva([(6, 54), (26, 38), (46, 54), (66, 38)], 'a', 3), ln(66, 38, 76, 46, 'a', 2.5), tx(78, 52, 'OH', 'start'),
        ''.join(circ(x, y, 3, 'fm') for x, y in ((6, 54), (26, 38), (46, 54), (66, 38))),
        tx(44, 76, 'butanol'), tx(44, 90, 'vértice = un C'), tx(110, 18, '–OH alcohol', 'start'), tx(110, 38, '–CHO aldehído', 'start'), tx(110, 58, '–CO– cetona', 'start'), tx(110, 78, '–COOH ácido', 'start')),
    'qui.estequiometria': svg(
        ''.join(circ(14 + 18 * k, 34, 6, 'fa') + circ(14 + 18 * k, 48, 6, 'fa') for k in range(2)), tx(62, 44, '+'),
        circ(80, 34, 7, 'fr') + circ(80, 50, 7, 'fr'), fl(96, 42, 120, 42, 'm', 2.5),
        ''.join(circ(140 + 32 * k, 42, 7, 'fr') + circ(131 + 32 * k, 30, 5, 'fa') + circ(149 + 32 * k, 30, 5, 'fa') for k in range(2)),
        tx(48, 80, '4 H · 2 O'), tx(156, 80, '4 H · 2 O'), tx(100, 16, '2 H₂ + O₂ → 2 H₂O')),
    'qui.composicion': svg(
        f'<rect x="14" y="28" width="{0.2727 * 172:.1f}" height="26" rx="6" class="fm"/>',
        f'<rect x="{14 + 0.2727 * 172:.1f}" y="28" width="{0.7273 * 172:.1f}" height="26" rx="6" class="fr"/>',
        tx(14 + 0.2727 * 86, 46, 'C'), tx(14 + 0.2727 * 172 + 0.7273 * 86, 46, 'O · 72,7 %'), tx(100, 16, 'CO₂ = 44 g/mol'),
        tx(100, 78, 'C: 12/44 = 27,3 %')),
    'qui.soluciones': svg(
        poly([(20, 30), (20, 80), (60, 80), (60, 30)], 'm', None), f'<rect x="21" y="52" width="38" height="27" style="fill:var(--acc2);fill-opacity:.35"/>',
        ''.join(circ(x, y, 3, 'fr') for x, y in ((30, 62), (44, 58), (38, 72), (52, 68))), tx(40, 92, '100 mL · 2 M'),
        fl(70, 56, 104, 56, 'm', 2.5), tx(87, 46, '+ agua'),
        poly([(118, 8), (118, 80), (186, 80), (186, 8)], 'm', None), f'<rect x="119" y="22" width="66" height="57" style="fill:var(--acc2);fill-opacity:.18"/>',
        ''.join(circ(x, y, 3, 'fr') for x, y in ((132, 40), (160, 34), (146, 64), (172, 58))), tx(152, 92, '400 mL · 0,5 M')),
}

# (id, pestaña, título, chips extra, idea, [(etiqueta, título, html)])  —  la tarjeta '§' lleva el esquema
TEMAS = [
    ('bio.celula', 'bio', 'Célula: organelos y células especializadas', [],
     'La célula es una fábrica: cada organelo hace un trabajo. Si una célula hace mucho de algo, tiene mucho del organelo que lo hace: <b>la forma sigue a la función</b>.',
     [('§', 'Forma ↔ función', 'Más superficie para absorber; más mitocondrias donde se gasta más energía.'),
      ('dos tipos', 'Procarionte y eucarionte', '<b>Procarionte</b> (bacterias): sin núcleo (ADN en el citoplasma) y sin organelos con membrana; tiene membrana, ribosomas, pared y a veces cápsula y flagelo. <b>Eucarionte</b>: núcleo con membrana y organelos (animales y plantas).'),
      ('animal vs vegetal', 'Lo que cambia', 'Solo vegetal: <b>pared celular</b> (celulosa), <b>cloroplastos</b> y una <b>vacuola central</b> grande. Solo animal: <b>centriolos</b>. Ambas: núcleo, mitocondrias, retículos, Golgi y ribosomas.'),
      ('control', 'Membrana, núcleo y nucléolo', '<b>Membrana</b>: controla qué entra y sale. <b>Núcleo</b>: guarda el ADN y dirige la célula. <b>Nucléolo</b>: arma los ribosomas.'),
      ('fábrica de proteínas', 'Ribosomas → RER → Golgi', '<b>Ribosomas</b>: hacen proteínas. <b>RER</b> (con ribosomas): proteínas para exportar o para la membrana. <b>Golgi</b>: las modifica, empaca y envía en vesículas. <b>REL</b> (liso): lípidos y desintoxicación.'),
      ('energía y limpieza', 'Mitocondria, cloroplasto, lisosoma, peroxisoma', '<b>Mitocondria</b>: respiración celular → ATP. <b>Cloroplasto</b>: fotosíntesis. <b>Lisosoma</b>: digiere con enzimas. <b>Peroxisoma</b>: degrada sustancias tóxicas, como el agua oxigenada (H₂O₂).'),
      ('forma y movimiento', 'Citoesqueleto, centriolos, cilios y flagelos', '<b>Citoesqueleto</b>: da forma y mueve cosas dentro de la célula. <b>Centriolos</b>: organizan el huso en la división. <b>Cilios y flagelos</b>: movimiento.'),
      ('células especializadas', 'Cuatro que salen en la PAES', '<b>Enterocito</b> (intestino): microvellosidades para absorber. <b>Fibra muscular esquelética</b>: muchas mitocondrias y varios núcleos. <b>Neurona</b>: dendritas y axón para conducir señales. <b>Célula pancreática secretora</b>: mucho RER y Golgi para fabricar y exportar enzimas.')]),
    ('bio.nervioso', 'bio', 'Sistema nervioso y sus cuidados', ['nuevo 2027'],
     'El sistema nervioso recibe estímulos, los integra y ordena una respuesta. La señal viaja <b>eléctrica</b> por la neurona y <b>química</b> de una neurona a otra (sinapsis).',
     [('§', 'La neurona', 'Dendritas reciben → el soma integra → el axón conduce → el terminal libera neurotransmisores. La mielina aísla el axón y hace que el impulso viaje más rápido.'),
      ('organización', 'Central y periférico', '<b>SNC</b>: encéfalo y médula espinal (integran). <b>SNP</b>: nervios. Las vías <b>sensitivas</b> llevan información al SNC; las <b>motoras</b> llevan órdenes a músculos y glándulas.'),
      ('impulso', 'De reposo a impulso', 'En reposo el interior es negativo (unos −70 mV); lo mantiene la bomba Na⁺/K⁺. Si el estímulo supera el <b>umbral</b>: entra Na⁺ (<b>despolarización</b>) y luego sale K⁺ (<b>repolarización</b>). Es «todo o nada».'),
      ('sinapsis química', 'De una neurona a otra', 'El impulso llega al terminal → se liberan <b>neurotransmisores</b> al espacio sináptico → se unen a <b>receptores</b> de la neurona siguiente → la excitan (nace una nueva señal) o la inhiben. Va en un solo sentido.'),
      ('arco reflejo', 'Responder sin pensar', 'Receptor → neurona <b>sensitiva</b> → <b>médula espinal</b> → neurona <b>motora</b> → efector (músculo). Es rápido e involuntario: la médula responde antes de que el cerebro «se entere».'),
      ('sustancias', 'Café, alcohol y drogas', '<b>Cafeína</b>: estimulante (más alerta). <b>Alcohol</b>: depresor (reflejos y coordinación más lentos). Las <b>drogas de abuso</b> alteran la sinapsis y generan tolerancia y dependencia.'),
      ('cuidados', 'Sueño y prevención', 'Dormir lo suficiente (adolescentes: unas 8 a 10 horas) ayuda a la memoria y al aprendizaje. Prevenir traumatismos: casco, cinturón de seguridad y no lanzarse de cabeza a aguas desconocidas.')]),
    ('bio.reproduccion', 'bio', 'Reproducción: gametos, fecundación y ciclos', ['nuevo 2027'],
     'Dos gametos con la mitad de los cromosomas se unen en la fecundación. Cada mes, el <b>ovario</b> prepara un ovocito y el <b>útero</b> prepara el endometrio; las hormonas coordinan ambos ciclos.',
     [('§', 'Las hormonas del ciclo', 'Estrógenos suben antes de la ovulación; un pico de LH la provoca; después domina la progesterona.'),
      ('gametos', 'Espermatozoide y ovocito', '<b>Espermatozoide</b>: pequeño, con flagelo, mitocondrias (energía) y acrosoma (enzimas para entrar al ovocito). <b>Ovocito</b>: grande, inmóvil, con reservas. Ambos tienen 23 cromosomas (haploides).'),
      ('fecundación', 'Dónde y cómo', 'Ocurre en la <b>trompa de Falopio</b>. Un espermatozoide atraviesa las cubiertas y entra; en ese momento el ovocito bloquea la entrada de otros. Luego se unen los núcleos y se forma el <b>cigoto</b> (46 cromosomas).'),
      ('sistemas', 'Órganos y funciones', 'Masculino: <b>testículos</b> (espermatozoides y testosterona), conductos deferentes, vesículas seminales y próstata (forman el semen), uretra. Femenino: <b>ovarios</b> (ovocitos, estrógenos y progesterona), trompas, útero y vagina.'),
      ('ciclo ovárico', 'Folicular → ovulación → lútea', '<b>Fase folicular</b> (días 1–14): madura un folículo (FSH) y produce estrógenos. <b>Ovulación</b> (~día 14): el pico de <b>LH</b> libera el ovocito. <b>Fase lútea</b>: el folículo vacío forma el <b>cuerpo lúteo</b>, que secreta progesterona.'),
      ('ciclo uterino', 'Menstrual → proliferativa → secretora', '<b>Menstruación</b> (días 1–5): se desprende el endometrio. <b>Proliferativa</b>: el endometrio crece (estrógenos). <b>Secretora</b>: se prepara para un embrión (progesterona). Sin embarazo, el cuerpo lúteo degenera, baja la progesterona y llega la menstruación.'),
      ('sexualidad', 'Más que biología', 'La sexualidad incluye afectos, respeto, consentimiento y responsabilidad con uno mismo y con los demás. La PAES puede preguntar por estos aspectos sociales y afectivos.')]),
    ('bio.anticoncepcion-its', 'bio', 'Métodos anticonceptivos e ITS', ['nuevo 2027'],
     'Los anticonceptivos evitan que se junten espermatozoide y ovocito, o que haya ovulación. <b>Solo el condón protege además de las ITS.</b>',
     [('§', 'Virus o bacteria', 'VIH y herpes (virus) no tienen cura, sí tratamiento; gonorrea y clamidia (bacterias) se curan con antibióticos.'),
      ('naturales', 'Calendario, temperatura basal, Billings', 'Buscan no tener relaciones en los días fértiles: por el calendario de ciclos anteriores, por la <b>temperatura basal</b> (sube un poco tras ovular) o por el <b>moco cervical</b> (filante y transparente en días fértiles). Son los menos eficaces.'),
      ('barrera', 'Condón y diafragma', 'Impiden físicamente que los espermatozoides lleguen al ovocito. El <b>condón</b> (masculino o femenino) es el único que además previene ITS.'),
      ('hormonales', 'Píldora, inyección, implante', 'Impiden la <b>ovulación</b> (y espesan el moco cervical). Son reversibles: al dejarlos vuelve la fertilidad.'),
      ('quirúrgicos', 'Vasectomía y ligadura', 'Se cortan los conductos deferentes (vasectomía) o las trompas (ligadura). Muy eficaces; se consideran <b>parcialmente reversibles</b> porque revertirlos es difícil y no siempre funciona.'),
      ('ITS', 'Cuatro que debes conocer', '<b>VIH</b> (virus): ataca defensas (linfocitos T) y puede llevar al SIDA; se transmite por sexo, sangre y de madre a hijo. <b>Herpes genital</b> (virus): vesículas dolorosas que reaparecen. <b>Gonorrea</b> (bacteria): ardor y secreción. <b>Clamidia</b> (bacteria): muchas veces sin síntomas.'),
      ('prevención', 'Cómo cuidarse', 'Condón en todas las relaciones, testeo periódico, no compartir jeringas y conversar con la pareja. Que no haya síntomas no significa que no haya infección.')]),
    ('bio.division', 'bio', 'Ciclo celular, mitosis y meiosis', [],
     '<b>Mitosis</b>: una célula da 2 hijas iguales (crecer y reparar). <b>Meiosis</b>: una célula da 4 células con la mitad de los cromosomas y distintas entre sí (variabilidad). En el ser humano forma los gametos: 4 espermatozoides, pero solo 1 ovocito (el resto son cuerpos polares).',
     [('§', 'Mitosis vs meiosis', 'Mitosis: 1 división, 2 células 2n idénticas. Meiosis: 2 divisiones, 4 células n distintas.'),
      ('cromatina', 'Del hilo al cromosoma', 'El ADN se enrolla en proteínas (histonas): eso es la <b>cromatina</b>. Para dividirse se compacta al máximo y se ven los cromosomas. Un cromosoma duplicado tiene 2 <b>cromátidas hermanas</b> unidas por el centrómero.'),
      ('interfase', 'G1 → S → G2', '<b>G1</b>: la célula crece y trabaja. <b>S</b>: duplica su ADN. <b>G2</b>: se prepara para dividirse. Casi toda su vida la célula está en interfase.'),
      ('controles', 'Puntos de control', '<b>G1–S</b>: ¿hay condiciones y el ADN está sano? <b>G2–M</b>: ¿se copió bien el ADN? <b>Metafase</b>: ¿todos los cromosomas están unidos al huso? Si fallan, la célula puede dividirse sin freno: <b>cáncer</b>.'),
      ('mitosis', 'Profase, metafase, anafase, telofase', '<b>Profase</b>: se condensan los cromosomas y se forma el huso. <b>Metafase</b>: se alinean al centro. <b>Anafase</b>: se separan las cromátidas hermanas. <b>Telofase</b>: dos núcleos nuevos. Luego la citocinesis divide el citoplasma.'),
      ('meiosis', 'Dos divisiones seguidas', '<b>Meiosis I</b>: se separan los cromosomas homólogos (2n → n); en la profase I hay <b>entrecruzamiento</b>. <b>Meiosis II</b>: se separan las cromátidas, como en una mitosis. Resultado: 4 células haploides distintas.'),
      ('variabilidad', 'Por qué los hermanos no son iguales', 'El <b>entrecruzamiento</b> mezcla genes entre homólogos, y la <b>permutación cromosómica</b> reparte los homólogos al azar en la metafase I. Por eso cada gameto es único.')]),
    ('bio.manipulacion', 'bio', 'Manipulación genética', [],
     'Manipular genes es cortar un gen útil de un organismo y ponerlo en otro, que lo «lee» y fabrica la proteína. Funciona porque <b>el código genético es casi universal</b>.',
     [('§', 'ADN recombinante', 'El gen se pega en un plásmido, entra a una bacteria y la bacteria fabrica la proteína.'),
      ('paso a paso', 'Cómo se hace', '1) Se cortan el gen y el plásmido con la misma <b>enzima de restricción</b>. 2) Se pega en un vector (un plásmido) con <b>ligasa</b>. 3) Se introduce en la célula que lo va a usar. 4) La célula se multiplica y produce la proteína.'),
      ('fármacos', 'Medicamentos', '<b>Insulina humana</b> hecha por bacterias (para personas con diabetes), hormona del crecimiento y algunas vacunas.'),
      ('alimentos', 'Cultivos y alimentos', 'Cultivos <b>transgénicos</b> resistentes a plagas o a la sequía; arroz con más provitamina A; enzimas para fabricar queso.'),
      ('detergentes y ropa', 'Más allá de la comida', '<b>Detergentes</b> con enzimas (proteasas, lipasas) hechas por microorganismos modificados, que sacan manchas en agua fría. <b>Algodón</b> transgénico resistente a insectos.'),
      ('debate', 'Ventajas y riesgos', 'Ventajas: más producción y medicamentos más accesibles. Riesgos y debate: efectos en los ecosistemas, dependencia de semillas y etiquetado. La PAES puede pedir que evalúes ambos lados.')]),
    ('bio.evolucion', 'bio', 'Evolución y selección natural', [],
     'Las especies cambian con el tiempo. Darwin y Wallace lo explicaron con la <b>selección natural</b>: los individuos con variaciones ventajosas dejan más descendencia.',
     [('§', 'Selección natural', 'Si el ambiente favorece una variante que ya existía, generación tras generación esa variante se vuelve la mayoría.'),
      ('Lamarck', 'Uso, desuso y herencia de lo adquirido', 'La jirafa estiraba el cuello y heredaba ese cuello más largo a sus crías. Hoy se sabe que lo adquirido en vida <b>no se hereda</b>.'),
      ('Darwin y Wallace', 'Misma idea, por separado', 'Llegaron a la <b>selección natural</b> cada uno por su lado (se presentó en 1858). Darwin la desarrolló en <i>El origen de las especies</i> (1859).'),
      ('cómo funciona', 'Cinco ideas', '1) Hay <b>variación</b> entre individuos. 2) Parte de ella se <b>hereda</b>. 3) Nacen más de los que sobreviven: hay competencia. 4) Los mejor adaptados sobreviven y se reproducen más. 5) Con las generaciones, la población cambia.'),
      ('ejemplos', 'En la vida real', 'Bacterias resistentes a antibióticos; polillas oscuras que aumentaron en bosques con hollín; distintos picos en los pinzones de Galápagos según su alimento.'),
      ('evidencias', 'Cómo se sabe', '<b>Registro fósil</b> (formas intermedias). <b>Anatomía comparada</b>: estructuras <b>homólogas</b> (mismo origen, aunque tengan distinta función: brazo humano y ala de murciélago) y <b>análogas</b> (distinto origen, misma función: ala de ave y de insecto). <b>Embriología</b>: embriones parecidos. <b>Biología molecular</b>: ADN más parecido = parentesco más cercano.')]),
    ('bio.fotosintesis', 'bio', 'Fotosíntesis y respiración celular', [],
     'La fotosíntesis guarda la energía de la luz en glucosa; la respiración celular la libera como ATP. Lo que una produce, la otra lo usa: así circulan el <b>carbono</b> y el <b>oxígeno</b>.',
     [('§', 'Dos procesos que se complementan', 'El cloroplasto fabrica glucosa y O₂; la mitocondria los usa y devuelve CO₂ y agua.'),
      ('ecuaciones', 'Una es el reverso de la otra', '<b>Fotosíntesis</b>: 6 CO₂ + 6 H₂O + luz → C₆H₁₂O₆ + 6 O₂. <b>Respiración</b>: C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O + energía (ATP).'),
      ('nutrición', 'Autótrofos y heterótrofos', '<b>Autótrofos</b> fabrican su materia orgánica (plantas, algas). <b>Heterótrofos</b> la obtienen comiendo a otros (animales). Las plantas también respiran, de día y de noche.'),
      ('fase luminosa', 'En los tilacoides', 'Necesita luz. La clorofila capta la luz; el agua se rompe (<b>fotólisis</b>) y libera el <b>O₂</b>; se forman ATP y NADPH.'),
      ('fase oscura', 'En el estroma (ciclo de Calvin)', 'No necesita luz directamente: usa el ATP y el NADPH de la fase luminosa para <b>fijar CO₂</b> y formar glucosa.'),
      ('variables', 'Qué la acelera', 'Sube con más <b>luz</b>, más <b>CO₂</b> y temperatura adecuada, hasta un máximo: ahí otro factor pasa a limitar. Si hace demasiado calor, las enzimas se dañan y baja.'),
      ('ecosistema', 'Energía fluye, materia circula', 'La energía va en un solo sentido (sol → productores → consumidores) y se pierde como calor. El carbono y el oxígeno se reciclan entre fotosíntesis y respiración.')]),
    ('qui.materia', 'qui', 'Materia, mezclas y su separación', [],
     'La materia es <b>pura</b> (un solo tipo de sustancia) o una <b>mezcla</b>. Las mezclas se separan con métodos físicos que aprovechan una diferencia: tamaño, densidad o punto de ebullición.',
     [('§', 'Cómo se clasifica', 'Pura: elemento o compuesto. Mezcla: homogénea o heterogénea.'),
      ('sustancias puras', 'Elemento y compuesto', '<b>Elemento</b>: un solo tipo de átomo (O₂, Fe). <b>Compuesto</b>: dos o más elementos unidos en proporción fija (H₂O, NaCl); solo se separa por métodos químicos.'),
      ('mezclas', 'Homogénea y heterogénea', '<b>Homogénea</b>: una sola fase, no se distinguen sus partes (agua con sal, aire). <b>Heterogénea</b>: se ven las partes (agua con aceite, arena con piedras).'),
      ('separación', 'Cuatro métodos', '<b>Decantación</b>: líquidos que no se mezclan, o un sólido que se va al fondo (densidad). <b>Filtración</b>: un sólido no disuelto en un líquido. <b>Tamizado</b>: sólidos de distinto tamaño. <b>Destilación</b>: líquidos con distinto punto de ebullición, o recuperar el solvente de una sal disuelta.'),
      ('propiedades', 'Densidad y puntos de cambio', 'Propiedades físicas: puntos de fusión y de ebullición, masa, volumen y <b>densidad = masa / volumen</b> (g/mL). Lo menos denso flota.')]),
    ('qui.modelos', 'qui', 'Modelos atómicos y partículas (Z, A)', [],
     'La idea del átomo cambió con cada experimento: de esfera maciza (Dalton) a núcleo pequeño con electrones en niveles de energía (Bohr).',
     [('§', 'Cuatro modelos', 'Esfera maciza → budín con electrones → núcleo + electrones → órbitas con energía fija.'),
      ('Dalton', 'Esfera indivisible', 'Átomos indivisibles; los de un mismo elemento son iguales; los compuestos combinan átomos en proporciones fijas.'),
      ('Thomson', 'Budín de pasas', 'Descubre el <b>electrón</b>. Modelo: una esfera positiva con electrones incrustados.'),
      ('Rutherford', 'Núcleo', 'Lámina de oro: casi todas las partículas alfa pasan derecho, unas pocas se desvían y muy pocas rebotan. Conclusión: el átomo es casi todo <b>vacío</b>, con un <b>núcleo</b> pequeño, denso y positivo.'),
      ('Bohr', 'Niveles de energía', 'Los electrones giran en órbitas de energía fija. Al saltar de nivel absorben o emiten energía (luz).'),
      ('partículas', 'Z y A', '<b>Protón</b> (+) y <b>neutrón</b> (sin carga) en el núcleo; <b>electrón</b> (−) afuera, con masa muchísimo menor. <b>Z</b> = protones. <b>A</b> = protones + neutrones. <b>Neutrones = A − Z</b>. Átomo neutro: electrones = protones.')]),
    ('qui.carbono', 'qui', 'Átomo de carbono: hibridación y enlaces', [],
     'El carbono forma <b>4 enlaces</b> (es tetravalente). Según cómo los reparta —simples, dobles o triples— cambia su hibridación, su forma y el ángulo entre enlaces.',
     [('§', 'Tres formas', 'sp³ tetraédrico (109,5°), sp² plano (120°), sp lineal (180°).'),
      ('tetravalencia', 'Cuatro enlaces', 'El carbono tiene 4 electrones de valencia: forma 4 enlaces covalentes y puede unirse a otros carbonos en cadenas largas, ramificadas o en anillos.'),
      ('regla rápida', 'Cuenta los enlaces del C', 'Solo simples → <b>sp³</b> (metano, CH₄). Un doble → <b>sp²</b> (eteno, C₂H₄). Un triple o dos dobles → <b>sp</b> (etino, C₂H₂; el C del CO₂).'),
      ('enlaces', 'Simple, doble, triple', 'Más enlaces entre dos carbonos = enlace <b>más corto</b> y <b>más fuerte</b>. Longitud: C≡C (120 pm) &lt; C=C (134 pm) &lt; C–C (154 pm). Energía: al revés.')]),
    ('qui.organica', 'qui', 'Hidrocarburos y grupos funcionales', [],
     'Los compuestos orgánicos son cadenas de carbono. Si solo hay C e H son <b>hidrocarburos</b>; si aparece otro grupo de átomos (–OH, –COOH…), ese <b>grupo funcional</b> define sus propiedades y su nombre.',
     [('§', 'Fórmula topológica', 'Cada vértice o extremo de la línea es un carbono; los H no se dibujan.'),
      ('hidrocarburos', 'Alcanos, alquenos, alquinos', '<b>Alcanos</b> (solo simples, -ano): CₙH₂ₙ₊₂. <b>Alquenos</b> (un doble, -eno): CₙH₂ₙ. <b>Alquinos</b> (un triple, -ino): CₙH₂ₙ₋₂. También cíclicos (anillos) y <b>aromáticos</b> (anillo de benceno).'),
      ('prefijos', 'Cuántos carbonos', '1 met, 2 et, 3 prop, 4 but, 5 pent, 6 hex, 7 hept, 8 oct.'),
      ('grupos con O', 'Los más preguntados', 'Alcohol R–OH (-ol). Fenol: –OH en un benceno. Éter R–O–R\'. Aldehído R–CHO (-al). Cetona R–CO–R\' (-ona). Ácido carboxílico R–COOH (ácido -oico). Éster R–COO–R\'. Anhídrido R–CO–O–CO–R\'.'),
      ('grupos con N, S y halógenos', 'El resto de la lista', 'Amina R–NH₂. Amida R–CONH₂. Nitrilo R–C≡N. Haluro R–X (cloro, bromo…). Sulfuro R–S–R\'.'),
      ('representaciones', 'Formas de escribir una molécula', '<b>Molecular</b> (C₂H₆O: cuenta átomos). <b>Empírica</b> (proporción mínima). <b>Desarrollada</b> (todos los enlaces). <b>Semidesarrollada</b> (CH₃–CH₂–OH). <b>Condensada</b> (CH₃CH₂OH o C₂H₅OH). <b>Topológica</b> (zigzag). Modelos de <b>esferas y varillas</b> y <b>compactos</b>.')]),
    ('qui.estequiometria', 'qui', 'Leyes ponderales, mol y reactivo limitante', [],
     'En una reacción los átomos no se crean ni se destruyen: solo se reordenan. Por eso se <b>balancea</b> la ecuación y se calculan cantidades con el <b>mol</b>.',
     [('§', 'Una ecuación balanceada', 'El mismo número de átomos de cada elemento a cada lado.'),
      ('leyes ponderales', 'Lavoisier, Proust, Dalton', '<b>Conservación de la masa</b>: masa de reactantes = masa de productos. <b>Proporciones definidas</b>: un compuesto siempre tiene la misma proporción en masa (agua: 1 g de H por cada 8 g de O). <b>Proporciones múltiples</b>: si dos elementos forman varios compuestos, con la misma masa de uno, la del otro está en razón de enteros simples: con 12 g de C hay 16 g de O en el CO y 32 g en el CO₂ (1 : 2).'),
      ('balancear', 'Solo coeficientes', 'Reactantes → productos. Se cambian los <b>coeficientes</b> (los números de adelante), nunca los subíndices.'),
      ('mol', 'Contar por montones', '1 mol = 6,02·10²³ partículas. <b>Masa molar</b> = suma de masas atómicas: H₂O = 2·1 + 16 = 18 g/mol. <b>n = m / M</b>.'),
      ('cómo resolver', 'Cuatro pasos', '1) Ecuación balanceada. 2) Pasa a moles (n = m/M). 3) Usa la razón de coeficientes. 4) Vuelve a gramos si te piden masa.'),
      ('reactivo limitante', 'El que se acaba primero', 'Determina cuánto producto se forma; el otro queda en <b>exceso</b>. Para hallarlo, divide los moles de cada reactivo por su coeficiente: el menor es el limitante.')]),
    ('qui.composicion', 'qui', 'Composición porcentual y fórmula empírica', [],
     'La composición porcentual dice qué parte de la masa es de cada elemento. Con esos porcentajes se reconstruye la <b>fórmula empírica</b> (la proporción más simple) y, con la masa molar, la <b>molecular</b>.',
     [('§', 'Porcentaje en masa', '% = masa del elemento en 1 mol ÷ masa molar · 100.'),
      ('empírica vs molecular', 'Proporción y fórmula real', '<b>Empírica</b>: la razón entera más simple (CH₂O). <b>Molecular</b>: la real (glucosa C₆H₁₂O₆ = 6 · CH₂O). Molecular = n · empírica, con <b>n = masa molar real ÷ masa de la empírica</b>.'),
      ('receta', 'De porcentajes a fórmula', '1) Supón 100 g: los % pasan a gramos. 2) Divide cada uno por su masa atómica (moles). 3) Divide todo por el menor. 4) Si queda ,5 multiplica por 2; si queda ,33 o ,67, por 3; si queda ,25 o ,75, por 4.')]),
    ('qui.soluciones', 'qui', 'Soluciones: concentración y dilución', [],
     'Una solución es un soluto disuelto en un solvente. La <b>concentración</b> dice cuánto soluto hay en cierta cantidad de solución. Al diluir, los moles de soluto no cambian: <b>C₁·V₁ = C₂·V₂</b>.',
     [('§', 'Diluir', 'Mismas partículas de soluto en más volumen: la concentración baja.'),
      ('componentes', 'Soluto y solvente', '<b>Soluto</b>: lo que se disuelve. <b>Solvente</b>: donde se disuelve (el agua es el más común). Una solución es una mezcla homogénea.'),
      ('unidades físicas', '%m/m, %m/v, %v/v, ppm', '<b>%m/m</b> = g de soluto en 100 g de <b>solución</b>. <b>%m/v</b> = g de soluto en 100 mL de solución. <b>%v/v</b> = mL de soluto en 100 mL de solución. <b>ppm</b> = mg de soluto por kg (o por L) de solución.'),
      ('unidades químicas', 'Molaridad, molalidad, fracción molar', '<b>Molaridad</b> = mol de soluto / L de solución. <b>Molalidad</b> = mol de soluto / kg de <b>solvente</b>. <b>Fracción molar</b> = mol de un componente / mol totales (todas suman 1).'),
      ('mezclar', 'Dos soluciones del mismo soluto', 'Se suman los moles y se suman los volúmenes: C = (C₁V₁ + C₂V₂) / (V₁ + V₂).'),
      ('solubilidad', 'Cuánto se puede disolver', 'Es la máxima cantidad de soluto que se disuelve en una cantidad dada de solvente (por ejemplo, 100 g de agua) a cierta temperatura. Sólidos: suele subir con la temperatura. Gases: baja con la temperatura y sube con la presión (una bebida fría y cerrada guarda más gas). «Lo semejante disuelve a lo semejante».')]),
]


def leccion(tid, tab, titulo, extras, idea, tarjetas):
    chips = '<span class="chip R">Rescate</span>' + ''.join(f'<span class="chip nuevo">{c}</span>' for c in extras)
    cards = []
    for etq, tit, html in tarjetas:
        if etq == '§':
            cards.append(f'      <div class="tarjeta"><span class="onda">en un dibujo</span><h4>{tit}</h4>{ESQUEMAS[tid]}<p>{html}</p></div>')
        else:
            cards.append(f'      <div class="tarjeta"><span class="onda">{etq}</span><h4>{tit}</h4>{DIBUJOS.get((tid, tit), "")}<p>{html}</p></div>')
    sobran = {k for k in DIBUJOS if k[0] == tid} - {(tid, x[1]) for x in tarjetas}
    assert not sobran, f'dibujos sin tarjeta: {sobran}'
    return (f'  <section class="leccion" id="{tid}" data-tab="{tab}">\n'
            f'    <div class="lec-head"><h2>{titulo}</h2>{chips}<span class="dom" data-tema="{tid}"></span></div>\n'
            f'    <div class="lec-body">\n    <p class="idea">{idea}</p>\n    <div class="tarjetas">\n' + '\n'.join(cards) + '\n    </div>\n'
            f'    <div class="paso"><h3><span class="n">✓</span> Práctica: 3 preguntas</h3><div class="practica" data-temas="{tid}"></div></div>\n'
            '    </div>\n  </section>')


def aplicar():
    p = RAIZ / 'bioquim.html'
    s = p.read_text(encoding='utf-8')
    for tab in ('bio', 'qui'):
        html = '\n'.join(leccion(*t) for t in TEMAS if t[1] == tab)
        s, n = re.subn(rf'(<!-- @@{tab}@@ -->).*?(<!-- @@/{tab}@@ -->)', lambda m: f'{m.group(1)}\n{html}\n  {m.group(2)}', s, flags=re.S)
        assert n == 1, tab
    p.write_text(s, encoding='utf-8')
    print(f'bioquim.html: {len(TEMAS)} temas, {sum(len(t[5]) for t in TEMAS)} tarjetas')


if __name__ == '__main__':
    aplicar()
