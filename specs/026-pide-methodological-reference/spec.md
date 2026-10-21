# Feature 026: PIDE — planificación de distribución basada en metodología prepublicada

## Objetivo
Permitir estudios técnicos-económicos de distribución siguiendo etapas metodológicas documentadas sin atribuirles vigencia reglamentaria no acreditada.

## Historias
- Como ingeniero quiero importar un GIS/VNR-GIS y proyectar demanda en horizontes configurables para diagnosticar alimentadores.
- Como planificador quiero comparar alternativas técnicas factibles y organizar una cartera anual documentada.
- Como auditor quiero distinguir evidencia oficial, proyecto prepublicado y TDR histórico por cada regla.

## Requisitos de aceptación
1. Pantalla y exportación indican: «PIDE: metodología de referencia prepublicada 2017; no aprobación normativa demostrada».
2. PIDE DL1208 restringido a FONAFE; estudios corporativos para privadas no cambian elegibilidad.
3. 20/4 años solo se autocompletan cuando el usuario elige explícitamente el **caso histórico Electro Puno 2018**; en los demás casos campos nulos hasta selección.
4. Trazabilidad de variantes y comparación económica sin parámetros imputados desde PIT.
5. Aplicar restricciones eléctricas vigentes por caso; resultados IA requieren validación con solver independiente.
6. Las fichas/formatos oficiales solo se activan tras auditar el anexo original y su vigencia.
7. Integra PMBOK 6 para proyecto seleccionado, con responsables y matriz de riesgos.

---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-026` · **Gate:** `G4` · **Dependencias:** SPEC-000.  
**Alcance verificable:** Preservar prepublicación MINEM 2017 con estado jurídico correcto y traza a fuentes.  
**Ubicación propuesta:** `docs/regulatory/, config/regulations/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-026-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-026-02:** entrada válida: Se conoce fuente El Peruano; no se confunde autorización de prepublicación con aprobación definitiva.
- **FR-026-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-026-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-026-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-026-01:** caso exitoso demuestra `FR-026-01/02` con fixture y evidencia automatizada.
- **AC-026-02:** caso negativo demuestra `FR-026-03`, sin alterar estado persistido ni fuente original.
- **AC-026-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-026-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.
