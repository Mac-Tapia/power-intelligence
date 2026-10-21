# Tareas 003

- [x] T003-01: unifilar generado desde el snapshot (layout radial, estados abiertos y barras sin tensión diferenciados) en la workstation.
- [ ] T003-02: geometría GIS. Hecho para la fuente CYME: `import-cyme` escribe `<alimentador>.geo.json` (secciones con vértices y nodos, ids = ids eléctricos, CRS del caso; 44 alimentadores, 0 nodos sin coordenadas). La extensión UTM 18S coincide con la concesión (15,3°-12,8° S; 76,3°-73,4° O); la verificación formal del CRS contra los metadatos VNR sigue pendiente. Falta la geometría VNR (`verTramoMT`, depende de 001).
- [ ] T003-03: selección bidireccional GIS ↔ unifilar por identificador persistente del activo.
- [ ] T003-04: mover un ícono del unifilar no cambia la longitud GIS; una edición eléctrica pide confirmación y crea un snapshot nuevo.
- [ ] T003-05: pruebas con un alimentador radial y con una red mallada.

## Backlog del plan maestro — tareas pendientes

**Gate:** G2 · **Depende de:** SPEC-010, SPEC-004

> **Fuente de verdad:** este `tasks.md`. El índice global de Markdown es generado y debe sincronizarse con el script `scripts/sdd/generate_task_index_md.py`.

- [ ] **SPEC-003/T201** — Definir proyecciones independientes map/unifilar del mismo snapshot con identificadores estables.  
  **Estado:** parcial · **Evidencia:** geo.json con ids eléctricos y unifilar desde snapshot; integración UI pendiente · **Responsable:** por asignar
- [ ] **SPEC-003/T202** — Implementar renderizado GIS con CRS y capa de red por zoom/límites.  
  **Estado:** parcial · **Evidencia:** map.js con CRS declarado; sin zoom ni conexión a la UI · **Responsable:** por asignar
- [ ] **SPEC-003/T203** — Implementar unifilar interactivo por equipos/terminales y layouts persistentes.  
  **Estado:** parcial · **Evidencia:** unifilar SVG automático; sin layouts persistentes · **Responsable:** por asignar
- [ ] **SPEC-003/T204** — Sincronizar selección, inspector de equipos y colores de resultados del solver.  
  **Estado:** parcial · **Evidencia:** UnitesisMap.select y colores; falta cablear con app.js · **Responsable:** por asignar
- [ ] **SPEC-003/T205** — Añadir edición validada por comandos/versionado y restauración de revisión.  
  **Estado:** pendiente · **Evidencia:** sin edición versionada · **Responsable:** por asignar
- [ ] **SPEC-003/T206** — Probar con red radial y mallada, zoom, miles de elementos y fallas de conexión.  
  **Estado:** pendiente · **Evidencia:** sin pruebas de UI con miles de elementos · **Responsable:** por asignar
- [ ] **SPEC-003/T207** — Contracts/negative permission tests  
  **Estado:** parcial · **Evidencia:** pruebas negativas existentes en el área; cobertura incompleta · **Responsable:** por asignar
- [ ] **SPEC-003/T208** — Integration and reproducibility evidence  
  **Estado:** parcial · **Evidencia:** evidencia releída/benchmarks del área · **Responsable:** por asignar
- [ ] **SPEC-003/T209** — Reference and regulatory review  
  **Estado:** pendiente · **Evidencia:** requiere revisión humana de referencias/normativa · **Responsable:** por asignar
- [ ] **SPEC-003/T210** — CI, review and acceptance  
  **Estado:** pendiente · **Evidencia:** CI existe; aceptación humana pendiente · **Responsable:** por asignar

**Política de cierre:** marcar `[x]` únicamente cuando exista evidencia de implementación, pruebas, revisión y aceptación vinculadas a la tarea. Conservar en GitHub el enlace al PR o artefacto verificable.
