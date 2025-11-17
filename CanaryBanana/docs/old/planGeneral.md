# Impacto Digital Proyectos

## Resumen Ejecutivo

Los proyectos ORG-DIG-02 y ORG-DIG-07 han marcado el inicio de un proceso de transformación digital en CanaryBanana Export. Aunque la empresa ha conseguido avances significativos en la organización y gestión de su información, la digitalización aún se encuentra en una fase inicial. Se han mejorado aspectos clave como la trazabilidad logística, la integración de datos entre áreas y la automatización parcial de los procesos administrativos. Sin embargo, persisten retos relacionados con la adopción del cambio, la capacitación del personal y la consolidación de una infraestructura tecnológica más madura. Este informe presenta los principales logros y dificultades observadas tras la puesta en marcha de los proyectos.

De los nuevos proyectos se han implementado un repositorio en la nube (**drive compartido**) y  se ha digitalizado la cadena logística y almacenes (**impresión de etiquetas y lectores de información desde la plantación al almacen** ).

![Digitalizacón inicio](img/im1.jpg)

## Desarrollo

Antes del despliegue de los proyectos de digitalización, CanaryBanana Export operaba con un nivel tecnológico muy básico.Las tareas administrativas, contables y logísticas se gestionaban de forma manual o mediante hojas de cálculo independientes. Esta fragmentación generaba duplicidades, errores en la documentación y lentitud en la coordinación entre departamentos. La falta de trazabilidad digital dificultaba la respuesta ante incidencias y limitaba la transparencia hacia los clientes internacionales.

Con los proyectos ORG-DIG-02 y ORG-DIG-07 se ha puesto en marcha una estructura inicial de gestión integrada, apoyada en modelos digitales de datos y operaciones. La implantación de un sistema de datos maestros ha permitido ordenar información básica sobre clientes, productos, puertos y plantas, creando una base común para las áreas de logística, finanzas y ventas. Este avance, aunque parcial, ha contribuido a mejorar la coherencia interna de los datos y a reducir los errores derivados de la gestión manual.

![Digitalizacón inicio](img/im2.jpg)

Uno de los progresos más visibles se encuentra en el control de las operaciones logísticas. La digitalización de pedidos y envíos ha introducido un sistema de seguimiento más sistemático, con estados que permiten conocer la evolución de cada envío. Aun así, la trazabilidad completa en tiempo real no se ha alcanzado, ya que la integración con los agentes externos y las navieras sigue dependiendo de intercambios manuales o de correos electrónicos. Este punto se identifica como un área prioritaria de mejora en futuras fases del proceso.

En el ámbito financiero, la automatización de las facturas y su vinculación con los pedidos ha permitido reducir parte del trabajo manual del personal administrativo. No obstante, el sistema aún requiere intervenciones frecuentes para la conciliación de pagos y la validación de datos. Los avances en este campo muestran un potencial claro, pero también evidencian la necesidad de consolidar procesos más estables y de dotar al personal de formación en el uso de las nuevas herramientas.

La migración hacia herramientas en la nube ha supuesto una mejora relevante en el acceso a la información, especialmente para el personal que trabaja entre distintas islas o en contacto con puertos internacionales. Sin embargo, la infraestructura de red y la conectividad no siempre garantizan un rendimiento óptimo. Persisten también dudas entre algunos empleados respecto a la seguridad y privacidad de los datos almacenados en entornos compartidos.

![Digitalizacón herramientas básicas](img/im3.jpg)

A nivel organizativo, los cambios tecnológicos han comenzado a modificar la dinámica interna. Algunos roles administrativos han evolucionado hacia funciones más analíticas, mientras que el área de IT ha adquirido mayor protagonismo como soporte a la gestión. 

No obstante, la adopción del cambio ha sido desigual: mientras parte del personal se adapta con rapidez, otros manifiestan dificultades en el manejo de las nuevas herramientas o cierta resistencia a abandonar los métodos tradicionales.

En conjunto, la digitalización ha permitido a la dirección disponer de una visión más clara de las operaciones, aunque el uso analítico de los datos sigue siendo incipiente. La empresa comienza a incorporar criterios de eficiencia y control basados en información integrada, pero aún debe avanzar hacia sistemas de análisis más automatizados y cuadros de mando operativos.

El impacto positivo de los proyectos es evidente, aunque limitado todavía por la falta de madurez tecnológica y por la necesidad de consolidar la cultura digital entre todos los equipos.

