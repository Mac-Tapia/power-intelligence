# Mapa de programa y especificaciones SDD

Sincronizado con `docs/architecture/ARCHITECTURE-INTEGRAL.md` (20/10/2026). Cada ID tiene una carpeta en `specs/`; el estado detallado vive en su `tasks.md`.

| ID | Dominio | Spec | Criterio de entrega | Estado |
|---|---|---|---|---|
| 000 | Repo, contratos, CI | `000-repository-foundation` | estructura y pruebas repetibles | operativo |
| 001 | Ingesta VNR-GIS multiempresa | `001-vnrgis-ingestion` | sin inventar atributos, calidad de datos y linaje | pendiente (esquema relevado) |
| 002 | Nueva carga y estudios | `002-new-load-impact` | comparación reproducible con solver | parcial (equilibrado) |
| 003 | GIS ↔ unifilar | `003-gis-unifilar` | sincronía por UUID con conectividad preservada | parcial (unifilar) |
| 004 | Motores de simulación | `004-simulation-engines` | estudios multifase/cortocircuito dentro de cobertura y tolerancia | 004-A y 004-B1 operativos |
| 005 | Expansión/SED/BESS/DER/EV | `005-expansion-planning` | alternativas factibles + Pareto | parcial (conductores) |
| 006 | SciML GNN/PINN | `006-sciml-physics-informed` | modelo propio entrenado con VNR-GIS y validado fuera de muestra | sin código |
| 007 | MARL multiagente seguro | `007-safe-madrl` | recompensas, versiones, riesgo y validación | sin código |
| 008 | LLM local + RAG | `008-llm-rag-tools` | tool calls tipados, citas y revisión humana | sin código |
| 009 | Industrialización | `009-industrialization` | permisos, observabilidad, recuperación y despliegue | no iniciado |
| 010 | Grafo eléctrico/activos y consultas | `010-electrical-graph` | proyección versionada, integridad, ACL | scaffold |
| 011 | P2P federado de colaboración | `011-p2p-federation` | firmas, peers autorizados, anti-replay y reconexión | scaffold |
| 012 | Auditoría criptográfica/ledger opcional | `012-ledger-evidence` | hashes off-chain verificables y decisión Fabric/Besu | scaffold |
| 013 | Mercado P2P energético simulado | `013-p2p-energy-market` | ofertas factibles AC, medición, controles regulatorios y sin pagos | scaffold |
| 014 | GraphRAG técnico | `014-graphrag-knowledge` | respuestas con citas y snapshot, aislamiento y sin edición del grafo físico | scaffold |
| 015 | Skills, agentes y MCP | `015-agent-skills-mcp` | mínimo privilegio y validación | operativo (lectura) |
| 020–025 | Regulación PIT/PIDE, PMBOK, UI regulatoria, monitor de fuentes | `020`…`025` | fuente versionada y aprobación humana | registro documental |
| 026–027 | PIDE metodológico y auditoría de fuentes | `026`, `027` | etiquetas y bloqueos de certificación | parcial |
| 029 | Fundación de datasets de entrenamiento | `029-training-dataset-foundation` | capas raw→gold, controles de calidad y autorización | controles operativos; fuentes bloqueadas |

El ID es estable; cambiar sus características exige un ADR y una revisión de compatibilidad. "Spec creada" no significa "implementada": el estado lo determinan el código, las pruebas y la evidencia.
