---
name: unitesis-sciml-pinn-gnn
description: "Entrenar PINN/GNN reproducibles y validar invariantes físicos. Úsalo al trabajar en packages/python/power-sciml/"
---
# unitesis-sciml-pinn-gnn

## Activación
Entrenar PINN/GNN reproducibles y validar invariantes físicos.

## Lecturas obligatorias
`AGENTS.md`, `.specify/memory/constitution.md`, `docs/architecture/MODULE-BOUNDARIES.md`, spec vigente y ADR relacionados. Revisar también `docs/agents/AGENT-ROLES.md`.

## Procedimiento
1. Consultar dataset manifest, split temporal/topológico, baseline y requisitos de precisión.
2. Implementar módulos PyTorch transparentes, semillas, loss con residual AC correctamente formulado, métricas por nodo y OOD. Datasets sintéticos o autorizados; métricas contra solver e intervalos de confianza; experiment tracker y artifact hash.
3. Escribir o actualizar pruebas y evidencias por ID de tarea de `specs/` antes de cerrar el PR.
4. Ejecutar la verificación aplicable: `python -m pytest -q` y el benchmark de la spec 029 (`benchmarks/sciml/`, se crea con T029-S05). Si falta un comando o entorno, registrar el bloqueo y no afirmar que la prueba pasó.

## Límites no negociables
Penalizaciones físicas suaves no garantizan cumplimiento; no afirmar aceleraciones sin benchmark.

## Alcance
packages/python/power-sciml/; workers/ml-training/

## Entrega
Resumen de cambios, decisiones, artefactos, pruebas ejecutadas realmente, errores, riesgos abiertos y vínculo al PR/spec.


## Fuentes de investigación
Antes de implementar, consultar `docs/scientific-evidence/modules/sciml.md`, `docs/scientific-evidence/modules/graph.md`, `docs/scientific-evidence/modules/solver.md`, además de `docs/scientific-evidence/MATRIX-MODULES.md`. Validar ficha y tipo de evidencia, documentar fuente y experimento en la spec. Nunca tratar referencias pendientes o abstracts como validación de producto.
