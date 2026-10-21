# Coordinación entre agentes

Varios agentes (Claude Code, Codex, Copilot u otros) pueden trabajar a la vez sobre el mismo árbol. Estas reglas evitan que se pisen el trabajo.

## Tablero vivo

`local-data/coordination/BOARD.md` (fuera de Git, compartido en disco) es el único tablero de trabajo en curso. Cada agente lo lee **antes** de editar y lo actualiza al empezar y al terminar.

Cada reclamo indica el agente o sesión, las specs y tareas, los archivos o carpetas que reclama, el estado (`trabajando`, `listo para commit`, `liberado`) y la hora.

## Reglas

1. **Reclamar antes de editar.** No se edita un archivo reclamado por otro agente. Si se necesita, se anota un pedido en el tablero (sección *Pedidos*) y se espera a que el dueño lo libere o lo acepte.
2. **Propiedad por capas y specs.** El dueño de cada área está en la tabla de abajo; un archivo compartido (p. ej. `apps/control-api/src/unitesis_api/main.py`) se cambia con reclamo explícito y el cambio más pequeño posible (un router o módulo nuevo, en vez de reescribir).
3. **Commits solo de lo propio.** Nunca `git add -A` ni `git commit -a` mientras haya trabajo ajeno sin commitear: se añaden rutas explícitas. Antes de commitear, `git status` y `git diff --cached --stat` para comprobar que no entra nada ajeno.
4. **Sin reescrituras destructivas.** Nada de `reset --hard`, `checkout --` sobre archivos ajenos, `stash` del trabajo de otro ni rebases de ramas compartidas.
5. **Verificación compartida.** Antes de liberar: `python scripts/verify_structure.py`, `ruff check .` y `python -m pytest -q`. Si una prueba ajena falla por un cambio propio, se corrige el cambio propio o se avisa en el tablero; no se desactiva la prueba.
6. **Specs como contrato.** Las tareas se marcan `[x]` solo con evidencia; si dos agentes cubren una misma spec, cada uno marca sus tareas y deja en el tablero qué falta.
7. **Al terminar.** Commit propio, estado `liberado` en el tablero y una línea con lo que queda para el siguiente agente.

## Propiedad vigente por área (actualizable en el tablero)

| Área | Specs | Rutas principales |
|---|---|---|
| Plataforma y gobierno | 000, 009, 015 | `apps/control-api`, `scripts/dev`, `scripts/agents`, `tools/mcp`, `.github`, `Makefile`, `job_repository.py`, `JobRepository` |
| Núcleo eléctrico, datos e IA | 001, 002, 003, 004, 005, 006, 007, 029 | `power-domain`, `power-topology`, `power-simulation`, `power-adapters` (importadores), `power-optimization`, `power-economics`, `power-sciml`, `power-application`, `scripts/datasets`, `scripts/benchmarks`, `scripts/fixtures`, `config/cases`, `config/datasets` |
| Compartido con reclamo | — | `apps/workstation-web`, `README.md`, `AGENTS.md`, `docs/architecture/*`, `docs/traceability/FEATURE-MAP.md`, `unitesis_ports/protocols.py`, `scripts/unitesis.py` |
