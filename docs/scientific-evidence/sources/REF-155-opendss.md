---
id: REF-155
title: "OpenDSS"
kind: documentacion
language: EN
primary_module: solver
related_modules: ["solver", "qa", "gis"]
source_url: "https://opendss.epri.com/"
doi: null
verification: importado_pendiente_auditoria
source_origin: importado_V2
full_text_reviewed: false
accessed_date: '2026-10-17'
---
# REF-155 · OpenDSS

**Tipo:** documentacion · **Idioma:** EN · **Módulo principal:** [Estudios eléctricos verificables](../modules/solver.md).  
**Fuente primaria o registro:** https://opendss.epri.com/  
**DOI (si se identificó):** pendiente / no aplica.  
**Estado epistemológico:** `importado_pendiente_auditoria`. La ficha es síntesis de páginas/registros y/o referencia legada, **NO es el texto íntegro de la publicación**, ni confirma lectura exhaustiva de PDF.

## Pregunta técnica de UNITESIS que fundamenta
¿Cómo justificar el diseño de **Estudios eléctricos verificables** mediante una referencia documentada, con resultados contrastables para el contexto de UNITESIS Power Intelligence?

## Aporte y aplicación concreta
Fuente heredada para contraste de arquitectura/algoritmos del área «Estudios eléctricos verificables»; evaluar si es directamente transferible al caso UNITESIS antes de asumirlo.

**Regla de implementación propuesta (inferencia de ingeniería, no cita literal):** Separar AC equilibrado, trifásico desequilibrado, cortocircuito y dinámica; cada resultado registra solver y tolerancias.

**Componentes a los que se traslada:** `power-simulation, PowerFlowPort`.

## Actividades para el agente
1. Recuperar de la URL la versión bibliográfica definitiva y comprobar autoría, año, DOI, tipo de publicación y disponibilidad legítima del texto completo.
2. Documentar metodología, tamaño de problema, hipótesis y datos de evaluación; señalar expresamente qué **NO** se valida en sistemas de distribución peruanos.
3. Convertir el aporte transferible en un ADR y tarea SDD con código trazable, fixtures reproducibles y análisis de alternativas.
4. Vincular a `specs/<feature>/research.md`, sin incorporar texto protegido por copyright ni simular que se ha reproducido el experimento.

## Prueba o evidencia exigida
Comparar IEEE 13/34/123 y otros casos disponibles, magnitudes, ángulos, pérdidas, KCL, convergencia.

## Límites y riesgos
Es documentación de herramienta, no evidencia independiente de eficacia científica.
No usar esta ficha como prueba de que un modelo está entrenado, un conector conectado, un solver calibrado o una norma vigente.

## Consulta rápida para agentes
`python scripts/research/query_evidence.py --module solver --query "opendss"`

## Palabras clave
`solver, unitesis, evidencia, scientific-software, en`
