# Preparación integral — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** integrar y completar UNITESIS por entregas verificables; el primer lote proporciona inventario repetible, jobs locales durables y recuperación comprobada.

**Architecture:** monolito modular existente, puertos tipados y adaptadores separados. El primer lote mantiene el perfil local con SQLite; no cierra el criterio PostgreSQL de 007 ni habilita exposición externa. La ejecución de cálculos conserva el solver y contraste actuales.

**Tech Stack:** Python 3.12, stdlib (`sqlite3`, `ast`, `hashlib`, `pathlib`), FastAPI/Pydantic y pytest ya instalados. Sin instalación ni actualización de dependencias en este lote.

**Spec:** `docs/development/READINESS-AND-CLEANUP.md`, aprobado el 21/10/2026; specs dueñas 000, 004/005/007/031 (antes 009) y 015. Estado de este plan: aprobado por el usuario el 21/10/2026; primer lote implementado y verificado mediante ejecución directa.

## Global Constraints

- “El código no contiene supuestos de país, empresa, frecuencia, CRS, moneda ni norma.”
- “Se conserva el solver propio como confirmación física.”
- “Solo se eliminan cachés regenerables o duplicados cuya identidad y falta de necesidad estén demostradas.”
- “Ningún candidato se considera integrado por existir en dicho registro.”
- “Las dependencias nuevas o actualizadas requieren autorización explícita conforme a `AGENTS.md`, regla 9”.
- Preservar el cambio previo de `cyme_ascii.py`, datos y fuentes locales; no copiar donantes con licencia pendiente.
- `technical_acceptance` continúa independiente del éxito de ejecución. No cambiar los umbrales eléctricos.
- No modificar esquemas eléctricos v2, fuentes autorizadas ni ámbito productivo en el primer lote.

## Review Focus

1. Archivos dinámicos y documentación sin imports: clasificarlos como soporte, sin inferir que son basura (tarea 1).
2. Symlinks, entorno y secretos durante inventario: no recorrer ni leer sus destinos/contenidos (tarea 1).
3. Caída entre inicio y finalización del cálculo: registrar interrupción; nunca publicar éxito ni repetir automáticamente (tareas 2–3).
4. Dos ejecutores sobre el mismo job: un solo claim atómico; transiciones obsoletas rechazadas (tarea 2).
5. Backup corrupto o destino existente: fallar sin sobrescribir datos (tarea 4).

## Lote 1: base local verificable

### Tarea 1 — Inventario de integración reproducible (spec 000)

**Files:** crear `scripts/dev/project_inventory.py` y `tests/governance/test_project_inventory.py`; actualizar `specs/000-repository-foundation/spec.md`, `tasks.md`, `Makefile` y `docs/development/READINESS-AND-CLEANUP.md`.

**Interfaces:** `build_inventory(root: Path) -> dict[str, Any]`; `main(argv: list[str] | None = None) -> int`. CLI: `python scripts/dev/project_inventory.py --root . --output local-data/diagnostics/inventory.json`.

Inventariar rutas relativas, tamaño, SHA-256 de archivos de producto, categoría y consumidores de imports `unitesis_*` mediante AST. Para `local-data`, registrar únicamente cantidad y tamaño agregado por subcarpeta; no publicar nombres de clientes. Excluir `.git`, `.venv`, cachés y secretos; enumerar symlinks como tales sin seguirlos. Leer Git mediante subprocess con argv y `-C`, sin shell. La ausencia de Git retorna error explícito, no un inventario completo ficticio. La salida debe estar bajo `local-data/` y publicarse atómicamente; no ofrecer opción de borrado.

