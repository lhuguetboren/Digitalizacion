# test_run_interactive.ps1
# Lanza el modo interactivo de evaluación (con guardado automático de comentarios/notas)

Param(
    [string]$InFile = "org_dig_tools\out\agregados_all.json",
    [string]$Solucion = "org_dig_tools\plantillas\solucion.xlsx"
)

$ErrorActionPreference = "Stop"

# === Configuración ===
$OUT_DIR = "org_dig_tools\out"
$OutJson = Join-Path $OUT_DIR "evaluacion_interactive.json"
$OutCsv  = Join-Path $OUT_DIR "puntuaciones_interactive.csv"

Write-Host "===> Activando modo interactivo de evaluación" -ForegroundColor Cyan

# Verificar que org_dig_tools es importable
try {
    python -c "import org_dig_tools; print('OK: org_dig_tools importable')"
} catch {
    Write-Host "ERROR: No se pudo importar org_dig_tools. Asegúrate de que esté instalado o en tu PYTHONPATH." -ForegroundColor Red
    exit 1
}


# Crear carpeta de salida si no existe
if (-not (Test-Path $OUT_DIR)) {
    New-Item -ItemType Directory -Force -Path $OUT_DIR | Out-Null
}

Write-Host "===> Ejecutando org_dig_tools en modo interactivo..." -ForegroundColor Cyan

python -m org_dig_tools.evaluate.evaluate_org_dig_ed `
  --in $InFile `
  --out-json $OutJson `
  --out-csv $OutCsv `
  --solution-file $Solucion `
  --interactive `
  --export-diffs (Join-Path $OUT_DIR "diffs_interactive.csv")

Write-Host "===> Modo interactivo finalizado." -ForegroundColor Green
Write-Host "Comentarios guardados en la carpeta '.comments/'" -ForegroundColor Cyan
Write-Host "Resultados exportados a:" -ForegroundColor Yellow
Write-Host "  $OutJson"
Write-Host "  $OutCsv"
