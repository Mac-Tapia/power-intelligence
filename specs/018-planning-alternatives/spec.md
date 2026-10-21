# SPEC-018 — planning-alternatives

**Propósito:** Proponer alternativas de expansión justificadas, factibles y comparables por marco de estudio.


---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-018` · **Gate:** `G4` · **Dependencias:** SPEC-002, SPEC-017, SPEC-022.  
**Alcance verificable:** Proponer alternativas de expansión justificadas, factibles y comparables por marco de estudio.  
**Ubicación propuesta:** `packages/python/power-application/, power-optimization/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-018-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-018-02:** entrada válida: Cada alternativa conserva hipótesis, obras, restricciones, fecha de servicio, viabilidad y evidencia económica; cantidad según perfil.
- **FR-018-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-018-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-018-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-018-01:** caso exitoso demuestra `FR-018-01/02` con fixture y evidencia automatizada.
- **AC-018-02:** caso negativo demuestra `FR-018-03`, sin alterar estado persistido ni fuente original.
- **AC-018-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-018-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.

## Criterios vigentes incorporados (antes spec 005)

**Estado:** parcial. Ya operativo: alternativas de conductor por línea, con contraste independiente y ranking por VPN (`unitesis_application.alternatives`). Paquetes: `power-optimization` y `power-economics`.

### Criterios de aceptación

- AC-018-E01: toda alternativa se evalúa en un escenario clonado y la confirma el solver propio más un contraste independiente. Sin contraste aprobado no hay ranking.
- AC-018-E02: costos, tasa, horizonte, precio de energía y factor de pérdidas son explícitos y tienen fuente. Sin costo, la alternativa se reporta "sin valorar".
- AC-018-E03: con varios objetivos (VPN, pérdidas, cargabilidad, CO2) se publica el frente de Pareto, no un único ganador.
- AC-018-E04: un sustituto de la spec 029 puede priorizar candidatos, pero la decisión la confirma el solver.
