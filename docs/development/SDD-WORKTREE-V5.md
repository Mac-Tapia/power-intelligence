# Flujo Spec Kit + Git Worktrees para features 010–014

Mantener un worktree por feature y no compartir directorios de entornos entre worktrees. La constitución y ADRs se versionan en ramas/PR; cambios de contrato requieren revisión de owners.

```powershell
# Desde la carpeta principal después de inicializar git con commit
python scripts/dev/worktree.py new 010-electrical-graph
python scripts/dev/worktree.py new 011-p2p-federation
python scripts/dev/worktree.py new 012-ledger-evidence
python scripts/dev/worktree.py new 013-p2p-energy-market
python scripts/dev/worktree.py new 014-graphrag-knowledge
```

Antes de ejecutar, consultar `python scripts/dev/worktree.py --help` y `docs/development/SDD-WORKTREE-GUIDE.md`. **No ejecutar aquí** sin repositorio Git inicializado. Los feature IDs corresponden a carpetas `specs/<feature-id>/` que tienen `spec.md`, `plan.md`, `tasks.md`. El uso de `git worktree` es Git nativo, no un requisito obligatorio de Spec Kit.

Orden de integración: 010 → (011 en paralelo al baseline de 012) → 013 condicionado por 004 → 014. Cualquier modificación del núcleo requiere PR con traceability, tests y ADR.
