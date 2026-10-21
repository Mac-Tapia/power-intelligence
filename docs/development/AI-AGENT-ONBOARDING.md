# Onboarding de agentes (Cursor / VS Code / Claude Code / Copilot)

1. Abrir la raíz del proyecto (o el worktree de la spec), no una carpeta suelta.
2. Leer `AGENTS.md`, `.specify/memory/constitution.md`, `docs/architecture/ARCHITECTURE-INTEGRAL.md` y `docs/agents/AGENT-ROLES.md`.
3. Elegir el rol y las skills en `connectors/registry.json`; abrir la spec y los ADR de la tarea.
4. Usar `.venv` con `requirements/dev.txt`; no instalar dependencias sin autorización.
5. MCP local opcional: `python -m pip install -r tools/mcp/requirements-mcp.txt` solo con autorización. En Cursor, `.cursor/mcp.json`; en VS Code, `python scripts/agents/bootstrap_mcp.py --target vscode --write`.
6. Sincronizar skills: `python scripts/agents/sync_skills.py --target claude` (o `--target copilot`).
7. Un worktree por spec: `python scripts/dev/worktree.py new <id-spec>` (ver `SDD-WORKTREE-GUIDE.md`).
8. Antes de entregar: `python scripts/verify_structure.py`, `python scripts/agents/validate_agent_setup.py`, `python -m pytest -q` y `ruff check .`.

Ejemplo de encargo: "Lee AGENTS.md y la spec 001. Con las skills `unitesis-gis-ingestion` y `unitesis-domain-ddd`, implementa T001-T003 en `power-adapters` con pruebas sobre un VNR sintético. No inventes atributos; los faltantes van a cuarentena."
