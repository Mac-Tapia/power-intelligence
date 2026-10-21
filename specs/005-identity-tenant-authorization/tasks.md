# Tasks — SPEC-005: identity-tenant-authorization

## Backlog del plan maestro — tareas pendientes

**Gate:** G0 · **Depende de:** SPEC-004

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-005/T201** — Definir matriz roles/atributos/permisos por proyectos, fuentes, escenarios y expedientes.  
  **Estado:** parcial · **Evidencia:** roles en credenciales bearer (security.py) (sin commit, sesión de plataforma) · **Responsable:** por asignar
- [ ] **SPEC-005/T202** — Integrar OIDC de proveedor configurable y sesiones seguras en API/BFF.  
  **Estado:** pendiente · **Evidencia:** sin OIDC · **Responsable:** por asignar
- [ ] **SPEC-005/T203** — Aplicar filtros tenant_id en consultas y políticas por resource ID.  
  **Estado:** parcial · **Evidencia:** almacenes por tenant; test_tenant_security.py (sin commit, sesión de plataforma) · **Responsable:** por asignar
- [ ] **SPEC-005/T204** — Establecer auditoría de modificaciones, no repudio interno y redacción de secretos.  
  **Estado:** parcial · **Evidencia:** evidencia append-only y errores sin secretos; sin auditoría de cambios por usuario · **Responsable:** por asignar
- [ ] **SPEC-005/T205** — Probar negativas cross-tenant, token expirado, escalamiento vertical y CSRF.  
  **Estado:** parcial · **Evidencia:** 401/403/tenant probados (sin commit, sesión de plataforma); CSRF y token expirado sin verificar en esta revisión · **Responsable:** por asignar
- [ ] **SPEC-005/T206** — Documentar aprovisionamiento/desaprovisionamiento y pruebas de recuperación.  
  **Estado:** parcial · **Evidencia:** apps/control-api/README.md · **Responsable:** por asignar
- [ ] **SPEC-005/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-005/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-005/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-005/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.

## Avance incorporado de la numeración anterior

- [ ] T005-I01: autenticación + RBAC + tenant en control-api. _(antes T009-01)_
- [x] T005-L4: bearer con caducidad, roles reader/engineer y almacenes separados por tenant; pruebas 401/403/404 y Chromium sin persistir token (`test_tenant_security.py`, `test_workstation_browser.py`). Continúa siendo perfil local. _(antes T009-L4)_
