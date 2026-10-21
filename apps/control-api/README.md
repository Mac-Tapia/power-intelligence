# apps/control-api

Frontera HTTP delgada (FastAPI) sobre los casos de uso de `power-application`. Sin cálculo eléctrico en los handlers: los estudios se encolan como jobs.

**Estado:** v0.2.0, solo local. No hay autenticación ni aislamiento por tenant: la app no arranca sin `UNITESIS_LOCAL_ONLY=1` y `scripts/unitesis.py serve` solo acepta `localhost`.

| Método | Ruta | Uso |
|---|---|---|
| GET | `/api/v1/health` | estado y versión |
| GET/POST | `/api/v1/snapshots` | listar / importar red JSON neutral (422 con cuarentena) |
| GET | `/api/v1/snapshots/{sha}` | snapshot canónico y resultados |
| POST | `/api/v1/studies` | flujo de potencia + contraste (job 202) |
| POST | `/api/v1/studies/new-load` | nueva carga en escenario clonado (job 202) |
| POST | `/api/v1/studies/conductor-alternatives` | alternativas de conductor con VPN (job 202) |
| GET | `/api/v1/jobs/{id}`, `/api/v1/results/{sha}` | estado de job / resultado |
| GET | `/api/v1/catalogs/conductors`, `/api/v1/examples[/{name}]`, `/api/v1/economic-basis/example` | datos de referencia |
| GET | `/` | workstation web (`apps/workstation-web/public`) |

Arranque: `python scripts/unitesis.py serve` (usa uvicorn si está instalado; si no, un puente local de la stdlib).
