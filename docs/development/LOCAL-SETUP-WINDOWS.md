# Entorno local (Windows + VS Code/Cursor + PowerShell)

1. Python 3.12 en `.venv` con las versiones de `requirements/dev.txt` (no actualizarlas sin autorización).
2. Verificar: `.venv\Scripts\python scripts/verify_structure.py`, `.venv\Scripts\python -m pytest -q` y `.venv\Scripts\ruff check .`.
3. Ejecutar la plataforma local: `.venv\Scripts\python scripts/unitesis.py serve` → http://127.0.0.1:8000/ (solo localhost; usa uvicorn si está instalado o un puente de la stdlib si no).
4. Datos del caso de aplicación: fuentes registradas en `config/datasets/sources.v2.json`. Los datos reales viven en `local-data/reference/` o en el archivo de donantes, nunca en Git.
5. SQL Server Express local (opcional, spec 001): restaurar los backups VNR-GIS solo en bases nuevas y en lectura; no modificar bases existentes.
6. Trabajo en paralelo: un worktree por spec (`python scripts/dev/worktree.py`), según `SDD-WORKTREE-GUIDE.md`.
