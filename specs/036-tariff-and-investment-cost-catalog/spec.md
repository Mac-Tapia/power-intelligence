# SPEC-036 — tariff-and-investment-cost-catalog

**Propósito:** Gestionar módulos estándares, unidades tarifarias y parámetros económicos versionados y aplicables.


---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-036` · **Gate:** `G4` · **Dependencias:** SPEC-020, SPEC-022.  
**Alcance verificable:** Gestionar módulos estándares, unidades tarifarias y parámetros económicos versionados y aplicables.  
**Ubicación propuesta:** `packages/python/power-regulation/, power-economics/, config/regulations/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-036-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-036-02:** entrada válida: Ninguna tarifa, costo estándar o tipo de cambio se fija sin fuente/fecha; el costo es reproducible por edición y jurisdicción.
- **FR-036-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-036-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-036-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-036-01:** caso exitoso demuestra `FR-036-01/02` con fixture y evidencia automatizada.
- **AC-036-02:** caso negativo demuestra `FR-036-03`, sin alterar estado persistido ni fuente original.
- **AC-036-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-036-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
