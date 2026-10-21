# Protocolo de revisión bibliográfica y de evidencia (preparado, NO ejecutado íntegramente)

## Alcance y cadena de búsqueda
- Bases objetivo: IEEE Xplore, Scopus, Web of Science, ACM Digital Library, Springer, Elsevier/ScienceDirect, Google Research, DeepMind, Anthropic, arXiv, HAL/theses.fr, repositorios UPM/UC3M, Unesp, USP, TU Delft, Georgia Tech.
- Idiomas: EN, ES, PT, FR, DE. Consultas normalizadas por sinónimo y dominio (ver `modules/*.md`).
- Período preferente: 2016–2026; se retienen obras fundacionales antiguas si aportan algoritmos o patrones relevantes.
- Inclusión: fuente institucional y pertinencia con capacidad concreta del sistema, metodología explícita, al menos metadatos recuperables.
- Exclusión: DOI no coincidente, páginas sin título/autor identificable, duplicados de preprints/edición final, publicidad no verificable y papers retractados.

## Estados de verificación
- `identificado_en_fuente_web`: página o registro localizado en la sesión; **no significa lectura del texto completo**.
- `importado_pendiente_auditoria`: referencia conservada de V2 que necesita comprobación de DOI, metadatos y edición.
- `metadatos_pendientes_confirmacion`: título/enlace de match incompleto, no citar como publicación confirmada.
- `texto_completo_revisado`: reservado para una iteración futura con revisión y notas verificables; actualmente cero.

## Tareas pendientes para afirmar 'revisión sistemática'
1. Exportar resultados con consulta, base, fecha, filtros y recuentos PRISMA.
2. Inspeccionar texto completo legítimo y extraer métodos, datos, validación y limitaciones, citando sección/página.
3. Revisar replicabilidad, comparadores, sesgo, conflictos de interés y validez externa.
4. Verificar DOI, indexación, autores, título de tesis, grado, año, universidad y ediciones de normas.
5. Consolidar preprint vs versión definitiva, marcando cada par, y mantener registro de retraction/watch.
6. Validar permisos y copyright. No incluir los PDFs de terceros en el ZIP sin licencia.
7. Registrar referencias APA/IEEE mediante metadatos confirmados, no reconstruirlos desde títulos.

## Evaluación de transferencia y gradiente de evidencia
| Nivel | Evidencia | Uso permitido |
|---|---|---|
| A | Experimento replicado en dataset VNR-GIS/IEEE + benchmark | Criterio de aceptación implementable |
| B | Estudio externo peer-reviewed leído y con metodología | Hipótesis de implementación + prueba |
| C | Preprint/tesis con métodos identificados | Prototipo y validación independiente |
| D | Manual/guía/portal | Selección de biblioteca y contrato, no afirmación de eficacia |
| E | Referencia importada y no auditada | Ruta de consulta, **no prueba científica** |

## Guardrails del sector eléctrico
- Una PINN no garantiza de forma exacta las ecuaciones AC; hay que resolver mismatch, errores fuera de distribución y corrección/rechazo.
- Un LLM no realiza estudios certificados ni sustituye la validez de un cálculo AC o una firma autorizada.
- La capa blockchain no decide factibilidad eléctrica y un mercado P2P hipotético no habilita comercio regulado en Perú.
