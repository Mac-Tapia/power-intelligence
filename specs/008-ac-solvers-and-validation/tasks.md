# Tasks — SPEC-008: ac-solvers-and-validation

## Backlog del plan maestro — tareas pendientes

**Gate:** G3 · **Depende de:** SPEC-006, SPEC-007, SPEC-010

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [x] **SPEC-008/T201** — Especificar contrato PowerFlowInput/Output incluyendo modelo de fases, slack y unidades.  
  **Estado:** cumplida · **Evidencia:** snapshot v4 por fase (`network.py`), `UnbalancedStudyResult`, `contracts/schemas/json/unbalanced-study-evidence.v1.schema.json` · **Responsable:** por asignar
- [ ] **SPEC-008/T202** — Crear adaptador OpenDSS/DSS-Extensions y motor pandapower donde cobertura aplicable.  
  **Estado:** parcial · **Evidencia:** adaptador pandapower; sin OpenDSS · **Responsable:** por asignar
- [x] **SPEC-008/T203** — Validar consistencia de datos y faltantes antes de cualquier ejecución del solver.  
  **Estado:** cumplida · **Evidencia:** cuarentena y rechazo de alcance antes de resolver · **Responsable:** por asignar
- [x] **SPEC-008/T204** — Ejecutar pruebas feeder de referencia radial, mallado y desbalanceado con tolerancias justificadas.  
  **Estado:** cumplida · **Evidencia:** `benchmarks/power-flow/results.json` (IEEE 33 radial/mallado, MT/BT) y `unbalanced-results.json` (IEEE 13: 32 tensiones publicadas, máx. 0,28 V con tolerancias de GridLAB-D); `tests/unit/test_three_phase.py` · **Responsable:** por asignar
- [x] **SPEC-008/T205** — Persistir versión solver, hash inputs/snapshot, residuos, iteraciones y flags de convergencia.  
  **Estado:** cumplida · **Evidencia:** versión, hashes, residuo, iteraciones y convergencia en StudyResult/evidencia · **Responsable:** por asignar
- [ ] **SPEC-008/T206** — Rechazar reportes con fallas físicas; comparar resultados frente a mediciones donde existan.  
  **Estado:** parcial · **Evidencia:** resultados fallidos nunca 'computed'; comparación con mediciones pendiente · **Responsable:** por asignar
- [ ] **SPEC-008/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-008/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-008/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-008/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.

## Avance incorporado de la numeración anterior

- [x] T008-A1: BFS radial equilibrado + adaptador pandapower + comparador con prueba de independencia. Alimentador sintético de 6 barras: diferencias máximas V 1.6e-13 p.u., ángulo 3.4e-13°, corriente 1.0e-11 A, pérdidas 3.8e-15 MW (pandapower 3.5.5). _(antes T004-A1)_
- [ ] T008-A3: revisión humana de licencias, código y resultados del alcance A; aceptación técnica registrada (no se cierra automáticamente). _(antes T004-A3)_
- [x] T008-B1: Y-bus compartida (`unitesis_simulation.ybus`, con el residuo AC que reutilizará la spec 029) y Newton-Raphson propio, para redes radiales y malladas (`NewtonRaphsonEngine`, CLI `--engine nr`). Benchmark `benchmarks/power-flow/results.json` frente a pandapower: 6 barras, IEEE 33 radial y mallada, con diferencia de tensión ≤ 1.1e-14 p.u. y 3-4 iteraciones. IEEE 33 reproduce a Baran & Wu (Vmin 0.9131 p.u. en B18, 202.7 kW). Pruebas: `tests/unit/test_newton_raphson.py`. _(antes T004-B1)_
- [x] T008-B2: transformador de dos devanados (`Transformer`: vk/vkr, relación por tensiones nominales, tap en AT, desfase de grupo) en la Y-bus compartida y el Newton-Raphson, con arranque plano que propaga los desfases. Snapshot v3 = v2 + transformadores; los snapshots sin transformadores conservan su hash v2. Contraste pandapower en 5 casos de tap/desfase/relación y en la fixture MT/BT (ΔV ≤ 1e-13 p.u.). El adaptador de referencia declara `tap_changer_type` (pandapower 3 ignora taps sin él) y usa arranque DC con desfases (el arranque plano converge a una solución espuria). El BFS los rechaza explícitamente. Rama magnetizante: pendiente. Pruebas: `tests/unit/test_transformers.py`. _(antes T004-B2)_
- [x] T008-C1: modelo por fase (snapshot v4), constantes de línea propias (Carson/Kron, neutro concéntrico), motor trifásico propio (Z-bus implícito), reguladores ideales, YNyn0, cargas ZIP estrella/delta; IEEE 13 contra valores publicados; equivalencia con NR. Evidencia: `three_phase.py`, `line_constants.py`, `benchmarks/power-flow/unbalanced-results.json`, `tests/unit/test_three_phase.py`. _(antes T004-C)_
- [ ] T008-C2: IEEE 123, transformadores Dyn, control automático de reguladores (compensación de línea) y contraste con un motor de fases independiente (OpenDSS vía DSS-Extensions, requiere autorización de dependencia).
- [ ] T008-C3: lectura CYME por fase (matrices desde valores de secuencia declarados en el catálogo) para los alimentadores con laterales no trifásicos.
