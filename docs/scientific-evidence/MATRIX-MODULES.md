# Matriz de trazabilidad bibliográfica por módulo y skill

Cada referencia está normalizada como ficha propia; una fuente puede apoyar varios módulos. El número de referencias **no mide madurez ni desempeño del producto**.

| Módulo | Nº referencias relacionadas | Fichas académicas (incluye preprints y tesis) | Trabajo exigido |
|---|---:|---:|---|
| [Arquitectura empresarial y plataforma](modules/arch.md) | 56 | 21 | Arquitectura C4 y ADR con contract tests y simulación de fallos de worker. |
| [Persistencia, linaje y series temporales](modules/bk.md) | 12 | 8 | Prueba de reproducibilidad de snapshot + ausencia de contaminación entre tenants. |
| [Frontend, experiencia GIS y unifilar](modules/fe.md) | 6 | 3 | Prueba E2E de selección de activo GIS→unifilar→detalle con snapshot consistente. |
| [GIS, adquisición y topología de redes](modules/gis.md) | 39 | 25 | Fixtures con nodos huérfanos, tramos invertidos, CRS incorrecto, bifásicos y switches abiertos. |
| [Grafo físico y GNN](modules/graph.md) | 37 | 30 | Cambiar configuración de interruptores y comprobar componentes, islas y tensión contra solver. |
| [Estudios eléctricos verificables](modules/solver.md) | 75 | 57 | Comparar IEEE 13/34/123 y otros casos disponibles, magnitudes, ángulos, pérdidas, KCL, convergencia. |
| [Expansión, optimización y planificación](modules/op.md) | 59 | 51 | Comparar óptimo/pareto vs baseline; reproducir factibilidad N-1, no anticipatividad y costos. |
| [PINN, GNN y simuladores sustitutos](modules/sciml.md) | 46 | 40 | Pruebas OOD por red/topología, error p.u., KCL, intervalos calibrados y rechazo de soluciones inviables. |
| [MADRL seguro y critic centralizado](modules/marl.md) | 15 | 13 | Curva de aprendizaje, generalización, tasa de violación física y recuperación tras fallos. |
| [LLM local, orquestación y permisos](modules/llm.md) | 6 | 3 | Evaluar fidelidad de citas, prompt injection, no-ejecución de cambios reales y costo/latencia. |
| [GraphRAG y conocimiento técnico](modules/graphrag.md) | 6 | 3 | Prueba de preguntas con documentos contradictorios, abrogados y fuentes sin acceso. |
| [P2P federación segura](modules/p2p.md) | 13 | 13 | Prueba de peer malicioso, replay, partición de red, aislamiento de empresa y sincronización. |
| [Blockchain permissioned y evidencia](modules/ledger.md) | 5 | 5 | Ensayos contra falsificación, duplicidad, reorg y costo; comparación contra log firmado sin cadena. |
| [Mercado P2P y flexibilidad (simulado)](modules/market.md) | 44 | 38 | Antes/después de trading con validación AC, pérdidas, cargos de red y cumplimiento de política. |
| [Seguridad, gobierno y control de agentes](modules/security.md) | 11 | 3 | Pentest focalizado: MCP prompt injection, SSRF, escalada de privilegios y fuga entre tenants. |
| [SDD, GitHub, skills y worktrees](modules/sdd.md) | 51 | 19 | CI falla si hay cambio de contrato sin spec o prueba de compatibilidad. |
| [MLOps, DevOps y observabilidad](modules/ops.md) | 47 | 19 | Recuperación de trabajos tras caída, reproducibilidad de métricas y control de costo CPU/GPU. |
| [Pruebas de aceptación científica y de agentes](modules/qa.md) | 45 | 15 | Criterios de aceptación cuantificados por estudio, error físico, seguridad y UX. |

## Skill -> módulo -> documentos

### `unitesis-api-contracts`

