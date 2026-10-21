# SPEC-006 — canonical-electrical-model

**Propósito:** Crear modelo canónico de equipos, terminales, fases, unidades, base de tensión y snapshots.


---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-006` · **Gate:** `G1` · **Dependencias:** SPEC-000.  
**Alcance verificable:** Crear modelo canónico de equipos, terminales, fases, unidades, base de tensión y snapshots.  
**Ubicación propuesta:** `packages/python/power-domain/, power-ports/, power-topology/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-006-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-006-02:** entrada válida: Nunca se confunde fase/tensión LL-LN, no existe conectividad implícita por GIS y cada equipo conserva origen y revisión.
- **FR-006-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-006-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-006-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-006-01:** caso exitoso demuestra `FR-006-01/02` con fixture y evidencia automatizada.
- **AC-006-02:** caso negativo demuestra `FR-006-03`, sin alterar estado persistido ni fuente original.
- **AC-006-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-006-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
