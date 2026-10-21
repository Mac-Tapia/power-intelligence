# Tasks — SPEC-006: canonical-electrical-model

## Backlog del plan maestro — tareas pendientes

**Gate:** G1 · **Depende de:** SPEC-000

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-006/T201** — Definir entidades de red, terminal, fase, switch, conductor, trafo, SED/SET, cargas y DER.  
  **Estado:** parcial · **Evidencia:** Bus/Line/Switch/Load/Slack/Transformer; faltan terminal, fase, SED/SET, DER · **Responsable:** por asignar
- [ ] **SPEC-006/T202** — Definir unidades, nominal/base, por fase y conexión a tierra con validación tipada.  
  **Estado:** parcial · **Evidencia:** unidades y validación numérica tipada; solo secuencia positiva · **Responsable:** por asignar
- [ ] **SPEC-006/T203** — Implementar snapshots inmutables y revisionado por comando con IDs estables.  
  **Estado:** parcial · **Evidencia:** snapshots inmutables con hash; sin revisionado por comando · **Responsable:** por asignar
- [ ] **SPEC-006/T204** — Definir mapeos a esquema CIM acotado y política de campos no soportados.  
  **Estado:** pendiente · **Evidencia:** sin mapeo CIM · **Responsable:** por asignar
- [ ] **SPEC-006/T205** — Construir property tests de conexiones incompatibles, islas y transformadores.  
  **Estado:** parcial · **Evidencia:** pruebas negativas de islas, mallas, tensiones y trafos; no son property-based · **Responsable:** por asignar
- [ ] **SPEC-006/T206** — Publicar contratos JSON y diagramas de relaciones sin dependencias de ORM.  
  **Estado:** parcial · **Evidencia:** esquemas JSON de evidencia; sin esquema JSON del snapshot ni diagramas · **Responsable:** por asignar
- [ ] **SPEC-006/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-006/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-006/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-006/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.

## Avance incorporado de la numeración anterior

- [x] T006-A2: contratos `ElectricalSnapshot` v2, `StudyRequest/Result`, evidencia releída y esquemas validados (`docs/architecture/CONTRACTS-AND-EVIDENCE.md`). _(antes T004-A2)_
- [x] T006-A4: `NetworkSnapshot` v1 retirado; `ElectricalSnapshot` v2 es la única identidad eléctrica (sus invariantes cubren duplicados, orden y tensión física). _(antes T004-A4)_
