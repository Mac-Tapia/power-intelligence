# Plan — Red P2P segura para colaboración entre nodos

**Estado:** DRAFT; no desplegado.

## Contexto y boundaries
Permitir mensajería de escenarios y evidencias entre instituciones autorizadas con independencia del comercio de energía y sin comandos SCADA.

## Plan de implementación
1. Congelar diseño, ADRs y amenazas; especificar interfaces y versiones.
2. Construir el adaptador de referencia aislado, con fixtures sintéticos.
3. Verificar invariantes, seguridad, reproducibilidad y pruebas negativas.
4. Ejecutar integración con la API/workers y generación de evidencia.
5. Benchmark, revisión y PR según SDD y Git worktree.

## Tasks
- Definir Envelopes P2P v1 y port PeerTransport
- Implementar adaptador broker/test primero, suite de autentificación
- Inbox/outbox, anti-replay, TTL, métricas, resiliencia
- Evaluar libp2p/relays/permissioning como ADR
- Integrar panel de peers y trazas auditables sin exponer secretos

## Gates de aprobación
- Peer desconocido rechazado, mensaje expirado/repetido rechazado.
- Rotación de claves y partición/reconexión sin re-ejecutar duplicados.
- Cualquier mensaje sobre SCADA/maniobras prohibido por contrato.
- Escenarios de prueba no atraviesan el boundary de tenant.

## Plan ejecutable — SPEC-011

**Gate de entrega:** G6 · **Dependencias aprobadas:** SPEC-005, SPEC-010, SPEC-035.

1. **Modelo/contratos:** definir request, response, objetos de dominio y política de validación en `packages/python/power-p2p/, workers/p2p-sync/`; separar entidades y DTO.
2. **Arquitectura:** casos de uso sin ORM/HTTP/LLM, puertos tipados y adaptadores reemplazables; usar monolito modular + workers para procesos intensivos.
3. **Persistencia y eventos:** migraciones/backups si hay estado; claves tenant, revisión y hash de procedencia; idempotencia para trabajos.
4. **API/Frontend:** exponer solo endpoints necesarios; OpenAPI versionado, cliente TS generado y UI con carga/error/ausencia de datos; controles no autorizados deben quedar inaccesibles.
5. **Algoritmo:** Permitir federación P2P entre instancias autorizadas para intercambio de información, sin maniobra remota. Nunca simular valores reales cuando faltan datos.
6. **Pruebas:** unitarias puras, contratos, integración aislada, fixtures reales autorizados o sintéticos etiquetados y E2E si corresponde.
7. **Métricas:** Peers autenticados, replays detectados, particiones recuperables y topología sensible no expuesta por defecto. Parámetros numéricos/tolerancias se pactan usando benchmarks y se versionan antes de aprobar.
8. **Evidencias:** informe de testing, fuente científica/regulatoria, changelog, hash del input, salida y revisión del responsable.

**Skills/RAG sugerido:** usar skill del módulo y consultar `docs/scientific-evidence` mediante `python scripts/research/query_evidence.py --module p2p --limit 10`; si el módulo no está registrado, buscar por palabra clave y registrar ausencia de evidencia.

**Riesgos y controles:** acceso empresarial autorizado, exactitud física, dependencia normativa, evolución de contrato, presupuesto de cómputo y regresión. No usar secretos, datos privados ni herramientas destructivas sin permisos explícitos.
