# Tasks 027

- [x] Matriz de fuentes y naturaleza jurídica.
- [x] Descripción por numerales TDR Electro Puno 2018.
- [x] Índice de 15 formatos con campos `null` hasta recuperar Anexo.
- [x] Política para tasa y horizonte explícitos.
- [x] Calculadora pura de anualidad ilustrativa + controles de certificación.
- [x] Fixture sintético y CLI de validación.
- [x] Tests unitarios.
- [ ] Descargar y auditar texto íntegro del proyecto MINEM 2017 y exposición de motivos (fuente primaria no accesible).
- [ ] Mapear campo por campo 15 formatos contra páginas originales.
- [ ] Confirmar disposiciones modificatorias o aprobación posterior y alcance por entidad.
- [ ] Integrar análisis de red real con motor determinista, GIS, ingresos y costos VNR.
- [ ] UI frontend con resumen y traza normativa y aprobación humana.

## Backlog del plan maestro — tareas pendientes

**Gate:** G4 · **Depende de:** SPEC-026

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-027/T201** — Localizar/solicitar documento primario original Anexo 1, guardar URI/hash/permisos.  
  **Estado:** bloqueada · **Evidencia:** anexo original no accesible en fuente primaria · **Responsable:** por asignar
- [ ] **SPEC-027/T202** — Inventariar artículos, anexos, formatos y fórmulas en matriz con páginas fuente.  
  **Estado:** bloqueada · **Evidencia:** depende del anexo · **Responsable:** por asignar
- [ ] **SPEC-027/T203** — Vincular campos, unidades, obligatoriedad y métodos de cálculo uno a uno.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-027/T204** — Implementar validaciones de formato y versión solo para contenido confirmado.  
  **Estado:** parcial · **Evidencia:** valida solo contenido confirmado · **Responsable:** por asignar
- [ ] **SPEC-027/T205** — Probar documentalmente cada requisito y registrar diferencias con TDR Electro Puno.  
  **Estado:** parcial · **Evidencia:** diferencias con TDR documentadas · **Responsable:** por asignar
- [x] **SPEC-027/T206** — Habilitar revisión humana obligatoria antes de activar perfil normativo.  
  **Estado:** cumplida · **Evidencia:** revisión humana obligatoria · **Responsable:** por asignar
- [ ] **SPEC-027/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-027/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-027/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-027/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.
