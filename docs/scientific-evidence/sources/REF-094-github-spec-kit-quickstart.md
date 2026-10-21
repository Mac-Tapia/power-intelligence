---
id: REF-094
title: "GitHub Spec Kit quickstart"
kind: documentacion
language: EN
primary_module: sdd
related_modules: ["sdd", "qa", "arch"]
source_url: "https://github.github.com/spec-kit/quickstart"
doi: null
verification: identificado_en_fuente_web
source_origin: web_2026-10-17
full_text_reviewed: false
accessed_date: '2026-10-17'
---
# REF-094 · GitHub Spec Kit quickstart

**Tipo:** documentacion · **Idioma:** EN · **Módulo principal:** [SDD, GitHub, skills y worktrees](../modules/sdd.md).  
**Fuente primaria o registro:** https://github.github.com/spec-kit/quickstart  
**DOI (si se identificó):** pendiente / no aplica.  
**Estado epistemológico:** `identificado_en_fuente_web`. La ficha es síntesis de páginas/registros y/o referencia legada, **NO es el texto íntegro de la publicación**, ni confirma lectura exhaustiva de PDF.

## Pregunta técnica de UNITESIS que fundamenta
¿Cómo justificar el diseño de **SDD, GitHub, skills y worktrees** mediante una referencia documentada, con resultados contrastables para el contexto de UNITESIS Power Intelligence?

## Aporte y aplicación concreta
Inicialización reproducible del pipeline SDD

**Regla de implementación propuesta (inferencia de ingeniería, no cita literal):** Toda feature se implementa en worktree con especificación, prueba, ADR y validación de evidencia.

**Componentes a los que se traslada:** `.specify, .agents/skills, AGENTS.md`.

## Actividades para el agente
1. Recuperar de la URL la versión bibliográfica definitiva y comprobar autoría, año, DOI, tipo de publicación y disponibilidad legítima del texto completo.
2. Documentar metodología, tamaño de problema, hipótesis y datos de evaluación; señalar expresamente qué **NO** se valida en sistemas de distribución peruanos.
3. Convertir el aporte transferible en un ADR y tarea SDD con código trazable, fixtures reproducibles y análisis de alternativas.
4. Vincular a `specs/<feature>/research.md`, sin incorporar texto protegido por copyright ni simular que se ha reproducido el experimento.

## Prueba o evidencia exigida
CI falla si hay cambio de contrato sin spec o prueba de compatibilidad.

## Límites y riesgos
Es documentación de herramienta, no evidencia independiente de eficacia científica.
No usar esta ficha como prueba de que un modelo está entrenado, un conector conectado, un solver calibrado o una norma vigente.

## Consulta rápida para agentes
`python scripts/research/query_evidence.py --module sdd --query "github-spec-kit-quickstart"`

## Palabras clave
`sdd, unitesis, evidencia, scientific-software, en`
