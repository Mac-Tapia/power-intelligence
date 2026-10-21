# Tareas 006

- [x] T006-01: generador de escenarios (`unitesis_sciml.pf_scenarios`) con el modelo de demanda declarado (kVA conectado × U(u_min,u_max) × LogNormal(σ) × fp), registrado en el manifiesto.
- [x] T006-02: dataset por alimentador en `.npz` (nodos eléctricos fusionados, aristas con R/X en p.u. desde la Y-bus compartida, P/Q, etiquetas V/θ/pérdidas) y manifiesto releído (`unitesis_application.pf_dataset`, CLI `build-pf-dataset`). Red real Electro Dunas: 44 alimentadores, 2 173 de 2 200 escenarios etiquetados (27 sin convergencia por carga extrema, contados); 215/215 contrastes pandapower aprobados.
- [x] T006-03: residuo AC de cada etiqueta verificado con `power_mismatch` (máx. 2.9e-7 p.u., umbral declarado 1e-6; las muestras que lo superan se descartan).
- [ ] T006-04: autorización para instalar `torch`; modelo GNN base (GraphSAGE/GAT) con pérdida física.
- [ ] T006-05: protocolo. Hecho: split por alimentador (30/6/8), métrica común `surrogate_metrics` y línea base física `pf_baselines` (`benchmarks/sciml/baseline-linear_*`: test p95 0.041 p.u., recall 0.94, no pasa AC-006-02). Falta: evaluar el GNN (T006-04) con la misma métrica.
- [ ] T006-06: integración como puerto `SurrogateEngine` con confirmación obligatoria por el solver.
