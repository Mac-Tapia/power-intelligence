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
