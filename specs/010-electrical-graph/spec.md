# Spec — Proyecciones Graph eléctricas y de conocimiento

**Estado:** DRAFT / Not implemented · Feature ID `010`.

## User intent y alcance
Construir proyección de lectura por snapshot a partir del maestro terminal/fase, con consultas trazables de activos, feeders, rutas y evidencia. Distinguir grafo eléctrico y grafo de conocimiento, incluyendo GraphRAG con referencias.

## Requerimientos verificables
- No usar geometría como prueba de conectividad; cada relación debe tener provenance/snapshot.
- Mantener modelos multi-fase y versiones de estado de interruptor.
- Prohibido escribir de GraphRAG al maestro físico.
- Comparativa PostgreSQL/PostGIS/NetworkX frente a Neo4j opcional.

## Criterios de aceptación
- 100% de edges de test sintético referencian endpoints existentes.
- Cambiar estado de interruptor genera snapshot nuevo sin modificar el anterior.
- Mismatched snapshot en consulta produce error, no mezcla.
- Consultas sin permiso cross-tenant no devuelven datos.

## Restricciones
Se prohíben ejecuciones sobre SCADA/protecciones. No se debe acceder a datos no autorizados ni inferir valores faltantes. El acceso comercial solo tras aprobación legal/regulatoria verificable.

## Dependencias
`001` ingesta y contratos; `003` GIS/unifilar; `004` solver validado; el resto según orden de `docs/traceability/FEATURE-MAP.md`.
