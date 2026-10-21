---
id: REF-037
title: "Graph Neural Networks and Their Applications in Power Systems: A Review"
kind: articulo_conferencia
language: EN
primary_module: graph
related_modules: ["graph", "gis", "sciml"]
source_url: "https://ieeexplore.ieee.org/document/11103635/"
doi: null
verification: identificado_en_fuente_web
source_origin: web_2026-10-17
full_text_reviewed: false
accessed_date: '2026-10-17'
---
# REF-037 · Graph Neural Networks and Their Applications in Power Systems: A Review

**Tipo:** articulo_conferencia · **Idioma:** EN · **Módulo principal:** [Grafo físico y GNN](../modules/graph.md).  
**Fuente primaria o registro:** https://ieeexplore.ieee.org/document/11103635/  
**DOI (si se identificó):** pendiente / no aplica.  
**Estado epistemológico:** `identificado_en_fuente_web`. La ficha es síntesis de páginas/registros y/o referencia legada, **NO es el texto íntegro de la publicación**, ni confirma lectura exhaustiva de PDF.

## Pregunta técnica de UNITESIS que fundamenta
¿Cómo justificar el diseño de **Grafo físico y GNN** mediante una referencia documentada, con resultados contrastables para el contexto de UNITESIS Power Intelligence?

## Aporte y aplicación concreta
Revisar observabilidad, fallas y robustez ante cambios de red

**Regla de implementación propuesta (inferencia de ingeniería, no cita literal):** Operar sobre terminales, fases y estados de interruptor; las inferencias no reescriben red certificada.

**Componentes a los que se traslada:** `power-graph, power-topology, power-sciml`.

## Actividades para el agente
1. Recuperar de la URL la versión bibliográfica definitiva y comprobar autoría, año, DOI, tipo de publicación y disponibilidad legítima del texto completo.
2. Documentar metodología, tamaño de problema, hipótesis y datos de evaluación; señalar expresamente qué **NO** se valida en sistemas de distribución peruanos.
3. Convertir el aporte transferible en un ADR y tarea SDD con código trazable, fixtures reproducibles y análisis de alternativas.
4. Vincular a `specs/<feature>/research.md`, sin incorporar texto protegido por copyright ni simular que se ha reproducido el experimento.

## Prueba o evidencia exigida
Cambiar configuración de interruptores y comprobar componentes, islas y tensión contra solver.

## Límites y riesgos
La evaluación del trabajo de origen no representa una medición de UNITESIS.
No usar esta ficha como prueba de que un modelo está entrenado, un conector conectado, un solver calibrado o una norma vigente.

## Consulta rápida para agentes
`python scripts/research/query_evidence.py --module graph --query "graph-neural-networks-and-their-appl"`

## Palabras clave
`graph, unitesis, evidencia, scientific-software, en`
