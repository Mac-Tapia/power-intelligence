# MLOps, DevOps y observabilidad — soporte científico y reglas implementables

**Área de código:** `workers, MLflow, traces, deploy`.  
**Consulta:** `python scripts/research/query_evidence.py --module ops --limit 12`.  
**Convención:** una ficha markdown describe una fuente o registro, **no contiene PDFs de terceros**.

## Tesis de arquitectura de este módulo
Registrar experimentos, seeds, DVC/manifests, semántica de jobs y trazas extremo a extremo.

## Qué está sustentado y qué es decisión UNITESIS
- **Evidencia externa:** las fichas enlazadas describen investigaciones, herramientas o normas existentes (calidad bibliográfica indicada individualmente).
- **Decisión de ingeniería UNITESIS:** adoptar interfaces y restricciones de aceptación diseñadas para este producto. No es conclusión causal de los artículos.
- **Vacío experimental:** no existe validación del módulo sobre VNR-GIS de distribuidoras dentro de esta biblioteca; hay que programar experimentos.

## Evidencia científica/tesis más directamente relacionada
- [REF-001 · MapReduce: Simplified Data Processing on Large Clusters](../sources/REF-001-mapreduce-simplified-data-processing-on-large-clusters.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.
- [REF-002 · The Google File System](../sources/REF-002-the-google-file-system.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.
- [REF-005 · Dremel: Interactive Analysis of Web-Scale Datasets](../sources/REF-005-dremel-interactive-analysis-of-web-scale-datasets.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.
- [REF-006 · Dremel: A Decade of Interactive SQL Analysis at Web Scale](../sources/REF-006-dremel-a-decade-of-interactive-sql-analysis-at-web-scale.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.
- [REF-120 · Physics-informed neural networks for power systems: A systematic review (2026)](../sources/REF-120-physics-informed-neural-networks-for-power-systems-a-systematic-review-2.md) — articulo_o_preprint, EN; `importado_pendiente_auditoria`.
- [REF-121 · Physics-Informed Neural Networks in Grid-Connected Inverters (2025)](../sources/REF-121-physics-informed-neural-networks-in-grid-connected-inverters-2025.md) — articulo_o_preprint, EN; `importado_pendiente_auditoria`.
- [REF-122 · Survey on power flow calculation in distribution networks: data-physics fusion (2026)](../sources/REF-122-survey-on-power-flow-calculation-in-distribution-networks-data-physics-f.md) — articulo_o_preprint, EN; `importado_pendiente_auditoria`.
- [REF-123 · Physics-informed neural networks in the energy sector (2026)](../sources/REF-123-physics-informed-neural-networks-in-the-energy-sector-2026.md) — articulo_o_preprint, EN; `importado_pendiente_auditoria`.
- [REF-129 · Designing an optimal microgrid control system using DRL: review (2024)](../sources/REF-129-designing-an-optimal-microgrid-control-system-using-drl-review-2024.md) — articulo_o_preprint, EN; `importado_pendiente_auditoria`.
- [REF-133 · Robust protection in DER-rich grids using DRL (2020)](../sources/REF-133-robust-protection-in-der-rich-grids-using-drl-2020.md) — articulo_o_preprint, EN; `importado_pendiente_auditoria`.
- [REF-135 · Aprendizaje automático aplicado en redes eléctricas inteligentes — UC3M (2024)](../sources/REF-135-aprendizaje-automatico-aplicado-en-redes-electricas-inteligentes-uc3m-20.md) — tesis_doctoral, ES; `importado_pendiente_auditoria`.
- [REF-136 · Advanced design methods for active distribution networks — DTU](../sources/REF-136-advanced-design-methods-for-active-distribution-networks-dtu.md) — tesis_doctoral, EN; `importado_pendiente_auditoria`.
- [REF-139 · Intelligence artificielle pour les systèmes d’énergie — Toulouse (2024)](../sources/REF-139-intelligence-artificielle-pour-les-systemes-denergie-toulouse-2024.md) — tesis_doctoral, FR; `importado_pendiente_auditoria`.
- [REF-140 · Application aux systèmes avec production renouvelable et batterie — theses.fr (2023)](../sources/REF-140-application-aux-systemes-avec-production-renouvelable-et-batterie-theses.md) — tesis_doctoral, FR; `importado_pendiente_auditoria`.
- [REF-141 · Réseau électrique intelligent pour les nouveaux usages — HAL (2019)](../sources/REF-141-reseau-electrique-intelligent-pour-les-nouveaux-usages-hal-2019.md) — tesis_doctoral, FR; `importado_pendiente_auditoria`.
- [REF-144 · Identificação de topologia de sistemas de distribuição — USP (2024)](../sources/REF-144-identificacao-de-topologia-de-sistemas-de-distribuicao-usp-2024.md) — tesis_doctoral, PT; `importado_pendiente_auditoria`.
- [REF-145 · Uso de técnicas de otimização baseadas em derivadas — UFRN](../sources/REF-145-uso-de-tecnicas-de-otimizacao-baseadas-em-derivadas-ufrn.md) — tesis_doctoral, PT; `importado_pendiente_auditoria`.
- [REF-148 · Modelling and Control of Active Distribution Networks — U Liège](../sources/REF-148-modelling-and-control-of-active-distribution-networks-u-liege.md) — tesis_doctoral, EN; `importado_pendiente_auditoria`.
- [REF-151 · Optimización lineal y no lineal de redes eléctricas — UNCP Perú](../sources/REF-151-optimizacion-lineal-y-no-lineal-de-redes-electricas-uncp-peru.md) — tesis, ES; `importado_pendiente_auditoria`.

## Documentación, guías o estándares útiles (no confundir con papers)
- [REF-007 · Dapper, a Large-Scale Distributed Systems Tracing Infrastructure](../sources/REF-007-dapper-a-large-scale-distributed-systems-tracing-infrastructure.md) — articulo_tecnico.
- [REF-008 · Borg, Omega, and Kubernetes](../sources/REF-008-borg-omega-and-kubernetes.md) — articulo_tecnico.
- [REF-178 · Temporal](../sources/REF-178-temporal.md) — documentacion.
- [REF-179 · MLflow](../sources/REF-179-mlflow.md) — documentacion.
- [REF-180 · OpenTelemetry](../sources/REF-180-opentelemetry.md) — documentacion.
- [REF-182 · Apache Arrow](../sources/REF-182-apache-arrow.md) — documentacion.
- [REF-183 · Apache Parquet](../sources/REF-183-apache-parquet.md) — documentacion.

## Contrato, implementación y pruebas
- **Contrato funcional:** especificación en `specs/`, identificadores estables y validación de entrada / salida.
- **Propiedades no negociables:** Registrar experimentos, seeds, DVC/manifests, semántica de jobs y trazas extremo a extremo.
- **Benchmark mínimo propuesto:** Recuperación de trabajos tras caída, reproducibilidad de métricas y control de costo CPU/GPU.
- **Evidencias:** registrar commit, snapshot de red, escenario, seed, versiones de librerías y motor, unidades, tolerancias, tablas y logs sanitizados.
- **Control de cambios:** PR bloqueada si se ocultan incertidumbres o se afirma que una ficha es texto completo cuando no lo es.

## Skills responsables
- `unitesis-devops-observability`
- `unitesis-testing-qa`

## Palabras clave multilingües
MLOps, DevOps y observabilidad; modularity; reproducibility; industrial validation
