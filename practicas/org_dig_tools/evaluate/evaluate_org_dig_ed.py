import json
from pathlib import Path
import argparse
import sys
from ..utils.cellmap_utils import normalize_value
from ..utils.solution_loader import load_solution_map
import re

class CommentsStore:
    def __init__(self, base_dir=".comments", read_only=False):
        self.base = Path(base_dir)
        self.base.mkdir(parents=True, exist_ok=True)
        self.read_only = read_only

    def _path(self, student_id: str) -> Path:
        return self.base / f"{student_id}.json"

    def get_comment(self, student_id: str) -> dict:
        p = self._path(student_id)
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
        return {"comment": "", "score": None}

    def set_comment(self, student_id: str, comment: str, score: float | None):
        if self.read_only:
            return False
        payload = {"comment": comment, "score": score}
        self._path(student_id).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return True


# --- helpers ---
COL_A1_RE = re.compile(r'^(?P<sheet>[^!]+)!(?P<col>[A-Z]+)(?P<row>\d+)$')

def col_to_index(col: str) -> int:
    """Convierte 'A'→1, 'B'→2, ..., 'Z'→26, 'AA'→27, etc."""
    n = 0
    for ch in col:
        n = n*26 + (ord(ch) - ord('A') + 1)
    return n

def parse_key(key: str):
    """
    Devuelve (sheet, row, col_index, col_str) para ordenar por:
    1) hoja, 2) fila numérica, 3) columna (A1).
    """
    m = COL_A1_RE.match(key)
    if not m:
        # fallback si el formato no es el esperado
        return (key, float('inf'), float('inf'), key)
    sheet = m.group('sheet')
    col = m.group('col')
    row = int(m.group('row'))
    return (sheet, row, col_to_index(col), col)

# --- deduplicación ---
def dedupe_penalties(penalties, by=("key",)): 
    """
    Quita duplicados. Por defecto, único por 'key' (conserva la primera ocurrencia).
    Si quieres deduplicar por combinación exacta usa by=("key","expected","student").
    """
    seen = set()
    out = []
    for it in penalties:
        k = tuple(it.get(f) for f in by)
        if k in seen:
            continue
        seen.add(k)
        out.append(it)
    return out


def load_aggregate(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def build_student_cellmap(extracted_for_student):
    """Devuelve un mapa {"SHEET!B3": valor} a partir de los datos extraídos."""
    cell_key_map = {}
    if not isinstance(extracted_for_student, dict):
        return cell_key_map

    def _collect(sheet_name: str, sheet_map):
        if not isinstance(sheet_map, dict):
            return
        for cell_ref, value in sheet_map.items():
            if not isinstance(cell_ref, str):
                continue
            if "!" in cell_ref:
                key = cell_ref
            else:
                key = f"{sheet_name}!{cell_ref}"
            cell_key_map[key] = value

    top_level_cms = extracted_for_student.get("cellmap_by_sheet")
    if isinstance(top_level_cms, dict):
        for sheet_name, sheet_map in top_level_cms.items():
            _collect(sheet_name, sheet_map)

    for sheet, payload in extracted_for_student.items():
        if sheet == "__error__" or not isinstance(payload, dict):
            continue
        cms = payload.get("cellmap_by_sheet")
        if isinstance(cms, dict):
            for inner_sheet, sheet_map in cms.items():
                target_sheet = inner_sheet if isinstance(inner_sheet, str) else sheet
                _collect(target_sheet, sheet_map)

    return cell_key_map

def choose_solution_from_aggregate(agg, solution_name_substring):
    for stu in agg["students"]:
        name = stu["name"]
        if solution_name_substring.lower() in name.lower():
            # buscar la sección de extracted correspondiente
            extracted_for_student = agg["extracted"].get(name)
            if extracted_for_student:
                return name, extracted_for_student
    # fallback: primer alumno con datos
    for stu in agg["students"]:
        name = stu["name"]
        ex = agg["extracted"].get(name)
        if ex and isinstance(ex, dict):
            return name, ex
    return None, None

def compare(student_map, solution_map):
    """Comparación por keys exactas (ya normalizadas); devuelve matches y penalties (listas de dicts)."""
    matches, penalties = [], []
    # union de claves
    all_keys = set(student_map.keys()) | set(solution_map.keys())
    for k in sorted(all_keys):
        sv = normalize_value(student_map.get(k))
        ev = normalize_value(solution_map.get(k))
        if sv == ev:
            matches.append({"key": k, "student": sv, "expected": ev})
        else:
            penalties.append({"key": k, "student": sv, "expected": ev})
    return matches, penalties

def export_diffs_csv(path, alumno, penalties_or_matches):
    try:
        import pandas as pd
    except Exception:
        # fallback a CSV manual
        import csv
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["alumno","key","expected","student"])
            for r in penalties_or_matches:
                w.writerow([alumno, r["key"], r.get("expected"), r.get("student")])
        return
    rows = []
    for r in penalties_or_matches:
        rows.append({"alumno": alumno, "key": r["key"], "expected": r.get("expected"), "student": r.get("student")})
    import pandas as pd
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)

