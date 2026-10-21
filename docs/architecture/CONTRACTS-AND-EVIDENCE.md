# Contratos, evidencias y ownership

## Regla general

Los contratos API/eventos/datos se gestionan por versión en `contracts/`; los esquemas deben incluir unidades, fase, zona/CRS cuando corresponda, y IDs estables. Todo breaking change exige migración, prueba de consumidor y ADR.

## `StudyRun` (borrador V0, no certificado)

El esquema `contracts/schemas/json/study-run.schema.json` define campos mínimos: ID de ejecución, hashes de snapshot y escenario, versión de solver, commit, estado de convergencia y evidencias. Un `StudyRun` con `status=completed` no implica por sí mismo precisión física: comparar valores en las pruebas golden y exigir tolerancias y validación separada.

## Ownership

- SourceAcquisition: ingestión + data quality
- ElectricalTopology: terminales/fases/switches + invariantes
- Study/Simulation: parametrización y solver
- Optimization: objetivo y solución candidata, no aprobación eléctrica
- ScientificML: modelos, entrenamiento y benchmarks fuera de muestra
- AgentOrchestration: planes e interacciones, no escritura directa sobre red original
- EvidenceAndReporting: hash y procedencia de resultados verificados

## Versionado de datos y modelos

`RunManifest = (snapshot_sha256, scenario_sha256, config_sha256, git_commit, engine/version, dataset_manifest, units, seed, convergence, elapsed, input_hashes)`.

El RAW VNR-GIS solo puede pasarse a Silver si se conocen formato y esquema concretos; pasar a Gold exige topología, controles y parámetros trazados (o declarar explícitamente una red parcial no simulable).
