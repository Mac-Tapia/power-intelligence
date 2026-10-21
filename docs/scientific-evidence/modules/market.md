# Mercado P2P y flexibilidad (simulado) — soporte científico y reglas implementables

**Área de código:** `power-market, market-clearing`.  
**Consulta:** `python scripts/research/query_evidence.py --module market --limit 12`.  
**Convención:** una ficha markdown describe una fuente o registro, **no contiene PDFs de terceros**.

## Tesis de arquitectura de este módulo
El clearing de ofertas no reemplaza factibilidad física ni permiso regulatorio.

## Qué está sustentado y qué es decisión UNITESIS
- **Evidencia externa:** las fichas enlazadas describen investigaciones, herramientas o normas existentes (calidad bibliográfica indicada individualmente).
- **Decisión de ingeniería UNITESIS:** adoptar interfaces y restricciones de aceptación diseñadas para este producto. No es conclusión causal de los artículos.
- **Vacío experimental:** no existe validación del módulo sobre VNR-GIS de distribuidoras dentro de esta biblioteca; hay que programar experimentos.

## Evidencia científica/tesis más directamente relacionada
- [REF-054 · P2P electricity trading: A systematic review on current developments and perspectives](../sources/REF-054-p2p-electricity-trading-a-systematic-review-on-current-developments-and-.md) — articulo_revision, EN; `identificado_en_fuente_web`.
- [REF-055 · Peer-to-peer energy trading in smart grid: Frameworks implementation methodologies and demonstration projects](../sources/REF-055-peer-to-peer-energy-trading-in-smart-grid-frameworks-implementation-meth.md) — articulo_revision, EN; `identificado_en_fuente_web`.
- [REF-056 · P2P energy trading via public power networks: Practical challenges emerging solutions](../sources/REF-056-p2p-energy-trading-via-public-power-networks-practical-challenges-emergi.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-057 · Peer-to-peer kilowatt and negawatt trading: A review](../sources/REF-057-peer-to-peer-kilowatt-and-negawatt-trading-a-review.md) — articulo_revision, EN; `identificado_en_fuente_web`.
- [REF-058 · A survey on peer-to-peer energy trading for local communities](../sources/REF-058-a-survey-on-peer-to-peer-energy-trading-for-local-communities.md) — articulo_revision, EN; `identificado_en_fuente_web`.
- [REF-063 · P2P Energy Trading of EVs Using Blockchain Technology in Centralized and Decentralized Networks](../sources/REF-063-p2p-energy-trading-of-evs-using-blockchain-technology-in-centralized-and.md) — articulo_revision, EN; `identificado_en_fuente_web`.
- [REF-082 · Integration of electric vehicles in a flexible electricity demand side management framework](../sources/REF-082-integration-of-electric-vehicles-in-a-flexible-electricity-demand-side-m.md) — tesis_doctoral, EN; `identificado_en_fuente_web`.
- [REF-125 · Designing the future electricity spot market with high renewables (2025)](../sources/REF-125-designing-the-future-electricity-spot-market-with-high-renewables-2025.md) — articulo_o_preprint, EN; `importado_pendiente_auditoria`.
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

## Documentación, guías o estándares útiles (no confundir con papers)
- Consultar fuentes institucionales oficiales a partir de las fichas científicas y agregar sus versiones al registro.

## Contrato, implementación y pruebas
- **Contrato funcional:** especificación en `specs/`, identificadores estables y validación de entrada / salida.
- **Propiedades no negociables:** El clearing de ofertas no reemplaza factibilidad física ni permiso regulatorio.
- **Benchmark mínimo propuesto:** Antes/después de trading con validación AC, pérdidas, cargos de red y cumplimiento de política.
- **Evidencias:** registrar commit, snapshot de red, escenario, seed, versiones de librerías y motor, unidades, tolerancias, tablas y logs sanitizados.
- **Control de cambios:** PR bloqueada si se ocultan incertidumbres o se afirma que una ficha es texto completo cuando no lo es.

## Skills responsables
- `unitesis-p2p-blockchain`
- `unitesis-power-simulation`

## Palabras clave multilingües
Mercado P2P y flexibilidad (simulado); modularity; reproducibility; industrial validation
