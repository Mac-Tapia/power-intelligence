# 000 — Fundación de repositorio UNITESIS (propuesta aprobable)

**Objetivo:** establecer monorepo profesional SDD/CI/worktrees con dependencias acotadas, convenciones Git y baseline reproducible sin simular capacidad eléctrica inexistente.

## Criterios de aceptación

- AC-000-01: `python scripts/verify_structure.py` termina sin error si el árbol base es íntegro.
- AC-000-02: `python -m pytest -q` prueba validaciones puras.
- AC-000-03: todo componente declarado tiene propietario lógico, contrato y ubicación de test.
- AC-000-04: configuración de Git y documentación de worktrees evita colisión entre espec y rama.
- AC-000-05: no se versionan datos privados, secretos, modelo pesos ni grandes artefactos.
- AC-000-06: inventario reproducible con hash, función, módulo propietario, specs existentes e importadores; componentes desconocidos fallan el control, sin borrado automático.
- AC-000-07: inventario excluye secretos, entornos y destinos de symlinks; local-data solo se resume con cantidades y bytes, sin nombres de clientes.

**Fuera del alcance:** flujos de potencia, entrenamientos y unifilares funcionales.

---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-000` · **Gate:** `G0` · **Dependencias:** ninguna.  
**Alcance verificable:** Mantener base monorepo, separación hexagonal y herramientas de desarrollo reproducibles.  
**Ubicación propuesta:** `scripts/, .github/, .specify/, .cursor/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-000-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-000-02:** entrada válida: Un checkout limpio pasa verificación, CI y tests de arranque sin credenciales externas.
- **FR-000-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-000-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-000-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-000-01:** caso exitoso demuestra `FR-000-01/02` con fixture y evidencia automatizada.
- **AC-000-02:** caso negativo demuestra `FR-000-03`, sin alterar estado persistido ni fuente original.
- **AC-000-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-000-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
