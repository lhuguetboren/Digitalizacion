Param(
    [ValidateSet("BASIC","ALL")]
    [string]$Mode = "BASIC"
)

$ErrorActionPreference = "Stop"

# === Configuración de rutas ===
$BASE_DIR   = "org_dig_tools"
$ENTREGAS   = Join-Path $BASE_DIR "entregas_2025"
$OUT_DIR    = Join-Path $BASE_DIR "out"
$PLANTILLAS = Join-Path $BASE_DIR "plantillas"
$SOLUCION   = Join-Path $PLANTILLAS "solucion.xlsx"
$SHEET_MAP  = Join-Path $PLANTILLAS "sheet_map.json"

# Crear carpeta de salida
if (-not (Test-Path $OUT_DIR)) {
    New-Item -ItemType Directory -Force -Path $OUT_DIR | Out-Null
}

Write-Host "===> Verificando que 'org_dig_tools' esté importable..." -ForegroundColor Cyan
try {
    python -c "import org_dig_tools; print('OK: org_dig_tools importable')"
} catch {
    Write-Host "ERROR: No se pudo importar 'org_dig_tools'. Asegúrate de que esté en tu PYTHONPATH o instalado (pip install -e .)" -ForegroundColor Red
    exit 1
}

switch ($Mode) {
  "BASIC" {
    Write-Host "===> MODO BASIC: extracción con --pattern 'calculadora'" -ForegroundColor Cyan
    python -m org_dig_tools.extract.extract_org_dig `
      --scan-dir "$ENTREGAS" `
      --out (Join-Path $OUT_DIR "agregados.json") `
      --sheets ORG-DIG-02 ORG-DIG-07 `
      --pattern calculadora

    Write-Host "===> Evaluación BASIC con solución externa" -ForegroundColor Cyan
    python -m org_dig_tools.evaluate.evaluate_org_dig_ed `
      --in (Join-Path $OUT_DIR "agregados.json") `
      --out-json (Join-Path $OUT_DIR "evaluacion.json") `
      --out-csv (Join-Path $OUT_DIR "puntuaciones.csv") `
      --solution-file "$SOLUCION" `
      --export-diffs (Join-Path $OUT_DIR "diffs.csv")
  }

  "ALL" {
    Write-Host "===> MODO ALL: extracción sin --pattern (incluye todos)" -ForegroundColor Cyan
    python -m org_dig_tools.extract.extract_org_dig `
      --scan-dir "$ENTREGAS" `
      --out (Join-Path $OUT_DIR "agregados_all.json") `
      --sheets ORG-DIG-02 ORG-DIG-07

    Write-Host "===> Evaluación ALL con --sheet-map" -ForegroundColor Cyan
    python -m org_dig_tools.evaluate.evaluate_org_dig_ed `
      --in (Join-Path $OUT_DIR "agregados_all.json") `
      --out-json (Join-Path $OUT_DIR "evaluacion_all.json") `
      --out-csv (Join-Path $OUT_DIR "puntuaciones_all.csv") `
      --solution-file "$SOLUCION" `
      --sheet-map "$SHEET_MAP" `
      --export-diffs (Join-Path $OUT_DIR "diffs_all.csv")
  }

  default {
    Write-Host "Uso: .\test_run.ps1 -Mode BASIC|ALL" -ForegroundColor Yellow
    exit 2
  }
}

Write-Host ("===> Listado de salidas en {0}" -f $OUT_DIR) -ForegroundColor Cyan
Get-ChildItem -Force $OUT_DIR

Write-Host "===> ¡Terminado con éxito!" -ForegroundColor Green
