---
id: REF-039
title: "From Local to Global: A Graph RAG Approach to Query-Focused Summarization"
kind: preprint
language: EN
primary_module: graphrag
related_modules: ["graphrag", "llm", "graph"]
source_url: "https://www.microsoft.com/en-us/research/publication/from-local-to-global-a-graph-rag-approach-to-query-focused-summarization/"
doi: null
verification: identificado_en_fuente_web
source_origin: web_2026-10-17
full_text_reviewed: false
accessed_date: '2026-10-17'
---
# REF-039 · From Local to Global: A Graph RAG Approach to Query-Focused Summarization

**Tipo:** preprint · **Idioma:** EN · **Módulo principal:** [GraphRAG y conocimiento técnico](../modules/graphrag.md).  
**Fuente primaria o registro:** https://www.microsoft.com/en-us/research/publication/from-local-to-global-a-graph-rag-approach-to-query-focused-summarization/  
**DOI (si se identificó):** pendiente / no aplica.  
**Estado epistemológico:** `identificado_en_fuente_web`. La ficha es síntesis de páginas/registros y/o referencia legada, **NO es el texto íntegro de la publicación**, ni confirma lectura exhaustiva de PDF.

## Pregunta técnica de UNITESIS que fundamenta
¿Cómo justificar el diseño de **GraphRAG y conocimiento técnico** mediante una referencia documentada, con resultados contrastables para el contexto de UNITESIS Power Intelligence?

## Aporte y aplicación concreta
Separar recuperación documental del grafo físico y adjuntar trazabilidad a respuestas

**Regla de implementación propuesta (inferencia de ingeniería, no cita literal):** Separar grafo documental de grafo eléctrico; citar normativa y vigencia sin inventar reglas.

**Componentes a los que se traslada:** `power-graphrag, retrieval`.

## Actividades para el agente
1. Recuperar de la URL la versión bibliográfica definitiva y comprobar autoría, año, DOI, tipo de publicación y disponibilidad legítima del texto completo.
2. Documentar metodología, tamaño de problema, hipótesis y datos de evaluación; señalar expresamente qué **NO** se valida en sistemas de distribución peruanos.
3. Convertir el aporte transferible en un ADR y tarea SDD con código trazable, fixtures reproducibles y análisis de alternativas.
4. Vincular a `specs/<feature>/research.md`, sin incorporar texto protegido por copyright ni simular que se ha reproducido el experimento.

## Prueba o evidencia exigida
Prueba de preguntas con documentos contradictorios, abrogados y fuentes sin acceso.

## Límites y riesgos
Puede carecer de revisión por pares; verificar versiones, experimentos y réplicas.
No usar esta ficha como prueba de que un modelo está entrenado, un conector conectado, un solver calibrado o una norma vigente.

## Consulta rápida para agentes
`python scripts/research/query_evidence.py --module graphrag --query "from-local-to-global-a-graph-rag-app"`

## Palabras clave
`graphrag, unitesis, evidencia, scientific-software, en`
