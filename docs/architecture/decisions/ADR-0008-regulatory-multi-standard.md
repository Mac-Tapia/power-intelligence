# ADR-0008 — Regulatorio multimarco versionado

**Estado:** propuesto para aprobación arquitectónica.

## Contexto
217-2013 trata SST/SCT y PIT; PIDE de distribución FONAFE requiere metodología separada, con borrador en 2017 y pendiente en 2025. PMBOK 6 gestiona proyectos y no crea umbrales eléctricos.

## Decisión
Contextos delimitados `power-regulation`, `power-economics`, `power-projects`, sin reglas hardcoded en agentes, front ni solvers. Fuentes y cláusulas por `source_id`, estado, `effective_from/to`, ámbito y validación humana.

## Consecuencias
- Aumentan validaciones por estudio pero se evita certificación falsa.
- Un borrador es insumo de investigación, no regla exigible.
- El motor regulatorio consume outputs de solvers independientes y puede marcar `blocked`.
- Separar modelo normativo de cálculo y flujo de aprobación humana.
