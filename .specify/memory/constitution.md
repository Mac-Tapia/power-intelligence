# UNITESIS Engineering Constitution v1.0

## Non-negotiable principles

I. **Physical correctness over plausible AI output.** A physics-informed neural net or LLM is not an electrical solver certification. All reported studies require independently verifiable calculations and explicit limits.

II. **Domain isolation.** Domain entities and electrical invariants do not import infrastructure frameworks. Use ports/adapters, strict dependencies, versioned contracts.

III. **Source fidelity and provenance.** Preserve original GIS files, topology lineage, units, CRS, phase and switching states. Quarantine missing values; never silently impute undocumented attributes.

IV. **Spec first; evidence always.** No production feature without reviewed `spec.md`, `plan.md`, `tasks.md`, acceptance tests, reproducible evidence and design review. Trace requirements -> code -> tests -> result.

V. **Safety and authorization.** Agents may recommend changes only in cloned study scenarios. Never operate production SCADA/protection by autonomous LLM or RL.

VI. **Repeatable computation.** Inputs, code commit, solver version, unit system, scenario, topology snapshot, random seeds, convergence, and uncertainty are recorded.

VII. **One deliverable per PR.** Each PR satisfies its spec and CI; worktrees isolate parallel agents and changes. Avoid branch-in-branch confusion.

VIII. **Security and licensing by design.** No confidential VNR-GIS/SQL/SCADA datasets or model weights committed. Protect secrets, data rights and tenant access.

## Quality gates

- G0: repository/tests/contracts and code owner approval.
- G1: no data loss ingest, raw manifests and invalidation.
- G2: topology and GIS/unifilar consistency.
- G3: power flow benchmark and independent validation.
- G4+: optimization and AI only when baselines pass.

If any principle must change, create an ADR and version this constitution through PR.

IX. **Separación Graph/P2P/Blockchain.** El grafo eléctrico canónico no es el grafo de comunicación ni mercado; las proyecciones GraphRAG son solo lectura y no pueden alterar parámetros físicos.

X. **Mercado P2P cerrado por defecto.** No existe liquidación real sin evidencia AC, dictamen jurídico peruano vigente, medición certificada y aprobación humana. Blockchain jamás sustituye estos controles.

XI. **Ledger opcional y privacidad.** Hashes y referencias ancladas off-chain-first; cero datos personales, topología sensible o SCADA en cadena. Todo ledger debe tener evaluación de necesidad y amenaza.

XII. **Agentes acotados y auditables.** Skills de Agent Skills versionados y MCP con perfil deny-by-default, scopes mínimos y revisión humana. Separar herramientas de desarrollo, APIs productivas y solvers científicos. Un prompt nunca es control de acceso.
