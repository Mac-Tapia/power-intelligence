# SPEC-019 — multiobjective-optimization

**Propósito:** Optimizar costos, pérdidas, calidad, riesgo y robustez con límites físicos.


---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-019` · **Gate:** `G4` · **Dependencias:** SPEC-018, SPEC-008.  
**Alcance verificable:** Optimizar costos, pérdidas, calidad, riesgo y robustez con límites físicos.  
**Ubicación propuesta:** `packages/python/power-optimization/, workers/optimization/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-019-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-019-02:** entrada válida: Pareto y sensibilidad son reproducibles; soluciones infactibles no pueden dominar; no se afirma óptimo global sin prueba.
- **FR-019-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-019-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-019-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-019-01:** caso exitoso demuestra `FR-019-01/02` con fixture y evidencia automatizada.
- **AC-019-02:** caso negativo demuestra `FR-019-03`, sin alterar estado persistido ni fuente original.
- **AC-019-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-019-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
