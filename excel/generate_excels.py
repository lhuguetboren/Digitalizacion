# generate_excels.py
from pathlib import Path
import os
import shutil
import time
import uuid

from excel_models import build_master, build_operations, build_finance

ROOT = Path(__file__).parent
OUT_DIR = ROOT / "excel"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def _atomic_replace(src: Path, dst: Path):
    """
    Reemplazo atómico y compatible con Windows.
    Si dst existe y está bloqueado, intenta varios reintentos cortos.
    """
    tries = 5
    last_err = None
    for i in range(tries):
        try:
            # En Windows, os.replace es atómico y reemplaza si existe
            os.replace(str(src), str(dst))
            return
        except PermissionError as e:
            last_err = e
            time.sleep(0.4 * (i + 1))
    # Si sigue bloqueado, intentamos renombrar el destino para no perder el resultado
    try:
        backup = dst.with_name(dst.stem + "_locked_" + str(int(time.time())) + dst.suffix)
        dst.rename(backup)
        os.replace(str(src), str(dst))
        print(f"[WARN] {dst.name} estaba bloqueado. Se guardó backup: {backup.name}")
    except Exception as e2:
        # Como último recurso dejamos el temporal al lado con nombre legible
        failed = dst.with_name(dst.stem + "_NEW_" + str(int(time.time())) + dst.suffix)
        shutil.move(str(src), str(failed))
        raise PermissionError(
            f"No se pudo reemplazar {dst.name}. Archivo nuevo guardado como {failed.name}. "
            f"Cierra Excel/pausa OneDrive y renómbralo manualmente."
        ) from (last_err or e2)

def _safe_build(builder_func, final_path: Path, include_demo: bool = True):
    """
    Construye el Excel en un archivo temporal en la misma carpeta y luego lo reemplaza.
    Evita PermissionError por bloqueos de Excel/OneDrive.
    """
    final_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_name = final_path.with_name(f".tmp_{final_path.stem}_{uuid.uuid4().hex}.xlsx")
    # Genera el archivo temporal
    builder_func(str(tmp_name), include_demo=include_demo)
    # Reemplaza el destino
    _atomic_replace(tmp_name, final_path)

def main():
    master = OUT_DIR / "master_data.xlsx"
    ops    = OUT_DIR / "operations.xlsx"
    fin    = OUT_DIR / "finance.xlsx"

    print("[1/3] Generando master_data.xlsx ...")
    _safe_build(build_master, master, include_demo=True)

    print("[2/3] Generando operations.xlsx ...")
    _safe_build(build_operations, ops, include_demo=True)

    print("[3/3] Generando finance.xlsx ...")
    _safe_build(build_finance, fin, include_demo=True)

    print("✅ Archivos generados en:", OUT_DIR.resolve())

if __name__ == "__main__":
    main()
