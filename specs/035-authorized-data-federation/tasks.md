# Tasks — SPEC-035: authorized-data-federation

## Backlog del plan maestro — tareas pendientes

**Gate:** G6 · **Depende de:** SPEC-001, SPEC-005, SPEC-007

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-035/T201** — Definir adaptadores para SQL Server/PostgreSQL y backups autorizados con clasificación de datos.  
  **Estado:** parcial · **Evidencia:** registro de fuentes con sensibilidad; postgres_repository (sin commit, sesión de plataforma) · **Responsable:** por asignar
- [ ] **SPEC-035/T202** — Establecer conectores de solo lectura, políticas de red y control de credenciales.  
  **Estado:** parcial · **Evidencia:** política MCP Postgres RO de ejemplo · **Responsable:** por asignar
- [ ] **SPEC-035/T203** — Construir incremental ingest por watermark y hashes para auditar cambios.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-035/T204** — Aislar sincronización de mediciones, activos GIS y metadatos con linaje.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-035/T205** — Probar alteración de esquema, reconexión, fuga tenant y límites de tamaño.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-035/T206** — Documentar desactivación segura y política de retención.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-035/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-035/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-035/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-035/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.

## Avance incorporado de la numeración anterior

- [x] T035-D01: inventario de datos de los proyectos archivados e identificación de las fuentes del caso piloto Electro Dunas (Prodma, informe, RECYM, VNR-GIS, DGER). _(antes T029-01)_
- [x] T035-D02: controles `unitesis_sciml.quality` (oráculo, desfase mensual, índice regular/posicional, cobertura real) con pruebas. _(antes T029-02)_
- [x] T035-D03: casos de aplicación universales (`config/cases/`, `unitesis_config.cases`) con el piloto `pe-ica-electrodunas` y la plantilla; prueba de universalidad con un caso ficticio a 50 Hz. _(antes T029-03)_
- [x] T035-D04: registro de fuentes v2 con `case_id` y `role`; auditor por caso; evidencia `datasets/quality/source_audit_pe-ica-electrodunas.json` (5 aprobadas, 7 pendientes de lector, 2 pendientes de restauración, 1 inventariada; Iquitos separado como referencia de método). _(antes T029-04)_
- [x] T035-D05: autorización confirmada por instrucción explícita del usuario el 21/10/2026, alcance `local_processing_and_training` (sin licencia de publicación); registrada en el caso. Una autorización confirmada debe declarar autoridad, fecha y alcance (validado por `unitesis_config.cases`). _(antes T029-05)_
