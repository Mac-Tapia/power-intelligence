# Plan candidato — VNR-GIS

1. Catalogar fuentes y licencias, inventariar tablas/campos y CRS por versión (no adivinar esquema).
2. Implementar puerto `RawSourceReader`, adapters por formato, `SchemaMappingRegistry` declarativo.
3. Transformar a nodos/equipos/terminales/fases; registrar procedencia por atributo.
4. Validadores por etapas Bronze / Silver / Gold, con reglas configurables y quarantined records.
5. Contrato de snapshot y hashing inmutable; tests de homomorfismo topológico.
6. Integrar con UI solo cuando el grafo pase las puertas de calidad.

**Riesgo principal:** el VNR-GIS puede describir activos y geometría sin datos mínimos de operación, por lo que su ingesta exitosa no demuestra viabilidad de flujo de carga.

## Plan ejecutable — SPEC-001

**Gate de entrega:** G1 · **Dependencias aprobadas:** SPEC-006.

1. **Modelo/contratos:** definir request, response, objetos de dominio y política de validación en `workers/ingestion/, packages/python/power-adapters/, data contracts`; separar entidades y DTO.
2. **Arquitectura:** casos de uso sin ORM/HTTP/LLM, puertos tipados y adaptadores reemplazables; usar monolito modular + workers para procesos intensivos.
3. **Persistencia y eventos:** migraciones/backups si hay estado; claves tenant, revisión y hash de procedencia; idempotencia para trabajos.
4. **API/Frontend:** exponer solo endpoints necesarios; OpenAPI versionado, cliente TS generado y UI con carga/error/ausencia de datos; controles no autorizados deben quedar inaccesibles.
5. **Algoritmo:** Ingerir fuentes reales VNR-GIS y adaptadores autorizados con procedencia e inconsistencias explícitas. Nunca simular valores reales cuando faltan datos.
6. **Pruebas:** unitarias puras, contratos, integración aislada, fixtures reales autorizados o sintéticos etiquetados y E2E si corresponde.
7. **Métricas:** Importaciones de dos esquemas documentados conservan RAW, unidades, CRS, atributos faltantes y cuarentena; repetición determinista. Parámetros numéricos/tolerancias se pactan usando benchmarks y se versionan antes de aprobar.
8. **Evidencias:** informe de testing, fuente científica/regulatoria, changelog, hash del input, salida y revisión del responsable.

**Skills/RAG sugerido:** usar skill del módulo y consultar `docs/scientific-evidence` mediante `python scripts/research/query_evidence.py --module gis --limit 10`; si el módulo no está registrado, buscar por palabra clave y registrar ausencia de evidencia.

**Riesgos y controles:** acceso empresarial autorizado, exactitud física, dependencia normativa, evolución de contrato, presupuesto de cómputo y regresión. No usar secretos, datos privados ni herramientas destructivas sin permisos explícitos.
