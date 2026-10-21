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
- [ ] T010 Lector offline de la exportación ASCII CYMDIST (`eldu-cyme-ascii-2026-08`: RED con 96 cabeceras, 38 681 nodos y 38 657 secciones; CARGA con 7 287 cargas; BD_Equipo con R1/X1/ampacidad por código de conductor) → `ElectricalSnapshot` por alimentador, sin ejecutar CYME (ADR-0010). Mapeo `BD_Equipo` ↔ `CodNorma` del VNR para dar R/X reales al VNR-GIS.
- [ ] T011 Lector offline de bases MDB por alimentador (`eldu-cyme-study-mdb`), previa autorización del lector Access (pyodbc + driver ODBC, o mdbtools); usar solo las copias `original` como raw.
- [ ] T012 Exportaciones DGS en texto (cuando existan para el caso), con las mismas reglas. Una fuente sin catálogo, con CRS ausente o con secciones sin el prefijo esperado conserva todos los elementos contados con su motivo de rechazo; no se filtra ni se completa en silencio. Si faltan datos necesarios, el cálculo se bloquea.
