---
name: unitesis-api-contracts
description: "Diseñar contratos OpenAPI, JSON Schema, eventos y clientes generados. Úsalo al trabajar en contracts/"
---
# unitesis-api-contracts

## Activación
Diseñar contratos OpenAPI, JSON Schema, eventos y clientes generados.

## Lecturas obligatorias
`AGENTS.md`, `.specify/memory/constitution.md`, `docs/architecture/MODULE-BOUNDARIES.md`, spec vigente y ADR relacionados. Revisar también `docs/agents/AGENT-ROLES.md`.

## Procedimiento
1. Abrir contracts/ y revisar versionado, unidades y snapshot IDs.
2. API-first o contract-first; schemas de request/response, tipos TS autogenerados con openapi-typescript tras validar la fuente. Contract tests consumidor-proveedor, migración compatible y deprecaciones. Definir errores estables y correlation_id.
3. Escribir o actualizar pruebas y evidencias por ID de tarea de `specs/` antes de cerrar el PR.
4. Ejecutar la verificación aplicable: `python -m pytest -q`. Si falta un comando o entorno, registrar el bloqueo y no afirmar que la prueba pasó.

## Límites no negociables
No editar manualmente código generado ni cambiar unidades o semántica de forma silenciosa.

## Alcance
contracts/; apps/control-api/ (OpenAPI generado en /openapi.json)

## Entrega
Resumen de cambios, decisiones, artefactos, pruebas ejecutadas realmente, errores, riesgos abiertos y vínculo al PR/spec.


## Fuentes de investigación
Antes de implementar, consultar `docs/scientific-evidence/modules/arch.md`, `docs/scientific-evidence/modules/bk.md`, `docs/scientific-evidence/modules/security.md`, `docs/scientific-evidence/modules/sdd.md`, además de `docs/scientific-evidence/MATRIX-MODULES.md`. Validar ficha y tipo de evidencia, documentar fuente y experimento en la spec. Nunca tratar referencias pendientes o abstracts como validación de producto.
