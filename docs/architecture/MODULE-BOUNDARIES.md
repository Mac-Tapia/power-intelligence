# Decisiones de módulos y reglas de dependencias

## Modelo de entrega
**Monolito modular para control + workers desacoplados para cargas pesadas.** La arquitectura no obliga a microservicios ni a Kafka durante G0-G3.

## Capas Python y regla de dependencia

```text
apps/control-api     -> application -> domain
workers/*            -> application -> ports -> adapters at composition root
power-adapters       -> domain + ports  (nunca al revés)
power-simulation     -> domain + ports  (solvers externos mediante adapter)
power-optimization   -> domain + ports  (solvers externos mediante adapter)
power-sciml          -> domain + schemas compartidos (sin filtrar modelos a domain)
power-agents         -> application ports + lectura citada (sin mutar red real)
power-domain         -> únicamente biblioteca estándar y tipos propios
```

- `domain`: entidades, invariantes, objetos de valor y eventos; inmutable cuando corresponda.
- `application`: casos de uso y transacciones, invoca puertos; orquestación de corta vida, no training.
- `ports`: interfaces abstractas (`NetworkRepository`, `PowerFlowPort`, `EvidenceStore`, `JobQueue`).
- `adapters`: PostgreSQL, VRNGIS, SQL, MDB, DGS, OpenDSS, etc. mediante contratos adaptadores.
- `compute`: siempre con snapshot inmutable + escenario + versión + semilla.
- `apps`: solo API, composición, autorización, UI. No ecuaciones duplicadas en web.

## Bounded contexts
`SourceAcquisition`, `AssetRegistry`, `ElectricalTopology`, `SpatialModel`, `Measurements`, `StudyCase`, `PowerFlow`, `ShortCircuit`, `Reliability`, `ExpansionPlanning`, `Optimization`, `ScientificML`, `AgentOrchestration`, `EvidenceAndReporting`, `IdentityAndAudit`.

## Interfaces y prohibiciones

- Tipos y esquemas versionados en `contracts/`; sus cambios requieren prueba de compatibilidad.
- La topología GIS cruda, el grafo eléctrico y el layout del unifilar **son tres representaciones distintas**, sincronizadas por ID de activo/terminal.
- Los catálogos regulatorios son versionados por jurisdicción y norma; las cifras no se codifican en la red neuronal.
- `power-domain` no depende de SQL, infraestructura, HTTP, PyTorch ni OpenDSS.
- Nada llamado `run_power_flow` debe fingir cálculo sin un motor conectado.
- Los workers de IA no acceden directamente a la base de producción; pasan por autorización, acción tipada y revisión.

## Guía de extracción futura
Separar un bounded context como servicio solo si límites de despliegue, licencias, latencia, volumen o autonomía de equipo lo justifican con mediciones.

### Extensión V5 (ownership)
- `power-topology`: única topología física versionada, nunca escrita directamente desde P2P, ledger, GraphRAG o agentes.
- `power-graph`: proyección/retrieval temporal y graph queries; los grafos no son el source of truth.
- `power-p2p`: P2P de comunicaciones para evidencia/escenarios únicamente; no SCADA.
- `power-market`: ofertas y clearing simulado; llama al puerto de validación AC antes de cualquier state transition autorizable.
- `power-ledger`: digests y anclajes opcionales; no persiste fuente original on-chain.
- `power-graphrag`: índice documental/knowledge graph para copiloto; respuestas fundamentadas, sin escribir en topología.
