# SPEC-037 — power-format-interop-dgs-mdb-sql

**Propósito:** Exportar/importar formatos eléctricos con especificaciones versionadas, preservación de semántica y pérdidas reportadas.


---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-037` · **Gate:** `G1` · **Dependencias:** SPEC-001, SPEC-006.  
**Alcance verificable:** Exportar/importar formatos eléctricos con especificaciones versionadas, preservación de semántica y pérdidas reportadas.  
**Ubicación propuesta:** `packages/python/power-adapters/, contracts/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-037-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-037-02:** entrada válida: Round-trip controlado detecta cualquier campo perdido; importaciones no afirman compatibilidad propietaria sin pruebas.
- **FR-037-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-037-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-037-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-037-01:** caso exitoso demuestra `FR-037-01/02` con fixture y evidencia automatizada.
- **AC-037-02:** caso negativo demuestra `FR-037-03`, sin alterar estado persistido ni fuente original.
- **AC-037-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-037-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.

## Ingeniería inversa acotada (ADR-0012)

- AC-037-R01: la estructura de cada formato real se recupera de archivos del propietario (secciones, columnas, tipos, cobertura del lector) sin copiar valores de registros; la versión que se publica contiene solo estructura.
- AC-037-R02: un código no documentado se interpreta solo si su correspondencia con un campo documentado es determinista; con conflicto o un solo valor observado queda como regla pendiente de confirmar.
- AC-037-R03: queda prohibido descompilar, desensamblar o interceptar programas propietarios y usar sus APIs (ADR-0010).
