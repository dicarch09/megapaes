# PAES Regular 2026 (Admisión 2027) — app de estudio express

Este archivo es la especificación del proyecto. Léelo entero al empezar cada sesión.

## Rol y forma de trabajo
- Eres ingeniero frontend y diseñador instruccional. Tú construyes; Ricardo prueba y corrige rápido. Él NO escribe código: su tiempo es para estudiar.
- Trabajas por fases. Al cerrar cada fase: commit en git, lista de "qué probar en 2 minutos" y lista de "qué quedó pendiente". Esperas su OK antes de la fase siguiente.
- Velocidad antes que pulido: la app compite con su tiempo de estudio, así que cada fase debe servir apenas se entrega.
- Honestidad: si un tema no alcanza a cubrirse bien en el tiempo, dilo y propón qué dejar fuera.
- Idioma de la app: español simple, frases cortas, sin jerga académica.

## Contexto
- Ricardo, Chile. Sabe programar (Rust, Python, TS).
- Hoy es domingo 22 de noviembre de 2026. Tiene 8 días de estudio (22 al 29) y más de 6 h diarias.
- Calendario de rendición (confirmado con DEMRE):
  - Lun 30 nov: reconocimiento de salas 12:00–13:00 · **M2 a las 15:00** (primera prueba)
  - Mar 1 dic: **Competencia Lectora 09:00** · **Ciencias Física 15:00**
  - Mié 2 dic: **M1 09:00**
- Prioridad: M2 > Física > M1 > Lenguaje.
- Nivel: M1 firme; M2 y Física débiles.

## Fuente de verdad: temarios oficiales DEMRE, Admisión 2027 (publicados el 19-03-2026)
- M2 (PDF): https://demre.cl/publicaciones/pdf/2027-26-03-19-temario-paes-regular-m2.pdf
- Ciencias (PDF): https://demre.cl/publicaciones/pdf/2027-26-03-19-temario-paes-regular-ciencias.pdf
- M1 (página): https://demre.cl/publicaciones/2027/2027-26-03-19-temario-paes-regular-m1
- Competencia Lectora (página): https://demre.cl/publicaciones/2027/2027-26-03-19-temario-paes-regular-competencia-lectora
- Contenidos nuevos 2027: https://demre.cl/noticias/2026-03-20-nuevos-contenidos-paes-regular-p2027

No inventes temas fuera del temario. Si dudas de si un tema entra, abre el PDF.

### Hallazgos clave de los temarios
- **M2:** 55 preguntas (50 cuentan para el puntaje), 2 h 20 min, 4 o 5 opciones. Incluye suficiencia de datos, con 5 opciones fijas: (1) por sí sola / (2) por sí sola / ambas juntas, (1) y (2) / cada una por sí sola, (1) o (2) / se requiere información adicional. M2 evalúa todo M1 más sus temas propios.
- **M1:** 65 preguntas, 2 h 20 min, 4 opciones.
- **Ciencias:** 80 preguntas (75 cuentan), 2 h 40 min, 4 o 5 opciones. Las primeras 54 son del Módulo Común (los 3 ejes) y las 26 siguientes del Módulo Electivo de Física. El temario NO dice cuántas preguntas del Módulo Común son de cada eje, ni qué temas de Física son solo del electivo. Por eso Física se trata como un solo bloque.
- **Competencia Lectora:** 65 preguntas, 2 h 30 min.
- **Física 2027 NO incluye** sonido ni ondas mecánicas, trabajo, energía mecánica, momentum, gravitación, calor, presión, torque, ley de Coulomb ni magnetismo. Ondas cubre solo ondas electromagnéticas. No crees contenido de esos temas.
- **Contenido nuevo en 2027** (súbelo de prioridad):
  - M2: rectas en el plano y esferas (área y volumen). M1 suma semejanza y cilindro, que también entran en M2.
  - Física: descripción del movimiento, relatividad de Galileo en MRU, MRU y MRUA (ecuación de itinerario y gráficos), modelos geocéntricos y heliocéntrico con los aportes de Galileo y Kepler, y origen del universo (Big Bang, Big Crunch y sus evidencias).
  - Biología: sistema nervioso; sexualidad y reproducción.

