---
id: REF-059
title: "Recent developments and challenges using blockchain techniques for peer-to-peer energy trading"
kind: articulo_revision
language: EN
primary_module: ledger
related_modules: ["ledger", "p2p", "bk"]
source_url: "https://doi.org/10.1016/j.rineng.2024.103666"
doi: "10.1016/j.rineng.2024.103666"
verification: identificado_en_fuente_web
source_origin: web_2026-10-17
full_text_reviewed: false
accessed_date: '2026-10-17'
---
# REF-059 · Recent developments and challenges using blockchain techniques for peer-to-peer energy trading

**Tipo:** articulo_revision · **Idioma:** EN · **Módulo principal:** [Blockchain permissioned y evidencia](../modules/ledger.md).  
**Fuente primaria o registro:** https://doi.org/10.1016/j.rineng.2024.103666  
**DOI (si se identificó):** 10.1016/j.rineng.2024.103666.  
**Estado epistemológico:** `identificado_en_fuente_web`. La ficha es síntesis de páginas/registros y/o referencia legada, **NO es el texto íntegro de la publicación**, ni confirma lectura exhaustiva de PDF.

## Pregunta técnica de UNITESIS que fundamenta
¿Cómo justificar el diseño de **Blockchain permissioned y evidencia** mediante una referencia documentada, con resultados contrastables para el contexto de UNITESIS Power Intelligence?

## Aporte y aplicación concreta
Medir privacidad, costos y riesgo de cadenas frente a base auditable tradicional

**Regla de implementación propuesta (inferencia de ingeniería, no cita literal):** Blockchain es opcional; se almacenan hashes y referencias, no mediciones ni planos sensibles.

**Componentes a los que se traslada:** `power-ledger, ledger-anchoring`.

## Actividades para el agente
1. Recuperar de la URL la versión bibliográfica definitiva y comprobar autoría, año, DOI, tipo de publicación y disponibilidad legítima del texto completo.
2. Documentar metodología, tamaño de problema, hipótesis y datos de evaluación; señalar expresamente qué **NO** se valida en sistemas de distribución peruanos.
3. Convertir el aporte transferible en un ADR y tarea SDD con código trazable, fixtures reproducibles y análisis de alternativas.
4. Vincular a `specs/<feature>/research.md`, sin incorporar texto protegido por copyright ni simular que se ha reproducido el experimento.

## Prueba o evidencia exigida
Ensayos contra falsificación, duplicidad, reorg y costo; comparación contra log firmado sin cadena.

## Límites y riesgos
Es una síntesis de literatura, no una prueba de desempeño del software.
No usar esta ficha como prueba de que un modelo está entrenado, un conector conectado, un solver calibrado o una norma vigente.

## Consulta rápida para agentes
`python scripts/research/query_evidence.py --module ledger --query "recent-developments-and-challenges-u"`

## Palabras clave
`ledger, unitesis, evidencia, scientific-software, en`
