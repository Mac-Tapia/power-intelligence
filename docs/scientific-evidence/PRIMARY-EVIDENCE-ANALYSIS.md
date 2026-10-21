# Análisis de evidencia primaria prioritaria

**Estado:** fichas interpretativas basadas en registros editoriales, abstracts o páginas institucionales consultadas el 17-10-2026. No se han auditado exhaustivamente los textos completos. Cada bloque separa lo que la fuente aporta de la decisión/propuesta experimental de UNITESIS.

## 1. Google DeepMind / ICML — Graph Networks as Learnable Physics Engines for Inference and Control
- **Publicación:** Sanchez-Gonzalez et al., 2018, 35th ICML, PMLR 80, pp. 4470–4479.
- **Original:** https://proceedings.mlr.press/v80/sanchez-gonzalez18a.html
- **Contenido confirmado en abstract:** modelos sobre grafos con sesgo inductivo para sistemas dinámicos; se evaluaron ocho sistemas físicos y reportaron generalización estructural.
- **No demostrado:** que esta arquitectura ya resuelva flujos AC desbalanceados de distribución del Perú.
- **UNITESIS:** investigar red eléctrica como grafo fase-terminal y comparar GNN frente a MLP y solver AC.
- **Prueba:** partición por alimentador completo, prueba de interruptores abiertos, KCL por barra/fase, tensiones y pérdidas fuera de distribución (OOD).
- **Módulos:** `graph`, `sciml`, `solver`.

## 2. Raissi, Perdikaris y Karniadakis — Physics-informed neural networks
- **Publicación:** *Journal of Computational Physics*, 378 (2019), 686–707; DOI: 10.1016/j.jcp.2018.10.045.
- **Original:** https://doi.org/10.1016/j.jcp.2018.10.045
- **Contenido confirmado en abstract:** entrenamiento que incorpora ecuaciones de física en problemas directos e inversos de ecuaciones no lineales.
- **No demostrado:** que imponer residuos penalizados garantice soluciones exactas de Kirchhoff o factibilidad de red en todas las condiciones.
- **UNITESIS:** incluir residuales de potencia activa/reactiva con Ybus, tensiones complejas y restricciones de equipos.
- **Prueba:** benchmarks de flujos AC, medición separada de error de datos y residuales físicos; rechazo de soluciones fuera de tolerancia.
- **Módulos:** `sciml`, `solver`, `qa`.

## 3. Fobes, Claeys, Geth y Coffrin — PowerModelsDistribution.jl
- **Publicación:** *Electric Power Systems Research*, 189 (2020), 106664; DOI: 10.1016/j.epsr.2020.106664.
- **Original:** https://doi.org/10.1016/j.epsr.2020.106664
- **Contenido confirmado:** formulaciones de flujo de potencia y OPF trifásico desequilibrado, diversas aproximaciones lineales y relajaciones; comparación frente a OpenDSS en alimentadores IEEE de 13, 34, 123 barras.
- **No demostrado:** precisión de cualquier importador GIS de UNITESIS.
- **UNITESIS:** puerto común de simulación que pueda contrastar resultados de varios motores por caso y versión.
- **Prueba:** validación numérica multifase y tolerancias por magnitud, ángulo, pérdidas y solución convergente.
- **Módulos:** `solver`, `op`, `gis`.

## 4. RWTH Aachen — Learning on graphs from theory to industrial application in power management of distribution grids
- **Publicación:** tesis doctoral, RWTH Aachen, 2024 (verificar datos completos de autor en repositorio).
- **Original:** https://publications.rwth-aachen.de/record/992117
- **Contenido confirmado en registro doctoral:** experimentos con GNN para flujos AC y congestión. Se indica expresamente que una GNN evaluada **todavía no es suficientemente precisa para sustituir a los solvers clásicos**.
- **UNITESIS:** esquema GNN como motor sustituto para cribado y priorización de escenarios, jamás único certificador eléctrico.
- **Prueba:** conjunto OOD por alimentador, error máximo de tensión y pérdidas, robustez ante topologías inéditas.
- **Módulos:** `graph`, `sciml`, `solver`.

## 5. A. C. Neagu — Adaptive Equivalent Models for Distribution Networks
- **Publicación:** tesis de maestría, TU Delft, 2024.
- **Original:** https://repository.tudelft.nl/record/uuid%3Abd8572f6-9410-49c6-85cb-c7461d004094
- **Contenido confirmado en resumen:** equivalentes adaptativos para modelar zonas activas de distribución con observabilidad limitada o información confidencial.
- **UNITESIS:** diseñar equivalentes de subred para cómputo federado/P2P cuando no se permite compartir la topología íntegra.
- **Prueba:** comparar flujo a través de puntos frontera con subred explícita, midiendo potencia y tensiones.
- **Módulos:** `graph`, `p2p`, `solver`, `security`.

