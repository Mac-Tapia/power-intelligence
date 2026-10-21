# Auditoría de documento base PIDE 2017 y referencias

**Fecha de revisión:** 17-10-2026  
**Resultado honesto:** se verificó el acto de *prepublicación* y se examinó a texto completo un TDR histórico de 23 páginas de Electro Puno; **NO se recuperó el PDF íntegro del Anexo metodológico del MINEM**. No se puede afirmar revisión artículo por artículo ni digitalización de sus formatos originales.

## Evidencia y jerarquía

| ID | Fuente | Alcance recuperado | ¿Sirve para declarar obligación? |
|---|---|---|---|
| RM_428_2017 | [El Peruano](https://busquedas.elperuano.pe/dispositivo/NL/1577466-1), 19/10/2017 | Autorización de publicación del proyecto y exposición de motivos; proyecto NO aprobado por este acto | NO |
| MINEM_CATALOG_2017 | [Catálogo de prepublicaciones](https://www.gob.pe/institucion/minem/colecciones/25457-pre-publicaciones-electricidad?sheet=2) | Registro ministerial del proyecto; adjunto no accesible para descarga | NO |
| ELECTRO_PUNO_TDR_2018 | [TDR Electro Puno 2018, 23 pp.](https://www.electropuno.com.pe/web/archivos_ftp/201804041549_84.pdf) | Textos completos 7–10, horizontes, estudios y formatos citados | NO, es contrato histórico |
| ADINELSA_BASES_2018 | [Bases ADINELSA](https://www.adinelsa.com.pe/files/adinelsaweb/Licitaciones_Procesos/AS-SM-36-2018-ADINELSA-1/BASES_INTEGRADAS_PIDE_20181122_182003_613.pdf) | Referencia de contratación histórica | NO |
| OSINERGMIN_LEGAL_628_2025 | [Informe 628-2025](https://www.osinergmin.gob.pe/Resoluciones/pdf/2025/Informe-Legal-628-2025-GRT.pdf) | Señala que no existía aprobación de metodología a la fecha del informe | Informe sobre estado hasta su fecha |
| DS_028_2021 | [Decreto 028-2021](https://cdn.www.gob.pe/uploads/document/file/3242050/DS%20N%C2%B0%20028-2021-MINEM-EM.pdf.pdf) | Difirió aprobación del instrumento | Sí en su ámbito/periodo, verificar modificaciones |
| REG_PROCEDURE_B12 | [Res. 264-2016-OS/CD](https://www.osinergmin.gob.pe/Resoluciones/pdf/2016/Osinergmin-264-2016-OS-CD.pdf) | Procedimiento para PIDE FONAFE; independiente de criterios sustantivos | Sujeta a versión y aplicación |

## Lo que sí sustenta Electro Puno (NO inferir que el Anexo impone exactamente lo mismo)

- Numeral 9.1: análisis histórico y mercado; proyecciones vegetativa/extra-tendencial; geografía de la carga. **10 años históricos** y **20 años a proyectar**, específicos TDR p.4–6.
- Numeral 9.2: diagnóstico físico y operativo; tensión, cargabilidad, pérdidas y continuidad. TDR p.7–8.
- Numeral 9.3: tres alternativas por sistema, hitos 4/8/12/16/20, rubros de inversión y evaluación preliminar. TDR p.8–10.
- Numeral 10: cartera para 4 años del caso histórico; años relativos 04–07; pruebas técnicas, CI/COyM/CP, VAN/TIR/anualidad; **vida útil de 30 años y tasa remitida al artículo 79 LCE**, sin inventar cifra vigente. TDR pp.11–16.
- Numerales 9–10: menciones explícitas de formatos N.° 01–07 (estudio largo plazo) y N.° 08–15 (cartera). **Sus campos y matrices oficiales no aparecen en la fuente revisada**.
- Diferenciar reporte e insumos GIS/flujo de carga de un expediente regulatorio **aprobado**; no tomar TDR de Electro Puno como fuente normativa de Electro Dunas.

## Bloqueadores documentales que siguen abiertos

1. Localizar archivo original del proyecto MINEM y su exposición de motivos, relacionado con RM 428-2017-MEM/DM (Anexo 1). **Sin el PDF no se puede transcribir ni implementar campo por campo los formatos 01–15.**
2. Obtener la última disposición expresa de aprobación/modificación si existiese, posterior al informe 628-2025-GRT; no se acreditó en esta revisión.
3. Comprobar escala/tamaño de cuadrículas, ecuaciones y parámetros de artículo 3.2 del proyecto original; ningún número se fija por conjetura.
4. Someter adaptación a empresa, régimen y año al revisor jurídico/regulatorio.

### Procedimiento de incorporación cuando se disponga del PDF

`python scripts/pide/register_source.py --pdf ruta\PIDE_2017_ANEXO.pdf --origin-url https://... --document-type original_methodology_draft`

Esto **solo registra hash, metadatos y copia local no versionada**; la auditoría humana debe completar referencias de página y aprobación antes de habilitar cualquier exportación oficial. Hasta entonces bloquear estado `approved`.