## Temas priorizados (aprobados en la Fase 0)
Los IDs se usan para etiquetar preguntas y guardar el dominio. Prioridad: A = aparece mucho + Ricardo débil.

### M2 (temas propios; todo M1 también puede aparecer)
| ID | Tema | Eje | Prio |
|---|---|---|---|
| m2.alg.sistemas-rectas | Rectas en el plano (nuevo) + sistemas 2×2 | Álgebra/Geometría | A |
| m2.num.log-exp | Logaritmos + función exponencial y logarítmica | Números/Álgebra | A |
| m2.pro.condicional | Probabilidad condicional | Probabilidad | A |
| m2.pro.combinatoria | Permutaciones y combinatoria | Probabilidad | A |
| m2.geo.trig-razones | Razones trigonométricas en triángulo rectángulo | Geometría | A |
| m2.pro.dispersion | Medidas de dispersión | Probabilidad | A |
| m2.sd | Suficiencia de datos (método de descarte) | Todos | A |
| m2.alg.trig-funciones | Gráficos de seno y coseno | Álgebra | B |
| m2.pro.binomial-normal | Binomial y normal | Probabilidad | B |
| m2.geo.circunferencia | Ángulos, arcos, cuerdas y secantes | Geometría | B |
| m2.geo.homotecia | Homotecia | Geometría | B |
| m2.num.financiera | Matemática financiera (AFP, créditos hipotecarios y de consumo) | Números | B |
| m2.geo.esfera | Esfera: área y volumen (nuevo, se aprende rápido) | Geometría | B |
| m2.alg.potencia | Función potencia | Álgebra | C |
| m2.num.reales | Operatoria en los reales | Números | C |
| m2.m1-dificil | M1 en versión difícil (cuadrática, semejanza, cilindro) | — | C |

### Física (Módulo Común + Electivo, un solo bloque)
| ID | Tema | Prio |
|---|---|---|
| fis.mec.cinematica | Posición, desplazamiento, rapidez, velocidad, aceleración (nuevo) | A |
| fis.mec.mru-mrua | MRU y MRUA: ecuación de itinerario y gráficos (nuevo) | A |
| fis.mec.newton | Leyes de Newton + diagrama de cuerpo libre | A |
| fis.mec.fuerzas | Peso, normal, tensión, Hooke, roce estático y cinético | A |
| fis.ond.elementos | Ondas: v = λ·f, período, amplitud | A |
| fis.ond.espejos-lentes | Espejos y lentes: formación de imágenes | A |
| fis.ele.ohm | Ley de Ohm: circuitos en serie, paralelo y mixtos | A |
| fis.ele.potencia | Potencia y energía eléctrica (P = V·I, kWh) | A |
| fis.ond.reflexion-refraccion | Reflexión, refracción, absorción, propagación rectilínea | B |
| fis.ond.espectro-color | Espectro EM (orden y usos), color y dispersión | B |
| fis.ond.doppler-interferencia | Doppler, interferencia, difracción (sin cálculos) | B |
| fis.mec.galileo | Relatividad de Galileo (nuevo) | B |
| fis.tie.tectonica | Deriva continental, tectónica de placas, sismos, interior de la Tierra | B |
| fis.mec.cosmos | Modelos del sistema solar + origen del universo (nuevo, en tarjetas) | C |
| fis.ond.dispositivos | Radar, láser, telescopios, fibra óptica, etc. | C |
| fis.ele.domiciliaria | Instalación eléctrica de la casa, consumo y eficiencia | C |

