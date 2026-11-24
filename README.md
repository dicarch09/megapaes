# PAES 2027 · estudio express

App offline para preparar la PAES Regular 2026 (Admisión 2027). La especificación está en `CLAUDE.md`.

## Abrir

```bash
cd paes27
python -m http.server 8000
```

Luego abre http://localhost:8000. Usa siempre el puerto 8000: el progreso se guarda en el navegador, por dirección y puerto. Para respaldarlo, usa la pestaña **Progreso** del hub.

## En línea (Netlify)

`netlify.toml` ya está listo: en Netlify → *Add new site* → *Import from Git* → este repo, rama `main`. Publica solo los HTML y `lib/` (sin `tools/`). El progreso en línea se guarda en ese navegador, aparte del de localhost: usa exportar/importar para moverlo.

## Verificar (antes de cada entrega)

```bash
cd paes27
python3 tools/esquemas.py           # dibuja los esquemas de «El porqué» en cada lección
python3 tools/bioquim.py            # escribe las lecciones de Biología y Química (tarjetas) en bioquim.html (dibujos en tools/bioquim_dibujos.py)
python3 tools/m1.py                 # escribe el repaso rápido y las trampas de M1 en m1.html (dibujos en tools/m1_dibujos.py)
python3 tools/tarjetas.py           # dibuja los esquemas de las tarjetas de Física (sistema solar, dispositivos, instalación eléctrica)
python3 tools/sync_core.py          # copia el bloque compartido y los bancos a cada HTML
python3 tools/verificar.py          # recalcula cada respuesta numérica
node tools/probar.js                # consola limpia, sin internet, flujos principales (con el servidor arriba)
```
