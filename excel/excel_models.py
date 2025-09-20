# excel_models.py
from pathlib import Path
from typing import Dict, List, Sequence
import pandas as pd
import os



# ====== Config JSON loader ======
import json
CONFIG_DIR = os.environ.get("EXCEL_MODELS_CONFIG", "/config")
def _load_cfg(name: str) -> dict:
    try:
        p = Path(CONFIG_DIR) / f"{name}.json"
        if p.exists():
            with p.open("r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}

# ====== Config JSON loader ======
import json

CONFIG_DIR = os.environ.get("EXCEL_MODELS_CONFIG", "config")

def _load_cfg(name: str) -> dict:
    try:
        p = Path(CONFIG_DIR) / f"{name}.json"
        if p.exists():
            with p.open("r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def _get_sheet(cfg: dict, sheet: str, default_headers: list[str], default_rows: list[dict] | None = None):
    s = (cfg.get("sheets") or {}).get(sheet, {})
    headers = s.get("headers", default_headers)
    rows = s.get("rows", default_rows or [])
    return headers, rows

# =========================
# Utilidades xlsxwriter
# =========================
def _add_table(ws, df: pd.DataFrame, table_name: str):
    nrows, ncols = df.shape
    ws.add_table(0, 0, max(nrows, 1), max(ncols, 1) - 1, {
        "name": table_name,
        "columns": [{"header": c} for c in df.columns],
        "autofilter": True,
    })
    ws.freeze_panes(1, 0)

def _write_sheet(writer, sheet: str, tbl: str, headers: Sequence[str], rows: List[Dict]):
    df = pd.DataFrame(rows, columns=headers)
    df.to_excel(writer, index=False, sheet_name=sheet)
    ws = writer.sheets[sheet]
    _add_table(ws, df.fillna(""), f"Tbl_{sheet}")

def _col_to_letter(idx: int) -> str:
    s = ""
    while idx:
        idx, r = divmod(idx - 1, 26)
        s = chr(65 + r) + s
    return s

def _apply_validations(workbook, worksheet, headers: Sequence[str], rules: Dict[str, Dict], max_rows: int):
    for col_name, rule in rules.items():
        if col_name not in headers:
            continue
        col_idx = headers.index(col_name)
        col_letter = _col_to_letter(col_idx + 1)
        if rule.get("type") == "list":
            src_sheet, _src_named = rule["source"]
            src_col_index = rule.get("col_index", 0)
            src_range = f"{src_sheet}!{_col_to_letter(src_col_index+1)}2:{_col_to_letter(src_col_index+1)}2001"
            worksheet.data_validation(
                f"{col_letter}2:{col_letter}{max_rows}",
                {"validate": "list", "source": f"={src_range}"}
            )

def _lists_sheet(writer, lists: Dict[str, List[str]], sheet="lists"):
    df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in lists.items()]))
    df.to_excel(writer, index=False, sheet_name=sheet)
    _add_table(writer.sheets[sheet], df.fillna(""), "Tbl_lists")
    return df  # útil para mapear índices de columnas

