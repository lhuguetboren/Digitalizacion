# Estructura de los ficheros Excel

- **`master_data.xlsx`** → Datos maestros: plantas, almacenes, clientes, puertos, artículos y cuentas.  
- **`operations.xlsx`** → Operaciones comerciales: pedidos de venta, líneas, envíos.  
- **`finance.xlsx`** → Finanzas: facturas, pagos, conciliación.

---

## Mapa del sistema

El guiente diagrama muestra cómo los tres Excel se conectan:

```mermaid
flowchart LR
    subgraph M[master_data.xlsx]
      M1[plants]
      M2[warehouses]
      M3[ports]
      M4[items]
      M5[parties -clientes/proveedores-]
      M6[chart_of_accounts / bank_accounts]
      M7[lists: uom, incoterms, currencies, so_status, shipment_status, payment_*]
    end

    subgraph O[operations.xlsx]
      O1[sales_orders]
      O2[sales_order_lines]
      O3[shipments]
    end

    subgraph F[finance.xlsx]
      F1[invoices]
      F2[payments]
      F3[ledger]
    end

    M5 -- customer_id --> O1
    M4 -- item_id --> O2
    M7 -- incoterms/uom/currencies --> O1
    O1 -- so_id --> O2
    O1 -. genera .-> O3
    O1 -. entrega cumplida .-> F1
    M5 -- party_id --> F1
    M7 -- payment_types/status --> F2
    F2 -. conciliación .-> F1
```

**Explicación**:  
- El **Master Data** centraliza las entidades (clientes, artículos, puertos).  
- **Operaciones** gestiona pedidos y logística.  
- **Finanzas** refleja facturación y cobros.  
- Todo se une mediante claves (`customer_id`, `so_id`, `party_id`).

---

## Flujo “Order-to-Cash”
Este diagrama describe el ciclo completo de negocio:

```mermaid
sequenceDiagram
    participant C as Cliente
    participant V as Ventas (sales_orders)
    participant L as Logística (shipments)
    participant F as Finanzas (invoices/payments)

    C->>V: Solicita pedido (incoterm, moneda)
    V->>V: Crear SO (status: confirmed)
    V->>L: Programar envío
    L-->>V: Confirmar entrega (delivered)
    V->>F: Emitir factura (status=pending)
    C->>F: Realiza pago
    F->>F: Conciliación (applied → reconciled)
    F-->>C: Confirmación / recibo
```

---

## Ejemplo real

- Cliente **PT-003 (Berlin3)** hace un pedido **SO-0043**.  
- Se confirma el pedido y se programa el envío.  
- Se emite factura **INV-0043** por **944,4 €**.  
- El ciclo conecta `master_data.xlsx` → `operations.xlsx` → `finance.xlsx`.

---

## Beneficios de la digitalización

- Elimina duplicidades y errores manuales.  
- Integra logística, ventas y finanzas en un solo flujo.  
- Mejora la transparencia hacia clientes internacionales.  
- Permite análisis económico y estratégico a partir de datos fiables.  