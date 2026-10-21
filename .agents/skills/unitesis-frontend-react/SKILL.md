---
name: unitesis-frontend-react
description: "Construir workstation React/TypeScript accesible, tipada y modular. Úsalo al trabajar en apps/workstation-web/"
---
# unitesis-frontend-react

## Activación
Construir workstation React/TypeScript accesible, tipada y modular.

## Lecturas obligatorias
`AGENTS.md`, `.specify/memory/constitution.md`, `docs/architecture/MODULE-BOUNDARIES.md`, spec vigente y ADR relacionados. Revisar también `docs/agents/AGENT-ROLES.md`.

## Procedimiento
1. Leer feature spec y OpenAPI; trazar estados loading, empty, error, stale y unauthorized.
2. Organizar por features; React/TypeScript estricto, composición y hooks de consulta; cliente generado de OpenAPI, sin URLs backend dispersas. Separar server state de UI state; diagramas GIS y unifilar sincronizados por ID estable y snapshot. Tests de componentes y E2E.
3. Escribir o actualizar pruebas y evidencias por ID de tarea de `specs/` antes de cerrar el PR.
4. Ejecutar la verificación aplicable: `python -m pytest -q tests/integration` y Playwright sobre `scripts/unitesis.py serve`. Si falta un comando o entorno, registrar el bloqueo y no afirmar que la prueba pasó.

## Límites no negociables
No replicar credenciales en localStorage, no ocultar fallos físicos con resultados ficticios, cumplir accesibilidad teclado y contraste.

## Alcance
apps/workstation-web/

## Entrega
Resumen de cambios, decisiones, artefactos, pruebas ejecutadas realmente, errores, riesgos abiertos y vínculo al PR/spec.


## Fuentes de investigación
Antes de implementar, consultar `docs/scientific-evidence/modules/fe.md`, `docs/scientific-evidence/modules/gis.md`, `docs/scientific-evidence/modules/graph.md`, además de `docs/scientific-evidence/MATRIX-MODULES.md`. Validar ficha y tipo de evidencia, documentar fuente y experimento en la spec. Nunca tratar referencias pendientes o abstracts como validación de producto.
