---
id: REF-129
title: "Designing an optimal microgrid control system using DRL: review (2024)"
kind: articulo_o_preprint
language: EN
primary_module: arch
related_modules: ["arch", "sdd", "ops"]
source_url: "https://doi.org/10.1016/j.jestch.2024.101651"
doi: "10.1016/j.jestch.2024.101651"
verification: importado_pendiente_auditoria
source_origin: importado_V2
full_text_reviewed: false
accessed_date: '2026-10-17'
---
# REF-129 · Designing an optimal microgrid control system using DRL: review (2024)

**Tipo:** articulo_o_preprint · **Idioma:** EN · **Módulo principal:** [Arquitectura empresarial y plataforma](../modules/arch.md).  
**Fuente primaria o registro:** https://doi.org/10.1016/j.jestch.2024.101651  
**DOI (si se identificó):** 10.1016/j.jestch.2024.101651.  
**Estado epistemológico:** `importado_pendiente_auditoria`. La ficha es síntesis de páginas/registros y/o referencia legada, **NO es el texto íntegro de la publicación**, ni confirma lectura exhaustiva de PDF.

## Pregunta técnica de UNITESIS que fundamenta
¿Cómo justificar el diseño de **Arquitectura empresarial y plataforma** mediante una referencia documentada, con resultados contrastables para el contexto de UNITESIS Power Intelligence?

## Aporte y aplicación concreta
Fuente heredada para contraste de arquitectura/algoritmos del área «Arquitectura empresarial y plataforma»; evaluar si es directamente transferible al caso UNITESIS antes de asumirlo.

**Regla de implementación propuesta (inferencia de ingeniería, no cita literal):** La solución conserva un monolito modular con workers; medir acoplamiento, latencia y fallas antes de extraer servicios.

**Componentes a los que se traslada:** `control-api, application, workers`.

## Actividades para el agente
1. Recuperar de la URL la versión bibliográfica definitiva y comprobar autoría, año, DOI, tipo de publicación y disponibilidad legítima del texto completo.
2. Documentar metodología, tamaño de problema, hipótesis y datos de evaluación; señalar expresamente qué **NO** se valida en sistemas de distribución peruanos.
3. Convertir el aporte transferible en un ADR y tarea SDD con código trazable, fixtures reproducibles y análisis de alternativas.
4. Vincular a `specs/<feature>/research.md`, sin incorporar texto protegido por copyright ni simular que se ha reproducido el experimento.

## Prueba o evidencia exigida
Arquitectura C4 y ADR con contract tests y simulación de fallos de worker.

## Límites y riesgos
Verificar metadatos, supuestos y aplicabilidad; no sobreinterpretar título o resumen.
No usar esta ficha como prueba de que un modelo está entrenado, un conector conectado, un solver calibrado o una norma vigente.

## Consulta rápida para agentes
`python scripts/research/query_evidence.py --module arch --query "designing-an-optimal-microgrid-contr"`

## Palabras clave
`arch, unitesis, evidencia, scientific-software, en`
