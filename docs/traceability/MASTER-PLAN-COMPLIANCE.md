# Cumplimiento del plan maestro (40 specs, 400 tareas)

**Revisión:** 21/10/2026, sobre el árbol activo `power-intelligence` (commit `ab21dd4` más el trabajo sin commit de la sesión de plataforma, que se marca como tal).
**Insumos revisados (nivel raíz):** `PLAN_MAESTRO_UNITESIS_V9_SPECS_Y_TAREAS.md`, `TAREAS_MAESTRAS_UNITESIS_V9_MD.md`, `UNITESIS_V9_BACKLOG_400_TAREAS.csv`, `REFERENCIAS_ACTUALIZADAS_UNITESIS_V9_2.md` y la carpeta `unitesis-power-intelligence/`.
**Matriz por tarea:** [`master-backlog-assessment.csv`](master-backlog-assessment.csv) (estado y evidencia de cada una de las 400 tareas).

## Criterio

- **cumplida:** implementada y con prueba o evidencia en el repositorio.
- **parcial:** existe una parte verificable (citada); falta alcance.
- **pendiente:** no implementada.
- **bloqueada:** depende de una fuente o decisión externa.

Las tareas genéricas T207 a T210 se califican por área: pruebas negativas, evidencia de integración, revisión de referencias y aceptación. **T209 y T210 exigen revisión humana**, por eso quedan pendientes en todas las specs.

## Resultado global

| Ámbito | Cumplidas | Parciales | Pendientes | Bloqueadas |
|---|---|---|---|---|
| 400 tareas | 31 (8 %) | 178 (45 %) | 189 (47 %) | 2 |
| 240 tareas sustantivas (T201-T206) | 31 (13 %) | 104 (43 %) | 103 (43 %) | 2 |

| Gate | Cumplidas | Parciales | Pendientes | Bloqueadas |
|---|---|---|---|---|
| G0 entorno, seguridad, agentes | 8 | 22 | 10 | 0 |
| G1 datos, modelo, grafo, jobs | 4 | 27 | 19 | 0 |
| G2 GIS/unifilar, escenarios | 1 | 12 | 7 | 0 |
| G3 solvers, demanda, cortocircuito, benchmarks | 3 | 22 | 15 | 0 |
| G4 planificación, regulación, economía, informes | 14 | 58 | 66 | 2 |
| G5 DER, SciML, MARL/LLM, transmisión | 1 | 9 | 30 | 0 |
| G6 P2P, ledger, mercado, GraphRAG, federación | 0 | 20 | 30 | 0 |
| G7 operación y release | 0 | 8 | 12 | 0 |

**Conclusión:** el proyecto **no cumple todavía el plan maestro completo**. Cumple de forma verificable el núcleo eléctrico determinista, la ingesta real CYME, la cadena de evidencia, el gobierno de agentes y los bloqueos regulatorios. Están **sin implementar** DER/BESS/EV (028), MARL/LLM (030), cartera (033), transmisión (034), P2P/ledger/mercado (011-013), GraphRAG (014), frontend React, OIDC, cortocircuito y confiabilidad.

## Numeración (resuelta el 21/10/2026)

El usuario aprobó adoptar la numeración del plan maestro como canónica. Las 40 specs viven en `specs/` con el avance previo incorporado, y las equivalencias están en [`SPEC-ID-MIGRATION.md`](SPEC-ID-MIGRATION.md). La copia `unitesis-power-intelligence/` se eliminó tras comprobar que su contenido útil (las specs) ya estaba consolidado. Los estados de esta matriz se aplicaron a las casillas de cada `tasks.md`.

## Módulos (código real)

| Paquete | Líneas | Estado |
|---|---|---|
| power-adapters | 984 | operativo: JSON neutral, CYME ASCII, SQLite; PostgreSQL, jobs y Excel de la plataforma (sin commit) |
| power-application | 928 | operativo: estudio, nueva carga, alternativas, capacidad remanente, importación, datasets |
| power-simulation | 582 | operativo: BFS, Newton-Raphson (radial/mallado/trafos), Y-bus, contraste |
| power-domain | 453 | operativo: snapshot v2/v3 con identidad numérica estable |
| power-sciml | 434 | operativo: datasets, controles de calidad, escenarios, métricas; sin modelo aprendido |
| power-optimization | 224 | operativo: catálogo, cribado, Pareto |
| power-topology | 195 | operativo |
| power-economics / regulation / evidence / config / ports | 58-181 | operativos en su alcance |
| power-graph / ledger / market | 15-42 | ayudantes mínimos |
| power-agents / graphrag / marl / p2p | 1 | vacíos |

## Proyecto activo frente a sus propias specs

- 185 tareas: 61 hechas y 124 abiertas. Ninguna tarea hecha cita evidencia inexistente; 40 hechas son de registro documental, sin ruta citada.
- `verify_structure.py`: pasa. `ruff`: limpio.
- Pruebas: 241 pasan y 1 falla, `tests/integration/test_workstation_browser.py` (sesión de plataforma, sin commit). Su API responde correctamente; el fallo está en la UI autenticada.

## Hallazgos sobre los archivos del nivel raíz

1. **`unitesis-power-intelligence/` es una segunda copia del proyecto** (andamiaje V8.2 más las 40 carpetas de spec del plan maestro, unas 300 líneas de Python). Contradice la regla de una sola carpeta activa y reintroduce lo eliminado (`storage/`, `workers/`, `package.json`, el plan V8). Su contenido útil son las 40 specs del plan maestro. Recomendación: migrar esas specs a `power-intelligence/specs` con la numeración decidida y archivar o eliminar la copia.
2. Los cuatro documentos del plan maestro están **fuera del repositorio** y tienen versión en el nombre (V9). Si se adoptan, conviene integrar su contenido en `docs/` sin versión y mantener `master-backlog-assessment.csv` como estado vivo.
3. El plan pide **React+TypeScript, OpenDSS, OIDC y compose**, que hoy no existen. Son decisiones de alcance y dependencias que debe aprobar el usuario.

## Siguientes pasos por impacto

1. ~~Decidir la numeración canónica y consolidar las specs del plan maestro.~~ Hecho (ver arriba).
2. G3: trifásico desbalanceado (desbloquea 49 alimentadores reales), cortocircuito y benchmark desbalanceado.
3. G5-029: entrenar el GNN informado por la física (PyTorch ya disponible) y compararlo con la línea base.
4. G0/G1: integrar router y mapa (003), cerrar la UI autenticada que falla y commitear el lote de plataforma.