- [x] Agregar a 000 los criterios de inventario repetible, privacidad y separación entre candidato e integrado.
- [x] Escribir pruebas: un archivo UI sin imports se conserva como soporte; un módulo con consumidor AST registra ese consumidor; un archivo privado en `.env` nunca aparece con contenido/hash; un symlink no se recorre; el destino fuera de `local-data` se rechaza; dos ejecuciones sin cambios producen el mismo conjunto de rutas y hashes.
- [x] Ejecutar `.venv/Scripts/python.exe -m pytest tests/governance/test_project_inventory.py -q`; comprobar fallo por implementación ausente.
- [x] Implementar las interfaces y añadir `inventory` al Makefile, sin modificar `doctor` ni introducir dependencias.
- [x] Repetir las pruebas y ejecutar la CLI sobre el proyecto real. Comparar los hashes de archivos versionados con el inventario previo; explicar diferencias por archivos añadidos, sin borrar aportes candidatos.

### Tarea 2 — Almacén durable de jobs (avance de T007-I02)

**Files:** crear `packages/python/power-adapters/src/unitesis_adapters/job_repository.py`, `tests/unit/test_job_repository.py`; añadir puerto a `packages/python/power-ports/src/unitesis_ports/protocols.py`; actualizar `specs/009-industrialization/spec.md` y `tasks.md`.

**Interfaces:** protocolo `JobRepository` y adaptador `SqliteJobRepository(path: str | Path)` con `enqueue(job_id: str, kind: str, request: dict[str, Any]) -> dict[str, Any]`, `get(job_id: str) -> dict[str, Any]`, `claim(job_id: str) -> bool`, `finish(job_id: str, outcome: dict[str, Any]) -> dict[str, Any]`, `fail(job_id: str, error_code: str) -> dict[str, Any]`, `recover_interrupted() -> int`, `close() -> None`.

Guardar solicitud JSON completa de estudio/nueva carga/alternativas para trazabilidad; no serializar dataclasses con pickle. `queued → running → finished|failed`; recuperación `running → failed` con `error_code=interrupted`. Los jobs queued siguen queued tras reinicio; no lanzarlos automáticamente. Terminales inmutables. Identificadores repetidos con contenido distinto producen conflicto; repetición idéntica es idempotente. Usar parámetros SQL, transacciones y conexiones por operación en archivo. Admitir `:memory:` para las pruebas existentes sin prometer persistencia en ese modo.

- [x] Especificar el subalcance local durable; mantener T007-I02 global abierta hasta probar PostgreSQL y worker independiente.
- [x] Escribir pruebas: reabrir archivo conserva request/outcome; dos repositorios simultáneos obtienen exactamente un claim; finish sin claim falla; terminal no se puede reemplazar; contenido distinto bajo mismo ID falla; recuperación afecta solo running; fallo no contiene secretos ni traceback.
- [x] Ejecutar `.venv/Scripts/python.exe -m pytest tests/unit/test_job_repository.py -q` y comprobar fallo inicial.
- [x] Implementar puerto y adaptador; `get` desconocido lanza `KeyError`, conflicto/transición inválida `ValueError`; JSON rechaza NaN/Infinity.
- [x] Repetir las pruebas con SQLite en archivo temporal y conexiones independientes. Verificar que el repositorio eléctrico append-only existente no se modifica ni elimina.

### Tarea 3 — API consume el almacén durable (avance de 007)

**Files:** modificar `apps/control-api/src/unitesis_api/main.py`; crear `tests/integration/test_durable_jobs.py`; actualizar `apps/control-api/README.md`.

**Interfaces:** conservar `create_app(db_path: str | Path | None = None) -> FastAPI`, endpoints y campos públicos actuales. Construir `SqliteJobRepository` sobre el mismo archivo elegido para snapshots; reemplazar el diccionario `jobs`. `_enqueue` persiste antes de agendar BackgroundTasks; `_run` exige claim, ejecuta y persiste terminal antes de responder a consultas. Ningún handler hace cálculo eléctrico. Exponer repositorios en `app.state` y cerrarlos mediante lifespan.

Las solicitudes almacenadas de alternativas contienen `catalog_id`, hash de catálogo y base económica JSON, nunca objetos Python serializados. No reproducir jobs interrumpidos. Mantener bloqueo de arranque sin `UNITESIS_LOCAL_ONLY=1` y restricción de host CLI. Un error público usa código genérico, sin interpolar excepciones que puedan contener rutas/datos privados.

