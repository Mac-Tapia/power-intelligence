# SPEC-004 — fullstack-runtime

**Propósito:** Crear backend FastAPI y frontend React operativos, con contratos y entorno local reproducible.


---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-004` · **Gate:** `G0` · **Dependencias:** SPEC-000.  
**Alcance verificable:** Crear backend FastAPI y frontend React operativos, con contratos y entorno local reproducible.  
**Ubicación propuesta:** `apps/control-api/, apps/workstation-web/, infra/compose/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-004-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-004-02:** entrada válida: API responde health/readiness, UI carga rutas reales, OpenAPI genera cliente TypeScript y CI ejecuta build completo.
- **FR-004-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-004-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-004-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-004-01:** caso exitoso demuestra `FR-004-01/02` con fixture y evidencia automatizada.
- **AC-004-02:** caso negativo demuestra `FR-004-03`, sin alterar estado persistido ni fuente original.
- **AC-004-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-004-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.

## Criterios vigentes incorporados (antes spec 009)

**Estado:** parcial. Además del perfil SQLite durable, están probados el perfil bearer local con roles/tenant, PostgreSQL/PostGIS con worker en otro proceso, trazas y backup/restauración nativos. La recuperación distribuida de workers interrumpidos, el empaquetado reproducible y la aceptación productiva siguen pendientes. Las pruebas locales no cierran por sí solas AC-004-I01..04.

### Criterios de aceptación

- AC-004-I01: autenticación y autorización por rol y tenant antes de cualquier exposición fuera de localhost.
- AC-004-I02: jobs persistentes (cola) y repositorio PostgreSQL/PostGIS con las mismas reglas append-only (`infra/db/postgres`).
- AC-004-I03: observabilidad (logs estructurados sin datos de clientes, métricas y trazas) y recuperación probada.
- AC-004-I04: empaquetado reproducible (lockfile y contenedor) y CI con todas las suites.

### Entrega local durable (subalcance, no cierra PostgreSQL ni producción)

- AC-004-L1: jobs en SQLite sobreviven reapertura; claim atómico único; terminales inmutables y solicitudes JSON completas. Sin pickle ni valores no finitos.
- AC-004-L2: inicio interrumpido queda failed/interrupted, queued permanece queued; no hay reejecución automática. Perfil local de un proceso API; no iniciar dos servidores contra el mismo archivo.
- AC-004-L3: estudio, nueva carga y alternativas se consultan después de reiniciar; fallo público usa código estable sin secretos ni traceback.
- AC-004-L4: backup SQLite y restauración a archivo nuevo comprueban integridad, esquema y conteos; nunca sobreescriben una base existente; la recuperación preserva restricciones append-only.
- AC-004-L5: perfil bearer opcional valida hash, rol, caducidad y tenant; 401 sin credencial, 403 sin rol de escritura, almacenes independientes por tenant. El tenant proviene de la credencial, nunca de datos de la solicitud.
