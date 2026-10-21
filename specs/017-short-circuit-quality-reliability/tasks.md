# Tasks — SPEC-017: short-circuit-quality-reliability

## Backlog del plan maestro — tareas pendientes

**Gate:** G3 · **Depende de:** SPEC-008, SPEC-009

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-017/T201** — Definir subtipos de estudio cortocircuito 3f/1f/2f y requisitos de secuencia/red puesta a tierra.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-017/T202** — Implementar adaptador de falla soportado con versión y pruebas cruzadas.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-017/T203** — Calcular perfiles de calidad y límites por normativa versionada, no por constante global.  
  **Estado:** parcial · **Evidencia:** planning_criteria del caso (NTCSE, numeral por verificar) · **Responsable:** por asignar
- [ ] **SPEC-017/T204** — Incorporar confiabilidad SAIDI/SAIFI/ENS únicamente con tasas e interrupciones documentadas.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-017/T205** — Agregar pruebas de TC/transformador/falla mal parametrizados y casos IEC/ANSI según cobertura.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-017/T206** — Emitir reporte de aplicabilidad normativa y faltantes antes de certificación.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-017/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-017/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-017/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-017/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.

## Avance incorporado de la numeración anterior

- [ ] T017-D: cortocircuito IEC 60909. _(antes T004-D)_

## Hallazgos REA aplicables (ADR-0012)

- [ ] T017-R01: impedancia equivalente de fuente desde `SUBSTATION` (R1/R0, KVLL, MVA) del export CYME, con cuarentena si falta.
