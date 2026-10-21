# Tasks — SPEC-018: planning-alternatives

## Backlog del plan maestro — tareas pendientes

**Gate:** G4 · **Depende de:** SPEC-002, SPEC-017, SPEC-022

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-018/T201** — Diseñar catálogo de soluciones: transferir, SED/SET, nuevo alimentador, reconductor, regulación, BESS.  
  **Estado:** parcial · **Evidencia:** solo reconductorado · **Responsable:** por asignar
- [ ] **SPEC-018/T202** — Establecer rule packs PIT/PIDE/interno separados con condiciones de aplicabilidad.  
  **Estado:** parcial · **Evidencia:** perfiles PIT/PIDE/interno separados · **Responsable:** por asignar
- [ ] **SPEC-018/T203** — Generar diseños candidatos con cambios de topología y recursos documentados.  
  **Estado:** parcial · **Evidencia:** cambio de conductor en escenario clonado · **Responsable:** por asignar
- [x] **SPEC-018/T204** — Validar cada candidato con solver de referencia e impedir factibilidad supuesta.  
  **Estado:** cumplida · **Evidencia:** contraste independiente obligatorio (alternatives.py) · **Responsable:** por asignar
- [ ] **SPEC-018/T205** — Comparar CAPEX, pérdidas, confiabilidad, plazo y Pareto cuando aplique.  
  **Estado:** parcial · **Evidencia:** CAPEX, pérdidas y Pareto; sin confiabilidad ni plazo · **Responsable:** por asignar
- [x] **SPEC-018/T206** — Aplicar mínimo de tres solo al perfil histórico que lo exige, nunca universal.  
  **Estado:** cumplida · **Evidencia:** pide_reference: mínimo 3 solo en perfil histórico (pruebas) · **Responsable:** por asignar
- [ ] **SPEC-018/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-018/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-018/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-018/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.

## Avance incorporado de la numeración anterior

- [x] T018-E01: alternativas de conductor + VPN + contraste (CLI, API y UI). _(antes T005-01)_
- [ ] T018-E02: refuerzo de SED (cambio de transformador) después de 004-B. _(antes T005-02)_
