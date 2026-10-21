# Prompt de consulta científica para cualquier agente UNITESIS

1. Identifica qué cambio del código/spec se solicita y módulo asociado de `MATRIX-MODULES.md`.
2. Lee `modules/<dominio>.md` y 3 a 8 fichas de fuentes **relevantes**; no tomes una URL como resultado de una lectura completa.
3. Responde con una matriz: **afirmación** / **fuente con URL** / **tipo** / **limitación** / **decisión** / **test**.
4. Distingue explícitamente revisión por pares, tesis, preprint, libro, norma y documentación de SDK.
5. Si se requiere una afirmación o fórmula exacta del artículo, abre el original con permiso y comprueba sección, edición, DOI y página.
6. Inserta evidencia y plan en `specs/<feature>/research.md` antes del PR.
7. Rechaza cualquier afirmación de velocidad, precisión, reducción de pérdidas o conformidad normativa sin benchmark del repositorio.

**Ejemplo de consulta:**
> Analiza si conviene un modelo Physics-Informed GNN para flujo AC trifásico en una topología cambiante importada del VNR-GIS. Compara contra DSS-Extensions/pandapower; presenta referencias y casos de prueba IEEE 13/34/123 y retención de calibración fuera de distribución.

**Salida requerida:** alternativa propuesta, contraargumento, benchmark, criterios GO/NO-GO, referencias con hipervínculo.
