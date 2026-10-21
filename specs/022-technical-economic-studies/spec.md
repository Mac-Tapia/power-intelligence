# Multi-domain electrical and economic studies

## User story
Catalog, study orchestration and comparison by scenario/constraint.

## Contract
A calculation output is not valid without independent solver validation, annual cost basis and approved evidence.

## Acceptance
1. Versioned normative source is present.
2. Eligibility is checked, not inferred from voltage alone.
3. Technical and financial results are traceable to inputs and independent validation.
4. Human reviewer approves regulatory claims.

---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-022` · **Gate:** `G4` · **Dependencias:** SPEC-008, SPEC-016.  
**Alcance verificable:** Evaluar costos e inversiones con flujos de caja trazables, horizontes normativos y escenarios.  
**Ubicación propuesta:** `packages/python/power-economics/, packages/python/power-application/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-022-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-022-02:** entrada válida: VAN/TIR/anualidad y pérdidas se reproducen con tasa, moneda/año base y perfiles explícitos; sin datos se informa falta.
- **FR-022-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-022-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-022-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-022-01:** caso exitoso demuestra `FR-022-01/02` con fixture y evidencia automatizada.
- **AC-022-02:** caso negativo demuestra `FR-022-03`, sin alterar estado persistido ni fuente original.
- **AC-022-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-022-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
