# LLM local, orquestación y permisos — soporte científico y reglas implementables

**Área de código:** `power-agents, MCP, RAG`.  
**Consulta:** `python scripts/research/query_evidence.py --module llm --limit 12`.  
**Convención:** una ficha markdown describe una fuente o registro, **no contiene PDFs de terceros**.

## Tesis de arquitectura de este módulo
El LLM interpreta y propone planes; herramientas tipadas ejecutan simulaciones, no comandos arbitrarios.

## Qué está sustentado y qué es decisión UNITESIS
- **Evidencia externa:** las fichas enlazadas describen investigaciones, herramientas o normas existentes (calidad bibliográfica indicada individualmente).
- **Decisión de ingeniería UNITESIS:** adoptar interfaces y restricciones de aceptación diseñadas para este producto. No es conclusión causal de los artículos.
- **Vacío experimental:** no existe validación del módulo sobre VNR-GIS de distribuidoras dentro de esta biblioteca; hay que programar experimentos.

## Evidencia científica/tesis más directamente relacionada
- [REF-009 · Attention Is All You Need](../sources/REF-009-attention-is-all-you-need.md) — articulo_conferencia, EN; `identificado_en_fuente_web`.
- [REF-020 · Constitutional AI: Harmlessness from AI feedback](../sources/REF-020-constitutional-ai-harmlessness-from-ai-feedback.md) — preprint, EN; `identificado_en_fuente_web`.
- [REF-039 · From Local to Global: A Graph RAG Approach to Query-Focused Summarization](../sources/REF-039-from-local-to-global-a-graph-rag-approach-to-query-focused-summarization.md) — preprint, EN; `identificado_en_fuente_web`.

## Documentación, guías o estándares útiles (no confundir con papers)
- [REF-016 · Building effective agents](../sources/REF-016-building-effective-agents.md) — guia_tecnica.
- [REF-017 · How we built our multi-agent research system](../sources/REF-017-how-we-built-our-multi-agent-research-system.md) — guia_tecnica.
- [REF-018 · Effective context engineering for AI agents](../sources/REF-018-effective-context-engineering-for-ai-agents.md) — guia_tecnica.

## Contrato, implementación y pruebas
- **Contrato funcional:** especificación en `specs/`, identificadores estables y validación de entrada / salida.
- **Propiedades no negociables:** El LLM interpreta y propone planes; herramientas tipadas ejecutan simulaciones, no comandos arbitrarios.
- **Benchmark mínimo propuesto:** Evaluar fidelidad de citas, prompt injection, no-ejecución de cambios reales y costo/latencia.
- **Evidencias:** registrar commit, snapshot de red, escenario, seed, versiones de librerías y motor, unidades, tolerancias, tablas y logs sanitizados.
- **Control de cambios:** PR bloqueada si se ocultan incertidumbres o se afirma que una ficha es texto completo cuando no lo es.

## Skills responsables
- `unitesis-marl-llm`
- `unitesis-mcp-connectors`

## Palabras clave multilingües
LLM local, orquestación y permisos; modularity; reproducibility; industrial validation
