# SPEC-034 — generation-transmission-integration

**Propósito:** Extender modelos y estudios a generación, transmisión e integración renovable con seguridad de red.


---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-034` · **Gate:** `G5` · **Dependencias:** SPEC-008, SPEC-017, SPEC-019, SPEC-028.  
**Alcance verificable:** Extender modelos y estudios a generación, transmisión e integración renovable con seguridad de red.  
**Ubicación propuesta:** `packages/python/power-simulation/, power-optimization/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-034-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-034-02:** entrada válida: Estudios N-1, generación, restricciones y OPF declaran alcance, convergencia y validación de modelo.
- **FR-034-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-034-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-034-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-034-01:** caso exitoso demuestra `FR-034-01/02` con fixture y evidencia automatizada.
- **AC-034-02:** caso negativo demuestra `FR-034-03`, sin alterar estado persistido ni fuente original.
- **AC-034-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-034-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
