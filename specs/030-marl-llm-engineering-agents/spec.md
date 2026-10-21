# SPEC-030 — marl-llm-engineering-agents

**Propósito:** Coordinar agentes especializados y políticas MARL con herramientas tipadas, simulador aislado y revisión humana.


---

## Anexo del plan maestro — Alcance y aceptación ejecutable (pendiente)

**Requisito:** `SPEC-030` · **Gate:** `G5` · **Dependencias:** SPEC-019, SPEC-029, SPEC-015.  
**Alcance verificable:** Coordinar agentes especializados y políticas MARL con herramientas tipadas, simulador aislado y revisión humana.  
**Ubicación propuesta:** `packages/python/power-agents/, power-marl/, workers/agent-runtime/`.

### Historias funcionales
- Como ingeniero/planificador, necesito usar este módulo sin falsear parámetros ni resultados.
- Como responsable técnico, necesito revisar evidencia, versión, normativa y resultados antes de aprobar un estudio.
- Como desarrollador/QA, necesito replicar fallos y casos positivos con tests y entradas versionadas.

### Requisitos y aceptación del plan maestro
- **FR-030-01:** implementar el comportamiento descrito en alcance, con contrato versionado y campos obligatorios documentados.
- **FR-030-02:** entrada válida: Agentes solo modifican escenarios clonados; acciones de red propuestas pasan solver/ACL y registran recompensas y rechazos.
- **FR-030-03:** entrada inválida/incompleta produce error tipado, auditable y sin valores silenciosos.
- **NFR-030-01:** separar dominio, casos de uso, puertos, adaptadores e interfaz; prohibido import circular y conexión a producción en tests.
- **NFR-030-02:** preservar trazabilidad de usuario/tenant, timestamp UTC, versión, hash de input y commit cuando aplique.
- **AC-030-01:** caso exitoso demuestra `FR-030-01/02` con fixture y evidencia automatizada.
- **AC-030-02:** caso negativo demuestra `FR-030-03`, sin alterar estado persistido ni fuente original.
- **AC-030-03:** integración/extremo a extremo y revisión técnica documentadas; tests verdes en CI.
- **AC-030-04:** normativa y licenciamiento verificados cuando afectan al resultado; ningún borrador PIDE tratado como vigente.

### Límites y estado
**Estado actual: especificación de implementación, no funcionalidad terminada.** Mantener los criterios anteriores de este documento como requisitos acumulativos. Cualquier contradicción debe resolverse con ADR y revisión humana.

## Criterios vigentes incorporados (antes spec 007)

**Estado:** propuesta, sin código en el núcleo. El entorno es universal y se instancia por caso de aplicación (spec 035). Hay prototipos en proyectos archivados de otras localidades (Iquitos, Lima), sin integrar; sus datos son solo `method_reference`. Paquete: `power-marl`; entrenamiento en `workers/ml-training`.

### Criterios de aceptación

- AC-030-M01: entrena con el dataset gold `district-flex-<case_id>` del caso. El piloto `pe-ica-electrodunas` se construye desde clientes importantes, medidores y exógenas reales de Electro Dunas. Ninguna observación de pronóstico tiene estado `oracle`. Los splits son por años disjuntos.
- AC-030-M02: los resultados previos obtenidos con la referencia de Iquitos (pronóstico oráculo) no se citan como resultado del producto. Si se usan para desarrollar métodos, se reportan con oráculo y con pronóstico honesto para cuantificar el sesgo.
- AC-030-M03: cada edificio o cliente se asigna a una barra del snapshot del caso de forma explícita. Las violaciones de tensión o cargabilidad que detecte el solver (o el sustituto 006, confirmado) son una restricción o una penalización registrada.
- AC-030-M04: hay una línea base basada en reglas (TOU y carga de VE inmediata) y comparaciones con HAPPO, MAPPO, MASAC y MATD3, con al menos 5 semillas e intervalos de confianza.
- AC-030-M05: las métricas de flexibilidad, CO2 y costo llevan unidades explícitas y la moneda del caso (`economics.currency`); el factor de emisión es un dato con fuente de la jurisdicción del caso.
- AC-030-M06: las políticas son propuestas en sandbox; no hay comandos a SCADA ni a equipos reales.

## Criterios vigentes incorporados (antes spec 008)

**Estado:** propuesta, sin código. Paquetes: `power-graphrag` (índice y citas) y `power-agents` (orquestación). Relacionada con 014 y 015.

### Decisión

No se preentrena un modelo propio. Primero se implementa RAG con citas y tool calling sobre la CLI y la API. Después, opcionalmente, se ajusta (LoRA) un modelo local con trazas de herramientas generadas y verificadas por el sistema (029), solo si mejora la evaluación.

### Criterios de aceptación

- AC-030-L01: toda cifra eléctrica de una respuesta proviene de una llamada a herramienta con su `result_sha256`. El LLM no calcula flujos.
- AC-030-L02: toda afirmación normativa cita un fragmento de una fuente registrada, con versión. Si no hay fragmento, la respuesta es "no fundamentado".
- AC-030-L03: la evaluación `eval-electrical-qa` mide exactitud numérica frente al solver, tasa de citas válidas y tasa correcta de "no fundamentado". Incluye pruebas de inyección de instrucciones en documentos.
- AC-030-L04: no se envían datos de clientes en prompts a modelos externos. El modelo es local, salvo autorización expresa.
- AC-030-L05: las acciones que cambian estado (crear un estudio, publicar evidencia) requieren confirmación humana.
