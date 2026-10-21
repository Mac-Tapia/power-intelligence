---
id: REF-126
title: "Multi-agent BESS collaborative control, Applied Energy (2024)"
kind: articulo_o_preprint
language: EN
primary_module: marl
related_modules: ["marl", "sciml", "op"]
source_url: "https://doi.org/10.1016/j.apenergy.2024.123858"
doi: "10.1016/j.apenergy.2024.123858"
verification: importado_pendiente_auditoria
source_origin: importado_V2
full_text_reviewed: false
accessed_date: '2026-10-17'
---
# REF-126 · Multi-agent BESS collaborative control, Applied Energy (2024)

**Tipo:** articulo_o_preprint · **Idioma:** EN · **Módulo principal:** [MADRL seguro y critic centralizado](../modules/marl.md).  
**Fuente primaria o registro:** https://doi.org/10.1016/j.apenergy.2024.123858  
**DOI (si se identificó):** 10.1016/j.apenergy.2024.123858.  
**Estado epistemológico:** `importado_pendiente_auditoria`. La ficha es síntesis de páginas/registros y/o referencia legada, **NO es el texto íntegro de la publicación**, ni confirma lectura exhaustiva de PDF.

## Pregunta técnica de UNITESIS que fundamenta
¿Cómo justificar el diseño de **MADRL seguro y critic centralizado** mediante una referencia documentada, con resultados contrastables para el contexto de UNITESIS Power Intelligence?

## Aporte y aplicación concreta
Fuente heredada para contraste de arquitectura/algoritmos del área «MADRL seguro y critic centralizado»; evaluar si es directamente transferible al caso UNITESIS antes de asumirlo.

**Regla de implementación propuesta (inferencia de ingeniería, no cita literal):** Entrenar en gemelo digital sandbox con restricciones duras del simulador y comparadores deterministas.

**Componentes a los que se traslada:** `power-marl, agent-runtime`.

## Actividades para el agente
1. Recuperar de la URL la versión bibliográfica definitiva y comprobar autoría, año, DOI, tipo de publicación y disponibilidad legítima del texto completo.
2. Documentar metodología, tamaño de problema, hipótesis y datos de evaluación; señalar expresamente qué **NO** se valida en sistemas de distribución peruanos.
3. Convertir el aporte transferible en un ADR y tarea SDD con código trazable, fixtures reproducibles y análisis de alternativas.
4. Vincular a `specs/<feature>/research.md`, sin incorporar texto protegido por copyright ni simular que se ha reproducido el experimento.

## Prueba o evidencia exigida
Curva de aprendizaje, generalización, tasa de violación física y recuperación tras fallos.

## Límites y riesgos
Verificar metadatos, supuestos y aplicabilidad; no sobreinterpretar título o resumen.
No usar esta ficha como prueba de que un modelo está entrenado, un conector conectado, un solver calibrado o una norma vigente.

## Consulta rápida para agentes
`python scripts/research/query_evidence.py --module marl --query "multi-agent-bess-collaborative-contr"`

## Palabras clave
`marl, unitesis, evidencia, scientific-software, en`
