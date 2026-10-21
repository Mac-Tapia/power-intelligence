---
id: REF-082
title: "Integration of electric vehicles in a flexible electricity demand side management framework"
kind: tesis_doctoral
language: EN
primary_module: market
related_modules: ["market", "p2p", "op"]
source_url: "https://era.ed.ac.uk/items/dfcfda2a-8eb3-41df-9152-fd6214e554b3"
doi: null
verification: identificado_en_fuente_web
source_origin: web_2026-10-17
full_text_reviewed: false
accessed_date: '2026-10-17'
---
# REF-082 · Integration of electric vehicles in a flexible electricity demand side management framework

**Tipo:** tesis_doctoral · **Idioma:** EN · **Módulo principal:** [Mercado P2P y flexibilidad (simulado)](../modules/market.md).  
**Fuente primaria o registro:** https://era.ed.ac.uk/items/dfcfda2a-8eb3-41df-9152-fd6214e554b3  
**DOI (si se identificó):** pendiente / no aplica.  
**Estado epistemológico:** `identificado_en_fuente_web`. La ficha es síntesis de páginas/registros y/o referencia legada, **NO es el texto íntegro de la publicación**, ni confirma lectura exhaustiva de PDF.

## Pregunta técnica de UNITESIS que fundamenta
¿Cómo justificar el diseño de **Mercado P2P y flexibilidad (simulado)** mediante una referencia documentada, con resultados contrastables para el contexto de UNITESIS Power Intelligence?

## Aporte y aplicación concreta
Generar perfiles EV estocásticos y restricciones por nodo

**Regla de implementación propuesta (inferencia de ingeniería, no cita literal):** El clearing de ofertas no reemplaza factibilidad física ni permiso regulatorio.

**Componentes a los que se traslada:** `power-market, market-clearing`.

## Actividades para el agente
1. Recuperar de la URL la versión bibliográfica definitiva y comprobar autoría, año, DOI, tipo de publicación y disponibilidad legítima del texto completo.
2. Documentar metodología, tamaño de problema, hipótesis y datos de evaluación; señalar expresamente qué **NO** se valida en sistemas de distribución peruanos.
3. Convertir el aporte transferible en un ADR y tarea SDD con código trazable, fixtures reproducibles y análisis de alternativas.
4. Vincular a `specs/<feature>/research.md`, sin incorporar texto protegido por copyright ni simular que se ha reproducido el experimento.

## Prueba o evidencia exigida
Antes/después de trading con validación AC, pérdidas, cargos de red y cumplimiento de política.

## Límites y riesgos
Una tesis requiere reproducir datos y métodos; no equivale a norma ni certificación.
No usar esta ficha como prueba de que un modelo está entrenado, un conector conectado, un solver calibrado o una norma vigente.

## Consulta rápida para agentes
`python scripts/research/query_evidence.py --module market --query "integration-of-electric-vehicles-in-"`

## Palabras clave
`market, unitesis, evidencia, scientific-software, en`
