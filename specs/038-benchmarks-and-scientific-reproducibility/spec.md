# SPEC-038 — benchmarks-and-scientific-reproducibility

**Propósito:** Establecer evaluación reproducible con casos IEEE, redes sintéticas y datasets autorizados.


---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-038` · **Gate:** `G3` · **Dependencias:** SPEC-008, SPEC-010.  
**Alcance verificable:** Establecer evaluación reproducible con casos IEEE, redes sintéticas y datasets autorizados.  
**Ubicación propuesta:** `benchmarks/, tests/electrical-golden/, docs/scientific-evidence/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-038-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-038-02:** entrada válida: Cada benchmark versiona entrada, licencia, resultados esperados, tolerancia, hardware y métricas reproducibles.
- **FR-038-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-038-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-038-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-038-01:** caso exitoso demuestra `FR-038-01/02` con fixture y evidencia automatizada.
- **AC-038-02:** caso negativo demuestra `FR-038-03`, sin alterar estado persistido ni fuente original.
- **AC-038-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-038-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
