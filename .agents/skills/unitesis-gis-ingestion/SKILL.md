---
name: unitesis-gis-ingestion
description: "Importar VNR-GIS/MDB/TXT/SQL con linaje y validación topológica. Úsalo al trabajar en workers/ingestion/"
---
# unitesis-gis-ingestion

## Activación
Importar VNR-GIS/MDB/TXT/SQL con linaje y validación topológica.

## Lecturas obligatorias
`AGENTS.md`, `.specify/memory/constitution.md`, `docs/architecture/MODULE-BOUNDARIES.md`, spec vigente y ADR relacionados. Revisar también `docs/agents/AGENT-ROLES.md`.

## Procedimiento
1. Buscar manifest de fuente, licencia, CRS, esquema, unidades y fecha de vigencia.
2. ETL bronze/silver/gold reproducible; mapa de columnas por distribuidora y versión; conservar fuente raw con hash; reportar atributos ausentes. Vincular GIS a nodos/terminales/fases por reglas auditadas, con cuarentena de registros ambiguos.
3. Escribir o actualizar pruebas y evidencias por ID de tarea de `specs/` antes de cerrar el PR.
4. Ejecutar la verificación aplicable: `tests/electrical-golden/ y tests/integration/`. Si falta un comando o entorno, registrar el bloqueo y no afirmar que la prueba pasó.

## Límites no negociables
No crear atributos ficticios, ni descargar bases no autorizadas, ni confundir VNR físico y modelo de cálculo.

## Alcance
workers/ingestion/; packages/python/power-topology/

## Entrega
Resumen de cambios, decisiones, artefactos, pruebas ejecutadas realmente, errores, riesgos abiertos y vínculo al PR/spec.


## Fuentes de investigación UNITESIS V7
Antes de implementar, consultar `docs/scientific-evidence/modules/gis.md`, `docs/scientific-evidence/modules/graph.md`, `docs/scientific-evidence/modules/bk.md`, además de `docs/scientific-evidence/MATRIX-MODULES.md`. Validar ficha y tipo de evidencia, documentar fuente y experimento en la spec. Nunca tratar referencias pendientes o abstracts como validación de producto.
