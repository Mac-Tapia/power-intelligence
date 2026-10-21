# MADRL seguro y critic centralizado — soporte científico y reglas implementables

**Área de código:** `power-marl, agent-runtime`.  
**Consulta:** `python scripts/research/query_evidence.py --module marl --limit 12`.  
**Convención:** una ficha markdown describe una fuente o registro, **no contiene PDFs de terceros**.

## Tesis de arquitectura de este módulo
Entrenar en gemelo digital sandbox con restricciones duras del simulador y comparadores deterministas.

## Qué está sustentado y qué es decisión UNITESIS
- **Evidencia externa:** las fichas enlazadas describen investigaciones, herramientas o normas existentes (calidad bibliográfica indicada individualmente).
- **Decisión de ingeniería UNITESIS:** adoptar interfaces y restricciones de aceptación diseñadas para este producto. No es conclusión causal de los artículos.
- **Vacío experimental:** no existe validación del módulo sobre VNR-GIS de distribuidoras dentro de esta biblioteca; hay que programar experimentos.

## Evidencia científica/tesis más directamente relacionada
- [REF-049 · Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments](../sources/REF-049-multi-agent-actor-critic-for-mixed-cooperative-competitive-environments.md) — preprint, EN; `identificado_en_fuente_web`.
- [REF-050 · QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning](../sources/REF-050-qmix-monotonic-value-function-factorisation-for-deep-multi-agent-reinfor.md) — preprint, EN; `identificado_en_fuente_web`.
- [REF-051 · Multi-Agent Reinforcement Learning: A Selective Overview of Theories and Algorithms](../sources/REF-051-multi-agent-reinforcement-learning-a-selective-overview-of-theories-and-.md) — preprint, EN; `identificado_en_fuente_web`.
- [REF-052 · PPO: Proximal Policy Optimization Algorithms](../sources/REF-052-ppo-proximal-policy-optimization-algorithms.md) — preprint, EN; `identificado_en_fuente_web`.
- [REF-053 · Multi-Agent Reinforcement Learning for Energy Networks](../sources/REF-053-multi-agent-reinforcement-learning-for-energy-networks.md) — preprint, EN; `identificado_en_fuente_web`.
- [REF-117 · Reinforcement Learning Meets the Power Grid, Jin (2025)](../sources/REF-117-reinforcement-learning-meets-the-power-grid-jin-2025.md) — articulo_o_preprint, EN; `importado_pendiente_auditoria`.
- [REF-118 · Reinforcement Learning for Efficient Power Systems Planning (2024)](../sources/REF-118-reinforcement-learning-for-efficient-power-systems-planning-2024.md) — articulo_o_preprint, EN; `importado_pendiente_auditoria`.
- [REF-119 · A Review of Smart Grid Evolution and Reinforcement Learning (2025)](../sources/REF-119-a-review-of-smart-grid-evolution-and-reinforcement-learning-2025.md) — articulo_o_preprint, EN; `importado_pendiente_auditoria`.
- [REF-124 · Multi-agent reinforcement learning for resources allocation optimization: survey (2025)](../sources/REF-124-multi-agent-reinforcement-learning-for-resources-allocation-optimization.md) — articulo_o_preprint, EN; `importado_pendiente_auditoria`.
- [REF-126 · Multi-agent BESS collaborative control, Applied Energy (2024)](../sources/REF-126-multi-agent-bess-collaborative-control-applied-energy-2024.md) — articulo_o_preprint, EN; `importado_pendiente_auditoria`.
- [REF-128 · Reinforcement Learning for Optimizing Renewable Energy Utilization in Smart Grids (2026)](../sources/REF-128-reinforcement-learning-for-optimizing-renewable-energy-utilization-in-sm.md) — articulo_o_preprint, EN; `importado_pendiente_auditoria`.
- [REF-130 · A Survey of Multi-Agent Systems for Smartgrids (2024)](../sources/REF-130-a-survey-of-multi-agent-systems-for-smartgrids-2024.md) — articulo_o_preprint, EN; `importado_pendiente_auditoria`.
- [REF-138 · Reinforcement Learning for Adaptive Distribution Network — U Alberta](../sources/REF-138-reinforcement-learning-for-adaptive-distribution-network-u-alberta.md) — tesis, EN; `importado_pendiente_auditoria`.

## Documentación, guías o estándares útiles (no confundir con papers)
- [REF-171 · Ray RLlib](../sources/REF-171-ray-rllib.md) — documentacion.
- [REF-172 · PettingZoo](../sources/REF-172-pettingzoo.md) — documentacion.

## Contrato, implementación y pruebas
- **Contrato funcional:** especificación en `specs/`, identificadores estables y validación de entrada / salida.
- **Propiedades no negociables:** Entrenar en gemelo digital sandbox con restricciones duras del simulador y comparadores deterministas.
- **Benchmark mínimo propuesto:** Curva de aprendizaje, generalización, tasa de violación física y recuperación tras fallos.
- **Evidencias:** registrar commit, snapshot de red, escenario, seed, versiones de librerías y motor, unidades, tolerancias, tablas y logs sanitizados.
- **Control de cambios:** PR bloqueada si se ocultan incertidumbres o se afirma que una ficha es texto completo cuando no lo es.

## Skills responsables
- `unitesis-marl-llm`
- `unitesis-testing-qa`

## Palabras clave multilingües
MADRL seguro y critic centralizado; modularity; reproducibility; industrial validation
