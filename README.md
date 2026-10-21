# UNITESIS Power Intelligence

Plataforma **universal** de ingeniería y planificación de redes de distribución: ingesta trazable, motor de flujo de potencia propio con contraste independiente, escenarios de nueva carga, alternativas técnico‑económicas, evidencia verificable y capas de IA (GNN/PINN, MADRL, LLM) que proponen pero nunca certifican.

Lo local (país, empresa, CRS, zona horaria, moneda, frecuencia, normas y fuentes) se declara por **caso de aplicación** en `config/cases/`. El caso piloto es `pe-ica-electrodunas` (Electro Dunas: Ica, Chincha, Pisco, Nasca).

## Estado

| Capa | Estado |
|---|---|
| Núcleo eléctrico (dominio, topología, BFS propio, contraste pandapower, evidencia) | operativo; G3 cumplida para el alcance radial equilibrado (spec 004‑A) |
| Nueva carga y alternativas de conductor con VPN | operativos (specs 002 y 005) |
| CLI, API local y workstation web | operativos, solo local (sin autenticación; spec 009) |
| Ingesta VNR-GIS | pendiente (spec 001); esquema relevado |
| Datasets por caso y controles de calidad | controles operativos; datasets gold pendientes (spec 029) |
| GNN/PINN, MADRL, LLM | specs 006/007/008 listas; sin código |

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
```

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
| `infra/db/postgres` | esquema SQL append-only (adaptador PostgreSQL: spec 009) |
| `datasets/quality` | evidencias de auditoría de fuentes (solo métricas) |
| `local-data/` | fuera de Git: fuentes de referencia del caso y salidas locales |

Las carpetas nuevas (workers, benchmarks, paquetes TS…) se crean cuando una tarea de spec las necesita; no se dejan carpetas vacías.
