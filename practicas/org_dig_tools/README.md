
# org_dig_tools (versión modular)

## Estructura
```
org_dig_tools/
 ├── extract/
 │   ├── __init__.py
 │   └── extract_org_dig.py
 ├── evaluate/
 │   ├── __init__.py
 │   └── evaluate_org_dig_ed.py
 ├── utils/
 │   ├── __init__.py
 │   ├── cellmap_utils.py
 │   └── solution_loader.py
 └── __init__.py
```

## 1) Extracción (por celda)
Ejemplos:
```
python -m org_dig_tools.extract.extract_org_dig \
  --scan-dir RUTA_ALUMNOS \
  --out agregados.json \
  --sheets ORG-DIG-02 ORG-DIG-07 \
  --pattern calculadora
```
o bien modo archivo único:
```
python -m org_dig_tools.extract.extract_org_dig \
  --in calculadora_IT_OT.xlsx \
  --out agregado_prueba.json \
  --sheets ORG-DIG-02 ORG-DIG-07
```

El JSON incluye `cellmap_by_sheet` por hoja para claves tipo `SHEET!B3`.

## 2) Evaluación
```
python -m org_dig_tools.evaluate.evaluate_org_dig_ed \
  --in agregados.json \
  --out-json evaluacion.json \
  --out-csv puntuaciones.csv \
  --solution-file solucion.xlsx \
  --export-diffs diffs.csv
```
- `--solution-file`: JSON/CSV/XLSX con columnas `sheet,col,row,value` (si tabular) o mapeo `{ "SHEET!B3": "SI" }` (si JSON).
- Si no se indica `--solution-file`, buscará un alumno solución por `--solution-name` dentro del agregado.

## 3) Notas/comentarios
El evaluador deja hueco para integrar el `comments_store.py` existente. Si `comments_store` está en el PYTHONPATH (p.ej. en el mismo directorio raíz), puede ampliarse el modo `--interactive`.
