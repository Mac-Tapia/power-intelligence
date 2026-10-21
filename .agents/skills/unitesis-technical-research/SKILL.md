---
name: unitesis-technical-research
description: "Verificar artículos, estándares, normas y antecedentes técnicos en varias lenguas. Úsalo al trabajar en docs/research/"
---
# unitesis-technical-research

## Activación
Verificar artículos, estándares, normas y antecedentes técnicos en varias lenguas.

## Lecturas obligatorias
`AGENTS.md`, `.specify/memory/constitution.md`, `docs/architecture/MODULE-BOUNDARIES.md`, spec vigente y ADR relacionados. Revisar también `docs/agents/AGENT-ROLES.md`.

## Procedimiento
1. Definir pregunta, términos ES/EN/PT/DE/FR, fecha y criterios de selección.
2. Buscar DOI/editor/repositorios institucionales; registrar autor, año, fuente, URL, método, dataset, límites y nivel de acceso. Distinguir literatura revisada de referencias solo identificadas y normativa vigente confirmada.
3. Escribir o actualizar pruebas y evidencias por ID de tarea de `specs/` antes de cerrar el PR.
4. Ejecutar la verificación aplicable: `revisión humana de matriz de fuentes`. Si falta un comando o entorno, registrar el bloqueo y no afirmar que la prueba pasó.

## Límites no negociables
No fabricar DOI, métricas, permisos normativos ni afirmar revisión de texto completo sin evidencia.

## Alcance
docs/research/; docs/reference/

## Entrega
Resumen de cambios, decisiones, artefactos, pruebas ejecutadas realmente, errores, riesgos abiertos y vínculo al PR/spec.


## Fuentes de investigación
Antes de implementar, consultar `docs/scientific-evidence/modules/qa.md`, `docs/scientific-evidence/modules/graphrag.md`, `docs/scientific-evidence/modules/sdd.md`, además de `docs/scientific-evidence/MATRIX-MODULES.md`. Validar ficha y tipo de evidencia, documentar fuente y experimento en la spec. Nunca tratar referencias pendientes o abstracts como validación de producto.
