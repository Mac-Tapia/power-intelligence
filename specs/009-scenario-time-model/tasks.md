# Tasks — SPEC-009: scenario-time-model

## Backlog del plan maestro — tareas pendientes

**Gate:** G2 · **Depende de:** SPEC-006, SPEC-007, SPEC-010

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-009/T201** — Definir snapshot red, perfil de demanda, fecha operativa y overlays de cambios.  
  **Estado:** parcial · **Evidencia:** escenarios por snapshot clonado; sin fecha operativa ni overlays · **Responsable:** por asignar
- [ ] **SPEC-009/T202** — Implementar clonado copy-on-write y diff estructurado entre escenarios.  
  **Estado:** parcial · **Evidencia:** clonado sí; diff estructurado no · **Responsable:** por asignar
- [ ] **SPEC-009/T203** — Crear escenarios máxima/mínima demanda, N-1 y programación 15 min/8760 h configurables.  
  **Estado:** parcial · **Evidencia:** escenarios de demanda en pf_dataset; sin N-1 ni 8760 h · **Responsable:** por asignar
- [x] **SPEC-009/T204** — Bloquear ejecución cuando se carezca de datos requeridos de operación.  
  **Estado:** cumplida · **Evidencia:** fail-closed por datos faltantes · **Responsable:** por asignar
- [ ] **SPEC-009/T205** — Conectar ediciones GIS/unifilar a revisiones de escenario y no a fuente primaria.  
  **Estado:** pendiente · **Evidencia:** sin edición GIS/unifilar · **Responsable:** por asignar
- [ ] **SPEC-009/T206** — Probar resultados deterministas, conflicto de revisión y escenario eliminado.  
  **Estado:** parcial · **Evidencia:** determinismo probado; conflictos de revisión no · **Responsable:** por asignar
- [ ] **SPEC-009/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-009/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-009/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-009/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.
