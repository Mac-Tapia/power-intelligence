# SPEC-016 — demand-forecast-and-load-profiles

**Propósito:** Procesar perfiles 15 min y pronosticar demanda con trazabilidad por medidor, alimentador y periodo.


---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-016` · **Gate:** `G3` · **Dependencias:** SPEC-001, SPEC-006, SPEC-009.  
**Alcance verificable:** Procesar perfiles 15 min y pronosticar demanda con trazabilidad por medidor, alimentador y periodo.  
**Ubicación propuesta:** `packages/python/power-application/, workers/ml-training/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-016-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-016-02:** entrada válida: Duplicados y huecos quedan informados; los nuevos clientes se agregan según medidor/fecha con potencia indicada; baselines medibles.
- **FR-016-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-016-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-016-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-016-01:** caso exitoso demuestra `FR-016-01/02` con fixture y evidencia automatizada.
- **AC-016-02:** caso negativo demuestra `FR-016-03`, sin alterar estado persistido ni fuente original.
- **AC-016-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-016-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
