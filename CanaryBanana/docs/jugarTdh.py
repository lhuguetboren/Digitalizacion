import json
from pathlib import Path

# ----------------------------------------------------------
# Determinar el directorio base del script (ejecución y debug)
# ----------------------------------------------------------
try:
    BASE_DIR = Path(__file__).parent
except NameError:
    # __file__ no existe (por ejemplo, en Jupyter / debug interactivo)
    BASE_DIR = Path.cwd()

# Archivos en el mismo directorio
input_file = BASE_DIR / "TDHSeleccionada.json"
output_file = BASE_DIR / "json_ordenado_por_fase.json"

# ----------------------------------------------------------
# Cargar el JSON
# ----------------------------------------------------------
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Manejo si el JSON es tipo dict con clave contenedora
if isinstance(data, dict):
    key = list(data.keys())[0]
    items = data[key]
else:
    items = data

# ----------------------------------------------------------
# Función para convertir Fase a número
# ----------------------------------------------------------
def fase_key(item):
    fase = item.get("Fase", "")
    if not fase:
        return 999  # Los vacíos al final
    try:
        # Permite formatos como: "Fase 3", "fase 2", "3", etc.
        return int(fase.lower().replace("fase", "").strip())
    except:
        return 999

# Ordenar por fase
items_sorted = sorted(items, key=fase_key)

# Reconstruir si era dict
if isinstance(data, dict):
    data[key] = items_sorted
    output = data
else:
    output = items_sorted

# ----------------------------------------------------------
# Guardar
# ----------------------------------------------------------
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"JSON ordenado guardado como: {output_file}")
