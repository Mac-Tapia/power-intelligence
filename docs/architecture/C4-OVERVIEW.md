# C4 inicial (contexto + contenedores)

```mermaid
flowchart TD
Engineer[Ingeniero de sistemas eléctricos] --> Web[Web Workstation / GIS + Unifilar]
Web --> API[Control API / DDD + Auth]
API --> DB[(PostGIS + Evidencias)]
API --> Queue[Workflow / Job Queue]
Queue --> ETL[Ingesta / Validación]
Queue --> Sim[CPU: Power Flow / Shorts / Studies]
Queue --> Opt[CPU: MILP / NSGA / UQ]
Queue --> ML[GPU: PINN + GNN + MARL]
API --> Agent[LLM / RAG / Tool API]
Sim --> Verify[Validador independiente]
Opt --> Verify
ML --> Verify
Verify --> DB
```

Diagramas C4 de componentes y despliegue se crearán por especificación; no se asume despliegue en Kubernetes sin necesidad.

### V5: Extensiones del diagrama de contenedores

`API -> Graph Query Adapter -> read model (PostgreSQL/NetworkX; Neo4j opcional)`; `API -> P2P Bridge -> trusted peer transport`; `Market Simulation -> Solver AC -> Evidence Store -> optional LedgerAnchor`. GraphRAG consume proyecciones por snapshot y ACL; nunca rutas de SCADA. Ver ADR-0004/0005/0006.
