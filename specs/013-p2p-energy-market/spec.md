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

---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-013` · **Gate:** `G6` · **Dependencias:** SPEC-011, SPEC-012, SPEC-019, SPEC-028.  
**Alcance verificable:** Simular escenarios de intercambio energético P2P con factibilidad física y sin liquidación real.  
**Ubicación propuesta:** `packages/python/power-market/, workers/market-clearing/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-013-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-013-02:** entrada válida: Transacciones se generan en modo simulación y toda alternativa es rechazada si viola AC/energía/reglas aplicables.
- **FR-013-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-013-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-013-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-013-01:** caso exitoso demuestra `FR-013-01/02` con fixture y evidencia automatizada.
- **AC-013-02:** caso negativo demuestra `FR-013-03`, sin alterar estado persistido ni fuente original.
- **AC-013-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-013-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
