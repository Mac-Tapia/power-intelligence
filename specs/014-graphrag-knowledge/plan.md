# Plan — GraphRAG técnico trazable de evidencias/normas

**Estado:** DRAFT; no desplegado.

## Contexto y boundaries
Recuperar contextos documentales y relaciones de estudios/normas con citas, ACL y snapshot correcto; no generar parámetros eléctricos inventados.

## Plan de implementación
1. Congelar diseño, ADRs y amenazas; especificar interfaces y versiones.
2. Construir el adaptador de referencia aislado, con fixtures sintéticos.
3. Verificar invariantes, seguridad, reproducibilidad y pruebas negativas.
4. Ejecutar integración con la API/workers y generación de evidencia.
5. Benchmark, revisión y PR según SDD y Git worktree.

## Tasks
- Ontology de assets / studies / standards / evidence
- Pipeline RAG y GraphRAG con metadatos/versiones
- Conectar índice de grafos con ACL sin PII
- Pruebas RAGAS/groundedness y red-team prompt injection
- Interfaz evidencias con subgrafo y citas

## Gates de aprobación
- 100% de respuestas con norma enlazan fragmento verificable.
- Los documentos inyectados no ejecutan instrucciones.
- Retrieval de un snapshot no extrae evidencia de otro.
- Resultados incorrectos regresan "no fundamentado".

## Plan ejecutable — SPEC-014

**Gate de entrega:** G6 · **Dependencias aprobadas:** SPEC-010, SPEC-030, SPEC-032.

1. **Modelo/contratos:** definir request, response, objetos de dominio y política de validación en `packages/python/power-graphrag/, workers/graph-retrieval/`; separar entidades y DTO.
2. **Arquitectura:** casos de uso sin ORM/HTTP/LLM, puertos tipados y adaptadores reemplazables; usar monolito modular + workers para procesos intensivos.
3. **Persistencia y eventos:** migraciones/backups si hay estado; claves tenant, revisión y hash de procedencia; idempotencia para trabajos.
4. **API/Frontend:** exponer solo endpoints necesarios; OpenAPI versionado, cliente TS generado y UI con carga/error/ausencia de datos; controles no autorizados deben quedar inaccesibles.
5. **Algoritmo:** Consultar documentación y relaciones de equipos/reglas/estudios mediante GraphRAG con citas comprobables. Nunca simular valores reales cuando faltan datos.
6. **Pruebas:** unitarias puras, contratos, integración aislada, fixtures reales autorizados o sintéticos etiquetados y E2E si corresponde.
7. **Métricas:** Toda respuesta técnica cita documento/fuente/fecha y no puede escribir la topología eléctrica ni cruzar tenants. Parámetros numéricos/tolerancias se pactan usando benchmarks y se versionan antes de aprobar.
8. **Evidencias:** informe de testing, fuente científica/regulatoria, changelog, hash del input, salida y revisión del responsable.

**Skills/RAG sugerido:** usar skill del módulo y consultar `docs/scientific-evidence` mediante `python scripts/research/query_evidence.py --module agents --limit 10`; si el módulo no está registrado, buscar por palabra clave y registrar ausencia de evidencia.

**Riesgos y controles:** acceso empresarial autorizado, exactitud física, dependencia normativa, evolución de contrato, presupuesto de cómputo y regresión. No usar secretos, datos privados ni herramientas destructivas sin permisos explícitos.
