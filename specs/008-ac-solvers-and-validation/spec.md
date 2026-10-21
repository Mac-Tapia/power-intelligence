# SPEC-008 — ac-solvers-and-validation

**Propósito:** Ejecutar cálculos eléctricos AC mediante adaptadores deterministas y verificar físicamente cada resultado.


---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-008` · **Gate:** `G3` · **Dependencias:** SPEC-006, SPEC-007, SPEC-010.  
**Alcance verificable:** Ejecutar cálculos eléctricos AC mediante adaptadores deterministas y verificar físicamente cada resultado.  
**Ubicación propuesta:** `packages/python/power-simulation/, workers/simulation/, tests/electrical-golden/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-008-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-008-02:** entrada válida: Cada estudio informa convergencia, errores P/Q, tensiones, corrientes, unidades y comparación con feeder benchmark y solver independiente.
- **FR-008-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-008-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-008-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-008-01:** caso exitoso demuestra `FR-008-01/02` con fixture y evidencia automatizada.
- **AC-008-02:** caso negativo demuestra `FR-008-03`, sin alterar estado persistido ni fuente original.
- **AC-008-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-008-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.

## Criterios vigentes incorporados (antes spec 004)

**Estado:** 008-A, 008-B1, 008-B2 y 008-C (IEEE 13) operativos; 008-C2/C3 y 017 pendientes. Paquete dueño: `power-simulation`. Motores propietarios excluidos (ADR-0010).

### Alcances

- **008-A (operativo):** flujo AC radial equilibrado por barrido atrás/adelante; una slack; cargas PQ; líneas serie; interruptores ideales; contraste con pandapower bajo las tolerancias de `docs/architecture/CONTRACTS-AND-EVIDENCE.md`.
- **008-B1 (operativo):** Newton-Raphson propio sobre la Y-bus compartida, para redes radiales y malladas, con interruptores ideales fusionados.
- **008-B2 (operativo):** transformadores MT/BT de dos devanados con impedancia, relación, tap y desfase de grupo (sin rama magnetizante).
- **008-C (operativo, IEEE 13):** trifásico desbalanceado en marco de fases: matrices de línea reducidas por Kron con admitancia en derivación, reguladores ideales de tap fijo, transformadores YNyn0, cargas ZIP en estrella o delta. Resultado propio `UnbalancedStudyResult` (separado del equilibrado).
- **017:** cortocircuito IEC 60909 simplificado.

### Criterios de aceptación

- AC-008-A01: cada motor declara su capacidad. Un snapshot con elementos fuera de ella se rechaza con la lista de elementos; nunca se simplifica en silencio.
- AC-008-A02: la Y-bus vive en `power-simulation` y la reutilizan el solver, el residuo físico de la spec 029 y el comparador. No hay dos formulaciones.
- AC-008-A03: cada alcance se contrasta con una referencia abierta (pandapower u OpenDSS mediante adaptador) en casos IEEE (13/33/123 nodos) y sintéticos, con las tolerancias de `docs/architecture/CONTRACTS-AND-EVIDENCE.md`. Los casos IEEE validan el motor; no son datos de entrenamiento. El resultado se publica en `benchmarks/power-flow/`.
- AC-008-A04: un caso no convergente devuelve `failed` con su residuo; un motor ausente devuelve `unavailable`.
