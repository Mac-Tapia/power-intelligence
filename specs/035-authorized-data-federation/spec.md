# SPEC-035 — authorized-data-federation

**Propósito:** Conectar SQL empresariales, historiales, telemetría y catálogos externos solo con credenciales autorizadas.


---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-035` · **Gate:** `G6` · **Dependencias:** SPEC-001, SPEC-005, SPEC-007.  
**Alcance verificable:** Conectar SQL empresariales, historiales, telemetría y catálogos externos solo con credenciales autorizadas.  
**Ubicación propuesta:** `packages/python/power-adapters/, workers/ingestion/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-035-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-035-02:** entrada válida: Todos conectores externos con read-only por defecto, scopes, reintentos, watermark y auditoría; nunca escriben SCADA.
- **FR-035-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-035-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-035-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-035-01:** caso exitoso demuestra `FR-035-01/02` con fixture y evidencia automatizada.
- **AC-035-02:** caso negativo demuestra `FR-035-03`, sin alterar estado persistido ni fuente original.
- **AC-035-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-035-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.

## Criterios vigentes incorporados (antes spec 029)

**Estado:** controles de calidad, registro de fuentes v2, casos de aplicación y auditor implementados; datasets gold pendientes.

### Principio rector: producto universal, caso de aplicación declarado

UNITESIS es universal: cualquier empresa, región, país, frecuencia, CRS, moneda y jurisdicción. El código nunca contiene supuestos locales. Lo local se declara en tres registros versionados y sincronizados:

| Registro | Archivo | Validador |
|---|---|---|
| Caso de aplicación (país, empresa, CRS, zona horaria, moneda, frecuencia, perfiles, fuentes) | `config/cases/<case_id>.json` (plantilla `_template.json`) | `unitesis_config.cases` |
| Fuentes de datos (`case_id`, `role`, origen por columna, sensibilidad, autorización) | `config/datasets/sources.v2.json` | `scripts/datasets/audit_sources.py` |
| Perfiles regulatorios (`jurisdiction`) | `config/regulations/profiles/*.json` | `check_consistency` (jurisdicción = país del caso) |

**Caso piloto:** `pe-ica-electrodunas` (Electro Dunas: Ica, Chincha, Pisco, Nasca). Sirve para generar datasets y pruebas con datos reales que validan el producto; no define el producto. Un segundo caso se añade copiando la plantilla, sin cambiar código (prueba `tests/unit/test_application_cases.py` con un caso ficticio a 50 Hz).

**Roles de fuente:**
- `application_case`: alimenta los datasets y evidencias de su caso.
- `method_reference`: datos de proyectos previos de otras localidades (p. ej. Iquitos), útiles solo para desarrollar o probar métodos. Nunca se presentan como evidencia de un caso, ni se mezclan con sus datos.

### Estado de las fuentes del caso piloto (auditoría 20/10/2026)

Evidencia: `datasets/quality/source_audit_pe-ica-electrodunas.json`.

| Fuente | Contenido | Estado |
|---|---|---|
| `eldu-vnrgis-2024-04` (+ parámetros) | VNR-GIS abr‑2024, backup SQL Server 819 MB | `pending_restore` |
| `eldu-cyme-ascii-2026-08` | red real en TXT ASCII CYMDIST: 96 alimentadores, 38 681 nodos, 7 287 cargas, catálogo de conductores con R/X | **pasa el control estructural** |
| `eldu-cyme-study-mdb` | 1 164 bases MDB por alimentador (3,45 GB) | `pending_reader` (lector Access) |
| `eldu-meter-demand-2023-2026` | P/Q cada 15 min por medidor (4 xlsx, 577 MB) | `pending_reader` |
| `eldu-line-demand-l6605-l6606` | kVA/kW/kvar 15 min, ene‑2023 a sep‑2026 | `pending_reader` |
| `eldu-feeder-head-measurements` | cabecera por sistema Chincha/Ica/Nasca/Pisco (1 GB xls) | `pending_reader` |
| `eldu-key-customers`, `eldu-supply-customers`, `eldu-feeder-meters`, `eldu-new-customers` | clientes y relaciones medidor-alimentador | `pending_reader` |
| `eldu-exog-*` (temperatura Ica 15 min, calendario, PBI BCRP, población INEI, NASA POWER Pisco) | variables exógenas | **pasan los controles** (la temperatura es reanálisis ERA5 interpolado: origen `interpolated_reanalysis`) |
| `eldu-dger-investment-studies` | 392 documentos (pdf, docx, xls, dwg) | `inventoried`; incluye un `.pfd` (formato PowerFactory): solo lectura offline, sin motor (ADR-0010) |

