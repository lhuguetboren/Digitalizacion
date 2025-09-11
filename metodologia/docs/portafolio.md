# Portafoli de Digitalització — Bloc Plantacions

## Diagrama (actualitzat)

```mermaid
flowchart TD

    subgraph Plantaciones
        P1[Operaris de camp<br>Recol·lecció manual]
        P2[Control de qualitat bàsic]
    end
    subgraph Almacén
        A1[Empaquetat i classificació]
    end
    subgraph Transporte
        T1[Conductors i transportistes]
    end



    P1 -- "PDA/Tablet — Registre digital" --> O4
    P2 -- "PDA/Tablet — Control digital" -->O4
    O4 <-- "Transmissió de dades" --> T1
    O4 <-- "Transmissió de dades" --> A1

    subgraph Oficina
        O4[Suport IT<br>Integració amb base de dades]
    end



    %% Estils
    linkStyle 0,1,2 stroke:green,color:green,stroke-width:2px
```

## Portafoli — Substitució de Mòbils per PDA/Tablets

**Raons de substitució**

- Els mòbils/SMS només permeten comunicació bàsica i no garanteixen la traçabilitat digital.
- Les PDA/Tablets permeten recollida de dades en temps real, integració amb bases de dades i ús d’aplicacions sectorials.
- Millora la coordinació entre camp, transport, magatzem i oficina.

**Formació necessària**

- Operaris de camp: ****

- Responsables de qualitat: ****

- Equip IT: ****

**Costos estimats**

- Inversió inicial: ¿Quantitat?

- Software: ¿Quantitat?

- Formació: ¿Quantitat?

- Manteniment: ¿Quantitat?

**Beneficis**

- Traçabilitat completa: xxxx.
- Eficiència: yyy.
- Qualitat: zzz.
- Competitivitat: aaa.
- Estalvi: bbb.