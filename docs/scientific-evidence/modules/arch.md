# Arquitectura empresarial y plataforma — soporte científico y reglas implementables

**Área de código:** `control-api, application, workers`.  
**Consulta:** `python scripts/research/query_evidence.py --module arch --limit 12`.  
**Convención:** una ficha markdown describe una fuente o registro, **no contiene PDFs de terceros**.

## Tesis de arquitectura de este módulo
La solución conserva un monolito modular con workers; medir acoplamiento, latencia y fallas antes de extraer servicios.

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
- [REF-003 · Bigtable: A Distributed Storage System for Structured Data](../sources/REF-003-bigtable-a-distributed-storage-system-for-structured-data.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.
- [REF-004 · Spanner: Google's Globally-Distributed Database](../sources/REF-004-spanner-google-s-globally-distributed-database.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.

## Documentación, guías o estándares útiles (no confundir con papers)
- [REF-089 · Microservices](../sources/REF-089-microservices.md) — articulo_tecnico.
- [REF-090 · Monolith First](../sources/REF-090-monolith-first.md) — articulo_tecnico.
- [REF-091 · What do you mean by Event-Driven?](../sources/REF-091-what-do-you-mean-by-event-driven.md) — articulo_tecnico.
- [REF-110 · Microservices Guide — Martin Fowler](../sources/REF-110-microservices-guide-martin-fowler.md) — libro_o_guia_tecnica.
- [REF-113 · AWS Well-Architected: six pillars](../sources/REF-113-aws-well-architected-six-pillars.md) — libro_o_guia_tecnica.
- [REF-114 · AWS Well-Architected definitions](../sources/REF-114-aws-well-architected-definitions.md) — libro_o_guia_tecnica.
- [REF-153 · Power System Analysis and Design, 7th ed. (2022)](../sources/REF-153-power-system-analysis-and-design-7th-ed-2022.md) — libro.
- [REF-154 · Power Generation, Operation and Control, 3rd ed. (2013)](../sources/REF-154-power-generation-operation-and-control-3rd-ed-2013.md) — libro.
- [REF-158 · PyPSA](../sources/REF-158-pypsa.md) — documentacion.
- [REF-164 · Open Energy Modelling Framework / oemof](../sources/REF-164-open-energy-modelling-framework-oemof.md) — documentacion.
- [REF-177 · FastAPI](../sources/REF-177-fastapi.md) — documentacion.
- [REF-181 · OpenAPI specification](../sources/REF-181-openapi-specification.md) — documentacion.
- [REF-185 · IEC Common Information Model introduction](../sources/REF-185-iec-common-information-model-introduction.md) — norma_o_estandar.
- [REF-189 · ISO 25010 quality model (ISO catalog)](../sources/REF-189-iso-25010-quality-model-iso-catalog.md) — norma_o_estandar.

## Contrato, implementación y pruebas
- **Contrato funcional:** especificación en `specs/`, identificadores estables y validación de entrada / salida.
- **Propiedades no negociables:** La solución conserva un monolito modular con workers; medir acoplamiento, latencia y fallas antes de extraer servicios.
- **Benchmark mínimo propuesto:** Arquitectura C4 y ADR con contract tests y simulación de fallos de worker.
- **Evidencias:** registrar commit, snapshot de red, escenario, seed, versiones de librerías y motor, unidades, tolerancias, tablas y logs sanitizados.
- **Control de cambios:** PR bloqueada si se ocultan incertidumbres o se afirma que una ficha es texto completo cuando no lo es.

## Skills responsables
- `unitesis-domain-ddd`
- `unitesis-backend-fastapi`
- `unitesis-devops-observability`

## Palabras clave multilingües
software architecture; DDD; arquitectura modular; arquitetura hexagonal; Architektur
