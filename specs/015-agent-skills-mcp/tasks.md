# Tareas 015

- [x] T015-01 Crear ADR y matriz de roles (diseño).
- [x] T015-02 Registrar skills en carpetas `SKILL.md`.
- [x] T015-03 Catálogo JSON y validador de referencias.
- [x] T015-04 Implementar helpers read-only de MCP con pruebas.
- [x] T015-05 Config Cursor y generador VS Code (sin instalación remota).
- [x] T015-06 Preparar guía backend/frontend y onboarding.
- [ ] T015-07 Instalar SDK MCP v2 y realizar handshake MCP con un cliente real en Cursor/VS Code.
- [ ] T015-08 Probar GitHub MCP con token mínimo y permisos RO, con autorización explícita.
- [ ] T015-09 Probar Playwright MCP en workstation local con UI ya implementada.
- [ ] T015-10 Probar Postgres RO sobre contenedor efímero y defensa SQL.
- [ ] T015-11 Diseñar y aprobar MCP específicos de simulación, GIS y evidencia (todavía planned).
- [x] T015-12 Generador VS Code selecciona el intérprete del entorno local o `sys.executable`, sin habilitar conectores externos (`test_generator_selects_project_interpreter`). Configuración no equivale a handshake.
- [x] T015-L1 SDK MCP 2.3.0 instalado con autorización; handshake stdio y llamadas reales, incluido rechazo de traversal (`test_mcp_transport.py`). No acredita la sesión de Cursor/VS Code requerida por T015-07.
- [x] T015-L2 Chromium instalado y prueba UI por Playwright ejecutada (`test_workstation_browser.py`). Es prueba del SDK de navegador; T015-09 requiere todavía el transporte MCP.

## Backlog del plan maestro — tareas pendientes

**Gate:** G0 · **Depende de:** SPEC-000

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [x] **SPEC-015/T201** — Validar estructura de 20 skills y cobertura por módulo y agente.  
  **Estado:** cumplida · **Evidencia:** scripts/agents/validate_agent_setup.py (24 skills) · **Responsable:** por asignar
- [x] **SPEC-015/T202** — Ejecutar lector MCP local de solo lectura y verificar compatibilidad de protocolo.  
  **Estado:** cumplida · **Evidencia:** tests/integration/test_mcp_transport.py (sin commit, sesión de plataforma) · **Responsable:** por asignar
- [x] **SPEC-015/T203** — Definir permisos/scopes por agente y riesgos de comandos destructivos.  
  **Estado:** cumplida · **Evidencia:** connectors/registry.json con deny por defecto · **Responsable:** por asignar
- [x] **SPEC-015/T204** — Integrar skills SDD para Cursor/otros clientes sin amarrar código a un agente.  
  **Estado:** cumplida · **Evidencia:** scripts/agents/sync_skills.py · **Responsable:** por asignar
- [x] **SPEC-015/T205** — Probar path traversal, escaping, secreto accidental y permisos denegados.  
  **Estado:** cumplida · **Evidencia:** tests/governance/test_agents_mcp.py · **Responsable:** por asignar
- [ ] **SPEC-015/T206** — Generar guía de conexión autenticada sin almacenar credenciales.  
  **Estado:** parcial · **Evidencia:** AI-AGENT-ONBOARDING.md; conexión autenticada externa no probada · **Responsable:** por asignar
- [ ] **SPEC-015/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-015/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-015/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-015/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.
