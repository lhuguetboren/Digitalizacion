# Evaluador ORG-DIG por celda

Este módulo proporciona el comando `python -m org_dig_tools.evaluate.evaluate_org_dig_ed` para calificar planillas extraídas por `org_dig_tools.extract`. El flujo recorre un JSON agregado de respuestas por alumno, construye un mapa de celdas comparable con la solución esperada y genera reportes automáticos en JSON y CSV, con soporte opcional para un modo interactivo de revisión y comentarios persistentes.

## Entradas esperadas
- **Agregado (`--in`)**: archivo JSON que contiene las llaves `students` y `extracted`. Cada entrada de `extracted` puede incluir `cellmap_by_sheet` en la raíz o en cada hoja; el evaluador normaliza ambas variantes para construir un mapa `HOJA!A1` uniforme.【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L34-L64】
- **Solución**: por defecto se busca un alumno cuyo nombre contenga la subcadena `--solution-name`. Alternativamente puede suministrarse un archivo externo mediante `--solution-file` (JSON, CSV o XLSX con columnas `sheet`, `col`, `row`, `value`).【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L236-L249】【F:org_dig_tools/utils/solution_loader.py†L5-L52】

## Salidas
El comando siempre escribe dos artefactos principales:
- **JSON (`--out-json`)**: incluye un resumen con la solución utilizada más un arreglo de reportes individuales con coincidencias, diferencias y métricas agregadas por alumno.【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L313-L344】
- **CSV (`--out-csv`)**: tabla simple con `alumno`, `score`, `num_matches`, `num_penalties` y `nota` (si se encuentra disponible). Cuando la biblioteca `pandas` está instalada se usa para la exportación, con un `fallback` manual en caso contrario.【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L323-L333】

Opcionalmente se pueden escribir CSV adicionales con las discrepancias por alumno mediante `--export-diffs`. El archivo de destino puede ser un directorio (crea un CSV por alumno) o una ruta concreta, en cuyo caso se agrega el nombre del estudiante antes de la extensión.【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L282-L293】

## Métrica de comparación
La comparación se realiza clave por clave tras normalizar los valores (`SI`/`NO`, espacios). El puntaje se calcula como la proporción de coincidencias sobre el total de claves evaluadas.【F:org_dig_tools/utils/cellmap_utils.py†L5-L16】【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L84-L96】【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L260-L292】

## Comentarios y notas
El script incorpora una clase `CommentsStore` que persiste comentarios y notas en archivos JSON por alumno dentro del directorio `--comments-dir` (por defecto `.comments`). Los campos `comentario_general` y `nota` de cada reporte se rellenan automáticamente con los valores almacenados y se sincronizan tras cada edición.【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L8-L28】【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L294-L333】 Si se habilita `--interactive`, la consola permite navegar entre alumnos, editar comentarios/notas y reescribir las salidas tras cada cambio.【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L166-L344】

## Ejemplo de uso
```bash
python -m org_dig_tools.evaluate.evaluate_org_dig_ed \
  --in agregados.json \
  --out-json evaluacion.json \
  --out-csv puntuaciones.csv \
  --solution-file solucion.xlsx \
  --export-diffs diffs/
```

## Notas adicionales
La herramienta se centra exclusivamente en las claves `HOJA!A1`, por lo que no es necesario configurar flags adicionales para forzar ese comportamiento.【F:org_dig_tools/evaluate/evaluate_org_dig_ed.py†L34-L115】