Referencias de método (Iquitos, `case_id: null`), las cuatro bloqueadas:
- dataset CityLearn con pronósticos oráculo;
- facturas con totales desfasados o inconsistentes;
- archivo 2013‑2025 con 1,2 % de datos reales;
- perfil 2024 con etiquetas desplazadas.

Antes de usarlas incluso como referencia de método hay que corregirlas.

### Principios

1. **Registrar una fuente no la autoriza.** Sin autorización confirmada del propietario (`authorization.status = confirmed` en el caso) no se publica ningún dataset gold.
2. **Capas inmutables:** `raw` (bytes y SHA-256) → `bronze` (parseado y tipado, sin cambiar valores) → `silver` (correcciones explícitas, una regla con evidencia por cada una) → `gold` (dataset de tarea con splits y manifiesto).
3. **Sin oráculo ni fuga temporal.** Los pronósticos se generan con modelos causales declarados. Los splits son cronológicos, con un hueco ≥ lag máximo + horizonte.
4. **Origen por columna:** measured, interpolated, disaggregated, imputed, forecast, scenario, reanalysis u official_statistic.
5. **Los valores de clientes nunca entran en Git.** En Git solo van manifiestos, hashes, métricas y esquemas.
6. **Los nombres de dataset gold son genéricos y parametrizados por caso:** `<producto>-<case_id>-v<n>`.

### Productos gold (por caso; ejemplo para el piloto)

| Propósito | Dataset gold | Fuentes del piloto | Bloqueo |
|---|---|---|---|
| Forecast | `feeder-load-15min-pe-ica-electrodunas` | medidores, líneas, cabeceras y exógenas | lector xlsx/xls/xlsb (autorizar `openpyxl`, `xlrd`, `pyxlsb`) |
| GNN/PINN (006) | `pf-scenarios-pe-ica-electrodunas` | redes reales TXT + MDB + VNR-GIS, catálogo BD_Equipo, perfiles gold, solver propio | lector TXT (T001-T010); lector MDB y VNR restaurado; transformadores (008-B2) |
| MADRL (007) | `district-flex-pe-ica-electrodunas` | clientes importantes, medidores, exógenas y DER de escenario | no existe dataset CityLearn de Ica: construirlo desde mediciones reales del caso |
| LLM (008) | `corpus-<jurisdicción>` + `tool-use-traces` + `eval-electrical-qa` | normas PE registradas, expedientes DGER autorizados, ejecuciones de la CLI | licencias y textos completos |

### Criterios de aceptación

- AC-035-D01: `audit_sources.py --case <id>` audita las fuentes del caso y publica evidencia releída. Los estados `oracle`, `shifted`, `inconsistent`, `rejected` y `mostly_empty` bloquean; `pending_reader` y `pending_restore` nunca cuentan como aprobados.
- AC-035-D02: los controles de `unitesis_sciml.quality` tienen pruebas negativas de cada defecto observado y una prueba positiva de serie regular.
- AC-035-D03: el caso, las fuentes y los perfiles son coherentes: `check_consistency` devuelve vacío para todo caso en `config/cases/`.
- AC-035-D04: un dataset gold publica un manifiesto con `case_id`, SHA de cada raw, reglas silver aplicadas, origen por columna, splits con fechas y hueco, versión de código y autorización.
- AC-035-D05: ningún dataset gold de un caso contiene filas de fuentes `method_reference` ni de otro caso.
- AC-035-D06: en el dataset LLM, cada respuesta numérica la regenera el solver dentro de las tolerancias de CONTRACTS-AND-EVIDENCE, y cada respuesta normativa cita un fragmento de una fuente de la jurisdicción del caso o responde "no fundamentado".
- AC-035-D07: ningún valor de cliente, importe facturado ni identificador personal entra en Git (prueba de escaneo de `datasets/`, `docs/`, `specs/` y `config/`).

### Fuera de alcance

- Preentrenar un LLM.
- Leer datos privados sin autorización.
- Corregir fuentes sin evidencia.
- Codificar en el núcleo supuestos de un país o empresa.
