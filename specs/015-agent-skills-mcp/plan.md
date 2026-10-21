# Plan 015 — SDD skills y MCP

1. Establecer ADR-0007 y roles con permisos mínimos.
2. Definir 20 skills siguiendo Agent Skills, en raíz portable `.agents/skills`.
3. Crear registro JSON de conectores y perfiles; validator con pruebas negativas.
4. Implementar conector MCP de lectura de documentación con SDK oficial y helpers testeables sin SDK.
5. Añadir configuración Cursor y plantilla portable para VS Code, con generador sin secretos.
6. Añadir sync idempotente skills a `.claude/skills` y `.github/skills` cuando el usuario lo solicite.
7. Integrar verificaciones en CI y con SDD/git-worktree.
8. Después de aprobación: instalar GitHub read-only, Playwright sandbox, PostgreSQL ro; comprobar conexiones reales.
9. Redactar blueprint backend/frontend como guía, sin confundirlo con apps terminadas.

## Plan ejecutable — SPEC-015

**Gate de entrega:** G0 · **Dependencias aprobadas:** SPEC-000.

1. **Modelo/contratos:** definir request, response, objetos de dominio y política de validación en `.agents/skills/, connectors/, scripts/agents/`; separar entidades y DTO.
2. **Arquitectura:** casos de uso sin ORM/HTTP/LLM, puertos tipados y adaptadores reemplazables; usar monolito modular + workers para procesos intensivos.
3. **Persistencia y eventos:** migraciones/backups si hay estado; claves tenant, revisión y hash de procedencia; idempotencia para trabajos.
4. **API/Frontend:** exponer solo endpoints necesarios; OpenAPI versionado, cliente TS generado y UI con carga/error/ausencia de datos; controles no autorizados deben quedar inaccesibles.
5. **Algoritmo:** Habilitar skills y MCP para agentes de programación con privilegios mínimos y sin acceso directo a producción. Nunca simular valores reales cuando faltan datos.
6. **Pruebas:** unitarias puras, contratos, integración aislada, fixtures reales autorizados o sintéticos etiquetados y E2E si corresponde.
7. **Métricas:** Skills localizables y MCP local RO probado; conectores externos denegados por defecto y se auditan sus permisos. Parámetros numéricos/tolerancias se pactan usando benchmarks y se versionan antes de aprobar.
8. **Evidencias:** informe de testing, fuente científica/regulatoria, changelog, hash del input, salida y revisión del responsable.

**Skills/RAG sugerido:** usar skill del módulo y consultar `docs/scientific-evidence` mediante `python scripts/research/query_evidence.py --module agents --limit 10`; si el módulo no está registrado, buscar por palabra clave y registrar ausencia de evidencia.

**Riesgos y controles:** acceso empresarial autorizado, exactitud física, dependencia normativa, evolución de contrato, presupuesto de cómputo y regresión. No usar secretos, datos privados ni herramientas destructivas sin permisos explícitos.
