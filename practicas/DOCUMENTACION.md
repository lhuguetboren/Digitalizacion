# Documentación general de `org_dig_tools`

## Visión general
La aplicación proporciona una cadena de herramientas en Python para corregir planillas del área de Organización Digital. El flujo típico consta de dos etapas:

1. **Extracción (`org_dig_tools.extract`)**: recorre archivos Excel entregados por el alumnado y genera un JSON agregado con los valores relevantes.
2. **Evaluación (`org_dig_tools.evaluate`)**: compara las respuestas extraídas contra una plantilla de solución, calcula métricas por estudiante y produce reportes JSON/CSV. Opcionalmente permite una revisión interactiva con comentarios persistentes.

La lógica compartida reside en `org_dig_tools.utils`, que provee utilidades para generar claves de celda, normalizar valores y cargar soluciones externas.

```
org_dig_tools/
 ├── extract/
 │   └── extract_org_dig.py
 ├── evaluate/
 │   └── evaluate_org_dig_ed.py
 ├── utils/
 │   ├── cellmap_utils.py
 │   └── solution_loader.py
 └── plantillas/
     ├── sheet_map.json
     └── solucion.xlsx
```

> Requisito principal: `pandas` es necesario para leer y escribir archivos tabulares (Excel/CSV).【F:org_dig_tools/extract/extract_org_dig.py†L7-L10】【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L323-L333】

---

## Módulo de extracción (`extract/extract_org_dig.py`)

### Propósito
Leer hojas específicas de planillas Excel (por defecto `ORG-DIG-02` y `ORG-DIG-07`) y producir un agregado JSON con toda la información relevante para la evaluación posterior.【F:org_dig_tools/extract/extract_org_dig.py†L12-L100】

### Flujo
1. **Entrada**
   - *Modo carpeta (`--scan-dir` + `--pattern`)*: explora subdirectorios (uno por estudiante) y selecciona el primer Excel cuyo nombre contenga la subcadena indicada.【F:org_dig_tools/extract/extract_org_dig.py†L65-L87】
   - *Modo archivo único (`--in`)*: procesa un único Excel de prueba o depuración.【F:org_dig_tools/extract/extract_org_dig.py†L52-L64】

2. **Lectura de celdas** (`read_excel_blocks`)
   - Divide cada hoja en dos bloques: `bloque_tabla` (filas 1-19, columnas B-D) y `bloque_unicos` (filas restantes). Cada fila guarda el valor de las columnas B, C, D junto a metadatos como número de fila y referencias A1.【F:org_dig_tools/extract/extract_org_dig.py†L14-L48】
   - Construye `cellmap_by_sheet`, un diccionario plano con claves `HOJA!COLUMNAFILA` (ej.: `ORG-DIG-02!B3`).【F:org_dig_tools/extract/extract_org_dig.py†L34-L48】

3. **Salida** (`build_aggregate`)
   - Devuelve un diccionario con tres secciones: `students` (metadatos y ruta del Excel), `extracted` (datos por estudiante) y `summary` (número de estudiantes y hojas procesadas).【F:org_dig_tools/extract/extract_org_dig.py†L88-L108】
   - El comando CLI guarda este JSON mediante `--out` y muestra una confirmación en consola.【F:org_dig_tools/extract/extract_org_dig.py†L110-L123】

### Uso típico
```bash
python -m org_dig_tools.extract.extract_org_dig \
  --scan-dir ENTREGAS/ \
  --out agregados.json \
  --sheets ORG-DIG-02 ORG-DIG-07 \
  --pattern calculadora
```

---

## Módulo de evaluación (`evaluate/evaluate_org_dig_ed.py`)

### Propósito
Transformar el JSON agregado en reportes de corrección. Construye un mapa de respuestas por estudiante, lo compara con la solución esperada y exporta resultados. Opcionalmente añade flujo interactivo para revisar manualmente comentarios y notas.【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L223-L344】

### Componentes clave
- **`CommentsStore`**: persiste comentarios/nota en archivos JSON individuales dentro de `--comments-dir`. Se usa durante el modo interactivo para mantener anotaciones entre ejecuciones.【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L8-L28】【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L166-L221】
- **`build_student_cellmap`**: normaliza la estructura `extracted` para soportar tanto `cellmap_by_sheet` plano como anidado por hoja, consolidando todas las entradas en claves `HOJA!A1`.【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L34-L64】
- **`choose_solution_from_aggregate`**: selecciona la respuesta canónica dentro del propio agregado cuando no se suministra un archivo de solución externo.【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L68-L82】
- **`compare`**: realiza la comparación clave a clave tras normalizar valores (`SI/NO`, espacios). Devuelve listas de coincidencias y penalizaciones.【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L84-L96】【F:org_dig_tools/utils/cellmap_utils.py†L5-L16】
- **`export_diffs_csv`**: exporta discrepancias por alumno a CSV, con `pandas` opcional y `fallback` manual.【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L98-L115】
- **`interactive_loop`**: interfaz de texto para navegar estudiantes, editar comentarios/notas y reescribir reportes bajo demanda.【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L166-L221】

