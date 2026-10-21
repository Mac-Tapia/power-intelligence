# Mapa de programa y especificaciones SDD

| ID | Dominio | Criterio de entrega |
|---|---|---|
| 000 | Repo, contratos, CI | estructura y pruebas repetibles |
| 001 | Ingesta VNR-GIS multiempresa | sin inventar atributos, data quality y linaje |
| 002 | Nueva carga y estudios | comparación reproducible con solver |
| 003 | GIS ↔ unifilar | sincronía UUID con conectividad preservada |
| 004 | motores de simulación | estudios multifase/cortos dentro de cobertura y tolerancia |
| 005 | expansión/SED/BESS/DER/EV | alternativas factibles + Pareto |
| 006 | SciML PINN/GNN | modelo propio entrenado y validado fuera de muestra |
| 007 | MARL multiagente seguro | rewards/versiones/riesgo/validación |
| 008 | LLM local + RAG | tool calls tipados, citas y revisión humana |
| 009 | industrialización | permisos, observabilidad, recovery y despliegue |
| 010 | Graph eléctrico/activos y consultas | proyección versionada, integridad, ACL |
| 011 | P2P federado de colaboración | firmas, peers autorizados, anti-replay y reconexión |
| 012 | Auditoría criptográfica/ledger opcional | hashes off-chain verificables y decisión Fabric/Besu |
| 013 | Mercado P2P energético simulado | ofertas factibles AC, medición, controles regulatorios y no pagos |
| 014 | GraphRAG técnico | respuestas con citas/snapshot, aislamiento y sin edición del grafo físico |

El ID es estable; cambiar características exige ADR y revisión de compatibilidad. Los IDs 004–014 representan backlog o contratos iniciales, no funcionalidades operativas.

- Feature 015 → skills/agent profiles/MCP registry/backend+frontend blueprint → `tests/bootstrap/test_v6_agents_mcp.py` → ADR-0007.
