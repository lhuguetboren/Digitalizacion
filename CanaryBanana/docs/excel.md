# Guía de usuario – Plantillas Excel de CanaryBanana

> **Objetivo**: Breve explicacoin de los archivos Excel creados para la gestión diaria de la empresa: desde la cosecha en plantaciones hasta el envío y la facturación.

---

## 1) Cómo encajan los archivos en tu día a día

**Flujo recomendado**:

1. **Maestros**: primero rellena las fichas base (Clientes, Productos/Presentaciones, Ubicaciones, Impuestos/Monedas). *(Son las listas que luego aparecerán como desplegables.)*
2. **Operación**: registra **cosecha y producción** en los libros de inventario y movimientos.
3. **Logística**: prepara el **Packing List/Albarán** para cada envío.
4. **Finanzas**: emite la **Factura** a partir del envío y, si aplica, **descuentos/tarifas**.
5. **Seguimiento**: consulta **inventario** y **movimientos** para conocer existencias y trazabilidad.

> **Consejo**: rellena siempre primero los **Maestros** para que los desplegables funcionen (IDs válidos) y se eviten errores de tecleo.

---

## 2) Archivos MAESTROS (listas base)

### 2.1. Maestro\_Clientes.xlsx

* **Para qué sirve**: guardar la ficha de cada cliente (datos fiscales, entrega, condiciones comerciales).
* **Cuándo lo uso**: cuando hay un cliente nuevo o cambian sus datos.
* **Cómo se rellena** (hoja **Clientes**):

  * **Cliente\_ID** (código único, p. ej. `CLT-0001`).
  * **Nombre\_Fiscal**, **CIF\_IVA**, **País**.
  * **Dir\_Fiscal** y **Dir\_Entrega** (si son distintas).
  * **Incoterm\_Preferente**, **Moneda**, **Condiciones\_Pago**.
  * **Contacto**: nombre, email, teléfono.
* **Resultado**: tendrás clientes disponibles en desplegables de pedidos, packing y facturas.

### 2.2. Maestro\_Productos\_Presentaciones.xlsx

* **Para qué sirve**: definir **productos** (variedad/calibre) y sus **presentaciones** (caja, kg/caja, cajas/pallet, etc.).
* **Hojas**: **Productos** y **Presentaciones**.
* **Cómo se rellena**:

  * **Producto\_ID** (único) con su **Variedad** y **Calibre**.
  * **Presentacion\_ID** ligada a un **Producto\_ID** con su **Descripción**, **Kg\_Por\_Caja**, **Cajas\_Por\_Pallet**, **Vida\_Útil** y **Código Arancelario**.
* **Resultado**: podrás elegir presentaciones exactas en inventario, packing y facturas.

### 2.3. Maestro\_Ubicaciones.xlsx

* **Para qué sirve**: dar de alta **lugares** donde está el producto o los insumos.
* **Incluye** ejemplos: `P1` (Plantación 1), `P2` (Plantación 2), `ALM1` (Almacén), `OF1` (Oficina).
* **Campos**: **Ubicacion\_ID**, **Tipo** (Plantación/Almacén/Oficina), **Descripción**, **Zona**, **Estantería**.

### 2.4. Maestro\_Impuestos\_Monedas.xlsx

* **Para qué sirve**: mantener las **tasas de impuestos** (IGIC/IVA, etc.) y **monedas** aceptadas.
* **Uso**: la **Factura** tomará Moneda/Impuestos desde aquí.

---

## 3) Operación: inventarios y movimientos

### 3.1. Inventario\_Producto\_Terminado.xlsx

* **Para qué sirve**: ver **existencias** reales por lote, presentación y ubicación.
* **Cómo se usa** (hoja **Inventario**):

  * **Fecha** del registro (día de conteo o actualización).
  * **Ubicacion\_ID** (desplegable).
  * **Lote\_ID** (tu código interno, p. ej. `P1-2025-09-18-003`).
  * **Presentacion\_ID** (desplegable), **Pallet\_ID** (si aplica), **Cajas**, **Kg\_Netos**.
  * **Estado**: *Liberado* / *Bloqueado* (por calidad o cuarentena).
* **Resultado**: visión clara del stock disponible antes de planificar cargas.

### 3.2. Movimientos\_Stock.xlsx

* **Para qué sirve**: registrar **entradas, salidas y ajustes** (tipo Kardex) para trazabilidad.
* **Cómo se usa**:

  * **Fecha**, **Tipo** (*Entrada/Salida/Ajuste*), **Documento\_Origen** (por ejemplo: Empaquetado, PL, Inventario).
  * **Ubicacion\_ID**, **Lote\_ID**, **Cajas** y **Kg** con signo (+/−).
  * Se calculan **Stock\_Resultante** (por línea) para control continuo.
* **Resultado**: histórico de movimientos y reconciliación con inventario.

---

## 4) Logística: preparar el envío

### 4.1. PackingList\_Albaranes.xlsx

