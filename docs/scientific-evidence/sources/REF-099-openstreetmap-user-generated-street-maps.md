---
id: REF-099
title: "OpenStreetMap: User-Generated Street Maps"
kind: articulo_revista
language: EN
primary_module: gis
related_modules: ["gis", "graph", "bk"]
source_url: "https://doi.org/10.1109/MPRV.2008.80"
doi: "10.1109/MPRV.2008.80"
verification: identificado_en_fuente_web
source_origin: web_2026-10-17
full_text_reviewed: false
accessed_date: '2026-10-17'
---
# REF-099 · OpenStreetMap: User-Generated Street Maps

**Tipo:** articulo_revista · **Idioma:** EN · **Módulo principal:** [GIS, adquisición y topología de redes](../modules/gis.md).  
**Fuente primaria o registro:** https://doi.org/10.1109/MPRV.2008.80  
**DOI (si se identificó):** 10.1109/MPRV.2008.80.  
**Estado epistemológico:** `identificado_en_fuente_web`. La ficha es síntesis de páginas/registros y/o referencia legada, **NO es el texto íntegro de la publicación**, ni confirma lectura exhaustiva de PDF.

## Pregunta técnica de UNITESIS que fundamenta
¿Cómo justificar el diseño de **GIS, adquisición y topología de redes** mediante una referencia documentada, con resultados contrastables para el contexto de UNITESIS Power Intelligence?

## Aporte y aplicación concreta
Proveniencia, licencias y control de exactitud en mapas de fondo

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
Las métricas y supuestos del artículo no se transfieren automáticamente a redes GIS del Perú.
No usar esta ficha como prueba de que un modelo está entrenado, un conector conectado, un solver calibrado o una norma vigente.

## Consulta rápida para agentes
`python scripts/research/query_evidence.py --module gis --query "openstreetmap-user-generated-street-"`

## Palabras clave
`gis, unitesis, evidencia, scientific-software, en`
