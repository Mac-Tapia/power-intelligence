# Dependencias

- Python 3.12. Las versiones efectivamente resueltas y verificadas están en `requirements/dev.txt`. Cambiar una versión exige volver a pasar toda la suite y `ruff`.
- Cada paquete declara sus dependencias en `packages/python/*/pyproject.toml`. `power-domain` y `power-config` solo usan la stdlib.
- `pandapower` es solo la referencia de contraste (ADR-0010). Si falta, el contraste reporta `unavailable`.
- El usuario autorizó explícitamente lectores Excel (035), PyTorch (029/030), SDK MCP (015), psycopg, uvicorn y Playwright el 21/10/2026. Versiones extendidas en `requirements/extended.txt`; wheel CUDA separado en `requirements/torch-cuda124.txt`. Instaladas en `.venv` mediante `uv pip --python` (el entorno no contiene pip).
- PyTorch 2.6.0+cu124 ejecutó una operación real en la GPU local. Esto no acredita entrenamiento ni evaluación de modelos; siguen sujetos a gold y a los criterios de cada spec.
- No se versionan pesos de modelos, datos VNR-GIS reales, backups SQL ni snapshots con datos de clientes; van fuera de Git, con checksum, licencia y manifiesto.
- El frontend actual es estático y no tiene dependencias Node. Un toolchain TS solo se introduce con una spec de frontend que lo justifique.
