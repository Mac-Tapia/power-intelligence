# UNITESIS Power Intelligence

Plataforma **universal** de ingeniería y planificación de redes de distribución: ingesta trazable, motor de flujo de potencia propio con contraste independiente, escenarios de nueva carga, alternativas técnico‑económicas, evidencia verificable y capas de IA (GNN/PINN, MADRL, LLM) que proponen pero nunca certifican.

Lo local (país, empresa, CRS, zona horaria, moneda, frecuencia, normas y fuentes) se declara por **caso de aplicación** en `config/cases/`. El caso piloto es `pe-ica-electrodunas` (Electro Dunas: Ica, Chincha, Pisco, Nasca).

## Estado

| Capa | Estado |
|---|---|
| Núcleo eléctrico (dominio, topología, BFS y Newton-Raphson propios, transformadores, contraste pandapower, evidencia) | operativo para redes equilibradas radiales y malladas (specs 006 y 008: 008-A, 008-B1, 008-B2; benchmark IEEE 33) |
| Nueva carga, alternativas de conductor con VPN, capacidad remanente y Pareto | operativos (specs 002, 018 y 019) |
| CLI, API local y workstation web | locales, con perfil bearer opcional (specs 004 y 005) |
| Jobs y recuperación | jobs durables locales; recuperación distribuida y producción pendientes (specs 007 y 031) |
| Ingesta de redes reales | TXT CYME ASCII operativo (93 alimentadores leídos, 44 validados); MDB y VNR-GIS pendientes (specs 001 y 037) |
| Datasets por caso y controles de calidad | controles operativos; datasets gold pendientes (spec 035) |
| GNN/PINN | dataset candidato desde la red real, línea base física y GraphSAGE unitario; entrenamiento pendiente de gold (spec 029) |
| MADRL, LLM | spec 030; sin código |

Las 40 specs siguen la numeración del plan maestro ([equivalencias con la anterior](docs/traceability/SPEC-ID-MIGRATION.md)).

Las 40 specs siguen la numeración del plan maestro ([equivalencias con la anterior](docs/traceability/SPEC-ID-MIGRATION.md)).

Las 40 specs siguen la numeración del plan maestro ([equivalencias con la anterior](docs/traceability/SPEC-ID-MIGRATION.md)).

Arquitectura y estado por capacidad: [`docs/architecture/ARCHITECTURE-INTEGRAL.md`](docs/architecture/ARCHITECTURE-INTEGRAL.md) · mapa de specs: [`docs/traceability/FEATURE-MAP.md`](docs/traceability/FEATURE-MAP.md) · contratos: [`docs/architecture/CONTRACTS-AND-EVIDENCE.md`](docs/architecture/CONTRACTS-AND-EVIDENCE.md).

## Uso

Entorno: Python 3.12 en `.venv` con `requirements/dev.txt`.

```powershell
.venv\Scripts\python scripts/unitesis.py study --input fixtures/networks/radial_feeder_6bus.json --output local-data/evidence/base.json
.venv\Scripts\python scripts/unitesis.py new-load --input fixtures/networks/radial_feeder_6bus.json --output local-data/evidence/nl.json --load-id NL1 --bus B3 --p-mw 0.5 --q-mvar 0.2
.venv\Scripts\python scripts/unitesis.py alternatives --input fixtures/networks/radial_feeder_6bus.json --output local-data/evidence/alt.json --line L13 --catalog config/catalogs/conductors/aaac6201_nexans_reference.json --basis fixtures/economics/conductor_alternatives_synthetic.json --temperature-c 75 --gmd-m 1.2
.venv\Scripts\python scripts/unitesis.py verify-evidence local-data/evidence/base.json
.venv\Scripts\python scripts/unitesis.py serve          # http://127.0.0.1:8000/
.venv\Scripts\python scripts/datasets/audit_sources.py --case pe-ica-electrodunas --archive-root <archivo-de-donantes>
```

Códigos de salida: 0 correcto · 2 entrada inválida o en cuarentena · 3 motor de referencia ausente · 4 sin convergencia · 5 contraste fallido · 6 evidencia corrupta.

## Verificación

```powershell
.venv\Scripts\python scripts/verify_structure.py   # estructura, specs, casos, prohibiciones
.venv\Scripts\python -m pytest -q                  # unit, contract, integration, security, governance
.venv\Scripts\ruff check .
.venv\Scripts\python scripts/dev/project_inventory.py --root . --output local-data/diagnostics/inventory.json
```

El inventario vincula archivos con módulo y specs existentes, detecta archivos sin dueño
y enumera consumidores Python. La propiedad documental no acredita implementación:
los módulos scaffold y las tareas pendientes siguen visibles en el mapa de capacidades.
El [diseño aprobado](docs/development/READINESS-AND-CLEANUP.md) y su
[plan de implementación](docs/development/READINESS-IMPLEMENTATION-PLAN.md) describen
las entregas de preparación integral y sus límites.

## Estructura por capas

| Carpeta | Contenido |
|---|---|
| `packages/python/power-*` | 19 módulos (dominio, puertos, adaptadores, topología, simulación, optimización, economía, regulación, evidencia, aplicación, config, sciml, marl, agents, graph, graphrag, p2p, market, ledger) |
| `apps/` | `control-api` (FastAPI) y `workstation-web/public` (UI estática servida por la API) |
| `scripts/` | `unitesis.py` (CLI única), `datasets/`, `agents/`, `research/`, `pide/`, `dev/`, `verify_structure.py` |
| `config/` | casos de aplicación, catálogos, perfiles regulatorios, registro de fuentes, catálogo de estudios |
| `contracts/` | esquemas JSON versionados y eventos |
| `specs/` | una carpeta por capacidad (`spec.md` + `tasks.md`) |
| `docs/` | arquitectura, ADR, contratos, trazabilidad, regulación, biblioteca científica, agentes, desarrollo |
| `fixtures/`, `tests/` | casos sintéticos y suites `unit`, `contract`, `integration`, `security`, `governance` |
| `infra/db/postgres` | esquema SQL append-only (adaptador PostgreSQL: spec 007) |
| `datasets/quality` | evidencias de auditoría de fuentes (solo métricas) |
| `local-data/` | fuera de Git: fuentes de referencia del caso y salidas locales |

Las carpetas nuevas (workers, benchmarks, paquetes TS…) se crean cuando una tarea de spec las necesita; no se dejan carpetas vacías.
