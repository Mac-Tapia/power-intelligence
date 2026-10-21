---
name: unitesis-domain-ddd
description: "Aplicar DDD, puertos/adaptadores y reglas de importación en el núcleo. Úsalo al trabajar en packages/python/power-domain/"
---
# unitesis-domain-ddd

## Activación
Aplicar DDD, puertos/adaptadores y reglas de importación en el núcleo.

## Lecturas obligatorias
`AGENTS.md`, `.specify/memory/constitution.md`, `docs/architecture/MODULE-BOUNDARIES.md`, spec vigente y ADR relacionados. Revisar también `docs/agents/AGENT-ROLES.md`.

## Procedimiento
1. Ubicar entidad, value object, agregado, servicio de dominio y bounded context antes de modificar.
2. Dominio y puertos sin FastAPI, ORM, PyTorch ni drivers GIS. Preferir tipos inmutables y validación dimensional; eventos versionados; política de autorización en aplicación/adaptador. Revisar reglas de dependencias con el test bootstrap.
3. Escribir o actualizar pruebas y evidencias por ID de tarea de `specs/` antes de cerrar el PR.
4. Ejecutar la verificación aplicable: `python -m unittest discover -s tests/bootstrap -v`. Si falta un comando o entorno, registrar el bloqueo y no afirmar que la prueba pasó.

## Límites no negociables
Nunca duplicar el NetworkSnapshot maestro ni inferir conexión eléctrica solo por coordenadas.

## Alcance
packages/python/power-domain/; packages/python/power-ports/

## Entrega
Resumen de cambios, decisiones, artefactos, pruebas ejecutadas realmente, errores, riesgos abiertos y vínculo al PR/spec.


## Fuentes de investigación UNITESIS V7
Antes de implementar, consultar `docs/scientific-evidence/modules/arch.md`, `docs/scientific-evidence/modules/bk.md`, `docs/scientific-evidence/modules/sdd.md`, además de `docs/scientific-evidence/MATRIX-MODULES.md`. Validar ficha y tipo de evidencia, documentar fuente y experimento en la spec. Nunca tratar referencias pendientes o abstracts como validación de producto.
