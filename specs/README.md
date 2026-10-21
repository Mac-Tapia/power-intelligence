# Especificaciones

Una carpeta por capacidad con identificador estable `NNN-titulo`. `spec.md` contiene el qué y el porqué, con criterios de aceptación verificables; `tasks.md` contiene las tareas trazables. `plan.md` es opcional, para el diseño cuando hace falta. Una tarea se marca `[x]` solo con evidencia ejecutada (pruebas, comandos, archivos).

El índice con el estado de cada spec está en `docs/traceability/FEATURE-MAP.md`. Toda spec listada allí debe existir aquí y viceversa; lo comprueba `scripts/verify_structure.py`.
