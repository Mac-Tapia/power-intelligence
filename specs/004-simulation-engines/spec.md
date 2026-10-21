# 004 — Motores de simulación propios

**Estado:** 004-A y 004-B1 operativos; 004-B2 a 004-D pendientes. Paquete dueño: `power-simulation`. Motores propietarios excluidos (ADR-0010).

## Alcances

- **004-A (operativo):** flujo AC radial equilibrado por barrido atrás/adelante; una slack; cargas PQ; líneas serie; interruptores ideales; contraste con pandapower bajo las tolerancias de `docs/architecture/CONTRACTS-AND-EVIDENCE.md`.
- **004-B1 (operativo):** Newton-Raphson propio sobre la Y-bus compartida, para redes radiales y malladas, con interruptores ideales fusionados.
- **004-B2:** transformadores MT/BT con impedancia y tap. Es requisito de la spec 006 con alimentadores reales.
- **004-C:** trifásico desbalanceado por fase (A/B/C/N), cargas monofásicas.
- **004-D:** cortocircuito IEC 60909 simplificado.

## Criterios de aceptación

- AC-004-01: cada motor declara su capacidad. Un snapshot con elementos fuera de ella se rechaza con la lista de elementos; nunca se simplifica en silencio.
- AC-004-02: la Y-bus vive en `power-simulation` y la reutilizan el solver, el residuo físico de la spec 006 y el comparador. No hay dos formulaciones.
- AC-004-03: cada alcance se contrasta con una referencia abierta (pandapower u OpenDSS mediante adaptador) en casos IEEE (13/33/123 nodos) y sintéticos, con las tolerancias de `docs/architecture/CONTRACTS-AND-EVIDENCE.md`. Los casos IEEE validan el motor; no son datos de entrenamiento. El resultado se publica en `benchmarks/power-flow/`.
- AC-004-04: un caso no convergente devuelve `failed` con su residuo; un motor ausente devuelve `unavailable`.
