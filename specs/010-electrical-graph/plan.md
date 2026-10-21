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

## Plan ejecutable — SPEC-010

**Gate de entrega:** G1 · **Dependencias aprobadas:** SPEC-001, SPEC-006.

1. **Modelo/contratos:** definir request, response, objetos de dominio y política de validación en `packages/python/power-graph/, power-topology/, workers/graph-projection/`; separar entidades y DTO.
2. **Arquitectura:** casos de uso sin ORM/HTTP/LLM, puertos tipados y adaptadores reemplazables; usar monolito modular + workers para procesos intensivos.
3. **Persistencia y eventos:** migraciones/backups si hay estado; claves tenant, revisión y hash de procedencia; idempotencia para trabajos.
4. **API/Frontend:** exponer solo endpoints necesarios; OpenAPI versionado, cliente TS generado y UI con carga/error/ausencia de datos; controles no autorizados deben quedar inaccesibles.
5. **Algoritmo:** Construir grafo topológico por terminal/fase/estado, separado del GIS, conocimiento y comunicación. Nunca simular valores reales cuando faltan datos.
6. **Pruebas:** unitarias puras, contratos, integración aislada, fixtures reales autorizados o sintéticos etiquetados y E2E si corresponde.
7. **Métricas:** El grafo conserva fases/switches y consultas de alimentador; falla por islas críticas o fuentes inconsistentes sin simular conexiones inexistentes. Parámetros numéricos/tolerancias se pactan usando benchmarks y se versionan antes de aprobar.
8. **Evidencias:** informe de testing, fuente científica/regulatoria, changelog, hash del input, salida y revisión del responsable.

**Skills/RAG sugerido:** usar skill del módulo y consultar `docs/scientific-evidence` mediante `python scripts/research/query_evidence.py --module graph --limit 10`; si el módulo no está registrado, buscar por palabra clave y registrar ausencia de evidencia.

**Riesgos y controles:** acceso empresarial autorizado, exactitud física, dependencia normativa, evolución de contrato, presupuesto de cómputo y regresión. No usar secretos, datos privados ni herramientas destructivas sin permisos explícitos.
