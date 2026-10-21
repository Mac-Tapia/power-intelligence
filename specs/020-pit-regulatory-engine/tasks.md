# Tasks — PIT SST/SCT regulatory profiles and versioned rules

- [x] Register SDD scope and traceability framework.
- [ ] Read full official texts and inspect current amendments for each clause.
- [ ] Develop API, persistence migrations and frontend pages.
- [ ] Implement calculations and reference benchmarks where applicable.
- [ ] Test with authorized real VNR-GIS and cost tables.
- [ ] User acceptance and legal/engineering sign-off.

## Backlog del plan maestro — tareas pendientes

**Gate:** G4 · **Depende de:** SPEC-017, SPEC-022, SPEC-025

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-020/T201** — Inventariar texto 217-2013, modificatorias, anexos y edición por periodo regulatorio.  
  **Estado:** parcial · **Evidencia:** docs/regulatory/SOURCES.json · **Responsable:** por asignar
- [ ] **SPEC-020/T202** — Construir matriz cláusula→datos→algoritmo→salida→test con fuente primaria.  
  **Estado:** parcial · **Evidencia:** PIT-217-CLAUSE-MATRIX.md · **Responsable:** por asignar
- [ ] **SPEC-020/T203** — Implementar elegibilidad SST/SCT y perfil independiente de distribución.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-020/T204** — Vincular alternativas y cálculos económicos al método reglamentario aplicable.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-020/T205** — Probar error por cláusula no verificada, fuente vencida o estudio no elegible.  
  **Estado:** parcial · **Evidencia:** certificación bloqueada (RegulatoryBlock) · **Responsable:** por asignar
- [x] **SPEC-020/T206** — Solicitar aprobación profesional antes de marcar expediente PIT como regulatorio.  
  **Estado:** cumplida · **Evidencia:** aprobación humana obligatoria · **Responsable:** por asignar
- [ ] **SPEC-020/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-020/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-020/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-020/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.
