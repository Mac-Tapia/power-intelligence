# Desarrollo dirigido por especificaciones + Git Worktrees (Windows/Cursor)

## Instalar herramientas

- Windows: Git, Python 3.12+ (para scripts de desarrollo), `uv`, Cursor; Node/pnpm solo al abrir frontend. Motores/GPU no son requisito para el scaffold.
- GitHub oficial: https://github.com/github/spec-kit
- Documentación: https://github.github.com/spec-kit/quickstart.html
- Git worktree: https://git-scm.com/docs/git-worktree.html

```powershell
cd unitesis-power-intelligence
git init -b main
git add .
git commit -m "chore: establish SDD monorepo architecture"
uv tool install specify-cli
# Advertencia: --force puede regenerar archivos; revisión obligatoria con git diff.
specify init --here --integration cursor-agent --script ps --force
specify check
# Funcionalidad de Git en Spec Kit, si está disponible para tu versión:
specify extension add git
```

Luego revisar `git diff`, recuperar la constitución `git show HEAD:.specify/memory/constitution.md` si la plantilla generada cambió los principios del proyecto, y confirmar el resultado. Los comandos de Spec Kit se ejecutan **en el chat del agente**, no como PowerShell.

## Orden recomendado: spec-first y worktree posterior

1. En Cursor desde el repo principal: `/speckit-constitution` (solo para fijar reglas) y `/speckit-specify` para `001-vnrgis-ingestion`. Si la integración genera la rama, **no** crear esa misma rama con `git worktree add -b`.
2. Crear/revisar especificación y escenarios de aceptación (`spec.md`); confirmar los archivos en la rama `001-vnrgis-ingestion` con Git.
3. Volver a `main` en el checkout principal; enlazar la rama existente:

```powershell
# Dentro del repositorio raíz, después de guardar y confirmar el spec:
git switch main
python scripts/dev/worktree.py attach 001-vnrgis-ingestion
# Se crea ../unitesis-worktrees/001-vnrgis-ingestion/
code -n ../unitesis-worktrees/001-vnrgis-ingestion
```

4. En Cursor abierto en **ese worktree**, continuar con `/speckit-clarify`, `/speckit-plan`, `/speckit-checklist`, `/speckit-tasks`, `/speckit-analyze`, `/speckit-implement`, `/speckit-converge` (según versión).
5. Ejecutar unit, contract, benchmark y validación; crear PR de esa rama (CI + code review), fusionar a `main`.
6. Una vez fusionado y el worktree esté limpio: `python scripts/dev/worktree.py remove 001-vnrgis-ingestion`; la rama se borra **solo después** por operación Git separada si ya se fusionó.

**Alternativa:** si manejas Git sin que Spec Kit cree ramas, crea un worktree nuevo con `python scripts/dev/worktree.py new 002-new-load-impact`, y configura explícitamente la característica en tu integración para evitar que `specify` intente recrear la rama. El ciclo predeterminado es **spec-first**, para evitar la colisión de ramas.

## Reglas de concurrencia

- Un PR/feature = una spec + una rama + un worktree (convención UNITESIS, no restricción universal de Git).
- No editar dos veces el mismo checkout desde agentes simultáneos.
- Las carpetas worktree deben estar **fuera del repositorio**, de modo que Git no las versione.
- Las instalaciones y artefactos por worktree son independientes; nunca compartir `.venv` activa dentro del árbol.
- No lanzar cambios concurrentes en contratos/capa canónica sin coordinación y pruebas de compatibilidad.
- Un branch reusado solo puede estar activo en un worktree por vez; `git worktree list` informa ubicación.
- `git worktree remove` rehúsa un worktree sucio salvo que se fuerce; este scaffold **nunca** usa `--force`.

## Extensiones comunitarias de worktree

GitHub Spec Kit lista extensiones comunitarias de worktree, pero no son parte obligatoria del núcleo. Instalar solo tras auditoría de código/versión/permisos. **No se verificó una implementación oficial específica atribuible a MoureDev**, así que las órdenes aquí usan Git nativo y la integración oficial documentada de Spec Kit.
