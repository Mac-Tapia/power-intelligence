# Plan — GraphRAG técnico trazable de evidencias/normas

**Estado:** DRAFT; no desplegado.

## Contexto y boundaries
Recuperar contextos documentales y relaciones de estudios/normas con citas, ACL y snapshot correcto; no generar parámetros eléctricos inventados.

## Plan de implementación
1. Congelar diseño, ADRs y amenazas; especificar interfaces y versiones.
2. Construir el adaptador de referencia aislado, con fixtures sintéticos.
3. Verificar invariantes, seguridad, reproducibilidad y pruebas negativas.
4. Ejecutar integración con la API/workers y generación de evidencia.
5. Benchmark, revisión y PR según SDD y Git worktree.

## Tasks
- Ontology de assets / studies / standards / evidence
- Pipeline RAG y GraphRAG con metadatos/versiones
- Conectar índice de grafos con ACL sin PII
- Pruebas RAGAS/groundedness y red-team prompt injection
- Interfaz evidencias con subgrafo y citas

## Gates de aprobación
- 100% de respuestas con norma enlazan fragmento verificable.
- Los documentos inyectados no ejecutan instrucciones.
- Retrieval de un snapshot no extrae evidencia de otro.
- Resultados incorrectos regresan "no fundamentado".
