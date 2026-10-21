---
name: unitesis-db-postgis
description: "Diseñar PostgreSQL/PostGIS con migraciones, índices espaciales y mínimo privilegio. Úsalo al trabajar en infra/database/"
---
# unitesis-db-postgis

## Activación
Diseñar PostgreSQL/PostGIS con migraciones, índices espaciales y mínimo privilegio.

## Lecturas obligatorias
`AGENTS.md`, `.specify/memory/constitution.md`, `docs/architecture/MODULE-BOUNDARIES.md`, spec vigente y ADR relacionados. Revisar también `docs/agents/AGENT-ROLES.md`.

## Procedimiento
1. Identificar snapshot, CRS, SRID, tenant y consulta crítica.
2. Modelar red canónica temporal con claves estables y SQL parametrizado. Crear migraciones expand/contract, rollback, índices GIST y BTree donde aplique. Diagnosticar con EXPLAIN solo bajo rol de lectura. Nunca inferir conectividad con ST_DWithin.
3. Escribir o actualizar pruebas y evidencias por ID de tarea de `specs/` antes de cerrar el PR.
4. Ejecutar la verificación aplicable: `tests/integration/ (PostGIS en ambiente efímero)`. Si falta un comando o entorno, registrar el bloqueo y no afirmar que la prueba pasó.

## Límites no negociables
Agentes de desarrollo usan read-only; migraciones y borrados exigen aprobación y credenciales separadas.

## Alcance
infra/database/; packages/python/power-adapters/

## Entrega
Resumen de cambios, decisiones, artefactos, pruebas ejecutadas realmente, errores, riesgos abiertos y vínculo al PR/spec.


## Fuentes de investigación
Antes de implementar, consultar `docs/scientific-evidence/modules/bk.md`, `docs/scientific-evidence/modules/gis.md`, `docs/scientific-evidence/modules/arch.md`, además de `docs/scientific-evidence/MATRIX-MODULES.md`. Validar ficha y tipo de evidencia, documentar fuente y experimento en la spec. Nunca tratar referencias pendientes o abstracts como validación de producto.
