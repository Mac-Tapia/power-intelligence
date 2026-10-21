---
name: unitesis-mcp-connectors
description: "Configurar MCP de mínimo privilegio y herramientas especializadas por agente. Úsalo al trabajar en connectors/"
---
# unitesis-mcp-connectors

## Activación
Configurar MCP de mínimo privilegio y herramientas especializadas por agente.

## Lecturas obligatorias
`AGENTS.md`, `.specify/memory/constitution.md`, `docs/architecture/MODULE-BOUNDARIES.md`, spec vigente y ADR relacionados. Revisar también `docs/agents/AGENT-ROLES.md`.

## Procedimiento
1. Consultar connectors/registry.json, policies y los perfiles del agente.
2. Activar primero conector local de documentación de solo lectura; habilitar GitHub/Playwright/PostgreSQL cuando estén instalados y autorizados. Revisar publisher, versionado, OAuth scopes, output untrusted y logging; pruebas smoke por herramienta.
3. Escribir o actualizar pruebas y evidencias por ID de tarea de `specs/` antes de cerrar el PR.
4. Ejecutar la verificación aplicable: `python scripts/agents/validate_agent_setup.py`. Si falta un comando o entorno, registrar el bloqueo y no afirmar que la prueba pasó.

## Límites no negociables
No arrancar servidores externos o instalar paquetes con npx @latest por defecto; nunca exponer shell genérica/SQL de escritura.

## Alcance
connectors/; tools/mcp/; .cursor/mcp.json

## Entrega
Resumen de cambios, decisiones, artefactos, pruebas ejecutadas realmente, errores, riesgos abiertos y vínculo al PR/spec.


## Fuentes de investigación
Antes de implementar, consultar `docs/scientific-evidence/modules/security.md`, `docs/scientific-evidence/modules/sdd.md`, `docs/scientific-evidence/modules/llm.md`, además de `docs/scientific-evidence/MATRIX-MODULES.md`. Validar ficha y tipo de evidencia, documentar fuente y experimento en la spec. Nunca tratar referencias pendientes o abstracts como validación de producto.
