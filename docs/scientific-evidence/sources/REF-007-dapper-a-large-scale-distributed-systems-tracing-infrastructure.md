---
id: REF-007
title: "Dapper, a Large-Scale Distributed Systems Tracing Infrastructure"
kind: articulo_tecnico
language: EN
primary_module: ops
related_modules: ["ops", "arch", "qa"]
source_url: "https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/"
doi: null
verification: identificado_en_fuente_web
source_origin: web_2026-10-17
full_text_reviewed: false
accessed_date: '2026-10-17'
---
# REF-007 · Dapper, a Large-Scale Distributed Systems Tracing Infrastructure

**Tipo:** articulo_tecnico · **Idioma:** EN · **Módulo principal:** [MLOps, DevOps y observabilidad](../modules/ops.md).  
**Fuente primaria o registro:** https://research.google/pubs/dapper-a-large-scale-distributed-systems-tracing-infrastructure/  
**DOI (si se identificó):** pendiente / no aplica.  
**Estado epistemológico:** `identificado_en_fuente_web`. La ficha es síntesis de páginas/registros y/o referencia legada, **NO es el texto íntegro de la publicación**, ni confirma lectura exhaustiva de PDF.

## Pregunta técnica de UNITESIS que fundamenta
¿Cómo justificar el diseño de **MLOps, DevOps y observabilidad** mediante una referencia documentada, con resultados contrastables para el contexto de UNITESIS Power Intelligence?

## Aporte y aplicación concreta
Propagar trace_id desde solicitudes API hasta solvers y agentes

**Regla de implementación propuesta (inferencia de ingeniería, no cita literal):** Registrar experimentos, seeds, DVC/manifests, semántica de jobs y trazas extremo a extremo.

**Componentes a los que se traslada:** `workers, MLflow, traces, deploy`.

## Actividades para el agente
1. Recuperar de la URL la versión bibliográfica definitiva y comprobar autoría, año, DOI, tipo de publicación y disponibilidad legítima del texto completo.
2. Documentar metodología, tamaño de problema, hipótesis y datos de evaluación; señalar expresamente qué **NO** se valida en sistemas de distribución peruanos.
3. Convertir el aporte transferible en un ADR y tarea SDD con código trazable, fixtures reproducibles y análisis de alternativas.
4. Vincular a `specs/<feature>/research.md`, sin incorporar texto protegido por copyright ni simular que se ha reproducido el experimento.

## Prueba o evidencia exigida
Recuperación de trabajos tras caída, reproducibilidad de métricas y control de costo CPU/GPU.

## Límites y riesgos
Verificar metadatos, supuestos y aplicabilidad; no sobreinterpretar título o resumen.
No usar esta ficha como prueba de que un modelo está entrenado, un conector conectado, un solver calibrado o una norma vigente.

## Consulta rápida para agentes
`python scripts/research/query_evidence.py --module ops --query "dapper-a-large-scale-distributed-sys"`

## Palabras clave
`ops, unitesis, evidencia, scientific-software, en`
