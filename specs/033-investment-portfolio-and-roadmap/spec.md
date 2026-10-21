# SPEC-033 — investment-portfolio-and-roadmap

**Propósito:** Priorizar cartera plurianual de proyectos con restricciones presupuestales, riesgos y dependencias.


---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-033` · **Gate:** `G4` · **Dependencias:** SPEC-018, SPEC-023.  
**Alcance verificable:** Priorizar cartera plurianual de proyectos con restricciones presupuestales, riesgos y dependencias.  
**Ubicación propuesta:** `packages/python/power-application/, apps/workstation-web/src/features/projects/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-033-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-033-02:** entrada válida: Cartera preserva decisiones, horizontes/regulación por tipo de proyecto, restricciones y métricas sin duplicar inversiones.
- **FR-033-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-033-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-033-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-033-01:** caso exitoso demuestra `FR-033-01/02` con fixture y evidencia automatizada.
- **AC-033-02:** caso negativo demuestra `FR-033-03`, sin alterar estado persistido ni fuente original.
- **AC-033-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-033-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
