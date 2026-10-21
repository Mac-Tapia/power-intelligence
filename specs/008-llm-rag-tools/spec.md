# 008 — LLM local con RAG, herramientas tipadas y revisión humana

**Estado:** propuesta, sin código. Paquetes: `power-graphrag` (índice y citas) y `power-agents` (orquestación). Relacionada con 014 y 015.

## Decisión

No se preentrena un modelo propio. Primero se implementa RAG con citas y tool calling sobre la CLI y la API. Después, opcionalmente, se ajusta (LoRA) un modelo local con trazas de herramientas generadas y verificadas por el sistema (029), solo si mejora la evaluación.

## Criterios de aceptación

- AC-008-01: toda cifra eléctrica de una respuesta proviene de una llamada a herramienta con su `result_sha256`. El LLM no calcula flujos.
- AC-008-02: toda afirmación normativa cita un fragmento de una fuente registrada, con versión. Si no hay fragmento, la respuesta es "no fundamentado".
- AC-008-03: la evaluación `eval-electrical-qa` mide exactitud numérica frente al solver, tasa de citas válidas y tasa correcta de "no fundamentado". Incluye pruebas de inyección de instrucciones en documentos.
- AC-008-04: no se envían datos de clientes en prompts a modelos externos. El modelo es local, salvo autorización expresa.
- AC-008-05: las acciones que cambian estado (crear un estudio, publicar evidencia) requieren confirmación humana.
