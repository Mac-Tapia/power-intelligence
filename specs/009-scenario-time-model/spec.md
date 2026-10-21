# SPEC-009 — scenario-time-model

**Propósito:** Gestionar casos de operación, horizonte, variantes técnicas y series temporales sin mutar la red original.


---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-009` · **Gate:** `G2` · **Dependencias:** SPEC-006, SPEC-007, SPEC-010.  
**Alcance verificable:** Gestionar casos de operación, horizonte, variantes técnicas y series temporales sin mutar la red original.  
**Ubicación propuesta:** `packages/python/power-application/, apps/workstation-web/src/features/scenarios/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-009-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-009-02:** entrada válida: Misma entrada y escenario/semilla produce mismas configuraciones; escenarios pueden compararse y reproducirse.
- **FR-009-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-009-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-009-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-009-01:** caso exitoso demuestra `FR-009-01/02` con fixture y evidencia automatizada.
- **AC-009-02:** caso negativo demuestra `FR-009-03`, sin alterar estado persistido ni fuente original.
- **AC-009-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-009-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