### Flujo de `main`
1. **Cargar agregado** (`--in`).【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L224-L235】
2. **Construir solución**:
   - Desde archivo externo (`--solution-file`), admitiendo formatos JSON o tabulares (CSV/XLSX).【F:org_dig_tools/utils/solution_loader.py†L5-L52】
   - O a partir de un alumno canónico dentro del agregado (`--solution-name`).【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L236-L249】
3. **Evaluar estudiantes**: genera reportes individuales con métricas (`score`, `num_matches`, `num_penalties`) y listas de coincidencias/discrepancias. La puntuación es `matches / (matches + penalties)`.【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L251-L292】
4. **Exportar resultados**: escribe JSON completo (`--out-json`) y CSV resumido (`--out-csv`). Si se solicitaron diferencias (`--export-diffs`), genera un archivo por alumno o agrega sufijos según corresponda.【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L282-L333】
5. **Modo interactivo (`--interactive`)**: permite revisión manual con persistencia de comentarios/nota usando `CommentsStore`. Escribe los archivos tras cada modificación y al salir.【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L339-L344】

### Uso típico
```bash
python -m org_dig_tools.evaluate.evaluate_org_dig_ed \
  --in agregados.json \
  --out-json evaluacion.json \
  --out-csv puntuaciones.csv \
  --solution-file plantillas/solucion.xlsx \
  --export-diffs diffs/
```

---

## Utilidades comunes (`utils`)

- **`cellmap_utils.make_cell_key(sheet, col, row)`**: genera claves `HOJA!COLFILA` normalizando la columna en mayúsculas.【F:org_dig_tools/utils/cellmap_utils.py†L1-L4】
- **`cellmap_utils.normalize_value(value)`**: estandariza cadenas, transformando variantes de `SI`/`SÍ` y `NO` a formas canónicas y recortando espacios.【F:org_dig_tools/utils/cellmap_utils.py†L6-L15】
- **`solution_loader.load_solution_map(path)`**: carga la solución esperada desde JSON o desde archivos tabulares (CSV/TSV/XLSX/XLS) con columnas `sheet`, `col`, `row`, `value`, construyendo el mapa `HOJA!COLFILA` necesario para la comparación.【F:org_dig_tools/utils/solution_loader.py†L5-L52】

---

## Artefactos de soporte (`plantillas/`)
- `solucion.xlsx`: plantilla de referencia que puede usarse con `--solution-file`.
- `sheet_map.json`: ejemplo de mapa con equivalencias de celdas.

Estos recursos sirven como guía para preparar archivos de solución y comprender la estructura esperada por las herramientas.

---

## Consideraciones y extensiones
- **Dependencias**: se recomienda un entorno con `pandas` para aprovechar la exportación directa a CSV/XLSX. El código ofrece alternativas manuales cuando no está disponible, pero la extracción requiere `pandas` obligatoriamente.【F:org_dig_tools/extract/extract_org_dig.py†L7-L10】【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L323-L333】
- **Persistencia de comentarios**: la clase `CommentsStore` escribe archivos JSON por estudiante en un directorio configurable, permitiendo que las notas queden guardadas entre sesiones. Se puede reemplazar o extender para integrarlo con otras plataformas de seguimiento.【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L8-L28】【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L166-L221】
- **Pruebas rápidas**: el flag `--in` del extractor facilita procesar un archivo aislado para validar la configuración antes de ejecutar sobre todas las entregas.【F:org_dig_tools/extract/extract_org_dig.py†L110-L123】

---

## Resumen de CLI
| Etapa | Comando base | Entradas clave | Salidas principales |
|-------|---------------|----------------|--------------------|
| Extracción | `python -m org_dig_tools.extract.extract_org_dig` | `--scan-dir` / `--in`, `--sheets`, `--pattern` | JSON agregado (`--out`) |
| Evaluación | `python -m org_dig_tools.evaluate.evaluate_org_dig_ed` | `--in`, `--solution-file` o `--solution-name`, `--export-diffs` | Reporte JSON (`--out-json`), CSV de puntuaciones (`--out-csv`), CSVs de diferencias opcionales |

Con esta documentación se cubre el flujo completo desde la extracción de datos en bruto hasta la evaluación automatizada y revisión manual, permitiendo a nuevas personas en el proyecto comprender rápidamente la arquitectura y los puntos de extensión.
