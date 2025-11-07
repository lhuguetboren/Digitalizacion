import pandas as pd
import json
from pathlib import Path
import re
from datetime import datetime, date

# --- CONFIGURACIÓN ---
input_path = Path("C:/Users/LlorençHuguetBoren\OneDrive - Grup STUCOM\Documentos/GitHub/Digitalizacion/practicas/org_dig_tools/_CIN1/RA1/salidas/resumen_ultimas_filas.json")
output_path = input_path.with_name("informe_comparacion_invoice_final.xlsx")

# --- CARGA DEL JSON ---
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- VALORES DE REFERENCIA (más utilizados) ---
valores_referencia = {
    "operations": {
        "sales_orders": {
            "id": "SO-0061",
            "currency": "EUR",
            "status": "confirmed",
            "incoterm": "FOB",
        },
        "sales_order_lines": {
            "so_id": "SO-0061",
            "item_id": "IT-01",
            "qty": 1500,
            "unit_price": 2.0,
            "currency": "EUR",
        },
        "shipments": {
            "id": "SHP-0016",
            "mode": "SEA",
            "status": "in_transit",
            "currency": "EUR",
        },
        "shipment_lines": {
            "shipment_id": "SHP-0016",
            "so_id": "SO-0061",
            "qty": 1500,
            "currency": "EUR",
        },
        "plant_to_wh_transfers": {
            "id": "TW-0182",
            "item_id": "IT-02",
            "qty": 1500,
            "uom": "KG",
        },
    },
    "finance": {
        "invoice": {
            "id": "INV-0061",
            "party_id": "PT-006",
            "invoice_date": "2025-12-01",
            "currency": "EUR",
            "amount": 3000.0,
            "status": "posted",
        },
        "invoice_lines": {
            "invoice_id": "INV-0061",
            "qty": 1500,
            "currency": "EUR",
            "line_amount": 3000.0,
        },
        "payments": {
            "id": "PAY-0061",
            "amount": 3000.0,
            "currency": "EUR",
            "status": "applied",
        },
        "payment_links": {
            "payment_id": "PAY-0061",
            "invoice_id": "INV-0061",
            "currency": "EUR",
        },
    },
}

# --- FUNCIONES AUXILIARES ---
def es_fecha(valor):
    """Devuelve True si el valor parece ser una fecha o timestamp."""
    if isinstance(valor, (datetime, date)):
        return True
    if isinstance(valor, str):
        # Detección simple por patrón AAAA-MM-DD o similar
        return bool(re.match(r"^\d{4}-\d{1,2}-\d{1,2}", valor.strip()))
    return False

# --- PROCESAMIENTO ---
registros = []

for entry in data:
    directory = entry.get("directory")
    category = entry.get("category")
    sheets = entry.get("sheets", {})

    ref_cat = valores_referencia.get(category, {})

    for sheet_name, sheet_info in sheets.items():
        status = sheet_info.get("status")
        ref_values = ref_cat.get(sheet_name, {})

        # Caso KO directo (hoja ausente o error)
        if status != "ok":
            detalles = f"Tipo de error: {status}"
            last_row = sheet_info.get("last_row", {})
            if isinstance(last_row, dict) and ref_values:
                campos_ref = set(ref_values.keys())
                campos_reales = set(last_row.keys())
                faltan = campos_ref - campos_reales
                extra = campos_reales - campos_ref
                detalles += f" | Campos faltantes: {', '.join(faltan) if faltan else '-'}"
                detalles += f" | Campos extra: {', '.join(extra) if extra else '-'}"
            else:
                if not ref_values:
                    detalles += " | No hay valores de referencia para comparar"

            registros.append({
                "directory": directory,
                "category": category,
                "sheet": sheet_name,
                "status": "ko",
                "detalles": detalles,
            })
            continue

        # Caso OK: comparar con referencia
        last_row = sheet_info.get("last_row", {})
        if not ref_values:
            registros.append({
                "directory": directory,
                "category": category,
                "sheet": sheet_name,
                "status": "ko",
                "detalles": "No hay valores de referencia para comparar",
            })
            continue

        difs = {}
        for key, val_ref in ref_values.items():
            val_real = last_row.get(key)

            # Ignorar campos con nombres o valores de fecha
            if "date" in key.lower() or es_fecha(val_ref) or es_fecha(val_real):
                continue

            if isinstance(val_real, float) and isinstance(val_ref, (int, float)):
                if abs(val_real - val_ref) > 1e-6:
                    difs[key] = (val_ref, val_real)
            elif val_real != val_ref:
                difs[key] = (val_ref, val_real)

        if not difs:
            status_final = "ok"
            detalles = "Coincide con los valores más utilizados"
        else:
            status_final = "diferencias"
            detalles = ", ".join(
                f"{k}: esperado {v[0]} / encontrado {v[1]}" for k, v in difs.items()
            )

        registros.append({
            "directory": directory,
            "category": category,
            "sheet": sheet_name,
            "status": status_final,
            "detalles": detalles,
        })

# --- EXPORTAR ---
df = pd.DataFrame(registros)
df.to_excel(output_path, index=False)

print(f"✅ Informe final con 'invoice' incluido y fechas ignoradas guardado en: {output_path}")