# --------------------------
#   INTERACTIVO REAL
# --------------------------
def _get_student_id_from_report(rep: dict) -> str:
    # usamos el nombre como ID estable por defecto
    return str(rep.get("alumno") or "unknown")

def _load_existing_comment(store, student_id: str):
    try:
        data = store.get_comment(student_id) if store else None
        if isinstance(data, dict):
            return data.get("comment", ""), data.get("score", None)
    except Exception:
        pass
    return "", None

def _edit_comment_and_score(store, rep: dict):
    sid = _get_student_id_from_report(rep)
    prev_comment, prev_score = _load_existing_comment(store, sid)
    print("\n--- Edición de comentario/nota ---")
    print("(Enter para mantener el valor actual)")
    print(f"Comentario actual: {prev_comment!r}")
    new_comment = input("Nuevo comentario: ").strip()
    if not new_comment:
        new_comment = prev_comment

    print(f"Nota actual: {prev_score!r}")
    raw = input("Nueva nota (número o vacío): ").strip()
    if raw == "":
        new_score = prev_score
    else:
        try:
            new_score = float(raw.replace(",", "."))
        except Exception:
            print("⚠  Valor de nota inválido. Se mantiene la nota anterior.")
            new_score = prev_score

    if store:
        ok = store.set_comment(sid, new_comment, new_score)
        print("✅ Guardado" if ok else "⚠ No se pudo guardar (¿read_only?)")
    else:
        print("⚠ comments_store no disponible: modo stub (no persiste).")

    # reflejar también en el reporte en memoria si existen esos campos
    if "comentario_general" in rep:
        rep["comentario_general"] = new_comment
    if "nota" in rep:
        rep["nota"] = new_score

def interactive_loop(reports: list, store, rewrite_outputs_cb):
    """
    reports: lista de dicts por alumno (ya calculados)
    store: instancia de CommentsStore (o None)
    rewrite_outputs_cb: callback para re-volcar JSON/CSV tras cambios
    """
    idx = 0
    total = len(reports)
    if total == 0:
        print("No hay alumnos para revisar.")
        return

    while True:
        rep = reports[idx]
        sid = _get_student_id_from_report(rep)
        # mostrar cabecera + estado actual
        print("\n" + "="*72)
        print(f"[{idx+1}/{total}] Alumno: {sid}")
        print("-"*72)
        if store:
            c0, s0 = _load_existing_comment(store, sid)
            print(f"Comentario actual: {c0!r}")
            print(f"Nota actual     : {s0!r}")
        else:
            print("comments_store no disponible (los cambios no se guardarán).")

        num_matches = rep.get("num_matches", 0)
        num_penalties = rep.get("num_penalties", 0)
        print(f"Coincidencias : {num_matches}")
        print(f"Penalizaciones: {num_penalties}")

        penalties = rep.get("penalties") or []

        # --- uso ---
        penalties_dedup = dedupe_penalties(penalties, by=("key",))  # o ("key","expected","student")
        penalties_sorted = sorted(penalties_dedup, key=lambda it: parse_key(it["key"]))

        # --- impresión ---

        if penalties:
            print("\nPenalizaciones detectadas (clave · esperado · alumno):")
            for item in penalties_sorted:
                key = item.get("key")
                expected = item.get("expected")
                student_val = item.get("student")
                print(f" - {key}: {expected!r} ←→ {student_val!r}")
        else:
            print("\nSin penalizaciones registradas.")

        print("\nAcciones: [n] siguiente  [p] anterior  [e] editar comentario/nota  [w] escribir salidas  [q] salir")
        cmd = input("> ").strip().lower()
        if cmd == "q":
            # última escritura de cortesía
            try:
                rewrite_outputs_cb()
            except Exception:
                pass
            print("Saliendo…")
            break
        elif cmd == "n":
            idx = (idx + 1) % total
        elif cmd == "p":
            idx = (idx - 1) % total
        elif cmd == "e":
            _edit_comment_and_score(store, rep)
            # re-volcar salidas tras cada edición para no perder cambios
            try:
                rewrite_outputs_cb()
            except Exception as e:
                print(f"⚠ No se pudo re-escribir salidas: {e}")
        elif cmd == "w":
            try:
                rewrite_outputs_cb()
                print("✅ Salidas reescritas.")
            except Exception as e:
                print(f"⚠ No se pudo re-escribir salidas: {e}")
        else:
            print("Comando no reconocido.")