- Dominios: [arch](modules/arch.md), [bk](modules/bk.md), [security](modules/security.md), [sdd](modules/sdd.md).
- Fuentes prioritarias: [REF-001](sources/REF-001-mapreduce-simplified-data-processing-on-large-clusters.md), [REF-002](sources/REF-002-the-google-file-system.md), [REF-003](sources/REF-003-bigtable-a-distributed-storage-system-for-structured-data.md), [REF-004](sources/REF-004-spanner-google-s-globally-distributed-database.md), [REF-005](sources/REF-005-dremel-interactive-analysis-of-web-scale-datasets.md), [REF-006](sources/REF-006-dremel-a-decade-of-interactive-sql-analysis-at-web-scale.md).

### `unitesis-backend-fastapi`

- Dominios: [arch](modules/arch.md), [bk](modules/bk.md), [ops](modules/ops.md), [security](modules/security.md).
- Fuentes prioritarias: [REF-001](sources/REF-001-mapreduce-simplified-data-processing-on-large-clusters.md), [REF-002](sources/REF-002-the-google-file-system.md), [REF-003](sources/REF-003-bigtable-a-distributed-storage-system-for-structured-data.md), [REF-004](sources/REF-004-spanner-google-s-globally-distributed-database.md), [REF-005](sources/REF-005-dremel-interactive-analysis-of-web-scale-datasets.md), [REF-006](sources/REF-006-dremel-a-decade-of-interactive-sql-analysis-at-web-scale.md).

### `unitesis-db-postgis`

- Dominios: [bk](modules/bk.md), [gis](modules/gis.md), [arch](modules/arch.md).
- Fuentes prioritarias: [REF-003](sources/REF-003-bigtable-a-distributed-storage-system-for-structured-data.md), [REF-004](sources/REF-004-spanner-google-s-globally-distributed-database.md), [REF-059](sources/REF-059-recent-developments-and-challenges-using-blockchain-techniques-for-peer-.md), [REF-060](sources/REF-060-electricity-powered-by-blockchain-a-review-with-a-european-perspective.md), [REF-061](sources/REF-061-applications-of-blockchain-technology-in-peer-to-peer-energy-markets-and.md), [REF-062](sources/REF-062-a-blockchain-based-optimal-peer-to-peer-energy-trading-framework-for-dec.md).

### `unitesis-design-system`

- Dominios: [fe](modules/fe.md), [gis](modules/gis.md), [qa](modules/qa.md).
- Fuentes prioritarias: [REF-096](sources/REF-096-d3-data-driven-documents.md), [REF-097](sources/REF-097-vega-lite-a-grammar-of-interactive-graphics.md), [REF-098](sources/REF-098-usability-analysis-of-visual-programming-environments-a-cognitive-dimens.md), [REF-011](sources/REF-011-graph-networks-as-learnable-physics-engines-for-inference-and-control.md), [REF-031](sources/REF-031-graph-attention-networks.md), [REF-032](sources/REF-032-semi-supervised-classification-with-graph-convolutional-networks.md).

### `unitesis-devops-observability`

- Dominios: [ops](modules/ops.md), [arch](modules/arch.md), [security](modules/security.md).
- Fuentes prioritarias: [REF-001](sources/REF-001-mapreduce-simplified-data-processing-on-large-clusters.md), [REF-002](sources/REF-002-the-google-file-system.md), [REF-005](sources/REF-005-dremel-interactive-analysis-of-web-scale-datasets.md), [REF-006](sources/REF-006-dremel-a-decade-of-interactive-sql-analysis-at-web-scale.md), [REF-120](sources/REF-120-physics-informed-neural-networks-for-power-systems-a-systematic-review-2.md), [REF-121](sources/REF-121-physics-informed-neural-networks-in-grid-connected-inverters-2025.md).

### `unitesis-domain-ddd`

