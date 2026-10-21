# Inicio rápido: Windows + Cursor + PowerShell

1. Descomprimir el ZIP y abrir la carpeta `unitesis-power-intelligence` en Cursor.
2. Verificar `git --version` y `python --version` (recomendado Python 3.12+), luego `python scripts/verify_structure.py`.
3. Ejecutar `python -m unittest discover -s tests/bootstrap -v` y confirmar tres pruebas correctas.
4. `git init -b main; git add .; git commit -m "chore: foundation"` (configurar usuario Git si corresponde).
5. Instalar Specify CLI: `uv tool install specify-cli` (instalar uv si no está disponible). Consultar `specify version`.
6. Antes de `specify init --here --integration cursor-agent --script ps --force`, haber confirmado todos los archivos. Revisar `git diff` y restituir constitución si fue reemplazada.
7. En el chat de Cursor usar comandos Spec Kit expuestos por su versión. Comenzar por 001 y luego usar `python scripts/dev/worktree.py attach <rama-generada>` tras confirmar cambios y volver a main.

**Aún no hay aplicación de escritorio ni API iniciable**, y no hay `uv.lock`/`pnpm-lock.yaml` porque todavía no se ha resuelto un entorno con dependencias. Generar locks únicamente al implementar paquetes y comprobar plataformas, CUDA y licencias.
