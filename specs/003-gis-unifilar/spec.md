# 003 — GIS y diagrama unifilar enlazados

**Objetivo:** dos proyecciones sincronizadas del mismo grafo eléctrico sin confundir geometría y conectividad.

**Aceptación:** UUID persistente; selección bidireccional; arrastre del icono unifilar no modifica longitud GIS; edición eléctrica tiene confirmación y genera nueva revisión; trazabilidad del estado de interruptores; pruebas para feeder y red mallada.

---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-003` · **Gate:** `G2` · **Dependencias:** SPEC-010, SPEC-004.  
**Alcance verificable:** Editar y sincronizar GIS y unifilar eléctrico sin mezclar geometría geográfica y topología física.  
**Ubicación propuesta:** `apps/workstation-web/, packages/ts/map-engine/, packages/ts/one-line-engine/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-003-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-003-02:** entrada válida: Selección bidireccional y revisión editable preservan UUID, fase, interruptores, longitud GIS y rollback.
- **FR-003-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-003-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-003-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-003-01:** caso exitoso demuestra `FR-003-01/02` con fixture y evidencia automatizada.
- **AC-003-02:** caso negativo demuestra `FR-003-03`, sin alterar estado persistido ni fuente original.
- **AC-003-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-003-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
