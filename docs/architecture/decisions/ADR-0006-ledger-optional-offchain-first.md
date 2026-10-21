# ADR-0006 — Evidencia off-chain y ledger permissioned opcional

**Estado:** aceptado para diseño; blockchain es decisión condicionada por evaluación de confianza, coste y operaciones.

Almacenar entradas brutas y resultados verificados fuera de cadena. Ledger solo registra hashes de evidencia, referencias pseudonimizadas, autorizaciones y estado de acuerdos. Prohibido colocar SCADA en tiempo real, PII, credenciales, topología sensible, datos comerciales confidenciales o cálculos AC dentro de contratos.

**Alternativas:** auditoría append-only central con firmas (baseline), Hyperledger Fabric (endorsement y colecciones privadas), Hyperledger Besu QBFT (smart contracts EVM). Solo se escoge blockchain si múltiples entidades autónomas exigen gobernanza compartida. Nunca conectarlo a protecciones o comandos SCADA.

Diseño `EvidenceStore`/`LedgerAnchorPort`: commit local -> outbox -> anclaje asíncrono -> finality check -> read model. Fallos de blockchain no bloquean estudios eléctricos ni safety interlocks. Comparar rendimiento, complejidad, privacidad y fallo BFT.
