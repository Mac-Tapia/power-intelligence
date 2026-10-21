# Contratos, evidencias y ownership

Contratos vigentes e implementados. Todo cambio incompatible exige una versión nueva, la migración explícita, la prueba del consumidor y un ADR.

## Identidades (hashes distintos, nunca intercambiables)

| Contrato | Esquema | Implementación | Identidad |
|---|---|---|---|
| SourceManifest | `unitesis.source-manifest/*` | `unitesis_adapters.neutral_json` | SHA-256 de los bytes originales, parser/versión, unidades, autorización, cuarentena por campo |
| ElectricalSnapshot | `unitesis.electrical-snapshot/v2` | `unitesis_domain.network` | hash canónico independiente del orden sobre equipos, conexiones, estados, P/Q, R/X, longitudes, tensiones y frecuencia. La geometría/CRS vive en el manifiesto de fuente. `NetworkSnapshot` v1 es legado y no identifica estudios |
| StudyRequest | `unitesis.study-request/v1` | `unitesis_domain.study` | snapshot + escenario + motor + ajustes del solver |
| StudyResult | `unitesis.study-result/v1` | `unitesis_domain.study` | resultado completo; el tiempo de ejecución no forma parte de la identidad |
| Evidencia | sobre `power-intelligence.evidence/1` con payload `unitesis.{study,new-load,alternatives}-evidence/1` | `unitesis_evidence.store` | SHA-256 del payload canónico; publicación atómica y relectura obligatoria |
| Caso de aplicación | `unitesis.application-case/1` | `unitesis_config.cases` | `case_id`; coherencia con los perfiles regulatorios y el registro de fuentes |
| Fuente de datos | `unitesis.dataset-sources/2` | `scripts/datasets/audit_sources.py` | `source_id` + `case_id` + `role` |
| Base económica | `unitesis.economic-basis/1` | `unitesis_economics.basis` | SHA-256 del documento; sin valores por defecto |

Los esquemas JSON de evidencia están en `contracts/schemas/json/*-evidence.v1.schema.json` y se validan contra payloads reales en `tests/contract/`.

## Estados

- Ingesta: `inventoried → parsed → quarantined | model_validated`.
- Estudio: `requested → running → failed | unavailable | computed`. `computed` exige convergencia y resultados de barras.
- Comparación independiente: `not_run | failed | unavailable | passed`. Falla si se usa el mismo motor, si hay cobertura distinta del snapshot esperado, IDs duplicados, valores no finitos u otro escenario.
- Evidencia: `not_persisted | persisted | reread_verified`.
- Aceptación técnica y regulatoria: campos independientes, siempre `false` hasta la revisión humana.

El éxito nunca se deduce de `converged`, de un HTTP 200, de `bool(valor)` ni de un digest. Se rechazan las cadenas truthy (`"false"`), las tolerancias no positivas o no finitas y las evidencias sin identidad, escenario o alcance comprobados.

## Tolerancias iniciales de contraste (por caso; nunca se relajan automáticamente)

| Magnitud | Tolerancia |
|---|---|
| Tensión | 1e-6 p.u. |
| Ángulo (misma slack, diferencia circular) | 1e-4 ° |
| Pérdidas | 1e-6 MW |
| Corriente | max(1e-3 A, 1e-4 × referencia) |
| Balance complejo | max(1e-6 MVA, 1e-6 × demanda aparente) |

Un paso de iteración pequeño no reemplaza el residuo ni el balance físico.

## Códigos de salida de la CLI (`scripts/unitesis.py`)

`0` correcto · `2` entrada inválida o en cuarentena · `3` motor de referencia ausente · `4` sin convergencia · `5` contraste fallido · `6` evidencia corrupta.

## Ownership

| Contexto | Dueño |
|---|---|
| Ingesta y calidad de datos | `power-adapters`, `power-sciml.quality` |
| Topología física | `power-topology` (único dueño; los demás grafos son proyecciones) |
| Simulación | `power-simulation` (motores propios y adaptadores de contraste) |
| Optimización y economía | `power-optimization`, `power-economics` (propuestas, no aprobación) |
| SciML / MADRL | `power-sciml`, `power-marl` (aproximan o exploran; nunca certifican) |
| Agentes / RAG | `power-agents`, `power-graphrag` (proponen y citan; no escriben en la red) |
| Evidencia | `power-evidence` |
| Casos y configuración | `power-config` |
