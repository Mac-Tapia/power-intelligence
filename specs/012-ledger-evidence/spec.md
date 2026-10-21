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

---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-012` · **Gate:** `G6` · **Dependencias:** SPEC-011, SPEC-032.  
**Alcance verificable:** Registrar anclajes verificables de evidencias con ledger opcional, manteniendo datos sensibles off-chain.  
**Ubicación propuesta:** `packages/python/power-ledger/, workers/ledger-anchoring/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-012-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-012-02:** entrada válida: Hash anclado es verificable e idempotente; ausencia de red blockchain no bloquea estudios pero sí anclajes requeridos.
- **FR-012-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-012-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-012-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-012-01:** caso exitoso demuestra `FR-012-01/02` con fixture y evidencia automatizada.
- **AC-012-02:** caso negativo demuestra `FR-012-03`, sin alterar estado persistido ni fuente original.
- **AC-012-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-012-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
