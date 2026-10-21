# ADR-0010 — Motores propios, sin APIs CYME/PowerFactory

- **Estado:** aceptada (mandato del usuario, 20/10/2026).
- **Decisión:** el cálculo productivo usa motores propios (`power-simulation`). Quedan excluidos `cympy`, el módulo `powerfactory`, COM/ComLdf, la automatización de sus GUI y cualquier worker que requiera instalaciones o licencias de CYMDIST/CYME o DIgSILENT PowerFactory. Tampoco se incorporan implementaciones de esas APIs desde proyectos donantes (marcadas `excluded_proprietary_api` en `docs/traceability/contribution-registry.json`).
- **Permitido:** lectores offline de archivos (p. ej. DGS o exportaciones de texto) que no ejecuten esos programas; una herramienta abierta de contraste (pandapower) con estado explícito (`unavailable` si falta), que nunca se convierte en dependencia oculta de cálculo.
- **Control permanente:** `tests/security/test_no_proprietary_engines.py` falla si el runtime del núcleo importa o invoca esas APIs.
- **Consecuencias:** cada capacidad nueva del motor necesita su propio benchmark independiente (spec 004, AC-004-03).
