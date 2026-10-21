# PIDE — Cronograma documentado del Anexo B.1.2 (procedimiento FONAFE)

**Fuente primaria:** Resolución OSINERGMIN N.° 080-2012-OS/CD, versión concordada a diciembre de 2016, Anexo B.1.2, páginas impresas 24–25 (PDF páginas 24–25, indexación 23–24), incorporado por Resolución 264-2016-OS/CD.

URL: https://www2.osinergmin.gob.pe/Resoluciones/pdf/2012/OSINERGMIN%20No.080-2012-OS-CD.pdf

**Naturaleza:** cronograma/procedimiento, distinto de los criterios técnicos de un supuesto «Anexo 1» PIDE. **No aplicar automáticamente estos plazos a expedientes actuales** sin revisar modificaciones y el régimen vigente. Su ámbito literal indicado es empresas bajo FONAFE.

| Ítem del anexo | Hito y responsable principal | Plazo de versión consultada |
|---|---|---|
| a | Presentación del estudio y plan por la empresa distribuidora bajo FONAFE | Primer día hábil de octubre del segundo año anterior a fijación VAD |
| b | Publicación y convocatoria por Osinergmin | 5 días hábiles desde vencimiento de presentación |
| c | Audiencia pública de las empresas | 10 días hábiles desde vencimiento de publicación |
| d | Observaciones de Osinergmin | 30 días hábiles desde audiencia pública de empresas |
| e | Absolución y entrega de estudio definitivo | 20 días hábiles desde recepción de observaciones |
| f | Publicación de absolución y estudio definitivo | 5 días hábiles desde vencimiento de entrega |
| g | Proyecto de resolución y convocatoria a audiencia | 30 días hábiles desde vencimiento de publicación del estudio definitivo |
| h | Audiencia pública de Osinergmin | 10 días hábiles desde publicación del proyecto de resolución |
| i | Opiniones y sugerencias sobre proyecto de resolución | 20 días hábiles después de audiencia pública de Osinergmin |
| j | Publicación de resolución de aprobación | 30 días hábiles desde vencimiento de plazo de comentarios; respetar separación mínima indicada en anexo |
| k | Presentación de recursos de reconsideración | 15 días hábiles desde publicación en El Peruano de resolución |
| l | Publicación de recursos y convocatoria | 5 días hábiles desde vencimiento de presentación de recursos |
| m | Audiencia pública de recursos | 10 días hábiles desde publicación de recursos |
| n | Opiniones sobre recursos | 10 días hábiles desde audiencia de recursos |
| ñ | Resolución de reconsideraciones | 30 días hábiles desde interposición de recurso |
| o | Publicación de resoluciones de reconsideración | 3 días hábiles desde emisión de resoluciones |
| p | Audiencias solicitadas por interesados | Durante todo el procedimiento |

### Componente de software y controles propuestos
1. `regulatory_calendar` maneja feriados nacionales/peruanos y días hábiles administrativos (con calendarios versionados y observación de días inhábiles extraordinarios).
2. `regulatory_milestone` almacena `normative_source`, `clause`, `party`, `trigger_id`, `relative_business_days`, `actual_date`, `due_date`, `evidence_hash`, `status`.
3. Validación de secuencia: un agente puede preparar expedientes, pero nunca alterar fechas oficiales ni marcar resolución emitida sin documento firmado.
4. Importador de resolución actualizada, revisión jurídica y aprobación humana *antes* de generación de vencimientos públicos.
5. UI Gantt PMBOK vincula cronograma regulatorio con cronograma del proyecto: calendarios distintos, dependencias explícitas.
6. Tests de feriados variables, cómputo de plazos y recursos de reconsideración; prohibido hardcodear feriados sin fuente.

**Límite documental:** la información precedente transcribe la estructura de hitos y resume plazos del texto histórico consultado. No es dictamen jurídico sobre vigencia posterior.

Secuencia completa de los ítems a–p (incluyendo ñ).
