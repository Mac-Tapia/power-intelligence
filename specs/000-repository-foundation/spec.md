# 000 — Fundación de repositorio UNITESIS (propuesta aprobable)

**Objetivo:** establecer monorepo profesional SDD/CI/worktrees con dependencias acotadas, convenciones Git y baseline reproducible sin simular capacidad eléctrica inexistente.

## Criterios de aceptación

- AC-000-01: `python scripts/verify_structure.py` termina sin error si el árbol base es íntegro.
- AC-000-02: `python -m unittest discover -s tests/bootstrap -v` prueba validaciones puras.
- AC-000-03: todo componente declarado tiene propietario lógico, contrato y ubicación de test.
- AC-000-04: configuración de Git y documentación de worktrees evita colisión entre espec y rama.
- AC-000-05: no se versionan datos privados, secretos, modelo pesos ni grandes artefactos.

**Fuera del alcance:** flujos de potencia, entrenamientos y unifilares funcionales.
