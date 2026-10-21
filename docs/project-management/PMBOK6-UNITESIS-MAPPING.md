# PMBOK 6 — gobernanza por cada proyecto de inversión UNITESIS

Se adopta la **sexta edición solicitada**, como adaptación del estándar de PMI (49 procesos en cinco grupos y diez áreas de conocimiento). La gestión es híbrida: etapas de ingeniería/regulación con firmas, desarrollo de código mediante SDD/Agile y control de cartera con PMBOK. El uso de guías no constituye certificación PMI.

## Grupos: Inicio, Planificación, Ejecución, Monitoreo y Control, Cierre

## Diez áreas y entregables

| Área | Artefacto concreto | Vínculo a plataforma |
|---|---|---|
| Integración | Acta, plan director, registro cambios, cierre | regulación y aprobaciones |
| Alcance | requisitos, WBS/EDT, diccionario EDT, aceptación | alternativa, instalaciones elegidas |
| Cronograma | actividades, duraciones, dependencias, ruta crítica, hitos COD | PIT periodo 4 años / cronograma real |
| Costos | CAPEX base, presupuesto, contingencia, EVM | evaluación financiera diferenciada |
| Calidad | plan, métricas, inspección y aceptación solver | NTCSE, CNE, estudios |
| Recursos | RACI, matriz equipos/roles, disponibilidad | workers y equipo proyecto |
| Comunicaciones | plan, minutas, reportes | interesados, regulador |
| Riesgos | registro, matriz, EMV, respuestas, reservas | Monte Carlo, incertidumbre |
| Adquisiciones | estrategia, proveedores, costos módulos, contratos | procurement/costos |
| Interesados | mapeo, involucramiento, aprobaciones | clientes, empresa, Osinergmin, MINEM, COES |

## Entregables por proyecto
```
projects/<project_id>/
  00_charter/       acta, business_case
  01_scope/         requisitos, EDT, diccionario
  02_engineering/   base GIS, demanda, alternativas y validación
  03_economics/     CAPEX_OPEX, pérdidas, VP, escenarios
  04_schedule/      cronograma, ruta_crítica, hitos COD
  05_quality/       cumplimiento por cláusula, pruebas
  06_resources/     roles, recursos, RACI
  07_communications/minutas, comunicaciones
  08_risks/         riesgos, EMV, Monte Carlo
  09_procurement/   proveedores, módulos, contratos
  10_stakeholders/  registro y aprobaciones
  11_changes/       RFC, impacto, decisiones
  12_closure/       actas, aceptación y lessons learned
```
No se guardan proyectos reales sensibles en git; `projects/` es una plantilla de estructura y los proyectos reales van a almacenamiento autorizado con ACL y cifrado.

## Reglas de aprobación
- Una solución técnica es **propuesta** hasta pasar G3.
- Una comparación económica es **preliminar** hasta pasar G5.
- Un proyecto es **aprobado** solo con autoridades competentes; LLM/agent no puede aprobar.
- La programación del PIT no equivale al cronograma físico de ejecución del PMBOK.
