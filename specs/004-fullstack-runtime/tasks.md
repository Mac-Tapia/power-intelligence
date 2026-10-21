# Tasks — SPEC-004: fullstack-runtime

## Backlog del plan maestro — tareas pendientes

**Gate:** G0 · **Depende de:** SPEC-000

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [x] **SPEC-004/T201** — Crear src/unitesis_api/main.py con app factory, versión API, routers y manejador central de errores.  
  **Estado:** cumplida · **Evidencia:** apps/control-api create_app, routers, errores con código (sin commit, sesión de plataforma) · **Responsable:** por asignar
- [ ] **SPEC-004/T202** — Crear React+TypeScript estricto, navegación, layout principal, cliente API tipado y estados de carga.  
  **Estado:** pendiente · **Evidencia:** sin React+TypeScript · **Responsable:** por asignar
- [ ] **SPEC-004/T203** — Configurar Postgres/PostGIS local, almacenamiento de objetos de desarrollo y migraciones iniciales.  
  **Estado:** parcial · **Evidencia:** postgres_repository.py (sin commit, sesión de plataforma); pruebas omitidas sin DSN; sin PostGIS/objetos · **Responsable:** por asignar
- [ ] **SPEC-004/T204** — Versionar contrato OpenAPI y generar cliente TS sin editar código generado a mano.  
  **Estado:** parcial · **Evidencia:** OpenAPI generado por FastAPI; sin cliente TS · **Responsable:** por asignar
- [ ] **SPEC-004/T205** — Configurar compose, healthchecks, seed sintético y comandos make/dev Windows.  
  **Estado:** parcial · **Evidencia:** health, Makefile, serve; sin compose · **Responsable:** por asignar
- [ ] **SPEC-004/T206** — Probar petición UI→API→DB con tests de integración y E2E de navegador.  
  **Estado:** parcial · **Evidencia:** tests/integration/test_workstation_browser.py (sin commit, sesión de plataforma) — FALLA actualmente · **Responsable:** por asignar
- [ ] **SPEC-004/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-004/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-004/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-004/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.

## Avance incorporado de la numeración anterior

- [ ] T004-I04: contenedores y CI completo. _(antes T009-04)_
