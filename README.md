# PAES 2027 · estudio express

App offline para preparar la PAES Regular 2026 (Admisión 2027). La especificación está en `CLAUDE.md`.

## Abrir

```bash
cd paes27
python -m http.server 8000
```

Luego abre http://localhost:8000. Usa siempre el puerto 8000: el progreso se guarda en el navegador, por dirección y puerto. Para respaldarlo, usa la pestaña **Progreso** del hub.

## Verificar (antes de cada entrega)

```bash
cd paes27
python3 tools/sync_core.py          # copia el bloque compartido y los bancos a cada HTML
python3 tools/verificar.py          # recalcula cada respuesta numérica
node tools/probar.js                # consola limpia, sin internet, flujos principales (con el servidor arriba)
```
