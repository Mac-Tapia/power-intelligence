# Expansión, optimización y planificación — soporte científico y reglas implementables

**Área de código:** `power-optimization, power-market`.  
**Consulta:** `python scripts/research/query_evidence.py --module op --limit 12`.  
**Convención:** una ficha markdown describe una fuente o registro, **no contiene PDFs de terceros**.

## Tesis de arquitectura de este módulo
Funciones objetivo CAPEX, OPEX, pérdidas, resiliencia, emisiones y riesgo con restricciones AC.

## Qué está sustentado y qué es decisión UNITESIS
- **Evidencia externa:** las fichas enlazadas describen investigaciones, herramientas o normas existentes (calidad bibliográfica indicada individualmente).
- **Decisión de ingeniería UNITESIS:** adoptar interfaces y restricciones de aceptación diseñadas para este producto. No es conclusión causal de los artículos.
- **Vacío experimental:** no existe validación del módulo sobre VNR-GIS de distribuidoras dentro de esta biblioteca; hay que programar experimentos.

## Evidencia científica/tesis más directamente relacionada
- [REF-043 · PowerModels.jl: An Open-Source Framework for Exploring Power Flow Formulations](../sources/REF-043-powermodels-jl-an-open-source-framework-for-exploring-power-flow-formula.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.
- [REF-045 · Optimal distributed generation planning in active distribution networks considering integration of energy storage](../sources/REF-045-optimal-distributed-generation-planning-in-active-distribution-networks-.md) — preprint, EN; `identificado_en_fuente_web`.
- [REF-046 · Optimal Generation and Transmission Expansion Planning Addressing Short-Term Constraints](../sources/REF-046-optimal-generation-and-transmission-expansion-planning-addressing-short-.md) — preprint, EN; `identificado_en_fuente_web`.
- [REF-047 · Stochastic Multistage Co-optimization of Generation and Transmission Expansion Planning](../sources/REF-047-stochastic-multistage-co-optimization-of-generation-and-transmission-exp.md) — preprint, EN; `identificado_en_fuente_web`.
- [REF-048 · Robust Dynamic Transmission and Renewable Generation Expansion Planning](../sources/REF-048-robust-dynamic-transmission-and-renewable-generation-expansion-planning.md) — preprint, EN; `identificado_en_fuente_web`.
- [REF-064 · Análisis de la Planificación de Redes Eléctricas en España](../sources/REF-064-analisis-de-la-planificacion-de-redes-electricas-en-espana.md) — tesis, ES; `identificado_en_fuente_web`.
- [REF-065 · Planejamento da expansão de sistemas de distribuição de energia elétrica considerando restauração](../sources/REF-065-planejamento-da-expansao-de-sistemas-de-distribuicao-de-energia-eletrica.md) — tesis_doctoral, PT; `identificado_en_fuente_web`.
- [REF-067 · Modelo para planejamento da expansão de sistemas de distribuição considerando confiabilidade](../sources/REF-067-modelo-para-planejamento-da-expansao-de-sistemas-de-distribuicao-conside.md) — tesis, PT; `identificado_en_fuente_web`.
- [REF-068 · Intégration du stockage dans les méthodes de planification des réseaux BT](../sources/REF-068-integration-du-stockage-dans-les-methodes-de-planification-des-reseaux-b.md) — tesis_doctoral, FR; `identificado_en_fuente_web`.
- [REF-071 · Synthèse robuste de dispositifs de stockage pour l'optimisation de micro-réseaux](../sources/REF-071-synthese-robuste-de-dispositifs-de-stockage-pour-l-optimisation-de-micro.md) — tesis_doctoral, FR; `identificado_en_fuente_web`.
- [REF-072 · Optimizing cross-linked infrastructure for future energy systems](../sources/REF-072-optimizing-cross-linked-infrastructure-for-future-energy-systems.md) — tesis_doctoral, DE; `identificado_en_fuente_web`.
- [REF-074 · Energy transition and sector coupling: the impact of renewable hydrogen](../sources/REF-074-energy-transition-and-sector-coupling-the-impact-of-renewable-hydrogen.md) — tesis_doctoral, EN; `identificado_en_fuente_web`.
- [REF-076 · Autonomous optimal Power Flow via Convex Solution - Sequential Linear Programming](../sources/REF-076-autonomous-optimal-power-flow-via-convex-solution-sequential-linear-prog.md) — tesis_doctoral, EN; `identificado_en_fuente_web`.
- [REF-077 · Computational Methods for Fast and Secure Distributed Optimal Power Flow](../sources/REF-077-computational-methods-for-fast-and-secure-distributed-optimal-power-flow.md) — tesis_doctoral, EN; `identificado_en_fuente_web`.
- [REF-083 · Optimising Qatar's energy transition through model-based analysis](../sources/REF-083-optimising-qatar-s-energy-transition-through-model-based-analysis.md) — tesis_doctoral, EN; `identificado_en_fuente_web`.
- [REF-084 · Ubicación óptima de generación distribuida en el sistema de distribución](../sources/REF-084-ubicacion-optima-de-generacion-distribuida-en-el-sistema-de-distribucion.md) — tesis, ES; `identificado_en_fuente_web`.
- [REF-085 · Planificación óptima de la generación distribuida en redes de distribución](../sources/REF-085-planificacion-optima-de-la-generacion-distribuida-en-redes-de-distribuci.md) — tesis_doctoral, ES; `identificado_en_fuente_web`.
- [REF-086 · Planeamiento de la generación distribuida en redes eléctricas](../sources/REF-086-planeamiento-de-la-generacion-distribuida-en-redes-electricas.md) — tesis_doctoral, ES; `identificado_en_fuente_web`.
- [REF-088 · Reconfiguração otimizada de redes de distribuição de energia elétrica](../sources/REF-088-reconfiguracao-otimizada-de-redes-de-distribuicao-de-energia-eletrica.md) — tesis, PT; `identificado_en_fuente_web`.
- [REF-102 · Planejamento integrado de redes de distribuição de energia elétrica com fontes renováveis de geração distribuída na média e baixa tensão](../sources/REF-102-planejamento-integrado-de-redes-de-distribuicao-de-energia-eletrica-com-.md) — tesis_doctoral, PT; `identificado_en_fuente_web`.
- [REF-103 · Planejamento de redes de distribuição de energia elétrica de média e baixa tensão](../sources/REF-103-planejamento-de-redes-de-distribuicao-de-energia-eletrica-de-media-e-bai.md) — tesis_doctoral, PT; `identificado_en_fuente_web`.
- [REF-104 · Reconfiguração de redes de distribuição de energia elétrica através de um algoritmo de busca dispersa](../sources/REF-104-reconfiguracao-de-redes-de-distribuicao-de-energia-eletrica-atraves-de-u.md) — tesis_maestria, PT; `identificado_en_fuente_web`.

## Documentación, guías o estándares útiles (no confundir con papers)
- [REF-013 · Discovering novel algorithms with AlphaTensor](../sources/REF-013-discovering-novel-algorithms-with-alphatensor.md) — divulgacion_investigacion.
- [REF-014 · AlphaChip: reinforcement learning for chip placement](../sources/REF-014-alphachip-reinforcement-learning-for-chip-placement.md) — divulgacion_investigacion.
- [REF-015 · AlphaEvolve: an evolutionary coding agent](../sources/REF-015-alphaevolve-an-evolutionary-coding-agent.md) — divulgacion_investigacion.
- [REF-165 · Pyomo](../sources/REF-165-pyomo.md) — documentacion.
- [REF-166 · pymoo](../sources/REF-166-pymoo.md) — documentacion.
- [REF-167 · DEAP](../sources/REF-167-deap.md) — documentacion.

## Contrato, implementación y pruebas
- **Contrato funcional:** especificación en `specs/`, identificadores estables y validación de entrada / salida.
- **Propiedades no negociables:** Funciones objetivo CAPEX, OPEX, pérdidas, resiliencia, emisiones y riesgo con restricciones AC.
- **Benchmark mínimo propuesto:** Comparar óptimo/pareto vs baseline; reproducir factibilidad N-1, no anticipatividad y costos.
- **Evidencias:** registrar commit, snapshot de red, escenario, seed, versiones de librerías y motor, unidades, tolerancias, tablas y logs sanitizados.
- **Control de cambios:** PR bloqueada si se ocultan incertidumbres o se afirma que una ficha es texto completo cuando no lo es.

## Skills responsables
- `unitesis-power-simulation`
- `unitesis-evidence-audit`

## Palabras clave multilingües
optimal expansion planning; planificación eléctrica; planejamento da expansão; Netzausbauplanung; planification des réseaux
