---
id: REF-078
title: "Deep Statistical Solver for Distribution System State Estimation"
kind: tesis_maestria
language: EN
primary_module: sciml
related_modules: ["sciml", "graph", "solver"]
source_url: "https://repository.tudelft.nl/record/uuid%3A1bc2734e-0ecc-4841-8a19-638a475b0c35"
doi: null
verification: identificado_en_fuente_web
source_origin: web_2026-10-17
full_text_reviewed: false
accessed_date: '2026-10-17'
---
# REF-078 · Deep Statistical Solver for Distribution System State Estimation

**Tipo:** tesis_maestria · **Idioma:** EN · **Módulo principal:** [PINN, GNN y simuladores sustitutos](../modules/sciml.md).  
**Fuente primaria o registro:** https://repository.tudelft.nl/record/uuid%3A1bc2734e-0ecc-4841-8a19-638a475b0c35  
**DOI (si se identificó):** pendiente / no aplica.  
**Estado epistemológico:** `identificado_en_fuente_web`. La ficha es síntesis de páginas/registros y/o referencia legada, **NO es el texto íntegro de la publicación**, ni confirma lectura exhaustiva de PDF.

## Pregunta técnica de UNITESIS que fundamenta
¿Cómo justificar el diseño de **PINN, GNN y simuladores sustitutos** mediante una referencia documentada, con resultados contrastables para el contexto de UNITESIS Power Intelligence?

## Aporte y aplicación concreta
Comparar GNN informada por física contra WLS bajo baja observabilidad

**Regla de implementación propuesta (inferencia de ingeniería, no cita literal):** Entrenar en redes GIS representativas y escenarios físicos; jamás declarar física exacta por penalización soft.

**Componentes a los que se traslada:** `power-sciml, ml-training`.

## Actividades para el agente
1. Recuperar de la URL la versión bibliográfica definitiva y comprobar autoría, año, DOI, tipo de publicación y disponibilidad legítima del texto completo.
2. Documentar metodología, tamaño de problema, hipótesis y datos de evaluación; señalar expresamente qué **NO** se valida en sistemas de distribución peruanos.
3. Convertir el aporte transferible en un ADR y tarea SDD con código trazable, fixtures reproducibles y análisis de alternativas.
4. Vincular a `specs/<feature>/research.md`, sin incorporar texto protegido por copyright ni simular que se ha reproducido el experimento.

## Prueba o evidencia exigida
Pruebas OOD por red/topología, error p.u., KCL, intervalos calibrados y rechazo de soluciones inviables.

## Límites y riesgos
Los resultados pueden tener alcance limitado a redes y hardware de estudio.
No usar esta ficha como prueba de que un modelo está entrenado, un conector conectado, un solver calibrado o una norma vigente.

## Consulta rápida para agentes
`python scripts/research/query_evidence.py --module sciml --query "deep-statistical-solver-for-distribu"`

## Palabras clave
`sciml, unitesis, evidencia, scientific-software, en`
