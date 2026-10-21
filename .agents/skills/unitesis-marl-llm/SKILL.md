---
name: unitesis-marl-llm
description: "Diseñar agentes LLM y MARL con herramientas deterministas y controles humanos. Úsalo al trabajar en packages/python/power-agents/"
---
# unitesis-marl-llm

## Activación
Diseñar agentes LLM y MARL con herramientas deterministas y controles humanos.

## Lecturas obligatorias
`AGENTS.md`, `.specify/memory/constitution.md`, `docs/architecture/MODULE-BOUNDARIES.md`, spec vigente y ADR relacionados. Revisar también `docs/agents/AGENT-ROLES.md`.

## Procedimiento
1. Clasificar actor, critic, reward, observación, acciones y riesgo de la ejecución.
2. Especificar acciones JSON tipadas, límites y simulador sandbox; entrenar CTDE offline en escenarios clonados. LLM orquesta, no calcula validación de potencia. Proteger RAG contra prompt injection, mantener trazas y costo de tokens.
3. Escribir o actualizar pruebas y evidencias por ID de tarea de `specs/` antes de cerrar el PR.
4. Ejecutar la verificación aplicable: `tests/security/ y tests/integration/`. Si falta un comando o entorno, registrar el bloqueo y no afirmar que la prueba pasó.

## Límites no negociables
Prohibido acceso directo de agente a producción SCADA, claves privadas o liquidación comercial real.

## Alcance
packages/python/power-agents/; packages/python/power-marl/

## Entrega
Resumen de cambios, decisiones, artefactos, pruebas ejecutadas realmente, errores, riesgos abiertos y vínculo al PR/spec.


## Fuentes de investigación UNITESIS V7
Antes de implementar, consultar `docs/scientific-evidence/modules/marl.md`, `docs/scientific-evidence/modules/llm.md`, `docs/scientific-evidence/modules/sciml.md`, además de `docs/scientific-evidence/MATRIX-MODULES.md`. Validar ficha y tipo de evidencia, documentar fuente y experimento en la spec. Nunca tratar referencias pendientes o abstracts como validación de producto.
