# Grafo físico y GNN — soporte científico y reglas implementables

**Área de código:** `power-graph, power-topology, power-sciml`.  
**Consulta:** `python scripts/research/query_evidence.py --module graph --limit 12`.  
**Convención:** una ficha markdown describe una fuente o registro, **no contiene PDFs de terceros**.

## Tesis de arquitectura de este módulo
Operar sobre terminales, fases y estados de interruptor; las inferencias no reescriben red certificada.

## Qué está sustentado y qué es decisión UNITESIS
- **Evidencia externa:** las fichas enlazadas describen investigaciones, herramientas o normas existentes (calidad bibliográfica indicada individualmente).
- **Decisión de ingeniería UNITESIS:** adoptar interfaces y restricciones de aceptación diseñadas para este producto. No es conclusión causal de los artículos.
- **Vacío experimental:** no existe validación del módulo sobre VNR-GIS de distribuidoras dentro de esta biblioteca; hay que programar experimentos.

## Evidencia científica/tesis más directamente relacionada
- [REF-011 · Graph Networks as Learnable Physics Engines for Inference and Control](../sources/REF-011-graph-networks-as-learnable-physics-engines-for-inference-and-control.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.
- [REF-031 · Graph Attention Networks](../sources/REF-031-graph-attention-networks.md) — preprint, EN; `identificado_en_fuente_web`.
- [REF-032 · Semi-Supervised Classification with Graph Convolutional Networks](../sources/REF-032-semi-supervised-classification-with-graph-convolutional-networks.md) — preprint, EN; `identificado_en_fuente_web`.
- [REF-033 · Neural Relational Inference for Interacting Systems](../sources/REF-033-neural-relational-inference-for-interacting-systems.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.
- [REF-034 · Graph inductive biases in Transformers without Message Passing](../sources/REF-034-graph-inductive-biases-in-transformers-without-message-passing.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.
- [REF-037 · Graph Neural Networks and Their Applications in Power Systems: A Review](../sources/REF-037-graph-neural-networks-and-their-applications-in-power-systems-a-review.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.
- [REF-038 · Applications of Graph Computing and Graph Neural Networks in Power Systems: A Survey](../sources/REF-038-applications-of-graph-computing-and-graph-neural-networks-in-power-syste.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.
- [REF-079 · Spatio-Temporal GNNs for Power Grid State Estimation under Topological Changes](../sources/REF-079-spatio-temporal-gnns-for-power-grid-state-estimation-under-topological-c.md) — tesis_maestria, EN; `identificado_en_fuente_web`.
- [REF-080 · Adaptive Equivalent Models for Distribution Networks](../sources/REF-080-adaptive-equivalent-models-for-distribution-networks.md) — tesis_maestria, EN; `identificado_en_fuente_web`.
- [REF-127 · Graph Neural Networks and Their Applications in Power Systems (IEEE 2025)](../sources/REF-127-graph-neural-networks-and-their-applications-in-power-systems-ieee-2025.md) — articulo_o_preprint, EN; `importado_pendiente_auditoria`.
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
- [REF-039 · From Local to Global: A Graph RAG Approach to Query-Focused Summarization](../sources/REF-039-from-local-to-global-a-graph-rag-approach-to-query-focused-summarization.md) — preprint, EN; `identificado_en_fuente_web`.

## Documentación, guías o estándares útiles (no confundir con papers)
- [REF-184 · NetworkX](../sources/REF-184-networkx.md) — documentacion.

## Contrato, implementación y pruebas
- **Contrato funcional:** especificación en `specs/`, identificadores estables y validación de entrada / salida.
- **Propiedades no negociables:** Operar sobre terminales, fases y estados de interruptor; las inferencias no reescriben red certificada.
- **Benchmark mínimo propuesto:** Cambiar configuración de interruptores y comprobar componentes, islas y tensión contra solver.
- **Evidencias:** registrar commit, snapshot de red, escenario, seed, versiones de librerías y motor, unidades, tolerancias, tablas y logs sanitizados.
- **Control de cambios:** PR bloqueada si se ocultan incertidumbres o se afirma que una ficha es texto completo cuando no lo es.

## Skills responsables
- `unitesis-electric-graph`
- `unitesis-sciml-pinn-gnn`

## Palabras clave multilingües
Grafo físico y GNN; modularity; reproducibility; industrial validation
