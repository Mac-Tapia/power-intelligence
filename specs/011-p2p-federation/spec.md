# Spec — Red P2P segura para colaboración entre nodos

**Estado:** DRAFT / Not implemented · Feature ID `011`.

## User intent y alcance
Permitir mensajería de escenarios y evidencias entre instituciones autorizadas con independencia del comercio de energía y sin comandos SCADA.

## Requerimientos verificables
- Firmas, mTLS/peer keys, ACL, expiración, idempotencia, anti-replay.
- Outbox/inbox at-least-once, store-and-forward y reintentos.
- libp2p opcional tras benchmark comparativo con broker central.
- Separación total entre mensajes P2P y conectividad eléctrica.

## Criterios de aceptación
- Peer desconocido rechazado, mensaje expirado/repetido rechazado.
- Rotación de claves y partición/reconexión sin re-ejecutar duplicados.
- Cualquier mensaje sobre SCADA/maniobras prohibido por contrato.
- Escenarios de prueba no atraviesan el boundary de tenant.

## Restricciones
Se prohíben ejecuciones sobre SCADA/protecciones. No se debe acceder a datos no autorizados ni inferir valores faltantes. El acceso comercial solo tras aprobación legal/regulatoria verificable.

## Dependencias
`001` ingesta y contratos; `003` GIS/unifilar; `004` solver validado; el resto según orden de `docs/traceability/FEATURE-MAP.md`.

---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-011` · **Gate:** `G6` · **Dependencias:** SPEC-005, SPEC-010, SPEC-035.  
**Alcance verificable:** Permitir federación P2P entre instancias autorizadas para intercambio de información, sin maniobra remota.  
**Ubicación propuesta:** `packages/python/power-p2p/, workers/p2p-sync/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-011-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-011-02:** entrada válida: Peers autenticados, replays detectados, particiones recuperables y topología sensible no expuesta por defecto.
- **FR-011-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-011-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-011-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-011-01:** caso exitoso demuestra `FR-011-01/02` con fixture y evidencia automatizada.
- **AC-011-02:** caso negativo demuestra `FR-011-03`, sin alterar estado persistido ni fuente original.
- **AC-011-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-011-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
