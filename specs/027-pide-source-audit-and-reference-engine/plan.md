# Plan 027

1. Registrar resoluciones oficiales y TDR con categorías de autoridad estrictas.
2. Matriz 16 requisitos verificables por numerales del TDR; señalar ausencias Anexo.
3. Crear registro de 15 formatos INACTIVOS, esperando diseño original.
4. Construir paquete `unitesis_regulation.pide_reference` libre de I/O y de dependencias externas.
5. Proveer CLI y fixture inequívocamente sintético.
6. Agregar 13 pruebas de bloqueo y evaluación; ejecutar las pruebas del repo original.
7. Abrir issue para localizar PDF MINEM; cualquier importación genera SHA y revisión legal, no autohabilitación.

## Plan ejecutable — SPEC-027

**Gate de entrega:** G4 · **Dependencias aprobadas:** SPEC-026.

1. **Modelo/contratos:** definir request, response, objetos de dominio y política de validación en `docs/regulatory/, power-regulation/, tests/contract/`; separar entidades y DTO.
2. **Arquitectura:** casos de uso sin ORM/HTTP/LLM, puertos tipados y adaptadores reemplazables; usar monolito modular + workers para procesos intensivos.
3. **Persistencia y eventos:** migraciones/backups si hay estado; claves tenant, revisión y hash de procedencia; idempotencia para trabajos.
4. **API/Frontend:** exponer solo endpoints necesarios; OpenAPI versionado, cliente TS generado y UI con carga/error/ausencia de datos; controles no autorizados deben quedar inaccesibles.
5. **Algoritmo:** Auditar el Anexo 1 PIDE y aplicar sus métodos solo si la fuente primaria respalda el campo y fórmula. Nunca simular valores reales cuando faltan datos.
6. **Pruebas:** unitarias puras, contratos, integración aislada, fixtures reales autorizados o sintéticos etiquetados y E2E si corresponde.
7. **Métricas:** 15 formatos marcados pendientes hasta auditar PDF; costo anualizado ilustrativo y número de opciones condicionado al perfil. Parámetros numéricos/tolerancias se pactan usando benchmarks y se versionan antes de aprobar.
8. **Evidencias:** informe de testing, fuente científica/regulatoria, changelog, hash del input, salida y revisión del responsable.

**Skills/RAG sugerido:** usar skill del módulo y consultar `docs/scientific-evidence` mediante `python scripts/research/query_evidence.py --module regulation --limit 10`; si el módulo no está registrado, buscar por palabra clave y registrar ausencia de evidencia.

**Riesgos y controles:** acceso empresarial autorizado, exactitud física, dependencia normativa, evolución de contrato, presupuesto de cómputo y regresión. No usar secretos, datos privados ni herramientas destructivas sin permisos explícitos.
