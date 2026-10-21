# Tasks — SPEC-007: durable-jobs-and-events

## Backlog del plan maestro — tareas pendientes

**Gate:** G1 · **Depende de:** SPEC-004, SPEC-005

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-007/T201** — Definir estados queued/running/succeeded/failed/cancelled y transición permitida.  
  **Estado:** parcial · **Evidencia:** queued/running/finished/failed (sin commit, sesión de plataforma); sin cancelled · **Responsable:** por asignar
- [ ] **SPEC-007/T202** — Implementar outbox transaccional y consumidor idempotente con claves de deduplicación.  
  **Estado:** parcial · **Evidencia:** enqueue idempotente y claim atómico (sin commit, sesión de plataforma); sin outbox · **Responsable:** por asignar
- [ ] **SPEC-007/T203** — Crear worker de prueba con límites, timeouts, cancelación y reintentos exponenciales.  
  **Estado:** pendiente · **Evidencia:** ejecución en proceso; sin worker con timeouts/reintentos · **Responsable:** por asignar
- [ ] **SPEC-007/T204** — Implementar API de colas, consulta de eventos y cuotas por tenant.  
  **Estado:** parcial · **Evidencia:** API de jobs; sin eventos ni cuotas · **Responsable:** por asignar
- [ ] **SPEC-007/T205** — Probar caída de worker, reinicio, doble entrega, cancelación y artefactos incompletos.  
  **Estado:** parcial · **Evidencia:** recuperación tras reinicio y doble claim probados (sin commit, sesión de plataforma) · **Responsable:** por asignar
- [ ] **SPEC-007/T206** — Medir latencias y auditar la identidad que disparó cada job.  
  **Estado:** pendiente · **Evidencia:** sin métricas de latencia ni auditoría de identidad por job · **Responsable:** por asignar
- [ ] **SPEC-007/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-007/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-007/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-007/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.

## Avance incorporado de la numeración anterior

- [ ] T007-I02: adaptador PostgreSQL y cola de jobs. _(antes T009-02)_
- [x] T007-L1: `SqliteJobRepository`, claim atómico, estados terminales protegidos y recuperación running→failed/interrupted (`tests/unit/test_job_repository.py`). _(antes T009-L1)_
- [x] T007-L2: API consume el puerto de jobs, conserva solicitudes y resultados al reabrir (`tests/integration/test_durable_jobs.py`: estudio, nueva carga y alternativas). _(antes T009-L2)_
- [x] T007-L5: repositorio y claim atómico PostgreSQL/PostGIS reales; API encola, CLI worker ejecuta en otro proceso y API reabierta relee resultados (`test_postgres.py`). Falta recuperación coordinada de workers interrumpidos para cerrar T007-I02. _(antes T009-L5)_
