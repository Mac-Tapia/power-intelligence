---
id: REF-004
title: "Spanner: Google's Globally-Distributed Database"
kind: articulo_conferencia
language: EN
primary_module: bk
related_modules: ["bk", "arch", "qa"]
source_url: "https://research.google/pubs/spanner-googles-globally-distributed-database-2/"
doi: null
verification: identificado_en_fuente_web
source_origin: web_2026-10-17
full_text_reviewed: false
accessed_date: '2026-10-17'
---
# REF-004 · Spanner: Google's Globally-Distributed Database

**Tipo:** articulo_conferencia · **Idioma:** EN · **Módulo principal:** [Persistencia, linaje y series temporales](../modules/bk.md).  
**Fuente primaria o registro:** https://research.google/pubs/spanner-googles-globally-distributed-database-2/  
**DOI (si se identificó):** pendiente / no aplica.  
**Estado epistemológico:** `identificado_en_fuente_web`. La ficha es síntesis de páginas/registros y/o referencia legada, **NO es el texto íntegro de la publicación**, ni confirma lectura exhaustiva de PDF.

## Pregunta técnica de UNITESIS que fundamenta
¿Cómo justificar el diseño de **Persistencia, linaje y series temporales** mediante una referencia documentada, con resultados contrastables para el contexto de UNITESIS Power Intelligence?

## Aporte y aplicación concreta
Estudiar versiones temporales y consistencia de snapshots multiempresa

**Regla de implementación propuesta (inferencia de ingeniería, no cita literal):** Asegurar identidad de activos, versiones bitemporales y lecturas idempotentes con datos fuera de orden.

**Componentes a los que se traslada:** `PostGIS, snapshots, measurements, datasets`.

## Actividades para el agente
1. Recuperar de la URL la versión bibliográfica definitiva y comprobar autoría, año, DOI, tipo de publicación y disponibilidad legítima del texto completo.
2. Documentar metodología, tamaño de problema, hipótesis y datos de evaluación; señalar expresamente qué **NO** se valida en sistemas de distribución peruanos.
3. Convertir el aporte transferible en un ADR y tarea SDD con código trazable, fixtures reproducibles y análisis de alternativas.
4. Vincular a `specs/<feature>/research.md`, sin incorporar texto protegido por copyright ni simular que se ha reproducido el experimento.

## Prueba o evidencia exigida
Prueba de reproducibilidad de snapshot + ausencia de contaminación entre tenants.

## Límites y riesgos
La evaluación del trabajo de origen no representa una medición de UNITESIS.
No usar esta ficha como prueba de que un modelo está entrenado, un conector conectado, un solver calibrado o una norma vigente.

## Consulta rápida para agentes
`python scripts/research/query_evidence.py --module bk --query "spanner-google-s-globally-distribute"`

## Palabras clave
`bk, unitesis, evidencia, scientific-software, en`
