
def make_cell_key(sheet: str, col: str, row: int) -> str:
    return f"{sheet}!{col.upper()}{int(row)}"

def column_index_to_letter(idx: int) -> str:
    """Convierte un índice de columna (1=A) a su letra correspondiente."""
    if not isinstance(idx, int):
        raise TypeError("idx debe ser entero")
    if idx <= 0:
        raise ValueError("El índice de columna debe ser >= 1")

    letters = []
    current = idx
    while current > 0:
        current, remainder = divmod(current - 1, 26)
        letters.append(chr(ord("A") + remainder))
    return "".join(reversed(letters))
def normalize_value(v):
    """Pequeña normalización para comparar: quita espacios extremos y homogeniza mayúsculas para 'SI/NO'."""
    if v is None:
        return None
    if isinstance(v, str):
        s = v.strip()
        if s.upper() in ("SI", "SÍ"):
            return "SI"
        if s.upper() == "NO":
            return "NO"
        return s
    return v