### Biología y Química (rescate, Fase 4)
Elige del temario los 10–15 temas de mayor rendimiento. Áreas de Biología: organización y actividad celular; procesos y funciones biológicas; herencia y evolución; organismo y ambiente. Áreas de Química: estructura atómica; química orgánica; reacciones químicas y estequiometría. Muéstrale la lista a Ricardo antes de escribir.

## Cómo aprende Ricardo (cada concepto en este orden)
1. **VER:** animación o forma del concepto antes de cualquier fórmula (la parábola que se mueve, el vector que se descompone, la onda que se propaga).
2. **MANIPULAR:** sliders y arrastre. Cambia un parámetro y ve el efecto en tiempo real, con la fórmula al lado actualizándose con los números.
3. **EL PORQUÉ:** derivación corta (máximo 5 pasos) de dónde sale la fórmula, en un acordeón cerrado por defecto.
4. **EJEMPLO RESUELTO** tipo PAES, mostrando un paso a la vez.
5. **PRÁCTICA** en 3 niveles (básico / PAES / difícil) con feedback inmediato. Cada alternativa incorrecta explica qué error la produce (cuál es la trampa).

## Arquitectura
```
paes27/
├─ index.html      hub: diagnósticos, ruta, dominio, repaso espaciado, ensayos, fichas
├─ m2.html         pestañas por eje; cada tema con los 5 pasos
├─ fisica.html     Mecánica · Ondas · Electricidad · Tierra y Universo
├─ bioquim.html    rescate de Biología y Química (Fase 4)
├─ m1.html         trampas + repaso rápido
├─ lenguaje.html   tipos de pregunta + práctica cronometrada
├─ lib/three.module.min.js
└─ tools/          scripts de verificación (no los usa la app)
```
- Cada HTML es autocontenido (CSS y JS inline), salvo Three.js. Sin backend, sin login, sin build step, sin CDN ni fuentes externas: todo debe funcionar offline.
- Three.js: bájalo de npm (`npm pack three`) y copia `build/three.module.min.js` a `lib/`. Cárgalo con import dinámico; si falla, la simulación cae a Canvas 2D sin romper la página.
- WebGL (Three.js) solo donde aporta: vectores y fuerzas, cinemática, óptica (rayos en espejos y lentes), ondas, cuerpos geométricos y transformaciones (esfera, homotecia). Todo lo demás va en Canvas 2D o SVG, para que cargue rápido.
- **Cómo se abre:** `python -m http.server 8000` en la carpeta y luego http://localhost:8000, siempre con el mismo puerto. Chrome bloquea los módulos ES en file://, y el localStorage depende del origen (incluido el puerto). Incluye igual exportar/importar progreso en JSON, y pon esta instrucción visible en el hub.
- Estética oscura y temática, pestañas por eje, contenido en acordeón. Atajos: 1–5 para responder, Enter para seguir.

## Contrato de datos (compartido entre páginas)
- Claves de localStorage: `paes27:diag`, `paes27:dominio`, `paes27:repaso`, `paes27:ruta`, `paes27:ensayos`.
- Formato de pregunta: `{id, prueba, eje, tema, nivel: "basico"|"paes"|"dificil", enunciado, opciones: [{texto, trampa}], correcta, explicacion}`. `tema` es un ID de las tablas de arriba.
- `dominio[tema]` va de 0 a 100, sube y baja con la práctica y pondera por nivel.
- Repaso espaciado: un tema fallado vuelve al día siguiente y a los 3 días.
- El código de progreso es el mismo bloque copiado en cada página, marcado `// == paes27-core vN ==`. Si cambia, actualízalo en todas.

