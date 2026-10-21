# Plan — Mercado simulado de energía/flexibilidad condicionado a red

**Estado:** DRAFT; no desplegado.

## Contexto y boundaries
Evaluar matching de ofertas prosumidor-BESS-EV con pérdidas, congestión, seguridad y legalidad, sin asumir habilitación peruana de venta P2P.

## Plan de implementación
1. Congelar diseño, ADRs y amenazas; especificar interfaces y versiones.
2. Construir el adaptador de referencia aislado, con fixtures sintéticos.
3. Verificar invariantes, seguridad, reproducibilidad y pruebas negativas.
4. Ejecutar integración con la API/workers y generación de evidencia.
5. Benchmark, revisión y PR según SDD y Git worktree.

## Tasks
- Definir EnergyTradeProposal y representación de agentes/intervalos
- Solver acoplado: matching -> security-constrained validation -> rechazo/ajuste
- BESS SOC y EV demandas temporales; minimización multiobjetivo
- Simular pérdidas/cargos de red/restricciones por alimentador
- Compliance Peru legal-gate y piloto experimental opt-in

## Gates de aprobación
- Oferta que viola tensión o ampacidad es rechazada.
- No settlement si faltan medición aprobada/solver o licencia.
- No hay trades duplicados en reintentos y fallas de red.
- Simulaciones en IEEE33/IEEE123 sintéticos comparan bienestar, pérdidas y equidad.

## Plan ejecutable — SPEC-013

**Gate de entrega:** G6 · **Dependencias aprobadas:** SPEC-011, SPEC-012, SPEC-019, SPEC-028.

1. **Modelo/contratos:** definir request, response, objetos de dominio y política de validación en `packages/python/power-market/, workers/market-clearing/`; separar entidades y DTO.
2. **Arquitectura:** casos de uso sin ORM/HTTP/LLM, puertos tipados y adaptadores reemplazables; usar monolito modular + workers para procesos intensivos.
3. **Persistencia y eventos:** migraciones/backups si hay estado; claves tenant, revisión y hash de procedencia; idempotencia para trabajos.
4. **API/Frontend:** exponer solo endpoints necesarios; OpenAPI versionado, cliente TS generado y UI con carga/error/ausencia de datos; controles no autorizados deben quedar inaccesibles.
5. **Algoritmo:** Simular escenarios de intercambio energético P2P con factibilidad física y sin liquidación real. Nunca simular valores reales cuando faltan datos.
6. **Pruebas:** unitarias puras, contratos, integración aislada, fixtures reales autorizados o sintéticos etiquetados y E2E si corresponde.
7. **Métricas:** Transacciones se generan en modo simulación y toda alternativa es rechazada si viola AC/energía/reglas aplicables. Parámetros numéricos/tolerancias se pactan usando benchmarks y se versionan antes de aprobar.
8. **Evidencias:** informe de testing, fuente científica/regulatoria, changelog, hash del input, salida y revisión del responsable.

**Skills/RAG sugerido:** usar skill del módulo y consultar `docs/scientific-evidence` mediante `python scripts/research/query_evidence.py --module market --limit 10`; si el módulo no está registrado, buscar por palabra clave y registrar ausencia de evidencia.

**Riesgos y controles:** acceso empresarial autorizado, exactitud física, dependencia normativa, evolución de contrato, presupuesto de cómputo y regresión. No usar secretos, datos privados ni herramientas destructivas sin permisos explícitos.
