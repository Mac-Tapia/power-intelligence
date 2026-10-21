# 027 — Auditoría de Anexo PIDE y motor de referencia

## User stories
- Como ingeniero necesito aplicar un protocolo de distribución documentado por fuentes y ver su naturaleza no vinculante.
- Como regulador/auditor necesito saber qué viene del TDR 2018 frente al anexo MINEM 2017.
- Como agente IA necesito 15 placeholders de formatos cuya oficialidad permanezca bloqueada hasta auditar el PDF de origen.

## Acceptance scenarios
- Given perfil histórico 2018, when hay menos de 3 opciones, then no satisface integridad documental.
- Given cualquier perfil prepublicado, when se solicita certificación, then error bloqueante.
- Given alternativa declarada viable sin solver independiente, then queda evidencia incompleta.
- Given costos/tasa/vida explicitados, when se calcula anualidad, then salida etiqueta `illustrative`.
- Given empresa diferente, when aplica un estudio corporativo, then no hereda 20/4 ni tres opciones por defecto.
- Given PDF original, when se registra, then se calcula SHA real y NO se certifica hasta revisión humana.

---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-027` · **Gate:** `G4` · **Dependencias:** SPEC-026.  
**Alcance verificable:** Auditar el Anexo 1 PIDE y aplicar sus métodos solo si la fuente primaria respalda el campo y fórmula.  
**Ubicación propuesta:** `docs/regulatory/, power-regulation/, tests/contract/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-027-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-027-02:** entrada válida: 15 formatos marcados pendientes hasta auditar PDF; costo anualizado ilustrativo y número de opciones condicionado al perfil.
- **FR-027-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-027-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-027-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-027-01:** caso exitoso demuestra `FR-027-01/02` con fixture y evidencia automatizada.
- **AC-027-02:** caso negativo demuestra `FR-027-03`, sin alterar estado persistido ni fuente original.
- **AC-027-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-027-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
