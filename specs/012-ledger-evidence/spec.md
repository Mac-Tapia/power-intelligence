# Spec — Registro criptográfico y blockchain permissioned optativo

**Estado:** DRAFT / Not implemented · Feature ID `012`.

## User intent y alcance
Anclar hash de evidencia en registro verificable y comparar log firmado central vs Hyperledger Fabric y Besu en laboratorio aislado.

## Requerimientos verificables
- No insertar archivos originales, topología, PII, SCADA ni precios privados on-chain.
- Anclaje posterior a validación off-chain.
- No bloquear solver o planificación al caer consenso.
- Idempotencia, finality y decisión de gobernanza documentada.

## Criterios de aceptación
- La modificación de 1 byte de evidencia cambia el digest SHA-256.
- Caída de blockchain no invalida estudio ni altera su hash.
- No se permite anchor CONFIRMED sin transacción verificada.
- PR aporta benchmarks de costo, TPS, latencia y fault tolerance con métrica reproducible.

## Restricciones
Se prohíben ejecuciones sobre SCADA/protecciones. No se debe acceder a datos no autorizados ni inferir valores faltantes. El acceso comercial solo tras aprobación legal/regulatoria verificable.

## Dependencias
`001` ingesta y contratos; `003` GIS/unifilar; `004` solver validado; el resto según orden de `docs/traceability/FEATURE-MAP.md`.
