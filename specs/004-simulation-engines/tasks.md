# Tareas 004

- [x] T004-A1: BFS radial equilibrado + adaptador pandapower + comparador con prueba de independencia. Alimentador sintético de 6 barras: diferencias máximas V 1.6e-13 p.u., ángulo 3.4e-13°, corriente 1.0e-11 A, pérdidas 3.8e-15 MW (pandapower 3.5.5).
- [x] T004-A2: contratos `ElectricalSnapshot` v2, `StudyRequest/Result`, evidencia releída y esquemas validados (`docs/architecture/CONTRACTS-AND-EVIDENCE.md`).
- [ ] T004-A3: revisión humana de licencias, código y resultados del alcance A; aceptación técnica registrada (no se cierra automáticamente).
- [ ] T004-A4: retirar `NetworkSnapshot` v1 de `power-domain` (hoy solo lo usa `tests/governance`), dejando una única identidad eléctrica.
- [x] T004-B1: Y-bus compartida (`unitesis_simulation.ybus`, con el residuo AC que reutilizará la spec 006) y Newton-Raphson propio, para redes radiales y malladas (`NewtonRaphsonEngine`, CLI `--engine nr`). Benchmark `benchmarks/power-flow/results.json` frente a pandapower: 6 barras, IEEE 33 radial y mallada, con diferencia de tensión ≤ 1.1e-14 p.u. y 3-4 iteraciones. IEEE 33 reproduce a Baran & Wu (Vmin 0.9131 p.u. en B18, 202.7 kW). Pruebas: `tests/unit/test_newton_raphson.py`.
- [ ] T004-B2: transformador de dos devanados (impedancia, tap, grupo) en el snapshot v2 → v3, con migración.
- [ ] T004-C: modelo por fase y cargas desbalanceadas; contraste IEEE 13/123.
- [ ] T004-D: cortocircuito IEC 60909.