# =========================
# Carga de IDs desde master_data.xlsx
# =========================
def _read_master_ids(master_path: str | None) -> Dict[str, List[str]]:
    """
    Lee IDs de master_data.xlsx si existe. Si no, devuelve listas vacías (se rellenarán con demo si procede).
    """
    ids = {
        "party_ids": [],
        "port_ids": [],
        "warehouse_ids": [],
        "plant_ids": [],
        "item_ids": [],
        "bank_ids": [],
        "account_ids": [],
        "uom": [],
        "currencies": [],
        "incoterms": [],
        "shipment_mode": [],
        "so_status": [],
        "shipment_status": [],
        "payment_types": [],
        "payment_status": [],
    }
    if not master_path:
        return ids
    p = Path(master_path)
    if not p.exists():
        return ids

    # Lee hojas si existen
    try:
        with pd.ExcelFile(p) as xls:
            if "parties" in xls.sheet_names:
                ids["party_ids"] = pd.read_excel(xls, "parties")["id"].dropna().astype(str).tolist()
            if "ports" in xls.sheet_names:
                ids["port_ids"] = pd.read_excel(xls, "ports")["id"].dropna().astype(str).tolist()
            if "warehouses" in xls.sheet_names:
                ids["warehouse_ids"] = pd.read_excel(xls, "warehouses")["id"].dropna().astype(str).tolist()
            if "plants" in xls.sheet_names:
                ids["plant_ids"] = pd.read_excel(xls, "plants")["id"].dropna().astype(str).tolist()
            if "items" in xls.sheet_names:
                ids["item_ids"] = pd.read_excel(xls, "items")["id"].dropna().astype(str).tolist()
            if "bank_accounts" in xls.sheet_names:
                ids["bank_ids"] = pd.read_excel(xls, "bank_accounts")["id"].dropna().astype(str).tolist()
            if "chart_of_accounts" in xls.sheet_names:
                ids["account_ids"] = pd.read_excel(xls, "chart_of_accounts")["id"].dropna().astype(str).tolist()
            if "lists" in xls.sheet_names:
                ldf = pd.read_excel(xls, "lists")
                for col in ids.keys():
                    if col in ldf.columns:
                        ids[col] = ldf[col].dropna().astype(str).tolist() or ids[col]
    except Exception:
        # Si algo falla leyendo, devolvemos lo que haya
        pass
    return ids

# =========================
# Master data
# =========================
def build_master(path: str, include_demo: bool = True, max_rows: int = 2000):
    cfg = _load_cfg('master')
    path = str(Path(path).resolve())
    lists = cfg.get('lists') or {
        "uom": ["EA", "KG", "L", "PAL"],
        "incoterms": ["EXW","FCA","FOB","CFR","CIF","DAP","DDP"],
        "currencies": ["EUR","USD","GBP"],
        "shipment_mode": ["SEA","AIR","ROAD","RAIL"],
        "so_status": ["draft","confirmed","fulfilled","cancelled"],
        "shipment_status": ["planned","in_transit","arrived","delivered","cancelled"],
        "payment_types": ["customer_payment","vendor_payment","bank_fee","other"],
        "payment_status": ["pending","applied","reconciled","cancelled"],
    }

    plants_headers = ["id","name","country","city"]
    warehouses_headers = ["id","name","plant_id","country","city"]
    items_headers = ["id","name","uom","description"]
    parties_headers = ["id","name","role","tax_id","country"]
    ports_headers = ["id","name","unlocode","country","city"]
    carriers_headers = ["id","name","mode","scac","country"]
    bank_headers = ["id","bank_name","iban","currency","country"]
    coa_headers = ["id","code","name","type","currency"]

    demo = include_demo
    plants_rows = [{"id":"PL-01","name":"Planta Central","country":"ES","city":"Valencia"}] if demo else []
    warehouses_rows = [{"id":"WH-01","name":"Almacén A","plant_id":"PL-01","country":"ES","city":"Valencia"}] if demo else []
    items_rows = [{"id":"IT-01","name":"Tomate enlatado","uom":"EA","description":"Lata 400g"}] if demo else []
    parties_rows = [{"id":"PT-01","name":"Cliente Demo","role":"customer","tax_id":"ESX1234567","country":"ES"}] if demo else []
    ports_rows = [{"id":"PR-01","name":"Puerto de Valencia","unlocode":"ESVLC","country":"ES","city":"Valencia"}] if demo else []
    carriers_rows = [{"id":"CR-01","name":"Naviera Demo","mode":"SEA","scac":"DEMO","country":"ES"}] if demo else []
    bank_rows = [{"id":"BK-01","bank_name":"Banco Demo","iban":"ES7620770024003102575766","currency":"EUR","country":"ES"}] if demo else []
    coa_rows = [{"id":"AC-700","code":"700","name":"Ventas","type":"revenue","currency":"EUR"}] if demo else []

    
    # Override headers/rows from master.json if present
    _ms = cfg.get("sheets") or {}
    def _ovr(name, headers, rows):
        s = _ms.get(name, {})
        return s.get("headers", headers), s.get("rows", rows)
    plants_headers, plants_rows = _ovr("plants", plants_headers, plants_rows)
    warehouses_headers, warehouses_rows = _ovr("warehouses", warehouses_headers, warehouses_rows)
    items_headers, items_rows = _ovr("items", items_headers, items_rows)
    parties_headers, parties_rows = _ovr("parties", parties_headers, parties_rows)
    ports_headers, ports_rows = _ovr("ports", ports_headers, ports_rows)
    carriers_headers, carriers_rows = _ovr("carriers", carriers_headers, carriers_rows)
    bank_headers, bank_rows = _ovr("bank_accounts", bank_headers, bank_rows)
    coa_headers, coa_rows = _ovr("chart_of_accounts", coa_headers, coa_rows)
    with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
        _lists_sheet(writer, lists, sheet="lists")

        _write_sheet(writer, "plants", "Tbl_plants", plants_headers, plants_rows)
        _write_sheet(writer, "warehouses", "Tbl_warehouses", warehouses_headers, warehouses_rows)
        _write_sheet(writer, "items", "Tbl_items", items_headers, items_rows)
        _write_sheet(writer, "parties", "Tbl_parties", parties_headers, parties_rows)
        _write_sheet(writer, "ports", "Tbl_ports", ports_headers, ports_rows)
        _write_sheet(writer, "carriers", "Tbl_carriers", carriers_headers, carriers_rows)
        _write_sheet(writer, "bank_accounts", "Tbl_banks", bank_headers, bank_rows)
        _write_sheet(writer, "chart_of_accounts", "Tbl_coa", coa_headers, coa_rows)

        wb = writer.book
        ws_items = writer.sheets["items"]
        _apply_validations(wb, ws_items, items_headers,
            {"uom": {"type":"list","source":("lists","uom"), "col_index": 0}}, max_rows)
        ws_car = writer.sheets["carriers"]
        _apply_validations(wb, ws_car, carriers_headers,
            {"mode":{"type":"list","source":("lists","shipment_mode"), "col_index": 3}}, max_rows)
        ws_banks = writer.sheets["bank_accounts"]
        _apply_validations(wb, ws_banks, bank_headers,
            {"currency":{"type":"list","source":("lists","currencies"), "col_index": 2}}, max_rows)
        ws_coa = writer.sheets["chart_of_accounts"]
        _apply_validations(wb, ws_coa, coa_headers,
            {"currency":{"type":"list","source":("lists","currencies"), "col_index": 2}}, max_rows)

