# Tasks — SPEC-038: benchmarks-and-scientific-reproducibility

## Backlog del plan maestro — tareas pendientes

**Gate:** G3 · **Depende de:** SPEC-008, SPEC-010

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-038/T201** — Inventariar feeders de referencia, problemas de optimización y datasets GIS accesibles.  
  **Estado:** parcial · **Evidencia:** IEEE 33, sintéticos, 44 reales · **Responsable:** por asignar
- [ ] **SPEC-038/T202** — Crear protocolo de tolerancias acordado con ingeniero y referencias independientes.  
  **Estado:** parcial · **Evidencia:** tolerancias en CONTRACTS-AND-EVIDENCE; sin acuerdo formal con ingeniero · **Responsable:** por asignar
- [ ] **SPEC-038/T203** — Implementar runner reproducible que capture CPU/RAM/GPU, semillas y versiones.  
  **Estado:** parcial · **Evidencia:** benchmark con versiones, plataforma y tiempos; sin RAM/GPU · **Responsable:** por asignar
- [ ] **SPEC-038/T204** — Incluir tests metamórficos (escalado, switch, interconexiones inválidas) sin falsos positivos.  
  **Estado:** parcial · **Evidencia:** invariancia de orden, int/float, fusión de interruptores · **Responsable:** por asignar
- [ ] **SPEC-038/T205** — Comparar cálculos deterministas vs modelos neuronales en igual set.  
  **Estado:** parcial · **Evidencia:** línea base física vs solver · **Responsable:** por asignar
- [ ] **SPEC-038/T206** — Publicar benchmarking y límites de validez con trazabilidad bibliográfica.  
  **Estado:** parcial · **Evidencia:** benchmarks/power-flow/results.json con límites · **Responsable:** por asignar
- [ ] **SPEC-038/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-038/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-038/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-038/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.
