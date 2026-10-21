# GraphRAG y conocimiento técnico — soporte científico y reglas implementables

**Área de código:** `power-graphrag, retrieval`.  
**Consulta:** `python scripts/research/query_evidence.py --module graphrag --limit 12`.  
**Convención:** una ficha markdown describe una fuente o registro, **no contiene PDFs de terceros**.

## Tesis de arquitectura de este módulo
Separar grafo documental de grafo eléctrico; citar normativa y vigencia sin inventar reglas.

## Qué está sustentado y qué es decisión UNITESIS
- **Evidencia externa:** las fichas enlazadas describen investigaciones, herramientas o normas existentes (calidad bibliográfica indicada individualmente).
- **Decisión de ingeniería UNITESIS:** adoptar interfaces y restricciones de aceptación diseñadas para este producto. No es conclusión causal de los artículos.
- **Vacío experimental:** no existe validación del módulo sobre VNR-GIS de distribuidoras dentro de esta biblioteca; hay que programar experimentos.

## Evidencia científica/tesis más directamente relacionada
- [REF-039 · From Local to Global: A Graph RAG Approach to Query-Focused Summarization](../sources/REF-039-from-local-to-global-a-graph-rag-approach-to-query-focused-summarization.md) — preprint, EN; `identificado_en_fuente_web`.
- [REF-009 · Attention Is All You Need](../sources/REF-009-attention-is-all-you-need.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.
- [REF-020 · Constitutional AI: Harmlessness from AI feedback](../sources/REF-020-constitutional-ai-harmlessness-from-ai-feedback.md) — preprint, EN; `identificado_en_fuente_web`.

## Documentación, guías o estándares útiles (no confundir con papers)
- Consultar fuentes institucionales oficiales a partir de las fichas científicas y agregar sus versiones al registro.

## Contrato, implementación y pruebas
- **Contrato funcional:** especificación en `specs/`, identificadores estables y validación de entrada / salida.
- **Propiedades no negociables:** Separar grafo documental de grafo eléctrico; citar normativa y vigencia sin inventar reglas.
- **Benchmark mínimo propuesto:** Prueba de preguntas con documentos contradictorios, abrogados y fuentes sin acceso.
- **Evidencias:** registrar commit, snapshot de red, escenario, seed, versiones de librerías y motor, unidades, tolerancias, tablas y logs sanitizados.
- **Control de cambios:** PR bloqueada si se ocultan incertidumbres o se afirma que una ficha es texto completo cuando no lo es.

## Skills responsables
- `unitesis-electric-graph`
- `unitesis-technical-research`

## Palabras clave multilingües
GraphRAG y conocimiento técnico; modularity; reproducibility; industrial validation
