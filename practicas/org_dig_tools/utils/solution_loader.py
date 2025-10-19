
from pathlib import Path
import json

from .cellmap_utils import column_index_to_letter

def _normalize_column_identifier(value) -> str:
    """Acepta letras ("C") o índices (3) y devuelve la letra de columna en mayúsculas."""
    if value is None:
        raise ValueError("Columna de la solución no puede ser vacía")

    # valores numéricos reales (int/float)
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        idx = int(value)
        if idx != value and not (isinstance(value, float) and value.is_integer()):
            raise ValueError(f"El índice de columna debe ser entero: {value!r}")
        return column_index_to_letter(idx)

    # cadenas -> intentar letras directas o números representados como texto
    if isinstance(value, str):
        raw = value.strip()
        if raw == "":
            raise ValueError("Columna de la solución no puede ser vacía")
        # admitir formatos tipo "3", "3.0", "003"
        try:
            as_float = float(raw.replace(",", "."))
            if as_float.is_integer():
                return column_index_to_letter(int(as_float))
        except ValueError:
            pass
        return raw.upper()

    raise TypeError(f"Tipo de columna no soportado: {type(value)!r}")

def load_solution_map(pathlike):
    """
    Load a solution map with keys like "SHEET!B3" -> "SI".
    Supported formats:
      - .json: object mapping of the above format
      - .csv/.xlsx: requires columns: sheet, col, row, value
    """
    path = Path(pathlike)
    ext = path.suffix.lower()
    if ext == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("JSON de solución debe ser un objeto clave->valor")
        return {str(k): v for k, v in data.items()}
    try:
        import pandas as pd
    except Exception as e:
        raise RuntimeError("Pandas es necesario para leer CSV/XLSX") from e

    if ext in (".csv", ".tsv"):
        sep = "," if ext == ".csv" else "\t"
        df = pd.read_csv(path, sep=sep)
    elif ext in (".xlsx", ".xls"):
        df = pd.read_excel(path)
    else:
        raise ValueError(f"Formato de solución no soportado: {ext}")

    required = {"sheet", "col", "row", "value"}
    if not required.issubset(set(map(str.lower, df.columns))):
        # try to normalize columns
        cols = {c.lower(): c for c in df.columns}
        missing = required - set(cols.keys())
        if missing:
            raise ValueError(f"Faltan columnas en solución tabular: {', '.join(sorted(missing))}")
        df = df.rename(columns={cols['sheet']:'sheet', cols['col']:'col', cols['row']:'row', cols['value']:'value'})

    m = {}
    for _, r in df.iterrows():
        sheet = str(r['sheet']).strip()
        col = _normalize_column_identifier(r['col'])
        
        try:
            row = int(r['row'])
        except Exception:
            # allow "3.0" etc.
            row = int(float(r['row']))
        key = f"{sheet}!{col}{row}"
        m[key] = r['value']
    return m
