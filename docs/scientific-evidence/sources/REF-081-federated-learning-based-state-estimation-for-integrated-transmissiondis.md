---
id: REF-081
title: "Federated Learning-Based State Estimation for Integrated Transmission–Distribution Networks"
kind: tesis_maestria
language: EN
primary_module: p2p
related_modules: ["p2p", "ledger", "security"]
source_url: "https://repository.tudelft.nl/record/uuid%3A1df1dcc1-aa5f-431f-bc1e-b25ea765cb6f"
doi: null
verification: identificado_en_fuente_web
source_origin: web_2026-10-17
full_text_reviewed: false
accessed_date: '2026-10-17'
---
# REF-081 · Federated Learning-Based State Estimation for Integrated Transmission–Distribution Networks

**Tipo:** tesis_maestria · **Idioma:** EN · **Módulo principal:** [P2P federación segura](../modules/p2p.md).  
**Fuente primaria o registro:** https://repository.tudelft.nl/record/uuid%3A1df1dcc1-aa5f-431f-bc1e-b25ea765cb6f  
**DOI (si se identificó):** pendiente / no aplica.  
**Estado epistemológico:** `identificado_en_fuente_web`. La ficha es síntesis de páginas/registros y/o referencia legada, **NO es el texto íntegro de la publicación**, ni confirma lectura exhaustiva de PDF.

## Pregunta técnica de UNITESIS que fundamenta
¿Cómo justificar el diseño de **P2P federación segura** mediante una referencia documentada, con resultados contrastables para el contexto de UNITESIS Power Intelligence?

## Aporte y aplicación concreta
Probar agregación federada preservando datos locales y separación operador/tenant

**Regla de implementación propuesta (inferencia de ingeniería, no cita literal):** Usar peers autenticados para replicar resúmenes/evidencias; la red P2P no controla interruptores reales.

**Componentes a los que se traslada:** `power-p2p, p2p-sync`.

## Actividades para el agente
1. Recuperar de la URL la versión bibliográfica definitiva y comprobar autoría, año, DOI, tipo de publicación y disponibilidad legítima del texto completo.
2. Documentar metodología, tamaño de problema, hipótesis y datos de evaluación; señalar expresamente qué **NO** se valida en sistemas de distribución peruanos.
3. Convertir el aporte transferible en un ADR y tarea SDD con código trazable, fixtures reproducibles y análisis de alternativas.
4. Vincular a `specs/<feature>/research.md`, sin incorporar texto protegido por copyright ni simular que se ha reproducido el experimento.

## Prueba o evidencia exigida
Prueba de peer malicioso, replay, partición de red, aislamiento de empresa y sincronización.

## Límites y riesgos
Los resultados pueden tener alcance limitado a redes y hardware de estudio.
No usar esta ficha como prueba de que un modelo está entrenado, un conector conectado, un solver calibrado o una norma vigente.

## Consulta rápida para agentes
`python scripts/research/query_evidence.py --module p2p --query "federated-learning-based-state-estim"`

## Palabras clave
`p2p, unitesis, evidencia, scientific-software, en`
