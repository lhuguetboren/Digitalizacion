flowchart TD
    %% =====================================================
    %% ESQUEMA GENERAL
    %% =====================================================
    subgraph G[Esquema General: CanaryExport]
        A[CanaryExport]:::principal

        subgraph Actores
            B[Empresa 1]
            C[Empresa 2]
            D[Empresa 3]
        end

        subgraph Areas
            R1[RA1 Diagnóstico digitalización]
            R2[RA2 Tecnologías habilitadoras]
            R3[RA3 Cloud y Edge]
            R4[RA4 Inteligencia Artificial]
            R5[RA5 Datos y Ciberseguridad]
        end

        subgraph Salidas
            F[RA6-informe final]
        end

        B --> R1 & R2 & R3 & R4 & R5
        C --> R1 & R2 & R3 & R4 & R5
        D --> R1 & R2 & R3 & R4 & R5
        R1 & R2 & R3 & R4 & R5  --> F
    end

    classDef principal fill:#ffd54f,stroke:#9c6b00,stroke-width:2px,color:#202020;


flowchart TD
    %% Simulación de digitalización competitiva
    A[Inicio de simulación] --> B[Formación de empresas/grupos<br/>y asignación de presupuesto inicial]
    B --> C[Briefing de reglas y métricas<br/> Objetivos, Costos, Rentabilidad, Clima]
    
    %% RA1
    C --> RA1
    subgraph RA1[RA1 · Diagnóstico y visión de digitalización]
        direction TB
        R1A[Actividades según RA1] --> R1D[Decisiones de inversión y ejecución]
        R1D --> R1O[Objetivos]
        R1D --> R1C[Costos]
        R1D --> R1R[Rentabilidad]
        R1D --> R1CL[Clima laboral]
        R1O --> R1RES[Resultados RA1]
        R1C --> R1RES
        R1R --> R1RES
        R1CL --> R1RES
    end
    RA1 --> COMP1[Comparativa entre empresas tras RA1<br/>• Objetivos cumplidos • Presupuesto restante<br/>• ROI parcial • Clima laboral]
    
    %% RA2
    COMP1 --> RA2
    subgraph RA2[RA2 · Tecnologías habilitadoras digitales THD]
        direction TB
        R2A[Actividades según RA2] --> R2D[Decisiones de inversión y ejecución]
        R2D --> R2O[Objetivos]
        R2D --> R2C[Costos]
        R2D --> R2R[Rentabilidad]
        R2D --> R2CL[Clima laboral]
        R2O --> R2RES[Resultados RA2]
        R2C --> R2RES
        R2R --> R2RES
        R2CL --> R2RES
    end
    RA2 --> COMP2[Comparativa tras RA2]

    %% RA3
    COMP2 --> RA3
    subgraph RA3[RA3 · Cloud/Fog/Edge y conectividad]
        direction TB
        R3A[Actividades según RA3] --> R3D[Decisiones de inversión y ejecución]
        R3D --> R3O[Objetivos]
        R3D --> R3C[Costos]
        R3D --> R3R[Rentabilidad]
        R3D --> R3CL[Clima laboral]
        R3O --> R3RES[Resultados RA3]
        R3C --> R3RES
        R3R --> R3RES
        R3CL --> R3RES
    end
    RA3 --> COMP3[Comparativa tras RA3]

    %% RA4
    COMP3 --> RA4
    subgraph RA4[RA4 · Aplicaciones de IA en el sector]
        direction TB
        R4A[Actividades según RA4] --> R4D[Decisiones de inversión y ejecución]
        R4D --> R4O[Objetivos]
        R4D --> R4C[Costos]
        R4D --> R4R[Rentabilidad]
        R4D --> R4CL[Clima laboral]
        R4O --> R4RES[Resultados RA4]
        R4C --> R4RES
        R4R --> R4RES
        R4CL --> R4RES
    end
    RA4 --> COMP4[Comparativa tras RA4]

    %% RA5
    COMP4 --> RA5
    subgraph RA5[RA5 · Datos, protección y ciberseguridad]
        direction TB
        R5A[Actividades según RA5] --> R5D[Decisiones de inversión y ejecución]
        R5D --> R5O[Objetivos]
        R5D --> R5C[Costos]
        R5D --> R5R[Rentabilidad]
        R5D --> R5CL[Clima laboral]
        R5O --> R5RES[Resultados RA5]
        R5C --> R5RES
        R5R --> R5RES
        R5CL --> R5RES
    end
    RA5 --> COMP5[Comparativa tras RA5]

    %% RA6 y cierre
    COMP5 --> RA6
    subgraph RA6[RA6 · Proyecto integrador de transformación digital]
        direction TB
        R6A[Diseño y ejecución del plan integral] --> R6D[Decisiones finales y priorización]
        R6D --> R6O[Objetivos]
        R6D --> R6C[Costos]
        R6D --> R6R[Rentabilidad]
        R6D --> R6CL[Clima laboral]
        R6O --> R6RES[Resultados RA6]
        R6C --> R6RES
        R6R --> R6RES
        R6CL --> R6RES
    end

    RA6 --> PORT[Portafolio final<br/>compila todos los trabajos y evidencias]
    PORT --> SCORE[Puntuación global<br/>• ROI acumulado • Cumplimiento de objetivos<br/>• Clima laboral promedio • Calidad del portafolio]
    SCORE --> RANK[Ranking final y empresa ganadora]




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

