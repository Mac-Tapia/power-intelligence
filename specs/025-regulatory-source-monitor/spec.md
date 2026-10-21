# Regulatory consolidation and amendment watcher

## User story
Controlled annual review and change impact analysis of Osinergmin/MINEM amendments and module prices.

## Contract
No dynamic remote source directly updates production policy; diff and legal approval required.

## Acceptance
1. Versioned normative source is present.
2. Eligibility is checked, not inferred from voltage alone.
3. Technical and financial results are traceable to inputs and independent validation.
4. Human reviewer approves regulatory claims.

---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-025` · **Gate:** `G4` · **Dependencias:** SPEC-015.  
**Alcance verificable:** Mantener catálogo de fuentes normativas y detectar cambios sin actualizar reglas automáticamente.  
**Ubicación propuesta:** `docs/regulatory/SOURCES.json, packages/python/power-regulation/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-025-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-025-02:** entrada válida: Detección de modificaciones crea revisión pendiente; no aplica nueva tasa/plazo/regla sin análisis y aprobación humana.
- **FR-025-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-025-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-025-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-025-01:** caso exitoso demuestra `FR-025-01/02` con fixture y evidencia automatizada.
- **AC-025-02:** caso negativo demuestra `FR-025-03`, sin alterar estado persistido ni fuente original.
- **AC-025-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-025-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
