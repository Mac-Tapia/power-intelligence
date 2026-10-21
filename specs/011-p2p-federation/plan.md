# Plan — Red P2P segura para colaboración entre nodos

**Estado:** DRAFT; no desplegado.

## Contexto y boundaries
Permitir mensajería de escenarios y evidencias entre instituciones autorizadas con independencia del comercio de energía y sin comandos SCADA.

## Plan de implementación
1. Congelar diseño, ADRs y amenazas; especificar interfaces y versiones.
2. Construir el adaptador de referencia aislado, con fixtures sintéticos.
3. Verificar invariantes, seguridad, reproducibilidad y pruebas negativas.
4. Ejecutar integración con la API/workers y generación de evidencia.
5. Benchmark, revisión y PR según SDD y Git worktree.

## Tasks
- Definir Envelopes P2P v1 y port PeerTransport
- Implementar adaptador broker/test primero, suite de autentificación
- Inbox/outbox, anti-replay, TTL, métricas, resiliencia
- Evaluar libp2p/relays/permissioning como ADR
- Integrar panel de peers y trazas auditables sin exponer secretos

## Gates de aprobación
- Peer desconocido rechazado, mensaje expirado/repetido rechazado.
- Rotación de claves y partición/reconexión sin re-ejecutar duplicados.
- Cualquier mensaje sobre SCADA/maniobras prohibido por contrato.
- Escenarios de prueba no atraviesan el boundary de tenant.
