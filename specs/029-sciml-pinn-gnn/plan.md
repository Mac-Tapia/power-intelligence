# Plan — SPEC-029: sciml-pinn-gnn


## Plan ejecutable — SPEC-029

**Gate de entrega:** G5 · **Dependencias aprobadas:** SPEC-008, SPEC-028, SPEC-038.

1. **Modelo/contratos:** definir request, response, objetos de dominio y política de validación en `packages/python/power-sciml/, workers/ml-training/`; separar entidades y DTO.
2. **Arquitectura:** casos de uso sin ORM/HTTP/LLM, puertos tipados y adaptadores reemplazables; usar monolito modular + workers para procesos intensivos.
3. **Persistencia y eventos:** migraciones/backups si hay estado; claves tenant, revisión y hash de procedencia; idempotencia para trabajos.
4. **API/Frontend:** exponer solo endpoints necesarios; OpenAPI versionado, cliente TS generado y UI con carga/error/ausencia de datos; controles no autorizados deben quedar inaccesibles.
5. **Algoritmo:** Entrenar PINN/GNN como aproximadores auditables de redes, nunca como certificación automática AC. Nunca simular valores reales cuando faltan datos.
6. **Pruebas:** unitarias puras, contratos, integración aislada, fixtures reales autorizados o sintéticos etiquetados y E2E si corresponde.
7. **Métricas:** Cada modelo tiene arquitectura, pesos, versión, datos, validación OOD, error y rechazo de resultados no factibles. Parámetros numéricos/tolerancias se pactan usando benchmarks y se versionan antes de aprobar.
8. **Evidencias:** informe de testing, fuente científica/regulatoria, changelog, hash del input, salida y revisión del responsable.

**Skills/RAG sugerido:** usar skill del módulo y consultar `docs/scientific-evidence` mediante `python scripts/research/query_evidence.py --module sciml --limit 10`; si el módulo no está registrado, buscar por palabra clave y registrar ausencia de evidencia.

**Riesgos y controles:** acceso empresarial autorizado, exactitud física, dependencia normativa, evolución de contrato, presupuesto de cómputo y regresión. No usar secretos, datos privados ni herramientas destructivas sin permisos explícitos.

## Plan incorporado (antes spec 006)

Implementar GraphSAGE explícito en `power-sciml/gnn.py`: agregación por aristas,
entradas por nodo, salidas V/ángulo y pérdida de balance AC compleja con Y-bus.
Las pruebas unitarias comprueban dimensión, gradiente y equilibrio conocido; no son
un experimento de entrenamiento ni evidencia de precisión fuera de muestra.

Antes de entrenar, `promote_pf_dataset` valida AC-035-D04 y AC-029-S01: procedencia,
fechas, hueco lag+horizonte, pertenencia temporal de cada muestra, split disjunto
por alimentador, hashes y contraste independiente. Sin esos datos se rechaza la
promoción y no se entrenan modelos con el candidato actual.

La instalación y ejecución GPU se registran por separado. No se modifica el
umbral p95/recall ni se habilita el sustituto hasta completar AC-029-S02..06.
