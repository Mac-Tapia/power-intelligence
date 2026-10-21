# Estudios eléctricos verificables — soporte científico y reglas implementables

**Área de código:** `power-simulation, PowerFlowPort`.  
**Consulta:** `python scripts/research/query_evidence.py --module solver --limit 12`.  
**Convención:** una ficha markdown describe una fuente o registro, **no contiene PDFs de terceros**.

## Tesis de arquitectura de este módulo
Separar AC equilibrado, trifásico desequilibrado, cortocircuito y dinámica; cada resultado registra solver y tolerancias.

## Qué está sustentado y qué es decisión UNITESIS
- **Evidencia externa:** las fichas enlazadas describen investigaciones, herramientas o normas existentes (calidad bibliográfica indicada individualmente).
- **Decisión de ingeniería UNITESIS:** adoptar interfaces y restricciones de aceptación diseñadas para este producto. No es conclusión causal de los artículos.
- **Vacío experimental:** no existe validación del módulo sobre VNR-GIS de distribuidoras dentro de esta biblioteca; hay que programar experimentos.

## Evidencia científica/tesis más directamente relacionada
- [REF-040 · Pandapower—An Open-Source Python Tool for Convenient Modeling Analysis and Optimization](../sources/REF-040-pandapoweran-open-source-python-tool-for-convenient-modeling-analysis-an.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-041 · PyPSA: Python for Power System Analysis](../sources/REF-041-pypsa-python-for-power-system-analysis.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-042 · MATPOWER: Steady-State Operations Planning and Analysis Tools](../sources/REF-042-matpower-steady-state-operations-planning-and-analysis-tools.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-044 · PowerModelsDistribution.jl: an open-source framework for exploring distribution power flow formulations](../sources/REF-044-powermodelsdistribution-jl-an-open-source-framework-for-exploring-distri.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-066 · Otimização da manutenção centrada na confiabilidade em redes de distribuição de energia elétrica](../sources/REF-066-otimizacao-da-manutencao-centrada-na-confiabilidade-em-redes-de-distribu.md) — tesis_doctoral, PT; `identificado_en_fuente_web`.
- [REF-069 · Stabilité des réseaux électriques de distribution en présence de productions d’énergie renouvelable](../sources/REF-069-stabilite-des-reseaux-electriques-de-distribution-en-presence-de-product.md) — tesis_doctoral, FR; `identificado_en_fuente_web`.
- [REF-070 · Supervision énergetique des réseaux de distribution](../sources/REF-070-supervision-energetique-des-reseaux-de-distribution.md) — tesis_doctoral, FR; `identificado_en_fuente_web`.
- [REF-073 · Die Aufnahmefähigkeit von Niederspannungsverteilnetzen für Photovoltaik](../sources/REF-073-die-aufnahmefahigkeit-von-niederspannungsverteilnetzen-fur-photovoltaik.md) — tesis_doctoral, DE; `identificado_en_fuente_web`.
- [REF-087 · Otimização baseada em confiabilidade de planos de manutenção de sistemas de distribuição](../sources/REF-087-otimizacao-baseada-em-confiabilidade-de-planos-de-manutencao-de-sistemas.md) — tesis_maestria, PT; `identificado_en_fuente_web`.
- [REF-131 · pandapower: Open Source Python Tool (2018) / bibliografía](../sources/REF-131-pandapower-open-source-python-tool-2018-bibliografia.md) — articulo_o_preprint, EN; `importado_pendiente_auditoria`.
- [REF-010 · GraphCast: Learned Global Weather Forecasting](../sources/REF-010-graphcast-learned-global-weather-forecasting.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.
- [REF-012 · GenCast: learning skillful ensemble forecasting of medium-range weather](../sources/REF-012-gencast-learning-skillful-ensemble-forecasting-of-medium-range-weather.md) — preprint, EN; `identificado_en_fuente_web`.
- [REF-024 · Physics-informed neural networks: A deep learning framework for solving forward and inverse problems](../sources/REF-024-physics-informed-neural-networks-a-deep-learning-framework-for-solving-f.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-025 · Physics-informed machine learning](../sources/REF-025-physics-informed-machine-learning.md) — articulo_revision, EN; `identificado_en_fuente_web`.
- [REF-026 · Neural Operator: Learning Maps Between Function Spaces](../sources/REF-026-neural-operator-learning-maps-between-function-spaces.md) — preprint, EN; `identificado_en_fuente_web`.
- [REF-027 · Fourier Neural Operator for Parametric Partial Differential Equations](../sources/REF-027-fourier-neural-operator-for-parametric-partial-differential-equations.md) — preprint, EN; `identificado_en_fuente_web`.
- [REF-028 · Learning nonlinear operators via DeepONet](../sources/REF-028-learning-nonlinear-operators-via-deeponet.md) — articulo_revista, EN; `metadatos_pendientes_confirmacion`.
- [REF-029 · Understanding and mitigating gradient pathologies in physics-informed neural networks](../sources/REF-029-understanding-and-mitigating-gradient-pathologies-in-physics-informed-ne.md) — preprint, EN; `identificado_en_fuente_web`.
- [REF-030 · A survey on physics-informed neural networks: state of the art and future research](../sources/REF-030-a-survey-on-physics-informed-neural-networks-state-of-the-art-and-future.md) — preprint, EN; `metadatos_pendientes_confirmacion`.
- [REF-035 · Physics-informed GNN for medium-high voltage AC power flow with edge-aware attention](../sources/REF-035-physics-informed-gnn-for-medium-high-voltage-ac-power-flow-with-edge-awa.md) — preprint, EN; `identificado_en_fuente_web`.
- [REF-036 · PowerModelsGAT-AI: Physics-Informed Graph Attention for Multi-System Power Flow](../sources/REF-036-powermodelsgat-ai-physics-informed-graph-attention-for-multi-system-powe.md) — preprint, EN; `identificado_en_fuente_web`.
- [REF-043 · PowerModels.jl: An Open-Source Framework for Exploring Power Flow Formulations](../sources/REF-043-powermodels-jl-an-open-source-framework-for-exploring-power-flow-formula.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.

## Documentación, guías o estándares útiles (no confundir con papers)
- [REF-152 · Power System Stability and Control, 2nd ed. — Kundur & Malik (2022)](../sources/REF-152-power-system-stability-and-control-2nd-ed-kundur-malik-2022.md) — libro.
- [REF-155 · OpenDSS](../sources/REF-155-opendss.md) — documentacion.
- [REF-156 · DSS-Extensions](../sources/REF-156-dss-extensions.md) — documentacion.
- [REF-157 · pandapower](../sources/REF-157-pandapower.md) — documentacion.
- [REF-161 · GridCal](../sources/REF-161-gridcal.md) — documentacion.
- [REF-162 · GridLAB-D](../sources/REF-162-gridlab-d.md) — documentacion.
- [REF-163 · MATPOWER](../sources/REF-163-matpower.md) — documentacion.
- [REF-186 · IEEE PES Distribution Test Feeders](../sources/REF-186-ieee-pes-distribution-test-feeders.md) — norma_o_estandar.

## Contrato, implementación y pruebas
- **Contrato funcional:** especificación en `specs/`, identificadores estables y validación de entrada / salida.
- **Propiedades no negociables:** Separar AC equilibrado, trifásico desequilibrado, cortocircuito y dinámica; cada resultado registra solver y tolerancias.
- **Benchmark mínimo propuesto:** Comparar IEEE 13/34/123 y otros casos disponibles, magnitudes, ángulos, pérdidas, KCL, convergencia.
- **Evidencias:** registrar commit, snapshot de red, escenario, seed, versiones de librerías y motor, unidades, tolerancias, tablas y logs sanitizados.
- **Control de cambios:** PR bloqueada si se ocultan incertidumbres o se afirma que una ficha es texto completo cuando no lo es.

## Skills responsables
- `unitesis-power-simulation`
- `unitesis-testing-qa`

## Palabras clave multilingües
AC power flow; unbalanced distribution network; flujo de potencia; fluxo de potência; Lastfluss; écoulement de puissance
