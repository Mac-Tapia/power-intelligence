# Matriz de roles y permisos de agentes — UNITESIS V6

Cada agente opera en su propio **git worktree** y con herramientas **mínimas**, nunca con todos los conectores a la vez. El perfil define qué skills puede descubrir y qué conectores puede **solicitar**, no concede acceso automático.

| Rol | Producto entregable | Rutas principales | Gate | 
|---|---|---|---|
| architect | ADR + C4 + plan revisado | docs/architecture, specs | Dependencias y riesgos aprobados |
| backend | API contract-first + casos de uso | apps/control-api, packages/python | Contrato y RBAC/ABAC verificados |
| frontend | workstation accesible con GIS/unifilar | apps/workstation-web, packages/ts | Contrato + Playwright + accesibilidad |
| gis-topology | ingesta y grafo canónico | packages/python/power-topology | Fidelidad GIS/CRS/topología |
| power-solver | estudios AC y benchmarks | packages/python/power-simulation | Tolerancias golden + convergencia |
| sciml | entrenamiento PINN/GNN | packages/python/power-sciml | Baselines + OOD + error físico |
| marl-llm | estrategias en sandbox | packages/python/power-marl, power-agents | Solo propuesta, solver valida |
| graph-rag | grafo documental y citas | packages/python/power-graphrag | Proveniencia + aislamiento tenant |
| p2p-ledger | federación/ledger simulado | packages/python/power-p2p, power-ledger | Permisos, replay, no datos on-chain |
| devops | CI, despliegue reproducible | .github, infra | Sin acceso productivo por defecto |
| qa | validación integral | tests, benchmarks | Evidencia reproducible |
| researcher | revisión bibliográfica | docs/research, docs/reference | DOI/fecha/fuente verificados |

El catálogo JSON de `connectors/registry.json` es la fuente de verdad de la relación agente → skills → MCPs. En PR se documenta qué conectores estuvieron habilitados, con qué alcance y para qué tarea.

## Separación de responsabilidades

- Architect no fusiona cambios de otros sin review de code owner.
- Backend no ejecuta simulaciones ni ML en handlers HTTP; solo jobs.
- Frontend no reimplementa reglas eléctricas; consulta API versionada y visualiza evidencia.
- LLM nunca tiene acceso a credenciales de DB de escritura, SCADA, o wallet/clave de ledger.
- Un agente de datos no descarga VNR privados o SQL de empresa sin mandato explícito.
- QA puede bloquear un PR por cobertura negativa insuficiente; CI no puede ser omitido.