- Dominios: [arch](modules/arch.md), [bk](modules/bk.md), [sdd](modules/sdd.md).
- Fuentes prioritarias: [REF-001](sources/REF-001-mapreduce-simplified-data-processing-on-large-clusters.md), [REF-002](sources/REF-002-the-google-file-system.md), [REF-003](sources/REF-003-bigtable-a-distributed-storage-system-for-structured-data.md), [REF-004](sources/REF-004-spanner-google-s-globally-distributed-database.md), [REF-005](sources/REF-005-dremel-interactive-analysis-of-web-scale-datasets.md), [REF-006](sources/REF-006-dremel-a-decade-of-interactive-sql-analysis-at-web-scale.md).

### `unitesis-electric-graph`

- Dominios: [graph](modules/graph.md), [gis](modules/gis.md), [graphrag](modules/graphrag.md).
- Fuentes prioritarias: [REF-010](sources/REF-010-graphcast-learned-global-weather-forecasting.md), [REF-011](sources/REF-011-graph-networks-as-learnable-physics-engines-for-inference-and-control.md), [REF-012](sources/REF-012-gencast-learning-skillful-ensemble-forecasting-of-medium-range-weather.md), [REF-024](sources/REF-024-physics-informed-neural-networks-a-deep-learning-framework-for-solving-f.md), [REF-025](sources/REF-025-physics-informed-machine-learning.md), [REF-026](sources/REF-026-neural-operator-learning-maps-between-function-spaces.md).

### `unitesis-evidence-audit`

- Dominios: [bk](modules/bk.md), [ledger](modules/ledger.md), [ops](modules/ops.md), [qa](modules/qa.md).
- Fuentes prioritarias: [REF-003](sources/REF-003-bigtable-a-distributed-storage-system-for-structured-data.md), [REF-004](sources/REF-004-spanner-google-s-globally-distributed-database.md), [REF-059](sources/REF-059-recent-developments-and-challenges-using-blockchain-techniques-for-peer-.md), [REF-060](sources/REF-060-electricity-powered-by-blockchain-a-review-with-a-european-perspective.md), [REF-061](sources/REF-061-applications-of-blockchain-technology-in-peer-to-peer-energy-markets-and.md), [REF-062](sources/REF-062-a-blockchain-based-optimal-peer-to-peer-energy-trading-framework-for-dec.md).

### `unitesis-frontend-react`

- Dominios: [fe](modules/fe.md), [gis](modules/gis.md), [graph](modules/graph.md).
- Fuentes prioritarias: [REF-096](sources/REF-096-d3-data-driven-documents.md), [REF-097](sources/REF-097-vega-lite-a-grammar-of-interactive-graphics.md), [REF-098](sources/REF-098-usability-analysis-of-visual-programming-environments-a-cognitive-dimens.md), [REF-011](sources/REF-011-graph-networks-as-learnable-physics-engines-for-inference-and-control.md), [REF-031](sources/REF-031-graph-attention-networks.md), [REF-032](sources/REF-032-semi-supervised-classification-with-graph-convolutional-networks.md).

### `unitesis-gis-ingestion`

- Dominios: [gis](modules/gis.md), [graph](modules/graph.md), [bk](modules/bk.md).
- Fuentes prioritarias: [REF-011](sources/REF-011-graph-networks-as-learnable-physics-engines-for-inference-and-control.md), [REF-031](sources/REF-031-graph-attention-networks.md), [REF-032](sources/REF-032-semi-supervised-classification-with-graph-convolutional-networks.md), [REF-033](sources/REF-033-neural-relational-inference-for-interacting-systems.md), [REF-034](sources/REF-034-graph-inductive-biases-in-transformers-without-message-passing.md), [REF-037](sources/REF-037-graph-neural-networks-and-their-applications-in-power-systems-a-review.md).

### `unitesis-git-worktree`

