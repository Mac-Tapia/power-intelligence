# SPEC-039 — production-release-and-governance

**Propósito:** Definir gate de producción por perfiles de producto, sin bloquear núcleo por capacidades experimentales.


---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-039` · **Gate:** `G7` · **Dependencias:** SPEC-031, SPEC-032, SPEC-038.  
**Alcance verificable:** Definir gate de producción por perfiles de producto, sin bloquear núcleo por capacidades experimentales.  
**Ubicación propuesta:** `docs/operations/, infra/, .github/workflows/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-039-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-039-02:** entrada válida: Solo se despliega release core si cumple seguridad, UAT, respaldo, rendimiento y aprobación; módulos P2P/AI requieren gate propio.
- **FR-039-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-039-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-039-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-039-01:** caso exitoso demuestra `FR-039-01/02` con fixture y evidencia automatizada.
- **AC-039-02:** caso negativo demuestra `FR-039-03`, sin alterar estado persistido ni fuente original.
- **AC-039-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-039-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
