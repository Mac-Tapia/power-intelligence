---
id: REF-116
title: "ENTSO-E CGMES Library (2026)"
kind: norma_o_estandar
language: EN
primary_module: gis
related_modules: ["gis", "graph", "bk"]
source_url: "https://www.entsoe.eu/data/cim/cim-for-grid-models-exchange/"
doi: null
verification: importado_pendiente_auditoria
source_origin: importado_V2
full_text_reviewed: false
accessed_date: '2026-10-17'
---
# REF-116 · ENTSO-E CGMES Library (2026)

**Tipo:** norma_o_estandar · **Idioma:** EN · **Módulo principal:** [GIS, adquisición y topología de redes](../modules/gis.md).  
**Fuente primaria o registro:** https://www.entsoe.eu/data/cim/cim-for-grid-models-exchange/  
**DOI (si se identificó):** pendiente / no aplica.  
**Estado epistemológico:** `importado_pendiente_auditoria`. La ficha es síntesis de páginas/registros y/o referencia legada, **NO es el texto íntegro de la publicación**, ni confirma lectura exhaustiva de PDF.

## Pregunta técnica de UNITESIS que fundamenta
¿Cómo justificar el diseño de **GIS, adquisición y topología de redes** mediante una referencia documentada, con resultados contrastables para el contexto de UNITESIS Power Intelligence?

## Aporte y aplicación concreta
Fuente heredada para contraste de arquitectura/algoritmos del área «GIS, adquisición y topología de redes»; evaluar si es directamente transferible al caso UNITESIS antes de asumirlo.

**Regla de implementación propuesta (inferencia de ingeniería, no cita literal):** La cartografía, conectividad terminal-fase y layout del unifilar requieren modelos diferentes.

**Componentes a los que se traslada:** `ingestion, topology, PostGIS`.

## Actividades para el agente
1. Recuperar de la URL la versión bibliográfica definitiva y comprobar autoría, año, DOI, tipo de publicación y disponibilidad legítima del texto completo.
2. Documentar metodología, tamaño de problema, hipótesis y datos de evaluación; señalar expresamente qué **NO** se valida en sistemas de distribución peruanos.
3. Convertir el aporte transferible en un ADR y tarea SDD con código trazable, fixtures reproducibles y análisis de alternativas.
4. Vincular a `specs/<feature>/research.md`, sin incorporar texto protegido por copyright ni simular que se ha reproducido el experimento.

## Prueba o evidencia exigida
Fixtures con nodos huérfanos, tramos invertidos, CRS incorrecto, bifásicos y switches abiertos.

## Límites y riesgos
Confirmar edición, país, vigencia, licencia y sección aplicable al estudio.
No usar esta ficha como prueba de que un modelo está entrenado, un conector conectado, un solver calibrado o una norma vigente.

## Consulta rápida para agentes
`python scripts/research/query_evidence.py --module gis --query "entso-e-cgmes-library-2026"`

## Palabras clave
`gis, unitesis, evidencia, scientific-software, en`