## 6. Rupolo — Planejamento integrado de redes de distribuição ... com fontes renováveis
- **Publicación:** tesis doctoral, Universidade Estadual Paulista (UNESP), 2017, portugués.
- **Original:** https://repositorio.unesp.br/entities/publication/46c006ce-081f-4863-9cad-51b45655f600
- **Contenido confirmado en resumen:** planificación MT/BT integral con costos de construcción, expansión, operación y confiabilidad; incertidumbre renovable y búsqueda por vecindad variable; casos de prueba en decenas y cientos de barras.
- **UNITESIS:** módulo de optimización multi-etapa con alternativas de expansión y restricciones MT-BT, más baseline heurístico GVNS.
- **Prueba:** reproducir formulación pequeña verificable, comparar costo y solución factible contra MILP/MINLP aplicable.
- **Módulos:** `op`, `market`, `solver`.

## 7. Grandez Fernandez — Planejamento da expansão ... considerando confiabilidade
- **Publicación:** tesis de maestría, UNESP, 2024, portugués.
- **Original:** https://repositorio.unesp.br/entities/publication/81bf30c8-9976-4ffa-a839-c06e42e72691
- **Contenido confirmado en registro:** planificación con alternativas radiales y ligeramente malladas para confiabilidad; modelo cónico entero mixto y heurísticas de vecindad variable.
- **UNITESIS:** considerar confiabilidad y restauración como criterios de expansión adicionales a pérdidas y CAPEX.
- **Prueba:** contingencias con switches, distinción radialidad operativa frente a redundancia física, costos auditables.
- **Módulos:** `op`, `graph`, `solver`.

## 8. Google Research — MapReduce
- **Publicación:** Dean y Ghemawat, 2004, *MapReduce: Simplified Data Processing on Large Clusters*.
- **Original:** https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/
- **Contenido confirmado:** modelo de procesamiento distribuido de datos a gran escala con tareas map/reduce y tolerancia a fallos.
- **UNITESIS:** procesamiento particionado de VNR-GIS/series temporales y escenarios, con procesos idempotentes y manifiestos de resultados.
- **No demostrado:** que MapReduce sea la arquitectura óptima para todo flujo de carga; se eligen workers de simulación especializados.
- **Prueba:** consistencia y recuperación de ingestión interrumpida, sin duplicar activos ni métricas.
- **Módulos:** `arch`, `bk`, `ops`.

## 9. Anthropic — Building effective agents / Demystifying evals for AI agents
- **Publicación:** artículos de ingeniería, Anthropic, 2024 y 2026, respectivamente. **No son artículos académicos arbitrados**.
- **Original:** https://www.anthropic.com/engineering/building-effective-agents y https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- **Contenido confirmado:** distinción de patrones de agentes y prácticas de evaluación con graders programáticos, basados en modelo y evaluación humana.
- **UNITESIS:** separar agente planificador/consultor y ejecutor autorizado, y evaluar acciones finales y fidelidad de fuentes, no sólo conversaciones.
- **Prueba:** ejecuciones deterministas en sandbox, riesgo de prompt injection, violaciones de permisos y resultados no fundamentados.
- **Módulos:** `llm`, `security`, `qa`, `sdd`.

## 10. D3: Data-Driven Documents
- **Publicación:** Bostock, Ogievetsky y Heer, 2011, *IEEE Transactions on Visualization and Computer Graphics*, 17(12), 2301–2309.
- **Original:** https://doi.org/10.1109/TVCG.2011.185
- **Contenido confirmado:** representación transparente, asociación de datos con el DOM y transformaciones visuales interactivas.
- **UNITESIS:** trazabilidad visual de activos y resultados, resaltado coordinado mapa↔unifilar↔escenario; no obliga a elegir una sola librería frontend.
- **Prueba:** consistencia de selección, rendimiento con miles de elementos y accesibilidad por teclado.
- **Módulos:** `fe`, `gis`, `qa`.

## 11. Yumbla Romero — Metodologia para reconfiguração de redes ativas ... matheurística
- **Publicación:** tesis de maestría, UNESP, 2021, portugués.
- **Original:** https://repositorio.unesp.br/entities/publication/4b2de0b8-96f1-4571-8fea-99da6a26236c/full
- **Contenido confirmado:** metodología de reconfiguración de redes activas con variables estocásticas y formulación de optimización combinada.
- **UNITESIS:** comparar algoritmos MILP/MISOCP + heurísticas antes de incorporar políticas MARL.
- **Prueba:** costos y pérdidas con escenarios cronológicos, radialidad y violaciones de tensiones.
- **Módulos:** `op`, `marl`, `solver`.

## 12. Anthropic — How we built our multi-agent research system
- **Publicación:** artículo de ingeniería industrial (no paper arbitrado), 2025.
- **Original:** https://www.anthropic.com/engineering/multi-agent-research-system
- **Contenido confirmado:** coordinación multiagente orientada a tareas de investigación, junto con recomendaciones de evaluación de resultados.
- **UNITESIS:** workers de búsqueda y contraste bibliográfico aislados de agentes autorizados para cambios de código y operaciones.
- **Prueba:** tasa de referencias válidas, completitud, deduplicación y ausencia de ejecución lateral de herramientas.
- **Módulos:** `llm`, `graphrag`, `security`.

## Uso como criterio de aceptación

Antes de aprobar una implementación, el agente debe entregar una tabla con: decisión, fuente original, supuesto transferible, baseline, experimento de validación, umbral explícito y evidencia reproducible. Ninguna referencia de este documento certifica que UNITESIS ya cumpla ese umbral.
