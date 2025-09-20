# Excel2CanaryBanana Export

## 1️⃣ Personal de **Plantas y Almacén**
### Objetivo:
Registrar y mantener actualizada la información de infraestructuras y stock.

### Ficheros y hojas a usar:
- **`master_data.xlsx`**
  - **plants**: registrar plantas de producción (id, nombre, país, ciudad).
  - **warehouses**: añadir almacenes asociados a una planta.
  - **items**: definir artículos (ej. bananas verdes, bananas empaquetadas) con su unidad de medida (UOM).
- **`operations.xlsx`**
  - **shipments**: confirmar el estado de los envíos (planned → in_transit → delivered).

### Instrucciones:
1. **Alta de almacén**  
   - Abrir `master_data.xlsx` → hoja `warehouses`.  
   - Introducir `id` único (ej. `WH-02`), nombre, planta asociada (`PL-01`), país, ciudad.  
   - ⚠️ Validación: `plant_id` debe existir en la hoja `plants`.

2. **Registro de artículos (bananas)**  
   - En `items`: cada producto debe tener un código (`IT-XX`), nombre, descripción y unidad de medida (KG, EA, etc.).  
   - ⚠️ UOM controlada por lista desplegable.

3. **Confirmar envíos**  
   - En `operations.xlsx` → `shipments`, cambiar estado de envío según avance real:  
     `planned` → `in_transit` → `arrived` → `delivered`.  
   - Ejemplo: un camión cargado en Las Palmas pasa de *planned* a *in_transit*.

---

## 2️⃣ Personal de **Administración y Ventas**
### Objetivo:
Registrar pedidos de clientes, emitir facturas y gestionar cobros/pagos.

### Ficheros y hojas a usar:
- **`operations.xlsx`**
  - **sales_orders**: pedidos de clientes (cabecera).
  - **sales_order_lines**: detalle de líneas (artículos, cantidades, precios).
- **`finance.xlsx`**
  - **invoices**: emisión y control de facturas.
  - **payments**: registro de cobros/pagos.

### Instrucciones:
1. **Registrar pedido de cliente (SO)**  
   - Abrir `operations.xlsx` → `sales_orders`.  
   - Introducir `id` (ej. `SO-0043`), `customer_id` (ej. `PT-003`), incoterm (ej. FOB), moneda (EUR).  
   - Completar fechas: orden, solicitada, prometida.  
   - Estado inicial: `confirmed`.  

2. **Añadir líneas del pedido**  
   - En `sales_order_lines`, indicar:  
     - `so_id` (ej. `SO-0043`).  
     - `item_id` (ej. `IT-01`).  
     - `qty` (ej. 200 KG).  
     - `unit_price` (ej. 1.20 €).  
   - ⚠️ Validación: `item_id` debe existir en `master_data.xlsx → items`.

3. **Emitir factura**  
   - En `finance.xlsx` → `invoices`.  
   - Copiar `party_id` del cliente (ej. PT-003).  
   - Introducir fecha de emisión, vencimiento, importe total.  
   - Estado inicial: `pending`.

4. **Registrar pago**  
   - En `payments`: indicar tipo (`customer_payment`), importe, fecha.  
   - Estado: `applied` cuando se asocia a factura, `reconciled` cuando está confirmado en banco.

---

## 3️⃣ Personal de **IT y Soporte Digital**
### Objetivo:
Mantener integridad, actualizaciones y copias de seguridad de los ficheros Excel.

### Ficheros a usar:
- **`master_data.xlsx`**, **`operations.xlsx`**, **`finance.xlsx`**  
- Scripts: `generate_excels.py`, `excel_models.py`  

### Instrucciones:
1. **Generar los ficheros desde cero**  
  
2. **Mantener listas de validación**  

   - Las listas (`uom`, `incoterms`, `currencies`, `status`) se gestionan en `master_data.xlsx → lists`.  
   - IT debe garantizar que no se eliminen filas de estas listas.

3. **Integridad de claves**  
   - Revisar que:  
     - `customer_id` en pedidos exista en `parties`.  
     - `item_id` en líneas exista en `items`.  
     - `party_id` en facturas exista en `parties`.  

4. **Copias de seguridad y control de versiones**  
   - Guardar versiones semanales de los tres Excel en servidor compartido.  
   - Recomendar nombrar con fecha: `finance_2025-09-20.xlsx`.

---

## Ejemplo de flujo práctico

1. Cliente **PT-003 (Berlin3)** hace pedido:  
   - `SO-0043` en `operations.xlsx`.  
   - Línea: 200 KG bananas a 1,2 €/kg.  
2. Almacén confirma envío → `shipments` pasa a `delivered`.  
3. Administración emite factura → `INV-0043` en `finance.xlsx`.  
4. Cliente paga → registro en `payments`.  
5. IT valida integridad y guarda copia de seguridad.  
