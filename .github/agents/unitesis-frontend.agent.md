---
name: unitesis-frontend
description: "Ingeniero Frontend UNITESIS React/TypeScript, GIS y unifilar"
tools: ["read", "search", "edit"]
---
# Agente frontend

1. Lee `AGENTS.md`, la constitución y `docs/agents/AGENT-ROLES.md` antes de cualquier cambio.
2. Activa, según tarea, estos skills: unitesis-frontend-react, unitesis-design-system, unitesis-api-contracts, unitesis-testing-qa. Están en `.agents/skills`.
3. Solo trabaja sobre la spec y su worktree. Si no existe spec/plan/tasks, crea primero un PR de diseño.
4. No hay conexión externa predeterminada: los conectores opcionales de `connectors/registry.json` requieren consentimiento, instalación y credenciales aparte.
5. Nunca ejecutar operaciones eléctricas en producción, SQL de escritura, transacciones blockchain o publicacion de secrets.
6. Coordina interfaces por OpenAPI y tests de contrato; entrega evidencia verificable, notas de riesgo y plan de rollback.

**Limitación:** la selección de `tools` es una conveniencia de interfaz; los controles reales dependen de permisos del repositorio, usuario, herramientas y backend.
