# GIS, adquisición y topología de redes — soporte científico y reglas implementables

**Área de código:** `ingestion, topology, PostGIS`.  
**Consulta:** `python scripts/research/query_evidence.py --module gis --limit 12`.  
**Convención:** una ficha markdown describe una fuente o registro, **no contiene PDFs de terceros**.

## Tesis de arquitectura de este módulo
La cartografía, conectividad terminal-fase y layout del unifilar requieren modelos diferentes.

## Qué está sustentado y qué es decisión UNITESIS
- **Evidencia externa:** las fichas enlazadas describen investigaciones, herramientas o normas existentes (calidad bibliográfica indicada individualmente).
- **Decisión de ingeniería UNITESIS:** adoptar interfaces y restricciones de aceptación diseñadas para este producto. No es conclusión causal de los artículos.
- **Vacío experimental:** no existe validación del módulo sobre VNR-GIS de distribuidoras dentro de esta biblioteca; hay que programar experimentos.

## Evidencia científica/tesis más directamente relacionada
- [REF-099 · OpenStreetMap: User-Generated Street Maps](../sources/REF-099-openstreetmap-user-generated-street-maps.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-100 · Citizens as sensors: the world of volunteered geography](../sources/REF-100-citizens-as-sensors-the-world-of-volunteered-geography.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-011 · Graph Networks as Learnable Physics Engines for Inference and Control](../sources/REF-011-graph-networks-as-learnable-physics-engines-for-inference-and-control.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.
- [REF-031 · Graph Attention Networks](../sources/REF-031-graph-attention-networks.md) — preprint, EN; `identificado_en_fuente_web`.
- [REF-032 · Semi-Supervised Classification with Graph Convolutional Networks](../sources/REF-032-semi-supervised-classification-with-graph-convolutional-networks.md) — preprint, EN; `identificado_en_fuente_web`.
- [REF-033 · Neural Relational Inference for Interacting Systems](../sources/REF-033-neural-relational-inference-for-interacting-systems.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.
- [REF-034 · Graph inductive biases in Transformers without Message Passing](../sources/REF-034-graph-inductive-biases-in-transformers-without-message-passing.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.
- [REF-037 · Graph Neural Networks and Their Applications in Power Systems: A Review](../sources/REF-037-graph-neural-networks-and-their-applications-in-power-systems-a-review.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.
- [REF-038 · Applications of Graph Computing and Graph Neural Networks in Power Systems: A Survey](../sources/REF-038-applications-of-graph-computing-and-graph-neural-networks-in-power-syste.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.
- [REF-040 · Pandapower—An Open-Source Python Tool for Convenient Modeling Analysis and Optimization](../sources/REF-040-pandapoweran-open-source-python-tool-for-convenient-modeling-analysis-an.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-041 · PyPSA: Python for Power System Analysis](../sources/REF-041-pypsa-python-for-power-system-analysis.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-042 · MATPOWER: Steady-State Operations Planning and Analysis Tools](../sources/REF-042-matpower-steady-state-operations-planning-and-analysis-tools.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-044 · PowerModelsDistribution.jl: an open-source framework for exploring distribution power flow formulations](../sources/REF-044-powermodelsdistribution-jl-an-open-source-framework-for-exploring-distri.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-066 · Otimização da manutenção centrada na confiabilidade em redes de distribuição de energia elétrica](../sources/REF-066-otimizacao-da-manutencao-centrada-na-confiabilidade-em-redes-de-distribu.md) — tesis_doctoral, PT; `identificado_en_fuente_web`.
- [REF-069 · Stabilité des réseaux électriques de distribution en présence de productions d’énergie renouvelable](../sources/REF-069-stabilite-des-reseaux-electriques-de-distribution-en-presence-de-product.md) — tesis_doctoral, FR; `identificado_en_fuente_web`.
- [REF-070 · Supervision énergetique des réseaux de distribution](../sources/REF-070-supervision-energetique-des-reseaux-de-distribution.md) — tesis_doctoral, FR; `identificado_en_fuente_web`.
- [REF-073 · Die Aufnahmefähigkeit von Niederspannungsverteilnetzen für Photovoltaik](../sources/REF-073-die-aufnahmefahigkeit-von-niederspannungsverteilnetzen-fur-photovoltaik.md) — tesis_doctoral, DE; `identificado_en_fuente_web`.
- [REF-079 · Spatio-Temporal GNNs for Power Grid State Estimation under Topological Changes](../sources/REF-079-spatio-temporal-gnns-for-power-grid-state-estimation-under-topological-c.md) — tesis_maestria, EN; `identificado_en_fuente_web`.
- [REF-080 · Adaptive Equivalent Models for Distribution Networks](../sources/REF-080-adaptive-equivalent-models-for-distribution-networks.md) — tesis_maestria, EN; `identificado_en_fuente_web`.
- [REF-087 · Otimização baseada em confiabilidade de planos de manutenção de sistemas de distribuição](../sources/REF-087-otimizacao-baseada-em-confiabilidade-de-planos-de-manutencao-de-sistemas.md) — tesis_maestria, PT; `identificado_en_fuente_web`.
- [REF-096 · D3: Data-Driven Documents](../sources/REF-096-d3-data-driven-documents.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-097 · Vega-Lite: A Grammar of Interactive Graphics](../sources/REF-097-vega-lite-a-grammar-of-interactive-graphics.md) — articulo_revista, EN; `identificado_en_fuente_web`.

## Documentación, guías o estándares útiles (no confundir con papers)
- [REF-116 · ENTSO-E CGMES Library (2026)](../sources/REF-116-entso-e-cgmes-library-2026.md) — norma_o_estandar.
- [REF-173 · GeoPandas](../sources/REF-173-geopandas.md) — documentacion.
- [REF-174 · PostGIS](../sources/REF-174-postgis.md) — documentacion.

## Contrato, implementación y pruebas
- **Contrato funcional:** especificación en `specs/`, identificadores estables y validación de entrada / salida.
- **Propiedades no negociables:** La cartografía, conectividad terminal-fase y layout del unifilar requieren modelos diferentes.
- **Benchmark mínimo propuesto:** Fixtures con nodos huérfanos, tramos invertidos, CRS incorrecto, bifásicos y switches abiertos.
- **Evidencias:** registrar commit, snapshot de red, escenario, seed, versiones de librerías y motor, unidades, tolerancias, tablas y logs sanitizados.
- **Control de cambios:** PR bloqueada si se ocultan incertidumbres o se afirma que una ficha es texto completo cuando no lo es.

## Skills responsables
- `unitesis-gis-ingestion`
- `unitesis-electric-graph`

## Palabras clave multilingües
GIS electrical network; topología; topologia; Netzmodell; géoréférencement; VNR-GIS
