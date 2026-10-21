# Regulatory UI and exportable dossier

## User story
Backend API and frontend workspaces for profile and status, alternatives, PMBOK plan, audit and evidence exports.

## Contract
A draft/unverified norm must display a hard warning; cannot generate an approved regulation badge.

## Acceptance
1. Versioned normative source is present.
2. Eligibility is checked, not inferred from voltage alone.
3. Technical and financial results are traceable to inputs and independent validation.
4. Human reviewer approves regulatory claims.

---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-024` · **Gate:** `G4` · **Dependencias:** SPEC-003, SPEC-020, SPEC-021, SPEC-023.  
**Alcance verificable:** Presentar trazabilidad de normas, estudios, evidencias y proyecto regulatorio en UI.  
**Ubicación propuesta:** `apps/workstation-web/src/features/evidence/, apps/control-api/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-024-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-024-02:** entrada válida: Usuario ve edición/fuente normativa, estado de verificación, bloqueos, fichas de alternativa y expedientes exportables.
- **FR-024-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-024-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-024-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-024-01:** caso exitoso demuestra `FR-024-01/02` con fixture y evidencia automatizada.
- **AC-024-02:** caso negativo demuestra `FR-024-03`, sin alterar estado persistido ni fuente original.
- **AC-024-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-024-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