## Funciones del hub (index.html)
- **Diagnóstico por prueba:** M2 15 preguntas; Ciencias 15 (11 de Física + 4 de Biología/Química, para decidir si el rescate vale la pena); M1 10; Lenguaje 6 (con un texto corto original). Cada pregunta etiquetada por eje y tema.
- **Ruta de 8 días:** bloques de 50 min + 10 min de pausa. Orden = peso del tema en la prueba × (1 − dominio) × cercanía de la fecha de esa prueba. M2 pesa más los primeros días porque se rinde primero.
- **Panel de dominio** por tema (0–100 %), que se actualiza con la práctica.
- **Modo ensayo cronometrado** con tiempos reales: M2 55 preguntas en 2 h 20 min; Ciencias 80 en 2 h 40 min; M1 65 en 2 h 20 min.
- **Ficha final** por prueba: una página con fórmulas y trampas para repasar la mañana del examen.
- Enlaces a los modelos y selecciones oficiales de DEMRE, para practicar con preguntas reales.

## Esqueleto de la ruta (el hub lo ajusta con el diagnóstico)
- Dom 22: diagnósticos + primeros temas débiles de M2.
- Lun 23 a mié 25: mañana M2; tarde Física; 30 min de Lenguaje (estrategias).
- Jue 26 y vie 27: Física y rescate de Biología/Química; M1 solo repaso de trampas.
- Sáb 28: ensayo M2 completo cronometrado + revisión de errores; en la tarde, ensayo parcial de Física.
- Dom 29: solo fichas finales y repaso espaciado. Nada nuevo.
- Entre pruebas: mar 1 en la mañana, ficha de Física; mar 1 en la noche, ficha de M1.

## Reglas de contenido
- Preguntas originales estilo PAES. M1: 4 alternativas. M2: 4 alternativas, salvo suficiencia de datos (5 fijas). Ciencias: 4 o 5.
- Calcula en código cada respuesta numérica antes de incluirla. Si una pregunta es dudosa, descártala.
- M2 incluye un mini-módulo de suficiencia de datos: método de descarte de alternativas + práctica.
- Rescate de Biología/Química: solo 10–15 temas, en formato tarjeta + 3 preguntas cada uno. Sin WebGL. Es la última prioridad de contenido.
- Lenguaje: módulo mínimo con tipos de pregunta (localizar, interpretar, evaluar), trampas típicas de las alternativas y práctica cronometrada con textos cortos originales.

## Fases
- **Fase 0: HECHA** (este archivo).
- **Fase 1 (hoy):** index.html completo (diagnósticos de las 4 pruebas, ruta, dominio, repaso, exportar/importar). Entrégalo PRIMERO y avisa, para que Ricardo haga los diagnósticos mientras sigues. Luego m2.html con 4 lecciones completas (los 5 pasos):
  1. Rectas en el plano + sistemas 2×2 (`m2.alg.sistemas-rectas`). Misma idea: dos rectas que se cortan, son paralelas o coinciden dan 1, 0 o infinitas soluciones.
  2. Logaritmos + función exponencial y logarítmica (`m2.num.log-exp`).
  3. Probabilidad condicional, con tablas de doble entrada y árbol (`m2.pro.condicional`).
  4. Trigonometría: del triángulo rectángulo a la circunferencia, y de ahí al seno y coseno (`m2.geo.trig-razones` + `m2.alg.trig-funciones`).
- **Fase 2:** resto de M2 (empieza por suficiencia de datos y combinatoria) + ensayo cronometrado de M2.
- **Fase 3:** fisica.html con las simulaciones WebGL.
- **Fase 4:** bioquim.html + m1.html (solo trampas y repaso rápido).
- **Fase 5:** lenguaje.html + fichas finales.

## Validación (antes de cerrar cada fase)
1. `tools/verificar.py` recalcula cada respuesta numérica del banco y falla si no coincide con `correcta`.
2. Un subagente revisa las preguntas nuevas sin ver tu razonamiento: que haya una sola correcta, que las trampas sean errores reales y que todo esté dentro del temario. Corrige o descarta lo que marque.
3. Cero errores de consola. Prueba con Chromium headless o Playwright si están disponibles; si no, usa `node --check` sobre el JS extraído y avísale a Ricardo qué no pudiste probar.
4. Funciona offline servido con http.server (sin pedidos a internet).
5. Cierre: commit `fase-N`, "qué probar en 2 minutos" y "pendiente".
