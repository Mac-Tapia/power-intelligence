# Tasks — Regulatory consolidation and amendment watcher

- [x] Register SDD scope and traceability framework.
- [ ] Read full official texts and inspect current amendments for each clause.
- [ ] Develop API, persistence migrations and frontend pages.
- [ ] Implement calculations and reference benchmarks where applicable.
- [ ] Test with authorized real VNR-GIS and cost tables.
- [ ] User acceptance and legal/engineering sign-off.

## Backlog del plan maestro — tareas pendientes

**Gate:** G4 · **Depende de:** SPEC-015

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-025/T201** — Estructurar URL primaria, autoridad, fecha y norma citada, huellas y política de licencia.  
  **Estado:** parcial · **Evidencia:** SOURCES.json con URL y autoridad · **Responsable:** por asignar
- [ ] **SPEC-025/T202** — Implementar lector manual/on-demand de fuentes permitidas con hash/diff.  
  **Estado:** parcial · **Evidencia:** scripts/pide/register_source.py · **Responsable:** por asignar
- [ ] **SPEC-025/T203** — Registrar estado de vigencia y cambios detectados como solicitudes de revisión.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-025/T204** — Construir matriz efecto cambios sobre estudios/reglas/expedientes.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-025/T205** — Probar origen inaccesible, enlace cambiado, PDF distinto y documentos duplicados.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-025/T206** — Añadir flujo de aprobación de cambio de versión regulatoria.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-025/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-025/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-025/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-025/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.
