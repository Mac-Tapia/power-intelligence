---
name: unitesis-git-worktree
description: "Desarrollar funciones aisladas con Git worktree, PR y CI. Úsalo al trabajar en scripts/dev/"
---
# unitesis-git-worktree

## Activación
Desarrollar funciones aisladas con Git worktree, PR y CI.

## Lecturas obligatorias
`AGENTS.md`, `.specify/memory/constitution.md`, `docs/architecture/MODULE-BOUNDARIES.md`, spec vigente y ADR relacionados. Revisar también `docs/agents/AGENT-ROLES.md`.

## Procedimiento
1. Inspeccionar rama actual, estados sin commit y objetivo de la spec.
2. Crear worktree con scripts/dev/worktree.py en rama feature, un agente por worktree. No compartir entornos, ni forzar pushes, ni borrar worktrees con cambios. Generar PR enlazando spec, evidencias y tests.
3. Escribir o actualizar pruebas y evidencias por ID de tarea de `specs/` antes de cerrar el PR.
4. Ejecutar la verificación aplicable: `git status --short`. Si falta un comando o entorno, registrar el bloqueo y no afirmar que la prueba pasó.

## Límites no negociables
Prohibidos push --force, git reset --hard y limpieza de worktrees ajenos sin autorización.

## Alcance
scripts/dev/; .github/; specs/

## Entrega
Resumen de cambios, decisiones, artefactos, pruebas ejecutadas realmente, errores, riesgos abiertos y vínculo al PR/spec.


## Fuentes de investigación
Antes de implementar, consultar `docs/scientific-evidence/modules/sdd.md`, `docs/scientific-evidence/modules/arch.md`, además de `docs/scientific-evidence/MATRIX-MODULES.md`. Validar ficha y tipo de evidencia, documentar fuente y experimento en la spec. Nunca tratar referencias pendientes o abstracts como validación de producto.
