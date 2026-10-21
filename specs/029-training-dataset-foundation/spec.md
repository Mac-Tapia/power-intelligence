# 029 — Fundación de datasets de entrenamiento (universal, por caso de aplicación)

**Estado:** controles de calidad, registro de fuentes v2, casos de aplicación y auditor implementados; datasets gold pendientes.

## Principio rector: producto universal, caso de aplicación declarado

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

## Estado de las fuentes del caso piloto (auditoría 20/10/2026)

Evidencia: `datasets/quality/source_audit_pe-ica-electrodunas.json`.

| Fuente | Contenido | Estado |
|---|---|---|
| `eldu-vnrgis-2024-04` (+ parámetros) | VNR-GIS abr‑2024, backup SQL Server 819 MB | `pending_restore` |
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

## Principios

1. **Registrar una fuente no la autoriza.** Sin autorización confirmada del propietario (`authorization.status = confirmed` en el caso) no se publica ningún dataset gold.
2. **Capas inmutables:** `raw` (bytes y SHA-256) → `bronze` (parseado y tipado, sin cambiar valores) → `silver` (correcciones explícitas, una regla con evidencia por cada una) → `gold` (dataset de tarea con splits y manifiesto).
3. **Sin oráculo ni fuga temporal.** Los pronósticos se generan con modelos causales declarados. Los splits son cronológicos, con un hueco ≥ lag máximo + horizonte.
4. **Origen por columna:** measured, interpolated, disaggregated, imputed, forecast, scenario, reanalysis u official_statistic.
5. **Los valores de clientes nunca entran en Git.** En Git solo van manifiestos, hashes, métricas y esquemas.
6. **Los nombres de dataset gold son genéricos y parametrizados por caso:** `<producto>-<case_id>-v<n>`.

## Productos gold (por caso; ejemplo para el piloto)

| Propósito | Dataset gold | Fuentes del piloto | Bloqueo |
|---|---|---|---|
| Forecast | `feeder-load-15min-pe-ica-electrodunas` | medidores, líneas, cabeceras y exógenas | lector xlsx/xls/xlsb (autorizar `openpyxl`, `xlrd`, `pyxlsb`) |
| GNN/PINN (006) | `vnr-pf-scenarios-pe-ica-electrodunas` | VNR-GIS + catálogo + perfiles gold + solver | restaurar el VNR; adaptador 001; motor 004‑B |
| MADRL (007) | `district-flex-pe-ica-electrodunas` | clientes importantes, medidores, exógenas y DER de escenario | no existe dataset CityLearn de Ica: construirlo desde mediciones reales del caso |
| LLM (008) | `corpus-<jurisdicción>` + `tool-use-traces` + `eval-electrical-qa` | normas PE registradas, expedientes DGER autorizados, ejecuciones de la CLI | licencias y textos completos |

## Criterios de aceptación

- AC-029-01: `audit_sources.py --case <id>` audita las fuentes del caso y publica evidencia releída. Los estados `oracle`, `shifted`, `inconsistent`, `rejected` y `mostly_empty` bloquean; `pending_reader` y `pending_restore` nunca cuentan como aprobados.
- AC-029-02: los controles de `unitesis_sciml.quality` tienen pruebas negativas de cada defecto observado y una prueba positiva de serie regular.
- AC-029-03: el caso, las fuentes y los perfiles son coherentes: `check_consistency` devuelve vacío para todo caso en `config/cases/`.
- AC-029-04: un dataset gold publica un manifiesto con `case_id`, SHA de cada raw, reglas silver aplicadas, origen por columna, splits con fechas y hueco, versión de código y autorización.
- AC-029-05: ningún dataset gold de un caso contiene filas de fuentes `method_reference` ni de otro caso.
- AC-029-06: en el dataset LLM, cada respuesta numérica la regenera el solver dentro de las tolerancias de CONTRACTS-AND-EVIDENCE, y cada respuesta normativa cita un fragmento de una fuente de la jurisdicción del caso o responde "no fundamentado".
- AC-029-07: ningún valor de cliente, importe facturado ni identificador personal entra en Git (prueba de escaneo de `datasets/`, `docs/`, `specs/` y `config/`).

## Fuera de alcance

- Preentrenar un LLM.
- Leer datos privados sin autorización.
- Corregir fuentes sin evidencia.
- Codificar en el núcleo supuestos de un país o empresa.
