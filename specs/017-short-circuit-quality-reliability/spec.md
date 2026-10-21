# SPEC-017 — short-circuit-quality-reliability

**Propósito:** Ofrecer estudios de falla, calidad y confiabilidad diferenciando condiciones de datos y normas aplicables.


---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-017` · **Gate:** `G3` · **Dependencias:** SPEC-008, SPEC-009.  
**Alcance verificable:** Ofrecer estudios de falla, calidad y confiabilidad diferenciando condiciones de datos y normas aplicables.  
**Ubicación propuesta:** `packages/python/power-simulation/, workers/simulation/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-017-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-017-02:** entrada válida: Corrientes de falla, límites de tensión, SAIDI/SAIFI y otras salidas solo se publican si hay parámetros exigibles y método declarado.
- **FR-017-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-017-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-017-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-017-01:** caso exitoso demuestra `FR-017-01/02` con fixture y evidencia automatizada.
- **AC-017-02:** caso negativo demuestra `FR-017-03`, sin alterar estado persistido ni fuente original.
- **AC-017-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-017-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
