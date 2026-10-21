# Onboarding rápido Cursor / VS Code / agentes externos (V6)

1. Abrir la carpeta raíz del proyecto, NO una carpeta `.worktrees` aleatoria sin confirmar rama/spec.
2. Leer `AGENTS.md`, `.specify/memory/constitution.md`, `docs/agents/AGENT-ROLES.md`.
3. Seleccionar rol y skill de `connectors/registry.json`; abrir la spec/ADR correspondientes.
4. Instalar Python 3.12, Git y Node/pnpm según feature. Mantener ambientes `venv` aislados por worktree si hay dependencias diferentes.
5. El conector MCP local es *opcional*. Ejecutar `python -m pip install -r tools/mcp/requirements-mcp.txt`; requiere red y revisión de dependencias. **No se instala solo.**
6. Cursor: revisar `.cursor/mcp.json` e iniciar el servidor en ajustes MCP; permitir solo ese servidor al principio.
7. VS Code: `python scripts/agents/bootstrap_mcp.py --target vscode --write`; comprobar `.mcp.json` local antes de permitir conexión.
8. Claude Code/Copilot: `python scripts/agents/sync_skills.py --target claude` o `--target copilot`; comprobar directorios generados e integrar Spec Kit según el modo soportado.
9. Crear worktree con `python scripts/dev/worktree.py new 016-first-backend-feature` si aún no existe rama; seguir la guía `docs/development/SDD-WORKTREE-GUIDE.md`.
10. Validar scaffold: `python scripts/verify_structure.py && python scripts/agents/validate_agent_setup.py && python -m unittest discover -s tests/bootstrap -v`.

## Comandos Spec Kit

La instalación/integración de Spec Kit se realiza solo después de revisar la versión oficial y los cambios potenciales. Si `specify init --here --integration cursor-agent` modifica una constitución preexistente, inspeccionar `git diff` y restaurar el contenido intencional. Las rutas de comando varían según agente y versión; no se asumen alias universales.

## Comandos sugeridos para un agente

> Lee `AGENTS.md`, selecciona el perfil `backend` en `connectors/registry.json` y usa `unitesis-backend-fastapi`, `unitesis-domain-ddd` y `unitesis-api-contracts`. Analiza spec y contrato antes de escribir código. No habilites MCP externos ni instales dependencias sin consentimiento. Entrega el cambio en tu worktree con pruebas y evidencia reproducible.

> Lee la spec de workstation y el perfil `frontend`. Diseña un flujo tipo DIgSILENT con vistas GIS y unifilar sincronizadas por `snapshot_id` y `asset_id`, estados de loading/error/empty, accesibilidad y cliente OpenAPI generado. Construye componentes en `apps/workstation-web` y `packages/ts` sin duplicar el solver.