- [x] Escribir pruebas: app A importa snapshot y calcula estudio; app B reabre el mismo archivo, consulta el job y ambos resultados con contraste passed; repetir para nueva carga y alternativas. Simular running persistido y comprobar fallo interrupted al iniciar app B. Job inexistente retorna 404. Sin bandera local no arranca.
- [x] Ejecutar `.venv/Scripts/python.exe -m pytest tests/integration/test_durable_jobs.py -q` y demostrar que el reinicio pierde jobs en el código previo.
- [x] Conectar repositorio, claim y recuperación; mantener respuestas de las pruebas de integración actuales.
- [x] Repetir pruebas nuevas y `tests/integration/test_study_vertical.py`, `tests/integration/test_integral_platform.py`. Verificar cierre de conexiones y reapertura real de archivo.

### Tarea 4 — Backup y restauración verificables (avance de T031-I03)

**Files:** crear `scripts/dev/database_backup.py`, `tests/integration/test_database_recovery.py`; actualizar `specs/007-durable-jobs-and-events/tasks.md`, `apps/control-api/README.md`.

**Interfaces:** `backup_database(source: Path, destination: Path) -> dict[str, Any]`, `restore_database(source: Path, destination: Path) -> dict[str, Any]`; CLI con subcomandos `backup` y `restore`, ambos con `--source` y `--destination`.

SQLite backup API, destino nuevo y distinto del origen; validación de integridad antes y después; publicación atómica; SHA-256 final y conteos de snapshots/resultados/jobs. Rechazar origen ausente, esquema ajeno, symlink, destino existente y destino fuera de `local-data/` en CLI. Restaurar solo a archivo nuevo, nunca sustituir la base activa. No afirmar recuperación PostgreSQL.

- [x] Escribir pruebas: ejecutar estudio real, hacer backup, restaurar a archivo nuevo y abrir otra app; consultar job/resultados y releer snapshot con digest igual. Un backup corrupto falla sin crear destino; destino existente conserva sus bytes; origen ausente no genera base vacía.
- [x] Ejecutar `.venv/Scripts/python.exe -m pytest tests/integration/test_database_recovery.py -q` y comprobar fallo inicial.
- [x] Implementar backup/restauración y CLI. Registrar resultados sin contenido privado en `local-data/diagnostics/`.
- [x] Repetir pruebas y comprobar restricciones append-only también en la base restaurada.

### Tarea 5 — Selección correcta de intérprete MCP (spec 015)

**Files:** modificar `scripts/agents/bootstrap_mcp.py`, `tests/governance/test_agents_mcp.py`, documentación de onboarding localizada mediante `rg bootstrap_mcp docs`.

**Interfaces:** conservar `generate() -> dict`. `command` apunta al intérprete `.venv/Scripts/python.exe` en Windows o `.venv/bin/python` en POSIX si existe; sin entorno local, usar `sys.executable`, nunca la cadena ambigua `python`. Mantener un único servidor de lectura y ruta absoluta del script.

- [x] Escribir prueba del intérprete efectivo y que el generador no habilita conectores externos ni inserta secretos.
- [x] Ejecutar `.venv/Scripts/python.exe -m pytest tests/governance/test_agents_mcp.py -q` y comprobar fallo de la selección actual.
- [x] Implementar selección y documentar que configurar intérprete no acredita SDK ni handshake; T015-07 continúa abierta.
- [x] Repetir suite específica y `scripts/agents/validate_agent_setup.py`.

### Tarea 6 — Verificación conjunta y estado honesto

**Files:** actualizar README, `docs/architecture/ARCHITECTURE-INTEGRAL.md`, `docs/traceability/FEATURE-MAP.md`, tareas 000/004/005/007/031/015 y este plan únicamente con evidencia ejecutada.

