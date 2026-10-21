# UNITESIS Power Intelligence

**Plataforma de ingeniería y planificación eléctrica con GIS, gemelo digital y computación científica.**

> Estado: **esqueleto estructural verificable, NO software eléctrico operativo**. El scaffold no calcula flujos, no importa VNR-GIS real y no ejecuta PINN/MARL. Toda capacidad se libera únicamente tras cumplir su especificación, pruebas y revisión.

## Primer objetivo vertical

`Fuente VNR-GIS autorizada -> Bronze/Silver -> grafo por terminal/fase -> GIS + unifilar -> completar parámetros -> nuevo cliente -> solver de referencia -> antes/después -> evidencia -> informe`.

## Estructura

- `apps/`: interfaz profesional y API de control.
- `packages/python/`: dominios, casos de uso, puertos, adaptadores y motores independientes.
- `packages/ts/`: contratos y componentes frontend.
- `workers/`: procesos de larga duración CPU/GPU/solvers, nunca en peticiones HTTP.
- `specs/` + `.specify/`: especificaciones SDD versionadas.
- `docs/`: C4, ADR, arquitecturas, contratos, trazabilidad y operaciones.
- `fixtures/` y `tests/`: casos sintéticos/abiertos y verificaciones.
- `scripts/`: herramientas de bootstrap y worktrees seguros.

## Primeras comprobaciones sin instalar dependencias

```powershell
python scripts/verify_structure.py
python -m unittest discover -s tests/bootstrap -v
python scripts/dev/worktree.py list
```

## Activación de GitHub Spec Kit (Cursor)

1. Crea un commit de esta estructura en Git para conservar los archivos antes de inicializar herramientas.
2. Instala Spec Kit y ejecuta `specify init --here --integration cursor-agent --script ps --force` **revisando la diferencia después**. Esto puede regenerar `.specify/` y `.cursor/`; recupera la constitución del commit si resultó reemplazada.
3. Si deseas ramas gestionadas desde Spec Kit: `specify extension add git` (según tu versión instalada).
4. Sigue las especificaciones (`/speckit-specify`, `/speckit-clarify`, `/speckit-plan`, `/speckit-checklist`, `/speckit-tasks`, `/speckit-analyze`, `/speckit-implement`, `/speckit-converge`). Las denominaciones visibles pueden variar por versión e integración.
5. No ejecutes `specify init` en cada worktree. Inicializa una vez, confirma los archivos generados y luego crea worktrees.

Ver `docs/development/SDD-WORKTREE-GUIDE.md` y `docs/architecture/MODULE-BOUNDARIES.md`.

## Extensión V5 — Graph, P2P y Blockchain

Esta versión añade **cinco bounded contexts nuevos** (`power-graph`, `power-p2p`, `power-ledger`, `power-market`, `power-graphrag`) y especificaciones SDD `010`–`014` con planes, tareas, schemas y pruebas de invariantes. **Ningún comercio P2P, libp2p, red blockchain o grafo DB de producción está desplegado**.

- Arquitectura: [`docs/architecture/GRAPH_P2P_BLOCKCHAIN_V5.md`](docs/architecture/GRAPH_P2P_BLOCKCHAIN_V5.md).
- Worktrees: [`docs/development/SDD-WORKTREE-V5.md`](docs/development/SDD-WORKTREE-V5.md).
- Contracts: `contracts/schemas/json/{graph-projection,p2p-envelope,p2p-energy-trade,ledger-anchor}.v1.schema.json`.
- Pruebas: `python -m unittest discover -s tests/bootstrap -v`.

## V6: Skills, conectores MCP y blueprint full-stack

Se agregaron **20 skills compatibles con Agent Skills**, perfiles técnicos, registro MCP con modo `deny`, conector local de lectura de documentación, un blueprint detallado de backend/frontend, script para preparar MCP portable y pruebas de seguridad del scaffold.

- `docs/agents/SKILLS-AND-CONNECTORS.md`: política, roles y configuración.
- `docs/architecture/BACKEND-FRONTEND-BLUEPRINT_V6.md`: diseño objetivo FastAPI + React, contratos y seguridad.
- `specs/015-agent-skills-mcp/`: spec, plan y tareas SDD.
- `.agents/skills/*/SKILL.md`: habilidades portables por tecnología.
- `connectors/registry.json`: qué puede solicitar cada agente (no activa conexiones).

Comprobar:
```bash
python scripts/verify_structure.py
python scripts/agents/validate_agent_setup.py
python -m unittest discover -s tests/bootstrap -v
```
Para ejecutar el servidor MCP **después de instalar voluntariamente el SDK oficial**:
```bash
python -m pip install -r tools/mcp/requirements-mcp.txt
# Cursor consume .cursor/mcp.json; verificar estado en Cursor > MCP
# VS Code: generar .mcp.json portable y local
python scripts/agents/bootstrap_mcp.py --target vscode --write
```
La V6 no instala paquetes de terceros, no conecta servicios externos, no implementa las aplicaciones ni despliega infraestructura.


## Biblioteca científica V7 para todos los agentes

**191 fichas Markdown originales** con fuentes enlazadas, organizadas por 18 dominios y mapeadas a 20 Agent Skills. Punto de entrada: [`docs/scientific-evidence/INDEX.md`](docs/scientific-evidence/INDEX.md).

```powershell
python scripts/research/validate_library.py
python scripts/research/query_evidence.py --module sciml --limit 10
```

Las fichas no incluyen el texto completo de publicaciones y su estatus bibliográfico está marcado; las fuentes originales exigen comprobación antes de ser citadas en una tesis o informe regulatorio.

## UNITESIS V8 — PIT, PIDE, economía y PMBOK 6
Lea `docs/regulatory/INDEX.md`, `PIDE-ANNEX1-STATUS.md`, `SOURCES.json`, y `docs/project-management/PMBOK6-UNITESIS-MAPPING.md` antes de estudiar inversiones o agregar reglas de cumplimiento. Norma 217-2013 SST/SCT ≠ metodología PIDE; bloquea certificación de borradores. El perfil 217 original requiere consolidar todas sus modificatorias. La biblioteca V7 sigue vigente.

## V8.1 PIDE distribución
Se documentó la prepublicación oficial 2017 y se agregó un perfil metodológico histórico separado del proceso regulatorio FONAFE. Leer `docs/regulatory/PIDE-2017-PREPUBLICACION-EL-PERUANO.md` antes de utilizar PIDE.

## PIDE V8.2: auditoría de fuentes y motor de referencia
Leer `docs/regulatory/pide_2017/INDEX.md`. CLI de ejemplo: `python scripts/pide/evaluate_reference.py --input fixtures/pide/reference_case_synthetic.json`. Los formatos originales 01–15 siguen bloqueados hasta recuperar el Anexo MINEM.

## Consolidación del workspace — revisión 20/10/2026

[Spec 028](specs/028-workspace-consolidation/spec.md), [revisión arquitectónica y limpieza](specs/028-workspace-consolidation/architecture-review.md) y [tareas con estado](specs/028-workspace-consolidation/tasks.md). Definen aportes por módulo, contratos y criterios de integración/eliminación. El núcleo continúa en fase de estructura y auxiliares; esta revisión no implementa ni acepta un solver eléctrico.
