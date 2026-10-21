# ADR-0004 — Cuatro grafos con semánticas independientes

**Estado:** aceptado para diseño, pendiente de prueba de rendimiento.

## Contexto
GIS, electricidad, conocimiento y peers no comparten las mismas relaciones. Un edge de comunicación NO es una línea eléctrica.

## Decisión
1. `G_el`: grafo eléctrico fuente en `power-topology`, terminal-fase, estado de interruptores y snapshot.
2. `G_asset`: grafo de activos/evidencia/relaciones normativas, proyección consultable en `power-graph`.
3. `G_p2p`: peers, ACL, sesiones y rutas de comunicación en `power-p2p`, nunca interpretado como flujo físico.
4. `G_market`: acuerdos/ofertas/contrapartes y restricciones georreferenciadas en `power-market`, referenciando `G_el` mediante IDs versionados.

GraphRAG recupera subgrafos de `G_asset` con fuentes, no infiere conectividad eléctrica. Las proyecciones se reconstruyen desde fuentes y eventos; nunca modifican directamente el modelo canónico. No imponer Neo4j hasta demostrar su beneficio sobre PostgreSQL + consultas/NetworkX en benchmarks.

## Invariantes
IDs canónicos + snapshot_id + topology_hash + tenant_id en cada proyección; las relaciones temporales incluyen `valid_from/valid_to` y `recorded_at`; control de permisos obligatorio.
