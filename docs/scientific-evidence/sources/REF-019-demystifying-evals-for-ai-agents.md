---
id: REF-019
title: "Demystifying evals for AI agents"
kind: guia_tecnica
language: EN
primary_module: qa
related_modules: ["qa", "solver", "fe"]
source_url: "https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents"
doi: null
verification: identificado_en_fuente_web
source_origin: web_2026-10-17
full_text_reviewed: false
accessed_date: '2026-10-17'
---
# REF-019 · Demystifying evals for AI agents

**Tipo:** guia_tecnica · **Idioma:** EN · **Módulo principal:** [Pruebas de aceptación científica y de agentes](../modules/qa.md).  
**Fuente primaria o registro:** https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents  
**DOI (si se identificó):** pendiente / no aplica.  
**Estado epistemológico:** `identificado_en_fuente_web`. La ficha es síntesis de páginas/registros y/o referencia legada, **NO es el texto íntegro de la publicación**, ni confirma lectura exhaustiva de PDF.

## Pregunta técnica de UNITESIS que fundamenta
¿Cómo justificar el diseño de **Pruebas de aceptación científica y de agentes** mediante una referencia documentada, con resultados contrastables para el contexto de UNITESIS Power Intelligence?

## Aporte y aplicación concreta
Definir evaluaciones de agentes reproducibles, adversariales y por trayectoria

**Regla de implementación propuesta (inferencia de ingeniería, no cita literal):** Los tests de scaffold NO prueban precisión eléctrica ni legalidad; crear datasets de referencia.

**Componentes a los que se traslada:** `tests, benchmarks, evidence`.

## Actividades para el agente
1. Recuperar de la URL la versión bibliográfica definitiva y comprobar autoría, año, DOI, tipo de publicación y disponibilidad legítima del texto completo.
2. Documentar metodología, tamaño de problema, hipótesis y datos de evaluación; señalar expresamente qué **NO** se valida en sistemas de distribución peruanos.
3. Convertir el aporte transferible en un ADR y tarea SDD con código trazable, fixtures reproducibles y análisis de alternativas.
4. Vincular a `specs/<feature>/research.md`, sin incorporar texto protegido por copyright ni simular que se ha reproducido el experimento.

## Prueba o evidencia exigida
Criterios de aceptación cuantificados por estudio, error físico, seguridad y UX.

## Límites y riesgos
Es guía de ingeniería, no experimento científico arbitrado.
No usar esta ficha como prueba de que un modelo está entrenado, un conector conectado, un solver calibrado o una norma vigente.

## Consulta rápida para agentes
`python scripts/research/query_evidence.py --module qa --query "demystifying-evals-for-ai-agents"`

## Palabras clave
`qa, unitesis, evidencia, scientific-software, en`