- [x] Ejecutar `python scripts/verify_structure.py`, `python -m pytest -q`, `ruff check .` con los ejecutables del entorno del proyecto; comprobar códigos 0 y explicar omisiones.
- [x] Ejecutar inventario real, estudio CLI, relectura de evidencia, persistencia entre dos procesos y backup/restauración con archivos sintéticos bajo `local-data/diagnostics/`.
- [x] Revisar `git diff --check` y comprobar que `cyme_ascii.py` conserva su cambio previo; sin operaciones sobre el archivo donante externo.
- [x] Registrar métricas y rutas de evidencia. Mantener explícitos los pendientes de producción, datos e IA; no marcar globalmente completadas 004/005/007/031.

## Continuación integral: entregas separadas, objetivo global abierto

El lote 1 no sustituye las otras entregas aprobadas. Cada una conserva su spec y se
planifica con el mismo detalle antes de tocar sus interfaces:

| Orden/dependencia | Entrega | Spec y condición de entrada | Evidencia exigida para cerrar |
|---|---|---|---|
| Tras lote 1 | Seguridad productiva, PostgreSQL y worker | 005/007/031; proveedor de identidad y destino identificados; driver autorizado | 401/403, aislamiento tenant en SQL, claims entre workers, reinicio, backup PostgreSQL, CI/contenedor real. |
| En cuanto se autoricen fuentes | Lectores e ingesta | 001/035; documento del propietario, licencia y dependencias lectoras autorizadas | raw→gold, cobertura/cuarentena, CRS/unidades y splits temporales/topológicos. |
| Después del contrato de datos | Transformadores y multifase | 008/017; parámetros con fuente y migración de snapshot | Benchmark IEEE 13/123 y cortocircuito con tolerancias independientes. |
| Sobre snapshots validados | GIS/estudios/expansión | 002/003/018/019 | UI E2E, IDs sincronizados, solver confirma alternativas y base económica. |
| Después de gold y autorización torch | GNN/PINN | 029/035 | Entrenamiento real y evaluación con el split vigente; superar AC-029-S* sin relajar umbrales. |
| Después de gold y entorno | MADRL | 030 | Baseline, entrenamiento multisemilla y validación AC por episodio/acción. |
| Corpus con derechos y modelo identificado | LLM/GraphRAG | 030/014 | Respuestas con citas verificables, herramientas tipadas y pruebas adversariales. |
| Contratos y aplicación disponibles | Grafo/P2P/ledger/mercado | 010–013 | Consumidores reales, firmas/anti-replay, separación de grafos y mercado exclusivamente simulado. |
| SDK y cliente autorizados | Conectores reales | 015 | Handshake y llamadas por transporte; cada conexión opcional probada individualmente. |
| Fuentes oficiales revisadas | Regulación y entrega | 020–027 | Cálculos trazables a cláusula/fuente vigente y revisión humana independiente. |

Ninguna autorización del diseño sustituye permisos del propietario de datos,
credenciales externas o aprobación para instalar paquetes. No fabricar esos insumos.

## Fundamento y revisión del plan

