---
name: unitesis-evidence-audit
description: "Generar evidencia reproducible de ingeniería, estudios y decisiones. Úsalo al trabajar en packages/python/power-evidence/"
---
# unitesis-evidence-audit

## Activación
Generar evidencia reproducible de ingeniería, estudios y decisiones.

## Lecturas obligatorias
`AGENTS.md`, `.specify/memory/constitution.md`, `docs/architecture/MODULE-BOUNDARIES.md`, spec vigente y ADR relacionados. Revisar también `docs/agents/AGENT-ROLES.md`.

## Procedimiento
1. Obtener requerimiento, escenario y hash de topología, parámetros, solver y commit.
2. Generar run_manifest, quality gates, métricas de convergencia, restricciones evaluadas y aprobaciones. Vincular informe a evidencia versionada; formatos PDF/MD solo cuando solicitados. Diferenciar evidencia off-chain y anclaje ledger.
3. Escribir o actualizar pruebas y evidencias por ID de tarea de `specs/` antes de cerrar el PR.
4. Ejecutar la verificación aplicable: `tests/contract/ y tests/electrical-golden/`. Si falta un comando o entorno, registrar el bloqueo y no afirmar que la prueba pasó.

## Límites no negociables
Nunca reportar estudio aprobado sin solver, tolerancias y firmante/autorización.

## Alcance
packages/python/power-evidence/; datasets/quality/

## Entrega
Resumen de cambios, decisiones, artefactos, pruebas ejecutadas realmente, errores, riesgos abiertos y vínculo al PR/spec.


## Fuentes de investigación
Antes de implementar, consultar `docs/scientific-evidence/modules/bk.md`, `docs/scientific-evidence/modules/ledger.md`, `docs/scientific-evidence/modules/ops.md`, `docs/scientific-evidence/modules/qa.md`, además de `docs/scientific-evidence/MATRIX-MODULES.md`. Validar ficha y tipo de evidencia, documentar fuente y experimento en la spec. Nunca tratar referencias pendientes o abstracts como validación de producto.
