# Tasks — GraphRAG técnico trazable de evidencias/normas

- [ ] T01 Ontology de assets / studies / standards / evidence
- [ ] T02 Pipeline RAG y GraphRAG con metadatos/versiones
- [ ] T03 Conectar índice de grafos con ACL sin PII
- [ ] T04 Pruebas RAGAS/groundedness y red-team prompt injection
- [ ] T05 Interfaz evidencias con subgrafo y citas

- [ ] CI y revisión técnica completa.
- [ ] Convergencia SDD: evidencia, documentación, ADR actualizado.

## Backlog del plan maestro — tareas pendientes

**Gate:** G6 · **Depende de:** SPEC-010, SPEC-030, SPEC-032

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-014/T201** — Construir índices textuales y relaciones de activos/documentos de solo lectura.  
  **Estado:** parcial · **Evidencia:** scripts/research/query_evidence.py (léxico) sobre 191 fichas · **Responsable:** por asignar
- [ ] **SPEC-014/T202** — Configurar ingestión de normativa, evidencia y biblioteca científica con permisos.  
  **Estado:** parcial · **Evidencia:** catálogo científico y regulatorio; sin permisos · **Responsable:** por asignar
- [ ] **SPEC-014/T203** — Implementar recuperación híbrida y scoring documentado.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-014/T204** — Generar respuestas con citas verificables, abstención y soporte de español/inglés.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-014/T205** — Probar prompt injection, documentos contaminados y aislamiento tenant.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-014/T206** — Medir exactitud factual, recall y tasa de abstención en set revisado.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-014/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-014/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-014/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-014/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.

## Avance incorporado de la numeración anterior

- [ ] T014-D11: corpus normativo PE con licencia por documento; trazas de herramientas; set de evaluación. _(antes T029-11)_
