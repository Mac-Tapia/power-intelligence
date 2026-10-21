# Tasks — SPEC-029: sciml-pinn-gnn

## Backlog del plan maestro — tareas pendientes

**Gate:** G5 · **Depende de:** SPEC-008, SPEC-028, SPEC-038

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-029/T201** — Diseñar dataset derivado de VNR-GIS y casos de entrenamiento con licencia/autorización.  
  **Estado:** parcial · **Evidencia:** dataset desde 44 alimentadores reales CYME con autorización; VNR pendiente · **Responsable:** por asignar
- [x] **SPEC-029/T202** — Definir residuales AC completos P/Q, unidades, fases, topología y límites adecuados.  
  **Estado:** cumplida · **Evidencia:** power_mismatch + verificación del residuo de cada etiqueta · **Responsable:** por asignar
- [ ] **SPEC-029/T203** — Entrenar baseline MLP/PINN y GNN con arquitectura y loss transparentes.  
  **Estado:** pendiente · **Evidencia:** PyTorch disponible; entrenamiento GNN/PINN pendiente · **Responsable:** por asignar
- [ ] **SPEC-029/T204** — Separar sets por tiempo/red/topología; prevenir leakage y registrar semillas.  
  **Estado:** parcial · **Evidencia:** split por alimentador con semilla; temporal pendiente · **Responsable:** por asignar
- [ ] **SPEC-029/T205** — Comparar velocidad/precisión frente a solver determinista por tipo de red.  
  **Estado:** parcial · **Evidencia:** línea base física vs solver (benchmarks/sciml); sin modelo aprendido · **Responsable:** por asignar
- [ ] **SPEC-029/T206** — Implementar detector OOD, rechazo seguro y registro reproducible de modelos.  
  **Estado:** parcial · **Evidencia:** rechazo seguro vía certificación del solver; sin detector OOD ni registro de modelos · **Responsable:** por asignar
- [ ] **SPEC-029/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-029/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-029/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-029/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.

## Avance incorporado de la numeración anterior

- [x] T029-S01: generador de escenarios (`unitesis_sciml.pf_scenarios`) con el modelo de demanda declarado (kVA conectado × U(u_min,u_max) × LogNormal(σ) × fp), registrado en el manifiesto. _(antes T006-01)_
- [x] T029-S02: dataset por alimentador en `.npz` (nodos eléctricos fusionados, aristas con R/X en p.u. desde la Y-bus compartida, P/Q, etiquetas V/θ/pérdidas) y manifiesto releído (`unitesis_application.pf_dataset`, CLI `build-pf-dataset`). Red real Electro Dunas: 44 alimentadores, 2 173 de 2 200 escenarios etiquetados (27 sin convergencia por carga extrema, contados); 215/215 contrastes pandapower aprobados. _(antes T006-02)_
- [x] T029-S03: residuo AC de cada etiqueta verificado con `power_mismatch` (máx. 2.9e-7 p.u., umbral declarado 1e-6; las muestras que lo superan se descartan). _(antes T006-03)_
- [ ] T029-S04: autorización para instalar `torch`; modelo GNN base (GraphSAGE/GAT) con pérdida física. _(antes T006-04)_
- [ ] T029-S05: protocolo. Hecho: split por alimentador (30/6/8), métrica común `surrogate_metrics` y línea base física `pf_baselines` (`benchmarks/sciml/baseline-linear_*`: test p95 0.041 p.u., recall 0.94, no pasa AC-029-S02). Falta: evaluar el GNN (T029-S04) con la misma métrica. _(antes T006-05)_
- [x] T029-S06: puerto `SurrogateEngine` y uso con confirmación obligatoria por el solver (capacidad remanente, T002-03). La línea base física está conectada; el GNN usará el mismo puerto. El acuerdo sustituto-solver se mide y se publica. _(antes T006-06)_
- [ ] T029-D09: `pf-scenarios-pe-ica-electrodunas` construido como dataset **candidato** desde la red real TXT (44 alimentadores, 2 173 muestras, manifiesto en `local-data/datasets/`). Pasa a gold cuando se confirme la autorización (T035-D05); MDB y VNR se agregan con T001-T011/T003. _(antes T029-09)_

## Destilación (ADR-0011)

- [x] T029-K01: módulo de destilación (procedencia de maestros, pérdida α/β/γ, escenarios sin etiquetar, evaluación por alimentador con alumno de control). Evidencia: `power-sciml/distillation.py`, `tests/unit/test_distillation.py`.
- [x] T029-K02: caso de uso y CLI `distill-pf-surrogate` con evidencia verificada y pesos en `local-data`. Evidencia: `power-application/distillation_study.py`.
- [x] T029-K05: prior físico lineal sobre la misma Y-bus como entrada y punto de partida (aprendizaje residual), residuo AC normalizado por alimentador y entrenamiento por etapas. Primer intento sin prior: divergió (errores de 10-60 p.u.) y quedó registrado. Resultado real (caso piloto, 44 alimentadores, split por alimentador, 60 épocas): maestro GraphSAGE de 33 538 parámetros con p95 test 0,0090 p.u. y recall 1,0 (la línea base lineal da 0,041). Alumno de 6 498 parámetros destilado: p95 valid 0,0098 frente a 0,0206 sin maestro; en test, 0,0203 frente a 0,0211. **Ningún modelo pasa todavía AC-029-S02 (p95 ≤ 0,005).** Evidencia local: `local-data/evidence/distillation-*.json`.
- [x] T029-K06: GNN con impedancias (`edge_gnn.py`), selección por validación sin consultar el test y dataset de 200 escenarios por alimentador (8 705 muestras, 885 contrastes aprobados, 0 fallidos). Resultados (test evaluado una sola vez por corrida): con 50 escenarios y 60 épocas se eligió GraphSAGE 64×4 (p95 valid 0,00516, test 0,0090); con 200 escenarios y 30 épocas, el GNN con impedancias 32×6 (valid 0,0072, test 0,0119). El GNN con impedancias no supera a GraphSAGE porque el prior lineal ya aporta la impedancia. En ninguna corrida el alumno destilado supera al alumno entrenado directamente en test. **Gate AC-029-S02 no superado.**
- [ ] T029-K07: cerrar la brecha validación-test, que es de generalización entre alimentadores (6 de validación, 8 de test): validación cruzada por grupos de alimentadores, curriculum por tamaño de alimentador, presupuesto de épocas con parada temprana por validación, y más alimentadores (los 77 validados, incluidos los de marco de fases, con etiquetas trifásicas).
- [ ] T029-K03: destilar sobre el dataset gold temporal cuando exista (hoy: candidato por escenarios de demanda) y fijar el umbral de aceptación del alumno con revisión humana.
- [ ] T029-K04: destilación con etiquetas en marco de fases (008-C) para alimentadores desbalanceados.
