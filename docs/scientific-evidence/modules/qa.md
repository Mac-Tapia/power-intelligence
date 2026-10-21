# Pruebas de aceptación científica y de agentes — soporte científico y reglas implementables

**Área de código:** `tests, benchmarks, evidence`.  
**Consulta:** `python scripts/research/query_evidence.py --module qa --limit 12`.  
**Convención:** una ficha markdown describe una fuente o registro, **no contiene PDFs de terceros**.

## Tesis de arquitectura de este módulo
Los tests de scaffold NO prueban precisión eléctrica ni legalidad; crear datasets de referencia.

## Qué está sustentado y qué es decisión UNITESIS
- **Evidencia externa:** las fichas enlazadas describen investigaciones, herramientas o normas existentes (calidad bibliográfica indicada individualmente).
- **Decisión de ingeniería UNITESIS:** adoptar interfaces y restricciones de aceptación diseñadas para este producto. No es conclusión causal de los artículos.
- **Vacío experimental:** no existe validación del módulo sobre VNR-GIS de distribuidoras dentro de esta biblioteca; hay que programar experimentos.

## Evidencia científica/tesis más directamente relacionada
- [REF-003 · Bigtable: A Distributed Storage System for Structured Data](../sources/REF-003-bigtable-a-distributed-storage-system-for-structured-data.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.
- [REF-004 · Spanner: Google's Globally-Distributed Database](../sources/REF-004-spanner-google-s-globally-distributed-database.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.
- [REF-040 · Pandapower—An Open-Source Python Tool for Convenient Modeling Analysis and Optimization](../sources/REF-040-pandapoweran-open-source-python-tool-for-convenient-modeling-analysis-an.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-041 · PyPSA: Python for Power System Analysis](../sources/REF-041-pypsa-python-for-power-system-analysis.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-042 · MATPOWER: Steady-State Operations Planning and Analysis Tools](../sources/REF-042-matpower-steady-state-operations-planning-and-analysis-tools.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-044 · PowerModelsDistribution.jl: an open-source framework for exploring distribution power flow formulations](../sources/REF-044-powermodelsdistribution-jl-an-open-source-framework-for-exploring-distri.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-066 · Otimização da manutenção centrada na confiabilidade em redes de distribuição de energia elétrica](../sources/REF-066-otimizacao-da-manutencao-centrada-na-confiabilidade-em-redes-de-distribu.md) — tesis_doctoral, PT; `identificado_en_fuente_web`.
- [REF-069 · Stabilité des réseaux électriques de distribution en présence de productions d’énergie renouvelable](../sources/REF-069-stabilite-des-reseaux-electriques-de-distribution-en-presence-de-product.md) — tesis_doctoral, FR; `identificado_en_fuente_web`.
- [REF-070 · Supervision énergetique des réseaux de distribution](../sources/REF-070-supervision-energetique-des-reseaux-de-distribution.md) — tesis_doctoral, FR; `identificado_en_fuente_web`.
- [REF-073 · Die Aufnahmefähigkeit von Niederspannungsverteilnetzen für Photovoltaik](../sources/REF-073-die-aufnahmefahigkeit-von-niederspannungsverteilnetzen-fur-photovoltaik.md) — tesis_doctoral, DE; `identificado_en_fuente_web`.
- [REF-087 · Otimização baseada em confiabilidade de planos de manutenção de sistemas de distribuição](../sources/REF-087-otimizacao-baseada-em-confiabilidade-de-planos-de-manutencao-de-sistemas.md) — tesis_maestria, PT; `identificado_en_fuente_web`.
- [REF-096 · D3: Data-Driven Documents](../sources/REF-096-d3-data-driven-documents.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-097 · Vega-Lite: A Grammar of Interactive Graphics](../sources/REF-097-vega-lite-a-grammar-of-interactive-graphics.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-098 · Usability Analysis of Visual Programming Environments: A Cognitive Dimensions Framework](../sources/REF-098-usability-analysis-of-visual-programming-environments-a-cognitive-dimens.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-131 · pandapower: Open Source Python Tool (2018) / bibliografía](../sources/REF-131-pandapower-open-source-python-tool-2018-bibliografia.md) — articulo_o_preprint, EN; `importado_pendiente_auditoria`.

## Documentación, guías o estándares útiles (no confundir con papers)
- [REF-019 · Demystifying evals for AI agents](../sources/REF-019-demystifying-evals-for-ai-agents.md) — guia_tecnica.

## Contrato, implementación y pruebas
- **Contrato funcional:** especificación en `specs/`, identificadores estables y validación de entrada / salida.
- **Propiedades no negociables:** Los tests de scaffold NO prueban precisión eléctrica ni legalidad; crear datasets de referencia.
- **Benchmark mínimo propuesto:** Criterios de aceptación cuantificados por estudio, error físico, seguridad y UX.
- **Evidencias:** registrar commit, snapshot de red, escenario, seed, versiones de librerías y motor, unidades, tolerancias, tablas y logs sanitizados.
- **Control de cambios:** PR bloqueada si se ocultan incertidumbres o se afirma que una ficha es texto completo cuando no lo es.

## Skills responsables
- `unitesis-testing-qa`
- `unitesis-evidence-audit`

## Palabras clave multilingües
Pruebas de aceptación científica y de agentes; modularity; reproducibility; industrial validation
