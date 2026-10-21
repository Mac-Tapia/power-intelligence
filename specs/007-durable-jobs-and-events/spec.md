# SPEC-007 — durable-jobs-and-events

**Propósito:** Ejecutar trabajos ETL/solvers/optimización fuera de API con persistencia y reintentos seguros.


---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-007` · **Gate:** `G1` · **Dependencias:** SPEC-004, SPEC-005.  
**Alcance verificable:** Ejecutar trabajos ETL/solvers/optimización fuera de API con persistencia y reintentos seguros.  
**Ubicación propuesta:** `apps/control-api/, workers/, infra/compose/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-007-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-007-02:** entrada válida: Un job reenviado no duplica efectos, recupera interrupciones y conserva estados/progreso y registro de evidencias.
- **FR-007-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-007-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-007-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-007-01:** caso exitoso demuestra `FR-007-01/02` con fixture y evidencia automatizada.
- **AC-007-02:** caso negativo demuestra `FR-007-03`, sin alterar estado persistido ni fuente original.
- **AC-007-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-007-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
