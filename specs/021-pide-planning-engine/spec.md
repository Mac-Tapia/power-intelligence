# PIDE FONAFE distribution planning with draft protection

## User story
PIDE procedural track B.1.2 and independent internal distribution planning.

## Contract
Do not enforce 2017 draft as approved. Annex 1 pending primary document verification; no silent assumptions.

## Acceptance
1. Versioned normative source is present.
2. Eligibility is checked, not inferred from voltage alone.
3. Technical and financial results are traceable to inputs and independent validation.
4. Human reviewer approves regulatory claims.

---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-021` · **Gate:** `G4` · **Dependencias:** SPEC-018, SPEC-022, SPEC-027.  
**Alcance verificable:** Construir planificación de distribución con perfil PIDE histórico parametrizable, sin declarar aprobada prepublicación.  
**Ubicación propuesta:** `packages/python/power-regulation/, docs/regulatory/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-021-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-021-02:** entrada válida: Cada output dice si método es prepublicación/propuesta/referencia; sin Anexo 1 auditado no se certifican los 15 formatos.
- **FR-021-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-021-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-021-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-021-01:** caso exitoso demuestra `FR-021-01/02` con fixture y evidencia automatizada.
- **AC-021-02:** caso negativo demuestra `FR-021-03`, sin alterar estado persistido ni fuente original.
- **AC-021-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-021-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
