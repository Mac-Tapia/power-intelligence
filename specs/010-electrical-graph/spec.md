# Spec — Proyecciones Graph eléctricas y de conocimiento

**Estado:** DRAFT / Not implemented · Feature ID `010`.

## User intent y alcance
Construir proyección de lectura por snapshot a partir del maestro terminal/fase, con consultas trazables de activos, feeders, rutas y evidencia. Distinguir grafo eléctrico y grafo de conocimiento, incluyendo GraphRAG con referencias.

## Requerimientos verificables
- No usar geometría como prueba de conectividad; cada relación debe tener provenance/snapshot.
- Mantener modelos multi-fase y versiones de estado de interruptor.
- Prohibido escribir de GraphRAG al maestro físico.
- Comparativa PostgreSQL/PostGIS/NetworkX frente a Neo4j opcional.

## Criterios de aceptación
- 100% de edges de test sintético referencian endpoints existentes.
- Cambiar estado de interruptor genera snapshot nuevo sin modificar el anterior.
- Mismatched snapshot en consulta produce error, no mezcla.
- Consultas sin permiso cross-tenant no devuelven datos.

## Restricciones
Se prohíben ejecuciones sobre SCADA/protecciones. No se debe acceder a datos no autorizados ni inferir valores faltantes. El acceso comercial solo tras aprobación legal/regulatoria verificable.

## Dependencias
`001` ingesta y contratos; `003` GIS/unifilar; `004` solver validado; el resto según orden de `docs/traceability/FEATURE-MAP.md`.

---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-010` · **Gate:** `G1` · **Dependencias:** SPEC-001, SPEC-006.  
**Alcance verificable:** Construir grafo topológico por terminal/fase/estado, separado del GIS, conocimiento y comunicación.  
**Ubicación propuesta:** `packages/python/power-graph/, power-topology/, workers/graph-projection/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-010-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-010-02:** entrada válida: El grafo conserva fases/switches y consultas de alimentador; falla por islas críticas o fuentes inconsistentes sin simular conexiones inexistentes.
- **FR-010-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-010-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-010-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-010-01:** caso exitoso demuestra `FR-010-01/02` con fixture y evidencia automatizada.
- **AC-010-02:** caso negativo demuestra `FR-010-03`, sin alterar estado persistido ni fuente original.
- **AC-010-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-010-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
