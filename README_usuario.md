# 📑 Guía de uso para usuarios de las hojas Excel

Esta guía está pensada para el **equipo de CanaryBanana Export** que trabaja en administración, logística, producción y finanzas. Explica cómo rellenar y utilizar los ficheros Excel que se han creado para gestionar la empresa.

---

## 1. Archivos disponibles

Tienes tres libros Excel principales:

1. **`master_data.xlsx`** → contiene los **datos maestros** (clientes, productos, plantas, almacenes, transportistas, bancos).  
2. **`operations.xlsx`** → contiene la **actividad diaria** (pedidos de venta, envíos, movimientos de stock, producción).  
3. **`finance.xlsx`** → contiene la **gestión financiera** (facturas, pagos, plan contable, asientos).  

Cada archivo tiene varias hojas. Están preparadas con **listas desplegables** y **comprobaciones automáticas** para evitar errores.

---

## 2. Cómo rellenar cada archivo

### 📒 `master_data.xlsx`
Debes completar primero este fichero, ya que los demás dependen de él.

- **plants** → registrar las plantas de producción (ej. “Plantación Norte”).  
- **warehouses** → registrar almacenes o centros de distribución.  
- **parties** → incluir clientes, proveedores, bancos y agentes.  
  - Seleccionar en `type` si es *customer*, *supplier*, *bank*, etc.  
  - El campo `currency` debe elegirse de la lista desplegable.  
- **items** → productos con su `sku`, descripción y unidad de medida (ej. “BAN-001”, “Banana Premium”, “KG”).  
- **carriers** → transportistas y su modo de envío (*sea*, *air*, *road*).  
- **ports** → puertos utilizados en exportaciones (ej. “ESLPA Las Palmas”).  
- **pricelists** y **pricelist_lines** → tarifas por divisa/incoterm.  
- **fx_rates** → tipos de cambio históricos (si aplica).  
- **bank_accounts** → cuentas bancarias de la empresa.  
- **employees** y **roles** → personal interno y sus funciones.  
- **CHECKS** → hoja que comprueba si hay `parties` duplicados.  

👉 **Recomendación**: antes de usar los otros ficheros, asegúrate de que clientes, productos y bancos estén correctamente cargados aquí.

---

### 📒 `operations.xlsx`
Aquí se registran las operaciones de negocio.

- **sales_orders** → cada pedido de cliente:  
  - `id`: código único (ej. SO-2025-0001).  
  - `customer_id`: debe existir en `master_data.xlsx > parties`.  
  - `currency` e `incoterm`: selecciona de las listas desplegables.  
  - `status`: cambia a medida que avanza (ej. *draft*, *confirmed*, *shipped*).  

- **sales_order_lines** → detalle de productos en cada pedido:  
  - `sales_order_id`: debe coincidir con un pedido existente.  
  - `item_id`: debe existir en `items` del master.  
  - `qty`, `uom`, `price`.  

- **shipments** → cada envío creado a partir de pedidos:  
  - Incluye `shipper_id`, `consignee_id`, `mode` (mar, aire, carretera) y `status`.  

- **shipment_containers** / **shipment_container_lines** → detalla qué pedidos van en qué contenedor.  

- **customs_docs** → documentos aduaneros (asocia `hs_code` a ítems).  

- **inventory_movements** → movimientos de stock en almacenes.  

- **plant_outputs** → producción en planta (lotes, fechas, cantidades).  

- **plant_to_wh_transfers** → traslados de planta a almacén (con estado).  

- **CHECKS** → control automático:  
  - Comprueba que los clientes existen,  
  - Que las líneas de pedido refieren a pedidos válidos,  
  - Que los puertos de los envíos existen.  

👉 **Recomendación**:  
1. Crear primero el pedido (cabecera).  
2. Añadir líneas de producto.  
3. Crear el envío y asignar contenedores.  
4. Rellenar aduanas e inventario.

---

### 📒 `finance.xlsx`
Aquí se gestiona la parte económica.

- **chart_of_accounts** → plan de cuentas contable.  
- **invoices** → facturas emitidas o recibidas.  
  - `invoice_no`: número oficial.  
  - `type`: *AR* (emitida a cliente) o *AP* (recibida de proveedor).  
  - `party_id`: cliente o proveedor, debe estar en master.  
  - `net`, `tax`, `gross`: importes.  

- **invoice_lines** → detalle de las facturas.  

- **payments** → pagos realizados o recibidos.  
  - `type`: *incoming* (cobro) o *outgoing* (pago).  
  - `bank_id`: debe existir en master.  
  - `status`: *initiated*, *confirmed*, *reconciled*.  

- **payment_links** → enlaza un pago con una factura concreta.  

- **journal_entries** → asientos contables (cabecera con totales).  
- **journal_entry_lines** → detalle de cuentas, debe/haber.  

- **CHECKS**:  
  - Verifica que **debe = haber** en cada asiento.  
  - Comprueba que las facturas tienen pagos asignados correctos.  

👉 **Recomendación**:  
1. Crear la factura.  
2. Registrar los pagos.  
3. Vincular pagos a facturas en `payment_links`.  
4. Revisar el cuadre contable en `CHECKS`.

---

## 3. Buenas prácticas

✅ **IDs únicos**: usa códigos estandarizados (`SO-`, `INV-`, `PAY-`, etc.).  
✅ **Listas desplegables**: siempre selecciona de las listas para evitar errores de escritura.  
✅ **Orden de trabajo**:  
1. Cargar **master_data.xlsx**  
2. Rellenar **operations.xlsx**  
3. Completar **finance.xlsx**  
✅ **CHECKS**: revisa las hojas de control con frecuencia.  
✅ **Históricos**: no sobrescribas, guarda una copia mensual como “cerrado”.  

---

## 4. Errores frecuentes y cómo resolverlos

- ❌ Aparece error en CHECKS → puede faltar un cliente, producto o puerto en `master_data`.  
- ❌ Pedido sin líneas → completa `sales_order_lines`.  
- ❌ Factura no enlaza con pago → revisa que el `invoice_id` sea correcto en `payment_links`.  
- ❌ Asiento descuadrado → corrige débitos y créditos hasta que ∑debe=∑haber.  

---

## 5. Soporte

En caso de duda:  
- **Logística/Operaciones** → coordinar con equipo de logística.  
- **Finanzas** → equipo de contabilidad.  
- **Problemas técnicos en Excel** → contactar con soporte IT interno.  
