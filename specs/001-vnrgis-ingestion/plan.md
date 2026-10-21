# Plan candidato — VNR-GIS

1. Catalogar fuentes y licencias, inventariar tablas/campos y CRS por versión (no adivinar esquema).
2. Implementar puerto `RawSourceReader`, adapters por formato, `SchemaMappingRegistry` declarativo.
3. Transformar a nodos/equipos/terminales/fases; registrar procedencia por atributo.
4. Validadores por etapas Bronze / Silver / Gold, con reglas configurables y quarantined records.
5. Contrato de snapshot y hashing inmutable; tests de homomorfismo topológico.
6. Integrar con UI solo cuando el grafo pase las puertas de calidad.

**Riesgo principal:** el VNR-GIS puede describir activos y geometría sin datos mínimos de operación, por lo que su ingesta exitosa no demuestra viabilidad de flujo de carga.
