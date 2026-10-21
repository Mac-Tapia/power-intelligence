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
