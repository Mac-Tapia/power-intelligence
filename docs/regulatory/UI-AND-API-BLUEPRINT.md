# Full Stack V8 — interfaz y contratos pendientes

## Workstation react frontend (React/TypeScript)
- `/regulations` catálogo por ámbito, versión y estado; banners «proyecto no vigente».
- `/studies/new` asistente área de demanda/empresa/periodo/norma; impide mezclas SST-SCT vs distribución.
- `/studies/{id}` subpestañas GIS/unifilar, demanda, estudios, alternativas, comparación económica, evidencia.
- `/projects/{id}` acta, EDT, recursos, costos, riesgos, cronograma, trazabilidad PMBOK.
- `/dossiers/{id}` documentos con formatos, anexos, firma y bloqueo si regla no consolidada.

## API contracts propuestos (NO endpoints implementados)
- `GET /api/v1/regulations?domain=transmission&at=...`
- `GET /api/v1/study-types`
- `POST /api/v1/studies` valida perfil, área, periodo, usuario.
- `POST /api/v1/studies/{id}/alternatives` registra mutación auditable sin tocar red real.
- `POST /api/v1/studies/{id}/simulations` encola solver aislado.
- `POST /api/v1/studies/{id}/economics` tras resultados físicos.
- `POST /api/v1/projects` genera artefactos y requiere aprobaciones.
- `GET /api/v1/dossiers/{id}` manifiesta bloqueos y referencias.

No hay servidor ni rutas implementadas en esta entrega: son contratos SDD a desarrollar y probar.
