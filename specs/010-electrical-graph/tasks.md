# Tasks — Proyecciones Graph eléctricas y de conocimiento

- [ ] T01 Esquema GraphProjection.v1, invariantes y pruebas multi-fase
- [ ] T02 Outbox para proyección incremental y reconstrucción idempotente
- [ ] T03 GraphQL/REST query tipados y frontend graph inspector
- [ ] T04 Benchmark grafos grandes, temporalidad, AIS/CIM profile mapping y autorización
- [ ] T05 GraphRAG index tenant-aware con citas y evaluación de retrieval

- [ ] CI y revisión técnica completa.
- [ ] Convergencia SDD: evidencia, documentación, ADR actualizado.

## Backlog del plan maestro — tareas pendientes

**Gate:** G1 · **Depende de:** SPEC-001, SPEC-006

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-010/T201** — Diseñar vertices/equipos/terminales y relaciones permitidas con hashes de revisiones.  
  **Estado:** parcial · **Evidencia:** buses/ramas con hash; sin terminales · **Responsable:** por asignar
- [x] **SPEC-010/T202** — Crear proyecciones de conectividad eléctrica y aislar grafo de mapa y GraphRAG.  
  **Estado:** cumplida · **Evidencia:** power-topology separado de geometría y GraphRAG (ADR-0003) · **Responsable:** por asignar
- [x] **SPEC-010/T203** — Detectar islas, huérfanos, ciclos, orientaciones y fronteras de alimentador.  
  **Estado:** cumplida · **Evidencia:** islas, mallas, desenergizados, árbol radial, raíces · **Responsable:** por asignar
- [x] **SPEC-010/T204** — Construir exportador topológico de entrada a solvers por adaptador.  
  **Estado:** cumplida · **Evidencia:** snapshot→Y-bus y →pandapower · **Responsable:** por asignar
- [ ] **SPEC-010/T205** — Probar consultas por subgrafo con límites y permisos tenant.  
  **Estado:** pendiente · **Evidencia:** sin consultas por subgrafo ni permisos · **Responsable:** por asignar
- [ ] **SPEC-010/T206** — Validar fases, transformadores, configuraciones de interruptor y reconfiguración.  
  **Estado:** parcial · **Evidencia:** trafos e interruptores validados; fases y reconfiguración pendientes · **Responsable:** por asignar
- [ ] **SPEC-010/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-010/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-010/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-010/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.
