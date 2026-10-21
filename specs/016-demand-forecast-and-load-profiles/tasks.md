# Tasks — SPEC-016: demand-forecast-and-load-profiles

## Backlog del plan maestro — tareas pendientes

**Gate:** G3 · **Depende de:** SPEC-001, SPEC-006, SPEC-009

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-016/T201** — Diseñar contrato de fechas/zonas horarias, kW/kvar/kWh y correspondencia medidor-alimentador.  
  **Estado:** parcial · **Evidencia:** DatasetSpec + zona horaria del caso; mapeo medidor-alimentador pendiente · **Responsable:** por asignar
- [ ] **SPEC-016/T202** — Ingerir archivos Excel/CSV/Parquet autorizados y normalizar resoluciones temporales.  
  **Estado:** parcial · **Evidencia:** CSV operativo; Excel bronze (sin commit, sesión de plataforma) · **Responsable:** por asignar
- [x] **SPEC-016/T203** — Aplicar QA de duplicados, periodos ausentes, outliers y reporte de decisión por imputación.  
  **Estado:** cumplida · **Evidencia:** power-sciml/datasets.py (outliers causales, congelados) + quality.py · **Responsable:** por asignar
- [ ] **SPEC-016/T204** — Integrar nuevas cargas como constantes 15 min únicamente donde usuario lo indique.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-016/T205** — Implementar baselines estacionales y evaluación temporal sin fuga futuro.  
  **Estado:** parcial · **Evidencia:** splits cronológicos con hueco; sin modelos base de pronóstico · **Responsable:** por asignar
- [ ] **SPEC-016/T206** — Publicar curvas, errores MAE/RMSE/MAPE cuando definido y bandas por escenario.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-016/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-016/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-016/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-016/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.

## Avance incorporado de la numeración anterior

- [ ] T016-D06: autorizar lectores (`openpyxl`, `xlrd`, `pyxlsb`) y crear la capa bronze de medidores, líneas y cabeceras. _(antes T029-06)_
- [ ] T016-D08: gold `feeder-load-15min-pe-ica-electrodunas` con exógenas aprobadas y splits cronológicos. _(antes T029-08)_
