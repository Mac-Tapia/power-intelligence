# Matriz verificable de requisitos PIDE (TDR 2018)

**No es copia ni transcripción del Anexo MINEM 2017.** Todos los ítems de esta matriz son atribuidos a [TDR Electro Puno 2018](https://www.electropuno.com.pe/web/archivos_ftp/201804041549_84.pdf), PDF 23 páginas. Las referencias a `§` son numerales del **TDR**.

| ID | Etapa | Referencia de origen | Requisito recuperado / delimitación | Módulo UNITESIS |
|---|---|---|---|---|
| PL-01 | historial | TDR §9.1.1, p4 | 10 años históricos desagregados por sector/mercado/tensión | `demand-historical` |
| PL-02 | proyeccion | TDR §9.1.1–9.1.2, pp4–6 | pronóstico vegetativo econométrico, nuevas cargas, escenarios exógenos, FC/FCP/FS | `demand-forecast` |
| PL-03 | geo | TDR §9.1.3, p6 | espacialización de demanda y mapas de densidad por cuadrículas; tamaños pendiente Anexo | `spatial-forecast` |
| PL-04 | diagnostico | TDR §9.2.1–9.2.3, pp7–8 | características, estado/seguridad, tensión, cargabilidad, pérdidas y calidad SAIDI/SAIFI | `baseline-diagnostic` |
| PL-05 | horizonte | TDR §9.3.1, p8 | 20 años, hitos 04/08/12/16/20: exclusivos TDR 2018 | `long-term-plan` |
| PL-06 | alternativas | TDR §9.3.1–9.3.2, pp8–9 | tres alternativas por sistema, factibilidad técnica; parámetro histórico | `candidate-alternatives` |
| PL-07 | rubros | TDR §9.3.2, pp8–9 | ampliación/reforzamiento, mejoramiento, remodelación, innovación/eficiencia, seguridad | `investment-category` |
| PL-08 | pre-economia | TDR §9.3.3, p9 | costos unitarios por kW, kWh, usuario, km; comprobación respecto proyectos comparables | `screening-costs` |
| PL-09 | cartera | TDR §10.1–10.2, pp11–12 | cartera cuatro años, años 04/05/06/07 referidos al ejemplo 2019–2023 | `portfolio-schedule` |
| PL-10 | tecnico | TDR §10.3, p13 | simular caída tensión, confiabilidad, cargabilidad por alternativa; descartar no factibles | `ac-study` |
| PL-11 | economia | TDR §10.4, pp13–14 | CI: materiales, armados, directos/indirectos; COyM; costos pérdidas de potencia y energía | `economic-model` |
| PL-12 | rubros-costos | TDR §10.4, p14 | LP/RP/refuerzo/protección/SED/BT-SP/BT-AP/luminarias/conexiones SER/total | `cost-breakdown` |
| PL-13 | rentabilidad | TDR §10.4, p14 | VAN, anualidad (CI+COyM+CP), TIR; 30 años vida útil en caso TDR; tasa LCE art 79 sin valor copiado | `npv-annuity-irr` |
| PL-14 | seleccion | TDR §10.5, p14 | priorizar alternativas factibles por recursos, restricciones y costos unitarios | `portfolio-optimization` |
| PL-15 | entregables | TDR §10.6–10.7, pp15–16 | fichas técnicas/económicas, unifilar A3 GIS, Gantt, formatos referidos 08–15 | `technical-dossier` |
| PL-16 | formatos | TDR §9 y 10, pp11 y16 | referencias a formatos 01–07 y 08–15; campos precisos no disponibles | `format-registry` |

## Controles de trazabilidad
- `source_id=ELECTRO_PUNO_TDR_2018`, `basis=historical_case_only` en cualquier evidencia o reporte.
- Toda regla normativa independiente (NTCSE, NTCSER, LCE, VAD) requiere perfil y versión específicos.
- Valores del escenario 20/4/30 años y tres alternativas no se trasladan automáticamente a otros escenarios.
- La documentación de los formatos F01–F15 es **índice de existencia**, no formulario digitalizado.
