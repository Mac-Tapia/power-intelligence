# Plan de implementación V8.2 — planificación de distribución basada en evidencia

## Fases con criterios de aceptación
1. **R0 Base documental**: vincular RM, catálogo, TDR e informe legal por URL y año; capturar estado `original_annex_pending`; prueba de fuente sin hash inventado.
2. **R1 Dataset/catálogo**: 10 años históricos solo si TDR-case, demanda vegetativa y nuevas cargas, FC/FCP/FS y red GIS; auditar fuentes/faltantes.
3. **R2 Modelo espacial + red**: georreferenciar puntos de carga, validar conectividad terminal/fase y estado eléctrico, graficar densidades sin imponer tamaño de celda no verificado.
4. **R3 Diagnóstico**: flujo AC con solver independiente y calidad SAIDI/SAIFI; test benchmarks y series temporales.
5. **R4 Alternativas**: tres candidatas independientes si modo histórico, hitos 4/8/12/16/20; costos unitarios preliminares y descarte de inviabilidad.
6. **R5 Cartera**: seleccionar años y presupuesto mediante optimización multiobjetivo; no mezclar escenarios técnicos sin proyecto.
7. **R6 Economía**: CI/COyM/CP desagregados por rubro, VAN, TIR y anualidad. Las tasas requieren fuente y revisión para no calcular resultados reglamentarios ficticios.
8. **R7 Evidencias y PMBOK 6**: ficha técnica, económica, diagrama GIS A3, Gantt, charter, EDT, presupuesto, riesgos, actas, responsables y criterios de aprobación.
9. **R8 Reconstrucción exacta Anexo 1** (bloqueada): cuando el MINEM original se obtenga, extraer 01–15 formato por formato (campos, unidades, validaciones, secciones), efectuar diff y versionar.

## Arquitectura de implementación
- `config/regulations/pide_tdr_2018_trace.json`: única fuente de números del TDR.
- `config/regulations/pide_formats_original_pending.json`: 15 formatos reservados, no utilizables como export oficial.
- `packages/python/power-regulation/src/unitesis_regulation/pide_reference.py`: evaluador de integridad y anualidad **solo ilustrativa**.
- `scripts/pide/evaluate_reference.py`: CLI de evaluación; nunca certifica.
- `scripts/pide/register_source.py`: registro local de fuente sin PDF en control de versiones.
- `tests/bootstrap/test_pide_reference_v82.py`: tests de límites de aprobación y tasas.
- `specs/027-pide-source-audit-and-reference-engine`: SDD para los agentes.

## PMBOK 6 por alternativa seleccionada
Inicio: Acta de constitución + interesados. Planificación: EDT/WBS, cronograma, presupuesto, línea base, calidad, recursos, comunicación, riesgos, adquisiciones, interesados. Ejecución: resultados ingeniería y contrataciones. Seguimiento y control: informes desempeño, cambios y trazabilidad normativa. Cierre: aceptación del entregable y lecciones aprendidas. Es aplicación metodológica, no reproducción del libro PMI.

## Definición de completado
- Módulo documental y calculadora referencial pasan pruebas unitarias y controles de origen.
- Los estudios GIS/flujos/economía de datos reales requieren ejecución e integración adicionales.
- Los formatos originales y la aprobación del texto MINEM se mantienen pendientes mientras no se recupere el Anexo.
