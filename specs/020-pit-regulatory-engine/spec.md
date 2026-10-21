# PIT SST/SCT regulatory profiles and versioned rules

## User story
Applicable rules PIT, clause-level traceability, amendment consolidation and blocked certification until human validation.

## Contract
Only apply SST/SCT to eligible transmission studies. Version source, clause, effective_date and reviewer; missing source blocks regulatory submission.

## Acceptance
1. Versioned normative source is present.
2. Eligibility is checked, not inferred from voltage alone.
3. Technical and financial results are traceable to inputs and independent validation.
4. Human reviewer approves regulatory claims.

---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-020` · **Gate:** `G4` · **Dependencias:** SPEC-017, SPEC-022, SPEC-025.  
**Alcance verificable:** Aplicar metodología SST/SCT PIT por versión consolidada y cláusula verificada.  
**Ubicación propuesta:** `packages/python/power-regulation/, docs/regulatory/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-020-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-020-02:** entrada válida: La fuente 217-2013-OS/CD y modificatorias aplicables están versionadas; elegibilidad y cláusulas tienen evidencia y revisión humana.
- **FR-020-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-020-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-020-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-020-01:** caso exitoso demuestra `FR-020-01/02` con fixture y evidencia automatizada.
- **AC-020-02:** caso negativo demuestra `FR-020-03`, sin alterar estado persistido ni fuente original.
- **AC-020-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-020-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
