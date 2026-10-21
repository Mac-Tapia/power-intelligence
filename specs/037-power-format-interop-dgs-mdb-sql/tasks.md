# Tasks — SPEC-037: power-format-interop-dgs-mdb-sql

## Backlog del plan maestro — tareas pendientes

**Gate:** G1 · **Depende de:** SPEC-001, SPEC-006

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-037/T201** — Definir matriz de cobertura y licencias de DGS, OpenDSS, MDB, TXT, SHP y SQL.  
  **Estado:** parcial · **Evidencia:** registro de formatos y ADR-0010 · **Responsable:** por asignar
- [ ] **SPEC-037/T202** — Implementar exportador inicial OpenDSS de red validada.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-037/T203** — Diseñar importador/exportador DGS solo con esquemas/versiones documentadas.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-037/T204** — Generar reporte de diferencias y atributos incompatibles en round-trip.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-037/T205** — Probar dos feeders golden con unidades, fases, taps y switches.  
  **Estado:** parcial · **Evidencia:** CYME sintético + red real; ida y vuelta neutral con trafos · **Responsable:** por asignar
- [x] **SPEC-037/T206** — Bloquear etiqueta compatible con PowerFactory/CYME hasta validación en herramienta original.  
  **Estado:** cumplida · **Evidencia:** ADR-0010 + tests/security/test_no_proprietary_engines.py · **Responsable:** por asignar
- [ ] **SPEC-037/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-037/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-037/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-037/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.

## Ingeniería inversa (ADR-0012)

- [x] T037-R01: perfilador de formatos con cobertura del lector y versión redactada. Evidencia: `power-adapters/format_profile.py`, CLI `profile-export`, `tests/unit/test_format_profile.py`.
- [x] T037-R02: estructura CYME ASCII recuperada del export real y códigos inferidos con evidencia. Evidencia: `docs/architecture/formats/CYME-ASCII-RECOVERED.md`, `cyme-ascii-structure.json`.
- [ ] T037-R03: aplicar el perfilador a MDB (requiere lector Access autorizado) y al esquema VNR-GIS restaurado.
- [ ] T037-R04: recuperación de métodos de estudios heredados por caja negra (entradas/salidas documentadas) con pruebas de reproducción.
- [ ] T037-R05: revisión legal de la norma peruana (D. Leg. 822) con texto oficial antes de cualquier análisis que la requiera.
