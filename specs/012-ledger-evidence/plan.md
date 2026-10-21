# Plan — Registro criptográfico y blockchain permissioned optativo

**Estado:** DRAFT; no desplegado.

## Contexto y boundaries
Anclar hash de evidencia en registro verificable y comparar log firmado central vs Hyperledger Fabric y Besu en laboratorio aislado.

## Plan de implementación
1. Congelar diseño, ADRs y amenazas; especificar interfaces y versiones.
2. Construir el adaptador de referencia aislado, con fixtures sintéticos.
3. Verificar invariantes, seguridad, reproducibilidad y pruebas negativas.
4. Ejecutar integración con la API/workers y generación de evidencia.
5. Benchmark, revisión y PR según SDD y Git worktree.

## Tasks
- Implementar EvidenceStore + append-only signed log baseline
- Definir LedgerAnchorPort + schema y eventos
- Proof-of-concept Fabric private data con permisos
- Proof-of-concept Besu QBFT con n>=4 validators
- Informe ADR coste/beneficio/gobernanza y hardening claves

## Gates de aprobación
- La modificación de 1 byte de evidencia cambia el digest SHA-256.
- Caída de blockchain no invalida estudio ni altera su hash.
- No se permite anchor CONFIRMED sin transacción verificada.
- PR aporta benchmarks de costo, TPS, latencia y fault tolerance con métrica reproducible.
