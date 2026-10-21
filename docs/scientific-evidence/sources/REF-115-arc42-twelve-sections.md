---
id: REF-115
title: "arc42 twelve sections"
kind: libro_o_guia_tecnica
language: EN
primary_module: sdd
related_modules: ["sdd", "qa", "arch"]
source_url: "https://examples.arc42.org/sections/"
doi: null
verification: importado_pendiente_auditoria
source_origin: importado_V2
full_text_reviewed: false
accessed_date: '2026-10-17'
---
# REF-115 · arc42 twelve sections

**Tipo:** libro_o_guia_tecnica · **Idioma:** EN · **Módulo principal:** [SDD, GitHub, skills y worktrees](../modules/sdd.md).  
**Fuente primaria o registro:** https://examples.arc42.org/sections/  
**DOI (si se identificó):** pendiente / no aplica.  
**Estado epistemológico:** `importado_pendiente_auditoria`. La ficha es síntesis de páginas/registros y/o referencia legada, **NO es el texto íntegro de la publicación**, ni confirma lectura exhaustiva de PDF.

## Pregunta técnica de UNITESIS que fundamenta
¿Cómo justificar el diseño de **SDD, GitHub, skills y worktrees** mediante una referencia documentada, con resultados contrastables para el contexto de UNITESIS Power Intelligence?

## Aporte y aplicación concreta
Fuente heredada para contraste de arquitectura/algoritmos del área «SDD, GitHub, skills y worktrees»; evaluar si es directamente transferible al caso UNITESIS antes de asumirlo.

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
Verificar metadatos, supuestos y aplicabilidad; no sobreinterpretar título o resumen.
No usar esta ficha como prueba de que un modelo está entrenado, un conector conectado, un solver calibrado o una norma vigente.

## Consulta rápida para agentes
`python scripts/research/query_evidence.py --module sdd --query "arc42-twelve-sections"`

## Palabras clave
`sdd, unitesis, evidencia, scientific-software, en`
