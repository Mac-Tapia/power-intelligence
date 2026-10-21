---
name: unitesis-pide-planning
description: Revisar, planificar y programar estudios de distribución UNITESIS basados en evidencia PIDE, separando prepublicación MINEM, TDR históricos y normas vigentes.
---
# PIDE Planning Skill

Antes de responder o cambiar código leer obligatoriamente:
1. `docs/regulatory/pide_2017/INDEX.md`
2. `docs/regulatory/pide_2017/sources.json` y `specs/027-pide-source-audit-and-reference-engine/`
3. `docs/regulatory/pide_2017/MATRIZ-TRAZABILIDAD.md`
4. `config/regulations/pide_tdr_2018_trace.json`
5. `config/regulations/pide_formats_original_pending.json`
6. `specs/021-pide-planning-engine/` y `specs/026-pide-methodological-reference/`

## Protocolo
- Determinar perfil: estudio interno, proyecto histórico Electro Puno 2018 o trámite FONAFE.
- No afirmar que RM 428-2017-MEM/DM aprobó el anexo; es PREPUBLICACIÓN.
- El documento MINEM íntegro está **pendiente**. No inventar los nombres, columnas, escalas ni fórmulas de formatos 01–15.
- Para histórico Electro Puno 2018: horizonte 20 años, hitos 4/8/12/16/20, cartera cuatro años, mínimo 3 opciones, vida útil 30 años; todos etiquetados como TDR histórico.
- Exigir solver independiente para aceptar factibilidad, y fuente de tasa/precios para economía.
- Cualquier PMBOK 6 está adaptado a proyectos de inversión, no reemplaza permisos regulatorios.
- Ejecutar `python -m pytest -q` y documentación de evidencia.
