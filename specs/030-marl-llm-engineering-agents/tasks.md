# Tasks — SPEC-030: marl-llm-engineering-agents

## Backlog del plan maestro — tareas pendientes

**Gate:** G5 · **Depende de:** SPEC-019, SPEC-029, SPEC-015

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-030/T201** — Definir roles planner/operator/economics/research/reviewer y permisos de herramientas.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-030/T202** — Construir acciones/observaciones/recompensas multiobjetivo con validación de unidades.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-030/T203** — Implementar entorno MARL offline y baseline heurístico determinista.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-030/T204** — Integrar LLM local para traducir tareas a tools JSON autorizadas (sin ejecutar código libre).  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-030/T205** — Comparar políticas, seguridad, generalización y costos de inferencia contra baseline.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-030/T206** — Probar prompt injection, tool spoofing y operaciones físicas rechazadas.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-030/T207** — Contracts/negative permission tests  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-030/T208** — Integration and reproducibility evidence  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-030/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-030/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.

## Avance incorporado de la numeración anterior

- [ ] T030-M01: dataset gold sin oráculo (depende de T001-D07/08). _(antes T007-01)_
- [ ] T030-M02: envoltorio del entorno con acople a red (puerto PowerFlowEngine / SurrogateEngine). _(antes T007-02)_
- [ ] T030-M03: línea base por reglas y protocolo de evaluación con varias semillas. _(antes T007-03)_
- [ ] T030-M04: migrar desde los prototipos el algoritmo de referencia elegido, con procedencia y licencia. _(antes T007-04)_
- [ ] T030-L01: corpus citado (T030-D10) e índice léxico como línea base. _(antes T008-01)_
- [ ] T030-L02: herramientas tipadas definidas a partir del OpenAPI de control-api. _(antes T008-02)_
- [ ] T030-L03: set de evaluación y arnés (T014-D11). _(antes T008-03)_
- [ ] T030-L04: selección y medición del modelo local; LoRA solo si mejora AC-030-L03. _(antes T008-04)_
- [ ] T030-D10: gold `district-flex-pe-ica-electrodunas` desde clientes importantes y medidores reales; pronósticos causales. _(antes T029-10)_

## Destilación para agentes (ADR-0011)

- [ ] T030-K01: corpus de trazas de herramientas (CLI/API) cuyas respuestas numéricas produce el solver, con licencia y procedencia por traza.
- [ ] T030-K02: destilación paso a paso (explicaciones + llamadas a herramientas) hacia un modelo local pequeño; solo con un maestro cuya licencia permita entrenar con sus salidas, registrada antes del uso.
- [ ] T030-K03: evaluación frente a RAG + herramientas con la misma batería; se adopta el alumno solo si mejora y nunca responde números sin herramienta.
- [ ] T030-K04: destilación de políticas MARL (maestro centralizado → políticas descentralizadas pequeñas) con verificación AC por acción.
