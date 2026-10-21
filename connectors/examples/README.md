# Catálogo de conectores externos — plantillas, no conectados

Los JSON de esta carpeta son **ejemplos inactivos** y no deben combinarse automáticamente con `.cursor/mcp.json`. Revisar versiones/canales oficiales antes de instalarlos. No cargar tokens en Git.

- GitHub: servidor oficial github/github-mcp-server, herramienta read-only y scopes estrictos. Ref: https://github.com/github/github-mcp-server
- Playwright: microsoft/playwright-mcp; usar solo pruebas locales y staging. Ref: https://github.com/microsoft/playwright-mcp
- PostgreSQL: microsoft/postgres-mcp o adapter auditado, identidad SQL RO y acceso a staging. Ref: https://github.com/microsoft/postgres-mcp
- Otros candidatos (QGIS, MLflow, Grafana, blockchain, GitHub Actions) requieren evaluación y no se incluyen como conectores activos.

Secuencia: validar seguridad → instalar entorno aislado → conectar credenciales en vault/variables → aprobar acceso → smoke test → registrar evidencia de ejecución.
