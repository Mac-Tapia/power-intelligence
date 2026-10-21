# Tareas 029

- [x] T029-01: inventario de datos de los proyectos archivados e identificación de las fuentes del caso piloto Electro Dunas (Prodma, informe, RECYM, VNR-GIS, DGER).
- [x] T029-02: controles `unitesis_sciml.quality` (oráculo, desfase mensual, índice regular/posicional, cobertura real) con pruebas.
- [x] T029-03: casos de aplicación universales (`config/cases/`, `unitesis_config.cases`) con el piloto `pe-ica-electrodunas` y la plantilla; prueba de universalidad con un caso ficticio a 50 Hz.
- [x] T029-04: registro de fuentes v2 con `case_id` y `role`; auditor por caso; evidencia `datasets/quality/source_audit_pe-ica-electrodunas.json` (5 aprobadas, 7 pendientes de lector, 2 pendientes de restauración, 1 inventariada; Iquitos separado como referencia de método).
- [x] T029-05: autorización confirmada por instrucción explícita del usuario el 21/10/2026, alcance `local_processing_and_training` (sin licencia de publicación); registrada en el caso. Una autorización confirmada debe declarar autoridad, fecha y alcance (validado por `unitesis_config.cases`).
- [ ] T029-06: autorizar lectores (`openpyxl`, `xlrd`, `pyxlsb`) y crear la capa bronze de medidores, líneas y cabeceras.
- [ ] T029-07: restaurar el VNR-GIS en una base local nueva y ejecutar el adaptador 001 (spec 001).
- [ ] T029-08: gold `feeder-load-15min-pe-ica-electrodunas` con exógenas aprobadas y splits cronológicos.
- [ ] T029-09: `pf-scenarios-pe-ica-electrodunas` construido como dataset **candidato** desde la red real TXT (44 alimentadores, 2 173 muestras, manifiesto en `local-data/datasets/`). Pasa a gold cuando se confirme la autorización (T029-05); MDB y VNR se agregan con T001-T011/T003.
- [ ] T029-10: gold `district-flex-pe-ica-electrodunas` desde clientes importantes y medidores reales; pronósticos causales.
- [ ] T029-11: corpus normativo PE con licencia por documento; trazas de herramientas; set de evaluación.
- [x] T029-12: `tests/security/test_no_sensitive_data.py` recorre los archivos versionados (sin `local-data/`, ids reales de clientes CYME, RUC, importes facturados ni correos no permitidos).
