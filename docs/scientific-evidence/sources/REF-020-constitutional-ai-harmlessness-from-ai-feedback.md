---
id: REF-020
title: "Constitutional AI: Harmlessness from AI feedback"
kind: preprint
language: EN
primary_module: llm
related_modules: ["llm", "graphrag", "security"]
source_url: "https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback"
doi: null
verification: identificado_en_fuente_web
source_origin: web_2026-10-17
full_text_reviewed: false
accessed_date: '2026-10-17'
---
# REF-020 · Constitutional AI: Harmlessness from AI feedback

**Tipo:** preprint · **Idioma:** EN · **Módulo principal:** [LLM local, orquestación y permisos](../modules/llm.md).  
**Fuente primaria o registro:** https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback  
**DOI (si se identificó):** pendiente / no aplica.  
**Estado epistemológico:** `identificado_en_fuente_web`. La ficha es síntesis de páginas/registros y/o referencia legada, **NO es el texto íntegro de la publicación**, ni confirma lectura exhaustiva de PDF.

## Pregunta técnica de UNITESIS que fundamenta
¿Cómo justificar el diseño de **LLM local, orquestación y permisos** mediante una referencia documentada, con resultados contrastables para el contexto de UNITESIS Power Intelligence?

## Aporte y aplicación concreta
Diseñar principios de actuación del agente sin confundir alineamiento con garantía física

**Regla de implementación propuesta (inferencia de ingeniería, no cita literal):** El LLM interpreta y propone planes; herramientas tipadas ejecutan simulaciones, no comandos arbitrarios.

**Componentes a los que se traslada:** `power-agents, MCP, RAG`.

## Actividades para el agente
1. Recuperar de la URL la versión bibliográfica definitiva y comprobar autoría, año, DOI, tipo de publicación y disponibilidad legítima del texto completo.
2. Documentar metodología, tamaño de problema, hipótesis y datos de evaluación; señalar expresamente qué **NO** se valida en sistemas de distribución peruanos.
3. Convertir el aporte transferible en un ADR y tarea SDD con código trazable, fixtures reproducibles y análisis de alternativas.
4. Vincular a `specs/<feature>/research.md`, sin incorporar texto protegido por copyright ni simular que se ha reproducido el experimento.

## Prueba o evidencia exigida
Evaluar fidelidad de citas, prompt injection, no-ejecución de cambios reales y costo/latencia.

## Límites y riesgos
Puede carecer de revisión por pares; verificar versiones, experimentos y réplicas.
No usar esta ficha como prueba de que un modelo está entrenado, un conector conectado, un solver calibrado o una norma vigente.

## Consulta rápida para agentes
`python scripts/research/query_evidence.py --module llm --query "constitutional-ai-harmlessness-from-"`

## Palabras clave
`llm, unitesis, evidencia, scientific-software, en`
