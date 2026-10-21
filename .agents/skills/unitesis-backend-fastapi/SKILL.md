---
name: unitesis-backend-fastapi
description: "Diseñar backend FastAPI mantenible con DDD, seguridad y jobs largos. Úsalo al trabajar en apps/control-api/"
---
# unitesis-backend-fastapi

## Activación
Diseñar backend FastAPI mantenible con DDD, seguridad y jobs largos.

## Lecturas obligatorias
`AGENTS.md`, `.specify/memory/constitution.md`, `docs/architecture/MODULE-BOUNDARIES.md`, spec vigente y ADR relacionados. Revisar también `docs/agents/AGENT-ROLES.md`.

## Procedimiento
1. Identificar módulo y contrato OpenAPI primero; escribir caso de uso y puertos independientes de frameworks.
2. Separar routers HTTP, auth, schemas, use-cases, interfaces y adapters. API fina con APIRouter y dependencias explícitas; nunca correr flujo de potencia ni entrenamientos en request handlers. Usar colas/workers con identificadores de job, progreso y cancelación. Prever idempotencia y aislamiento de tenant.
3. Escribir o actualizar pruebas y evidencias por ID de tarea de `specs/` antes de cerrar el PR.
4. Ejecutar la verificación aplicable: `pytest tests/contract tests/integration -q (cuando existan tests reales)`. Si falta un comando o entorno, registrar el bloqueo y no afirmar que la prueba pasó.

## Límites no negociables
Validar 401/403, paginación, errores RFC 9457 cuando se acuerde, límites, registros sin secretos, rutas versionadas y pruebas de contrato.

## Alcance
apps/control-api/; packages/python/power-application/; contracts/openapi/

## Entrega
Resumen de cambios, decisiones, artefactos, pruebas ejecutadas realmente, errores, riesgos abiertos y vínculo al PR/spec.


## Fuentes de investigación UNITESIS V7
Antes de implementar, consultar `docs/scientific-evidence/modules/arch.md`, `docs/scientific-evidence/modules/bk.md`, `docs/scientific-evidence/modules/ops.md`, `docs/scientific-evidence/modules/security.md`, además de `docs/scientific-evidence/MATRIX-MODULES.md`. Validar ficha y tipo de evidencia, documentar fuente y experimento en la spec. Nunca tratar referencias pendientes o abstracts como validación de producto.
