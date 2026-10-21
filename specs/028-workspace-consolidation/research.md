# Investigación y decisiones para 028

Consulta web: 20 de octubre de 2026. Registros y resúmenes consultados; no se afirma lectura integral ni reproducción de experimentos.

| Afirmación / decisión | Fuente | Supuesto o límite | Prueba local exigida |
|---|---|---|---|
| Diferenciar copias exactas, clones estructurales y diferencias | Gamvrinos, maestría TU Delft 2020: https://repository.tudelft.nl/record/uuid:399edf65-69c6-4d20-a3d7-9658ccb9bc17 ; Rattan et al., Information and Software Technology 2013: https://doi.org/10.1016/j.infsof.2013.01.008 | SHA/AST no implica equivalencia funcional ni autoriza borrado | Inventario y SHA completos de candidatos; preservar archivos exclusivos |
| Reutilizar con origen, versión y pruebas | Ragkhitwetsagul, doctorado UCL 2018: https://discovery.ucl.ac.uk/id/eprint/10057538/ | No se ejecutó Siamese; se adopta el principio de revisar versiones/licencias | Mapa source/hash/destino y regresión por componente |
| Un gemelo requiere fidelidad de modelos e interoperabilidad | Thwe et al., IEEE Access 2025, artículo indexado en Scopus según registro TU Delft: https://doi.org/10.1109/ACCESS.2025.3580055 | El artículo no valida el producto | Modelo con unidades, snapshot, cobertura y resultado verificable |
| Mantener solver físico y referencia independiente | Biblioteca local REF-040 pandapower, REF-042 MATPOWER y REF-044 PowerModelsDistribution: https://ieeexplore.ieee.org/document/8344496 ; https://ieeexplore.ieee.org/document/5491276/ ; https://doi.org/10.1016/j.epsr.2020.106664 | Alcance inicial equilibrado radial; sin transferencia a trifásico desbalanceado | Dos barras y caso abierto, balance y tolerancias explícitas |

Decisiones de ingeniería propias: reutilizar por módulos, mantener dominio puro, registrar lectura posterior y bloquear datos ausentes. La fuente local del barrido radial es `SelecCablesAAAC/.../aaac_pf/bfs_solver.py`; las interfaces neutrales y validación se contrastan con `flujos/src/flujos/solvers/`; la custodia con `Prodma/src/prodma/custody/`; evidencia con `PITELD/src/piteld/audit.py` y `RECYM/src/core/persisted_readback.py`.

## Ampliación arquitectónica verificada en la web

Faustino, D. A. dos R. (2021). *Stepwise migration of a monolith to a microservices architecture: Performance and migration effort evaluation* [Tesis de maestría, Instituto Superior Técnico]. [Registro institucional](https://scholar.tecnico.ulisboa.pt/records/XKqbIZTcTB73uxjyhKxgFUUKqlmfq9g3oTO7?lang=en).

El resumen compara esfuerzo y rendimiento al pasar de monolito a arquitectura modular y luego a microservicios; identifica costos ya en la etapa modular. Sustenta evaluar la migración por etapas y contratos. Mantener monolito modular con workers en este workspace es decisión local, coherente con ADR-0001, no resultado demostrado por esa tesis sobre PowerIntelligence. La consulta fue al registro/resumen; no se reprodujeron mediciones.

Gamvrinos, S. (2020). *Language-agnostic incremental code clone detection* [Tesis de maestría, Delft University of Technology]. [Registro institucional](https://repository.tudelft.nl/record/uuid:399edf65-69c6-4d20-a3d7-9658ccb9bc17). Se verificaron tipo, año y resumen. Justifica distinguir detección exacta de equivalencia funcional; esta auditoría utiliza SHA/AST, no LIICD ni LSH.

Ragkhitwetsagul, C. (2018). *Code similarity and clone search in large-scale source code data* [Tesis doctoral, University College London]. [Registro institucional](https://discovery.ucl.ac.uk/id/eprint/10057538/). Sustenta tratar similitud, versiones y reutilización como revisión de evidencia, no autorización automática de eliminación. No se ejecutó Siamese. Registro consultado en la investigación original; una reapertura posterior devolvió timeout, sin invalidar la consulta previa.

Thwe, M. M., Stefanov, A., Rajkumar, V. S., & Palensky, P. (2025). Digital twins for power systems: Review of current practices, requirements, enabling technologies, data federation and challenges. *IEEE Access, 13*, 105517–105540. https://doi.org/10.1109/ACCESS.2025.3580055. [Registro institucional](https://research.tudelft.nl/en/publications/digital-twins-for-power-systems-review-of-current-practices-requi/) identifica artículo revisado por pares y Scopus 105008648157. Su resumen trata fidelidad, modelos e interoperabilidad; sustenta contratos y procedencia, no certifica el núcleo ni establece nuestras tolerancias.

Estas fuentes no prueban que ningún archivo concreto sea eliminable. La evidencia local exigida es journal por archivo, SHA completo cuando corresponde, preservación de contexto y pruebas de sustitución. Las tolerancias de spec.md, la ubicación inicial del forecasting y los nombres de estados son decisiones de ingeniería pendientes de implementación y calibración.
