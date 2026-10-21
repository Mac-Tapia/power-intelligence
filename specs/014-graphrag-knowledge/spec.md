# Spec — GraphRAG técnico trazable de evidencias/normas

**Estado:** DRAFT / Not implemented · Feature ID `014`.

## User intent y alcance
Recuperar contextos documentales y relaciones de estudios/normas con citas, ACL y snapshot correcto; no generar parámetros eléctricos inventados.

## Requerimientos verificables
- Separar retrieval documental de la topología física.
- Citar fuentes y versiones con retrieval determinista auditable.
- Bloquear prompt injection y cruces multi-tenant.
- Evaluar contra búsqueda léxica/vectorial sin Grafo.

## Criterios de aceptación
- 100% de respuestas con norma enlazan fragmento verificable.
- Los documentos inyectados no ejecutan instrucciones.
- Retrieval de un snapshot no extrae evidencia de otro.
- Resultados incorrectos regresan "no fundamentado".

## Restricciones
Se prohíben ejecuciones sobre SCADA/protecciones. No se debe acceder a datos no autorizados ni inferir valores faltantes. El acceso comercial solo tras aprobación legal/regulatoria verificable.

## Dependencias
`001` ingesta y contratos; `003` GIS/unifilar; `004` solver validado; el resto según orden de `docs/traceability/FEATURE-MAP.md`.
