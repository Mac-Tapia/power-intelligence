# 007 — MADRL multiagente seguro (CityLearn acoplado a red)

**Estado:** propuesta, sin código en el núcleo. El entorno es universal y se instancia por caso de aplicación (spec 029). Hay prototipos en proyectos archivados de otras localidades (Iquitos, Lima), sin integrar; sus datos son solo `method_reference`. Paquete: `power-marl`; entrenamiento en `workers/ml-training`.

## Criterios de aceptación

- AC-007-01: entrena con el dataset gold `district-flex-<case_id>` del caso. El piloto `pe-ica-electrodunas` se construye desde clientes importantes, medidores y exógenas reales de Electro Dunas. Ninguna observación de pronóstico tiene estado `oracle`. Los splits son por años disjuntos.
- AC-007-02: los resultados previos obtenidos con la referencia de Iquitos (pronóstico oráculo) no se citan como resultado del producto. Si se usan para desarrollar métodos, se reportan con oráculo y con pronóstico honesto para cuantificar el sesgo.
- AC-007-03: cada edificio o cliente se asigna a una barra del snapshot del caso de forma explícita. Las violaciones de tensión o cargabilidad que detecte el solver (o el sustituto 006, confirmado) son una restricción o una penalización registrada.
- AC-007-04: hay una línea base basada en reglas (TOU y carga de VE inmediata) y comparaciones con HAPPO, MAPPO, MASAC y MATD3, con al menos 5 semillas e intervalos de confianza.
- AC-007-05: las métricas de flexibilidad, CO2 y costo llevan unidades explícitas y la moneda del caso (`economics.currency`); el factor de emisión es un dato con fuente de la jurisdicción del caso.
- AC-007-06: las políticas son propuestas en sandbox; no hay comandos a SCADA ni a equipos reales.
