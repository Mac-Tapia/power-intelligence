# 015 — Skills y conectores de agentes (Spec V6)

**Objetivo:** habilitar agentes IA para implementación segura de backend, frontend y módulos científicos con instrucciones portables y conectores de mínimo privilegio.

## Requerimientos
- REQ-015-01: Cada skill debe seguir Agent Skills con `name` y `description` únicos, más pasos, prohibiciones y pruebas.
- REQ-015-02: La matriz agente → skill → MCP define status y permiso, denegado por defecto.
- REQ-015-03: El conector local solo lee specs, ADRs y documentación allowlisted; bloquea traversal, symlinks, rutas fuera del root, binarios y archivos enormes.
- REQ-015-04: Cursor tendrá configuración MCP sin secretos; VS Code podrá generar configuración portable sin duplicados.
- REQ-015-05: Worktree por tarea y sincronización reproducible de skills para clientes compatibles.
- REQ-015-06: Backend y frontend tienen guías separadas: contratos-first, API tipada y E2E.
- REQ-015-07: Cualquier conector externo queda optional/planned hasta conectar, autenticar, revisar publisher y probar en sandbox.
- REQ-015-08: Pruebas negativas de exposición de credenciales, rutas fuera de allowlist y escritura sin autorización.

## Escenarios
- Given agente backend, when revisa plan, then identifica skill, contrato y pruebas sin privilegios extra.
- Given agente frontend, when cambia unifilar, then consulta OpenAPI y ejecuta E2E local (si dependencias instaladas).
- Given `../../.env` como lectura MCP, then es rechazado antes de tocar disco fuera de allowlist.
- Given `connectors/registry.json`, when se valida, then roles no referencian skills o conectores inexistentes.
- Given la ausencia de servidor GitHub/Playwright/Postgres, then sus configuraciones se documentan pero NO se presentan como conectadas.

## Fuera de alcance
Integración efectiva con SCADA, despliegue de blockchain, ejecución de flujos eléctricos, despliegue de agentes en nube, conexión de bases de terceros.
