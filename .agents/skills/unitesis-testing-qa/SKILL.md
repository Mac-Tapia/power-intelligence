---
name: unitesis-testing-qa
description: "Aplicar pirámide de pruebas: unit, property, contract, E2E y golden electrical. Úsalo al trabajar en tests/"
---
# unitesis-testing-qa

## Activación
Aplicar pirámide de pruebas: unit, property, contract, E2E y golden electrical.

## Lecturas obligatorias
`AGENTS.md`, `.specify/memory/constitution.md`, `docs/architecture/MODULE-BOUNDARIES.md`, spec vigente y ADR relacionados. Revisar también `docs/agents/AGENT-ROLES.md`.

## Procedimiento
1. Extraer criterios de aceptación de spec; distinguir fixtures sintéticos de datos reales licenciados.
2. Unit pytest/unittest, hypothesis, contrato OpenAPI, integración en contenedores efímeros, Playwright accesibilidad y trazas. Regresión eléctrica por circuito y solver, y seguridad negativa para P2P/MCP/GraphRAG.
3. Escribir o actualizar pruebas y evidencias por ID de tarea de `specs/` antes de cerrar el PR.
4. Ejecutar la verificación aplicable: `python -m pytest -q`. Si falta un comando o entorno, registrar el bloqueo y no afirmar que la prueba pasó.

## Límites no negociables
No convertir snapshots de interfaz en prueba de corrección eléctrica o autorización.

## Alcance
tests/; benchmarks/; .github/workflows/

## Entrega
Resumen de cambios, decisiones, artefactos, pruebas ejecutadas realmente, errores, riesgos abiertos y vínculo al PR/spec.


## Fuentes de investigación
Antes de implementar, consultar `docs/scientific-evidence/modules/qa.md`, `docs/scientific-evidence/modules/solver.md`, `docs/scientific-evidence/modules/fe.md`, `docs/scientific-evidence/modules/ops.md`, además de `docs/scientific-evidence/MATRIX-MODULES.md`. Validar ficha y tipo de evidencia, documentar fuente y experimento en la spec. Nunca tratar referencias pendientes o abstracts como validación de producto.
