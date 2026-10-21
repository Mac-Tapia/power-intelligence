---
id: REF-147
title: "Supervised learning for optimal investment planning in active networks — UPC"
kind: tesis
language: EN
primary_module: sciml
related_modules: ["sciml", "graph", "solver"]
source_url: "https://upcommons.upc.edu/entities/publication/892b5cda-a92d-4e8e-917b-d8716f23c73b"
doi: null
verification: importado_pendiente_auditoria
source_origin: importado_V2
full_text_reviewed: false
accessed_date: '2026-10-17'
---
# REF-147 · Supervised learning for optimal investment planning in active networks — UPC

**Tipo:** tesis · **Idioma:** EN · **Módulo principal:** [PINN, GNN y simuladores sustitutos](../modules/sciml.md).  
**Fuente primaria o registro:** https://upcommons.upc.edu/entities/publication/892b5cda-a92d-4e8e-917b-d8716f23c73b  
**DOI (si se identificó):** pendiente / no aplica.  
**Estado epistemológico:** `importado_pendiente_auditoria`. La ficha es síntesis de páginas/registros y/o referencia legada, **NO es el texto íntegro de la publicación**, ni confirma lectura exhaustiva de PDF.

## Pregunta técnica de UNITESIS que fundamenta
¿Cómo justificar el diseño de **PINN, GNN y simuladores sustitutos** mediante una referencia documentada, con resultados contrastables para el contexto de UNITESIS Power Intelligence?

## Aporte y aplicación concreta
Fuente heredada para contraste de arquitectura/algoritmos del área «PINN, GNN y simuladores sustitutos»; evaluar si es directamente transferible al caso UNITESIS antes de asumirlo.

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
Grado académico y alcance de la tesis deben confirmarse en registro institucional.
No usar esta ficha como prueba de que un modelo está entrenado, un conector conectado, un solver calibrado o una norma vigente.

## Consulta rápida para agentes
`python scripts/research/query_evidence.py --module sciml --query "supervised-learning-for-optimal-inve"`

## Palabras clave
`sciml, unitesis, evidencia, scientific-software, en`
