---
name: unitesis-electric-graph
description: "Gestionar grafos de red por terminal/fase y proyecciones de activos. Úsalo al trabajar en packages/python/power-graph/"
---
# unitesis-electric-graph

## Activación
Gestionar grafos de red por terminal/fase y proyecciones de activos.

## Lecturas obligatorias
`AGENTS.md`, `.specify/memory/constitution.md`, `docs/architecture/MODULE-BOUNDARIES.md`, spec vigente y ADR relacionados. Revisar también `docs/agents/AGENT-ROLES.md`.

## Procedimiento
1. Leer ADR-0004 y determinar si el grafo solicitado es eléctrico, de activos, comercial o P2P.
2. Construir G_el desde snapshot y estado de maniobra; proyecciones de solo lectura con versionado, hashes y tenant. Probar grafos desconectados, lazos, fases y cambios de estado. Explicitar CRS solo para vista GIS.
3. Escribir o actualizar pruebas y evidencias por ID de tarea de `specs/` antes de cerrar el PR.
4. Ejecutar la verificación aplicable: `python -m pytest -q`. Si falta un comando o entorno, registrar el bloqueo y no afirmar que la prueba pasó.

## Límites no negociables
No mezclar grafo eléctrico, grafo social P2P ni resultados GraphRAG como fuente física.

## Alcance
packages/python/power-graph/; packages/python/power-topology/

## Entrega
Resumen de cambios, decisiones, artefactos, pruebas ejecutadas realmente, errores, riesgos abiertos y vínculo al PR/spec.


## Fuentes de investigación
Antes de implementar, consultar `docs/scientific-evidence/modules/graph.md`, `docs/scientific-evidence/modules/gis.md`, `docs/scientific-evidence/modules/graphrag.md`, además de `docs/scientific-evidence/MATRIX-MODULES.md`. Validar ficha y tipo de evidencia, documentar fuente y experimento en la spec. Nunca tratar referencias pendientes o abstracts como validación de producto.