---

## Diagrama actualizado

```mermaid
flowchart TD

    %% ÁREAS
    subgraph Plantaciones
        P1[Operarios de campo<br>Registro digital inicial -tablets-]
        P2[Control de calidad digital<br>Conexión a Almacén]
    end

    subgraph Transporte
        T1[Conductores y transportistas<br>Rutas digitalizadas]
        T2[Traslado a empaquetado y puertos<br>Trazabilidad parcial]
    end

    subgraph Almacén
        A1[Empaquetado y clasificación<br>Control digital de lotes]
        A2[Control de calidad<br>Registro digital compartido]
    end

    subgraph "Digitalización de la Cadena Logística y Almacenes"
        D1[Integración Transporte-Almacén<br>Datos compartidos]
        D2[Seguimiento de mercancía<br>Estados actualizados por envío]
        D3[Control de inventario y trazabilidad<br>Datos en tiempo casi real]
    end

    subgraph Oficina
        O1[Dirección general<br>Visión consolidada de operaciones]
        O2[Finanzas y contabilidad<br>Automatización parcial de facturación]
        O3[Comercio internacional / ventas<br>Gestión digital de pedidos]
        O4[Soporte IT<br>Gestión en la nube y mantenimiento de sistemas]
    end

    subgraph Aduana
        AD1[Coordinación de envíos<br>Datos compartidos con logística]
        AD2[Gestión documental electrónica<br>Facturas y certificados]
        AD3[Intercambio con navieras<br>Correo y nube -pendiente integración-]
    end

    %% CONEXIONES PRINCIPALES
    P1 --> D1
    P2 --> D1
    D1 --> D2
    D2 --> D3
    D3 --> A1
    T1 --> D1
    T2 --> D3
    A1 --> AD1
    AD1 --> AD2
    AD2 --> O2
    O3 --> D1
    O4 --> D3



    %% ESTILOS
    linkStyle 0,1,5 stroke:green,color:green,stroke-width:2px
    linkStyle 2,3,4 stroke:green,color:green,stroke-width:2px
    linkStyle 6,7,8 stroke:green,color:green,stroke-width:2px
    linkStyle 9 stroke:gray,color:gray,stroke-width:2px
    linkStyle 10,11 stroke:purple,color:purple,stroke-width:2px
```

---

# Introducción a las TDH

Después de 15 años de crecimiento, CanaryBanana se ha consolidado como
una empresa agroexportadora reconocida en el mercado internacional. Su
trayectoria se ha apoyado en la calidad del producto, el esfuerzo del
personal y una logística capaz de conectar las plantaciones canarias con
los clientes europeos.

El análisis del estado actual revela que gran parte del trabajo diario
depende todavía de procesos manuales, documentos en papel, falta de
integración entre áreas y una limitada trazabilidad operativa. Estas
debilidades generan riesgos en tareas esenciales como calidad,
logística, documentación de exportación y toma de decisiones
financieras.

Sin embargo, la empresa ha dado sus primeros pasos firmes hacia la
modernización. Gracias a las mejoras asociadas a ORG-ED-02 y ORG-ED-07:

- La información de campo y almacén empieza a registrarse digitalmente.
- El flujo logístico incorpora estados y rutas más controladas.
- La documentación comienza a estandarizarse en formato electrónico.
- Los pedidos, facturación y cobros adoptan procesos digitales.
- Un repositorio en la nube mejora el acceso y la colaboración entre áreas.

Estas mejoras suponen una transición desde un entorno manual hacia una
digitalización básica conectada. Aun así, la integración completa, la
analítica avanzada y la trazabilidad total siguen siendo retos por
abordar.

> **CanaryBanana ha iniciado su transformación digital con una base
> positiva, pero aún queda un camino importante para lograr una
> integración plena e inteligente.**

Para dar continuidad a esta transformación, la dirección de CanaryBanana ha contratado a un equipo de consultores IT especializados en digitalización agroexportadora. Su misión consiste en diseñar un plan integral basado en dos pilares complementarios: la modernización tecnológica del proceso agro-bananero y la digitalización de la dimensión comercial e internacional. Este enfoque dual permitirá alinear producción, logística, calidad, exportación y análisis de datos dentro de un ecosistema digital coherente, escalable y orientado a la competitividad global.

**Negocios Internacionales Digitales: la dimensión externa**

Metas para competir y operar en mercados internacionales mediante tecnologías como IA, blockchain, IoT logístico, analítica y plataformas globales.

