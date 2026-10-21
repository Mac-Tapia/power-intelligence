# 006 — SciML: sustituto GNN informado por la física (y PINN) entrenado con VNR-GIS

**Estado:** propuesta, sin código. Paquetes: `power-sciml` (modelos, datasets, métricas) y `workers/ml-training` (entrenamiento GPU). Depende de 001 (VNR-GIS → snapshot), 004-A/B (etiquetas) y 029 (datos gold).

## Intención

Estimar en milisegundos tensiones, ángulos, corrientes y cargabilidad de alimentadores reales para cribar miles de escenarios (planificación, nueva carga, MADRL). El solver propio sigue siendo la verdad (ADR-0002): el modelo prioriza y el solver confirma.

## Terminología (sin sobreprometer)

- **GNN informado por la física:** aprende de las etiquetas del solver y se regulariza con el residuo de balance AC calculado con la Y-bus de dominio (AC-004-02). Es la técnica principal para flujo estacionario.
- **PINN estricto** (EDP con autodiferenciación): solo para dinámica o transitorios, en una fase posterior. Un flujo en régimen estacionario no se presenta como PINN.
- Una penalización física suave no garantiza que se cumpla la física. Toda predicción que sirva para decidir se verifica.

## Datos (dataset gold `vnr-pf-scenarios-<case_id>`, spec 029)

El método es universal: sirve para cualquier empresa cuyo inventario se ingeste con la spec 001. El caso piloto de entrenamiento y pruebas es `pe-ica-electrodunas` (VNR-GIS Electro Dunas, abr‑2024).

1. Snapshots por alimentador desde VNR-GIS (`mtSalida`, `mtTramo`, `mtEquipo`, `Sed`), con el mapeo `CodNorma` → catálogo de conductores versionado y con fuente. Lo que no se pueda mapear va a cuarentena.
2. Escenarios: demanda por SED = `MaxDemTotal` × perfil normalizado (forecast gold) × factor de potencia **declarado como supuesto de escenario**; variantes N-1 de interruptores.
3. Etiquetas: las produce el solver propio. Solo se aceptan muestras convergidas y con contraste por muestreo.
4. Cada muestra es un grafo (nodos: barras con kV y P/Q; aristas: R, X, longitud y estado) más sus etiquetas, `snapshot_sha256` y `scenario_id`.

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
