# Tasks — Red P2P segura para colaboración entre nodos

- [ ] T01 Definir Envelopes P2P v1 y port PeerTransport
- [ ] T02 Implementar adaptador broker/test primero, suite de autentificación
- [ ] T03 Inbox/outbox, anti-replay, TTL, métricas, resiliencia
- [ ] T04 Evaluar libp2p/relays/permissioning como ADR
- [ ] T05 Integrar panel de peers y trazas auditables sin exponer secretos

- [ ] CI y revisión técnica completa.
- [ ] Convergencia SDD: evidencia, documentación, ADR actualizado.

## Backlog del plan maestro — tareas pendientes

**Gate:** G6 · **Depende de:** SPEC-005, SPEC-010, SPEC-035

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-011/T201** — Definir mensajes tipados, esquema de identidad mutua y scopes de datos.  
  **Estado:** parcial · **Evidencia:** contracts/schemas/json/p2p-envelope.v1 · **Responsable:** por asignar
- [ ] **SPEC-011/T202** — Implementar transporte libp2p en laboratorio aislado o adaptador equivalente evaluado.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-011/T203** — Incluir anti-replay, expiración, cuotas y cifrado autenticado.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-011/T204** — Diseñar reconciliación eventual y resolución de conflictos por versiones.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-011/T205** — Probar pérdidas de mensajes, reintentos, nodo falso y desincronización.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-011/T206** — Mantener desactivada escritura sobre SCADA y equipos de campo.  
  **Estado:** parcial · **Evidencia:** no existe integración SCADA; falta control explícito · **Responsable:** por asignar
- [ ] **SPEC-011/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-011/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-011/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-011/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.
