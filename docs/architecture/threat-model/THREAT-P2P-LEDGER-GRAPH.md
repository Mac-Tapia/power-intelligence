# Threat model V5 — P2P / Ledger / Graph

| Superficie | Ataque | Control requerido | Prueba |
|---|---|---|---|
| Peer discovery | Sybil, eclipse | PKI allowlist, ACL, rate limits | peers desconocidos rechazados |
| Mensajes | replay/duplicados/firma falsa | nonce+TTL, inbox idempotente, firmas criptográficas | mensaje repetido no genera doble evento |
| Ledger | doble anclaje, claves, falla de consenso | idempotency, HSM/KMS, finality, auditoría | falla y recuperación sin pérdida de evidencia |
| Oráculo/medidor | falsa medición | sello tiempo, validación equipos y comparación | liquidación bloqueada sin medida válida |
| Graph query | fuga multiempresa | tenant-scoped queries, ACL, redacción | no cross-tenant leakage |
| GraphRAG | prompt injection desde fuentes | citas, whitelists, sandbox sin ejecución | documento hostil no autoriza maniobra |
| Mercado | trade físicamente inviable | prueba AC + compliance gate + aprobación | violación de tensión bloquea liquidación |

*Estas verificaciones son requisitos futuros; no se declara que la seguridad esté implementada.*