- Optimizar logística de exportación, documentación y trazabilidad.

- Aumentar transparencia con clientes europeos.

- Facilitar la internacionalización ágil, con menos trámites y más
información en tiempo real.
- Mejorar personalización, competitividad y acceso a mercados.

>**Visión comercial--logística--estratégica**

**Transformación Digital Agro-Bananera: la dimensión interna**

Metas en la producción agrícola y en cómo digitalizar
todo el proceso operativo:

- IoT agrícola, drones, riego inteligente, gemelo digital.

- IA para predicción de rendimientos y planificación.

- Blockchain para garantizar calidad y seguridad alimentaria.

- ERP agrícola + SCM para integrar toda la cadena productiva.

>**Es la visión operativa--productiva--técnica**

## Tecnologías Habilitadoras Digitales para Agro-Bananera

### Ámbito de producción y eficiencia operativa

- **IoT agrícola:** sensores de suelo, humedad, temperatura,
    nutrientes y radiación.
- **Teledetección y drones:** imágenes multiespectrales, NDVI,
    detección de estrés hídrico y plagas.
- **Gemelo digital:** simulación virtual de plantaciones y escenarios
    de manejo.
- **Automatización y robótica:** maquinaria inteligente para riego,
    poda y recolección.
- **Riego inteligente:** control automático con datos IoT y
    predicciones meteorológicas.
- **Automatización energética:** control del consumo e integración con
    energías renovables (fotovoltaica).

### Ámbito de gestión y análisis de datos

- **ERP agrícola:** registro centralizado de costes, lotes,
    rendimientos y operaciones.
- **Big Data agrícola:** lago de datos unificado para integrar
    información de sensores, clima y producción.
- **Inteligencia Artificial (IA):** predicción de rendimientos,
    plagas, eficiencia hídrica y logística.
- **Dashboards y BI:** visualización de indicadores clave (KPIs) de
    producción, costes, eficiencia y sostenibilidad.

### Ámbito de trazabilidad, seguridad y sostenibilidad

- **Blockchain alimentaria:** registro inmutable de la cadena productiva y logística.
- **SCM (Supply Chain Management):** coordinación de proveedores,transporte y distribución.
- **Certificación digital y ESG:** integración con normas GlobalG.A.P,
    ISO 22000, Rainforest Alliance.
- **IoT logístico:** sensores de cadena de frío, GPS, temperatura yhumedad en transporte.
- **Economía circular digital:** plataformas para reutilizar residuosagrícolas (biogás, compost).
- **Monitorización ambiental:** seguimiento automático de emisiones,agua, energía y residuos.

## Diagramas agro-bananera

``` mermaid
flowchart TB
 subgraph NEG_INT["-"]
         E1["Líneas de trabajo"]

    B1[Productividad Agrícola]
    B2[Eficiencia en el uso de recursos naturales]
    B3[Trazabilidad y Seguridad Alimentaria]
  end
 subgraph TECNOL["-"]
        E3["Tecnología"]
        C1A[IoT, Drones, IA, ERP, Gemelo Digital]
        C2A[IoT hídrico, Riego inteligente, Energía solar, Economía circular]
        C3A[ERP, Blockchain, IoT logístico, SCM, IA]
  end

 subgraph MECANISMOS["-"]
        E4["Mecanismos"]
    C1B[Monitoreo, Predicción, Automatización, Aprendizaje]
    C2B[Medición, Optimización, Reutilización, Transparencia]
    C3B[Registro, Control, Auditorías, Respuesta rápida]
  end

 subgraph IMPACTOS["-"]
        E5["Impactos"]
    C1C[Mayor rendimiento y menor variabilidad]
    C2C[Ahorro de recursos, sostenibilidad y reducción de costes]
    C3C[Calidad, Confianza, Cumplimiento y Competitividad]
  end
    B1 --> C1A
    B2 --> C2A
    B3 --> C3A
    C1A --> C1B
    C2A --> C2B
    C3A --> C3B
    C1B --> C1C
    C2B --> C2C
    C3B --> C3C
   

    classDef espaciador fill:transparent,stroke:transparent
    classDef negocios fill:#BBDEFB,stroke:#1565C0,color:#0D47A1,stroke-width:3.5px,rx:8,ry:8
    classDef tecnos fill:#C8E6C9,stroke:#2E7D32,color:#1B5E20,stroke-width:3.px,rx:8,ry:8
    classDef impactos fill:#FFE0B2,stroke:#EF6C00,color:#E65100,stroke-width:3.5px,rx:8,ry:8
    style NEG_INT fill:#E3F2FD,stroke:#2196F3,stroke-width:2px,rx:10,ry:10,margin-top:30px
    style TECNOL fill:#E8F5E9,stroke:#43A047,stroke-width:2px,rx:10,ry:10
    style IMPACTOS fill:#FFF3E0,stroke:#FB8C00,stroke-width:2px,rx:10,ry:10


```

