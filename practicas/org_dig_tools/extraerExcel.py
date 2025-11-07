#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import pandas as pd
import json
from typing import Dict, Any, List, Optional

import os

import numpy as np
import datetime

def make_json_safe(obj):
    """
    Recorrido recursivo que convierte cualquier cosa rara (numpy, Timestamp, NaN...) 
    en tipos estándar JSON (str, float, int, None, list, dict).
    """
    # Tipos básicos OK
    if obj is None or isinstance(obj, (str, int, float, bool)):
        # Ojo: float('nan') sigue siendo float; lo dejamos tal cual porque json.dump lo serializa como NaN? 
        # No: json.dump por defecto NO permite NaN si allow_nan=False.
        # Nosotros mantenemos allow_nan=True (por defecto), así que se escribirá como NaN.
        # Si quieres estrictamente válido RFC 8259, convierte NaN a None aquí.
        if isinstance(obj, float) and (pd.isna(obj)):
            return None
        return obj

    # numpy escalares
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        # cuidado con NaN otra vez
        val = float(obj)
        if pd.isna(val):
            return None
        return val
    if isinstance(obj, (np.bool_)):
        return bool(obj)

    # pandas Timestamp / datetime / date
    if isinstance(obj, (pd.Timestamp, datetime.datetime, datetime.date)):
        # ISO 8601 string legible
        return obj.isoformat()

    # pandas NaT
    if obj is pd.NaT:
        return None

    # dict → lo limpio campo a campo
    if isinstance(obj, dict):
        return {str(k): make_json_safe(v) for k, v in obj.items()}

    # lista / tupla / set → lista JSON segura
    if isinstance(obj, (list, tuple, set)):
        return [make_json_safe(x) for x in obj]

    # cualquier otra cosa rara → str() para no romper
    return str(obj)

#ROOT_DIR = os.path.basename("/_CIN2/salidas")
#print(out)
#ROOT_DIR
#grupo=input("RUTA/A/TU/SUBDIRECTORIO","practicas/org_dig_tools")
# --- Configuración ---
# Directorio raíz a recorrer (cámbialo o pásalo por variable de entorno/argparse si lo prefieres)
#ROOT_DIR = Path(grupo)  # <-- CAMBIA ESTO
ROOT_DIR = Path("C:/Users/LlorençHuguetBoren/OneDrive - Grup STUCOM/Documentos/GitHub/Digitalizacion/practicas/org_dig_tools/_CIN1/RA1/salidas") 
# Palabras clave por categoría (en el nombre del archivo)
OPS_TOKENS = ["operations", "operaciones","operacions"]
FIN_TOKENS = ["finance", "finanzas"]

# Hojas objetivo por categoría
OPS_SHEETS = [
    "sales_orders",
    "sales_order_lines",
    "shipments",
    "shipment_lines",
    "plant_to_wh_transfers",
]

FIN_SHEETS = [
    "invoice",
    "invoice_lines",
    "payments",
    "payment_links",
]

# Nombre del JSON de salida
OUTPUT_JSON = "resumen_ultimas_filas.json"


def detectar_categoria(nombre_fichero: str) -> Optional[str]:
    """Devuelve 'operations', 'finance' o None según tokens en el nombre del archivo."""
    n = nombre_fichero.lower()
    if any(tok in n for tok in OPS_TOKENS):
        return "operations"
    if any(tok in n for tok in FIN_TOKENS):
        return "finance"
    return None


def ultima_fila_no_vacia(df: pd.DataFrame) -> Optional[Dict[str, Any]]:
    """
    Devuelve un dict con la última fila no vacía del DataFrame (o None si no hay datos).
    Incluye el índice original de la fila bajo la clave '__row_index__'.
    """
    if df is None or df.empty:
        return None
    # Eliminar filas completamente vacías
    df2 = df.dropna(how="all")
    if df2.empty:
        return None
    last_idx = df2.index[-1]
    row_dict = df2.iloc[[-1]].to_dict(orient="records")[0]
    # Convertir claves que no son str a str (por seguridad)
    row_dict = {str(k): v for k, v in row_dict.items()}
    row_dict["__row_index__"] = int(last_idx) if isinstance(last_idx, (int, float)) and not pd.isna(last_idx) else str(last_idx)
    return row_dict


def extraer_ultimas_filas_excel(xlsx_path: Path, hojas: List[str]) -> Dict[str, Any]:
    """
    Lee las hojas indicadas y devuelve un diccionario { hoja: ultima_fila_dict | 'missing' }.
    """
    resultado: Dict[str, Any] = {}
    for hoja in hojas:
        try:
            df = pd.read_excel(xlsx_path, sheet_name=hoja, engine="openpyxl")
        except ValueError as e:
            # Hoja no existe en el libro
            resultado[hoja] = {"status": "missing_sheet"}
            continue
        except Exception as e:
            # Error de lectura general del libro/hoja
            resultado[hoja] = {"status": "read_error", "error": str(e)}
            continue

        fila = ultima_fila_no_vacia(df)
        if fila is None:
            resultado[hoja] = {"status": "empty_or_all_nan"}
        else:
            resultado[hoja] = {"status": "ok", "last_row": fila}
    return resultado


def main():
    if not ROOT_DIR.exists():
        raise SystemExit(f"El directorio raíz no existe: {ROOT_DIR}")

    resumen: List[Dict[str, Any]] = []

    # Extensiones típicas de Excel
    extensiones = {".xlsx", ".xlsm", ".xlsb", ".xls"}  # .xlsb requiere engine alternativo; si falla, se informará.
    for path in ROOT_DIR.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in extensiones:
            continue

        categoria = detectar_categoria(path.name)
        if categoria is None:
            continue

        if categoria == "operations":
            hojas = OPS_SHEETS
        elif categoria == "finance":
            hojas = FIN_SHEETS
        else:
            continue

        try:
            hojas_resultado = extraer_ultimas_filas_excel(path, hojas)
        except Exception as e:
            hojas_resultado = {"__book_error__": str(e)}

        # Nombre del directorio que se está recorriendo (relativo al ROOT)
        try:
            dir_rel = str(path.parent.relative_to(ROOT_DIR))
        except ValueError:
            dir_rel = str(path.parent)

        # Registro por archivo
        resumen.append({
            "directory": dir_rel if dir_rel != "." else str(ROOT_DIR.name),
            "file": str(path.name),
            "category": categoria,
            "sheets": hojas_resultado,
        })

    # Guardar a JSON (UTF-8, legible)
    out_path = ROOT_DIR / OUTPUT_JSON
    resumen_safe = make_json_safe(resumen)    
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(resumen_safe, f, ensure_ascii=False, indent=2)

    print(f"✅ He generado el JSON con {len(resumen)} entradas: {out_path}")


if __name__ == "__main__":
    main()
