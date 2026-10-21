# 002 — Impacto de nueva carga en red de distribución

**Estado:** cribado equilibrado operativo (`scripts/unitesis.py new-load`, `POST /api/v1/studies/new-load`, pestaña "Nueva carga" de la workstation). El estudio completo por fase depende de 008-C.

**Dependencias:** 001 (red real del caso), 008-A (operativo) / 008-C (por fase), perfiles de carga gold del caso (029), perfil regulatorio del caso.

**Alcance:** clonar el snapshot, asignar una nueva demanda real al nodo o equipo de conexión aprobado, simular antes y después, y comparar cargabilidad, tensión (por fase cuando exista 008-C), pérdidas, capacidad remanente, alternativas y CAPEX/OPEX trazables.

## Criterios de aceptación

- AC-002-01: la carga nueva actúa sobre un escenario clonado. El snapshot de origen no cambia (hash idéntico antes y después) y la barra de conexión debe existir; nunca se infiere.
- AC-002-02: ningún `StudyResult` sale sin versión del solver, convergencia, unidades, hash de entradas y estado de contraste. La aceptación técnica es `false` hasta la revisión humana.
- AC-002-03: si faltan parámetros, la simulación se rechaza con un reporte (código de salida 2), nunca con valores supuestos de potencia por alimentador.
- AC-002-04: los criterios de cribado (V mínima, cargabilidad máxima) son explícitos en la solicitud y se registran en la evidencia.
- AC-002-05: las alternativas de mitigación pasan la validación física del solver propio y el contraste independiente (spec 018).

---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-002` · **Gate:** `G4` · **Dependencias:** SPEC-008, SPEC-009, SPEC-016, SPEC-022.  
**Alcance verificable:** Evaluar nuevas cargas mayores o menores según configuración, sin alterar red base, y proponer alternativas verificadas.  
**Ubicación propuesta:** `packages/python/power-application/, apps/workstation-web/src/features/studies/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-002-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-002-02:** entrada válida: Se comparan escenarios antes/después con nodos, perfiles P/Q, convergencia, pérdidas, tensión, cargabilidad y costos reproducibles.
- **FR-002-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-002-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-002-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-002-01:** caso exitoso demuestra `FR-002-01/02` con fixture y evidencia automatizada.
- **AC-002-02:** caso negativo demuestra `FR-002-03`, sin alterar estado persistido ni fuente original.
- **AC-002-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-002-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