### Productividad Agrícola

``` mermaid
mindmap
  ((Productividad Agrícola))
    Tecnologías
      IoT[Sensores de suelo, clima y humedad]
      Drones[Teledetección y NDVI]
      IA[Modelos predictivos y Big Data]
      Robots[Automatización de tareas]
      Gemelo[Gemelo digital de la plantación]
      ERP[ERP agrícola y dashboards]
    Mecanismos
      Monitoreo[Monitoreo continuo]
      Predicción[Predicción de crecimiento y plagas]
      Precisión[Aplicación precisa de agua y nutrientes]
      Automatización[Ejecución automatizada]
      Aprendizaje[Análisis de históricos]
    Impacto
      Rendimiento[Mayor rendimiento y calidad]
      Variabilidad[Menor variabilidad y pérdidas]
```


### Eficiencia en el Uso de Recursos Naturales

``` mermaid
mindmap
  ((Eficiencia en el uso de recursos naturales))
    Tecnologías
      IoT[Sensores de suelo y nutrientes]
      Drones[Teledetección / NDVI hídrico]
      Riego[Riego inteligente automatizado]
      IA[Modelos predictivos de eficiencia]
      Energía[Automatización energética / solar]
      Circular[Economía circular digital]
      ESG[Monitorización ambiental / ESG]
    Mecanismos
      Medición[Control en tiempo real]
      Predicción[Predicción de necesidades]
      Optimización[Optimización de recursos]
      Reutilización[Reutilización de subproductos]
      Transparencia[Seguimiento ambiental]
    Impacto
      Ahorro[Ahorro de agua y energía]
      Reducción[Reducción de residuos y emisiones]
      Sostenibilidad[Sostenibilidad y cumplimiento]
      Coste[Menores costes operativos]
```

------------------------------------------------------------------------

#### Trazabilidad y Seguridad Alimentaria

``` mermaid
mindmap
  ((Trazabilidad y Seguridad Alimentaria))
    Tecnologías
      ERP[ERP agrícola integrado]
      Blockchain[Blockchain alimentaria]
      IoT[Sensores de cadena de frío / GPS]
      IA[Análisis predictivo y Big Data]
      SCM[Gestión de cadena de suministro]
      Certificación[Certificación digital ESG y normas UE]
      Dashboards[Visores y portales de trazabilidad]
    Mecanismos
      Registro[Registro digital completo]
      Transparencia[Transparencia verificable]
      Control[Control en tiempo real]
      Auditorías[Auditorías automatizadas]
      Respuesta[Respuesta rápida ante incidencias]
    Impacto
      Calidad[Seguridad y calidad garantizada]
      Confianza[Confianza del cliente y mercado]
      Cumplimiento[Cumplimiento normativo UE]
      Competitividad[Ventaja comercial y acceso a mercados]
```

## Tecnologías Habilitadoras Digitales para Negocios internacionales

- **Inteligencia Artificial (IA):** automatiza análisis predictivos, mejora la toma de decisiones y permite personalización avanzada.
- **Big Data y Analítica Avanzada:** transforma datos globales en conocimiento accionable.
- **Blockchain:** garantiza transparencia, trazabilidad y seguridad en transacciones internacionales.
- **Internet de las Cosas (IoT):** permite monitoreo en tiempo real de mercancías y procesos logísticos.
- **Automatización y Robótica:** optimizan flujos de trabajo y reducen tiempos operativos.
- **Plataformas de Comercio Electrónico Global:** facilitan la entrada de PYMES en mercados internacionales.
- **Economía Circular y Sostenibilidad:** integran prácticas responsables en la cadena global de valor.

## Diagramas Negocios internacionales 

