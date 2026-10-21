# Contratos

- `schemas/json/`: esquemas versionados. Vigentes e implementados: `study-evidence.v1`, `new-load-evidence.v1`, `alternatives-evidence.v1` (validados contra payloads reales en `tests/contract/`). Borradores de las specs 010-013: `graph-projection.v1`, `p2p-envelope.v1`, `p2p-energy-trade.v1`, `ledger-anchor.v1`. Spec 020/024: `regulatory-study`.
- `events/`: eventos P2P y ledger (specs 011/012), con causación, correlación y compatibilidad por versión.
- OpenAPI: lo genera `apps/control-api` en `/openapi.json`; no se mantiene una copia manual.
- Unidades explícitas (kV, MW, MVAr, kA, ohm/km, p.u., CRS) en cada esquema; no se asumen unidades implícitas.

Detalle de identidades, estados y tolerancias: `docs/architecture/CONTRACTS-AND-EVIDENCE.md`.
