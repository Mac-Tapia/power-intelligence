# Tareas 003

- [x] T003-01: unifilar generado desde el snapshot (layout radial, estados abiertos y barras sin tensión diferenciados) en la workstation.
- [ ] T003-02: geometría GIS. Hecho para la fuente CYME: `import-cyme` escribe `<alimentador>.geo.json` (secciones con vértices y nodos, ids = ids eléctricos, CRS del caso; 44 alimentadores, 0 nodos sin coordenadas). La extensión UTM 18S coincide con la concesión (15,3°-12,8° S; 76,3°-73,4° O); la verificación formal del CRS contra los metadatos VNR sigue pendiente. Falta la geometría VNR (`verTramoMT`, depende de 001).
- [ ] T003-03: selección bidireccional GIS ↔ unifilar por identificador persistente del activo.
- [ ] T003-04: mover un ícono del unifilar no cambia la longitud GIS; una edición eléctrica pide confirmación y crea un snapshot nuevo.
- [ ] T003-05: pruebas con un alimentador radial y con una red mallada.
