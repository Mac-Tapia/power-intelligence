# UNITESIS — Referencias científicas, regulatorias y técnicas actualizadas (21/10/2026)

**Origen:** plan maestro (40 specs, 400 tareas).  
**Criterio de actualización:** distinguir registros históricos, páginas editoriales verificadas en la consulta actual y documentos que requieren revisión adicional.  
**No es una revisión sistemática terminada:** los enlaces confirmados permiten localizar la fuente, pero no implican lectura completa ni aprobación regulatoria.

## 1. Inventario heredado
- **191 fichas Markdown heredadas** en `docs/scientific-evidence/sources/`.
- **21 fuentes prioritarias** comprobadas en páginas editoriales, institucionales o documentación oficial durante la actualización.
- Algunas de las fuentes prioritarias ya estaban representadas en el catálogo anterior; **no se suman como publicaciones únicas nuevas**.
- Esta edición conserva el estado de verificación original de las fichas heredadas y añade una lista curada; no cambia a “auditado” ningún documento que no se haya examinado íntegramente.

Estados del catálogo anterior:

| Etiqueta de estado | Cantidad |
|---|---:|
| `identificado_en_fuente_web` | 104 |
| `importado_pendiente_auditoria` | 85 |
| `metadatos_pendientes_confirmacion` | 2 |

## 2. Referencias verificadas recientemente — Prioritarias para implementar

