# Implementation plan — Multi-domain electrical and economic studies

- Phase 0: verify applicable source texts, dates and annexes.
- Phase 1: specify schemas, authorization boundaries and UX.
- Phase 2: implement pure domain service, isolated adapters and tests.
- Phase 3: scientific and legal cross-validation.
- Phase 4: end-to-end UI and reproducible export.

**Current status**: specification/scaffold only.

## Plan ejecutable — SPEC-022

**Gate de entrega:** G4 · **Dependencias aprobadas:** SPEC-008, SPEC-016.

1. **Modelo/contratos:** definir request, response, objetos de dominio y política de validación en `packages/python/power-economics/, packages/python/power-application/`; separar entidades y DTO.
2. **Arquitectura:** casos de uso sin ORM/HTTP/LLM, puertos tipados y adaptadores reemplazables; usar monolito modular + workers para procesos intensivos.
3. **Persistencia y eventos:** migraciones/backups si hay estado; claves tenant, revisión y hash de procedencia; idempotencia para trabajos.
4. **API/Frontend:** exponer solo endpoints necesarios; OpenAPI versionado, cliente TS generado y UI con carga/error/ausencia de datos; controles no autorizados deben quedar inaccesibles.
5. **Algoritmo:** Evaluar costos e inversiones con flujos de caja trazables, horizontes normativos y escenarios. Nunca simular valores reales cuando faltan datos.
6. **Pruebas:** unitarias puras, contratos, integración aislada, fixtures reales autorizados o sintéticos etiquetados y E2E si corresponde.
7. **Métricas:** VAN/TIR/anualidad y pérdidas se reproducen con tasa, moneda/año base y perfiles explícitos; sin datos se informa falta. Parámetros numéricos/tolerancias se pactan usando benchmarks y se versionan antes de aprobar.
8. **Evidencias:** informe de testing, fuente científica/regulatoria, changelog, hash del input, salida y revisión del responsable.

**Skills/RAG sugerido:** usar skill del módulo y consultar `docs/scientific-evidence` mediante `python scripts/research/query_evidence.py --module economics --limit 10`; si el módulo no está registrado, buscar por palabra clave y registrar ausencia de evidencia.

**Riesgos y controles:** acceso empresarial autorizado, exactitud física, dependencia normativa, evolución de contrato, presupuesto de cómputo y regresión. No usar secretos, datos privados ni herramientas destructivas sin permisos explícitos.
