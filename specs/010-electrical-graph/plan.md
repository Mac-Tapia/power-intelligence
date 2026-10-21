# Plan — Proyecciones Graph eléctricas y de conocimiento

**Estado:** DRAFT; no desplegado.

## Contexto y boundaries
Construir proyección de lectura por snapshot a partir del maestro terminal/fase, con consultas trazables de activos, feeders, rutas y evidencia. Distinguir grafo eléctrico y grafo de conocimiento, incluyendo GraphRAG con referencias.

## Plan de implementación
1. Congelar diseño, ADRs y amenazas; especificar interfaces y versiones.
2. Construir el adaptador de referencia aislado, con fixtures sintéticos.
3. Verificar invariantes, seguridad, reproducibilidad y pruebas negativas.
4. Ejecutar integración con la API/workers y generación de evidencia.
5. Benchmark, revisión y PR según SDD y Git worktree.

## Tasks
- Esquema GraphProjection.v1, invariantes y pruebas multi-fase
- Outbox para proyección incremental y reconstrucción idempotente
- GraphQL/REST query tipados y frontend graph inspector
- Benchmark grafos grandes, temporalidad, AIS/CIM profile mapping y autorización
- GraphRAG index tenant-aware con citas y evaluación de retrieval

## Gates de aprobación
- 100% de edges de test sintético referencian endpoints existentes.
- Cambiar estado de interruptor genera snapshot nuevo sin modificar el anterior.
- Mismatched snapshot en consulta produce error, no mezcla.
- Consultas sin permiso cross-tenant no devuelven datos.