| Código | Tipo y año | Referencia original | Módulo y aplicación | Estado/advertencia |
|---|---|---|---|---|
| N-01 | Norma regulatoria original · 2013 | [Norma: Tarifas y Compensaciones para SST y SCT, R. 217-2013-OS/CD](https://www.osinergmin.gob.pe/Resoluciones/pdf/2013/OSINERGMIN%20No.217-2013-OS-CD.pdf) — Osinergmin | PIT, evaluación técnico-económica | Texto original; verificar modificatorias y vigencia para cada periodo. |
| N-02 | Resolución de prepublicación · 2017 | [R.M. 428-2017-MEM/DM: autorización de prepublicación de metodología PIDE](https://busquedas.elperuano.pe/dispositivo/NL/1577466-1) — MINEM / El Peruano | PIDE y planificación de distribución | No equivale a aprobación de la metodología. |
| N-03 | Ficha oficial del proyecto (no norma final) · 2017 | [Proyecto de Norma: Criterios y Metodología de Planificación para PIDE](https://www.gob.pe/institucion/minem/informes-publicaciones/4721290-resolucion-ministerial-que-aprueba-la-norma-criterios-y-metodologia-de-planificacion-para-la-elaboracion-del-plan-de-inversion-en-distribucion-electrica-pide) — MINEM | PIDE, formatos 01-15 | La ficha oficial identifica el proyecto; anexo completo y norma final sin acreditar. |
| N-04 | Informe legal institucional · 2025 | [Informe Legal N.° 628-2025-GRT](https://www.osinergmin.gob.pe/Resoluciones/pdf/2025/Informe-Legal-628-2025-GRT.pdf) — Osinergmin | PIDE, estado normativo | Informa que la metodología PIDE estaba pendiente al 22/08/2025; no certifica situación posterior. |
| N-05 | Expediente técnico empresarial · 2024 | [Informe técnico de Electro Dunas — Peajes SST/SCT 2025-2029](https://www2.osinergmin.gob.pe/GRT/Fijacion-SST-SCT/peajes-comp-sistsec-comp-2025-2029/E/14%20Electro%20Dunas/Informe.pdf) — Electro Dunas / Osinergmin | PIT, CAPEX, sistemas SST/SCT | Caso real; condiciones regulatorias deben seleccionarse según periodo. |
| N-06 | Informe/observaciones de regulación · 2024 | [Observaciones de Osinergmin a propuesta Electro Dunas 2025–2029](https://www2.osinergmin.gob.pe/GRT/Fijacion-SST-SCT/peajes-comp-sistsec-comp-2025-2029/D/16.%20Electrodunas/Adjunto%20oficio%20Electrodunas.pdf) — Osinergmin | Evidencias regulatorias y trazabilidad | Observación sobre vínculos/trazabilidad de cálculos; emplear como criterio de prueba documental. |
| P-01 | Libro / guía de gestión · 2018 (edición combinada) | [A Guide to PMBOK, Sixth Edition + Agile Practice Guide (edición española)](https://www.pmi.org/shop/p-/book/a-guide-to-the-project-management-body-of-knowledge-%28pmbok-guide%29-%E2%80%94-sixth-edition-and-agile-practice-guide-%28spanish%29/00101604200) — Project Management Institute | PMBOK, gestión de proyectos | El registro de 2018 es del paquete editorial; PMBOK 6 fue publicado originalmente en 2017. |
| S-01 | Documentación técnica oficial · 2026 (documentación consultada) | [GitHub Spec Kit — Spec-Driven Development y convergencia](https://github.com/github/spec-kit/blob/main/docs/index.md) — GitHub | SDD, 40 specs, 400 tareas | Flujo vigente incluye convergencia; evitar fijar comandos no soportados por versión instalada. |
| S-02 | Documentación técnica oficial · 2026 (manual actualizado) | [git-worktree — Manual oficial](https://git-scm.com/docs/git-worktree.html) — Git SCM | Worktrees y ramas aisladas | Usar add/list/remove/repair seguros; nunca borrar cambios sin confirmación. |
| S-03 | Artículo de ingeniería · 2026 | [Demystifying evals for AI agents](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) — Anthropic | Agentes, evaluación y QA | Eval por estado final, pruebas deterministas, trazas y revisión humana. No es paper arbitrado. |
| S-04 | Especificación técnica · 2025–2026 (especificación consultada) | [Model Context Protocol — server primitives](https://modelcontextprotocol.io/specification/draft/server/index) — Model Context Protocol | MCP, recursos y herramientas | El enlace es draft; fijar versión estable concreta en implementación. |
| S-05 | Nota técnica de especificación · 2025 | [One Year of MCP: November 2025 Specification Release](https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/) — MCP maintainers | MCP y actualizaciones | Evaluar cambios de autorización y compatibilidad del SDK al actualizar. |
| E-01 | Artículo arbitrado · 2018 | [pandapower — An Open-Source Python Tool](https://doi.org/10.1109/TPWRS.2018.2829021) — IEEE Transactions on Power Systems | Motor AC, cortocircuito, integración Python | Probar límites en redes desequilibradas y verificar contra benchmarks. |
| E-02 | Artículo arbitrado · 2020 | [PowerModelsDistribution.jl: An Open-Source Framework](https://doi.org/10.1016/j.epsr.2020.106664) — Electric Power Systems Research | Flujos multifase, OPF, redes desequilibradas | Ideal como referencia para validar OpenDSS y formulaciones eléctricas. |
| E-03 | Artículo arbitrado · 2018 | [PyPSA: Python for Power System Analysis](https://doi.org/10.5334/jors.188) — Journal of Open Research Software | Generación, transmisión, expansión y renovables | Adecuar su ámbito a estudios; no asumir equivalencia con un solver trifásico desequilibrado. |
| E-04 | Benchmark técnico · Edición institucional histórica | [IEEE PES Distribution System Analysis Subcommittee — Radial Distribution Test Feeders](https://ewh.ieee.org/soc/pes/dsacom/testfeeders/testfeeders.pdf) — IEEE PES | IEEE 13/34/123 y pruebas de cálculo | Pruebas reproducibles sobre reguladores, fases y cargas desequilibradas. |
| G-01 | Artículo de conferencia arbitrado · 2018 | [Graph Networks as Learnable Physics Engines for Inference and Control](https://proceedings.mlr.press/v80/sanchez-gonzalez18a.html) — Google DeepMind / ICML / PMLR | Graph, GNN, modelos sustitutos | Aplicación a flujos eléctricos es hipótesis UNITESIS; requiere experimento propio. |
| I-01 | Artículo arbitrado · 2019 | [Physics-informed neural networks: A deep learning framework...](https://doi.org/10.1016/j.jcp.2018.10.045) — Journal of Computational Physics | PINN, SciML, entrenamiento físico | Una PINN no garantiza factibilidad física perfecta; usar residuales AC y solver final. |
| I-02 | Preprint / revisión · 2024 | [Multi-Agent Reinforcement Learning for Energy Networks: Computational Challenges, Progress and Open Problems](https://arxiv.org/abs/2404.15583) — Keren, Essayeh, Albrecht y Morstyn | MADRL, DER, BESS, agentes | Revisión de desafíos; no confirma rendimiento de una implementación específica. |
| D-01 | Norma técnica GIS · 2023 (documentación OGC) | [GeoPackage Encoding Standard 1.4.0](https://www.ogc.org/standards/geopackage/) — Open Geospatial Consortium | GIS, datos geoespaciales | Conservar CRS, geometría y formato interoperable. |
| D-02 | Manual técnico · 2026 (documentación consultada) | [libp2p — What is libp2p](https://libp2p.io/docs/) — libp2p | Red P2P y mensajería | Comunicación cifrada no equivale a autorización de comercio energético. |

## 3. Evidencia → implementación → pruebas

| Área / SPEC | Fuentes obligatorias de partida | Evidencia a producir antes de marcar `tasks.md` |
|---|---|---|
| Fundación full stack (`004`) | S-01, S-02, S-03, S-04 | Healthcheck real; contratos OpenAPI; Playwright; acceso controlado; CI reproducible |
| VNR-GIS / topología (`001`, `003`) | D-01, E-04 | Lectura GIS real con CRS; nodos huérfanos; fases; trazabilidad de origen; edición de unifilar |
| Solvers AC (`008`) | E-01, E-02, E-04 | Voltaje, ángulo, pérdidas y KCL en IEEE 13/34/123; diferencias documentadas |
| PIT y estudios económicos | N-01, N-05, N-06 | Matriz de artículos aplicables, costos, escenario y expediente trazable |
| PIDE y planificación MT/BT | N-02, N-03, N-04 | Estado “metodología prepublicada”; validación de métodos; no reclamar cumplimiento final |
| PMBOK 6 | P-01 | Acta, WBS/EDT, cronograma, costo, riesgos, calidad, cambios y cierre por proyecto |
| PINN + GNN | G-01, I-01, E-02 | Residuales físicos, métricas fuera de distribución y rechazo de soluciones no factibles |
| MADRL/LLM/MCP | I-02, S-03, S-04 | Entrenamiento aislado, permisos mínimos, trazas y evaluaciones de resultado |
| P2P y marketplace | D-02, E-02, N-04 | Autenticación peer; pruebas de replay; simulación AC; bloqueo de operación no autorizada |

## 4. Alertas sobre vigencia de normas

- **PIT/SST/SCT:** N-01 corresponde al texto original 217-2013-OS/CD; el sistema debe mantener sus modificaciones y el periodo regulatorio como variables explícitas. No llamar “consolidada 2026” a esta referencia.
- **PIDE:** N-02 y N-03 identifican la prepublicación de 2017. N-04 confirmó que se consideraba pendiente al 22/08/2025. No se verificó aquí una aprobación normativa posterior: exigir consulta normativa antes de expedientes oficiales.
- **PMBOK:** se usa deliberadamente la sexta edición por requerimiento del proyecto. La ficha del paquete español de PMI indica 2018; distinguir de la publicación original de PMBOK 6 (2017).

## 5. Reglas obligatorias para agentes de programación

1. Leer `AGENTS.md`, constitución y el `spec.md` del módulo.
2. Buscar 2–3 fuentes científicas pertinentes **y** la norma oficial cuando corresponda.
3. Crear o actualizar `specs/<feature>/research.md` con URL, metadatos, hallazgo, alcance, supuesto, riesgo y prueba.
4. Una ficha que diga `importado_pendiente_auditoria` no puede presentarse como evidencia validada.
5. Documentar fecha de consulta y pin de versión de framework/estándar; no interpretar “última versión” como perpetuamente vigente.
6. Actualizar `tasks.md` únicamente cuando exista evidencia de las pruebas realmente ejecutadas.
7. Los LLM, GNN y PINN no sustituyen al solver eléctrico ni al responsable ingeniero en aprobación final.

## 6. Catálogo heredado íntegro (191 fichas)

Cada línea conserva exactamente la referencia previa y su etiqueta de verificación; este apartado es **inventario**, no recertificación bibliográfica.

### ARCH — 35 fichas de dominio

- **REF-001** [MapReduce: Simplified Data Processing on Large Clusters](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/) — `articulo_conferencia` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-001-mapreduce-simplified-data-processing-on-large-clusters.md).
- **REF-002** [The Google File System](https://research.google/pubs/the-google-file-system/) — `articulo_conferencia` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-002-the-google-file-system.md).
- **REF-005** [Dremel: Interactive Analysis of Web-Scale Datasets](https://research.google/pubs/dremel-interactive-analysis-of-web-scale-datasets-2/) — `articulo_conferencia` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-005-dremel-interactive-analysis-of-web-scale-datasets.md).
- **REF-006** [Dremel: A Decade of Interactive SQL Analysis at Web Scale](https://research.google/pubs/dremel-a-decade-of-interactive-sql-analysis-at-web-scale/) — `articulo_conferencia` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-006-dremel-a-decade-of-interactive-sql-analysis-at-web-scale.md).
- **REF-089** [Microservices](https://www.martinfowler.com/articles/microservices.html) — `articulo_tecnico` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-089-microservices.md).
- **REF-090** [Monolith First](https://martinfowler.com/bliki/MonolithFirst.html) — `articulo_tecnico` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-090-monolith-first.md).
- **REF-091** [What do you mean by Event-Driven?](https://martinfowler.com/articles/201701-event-driven.html) — `articulo_tecnico` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-091-what-do-you-mean-by-event-driven.md).
- **REF-110** [Microservices Guide — Martin Fowler](https://www.martinfowler.com/microservices/) — `libro_o_guia_tecnica` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-110-microservices-guide-martin-fowler.md).
- **REF-113** [AWS Well-Architected: six pillars](https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html) — `libro_o_guia_tecnica` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-113-aws-well-architected-six-pillars.md).
- **REF-114** [AWS Well-Architected definitions](https://docs.aws.amazon.com/wellarchitected/latest/framework/definitions.html) — `libro_o_guia_tecnica` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-114-aws-well-architected-definitions.md).
- **REF-120** [Physics-informed neural networks for power systems: A systematic review (2026)](https://www.sciencedirect.com/science/article/abs/pii/S2352467726001438) — `articulo_o_preprint` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-120-physics-informed-neural-networks-for-power-systems-a-systematic-review-2.md).
- **REF-121** [Physics-Informed Neural Networks in Grid-Connected Inverters (2025)](https://doi.org/10.3390/en18205441) — `articulo_o_preprint` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-121-physics-informed-neural-networks-in-grid-connected-inverters-2025.md).
- **REF-122** [Survey on power flow calculation in distribution networks: data-physics fusion (2026)](https://www.sciencedirect.com/science/article/pii/S2352467726001402) — `articulo_o_preprint` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-122-survey-on-power-flow-calculation-in-distribution-networks-data-physics-f.md).
- **REF-123** [Physics-informed neural networks in the energy sector (2026)](https://www.sciencedirect.com/science/article/pii/S2352484725008893) — `articulo_o_preprint` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-123-physics-informed-neural-networks-in-the-energy-sector-2026.md).
- **REF-129** [Designing an optimal microgrid control system using DRL: review (2024)](https://doi.org/10.1016/j.jestch.2024.101651) — `articulo_o_preprint` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-129-designing-an-optimal-microgrid-control-system-using-drl-review-2024.md).
- **REF-133** [Robust protection in DER-rich grids using DRL (2020)](https://arxiv.org/abs/2003.02422) — `articulo_o_preprint` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-133-robust-protection-in-der-rich-grids-using-drl-2020.md).
- **REF-135** [Aprendizaje automático aplicado en redes eléctricas inteligentes — UC3M (2024)](https://e-archivo.uc3m.es/entities/publication/72e0f36a-16aa-44be-8fd0-1093693ccfe7) — `tesis_doctoral` · `ES` · `importado_pendiente_auditoria` · [Ficha](sources/REF-135-aprendizaje-automatico-aplicado-en-redes-electricas-inteligentes-uc3m-20.md).
- **REF-136** [Advanced design methods for active distribution networks — DTU](https://orbit.dtu.dk/files/257934164/PhD_thesis_Sergey_Klyapovskiy.pdf) — `tesis_doctoral` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-136-advanced-design-methods-for-active-distribution-networks-dtu.md).
- **REF-139** [Intelligence artificielle pour les systèmes d’énergie — Toulouse (2024)](https://utheme.utoulouse.fr/s/fr/item/6097) — `tesis_doctoral` · `FR` · `importado_pendiente_auditoria` · [Ficha](sources/REF-139-intelligence-artificielle-pour-les-systemes-denergie-toulouse-2024.md).
- **REF-140** [Application aux systèmes avec production renouvelable et batterie — theses.fr (2023)](https://theses.fr/2023EMAC0018) — `tesis_doctoral` · `FR` · `importado_pendiente_auditoria` · [Ficha](sources/REF-140-application-aux-systemes-avec-production-renouvelable-et-batterie-theses.md).
- **REF-141** [Réseau électrique intelligent pour les nouveaux usages — HAL (2019)](https://theses.hal.science/tel-02460664) — `tesis_doctoral` · `FR` · `importado_pendiente_auditoria` · [Ficha](sources/REF-141-reseau-electrique-intelligent-pour-les-nouveaux-usages-hal-2019.md).
- **REF-144** [Identificação de topologia de sistemas de distribuição — USP (2024)](https://teses.usp.br/teses/disponiveis/18/18154/tde-16092024-152321/) — `tesis_doctoral` · `PT` · `importado_pendiente_auditoria` · [Ficha](sources/REF-144-identificacao-de-topologia-de-sistemas-de-distribuicao-usp-2024.md).
- **REF-145** [Uso de técnicas de otimização baseadas em derivadas — UFRN](https://repositorio.ufrn.br/items/111bf3be-eebc-408d-9ec6-301b2dde1e8d) — `tesis_doctoral` · `PT` · `importado_pendiente_auditoria` · [Ficha](sources/REF-145-uso-de-tecnicas-de-otimizacao-baseadas-em-derivadas-ufrn.md).
- **REF-148** [Modelling and Control of Active Distribution Networks — U Liège](https://orbi.uliege.be/bitstream/2268/328123/1/thesis.pdf) — `tesis_doctoral` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-148-modelling-and-control-of-active-distribution-networks-u-liege.md).
- **REF-151** [Optimización lineal y no lineal de redes eléctricas — UNCP Perú](https://repositorio.uncp.edu.pe/handle/20.500.12894/3598) — `tesis` · `ES` · `importado_pendiente_auditoria` · [Ficha](sources/REF-151-optimizacion-lineal-y-no-lineal-de-redes-electricas-uncp-peru.md).
- **REF-153** [Power System Analysis and Design, 7th ed. (2022)](https://www.powerworld.com/gloveroverbyesarma) — `libro` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-153-power-system-analysis-and-design-7th-ed-2022.md).
- **REF-154** [Power Generation, Operation and Control, 3rd ed. (2013)](https://www.wiley-vch.de/en/areas-interest/engineering/power-generation-operation-and-control-978-0-471-79055-6) — `libro` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-154-power-generation-operation-and-control-3rd-ed-2013.md).
- **REF-158** [PyPSA](https://pypsa.org/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-158-pypsa.md).
- **REF-164** [Open Energy Modelling Framework / oemof](https://oemof.org/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-164-open-energy-modelling-framework-oemof.md).
- **REF-177** [FastAPI](https://fastapi.tiangolo.com/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-177-fastapi.md).
- **REF-181** [OpenAPI specification](https://spec.openapis.org/oas/latest.html) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-181-openapi-specification.md).
- **REF-185** [IEC Common Information Model introduction](https://www.iec.ch/) — `norma_o_estandar` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-185-iec-common-information-model-introduction.md).
- **REF-189** [ISO 25010 quality model (ISO catalog)](https://www.iso.org/) — `norma_o_estandar` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-189-iso-25010-quality-model-iso-catalog.md).
- **REF-190** [OSINERGMIN portal](https://www.gob.pe/osinergmin) — `norma_o_estandar` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-190-osinergmin-portal.md).
- **REF-191** [MINEM portal](https://www.gob.pe/minem) — `norma_o_estandar` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-191-minem-portal.md).

### BK — 3 fichas de dominio

- **REF-003** [Bigtable: A Distributed Storage System for Structured Data](https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/) — `articulo_conferencia` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-003-bigtable-a-distributed-storage-system-for-structured-data.md).
- **REF-004** [Spanner: Google's Globally-Distributed Database](https://research.google/pubs/spanner-googles-globally-distributed-database-2/) — `articulo_conferencia` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-004-spanner-google-s-globally-distributed-database.md).
- **REF-092** [Event Sourcing](https://www.martinfowler.com/eaaDev/EventSourcing.html) — `articulo_tecnico` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-092-event-sourcing.md).

### FE — 5 fichas de dominio

- **REF-096** [D3: Data-Driven Documents](https://doi.org/10.1109/TVCG.2011.185) — `articulo_revista` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-096-d3-data-driven-documents.md).
- **REF-097** [Vega-Lite: A Grammar of Interactive Graphics](https://doi.org/10.1109/TVCG.2016.2599030) — `articulo_revista` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-097-vega-lite-a-grammar-of-interactive-graphics.md).
- **REF-098** [Usability Analysis of Visual Programming Environments: A Cognitive Dimensions Framework](https://doi.org/10.1006/jvlc.1996.0009) — `articulo_revista` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-098-usability-analysis-of-visual-programming-environments-a-cognitive-dimens.md).
- **REF-175** [MapLibre GL JS](https://maplibre.org/maplibre-gl-js/docs/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-175-maplibre-gl-js.md).
- **REF-176** [React Flow](https://reactflow.dev/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-176-react-flow.md).

### GIS — 5 fichas de dominio

- **REF-099** [OpenStreetMap: User-Generated Street Maps](https://doi.org/10.1109/MPRV.2008.80) — `articulo_revista` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-099-openstreetmap-user-generated-street-maps.md).
- **REF-100** [Citizens as sensors: the world of volunteered geography](https://doi.org/10.1007/s10708-007-9111-y) — `articulo_revista` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-100-citizens-as-sensors-the-world-of-volunteered-geography.md).
- **REF-116** [ENTSO-E CGMES Library (2026)](https://www.entsoe.eu/data/cim/cim-for-grid-models-exchange/) — `norma_o_estandar` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-116-entso-e-cgmes-library-2026.md).
- **REF-173** [GeoPandas](https://geopandas.org/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-173-geopandas.md).
- **REF-174** [PostGIS](https://postgis.net/documentation/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-174-postgis.md).

### GRAPH — 11 fichas de dominio

- **REF-011** [Graph Networks as Learnable Physics Engines for Inference and Control](https://proceedings.mlr.press/v80/sanchez-gonzalez18a.html) — `articulo_conferencia` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-011-graph-networks-as-learnable-physics-engines-for-inference-and-control.md).
- **REF-031** [Graph Attention Networks](https://arxiv.org/abs/1710.10903) — `preprint` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-031-graph-attention-networks.md).
- **REF-032** [Semi-Supervised Classification with Graph Convolutional Networks](https://arxiv.org/abs/1609.02907) — `preprint` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-032-semi-supervised-classification-with-graph-convolutional-networks.md).
- **REF-033** [Neural Relational Inference for Interacting Systems](https://proceedings.mlr.press/v80/kipf18a.html) — `articulo_conferencia` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-033-neural-relational-inference-for-interacting-systems.md).
- **REF-034** [Graph inductive biases in Transformers without Message Passing](https://proceedings.mlr.press/v202/ma23c.html) — `articulo_conferencia` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-034-graph-inductive-biases-in-transformers-without-message-passing.md).
- **REF-037** [Graph Neural Networks and Their Applications in Power Systems: A Review](https://ieeexplore.ieee.org/document/11103635/) — `articulo_conferencia` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-037-graph-neural-networks-and-their-applications-in-power-systems-a-review.md).
- **REF-038** [Applications of Graph Computing and Graph Neural Networks in Power Systems: A Survey](https://ieeexplore.ieee.org/document/10754312/) — `articulo_conferencia` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-038-applications-of-graph-computing-and-graph-neural-networks-in-power-syste.md).
- **REF-079** [Spatio-Temporal GNNs for Power Grid State Estimation under Topological Changes](https://repository.tudelft.nl/record/uuid%3A2d8a6cb4-93ab-466d-b8ea-5a78d7501016) — `tesis_maestria` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-079-spatio-temporal-gnns-for-power-grid-state-estimation-under-topological-c.md).
- **REF-080** [Adaptive Equivalent Models for Distribution Networks](https://repository.tudelft.nl/record/uuid%3Abd8572f6-9410-49c6-85cb-c7461d004094) — `tesis_maestria` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-080-adaptive-equivalent-models-for-distribution-networks.md).
- **REF-127** [Graph Neural Networks and Their Applications in Power Systems (IEEE 2025)](https://doi.org/10.1109/eIT64391.2025.11103635) — `articulo_o_preprint` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-127-graph-neural-networks-and-their-applications-in-power-systems-ieee-2025.md).
- **REF-184** [NetworkX](https://networkx.org/documentation/stable/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-184-networkx.md).

### GRAPHRAG — 1 fichas de dominio

- **REF-039** [From Local to Global: A Graph RAG Approach to Query-Focused Summarization](https://www.microsoft.com/en-us/research/publication/from-local-to-global-a-graph-rag-approach-to-query-focused-summarization/) — `preprint` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-039-from-local-to-global-a-graph-rag-approach-to-query-focused-summarization.md).

### LEDGER — 4 fichas de dominio

- **REF-059** [Recent developments and challenges using blockchain techniques for peer-to-peer energy trading](https://doi.org/10.1016/j.rineng.2024.103666) — `articulo_revision` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-059-recent-developments-and-challenges-using-blockchain-techniques-for-peer-.md).
- **REF-060** [Electricity powered by blockchain: A review with a European perspective](https://orbilu.uni.lu/handle/10993/51926) — `articulo_revision` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-060-electricity-powered-by-blockchain-a-review-with-a-european-perspective.md).
- **REF-061** [Applications of blockchain technology in peer-to-peer energy markets and green hydrogen supply chains](https://www.nature.com/articles/s41598-024-72642-2) — `articulo_revision` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-061-applications-of-blockchain-technology-in-peer-to-peer-energy-markets-and.md).
- **REF-062** [A blockchain-based optimal peer-to-peer energy trading framework for decentralized energy management](https://doi.org/10.1016/j.apenergy.2024.123243) — `articulo_revista` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-062-a-blockchain-based-optimal-peer-to-peer-energy-trading-framework-for-dec.md).

### LLM — 5 fichas de dominio

- **REF-009** [Attention Is All You Need](https://research.google/pubs/attention-is-all-you-need/) — `articulo_conferencia` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-009-attention-is-all-you-need.md).
- **REF-016** [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) — `guia_tecnica` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-016-building-effective-agents.md).
- **REF-017** [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) — `guia_tecnica` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-017-how-we-built-our-multi-agent-research-system.md).
- **REF-018** [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — `guia_tecnica` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-018-effective-context-engineering-for-ai-agents.md).
- **REF-020** [Constitutional AI: Harmlessness from AI feedback](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback) — `preprint` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-020-constitutional-ai-harmlessness-from-ai-feedback.md).

### MARKET — 8 fichas de dominio

- **REF-054** [P2P electricity trading: A systematic review on current developments and perspectives](https://doi.org/10.1016/j.ref.2023.01.008) — `articulo_revision` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-054-p2p-electricity-trading-a-systematic-review-on-current-developments-and-.md).
- **REF-055** [Peer-to-peer energy trading in smart grid: Frameworks implementation methodologies and demonstration projects](https://www.sciencedirect.com/science/article/pii/S0378779622009580) — `articulo_revision` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-055-peer-to-peer-energy-trading-in-smart-grid-frameworks-implementation-meth.md).
- **REF-056** [P2P energy trading via public power networks: Practical challenges emerging solutions](https://link.springer.com/article/10.1007/s11708-023-0873-9) — `articulo_revista` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-056-p2p-energy-trading-via-public-power-networks-practical-challenges-emergi.md).
- **REF-057** [Peer-to-peer kilowatt and negawatt trading: A review](https://doi.org/10.1016/j.rser.2022.112908) — `articulo_revision` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-057-peer-to-peer-kilowatt-and-negawatt-trading-a-review.md).
- **REF-058** [A survey on peer-to-peer energy trading for local communities](https://doi.org/10.3389/fcomp.2022.1008504) — `articulo_revision` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-058-a-survey-on-peer-to-peer-energy-trading-for-local-communities.md).
- **REF-063** [P2P Energy Trading of EVs Using Blockchain Technology in Centralized and Decentralized Networks](https://doi.org/10.3390/en17092135) — `articulo_revision` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-063-p2p-energy-trading-of-evs-using-blockchain-technology-in-centralized-and.md).
- **REF-082** [Integration of electric vehicles in a flexible electricity demand side management framework](https://era.ed.ac.uk/items/dfcfda2a-8eb3-41df-9152-fd6214e554b3) — `tesis_doctoral` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-082-integration-of-electric-vehicles-in-a-flexible-electricity-demand-side-m.md).
- **REF-125** [Designing the future electricity spot market with high renewables (2025)](https://www.nature.com/articles/s44287-025-00163-9) — `articulo_o_preprint` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-125-designing-the-future-electricity-spot-market-with-high-renewables-2025.md).

### MARL — 15 fichas de dominio

- **REF-049** [Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments](https://arxiv.org/abs/1706.02275) — `preprint` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-049-multi-agent-actor-critic-for-mixed-cooperative-competitive-environments.md).
- **REF-050** [QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning](https://arxiv.org/abs/1803.11485) — `preprint` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-050-qmix-monotonic-value-function-factorisation-for-deep-multi-agent-reinfor.md).
- **REF-051** [Multi-Agent Reinforcement Learning: A Selective Overview of Theories and Algorithms](https://arxiv.org/abs/1911.10635) — `preprint` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-051-multi-agent-reinforcement-learning-a-selective-overview-of-theories-and-.md).
- **REF-052** [PPO: Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347) — `preprint` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-052-ppo-proximal-policy-optimization-algorithms.md).
- **REF-053** [Multi-Agent Reinforcement Learning for Energy Networks](https://arxiv.org/abs/2404.15583) — `preprint` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-053-multi-agent-reinforcement-learning-for-energy-networks.md).
- **REF-117** [Reinforcement Learning Meets the Power Grid, Jin (2025)](https://doi.org/10.1561/3100000043) — `articulo_o_preprint` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-117-reinforcement-learning-meets-the-power-grid-jin-2025.md).
- **REF-118** [Reinforcement Learning for Efficient Power Systems Planning (2024)](https://doi.org/10.3390/en17092167) — `articulo_o_preprint` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-118-reinforcement-learning-for-efficient-power-systems-planning-2024.md).
- **REF-119** [A Review of Smart Grid Evolution and Reinforcement Learning (2025)](https://doi.org/10.3390/en18071837) — `articulo_o_preprint` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-119-a-review-of-smart-grid-evolution-and-reinforcement-learning-2025.md).
- **REF-124** [Multi-agent reinforcement learning for resources allocation optimization: survey (2025)](https://link.springer.com/article/10.1007/s10462-025-11340-5) — `articulo_o_preprint` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-124-multi-agent-reinforcement-learning-for-resources-allocation-optimization.md).
- **REF-126** [Multi-agent BESS collaborative control, Applied Energy (2024)](https://doi.org/10.1016/j.apenergy.2024.123858) — `articulo_o_preprint` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-126-multi-agent-bess-collaborative-control-applied-energy-2024.md).
- **REF-128** [Reinforcement Learning for Optimizing Renewable Energy Utilization in Smart Grids (2026)](https://www.mdpi.com/2412-3811/11/7/240) — `articulo_o_preprint` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-128-reinforcement-learning-for-optimizing-renewable-energy-utilization-in-sm.md).
- **REF-130** [A Survey of Multi-Agent Systems for Smartgrids (2024)](https://doi.org/10.3390/en17153620) — `articulo_o_preprint` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-130-a-survey-of-multi-agent-systems-for-smartgrids-2024.md).
- **REF-138** [Reinforcement Learning for Adaptive Distribution Network — U Alberta](https://ualberta.scholaris.ca/items/d5c9d718-a6b9-498e-a182-cf4820b3f1fc) — `tesis` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-138-reinforcement-learning-for-adaptive-distribution-network-u-alberta.md).
- **REF-171** [Ray RLlib](https://docs.ray.io/en/latest/rllib/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-171-ray-rllib.md).
- **REF-172** [PettingZoo](https://pettingzoo.farama.org/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-172-pettingzoo.md).

### OP — 36 fichas de dominio

- **REF-013** [Discovering novel algorithms with AlphaTensor](https://deepmind.google/blog/discovering-novel-algorithms-with-alphatensor/) — `divulgacion_investigacion` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-013-discovering-novel-algorithms-with-alphatensor.md).
- **REF-014** [AlphaChip: reinforcement learning for chip placement](https://deepmind.google/blog/how-alphachip-transformed-computer-chip-design/) — `divulgacion_investigacion` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-014-alphachip-reinforcement-learning-for-chip-placement.md).
- **REF-015** [AlphaEvolve: an evolutionary coding agent](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) — `divulgacion_investigacion` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-015-alphaevolve-an-evolutionary-coding-agent.md).
- **REF-043** [PowerModels.jl: An Open-Source Framework for Exploring Power Flow Formulations](https://arxiv.org/abs/1711.01728) — `articulo_conferencia` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-043-powermodels-jl-an-open-source-framework-for-exploring-power-flow-formula.md).
- **REF-045** [Optimal distributed generation planning in active distribution networks considering integration of energy storage](https://arxiv.org/abs/1808.05712) — `preprint` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-045-optimal-distributed-generation-planning-in-active-distribution-networks-.md).
- **REF-046** [Optimal Generation and Transmission Expansion Planning Addressing Short-Term Constraints](https://arxiv.org/abs/1910.00446) — `preprint` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-046-optimal-generation-and-transmission-expansion-planning-addressing-short-.md).
- **REF-047** [Stochastic Multistage Co-optimization of Generation and Transmission Expansion Planning](https://arxiv.org/abs/1910.01640) — `preprint` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-047-stochastic-multistage-co-optimization-of-generation-and-transmission-exp.md).
- **REF-048** [Robust Dynamic Transmission and Renewable Generation Expansion Planning](https://arxiv.org/abs/1701.08649) — `preprint` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-048-robust-dynamic-transmission-and-renewable-generation-expansion-planning.md).
- **REF-064** [Análisis de la Planificación de Redes Eléctricas en España](https://oa.upm.es/90884/) — `tesis` · `ES` · `identificado_en_fuente_web` · [Ficha](sources/REF-064-analisis-de-la-planificacion-de-redes-electricas-en-espana.md).
- **REF-065** [Planejamento da expansão de sistemas de distribuição de energia elétrica considerando restauração](https://repositorio.unesp.br/items/620d6f0e-ad0b-405b-8809-78d5b0498dcc) — `tesis_doctoral` · `PT` · `identificado_en_fuente_web` · [Ficha](sources/REF-065-planejamento-da-expansao-de-sistemas-de-distribuicao-de-energia-eletrica.md).
- **REF-067** [Modelo para planejamento da expansão de sistemas de distribuição considerando confiabilidade](https://lume.ufrgs.br/handle/10183/230173) — `tesis` · `PT` · `identificado_en_fuente_web` · [Ficha](sources/REF-067-modelo-para-planejamento-da-expansao-de-sistemas-de-distribuicao-conside.md).
- **REF-068** [Intégration du stockage dans les méthodes de planification des réseaux BT](https://theses.hal.science/tel-01841465) — `tesis_doctoral` · `FR` · `identificado_en_fuente_web` · [Ficha](sources/REF-068-integration-du-stockage-dans-les-methodes-de-planification-des-reseaux-b.md).
- **REF-071** [Synthèse robuste de dispositifs de stockage pour l'optimisation de micro-réseaux](https://theses.fr/2020INPT0092) — `tesis_doctoral` · `FR` · `identificado_en_fuente_web` · [Ficha](sources/REF-071-synthese-robuste-de-dispositifs-de-stockage-pour-l-optimisation-de-micro.md).
- **REF-072** [Optimizing cross-linked infrastructure for future energy systems](https://www.ecpe.rwth-aachen.de/cms/ecpe/forschung/publikationen/~eknl/details/?file=861215) — `tesis_doctoral` · `DE` · `identificado_en_fuente_web` · [Ficha](sources/REF-072-optimizing-cross-linked-infrastructure-for-future-energy-systems.md).
- **REF-074** [Energy transition and sector coupling: the impact of renewable hydrogen](https://depositonce.tu-berlin.de/items/f9153dd8-300b-4233-9411-4bbb436475fc) — `tesis_doctoral` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-074-energy-transition-and-sector-coupling-the-impact-of-renewable-hydrogen.md).
- **REF-076** [Autonomous optimal Power Flow via Convex Solution - Sequential Linear Programming](https://repository.gatech.edu/items/92b47699-c568-42ad-a366-6f52642ad792) — `tesis_doctoral` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-076-autonomous-optimal-power-flow-via-convex-solution-sequential-linear-prog.md).
- **REF-077** [Computational Methods for Fast and Secure Distributed Optimal Power Flow](https://repository.gatech.edu/entities/publication/7e7b40c7-2d68-4add-a036-649f2efde3c2) — `tesis_doctoral` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-077-computational-methods-for-fast-and-secure-distributed-optimal-power-flow.md).
- **REF-083** [Optimising Qatar's energy transition through model-based analysis](https://doi.org/10.25560/83106) — `tesis_doctoral` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-083-optimising-qatar-s-energy-transition-through-model-based-analysis.md).
- **REF-084** [Ubicación óptima de generación distribuida en el sistema de distribución](https://dspace.ups.edu.ec/handle/123456789/13584) — `tesis` · `ES` · `identificado_en_fuente_web` · [Ficha](sources/REF-084-ubicacion-optima-de-generacion-distribuida-en-el-sistema-de-distribucion.md).
- **REF-085** [Planificación óptima de la generación distribuida en redes de distribución](https://dialnet.unirioja.es/servlet/tesis?codigo=205224) — `tesis_doctoral` · `ES` · `identificado_en_fuente_web` · [Ficha](sources/REF-085-planificacion-optima-de-la-generacion-distribuida-en-redes-de-distribuci.md).
- **REF-086** [Planeamiento de la generación distribuida en redes eléctricas](https://alicia.concytec.gob.pe/vufind/Record/UNAC_ee56489c7f1afbaffcba931035ff3f71) — `tesis_doctoral` · `ES` · `identificado_en_fuente_web` · [Ficha](sources/REF-086-planeamiento-de-la-generacion-distribuida-en-redes-electricas.md).
- **REF-088** [Reconfiguração otimizada de redes de distribuição de energia elétrica](https://repositorio.ufu.br/handle/123456789/20975) — `tesis` · `PT` · `identificado_en_fuente_web` · [Ficha](sources/REF-088-reconfiguracao-otimizada-de-redes-de-distribuicao-de-energia-eletrica.md).
- **REF-102** [Planejamento integrado de redes de distribuição de energia elétrica com fontes renováveis de geração distribuída na média e baixa tensão](https://repositorio.unesp.br/entities/publication/46c006ce-081f-4863-9cad-51b45655f600) — `tesis_doctoral` · `PT` · `identificado_en_fuente_web` · [Ficha](sources/REF-102-planejamento-integrado-de-redes-de-distribuicao-de-energia-eletrica-com-.md).
- **REF-103** [Planejamento de redes de distribuição de energia elétrica de média e baixa tensão](https://repositorio.unesp.br/entities/publication/0e96e2cd-7287-4fae-9e88-4f2f11639529/full) — `tesis_doctoral` · `PT` · `identificado_en_fuente_web` · [Ficha](sources/REF-103-planejamento-de-redes-de-distribuicao-de-energia-eletrica-de-media-e-bai.md).
- **REF-104** [Reconfiguração de redes de distribuição de energia elétrica através de um algoritmo de busca dispersa](https://repositorio.unesp.br/entities/publication/9c497ba8-4fbf-4435-b202-a6606722ef2c) — `tesis_maestria` · `PT` · `identificado_en_fuente_web` · [Ficha](sources/REF-104-reconfiguracao-de-redes-de-distribuicao-de-energia-eletrica-atraves-de-u.md).
- **REF-105** [Planejamento da expansão de sistemas de distribuição de energia elétrica considerando confiabilidade](https://repositorio.unesp.br/entities/publication/81bf30c8-9976-4ffa-a839-c06e42e72691) — `tesis_maestria` · `PT` · `identificado_en_fuente_web` · [Ficha](sources/REF-105-planejamento-da-expansao-de-sistemas-de-distribuicao-de-energia-eletrica.md).
- **REF-106** [Metodologia para reconfiguração de redes ativas de distribuição de energia elétrica através de uma matheuristica baseada em critérios de vizinhança](https://repositorio.unesp.br/entities/publication/4b2de0b8-96f1-4571-8fea-99da6a26236c/full) — `tesis_maestria` · `PT` · `identificado_en_fuente_web` · [Ficha](sources/REF-106-metodologia-para-reconfiguracao-de-redes-ativas-de-distribuicao-de-energ.md).
- **REF-132** [Deep RL-Based Distribution Network Planning (2025)](https://www.mdpi.com/1996-1073/18/5/1254) — `articulo_o_preprint` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-132-deep-rl-based-distribution-network-planning-2025.md).
- **REF-134** [Planning and operational resilience with DER and complex networks (2022)](https://arxiv.org/abs/2208.11543) — `articulo_o_preprint` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-134-planning-and-operational-resilience-with-der-and-complex-networks-2022.md).
- **REF-142** [Application of Optimization in Regional Distribution Network — HAL (2025)](https://theses.hal.science/tel-04977979v1/file/2025ESMA0001_karnib.pdf) — `tesis_doctoral` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-142-application-of-optimization-in-regional-distribution-network-hal-2025.md).
- **REF-143** [Planejamento de redes de distribuição de energia elétrica — UNESP](https://repositorio.unesp.br/entities/publication/0e96e2cd-7287-4fae-9e88-4f2f11639529) — `tesis_doctoral` · `PT` · `importado_pendiente_auditoria` · [Ficha](sources/REF-143-planejamento-de-redes-de-distribuicao-de-energia-eletrica-unesp.md).
- **REF-146** [Electricity Distribution Network Planning Considering DG — DiVA](https://www.diva-portal.org/smash/get/diva2%3A697178/fulltext01.pdf) — `tesis` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-146-electricity-distribution-network-planning-considering-dg-diva.md).
- **REF-149** [Microgrid Planning in Distribution Networks Through Optimal ... — Saskatchewan](https://harvest.usask.ca/bitstreams/bc8f8357-376c-4df7-9f8f-29924a803ff7/download) — `tesis` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-149-microgrid-planning-in-distribution-networks-through-optimal-saskatchewan.md).
- **REF-165** [Pyomo](https://www.pyomo.org/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-165-pyomo.md).
- **REF-166** [pymoo](https://pymoo.org/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-166-pymoo.md).
- **REF-167** [DEAP](https://deap.readthedocs.io/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-167-deap.md).

### OPS — 7 fichas de dominio

- **REF-007** [Dapper, a Large-Scale Distributed Systems Tracing Infrastructure](https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/) — `articulo_tecnico` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-007-dapper-a-large-scale-distributed-systems-tracing-infrastructure.md).
- **REF-008** [Borg, Omega, and Kubernetes](https://research.google/pubs/borg-omega-and-kubernetes/) — `articulo_tecnico` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-008-borg-omega-and-kubernetes.md).
- **REF-178** [Temporal](https://docs.temporal.io/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-178-temporal.md).
- **REF-179** [MLflow](https://mlflow.org/docs/latest/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-179-mlflow.md).
- **REF-180** [OpenTelemetry](https://opentelemetry.io/docs/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-180-opentelemetry.md).
- **REF-182** [Apache Arrow](https://arrow.apache.org/docs/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-182-apache-arrow.md).
- **REF-183** [Apache Parquet](https://parquet.apache.org/docs/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-183-apache-parquet.md).

### P2P — 1 fichas de dominio

- **REF-081** [Federated Learning-Based State Estimation for Integrated Transmission–Distribution Networks](https://repository.tudelft.nl/record/uuid%3A1df1dcc1-aa5f-431f-bc1e-b25ea765cb6f) — `tesis_maestria` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-081-federated-learning-based-state-estimation-for-integrated-transmissiondis.md).

### QA — 1 fichas de dominio

- **REF-019** [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — `guia_tecnica` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-019-demystifying-evals-for-ai-agents.md).

### SCIML — 20 fichas de dominio

- **REF-010** [GraphCast: Learned Global Weather Forecasting](https://deepmind.google/research/publications/22598/) — `articulo_conferencia` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-010-graphcast-learned-global-weather-forecasting.md).
- **REF-012** [GenCast: learning skillful ensemble forecasting of medium-range weather](https://deepmind.google/research/publications/gencast-learning-skillful-ensemble-forecasting-of-medium-range-weather/) — `preprint` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-012-gencast-learning-skillful-ensemble-forecasting-of-medium-range-weather.md).
- **REF-024** [Physics-informed neural networks: A deep learning framework for solving forward and inverse problems](https://doi.org/10.1016/j.jcp.2018.10.045) — `articulo_revista` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-024-physics-informed-neural-networks-a-deep-learning-framework-for-solving-f.md).
- **REF-025** [Physics-informed machine learning](https://www.nature.com/articles/s42254-021-00314-5) — `articulo_revision` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-025-physics-informed-machine-learning.md).
- **REF-026** [Neural Operator: Learning Maps Between Function Spaces](https://arxiv.org/abs/2108.08481) — `preprint` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-026-neural-operator-learning-maps-between-function-spaces.md).
- **REF-027** [Fourier Neural Operator for Parametric Partial Differential Equations](https://arxiv.org/abs/2010.08895) — `preprint` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-027-fourier-neural-operator-for-parametric-partial-differential-equations.md).
- **REF-028** [Learning nonlinear operators via DeepONet](https://www.nature.com/articles/s42256-021-00302-5) — `articulo_revista` · `EN` · `metadatos_pendientes_confirmacion` · [Ficha](sources/REF-028-learning-nonlinear-operators-via-deeponet.md).
- **REF-029** [Understanding and mitigating gradient pathologies in physics-informed neural networks](https://arxiv.org/abs/2001.04536) — `preprint` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-029-understanding-and-mitigating-gradient-pathologies-in-physics-informed-ne.md).
- **REF-030** [A survey on physics-informed neural networks: state of the art and future research](https://arxiv.org/abs/2211.08064) — `preprint` · `EN` · `metadatos_pendientes_confirmacion` · [Ficha](sources/REF-030-a-survey-on-physics-informed-neural-networks-state-of-the-art-and-future.md).
- **REF-035** [Physics-informed GNN for medium-high voltage AC power flow with edge-aware attention](https://arxiv.org/abs/2509.22458) — `preprint` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-035-physics-informed-gnn-for-medium-high-voltage-ac-power-flow-with-edge-awa.md).
- **REF-036** [PowerModelsGAT-AI: Physics-Informed Graph Attention for Multi-System Power Flow](https://arxiv.org/abs/2603.16879) — `preprint` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-036-powermodelsgat-ai-physics-informed-graph-attention-for-multi-system-powe.md).
- **REF-075** [Improving Power System Approximations Through Machine Learning-Inspired Optimization Methods](https://repository.gatech.edu/items/ce61b5eb-bd5b-4d05-920c-23bdc551cb07) — `tesis_doctoral` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-075-improving-power-system-approximations-through-machine-learning-inspired-.md).
- **REF-078** [Deep Statistical Solver for Distribution System State Estimation](https://repository.tudelft.nl/record/uuid%3A1bc2734e-0ecc-4841-8a19-638a475b0c35) — `tesis_maestria` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-078-deep-statistical-solver-for-distribution-system-state-estimation.md).
- **REF-101** [Learning on graphs from theory to industrial application in power management of distribution grids](https://publications.rwth-aachen.de/record/992117) — `tesis_doctoral` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-101-learning-on-graphs-from-theory-to-industrial-application-in-power-manage.md).
- **REF-137** [Application of Deep Learning Methods in Monitoring and Optimization of Electric Power Systems (2023)](https://arxiv.org/abs/2309.00498) — `tesis_doctoral` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-137-application-of-deep-learning-methods-in-monitoring-and-optimization-of-e.md).
- **REF-147** [Supervised learning for optimal investment planning in active networks — UPC](https://upcommons.upc.edu/entities/publication/892b5cda-a92d-4e8e-917b-d8716f23c73b) — `tesis` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-147-supervised-learning-for-optimal-investment-planning-in-active-networks-u.md).
- **REF-150** [Desarrollo de red neuronal para estimar demanda — UNAP Perú](https://repositorio.unapiquitos.edu.pe/items/53f085c4-9813-447a-998b-d80fa00d8fe4) — `tesis` · `ES` · `importado_pendiente_auditoria` · [Ficha](sources/REF-150-desarrollo-de-red-neuronal-para-estimar-demanda-unap-peru.md).
- **REF-168** [PyTorch](https://pytorch.org/docs/stable/index.html) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-168-pytorch.md).
- **REF-169** [DeepXDE](https://deepxde.readthedocs.io/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-169-deepxde.md).
- **REF-170** [JAX](https://docs.jax.dev/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-170-jax.md).

### SDD — 11 fichas de dominio

- **REF-023** [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) — `guia_tecnica` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-023-equipping-agents-for-the-real-world-with-agent-skills.md).
- **REF-093** [GitHub Spec Kit documentation](https://github.github.com/spec-kit/) — `documentacion` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-093-github-spec-kit-documentation.md).
- **REF-094** [GitHub Spec Kit quickstart](https://github.github.com/spec-kit/quickstart) — `documentacion` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-094-github-spec-kit-quickstart.md).
- **REF-107** [Fundamentals of Software Architecture, 2nd ed. (Richards & Ford, 2025)](https://www.oreilly.com/library/view/fundamentals-of-software/9781098175504/) — `libro_o_guia_tecnica` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-107-fundamentals-of-software-architecture-2nd-ed-richards-ford-2025.md).
- **REF-108** [Software Architecture: The Hard Parts (Ford et al., 2021)](https://www.oreilly.com/library/view/software-architecture-the/9781492086888/) — `libro_o_guia_tecnica` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-108-software-architecture-the-hard-parts-ford-et-al-2021.md).
- **REF-109** [Building Evolutionary Architectures, 2nd ed. (Ford et al., 2022)](https://www.oreilly.com/library/view/building-evolutionary-architectures/9781492097532/) — `libro_o_guia_tecnica` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-109-building-evolutionary-architectures-2nd-ed-ford-et-al-2022.md).
- **REF-111** [arc42 Method](https://arc42.org/method/) — `libro_o_guia_tecnica` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-111-arc42-method.md).
- **REF-112** [arc42 Quality Requirements](https://docs.arc42.org/section-10/) — `libro_o_guia_tecnica` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-112-arc42-quality-requirements.md).
- **REF-115** [arc42 twelve sections](https://examples.arc42.org/sections/) — `libro_o_guia_tecnica` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-115-arc42-twelve-sections.md).
- **REF-159** [PowerModels.jl](https://lanl-ansi.github.io/PowerModels.jl/stable/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-159-powermodels-jl.md).
- **REF-160** [PowerModelsDistribution.jl](https://lanl-ansi.github.io/PowerModelsDistribution.jl/stable/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-160-powermodelsdistribution-jl.md).

### SECURITY — 5 fichas de dominio

- **REF-021** [Mitigating the risk of prompt injections in browser use](https://www.anthropic.com/research/prompt-injection-defenses) — `guia_tecnica` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-021-mitigating-the-risk-of-prompt-injections-in-browser-use.md).
- **REF-022** [Trustworthy agents in practice](https://www.anthropic.com/research/trustworthy-agents) — `guia_tecnica` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-022-trustworthy-agents-in-practice.md).
- **REF-095** [Model Context Protocol authorization specification](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/basic/authorization.mdx) — `especificacion` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-095-model-context-protocol-authorization-specification.md).
- **REF-187** [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework) — `norma_o_estandar` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-187-nist-cybersecurity-framework-2-0.md).
- **REF-188** [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) — `norma_o_estandar` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-188-owasp-asvs.md).

### SOLVER — 18 fichas de dominio

- **REF-040** [Pandapower—An Open-Source Python Tool for Convenient Modeling Analysis and Optimization](https://ieeexplore.ieee.org/document/8344496) — `articulo_revista` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-040-pandapoweran-open-source-python-tool-for-convenient-modeling-analysis-an.md).
- **REF-041** [PyPSA: Python for Power System Analysis](https://doi.org/10.5334/jors.188) — `articulo_revista` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-041-pypsa-python-for-power-system-analysis.md).
- **REF-042** [MATPOWER: Steady-State Operations Planning and Analysis Tools](https://ieeexplore.ieee.org/document/5491276/) — `articulo_revista` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-042-matpower-steady-state-operations-planning-and-analysis-tools.md).
- **REF-044** [PowerModelsDistribution.jl: an open-source framework for exploring distribution power flow formulations](https://doi.org/10.1016/j.epsr.2020.106664) — `articulo_revista` · `EN` · `identificado_en_fuente_web` · [Ficha](sources/REF-044-powermodelsdistribution-jl-an-open-source-framework-for-exploring-distri.md).
- **REF-066** [Otimização da manutenção centrada na confiabilidade em redes de distribuição de energia elétrica](https://tedebc.ufma.br/jspui/handle/tede/6523) — `tesis_doctoral` · `PT` · `identificado_en_fuente_web` · [Ficha](sources/REF-066-otimizacao-da-manutencao-centrada-na-confiabilidade-em-redes-de-distribu.md).
- **REF-069** [Stabilité des réseaux électriques de distribution en présence de productions d’énergie renouvelable](https://theses.fr/2023GRALT066) — `tesis_doctoral` · `FR` · `identificado_en_fuente_web` · [Ficha](sources/REF-069-stabilite-des-reseaux-electriques-de-distribution-en-presence-de-product.md).
- **REF-070** [Supervision énergetique des réseaux de distribution](https://theses.fr/2021HESAE068) — `tesis_doctoral` · `FR` · `identificado_en_fuente_web` · [Ficha](sources/REF-070-supervision-energetique-des-reseaux-de-distribution.md).
- **REF-073** [Die Aufnahmefähigkeit von Niederspannungsverteilnetzen für Photovoltaik](https://mediatum.ub.tum.de/?id=998003) — `tesis_doctoral` · `DE` · `identificado_en_fuente_web` · [Ficha](sources/REF-073-die-aufnahmefahigkeit-von-niederspannungsverteilnetzen-fur-photovoltaik.md).
- **REF-087** [Otimização baseada em confiabilidade de planos de manutenção de sistemas de distribuição](https://repositorio.unicamp.br/acervo/detalhe/440731) — `tesis_maestria` · `PT` · `identificado_en_fuente_web` · [Ficha](sources/REF-087-otimizacao-baseada-em-confiabilidade-de-planos-de-manutencao-de-sistemas.md).
- **REF-131** [pandapower: Open Source Python Tool (2018) / bibliografía](https://www.pandapower.org/references/) — `articulo_o_preprint` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-131-pandapower-open-source-python-tool-2018-bibliografia.md).
- **REF-152** [Power System Stability and Control, 2nd ed. — Kundur & Malik (2022)](https://www.mheducation.com/highered/mhp/product/power-system-stability-control-second-edition.html) — `libro` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-152-power-system-stability-and-control-2nd-ed-kundur-malik-2022.md).
- **REF-155** [OpenDSS](https://opendss.epri.com/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-155-opendss.md).
- **REF-156** [DSS-Extensions](https://dss-extensions.org/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-156-dss-extensions.md).
- **REF-157** [pandapower](https://pandapower.readthedocs.io/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-157-pandapower.md).
- **REF-161** [GridCal](https://gridcal.readthedocs.io/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-161-gridcal.md).
- **REF-162** [GridLAB-D](https://www.gridlabd.org/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-162-gridlab-d.md).
- **REF-163** [MATPOWER](https://matpower.org/) — `documentacion` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-163-matpower.md).
- **REF-186** [IEEE PES Distribution Test Feeders](https://cmte.ieee.org/pes-testfeeders/) — `norma_o_estandar` · `EN` · `importado_pendiente_auditoria` · [Ficha](sources/REF-186-ieee-pes-distribution-test-feeders.md).

