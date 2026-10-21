# Spec — GraphRAG técnico trazable de evidencias/normas

**Estado:** DRAFT / Not implemented · Feature ID `014`.

## User intent y alcance
Recuperar contextos documentales y relaciones de estudios/normas con citas, ACL y snapshot correcto; no generar parámetros eléctricos inventados.

## Requerimientos verificables
- Separar retrieval documental de la topología física.
- Citar fuentes y versiones con retrieval determinista auditable.
- Bloquear prompt injection y cruces multi-tenant.
- Evaluar contra búsqueda léxica/vectorial sin Grafo.

## Criterios de aceptación
- 100% de respuestas con norma enlazan fragmento verificable.
- Los documentos inyectados no ejecutan instrucciones.
- Retrieval de un snapshot no extrae evidencia de otro.
- Resultados incorrectos regresan "no fundamentado".

## Restricciones
Se prohíben ejecuciones sobre SCADA/protecciones. No se debe acceder a datos no autorizados ni inferir valores faltantes. El acceso comercial solo tras aprobación legal/regulatoria verificable.

## Dependencias
`001` ingesta y contratos; `003` GIS/unifilar; `004` solver validado; el resto según orden de `docs/traceability/FEATURE-MAP.md`.

---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-014` · **Gate:** `G6` · **Dependencias:** SPEC-010, SPEC-030, SPEC-032.  
**Alcance verificable:** Consultar documentación y relaciones de equipos/reglas/estudios mediante GraphRAG con citas comprobables.  
**Ubicación propuesta:** `packages/python/power-graphrag/, workers/graph-retrieval/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-014-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-014-02:** entrada válida: Toda respuesta técnica cita documento/fuente/fecha y no puede escribir la topología eléctrica ni cruzar tenants.
- **FR-014-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-014-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-014-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-014-01:** caso exitoso demuestra `FR-014-01/02` con fixture y evidencia automatizada.
- **AC-014-02:** caso negativo demuestra `FR-014-03`, sin alterar estado persistido ni fuente original.
- **AC-014-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-014-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
