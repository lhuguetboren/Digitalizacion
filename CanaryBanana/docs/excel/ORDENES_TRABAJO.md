# 📋 Órdenes de Trabajo – CanaryBanana Export

---

## 1️⃣ Planta → Almacén: Envío interno de producto

**Objetivo**: Registrar que la planta envía bananas frescas al almacén central para preparación de pedidos.

1. Abrir **`master_data.xlsx`** y verificar:  
   - La planta de origen existe en la hoja `plants` (ej. `PL-01`).  
   - El almacén de destino está registrado en `warehouses` (ej. `WH-01`).  
   - El producto (bananas) está en `items` (ej. `IT-01` – Banana fresca KG).  

2. Abrir **`operations.xlsx` → `shipments`**.  
   - Crear nuevo registro con:  
     - `id`: SH-0101  
     - `origin`: PL-01  
     - `destination`: WH-01  
     - `item_id`: IT-01  
     - `qty`: 2.000 KG  
     - `status`: *planned*  

3. Cuando la carga salga de la planta, actualizar `status` → *in_transit*.  
4. Una vez llegue al almacén, marcar `status` → *delivered*.  

---

## 2️⃣ Orden de trabajo - Administración: Nueva orden de venta

**Objetivo**: Registrar un pedido confirmado de un cliente internacional.

1. Abrir **`operations.xlsx` → `sales_orders`**.  
   - Crear nuevo pedido con:  
     - `id`: SO-0101  
     - `customer_id`: PT-011 (Cliente Alemania, Berlín)  
     - `incoterm`: FOB  
     - `currency`: EUR  
     - `status`: *confirmed*  
     - `order_date`: 2025-09-21  
     - `requested_date`: 2025-09-25  
     - `promised_date`: 2025-09-27  

2. Abrir **`sales_order_lines`** y añadir detalle:  
   - `so_id`: SO-0101  
   - `line_no`: 1  
   - `item_id`: IT-01 (Bananas frescas KG)  
   - `qty`: 1.500 KG  
   - `uom`: KG  
   - `unit_price`: 1.25  
   - `currency`: EUR  

## 3️⃣ Orden de trabajo - Finanzas: Facturación de la venta

**Objetivo**: Emitir la factura correspondiente al pedido SO-0101.

1. Abrir **`finance.xlsx` → `invoices`**.  
   - Crear nuevo registro:  
     - `id`: INV-0101  
     - `party_id`: PT-011  
     - `invoice_date`: 2025-09-22  
     - `due_date`: 2025-10-22  
     - `currency`: EUR  
     - `total`: 1.500 × 1.25 = **1.875 €**  
     - `status`: *pending*  

2. Enviar copia de la factura al cliente.  
3. Cuando el cliente pague, registrar en **`payments`**:  
   - `id`: PAY-0101  
   - `invoice_id`: INV-0101  
   - `payment_type`: customer_payment  
   - `amount`: 1.875 €  
   - `status`: *applied* → actualizar a *reconciled* al confirmarse en banco.  

---

## 4️⃣ Logística → Envío internacional

**Objetivo**: Registrar la salida del pedido hacia el cliente en Alemania.

1. Abrir **`operations.xlsx` → `shipments`**.  
   - Crear envío vinculado a la orden SO-0101:  
     - `id`: SH-0201  
     - `origin`: WH-01 (Almacén central Las Palmas)  
     - `destination`: PT-011 (Cliente en Berlín)  
     - `item_id`: IT-01  
     - `qty`: 1.500 KG  
     - `status`: *planned*  

2. Cambiar estado según avance:  
   - Salida del puerto → *in_transit*.  
   - Llegada a Alemania → *arrived*.  
   - Entrega final → *delivered*.  

---

**Resultado esperado**:

- La planta registra producción enviada al almacén.  
- Administración crea un pedido y su factura.  
- Finanzas controla cobro y conciliación.  
- Logística asegura trazabilidad del envío internacional.  
