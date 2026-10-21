# ADR-0007 — Agent Skills y MCP con principio de menor privilegio

**Estado:** propuesto, sujeto a revisión de seguridad.

## Contexto
El proyecto incluye agentes LLM científicos y SDD, pero no un inventario portable de habilidades especializadas ni un esquema explícito de permisos para herramientas de desarrollo. Backend y frontend necesitan mecanismos de consulta, pruebas y trazabilidad sin acceso irrestricto a datos de empresa.

## Decisión
- Skills en `.agents/skills` según Agent Skills con progresive disclosure y sync por cliente; `AGENTS.md` como política base.
- Conectores MCP en registry con `read`, `test`, `execute-sandbox`, `write` y aprobación por perfil; no se conceden credenciales por selección de rol.
- Solo activar por defecto MCP local de lectura de documentación en rutas permitidas; las integraciones GitHub, Browser, PostgreSQL y repos científicos son opt-in.
- No MCP directo a SCADA, SQL de escritura, producción, wallets privadas ni sistemas de protección. Las API de ejecución científica se exponen por interfaces de negocio con validación/autorización externa al LLM.
- Validación automatizada de SKILL.md, registry y reglas de configuración; seguridad adicional aplicada a nivel real de cuentas/roles y red.

## Alternativas
Todo a través de MCP: descartado por crecimiento de superficie de ataque y acoplamiento. Skills embebidos en prompts: descartado por falta de versionado. Privilegios globales: descartado.

## Consecuencias
Agentes de distintos IDEs comparten conocimiento; herramientas externalizadas requieren revisión de proveedor y scopes; onboarding necesita sincronizar skills en clientes que no leen `.agents/skills`.
