
import json
from pathlib import Path
import argparse

try:
    import pandas as pd
except Exception as e:
    raise RuntimeError("Se requiere pandas para extraer datos de Excel") from e

from ..utils.cellmap_utils import make_cell_key

DEFAULT_SHEETS = ["ORG-DIG-02", "ORG-DIG-07"]

def read_excel_blocks(path: Path, sheets):
    """
    Lee cada hoja en dos bloques: bloque_tabla (filas 0..18, B-D) y bloque_unicos (desde la 19).
    Anota row_excel y cells (B/C/D).
    Devuelve dict: { sheet: { bloque_tabla: [...], bloque_unicos: [...], cellmap_by_sheet: {SHEET: {SHEET!B5: value, ...}} } }
    """
    xl = pd.ExcelFile(path)
    out = {}

    for sheet in sheets:
        if sheet not in xl.sheet_names:
            continue
        df = xl.parse(sheet, header=None)  # sin encabezados, trabajamos por posición

        # bloque_tabla: filas 0..18, columnas B-D => indices (0..18, 1..3)
        bloque_tabla = []
        for i in range(0, min(19, len(df))):
            row_excel = i + 1  # 1-based para Excel
            a = df.iat[i, 0] if df.shape[1] > 0 else None
            b = df.iat[i, 1] if df.shape[1] > 1 else None
            c = df.iat[i, 2] if df.shape[1] > 2 else None
            d = df.iat[i, 3] if df.shape[1] > 3 else None
            bloque_tabla.append({
                "grupo": a, "b": b, "c": c, "d": d,
                "row_excel": row_excel,
                "cells": {"B": f"B{row_excel}", "C": f"C{row_excel}", "D": f"D{row_excel}"}
            })

        # bloque_unicos: desde fila 19 en adelante (posición 19 -> Excel 20)
        bloque_unicos = []
        for i in range(19, len(df)):
            row_excel = i + 1
            a = df.iat[i, 0] if df.shape[1] > 0 else None
            b = df.iat[i, 1] if df.shape[1] > 1 else None
            c = df.iat[i, 2] if df.shape[1] > 2 else None
            d = df.iat[i, 3] if df.shape[1] > 3 else None
            bloque_unicos.append({
                "grupo": a, "b": b, "c": c, "d": d,
                "row_excel": row_excel,
                "cells": {"B": f"B{row_excel}", "C": f"C{row_excel}", "D": f"D{row_excel}"}
            })

        # Construir cellmap_by_sheet (SHEET!B3 -> valor)
        cellmap = {}
        def add_cell(col_letter, value, row_excel):
            if value is None or (isinstance(value, float) and pd.isna(value)):
                return
            key = make_cell_key(sheet, col_letter, row_excel)
            cellmap[key] = value

        for r in bloque_tabla:
            re = r["row_excel"]
            for L in ("B","C","D"):
                add_cell(L, r.get(L.lower()), re)

        for r in bloque_unicos:
            re = r["row_excel"]
            for L in ("B","C","D"):
                add_cell(L, r.get(L.lower()), re)

        out[sheet] = {
            "bloque_tabla": bloque_tabla,
            "bloque_unicos": bloque_unicos,
            "cellmap_by_sheet": {sheet: cellmap}
        }
    return out

def scan_students(scan_dir: Path, pattern: str):
    """
    Recorre subcarpetas de scan_dir. Por cada subcarpeta, busca un archivo Excel cuyo nombre contenga 'pattern'.
    Devuelve lista de dicts con {name, excel_path}.
    """
    students = []
    for entry in sorted(scan_dir.iterdir()):
        print(entry)
        if not entry.is_dir():
            continue
        name = entry.name
        # buscar primer excel que contenga pattern
        excel = None
        for f in entry.iterdir():
            if f.is_file() and pattern.lower() in f.name.lower() and f.suffix.lower() in (".xlsx",".xls"):
                excel = f
                break
        if excel:
            students.append({"name": name, "excel_path": str(excel)})
    return students

def build_aggregate(scan_dir=None, in_file=None, sheets=None, pattern="calculadora"):
    sheets = sheets or DEFAULT_SHEETS
    if in_file:
        p = Path(in_file)
        ext = p.suffix.lower()
        if ext not in (".xlsx", ".xls"):
            raise ValueError("El archivo de entrada debe ser .xlsx/.xls")
        extracted = read_excel_blocks(p, sheets)
        students = [{"name": p.stem, "excel_path": str(p)}]
    else:
        scan = Path(scan_dir)
        print(scan)
        studs = scan_students(scan, pattern)
        students = studs
        extracted = {}
        for s in students:
            p = Path(s["excel_path"])
            try:
                ex = read_excel_blocks(p, sheets)
            except Exception as e:
                ex = {"__error__": str(e)}
            extracted[s["name"]] = ex

    summary = {
        "num_students": len(students),
        "sheets": sheets,
    }
    return {
        "students": students,
        "extracted": extracted,
        "summary": summary
    }

def main():
    ap = argparse.ArgumentParser(description="Extracción ORG-DIG con cellmap por celda")
    ap.add_argument("--scan-dir", help="Directorio con subcarpetas por alumno")
    ap.add_argument("--in", dest="in_file", help="Archivo Excel único para prueba")
    ap.add_argument("--out", required=True, help="JSON de salida")
    ap.add_argument("--sheets", nargs="+", default=DEFAULT_SHEETS, help="Hojas a procesar")
    ap.add_argument("--pattern", default="calculadora", help="Subcadena para localizar el Excel por alumno")
    args = ap.parse_args()

    if not args.in_file and not args.scan_dir:
        ap.error("Debes indicar --in o --scan-dir")
    print(args.scan_dir)
    data = build_aggregate(scan_dir=args.scan_dir, in_file=args.in_file, sheets=args.sheets, pattern=args.pattern)
    Path(args.out).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] Escrito {args.out}")

if __name__ == "__main__":
    main()
