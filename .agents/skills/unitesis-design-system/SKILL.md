---
name: unitesis-design-system
description: "Mantener librería UI reutilizable, diseño accesible y visualizaciones de ingeniería. Úsalo al trabajar en packages/ts/ui-kit/"
---
# unitesis-design-system

## Activación
Mantener librería UI reutilizable, diseño accesible y visualizaciones de ingeniería.

## Lecturas obligatorias
`AGENTS.md`, `.specify/memory/constitution.md`, `docs/architecture/MODULE-BOUNDARIES.md`, spec vigente y ADR relacionados. Revisar también `docs/agents/AGENT-ROLES.md`.

## Procedimiento
1. Identificar tokens visuales, accesibilidad, estados y unidades antes de diseñar.
2. Componentizar tablas científicas, paneles, árboles de proyecto, diálogos, inspector de propiedades, escalas, leyendas y unidades; documentar variants y estados. Usar el mismo ID eléctrico entre mapa y unifilar, separando coordenadas geográficas de layouts.
3. Escribir o actualizar pruebas y evidencias por ID de tarea de `specs/` antes de cerrar el PR.
4. Ejecutar la verificación aplicable: `python -m pytest -q tests/integration` (la UI se sirve desde control-api). Si falta un comando o entorno, registrar el bloqueo y no afirmar que la prueba pasó.

## Límites no negociables
No usar color como único indicador de criticidad; interfaces de control requieren confirmación humana.

## Alcance
apps/workstation-web/public/

## Entrega
Resumen de cambios, decisiones, artefactos, pruebas ejecutadas realmente, errores, riesgos abiertos y vínculo al PR/spec.


## Fuentes de investigación
Antes de implementar, consultar `docs/scientific-evidence/modules/fe.md`, `docs/scientific-evidence/modules/gis.md`, `docs/scientific-evidence/modules/qa.md`, además de `docs/scientific-evidence/MATRIX-MODULES.md`. Validar ficha y tipo de evidencia, documentar fuente y experimento en la spec. Nunca tratar referencias pendientes o abstracts como validación de producto.
