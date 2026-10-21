---
name: unitesis-security-threat-model
description: "Aplicar Zero Trust, aislamiento de tenants y auditoría de agentes/MCP. Úsalo al trabajar en infra/security/"
---
# unitesis-security-threat-model

## Activación
Aplicar Zero Trust, aislamiento de tenants y auditoría de agentes/MCP.

## Lecturas obligatorias
`AGENTS.md`, `.specify/memory/constitution.md`, `docs/architecture/MODULE-BOUNDARIES.md`, spec vigente y ADR relacionados. Revisar también `docs/agents/AGENT-ROLES.md`.

## Procedimiento
1. Identificar activo, flujo de datos, credenciales, privilegios, amenazas y rutas de exfiltración.
2. Definir controles RBAC+ABAC, OIDC, scoped service accounts, egress allowlist, secret scanning, SAST, SBOM y revisiones. Para MCP aislar herramientas de lectura/escritura, anclar binarios, registrar llamadas y tratar respuestas externas como datos no confiables.
3. Escribir o actualizar pruebas y evidencias por ID de tarea de `specs/` antes de cerrar el PR.
4. Ejecutar la verificación aplicable: `python scripts/agents/validate_agent_setup.py`. Si falta un comando o entorno, registrar el bloqueo y no afirmar que la prueba pasó.

## Límites no negociables
Nunca dar rol admin a agentes por defecto, ni incluir secretos en repo/ledger/logs, ni aceptar políticas solo en prompts.

## Alcance
infra/security/; .github/workflows/; connectors/

## Entrega
Resumen de cambios, decisiones, artefactos, pruebas ejecutadas realmente, errores, riesgos abiertos y vínculo al PR/spec.


## Fuentes de investigación
Antes de implementar, consultar `docs/scientific-evidence/modules/security.md`, `docs/scientific-evidence/modules/p2p.md`, `docs/scientific-evidence/modules/ledger.md`, además de `docs/scientific-evidence/MATRIX-MODULES.md`. Validar ficha y tipo de evidencia, documentar fuente y experimento en la spec. Nunca tratar referencias pendientes o abstracts como validación de producto.