``` mermaid
flowchart TB
 subgraph NEG_INT["-"]
         E1["Líneas <br>de trabajo"]

        A1["Internacionalización ágil y accesible"]
        A2["Eficiencia logística y documental"]
        A3["Competitividad y personalización"]
  end
 subgraph TECNOL["-"]
        E3["Tecnologías <br>emergentes"]
        B1["Plataformas globales<br>IA · Blockchain"]
        B2["IoT · Robótica · ERP· Blockchain"]
        B3["Big Data · CRM · Analítica predictiva"]
  end
 subgraph IMPACTOS["-"]
        E2["Impactos en los<br> negocios internacionales"]
        C1["Acceso global<br>y democratización"]
        C2["Optimización logística<br>y trazabilidad"]
        C3["Diferenciación<br>y fidelización"]
  end
    A1 --> B1
    A2 --> B2
    A3 --> B3
    B1 --> C1
    B2 --> C2
    B3 --> C3

   
     A1:::negocios
     A2:::negocios
     A3:::negocios
     B1:::tecnos
     B2:::tecnos
     B3:::tecnos
     C1:::impactos
     C2:::impactos
     C3:::impactos
    classDef espaciador fill:transparent,stroke:transparent
    classDef negocios fill:#BBDEFB,stroke:#1565C0,color:#0D47A1,stroke-width:3.5px,rx:8,ry:8
    classDef tecnos fill:#C8E6C9,stroke:#2E7D32,color:#1B5E20,stroke-width:3.px,rx:8,ry:8
    classDef impactos fill:#FFE0B2,stroke:#EF6C00,color:#E65100,stroke-width:3.5px,rx:8,ry:8
    style NEG_INT fill:#E3F2FD,stroke:#2196F3,stroke-width:2px,rx:10,ry:10,margin-top:30px
    style TECNOL fill:#E8F5E9,stroke:#43A047,stroke-width:2px,rx:10,ry:10
    style IMPACTOS fill:#FFF3E0,stroke:#FB8C00,stroke-width:2px,rx:10,ry:10


```

### La internacionalización más ágil y accesible

``` mermaid
mindmap
 ((Internacionalización ágil y accesible))
    Tecnologías
      Plataformas digitales de comercio global
      ERP gestión
      Blockchain para contratos inteligentes
      Inteligencia Artificial aplicada a análisis de mercados
    Mecanismos
      Simplificación de trámites de exportación
      Integración de marketplaces internacionales
      Modelos de negocio digitales para PYMES
    Impactos
      Acceso democratizado a mercados globales
      Reducción de costos y tiempos de internacionalización
      Incremento en la participación de PYMES exportadoras
```

### La eficiencia en la gestión logística y documental

``` mermaid
mindmap
  ((Eficiencia logística y documental))
    Tecnologías
      Internet de las Cosas (IoT)
      Robótica y automatización de almacenes
      Blockchain para trazabilidad
    Mecanismos
      Digitalización de aduanas y documentación
      Seguimiento en tiempo real de envíos
      Sistemas de gestión documental inteligente
    Impactos
      Reducción de errores y fraudes
      Optimización de rutas y tiempos de entrega
      Mayor transparencia y control en la cadena logística
```

### La mejora de la competitividad y personalización de servicios

``` mermaid
mindmap
  ((Competitividad y personalización))
    (Tecnologías)
      Big Data y analítica predictiva
      Inteligencia Artificial -IA- y machine learning
      Plataformas CRM y automatización del marketing
    Mecanismos
      Segmentación avanzada de clientes
      Optimización de precios dinámicos
      Personalización de experiencias postventa
    Impactos
      Incremento de la lealtad del cliente
      Mejora en la toma de decisiones comerciales
      Aumento del valor percibido y del margen competitivo
```

-->Re

# Fases de aplicación de TDH

```mermaid
flowchart TB
    F1["Fase 1<br>Digitalización básica"]

 subgraph TECNOL["Tecnologías"]
    T1_1["Documentación digital<br>(facturas, pedidos, albaranes)"]
    T1_2["Ofimática en nube<br>(carpetas compartidas)"]
    T1_3["Registros digitales básicos<br>(Excel · ERP inicial)"]
 end

 subgraph IMPACTOS["Impactos"]
    I1_1["Menos papel y menos errores administrativos"]
    I1_2["Información más ordenada y accesible"]
    I1_3["Primer paso para integrar áreas en el futuro"]
 end

 F1 --> T1_1
 F1 --> T1_2
 F1 --> T1_3

 T1_1 --> I1_1
 T1_2 --> I1_2
 T1_3 --> I1_2
 T1_3 --> I1_3


```

