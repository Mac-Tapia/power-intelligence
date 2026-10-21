# Plan — Fundación

1. Política de repositorio y constitución.
2. Paquetes Python con imports unidireccionales; solo el paquete domain implementa invariantes de ejemplo.
3. Script de worktrees sin borrado forzado.
4. CI mínima sin servicios externos.
5. Verificación local y evidencia del resultado.

## Plan ejecutable — SPEC-000

**Gate de entrega:** G0 · **Dependencias aprobadas:** ninguna.

1. **Modelo/contratos:** definir request, response, objetos de dominio y política de validación en `scripts/, .github/, .specify/, .cursor/`; separar entidades y DTO.
2. **Arquitectura:** casos de uso sin ORM/HTTP/LLM, puertos tipados y adaptadores reemplazables; usar monolito modular + workers para procesos intensivos.
3. **Persistencia y eventos:** migraciones/backups si hay estado; claves tenant, revisión y hash de procedencia; idempotencia para trabajos.
4. **API/Frontend:** exponer solo endpoints necesarios; OpenAPI versionado, cliente TS generado y UI con carga/error/ausencia de datos; controles no autorizados deben quedar inaccesibles.
5. **Algoritmo:** Mantener base monorepo, separación hexagonal y herramientas de desarrollo reproducibles. Nunca simular valores reales cuando faltan datos.
6. **Pruebas:** unitarias puras, contratos, integración aislada, fixtures reales autorizados o sintéticos etiquetados y E2E si corresponde.
7. **Métricas:** Un checkout limpio pasa verificación, CI y tests de arranque sin credenciales externas. Parámetros numéricos/tolerancias se pactan usando benchmarks y se versionan antes de aprobar.
8. **Evidencias:** informe de testing, fuente científica/regulatoria, changelog, hash del input, salida y revisión del responsable.

**Skills/RAG sugerido:** usar skill del módulo y consultar `docs/scientific-evidence` mediante `python scripts/research/query_evidence.py --module architecture --limit 10`; si el módulo no está registrado, buscar por palabra clave y registrar ausencia de evidencia.

**Riesgos y controles:** acceso empresarial autorizado, exactitud física, dependencia normativa, evolución de contrato, presupuesto de cómputo y regresión. No usar secretos, datos privados ni herramientas destructivas sin permisos explícitos.
