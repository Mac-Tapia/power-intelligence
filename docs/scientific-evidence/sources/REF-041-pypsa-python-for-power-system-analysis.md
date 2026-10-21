---
id: REF-041
title: "PyPSA: Python for Power System Analysis"
kind: articulo_revista
language: EN
primary_module: solver
related_modules: ["solver", "qa", "gis"]
source_url: "https://doi.org/10.5334/jors.188"
doi: "10.5334/jors.188"
verification: identificado_en_fuente_web
source_origin: web_2026-10-17
full_text_reviewed: false
accessed_date: '2026-10-17'
---
# REF-041 · PyPSA: Python for Power System Analysis

**Tipo:** articulo_revista · **Idioma:** EN · **Módulo principal:** [Estudios eléctricos verificables](../modules/solver.md).  
**Fuente primaria o registro:** https://doi.org/10.5334/jors.188  
**DOI (si se identificó):** 10.5334/jors.188.  
**Estado epistemológico:** `identificado_en_fuente_web`. La ficha es síntesis de páginas/registros y/o referencia legada, **NO es el texto íntegro de la publicación**, ni confirma lectura exhaustiva de PDF.

## Pregunta técnica de UNITESIS que fundamenta
¿Cómo justificar el diseño de **Estudios eléctricos verificables** mediante una referencia documentada, con resultados contrastables para el contexto de UNITESIS Power Intelligence?

## Aporte y aplicación concreta
Estudios multihorarios de energía y expansión con modelos comparables

**Regla de implementación propuesta (inferencia de ingeniería, no cita literal):** Separar AC equilibrado, trifásico desequilibrado, cortocircuito y dinámica; cada resultado registra solver y tolerancias.

**Componentes a los que se traslada:** `power-simulation, PowerFlowPort`.

## Actividades para el agente
1. Recuperar de la URL la versión bibliográfica definitiva y comprobar autoría, año, DOI, tipo de publicación y disponibilidad legítima del texto completo.
2. Documentar metodología, tamaño de problema, hipótesis y datos de evaluación; señalar expresamente qué **NO** se valida en sistemas de distribución peruanos.
3. Convertir el aporte transferible en un ADR y tarea SDD con código trazable, fixtures reproducibles y análisis de alternativas.
4. Vincular a `specs/<feature>/research.md`, sin incorporar texto protegido por copyright ni simular que se ha reproducido el experimento.

## Prueba o evidencia exigida
Comparar IEEE 13/34/123 y otros casos disponibles, magnitudes, ángulos, pérdidas, KCL, convergencia.

## Límites y riesgos
Las métricas y supuestos del artículo no se transfieren automáticamente a redes GIS del Perú.
No usar esta ficha como prueba de que un modelo está entrenado, un conector conectado, un solver calibrado o una norma vigente.

## Consulta rápida para agentes
`python scripts/research/query_evidence.py --module solver --query "pypsa-python-for-power-system-analys"`

## Palabras clave
`solver, unitesis, evidencia, scientific-software, en`
