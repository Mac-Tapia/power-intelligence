# Spec — Mercado simulado de energía/flexibilidad condicionado a red

**Estado:** DRAFT / Not implemented · Feature ID `013`.

## User intent y alcance
Evaluar matching de ofertas prosumidor-BESS-EV con pérdidas, congestión, seguridad y legalidad, sin asumir habilitación peruana de venta P2P.

## Requerimientos verificables
- Default simulation; no pagos, contratos ni activos reales.
- Liquidación exige dictamen normativo, medición, solver AC y firma humana.
- Separar optimización off-chain y ledger de finalización.
- Comparar doble subasta, clearing central y ADMM/mercados locales.

## Criterios de aceptación
- Oferta que viola tensión o ampacidad es rechazada.
- No settlement si faltan medición aprobada/solver o licencia.
- No hay trades duplicados en reintentos y fallas de red.
- Simulaciones en IEEE33/IEEE123 sintéticos comparan bienestar, pérdidas y equidad.

## Restricciones
Se prohíben ejecuciones sobre SCADA/protecciones. No se debe acceder a datos no autorizados ni inferir valores faltantes. El acceso comercial solo tras aprobación legal/regulatoria verificable.

## Dependencias
`001` ingesta y contratos; `003` GIS/unifilar; `004` solver validado; el resto según orden de `docs/traceability/FEATURE-MAP.md`.
