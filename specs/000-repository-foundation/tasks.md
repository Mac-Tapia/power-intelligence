# Tasks — Fundación

- [x] T001 Definir dominios y directorios con READMEs de responsabilidad.
- [x] T002 Añadir constitución y guía Spec Kit / Cursor / Git.
- [x] T003 Añadir workflow de CI para baseline.
- [x] T004 Añadir herramienta worktree con validación de rama y limpieza segura.
- [x] T005 Probar invariantes de dominio (no potencia eléctrica).
- [ ] T006 Activar GitHub repo remote, rulesets y CODEOWNERS reales.
- [ ] T007 Instalar Specify CLI en máquina de destino y regenerar integración Cursor.
- [x] T008 Motores propios y contraste independiente pandapower conectados para alcance equilibrado (spec 008-A/B1, `tests/unit/test_simulation.py`, `tests/unit/test_newton_raphson.py` y estudio CLI con evidencia releída). No acredita cobertura multifase ni cortocircuito.

- [x] T009 Inventario reproducible de archivos/propietarios/specs/importadores, sin secretos ni nombres de datos locales (`scripts/dev/project_inventory.py`, `tests/governance/test_project_inventory.py`). Un archivo sin dueño bloquea la verificación; no se elimina automáticamente.

## Backlog del plan maestro — tareas pendientes

**Gate:** G0 · **Depende de:** ninguna

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-000/T201** — Auditar requisitos de Python, uv, Node, pnpm, Git y herramientas de Cursor en Windows.  
  **Estado:** parcial · **Evidencia:** docs/development/LOCAL-SETUP-WINDOWS.md; sin Node/pnpm (UI estática) · **Responsable:** por asignar
- [ ] **SPEC-000/T202** — Establecer lockfiles reproducibles y validar instalaciones limpias sin rutas personales.  
  **Estado:** parcial · **Evidencia:** requirements/dev.txt y extended.txt fijados; sin uv.lock · **Responsable:** por asignar
- [x] **SPEC-000/T203** — Ejecutar y corregir verificación estructural y matrices de dependencias entre paquetes.  
  **Estado:** cumplida · **Evidencia:** scripts/verify_structure.py; scripts/dev/project_inventory.py (sin commit, sesión de plataforma) · **Responsable:** por asignar
- [ ] **SPEC-000/T204** — Configurar GitHub CODEOWNERS, branch protection y PR template según acceso real.  
  **Estado:** parcial · **Evidencia:** .github/CODEOWNERS y PR template; protección de rama no configurada en GitHub · **Responsable:** por asignar
- [ ] **SPEC-000/T205** — Comprobar creación y desmontaje seguro de Git worktrees sin pérdida de cambios.  
  **Estado:** parcial · **Evidencia:** scripts/dev/worktree.py sin prueba dedicada · **Responsable:** por asignar
- [x] **SPEC-000/T206** — Documentar configuración reproducible, fallo controlado y evidencia de revisión para repository-foundation.  
  **Estado:** cumplida · **Evidencia:** README.md, docs/development/*, AGENT-COORDINATION.md · **Responsable:** por asignar
- [ ] **SPEC-000/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-000/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-000/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-000/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.
