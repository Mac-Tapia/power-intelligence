---
name: unitesis-power-simulation
description: "Implementar estudios eléctricos verificables mediante solver y benchmarks. Úsalo al trabajar en packages/python/power-simulation/"
---
# unitesis-power-simulation

## Activación
Implementar estudios eléctricos verificables mediante solver y benchmarks.

## Lecturas obligatorias
`AGENTS.md`, `.specify/memory/constitution.md`, `docs/architecture/MODULE-BOUNDARIES.md`, spec vigente y ADR relacionados. Revisar también `docs/agents/AGENT-ROLES.md`.

## Procedimiento
1. Definir hipótesis, unidades, versión del motor, modelo de red y tolerancias.
2. Adaptar OpenDSS/pandapower/otro bajo interfaz PowerFlowPort; registrar convergencia, fases, tensión, corriente, pérdidas y topología. Separar referencias golden de escenarios de inferencia. Cortocircuitos y OPF tienen validaciones especializadas.
3. Escribir o actualizar pruebas y evidencias por ID de tarea de `specs/` antes de cerrar el PR.
4. Ejecutar la verificación aplicable: `tests/electrical-golden/`. Si falta un comando o entorno, registrar el bloqueo y no afirmar que la prueba pasó.

## Límites no negociables
Prohibido presentar PINN o LLM como validación final; no habilitar maniobras SCADA.

## Alcance
packages/python/power-simulation/; workers/simulation/

## Entrega
Resumen de cambios, decisiones, artefactos, pruebas ejecutadas realmente, errores, riesgos abiertos y vínculo al PR/spec.


## Fuentes de investigación UNITESIS V7
Antes de implementar, consultar `docs/scientific-evidence/modules/solver.md`, `docs/scientific-evidence/modules/sciml.md`, `docs/scientific-evidence/modules/op.md`, además de `docs/scientific-evidence/MATRIX-MODULES.md`. Validar ficha y tipo de evidencia, documentar fuente y experimento en la spec. Nunca tratar referencias pendientes o abstracts como validación de producto.
