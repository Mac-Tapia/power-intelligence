# Frontend, experiencia GIS y unifilar — soporte científico y reglas implementables

**Área de código:** `workstation-web, map-engine, one-line-engine`.  
**Consulta:** `python scripts/research/query_evidence.py --module fe --limit 12`.  
**Convención:** una ficha markdown describe una fuente o registro, **no contiene PDFs de terceros**.

## Tesis de arquitectura de este módulo
Mantener estado servidor, UI y grafo visual independientes, unidos por IDs eléctricos inmutables.

## Qué está sustentado y qué es decisión UNITESIS
- **Evidencia externa:** las fichas enlazadas describen investigaciones, herramientas o normas existentes (calidad bibliográfica indicada individualmente).
- **Decisión de ingeniería UNITESIS:** adoptar interfaces y restricciones de aceptación diseñadas para este producto. No es conclusión causal de los artículos.
- **Vacío experimental:** no existe validación del módulo sobre VNR-GIS de distribuidoras dentro de esta biblioteca; hay que programar experimentos.

## Evidencia científica/tesis más directamente relacionada
- [REF-096 · D3: Data-Driven Documents](../sources/REF-096-d3-data-driven-documents.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-097 · Vega-Lite: A Grammar of Interactive Graphics](../sources/REF-097-vega-lite-a-grammar-of-interactive-graphics.md) — articulo_revista, EN; `identificado_en_fuente_web`.
- [REF-098 · Usability Analysis of Visual Programming Environments: A Cognitive Dimensions Framework](../sources/REF-098-usability-analysis-of-visual-programming-environments-a-cognitive-dimens.md) — articulo_revista, EN; `identificado_en_fuente_web`.

## Documentación, guías o estándares útiles (no confundir con papers)
- [REF-175 · MapLibre GL JS](../sources/REF-175-maplibre-gl-js.md) — documentacion.
- [REF-176 · React Flow](../sources/REF-176-react-flow.md) — documentacion.

## Contrato, implementación y pruebas
- **Contrato funcional:** especificación en `specs/`, identificadores estables y validación de entrada / salida.
- **Propiedades no negociables:** Mantener estado servidor, UI y grafo visual independientes, unidos por IDs eléctricos inmutables.
- **Benchmark mínimo propuesto:** Prueba E2E de selección de activo GIS→unifilar→detalle con snapshot consistente.
- **Evidencias:** registrar commit, snapshot de red, escenario, seed, versiones de librerías y motor, unidades, tolerancias, tablas y logs sanitizados.
- **Control de cambios:** PR bloqueada si se ocultan incertidumbres o se afirma que una ficha es texto completo cuando no lo es.

## Skills responsables
- `unitesis-frontend-react`
- `unitesis-design-system`

## Palabras clave multilingües
Frontend, experiencia GIS y unifilar; modularity; reproducibility; industrial validation
