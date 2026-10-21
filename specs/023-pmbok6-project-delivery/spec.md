# PMBOK 6 project governance for each investment

## User story
Project Charter, WBS, schedule, cost, quality, risk, procurement, stakeholder and closure packs.

## Contract
Each investment alternative links to a project charter and register; project approvals separate from study results.

## Acceptance
1. Versioned normative source is present.
2. Eligibility is checked, not inferred from voltage alone.
3. Technical and financial results are traceable to inputs and independent validation.
4. Human reviewer approves regulatory claims.

---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-023` · **Gate:** `G4` · **Dependencias:** SPEC-022.  
**Alcance verificable:** Gestionar proyectos PIT/PIDE y obras bajo cinco grupos de procesos y diez áreas PMBOK sexta edición.  
**Ubicación propuesta:** `docs/project-management/, packages/python/power-application/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-023-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-023-02:** entrada válida: Cada alternativa aprobada genera expediente de proyecto con charter, EDT/WBS, cronograma, costos, riesgos, stakeholders y seguimiento.
- **FR-023-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-023-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-023-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-023-01:** caso exitoso demuestra `FR-023-01/02` con fixture y evidencia automatizada.
- **AC-023-02:** caso negativo demuestra `FR-023-03`, sin alterar estado persistido ni fuente original.
- **AC-023-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-023-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
