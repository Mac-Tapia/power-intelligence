# SPEC-032 — reporting-and-evidence

**Propósito:** Emitir memorias, informes y expedientes con trazabilidad de cálculos, normas y aprobaciones.


---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-032` · **Gate:** `G4` · **Dependencias:** SPEC-008, SPEC-022, SPEC-023.  
**Alcance verificable:** Emitir memorias, informes y expedientes con trazabilidad de cálculos, normas y aprobaciones.  
**Ubicación propuesta:** `packages/python/power-evidence/, apps/control-api/, docs/templates/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-032-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-032-02:** entrada válida: Informe enlaza hash de input, solver, commit, supuestos, tablas, gráficos y revisiones humanas; no inventa resultados.
- **FR-032-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-032-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-032-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-032-01:** caso exitoso demuestra `FR-032-01/02` con fixture y evidencia automatizada.
- **AC-032-02:** caso negativo demuestra `FR-032-03`, sin alterar estado persistido ni fuente original.
- **AC-032-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-032-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
