# Tasks — SPEC-031: security-observability-operations

## Backlog del plan maestro — tareas pendientes

**Gate:** G7 · **Depende de:** SPEC-004, SPEC-005, SPEC-007

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-031/T201** — Aplicar threat model STRIDE y escáner de dependencias/secretos/SBOM.  
  **Estado:** parcial · **Evidencia:** threat model P2P/ledger; sin escáneres ni SBOM · **Responsable:** por asignar
- [ ] **SPEC-031/T202** — Configurar métricas, trazas estructuradas, logs correlacionados y redacción sensible.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-031/T203** — Diseñar backup/restauración de Postgres/PostGIS y artefactos con pruebas reales.  
  **Estado:** parcial · **Evidencia:** backup/restauración SQLite (sin commit, sesión de plataforma); PostgreSQL omitido · **Responsable:** por asignar
- [ ] **SPEC-031/T204** — Separar entornos local/staging/prod y gestión de secretos/rotación.  
  **Estado:** parcial · **Evidencia:** perfil solo-local y credenciales fuera de Git · **Responsable:** por asignar
- [ ] **SPEC-031/T205** — Ejecutar pruebas de carga, degradación de cola, DR y límites de recursos.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-031/T206** — Documentar on-call, runbooks, incidentes y SLO medidos, no supuestos.  
  **Estado:** pendiente · **Evidencia:** sin evidencia todavía · **Responsable:** por asignar
- [ ] **SPEC-031/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-031/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-031/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-031/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.

## Avance incorporado de la numeración anterior

- [ ] T031-I03: observabilidad y backups. _(antes T009-03)_
- [x] T031-L3: backup/restauración SQLite a destino nuevo con integridad y relectura; restricciones append-only preservadas (`tests/integration/test_database_recovery.py`). _(antes T009-L3)_
- [x] T031-L6: logs estructurados sin valores privados, métricas por tenant y trace ID (`test_observability.py`); pg_dump/pg_restore en base nueva con relectura de snapshot y resultado (`test_postgres_recovery.py`). _(antes T009-L6)_
- [x] T031-D12: `tests/security/test_no_sensitive_data.py` recorre los archivos versionados (sin `local-data/`, ids reales de clientes CYME, RUC, importes facturados ni correos no permitidos). _(antes T029-12)_
