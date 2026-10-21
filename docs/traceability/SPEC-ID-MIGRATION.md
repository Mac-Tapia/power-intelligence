# Migración de identificadores de spec

**Fecha:** 21/10/2026 · **Decisión:** el usuario aprobó adoptar como canónica la numeración del plan maestro (40 specs, 400 tareas) y consolidar sus specs en este repositorio.

Las tareas y criterios hechos con la numeración anterior se trasladaron a la spec canónica correspondiente. En cada `tasks.md` aparecen bajo "Avance incorporado de la numeración anterior" con su ID previo entre paréntesis; los criterios de aceptación previos están en `spec.md` bajo "Criterios vigentes incorporados (antes spec NNN)". Las specs 000-003, 010-015 y 020-027 conservan su ID: a su contenido previo se añadió el anexo del plan maestro.

## Carpetas

| Antes | Ahora |
|---|---|
| `004-simulation-engines` | `008-ac-solvers-and-validation` |
| `005-expansion-planning` | `018-planning-alternatives` |
| `006-sciml-physics-informed` | `029-sciml-pinn-gnn` |
| `007-safe-madrl` | `030-marl-llm-engineering-agents` |
| `008-llm-rag-tools` | `030-marl-llm-engineering-agents` |
| `009-industrialization` | `004-fullstack-runtime` |
| `029-training-dataset-foundation` | `035-authorized-data-federation` |

## Criterios de aceptación

`AC-<antes>-NN` pasa a `AC-<ahora>-<letra>NN`. Los sub-entregables locales `AC-009-L*` pasan a `AC-004-L*`.

| Prefijo anterior | Prefijo canónico |
|---|---|
| `AC-004-NN` | `AC-008-ANN` |
| `AC-005-NN` | `AC-018-ENN` |
| `AC-006-NN` | `AC-029-SNN` |
| `AC-007-NN` | `AC-030-MNN` |
| `AC-008-NN` | `AC-030-LNN` |
| `AC-009-NN` | `AC-004-INN` |
| `AC-029-NN` | `AC-035-DNN` |

## Tareas

| Antes | Ahora | Spec |
|---|---|---|
| `T004-A1` | `T008-A1` | `008-ac-solvers-and-validation` |
| `T004-A2` | `T006-A2` | `006-canonical-electrical-model` |
| `T004-A3` | `T008-A3` | `008-ac-solvers-and-validation` |
| `T004-A4` | `T006-A4` | `006-canonical-electrical-model` |
| `T004-B1` | `T008-B1` | `008-ac-solvers-and-validation` |
| `T004-B2` | `T008-B2` | `008-ac-solvers-and-validation` |
| `T004-C` | `T008-C` | `008-ac-solvers-and-validation` |
| `T004-D` | `T017-D` | `017-short-circuit-quality-reliability` |
| `T005-01` | `T018-E01` | `018-planning-alternatives` |
| `T005-02` | `T018-E02` | `018-planning-alternatives` |
| `T005-03` | `T028-E03` | `028-der-bess-ev-and-renewables` |
| `T005-04` | `T019-E04` | `019-multiobjective-optimization` |
| `T006-01` | `T029-S01` | `029-sciml-pinn-gnn` |
| `T006-02` | `T029-S02` | `029-sciml-pinn-gnn` |
| `T006-03` | `T029-S03` | `029-sciml-pinn-gnn` |
| `T006-04` | `T029-S04` | `029-sciml-pinn-gnn` |
| `T006-05` | `T029-S05` | `029-sciml-pinn-gnn` |
| `T006-06` | `T029-S06` | `029-sciml-pinn-gnn` |
| `T007-01` | `T030-M01` | `030-marl-llm-engineering-agents` |
| `T007-02` | `T030-M02` | `030-marl-llm-engineering-agents` |
| `T007-03` | `T030-M03` | `030-marl-llm-engineering-agents` |
| `T007-04` | `T030-M04` | `030-marl-llm-engineering-agents` |
| `T008-01` | `T030-L01` | `030-marl-llm-engineering-agents` |
| `T008-02` | `T030-L02` | `030-marl-llm-engineering-agents` |
| `T008-03` | `T030-L03` | `030-marl-llm-engineering-agents` |
| `T008-04` | `T030-L04` | `030-marl-llm-engineering-agents` |
| `T009-01` | `T005-I01` | `005-identity-tenant-authorization` |
| `T009-02` | `T007-I02` | `007-durable-jobs-and-events` |
| `T009-03` | `T031-I03` | `031-security-observability-operations` |
| `T009-04` | `T004-I04` | `004-fullstack-runtime` |
| `T009-L1` | `T007-L1` | `007-durable-jobs-and-events` |
| `T009-L2` | `T007-L2` | `007-durable-jobs-and-events` |
| `T009-L3` | `T031-L3` | `031-security-observability-operations` |
| `T009-L4` | `T005-L4` | `005-identity-tenant-authorization` |
| `T009-L5` | `T007-L5` | `007-durable-jobs-and-events` |
| `T009-L6` | `T031-L6` | `031-security-observability-operations` |
| `T029-01` | `T035-D01` | `035-authorized-data-federation` |
| `T029-02` | `T035-D02` | `035-authorized-data-federation` |
| `T029-03` | `T035-D03` | `035-authorized-data-federation` |
| `T029-04` | `T035-D04` | `035-authorized-data-federation` |
| `T029-05` | `T035-D05` | `035-authorized-data-federation` |
| `T029-06` | `T016-D06` | `016-demand-forecast-and-load-profiles` |
| `T029-07` | `T001-D07` | `001-vnrgis-ingestion` |
| `T029-08` | `T016-D08` | `016-demand-forecast-and-load-profiles` |
| `T029-09` | `T029-D09` | `029-sciml-pinn-gnn` |
| `T029-10` | `T030-D10` | `030-marl-llm-engineering-agents` |
| `T029-11` | `T014-D11` | `014-graphrag-knowledge` |
| `T029-12` | `T031-D12` | `031-security-observability-operations` |

## Alcances del solver

`004-A`, `004-B1`, `004-B2` y `004-C` pasan a `008-A`, `008-B1`, `008-B2` y `008-C`; `004-D` (cortocircuito) pasa a la spec 017.

## Identificadores que no cambian

Las claves de esquemas ya publicadas en evidencia (por ejemplo `gate_ac_006_02` en `unitesis.surrogate-evaluation/1`) se mantienen para no invalidar los hashes de evidencia; corresponden a `AC-029-S02`. Un cambio de clave exige una nueva versión de esquema.
