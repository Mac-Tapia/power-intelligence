# Tasks — SPEC-019: multiobjective-optimization

## Backlog del plan maestro — tareas pendientes

**Gate:** G4 · **Depende de:** SPEC-018, SPEC-008

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-019/T201** — Formalizar variables discretas/continuas, costos y restricciones eléctricas.  
  **Estado:** parcial · **Evidencia:** variables de conductor y costos · **Responsable:** por asignar
- [ ] **SPEC-019/T202** — Crear baseline MILP o búsqueda exhaustiva pequeña y heurística NSGA-II/III según problema.  
  **Estado:** parcial · **Evidencia:** exhaustivo sobre catálogo; sin NSGA · **Responsable:** por asignar
- [ ] **SPEC-019/T203** — Conectar evaluador AC y cache por hash de red/decisiones sin valores simulados.  
  **Estado:** parcial · **Evidencia:** evaluador AC sí; caché no · **Responsable:** por asignar
- [ ] **SPEC-019/T204** — Implementar Monte Carlo, escenarios de demanda y sensibilidad de pesos.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-019/T205** — Comparar con baseline y reportar hypervolume/tiempo/violaciones cuando pertinente.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-019/T206** — Persistir semilla, versión, presupuesto de cómputo y Pareto no dominado.  
  **Estado:** parcial · **Evidencia:** frente de Pareto persistido en evidencia · **Responsable:** por asignar
- [ ] **SPEC-019/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-019/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-019/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-019/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.

## Avance incorporado de la numeración anterior

- [x] T019-E04: frente de Pareto (`unitesis_optimization.pareto`) publicado en la evidencia de alternativas: VPN, pérdidas, cargabilidad, V mínima y CO2 de pérdidas (solo si la base económica declara un factor de emisión con fuente). Las dominadas quedan trazadas con su dominante; el recomendado por VPN se mantiene con su criterio explícito. Motor por defecto: Newton-Raphson. Pruebas: `tests/unit/test_pareto.py`. _(antes T005-04)_
