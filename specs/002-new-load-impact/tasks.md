# Tareas 002

- [x] T002-01: escenario clonado con carga nueva y cribado equilibrado antes/después (CLI `new-load`, API, UI); el hash del origen no cambia (`tests/integration/test_study_vertical.py`).
- [x] T002-02: criterios de cribado desde `planning_criteria` del caso (NTCSE, numeral por verificar), con precedencia orden > caso > valor por defecto etiquetado; la fuente queda en la evidencia (`--case`).
- [x] T002-03: capacidad remanente por barra sobre la red real del caso (`hosting-capacity`, `unitesis_application.hosting_capacity`): el sustituto criba y el solver certifica cada límite; los límites coinciden con un barrido exhaustivo (`tests/unit/test_hosting_capacity.py`). Alimentador real IC103: 190 barras, 1 106 llamadas al solver frente a 9 120 por fuerza bruta.
- [ ] T002-04: estudio por fase (depende de 008-C) y mitigaciones vía spec 018.
- [ ] T002-05: revisión humana del cribado con un caso real de Electro Dunas autorizado.

## Backlog del plan maestro — tareas pendientes

**Gate:** G4 · **Depende de:** SPEC-008, SPEC-009, SPEC-016, SPEC-022

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-002/T201** — Crear contrato de solicitud de nueva carga con fase, kW, kvar/fp, fecha y nodo autorizado.  
  **Estado:** parcial · **Evidencia:** p/q/barra en new-load; faltan fase y fecha · **Responsable:** por asignar
- [ ] **SPEC-002/T202** — Vincular curvas 15 min al equipo/medidor y generar snapshot clon inmutable.  
  **Estado:** parcial · **Evidencia:** escenario clonado sí; curvas 15 min por medidor no · **Responsable:** por asignar
- [x] **SPEC-002/T203** — Ejecutar análisis AC antes/después y capturar no convergencia y parámetros faltantes.  
  **Estado:** cumplida · **Evidencia:** run_new_load_study + evidencia; no convergencia reportada · **Responsable:** por asignar
- [ ] **SPEC-002/T204** — Comparar los indicadores por barra/fase/elemento y límites de normativa seleccionada.  
  **Estado:** parcial · **Evidencia:** criterios del caso (NTCSE) aplicados; sin desagregación por fase · **Responsable:** por asignar
- [ ] **SPEC-002/T205** — Evaluar alternativas transferir/repotenciar/refuerzo sin aplicar maniobras reales.  
  **Estado:** parcial · **Evidencia:** solo alternativas de conductor y capacidad remanente · **Responsable:** por asignar
- [ ] **SPEC-002/T206** — Generar reporte trazable con evidencia de solver, CAPEX/OPEX y recomendación revisable.  
  **Estado:** parcial · **Evidencia:** evidencia JSON trazable; sin informe formateado · **Responsable:** por asignar
- [ ] **SPEC-002/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-002/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-002/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-002/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.