# =========================
# Operations
# =========================
def build_operations(path: str, include_demo: bool = True, max_rows: int = 2000, master_path: str | None = None):
    cfg = _load_cfg('operations')
    """
    Crea operations.xlsx; si se pasa master_path, toma IDs y listas desde master_data.xlsx
    """
    path = str(Path(path).resolve())
    mid = _read_master_ids(master_path)

    # Si no hay master y se quiere demo, rellenamos mínimos
    def _fill(lst, demo_val):
        return lst if lst else ([demo_val] if include_demo and demo_val else [])

    id_lists = {
        "party_ids":    _fill(mid["party_ids"], "PT-01"),
        "port_ids":     _fill(mid["port_ids"], "PR-01"),
        "warehouse_ids":_fill(mid["warehouse_ids"], "WH-01"),
        "plant_ids":    _fill(mid["plant_ids"], "PL-01"),
        "item_ids":     _fill(mid["item_ids"], "IT-01"),
    }
    lists = {
        "currencies": mid["currencies"] or ["EUR","USD","GBP"],
        "incoterms": mid["incoterms"] or ["EXW","FCA","FOB","CFR","CIF","DAP","DDP"],
        "shipment_mode": mid["shipment_mode"] or ["SEA","AIR","ROAD","RAIL"],
        "uom": (cfg.get('lists',{}).get('uom') or mid['uom'] or ['EA','KG','L','PAL']),
        "so_status": (cfg.get('lists',{}).get('so_status') or mid['so_status'] or ['draft','confirmed','fulfilled','cancelled']),
        "shipment_status": (cfg.get('lists',{}).get('shipment_status') or mid['shipment_status'] or ['planned','in_transit','arrived','delivered','cancelled']),
        **id_lists
    }

    so_headers  = ["id","customer_id","incoterm","currency","status","order_date","requested_date","promised_date"]
    sol_headers = ["so_id","line_no","item_id","qty","uom","unit_price","currency"]
    shp_headers = ["id","mode","status","shipper_id","consignee_id","port_load","port_discharge","etd","eta","currency"]
    shl_headers = ["shipment_id","so_id","so_line_no","item_id","qty","uom","unit_price","currency"]
    invm_headers = ["id","movement_date","warehouse_id","item_id","qty","uom","reason"]
    pout_headers = ["id","output_date","plant_id","item_id","qty","uom","batch"]
    p2w_headers  = ["id","transfer_date","plant_id","warehouse_id","item_id","qty","uom"]

    demo = include_demo
    so_rows = [{
        "id":"SO-0001","customer_id": id_lists["party_ids"][0] if id_lists["party_ids"] else "",
        "incoterm":"FOB","currency":"EUR","status":"confirmed",
        "order_date":"2025-09-01","requested_date":"2025-09-10","promised_date":"2025-09-12"
    }] if demo else []
    sol_rows = [{
        "so_id":"SO-0001","line_no":1,"item_id": id_lists["item_ids"][0] if id_lists["item_ids"] else "",
        "qty":100,"uom":"EA","unit_price":1.2,"currency":"EUR"
    }] if demo else []
    shp_rows = [{
        "id":"SHP-0001","mode":"SEA","status":"in_transit",
        "shipper_id": id_lists["party_ids"][0] if id_lists["party_ids"] else "",
        "consignee_id": id_lists["party_ids"][0] if id_lists["party_ids"] else "",
        "port_load": id_lists["port_ids"][0] if id_lists["port_ids"] else "",
        "port_discharge": id_lists["port_ids"][0] if id_lists["port_ids"] else "",
        "etd":"2025-09-05","eta":"2025-09-18","currency":"EUR"
    }] if demo else []
    shl_rows = [{
        "shipment_id":"SHP-0001","so_id":"SO-0001","so_line_no":1,
        "item_id": id_lists["item_ids"][0] if id_lists["item_ids"] else "",
        "qty":100,"uom":"EA","unit_price":1.2,"currency":"EUR"
    }] if demo else []
    invm_rows = [{
        "id":"IM-0001","movement_date":"2025-09-06",
        "warehouse_id": id_lists["warehouse_ids"][0] if id_lists["warehouse_ids"] else "",
        "item_id": id_lists["item_ids"][0] if id_lists["item_ids"] else "",
        "qty":100,"uom":"EA","reason":"receipt"
    }] if demo else []
    pout_rows = [{
        "id":"PO-0001","output_date":"2025-09-04",
        "plant_id": id_lists["plant_ids"][0] if id_lists["plant_ids"] else "",
        "item_id": id_lists["item_ids"][0] if id_lists["item_ids"] else "",
        "qty":100,"uom":"EA","batch":"B-001"
    }] if demo else []
    p2w_rows = [{
        "id":"TW-0001","transfer_date":"2025-09-05",
        "plant_id": id_lists["plant_ids"][0] if id_lists["plant_ids"] else "",
        "warehouse_id": id_lists["warehouse_ids"][0] if id_lists["warehouse_ids"] else "",
        "item_id": id_lists["item_ids"][0] if id_lists["item_ids"] else "",
        "qty":100,"uom":"EA"
    }] if demo else []

    
    # Override headers/rows from operations.json if present
    _ops = cfg.get("sheets") or {}
    def _ovr(name, headers, rows):
        s = _ops.get(name, {})
        return s.get("headers", headers), s.get("rows", rows)
    so_headers, so_rows = _ovr("sales_orders", so_headers, so_rows)
    sol_headers, sol_rows = _ovr("sales_order_lines", sol_headers, sol_rows)
    shp_headers, shp_rows = _ovr("shipments", shp_headers, shp_rows)
    shl_headers, shl_rows = _ovr("shipment_lines", shl_headers, shl_rows)
    invm_headers, invm_rows = _ovr("inventory_movements", invm_headers, invm_rows)
    pout_headers, pout_rows = _ovr("plant_outputs", pout_headers, pout_rows)
    p2w_headers, p2w_rows = _ovr("plant_to_warehouse", p2w_headers, p2w_rows)
    with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
        lists_df = _lists_sheet(writer, lists, sheet="lists")
        lists_col_index = {k: i for i, k in enumerate(lists_df.columns)}

        _write_sheet(writer, "sales_orders", "Tbl_sales_orders", so_headers, so_rows)
        _write_sheet(writer, "sales_order_lines", "Tbl_sales_order_lines", sol_headers, sol_rows)
        _write_sheet(writer, "shipments", "Tbl_shipments", shp_headers, shp_rows)
        _write_sheet(writer, "shipment_lines", "Tbl_shipment_lines", shl_headers, shl_rows)
        _write_sheet(writer, "inventory_movements", "Tbl_inventory_movements", invm_headers, invm_rows)
        _write_sheet(writer, "plant_outputs", "Tbl_plant_outputs", pout_headers, pout_rows)
        _write_sheet(writer, "plant_to_wh_transfers", "Tbl_p2w_transfers", p2w_headers, p2w_rows)

        wb = writer.book
        _apply_validations(wb, writer.sheets["sales_orders"], so_headers, {
            "incoterm":{"type":"list","source":("lists","incoterms"), "col_index": lists_col_index["incoterms"]},
            "currency":{"type":"list","source":("lists","currencies"), "col_index": lists_col_index["currencies"]},
            "status":{"type":"list","source":("lists","so_status"), "col_index": lists_col_index["so_status"]},
            "customer_id":{"type":"list","source":("lists","party_ids"), "col_index": lists_col_index["party_ids"]},
        }, max_rows)
        _apply_validations(wb, writer.sheets["sales_order_lines"], sol_headers, {
            "uom":{"type":"list","source":("lists","uom"), "col_index": lists_col_index["uom"]},
            "currency":{"type":"list","source":("lists","currencies"), "col_index": lists_col_index["currencies"]},
            "item_id":{"type":"list","source":("lists","item_ids"), "col_index": lists_col_index["item_ids"]},
        }, max_rows)
        _apply_validations(wb, writer.sheets["shipments"], shp_headers, {
            "mode":{"type":"list","source":("lists","shipment_mode"), "col_index": lists_col_index["shipment_mode"]},
            "status":{"type":"list","source":("lists","shipment_status"), "col_index": lists_col_index["shipment_status"]},
            "shipper_id":{"type":"list","source":("lists","party_ids"), "col_index": lists_col_index["party_ids"]},
            "consignee_id":{"type":"list","source":("lists","party_ids"), "col_index": lists_col_index["party_ids"]},
            "port_load":{"type":"list","source":("lists","port_ids"), "col_index": lists_col_index["port_ids"]},
            "port_discharge":{"type":"list","source":("lists","port_ids"), "col_index": lists_col_index["port_ids"]},
        }, max_rows)
        _apply_validations(wb, writer.sheets["inventory_movements"], invm_headers, {
            "uom":{"type":"list","source":("lists","uom"), "col_index": lists_col_index["uom"]},
            "warehouse_id":{"type":"list","source":("lists","warehouse_ids"), "col_index": lists_col_index["warehouse_ids"]},
            "item_id":{"type":"list","source":("lists","item_ids"), "col_index": lists_col_index["item_ids"]},
        }, max_rows)
        _apply_validations(wb, writer.sheets["plant_outputs"], pout_headers, {
            "uom":{"type":"list","source":("lists","uom"), "col_index": lists_col_index["uom"]},
            "plant_id":{"type":"list","source":("lists","plant_ids"), "col_index": lists_col_index["plant_ids"]},
            "item_id":{"type":"list","source":("lists","item_ids"), "col_index": lists_col_index["item_ids"]},
        }, max_rows)
        _apply_validations(wb, writer.sheets["plant_to_wh_transfers"], p2w_headers, {
            "uom":{"type":"list","source":("lists","uom"), "col_index": lists_col_index["uom"]},
            "plant_id":{"type":"list","source":("lists","plant_ids"), "col_index": lists_col_index["plant_ids"]},
            "warehouse_id":{"type":"list","source":("lists","warehouse_ids"), "col_index": lists_col_index["warehouse_ids"]},
            "item_id":{"type":"list","source":("lists","item_ids"), "col_index": lists_col_index["item_ids"]},
        }, max_rows)