```mermaid

flowchart TB
    F2["Fase 2<br>Integración operativa"]

 subgraph TECNOL["Tecnologías"]
    T2_1["Integración IT–OT<br>(oficina + planta + logística)"]
    T2_2["IoT agrícola e hídrico<br>(sensores de campo y riego)"]
    T2_3["ERP · SCM<br>para coordinar producción, almacén y transporte"]
 end

 subgraph IMPACTOS["Impactos"]
    I2_1["Flujo de información entre producción, almacén y oficina"]
    I2_2["Menos duplicidad de datos<br>y menos tareas repetitivas"]
    I2_3["Base para coordinar mejor la logística y la exportación"]
 end

 F2 --> T2_1
 F2 --> T2_2
 F2 --> T2_3

 T2_1 --> I2_1
 T2_1 --> I2_2
 T2_2 --> I2_1
 T2_3 --> I2_1
 T2_3 --> I2_3
```

```mermaid

flowchart TB
    F3["Fase 3<br>Trazabilidad completa y logística inteligente"]

 subgraph TECNOL["Tecnologías"]
    T3_1["IoT logístico<br>(cadena de frío, GPS, sensores en transporte)"]
    T3_2["Blockchain alimentaria<br>para trazabilidad de lote a cliente"]
    T3_3["ERP + SCM<br>integrando almacén, transporte y puertos"]
 end

 subgraph IMPACTOS["Impactos"]
    I3_1["Trazabilidad de lote<br>desde finca hasta cliente europeo"]
    I3_2["Seguridad alimentaria y cumplimiento normativo UE"]
    I3_3["Mayor visibilidad logística<br>y respuesta rápida ante incidencias"]
 end

 F3 --> T3_1
 F3 --> T3_2
 F3 --> T3_3

 T3_1 --> I3_1
 T3_1 --> I3_3
 T3_2 --> I3_1
 T3_2 --> I3_2
 T3_3 --> I3_1
 T3_3 --> I3_3

```

```mermaid
flowchart TB
    F4["Fase 4<br>Decisiones basadas en datos (Data-Driven)"]
 

 subgraph TECNOL["Tecnologías"]
    T4_1["Big Data agrícola<br>(datos de IoT, clima, producción)"]
    T4_2["Analítica avanzada · BI<br>(cuadros de mando)"]
    T4_3["Inteligencia Artificial (IA)<br>para predicción de rendimientos y demanda"]
 end

 subgraph IMPACTOS["Impactos"]
    I4_1["Mejor planificación de cosechas y envíos"]
    I4_2["Decisiones de producción, logística y precios basadas en datos"]
    I4_3["Optimización de costes<br>y reducción de desperdicio"]

 end

 F4 --> T4_1
 F4 --> T4_2
 F4 --> T4_3

 T4_1 --> I4_1
 T4_1 --> I4_2
 T4_2 --> I4_2
 T4_2 --> I4_3
 T4_3 --> I4_1
 T4_3 --> I4_3
```

```mermaid
flowchart TB
    F5["Fase 5<br>Ecosistema digital avanzado"]

 subgraph TECNOL["Tecnologías"]
    T5_1["Gemelo digital<br>de plantaciones y operaciones"]
    T5_2["Drones y teledetección avanzada"]
    T5_3["Riego inteligente e IoT hídrico<br>con energía solar"]
    T5_4["Automatización y robótica<br>en riego, poda y recolección"]
    T5_5["Economía circular digital<br>y monitorización ambiental"]

 end

 subgraph IMPACTOS["Impactos"]
    I5_1["Operación predictiva y automatizada"]
    I5_2["Mayor rendimiento con menor variabilidad"]
    I5_3["Ahorro de agua y energía<br>+ reducción de residuos"]
    I5_4["Sostenibilidad y certificaciones ESG"]
    I5_5["Alta competitividad y confianza<br>en mercados internacionales"]
 end

 F5 --> T5_1
 F5 --> T5_2
 F5 --> T5_3
 F5 --> T5_4
 F5 --> T5_5

 T5_1 --> I5_1
 T5_1 --> I5_2
 T5_2 --> I5_2
 T5_2 --> I5_5
 T5_3 --> I5_3
 T5_3 --> I5_4
 T5_4 --> I5_1
 T5_4 --> I5_2
 T5_5 --> I5_3
 T5_5 --> I5_4
 T5_5 --> I5_5

```