- Dominios: [sdd](modules/sdd.md), [arch](modules/arch.md).
- Fuentes prioritarias: [REF-001](sources/REF-001-mapreduce-simplified-data-processing-on-large-clusters.md), [REF-002](sources/REF-002-the-google-file-system.md), [REF-005](sources/REF-005-dremel-interactive-analysis-of-web-scale-datasets.md), [REF-006](sources/REF-006-dremel-a-decade-of-interactive-sql-analysis-at-web-scale.md), [REF-120](sources/REF-120-physics-informed-neural-networks-for-power-systems-a-systematic-review-2.md), [REF-121](sources/REF-121-physics-informed-neural-networks-in-grid-connected-inverters-2025.md).

### `unitesis-marl-llm`

- Dominios: [marl](modules/marl.md), [llm](modules/llm.md), [sciml](modules/sciml.md).
- Fuentes prioritarias: [REF-049](sources/REF-049-multi-agent-actor-critic-for-mixed-cooperative-competitive-environments.md), [REF-050](sources/REF-050-qmix-monotonic-value-function-factorisation-for-deep-multi-agent-reinfor.md), [REF-051](sources/REF-051-multi-agent-reinforcement-learning-a-selective-overview-of-theories-and-.md), [REF-052](sources/REF-052-ppo-proximal-policy-optimization-algorithms.md), [REF-053](sources/REF-053-multi-agent-reinforcement-learning-for-energy-networks.md), [REF-117](sources/REF-117-reinforcement-learning-meets-the-power-grid-jin-2025.md).

### `unitesis-mcp-connectors`

- Dominios: [security](modules/security.md), [sdd](modules/sdd.md), [llm](modules/llm.md).
- Fuentes prioritarias: [REF-009](sources/REF-009-attention-is-all-you-need.md), [REF-020](sources/REF-020-constitutional-ai-harmlessness-from-ai-feedback.md), [REF-081](sources/REF-081-federated-learning-based-state-estimation-for-integrated-transmissiondis.md), [REF-001](sources/REF-001-mapreduce-simplified-data-processing-on-large-clusters.md), [REF-002](sources/REF-002-the-google-file-system.md), [REF-005](sources/REF-005-dremel-interactive-analysis-of-web-scale-datasets.md).

### `unitesis-p2p-blockchain`

- Dominios: [p2p](modules/p2p.md), [ledger](modules/ledger.md), [market](modules/market.md), [security](modules/security.md).
- Fuentes prioritarias: [REF-054](sources/REF-054-p2p-electricity-trading-a-systematic-review-on-current-developments-and-.md), [REF-055](sources/REF-055-peer-to-peer-energy-trading-in-smart-grid-frameworks-implementation-meth.md), [REF-056](sources/REF-056-p2p-energy-trading-via-public-power-networks-practical-challenges-emergi.md), [REF-057](sources/REF-057-peer-to-peer-kilowatt-and-negawatt-trading-a-review.md), [REF-058](sources/REF-058-a-survey-on-peer-to-peer-energy-trading-for-local-communities.md), [REF-059](sources/REF-059-recent-developments-and-challenges-using-blockchain-techniques-for-peer-.md).

### `unitesis-power-simulation`

- Dominios: [solver](modules/solver.md), [sciml](modules/sciml.md), [op](modules/op.md).
- Fuentes prioritarias: [REF-010](sources/REF-010-graphcast-learned-global-weather-forecasting.md), [REF-012](sources/REF-012-gencast-learning-skillful-ensemble-forecasting-of-medium-range-weather.md), [REF-024](sources/REF-024-physics-informed-neural-networks-a-deep-learning-framework-for-solving-f.md), [REF-025](sources/REF-025-physics-informed-machine-learning.md), [REF-026](sources/REF-026-neural-operator-learning-maps-between-function-spaces.md), [REF-027](sources/REF-027-fourier-neural-operator-for-parametric-partial-differential-equations.md).

### `unitesis-sciml-pinn-gnn`

