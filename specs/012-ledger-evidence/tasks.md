# Tasks — Registro criptográfico y blockchain permissioned optativo

- [ ] T01 Implementar EvidenceStore + append-only signed log baseline
- [ ] T02 Definir LedgerAnchorPort + schema y eventos
- [ ] T03 Proof-of-concept Fabric private data con permisos
- [ ] T04 Proof-of-concept Besu QBFT con n>=4 validators
- [ ] T05 Informe ADR coste/beneficio/gobernanza y hardening claves

- [ ] CI y revisión técnica completa.
- [ ] Convergencia SDD: evidencia, documentación, ADR actualizado.

## Backlog del plan maestro — tareas pendientes

**Gate:** G6 · **Depende de:** SPEC-011, SPEC-032

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-012/T201** — Definir contrato EvidenceAnchor, políticas de privacidad y evaluación necesidad de blockchain.  
  **Estado:** parcial · **Evidencia:** ledger-anchor.v1 schema · **Responsable:** por asignar
- [ ] **SPEC-012/T202** — Implementar ledger local/in-memory y validaciones de idempotencia.  
  **Estado:** parcial · **Evidencia:** power-ledger/attest.py (digest) · **Responsable:** por asignar
- [ ] **SPEC-012/T203** — Crear adaptador para red permissioned de prueba aislada sujeto a threat model.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-012/T204** — Verificar hashes, sellos temporales y permisos, sin almacenar SCADA o PII on-chain.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-012/T205** — Probar tampering, reordenamiento, reenvíos, caída de nodo y restauración.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-012/T206** — Emitir evidencia de costo y latencia antes de optar por ledger productivo.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-012/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-012/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-012/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-012/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.
