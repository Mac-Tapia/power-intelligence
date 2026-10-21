# 005 — Expansión: conductores, SED, BESS, DER y EV

**Estado:** parcial. Ya operativo: alternativas de conductor por línea, con contraste independiente y ranking por VPN (`unitesis_application.alternatives`). Paquetes: `power-optimization` y `power-economics`.

## Criterios de aceptación

- AC-005-01: toda alternativa se evalúa en un escenario clonado y la confirma el solver propio más un contraste independiente. Sin contraste aprobado no hay ranking.
- AC-005-02: costos, tasa, horizonte, precio de energía y factor de pérdidas son explícitos y tienen fuente. Sin costo, la alternativa se reporta "sin valorar".
- AC-005-03: con varios objetivos (VPN, pérdidas, cargabilidad, CO2) se publica el frente de Pareto, no un único ganador.
- AC-005-04: un sustituto de la spec 006 puede priorizar candidatos, pero la decisión la confirma el solver.