El artículo de [Thurner et al. (2018)](https://www.pandapower.org/references/), la
[tesis de maestría de Tadvin (2024)](https://digitalcommons.uri.edu/theses/2568/) y
la [tesis doctoral de Alvarez (2019)](https://ltu.diva-portal.org/smash/record.jsf?pid=diva2:1283534)
fundamentan análisis reproducible e integración entre componentes. Los mecanismos
SQLite, estados de jobs y secuencia del plan son decisiones de ingeniería, no
resultados demostrados por esas tesis. Se revisaron registros/resúmenes, no sus
textos completos; el repositorio doctoral aplicó una restricción de acceso en la
reconsulta del 21/10/2026 y no se atribuyen hallazgos nuevos a esa consulta.

Revisión propia: las tareas 1–6 cubren el primer lote y sus cinco modos de fallo;
las entregas restantes están explícitas en la tabla y no se consideran implementadas.
Las firmas conservan la API actual; las dependencias de tareas 2→3→4 son secuenciales.
Las pruebas nuevas se observaron fallar antes de implementar y pasar después. La evidencia local entre procesos está en `local-data/diagnostics/readiness-20261021/acceptance-d3a701b9/acceptance.json`. La suite completa, estructura, Ruff e inventario se ejecutaron; los resultados vigentes se registran bajo `local-data/diagnostics/readiness-20261021/verification.json`.


## Decisiones registradas durante la ejecución

- Ejecución en la carpeta activa aprobada, preservando cambios previos; no se crearon worktrees ni instalaron dependencias.
- El inventario resume todo local-data únicamente en conteos y bytes para evitar divulgar nombres privados; conserva hashes y relaciones de los archivos de producto.
- El perfil SQLite es de un solo proceso API: recuperar running al abrir no constituye un protocolo distribuido de leases; PostgreSQL y worker siguen pendientes.
- Revisión independiente: corregido resolve() del intérprete virtual a absolute(), con regresión roja/verde que emula el symlink POSIX en Windows.
- Hallazgo de validación: entrada no finita devolvía 500 al serializar errores Pydantic. Se añadió respuesta 422 con campo/tipo sin input ni contexto privado; regresión roja500/verde422.

Verificación final ejecutada: **205 pruebas aprobadas, 2 omitidas por permisos de
symlink y 63 subpruebas aprobadas**. Una advertencia existente de Starlette/HTTPX.
Estructura (25 specs), Ruff, inventario (587 archivos sin dueño/spec faltante),
catálogo de 24 skills/conectores, biblioteca científica y diff sin errores de
espacios: aprobados. La revisión independiente no dejó hallazgos importantes.

## Método obligatorio por spec y verificación de la continuación

Mandato del usuario del 21/10/2026: cada modificación o mejora conserva la
metodología de su spec hasta satisfacer los criterios de cierre. Antes de editar,
revisar requisito, método, contratos, tareas y ADR; implementar con pruebas de los
modos de fallo; ejecutar el consumidor real; releer evidencia y contrastar cada AC.
Una dependencia instalada, un archivo existente o una prueba unitaria no cierran
criterios de aceptación funcional, científica ni productiva. El alcance parcial se
registra sin marcar la tarea principal como terminada. Las contradicciones se
resuelven explícitamente sin reducir tolerancias ni inventar insumos.

| Spec | Implementación y evidencia de esta continuación | Cierre que permanece abierto |
|---|---|---|
| 005/007/031 | bearer local, 401/403/aislamiento; worker PostgreSQL/PostGIS independiente; pg_dump/pg_restore a base nueva con relectura; trazas y métricas | recuperación coordinada tras caída del worker, contenedor/lockfile de aplicación y aceptación productiva |
| 015 | SDK MCP 2.3.0 y handshake stdio con lectura/rechazo de traversal; Playwright/Chromium reales | sesión del cliente IDE y transportes MCP opcionales específicos |
| 029 | PyTorch CUDA disponible, GraphSAGE y pérdida AC con gradientes unitarios | entrenamiento/evaluación sobre gold, umbrales AC y consumidor del GNN |
| 035 | autorización local del usuario; bronze Excel de líneas (3 libros, 129 471 filas); promoción comprueba registro/caso/rol, hashes raw, origen, fechas/hueco y particiones no vacías | silver documentado y gold temporal real; medidores/cabeceras y resto de productos |

Ruling: el candidato PF actual no se promueve por mera autorización. Carece de
fechas y separación temporal exigidas por AC-029-S01 y AC-035-D04; el intento de
atestación anterior se preservó fuera del dataset como evidencia invalidada. No
se entrenó ningún modelo con ese candidato. La atestación exige destino nuevo;
no puede sobrescribir raw, NPZ ni manifiesto.

Las cifras 205/587 de la entrega inicial describen aquel lote. La verificación
vigente se guarda en `local-data/diagnostics/readiness-20261021/`; inventario actual
618 archivos sin dueño ni spec faltante. El resultado global de pruebas solo se
actualiza después de terminar la ejecución y resolver los fallos.

Fundamento científico: se conservan las referencias al artículo de Thurner, tesis
de maestría de Tadvin y doctoral de Alvarez citadas arriba, con sus límites de
lectura declarados. Esas fuentes respaldan la necesidad de contraste y evaluación;
no se les atribuye la implementación concreta de bearer, SQLite o PostgreSQL.
