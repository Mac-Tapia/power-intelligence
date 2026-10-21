# UNITESIS V8 — Centro normativo técnico-económico

> Estado 17-10-2026: diseño e implementación parcial de funciones puras; no constituye un validador legal completo ni un estudio aprobado.

## Delimitación obligatoria
1. **PIT SST/SCT** Resolución 217-2013-OS/CD, normas concordantes y modificatorias, PIT 2025–2029, Área de Demanda. La resolución original regula transmisión, **no equivale a la metodología PIDE**.
2. **PIDE FONAFE** D.Leg. 1208, DS 023-2016-EM, Anexo B.1.2 de Res. 080-2012-OS/CD incorporado con Res. 264-2016-OS/CD. El anexo fija procedimiento; criterios sustantivos son otra pieza. **RM 428-2017-MEM/DM solo publica proyecto**; Informe Legal 628-2025-GRT refiere no aprobación al 22-08-2025. Estado legal posterior NO confirmado. El solicitado «Anexo 1» sustantivo no fue verificado a texto completo: requerir PDF oficial antes de codificar umbrales.
3. **PMBOK 6** es metodología de gestión de proyectos, no norma eléctrica ni marco normativo de Osinergmin. Aplicación adaptada; no reproduce contenido protegido ni implica certificación PMI.

## Metodología PIT identificada en norma original (con reserva de modificaciones)
- Art. 6 y 8: proyección regulada, datos 15-min, FC/FCP, econometría, 30 años proyección (núm. 6.2.1), desagregación espacial 1 km² y F-101/102/103/104/105/113/123.
- Art. 10: alternativas de tensión, transformación y conductores; eficiencia y calidad, horizonte de obras 4 años.
- Art. 11.3: mínimo valor presente **inversión + operación + mantenimiento + pérdidas físicas valorizadas** con horizonte evaluación 10 años; condiciones específicas de pérdida incremental y año base se verifican en el texto oficial.
- Art. 12: calidad NTCSE; capacidad, equipos y reglas particulares. **12.3 modificado en 2018**, no fijar N-1 sin consolidación.
- Art. 5.7 y Título IV: anexos y formatos regulatorios; los modelos internos NO reemplazan archivos regulatorios oficiales.

## Regla de optimización
Una alternativa no puede ganar solo por costo si es técnicamente inviable. Para PIT aplicar filtro de restricciones regulatorias y técnicas según artículos vigentes, luego minimizar VP de costos conforme norma. Para estudio interno de distribución puede usar Pareto CAPEX/OPEX/pérdidas/calidad/ENS si se define política: no etiquetar como decisión PIDE aprobada.

## Versiones
- `config/regulations/profiles/`: estudios separados SST/SCT, PIT 2025–2029 y PIDE interno/draft.
- `docs/regulatory/SOURCES.json`: fuentes y sus clases.
- `config/studies/catalog.json`: catálogo técnico/económico.
- `config/regulations/alternatives.json`: hipótesis de solución, **no lista de obligaciones regulatorias**.

## Criterios de gate regulatorio
- G0 eligibilidad entidad/área/red/periodo.
- G1 vigencia: norm + modificatorias consolidada, aprobada por revisor jurídico.
- G2 completitud: fuentes de demanda, topología GIS, costos, parámetros y fecha.
- G3 ensayo eléctrico: comparación independiente y tolerancias declaradas.
- G4 alternativas mínimas: sin proyecto y opciones pertinentes documentadas; descartar inviables.
- G5 evaluación VP con moneda, año base, tasa y módulos con fuente autorizada.
- G6 PMBOK: trazabilidad de Charter/WBS/Cronograma/Riesgos/Costos.
- G7 expediente y formatos; firma/segregación de roles, sin aprobación automática.

## Fuentes
Ver `SOURCES.json`; para PIDE consultar específicamente informe legal 628-2025-GRT y R. 264-2016. Un link de borrador no demuestra vigencia.

- [Anexo B.1.2 - procedimiento FONAFE](PIDE-ANNEX-B1.2-PROCEDURE.md)

### PIDE 2017 — V8.2
[Auditoría del Anexo pendiente y matriz TDR verificable](pide_2017/INDEX.md). No confundir TDR Electro Puno con el texto normativo oficial.
