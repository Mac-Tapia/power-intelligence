# Instrucciones para agentes de código (UNITESIS)

Antes de cambiar código, leer `.specify/memory/constitution.md`, `docs/architecture/ARCHITECTURE-INTEGRAL.md`, `docs/architecture/MODULE-BOUNDARIES.md`, la spec de la capacidad (`specs/<id>/spec.md` y `tasks.md`) y los ADR relacionados (`docs/architecture/decisions/`).

## Reglas

0. **Trabajo concurrente.** Antes de editar, leer y actualizar el tablero `local-data/coordination/BOARD.md` según `docs/development/AGENT-COORDINATION.md`: reclamar archivos, no editar los reclamados por otro agente y commitear solo rutas explícitas propias (nunca `git add -A` con trabajo ajeno sin commitear).
1. **Producto universal.** No codificar supuestos de país, empresa, frecuencia, CRS, moneda ni norma. Lo local va en `config/cases/<case_id>.json`, en perfiles regulatorios con `jurisdiction` y en `config/datasets/sources.v2.json`. El caso piloto es `pe-ica-electrodunas`.
2. **Motores propios** (ADR-0010). Nada de `cympy`, `powerfactory`, COM/ComLdf ni automatización de sus GUI; lo vigila `tests/security/test_no_proprietary_engines.py`. Se permiten lectores offline de archivos.
3. **Verdad eléctrica** (ADR-0002). GNN/PINN, MADRL y LLM proponen o criban; el solver propio confirma con contraste independiente y la aceptación es humana. Nunca afirmar que un cálculo es correcto sin benchmark y tolerancias declaradas (`docs/architecture/CONTRACTS-AND-EVIDENCE.md`).
4. **Sin valores inventados.** Los parámetros faltantes van a cuarentena y quedan visibles. La proximidad GIS no implica conectividad (ADR-0003).
5. **Dominio puro.** `power-domain` usa solo la stdlib; no importar FastAPI, SQL, Torch, GIS ni motores.
6. **Datos.** Entrenar solo con datasets gold de la spec 035 por `case_id`. Las fuentes `method_reference` nunca son evidencia de un caso. Los valores de clientes no entran en Git.
7. **Spec primero.** Toda capacidad nueva empieza con spec, criterios y tareas; marcar las tareas solo con evidencia ejecutada.
8. **Sin historia en el árbol.** No crear documentos versionados (`*_V5.md`, planes superados, logs de operaciones) ni carpetas vacías; el historial vive en Git.
9. **Dependencias.** No instalar ni actualizar dependencias, ni descargar datos confidenciales, sin autorización explícita. Las versiones están en `requirements/dev.txt`.
10. Ejecutar antes de entregar: `python scripts/verify_structure.py`, `python -m pytest -q` y `ruff check .`.

## Dominios específicos

- **Grafo, P2P, ledger y mercado (010–013):** ADR-0004/0005/0006. No mezclar el grafo P2P, el comercial y el eléctrico; no hay transacciones reales ni datos de red sensibles en el ledger.
- **Regulación (020–027):** `docs/regulatory/INDEX.md`, `docs/regulatory/pide_2017/INDEX.md`, `SOURCES.json` y `docs/project-management/PMBOK6-UNITESIS-MAPPING.md`. El PIDE 2017 es una prepublicación, no una norma aprobada; la certificación automática está bloqueada.
- **Investigación:** `docs/scientific-evidence/INDEX.md` y `python scripts/research/query_evidence.py`. Las fichas no reemplazan al artículo original.
- **Agentes y MCP (015):** `.agents/skills/`, `docs/agents/AGENT-ROLES.md`, `connectors/registry.json`. El MCP local solo lee documentación permitida; ningún conector opcional está activo.
