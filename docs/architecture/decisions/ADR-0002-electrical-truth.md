# ADR-0002: la verdad eléctrica no depende del LLM

- **Estado:** Aceptada como regla de investigación y seguridad.
- **Decisión:** snapshot de red, datos con origen, solver determinista y evidencia de validación son autoritativos. GNN/PINN/MARL son aproximadores o exploradores y nunca certifican por sí solos un resultado.
- **Consecuencias:** cada recomendación tiene `run_id`, referencias, tolerancias, estado de convergencia y revisión humana antes de ejecutar maniobras reales.