- Dominios: [sciml](modules/sciml.md), [graph](modules/graph.md), [solver](modules/solver.md).
- Fuentes prioritarias: [REF-010](sources/REF-010-graphcast-learned-global-weather-forecasting.md), [REF-011](sources/REF-011-graph-networks-as-learnable-physics-engines-for-inference-and-control.md), [REF-012](sources/REF-012-gencast-learning-skillful-ensemble-forecasting-of-medium-range-weather.md), [REF-024](sources/REF-024-physics-informed-neural-networks-a-deep-learning-framework-for-solving-f.md), [REF-025](sources/REF-025-physics-informed-machine-learning.md), [REF-026](sources/REF-026-neural-operator-learning-maps-between-function-spaces.md).

### `unitesis-security-threat-model`

- Dominios: [security](modules/security.md), [p2p](modules/p2p.md), [ledger](modules/ledger.md).
- Fuentes prioritarias: [REF-009](sources/REF-009-attention-is-all-you-need.md), [REF-020](sources/REF-020-constitutional-ai-harmlessness-from-ai-feedback.md), [REF-081](sources/REF-081-federated-learning-based-state-estimation-for-integrated-transmissiondis.md), [REF-054](sources/REF-054-p2p-electricity-trading-a-systematic-review-on-current-developments-and-.md), [REF-055](sources/REF-055-peer-to-peer-energy-trading-in-smart-grid-frameworks-implementation-meth.md), [REF-056](sources/REF-056-p2p-energy-trading-via-public-power-networks-practical-challenges-emergi.md).

### `unitesis-spec-driven`

- Dominios: [sdd](modules/sdd.md), [arch](modules/arch.md), [qa](modules/qa.md).
- Fuentes prioritarias: [REF-001](sources/REF-001-mapreduce-simplified-data-processing-on-large-clusters.md), [REF-002](sources/REF-002-the-google-file-system.md), [REF-005](sources/REF-005-dremel-interactive-analysis-of-web-scale-datasets.md), [REF-006](sources/REF-006-dremel-a-decade-of-interactive-sql-analysis-at-web-scale.md), [REF-120](sources/REF-120-physics-informed-neural-networks-for-power-systems-a-systematic-review-2.md), [REF-121](sources/REF-121-physics-informed-neural-networks-in-grid-connected-inverters-2025.md).

### `unitesis-technical-research`

- Dominios: [qa](modules/qa.md), [graphrag](modules/graphrag.md), [sdd](modules/sdd.md).
- Fuentes prioritarias: [REF-003](sources/REF-003-bigtable-a-distributed-storage-system-for-structured-data.md), [REF-004](sources/REF-004-spanner-google-s-globally-distributed-database.md), [REF-040](sources/REF-040-pandapoweran-open-source-python-tool-for-convenient-modeling-analysis-an.md), [REF-041](sources/REF-041-pypsa-python-for-power-system-analysis.md), [REF-042](sources/REF-042-matpower-steady-state-operations-planning-and-analysis-tools.md), [REF-044](sources/REF-044-powermodelsdistribution-jl-an-open-source-framework-for-exploring-distri.md).

### `unitesis-testing-qa`

- Dominios: [qa](modules/qa.md), [solver](modules/solver.md), [fe](modules/fe.md), [ops](modules/ops.md).
- Fuentes prioritarias: [REF-003](sources/REF-003-bigtable-a-distributed-storage-system-for-structured-data.md), [REF-004](sources/REF-004-spanner-google-s-globally-distributed-database.md), [REF-040](sources/REF-040-pandapoweran-open-source-python-tool-for-convenient-modeling-analysis-an.md), [REF-041](sources/REF-041-pypsa-python-for-power-system-analysis.md), [REF-042](sources/REF-042-matpower-steady-state-operations-planning-and-analysis-tools.md), [REF-044](sources/REF-044-powermodelsdistribution-jl-an-open-source-framework-for-exploring-distri.md).

