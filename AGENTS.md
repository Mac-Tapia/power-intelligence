# Instructions for coding agents (UNITESIS)

Read `.specify/memory/constitution.md`, the feature's `specs/<id>/spec.md`, `docs/architecture/MODULE-BOUNDARIES.md`, the relevant ADR and test plan **before** changing code.

1. Never claim an electrical calculation is correct unless verified on a reference benchmark under declared tolerances.
2. No invented VNR-GIS attributes; missing parameters must be quarantined and made visible to the engineer.
3. Electrical topology is based on terminals, voltage, phase and switch states; GIS proximity is not connectivity.
4. LLM, PINN and MARL may propose or screen candidates; final acceptance requires a deterministic independent solver and approved engineering workflow.
5. All features start with a human-reviewable spec, acceptance scenarios and tasks; use one branch and worktree per feature when parallel.
6. Keep domain pure: no importing FastAPI, SQLAlchemy, Torch, GIS drivers or simulation libraries into `power-domain`.
7. Always run targeted unit, contract and regression tests; update evidence and spec status. No production SCADA switching from an autonomous agent.
8. Do not auto-update dependencies or fetch confidential datasets without explicit authorization.

- Features 010–014: leer ADR-0004, ADR-0005, ADR-0006 y `docs/architecture/GRAPH_P2P_BLOCKCHAIN_V5.md` antes de modificar graph/P2P/ledger.
- Prohibido mezclar grafo lógico P2P, grafo comercial y grafo eléctrico terminal/fase.
- No ejecutar contratos ni transacciones reales desde pruebas, ni enviar datos de red sensibles a ledger.

## V6 — Agentes, skills y conectores

**Antes de cualquier tarea** consulta `.agents/skills/` según rol, `docs/agents/AGENT-ROLES.md`, `connectors/registry.json` y `docs/agents/SKILLS-AND-CONNECTORS.md`. El MCP local solo lee documentación allowlisted, y ningún conector opcional representa una conexión activa.

- Todo agente trabaja en un worktree por spec/feature; no hereda privilegios de otros agentes.
- Para backend aplica skill FastAPI + DDD + API Contracts; para frontend React + Design System + contratos. Validar conjuntamente con QA.
- MCP nunca sustituye RBAC/ABAC real, límites de base de datos, aprobación humana ni seguridad de red.
- No instalar MCP de terceros, habilitar GitHub-write, operar PostgreSQL productivo o descargar datasets regulados sin revisión y autorización explícitas.
- No afirmar test UI, conexión MCP real o backend/frontend ejecutables cuando aún no existen.


## Protocolo científico obligatorio UNITESIS V7
- Antes de diseñar o modificar un módulo, leer `docs/scientific-evidence/INDEX.md`, `MATRIX-MODULES.md` y `modules/<área>.md`.
- Consultar fichas Markdown en `sources/`; cada ficha indica si está basada en página localizada o referencia heredada V2. **Ninguna ficha reemplaza el artículo original**.
- Usar `python scripts/research/query_evidence.py` para búsquedas offline por palabras clave, módulo e idioma.
- Al proponer algoritmos o cambios de API/UI, añadir `specs/<feature>/research.md` con matriz evidencia-vacíos-pruebas; no confundir documentación técnica con artículo científico revisado por pares.
- No declarar PINN físicamente exacta, blockchain normativamente habilitada ni reproducibilidad sin evidencia ejecutada.
- Biblioteca multilingüe EN/ES/PT/FR/DE; no copiar PDFs ni transcripciones completas protegidas.

## UNITESIS V8 — PIT, PIDE, economía y PMBOK 6
Lea `docs/regulatory/INDEX.md`, `PIDE-ANNEX1-STATUS.md`, `SOURCES.json`, y `docs/project-management/PMBOK6-UNITESIS-MAPPING.md` antes de estudiar inversiones o agregar reglas de cumplimiento. Norma 217-2013 SST/SCT ≠ metodología PIDE; bloquea certificación de borradores. El perfil 217 original requiere consolidar todas sus modificatorias. La biblioteca V7 sigue vigente.

## V8.1 — prepublicación PIDE 2017
Para toda planificación de distribución leer `docs/regulatory/PIDE-2017-PREPUBLICACION-EL-PERUANO.md` y `docs/agents/PIDE-DISTRIBUTION-AGENT-QUERY.md`; perfil PIDE referencia no es norma aprobada, 20/4 histórico solo se aplica al caso explícito; comprobar FONAFE antes de usar trámite B.1.2.

## V8.2 — REGLA BASE PIDE DOCUMENTAL
**Leer primero** `docs/regulatory/pide_2017/INDEX.md`. RM 428-2017 prepublicó, no aprobó; Anexo original 01–15 pendiente. TDR Electro Puno 2018 NO es la norma. La calculadora `pide_reference` es ilustrativa; prohibido reportar cumplimiento regulatorio o estudios reales sin datos/solver.
