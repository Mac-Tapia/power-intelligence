# 002 — Impacto de nueva carga en red de distribución

**Estado:** cribado equilibrado operativo (`scripts/unitesis.py new-load`, `POST /api/v1/studies/new-load`, pestaña "Nueva carga" de la workstation). El estudio completo por fase depende de 004‑C.

**Dependencias:** 001 (red real del caso), 004‑A (operativo) / 004‑C (por fase), perfiles de carga gold del caso (029), perfil regulatorio del caso.

**Alcance:** clonar el snapshot, asignar una nueva demanda real al nodo o equipo de conexión aprobado, simular antes y después, y comparar cargabilidad, tensión (por fase cuando exista 004‑C), pérdidas, capacidad remanente, alternativas y CAPEX/OPEX trazables.

## Criterios de aceptación

- AC-002-01: la carga nueva actúa sobre un escenario clonado. El snapshot de origen no cambia (hash idéntico antes y después) y la barra de conexión debe existir; nunca se infiere.
- AC-002-02: ningún `StudyResult` sale sin versión del solver, convergencia, unidades, hash de entradas y estado de contraste. La aceptación técnica es `false` hasta la revisión humana.
- AC-002-03: si faltan parámetros, la simulación se rechaza con un reporte (código de salida 2), nunca con valores supuestos de potencia por alimentador.
- AC-002-04: los criterios de cribado (V mínima, cargabilidad máxima) son explícitos en la solicitud y se registran en la evidencia.
- AC-002-05: las alternativas de mitigación pasan la validación física del solver propio y el contraste independiente (spec 005).
