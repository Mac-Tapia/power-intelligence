# Eventos de integración P2P y ledger (propuesta, specs 011/012)

**No ejecutables**. Versionar en `contracts/` y publicar desde outbox transaccional.

- `GridSnapshotPublished.v1`: network_snapshot_id + topology_hash + tenant_id + evidence manifest.
- `GraphProjectionReady.v1`: projection_version, snapshot_id y prueba integridad.
- `P2PMessageAccepted.v1`: message_id, sender, signature_verified, issued_at; no información sensible.
- `EnergyTradeProposed.v1`: cantidad, periodo, comprador/vendedor pseudonimizados, tenant.
- `MarketClearingValidated.v1`: solver, constraints, evidencia de balance y autorizações.
- `EvidenceAnchorRequested.v1`: digest y puntero; `EvidenceAnchorConfirmed.v1`: tx_ref y verificación.

Usar idempotency keys, delivery at-least-once + outbox/inbox, control de esquemas y autenticación. Eventos no autorizan por sí mismos maniobras, pagos o trading.
