# Primer paso hacia la digitalización

Tras revisar el estado de la empresa, se decidio que el primer paso era organizar la información con una herramienta simple pero potente para empezar a sustituir procesos manuales. Este primer paso deberá ayudarnos a conocer los procesos y detectar las necesidades. IT ha generado un conjunto de hojas excel que deberemos conocer.

Este es el estado de la empresa que intenta documentar esta primera aplicación.

``` mermaid

flowchart TD

    %% ÁREAS
    subgraph Plantaciones
        P1[Operarios de campo<br>Recolección manual]
        P2[Control de calidad básico]
    end

    subgraph Transporte
        T1[Conductores y transportistas<br>Gestión manual de rutas]
        T2[Traslado a empaquetado y puertos]
    end

    subgraph Almacén
        A1[Empaquetado y clasificación]
        A2[Control de calidad<br>Registros en papel]
    end

    subgraph Oficina
        O1[Dirección general]
        O2[Finanzas y contabilidad<br>Software contable básico]
        O3[Comercio internacional / ventas<br>Programas ofimáticos]
        O4[Soporte IT - 2 técnicos<br>Red local interna -LAN]
    end

    subgraph Aduana
        AD1[Coordinación de envíos]
        AD2[Gestión documental<br> Manual -facturas, certificados-]
        AD3[Contacto con navieras y autoridades]
    end

    %% RELACIONES + TECNOLOGÍA USADA
    P1 -- "Registros en papel" --> T1
    P2 -- "Registros en papel" --> T1

    %% Uso de móviles/SMS
    P1 -- "Móviles / SMS" --> T1
    T1 -- "Móviles / SMS" --> AD1
    A1 -- "Móviles / SMS" --> O2
    A1 -- "Móviles / SMS" --> O3
    T1 -- "Sin trazabilidad digital" --> A1
    T2 -- "Procesos manuales" --> A1

    A1 -- "Listados manuales" --> A2
    A2 -- "Documentación manual" --> AD1
    
    AD1 -- "Archivos ofimáticos" --> AD2
    AD2 -- "Tramitación manual" --> AD3

    O1 -- "Ofimática" --> O3
    O1 -- "Ofimática" --> O2

    O2 -- "Software contable básico" --> AD2
    O3 -- "Ofimática vía LAN" --> AD1

    O4 -- "Soporte LAN intern<br>(sin acceso remoto)" --> O2
    O4 -- "Soporte LAN interna" --> O3

    %% LEYENDA
    subgraph Leyenda [Leyenda Tecnologías]
        L1[🟤 Papel / registros manuales]
        L2[🔵 Móviles / SMS]
        L3[⚪ Procesos manuales -sin digitalización-]
        L4[🟢 Ofimática]
        L5[🟠 Software contable básico]
        L6[🟣 Red local interna -LAN-]
    end
 AD3 -.-> Leyenda
    %% ESTILOS
    %% Papel -> marrón
    linkStyle 0,1,6,7 stroke:brown,color:brown,stroke-width:2px
    %% Móviles / SMS -> azul
    linkStyle 2,3 stroke:blue,color:blue,stroke-width:2px
    %% Manual / procesos sin digitalización -> gray
    linkStyle 4,5,9 stroke:gray,color:gray,stroke-width:2px
    %% Ofimática -> green
    linkStyle 8,10 stroke:green,color:green,stroke-width:2px
    %% Software contable -> orange
    linkStyle 11 stroke:orange,color:orange,stroke-width:2px
    %% LAN interna -> purple
    linkStyle 12,13 stroke:purple,color:purple,stroke-width:2px
```