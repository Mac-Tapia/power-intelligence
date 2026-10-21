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
