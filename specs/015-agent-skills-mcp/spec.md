# 015 — Skills y conectores de agentes

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
- REQ-015-09: el generador portable selecciona el intérprete del entorno del proyecto si existe y, en su defecto, el intérprete ejecutor; no utiliza un `python` global ambiguo ni declara handshake por generar configuración.

## Escenarios
- Given agente backend, when revisa plan, then identifica skill, contrato y pruebas sin privilegios extra.
- Given agente frontend, when cambia unifilar, then consulta OpenAPI y ejecuta E2E local (si dependencias instaladas).
- Given `../../.env` como lectura MCP, then es rechazado antes de tocar disco fuera de allowlist.
- Given `connectors/registry.json`, when se valida, then roles no referencian skills o conectores inexistentes.
- Given la ausencia de servidor GitHub/Playwright/Postgres, then sus configuraciones se documentan pero NO se presentan como conectadas.

## Fuera de alcance
Integración efectiva con SCADA, despliegue de blockchain, ejecución de flujos eléctricos, despliegue de agentes en nube, conexión de bases de terceros.

---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-015` · **Gate:** `G0` · **Dependencias:** SPEC-000.  
**Alcance verificable:** Habilitar skills y MCP para agentes de programación con privilegios mínimos y sin acceso directo a producción.  
**Ubicación propuesta:** `.agents/skills/, connectors/, scripts/agents/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-015-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-015-02:** entrada válida: Skills localizables y MCP local RO probado; conectores externos denegados por defecto y se auditan sus permisos.
- **FR-015-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-015-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-015-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-015-01:** caso exitoso demuestra `FR-015-01/02` con fixture y evidencia automatizada.
- **AC-015-02:** caso negativo demuestra `FR-015-03`, sin alterar estado persistido ni fuente original.
- **AC-015-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-015-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
