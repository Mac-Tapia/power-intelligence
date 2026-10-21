---
name: unitesis-devops-observability
description: "Preparar CI/CD, telemetría, rastreabilidad y despliegue gradual. Úsalo al trabajar en infra/"
---
# unitesis-devops-observability

## Activación
Preparar CI/CD, telemetría, rastreabilidad y despliegue gradual.

## Lecturas obligatorias
`AGENTS.md`, `.specify/memory/constitution.md`, `docs/architecture/MODULE-BOUNDARIES.md`, spec vigente y ADR relacionados. Revisar también `docs/agents/AGENT-ROLES.md`.

## Procedimiento
1. Definir SLO, dependencia de datos, migraciones y política de artefactos.
2. Implementar quality gates, logs JSON con trace_id/job_id/snapshot_id, OpenTelemetry, health/readiness, colas reintentables e idempotencia. Infra como código, SBOM, imágenes sin root y despliegue progresivo con rollback.
3. Escribir o actualizar pruebas y evidencias por ID de tarea de `specs/` antes de cerrar el PR.
4. Ejecutar la verificación aplicable: `python scripts/verify_structure.py`. Si falta un comando o entorno, registrar el bloqueo y no afirmar que la prueba pasó.

## Límites no negociables
No introducir Kubernetes por defecto ni habilitar despliegue productivo automático desde agentes.

## Alcance
infra/; .github/workflows/; workers/

## Entrega
Resumen de cambios, decisiones, artefactos, pruebas ejecutadas realmente, errores, riesgos abiertos y vínculo al PR/spec.


## Fuentes de investigación
Antes de implementar, consultar `docs/scientific-evidence/modules/ops.md`, `docs/scientific-evidence/modules/arch.md`, `docs/scientific-evidence/modules/security.md`, además de `docs/scientific-evidence/MATRIX-MODULES.md`. Validar ficha y tipo de evidencia, documentar fuente y experimento en la spec. Nunca tratar referencias pendientes o abstracts como validación de producto.
