---
name: unitesis-p2p-blockchain
description: "Construir P2P seguro y evidencia blockchain opcional off-chain-first. Úsalo al trabajar en packages/python/power-p2p/"
---
# unitesis-p2p-blockchain

## Activación
Construir P2P seguro y evidencia blockchain opcional off-chain-first.

## Lecturas obligatorias
`AGENTS.md`, `.specify/memory/constitution.md`, `docs/architecture/MODULE-BOUNDARIES.md`, spec vigente y ADR relacionados. Revisar también `docs/agents/AGENT-ROLES.md`.

## Procedimiento
1. Leer ADR-0005/0006 y revisar marco comercial de Perú antes de cualquier piloto.
2. Separar comunicación P2P y comercio de energía; validar identities, TTL, firmas y replay. Ejecutar simulador de mercado 15 min, luego solver AC y aprobaciones; ledger guarda compromisos mínimos, no datos sensibles.
3. Escribir o actualizar pruebas y evidencias por ID de tarea de `specs/` antes de cerrar el PR.
4. Ejecutar la verificación aplicable: `tests/blockchain-lab/ y tests/security/`. Si falta un comando o entorno, registrar el bloqueo y no afirmar que la prueba pasó.

## Límites no negociables
No abrir transacciones reales, desplegar validadores externos ni operar equipos sin aprobación humana explícita.

## Alcance
packages/python/power-p2p/; packages/python/power-ledger/; packages/python/power-market/

## Entrega
Resumen de cambios, decisiones, artefactos, pruebas ejecutadas realmente, errores, riesgos abiertos y vínculo al PR/spec.


## Fuentes de investigación UNITESIS V7
Antes de implementar, consultar `docs/scientific-evidence/modules/p2p.md`, `docs/scientific-evidence/modules/ledger.md`, `docs/scientific-evidence/modules/market.md`, `docs/scientific-evidence/modules/security.md`, además de `docs/scientific-evidence/MATRIX-MODULES.md`. Validar ficha y tipo de evidencia, documentar fuente y experimento en la spec. Nunca tratar referencias pendientes o abstracts como validación de producto.
