# Dependencias

- Python 3.12. Las versiones efectivamente resueltas y verificadas están en `requirements/dev.txt`. Cambiar una versión exige volver a pasar toda la suite y `ruff`.
- Cada paquete declara sus dependencias en `packages/python/*/pyproject.toml`. `power-domain` y `power-config` solo usan la stdlib.
- `pandapower` es solo la referencia de contraste (ADR-0010). Si falta, el contraste reporta `unavailable`.
- Dependencias pendientes de autorización por spec: lectores Excel `openpyxl`/`xlrd`/`pyxlsb` (029), `torch` (006/007) y el SDK MCP (015).
- No se versionan pesos de modelos, datos VNR-GIS reales, backups SQL ni snapshots con datos de clientes; van fuera de Git, con checksum, licencia y manifiesto.
- El frontend actual es estático y no tiene dependencias Node. Un toolchain TS solo se introduce con una spec de frontend que lo justifique.
