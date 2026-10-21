---
id: REF-005
title: "Dremel: Interactive Analysis of Web-Scale Datasets"
kind: articulo_conferencia
language: EN
primary_module: arch
related_modules: ["arch", "sdd", "ops"]
source_url: "https://research.google/pubs/dremel-interactive-analysis-of-web-scale-datasets-2/"
doi: null
verification: identificado_en_fuente_web
source_origin: web_2026-10-17
full_text_reviewed: false
accessed_date: '2026-10-17'
---
# REF-005 · Dremel: Interactive Analysis of Web-Scale Datasets

**Tipo:** articulo_conferencia · **Idioma:** EN · **Módulo principal:** [Arquitectura empresarial y plataforma](../modules/arch.md).  
**Fuente primaria o registro:** https://research.google/pubs/dremel-interactive-analysis-of-web-scale-datasets-2/  
**DOI (si se identificó):** pendiente / no aplica.  
**Estado epistemológico:** `identificado_en_fuente_web`. La ficha es síntesis de páginas/registros y/o referencia legada, **NO es el texto íntegro de la publicación**, ni confirma lectura exhaustiva de PDF.

## Pregunta técnica de UNITESIS que fundamenta
¿Cómo justificar el diseño de **Arquitectura empresarial y plataforma** mediante una referencia documentada, con resultados contrastables para el contexto de UNITESIS Power Intelligence?

## Aporte y aplicación concreta
Diseño de consultas columnares sobre resultados Parquet de estudios masivos

**Regla de implementación propuesta (inferencia de ingeniería, no cita literal):** La solución conserva un monolito modular con workers; medir acoplamiento, latencia y fallas antes de extraer servicios.

**Componentes a los que se traslada:** `control-api, application, workers`.

## Actividades para el agente
1. Recuperar de la URL la versión bibliográfica definitiva y comprobar autoría, año, DOI, tipo de publicación y disponibilidad legítima del texto completo.
2. Documentar metodología, tamaño de problema, hipótesis y datos de evaluación; señalar expresamente qué **NO** se valida en sistemas de distribución peruanos.
3. Convertir el aporte transferible en un ADR y tarea SDD con código trazable, fixtures reproducibles y análisis de alternativas.
4. Vincular a `specs/<feature>/research.md`, sin incorporar texto protegido por copyright ni simular que se ha reproducido el experimento.

## Prueba o evidencia exigida
Arquitectura C4 y ADR con contract tests y simulación de fallos de worker.

## Límites y riesgos
La evaluación del trabajo de origen no representa una medición de UNITESIS.
No usar esta ficha como prueba de que un modelo está entrenado, un conector conectado, un solver calibrado o una norma vigente.

## Consulta rápida para agentes
`python scripts/research/query_evidence.py --module arch --query "dremel-interactive-analysis-of-web-s"`

## Palabras clave
`arch, unitesis, evidencia, scientific-software, en`
