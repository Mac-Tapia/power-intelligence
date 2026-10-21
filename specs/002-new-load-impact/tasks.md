# Tareas 002

- [x] T002-01: escenario clonado con carga nueva y cribado equilibrado antes/después (CLI `new-load`, API, UI); el hash del origen no cambia (`tests/integration/test_study_vertical.py`).
- [x] T002-02: criterios de cribado desde `planning_criteria` del caso (NTCSE, numeral por verificar), con precedencia orden > caso > valor por defecto etiquetado; la fuente queda en la evidencia (`--case`).
- [x] T002-03: capacidad remanente por barra sobre la red real del caso (`hosting-capacity`, `unitesis_application.hosting_capacity`): el sustituto criba y el solver certifica cada límite; los límites coinciden con un barrido exhaustivo (`tests/unit/test_hosting_capacity.py`). Alimentador real IC103: 190 barras, 1 106 llamadas al solver frente a 9 120 por fuerza bruta.
- [ ] T002-04: estudio por fase (depende de 004-C) y mitigaciones vía spec 005.
- [ ] T002-05: revisión humana del cribado con un caso real de Electro Dunas autorizado.
