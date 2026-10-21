---
id: REF-103
title: "Planejamento de redes de distribuição de energia elétrica de média e baixa tensão"
kind: tesis_doctoral
language: PT
primary_module: op
related_modules: ["op", "solver", "market"]
source_url: "https://repositorio.unesp.br/entities/publication/0e96e2cd-7287-4fae-9e88-4f2f11639529/full"
doi: null
verification: identificado_en_fuente_web
source_origin: web_2026-10-17
full_text_reviewed: false
accessed_date: '2026-10-17'
---
# REF-103 · Planejamento de redes de distribuição de energia elétrica de média e baixa tensão

**Tipo:** tesis_doctoral · **Idioma:** PT · **Módulo principal:** [Expansión, optimización y planificación](../modules/op.md).  
**Fuente primaria o registro:** https://repositorio.unesp.br/entities/publication/0e96e2cd-7287-4fae-9e88-4f2f11639529/full  
**DOI (si se identificó):** pendiente / no aplica.  
**Estado epistemológico:** `identificado_en_fuente_web`. La ficha es síntesis de páginas/registros y/o referencia legada, **NO es el texto íntegro de la publicación**, ni confirma lectura exhaustiva de PDF.

## Pregunta técnica de UNITESIS que fundamenta
¿Cómo justificar el diseño de **Expansión, optimización y planificación** mediante una referencia documentada, con resultados contrastables para el contexto de UNITESIS Power Intelligence?

## Aporte y aplicación concreta
UNESP tesis doctoral Cossi 2008: balance de fases, cantidad/ubicación de transformadores y trazado de redes BT

**Regla de implementación propuesta (inferencia de ingeniería, no cita literal):** Funciones objetivo CAPEX, OPEX, pérdidas, resiliencia, emisiones y riesgo con restricciones AC.

**Componentes a los que se traslada:** `power-optimization, power-market`.

## Actividades para el agente
1. Recuperar de la URL la versión bibliográfica definitiva y comprobar autoría, año, DOI, tipo de publicación y disponibilidad legítima del texto completo.
2. Documentar metodología, tamaño de problema, hipótesis y datos de evaluación; señalar expresamente qué **NO** se valida en sistemas de distribución peruanos.
3. Convertir el aporte transferible en un ADR y tarea SDD con código trazable, fixtures reproducibles y análisis de alternativas.
4. Vincular a `specs/<feature>/research.md`, sin incorporar texto protegido por copyright ni simular que se ha reproducido el experimento.

## Prueba o evidencia exigida
Comparar óptimo/pareto vs baseline; reproducir factibilidad N-1, no anticipatividad y costos.

## Límites y riesgos
Una tesis requiere reproducir datos y métodos; no equivale a norma ni certificación.
No usar esta ficha como prueba de que un modelo está entrenado, un conector conectado, un solver calibrado o una norma vigente.

## Consulta rápida para agentes
`python scripts/research/query_evidence.py --module op --query "planejamento-de-redes-de-distribuica"`

## Palabras clave
`op, unitesis, evidencia, scientific-software, pt`
