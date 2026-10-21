# Tasks — Multi-domain electrical and economic studies

- [x] Register SDD scope and traceability framework.
- [ ] Read full official texts and inspect current amendments for each clause.
- [ ] Develop API, persistence migrations and frontend pages.
- [ ] Implement calculations and reference benchmarks where applicable.
- [ ] Test with authorized real VNR-GIS and cost tables.
- [ ] User acceptance and legal/engineering sign-off.

## Backlog del plan maestro — tareas pendientes

**Gate:** G4 · **Depende de:** SPEC-008, SPEC-016

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-022/T201** — Definir contratos CAPEX, OPEX, reposición, pérdidas, energía no suministrada y horizonte.  
  **Estado:** parcial · **Evidencia:** EconomicBasis; sin reposición ni ENS · **Responsable:** por asignar
- [ ] **SPEC-022/T202** — Implementar flujos de caja reales/nominales y valor presente con tasas declaradas.  
  **Estado:** parcial · **Evidencia:** valor presente real; nominal no · **Responsable:** por asignar
- [ ] **SPEC-022/T203** — Agregar costos de módulos estándares solo desde catálogo/regla versionada.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-022/T204** — Vincular energía/pérdidas al solver y escenarios de crecimiento.  
  **Estado:** parcial · **Evidencia:** pérdidas del solver; crecimiento no · **Responsable:** por asignar
- [x] **SPEC-022/T205** — Probar factores de descuento, signos, tasas límite, datos faltantes y sensibilidad.  
  **Estado:** cumplida · **Evidencia:** tests/unit/test_economic_basis.py, governance/test_economics_regressions.py · **Responsable:** por asignar
- [x] **SPEC-022/T206** — Exportar comparativas por alternativa con fuente de precios y resumen de supuestos.  
  **Estado:** cumplida · **Evidencia:** evidencia de alternativas con fuente de precios · **Responsable:** por asignar
- [ ] **SPEC-022/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-022/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-022/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-022/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.