* **Para qué sirve**: generar el **packing list** (albarán de exportación) con todo el detalle de la carga.
* **Estructura**:

  * **Cabecera**: **PL\_ID**, **Fecha**, **Cliente\_ID**, **Pedido\_ID** (si lo usas), **Transporte** (*Camión/Contenedor*), **Contenedor**, **Sello**, **Puertos** (salida/llegada), **Incoterm**, **Temperatura\_Setpoint**, **Observaciones**.
  * **Líneas**: por cada producto/lote que va en la carga: **Lote\_ID**, **Presentacion\_ID**, **Pallets**, **Cajas**, **Kg\_Netos**, **Kg\_Brutos**.
* **Cuándo lo uso**: cuando confirmas qué pallets/cajas entran en un envío concreto.
* **Resultado**: documento base para transporte, aduana y posterior facturación.

---

## 5) Finanzas: facturación y descuentos

### 5.1. Facturas\_Emitidas.xlsx

* **Para qué sirve**: emitir facturas de venta vinculadas a un pedido y/o packing list.
* **Estructura**:

  * **Cabecera**: **Factura\_ID**, **Fecha**, **Cliente\_ID**, referencia a **Pedido\_o\_PL**, **Moneda**, **Tipo\_Cambio**, **Base**, **Impuestos**, **Descuentos**, **Total**, **Vencimiento**, **Estado** (*Pendiente/Cobrado*), **Observaciones**.
  * **Líneas**: **Producto\_ID**, **Presentacion\_ID**, **Cantidad** (cajas o kg), **Precio\_Unit**, **%Dto**, **Importe\_Linea**.
* **Resultado**: control de facturación y cartera de cobros.

### 5.2. Tarifas\_y\_Descuentos.xlsx

* **Para qué sirve**: definir **reglas de descuento** por cliente, por volumen o por temporada.
* **Campos clave**: **Regla\_ID**, **Tipo** (Cliente/Volumen/Temporada), **Cliente\_ID\_Grupo**, **Condición Mínima** (cajas/kg), **Valor** (% o €), **Vigencia**, **Prioridad**, **Acumulable** (S/N).
* **Uso**: consulta estas reglas para aplicar descuentos coherentes y trazables en la factura.

---

## 6) Organización interna

### Organigrama\_canarybanana.xlsx

* **Para qué sirve**: visualizar la estructura de la empresa.
* **Hojas**:

  * **Tabla Jerárquica (detallada)**: lista que puedes usar para generar diagramas.
  * **Organigrama Simple**: Dirección y grandes áreas.
  * **Organigrama Detallado**: áreas y puestos con número de personas.
* **Uso**: imprimir, compartir en reuniones o incorporar a presentaciones.

---

## 7) Reglas de uso y buenas prácticas

* **IDs únicos**: usa códigos estables (Cliente\_ID, Lote\_ID, PL\_ID, Factura\_ID) para que todo enlace bien.
* **Fechas**: formato `AAAA-MM-DD` para evitar confusiones (ej.: `2025-09-19`).
* **Desplegables**: si un desplegable no muestra datos, primero rellena el **Maestro** correspondiente o la hoja **Listas** del archivo.
* **Unidades**: mantén coherencia entre **cajas**, **kg netos** y **pallets**.
* **Estados**: bloquea lotes con dudas de calidad (no los cargues ni factures hasta resolver).
* **Trazabilidad**: cada **packing** debe indicar claramente **qué lotes** van y en qué cantidad.

---

## 8) Errores habituales y cómo evitarlos

* **El desplegable sale vacío** → faltan datos en **Maestros** o en **Listas**. Añade los IDs primero.
* **No encuentro un Lote\_ID** → comprueba que se escribió igual en Inventario/Movimientos/PL (respeta mayúsculas/minúsculas y guiones).
* **Totales que no cuadran** → revisa que las **unidades** (cajas/kg) coinciden entre líneas de PL y de Factura.
* **Dudas de impuestos/moneda** → confirma la configuración en **Maestro\_Impuestos\_Monedas**.

---

## 9) Glosario rápido

* **Lote\_ID**: código que identifica la fruta desde la plantación y fecha de corte (ej.: `P1-2025-09-18-003`).
* **Presentación**: forma de venta (p. ej. caja 18 kg), ligada a un producto.
* **Packing List (PL)**: detalle de lo que viaja en un camión o contenedor (pallets, cajas, kg; por lote).
* **Incoterm**: regla comercial internacional que define responsabilidades de transporte/costos.
* **Kardex/Movimientos**: registro cronológico de entradas/salidas/ajustes de stock.

---

## 10) Checklist para el primer uso

* [ ] Cargar **Clientes**.
* [ ] Cargar **Productos** y **Presentaciones**.
* [ ] Confirmar **Ubicaciones** (P1, P2, ALM1, OF1) y añadir si hace falta.
* [ ] Revisar **Impuestos y Monedas**.
* [ ] Registrar inventario inicial o los primeros **Movimientos de Stock**.
* [ ] Preparar un **Packing List** de prueba.
* [ ] Emitir una **Factura** de ejemplo usando ese PL.

> Con esto tendrás un circuito completo, claro y trazable, listo para operar y crecer sin perder control.
