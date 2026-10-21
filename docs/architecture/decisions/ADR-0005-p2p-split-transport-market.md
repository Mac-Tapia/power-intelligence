# ADR-0005 — Separación obligatoria: P2P transporte vs mercado energético

**Estado:** aceptado para diseño.

La red P2P transporta propuestas/evidencia entre nodos autorizados sin controlar equipos. El mercado P2P representa agentes/prosumidores y un mecanismo de asignación económica de flexibilidad/energía sujeto a la física y a la normativa vigente.

**Decisión:** dos bounded contexts (`power-p2p`, `power-market`), APIs y propietarios separados. Mensajes autenticados con identidad, autorización, anti-replay, expiración, idempotencia, cifrado, cuotas. Doble opción: API/broker central en despliegue inicial; libp2p solo si aporta independencia/replicación verificable.

La subcapa mercado opera **simulation-by-default**, no transfiere dinero ni contratos jurídicos reales. El settlement se bloquea sin validación AC, medición, consentimiento, aprobación legal/regulador/operador y aprobación humana.
