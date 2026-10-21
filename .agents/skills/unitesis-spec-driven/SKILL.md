---
name: unitesis-spec-driven
description: "Especificar antes de programar y mantener trazabilidad SDD GitHub Spec Kit. Úsalo al trabajar en specs/"
---
# unitesis-spec-driven

## Activación
Especificar antes de programar y mantener trazabilidad SDD GitHub Spec Kit.

## Lecturas obligatorias
`AGENTS.md`, `.specify/memory/constitution.md`, `docs/architecture/MODULE-BOUNDARIES.md`, spec vigente y ADR relacionados. Revisar también `docs/agents/AGENT-ROLES.md`.

## Procedimiento
1. Antes de modificar código inspeccionar constitución, spec/plan/tasks, ADRs y pruebas relacionadas.
2. Crear o actualizar spec con escenarios Given/When/Then; plan con decisiones y riesgos; tasks con IDs; solo después implementar una tarea a la vez. Usar Spec Kit cuando esté instalado; no simular comandos ausentes.
3. Escribir o actualizar pruebas y evidencias por ID de tarea de `specs/` antes de cerrar el PR.
4. Ejecutar la verificación aplicable: `python scripts/verify_structure.py`. Si falta un comando o entorno, registrar el bloqueo y no afirmar que la prueba pasó.

## Límites no negociables
No aprobar cambios que carezcan de criterios de aceptación, trazabilidad o revisión humana.

## Alcance
specs/; .specify/; docs/traceability/

## Entrega
Resumen de cambios, decisiones, artefactos, pruebas ejecutadas realmente, errores, riesgos abiertos y vínculo al PR/spec.


## Fuentes de investigación UNITESIS V7
Antes de implementar, consultar `docs/scientific-evidence/modules/sdd.md`, `docs/scientific-evidence/modules/arch.md`, `docs/scientific-evidence/modules/qa.md`, además de `docs/scientific-evidence/MATRIX-MODULES.md`. Validar ficha y tipo de evidencia, documentar fuente y experimento en la spec. Nunca tratar referencias pendientes o abstracts como validación de producto.
