---
id: REF-021
title: "Mitigating the risk of prompt injections in browser use"
kind: guia_tecnica
language: EN
primary_module: security
related_modules: ["security", "sdd", "ops"]
source_url: "https://www.anthropic.com/research/prompt-injection-defenses"
doi: null
verification: identificado_en_fuente_web
source_origin: web_2026-10-17
full_text_reviewed: false
accessed_date: '2026-10-17'
---
# REF-021 · Mitigating the risk of prompt injections in browser use

**Tipo:** guia_tecnica · **Idioma:** EN · **Módulo principal:** [Seguridad, gobierno y control de agentes](../modules/security.md).  
**Fuente primaria o registro:** https://www.anthropic.com/research/prompt-injection-defenses  
**DOI (si se identificó):** pendiente / no aplica.  
**Estado epistemológico:** `identificado_en_fuente_web`. La ficha es síntesis de páginas/registros y/o referencia legada, **NO es el texto íntegro de la publicación**, ni confirma lectura exhaustiva de PDF.

## Pregunta técnica de UNITESIS que fundamenta
¿Cómo justificar el diseño de **Seguridad, gobierno y control de agentes** mediante una referencia documentada, con resultados contrastables para el contexto de UNITESIS Power Intelligence?

## Aporte y aplicación concreta
Tratar documentos y resultados MCP como entrada no confiable

**Regla de implementación propuesta (inferencia de ingeniería, no cita literal):** Permiso mínimo, RBAC/ABAC, secrets fuera de repositorio, auditoría y entornos con aislamiento.

**Componentes a los que se traslada:** `connectors, identity, audits`.

## Actividades para el agente
1. Recuperar de la URL la versión bibliográfica definitiva y comprobar autoría, año, DOI, tipo de publicación y disponibilidad legítima del texto completo.
2. Documentar metodología, tamaño de problema, hipótesis y datos de evaluación; señalar expresamente qué **NO** se valida en sistemas de distribución peruanos.
3. Convertir el aporte transferible en un ADR y tarea SDD con código trazable, fixtures reproducibles y análisis de alternativas.
4. Vincular a `specs/<feature>/research.md`, sin incorporar texto protegido por copyright ni simular que se ha reproducido el experimento.

## Prueba o evidencia exigida
Pentest focalizado: MCP prompt injection, SSRF, escalada de privilegios y fuga entre tenants.

## Límites y riesgos
Es guía de ingeniería, no experimento científico arbitrado.
No usar esta ficha como prueba de que un modelo está entrenado, un conector conectado, un solver calibrado o una norma vigente.

## Consulta rápida para agentes
`python scripts/research/query_evidence.py --module security --query "mitigating-the-risk-of-prompt-inject"`

## Palabras clave
`security, unitesis, evidencia, scientific-software, en`
