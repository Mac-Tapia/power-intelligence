# Tareas 001 — Ingesta VNR-GIS y fuentes eléctricas (universal; piloto `pe-ica-electrodunas`)

- [ ] T001 Catalogar y verificar legalmente al menos dos esquemas de entrada representativos (piloto: VNR-GIS Electro Dunas abr‑2024; autorización en `config/cases/pe-ica-electrodunas.json`).
- [ ] T002 Esquemas declarativos tipados y versión del mapping (por formato/versión VNR, no por empresa).
- [ ] T003 Lector RAW + hash + manifiesto y validaciones de integridad. Restaurar el `.bak` en una base local nueva, en solo lectura.
- [ ] T004 Normalización de CRS (desde el caso; verificar contra la fuente), unidades y nombres según campos documentados; tabla versionada `CodTenNomi` → kV.
- [ ] T005 Grafo por equipo/terminal/fase/switch: conectividad `CodTramoMTPadre` (raíz `'0'`), estado `CodEstadoOperacion` (NC/NA) → `closed` por regla documentada.
- [ ] T006 QA: huérfanos, islas, alimentadores con varias raíces, solapes, fases incompatibles, campos obligatorios.
- [ ] T007 Cuarentena de faltantes sin imputación por defecto; mapeo `CodNorma` → catálogo de conductores con fuente; lo no mapeable queda bloqueado para el cálculo.
- [ ] T008 Tests unitarios/contract/golden con VNR sintético y prueba de determinismo (mismo origen → mismo `content_sha256`).
- [ ] T009 Publicar la evidencia y revisar la aceptación con un ingeniero.
- [ ] T010 Lectores offline de exportaciones DGS/CYME en texto, sin ejecutar esos programas (ADR-0010). Una fuente sin catálogo, con CRS ausente o con secciones sin el prefijo esperado conserva todos los elementos contados con su motivo de rechazo; no se filtra ni se completa en silencio. Si faltan datos necesarios, el cálculo se bloquea.
