# Plan — Registro criptográfico y blockchain permissioned optativo

**Estado:** DRAFT; no desplegado.

## Contexto y boundaries
Anclar hash de evidencia en registro verificable y comparar log firmado central vs Hyperledger Fabric y Besu en laboratorio aislado.

## Plan de implementación
1. Congelar diseño, ADRs y amenazas; especificar interfaces y versiones.
2. Construir el adaptador de referencia aislado, con fixtures sintéticos.
3. Verificar invariantes, seguridad, reproducibilidad y pruebas negativas.
4. Ejecutar integración con la API/workers y generación de evidencia.
5. Benchmark, revisión y PR según SDD y Git worktree.

## Tasks
- Implementar EvidenceStore + append-only signed log baseline
- Definir LedgerAnchorPort + schema y eventos
- Proof-of-concept Fabric private data con permisos
- Proof-of-concept Besu QBFT con n>=4 validators
- Informe ADR coste/beneficio/gobernanza y hardening claves

## Gates de aprobación
- La modificación de 1 byte de evidencia cambia el digest SHA-256.
- Caída de blockchain no invalida estudio ni altera su hash.
- No se permite anchor CONFIRMED sin transacción verificada.
- PR aporta benchmarks de costo, TPS, latencia y fault tolerance con métrica reproducible.

## Plan ejecutable — SPEC-012

**Gate de entrega:** G6 · **Dependencias aprobadas:** SPEC-011, SPEC-032.

1. **Modelo/contratos:** definir request, response, objetos de dominio y política de validación en `packages/python/power-ledger/, workers/ledger-anchoring/`; separar entidades y DTO.
2. **Arquitectura:** casos de uso sin ORM/HTTP/LLM, puertos tipados y adaptadores reemplazables; usar monolito modular + workers para procesos intensivos.
3. **Persistencia y eventos:** migraciones/backups si hay estado; claves tenant, revisión y hash de procedencia; idempotencia para trabajos.
4. **API/Frontend:** exponer solo endpoints necesarios; OpenAPI versionado, cliente TS generado y UI con carga/error/ausencia de datos; controles no autorizados deben quedar inaccesibles.
5. **Algoritmo:** Registrar anclajes verificables de evidencias con ledger opcional, manteniendo datos sensibles off-chain. Nunca simular valores reales cuando faltan datos.
6. **Pruebas:** unitarias puras, contratos, integración aislada, fixtures reales autorizados o sintéticos etiquetados y E2E si corresponde.
7. **Métricas:** Hash anclado es verificable e idempotente; ausencia de red blockchain no bloquea estudios pero sí anclajes requeridos. Parámetros numéricos/tolerancias se pactan usando benchmarks y se versionan antes de aprobar.
8. **Evidencias:** informe de testing, fuente científica/regulatoria, changelog, hash del input, salida y revisión del responsable.

**Skills/RAG sugerido:** usar skill del módulo y consultar `docs/scientific-evidence` mediante `python scripts/research/query_evidence.py --module blockchain --limit 10`; si el módulo no está registrado, buscar por palabra clave y registrar ausencia de evidencia.

**Riesgos y controles:** acceso empresarial autorizado, exactitud física, dependencia normativa, evolución de contrato, presupuesto de cómputo y regresión. No usar secretos, datos privados ni herramientas destructivas sin permisos explícitos.
