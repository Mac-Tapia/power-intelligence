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
- [x] T010 Lector offline CYME ASCII (`unitesis_adapters.cyme_ascii`, CLI `import-cyme`, caso de uso `network_import`). Reglas declaradas en el caso: `DEFAULT` ≤ 10 m como conexión ideal, Status 1 = cerrado, ValueType 2 = kW+fp, carga en el ToNode; aproximación de secuencia positiva solo si se declara. Red real Electro Dunas: 93 alimentadores leídos, 44 validados y 49 en cuarentena con motivo (222 secciones con código fuera del catálogo, laterales no trifásicos). Los 44 calculan con Newton-Raphson y pasan el contraste pandapower (ΔV ≤ 8e-10 p.u.). Pruebas: `tests/unit/test_cyme_ascii_reader.py`. Pendiente: mapeo `BD_Equipo` ↔ `CodNorma` (con el VNR restaurado).
- [ ] T011 Lector offline de bases MDB por alimentador (`eldu-cyme-study-mdb`), previa autorización del lector Access (pyodbc + driver ODBC, o mdbtools); usar solo las copias `original` como raw.
- [ ] T012 Exportaciones DGS en texto (cuando existan para el caso), con las mismas reglas. Una fuente sin catálogo, con CRS ausente o con secciones sin el prefijo esperado conserva todos los elementos contados con su motivo de rechazo; no se filtra ni se completa en silencio. Si faltan datos necesarios, el cálculo se bloquea.

## Backlog del plan maestro — tareas pendientes

**Gate:** G1 · **Depende de:** SPEC-006

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-001/T201** — Inventariar dos fuentes públicas/autorizadas y licencias; archivar metadatos y hash original.  
  **Estado:** parcial · **Evidencia:** config/datasets/sources.v2.json + auditoría con SHA; licencias por documento pendientes · **Responsable:** por asignar
- [ ] **SPEC-001/T202** — Crear contrato de manifest, mapeador schema-version, CRS y diccionario de atributos por origen.  
  **Estado:** parcial · **Evidencia:** manifiestos CYME/neutral con parser, reglas e interpretaciones; mapper VNR pendiente · **Responsable:** por asignar
- [ ] **SPEC-001/T203** — Implementar extractores SHP/GeoPackage/ZIP seguros sin inferir terminales por cercanía.  
  **Estado:** pendiente · **Evidencia:** sin extractores SHP/GeoPackage/ZIP · **Responsable:** por asignar
- [ ] **SPEC-001/T204** — Construir pipeline bronze/silver con validación, cuarentena y reportes de rechazo.  
  **Estado:** parcial · **Evidencia:** CYME→snapshot con cuarentena (cyme_ascii.py); bronze Excel spreadsheet.py (sin commit, sesión de plataforma) · **Responsable:** por asignar
- [ ] **SPEC-001/T205** — Agregar pruebas golden para CRS, duplicados, columnas ausentes, unidades y archivos corruptos.  
  **Estado:** parcial · **Evidencia:** tests/unit/test_cyme_ascii_reader.py, test_adapters_evidence.py · **Responsable:** por asignar
- [ ] **SPEC-001/T206** — Exponer import-jobs asíncronos con seguimiento y enlace a snapshot canónico.  
  **Estado:** pendiente · **Evidencia:** importación por CLI; API de redes solo lectura (networks.py) · **Responsable:** por asignar
- [ ] **SPEC-001/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-001/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-001/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-001/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.

## Avance incorporado de la numeración anterior

- [ ] T001-D07: restaurar el VNR-GIS en una base local nueva y ejecutar el adaptador 001 (spec 001). _(antes T029-07)_

## Hallazgos REA aplicables (ADR-0012)

- [x] T001-R01: leer `CUSTOMER LOADS.Phase` con la máscara recuperada (1=A, 2=B, 4=C) y poner en cuarentena códigos fuera de ella; declarar `LOADS.Connection` como regla pendiente de confirmación.
- [ ] T001-R02: leer `LINE CONFIGURATION.Overhead` y verificar `HEADNODES` contra `SOURCE`.
