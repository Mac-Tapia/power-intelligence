---
id: REF-176
title: "React Flow"
kind: documentacion
language: EN
primary_module: fe
related_modules: ["fe", "qa", "gis"]
source_url: "https://reactflow.dev/"
doi: null
verification: importado_pendiente_auditoria
source_origin: importado_V2
full_text_reviewed: false
accessed_date: '2026-10-17'
---
# REF-176 · React Flow

**Tipo:** documentacion · **Idioma:** EN · **Módulo principal:** [Frontend, experiencia GIS y unifilar](../modules/fe.md).  
**Fuente primaria o registro:** https://reactflow.dev/  
**DOI (si se identificó):** pendiente / no aplica.  
**Estado epistemológico:** `importado_pendiente_auditoria`. La ficha es síntesis de páginas/registros y/o referencia legada, **NO es el texto íntegro de la publicación**, ni confirma lectura exhaustiva de PDF.

## Pregunta técnica de UNITESIS que fundamenta
¿Cómo justificar el diseño de **Frontend, experiencia GIS y unifilar** mediante una referencia documentada, con resultados contrastables para el contexto de UNITESIS Power Intelligence?

## Aporte y aplicación concreta
Fuente heredada para contraste de arquitectura/algoritmos del área «Frontend, experiencia GIS y unifilar»; evaluar si es directamente transferible al caso UNITESIS antes de asumirlo.

**Regla de implementación propuesta (inferencia de ingeniería, no cita literal):** Mantener estado servidor, UI y grafo visual independientes, unidos por IDs eléctricos inmutables.

**Componentes a los que se traslada:** `workstation-web, map-engine, one-line-engine`.

## Actividades para el agente
1. Recuperar de la URL la versión bibliográfica definitiva y comprobar autoría, año, DOI, tipo de publicación y disponibilidad legítima del texto completo.
2. Documentar metodología, tamaño de problema, hipótesis y datos de evaluación; señalar expresamente qué **NO** se valida en sistemas de distribución peruanos.
3. Convertir el aporte transferible en un ADR y tarea SDD con código trazable, fixtures reproducibles y análisis de alternativas.
4. Vincular a `specs/<feature>/research.md`, sin incorporar texto protegido por copyright ni simular que se ha reproducido el experimento.

## Prueba o evidencia exigida
Prueba E2E de selección de activo GIS→unifilar→detalle con snapshot consistente.

## Límites y riesgos
Es documentación de herramienta, no evidencia independiente de eficacia científica.
No usar esta ficha como prueba de que un modelo está entrenado, un conector conectado, un solver calibrado o una norma vigente.

## Consulta rápida para agentes
`python scripts/research/query_evidence.py --module fe --query "react-flow"`

## Palabras clave
`fe, unitesis, evidencia, scientific-software, en`
