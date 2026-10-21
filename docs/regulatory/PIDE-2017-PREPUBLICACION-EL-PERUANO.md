# PIDE — Prepublicación oficial (19/10/2017) y aplicación metodológica

## Identificación y jerarquía de fuentes
- **Primaria normativa**: Resolución Ministerial N.° 428-2017-MEM/DM, diario oficial El Peruano, 19/10/2017. **Autoriza publicar** el proyecto de resolución que aprobaría «Criterios y Metodología de Planificación para la Elaboración del Plan de Inversión en Distribución Eléctrica (PIDE)». https://busquedas.elperuano.pe/dispositivo/NL/1577466-1
- **Catálogo MINEM**: aparece bajo **Pre Publicaciones Electricidad**. https://www.gob.pe/institucion/minem/colecciones/25457-pre-publicaciones-electricidad?sheet=2
- **Marco principal**: Decreto Legislativo N.° 1208, D.S. N.° 023-2016-EM, D.S. N.° 027-2018-EM, D.S. N.° 028-2021-EM. Procedimiento Anexo B.1.2 de Resolución 080-2012-OS/CD, incorporado por Resolución 264-2016-OS/CD.
- **Estado sustentado**: Informe Legal N.° 628-2025-GRT, Osinergmin, relata que en julio de 2025 persistía la falta de aprobación de criterios y metodología sustantivos. https://www.osinergmin.gob.pe/Resoluciones/pdf/2025/Informe-Legal-628-2025-GRT.pdf
- **2026**: no se ha acreditado en esta investigación una aprobación posterior con su resolución y anexo íntegro. No afirmar imposibilidad absoluta ni aprobación.

## Diferencias normativas (bloqueo obligatorio)
| Perfil | Objetivo | Naturaleza | Alcance |
|---|---|---|---|
| PIT SST/SCT | Expansión de transmisión | R. 217-2013-OS/CD + modificatorias | Sistemas de transmisión y áreas de demanda |
| PIDE FONAFE | Plan de inversión de distribución asociado a VAD | DL 1208 y reglamento; procedimiento B.1.2, proyecto de criterios 2017 | Distribuidoras bajo FONAFE sujetas al régimen |
| Planificación distribución interna | Estudios técnico-económicos corporativos | Metodología inspirada en borrador, doctrina y normas técnicas aplicables | Empresas públicas y privadas, sin certificación PIDE |

**No trasladar automáticamente la obligación PIDE DL1208 a distribuidoras privadas**. Ej.: Electro Dunas puede adoptar este flujo como práctica de planificación, pero no autoproclamarse sujeto al expediente FONAFE. El acrónimo PIDE aquí NO es la Plataforma de Interoperabilidad del Estado.

## Flujo metodológico de referencia basado en documentos sectoriales históricos (NO transcripción del Anexo 1)
Fuente operativa de referencia: TDR Electro Puno 2018 https://www.electropuno.com.pe/web/archivos_ftp/201804041549_84.pdf ; además bases ADINELSA 2018 y tesis UNI (referencias en SOURCES.json). Son insumos históricos y académicos **no equivalentes a una norma aprobada**.

**Etapa A — Planeamiento de largo plazo** (20 años: valor histórico empleado por TDR Electro Puno, parametrizable):
1. Delimitar ámbito, inventario, topología GIS/VNR-GIS, calidad de datos, catálogos de equipos y costos.
2. Análisis del mercado: evolución comercial, demanda vegetativa y emergente, factores de coincidencia, proyección por alimentador y distribución espacial.
3. Diagnóstico base: tensión, cargabilidad, pérdidas, confiabilidad, continuidad y estado de red; escenarios horarios/estacionales.
4. Formular alternativas de expansión y reforzamiento: redistribución/transferencia, repotenciación de MT/BT, nueva SED, nuevos alimentadores, automatización, DER/BESS/EV cuando procede.
5. Viabilidad técnica de alternativas con simulador independiente; entregar portafolio de opciones trazables.

**Etapa B — Cartera de inversiones de corto plazo** (cuatro años: valor histórico de TDR y VAD del caso, NO suponer universal):
6. Formular variantes por año y segmento, registrar compatibilidad con modelo eficiente y restricciones técnicas.
7. Evaluar cada alternativa: caída de tensión, niveles de carga, fiabilidad, demanda y pérdidas.
8. Calcular inversión, O&M, pérdidas y valor presente/beneficio-costo usando fuente de precios, tasa y horizonte declarados; no imputar tasas del PIT.
9. Selección/ordenamiento por factibilidad y criterio económico explícito, con incertidumbre y sensibilidad; toda decisión necesita revisión humana.
10. Emitir ficha técnica, ficha económica, presupuesto, metrados, diagrama unifilar GIS antes/después, Gantt, riesgos, responsables y plan PMBOK6; conservar los archivos de cálculo.

**Anexos y formatos**: Los TDR de 2018 describen formatos 01–07 (planeamiento) y 08–15 (PIDE), pero el **contenido exacto, campo por campo, del anexo sustantivo oficial no se recuperó**. Los formularios UNITESIS serán plantillas internas hasta tener el anexo y revisión de abogado especialista. No inventar campos regulatorios.

## Casos y pruebas obligatorias
- Escenario sin proyecto, demanda base vs. proyección, alternativas independientes, solución seleccionada y contingencias cuando corresponde.
- Pruebas de importación GIS, conectividad, cambio topológico controlado, validación de parámetros físicos, restricciones de tensión/cargabilidad, reconciliación de costos y trazabilidad.
- Casos negativos: perfil borrador nunca permite estado `normatively_approved`; sin fuente o parámetros bloquea reporte oficial.
- Etiquetado por modo: `pide_methodological_reference`, `pide_fonafe_procedure`, `distribution_internal`.
- Cada proyecto: charter, WBS/EDT, cronograma, CAPEX/OPEX, matriz de riesgos y aprobaciones PMBOK 6.

## Trabajo pendiente y control de fuentes
1. Descargar desde el MINEM la **versión completa del proyecto de criterios y sus anexos** para extraer íntegramente formatos/métodos.
2. Buscar resolución de **aprobación definitiva posterior a julio de 2025**; si se identifica, comparar artículo por artículo y versionar desde su vigencia.
3. Auditoría técnico-jurídica por empresa, periodo y régimen.
4. Mantener expediente de evidencia, versión y hash del documento real descargado. No inferir hash de una URL.
