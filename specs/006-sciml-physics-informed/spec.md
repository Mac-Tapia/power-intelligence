# 006 — SciML: sustituto GNN informado por la física (y PINN) entrenado con VNR-GIS

**Estado:** propuesta, sin código. Paquetes: `power-sciml` (modelos, datasets, métricas) y `workers/ml-training` (entrenamiento GPU). Depende de 001 (VNR-GIS → snapshot), 004-A/B (etiquetas) y 029 (datos gold).

## Intención

Estimar en milisegundos tensiones, ángulos, corrientes y cargabilidad de alimentadores reales para cribar miles de escenarios (planificación, nueva carga, MADRL). El solver propio sigue siendo la verdad (ADR-0002): el modelo prioriza y el solver confirma.

## Terminología (sin sobreprometer)

- **GNN informado por la física:** aprende de las etiquetas del solver y se regulariza con el residuo de balance AC calculado con la Y-bus de dominio (AC-004-02). Es la técnica principal para flujo estacionario.
- **PINN estricto** (EDP con autodiferenciación): solo para dinámica o transitorios, en una fase posterior. Un flujo en régimen estacionario no se presenta como PINN.
- Una penalización física suave no garantiza que se cumpla la física. Toda predicción que sirva para decidir se verifica.

## Datos: redes reales del caso (dataset gold `vnr-pf-scenarios-<case_id>`, spec 029)

El entrenamiento se hace **con redes reales** de la empresa del caso. Los benchmarks IEEE y las redes sintéticas solo validan el motor y las pruebas unitarias, nunca entrenan. El método es universal (cualquier empresa ingestada con la spec 001). El piloto es `pe-ica-electrodunas`, con tres fuentes complementarias:

| Fuente | Registro | Aporte | Estado |
|---|---|---|---|
| TXT: exportación ASCII CYMDIST (RED, CARGA, BD_Equipo) | `eldu-cyme-ascii-2026-08` | topología de 96 alimentadores (38 681 nodos, 38 657 secciones), 7 287 cargas, R1/X1/ampacidad por código de conductor | estructura auditada; lector T001-T010 |
| MDB: bases de estudio por alimentador | `eldu-cyme-study-mdb` | modelos por alimentador para contrastar la topología TXT | pendiente de un lector Access autorizado (T001-T011) |
| VNR-GIS (SQL Server) | `eldu-vnrgis-2024-04` (+ parámetros) | inventario oficial, geometría UTM, `MaxDemTotal` por SED, estado de equipos | pendiente de restaurar (T001-T003) |

1. Los snapshots por alimentador se construyen con los lectores offline de la spec 001. La R/X sale del catálogo real (`BD_Equipo`, mapeado a `CodNorma`); lo no mapeable va a cuarentena y la muestra se descarta, nunca se completa.
2. Escenarios: demanda por carga o SED escalada con perfiles gold del caso (medidores 2023-2026), con el factor de potencia **declarado como supuesto de escenario** y variantes N-1 de interruptores.
3. Etiquetas: las produce el solver propio (Newton-Raphson, 004-B1; con transformadores tras 004-B2). Solo se aceptan muestras convergidas y con contraste por muestreo.
4. Cada muestra es un grafo (nodos: barras con kV y P/Q; aristas: R, X, longitud y estado) con sus etiquetas, `snapshot_sha256`, `scenario_id` y `source_id`.
5. La fuente de cada alimentador (TXT, MDB o VNR) queda registrada. Si dos fuentes describen el mismo alimentador, las diferencias de topología se reportan antes de entrenar.

## Criterios de aceptación

- AC-006-01: **split por alimentador** (grupos disjuntos train/valid/test) y además split temporal de escenarios. Se reporta el error OOD en alimentadores no vistos.
- AC-006-02: métricas frente al solver en test: error absoluto de tensión p95 ≤ 0,005 p.u. y detección de violaciones (V < 0,95 p.u. o carga > 100 %) con recall ≥ 0,99. Si no se alcanzan, el modelo no se habilita.
- AC-006-03: se reporta el residuo de balance AC de las predicciones por nodo. Las muestras con residuo mayor que el umbral se marcan "requiere solver".
- AC-006-04: modelo, dataset, código, semillas y versiones de librerías se registran con hash en un manifiesto de evidencia. Sin manifiesto no hay despliegue.
- AC-006-05: todo uso del sustituto que derive en una decisión confirma la alternativa ganadora con el solver propio, y la evidencia guarda ambos resultados.
- AC-006-06: se compara con líneas base (flujo DC linealizado, regresión sin grafo) para justificar el GNN. No se afirman aceleraciones sin benchmark (skill `unitesis-sciml-pinn-gnn`).

## Fuera de alcance

- Entrenar con datos no autorizados.
- Inferir R/X ausentes con la red neuronal.
- Controlar equipos.
