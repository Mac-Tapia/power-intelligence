# Multi-agent technical-economic / regulatory SDD

## Roles
- Normative Researcher: fetch and classify official norms only; cannot set approved state.
- Regulator Analyst: compare amendment to rule, create human approval change request.
- Grid Engineer: runs solver and checks NTCSE/CNE under approved inputs.
- Demand Scientist: 15min profiles, forecast 30yr only when applicable, error diagnostics.
- Investment Economist: validates cashflows, modules, 10yr VP when applicable, scenarios.
- PMBOK Planner: creates one governed project per accepted alternative.
- Full-stack implementer: APIs and UI gates, no autonomous approval.
- QA/Auditor: replay test and block undocumented calculation.

## Roles cannot assume legal authority
A referenced PDF or article is not proof of current norm; human legal review required. Each agent must read `.agents/skills/unitesis-pit-regulation/`, `.agents/skills/unitesis-pide-planning/`, `.agents/skills/unitesis-technoeconomic-studies/`, or `.agents/skills/unitesis-pmbok6-delivery/` as appropriate.

## Suggested connector permissions
- Osinergmin/MINEM public source fetch: read-only with archival digest and anti-SSRF allowlist.
- GitHub MCP: read + branch/PR controlled, never merge automatically.
- PostgreSQL/PostGIS: readonly on real assets; isolated test write DB only.
- Power solver: sandboxed against snapshots; no switching or writeback to SCADA.
- PMBOK exporter: local temp outputs and explicit approval to publish.
- Web/GraphRAG: citation retrieval only; never self-enforce extracted limits.
