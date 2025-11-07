# Explotar información: Introducción a fórmulas y gráficos en Excel

**Archivos de trabajo:**

- `operacions.xlsx` → listado de operaciones comerciales  

---

## Objetivos de aprendizaje

Al finalizar estos ejercicios, será capaz de:

1. Usar fórmulas básicas en Excel (sumas, promedios, productos, condicionales).  
2. Relacionar datos entre hojas mediante funciones de búsqueda (`BUSCARV`).  
3. Organizar y presentar información comercial con tablas y gráficos.  
4. Interpretar la información obtenida (países con más ventas, márgenes, etc.).

---

## Ejercicio 1. Cálculo del importe y margen de venta

**Objetivo:** practicar fórmulas básicas y referencias absolutas/relativas.  
**Archivo:** `operacions_RA2.xlsx`
**Hoja:** sales_order_lines

### Pasos

1. Abre el archivo y observa las columnas: `Cliente`, `Producto`, `Cantidad`, `Precio unitario`, `Fecha`…  
2. Crea una nueva columna llamada **Importe total**:

   ```excel
   =Cantidad * Precio_unitario
   ```

3. Añade una columna **Coste estimado** (70 % del precio unitario):  

   ```excel
   =Precio_unitario * 0,7
   ```

4. Calcula el **Margen bruto (€)** y el **Margen (%)**:

   ```excel
   =Importe_total - Coste_est
   =Margen_bruto / Importe_total
   ```

5. Aplica formato de número con dos decimales y de porcentaje donde corresponda.  
6. Usa **formato condicional** para resaltar en rojo los márgenes menores del 40 %.

**Competencias:** cálculo comercial, comprensión de márgenes, uso de fórmulas básicas.

---

## Ejercicio 2. Buscar información del cliente y país

**Objetivo:** relacionar hojas mediante funciones de búsqueda.  
**Hojas:** sales_order_lines

### Pasos

1. Incluir el país de cliente 
1. En `operacions.xlsx`, añade una columna llamada **País del cliente**.  
2. Usa `BUSCARV` o `XLOOKUP` para buscar el país a partir del código o nombre del cliente:  
   
   ```excel
   =BUSCARV(??, lists!??, ?, FALSO)
   ```
4. Comprueba que no hay errores `#N/A` y corrige si es necesario.  
5. Guarda el archivo.

**Competencias:** integración de datos, comprensión de relaciones entre tablas.

---

## Ejercicio 3. Conversión de divisas

**Objetivo:** practicar operaciones con datos externos y uso de constantes absolutas.  
**Archivo:** `operacions_complet.xlsx`

### Pasos

1. Supón que el tipo de cambio EUR/USD es **1,10** (1 € = 1,10 $).  

2. En una nueva columna, convierte el importe total a dólares:  

   ```excel
   =Importe_total * $F$1
   ```


3. Muestra también el **importe total en euros** redondeado a 2 decimales:  

   ```excel
   =REDONDEAR(Importe_total/TipoCambio, 2)
   ```

4. Aplica formato de moneda distinto (€, $, £).

**Competencias:** operaciones con tipos de cambio, referencias absolutas.

---

## Ejercicio 4. Tablas dinámicas básicas

**Objetivo:** crear y analizar datos mediante tablas y gráficos dinámicos.  
**Archivo:** `operacions_complet.xlsx`

### Pasos

1. Inserta una **tabla dinámica** desde todo el rango de datos.  
2. Configura:
   - **Filas:** País del cliente  
   - **Valores:** Suma del importe total  
3. Inserta un **gráfico dinámico** (columna o circular).  
4. Cambia el estilo del gráfico (colores, títulos, etiquetas).  
5. Guarda el archivo.

**Competencias:** análisis de ventas por país, creación de gráficos.

---

## Ejercicio 5. Evolución de producción

**Objetivo:** trabajar con fechas y representar tendencias.  
**Hoja:** `plant_outputs`

### Pasos

1. Añade una columna **Año**:  

   ```excel
   =DIA(Fecha)
   ```

2. Crea una tabla dinámica con la suma de producción por dia.  
3. Inserta un **gráfico de líneas** para ver la evolución temporal.  
4. Añade formato condicional que marque en rojo las caídas de producción respecto al día anterior.  

   ```excel
   =SI(B3<B2,"↓","↑")
   ```
5. Guarda el archivo.

**Competencias:** análisis temporal, interpretación visual de datos.

---


