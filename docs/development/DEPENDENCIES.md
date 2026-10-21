# Dependencias y locks

- Python 3.12 como objetivo de baseline de desarrollo, antes de conectar GPU/solvers verificar matriz de compatibilidad Windows/Linux.
- Paquetes individuales: `packages/python/*/pyproject.toml`; `uv.lock` único **generado**, no falsificar lock.
- Frontend: `pnpm-workspace.yaml`, manifests TS; generar `pnpm-lock.yaml` cuando existan dependencias verificadas.
- Pesos de modelos, datos VNR-GIS reales, SQL backups y snapshots no van a Git. Almacenar en object store con checksum, licencia y manifiesto.
- Pinar versiones efectivamente resueltas de dependencias y revisar vulnerabilidades y licencias antes de producción.
- No copiar un enorme requirements.txt con todas las librerías de investigación desde el día cero.