# =========================
# Finance
# =========================
def build_finance(path: str, include_demo: bool = True, max_rows: int = 2000, master_path: str | None = None):
    cfg = _load_cfg('finance')
    from pathlib import Path
    import pandas as pd

    path = str(Path(path).resolve())
    mid = _read_master_ids(master_path)

    def _fill(lst, demo_val):
        return lst if lst else ([demo_val] if include_demo and demo_val else [])

    # IDs y listas base (desde master o demo)
    id_lists = {
        "party_ids": _fill(mid["party_ids"], "PT-01"),
        "item_ids": _fill(mid["item_ids"], "IT-01"),
        "bank_ids": _fill(mid["bank_ids"], "BK-01"),
        "account_ids": _fill(mid["account_ids"], "AC-700"),
    }
    base_lists = {
        "uom": mid["uom"] or ["EA","KG","L","PAL"],
        "currencies": mid["currencies"] or ["EUR","USD","GBP"],
        "payment_types": mid["payment_types"] or ["customer_payment","vendor_payment","bank_fee","other"],
        "payment_status": mid["payment_status"] or ["pending","applied","reconciled","cancelled"],
        **id_lists
    }

    inv_headers = ["id","party_id","invoice_date","due_date","currency","total","status"]
    inl_headers = ["invoice_id","line_no","item_id","description","qty","uom","unit_price","currency","line_amount"]
    pay_headers = ["id","party_id","bank_id","payment_date","type","currency","amount","status"]
    plink_headers = ["payment_id","invoice_id","applied_amount","currency"]
    je_headers = ["id","entry_date","currency","description"]
    jel_headers = ["je_id","line_no","account_id","debit","credit","currency","memo"]

    demo = include_demo
    inv_rows = [{
        "id":"INV-0001","party_id": id_lists["party_ids"][0] if id_lists["party_ids"] else "",
        "invoice_date":"2025-09-10","due_date":"2025-10-10","currency":"EUR","total":120.0,"status":"pending"
    }] if demo else []
    inl_rows = [{
        "invoice_id":"INV-0001","line_no":1,"item_id": id_lists["item_ids"][0] if id_lists["item_ids"] else "",
        "description":"Venta","qty":100,"uom":"EA","unit_price":1.2,"currency":"EUR","line_amount":120.0
    }] if demo else []
    pay_rows = [{
        "id":"PAY-0001","party_id": id_lists["party_ids"][0] if id_lists["party_ids"] else "",
        "bank_id": id_lists["bank_ids"][0] if id_lists["bank_ids"] else "",
        "payment_date":"2025-09-15","type":"customer_payment","currency":"EUR","amount":100.0,"status":"applied"
    }] if demo else []
    plink_rows = [{
        "payment_id":"PAY-0001","invoice_id":"INV-0001","applied_amount":100.0,"currency":"EUR"
    }] if demo else []
    je_rows = [{"id":"JE-0001","entry_date":"2025-09-10","currency":"EUR","description":"Venta INV-0001"}] if demo else []
    jel_rows = [{
        "je_id":"JE-0001","line_no":1,"account_id": id_lists["account_ids"][0] if id_lists["account_ids"] else "",
        "debit":0.0,"credit":120.0,"currency":"EUR","memo":"Ingreso por ventas"
    }] if demo else []

    
    # Override headers/rows from finance.json if present
    _fin = cfg.get("sheets") or {}
    def _ovr(name, headers, rows):
        s = _fin.get(name, {})
        return s.get("headers", headers), s.get("rows", rows)
    inv_headers, inv_rows = _ovr("invoices", inv_headers, inv_rows)
    inl_headers, inl_rows = _ovr("invoice_lines", inl_headers, inl_rows)
    pay_headers, pay_rows = _ovr("payments", pay_headers, pay_rows)
    plink_headers, plink_rows = _ovr("payment_links", plink_headers, plink_rows)
    je_headers, je_rows = _ovr("journal_entries", je_headers, je_rows)
    jel_headers, jel_rows = _ovr("journal_entry_lines", jel_headers, jel_rows)
    with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
        # 1) Escribir HOJAS DE DATOS primero (aún sin 'lists')
        _write_sheet(writer, "invoices", "Tbl_invoices", inv_headers, inv_rows)
        _write_sheet(writer, "invoice_lines", "Tbl_invoice_lines", inl_headers, inl_rows)
        _write_sheet(writer, "payments", "Tbl_payments", pay_headers, pay_rows)
        _write_sheet(writer, "payment_links", "Tbl_payment_links", plink_headers, plink_rows)
        _write_sheet(writer, "journal_entries", "Tbl_journal_entries", je_headers, je_rows)
        _write_sheet(writer, "journal_entry_lines", "Tbl_journal_entry_lines", jel_headers, jel_rows)

        # 2) Construir columnas dinámicas a partir de lo escrito (IDs de cabeceras)
        invoices_df = pd.DataFrame(inv_rows, columns=inv_headers)
        payments_df = pd.DataFrame(pay_rows, columns=pay_headers)
        dyn_cols = {
            "invoice_ids": invoices_df["id"].dropna().astype(str).tolist(),
            "payment_ids": payments_df["id"].dropna().astype(str).tolist(),
        }

        # 3) Unir listas base + dinámicas y ESCRIBIR 'lists' UNA SOLA VEZ
        merged_lists = {**base_lists, **dyn_cols}
        lists_full = pd.DataFrame({k: pd.Series(v) for k, v in merged_lists.items()})
        lists_full.to_excel(writer, index=False, sheet_name="lists")
        _add_table(writer.sheets["lists"], lists_full.fillna(""), "Tbl_lists")

        # 4) Índices de columnas para validaciones
        lists_col_index = {k: i for i, k in enumerate(lists_full.columns)}

        # 5) Aplicar VALIDACIONES (todas referenciando la 'lists' ya definitiva)
        wb = writer.book
        _apply_validations(wb, writer.sheets["invoices"], inv_headers, {
            "currency":{"type":"list","source":("lists","currencies"), "col_index": lists_col_index["currencies"]},
            "party_id":{"type":"list","source":("lists","party_ids"), "col_index": lists_col_index["party_ids"]},
        }, max_rows)

        _apply_validations(wb, writer.sheets["invoice_lines"], inl_headers, {
            "uom":{"type":"list","source":("lists","uom"), "col_index": lists_col_index["uom"]},
            "currency":{"type":"list","source":("lists","currencies"), "col_index": lists_col_index["currencies"]},
            "item_id":{"type":"list","source":("lists","item_ids"), "col_index": lists_col_index["item_ids"]},
            "invoice_id":{"type":"list","source":("lists","invoice_ids"), "col_index": lists_col_index["invoice_ids"]},
        }, max_rows)

        _apply_validations(wb, writer.sheets["payments"], pay_headers, {
            "type":{"type":"list","source":("lists","payment_types"), "col_index": lists_col_index["payment_types"]},
            "currency":{"type":"list","source":("lists","currencies"), "col_index": lists_col_index["currencies"]},
            "status":{"type":"list","source":("lists","payment_status"), "col_index": lists_col_index["payment_status"]},
            "party_id":{"type":"list","source":("lists","party_ids"), "col_index": lists_col_index["party_ids"]},
            "bank_id":{"type":"list","source":("lists","bank_ids"), "col_index": lists_col_index["bank_ids"]},
        }, max_rows)

        _apply_validations(wb, writer.sheets["payment_links"], plink_headers, {
            "currency":{"type":"list","source":("lists","currencies"), "col_index": lists_col_index["currencies"]},
            "payment_id":{"type":"list","source":("lists","payment_ids"), "col_index": lists_col_index["payment_ids"]},
            "invoice_id":{"type":"list","source":("lists","invoice_ids"), "col_index": lists_col_index["invoice_ids"]},
        }, max_rows)

        _apply_validations(wb, writer.sheets["journal_entry_lines"], jel_headers, {
            "currency":{"type":"list","source":("lists","currencies"), "col_index": lists_col_index["currencies"]},
            "account_id":{"type":"list","source":("lists","account_ids"), "col_index": lists_col_index["account_ids"]},
        }, max_rows)