def main():
    ap = argparse.ArgumentParser(description="Evaluación ORG-DIG por celda")
    ap.add_argument("--in", dest="in_file", required=True, help="JSON agregado (salida del extractor)")
    ap.add_argument("--out-json", required=True, help="Ruta JSON de evaluación")
    ap.add_argument("--out-csv", required=True, help="Ruta CSV de puntuaciones")
    ap.add_argument("--solution-name", default="solucion", help="Subcadena para buscar alumno canónico dentro del agregado")
    ap.add_argument("--solution-file", help="Ruta a solución externa (JSON/CSV/XLSX)")
    ap.add_argument("--export-diffs", help="Ruta CSV opcional para exportar diferencias por alumno")
    ap.add_argument("--interactive", action="store_true", help="Modo interactivo para anotar comentarios y notas")
    ap.add_argument("--comments-dir", default=".comments", help="Directorio donde se guardan comentarios/nota (default: .comments)")
    args = ap.parse_args()

    agg = load_aggregate(args.in_file)

    # Preparar mapa de solución
    solution_label = None
    if args.solution_file:
        solution_map = load_solution_map(args.solution_file)
        solution_label = Path(args.solution_file).name
    else:
        # elegir dentro del agregado
        sol_name, sol_extracted = choose_solution_from_aggregate(agg, args.solution_name)
        if sol_extracted is None:
            raise SystemExit("No se pudo determinar la solución (ni externa ni dentro del agregado)")
        solution_map = build_student_cellmap(sol_extracted)
        if not solution_map:
            raise SystemExit("La solución seleccionada no contiene cellmap_by_sheet válido")
        solution_label = sol_name

    # Evaluar cada alumno
    reports = []
    for stu in agg["students"]:
        name = stu["name"]
        extracted = agg["extracted"].get(name)
        if not isinstance(extracted, dict):
            continue
        student_map = build_student_cellmap(extracted)

        matches, penalties = compare(student_map, solution_map)
        score = len(matches) / max(1, (len(matches) + len(penalties)))

        rep = {
            "alumno": name,
            "score": score,
            "matches": matches,
            "penalties": penalties,
            "num_matches": len(matches),
            "num_penalties": len(penalties),
            "solution_ref": solution_label,
        }

        # incluir campos editables si existe comments_store
        if CommentsStore is not None:
            rep.update({
                "comentario_general": "",
                "nota": None,
                "comentarios_por_item": {},
            })
        reports.append(rep)

        # export diffs por alumno si procede
        if args.export_diffs:
            # generamos un csv por alumno añadiendo sufijo con nombre
            safe = "".join(c for c in name if c.isalnum() or c in ("-","_")).rstrip()
            dst = Path(args.export_diffs)
            if dst.is_dir():
                outp = dst / f"diffs_{safe}.csv"
            else:
                # si es archivo, añadimos el nombre del alumno
                outp = dst.parent / f"{dst.stem}_{safe}{dst.suffix or '.csv'}"
            export_diffs_csv(str(outp), name, penalties)

    # instancia de CommentsStore si existe
    store = None
    if CommentsStore is not None:
        try:
            store = CommentsStore(base_dir=args.comments_dir, read_only=False)
        except Exception as e:
            print(f"⚠ No se pudo inicializar CommentsStore: {e}")
            store = None

    # cargar comentarios existentes al reporte (si los hay) para que salgan en el JSON
    if store is not None:
        for rep in reports:
            sid = _get_student_id_from_report(rep)
            c0, s0 = _load_existing_comment(store, sid)
            if "comentario_general" in rep:
                rep["comentario_general"] = c0
            if "nota" in rep:
                rep["nota"] = s0

    def write_outputs():
        out_json = {
            "summary": {
                "num_students": len(reports),
                "solution_ref": solution_label,
            },
            "reports": reports
        }
        Path(args.out_json).write_text(json.dumps(out_json, ensure_ascii=False, indent=2), encoding="utf-8")

        # puntuaciones CSV básico
        try:
            import pandas as pd
            rows = [{"alumno": r["alumno"], "score": r["score"], "num_matches": r["num_matches"], "num_penalties": r["num_penalties"], "nota": r.get("nota")} for r in reports]
            pd.DataFrame(rows).to_csv(args.out_csv, index=False)
        except Exception:
            # fallback plano
            with open(args.out_csv, "w", encoding="utf-8") as f:
                f.write("alumno,score,num_matches,num_penalties,nota\n")
                for r in reports:
                    f.write(f"{r['alumno']},{r['score']},{r['num_matches']},{r['num_penalties']},{r.get('nota')}\n")

    # escritura inicial
    write_outputs()
    print(f"[OK] Escrito {args.out_json} y {args.out_csv}")

    # Interactivo real
    if args.interactive:
        interactive_loop(reports, store, rewrite_outputs_cb=write_outputs)
        # escritura final de cortesía
        write_outputs()
        print("[OK] Interactivo finalizado y salidas actualizadas.")

if __name__ == "__main__":
    main()
