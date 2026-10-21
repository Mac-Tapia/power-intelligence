# Tasks — Mercado simulado de energía/flexibilidad condicionado a red

- [ ] T01 Definir EnergyTradeProposal y representación de agentes/intervalos
- [ ] T02 Solver acoplado: matching -> security-constrained validation -> rechazo/ajuste
- [ ] T03 BESS SOC y EV demandas temporales; minimización multiobjetivo
- [ ] T04 Simular pérdidas/cargos de red/restricciones por alimentador
- [ ] T05 Compliance Peru legal-gate y piloto experimental opt-in

- [ ] CI y revisión técnica completa.
- [ ] Convergencia SDD: evidencia, documentación, ADR actualizado.

## Backlog del plan maestro — tareas pendientes

**Gate:** G6 · **Depende de:** SPEC-011, SPEC-012, SPEC-019, SPEC-028

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-013/T201** — Definir ofertas P/Q, precios, límites, intervalos y roles DER/BESS/EV.  
  **Estado:** parcial · **Evidencia:** p2p-energy-trade.v1 schema · **Responsable:** por asignar
- [ ] **SPEC-013/T202** — Crear motor de clearing simulado con balance de energía y restricciones de recursos.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-013/T203** — Ejecutar solver AC para cada propuesta de despacho o intercambio.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-013/T204** — Comparar bienestar, pérdidas, congestión y costos transaccionales.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-013/T205** — Probar fraude, oferta imposible, baterías sin energía y escenarios sin convergencia.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-013/T206** — Bloquear liquidación comercial real hasta dictamen jurídico y autorización expresa.  
  **Estado:** parcial · **Evidencia:** power-market/gates.py bloquea propuestas sin evidencia · **Responsable:** por asignar
- [ ] **SPEC-013/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-013/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-013/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-013/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.
