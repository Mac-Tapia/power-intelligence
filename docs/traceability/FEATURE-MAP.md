# Mapa de programa y especificaciones SDD

Numeración canónica: las 40 specs del plan maestro (decisión del usuario, 21/10/2026). Sincronizado con `docs/architecture/ARCHITECTURE-INTEGRAL.md`. Cada ID tiene una carpeta en `specs/`; el estado detallado vive en su `tasks.md` y en `master-backlog-assessment.csv`. Las equivalencias con la numeración anterior están en [`SPEC-ID-MIGRATION.md`](SPEC-ID-MIGRATION.md).

| ID | Dominio | Spec | Gate | Tareas hechas | Estado |
|---|---|---|---|---|---|
| 000 | repository foundation | `000-repository-foundation` | G0 | 9/19 | operativo |
| 001 | vnrgis ingestion | `001-vnrgis-ingestion` | G1 | 1/23 | parcial: CYME ASCII operativo; VNR-GIS y MDB pendientes |
| 002 | new load impact | `002-new-load-impact` | G4 | 4/15 | parcial: cribado equilibrado operativo |
| 003 | gis unifilar | `003-gis-unifilar` | G2 | 1/15 | parcial: unifilar y router de geometría |
| 004 | fullstack runtime | `004-fullstack-runtime` | G0 | 1/11 | parcial: CLI, API y workstation locales |
| 005 | identity tenant authorization | `005-identity-tenant-authorization` | G0 | 1/12 | parcial: bearer local con tenant |
| 006 | canonical electrical model | `006-canonical-electrical-model` | G1 | 2/12 | operativo: snapshot v2/v3 |
| 007 | durable jobs and events | `007-durable-jobs-and-events` | G1 | 3/14 | parcial: jobs durables locales |
| 008 | ac solvers and validation | `008-ac-solvers-and-validation` | G3 | 5/15 | parcial: BFS, NR, transformadores y trifásico desbalanceado (IEEE 13) operativos; IEEE 123 y Dyn pendientes |
| 009 | scenario time model | `009-scenario-time-model` | G2 | 1/10 | parcial: escenarios de carga en datasets PF |
| 010 | electrical graph | `010-electrical-graph` | G1 | 3/17 | scaffold |
| 011 | p2p federation | `011-p2p-federation` | G6 | 0/17 | scaffold |
| 012 | ledger evidence | `012-ledger-evidence` | G6 | 0/17 | scaffold |
| 013 | p2p energy market | `013-p2p-energy-market` | G6 | 0/17 | scaffold |
| 014 | graphrag knowledge | `014-graphrag-knowledge` | G6 | 0/18 | pendiente |
| 015 | agent skills mcp | `015-agent-skills-mcp` | G0 | 14/24 | parcial: SDK y handshake MCP stdio |
| 016 | demand forecast and load profiles | `016-demand-forecast-and-load-profiles` | G3 | 1/12 | parcial: splits cronológicos |
| 017 | short circuit quality reliability | `017-short-circuit-quality-reliability` | G3 | 0/11 | pendiente |
| 018 | planning alternatives | `018-planning-alternatives` | G4 | 3/12 | parcial: conductores con VPN y capacidad remanente |
| 019 | multiobjective optimization | `019-multiobjective-optimization` | G4 | 1/11 | parcial: frente de Pareto |
| 020 | pit regulatory engine | `020-pit-regulatory-engine` | G4 | 2/16 | registro documental |
| 021 | pide planning engine | `021-pide-planning-engine` | G4 | 4/16 | registro documental |
| 022 | technical economic studies | `022-technical-economic-studies` | G4 | 3/16 | registro documental |
| 023 | pmbok6 project delivery | `023-pmbok6-project-delivery` | G4 | 2/16 | registro documental |
| 024 | regulatory ui evidence | `024-regulatory-ui-evidence` | G4 | 1/16 | registro documental |
| 025 | regulatory source monitor | `025-regulatory-source-monitor` | G4 | 1/16 | registro documental |
| 026 | pide methodological reference | `026-pide-methodological-reference` | G4 | 7/19 | parcial |
| 027 | pide source audit and reference engine | `027-pide-source-audit-and-reference-engine` | G4 | 8/22 | parcial |
| 028 | der bess ev and renewables | `028-der-bess-ev-and-renewables` | G5 | 0/11 | pendiente |
| 029 | sciml pinn gnn | `029-sciml-pinn-gnn` | G5 | 5/17 | parcial: dataset candidato, línea base y destilación maestro → alumno entrenada (maestro p95 test 0,009 p.u.); gate AC-029-S02 aún no superado |
| 030 | marl llm engineering agents | `030-marl-llm-engineering-agents` | G5 | 0/19 | pendiente |
| 031 | security observability operations | `031-security-observability-operations` | G7 | 3/14 | parcial: telemetría y respaldo local |
| 032 | reporting and evidence | `032-reporting-and-evidence` | G4 | 0/10 | parcial: sobre de evidencia |
| 033 | investment portfolio and roadmap | `033-investment-portfolio-and-roadmap` | G4 | 0/10 | pendiente |
| 034 | generation transmission integration | `034-generation-transmission-integration` | G5 | 0/10 | pendiente |
| 035 | authorized data federation | `035-authorized-data-federation` | G6 | 5/15 | parcial: controles de calidad; fuentes pendientes |
| 036 | tariff and investment cost catalog | `036-tariff-and-investment-cost-catalog` | G4 | 0/10 | parcial: catálogo de conductores |
| 037 | power format interop dgs mdb sql | `037-power-format-interop-dgs-mdb-sql` | G1 | 1/10 | parcial: CYME ASCII; estructura recuperada por ingeniería inversa (ADR-0012) |
| 038 | benchmarks and scientific reproducibility | `038-benchmarks-and-scientific-reproducibility` | G3 | 0/10 | parcial: benchmark de flujo de potencia |
| 039 | production release and governance | `039-production-release-and-governance` | G7 | 0/10 | pendiente |

El ID es estable; cambiar sus características exige un ADR y una revisión de compatibilidad. "Spec creada" no significa "implementada": el estado lo determinan el código, las pruebas y la evidencia.
